import urllib.request, re, json
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

def get(url):
    req = urllib.request.Request(url, headers=UA)
    return urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")

p = get("https://livescore.tennis365.com/")
# find hrefs mentioning targets
for L in re.findall(r'href="([^"]+)"', p):
    if re.search(r"templeton|pareja|frodin|cazacu|vrba|maklakova|olivieri|andrade|lucsil|ence|aimhaus|jordan.?lee|khomon", L, re.I):
        print("LINK", L)

# strip scripts then lines
text = re.sub(r"<script[\s\S]*?</script>", " ", p, flags=re.I)
text = re.sub(r"<[^>]+", "\n", text)
lines = [L.strip() for L in text.splitlines() if L.strip() and L.strip() != "&nbsp;"]

# print block around Andrade Da Silva and Marcondes and any Pareja
for name in ["Andrade Da Silva", "Marcondes", "Pareja", "Frodin", "Cazacu", "Maklakova", "Jordan Lee", "Lee, Jordan"]:
    for i, L in enumerate(lines):
        if name.lower() in L.lower():
            print("====", name, "at", i)
            for j in range(max(0, i-4), min(len(lines), i+15)):
                print(f"{j}: {lines[j][:160]}")
            break

# ESPN MLB CWS-HOU detail
print("==== ESPN MLB ====")
d = json.load(urllib.request.urlopen("https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard", timeout=20))
for e in d.get("events", []):
    if "White Sox" in e.get("name", "") or "Astros" in e.get("name", ""):
        s = e["status"]["type"]
        comps = e["competitions"][0]
        print(e["name"], s.get("detail"), s.get("state"))
        for c in comps["competitors"]:
            print(" ", c["team"]["abbreviation"], c.get("score"), "homeAway", c.get("homeAway"))
        sit = comps.get("situation") or {}
        print(" situation", {k: sit.get(k) for k in ("outs", "balls", "strikes", "onFirst", "onSecond", "onThird", "lastPlay") if k in sit or True})

print("==== ESPN NHL FLA ====")
d = json.load(urllib.request.urlopen("https://site.api.espn.com/apis/site/v2/sports/hockey/nhl/scoreboard", timeout=20))
for e in d.get("events", []):
    if "Panthers" in e.get("name", "") or "Hurricanes" in e.get("name", ""):
        s = e["status"]["type"]
        print(e["name"], s.get("detail"), s.get("state"), [(c["team"]["abbreviation"], c.get("score")) for c in e["competitions"][0]["competitors"]])
