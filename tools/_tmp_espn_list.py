import urllib.request, json
req = urllib.request.Request(
  'https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?limit=200',
  headers={'User-Agent':'Mozilla/5.0'})
data = json.loads(urllib.request.urlopen(req, timeout=20).read())
print('events', len(data.get('events', [])))
for ev in data.get('events', []):
  comp = ev['competitions'][0]
  st = comp['status']['type']
  teams = ', '.join(f"{c['team']['abbreviation']} {c.get('score')}" for c in comp['competitors'])
  print(f"{st.get('state'):5} | {st.get('detail') or st.get('shortDetail')} | {ev.get('name')} | {teams}")
