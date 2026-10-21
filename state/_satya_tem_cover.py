import sys, json
sys.path.insert(0, r"C:\Users\lilli\AI-Shared\tools")
import executor as X
from datetime import datetime

m = X.Mcp()
slug = "aec-cfb-templ-sfl-2026-10-03"
for o in (m.call("polymarket_open_orders", {}) or {}).get("orders") or []:
    if o.get("marketSlug") == slug:
        oid = o["id"]
        r = m.call("polymarket_cancel_order", {"order_id": oid, "market_slug": slug})
        print("CANCEL", oid, json.dumps(r)[:200])

order = {
    "marketSlug": slug,
    "intent": "ORDER_INTENT_SELL_SHORT",
    "type": "ORDER_TYPE_LIMIT",
    "price": {"value": "0.61", "currency": "USD"},
    "quantity": "13.70",
    "tif": "TIME_IN_FORCE_GOOD_TILL_CANCEL",
}
result = m.call("polymarket_place_order", {"order": order})
print("PLACE", json.dumps(result)[:500])
line = (
    f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] #manual grok-bot/satya-twin "
    f"EXIT NO {slug} 13.70sh @0.61 -> PLACED {json.dumps(result)[:120]} "
    f"| why: KILL TEM leads; desk-trade .2f rounded ask under; cover at 0.61\n"
)
with open(r"C:\Users\lilli\AI-Shared\state\desk-trade.md", "a", encoding="utf-8") as fh:
    fh.write(line)
print("logged")
