import urllib.request, json, re
# find event ids then summary
url='https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard'
j=json.load(urllib.request.urlopen(url, timeout=20))
want={'CCU','MRSH','UAB','MEM','UGA','ALA'}
for e in j.get('events',[]):
  c=e['competitions'][0]
  abs_=set(x['team']['abbreviation'] for x in c['competitors'])
  if not want.intersection(abs_):
    continue
  eid=e['id']
  print('EVENT', e.get('shortName'), eid)
  # try winprobability endpoint
  for path in [
    f'https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event={eid}',
    f'https://sports.core.api.espn.com/v2/sports/football/leagues/college-football/events/{eid}/competitions/{eid}/probabilities?limit=1',
  ]:
    try:
      raw=urllib.request.urlopen(path, timeout=20).read().decode('utf-8','replace')
      data=json.loads(raw)
    except Exception as ex:
      print('  fail', path.split('/')[-1][:40], ex)
      continue
    if 'winprobability' in data:
      wp=data['winprobability']
      if isinstance(wp, list) and wp:
        last=wp[-1]
        print('  WP last', {k:last.get(k) for k in last if 'home' in k.lower() or 'away' in k.lower() or 'tie' in k.lower() or 'playId' in k or 'percentage' in k.lower()})
        print('  WP keys', list(last.keys())[:20])
      else:
        print('  WP type', type(wp), str(wp)[:200])
    if 'header' in data:
      comps=data['header'].get('competitions',[{}])[0].get('competitors',[])
      for x in comps:
        print('  hdr', x.get('team',{}).get('abbreviation'), 'score', x.get('score'), 'winner', x.get('winner'), 'prob', x.get('probability'))
    if 'items' in data and data['items']:
      it=data['items'][-1]
      print('  prob item', {k:it.get(k) for k in list(it)[:15]})
