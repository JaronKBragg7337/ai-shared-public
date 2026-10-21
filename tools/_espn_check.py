import urllib.request, json
url = "https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard"
with urllib.request.urlopen(url, timeout=20) as r:
    data = json.load(r)
want = ["indiana", "nebraska", "south carolina", "florida", "north carolina", "pittsburgh", "texas a&m", "missouri", "oklahoma state", "ucf"]
for ev in data.get("events", []):
    name = ev.get("name", "")
    short = ev.get("shortName", "")
    low = (name + " " + short).lower()
    if not any(w in low for w in want):
        continue
    comp = ev["competitions"][0]
    st = comp["status"]["type"]
    status = st.get("detail") or st.get("description")
    parts = []
    for c in comp["competitors"]:
        ha = "home" if c["homeAway"] == "home" else "away"
        parts.append("%s %s (%s)" % (c["team"]["abbreviation"], c["score"], ha))
    print("%s | %s | %s" % (short, status, " - ".join(parts)))
