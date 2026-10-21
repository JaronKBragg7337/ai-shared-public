import sys, json
sys.path.insert(0, r'C:\Users\lilli\AI-Shared\tools')
import executor as X
m = X.Mcp()
r = m.call("polymarket_cancel_order", {"order_id": "CJPE8WZTJW22", "market_slug": "aec-wta-malrap-gabknu-2026-09-18"})
print(json.dumps(r, indent=2)[:2000])
orders = m.call("polymarket_open_orders", {})
print("REMAINING ORDERS:", json.dumps(orders)[:800])
