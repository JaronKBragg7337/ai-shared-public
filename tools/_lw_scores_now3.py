import json, urllib.request

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.load(r)

def dump(name, url, want=None):
    try:
        d = get(url)
    except Exception as ex:
        print(name, "ERR", ex)
        return
    evs = d.get("events", [])
    print("===", name, "n=", len(evs), "===")
    for e in evs:
        st = e.get("status", {}).get("type", {})
        comps = (e.get("competitions") or [{}])[0]
        teams = []
        home_wp = None
        for c in comps.get("competitors", []):
            ab = c.get("team", {}).get("abbreviation", "?")
            sc = c.get("score", "")
            ha = c.get("homeAway", "")
            teams.append(f"{ab} {sc} ({ha})")
            if ha == "home":
                home_wp = c.get("probability", {}).get("winPercentage") if isinstance(c.get("probability"), dict) else None
                if home_wp is None:
                    home_wp = c.get("records")  # noop
        # situation / win probability alternate paths
        sit = comps.get("situation") or {}
        last = comps.get("lastPlay") or {}
        # ESPN sometimes puts winProbability in competitors as float via geoBroadcasts etc
        probs = []
        for c in comps.get("competitors", []):
            ab = c.get("team", {}).get("abbreviation", "?")
            for k in ("probability", "winProbability"):
                if k in c:
                    probs.append(f"{ab}:{c[k]}")
        # try summary endpoint field on competition
        wp_field = comps.get("probability") or comps.get("winProbability")
        line = " | ".join([
            e.get("shortName") or e.get("name", ""),
            st.get("state", ""),
            st.get("detail", ""),
            " / ".join(teams),
            f"wp={wp_field}" if wp_field else "",
            " ".join(probs) if probs else "",
        ])
        if want:
            key = (e.get("shortName") or e.get("name") or "").lower()
            if not any(w.lower() in key for w in want):
                continue
        print(line)

# CFB
dump("cfb", "https://site.web.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?dates=20260919&limit=100",
     want=["fresno", "san jose", "james madison", "south dakota", "boise", "purdue", "ucla", "montana", "oregon st", "lsu", "ole miss", "virginia tech", "maryland"])
dump("mlb", "https://site.web.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard?dates=20260919",
     want=["nyy", "ari", "mia", "sd", "min", "laa", "sf", "lad"])

# Also fetch game summaries for WP on key games
summaries = [
    ("frest-sjst", "https://site.web.api.espn.com/apis/site/v2/sports/football/college-football/summary?event="),
    ("jmad-sdst", "https://site.web.api.espn.com/apis/site/v2/sports/football/college-football/summary?event="),
]
# first get event ids from scoreboard
try:
    d = get("https://site.web.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?dates=20260919&limit=100")
    for e in d.get("events", []):
        name = (e.get("shortName") or e.get("name") or "").lower()
        eid = e.get("id")
        if any(x in name for x in ("fresno", "san jos", "james madison", "s dakota st", "south dakota st", "purdue", "ucla")):
            print("EVENT", name, eid)
            try:
                s = get(f"https://site.web.api.espn.com/apis/site/v2/sports/football/college-football/summary?event={eid}")
                wp = s.get("winprobability") or s.get("predictor") or {}
                # header
                header = (s.get("header") or {})
                comps = ((header.get("competitions") or [{}])[0])
                print("  status", (header.get("competitions") or [{}])[0].get("status", {}).get("type", {}).get("detail"))
                for c in comps.get("competitors", []):
                    print("  ", c.get("team", {}).get("abbreviation"), c.get("score"), "homeAway", c.get("homeAway"))
                # win prob plays last
                wpl = s.get("winprobability") or []
                if isinstance(wpl, list) and wpl:
                    last = wpl[-1]
                    print("  lastWP", last)
                elif wp:
                    print("  wpobj", json.dumps(wp)[:500])
                #predictor
                pred = s.get("predictor") or {}
                if pred:
                    print("  predictor", json.dumps(pred)[:400])
            except Exception as ex:
                print("  summary ERR", ex)
except Exception as ex:
    print("cfb id ERR", ex)

try:
    d = get("https://site.web.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard?dates=20260919")
    for e in d.get("events", []):
        name = (e.get("shortName") or e.get("name") or "").lower()
        eid = e.get("id")
        if any(x in name for x in ("nyy", "ari", "mia", "sd", "min", "laa")):
            print("MLB EVENT", name, eid)
            try:
                s = get(f"https://site.web.api.espn.com/apis/site/v2/sports/baseball/mlb/summary?event={eid}")
                header = (s.get("header") or {})
                comps = ((header.get("competitions") or [{}])[0])
                print("  status", comps.get("status", {}).get("type", {}).get("detail"))
                for c in comps.get("competitors", []):
                    print("  ", c.get("team", {}).get("abbreviation"), c.get("score"), c.get("homeAway"))
                wpl = s.get("winprobability") or []
                if isinstance(wpl, list) and wpl:
                    print("  lastWP", wpl[-1])
                sit = comps.get("situation") or {}
                if sit:
                    print("  sit keys", list(sit.keys())[:20], "outs", sit.get("outs"), "inning", comps.get("status", {}).get("period"))
            except Exception as ex:
                print("  mlb summary ERR", ex)
except Exception as ex:
    print("mlb id ERR", ex)
