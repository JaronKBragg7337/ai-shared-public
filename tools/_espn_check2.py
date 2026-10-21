import urllib.request, json
for path in [
 'https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?groups=80',
 'https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?groups=12',
 'https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?limit=300',
]:
  try:
    d=json.loads(urllib.request.urlopen(path,timeout=20).read().decode())
  except Exception as e:
    print('fail', path, e); continue
  for e in d.get('events',[]):
    n=e.get('name','')
    if any(x in n for x in ['Columbia','Marist','Wyoming','San Jose','Utah State','Washington State']):
      c=e['competitions'][0]
      s=c.get('status',{}).get('type',{}).get('detail','')
      teams=', '.join(f"{x['team']['abbreviation']} {x['score']}" for x in c['competitors'])
      print(f'{n} | {teams} | {s}')
