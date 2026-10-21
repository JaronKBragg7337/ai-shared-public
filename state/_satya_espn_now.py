import urllib.request, json, sys
url = 'https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard'
with urllib.request.urlopen(url, timeout=20) as r:
    d = json.load(r)
for e in d.get('events', []):
    comp = e['competitions'][0]
    st = comp['status']['type']
    if st.get('completed'):
        continue
    teams = comp['competitors']
    home = next(t for t in teams if t['homeAway'] == 'home')
    away = next(t for t in teams if t['homeAway'] == 'away')
    detail = st.get('detail', '')
    state = st.get('state')
    print(f"{e['shortName']}: {away['team']['abbreviation']} {away['score']}-{home['team']['abbreviation']} {home['score']} | {detail} state={state}")
    # try summary for WP
    eid = e.get('id')
    try:
        surl = f'https://site.api.espn.com/apis/site/v2/sports/football/nfl/summary?event={eid}'
        with urllib.request.urlopen(surl, timeout=15) as sr:
            s = json.load(sr)
        pred = s.get('predictor') or s.get('winprobability') or []
        if isinstance(pred, list) and pred:
            last = pred[-1]
            print('  winprob last', last)
        elif isinstance(pred, dict):
            print('  predictor', {k: pred.get(k) for k in list(pred)[:8]})
        # also check situation
        sit = s.get('situation') or {}
        print('  situation', {k: sit.get(k) for k in ('possession','downDistanceText','lastPlay','isRedZone') if k in sit or True})
        for p in (s.get('winprobability') or [])[-3:]:
            print('  wp', p)
    except Exception as ex:
        print('  summary err', ex)
