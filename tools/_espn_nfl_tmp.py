import urllib.request, json
u = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
d = json.load(urllib.request.urlopen(u, timeout=20))
for e in d.get("events", []):
    s = e["status"]["type"]
    comp = e["competitions"][0]
    teams = comp["competitors"]
    home = next(t for t in teams if t["homeAway"] == "home")
    away = next(t for t in teams if t["homeAway"] == "away")
    wp = ""
    for t in teams:
        if "situation" in comp:
            pass
        prob = t.get("probability", {}) or {}
        # try winPercent
        w = t.get("records")
    # win probability from competitor if present
    awp = away.get("probability", away.get("stats"))
    detail = s.get("detail", "")
    print("%s %s @ %s %s | %s | state=%s" % (
        away["team"]["abbreviation"], away["score"],
        home["team"]["abbreviation"], home["score"],
        detail, s.get("state")))
    # print win probs if available
    for t in teams:
        if "probability" in t:
            print("  WP %s: %s" % (t["team"]["abbreviation"], t["probability"]))
