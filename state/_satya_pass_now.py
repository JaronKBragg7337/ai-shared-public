import json, urllib.request, subprocess, sys

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.load(r)

print("===PITT===")
s = get("https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event=401858245")
hdr = s["header"]["competitions"][0]
print("status", hdr["status"]["type"].get("detail"))
for c in hdr["competitors"]:
    print(c["team"]["abbreviation"], c.get("score"), c["homeAway"])
wps = s.get("winprobability") or []
if wps:
    wp = wps[-1]
    hwp = float(wp.get("homeWinPercentage", 0))
    print("homeWinPct VT", round(hwp,4), "pittWP", round(1-hwp,4))

# find penn state / liberty event ids from scoreboard
print("===CFB BOARD FILTER===")
b = get("https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard")
for e in b.get("events", []):
    name = e.get("name","")
    if any(x in name for x in ["Penn State","Northwestern","Liberty","Delaware","Pittsburgh","Virginia Tech"]):
        comp = e["competitions"][0]
        print(e.get("id"), name, "|", comp["status"]["type"].get("detail"))
        for c in comp["competitors"]:
            print(" ", c["team"]["abbreviation"], c.get("score"))

def dry(slug):
    cmd = [sys.executable, r"C:\Users\lilli\AI-Shared\tools\desk-trade.py",
           "--by","grok-bot/satya-twin","--slug",slug,"--side","yes","--size","5",
           "--why","Satya pass BBO","--kill","n/a","--dry-run"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    out = ((r.stdout or "") + (r.stderr or "")).strip()
    print("SLUG", slug)
    print(out[-700:] if len(out)>700 else out)
    print("---")

print("===DRY===")
for slug in [
    "aec-cfb-pitt-vtech-2026-10-02",
    "aec-cfb-pennst-nw-2026-10-02",
    "aec-cfb-librty-del-2026-10-02",
    "atc-cnl-mtq-hnd-2026-10-02-hnd",
    "atc-intf-col-par-2026-10-02-col",
]:
    dry(slug)
