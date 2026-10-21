import json, subprocess, sys
raw = subprocess.check_output([sys.executable, r'C:\Users\lilli\AI-Shared\tools\desk.py', 'account', '--json'], text=True)
if raw.startswith('\ufeff'):
    raw = raw[1:]
d = json.loads(raw)
pos = d.get('positions') or {}
items = pos.get('positions') if isinstance(pos, dict) else pos
for p in items:
    meta = p.get('marketMetadata') or {}
    event = meta.get('event') or {}
    mkt = meta.get('market') or meta
    slug = mkt.get('slug') or event.get('slug') or meta.get('slug')
    print('---')
    print('slug', slug)
    print('name', mkt.get('name') or mkt.get('question') or event.get('name'))
    print('net', p.get('netPosition'), 'avail', p.get('qtyAvailable'), 'bought', p.get('qtyBought'), 'sold', p.get('qtySold'))
    print('avg', p.get('avgPx'), 'cost', p.get('cost'), 'now', p.get('cashValue'), 'realized', p.get('realized'))
    print('outcome', meta.get('outcome') or mkt.get('outcome') or meta.get('outcomes'))
