import sys, json
sys.path.insert(0, r"C:\Users\lilli\AI-Shared\tools")
import executor as X
m = X.Mcp()
r = m.call("polymarket_cancel_order", {"order_id": "D1K91PZ9PZ8H", "market_slug": "aec-nfl-ind-pit-2026-10-11"})
print("cancel:", json.dumps(r)[:1000])
bid, ask, short = X.best_ask(m, "aec-nfl-ind-pit-2026-10-11")
print("book", bid, ask, short)
