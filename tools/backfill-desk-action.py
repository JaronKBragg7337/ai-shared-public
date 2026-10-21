"""Backfill fill direction from the recent Polymarket US activity page (read-only venue)."""
import sys
import re
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, __import__("os").path.dirname(__file__))
import verifier as X

env = X.secrets()
mcp = X.Mcp()
activities = mcp.call("polymarket_activities", {"limit": 100}).get("activities") or []
actions_by_order = {}
actions_by_trade = {}
times = []
for a in activities:
    if a.get("type") != "ACTIVITY_TYPE_TRADE":
        continue
    tr = a.get("trade") or {}
    times.extend(e.get("transactTime") for e in (tr.get("aggressorExecution"), tr.get("passiveExecution"))
                 if e and e.get("transactTime"))
    for ex in (tr.get("aggressorExecution"), tr.get("passiveExecution")):
        if not ex:
            continue
        o = ex.get("order") or {}
        act = o.get("action")
        act = "buy" if act == "ORDER_ACTION_BUY" else "sell" if act == "ORDER_ACTION_SELL" else None
        if not act:
            intent = o.get("intent")
            act = "buy" if intent in ("ORDER_INTENT_BUY_LONG", "ORDER_INTENT_BUY_SHORT") else \
                  "sell" if intent in ("ORDER_INTENT_SELL_LONG", "ORDER_INTENT_SELL_SHORT") else None
        if act:
            if o.get("id"):
                actions_by_order[o["id"]] = act
            actions_by_trade.setdefault(tr.get("id"), set()).add(act)

fills = X.sb(env, "GET", "desk_trades?select=id,order_id,action,note,price,quantity,cost_usd&kind=eq.fill&limit=10000")
by_action = {"buy": [], "sell": []}
feed_matched = 0
note_fallback = 0
for row in fills:
    action = actions_by_order.get(row.get("order_id"))
    possible = actions_by_trade.get(row["id"], set())
    if not action and len(possible) == 1:
        action = next(iter(possible))
    if action:
        feed_matched += 1
    if not action:
        note = row.get("note") or ""
        if "ORDER_INTENT_BUY_LONG" in note or "ORDER_INTENT_BUY_SHORT" in note:
            action = "buy"
        elif "ORDER_INTENT_SELL_LONG" in note or "ORDER_INTENT_SELL_SHORT" in note:
            action = "sell"
        if action:
            note_fallback += 1
    if action and row.get("action") != action:
        by_action[action].append(row["id"])
matched = 0
for action, ids in by_action.items():
    for start in range(0, len(ids), 100):
        batch = ids[start:start + 100]
        X.sb(env, "PATCH", f"desk_trades?id=in.({','.join(batch)})", {"action": action})
        matched += len(batch)

# Old verifier rows added a positive sell commission to proceeds instead of deducting it.
# Price is stored in the contract's outcome scale; note retains the collected fee.
sell_fixes = []
for row in fills:
    action = actions_by_order.get(row.get("order_id"))
    possible = actions_by_trade.get(row["id"], set())
    if not action and len(possible) == 1:
        action = next(iter(possible))
    if not action:
        note = row.get("note") or ""
        action = "buy" if "ORDER_INTENT_BUY_" in note else "sell" if "ORDER_INTENT_SELL_" in note else None
    if action != "sell" or row.get("price") is None or row.get("quantity") is None:
        continue
    fee_match = re.search(r"\bfee\s+(-?\d+(?:\.\d+)?)", row.get("note") or "")
    fee = float(fee_match.group(1)) if fee_match else 0.0
    correct = round(float(row["price"]) * float(row["quantity"]) - fee, 4)
    if abs(correct - float(row.get("cost_usd") or 0)) > 0.0001:
        sell_fixes.append((row["id"], correct))
def patch_cost(item):
    X.sb(env, "PATCH", f"desk_trades?id=eq.{item[0]}", {"cost_usd": item[1]})
with ThreadPoolExecutor(max_workers=8) as pool:
    list(pool.map(patch_cost, sell_fixes))
def inferred(row):
    if actions_by_order.get(row.get("order_id")) or len(actions_by_trade.get(row["id"], set())) == 1 or row.get("action"):
        return True
    note = row.get("note") or ""
    return any(x in note for x in ("ORDER_INTENT_BUY_LONG", "ORDER_INTENT_BUY_SHORT",
                                   "ORDER_INTENT_SELL_LONG", "ORDER_INTENT_SELL_SHORT"))
unknown = sum(1 for row in fills if not inferred(row))
print(f"activity_page={len(activities)} trades={len(actions_by_trade)} oldest_trade={min(times) if times else 'none'}")
print(f"feed_matched_rows={feed_matched}; intent_note_fallback={note_fallback}; action_rows_changed={matched}; corrected_sell_proceeds={len(sell_fixes)}")
print(f"total_rows={len(fills)}; action_unknown={unknown}")
