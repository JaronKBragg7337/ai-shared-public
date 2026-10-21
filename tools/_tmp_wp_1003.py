import urllib.request, json

eids = {
  'FLA-MIZ': '401856708',
  'UK-SC': '401856709',
  'AUB-TENN': '401856710',
  'OSU-IOWA': '401858473',
}

sb = json.load(urllib.request.urlopen(
  'https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?dates=20261003&groups=80&limit=200',
  timeout=25))
print('SCOREBOARD events', len(sb.get('events', [])))
for e in sb.get('events', []):
  c = e['competitions'][0]
  st = c['status']['type']
  if st.get('name') == 'STATUS_SCHEDULED' or st.get('completed'):
    continue
  teams = []
  for t in c['competitors']:
    teams.append('%s %s' % (t['team']['abbreviation'], t.get('score', '?')))
  print('LIVE', e['id'], ' vs '.join(teams), '|', st.get('detail'))
  eids[e.get('shortName', e['id'])] = e['id']

for label, eid in list(eids.items())[:25]:
  try:
    d = json.load(urllib.request.urlopen(
      'https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event=%s' % eid,
      timeout=20))
    wp = d.get('winprobability') or []
    last = wp[-1] if wp else {}
    h = (d.get('header') or {}).get('competitions') or [{}]
    comps = h[0]
    teams = []
    home_abb = None
    away_abb = None
    for c in comps.get('competitors', []):
      abb = c['team']['abbreviation']
      teams.append('%s %s (%s)' % (abb, c.get('score', '?'), c['homeAway']))
      if c['homeAway'] == 'home':
        home_abb = abb
      else:
        away_abb = abb
    st = (comps.get('status') or {}).get('type', {})
    hwp = last.get('homeWinPercentage')
    if hwp is None:
      print('WP', label, '|', ' vs '.join(teams), '|', st.get('detail'), '| no wp')
    else:
      awp = 1.0 - float(hwp)
      print('WP', label, '|', ' vs '.join(teams), '|', st.get('detail'),
            '| home=%s WP=%.1f%% | away=%s WP=%.1f%%' % (home_abb, 100*float(hwp), away_abb, 100*awp))
  except Exception as ex:
    print('WP', label, 'ERR', ex)
