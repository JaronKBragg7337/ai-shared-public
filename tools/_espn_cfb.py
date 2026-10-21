import urllib.request, json
url='https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard'
with urllib.request.urlopen(url, timeout=20) as r:
    data=json.load(r)
for e in data.get('events', []):
    comp=e['competitions'][0]
    status=comp['status']['type']
    teams=comp['competitors']
    home=next(t for t in teams if t['homeAway']=='home')
    away=next(t for t in teams if t['homeAway']=='away')
    name=e.get('shortName') or e.get('name')
    line='{} | {} {} @ {} {} | {} | state={}'.format(
        name,
        away['team']['abbreviation'], away.get('score','?'),
        home['team']['abbreviation'], home.get('score','?'),
        status.get('detail'), status.get('state'))
    print(line)
