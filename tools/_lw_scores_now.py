import json, urllib.request

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.load(r)

sb = get("https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?groups=80&limit=300")
keys = ["FRES", "SJSU", "PUR", "UCLA", "JMU", "SDSU", "NDSU", "SAC", "SDAK", "BOIS", "FRESNO", "SAN JOSE", "PURDUE", "JAMES MADISON", "NORTH DAKOTA", "SOUTH DAKOTA", "BOISE"]
for e in sb.get("events", []):
    c = e["competitions"][0]
    st = c["status"]
    typ = st["type"]
    teams = []
    for t in c["competitors"]:
        ab = t["team"].get("abbreviation", "")
        teams.append((t["homeAway"], ab, t.get("score"), t["team"].get("displayName")))
    blob = " ".join([x[1] + " " + x[3] for x in teams]).upper()
    if not any(k in blob for k in keys):
        continue
    print("CFB", typ.get("state"), e.get("shortName"), typ.get("detail"), "clock", st.get("displayClock"), "p", st.get("period"), "id", e.get("id"))
    for ha, ab, sc, dn in teams:
        print(" ", ha, ab, sc, dn)

# win probs for live games of interest
for eid in []:
    pass

ids = []
for e in sb.get("events", []):
    c = e["competitions"][0]
    if c["status"]["type"].get("state") != "in":
        continue
    blob = " ".join(t["team"].get("abbreviation","")+" "+t["team"].get("displayName","") for t in c["competitors"]).upper()
    if any(k in blob for k in ["FRES", "SJSU", "PUR", "UCLA", "JMU", "SDSU", "NDSU", "SDAK", "BOIS", "FRESNO", "PURDUE", "JAMES MADISON", "BOISE", "SOUTH DAKOTA"]):
        ids.append(e["id"])

for eid in ids:
    try:
        s = get(f"https://site.web.api.espn.com/apis/site/v2/sports/football/college-football/summary?event={eid}")
    except Exception as ex:
        print("summary err", eid, ex)
        continue
    h = s.get("header", {})
    c = h.get("competitions", [{}])[0]
    st = c.get("status", {})
    print("SUMMARY", eid, st.get("type", {}).get("detail"), "clock", st.get("displayClock"))
    for t in c.get("competitors", []):
        print(" ", t.get("homeAway"), t.get("team", {}).get("abbreviation"), t.get("score"))
    wp = s.get("winprobability") or []
    if wp:
        last = wp[-1]
        print(" WP", {k: last.get(k) for k in last})
    for pc in (s.get("pickcenter") or [])[:1]:
        print(" PC", {k: pc.get(k) for k in ["details", "spread", "overUnder"]})
        ato = pc.get("awayTeamOdds") or {}
        hto = pc.get("homeTeamOdds") or {}
        print("  awayML", ato.get("moneyLine"), "homeML", hto.get("moneyLine"))

for league in ["wta", "atp"]:
    try:
        tb = get(f"https://site.api.espn.com/apis/site/v2/sports/tennis/{league}/scoreboard")
    except Exception as ex:
        print("TENNIS", league, "err", ex)
        continue
    n_in = 0
    for e in tb.get("events", []):
        c = e["competitions"][0]
        typ = c["status"]["type"]
        if typ.get("state") != "in":
            continue
        n_in += 1
        print("TENNIS", league, e.get("name"), typ.get("detail"))
        for t in c["competitors"]:
            who = (t.get("athlete") or {}).get("displayName") or (t.get("team") or {}).get("displayName")
            print(" ", t.get("homeAway"), who, "score", t.get("score"), "lines", t.get("linescores"))
    print("TENNIS", league, "live_count", n_in)
