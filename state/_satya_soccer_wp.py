import urllib.request, json
# pull ESPN event details for Lens-Lyon and Malaga-Espanyol if available
for league in ('fra.1','esp.1','ger.1'):
  u=f'https://site.api.espn.com/apis/site/v2/sports/soccer/{league}/scoreboard'
  with urllib.request.urlopen(u, timeout=20) as r:
    d=json.load(r)
  for e in d.get('events',[]):
    comp=e['competitions'][0]
    names=[t['team']['displayName'] for t in comp['competitors']]
    print('EVENT', e.get('id'), names, e.get('name'))
    print(' status', comp['status'])
    # try situation / probability if present
    sit=comp.get('situation') or {}
    print(' situation_keys', list(sit.keys())[:20])
    odds=comp.get('odds')
    if odds: print(' odds', odds[:1] if isinstance(odds,list) else odds)
    for t in comp['competitors']:
      print(' ', t['team']['abbreviation'], 'score', t.get('score'), 'winner', t.get('winner'), 'prob', t.get('probability'))
