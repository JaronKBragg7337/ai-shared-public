import json, urllib.request

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.load(r)

url = "https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?groups=80&dates=20261002"
data = fetch(url)
want = ("Pittsburgh", "Virginia Tech", "Penn State", "Northwestern", "Liberty", "Delaware")
for e in data.get("events", []):
    name = e.get("name", "")
    if not any(x in name for x in want):
        continue
    comp = e["competitions"][0]
    st = comp["status"]["type"]
    print("=", name)
    print(" status:", st.get("detail"), "|", st.get("state"))
    for c in comp["competitors"]:
        print(f"  {c['team']['abbreviation']} {c.get('score')} {c.get('homeAway')}")
    eid = e.get("id")
    try:
        summ = fetch(f"https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event={eid}")
        wp = summ.get("winprobability") or []
        if wp:
            last = wp[-1]
            print("  winprob last:", json.dumps(last)[:400])
        pred = summ.get("predictor") or {}
        if pred:
            print("  predictor:", json.dumps(pred)[:400])
        hdr = summ.get("header") or {}
        comps = (hdr.get("competitions") or [{}])[0]
        for c in comps.get("competitors", []):
            print("  header", c.get("team",{}).get("abbreviation"), "prob", c.get("probability"), "score", c.get("score"))
        # situation
        sit = summ.get("situation") or {}
        if sit:
            print("  situation keys sample:", {k: sit.get(k) for k in list(sit)[:12]})
    except Exception as ex:
        print("  summary err", ex)
