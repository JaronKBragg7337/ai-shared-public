#!/usr/bin/env python3
import json, urllib.request

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.load(r)

def dump_sb(label, url, want_abbrs=None):
    print("===", label, "===")
    data = get(url)
    for e in data.get("events", []):
        comp = e["competitions"][0]
        st = comp["status"]["type"]
        teams = comp["competitors"]
        home = next(t for t in teams if t["homeAway"] == "home")
        away = next(t for t in teams if t["homeAway"] == "away")
        def nm(t):
            return t["team"].get("abbreviation") or t["team"].get("shortDisplayName")
        a, h = nm(away), nm(home)
        if want_abbrs and not ({a, h} & want_abbrs):
            if st.get("state") != "in":
                continue
        # win pct from situation / odds
        wp = None
        sit = comp.get("situation") or {}
        # competitor probability sometimes under 'probability'
        for t in teams:
            p = t.get("probability")
            if isinstance(p, dict) and "winPercentage" in p:
                side = "home" if t["homeAway"]=="home" else "away"
                wp = (side, p["winPercentage"]) if wp is None else wp
        # alternate: headers.competitions winprobability endpoint not here
        line = f"{a} {away.get('score')} @ {h} {home.get('score')} | {st.get('detail')} | state={st.get('state')}"
        print(line)
        # print both probs if present
        for t in teams:
            p = t.get("probability") or {}
            if p:
                print(f"  {nm(t)} prob={p}")
        if sit:
            keys = [k for k in sit.keys() if k in ("downDistanceText","possessionText","lastPlay","isRedZone")]
            if keys:
                print("  sit:", {k: sit.get(k) for k in keys if not isinstance(sit.get(k), dict)})
                lp = sit.get("lastPlay")
                if isinstance(lp, dict):
                    print("  lastPlay:", lp.get("text"))

# CFB
dump_sb("CFB", "https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard",
        want_abbrs={"LSU","MISS","COLO","NW","WVU","UVA","VT","MD","UNM","OU","MSU","ND","BYU","CSU","SMU","LOU","SELA","ULM","ECU","ODU"})
# also dump all in-progress
print("=== CFB IN-PROGRESS ALL ===")
data = get("https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard")
for e in data.get("events", []):
    comp = e["competitions"][0]
    st = comp["status"]["type"]
    if st.get("state") != "in":
        continue
    teams = comp["competitors"]
    home = next(t for t in teams if t["homeAway"] == "home")
    away = next(t for t in teams if t["homeAway"] == "away")
    def nm(t):
        return t["team"].get("abbreviation") or t["team"].get("shortDisplayName")
    probs = []
    for t in teams:
        p = t.get("probability") or {}
        if "winPercentage" in p:
            probs.append(f"{nm(t)}={p['winPercentage']:.3f}")
    print(f"{nm(away)} {away.get('score')} @ {nm(home)} {home.get('score')} | {st.get('detail')} | {' '.join(probs)}")

print("=== MLB IN-PROGRESS ===")
data = get("https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard")
for e in data.get("events", []):
    comp = e["competitions"][0]
    st = comp["status"]["type"]
    if st.get("state") not in ("in", "post"):
        continue
    teams = comp["competitors"]
    home = next(t for t in teams if t["homeAway"] == "home")
    away = next(t for t in teams if t["homeAway"] == "away")
    def nm(t):
        return t["team"].get("abbreviation") or t["team"].get("shortDisplayName")
    print(f"{nm(away)} {away.get('score')} @ {nm(home)} {home.get('score')} | {st.get('detail')} | state={st.get('state')}")

# winprob helper for specific games
print("=== WINPROB SAMPLE ===")
for gid in ["401856688", "401856796"]:
    try:
        u = f"https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event={gid}"
        d = get(u)
        wp = d.get("winprobability") or []
        hdr = d.get("header") or {}
        comps = (hdr.get("competitions") or [{}])[0]
        status = ((comps.get("status") or {}).get("type") or {}).get("detail")
        teams = comps.get("competitors") or []
        sc = []
        for t in teams:
            sc.append(f"{t['team'].get('abbreviation')}={t.get('score')}")
        print(gid, status, " ".join(sc))
        if wp:
            last = wp[-1]
            print("  last wp homeWinPct=", last.get("homeWinPercentage"), "playId=", last.get("playId"))
        # predictor
        pred = d.get("predictor") or {}
        if pred:
            print("  predictor", {k: pred.get(k) for k in pred if "percentage" in k.lower() or "chance" in k.lower() or k in ("homeTeam", "awayTeam")})
    except Exception as ex:
        print(gid, "ERR", ex)
