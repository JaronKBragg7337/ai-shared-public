import json, urllib.request

def fetch(url):
    with urllib.request.urlopen(url, timeout=25) as r:
        return json.load(r)

want = ("Pittsburgh", "Virginia Tech", "Penn State", "Northwestern", "Liberty", "Delaware")
url = "https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard"
data = fetch(url)
print("CFB events:", len(data.get("events", [])))
for e in data.get("events", []):
    name = e.get("name", "")
    if not any(x in name for x in want):
        continue
    comp = e["competitions"][0]
    st = comp["status"]["type"]
    print("=", name)
    print(" status:", st.get("detail"), "|", st.get("state"), "| period", st.get("period"))
    for c in comp["competitors"]:
        ab = c["team"]["abbreviation"]
        sc = c.get("score")
        print(f"  {ab} {sc} homeAway={c.get('homeAway')} winner={c.get('winner')}")
    # winprob from summary endpoint if available
    eid = e.get("id")
    try:
        summ = fetch(f"https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event={eid}")
        wp = summ.get("winprobability") or []
        if wp:
            last = wp[-1]
            print("  winprob last:", {k: last.get(k) for k in ("homeWinPercentage","tiePercentage","secondsLeft","playId") if k in last or True})
            print("  winprob keys:", list(last.keys()))
            print("  winprob raw:", json.dumps(last)[:300])
        # also predictor
        pred = summ.get("predictor") or {}
        if pred:
            print("  predictor:", json.dumps(pred)[:400])
        hdr = summ.get("header") or {}
        comps = (hdr.get("competitions") or [{}])[0]
        for c in comps.get("competitors", []):
            prob = c.get("probability")
            print("  header", c.get("team",{}).get("abbreviation"), "prob", prob)
    except Exception as ex:
        print("  summary err", ex)

# soccer quick
for label, path in [
    ("soccer", "https://site.api.espn.com/apis/site/v2/sports/soccer/all/scoreboard"),
]:
    try:
        sd = fetch(path)
        print("SOCCER events", len(sd.get("events", [])))
        for e in sd.get("events", [])[:80]:
            name = e.get("name", "")
            if any(x in name for x in ("Colombia", "Paraguay", "Martinique", "Honduras", "Suriname", "Guatemala")):
                comp = e["competitions"][0]
                st = comp["status"]["type"].get("detail")
                print("=", name, "|", st)
                for c in comp["competitors"]:
                    print(" ", c["team"].get("abbreviation") or c["team"].get("displayName"), c.get("score"))
    except Exception as ex:
        print("soccer err", ex)
