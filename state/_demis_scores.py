import json, urllib.request
urls = {
  'nhl': 'https://site.api.espn.com/apis/site/v2/sports/hockey/nhl/scoreboard',
  'wnba': 'https://site.api.espn.com/apis/site/v2/sports/basketball/wnba/scoreboard',
}
for k, u in urls.items():
  print('====', k, '====')
  try:
    d = json.load(urllib.request.urlopen(u, timeout=15))
  except Exception as e:
    print('ERR', e)
    continue
  for e in d.get('events', []):
    comp = e['competitions'][0]
    teams = comp['competitors']
    a = next(t for t in teams if t['homeAway'] == 'away')
    h = next(t for t in teams if t['homeAway'] == 'home')
    st = comp['status']['type']
    line = '%s %s @ %s %s | %s | %s' % (
      a['team']['abbreviation'], a.get('score', '?'),
      h['team']['abbreviation'], h.get('score', '?'),
      st.get('detail', ''), st.get('state'))
    print(line)
    for t in (a, h):
      if 'probability' in t:
        print('  WP', t['team']['abbreviation'], t['probability'])
