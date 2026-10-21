import urllib.request, re, json
req=urllib.request.Request('https://www.espn.com/tennis/scoreboard', headers={'User-Agent':'Mozilla/5.0'})
html=urllib.request.urlopen(req,timeout=25).read().decode('utf-8','replace')
m=re.search(r"window\['__espnfitt__'\]\s*=\s*(\{.*?\});\s*</script>", html)
raw=m.group(1)
# find athlete names near scores via regex on the big blob
for key in ['Inglis','Sonmez','Bai Zhuoxuan','Zhuoxuan Bai','Fruhvirtova','Arthur Fils','Van Assche','Cerundolo','Yunchaokete','Lehecka','Bergs','Maddison']:
    for m2 in re.finditer(re.escape(key), raw):
        print('---', key, 'at', m2.start())
        print(raw[max(0,m2.start()-200):m2.start()+300][:500])
        print()
        break
