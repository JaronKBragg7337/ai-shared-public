#!/usr/bin/env python3
import json, urllib.request

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.load(r)

data = get("https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard")
want = {"BAL", "DAL", "LV", "NO", "MIN", "TB", "ARI", "SF"}
events = []
for e in data.get("events", []):
    comp = e["competitions"][0]
    st = comp["status"]["type"]
    teams = comp["competitors"]
    home = next(t for t in teams if t["homeAway"] == "home")
    away = next(t for t in teams if t["homeAway"] == "away")
    a = away["team"].get("abbreviation")
    h = home["team"].get("abbreviation")
    if not ({a, h} & want):
        continue
    print(f"{a} {away.get('score')} @ {h} {home.get('score')} | {st.get('detail')} | eid={e['id']}")
    for t in teams:
        p = t.get("probability") or {}
        if p:
            print(" ", t["team"].get("abbreviation"), p)
    sit = comp.get("situation") or {}
    if sit.get("downDistanceText") or sit.get("possessionText"):
        print("  sit:", sit.get("downDistanceText"), sit.get("possessionText"))
        lp = sit.get("lastPlay") or {}
        if isinstance(lp, dict):
            print("  last:", (lp.get("text") or "")[:140])
    events.append(e["id"])

print("=== SUMMARIES ===")
for eid in events:
    try:
        d = get(f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/summary?event={eid}")
        wp = d.get("winprobability") or []
        hdr = d.get("header") or {}
        comps = (hdr.get("competitions") or [{}])[0]
        status = ((comps.get("status") or {}).get("type") or {}).get("detail")
        sc = []
        home_abb = None
        for t in comps.get("competitors") or []:
            abb = t["team"].get("abbreviation")
            sc.append(f"{abb}={t.get('score')}")
            if t.get("homeAway") == "home":
                home_abb = abb
        print(eid, status, " ".join(sc))
        if wp:
            last = wp[-1]
            hwp = float(last.get("homeWinPercentage") or 0)
            print(f"  last homeWinPct={hwp:.3f} ({home_abb}) awayWinPct={1-hwp:.3f}")
        pred = d.get("predictor") or {}
        if pred:
            print("  predictor home=", pred.get("homeTeam", {}).get("gameProjection"), "away=", pred.get("awayTeam", {}).get("gameProjection"))
    except Exception as ex:
        print(eid, "ERR", ex)
