import json, sys, subprocess
sys.path.insert(0, r"C:\Users\lilli\AI-Shared\tools")
import executor as X
mcp = X.Mcp()

slugs = [
    "aec-nfl-den-lac-2026-10-11",
    "aec-nfl-det-ari-2026-10-11",
    "aec-nfl-sf-sea-2026-10-11",
]

print("=== POSITIONS ===")
try:
    r = mcp.call("polymarket_positions", {})
    pos = (r or {}).get("positions") or {}
    nz = []
    for k, v in pos.items():
        if not isinstance(v, dict):
            continue
        net = float(v.get("netPositionDecimal") or 0)
        if abs(net) > 0.01:
            nz.append((k, net, v.get("cost"), v.get("currentValue") or v.get("now")))
    print("OPEN_N", len(nz))
    for row in nz[:30]:
        print(row)
except Exception as e:
    print("pos err", type(e).__name__, e)

print("=== BALANCE ===")
for meth in ["polymarket_balance", "polymarket_account", "get_balance", "account"]:
    try:
        r = mcp.call(meth, {})
        print(meth, json.dumps(r)[:500])
    except Exception as e:
        print(meth, "err", type(e).__name__, str(e)[:120])

print("=== BOOKS ===")
for slug in slugs:
    try:
        ask = X.best_ask(mcp, slug)
        print(slug, "best_ask", ask)
    except Exception as e:
        print(slug, "ask err", e)
    try:
        # also bid if available
        if hasattr(X, "best_bid"):
            print(slug, "best_bid", X.best_bid(mcp, slug))
    except Exception as e:
        print(slug, "bid err", e)

print("=== DRY RUNS via desk-trade ===")
for slug in slugs:
    cmd = [sys.executable, r"C:\Users\lilli\AI-Shared\tools\desk-trade.py",
           "--by", "grok-bot/satya-twin", "--slug", slug, "--side", "yes",
           "--size", "5", "--why", "probe", "--kill", "probe", "--dry-run"]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
    out = (r.stdout or "") + (r.stderr or "")
    print(slug)
    print(out[-800:])
