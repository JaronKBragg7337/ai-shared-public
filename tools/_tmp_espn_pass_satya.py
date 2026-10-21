import urllib.request, json
req = urllib.request.Request(
  'https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard',
  headers={'User-Agent':'Mozilla/5.0'})
data = json.loads(urllib.request.urlopen(req, timeout=20).read())
print('events', len(data.get('events', [])))
want = ['baylor','arizona state','cincinnati','fresno','washington state','san jose','hawai','texas state','san diego','eastern washington','uc davis','southern utah']
for ev in data.get('events', []):
  name = ev.get('name','')
  low = name.lower()
  if not any(w in low for w in want):
    continue
  comp = ev['competitions'][0]
  st = comp['status']['type']
  print('GAME', name)
  print('  status', st.get('state'), st.get('detail') or st.get('description'))
  for c in comp['competitors']:
    print('  ', c['team']['abbreviation'], c.get('score'), c.get('homeAway'))
  eid = ev.get('id')
  try:
    sreq = urllib.request.Request(
      f'https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event={eid}',
      headers={'User-Agent':'Mozilla/5.0'})
    sdata = json.loads(urllib.request.urlopen(sreq, timeout=15).read())
    wpr = sdata.get('winprobability') or []
    if wpr:
      last = wpr[-1]
      print('  WPlast', {k:last.get(k) for k in ('homeWinPercentage','tiePercentage','playId','secondsLeft') if k in last or True})
      print('  WPlast_raw_keys', list(last.keys())[:12])
      print('  WPlast_vals', last)
  except Exception as e:
    print('  summary err', type(e).__name__, e)
  print()
