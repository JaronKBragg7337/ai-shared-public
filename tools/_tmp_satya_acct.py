import json, os, sys
ROOT = r'C:\Users\lilli\AI-Shared\tools'
sys.path.insert(0, ROOT)
import executor as X
mcp = X.Mcp()
b = mcp.call('polymarket_account_balances', {})
print('BALANCES', json.dumps(b, indent=2)[:2000])
pm = mcp.call('polymarket_positions', {})
pos = pm.get('positions') or {}
print('POSITION_COUNT', len(pos))
for slug, p in sorted(pos.items()):
    net = p.get('netPositionDecimal')
    cost = (p.get('cost') or {}).get('value')
    if abs(float(net or 0)) < 0.01 and abs(float(cost or 0)) < 0.01:
        continue
    print(json.dumps({'slug': slug, 'net': net, 'cost': cost, 'side_hint': 'YES' if float(net or 0) > 0 else 'NO'}))
