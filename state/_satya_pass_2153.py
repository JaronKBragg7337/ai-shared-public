import json, urllib.request, ssl
ctx = ssl.create_default_context()
H = {"User-Agent": "Mozilla/5.0"}

def get(u):
    req = urllib.request.Request(u, headers=H)
    return json.loads(urllib.request.urlopen(req, timeout=25, context=ctx).read())

url = "https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard"
data = get(url)
want = (
    "ohio", "kent", "toledo", "ball", "auburn", "tennessee", "florida", "missouri",
    "louisville", "maryland", "nebraska", "virginia", "florida state", "california",
    "unlv", "purdue", "illinois", "kentucky", "south carolina", "old dominion",
    "nc state", "iowa", "ohio state", "bowling", "miami", "marshall", "james madison",
    "akron", "central michigan", "eastern michigan", "massachusetts"
)
for e in data.get("events", []):
    name = e.get("name", "")
    low = name.lower()
    if not any(w in low for w in want):
        continue
    comp = e["competitions"][0]
    st = comp["status"]["type"]
    status = st.get("detail") or st.get("description")
    state = st.get("state")
    print(name, "|", status, "|", state, "| id", e.get("id"))
    for c in comp["competitors"]:
        t = c["team"].get("abbreviation") or c["team"].get("shortDisplayName")
        score = c.get("score")
        home = c.get("homeAway")
        prob = None
        if isinstance(c.get("probability"), dict):
            prob = c["probability"].get("winPercentage")
        print(f"  {home} {t} {score} wp={prob}")
    print()
