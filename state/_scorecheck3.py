import urllib.request, json
u='https://site.api.espn.com/apis/site/v2/sports/hockey/nhl/scoreboard'
d=json.loads(urllib.request.urlopen(u,timeout=15).read())
for e in d.get('events',[]):
    if 'Canuck' in e['name'] or 'Oilers' in e['name']:
        c=e['competitions'][0]
        for x in c['competitors']:
            print(x['homeAway'], x['team']['abbreviation'], x['score'])
        print('status', e['status']['type']['detail'])
        print('last', (c.get('situation') or {}).get('lastPlay',{}).get('text'))
