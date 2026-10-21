import urllib.request, json

def get(url):
    req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'})
    return json.loads(urllib.request.urlopen(req, timeout=15).read())

# summary for VAN-EDM
for eid in ['401891804']:
    try:
        s = get(f'https://site.api.espn.com/apis/site/v2/sports/hockey/nhl/summary?event={eid}')
        box = s.get('boxscore',{})
        header = s.get('header',{})
        comps = header.get('competitions',[{}])[0].get('competitors',[])
        status = header.get('competitions',[{}])[0].get('status',{}).get('type',{}).get('detail')
        print('EVENT', eid, status)
        for c in comps:
            print(c['team']['abbreviation'], c['score'], 'home' if c.get('homeAway')=='home' else 'away')
        sit = header.get('competitions',[{}])[0].get('situation',{})
        print('situation', sit.get('lastPlay',{}).get('text'))
        # shots if available
        for t in box.get('teams',[]):
            stats = {x['name']: x.get('displayValue') for x in t.get('statistics',[])}
            print('stats', t.get('team',{}).get('abbreviation'), 'sog', stats.get('sog') or stats.get('shotsTotal') or stats)
    except Exception as ex:
        print('nhl summary err', ex)

# tennis via core API search
for q in ['Vidmanova','Vacherot','Lehecka','Khachanov']:
    try:
        u = f'https://site.api.espn.com/apis/common/v3/search?query={q}&limit=5&type=player'
        d = get(u)
        print('search', q, list(d.keys())[:5])
    except Exception as ex:
        print('search err', q, ex)

# alternate tennis scoreboard
for url in [
    'https://site.api.espn.com/apis/site/v2/sports/tennis/atp/scoreboard',
    'https://site.api.espn.com/apis/site/v2/sports/tennis/wta/scoreboard',
    'https://site.web.api.espn.com/apis/v2/sports/tennis/scoreboard',
]:
    try:
        d = get(url)
        evs = d.get('events') or d.get('leagues',[{}])[0].get('events',[]) if isinstance(d.get('leagues'), list) else d.get('events',[])
        print(url, 'events', len(evs or []))
        for e in (evs or [])[:8]:
            print(' ', e.get('name'), e.get('status',{}).get('type',{}).get('detail'))
    except Exception as ex:
        print('url err', url, ex)
