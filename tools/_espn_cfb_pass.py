import urllib.request, json
url='https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard'
raw=urllib.request.urlopen(url, timeout=20).read().decode()
data=json.loads(raw)
want=('tech','colorado','washington','usc','southern cal','byu','tcu','miami','clemson','indiana','rutgers','army','temple','south florida','oregon state','boise','utah state')
for ev in data.get('events',[]):
  name=ev.get('name','')
  low=name.lower()
  if not any(w in low for w in want): continue
  comp=ev['competitions'][0]
  status=comp['status']['type'].get('detail') or comp['status']['type'].get('description')
  teams=[]
  probs=[]
  for c in comp['competitors']:
    abbr=c['team']['abbreviation']
    teams.append(f"{abbr} {c.get('score')} ({c.get('homeAway')})")
    p=c.get('probability') or {}
    if p:
      probs.append(f"{abbr}:{p.get('winPercentage')}")
  print(name, '|', status)
  print(' ', '; '.join(teams))
  print('  WP', probs)
