#!/usr/bin/env python3
import sys, json
sys.path.insert(0, r"C:\Users\lilli\AI-Shared\tools")
import executor as X
m = X.Mcp()
orders = m.call("polymarket_open_orders", {})
print(json.dumps(orders, indent=2)[:5000])
