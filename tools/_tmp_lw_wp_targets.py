import urllib.request, json

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.load(r)

def cfb_wp(eid, label):
    try:
        # try site.api then site.web.api
        for base in (
            "https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary",
            "https://site.web.api.espn.com/apis/site/v2/sports/football/college-football/summary",
        ):
            try:
                d = get(f"{base}?event={eid}")
                break
            except Exception as e:
                last = e
                d = None
        if d is None:
            print(label, "ERR", last)
            return
        wp = d.get("winprobability") or []
        last = wp[-1] if wp else {}
        h = d.get("header") or {}
        comps = (h.get("competitions") or [{}])[0]
        teams = []
        for c in comps.get("competitors", []):
            teams.append(f"{c['team']['abbreviation']} {c.get('score','?')} ({c['homeAway']})")
        st = (comps.get("status") or {}).get("type", {})
        print(f"{label} | {' vs '.join(teams)} | {st.get('detail')} | homeWinPct={last.get('homeWinPercentage')} away~={None if last.get('homeWinPercentage') is None else 1-float(last.get('homeWinPercentage'))}")
    except Exception as e:
        print(label, "ERR", e)

# scoreboard for JMU/VT/LSU
for dates in ("20260919", "20260920"):
    try:
        data = get(f"https://site.web.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?dates={dates}&limit=300")
    except Exception as e:
        print("SB", dates, e)
        continue
    for e in data.get("events", []):
        abbs = [c["team"]["abbreviation"] for c in e["competitions"][0]["competitors"]]
        if any(a in abbs for a in ("JMU", "SDSU", "VT", "MD", "LSU", "MISS")):
            st = e["competitions"][0]["status"]["type"]
            print("FOUND", e["id"], e.get("shortName"), abbs, st.get("detail"), "state", st.get("state"))
            if st.get("state") == "in":
                cfb_wp(e["id"], e.get("shortName"))
