import sys, json
sys.path.insert(0, r"C:\Users\lilli\AI-Shared\tools")
import executor as X
m = X.Mcp()
oid = "D0ZE3KR68Z8H"
print("CANCEL", oid)
try:
    r = m.call("polymarket_cancel_order", {"orderId": oid})
    print(json.dumps(r, indent=2)[:2000])
except Exception as e:
    print("ERR orderId", e)
    try:
        r = m.call("polymarket_cancel_order", {"id": oid})
        print(json.dumps(r, indent=2)[:2000])
    except Exception as e2:
        print("ERR id", e2)
