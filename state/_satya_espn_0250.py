import json, urllib.request

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=12) as r:
        return json.load(r)

want = ["lsu", "kentucky", "georgia", "alabama", "usc", "penn state", "kansas", "utah", "james madison", "georgia southern", "syracuse", "virginia", "fresno", "boise"]
j = get("https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?groups=80&limit=200")
for e in j.get("events", []):
    c = e["competitions"][0]
    st = c["status"]["type"]
    state = st.get("state")
    if state == "pre":
        continue
    comps = c["competitors"]
    names = " / ".join(x["team"]["displayName"] for x in comps)
    low = names.lower()
    if not any(w in low for w in want):
        continue
    detail = st.get("detail")
    scores = " ".join("%s=%s" % (x["team"]["abbreviation"], x["score"]) for x in comps)
    eid = e["id"]
    home = next(x for x in comps if x["homeAway"] == "home")
    away = next(x for x in comps if x["homeAway"] == "away")
    hwp = awp = None
    err = ""
    try:
        sj = get("https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event=%s" % eid)
        wp = sj.get("winprobability") or []
        if wp:
            last = wp[-1]
            hwp = last.get("homeWinPercentage")
            awp = (1.0 - float(hwp)) if hwp is not None else None
        if hwp is None:
            sit = (sj.get("header", {}).get("competitions") or [{}])[0].get("situation") or {}
            hwp = sit.get("homeWinPercentage")
            awp = sit.get("awayWinPercentage")
    except Exception as ex:
        err = str(ex)[:80]
    print("%s | %s | %s | home=%s WP=%s | away=%s WP=%s | state=%s | %s" % (
        detail, names, scores,
        home["team"]["abbreviation"], ("%.3f" % float(hwp)) if hwp is not None else None,
        away["team"]["abbreviation"], ("%.3f" % float(awp)) if awp is not None else None, state, err))
