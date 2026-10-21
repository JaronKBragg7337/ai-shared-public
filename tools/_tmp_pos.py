import json, subprocess, sys
raw = subprocess.check_output([sys.executable, r'C:\Users\lilli\AI-Shared\tools\desk.py', 'account', '--json'], text=True)
# strip BOM if any
if raw.startswith('\ufeff'):
    raw = raw[1:]
d = json.loads(raw)
print('available', d.get('balances'))
pos = d.get('positions') or {}
if isinstance(pos, dict):
    items = pos.get('positions') or pos.get('items') or pos
    if isinstance(items, dict):
        items = items.get('positions') or list(items.values())
else:
    items = pos
print('positions type', type(pos), 'items type', type(items))
if isinstance(items, list):
    for p in items:
        m = (p.get('market') or {})
        slug = m.get('slug') or p.get('slug')
        print(json.dumps({
            'slug': slug,
            'title': (m.get('title') or m.get('question') or '')[:60],
            'outcome': (p.get('outcome') or {}).get('name') if isinstance(p.get('outcome'), dict) else p.get('outcome'),
            'side': p.get('side') or p.get('positionSide'),
            'qty': p.get('quantity') or p.get('qty') or p.get('shares'),
            'avg': p.get('avgPx') or p.get('averagePrice'),
            'cost': p.get('cost'),
            'cashValue': p.get('cashValue'),
            'keys': list(p.keys())[:20],
        }, default=str))
elif isinstance(items, dict):
    print(json.dumps(items, indent=2, default=str)[:3000])
else:
    print(repr(items)[:2000])
oo = d.get('open_orders') or {}
print('open_orders keys', list(oo.keys()) if isinstance(oo, dict) else type(oo))
