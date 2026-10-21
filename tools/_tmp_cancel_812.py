import sys, json
sys.path.insert(0, r'C:\Users\lilli\AI-Shared\tools')
import executor as X
m = X.Mcp()
oid = 'CRTXKF97PYB5'
slug = 'aec-nfl-lar-den-2026-09-27'
print('CANCEL', oid, slug)
r = m.call('polymarket_cancel_order', {'order_id': oid, 'market_slug': slug})
print(json.dumps(r, indent=2)[:3000])
