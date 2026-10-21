import urllib.request, json
req = urllib.request.Request(
  'https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?dates=20261003&limit=200',
  headers={'User-Agent':'Mozilla/5.0'})
data = json.loads(urllib.request.urlopen(req, timeout=20).read())
want = ['fresno','baylor','texas state','cincinnati','san jos','hawai','eastern washington','uc davis','southern utah']
for ev in data.get('events', []):
  name = ev.get('name','')
  if not any(w in name.lower() for w in want):
    continue
  comp = ev['competitions'][0]
  st = comp['status']['type']
  print('GAME', name)
  print('  status', st.get('state'), st.get('detail') or st.get('shortDetail'))
  home_abbr=away_abbr=None
  for c in comp['competitors']:
    print('  ', c['team']['abbreviation'], c.get('score'), c.get('homeAway'))
    if c.get('homeAway')=='home': home_abbr=c['team']['abbreviation']
    else: away_abbr=c['team']['abbreviation']
  eid = ev.get('id')
  try:
    sreq = urllib.request.Request(
      f'https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event={eid}',
      headers={'User-Agent':'Mozilla/5.0'})
    sdata = json.loads(urllib.request.urlopen(sreq, timeout=15).read())
    wpr = sdata.get('winprobability') or []
    if wpr:
      last = wpr[-1]
      hwp = last.get('homeWinPercentage')
      print(f'  homeWP={hwp} awayWP={None if hwp is None else 1-hwp} home={home_abbr} away={away_abbr}')
      print('  keys', list(last.keys()))
    else:
      print('  no WP')
  except Exception as e:
    print('  err', e)
  print()
# also USA Mexico soccer
print('---SOCCER USA MEX---')
for dates in ['20261003','20261004']:
  u=f'https://site.api.espn.com/apis/site/v2/sports/soccer/fifa.friendly/scoreboard?dates={dates}'
  try:
    d=json.loads(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=15).read())
    for ev in d.get('events',[]):
      n=ev.get('name','')
      if 'united states' in n.lower() or 'mexico' in n.lower() or 'usa' in n.lower():
        st=ev['competitions'][0]['status']['type']
        print(dates, n, st.get('detail'), [(c['team']['abbreviation'], c.get('score')) for c in ev['competitions'][0]['competitors']])
  except Exception as e:
    print('soccer err', dates, e)
