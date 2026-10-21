import sys, json
sys.path.insert(0, r"C:\Users\lilli\AI-Shared\tools")
import executor as X
m = X.Mcp()
r = m.call("polymarket_cancel_order", {"order_id": "D0ZE3KR68Z8H", "market_slug": "aec-cfb-ncar-pitt-2026-10-10"})
print(json.dumps(r, indent=2)[:3000])
