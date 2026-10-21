import re, urllib.request, json
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0.0.0 Safari/537.36"
url = "https://www.scoremania.com/tennis-live-centre/match-detail/harold-mayot-vs-murphy-cassone/37127/info"
req = urllib.request.Request(url, headers={"User-Agent": UA})
html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")
# find JSON-looking blobs with Mayot/score
for pat in [
    r"__NEXT_DATA__\s*=\s*(\{.*?\})\s*;", 
    r"window\.__INITIAL_STATE__\s*=\s*(\{.*?\});",
    r"\"homeScore\"\s*:\s*\{[^}]+\}",
    r"\"period3\"[^,]{0,40}",
    r"\"games\"[^,]{0,40}",
    r"currentGame[^,]{0,80}",
    r"setScores[^,]{0,120}",
]:
    ms = re.findall(pat, html, flags=re.I|re.S)
    print(pat, "count", len(ms))
    for m in ms[:3]:
        s = m if isinstance(m,str) else str(m)
        print(s[:400])
# search raw for period3 / game numbers near
idx = html.lower().find("mayot")
print("first mayot idx", idx)
# extract all script type application/json
for m in re.finditer(r"<script[^>]*type=[\"\']application/json[\"\'][^>]*>(.*?)</script>", html, flags=re.I|re.S):
    body = m.group(1)
    if "Mayot" in body or "score" in body.lower():
        print("JSON SCRIPT", body[:500])
# look for numbers pattern like 5,6,x
for m in re.finditer(r"(?:period|set|game)[A-Za-z0-9_\"\']{0,20}[:\"\s]+(\d+)", html, flags=re.I):
    pass
nums = re.findall(r"\"(?:period1|period2|period3|current|display|game|set1|set2|set3)\"\s*:\s*\"?(\d+)\"?", html, flags=re.I)
print("score fields", nums[:50])
# dump lines containing 3rd or period
for line in html.split("\n"):
    if any(x in line.lower() for x in ["period3", "set3", "third", "\"games\"", "gameScore", "currentScore"]):
        if len(line) < 500:
            print("LINE", line.strip()[:400])
