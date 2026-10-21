import urllib.request, json

def fetch(url):
    with urllib.request.urlopen(url, timeout=25) as r:
        return json.load(r)

urls = [
    'https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?groups=80',
    'https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?groups=81',
    'https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?dates=20261009',
    'https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?dates=20261009&groups=80',
]
seen=set()
for url in urls:
    try:
        data=fetch(url)
    except Exception as e:
        print('FAIL', url, e)
        continue
    for e in data.get('events', []):
        eid=e.get('id')
        if eid in seen: continue
        seen.add(eid)
        name=(e.get('shortName') or e.get('name') or '').upper()
        if any(k in name for k in ['FSU','LOU','FLORIDA ST','LOUISVILLE','COLUMBIA','MARIST','CLMB','MRST','WYO','SJSU','WSU','USU']):
            comp=e['competitions'][0]
            status=comp['status']['type']
            teams=comp['competitors']
            home=next(t for t in teams if t['homeAway']=='home')
            away=next(t for t in teams if t['homeAway']=='away')
            print('{} | {} {} @ {} {} | {} | state={} | id={}'.format(
                e.get('shortName') or e.get('name'),
                away['team']['abbreviation'], away.get('score','?'),
                home['team']['abbreviation'], home.get('score','?'),
                status.get('detail'), status.get('state'), eid))
print('total unique events scanned', len(seen))
