import urllib.request, json, subprocess, sys

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.load(r)

print("===PSU SUMMARY===")
s = get("https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event=401858476")
hdr = s["header"]["competitions"][0]
print("status", hdr["status"]["type"].get("detail"))
for c in hdr["competitors"]:
    print(c["team"]["abbreviation"], c.get("score"), c["homeAway"])
wps = s.get("winprobability") or []
if wps:
    wp = wps[-1]
    hwp = float(wp.get("homeWinPercentage", 0))
    print("homeWinPct NU", hwp, "psuAwayWP", round(1 - hwp, 4))
else:
    print("no winprobability yet")

print("===LIB SUMMARY===")
s2 = get("https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event=401871050")
hdr2 = s2["header"]["competitions"][0]
print("status", hdr2["status"]["type"].get("detail"))
for c in hdr2["competitors"]:
    print(c["team"]["abbreviation"], c.get("score"), c["homeAway"])
wps2 = s2.get("winprobability") or []
if wps2:
    wp = wps2[-1]
    hwp = float(wp.get("homeWinPercentage", 0))
    print("homeWinPct", hwp)

print("===PITT AGAIN===")
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

print("===DRY BBO===")
why = "Satya pass BBO check: comparing ESPN win prob to live ask for score-price edge scan"
for slug in (
    "aec-cfb-pitt-vtech-2026-10-02",
    "aec-cfb-pennst-nw-2026-10-02",
    "aec-cfb-librty-del-2026-10-02",
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
    # keep last chunk with book info
    print(out[-700:] if len(out) > 700 else out)
    print("---")
