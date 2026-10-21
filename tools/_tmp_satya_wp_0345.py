import json, urllib.request
def wp(sport_path, event_filter):
    url = f"https://site.api.espn.com/apis/site/v2/sports/{sport_path}/scoreboard"
    if sport_path.endswith('nba') or sport_path.endswith('nhl'):
        url += "?dates=20261010"
    j = json.load(urllib.request.urlopen(url, timeout=20))
    for e in j.get("events", []):
        c = e["competitions"][0]
        if c["status"]["type"]["state"] == "pre":
            continue
        names = " / ".join(x["team"]["displayName"] for x in c["competitors"])
        low = names.lower()
        if not any(w in low for w in event_filter):
            continue
        detail = c["status"]["type"]["detail"]
        scores = " ".join("%s=%s" % (x["team"]["abbreviation"], x["score"]) for x in c["competitors"])
        eid = e["id"]
        hwp = awp = None
        err = ""
        try:
            surl = f"https://site.api.espn.com/apis/site/v2/sports/{sport_path}/summary?event={eid}"
            sj = json.load(urllib.request.urlopen(surl, timeout=15))
            wpl = sj.get("winprobability") or []
            if wpl:
                last = wpl[-1]
                hwp = last.get("homeWinPercentage")
                awp = 1.0 - float(hwp) if hwp is not None else None
        except Exception as ex:
            err = str(ex)
        home = next(x for x in c["competitors"] if x["homeAway"] == "home")
        away = next(x for x in c["competitors"] if x["homeAway"] == "away")
        print(f"{detail} | {names} | {scores} | home={home['team']['abbreviation']} WP={hwp} | away={away['team']['abbreviation']} WP={awp} | {err}")
wp("football/college-football", ["boise", "fresno", "kansas", "utah", "hawaii", "arizona state", "james madison", "georgia southern"])
wp("basketball/nba", ["spurs", "suns"])
wp("hockey/nhl", ["ducks", "flames", "kings", "golden knights", "vegas"])
