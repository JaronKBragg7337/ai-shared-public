import json, urllib.request, ssl
ctx = ssl.create_default_context()
H = {"User-Agent": "Mozilla/5.0"}

def get(u):
    req = urllib.request.Request(u, headers=H)
    return json.loads(urllib.request.urlopen(req, timeout=25, context=ctx).read())

# All in-progress CFB from scoreboard
sb = get("https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard")
live = []
for e in sb.get("events", []):
    comp = e["competitions"][0]
    st = comp["status"]["type"]
    if st.get("state") != "in":
        continue
    eid = e.get("id")
    name = e.get("name", "")
    status = st.get("detail") or st.get("description")
    rows = []
    for c in comp["competitors"]:
        t = c["team"].get("abbreviation") or c["team"].get("shortDisplayName")
        rows.append((c.get("homeAway"), t, c.get("score")))
    live.append((eid, name, status, rows))
    print("LIVE", eid, name, "|", status, rows)

print("---WPs---")
for eid, name, status, rows in live:
    try:
        j = get(f"https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event={eid}")
        wps = j.get("winprobability") or []
        wp = wps[-1] if wps else {}
        hwp = float(wp.get("homeWinPercentage") or 0)
        print(name, "|", status, "| homeWP", round(hwp * 100, 1), "awayWP", round((1 - hwp) * 100, 1), "|", rows)
    except Exception as ex:
        print(name, "WPERR", ex)
