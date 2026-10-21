import urllib.request, json
urls = [
  'https://site.api.espn.com/apis/site/v2/sports/soccer/ger.1/scoreboard?dates=20261009',
  'https://site.api.espn.com/apis/site/v2/sports/soccer/esp.1/scoreboard?dates=20261009',
  'https://site.api.espn.com/apis/site/v2/sports/soccer/ksa.1/scoreboard?dates=20261009',
  'https://site.api.espn.com/apis/site/v2/sports/basketball/euroleague/scoreboard?dates=20261009',
  'https://cdn.euroleague.net/live/gamecenters/json',
]
for u in urls:
  try:
    req = urllib.request.Request(u, headers={'User-Agent':'Mozilla/5.0'})
    r = urllib.request.urlopen(req, timeout=20)
    raw = r.read()
    print('OK', u[:80], 'bytes', len(raw))
    try:
      d = json.loads(raw)
    except Exception:
      print('  not json')
      continue
    if isinstance(d, dict) and 'events' in d:
      for e in d.get('events') or []:
        c = (e.get('competitions') or [{}])[0]
        st = (c.get('status') or {}).get('type') or {}
        comps = c.get('competitors') or []
        names = ' vs '.join(f"{(x.get('team') or {}).get('displayName','?')} {x.get('score','')}" for x in comps)
        print(' ', st.get('state'), st.get('detail'), '|', names)
    elif isinstance(d, list):
      print('  list len', len(d), 'sample', str(d[:1])[:200])
    else:
      print('  keys', list(d)[:12] if isinstance(d, dict) else type(d))
  except Exception as ex:
    print('FAIL', u[:70], ex)
