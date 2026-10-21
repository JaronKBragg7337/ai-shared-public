import urllib.request, re, json
req=urllib.request.Request('https://www.espn.com/tennis/scoreboard', headers={'User-Agent':'Mozilla/5.0'})
html=urllib.request.urlopen(req,timeout=25).read().decode('utf-8','replace')
m=re.search(r"window\['__espnfitt__'\]\s*=\s*(\{.*?\});\s*</script>", html)
raw=m.group(1)
# extract competition objects containing our names
for key in ['Bai Zhuoxuan','Arthur Fils','Juan Manuel Cerundolo','Maddison','Inglis','Lehecka','Sonmez']:
    i=raw.find(key)
    if i<0:
        print(key, 'MISSING'); continue
    # walk back to nearest "status"
    chunk=raw[max(0,i-800):i+500]
    st=re.search(r'"status":\{([^}]{0,200})\}', chunk)
    lines=re.findall(r'"nm":"([^"]+)".*?"lnescrs":(\[[^\]]*\])', chunk)
    print('==', key)
    if st: print(' status', st.group(1)[:200])
    for nm, ls in lines:
        print(' ', nm, ls)
    print()
