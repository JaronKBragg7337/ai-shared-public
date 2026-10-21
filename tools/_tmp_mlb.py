import json, urllib.request
r = urllib.request.urlopen('https://statsapi.mlb.com/api/v1/schedule?sportId=1&date=2026-09-23&hydrate=linescore,team', timeout=25)
d = json.load(r)
for day in d.get('dates', []):
    for g in day.get('games', []):
        a = g['teams']['away']; h = g['teams']['home']; ls = g.get('linescore') or {}; st = g.get('status') or {}
        aa = a['team']['abbreviation']; ha = h['team']['abbreviation']
        if aa in ('HOU','SD','LAA') or ha in ('SEA','LAD','ATH'):
            print('%s %s @ %s %s | %s inn=%s %s' % (aa, a.get('score'), ha, h.get('score'), st.get('detailedState'), ls.get('currentInning'), ls.get('inningState')))
