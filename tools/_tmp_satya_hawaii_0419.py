import json, urllib.request
j=json.load(urllib.request.urlopen('https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?groups=80&limit=200', timeout=25))
for e in j.get('events',[]):
  c=e['competitions'][0]
  names=' / '.join(x['team']['displayName'] for x in c['competitors'])
  low=names.lower()
  if 'hawaii' in low or 'arizona state' in low:
    print(c['status']['type']['detail'], '|', names, '|', ' '.join('%s=%s'%(x['team']['abbreviation'],x['score']) for x in c['competitors']), '|', c['status']['type']['state'])
print('done')
