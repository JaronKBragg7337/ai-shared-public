import urllib.request, json
url = 'https://statsapi.mlb.com/api/v1/schedule?sportId=1&date=2026-09-25&hydrate=linescore,team'
with urllib.request.urlopen(url, timeout=20) as r:
    d = json.load(r)
for g in d.get('dates', [{}])[0].get('games', []):
    a = g['teams']['away']
    h = g['teams']['home']
    ls = g.get('linescore', {})
    inn = ls.get('currentInning', '?')
    half = ls.get('inningHalf', '')
    state = g['status']['detailedState']
    ar = a.get('score', '?')
    hr = h.get('score', '?')
    aa = a['team']['abbreviation']
    ha = h['team']['abbreviation']
    print(f'{aa} {ar} @ {ha} {hr} | {state} inn={inn} {half}')
