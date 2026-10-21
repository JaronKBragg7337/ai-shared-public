import urllib.request, json
# EWU / Southern Utah on 20261003 scoreboard
req = urllib.request.Request(
  'https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?dates=20261003&limit=300&groups=80',
  headers={'User-Agent':'Mozilla/5.0'})
# try without groups first full
req = urllib.request.Request(
  'https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?dates=20261003&limit=300',
  headers={'User-Agent':'Mozilla/5.0'})
data = json.loads(urllib.request.urlopen(req, timeout=20).read())
for ev in data.get('events', []):
  n=ev.get('name','').lower()
  if any(x in n for x in ['eastern washington','uc davis','southern utah','utah tech','fresno','baylor','texas state','cincinnati','san jos','hawai']):
    comp=ev['competitions'][0]; st=comp['status']['type']
    print(ev.get('name'), '|', st.get('detail'), '|', [(c['team']['abbreviation'], c.get('score'), c.get('homeAway')) for c in comp['competitors']])
    eid=ev['id']
    try:
      s=json.loads(urllib.request.urlopen(urllib.request.Request(f'https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event={eid}',headers={'User-Agent':'Mozilla/5.0'}),timeout=15).read())
      w=s.get('winprobability') or []
      if w:
        h=w[-1].get('homeWinPercentage'); home=[c['team']['abbreviation'] for c in comp['competitors'] if c.get('homeAway')=='home'][0]; away=[c['team']['abbreviation'] for c in comp['competitors'] if c.get('homeAway')=='away'][0]
        print(f'  WP home {home}={h:.3f} away {away}={1-h:.3f}')
    except Exception as e:
      print('  wp err', e)
