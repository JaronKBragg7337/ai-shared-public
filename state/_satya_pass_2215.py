import json, urllib.request, ssl, subprocess
ctx = ssl.create_default_context()
H = {"User-Agent": "Mozilla/5.0"}

def get(u):
    req = urllib.request.Request(u, headers=H)
    return json.loads(urllib.request.urlopen(req, timeout=25, context=ctx).read())

eids = [
    ("OHIO", "401866434"),
    ("AUB", "401856710"),
    ("PUR", "401858472"),
    ("BGSU", "401866477"),
    ("CAL", "401858247"),
    ("MD", "401858475"),
    ("UVA", "401858253"),
    ("LOU", "401858474"),
    ("UK", "401858252"),
    ("EMU", "401866433"),
    ("ODU", "401866435"),
    ("ORST", "401858476"),
]
print("---WPs---")
for name, eid in eids:
    try:
        j = get(f"https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event={eid}")
    except Exception as e:
        print(name, "ERR", e)
        continue
    wps = j.get("winprobability") or []
    wp = wps[-1] if wps else {}
    hwp = float(wp.get("homeWinPercentage") or 0)
    h = j.get("header", {})
    comps = (h.get("competitions") or [{}])[0]
    status = (comps.get("status") or {}).get("type", {}).get("detail")
    state = (comps.get("status") or {}).get("type", {}).get("state")
    rows = [(c.get("homeAway"), c.get("team", {}).get("abbreviation"), c.get("score")) for c in comps.get("competitors", [])]
    print(name, rows, status, state, "homeWP", round(hwp * 100, 1), "awayWP", round((1 - hwp) * 100, 1))
