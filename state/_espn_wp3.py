import json, urllib.request

def get(u):
    r = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
    return json.load(urllib.request.urlopen(r, timeout=25))

for gid, lab in [('401869842', 'ARMY-LT'), ('401856821', 'TTU-COLO')]:
    d = get(f'https://site.web.api.espn.com/apis/site/v2/sports/football/college-football/summary?event={gid}')
    wp = d.get('winprobability', [])
    hdr = d['header']['competitions'][0]
    teams = ','.join(f"{t['team']['abbreviation']}{t.get('score','')}" for t in hdr['competitors'])
    print(lab, hdr['status']['type']['detail'], teams, 'homeWP', wp[-1] if wp else None)

print('---OTHER---')
d = get('https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?dates=20261003&limit=300')
for e in d.get('events', []):
    n = e.get('name', '')
    if any(x in n for x in ('Temple', 'South Florida', 'Georgia Southern', 'Coastal Carolina', 'UTSA', 'Rice')):
        c = e['competitions'][0]
        st = c['status']['type']
        teams = ' / '.join(f"{t['team']['abbreviation']} {t.get('score','')}" for t in c['competitors'])
        print(e.get('shortName'), st.get('detail'), teams, e.get('id'), 'done', st.get('completed'))
