import urllib.request, json, subprocess, sys
from pathlib import Path

def get(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    return json.loads(urllib.request.urlopen(req, timeout=25).read().decode())

# WSU / Utah State search
print('=== WSU/USU search ===')
for groups in ['80', '81']:
    try:
        sb = get(f'https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?groups={groups}&limit=300')
        for e in sb.get('events', []):
            name = (e.get('name') or '') + (e.get('shortName') or '')
            if 'Washington State' in name or 'Utah State' in name or 'Wash St' in name:
                st = e.get('status', {}).get('type', {})
                comps = e.get('competitions', [{}])[0]
                teams = comps.get('competitors', [])
                parts = [f"{t.get('team',{}).get('abbreviation')} {t.get('score')}" for t in sorted(teams, key=lambda x: x.get('homeAway'))]
                print(groups, e.get('shortName'), st.get('description'), st.get('detail'), '|', ' - '.join(parts), 'id', e.get('id'))
    except Exception as ex:
        print('err', groups, ex)

# date-specific
print('=== scoreboard dates ===')
for d in ['20261009', '20261010']:
    try:
        sb = get(f'https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?dates={d}')
        for e in sb.get('events', []):
            name = e.get('name') or ''
            if 'Washington State' in name or 'Utah State' in name:
                st = e.get('status', {}).get('type', {})
                comps = e.get('competitions', [{}])[0]
                teams = comps.get('competitors', [])
                parts = [f"{t.get('team',{}).get('abbreviation')} {t.get('score')}" for t in sorted(teams, key=lambda x: x.get('homeAway'))]
                print(d, e.get('shortName'), st.get('description'), st.get('detail'), '|', ' - '.join(parts))
                eid = e.get('id')
                try:
                    wp = get(f'https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event={eid}')
                    wps = wp.get('winprobability') or []
                    if wps:
                        print('  WP', wps[-1].get('homeWinPercentage'), 'home=', [t.get('team',{}).get('abbreviation') for t in wp.get('header',{}).get('competitions',[{}])[0].get('competitors',[]) if t.get('homeAway')=='home'])
                except Exception as ex:
                    print('  wp err', ex)
    except Exception as ex:
        print('date err', d, ex)

# Liga MX / soccer
print('=== soccer try ===')
for path in [
    'https://site.api.espn.com/apis/site/v2/sports/soccer/mex.1/scoreboard',
    'https://site.api.espn.com/apis/site/v2/sports/soccer/mex.1/scoreboard?dates=20261009',
    'https://site.api.espn.com/apis/site/v2/sports/soccer/mex.1/scoreboard?dates=20261010',
]:
    try:
        sb = get(path)
        for e in sb.get('events', []):
            name = e.get('name') or ''
            if 'Tigre' in name or 'Toluca' in name or 'UANL' in name:
                st = e.get('status', {}).get('type', {})
                comps = e.get('competitions', [{}])[0]
                teams = comps.get('competitors', [])
                parts = [f"{t.get('team',{}).get('displayName')} {t.get('score')}" for t in sorted(teams, key=lambda x: x.get('homeAway'))]
                print(path.split('scoreboard')[0][-20:], e.get('shortName'), st.get('description'), st.get('detail'), '|', ' - '.join(parts))
    except Exception as ex:
        print('soccer err', ex)

# list desk tools for account
tools = Path(r'C:\Users\lilli\AI-Shared\tools')
print('=== tools ===')
for p in sorted(tools.glob('*')):
    if p.is_file() and any(k in p.name.lower() for k in ('desk','account','poly','trade','live')):
        print(p.name)
