import sys, json
sys.path.insert(0, r"C:\Users\lilli\AI-Shared\tools")
import executor as X
m = X.Mcp()
# list tools if available
for name in ["polymarket_cancel_order","polymarket_cancel_orders","polymarket_open_orders","cancel_order"]:
    try:
        r = m.call(name, {})
        print(name, ":", json.dumps(r)[:800])
    except Exception as e:
        print(name, "ERR", e)
