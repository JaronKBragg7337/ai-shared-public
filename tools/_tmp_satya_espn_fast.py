import json, urllib.request
url = "https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?groups=80&limit=100"
j = json.load(urllib.request.urlopen(url, timeout=15))
want = ["tennessee", "arkansas", "texas", "oklahoma", "illinois", "michigan state", "lsu", "kentucky"]
rows = []
for e in j.get("events", []):
    c = e["competitions"][0]
    if c["status"]["type"]["state"] == "pre":
        continue
    comps = c["competitors"]
    names = " / ".join(x["team"]["displayName"] for x in comps)
    if not any(w in names.lower() for w in want):
        continue
    rows.append((e["id"], c["status"]["type"]["detail"], names, comps))
print("SCOREBOARD", len(rows))
for eid, detail, names, comps in rows:
    scores = " ".join("%s=%s" % (x["team"]["abbreviation"], x["score"]) for x in comps)
    print("SB", detail, "|", names, "|", scores, "| id", eid)
for eid, detail, names, comps in rows:
    try:
        sj = json.load(urllib.request.urlopen(
            "https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event=%s" % eid,
            timeout=12))
        wp = sj.get("winprobability") or []
        hwp = wp[-1].get("homeWinPercentage") if wp else None
        home = next(x for x in comps if x["homeAway"] == "home")
        away = next(x for x in comps if x["homeAway"] == "away")
        print("WP", names, "| home", home["team"]["abbreviation"], hwp, "| away", away["team"]["abbreviation"], (None if hwp is None else 1-float(hwp)), "|", detail)
    except Exception as ex:
        print("WPERR", names, ex)
