import urllib.request, re, json
req = urllib.request.Request(
    'https://www.espn.com/tennis/scoreboard',
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
)
html = urllib.request.urlopen(req, timeout=25).read().decode('utf-8', 'ignore')
# find espnfitt JSON
m = re.search(r"window\['__espnfitt__'\]\s*=\s*(\{.*?\});\s*</script>", html, re.S)
if not m:
    m = re.search(r'"scoreboard"\s*:\s*(\{)', html)
    print('fallback scoreboard start', bool(m))
else:
    raw = m.group(1)
    print('espnfitt len', len(raw))
    open(r'C:\Users\lilli\AI-Shared\tools\_tmp_espn.json','w',encoding='utf-8').write(raw[:2000000])
    print('wrote partial')
# simpler: extract match cards containing Rapolu
idx = html.find('Malaika Rapolu')
print('idx', idx)
chunk = html[idx-3000:idx+5000]
# find linescores
for pat in [r'linescores[^\]]{0,800}\]', r'"displayValue":"[0-9]+"', r'"period":[0-9]+', r'In Progress[^<]{0,80}', r'2nd Set[^<]{0,200}']:
    for mm in re.finditer(pat, chunk):
        print('HIT', pat[:30], mm.group(0)[:200])
# print readable text of chunk
text = re.sub(r'<script[^>]*>.*?</script>', ' ', chunk, flags=re.S|re.I)
text = re.sub(r'<[^>]+>', '|', text)
text = re.sub(r'\|+','|', text)
text = re.sub(r'\s+',' ', text)
print('TEXT', text[:2000])
