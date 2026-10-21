import urllib.request, json, pathlib, subprocess, sys

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.load(r)

# Broad CFB scoreboards
urls = [
    "https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard",
    "https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?groups=80",
    "https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?dates=20261002",
    "https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?dates=20261003",
]
seen = set()
print("===ALL CFB EVENTS===")
for url in urls:
    try:
        sb = get(url)
    except Exception as e:
        print("fail", url, e)
        continue
    for ev in sb.get("events", []):
        if ev["id"] in seen:
            continue
        seen.add(ev["id"])
        comp = ev["competitions"][0]
        st = comp["status"]["type"]
        teams = comp["competitors"]
        a = next(t for t in teams if t["homeAway"] == "away")
        h = next(t for t in teams if t["homeAway"] == "home")
        name = ev.get("shortName") or ev.get("name")
        print("%s | %s %s-%s %s | %s | %s | %s" % (
            name, a["team"]["abbreviation"], a.get("score"),
            h.get("score"), h["team"]["abbreviation"],
            st.get("detail"), st.get("state"), ev["id"]))

# Try find PSU / Liberty by search
print("===SEARCH PSU LIB===")
for q in ("Penn State", "Liberty", "Northwestern", "Delaware"):
    try:
        data = get("https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?limit=300&dates=20261002-20261003")
        # fallback search endpoint
    except Exception:
        pass
try:
    s = get("http://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?dates=20261002&groups=80&limit=200")
    print("groups80 count", len(s.get("events", [])))
    for ev in s.get("events", []):
        comp = ev["competitions"][0]
        st = comp["status"]["type"]
        teams = comp["competitors"]
        a = next(t for t in teams if t["homeAway"] == "away")
        h = next(t for t in teams if t["homeAway"] == "home")
        print("%s %s @ %s %s | %s" % (a["team"]["abbreviation"], a.get("score"), h["team"]["abbreviation"], h.get("score"), st.get("detail")))
except Exception as e:
    print("g80", e)

# Dry-run BBO for Pitt and PennSt via desk-trade
print("===DRY RUN BBO===")
for slug, side in (
    ("aec-cfb-pitt-vtech-2026-10-02", "yes"),
    ("aec-cfb-pennst-nw-2026-10-02", "yes"),
    ("aec-cfb-librty-del-2026-10-02", "yes"),
):
    cmd = [
        sys.executable,
        r"C:\Users\lilli\AI-Shared\tools\desk-trade.py",
        "--by", "grok-bot/satya-twin",
        "--slug", slug,
        "--side", side,
        "--size", "5",
        "--why", "pass-check bbo",
        "--kill", "n/a",
        "--dry-run",
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    out = (r.stdout or "") + (r.stderr or "")
    print("SLUG", slug)
    print(out[-500:] if len(out) > 500 else out)
