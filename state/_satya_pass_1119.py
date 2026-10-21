import urllib.request, json

def get(u):
    return json.load(urllib.request.urlopen(u, timeout=20))

print('====EPL NOW====')
d=get('https://site.api.espn.com/apis/site/v2/sports/soccer/eng.1/scoreboard')
for e in d.get('events',[]):
    s=e['status']['type']; comp=e['competitions'][0]; teams=comp['competitors']
    home=next(t for t in teams if t['homeAway']=='home')
    away=next(t for t in teams if t['homeAway']=='away')
    if s.get('state')!='in' and 'Brighton' not in e['name'] and 'Brentford' not in e['name'] and 'Chelsea' not in e['name'] and 'Fulham' not in e['name']:
        continue
    print(e['name'], '|', away['score'], '-', home['score'], '|', s.get('detail'), s.get('state'))
    ml=(comp.get('odds') or [None])[0]
    if ml and ml.get('moneyline'):
        m=ml['moneyline']
        def odd(side):
            c=(m.get(side) or {}).get('current') or {}
            return c.get('odds')
        print('  ML home', odd('home'), 'away', odd('away'), 'draw', odd('draw'))

print('====ATM search====')
for path in ['esp.1','esp.2','uefa.champions','uefa.europa']:
    try:
        d=get(f'https://site.api.espn.com/apis/site/v2/sports/soccer/{path}/scoreboard')
        for e in d.get('events',[]):
            if 'Atletico' in e['name'] or 'Madrid' in e['name'] or 'Alaves' in e['name'] or 'Alav' in e['name']:
                s=e['status']['type']; comp=e['competitions'][0]; teams=comp['competitors']
                home=next(t for t in teams if t['homeAway']=='home')
                away=next(t for t in teams if t['homeAway']=='away')
                print(path, e['name'], '|', away['score'], '-', home['score'], '|', s.get('detail'), s.get('state'))
    except Exception as ex:
        print(path, 'err', ex)

# also market detail
print('====MARKET ATM====')
import subprocess,sys
r=subprocess.run([sys.executable,r'C:\Users\lilli\AI-Shared\tools\desk.py','market','atc-lal-ala-atm-2026-10-10-atm'],capture_output=True,text=True,timeout=45)
print((r.stdout or '')[:1200])
