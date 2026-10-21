import json, urllib.request
url = 'https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?groups=80&limit=200'
j = json.load(urllib.request.urlopen(url, timeout=20))
keys = ('Indiana','Nebraska','Texas A&M','Missouri','UCF','Oklahoma State','Pittsburgh','North Carolina','South Carolina','Florida','Wake Forest','NC State','Arizona','West Virginia','Tulane','Army','Sacramento','Bowling')
for e in j.get('events', []):
    comp = e['competitions'][0]
    st = comp['status']['type']['name']
    if st not in ('STATUS_IN_PROGRESS','STATUS_HALFTIME','STATUS_END_PERIOD'):
        continue
    home = next(c for c in comp['competitors'] if c['homeAway']=='home')
    away = next(c for c in comp['competitors'] if c['homeAway']=='away')
    names = away['team']['displayName'] + ' @ ' + home['team']['displayName']
    if not any(k in names for k in keys):
        continue
    def wp(c):
        p = c.get('probability') or {}
        return p.get('winPercentage')
    sit = ''
    try:
        lp = (comp.get('situation') or {}).get('lastPlay') or {}
        pr = lp.get('probability') or {}
        if pr:
            sit = json.dumps(pr)
    except Exception:
        pass
    line = '%s %s - %s %s | %s | homeWP=%s awayWP=%s | %s' % (
        away['team']['abbreviation'], away['score'],
        home['team']['abbreviation'], home['score'],
        comp['status']['type']['detail'], wp(home), wp(away), names)
    print(line)
    if sit:
        print('  sit', sit[:240])
