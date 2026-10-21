import urllib.request, json

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    return json.loads(urllib.request.urlopen(req, timeout=25).read())

# game ids from scoreboard
ids = {
  "TOL": "401866431",
  "SYR": None,
  "WMU": None,
  "EMU": None,
  "ODU": None,
  "OSU": None,
  "LOU": None,
  "AUB": None,
  "UVA": None,
}

# refresh ids
board = get("https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?dates=20261003&limit=300")
name_to_id = {}
for ev in board.get("events", []):
    name_to_id[ev.get("name","")] = ev.get("id")
    print("EVENT", ev.get("id"), ev.get("name"), ev["competitions"][0]["status"]["type"]["detail"])

# pick key games
wanted = {
  "Toledo": None,
  "Syracuse": None,
  "Western Michigan": None,
  "Eastern Michigan": None,
  "Old Dominion": None,
  "Ohio State": None,
  "Louisville": None,
  "Auburn": None,
  "Virginia": None,
  "California": None,
  "Bowling Green": None,
  "Akron": None,
}
for name, eid in name_to_id.items():
    for w in wanted:
        if w in name:
            wanted[w] = eid

print("IDS", wanted)

for label, eid in wanted.items():
    if not eid:
        continue
    # winprobability endpoint
    urls = [
      f"https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event={eid}",
      f"https://sports.core.api.espn.com/v2/sports/football/leagues/college-football/events/{eid}/competitions/{eid}/probabilities?limit=1",
      f"https://sports.core.api.espn.com/v2/sports/football/leagues/college-football/events/{eid}/competitions/{eid}/odds",
    ]
    print("====", label, eid)
    # summary winprobability
    try:
        s = get(urls[0])
        wp = s.get("winprobability") or []
        if wp:
            last = wp[-1]
            print("WP last", json.dumps(last)[:400])
        else:
            print("no winprobability key; keys", list(s.keys())[:30])
        # header
        header = s.get("header") or {}
        comps = ((header.get("competitions") or [{}])[0].get("competitors") or [])
        for c in comps:
            print("HDR", c.get("homeAway"), (c.get("team") or {}).get("abbreviation"), c.get("score"), "prob", c.get("probability"))
        # pickcenter
        pc = s.get("pickcenter") or []
        if pc:
            print("pick", json.dumps(pc[0])[:300])
    except Exception as e:
        print("sum err", e)
    try:
        p = get(urls[1])
        items = p.get("items") or []
        if items:
            print("prob item", json.dumps(items[-1])[:400])
        else:
            print("prob empty", list(p.keys()))
    except Exception as e:
        print("prob err", e)
