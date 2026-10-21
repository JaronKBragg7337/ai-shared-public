import urllib.request, json, sys

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    return json.load(urllib.request.urlopen(req, timeout=25))

print("=== LIVE CFB ===")
for dates in ["20261002", "20261003"]:
    data = get(f"https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?dates={dates}&limit=300")
    for ev in data.get("events") or []:
        comp = (ev.get("competitions") or [{}])[0]
        st = (comp.get("status") or {}).get("type", {})
        if st.get("state") != "in":
            continue
        scores = []
        for c in comp.get("competitors") or []:
            scores.append(f"{c.get('team',{}).get('abbreviation')} {c.get('score')} ({c.get('homeAway')})")
        print(dates, ev.get("name"), "|", st.get("detail"), "|", " / ".join(scores))
        sit = comp.get("situation") or {}
        lp = sit.get("lastPlay") or {}
        print("  lastPlay", (lp.get("text") or "")[:140])
        print("  prob", lp.get("probability"))

print("=== MTST DETAIL ===")
found = False
for dates in ["20261002", "20261003"]:
    data = get(f"https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?dates={dates}&limit=300")
    for ev in data.get("events") or []:
        name = ev.get("name", "")
        if "Montana State" not in name:
            continue
        found = True
        eid = ev.get("id")
        comp = (ev.get("competitions") or [{}])[0]
        st = (comp.get("status") or {}).get("type", {})
        print("NAME", name, "eid", eid)
        print("STATUS", st.get("detail"), st.get("state"), st.get("completed"))
        for c in comp.get("competitors") or []:
            print(" ", c.get("team", {}).get("abbreviation"), c.get("score"), c.get("homeAway"), "winner", c.get("winner"))
        try:
            s = get(f"https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event={eid}")
            wp = s.get("winprobability") or []
            if wp:
                print("LAST_WP", wp[-1])
            sit = s.get("situation") or {}
            print("SIT", sit.get("downDistanceText"), "poss", sit.get("possession"))
            lp = sit.get("lastPlay") or {}
            print("LP", (lp.get("text") or "")[:160], "prob", lp.get("probability"))
        except Exception as e:
            print("summary err", e)
if not found:
    print("Montana State not on scoreboard")

print("=== DONE ===")
