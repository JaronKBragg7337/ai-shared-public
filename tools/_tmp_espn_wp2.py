import urllib.request, json
url='https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard'
j=json.load(urllib.request.urlopen(url, timeout=25))
want_pairs=[('CCU','MRSH'),('UAB','MEM'),('LSU','UK'),('USC','PSU'),('UGA','ALA')]
for e in j.get('events',[]):
  c=e['competitions'][0]
  abs_=set(x['team']['abbreviation'] for x in c['competitors'])
  if not any(set(p)<=abs_ for p in want_pairs):
    continue
  eid=e['id']
  parts=[]
  home_abbr=None
  for x in c['competitors']:
    ab=x['team']['abbreviation']
    parts.append(f"{ab}{x.get('score','?')}({'H' if x['homeAway']=='home' else 'A'})")
    if x['homeAway']=='home':
      home_abbr=ab
  st=c['status']['type'].get('detail','')
  print('GAME', e.get('shortName'), eid, ' '.join(parts), st)
  try:
    s=json.load(urllib.request.urlopen(f'https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event={eid}', timeout=25))
  except Exception as ex:
    print('  summary err', ex)
    continue
  wpl=s.get('winprobability') or []
  if wpl:
    last=wpl[-1]
    hwp=float(last.get('homeWinPercentage') or 0)
    print(f'  homeWP={hwp:.1%} home={home_abbr} awayWP={1-hwp:.1%}')
  else:
    print('  no winprobability array')
