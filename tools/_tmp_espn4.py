import urllib.request, re
req = urllib.request.Request('https://www.espn.com/tennis/scoreboard', headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(req, timeout=25).read().decode('utf-8', 'ignore')
i = html.find('Malaika Rapolu')
print('idx', i)
if i > 0:
    # find status detail near competitor block in espnfitt
    j = html.find('183726')
    print('event', j)
    chunk = html[j:j+800] if j>0 else html[i-100:i+500]
    print(chunk[:800])
text = re.sub(r'<[^>]+>', ' ', html[max(0,i-80):i+400])
print('TEXT', re.sub(r'\s+', ' ', text)[:300])
