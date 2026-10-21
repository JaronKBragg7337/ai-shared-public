import urllib.request, json, os, glob
# ESPN summary for FSU-LOU and COL-MRST
for gid in ['401780285','401868265','401780284']:
  try:
    u=f'https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event={gid}'
    d=json.load(urllib.request.urlopen(u, timeout=15))
  except Exception as e:
    print('fail',gid,e); continue
  h=d.get('header',{}); print('EVENT', h.get('id'), h.get('competitions',[{}])[0].get('competitors'))
  sit=d.get('situation') or {}
  print('situation keys', list(sit.keys())[:20] if isinstance(sit,dict) else sit)
  wp=d.get('winprobability') or []
  if wp: print('wp last', wp[-1])
  # also predictor
  pred=d.get('predictor') or {}
  print('predictor', pred)
  comps=h.get('competitions',[{}])[0]
  print('status', comps.get('status',{}).get('type',{}).get('detail'))
  for t in comps.get('competitors',[]):
    print(t.get('homeAway'), t['team']['abbreviation'], t.get('score'), 'prob', t.get('probability'))
  print('---')
# find open positions files
for pat in [r'C:\Users\lilli\AI-Shared\state\*open*', r'C:\Users\lilli\AI-Shared\state\*position*', r'C:\Users\lilli\AI-Shared\state\*hold*', r'C:\Users\lilli\AI-Shared\state\desk*', r'C:\Users\lilli\AI-Shared\ledger\*', r'C:\Users\lilli\AI-Shared\tools\desk*']:
  print('PAT', pat)
