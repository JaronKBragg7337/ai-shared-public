import sys, json
sys.path.insert(0, r'C:\Users\lilli\AI-Shared\tools')
import executor as X
m = X.Mcp()
r = m._rpc({"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}})
for t in r["result"]["tools"]:
    if t["name"] in ("polymarket_cancel_order","polymarket_open_orders","polymarket_modify_order"):
        print(t["name"])
        print(json.dumps(t.get("inputSchema"), indent=2))
        print("---")
orders = m.call("polymarket_open_orders", {})
print("OPEN ORDERS:")
print(json.dumps(orders, indent=2)[:4000])
