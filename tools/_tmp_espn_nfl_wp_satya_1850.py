import urllib.request, json

url = 'https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard'
data = json.loads(urllib.request.urlopen(url, timeout=20).read())
for e in data.get('events', []):
    comp = e['competitions'][0]
    st = comp['status']['type']
    status = st.get('description', '')
    state = st.get('state', '')
    clock = comp['status'].get('displayClock', '')
    period = comp['status'].get('period', '')
    eid = e['id']
    name = e.get('name', '')
    print(f'{eid} {name} | {status} {clock} P{period} state={state}')
    for c in comp['competitors']:
        print(' ', c['homeAway'], c['team']['abbreviation'], c.get('score'), c.get('probability'))
    try:
        s = json.loads(urllib.request.urlopen(
            f'https://site.api.espn.com/apis/site/v2/sports/football/nfl/summary?event={eid}',
            timeout=20).read())
        wp = s.get('winprobability') or []
        if wp:
            last = wp[-1]
            print('  lastWP home=%.3f away=%s' % (
                float(last.get('homeWinPercentage') or 0),
                last.get('awayWinPercentage')))
            # derive away if missing
            h = float(last.get('homeWinPercentage') or 0)
            a = last.get('awayWinPercentage')
            if a is None:
                a = 1.0 - h
            print('  WP home=%.1f%% away=%.1f%%' % (100*h, 100*float(a)))
        else:
            print('  lastWP none')
        pred = s.get('predictor') or {}
        if pred:
            print('  pred home', (pred.get('homeTeam') or {}).get('gameProjection'),
                  'away', (pred.get('awayTeam') or {}).get('gameProjection'))
        sit = s.get('situation') or {}
        if sit:
            print('  sit', sit.get('downDistanceText'), 'poss', sit.get('possession'))
    except Exception as ex:
        print('  summary err', ex)
