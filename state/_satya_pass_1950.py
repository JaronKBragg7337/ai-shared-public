import json, urllib.request, pathlib
lb = json.loads(pathlib.Path(r"C:\Users\lilli\AI-Shared\state\live-board.json").read_text(encoding="utf-8"))
# structure probe
if isinstance(lb, dict):
    print("keys", list(lb.keys())[:20])
    games = lb.get("games") or lb.get("markets") or lb.get("rows") or lb.get("items") or []
    if not games and "board" in lb: games = lb["board"]
    print("n", len(games) if hasattr(games,"__len__") else type(games))
    if isinstance(games, list) and games:
        print("sample", json.dumps(games[0], default=str)[:500])
elif isinstance(lb, list):
    print("list n", len(lb))
    print("sample", json.dumps(lb[0], default=str)[:500])
# ESPN all in-progress with WP
url = "https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?groups=80&limit=200"
with urllib.request.urlopen(url, timeout=20) as r:
    data = json.load(r)
print("\n=== IN-PROGRESS CFB WP ===")
for ev in data.get("events", []):
    st = ev.get("status",{}).get("type",{})
    if st.get("state") != "in":
        continue
    name = ev["name"]
    comps = ev["competitions"][0]
    competitors = comps["competitors"]
    scores = {c["team"]["abbreviation"]: c.get("score") for c in competitors}
    detail = st.get("detail","")
    eid = ev["id"]
    try:
        with urllib.request.urlopen(f"https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event={eid}", timeout=12) as r2:
            sdata = json.load(r2)
        wpr = sdata.get("winprobability") or []
        if not wpr:
            print(f"{name} | {detail} | {scores} no wp")
            continue
        home_wp = wpr[-1].get("homeWinPercentage")
        home = next(c["team"]["abbreviation"] for c in competitors if c.get("homeAway")=="home")
        away = next(c["team"]["abbreviation"] for c in competitors if c.get("homeAway")=="away")
        print(f"{name} | {detail} | {scores} | {away}={1-home_wp:.1%} {home}={home_wp:.1%}")
    except Exception as e:
        print(f"{name} err {e}")
