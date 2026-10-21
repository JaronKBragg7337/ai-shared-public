import urllib.request, re
req=urllib.request.Request('https://www.espn.com/tennis/scoreboard', headers={'User-Agent':'Mozilla/5.0'})
html=urllib.request.urlopen(req,timeout=25).read().decode('utf-8','replace')
for key in ['Inglis','Sonmez','Bai','Fruhvirtova','Fils','Van Assche','Cerundolo','Yunchaokete','Lehecka','Bergs']:
    idx=html.lower().find(key.lower())
    print(key, 'found' if idx>=0 else 'NO', (html[max(0,idx-80):idx+120].replace('\n',' ') if idx>=0 else ''))
print('len', len(html))
# try __espnfitt__ or similar
m=re.search(r'window\[\'__espnfitt__\'\]\s*=\s*(\{.*?\});\s*</script>', html)
if not m:
 m=re.search(r'"scoreboard":\{', html)
 print('scoreboard marker', bool(m))
else:
 print('espnfitt found', len(m.group(1)))
