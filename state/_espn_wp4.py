import json, urllib.request

def get(u):
    r = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
    return json.load(urllib.request.urlopen(r, timeout=25))

d = get('https://site.web.api.espn.com/apis/site/v2/sports/football/college-football/summary?event=401869842')
wp = d.get('winprobability', [])
hdr = d['header']['competitions'][0]
teams = [(t['team']['abbreviation'], t.get('score'), t['homeAway']) for t in hdr['competitors']]
print('status', hdr['status']['type']['detail'])
print('teams', teams)
print('homeWP last', wp[-1] if wp else None)
print('awayWP', (1.0 - wp[-1]['homeWinPercentage']) if wp else None)
