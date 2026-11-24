"""Jaron's manual Polymarket trades, kept separate from bot actors."""
import collections, sys, os
sys.path.insert(0, os.path.dirname(__file__))
import verifier as X
import trade_pnl as P

kw = (sys.argv[1] if len(sys.argv) > 1 else "").lower()
def sb_all(env, q):   # verifier has no paged reader; page 1000 at a time
    out, off = [], 0
    while True:
        r = X.sb(env, "GET", f"{q}&order=at.asc&limit=1000&offset={off}") or []
        out += r; off += 1000
        if len(r) < 1000: return out
rows = sb_all(X.secrets(), "desk_trades?select=kind,action,cost_usd,pnl_usd,at,slug,side,quantity&actor=eq.jaron-manual")
markets = P.market_pnl([r for r in rows if r.get("kind") in ("fill", "resolution") and
                        (not kw or kw in (r.get("slug") or "").lower())])

def cat(slug):
    s = slug or ""
    for k, name in (("btc", "bitcoin"), ("-nfl-", "nfl"), ("-cfb-", "college football"), ("-mlb-", "mlb"),
                    ("-nhl-", "nhl"), ("-wnba-", "wnba"), ("-wta-", "tennis"), ("-atp-", "tennis"), ("-ufc-", "ufc")):
        if k in s: return name
    return "other"

def fmt(v): return f"{'+' if v >= 0 else '-'}${abs(v):.2f}"

if kw:
    print("| market | first | fills | buys | sells | sale realized | settlement P&L | open cost |")
    print("|---|---|---:|---:|---:|---:|---:|---:|")
    for slug, m in sorted(markets.items(), key=lambda x: x[1]["first"] or ""):
        print(f"| {slug} | {m['first']} | {m['fills']} | ${m['bought']:.2f} | ${m['sold']:.2f} | {fmt(m['realized_sales'])} | {fmt(m['settlement']) if m['settled'] else 'open'} | ${m['open_cost']:.2f} |")

C = collections.defaultdict(lambda: [0, 0, 0.0, 0.0, 0.0])
for slug, m in markets.items():
    c = C[cat(slug)]; c[0] += 1; c[1] += m["settled"]
    c[2] += m["realized_sales"]; c[3] += m["settlement"]; c[4] += m["open_cost"]
print("\n| category | markets | settled | sale realized | settlement P&L | open cost |")
print("|---|---:|---:|---:|---:|---:|")
for k, c in sorted(C.items(), key=lambda x: x[1][2] + x[1][3]):
    print(f"| {k} | {c[0]} | {c[1]} | {fmt(c[2])} | {fmt(c[3])} | ${c[4]:.2f} |")
sales = sum(m["realized_sales"] for m in markets.values())
settlement = sum(m["settlement"] for m in markets.values())
money = P.account_money()
print(f"\nMoney: settled profit {fmt(sales + settlement)} (sale realized {fmt(sales)} + settlement P&L {fmt(settlement)}).")
if money:
    print(f"Open value ${money['open_value']:.2f}; cash ${money['cash']:.2f}; buying power ${money['buying_power']:.2f} (shared account snapshot {money['updated_at']}).")
else:
    print("Open value and cash unavailable: no saved account snapshot.")
print("Open value and cash are whole-account figures; only profit above is actor-filtered to jaron-manual.")
