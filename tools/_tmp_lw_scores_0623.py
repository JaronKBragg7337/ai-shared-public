import urllib.request, json, re, html as H

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json,text/html"})
    return urllib.request.urlopen(req, timeout=25).read()

print("=== ESPN WTA/ATP ===")
for path in [
    "https://site.api.espn.com/apis/site/v2/sports/tennis/wta/scoreboard",
    "https://site.api.espn.com/apis/site/v2/sports/tennis/atp/scoreboard",
]:
    try:
        d = json.loads(get(path).decode())
        print(path.split("/")[-2], "events", len(d.get("events") or []))
        for e in d.get("events") or []:
            name = e.get("name") or e.get("shortName") or ""
            comps = (e.get("competitions") or [{}])[0]
            st = ((comps.get("status") or {}).get("type") or {})
            detail = st.get("detail") or st.get("description")
            parts = []
            for c in comps.get("competitors") or []:
                ath = (c.get("athlete") or c.get("team") or {})
                nm = ath.get("displayName") or ath.get("shortName") or "?"
                parts.append(f"{nm}:{c.get('score')}")
            print(" -", name, "|", detail, "|", " / ".join(parts))
    except Exception as ex:
        print("ERR", path, ex)

print("\n=== tennis365 Tomic raw window ===")
url = "https://livescore.tennis365.com/China-ATP-Challenger-Jingshan-Tomic,Bernard-vs-Sun,-Fajing-3381538"
raw = get(url).decode("utf-8", "replace")
# find status words
for pat in [r"Set\s*3", r"Final", r"Completed", r"Retired", r"1\s*-\s*1", r"10", r"match"]:
    print(pat, "count", len(re.findall(pat, raw, re.I)))
text = re.sub(r"<script[\s\S]*?</script>", " ", raw)
text = re.sub(r"<style[\s\S]*?</style>", " ", text)
text = re.sub(r"<[^>]+>", "\n", text)
ls = [l.strip() for l in text.splitlines() if l.strip()]
print("WINDOW 110-160:")
for i, l in enumerate(ls):
    if 110 <= i <= 160:
        print(f"{i}: {l}")

print("\n=== flashscore search stub ===")
try:
    # tennis explorer live
    u = "https://www.tennisexplorer.com/matches/?type=atp-single&year=2026&month=09&day=29"
    t = get(u).decode("utf-8", "replace")
    if "Tomic" in t or "Sun" in t:
        for m in re.finditer(r".{0,40}Tomic.{0,80}", t):
            print(re.sub(r"<[^>]+>", " ", m.group(0))[:120])
    else:
        print("no Tomic on TE day page; len", len(t))
except Exception as ex:
    print("TE ERR", ex)
