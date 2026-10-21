import urllib.request, json

def get(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    return json.loads(urllib.request.urlopen(req, timeout=25).read().decode())

# refresh scores
sb = get('https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?groups=80')
for e in sb.get('events', []):
    name = e.get('name') or ''
    if 'BYU' in name or 'Iowa State' in name or 'Washington State' in name or 'Utah State' in name:
        st = e.get('status', {}).get('type', {})
        comps = e.get('competitions', [{}])[0]
        teams = comps.get('competitors', [])
        parts = [f"{t.get('team',{}).get('abbreviation')} {t.get('score')}" for t in sorted(teams, key=lambda x: x.get('homeAway'))]
        print(e.get('shortName'), st.get('description'), st.get('detail'), '|', ' - '.join(parts), 'id', e.get('id'))
        eid = e.get('id')
        wp = get(f'https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event={eid}')
        wps = wp.get('winprobability') or []
        if wps:
            print('  homeWP', wps[-1].get('homeWinPercentage'))

soc = get('https://site.api.espn.com/apis/site/v2/sports/soccer/mex.1/scoreboard')
for e in soc.get('events', []):
    name = e.get('name') or ''
    if 'Tigre' in name or 'Toluca' in name or 'UANL' in name:
        st = e.get('status', {}).get('type', {})
        comps = e.get('competitions', [{}])[0]
        teams = comps.get('competitors', [])
        parts = [f"{t.get('team',{}).get('displayName')} {t.get('score')}" for t in sorted(teams, key=lambda x: x.get('homeAway'))]
        print('SOCCER', e.get('shortName'), st.get('description'), st.get('detail'), st.get('state'), '|', ' - '.join(parts))
