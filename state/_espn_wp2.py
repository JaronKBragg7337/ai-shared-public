import json, os, urllib.request

def get(url):
    req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.load(r)

# winprobability endpoint
for gid, label in [('401856821','TTU-COLO'),('401856818','BYU-TCU'),('401858478','WASH-USC')]:
    for path in [
        f'https://sports.core.api.espn.com/v2/sports/football/leagues/college-football/events/{gid}/competitions/{gid}/probabilities?limit=1',
        f'https://site.web.api.espn.com/apis/site/v2/sports/football/college-football/summary?event={gid}',
    ]:
        try:
            d = get(path)
            if 'items' in d:
                # follow first item
                if d['items']:
                    item = get(d['items'][0]['$ref']) if isinstance(d['items'][0], dict) and '$ref' in d['items'][0] else d['items'][0]
                    print(label, 'prob-item', json.dumps(item)[:500])
                else:
                    print(label, 'prob empty', path)
            else:
                # look for winprobability key
                keys = list(d.keys())
                print(label, 'summary keys', keys)
                if 'winprobability' in d:
                    wp = d['winprobability']
                    print(label, 'wp last', wp[-1] if wp else None)
                if 'predictor' in d:
                    print(label, 'predictor', d['predictor'])
        except Exception as ex:
            print(label, path.split('/')[-1][:40], 'ERR', ex)

# find Army / Louisiana Tech
print('---SEARCH ARMY---')
try:
    d = get('https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?groups=80&limit=300')
    for e in d.get('events', []):
        name = e.get('name','')
        if 'Army' in name or 'Louisiana Tech' in name or 'Tech' in e.get('shortName',''):
            c=e['competitions'][0]; st=c['status']['type']
            teams=' / '.join(f"{t['team']['abbreviation']} {t.get('score','')}" for t in c['competitors'])
            print(e.get('shortName'), st.get('detail'), teams, 'id', e.get('id'), 'completed', st.get('completed'))
except Exception as ex:
    print('board ERR', ex)

# also search scoreboard date
try:
    d = get('https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?dates=20261003&limit=300')
    for e in d.get('events', []):
        name = e.get('name','')
        if 'Army' in name or 'Louisiana Tech' in name:
            c=e['competitions'][0]; st=c['status']['type']
            teams=' / '.join(f"{t['team']['abbreviation']} {t.get('score','')}" for t in c['competitors'])
            print('DATED', e.get('shortName'), st.get('detail'), teams, 'id', e.get('id'))
except Exception as ex:
    print('dated ERR', ex)
