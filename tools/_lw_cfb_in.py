import json, urllib.request

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.load(r)

# Full CFB in-progress
d = get("https://site.web.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?dates=20260919&limit=100")
for e in d.get("events", []):
    st = e.get("status", {}).get("type", {})
    if st.get("state") != "in":
        continue
    comps = (e.get("competitions") or [{}])[0]
    teams = []
    for c in comps.get("competitors", []):
        teams.append(f"{c.get('team',{}).get('abbreviation')} {c.get('score')} ({c.get('homeAway')})")
    print(e.get("id"), e.get("shortName"), st.get("detail"), "|", " / ".join(teams))

print("--- summaries ---")
for eid, label in [
    ("401860888", "fresno-sjst"),
    ("401860889", "maybe-jmu"),
]:
    pass

# find fresno / jmu / lsu / montana / boise / sdak by name
for e in d.get("events", []):
    name = (e.get("shortName") or "").lower()
    if any(x in name for x in ("fres", "sjsu", "jmu", "jmu", "james", "sdst", "s dakota", "boise", "mont", "oregst", "lsu", "miss")):
        eid = e["id"]
        st = e.get("status", {}).get("type", {})
        print("MATCH", name, eid, st.get("state"), st.get("detail"))
        try:
            s = get(f"https://site.web.api.espn.com/apis/site/v2/sports/football/college-football/summary?event={eid}")
            comps = ((s.get("header") or {}).get("competitions") or [{}])[0]
            for c in comps.get("competitors", []):
                print(" ", c.get("team", {}).get("abbreviation"), c.get("score"), c.get("homeAway"))
            wpl = s.get("winprobability") or []
            if isinstance(wpl, list) and wpl:
                print("  lastWP", wpl[-1])
        except Exception as ex:
            print("  ERR", ex)
