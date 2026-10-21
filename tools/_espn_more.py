import urllib.request, json
base='https://site.api.espn.com/apis/site/v2/sports/football/college-football'
# include groups for more games
for url in [base+'/scoreboard', base+'/scoreboard?groups=80']:
  try:
    data=json.loads(urllib.request.urlopen(url, timeout=20).read().decode())
    print('URL', url, 'events', len(data.get('events',[])))
  except Exception as e:
    print('fail', url, e)
data=json.loads(urllib.request.urlopen(base+'/scoreboard?groups=80', timeout=20).read().decode())
keys=('Army','Temple','South Florida','Oregon','Colorado State','Louisiana','Arkansas State','McNeese','LSU','Navy','West Virginia','Iowa State','California','UNLV','Houston','UCF')
for ev in data.get('events',[]):
  name=ev.get('name','')
  if not any(k in name for k in keys): continue
  eid=ev['id']
  comp=ev['competitions'][0]
  st=comp['status']['type'].get('detail','')
  state=comp['status']['type'].get('state')
  scores=', '.join(f"{c['team']['abbreviation']} {c.get('score')}" for c in comp['competitors'])
  s=json.loads(urllib.request.urlopen(base+f'/summary?event={eid}', timeout=15).read().decode())
  wp=(s.get('winprobability') or [None])[-1]
  hwp=wp.get('homeWinPercentage') if wp else None
  home=next(c['team']['abbreviation'] for c in comp['competitors'] if c['homeAway']=='home')
  away=next(c['team']['abbreviation'] for c in comp['competitors'] if c['homeAway']=='away')
  print(f"{name} | {st} | {scores} | home={home} WPh={hwp} => awayWP={None if hwp is None else round(1-hwp,4)}")
