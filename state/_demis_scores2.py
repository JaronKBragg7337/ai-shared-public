import json, urllib.request

def dump(path, want):
    url = f'https://site.api.espn.com/apis/site/v2/sports/{path}'
    with urllib.request.urlopen(url, timeout=20) as r:
        data = json.load(r)
    for ev in data.get('events', []):
        name = ev.get('shortName') or ev.get('name')
        if not any(w.lower() in name.lower() for w in want):
            continue
        comp = ev['competitions'][0]
        st = comp['status']['type']
        print(name, '|', st.get('detail') or st.get('description'))
        for c in comp['competitors']:
            print(f"  {c['team']['abbreviation']} score={c.get('score')} homeAway={c['homeAway']} winner={c.get('winner')}")
        # situation probability (basketball)
        sit = comp.get('situation') or {}
        last = sit.get('lastPlay') or {}
        prob = last.get('probability') or {}
        if prob:
            print('  lastPlay WP:', prob)
        # try status / odds win pct
        for o in (comp.get('odds') or []):
            print('  odds:', {k:o.get(k) for k in ('homeWinPercentage','awayWinPercentage','details','spread','overUnder') if k in o})
        # dig for winprobability endpoints hint in links
        print('  status state', st.get('state'), 'completed', st.get('completed'))

dump('hockey/nhl/scoreboard', ['STL','DAL','ANA','VGK','VEG'])
dump('basketball/wnba/scoreboard', ['DAL','GS','GSV'])
