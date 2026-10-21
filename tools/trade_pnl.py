"""Average-cost realized P&L helpers for desk_trades fill and resolution rows."""
import collections
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import verifier as X


def market_pnl(rows):
    """Return per-slug metrics; resolution P&L is cumulative, so subtract prior sale P&L."""
    markets = collections.defaultdict(lambda: {
        "fills": 0, "bought": 0.0, "sold": 0.0, "realized_sales": 0.0,
        "settlement": 0.0, "settled_profit": 0.0, "settled": False,
        "open_shares": 0.0, "open_cost": 0.0, "first": None,
        "sales_by_day": collections.defaultdict(float), "settlement_by_day": collections.defaultdict(float),
    })
    inventory = collections.defaultdict(lambda: [0.0, 0.0])  # (slug, side) -> shares, cost basis
    realized = collections.defaultdict(float)
    for r in sorted(rows, key=lambda x: x.get("at") or ""):
        slug = r.get("slug") or "?"
        m = markets[slug]
        if r.get("at"):
            m["first"] = min(filter(None, (m["first"], r["at"][:10])))
        if r.get("kind") == "fill":
            m["fills"] += 1
            side = r.get("side") or "?"
            qty = abs(float(r.get("quantity") or 0))
            amount = abs(float(r.get("cost_usd") or 0))
            shares, basis = inventory[(slug, side)]
            if r.get("action") == "buy":
                inventory[(slug, side)] = [shares + qty, basis + amount]
                m["bought"] += amount
            elif r.get("action") == "sell":
                sold = min(qty, shares)
                allocated = (basis / shares * sold) if shares else 0.0
                inventory[(slug, side)] = [shares - sold, max(0.0, basis - allocated)]
                m["sold"] += amount
                realized[slug] += amount - allocated
                m["realized_sales"] += amount - allocated
                if r.get("at"):
                    m["sales_by_day"][r["at"][:10]] += amount - allocated
        elif r.get("kind") == "resolution":
            m["settled"] = True
            cumulative = float(r.get("pnl_usd") or 0)
            m["settlement"] = cumulative - realized[slug]
            m["settled_profit"] = realized[slug] + m["settlement"]
            if r.get("at"):
                m["settlement_by_day"][r["at"][:10]] += m["settlement"]
            for key in [key for key in inventory if key[0] == slug]:
                inventory[key] = [0.0, 0.0]
    for (slug, _side), (shares, basis) in inventory.items():
        markets[slug]["open_shares"] += shares
        markets[slug]["open_cost"] += basis
    for slug, m in markets.items():
        if not m["settled"]:
            m["settled_profit"] = m["realized_sales"]
    return markets


def account_money(env=None):
    """Latest saved account totals. These are shared-account values, not actor-specific cash."""
    env = env or X.secrets()
    rows = X.sb(env, "GET", "desk_account?select=balance_usd,buying_power,positions,updated_at&id=eq.polymarket-us&limit=1")
    if not rows:
        return None
    row = rows[0]
    positions = row.get("positions") or []
    return {
        "cash": float(row.get("balance_usd") or 0),
        "buying_power": float(row.get("buying_power") or 0),
        "open_value": sum(float(p.get("value") or 0) for p in positions),
        "updated_at": row.get("updated_at"),
    }
