import json,urllib.request
for d in ['2026-09-23','2026-09-24']:
  url='https://statsapi.mlb.com/api/v1.1/schedule?sportId=1&date=%s&hydrate=linescore,team'%d
  try:
    with urllib.request.urlopen(url,timeout=20) as r:
      data=json.load(r)
  except Exception as e:
    print('MLB',d,e); continue
  print('=== MLB',d)
  for date in data.get('dates',[]):
    for g in date.get('games',[]):
      aw=g['teams']['away']; hm=g['teams']['home']
      status=g.get('status',{}).get('detailedState')
      ls=g.get('linescore',{})
      print('%s %s @ %s %s | %s %s %s'%(aw['team']['abbreviation'],aw.get('score'),hm['team']['abbreviation'],hm.get('score'),status,ls.get('inningHalf'),ls.get('currentInning')))
