import urllib.request, json

def get(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.load(r)

def show_event(e, deep=False):
    comp = e['competitions'][0]
    st = comp['status']['type']
    teams = comp['competitors']
    home = [t for t in teams if t['homeAway']=='home'][0]
    away = [t for t in teams if t['homeAway']=='away'][0]
    print(f"{away['team']['displayName']} {away['score']} @ {home['team']['displayName']} {home['score']} | {st.get('detail')} | {st.get('description')}")
    for t in teams:
        print(' ', t['team']['abbreviation'], 'score', t['score'], 'winner', t.get('winner'), 'homeAway', t['homeAway'])
        # try probability fields
        for k in ('probability','winProbability','records'):
            if k in t:
                print('   ', k, str(t[k])[:200])
    sit = comp.get('situation') or {}
    if sit:
        print('  situation keys', list(sit.keys())[:20])
        lp = sit.get('lastPlay') or {}
        if lp:
            print('  lastPlay', str(lp.get('text',''))[:160], 'prob', lp.get('probability'))
            if 'probability' in lp:
                print('  lastPlay.probability', lp['probability'])
    if deep:
        # dump competitor prob if nested
        print('  status', st)

# FCS / CFB with groups
urls = [
 'https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?groups=80&limit=300',
 'https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?groups=20&limit=300',
 'https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?dates=20261002&limit=300',
 'https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?dates=20261003&limit=300',
]
seen=set()
for u in urls:
    print('URL', u)
    try:
        d=get(u)
    except Exception as ex:
        print('ERR', ex); continue
    for e in d.get('events',[]):
        name=e.get('name','')
        if 'Montana' in name or 'Idaho' in name:
            if e['id'] in seen: continue
            seen.add(e['id'])
            print('***', name)
            show_event(e, deep=True)
            # also try summary endpoint for WP
            eid=e['id']
            try:
                s=get(f'https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event={eid}')
                wp=s.get('winprobability') or s.get('predictor') or {}
                print(' summary winprobability sample', str(wp)[:300] if wp else None)
                if isinstance(wp, list) and wp:
                    print(' last wp entry', wp[-1])
                # situation from header
                hdr=s.get('header') or {}
                comps=(hdr.get('competitions') or [{}])[0]
                sit=comps.get('situation') or {}
                print(' summary situation', str(sit)[:400])
                for c in (comps.get('competitors') or []):
                    print('  comp', c.get('team',{}).get('abbreviation'), 'score', c.get('score'), 'prob fields', {k:c.get(k) for k in c if 'prob' in k.lower() or k=='records'})
            except Exception as ex:
                print(' summary err', ex)

print('== ANA detail ==')
d=get('https://site.api.espn.com/apis/site/v2/sports/hockey/nhl/scoreboard')
for e in d.get('events',[]):
    if 'Anaheim' in e.get('name','') or 'Vegas' in e.get('name',''):
        show_event(e)
