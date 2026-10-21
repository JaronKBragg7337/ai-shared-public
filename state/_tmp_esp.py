import urllib.request, json
# find Malaga-Espanyol event id then summary
u='https://site.api.espn.com/apis/site/v2/sports/soccer/esp.1/scoreboard?dates=20261009'
req=urllib.request.Request(u, headers={'User-Agent':'Mozilla/5.0'})
d=json.load(urllib.request.urlopen(req, timeout=20))
for e in d.get('events') or []:
  print('EVENT', e.get('id'), e.get('name'), e.get('status',{}).get('type',{}).get('detail'))
  c=(e.get('competitions') or [{}])[0]
  for x in c.get('competitors') or []:
    print(' ', (x.get('team') or {}).get('displayName'), 'score', x.get('score'), 'homeAway', x.get('homeAway'), 'winner', x.get('winner'))
  eid=e.get('id')
  for path in [
    f'https://site.api.espn.com/apis/site/v2/sports/soccer/esp.1/summary?event={eid}',
    f'https://site.api.espn.com/apis/site/v2/sports/soccer/esp.1/summary?event={eid}',
  ]:
    try:
      s=json.load(urllib.request.urlopen(urllib.request.Request(path, headers={'User-Agent':'Mozilla/5.0'}), timeout=20))
      print('summary keys', list(s)[:20])
      winp=s.get('winprobability') or s.get('predictor') or s.get('probables')
      print('winp type', type(winp), str(winp)[:500] if winp else None)
      if isinstance(s.get('winprobability'), list) and s['winprobability']:
        print('last wp', s['winprobability'][-1])
      situ=s.get('situation') or {}
      print('situation', {k:situ.get(k) for k in list(situ)[:15]})
      # header competitions status
      hdr=s.get('header') or {}
      print('header competitions', str((hdr.get('competitions') or [])[:1])[:400])
    except Exception as ex:
      print('sum fail', ex)
