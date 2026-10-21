import json,urllib.request
UA={'User-Agent':'Mozilla/5.0'}
def get(url):
  req=urllib.request.Request(url,headers=UA)
  with urllib.request.urlopen(req,timeout=20) as r:
    return json.load(r)
# ESPN scoreboards
for path,label in [
 ('http://site.api.espn.com/apis/site/v2/sports/tennis/wta/scoreboard','WTA'),
 ('http://site.api.espn.com/apis/site/v2/sports/tennis/atp/scoreboard','ATP'),
 ('http://site.api.espn.com/apis/site/v2/sports/basketball/wnba/scoreboard','WNBA'),
 ('http://site.api.espn.com/apis/site/v2/sports/hockey/nhl/scoreboard','NHL'),
]:
  try:
    d=get(path)
  except Exception as e:
    print(label,'ERR',e); continue
  print('===',label)
  for ev in d.get('events',[]):
    name=ev.get('name')
    status=ev.get('status',{}).get('type',{}).get('description')
    comps=ev.get('competitions',[{}])[0]
    comps_list=comps.get('competitors',[])
    scores=[]
    for c in comps_list:
      scores.append('%s %s'%(c.get('athlete',c.get('team',{})).get('displayName',c.get('homeAway')), c.get('score')))
    lines=comps.get('situation') or {}
    print(name,'|',status,'|', ' / '.join(scores))
    # linescores detail
    for c in comps_list:
      ls=c.get('linescores')
      if ls: print('  lines',c.get('homeAway'),ls)
