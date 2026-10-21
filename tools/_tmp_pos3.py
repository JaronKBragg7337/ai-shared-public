import json, subprocess, sys
raw = subprocess.check_output([sys.executable, r'C:\Users\lilli\AI-Shared\tools\desk.py', 'account', '--json'], text=True)
if raw.startswith('\ufeff'):
    raw = raw[1:]
d = json.loads(raw)
pos = d.get('positions')
print(type(pos))
if isinstance(pos, dict):
    print('pos keys', pos.keys())
    for k,v in pos.items():
        print(' sub', k, type(v), (len(v) if hasattr(v,'__len__') and not isinstance(v,str) else ''))
        if k == 'positions' and isinstance(v, list):
            for i,p in enumerate(v):
                print('  item', i, type(p))
                if isinstance(p, dict):
                    meta = p.get('marketMetadata')
                    print('   net', p.get('netPosition'), 'sold', p.get('qtySold'), 'bought', p.get('qtyBought'), 'now', p.get('cashValue'), 'avg', p.get('avgPx'))
                    print('   meta type', type(meta))
                    if isinstance(meta, dict):
                        print('   meta keys', list(meta.keys())[:30])
                        print('   meta snippet', json.dumps(meta, default=str)[:500])
                else:
                    print('   raw', repr(p)[:200])
