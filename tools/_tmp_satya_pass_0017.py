import json, urllib.request
url = "https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?groups=80&limit=100"
j = json.load(urllib.request.urlopen(url, timeout=20))
want = ["lsu", "kentucky", "utah", "kansas", "usc", "penn state", "uab", "memphis", "georgia", "alabama", "northern illinois", "air force", "coastal", "marshall", "james madison", "georgia southern", "minnesota", "purdue", "north dakota", "unlv", "nevada", "utep", "syracuse", "virginia", "tarleton"]
for e in j.get("events", []):
    c = e["competitions"][0]
    st = c["status"]["type"]["state"]
    if st == "pre":
        continue
    comps = c["competitors"]
    names = " / ".join(x["team"]["displayName"] for x in comps)
    low = names.lower()
    if not any(w in low for w in want):
        continue
    detail = c["status"]["type"]["detail"]
    scores = " ".join("%s=%s" % (x["team"]["abbreviation"], x["score"]) for x in comps)
    eid = e["id"]
    hwp = None
    err = ""
    try:
        surl = "https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event=%s" % eid
        sj = json.load(urllib.request.urlopen(surl, timeout=15))
        wp = sj.get("winprobability") or []
        if wp:
            hwp = wp[-1].get("homeWinPercentage")
        sit = (sj.get("header", {}).get("competitions") or [{}])[0].get("situation") or {}
        if hwp is None:
            hwp = sit.get("homeWinPercentage")
    except Exception as ex:
        err = str(ex)
    home = next(x for x in comps if x["homeAway"] == "home")
    away = next(x for x in comps if x["homeAway"] == "away")
    awp = None if hwp is None else 1.0 - float(hwp)
    print("%s | %s | %s | home=%s WP=%s | away=%s WP=%s | %s" % (
        detail, names, scores,
        home["team"]["abbreviation"], hwp,
        away["team"]["abbreviation"], awp, err))
