import json, urllib.request
url = "https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?groups=80&limit=100"
j = json.load(urllib.request.urlopen(url, timeout=20))
want = ["tennessee", "arkansas", "texas", "oklahoma", "ucla", "oregon", "lsu", "kentucky", "illinois", "michigan state", "ohio state", "maryland", "houston", "kansas"]
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
    hwp = awp = None
    err = ""
    try:
        surl = "https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event=%s" % eid
        sj = json.load(urllib.request.urlopen(surl, timeout=15))
        wp = sj.get("winprobability") or []
        if wp:
            last = wp[-1]
            hwp = last.get("homeWinPercentage")
            awp = 1.0 - float(hwp) if hwp is not None else None
        sit = (sj.get("header", {}).get("competitions") or [{}])[0].get("situation") or {}
        if hwp is None:
            hwp = sit.get("homeWinPercentage")
            awp = sit.get("awayWinPercentage")
    except Exception as ex:
        err = str(ex)
    home = next(x for x in comps if x["homeAway"] == "home")
    away = next(x for x in comps if x["homeAway"] == "away")
    print("%s | %s | %s | home=%s WP=%s | away=%s WP=%s | %s" % (
        detail, names, scores,
        home["team"]["abbreviation"], hwp,
        away["team"]["abbreviation"], awp, err))
