import urllib.request, json
u = "https://statsapi.mlb.com/api/v1/schedule?sportId=1&date=2026-09-20&hydrate=linescore,team"
req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
d = json.load(urllib.request.urlopen(req, timeout=20))
for g in d.get("dates", [{}])[0].get("games", []):
    a = g["teams"]["away"]; h = g["teams"]["home"]; ls = g.get("linescore", {})
    aa = a["team"].get("abbreviation", a["team"]["name"])
    ha = h["team"].get("abbreviation", h["team"]["name"])
    print(f"{aa} {a.get('score','?')} @ {ha} {h.get('score','?')} | {g['status']['detailedState']} inning={ls.get('currentInning','?')} {ls.get('inningState','')}")
