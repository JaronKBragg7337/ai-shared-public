import json, urllib.request

url = "https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard"
data = json.loads(urllib.request.urlopen(url, timeout=25).read())
want = (
    "ohio", "kent", "toledo", "ball", "auburn", "tennessee", "florida", "missouri",
    "louisville", "maryland", "nebraska", "virginia", "florida state", "california",
    "unlv", "purdue", "illinois", "eastern michigan", "massachusetts", "kentucky",
    "south carolina", "old dominion", "georgia state", "cal", "nc state"
)
for e in data.get("events", []):
    name = e.get("name", "")
    low = name.lower()
    if not any(w in low for w in want):
        continue
    comp = e["competitions"][0]
    st = comp["status"]["type"]
    status = st.get("detail") or st.get("description")
    print(name, "|", status)
    for c in comp["competitors"]:
        t = c["team"].get("abbreviation") or c["team"].get("shortDisplayName")
        score = c.get("score")
        home = c.get("homeAway")
        prob = None
        if isinstance(c.get("probability"), dict):
            prob = c["probability"].get("winPercentage")
        print(f"  {home} {t} {score} wp={prob}")
    # win probability from situation / odds if present
    for key in ("situation", "odds", "predictor"):
        if key in comp and comp[key]:
            print(" ", key, json.dumps(comp[key])[:300])
    print()
