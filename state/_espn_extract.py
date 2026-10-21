import json, urllib.request
url = 'https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?groups=80&dates=20261003'
req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0','Accept':'application/json'})
with urllib.request.urlopen(req, timeout=40) as r:
    d = json.load(r)
keys = ['Western Michigan','Buffalo','West Virginia','Iowa State','Syracuse','Connecticut','Toledo','Ball State','Michigan','Minnesota','Houston','UCF','Navy','Air Force','Alabama','Mississippi State','Vanderbilt','Georgia','Notre Dame','North Carolina','SMU','Boston College']
for e in d.get('events', []):
    n = e.get('name','')
    if not any(k.lower() in n.lower() for k in keys):
        continue
    c = e['competitions'][0]
    s = c['status']['type']
    comps = c['competitors']
    a = next(x for x in comps if x['homeAway']=='away')
    h = next(x for x in comps if x['homeAway']=='home')
    print('GAME', n)
    print(' STATUS', s.get('detail'), '|', s.get('state'), '| completed', s.get('completed'))
    for x in comps:
        print(' ', x['homeAway'], x['team']['abbreviation'], x['team']['displayName'], 'score', x.get('score'), 'winner', x.get('winner'))
    sit = c.get('situation') or {}
    if sit:
        print(' situation lastPlay', (sit.get('lastPlay') or {}).get('text','')[:120])
    # probability from competitors
    for x in comps:
        if 'probability' in x and x['probability']:
            print(' prob', x['team']['abbreviation'], x['probability'])
    print()
# also dump win probs if in status
print('events', len(d.get('events',[])))
