import urllib.request, json, subprocess, sys

def get(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    return json.loads(urllib.request.urlopen(req, timeout=25).read().decode())

eid = '401872989'
sb = get('https://site.api.espn.com/apis/site/v2/sports/football/nfl/summary?event=' + eid)
wps = sb.get('winprobability') or []
last = wps[-1] if wps else {}
hwp = float(last.get('homeWinPercentage') or 0)  # LAC
dwp = 1.0 - hwp
h = sb['header']['competitions'][0]
detail = h['status']['type'].get('detail')
scores = {}
for c in h['competitors']:
    scores[c['team']['abbreviation']] = c.get('score')
print('status', detail, scores, 'LAC_WP', round(hwp,4), 'DEN_WP', round(dwp,4))

sys.path.insert(0, r'C:\Users\lilli\AI-Shared\tools')
import executor as X
mcp = X.Mcp()
slug = 'aec-nfl-den-lac-2026-10-11'
bid, ask, short = X.best_ask(mcp, slug)
print('book', bid, ask, 'short', short)

# Edge: market prices DEN ~ask, ESPN DEN WP lower -> buy NO (Chargers)
no_cost = 1.0 - float(bid)
edge = hwp - no_cost
print('no_cost', round(no_cost,4), 'edge_vs_LAC_WP', round(edge,4))
if edge < 0.06:
    print('SKIP thin edge', edge)
    sys.exit(2)

why = (
    f"DEN{scores.get('DEN')}-LAC{scores.get('LAC')} {detail}; ESPN LAC WP{hwp*100:.1f} vs Broncos bid{bid:.3f} "
    f"(NO~{no_cost:.2f}) ~{edge*100:.0f}c; market rich on leading DEN"
)
kill = 'ESPN LAC WP under 0.20 or DEN extends lead another score'
cmd = [
    sys.executable,
    r'C:\Users\lilli\AI-Shared\tools\desk-trade.py',
    '--by', 'grok-bot/satya-twin',
    '--slug', slug,
    '--side', 'no',
    '--size', '5',
    '--why', why,
    '--kill', kill,
]
print('LIVE PLACE', why)
r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
print(r.stdout)
print(r.stderr)
sys.exit(r.returncode)
