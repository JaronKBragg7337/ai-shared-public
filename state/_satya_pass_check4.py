import urllib.request, json, subprocess, sys

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.load(r)

# Soccer scoreboard today
print("===SOCCER SCOREBOARD===")
for path in [
    "https://site.api.espn.com/apis/site/v2/sports/soccer/all/scoreboard",
    "https://site.api.espn.com/apis/site/v2/sports/soccer/uefa.nations/scoreboard",
    "https://site.api.espn.com/apis/site/v2/sports/soccer/fifa.worldq.conmebol/scoreboard",
]:
    try:
        d = get(path)
        for e in d.get("events", []):
            name = e.get("name", "")
            low = name.lower()
            if any(x in low for x in ["martinique", "honduras", "colombia", "paraguay", "mtq", "hnd"]):
                comp = e["competitions"][0]
                st = comp["status"]["type"].get("detail")
                print(path.split("/")[-2], name, st)
                for c in comp["competitors"]:
                    print(" ", c["team"].get("abbreviation"), c.get("score"), c["homeAway"])
    except Exception as ex:
        print("fail", path, ex)

# Polymarket-ish: try live-board related soccer via fotmob-ish? Just desk dry-run for soccer slugs
print("===SOCCER DRY===")
why = "Satya soccer BBO check"
for slug in (
    "atc-cnl-mtq-hnd-2026-10-02-hnd",
    "atc-intf-col-par-2026-10-02-col",
):
    cmd = [
        sys.executable,
        r"C:\Users\lilli\AI-Shared\tools\desk-trade.py",
        "--by", "grok-bot/satya-twin",
        "--slug", slug,
        "--side", "yes",
        "--size", "5",
        "--why", why,
        "--kill", "n/a check only",
        "--dry-run",
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    out = ((r.stdout or "") + (r.stderr or "")).strip()
    print("SLUG", slug)
    print(out[-500:] if len(out) > 500 else out)
    print("---")

# Also refresh Pitt wp once more
print("===PITT LIVE===")
s3 = get("https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event=401858245")
hdr3 = s3["header"]["competitions"][0]
print("status", hdr3["status"]["type"].get("detail"))
for c in hdr3["competitors"]:
    print(c["team"]["abbreviation"], c.get("score"), c["homeAway"])
wps3 = s3.get("winprobability") or []
if wps3:
    wp = wps3[-1]
    hwp = float(wp.get("homeWinPercentage", 0))
    print("homeWinPct VT", hwp, "pittWP", round(1 - hwp, 4))
