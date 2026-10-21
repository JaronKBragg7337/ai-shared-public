import json, urllib.request, os
from datetime import date

def get(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json"
    })
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.loads(r.read().decode())

def espn(path, label):
    for host in ("site.web.api.espn.com", "cdn.espn.com", "site.api.espn.com"):
        url = f"https://{host}/apis/site/v2/sports/{path}/scoreboard"
        try:
            data = get(url)
            print(f"OK {label} via {host}")
            for e in data.get("events", []):
                c = e["competitions"][0]
                st = c["status"]["type"]
                state = st.get("state", "")
                name = st.get("name", "")
                if state not in ("in", "halftime") and "PROGRESS" not in name and "HALF" not in name and "END" not in name:
                    continue
                teams = sorted(c["competitors"], key=lambda x: 0 if x.get("homeAway")=="away" else 1)
                line = " - ".join(f"{t['team'].get('abbreviation','?')} {t.get('score','?')}" for t in teams)
                print(f"  {e.get('shortName')} | {line} | {st.get('detail')} | {name}")
            return
        except Exception as ex:
            print(f"ERR {label} {host}: {ex}")

espn("football/nfl", "NFL")
espn("soccer/usa.1", "MLS")
espn("soccer/mex.1", "LMX")
espn("basketball/wnba", "WNBA")
espn("hockey/nhl", "NHL")
espn("tennis/wta", "WTA")

d = date.today().isoformat()
url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&date={d}&hydrate=linescore,team"
try:
    data = get(url)
    print("OK MLB")
    for dateblk in data.get("dates", []):
        for g in dateblk.get("games", []):
            st = g.get("status", {}).get("detailedState", "?")
            if "Progress" not in st and st not in ("Warmup", "Delayed"):
                continue
            ls = g.get("linescore", {})
            aw = g["teams"]["away"]["team"]["abbreviation"]
            hm = g["teams"]["home"]["team"]["abbreviation"]
            ar = ls.get("teams", {}).get("away", {}).get("runs", "?")
            hr = ls.get("teams", {}).get("home", {}).get("runs", "?")
            print(f"  {aw}{ar}-{hm}{hr} | {ls.get('inningHalf','')} {ls.get('currentInningOrdinal','')} outs={ls.get('outs','')} | {st}")
except Exception as ex:
    print("ERR MLB", ex)

# try nfl.com scorestrip-ish
try:
    data = get("https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard?limit=100")
    print("espn site.api nfl retry", len(data.get("events",[])))
except Exception as ex:
    print("espn site.api nfl", ex)
