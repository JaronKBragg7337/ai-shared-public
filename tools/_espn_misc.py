import urllib.request, json
base='https://site.api.espn.com/apis/site/v2/sports/football/college-football'
data=json.loads(urllib.request.urlopen(base+'/scoreboard?groups=80', timeout=20).read().decode())
# also fcs groups?
for g in ['80','81','']: 
  pass
keys=('Pine Bluff','Southern','Georgia Southern','Coastal','Arkansas','Texas A&M','UTSA','Rice','Illinois State','South Dakota')
for ev in data.get('events',[]):
  name=ev.get('name','')
  if not any(k.lower() in name.lower() for k in keys): continue
  eid=ev['id']; comp=ev['competitions'][0]
  st=comp['status']['type'].get('detail','')
  scores=', '.join(f"{c['team']['abbreviation']} {c.get('score')}" for c in comp['competitors'])
  s=json.loads(urllib.request.urlopen(base+f'/summary?event={eid}', timeout=15).read().decode())
  wp=(s.get('winprobability') or [None])[-1]
  hwp=wp.get('homeWinPercentage') if wp else None
  home=next(c['team']['abbreviation'] for c in comp['competitors'] if c['homeAway']=='home')
  print(f"{name} | {st} | {scores} | home={home} WPh={hwp} awayWP={None if hwp is None else round(1-hwp,4)}")
# also try scoreboard without groups for more
