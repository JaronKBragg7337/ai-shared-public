#!/usr/bin/env python3
import sys, json
sys.path.insert(0, r"C:\Users\lilli\AI-Shared\tools")
import executor as X
m = X.Mcp()
r = m.call("polymarket_cancel_order", {
    "order_id": "CRP8PQ7TGYC6",
    "market_slug": "aec-nfl-lv-no-2026-09-27",
})
print(json.dumps(r, indent=2)[:2000])
