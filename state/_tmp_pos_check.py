import sys
sys.path.insert(0, r'C:\Users\lilli\AI-Shared\tools')
import importlib
# find how desk-trade imports X
import desk_trade as DT
# Actually just replicate MCP call
import executor as X
mcp = X.Mcp()
pos = mcp.call('polymarket_positions', {})
print('TOP KEYS', list(pos.keys()) if isinstance(pos, dict) else type(pos))
p = pos.get('positions') if isinstance(pos, dict) else None
print('positions type', type(p), 'keys sample', list(p.keys())[:8] if isinstance(p, dict) else p)
slug='aec-cfb-ucla-ore-2026-10-10'
row = (p or {}).get(slug) if isinstance(p, dict) else None
print('ROW', row)
if row is None and isinstance(p, dict) and 'positions' in p:
    print('nested', (p.get('positions') or {}).get(slug))
