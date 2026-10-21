import urllib.request, json
base='https://site.api.espn.com/apis/site/v2/sports/football/college-football'
eids=['401856820','401860921','401856817','401860900']
for eid in eids:
  print('===', eid)
  try:
    s=json.load(urllib.request.urlopen(base+f'/summary?event={eid}', timeout=25))
    hdr=s.get('header',{}).get('competitions',[{}])[0]
    status=hdr.get('status',{}).get('type',{}).get('detail','')
    print(' status', status)
    for c in hdr.get('competitors',[]):
      print(' ', c['team']['abbreviation'], c.get('score'), 'homeAway', c.get('homeAway'), 'prob', c.get('probability'))
    wp=s.get('winprobability') or []
    if wp:
      last=wp[-1]
      print(' lastWP homeWinPct', last.get('homeWinPercentage'), 'playId', last.get('playId'), 'secs', last.get('secondsLeft'))
      print(' keys', list(last.keys()))
    else:
      print(' no winprobability array')
  except Exception as e:
    print(' ERR', e)
