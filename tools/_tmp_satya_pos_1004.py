import json, sys
sys.path.insert(0, r"C:\Users\lilli\AI-Shared\tools")
import executor as X
mcp = X.Mcp()
slug = "aec-nfl-ind-was-2026-10-04"
try:
    r = mcp.call("polymarket_positions", {})
    pos = (r or {}).get("positions") or {}
    print("HELD", json.dumps(pos.get(slug), indent=2)[:1000] if slug in pos else "none")
    nz = []
    for k, v in pos.items():
        if not isinstance(v, dict):
            continue
        net = float(v.get("netPositionDecimal") or 0)
        if abs(net) > 0.01:
            nz.append((k, net, v.get("cost")))
    print("OPEN_N", len(nz))
    for row in nz[:20]:
        print(row)
except Exception as e:
    print("pos err", type(e).__name__, e)
try:
    print("BOOK", X.best_ask(mcp, slug))
except Exception as e:
    print("book err", e)
