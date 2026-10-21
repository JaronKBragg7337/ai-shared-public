import sys, os, json
sys.path.insert(0, r'C:\Users\lilli\AI-Shared\tools')
import executor as X
mcp = X.Mcp()
b = mcp.call('polymarket_account_balances', {})
print('BALANCES', json.dumps(b)[:1500])
pm = mcp.call('polymarket_positions', {})
pos = pm.get('positions') or {}
print('N', len(pos))
for slug, p in pos.items():
    cost = (p.get('cost') or {}).get('value')
    mv = p.get('marketValue') or p.get('mark') or {}
    if isinstance(mv, dict):
        mv = mv.get('value')
    net = p.get('netPositionDecimal')
    if abs(float(net or 0)) < 0.01 and abs(float(cost or 0)) < 0.01:
        continue
    print(json.dumps({'slug': slug, 'net': net, 'cost': cost, 'mv': mv}, default=str))
