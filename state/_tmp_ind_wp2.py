import urllib.request, re, json, ssl
ctx = ssl.create_default_context()
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"}

def fetch(u):
    req = urllib.request.Request(u, headers=UA)
    return urllib.request.urlopen(req, timeout=25, context=ctx).read().decode("utf-8", "replace")

text = fetch("https://www.cricbuzz.com/live-cricket-scores/151554/ind-vs-wi-3rd-odi-india-vs-west-indies")
m = re.search(r'"winProbability":(\{.*?\})\s*,\s*"', text)
if not m:
    m = re.search(r'winProbability":(\{[^}]+\{[^}]+\}[^}]+\{[^}]+\}[^}]*\})', text)
if m:
    print("WP_RAW", m.group(1)[:500])
else:
    idx = text.find("winProbability")
    print("WP_NEAR", text[idx:idx+400] if idx>=0 else "missing")

# title / batters
t = re.search(r"<title>([^<]+)</title>", text)
print("TITLE", t.group(1) if t else None)
for pat in [r"IND[^<]{0,30}\d{2,3}/\d[^<]{0,20}", r"\"status\":\"[^\"]+\"", r"Last 10 overs[^<]{0,40}"]:
    ms = re.findall(pat, text)
    print("P", pat[:30], ms[:5])

print("\n=== VLR match ===")
html = fetch("https://www.vlr.gg/753463/karmine-corp-vs-nongshim-redforce-valorant-champions-2026-decider-d")
# scores
for m in re.finditer(r'class="match-header-vs-score[^>]*>.*?</div>', html, re.S):
    print("SCOREBLOCK", re.sub(r"<[^>]+>", "|", m.group(0))[:200])
for m in re.finditer(r'match-header-vs-score-wins[^>]*>\s*(\d+)', html):
    print("WINS", m.group(1))
# map scores
maps = re.findall(r'map":\s*"([^"]+)".{0,80}?score":\s*\[(\d+),\s*(\d+)\]', html)
print("MAPS_JSON", maps[:6])
# simpler
for m in re.finditer(r'([A-Za-z][A-Za-z0-9 /]{2,20})\s*</div>\s*<div class="score">\s*(\d+)\s*:\s*(\d+)', html):
    print("MAP", m.groups())
# note live flag
if "mod-live" in html or "LIVE" in html[:5000]:
    print("HAS_LIVE_MARKER")
# extract eta / note
note = re.search(r'match-header-note[^>]*>([^<]+)', html)
print("NOTE", note.group(1).strip() if note else None)
status = re.search(r'match-header-date[^>]*>.*?mod-\w+[^>]*>([^<]+)', html, re.S)
print("STATUS dig", re.findall(r'mod-(live|upcoming|complete)[^>]*>\s*([^<]+)', html)[:5])
# team scores series
print("SERIES", re.findall(r'match-header-vs-score-wins[^>]*>\s*(\d+)\s*<', html)[:4])
