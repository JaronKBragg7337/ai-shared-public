import json, urllib.request, ssl, subprocess, sys
sys.path.insert(0, r"C:\Users\lilli\AI-Shared\tools")
import executor as X

ctx = ssl.create_default_context()
H = {"User-Agent": "Mozilla/5.0"}

def get(u):
    req = urllib.request.Request(u, headers=H)
    return json.loads(urllib.request.urlopen(req, timeout=25, context=ctx).read())

eids = [
    ("OHIO", "401866434"),
    ("AUB", "401856710"),
    ("PUR", "401858472"),
    ("ORST", "401860899"),
    ("UK", "401856709"),
    ("MD", "401858475"),
    ("LOU", "401858248"),
    ("CAL", "401858247"),
    ("UVA", "401858253"),
    ("OSU", "401858471"),
    ("FLA", "401856708"),
    ("EMU", "401866433"),
    ("BGSU", "401866477"),
    ("NYY", None),
]
print("---WPs---")
for name, eid in eids:
    if not eid:
        continue
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

# MLB ATL-LAD and NYY-TB
for name, eid in [("ATL-LAD", "401696239"), ("NYY-TB", "401696240")]:
    try:
        j = get(f"https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/summary?event={eid}")
        wps = j.get("winprobability") or []
        wp = wps[-1] if wps else {}
        hwp = float(wp.get("homeWinPercentage") or 0)
        h = j.get("header", {})
        comps = (h.get("competitions") or [{}])[0]
        status = (comps.get("status") or {}).get("type", {}).get("detail")
        rows = [(c.get("homeAway"), c.get("team", {}).get("abbreviation"), c.get("score")) for c in comps.get("competitors", [])]
        print(name, rows, status, "homeWP", round(hwp * 100, 1), "awayWP", round((1 - hwp) * 100, 1))
    except Exception as e:
        print(name, "ERR", e)

print("---BOOKS---")
m = X.Mcp()
slugs = [
    "aec-cfb-ohio-kentst-2026-10-03",
    "aec-cfb-aubrn-tenn-2026-10-03",
    "aec-cfb-pur-ill-2026-10-03",
    "aec-cfb-oregst-colst-2026-10-03",
    "aec-cfb-uk-sc-2026-10-03",
    "aec-cfb-mary-nebr-2026-10-03",
    "aec-cfb-lou-ncst-2026-10-03",
    "aec-cfb-cah-unlv-2026-10-03",
    "aec-cfb-vir-flst-2026-10-03",
    "aec-cfb-ohiost-iowa-2026-10-03",
    "aec-cfb-fl-missr-2026-10-03",
    "aec-cfb-bowlgr-miaoh-2026-10-03",
    "aec-cfb-emich-umass-2026-10-03",
    "tsc-cfb-alaam-jackst-2026-10-03-total-51pt5",
    "tsc-cfb-alaam-jackst-2026-10-03-total-52pt5",
    "aec-mlb-atl-lad-2026-10-03",
    "aec-mlb-nyy-tb-2026-10-03",
]
for slug in slugs:
    try:
        b = m.call("polymarket_get_book", {"market_slug": slug})
        # normalize
        bid = ask = None
        if isinstance(b, dict):
            bid = b.get("bid") or b.get("best_bid")
            ask = b.get("ask") or b.get("best_ask")
            if bid is None and "book" in b:
                bk = b["book"]
                bid = bk.get("bid") or bk.get("best_bid")
                ask = bk.get("ask") or bk.get("best_ask")
        print(slug, "bid/ask", bid, ask, str(b)[:180].replace("\n"," "))
    except Exception as e:
        print(slug, "ERR", e)

print("---OPEN ORDERS---")
try:
    oo = m.call("polymarket_open_orders", {})
    orders = (oo or {}).get("orders") or oo or []
    if isinstance(orders, dict):
        orders = orders.get("orders") or []
    print("count", len(orders) if isinstance(orders, list) else type(orders))
    for o in (orders if isinstance(orders, list) else [])[:30]:
        print(json.dumps(o, default=str)[:300])
except Exception as e:
    print("open_orders ERR", e)

print("---POSITIONS---")
try:
    pos = m.call("polymarket_positions", {})
    print(str(pos)[:2000])
except Exception as e:
    print("pos ERR", e)
