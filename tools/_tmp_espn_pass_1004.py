import urllib.request, json, sys

def get(url):
    return json.load(urllib.request.urlopen(url, timeout=25))

def dump(name, url, keys=None):
    print('==', name)
    data = get(url)
    for e in data.get('events', []):
        st = e['status']['type']['state']
        comp = e['competitions'][0]
        teams = comp['competitors']
        home = next(t for t in teams if t['homeAway'] == 'home')
        away = next(t for t in teams if t['homeAway'] == 'away')
        detail = e['status']['type'].get('detail', '')
        ab = away['team']['abbreviation']
        hb = home['team']['abbreviation']
        key = f'{ab}@{hb}'.upper()
        if st == 'in' or (keys and any(k in key for k in keys)):
            print(f"{ab} {away.get('score','?')} @ {hb} {home.get('score','?')} | {detail} | state={st} | id={e['id']}")

dump('cfb', 'https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?groups=80&limit=300',
     keys=['CIN','ARIZ','FRES','WSU','BAY','ASU','TXST','SDSU','HAW','SJSU'])
# also FCS/all groups
dump('cfb80b', 'https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?limit=300',
     keys=['CIN','ARIZ','FRES','WSU','BAY','ASU','TXST','SDSU','HAW','SJSU'])
dump('nhl', 'https://site.api.espn.com/apis/site/v2/sports/hockey/nhl/scoreboard')
dump('mlb', 'https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard')

# WP for specific event ids if found live
print('== WP pulls')
for eid in sys.argv[1:] or []:
    url = f'https://sports.core.api.espn.com/v2/sports/football/leagues/college-football/events/{eid}/competitions/{eid}/probabilities?limit=5'
    try:
        d = get(url)
        items = d.get('items') or []
        print(eid, 'items', len(items))
        if items:
            last = get(items[-1]['$ref']) if '$ref' in items[-1] else items[-1]
            print(' last', {k: last.get(k) for k in ('homeWinPercentage','awayWinPercentage','tiePercentage','playId') if k in last or True})
    except Exception as ex:
        print(eid, 'ERR', ex)
