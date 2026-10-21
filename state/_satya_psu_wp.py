import json, urllib.request

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.load(r)

for eid, label, away in [("401858476","PSU@NU","PSU"), ("401871050","LIB@DEL","LIB"), ("401858245","PITT@VT","PITT")]:
    s = get(f"https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event={eid}")
    hdr = s["header"]["competitions"][0]
    print("=", label, hdr["status"]["type"].get("detail"))
    home_ab = None
    for c in hdr["competitors"]:
        print(" ", c["team"]["abbreviation"], c.get("score"), c["homeAway"])
        if c["homeAway"] == "home":
            home_ab = c["team"]["abbreviation"]
    wps = s.get("winprobability") or []
    if wps:
        wp = wps[-1]
        hwp = float(wp.get("homeWinPercentage", 0))
        print(" homeWinPct", home_ab, round(hwp,4), "awayWin", round(1-hwp,4))
    else:
        print(" no winprob")
