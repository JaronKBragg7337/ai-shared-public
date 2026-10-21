import urllib.request, json, pathlib, subprocess, sys

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)

print("===SATYA DESK LINES===")
text = pathlib.Path(r"C:\Users\lilli\AI-Shared\state\desk-trade.md").read_text(encoding="utf-8", errors="replace")
for l in [x for x in text.splitlines() if "satya-twin" in x.lower()][-20:]:
    print(l[:240])

print("===ESPN CFB LIVE/POST===")
sb = get("https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard")
for ev in sb.get("events", []):
    comp = ev["competitions"][0]
    st = comp["status"]["type"]
    state = st.get("state")
    detail = st.get("detail", "")
    if state not in ("in", "post") and "Half" not in detail:
        continue
    teams = comp["competitors"]
    a = next(t for t in teams if t["homeAway"] == "away")
    h = next(t for t in teams if t["homeAway"] == "home")
    print("%s %s @ %s %s | %s | id=%s" % (
        a["team"]["abbreviation"], a.get("score"),
        h["team"]["abbreviation"], h.get("score"),
        detail, ev["id"]))

print("===PITT SUMMARY===")
s = get("https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event=401858245")
hdr = s["header"]["competitions"][0]
print("status", hdr["status"]["type"].get("detail"))
for c in hdr["competitors"]:
    print(c["team"]["abbreviation"], c.get("score"), c["homeAway"])
wps = s.get("winprobability") or []
if wps:
    wp = wps[-1]
    hwp = float(wp.get("homeWinPercentage", 0))
    print("homeWinPct", hwp, "pittAwayWP", round(1 - hwp, 4))

print("===KEY GAMES===")
for ev in sb.get("events", []):
    name = ev.get("name", "")
    if any(k in name for k in ("Penn State", "Northwestern", "Liberty", "Delaware", "Pittsburgh", "Virginia Tech")):
        comp = ev["competitions"][0]
        st = comp["status"]["type"]
        teams = comp["competitors"]
        a = next(t for t in teams if t["homeAway"] == "away")
        h = next(t for t in teams if t["homeAway"] == "home")
        print("%s: %s %s @ %s %s | %s | %s" % (
            name, a["team"]["abbreviation"], a.get("score"),
            h["team"]["abbreviation"], h.get("score"),
            st.get("detail"), ev["id"]))

print("===LIVE BOARD CFB/NHL LINES===")
board = pathlib.Path(r"C:\Users\lilli\AI-Shared\state\live-board.md").read_text(encoding="utf-8", errors="replace")
for l in board.splitlines():
    if any(k in l for k in ("cfb", "nhl", "Live board")):
        print(l[:200])
