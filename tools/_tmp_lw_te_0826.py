import urllib.request, re
ua={'User-Agent':'Mozilla/5.0'}
html=urllib.request.urlopen(urllib.request.Request('https://www.tennisexplorer.com/matches/?type=all&year=2026&month=09&day=27', headers=ua), timeout=30).read().decode('utf-8','replace')
# find Digvijay / Nordquist / Gaston blocks
for key in ['Digvijay','Nordquist','Gaston','Rublev','Singh D','Pratap']:
  idxs=[m.start() for m in re.finditer(re.escape(key), html, re.I)]
  print(key, 'hits', len(idxs))
  for i in idxs[:3]:
    snip=re.sub(r'<[^>]+>',' ', html[max(0,i-200):i+400])
    snip=re.sub(r'\s+',' ', snip)
    print(' ', snip[:350])
    print(' ---')
