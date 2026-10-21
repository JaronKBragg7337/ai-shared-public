import json, urllib.request, ssl

ctx = ssl.create_default_context()
UA = {"User-Agent": "Mozilla/5.0"}

def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=25, context=ctx) as r:
        return json.load(r)

# CFB scoreboard
sb = get("https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?dates=20261003&limit=100")
want = ("UCF", "Houston", "Alabama", "Mississippi State", "Boston College", "SMU",
        "Notre Dame", "North Carolina", "Michigan", "Minnesota", "West Virginia",
        "Iowa State", "Navy", "Air Force", "Stanford", "Wake", "Syracuse", "UConn")
for e in sb.get("events", []):
    name = e.get("name", "")
    if not any(w in name for w in want):
        continue
    comp = e["competitions"][0]
    st = comp.get("status", {}).get("type", {}).get("detail", "")
    print("GAME", name, "|", st)
    eid = e["id"]
    try:
        sm = get(f"https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event={eid}")
        wps = sm.get("winprobability") or []
        if wps:
            p = wps[-1]
            print("  homeWinPct", round(float(p.get("homeWinPercentage", 0)) * 100, 1))
        comps = sm.get("header", {}).get("competitions", [{}])[0].get("competitors", [])
        for c in comps:
            print(" ", c.get("team", {}).get("abbreviation"), "score", c.get("score"),
                  c.get("homeAway"), "prob", c.get("probability"))
    except Exception as ex:
        print("  err", ex)

# Cricket: try ESPN Cricinfo match via series
print("---CRICKET---")
for url in [
    "https://hs-consumer-api.espncricinfo.com/v1/pages/match/details?lang=en&seriesId=1529215&matchId=1529229&latest=true",
    "https://www.espncricinfo.com/ci/engine/match/1529229.json",
]:
    try:
        data = get(url)
        print("ok", url[:60])
        print(json.dumps(data)[:2500])
        break
    except Exception as ex:
        print("fail", url[:50], ex)
