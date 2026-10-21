#!/usr/bin/env python3
import sys, json
sys.path.insert(0, r"C:\Users\lilli\AI-Shared\tools")
import executor as X
m = X.Mcp()
oid = "CRP8PQ7TGYC6"
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
        # discover schema
        lst = m._rpc({"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}})
        for t in lst["result"]["tools"]:
            if t["name"] == "polymarket_cancel_order":
                print(json.dumps(t.get("inputSchema"), indent=2))
