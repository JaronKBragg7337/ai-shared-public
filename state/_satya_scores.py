import json, urllib.request

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.load(r)

def show_board(url, want=None):
    data = fetch(url)
    for e in data.get("events", []):
        name = e.get("name", "")
        if want and not any(w.lower() in name.lower() for w in want):
            continue
        st = e.get("status", {}).get("type", {})
        comps = e.get("competitions", [{}])[0]
        parts = []
        for t in comps.get("competitors", []):
            team = t.get("team", {})
            ab = team.get("abbreviation", "?")
            sc = t.get("score", "")
            home = t.get("homeAway")
            wp = None
            for cur in (t.get("statistics") or []):
                pass
            # win probability often under competitor.prob or situation
            parts.append(f"{ab}({home})={sc}")
        # probability from competitors
        probs = []
        for t in comps.get("competitors", []):
            ab = t.get("team", {}).get("abbreviation", "?")
            p = t.get("probability") or t.get("winProbability")
            if p is None and isinstance(t.get("statistics"), list):
                for s in t["statistics"]:
                    if str(s.get("name","")).lower().find("win") >= 0:
                        p = s.get("displayValue") or s.get("value")
            probs.append(f"{ab}:{p}")
        sit = comps.get("situation") or {}
        print(name)
        print("  score:", " | ".join(parts), "|", st.get("description"), st.get("detail"))
        print("  probs:", ", ".join(probs))
        if sit:
            print("  sit:", {k: sit.get(k) for k in ("clock","downDistanceText","possessionText","isRedZone") if k in sit or True})
        # also dump winprobability path if present
        for t in comps.get("competitors", []):
            if "probability" in t:
                print("  rawprob", t.get("team",{}).get("abbreviation"), t.get("probability"))

print("=== CFB ===")
show_board("https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard", ["Florida State", "Louisville", "Columbia", "Marist", "Iowa", "Washington", "BYU", "Iowa State"])
print("=== NHL ===")
show_board("https://site.api.espn.com/apis/site/v2/sports/hockey/nhl/scoreboard", ["Rangers", "Capitals", "Penguins", "Blue Jackets", "Kraken", "Red Wings"])
print("=== WNBA ===")
show_board("https://site.api.espn.com/apis/site/v2/sports/basketball/wnba/scoreboard", ["Dream", "Liberty"])
