import sys, json
sys.path.insert(0, r'C:\Users\lilli\AI-Shared\tools')
import executor as X
m = X.Mcp()
slug = 'aec-atp-fabmar-kyrjac-2026-09-27'
r = m.call('polymarket_cancel_order', {'order_id': 'CR9Z4A610YAQ', 'market_slug': slug})
print('CANCEL', json.dumps(r)[:200])
# aggressive flatten: sell 9.26 at 0.01 (below bid) so it takes
order = {
  'marketSlug': slug,
  'intent': 'ORDER_INTENT_SELL_LONG',
  'type': 'ORDER_TYPE_LIMIT',
  'price': {'value': '0.01', 'currency': 'USD'},
  'quantity': '9.26',
  'tif': 'TIME_IN_FORCE_GOOD_TILL_CANCEL',
}
res = m.call('polymarket_place_order', {'order': order})
print('PLACE', json.dumps(res)[:600])
orders = m.call('polymarket_open_orders', {})
for o in (orders or {}).get('orders') or []:
    if o.get('marketSlug') == slug:
        print('OPEN', o.get('id'), o.get('quantity'), o.get('leavesQuantity'), o.get('price'), o.get('cumQuantity'), o.get('state'))
