import json, urllib.request, ssl, subprocess
ctx = ssl.create_default_context()
H = {"User-Agent": "Mozilla/5.0"}

def get(u):
    req = urllib.request.Request(u, headers=H)
    return json.loads(urllib.request.urlopen(req, timeout=25, context=ctx).read())

# Ohio recheck + BGSU + PUR ILL details
for name, eid in [("OHIO","401866434"),("BGSU","401866477"),("PUR","401858472"),("EMU","401866433")]:
    j = get(f"https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event={eid}")
    wps = j.get("winprobability") or []
    wp = wps[-1] if wps else {}
    hwp = float(wp.get("homeWinPercentage") or 0)
    comps = (j.get("header", {}).get("competitions") or [{}])[0]
    status = (comps.get("status") or {}).get("type", {}).get("detail")
    rows = [(c.get("homeAway"), c.get("team", {}).get("abbreviation"), c.get("score")) for c in comps.get("competitors", [])]
    print(name, rows, status, "homeWP", round(hwp*100,1), "awayWP", round((1-hwp)*100,1))

# dry NO Illinois via PUR short? actually want YES Illinois = NO Purdue
p = subprocess.run(
    ["python", r"C:\Users\lilli\AI-Shared\tools\desk-trade.py",
     "--by", "grok-bot/satya-twin", "--slug", "aec-cfb-pur-ill-2026-10-03", "--side", "no",
     "--size", "10", "--why", "dry-run book check Illinois favourite trailing Purdue",
     "--kill", "dry-run only not a live kill", "--dry-run"],
    capture_output=True, text=True, timeout=90,
)
print("PUR NO (ILL yes)")
print(((p.stdout or "")+(p.stderr or ""))[:500])
