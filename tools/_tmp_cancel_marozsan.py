import sys, json
sys.path.insert(0, r'C:\Users\lilli\AI-Shared\tools')
import executor as X
m = X.Mcp()
slug = 'aec-atp-fabmar-kyrjac-2026-09-27'
for oid in ('CR9MP9JY6YCC', 'CR9YWHG56YCA'):
    r = m.call('polymarket_cancel_order', {'order_id': oid, 'market_slug': slug})
    print('CANCEL', oid, json.dumps(r)[:300])
bid, ask, short = X.best_ask(m, slug)
print('BOOK', bid, ask, short)
orders = m.call('polymarket_open_orders', {})
print('REMAINING', len((orders or {}).get('orders') or []))
for o in (orders or {}).get('orders') or []:
    if o.get('marketSlug') == slug:
        print('STILL', o.get('id'), o.get('quantity'), o.get('price'))
