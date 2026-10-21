import json, urllib.request, ssl, subprocess
ctx = ssl.create_default_context()
H = {"User-Agent": "Mozilla/5.0"}

def get(u):
    req = urllib.request.Request(u, headers=H)
    return json.loads(urllib.request.urlopen(req, timeout=25, context=ctx).read())

eids = [
    ("OHIO", "401866434"),
    ("PUR", "401858472"),
    ("AUB", "401856710"),
    ("BGSU", "401866477"),
    ("CAL", "401858247"),
    ("MD", "401858475"),
    ("UVA", "401858253"),
]
print("---WPs---")
for name, eid in eids:
    j = get(f"https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event={eid}")
    wps = j.get("winprobability") or []
    wp = wps[-1] if wps else {}
    hwp = float(wp.get("homeWinPercentage") or 0)
    h = j.get("header", {})
    comps = (h.get("competitions") or [{}])[0]
    status = (comps.get("status") or {}).get("type", {}).get("detail")
    rows = [(c.get("homeAway"), c.get("team", {}).get("abbreviation"), c.get("score")) for c in comps.get("competitors", [])]
    print(name, rows, status, "homeWP", round(hwp * 100, 1), "awayWP", round((1 - hwp) * 100, 1))

probes = [
    ("aec-cfb-aubrn-tenn-2026-10-03", "no"),
    ("aec-cfb-ohio-kentst-2026-10-03", "yes"),
    ("aec-cfb-pur-ill-2026-10-03", "yes"),
    ("aec-cfb-bowlgr-miaoh-2026-10-03", "yes"),
    ("aec-cfb-cah-unlv-2026-10-03", "no"),
    ("aec-cfb-vir-flst-2026-10-03", "no"),
]
print("---DRY---")
for slug, side in probes:
    p = subprocess.run(
        ["python", r"C:\Users\lilli\AI-Shared\tools\desk-trade.py",
         "--by", "grok-bot/satya-twin", "--slug", slug, "--side", side,
         "--size", "10",
         "--why", "dry-run book check for trading pass edge scan",
         "--kill", "dry-run only not a real kill rule",
         "--dry-run"],
        capture_output=True, text=True, timeout=90,
    )
    out = (p.stdout or "") + (p.stderr or "")
    print("PROBE", slug, side)
    print(out[:600])
    print()
