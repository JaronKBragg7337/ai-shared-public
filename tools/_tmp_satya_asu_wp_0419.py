import json, urllib.request
def get(url):
    req=urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.load(r)
j=get('https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?groups=80&limit=200')
for e in j.get('events',[]):
  c=e['competitions'][0]
  names=' / '.join(x['team']['displayName'] for x in c['competitors'])
  low=names.lower()
  if 'hawaii' not in low and 'arizona state' not in low and 'boise' not in low and 'fresno' not in low:
    continue
  if c['status']['type']['state']=='pre':
    continue
  detail=c['status']['type']['detail']
  scores=' '.join('%s=%s'%(x['team']['abbreviation'],x['score']) for x in c['competitors'])
  eid=e['id']
  home=next(x for x in c['competitors'] if x['homeAway']=='home')
  away=next(x for x in c['competitors'] if x['homeAway']=='away')
  hwp=awp=None
  try:
    sj=get('https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event=%s'%eid)
    wp=sj.get('winprobability') or []
    if wp:
      last=wp[-1]
      hwp=last.get('homeWinPercentage')
      awp=1.0-float(hwp) if hwp is not None else None
  except Exception as ex:
    print('err', ex)
  print('%s | %s | %s | home=%s WP=%s | away=%s WP=%s'%(detail,names,scores,home['team']['abbreviation'],hwp,away['team']['abbreviation'],awp))
# refresh Spurs too
j2=get('https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard?dates=20261010')
for e in j2.get('events',[]):
  c=e['competitions'][0]
  names=' / '.join(x['team']['displayName'] for x in c['competitors'])
  if 'spurs' not in names.lower() and 'suns' not in names.lower():
    continue
  if c['status']['type']['state']=='pre':
    continue
  detail=c['status']['type']['detail']
  scores=' '.join('%s=%s'%(x['team']['abbreviation'],x['score']) for x in c['competitors'])
  eid=e['id']
  home=next(x for x in c['competitors'] if x['homeAway']=='home')
  away=next(x for x in c['competitors'] if x['homeAway']=='away')
  hwp=awp=None
  try:
    sj=get('https://site.api.espn.com/apis/site/v2/sports/basketball/nba/summary?event=%s'%eid)
    wp=sj.get('winprobability') or []
    if wp:
      last=wp[-1]
      hwp=last.get('homeWinPercentage')
      awp=1.0-float(hwp) if hwp is not None else None
  except Exception as ex:
    print('err', ex)
  print('%s | %s | %s | home=%s WP=%s | away=%s WP=%s'%(detail,names,scores,home['team']['abbreviation'],hwp,away['team']['abbreviation'],awp))
