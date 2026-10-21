import json, urllib.request, ssl, subprocess, sys
sys.path.insert(0, r"C:\Users\lilli\AI-Shared\tools")
import executor as X

ctx = ssl.create_default_context()
H = {"User-Agent": "Mozilla/5.0"}

def get(u):
    req = urllib.request.Request(u, headers=H)
    return json.loads(urllib.request.urlopen(req, timeout=25, context=ctx).read())

# Cancel stray old-gast order
m = X.Mcp()
oid = "CWGHMF52AYH0"
slug = "aec-cfb-old-gast-2026-10-03"
print("CANCEL", oid, slug)
r = m.call("polymarket_cancel_order", {"order_id": oid, "market_slug": slug})
print(json.dumps(r)[:500])
orders = m.call("polymarket_open_orders", {})
print("open_orders_left", len((orders or {}).get("orders") or []))

eids = [
    ("OHIO", "401866434"),
    ("AUB", "401856710"),
    ("PUR", "401858472"),
    ("BGSU", "401866477"),
    ("ORST", "401860899"),
    ("LOU", "401858248"),
    ("ODU", "401869956"),
    ("CAL", "401858247"),
    ("UK", "401856709"),
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
