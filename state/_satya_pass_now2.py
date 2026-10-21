import json, urllib.request, subprocess, sys

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.load(r)

# CFB scoreboard groups - try default and dates
print("===CFB SEARCH===")
for url in [
    "https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard",
    "https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?groups=80",
    "https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?dates=20261002",
    "https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?dates=20261003",
]:
    try:
        b = get(url)
        evs = b.get("events", [])
        print(url.split("?")[-1] if "?" in url else "default", "n=", len(evs))
        for e in evs:
            name = e.get("shortName") or e.get("name") or ""
            low = name.lower()
            if any(x in low for x in ["pitt", "vt", "psu", "nw", "lib", "del", "penn", "virgin", "northw", "libert", "delaw"]):
                comp = e["competitions"][0]
                print(" ", e.get("id"), name, "|", comp["status"]["type"].get("detail"))
                for c in comp["competitors"]:
                    print("   ", c["team"]["abbreviation"], c.get("score"))
    except Exception as ex:
        print("err", url, ex)

# Known / search penn state summary via scoreboard all events print shortNames
print("===ALL SHORT===")
b = get("https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?dates=20261002")
for e in b.get("events", []):
    print(e.get("id"), e.get("shortName"), e["competitions"][0]["status"]["type"].get("detail"))

b3 = get("https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?dates=20261003")
print("--- Oct3 ---")
for e in b3.get("events", []):
    print(e.get("id"), e.get("shortName"), e["competitions"][0]["status"]["type"].get("detail"))

def dry(slug):
    why = "Score-price check for Satya Twin trading pass; dry-run only for book"
    cmd = [sys.executable, r"C:\Users\lilli\AI-Shared\tools\desk-trade.py",
           "--by","grok-bot/satya-twin","--slug",slug,"--side","yes","--size","5",
           "--why",why,"--kill","edge gone or kill score","--dry-run"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    out = ((r.stdout or "") + (r.stderr or "")).strip()
    print("SLUG", slug)
    print(out[-900:] if len(out)>900 else out)
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
