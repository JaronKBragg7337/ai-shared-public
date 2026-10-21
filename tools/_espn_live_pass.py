import json, urllib.request

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=40) as r:
        return json.load(r)

want = (
    "Cincinnati", "Arizona", "San Jose", "Hawai", "Baylor", "Fresno",
    "Texas State", "Eastern Washington", "UC Davis", "Washington State",
    "San Diego State", "Arizona State",
)
urls = [
    "https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?limit=300",
    "https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?groups=80&limit=300",
    "https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?groups=81&limit=300",
]
seen = set()
for url in urls:
    try:
        data = get(url)
    except Exception as e:
        print("ERR", url, e)
        continue
    for e in data.get("events", []):
        eid = e.get("id")
        if eid in seen:
            continue
        name = e.get("name", "")
        if not any(w in name for w in want):
            continue
        seen.add(eid)
        c = e["competitions"][0]
        comps = c["competitors"]
        home = next(x for x in comps if x["homeAway"] == "home")
        away = next(x for x in comps if x["homeAway"] == "away")
        st = c["status"]
        sit = c.get("situation") or {}
        lp = sit.get("lastPlay") or {}
        prob = lp.get("probability") or sit.get("probability") or {}
        print(
            f"{away['team']['abbreviation']} {away.get('score')} @ "
            f"{home['team']['abbreviation']} {home.get('score')} | "
            f"{st['type'].get('detail')} clock={st.get('displayClock')} q={st.get('period')}"
        )
        print(
            f"  id={eid} homeWP={prob.get('homeWinPercentage')} "
            f"awayWP={prob.get('awayWinPercentage')}"
        )
        if sit:
            print(
                f"  down={sit.get('down')} dist={sit.get('distance')} "
                f"yard={sit.get('yardLine')} poss={sit.get('possession')}"
            )

# summary endpoints for known game ids if needed
for gid in list(seen)[:8]:
    try:
        s = get(f"https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event={gid}")
        drives = (s.get("drives") or {}).get("current") or {}
        plays = s.get("plays") or {}
        wp = None
        # winprobability array
        wparr = s.get("winprobability") or []
        if wparr:
            last = wparr[-1]
            wp = last
        hdr = s.get("header") or {}
        comps = ((hdr.get("competitions") or [{}])[0].get("competitors") or [])
        scores = []
        for x in comps:
            scores.append(f"{x.get('team',{}).get('abbreviation')}={x.get('score')} homeAway={x.get('homeAway')}")
        print(f"SUMMARY {gid}: {'; '.join(scores)} wp_last={wp}")
    except Exception as e:
        print("SUMERR", gid, e)
