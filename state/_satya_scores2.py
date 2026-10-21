import urllib.request, json

def get(url):
    with urllib.request.urlopen(url, timeout=25) as r:
        return json.load(r)

print('===CFB ALL LIVE/TODAY===')
for url in [
    'https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard',
    'https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?dates=20261002',
    'https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?groups=80&dates=20261002',
]:
    try:
        d = get(url)
        print('URL', url, 'events', len(d.get('events', [])))
        for e in d.get('events', []):
            comp = e['competitions'][0]
            status = comp['status']['type']
            teams = comp['competitors']
            home = [t for t in teams if t['homeAway'] == 'home'][0]
            away = [t for t in teams if t['homeAway'] == 'away'][0]
            state = status.get('name', '')
            detail = status.get('detail', '')
            print('-', e.get('shortName') or e.get('name'), '|', away['team'].get('abbreviation'), away.get('score'), '@', home['team'].get('abbreviation'), home.get('score'), '|', detail, state)
            for t in teams:
                p = t.get('curatedRank')
                prob = None
                # try situation / links
                print('  ', t['team']['abbreviation'], t.get('score'), 'winner', t.get('winner'), 'records', t.get('records'))
            # win prob from competitor
            for t in teams:
                if 'probability' in t:
                    print('  prob', t['team']['abbreviation'], t['probability'])
            sit = comp.get('situation') or {}
            if sit:
                print('  situation keys', list(sit.keys())[:12])
                if 'lastPlay' in sit:
                    print('  lastPlay', sit.get('lastPlay', {}).get('text','')[:120])
    except Exception as ex:
        print('fail', url, ex)

print('===SUMMARY STATUS===')
try:
    d = get('https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?dates=20261002')
    for e in d.get('events', []):
        print(e.get('shortName'), e['competitions'][0]['status']['type'].get('detail'))
except Exception as ex:
    print(ex)

# H2H win probability endpoint sometimes
print('===LOOKUP PITT VT LIB DEL===')
# search
try:
    d = get('https://site.web.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?dates=20261002&limit=100')
    print('web api events', len(d.get('events',[])))
except Exception as ex:
    print('web', ex)
