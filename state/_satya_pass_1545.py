import urllib.request, json, sys

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    return json.loads(urllib.request.urlopen(req, timeout=25).read())

want = ("Toledo", "Ball State", "Syracuse", "Western Michigan", "Auburn", "Ohio State",
        "Louisville", "Virginia", "Florida State", "California", "UNLV", "Old Dominion",
        "Georgia State", "Akron", "Central Michigan", "Eastern Michigan", "UMass",
        "Bowling Green", "Miami (OH)", "Wyoming", "North Dakota State", "Elon",
        "New Hampshire", "Navy", "Army", "Michigan", "Minnesota", "Houston", "UCF")

url = "https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?dates=20261003&limit=300"
data = get(url)
print("=== CFB ===")
for ev in data.get("events", []):
    name = ev.get("name", "")
    if not any(w in name for w in want):
        continue
    comp = ev["competitions"][0]
    status = comp["status"]["type"]["detail"]
    comps = comp["competitors"]
    home = next(c for c in comps if c["homeAway"] == "home")
    away = next(c for c in comps if c["homeAway"] == "away")
    line = "%s | %s %s-%s %s | %s" % (
        name,
        away["team"]["abbreviation"], away.get("score", "?"),
        home.get("score", "?"), home["team"]["abbreviation"],
        status,
    )
    print(line)
    for c in comps:
        p = c.get("probability") or {}
        if p:
            print("  WP", c["team"]["abbreviation"], json.dumps(p))
    # also check competitor winPercentage fields sometimes elsewhere
    for c in comps:
        for k in ("winprobability", "winProbability"):
            if k in c:
                print("  ", k, c["team"]["abbreviation"], c[k])

# summary predictor API for live games
print("=== SOCCER UEFA NL ===")
for path in (
    "https://site.api.espn.com/apis/site/v2/sports/soccer/uefa.nations/scoreboard?dates=20261003",
):
    try:
        s = get(path)
        for ev in s.get("events", []):
            name = ev.get("name", "")
            comp = ev["competitions"][0]
            status = comp["status"]["type"]["detail"]
            comps = comp["competitors"]
            home = next(c for c in comps if c["homeAway"] == "home")
            away = next(c for c in comps if c["homeAway"] == "away")
            print("%s | %s %s-%s %s | %s" % (
                name, away["team"]["abbreviation"], away.get("score","?"),
                home.get("score","?"), home["team"]["abbreviation"], status))
    except Exception as e:
        print("soccer err", e)

print("=== DONE ===")
