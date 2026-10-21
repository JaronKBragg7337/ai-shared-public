import json, urllib.request, subprocess, sys

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.load(r)

d = fetch("https://site.web.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard")
for e in d["events"]:
    c = e["competitions"][0]
    if c["status"]["type"].get("state") != "in":
        continue
    situ = c.get("situation") or {}
    lp = situ.get("lastPlay") or {}
    p = lp.get("probability") or {}
    comps = {x["homeAway"]: x for x in c["competitors"]}
    a, h = comps["away"], comps["home"]
    txt = (lp.get("text") or "")[:90]
    print(
        f"{e['shortName']}: {a['team']['abbreviation']} {a['score']}-{h['score']} {h['team']['abbreviation']} | "
        f"{c['status']['type']['detail']} | awayWP={p.get('awayWinPercentage')} homeWP={p.get('homeWinPercentage')} | {txt}"
    )

print("---BOOKS---")
for slug in [
    "aec-nfl-min-tb-2026-09-27",
    "aec-nfl-bal-dal-2026-09-27",
    "aec-nfl-lv-no-2026-09-27",
    "aec-nfl-ari-sf-2026-09-27",
]:
    subprocess.run([sys.executable, r"C:\Users\lilli\AI-Shared\tools\desk.py", "book", slug])
print("---HELP---")
subprocess.run([sys.executable, r"C:\Users\lilli\AI-Shared\tools\desk-trade.py", "--help"])
