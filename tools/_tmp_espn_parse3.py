import urllib.request, re, json
req=urllib.request.Request('https://www.espn.com/tennis/scoreboard', headers={'User-Agent':'Mozilla/5.0'})
html=urllib.request.urlopen(req,timeout=25).read().decode('utf-8','replace')
m=re.search(r"window\['__espnfitt__'\]\s*=\s*(\{.*?\});\s*</script>", html)
raw=m.group(1)
# Find competition blocks by looking for nm and nearby status with a tighter window using competitor arrays
# Pull all objects that have lnescrs
pat=re.compile(r'\{"id":"(\d+)","status":(\{.*?\}),"date":"([^"]+)".*?"competitors":(\[.*?\]\}\])\}', re.DOTALL)
# simpler: find each nm with lnescrs pair sequences of 2 competitors
blocks=re.finditer(r'"status":(\{[^{}]+\}).{0,120}?"competitors":\[(\{.*?\}\]),(\{.*?\})\]', raw)
count=0
for b in blocks:
    comps=b.group(2)+'],'+b.group(3)
    names=re.findall(r'"nm":"([^"]+)"', comps)
    scores=re.findall(r'"nm":"([^"]+)".*?"lnescrs":(\[[^\]]*\])', comps)
    joined=' '.join(names)
    if any(x in joined for x in ['Bai','Fruhvirtova','Fils','Van Assche','Cerundolo','Yunchaokete','Inglis','Sonmez','Lehecka','Bergs']):
        print(b.group(1))
        for nm,ls in scores:
            print(' ', nm, ls)
        print()
        count+=1
print('matched', count)
