import urllib.request, json, re

def get(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    return json.loads(urllib.request.urlopen(req, timeout=25).read().decode())

# CFB scoreboard + find BYU/ISU and WSU/USU event ids
sb = get('https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard')
print('=== LIVE CFB ===')
for e in sb.get('events', []):
    st = e.get('status', {}).get('type', {})
    if st.get('completed') or st.get('state') == 'pre':
        continue
    eid = e.get('id')
    comps = e.get('competitions', [{}])[0]
    teams = comps.get('competitors', [])
    parts = []
    for t in sorted(teams, key=lambda x: x.get('homeAway')):
        parts.append(f"{t.get('team', {}).get('abbreviation','?')} {t.get('score','?')} (homeAway={t.get('homeAway')})")
    print(f"{e.get('shortName')} id={eid} | {' | '.join(parts)} | {st.get('detail')}")
    # try win probability
    try:
        wp = get(f'https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event={eid}')
        wps = wp.get('winprobability') or wp.get('predictor') or {}
        # winprobability is often a list of points
        if isinstance(wps, list) and wps:
            last = wps[-1]
            print('  WP last:', {k: last.get(k) for k in last if k in ('homeWinPercentage','awayWinPercentage','tiePercentage','secondsLeft','playId') or 'Win' in k or 'win' in k})
            print('  WP keys sample:', list(last.keys())[:20])
        elif isinstance(wps, dict):
            print('  predictor:', wps)
        # also check header competitions situation
        hdr = wp.get('header', {}).get('competitions', [{}])[0]
        sit = hdr.get('situation') or {}
        if sit:
            print('  situation:', {k: sit.get(k) for k in ('downDistanceText','possessionText','lastPlay') if k in sit or True})
            lp = sit.get('lastPlay') or {}
            if lp:
                print('  lastPlay:', lp.get('text'))
        # probability in situation?
        for t in hdr.get('competitors', []):
            print('  team', t.get('team',{}).get('abbreviation'), 'score', t.get('score'), 'prob', t.get('probability') or t.get('record'))
    except Exception as ex:
        print('  WP err', ex)

# also check Iowa-Wash if still in progress
print('=== ALL IN-PROGRESS OR RECENT IOWA/WASH/WSU ===')
for e in sb.get('events', []):
    name = (e.get('shortName') or '') + ' ' + (e.get('name') or '')
    if any(x in name.upper() for x in ('IOWA', 'WASH', 'BYU', 'UTAH ST', 'WASH ST', 'WSU', 'USU')):
        st = e.get('status', {}).get('type', {})
        print(e.get('shortName'), st.get('description'), st.get('detail'), 'id', e.get('id'))
