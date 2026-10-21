import json, urllib.request

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=40) as r:
        return json.load(r)

board = get("https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?dates=20261003&limit=300")
want = [
    "Ohio Bobcats", "Kent State", "Toledo", "Ball State", "Auburn", "Tennessee",
    "Florida", "Missouri", "Louisville", "Maryland", "Nebraska", "Virginia",
    "Florida State", "California", "UNLV", "Purdue", "Illinois", "Eastern Michigan",
    "Massachusetts", "Kentucky", "South Carolina", "Old Dominion", "Georgia State",
    "NC State", "Ohio State", "Iowa",
]
# also match shorter names carefully
keys = ["Toledo", "Ball State", "Kent State", "Ohio", "Auburn", "Tennessee", "Florida", "Missouri",
        "Louisville", "Maryland", "Nebraska", "Virginia", "California", "UNLV", "Purdue", "Illinois",
        "Eastern Michigan", "Massachusetts", "Kentucky", "South Carolina", "Old Dominion", "Georgia State",
        "NC State", "Ohio State", "Iowa Hawkeyes"]

seen = set()
for e in board.get("events", []):
    n = e.get("name", "")
    # prefer exact-ish matches; skip Ohio State when looking for Ohio Bobcats
    matched = None
    for k in ("Toledo", "Ball State", "Kent State", "Auburn", "Tennessee Volunteers",
              "Florida Gators", "Missouri", "Louisville", "Maryland", "Nebraska",
              "Virginia Cavaliers", "Florida State", "California", "UNLV", "Purdue",
              "Illinois", "Eastern Michigan", "Massachusetts", "Kentucky", "South Carolina",
              "Old Dominion", "Georgia State", "NC State", "Ohio State", "Iowa Hawkeyes",
              "Ohio Bobcats"):
        if k in n:
            matched = k
            break
    if "Ohio" in n and "Ohio State" not in n and "Ohio Bobcats" not in n:
        # Bobcats often listed as Ohio vs Kent State
        if "Kent" in n:
            matched = "Ohio Bobcats"
    if not matched:
        continue
    if e["id"] in seen:
        continue
    seen.add(e["id"])
    eid = e["id"]
    c = e["competitions"][0]
    s = c["status"]["type"]
    a = next(x for x in c["competitors"] if x["homeAway"] == "away")
    h = next(x for x in c["competitors"] if x["homeAway"] == "home")
    print("EVENT", eid, n, "|", a["team"]["abbreviation"], a["score"], "-", h["score"], h["team"]["abbreviation"], "|", s.get("detail"))
    try:
        summ = get(f"https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event={eid}")
        wp = summ.get("winprobability") or []
        if wp:
            last = wp[-1]
            print(" WP", {k: last.get(k) for k in ("homeWinPercentage", "awayWinPercentage", "tiePercentage", "secondsLeft", "playId") if k in last or True})
            # dump keys
            print(" WP_KEYS", list(last.keys()))
            print(" WP_RAW", json.dumps(last)[:350])
        sit = (c.get("situation") or {})
        lp = (sit.get("lastPlay") or {})
        prob = lp.get("probability") or {}
        if prob:
            print(" LASTPLAY_WP", prob)
        hdr = summ.get("header") or {}
        comps2 = ((hdr.get("competitions") or [{}])[0].get("competitors") or [])
        for x in comps2:
            print(" HDR", x.get("homeAway"), (x.get("team") or {}).get("abbreviation"), x.get("score"), "prob", x.get("probability"))
    except Exception as ex:
        print(" err", ex)
    print()
