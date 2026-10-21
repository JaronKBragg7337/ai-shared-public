import urllib.request, json, subprocess, sys

def sb(path):
    u=f'https://site.api.espn.com/apis/site/v2/sports/soccer/{path}/scoreboard'
    return json.load(urllib.request.urlopen(u, timeout=20))

for league, path in [('BUND','ger.1'),('LALIGA','esp.1'),('SERIEA','ita.1')]:
    print('====', league)
    try:
        d=sb(path)
        for e in d.get('events',[]):
            s=e['status']['type']; comp=e['competitions'][0]; teams=comp['competitors']
            home=next(t for t in teams if t['homeAway']=='home')
            away=next(t for t in teams if t['homeAway']=='away')
            print(away['team']['displayName'], away['score'], '-', home['score'], home['team']['displayName'], '|', s.get('detail'), 'state=', s.get('state'))
            ml=(comp.get('odds') or [{}])[0].get('moneyline') if comp.get('odds') else None
            if ml:
                print('  ML home', ml.get('home',{}).get('current'), 'away', ml.get('away',{}).get('current'), 'draw', ml.get('draw',{}).get('current'))
    except Exception as ex:
        print('err', ex)

print('====BOOKS====')
for slug in ['atc-bun-aug-fcb-2026-10-10-fcb','atc-lal-ala-atm-2026-10-10-atm','atc-epl-sun-bha-2026-10-10-bha','atc-epl-ast-bre-2026-10-10-bre','atc-bun-hof-hsv-2026-10-10-hof','atc-bun-mai-lev-2026-10-10-lev']:
    r=subprocess.run([sys.executable, r'C:\Users\lilli\AI-Shared\tools\desk.py','book',slug], capture_output=True, text=True, timeout=45)
    print(slug)
    print((r.stdout or '')[:500])
    if r.stderr: print('err', r.stderr[:200])
