import sys, json
sys.path.insert(0, r'C:\Users\lilli\AI-Shared\tools')
import executor as X
m = X.Mcp()
for slug in ('aec-atp-fabmar-kyrjac-2026-09-27','aec-wta-mayjoi-kimbir-2026-09-27'):
    bid, ask, short = X.best_ask(m, slug)
    print(slug, 'BOOK', bid, ask, short)
orders = m.call('polymarket_open_orders', {})
print('OPEN COUNT', len((orders or {}).get('orders') or []))
for o in (orders or {}).get('orders') or []:
    print(o.get('id'), o.get('marketSlug'), o.get('intent'), o.get('quantity'), o.get('leavesQuantity'), o.get('price'), o.get('state'), 'cum', o.get('cumQuantity'))
# try modify marozsan sell lower to cross
r = m.call('polymarket_modify_order', {'order_id': 'CR9Z4A610YAQ', 'changes': {'price': {'value': '0.01', 'currency': 'USD'}}})
print('MODIFY', json.dumps(r)[:500])
