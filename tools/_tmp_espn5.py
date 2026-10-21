import urllib.request, re, json
req = urllib.request.Request('https://www.espn.com/tennis/scoreboard', headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(req, timeout=25).read().decode('utf-8', 'ignore')
m = re.search(r"window\['__espnfitt__'\]\s*=\s*(\{.*?\});\s*</script>", html, re.S)
raw = m.group(1)
# find the 183726 competition object
i = raw.find('"183726"')
print(raw[i:i+900])
