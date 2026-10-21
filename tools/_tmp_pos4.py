import json, subprocess, sys
raw = subprocess.check_output([sys.executable, r'C:\Users\lilli\AI-Shared\tools\desk.py', 'account', '--json'], text=True)
if raw.startswith('\ufeff'):
    raw = raw[1:]
d = json.loads(raw)
pos = d['positions']['positions']
print('n', len(pos), 'type', type(pos))
for k,p in pos.items():
    print('=== key', k)
    if not isinstance(p, dict):
        print(type(p), repr(p)[:200]); continue
    meta = p.get('marketMetadata') or {}
    print('net', p.get('netPosition'), 'avail', p.get('qtyAvailable'), 'bought', p.get('qtyBought'), 'sold', p.get('qtySold'))
    print('avg', p.get('avgPx'), 'cost', p.get('cost'), 'now', p.get('cashValue'), 'realized', p.get('realized'))
    print('meta', json.dumps(meta, default=str)[:600])
