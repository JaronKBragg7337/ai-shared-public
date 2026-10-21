import sys, json
sys.path.insert(0, r'C:\Users\lilli\AI-Shared\tools')
import executor as X
m = X.Mcp()
orders = m.call('polymarket_open_orders', {})
print(json.dumps(orders, indent=2)[:5000])
slug = 'aec-atp-huggas-andrub-2026-09-27'
for o in (orders or {}).get('orders') or []:
    if o.get('marketSlug') == slug or slug in str(o):
        oid = o.get('id') or o.get('order_id')
        print('TARGET', oid, o.get('price'), o.get('quantity'), o.get('side') or o.get('intent'))
        if oid:
            r = m.call('polymarket_cancel_order', {'order_id': oid, 'market_slug': slug})
            print('CANCEL', oid, json.dumps(r)[:400])
