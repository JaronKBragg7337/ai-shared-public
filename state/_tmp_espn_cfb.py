import json, urllib.request
url = 'http://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard'
d = json.load(urllib.request.urlopen(url, timeout=20))
for e in d.get('events', []):
    comp = e['competitions'][0]
    st = comp['status']['type']['name']
    if st in ('STATUS_SCHEDULED',):
        continue
    teams = []
    for c in comp['competitors']:
        home = 'H' if c.get('homeAway')=='home' else 'A'
        wp = ''
        if c.get('probability'):
            wp = f" WP{c['probability'].get('winPercentage','?')}"
        teams.append(f"{c['team']['abbreviation']}({home}) {c['score']}{wp}")
    clock = comp['status'].get('displayClock','')
    period = comp['status'].get('period','')
    detail = comp['status']['type'].get('detail','')
    print(f"{e['shortName']} | {' | '.join(teams)} | {detail} | {st} {clock} P{period}")
