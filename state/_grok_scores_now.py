import urllib.request, json

def load(url):
    with urllib.request.urlopen(url, timeout=25) as r:
        return json.load(r)

def dump(label, url, keys=None):
    print('==', label, '==')
    try:
        d = load(url)
    except Exception as ex:
        print('ERR', ex)
        return
    for e in d.get('events', []):
        comp = e['competitions'][0]
        st = comp['status']['type']['description']
        detail = comp['status']['type'].get('detail', '')
        teams = comp['competitors']
        home = [t for t in teams if t['homeAway'] == 'home'][0]
        away = [t for t in teams if t['homeAway'] == 'away'][0]
        name = e.get('name', '')
        line = f"{away['team']['abbreviation']} {away['score']}-{home['score']} {home['team']['abbreviation']} | {st} | {detail} | {name}"
        if keys:
            blob = (name + ' ' + home['team']['displayName'] + ' ' + away['team']['displayName']).lower()
            if any(k.lower() in blob for k in keys):
                print('***', line)
                wp = comp.get('situation', {}) or {}
                if 'lastPlay' in wp:
                    print('   lastPlay', wp.get('lastPlay', {}).get('text', '')[:120])
                # win probability if present
                for t in teams:
                    print('  ', t['team']['abbreviation'], 'score', t['score'], t.get('winner', ''), 'prob', t.get('prob', t.get('possession', '')))
        else:
            if st not in ('Scheduled', 'Pre-Game', 'Postponed'):
                print(line)

dump('NHL', 'https://site.api.espn.com/apis/site/v2/sports/hockey/nhl/scoreboard')
dump('CFB', 'https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard', keys=['Montana', 'Idaho', 'Bobcat'])
dump('CFB-all-live', 'https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard')
dump('CNL', 'https://site.api.espn.com/apis/site/v2/sports/soccer/concacaf.nations.league/scoreboard', keys=['Jamaica', 'Salvador', 'El Salvador'])
# also try general soccer scoreboard search
for league in ['fifa.worldq.concacaf', 'usa.1', 'eng.1', 'mex.1']:
    dump('SOC-'+league, f'https://site.api.espn.com/apis/site/v2/sports/soccer/{league}/scoreboard', keys=['Jamaica', 'Salvador'])
