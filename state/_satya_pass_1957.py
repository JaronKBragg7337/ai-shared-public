import urllib.request, json, sys

urls = [
 'https://site.api.espn.com/apis/site/v2/sports/soccer/esp.2/scoreboard',
 'https://site.api.espn.com/apis/site/v2/sports/soccer/esp.1/scoreboard',
 'https://site.api.espn.com/apis/site/v2/sports/soccer/ger.1/scoreboard',
 'https://site.api.espn.com/apis/site/v2/sports/soccer/fra.1/scoreboard',
 'https://site.api.espn.com/apis/site/v2/sports/soccer/ksa.1/scoreboard',
 'https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard',
 'https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard',
]

for u in urls:
  try:
    with urllib.request.urlopen(u, timeout=20) as r:
      d = json.load(r)
    league = u.rstrip('/').split('/')[-2]
    print('==', league, 'events', len(d.get('events', [])))
    for e in d.get('events', []):
      comp = e['competitions'][0]
      st = comp['status']['type']['description']
      detail = comp['status']['type'].get('detail', '')
      clock = comp['status'].get('displayClock', '')
      period = comp['status'].get('period', '')
      teams = []
      for t in comp['competitors']:
        teams.append('%s %s' % (t['team']['displayName'], t.get('score', '?')))
      print(' | '.join(teams), '|', st, detail, 'clk', clock, 'p', period)
  except Exception as ex:
    print('ERR', u, ex)
