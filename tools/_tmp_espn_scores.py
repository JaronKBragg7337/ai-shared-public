import urllib.request, json
urls = [
  'https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard',
  'https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?groups=80',
]
keys = {'CCU','MRSH','UAB','MEM','USC','PSU','ALA','UGA','LSU','UK','KU','UTAH','NILL','AFA'}
seen = set()
for url in urls:
  try:
    j = json.load(urllib.request.urlopen(url, timeout=20))
  except Exception as e:
    print('ERR', url, e)
    continue
  for e in j.get('events', []):
    eid = e.get('id')
    if eid in seen:
      continue
    c = e['competitions'][0]
    abs_ = [x['team']['abbreviation'] for x in c['competitors']]
    if not keys.intersection(abs_):
      continue
    seen.add(eid)
    parts = []
    for x in sorted(c['competitors'], key=lambda t: t['homeAway'] != 'away'):
      parts.append(f"{x['team']['abbreviation']} {x.get('score','?')}")
    st = c['status']['type'].get('detail','')
    probs = []
    # situation/lastPlay sometimes has win probability
    situ = c.get('situation') or {}
    lp = situ.get('lastPlay') or {}
    # competitor probability fields vary; also check situation.probability
    for x in c['competitors']:
      pr = x.get('probability')
      if isinstance(pr, dict) and 'winPercentage' in pr:
        probs.append(f"{x['team']['abbreviation']}WP{pr['winPercentage']}")
    # ESPN often embeds winprobability in situation
    wp = situ.get('probability')
    if isinstance(wp, (int, float)):
      probs.append(f"situWP{wp}")
    print(e.get('shortName'), '|', ' '.join(parts), '|', st, '|', ' '.join(probs))
