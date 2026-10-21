import json,urllib.request
req=urllib.request.Request('https://api.sofascore.com/api/v1/sport/tennis/events/live', headers={'User-Agent':'Mozilla/5.0'})
try:
  d=json.load(urllib.request.urlopen(req, timeout=20))
  print('live', len(d.get('events') or []))
  for ev in d.get('events') or []:
    h=ev.get('homeTeam',{}).get('name',''); a=ev.get('awayTeam',{}).get('name','')
    sc=ev.get('homeScore',{}); ac=ev.get('awayScore',{})
    print(f"{h} {sc.get('current')}({sc.get('period1')}-{sc.get('period2')}-{sc.get('period3')}) vs {a} {ac.get('current')}({ac.get('period1')}-{ac.get('period2')}-{ac.get('period3')}) | {ev.get('status',{}).get('description')} | {ev.get('tournament',{}).get('name')}")
except Exception as e:
  print('fail', e)
