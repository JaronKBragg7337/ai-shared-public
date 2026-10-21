import urllib.request, re
req = urllib.request.Request('https://www.espn.com/tennis/scoreboard', headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(req, timeout=25).read().decode('utf-8', 'ignore')
m = re.search(r"window\['__espnfitt__'\]\s*=\s*(\{.*?\});\s*</script>", html, re.S)
raw = m.group(1)
for name in ['Malaika Rapolu', 'Pavel Kotov', 'Harold Mayot', 'Tom Gentzsch']:
    i = raw.find(name)
    print('====', name, i)
    if i > 0:
        print(raw[i-350:i+550])
        print()
