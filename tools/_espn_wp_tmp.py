import urllib.request, json
u = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
d = json.load(urllib.request.urlopen(u, timeout=20))
for e in d.get("events", []):
    s = e["status"]["type"]
    if s.get("state") != "in":
        continue
    comp = e["competitions"][0]
    teams = comp["competitors"]
    home = next(t for t in teams if t["homeAway"] == "home")
    away = next(t for t in teams if t["homeAway"] == "away")
    # situation / win probability
    sit = comp.get("situation") or {}
    # try lastPlay, or probability on competitors
    lines = []
    for t in teams:
        # ESPN sometimes puts winPercentage here via predictor
        pass
    # fetch summary for WP
    eid = e["id"]
    try:
        su = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/summary?event=%s" % eid
        sd = json.load(urllib.request.urlopen(su, timeout=15))
        pred = sd.get("predictor") or {}
        # also winprobability array
        wp_arr = sd.get("winprobability") or []
        last_wp = wp_arr[-1] if wp_arr else {}
        home_wp = last_wp.get("homeWinPercentage")
        away_wp = last_wp.get("awayWinPercentage")
        if home_wp is None and pred:
            # alternate
            ha = pred.get("homeTeam") or {}
            aa = pred.get("awayTeam") or {}
            home_wp = ha.get("gameProjection")
            away_wp = aa.get("gameProjection")
        print("%s %s @ %s %s | %s" % (away["team"]["abbreviation"], away["score"], home["team"]["abbreviation"], home["score"], s.get("detail","")))
        print("  WP away=%s home=%s | lastPlay=%s" % (away_wp, home_wp, (sit.get("lastPlay") or {}).get("text","")[:80] if isinstance(sit.get("lastPlay"), dict) else ""))
        # also check header competitions probability
        for t in teams:
            p = t.get("probability")
            if p: print("  competitor.probability %s %s" % (t["team"]["abbreviation"], p))
    except Exception as ex:
        print("ERR %s: %s" % (e.get("shortName"), ex))
