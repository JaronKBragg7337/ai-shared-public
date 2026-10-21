import urllib.request, json, subprocess, sys

req = urllib.request.Request(
    'https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event=401858245',
    headers={'User-Agent': 'Mozilla/5.0'},
)
with urllib.request.urlopen(req, timeout=20) as r:
    s = json.load(r)
wp = s.get('winprobability')[-1]
h = s['header']['competitions'][0]
print('status', h['status']['type'].get('detail'))
for c in h['competitors']:
    print(c['team']['abbreviation'], c.get('score'))
pitt_wp = 1 - float(wp.get('homeWinPercentage', 0))
print('homeWinPct VT', wp.get('homeWinPercentage'), 'pittWP', round(pitt_wp, 4))

why = (
    f"ESPN PITT 7 VT 14 End 1st; VT homeWP {float(wp.get('homeWinPercentage')):.2f} so Pitt WP~{pitt_wp:.0%} "
    f"vs Panthers ask~0.28 (~5c cheap on early 7-pt trail vs near-pickem)"
)
kill = 'VT lead 14+ or ESPN Pitt WP under 0.20'
cmd = [
    sys.executable,
    r'C:\Users\lilli\AI-Shared\tools\desk-trade.py',
    '--by', 'grok-bot/satya-twin',
    '--slug', 'aec-cfb-pitt-vtech-2026-10-02',
    '--side', 'yes',
    '--size', '5',
    '--why', why,
    '--kill', kill,
]
print('LIVE PLACE')
r = subprocess.run(cmd, capture_output=True, text=True)
print(r.stdout)
print(r.stderr)
sys.exit(r.returncode)
