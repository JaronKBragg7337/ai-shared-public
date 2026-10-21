import sys, json
sys.path.insert(0, r'C:\Users\lilli\AI-Shared\tools')
import executor as X
m = X.Mcp()
r = m._rpc({"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}})
names = [t["name"] for t in r["result"]["tools"]]
print("\n".join(names))
