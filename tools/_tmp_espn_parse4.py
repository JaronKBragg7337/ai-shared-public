import urllib.request, re
req=urllib.request.Request('https://www.espn.com/tennis/scoreboard', headers={'User-Agent':'Mozilla/5.0'})
html=urllib.request.urlopen(req,timeout=25).read().decode('utf-8','replace')
m=re.search(r"window\['__espnfitt__'\]\s*=\s*(\{.*?\});\s*</script>", html)
raw=m.group(1)
for key in ['Bai Zhuoxuan','Arthur Fils','Juan Manuel Cerundolo','Luca Van Assche','Bu Yunchaokete','Linda Fruhvirtova']:
    i=0
    while True:
        j=raw.find('"nm":"%s"'%key, i)
        if j<0: break
        print(key, raw[j:j+180])
        i=j+1
        break
# status near Bai
j=raw.find('Bai Zhuoxuan')
print('BAI CONTEXT STATUS', re.findall(r'"description":"([^"]+)".{0,40}"detail":"([^"]+)"', raw[max(0,j-1000):j+200])[-3:])
