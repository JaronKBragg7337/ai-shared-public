"""Price alerts to Jaron's phone (ntfy). Alerts only - it never trades; he sells himself in the app.
state/price-alerts.json: [{"sym": "QNT", "above": 275, "note": "..."}]. Each alert buzzes once, then is marked done.
Price: Coinbase public spot (free, no key). Task "HB Price Alerts", every 5 min."""
import os, json, datetime, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
CFG = os.path.join(ROOT, "state", "price-alerts.json")
SEC = os.path.join(os.path.expanduser("~"), ".secrets", "keys.env")


def topic():
    for l in open(SEC, encoding="utf-8"):
        if l.startswith("NTFY_TOPIC="): return l.split("=", 1)[1].strip()


def price(sym):
    r = urllib.request.urlopen("https://api.coinbase.com/v2/prices/%s-USD/spot" % sym, timeout=15)
    return float(json.load(r)["data"]["amount"])


alerts = json.load(open(CFG, encoding="utf-8")) if os.path.exists(CFG) else []
changed = False
for a in alerts:
    if a.get("done"): continue
    try: p = price(a["sym"])
    except Exception: continue
    hit = ("above" in a and p >= a["above"]) or ("below" in a and p <= a["below"])
    if hit:
        msg = "%s is $%.2f (alert %s $%s). %s" % (a["sym"], p, "above" if "above" in a else "below", a.get("above", a.get("below")), a.get("note", ""))
        urllib.request.urlopen(urllib.request.Request("https://ntfy.sh/" + topic(), msg.encode(), {"Title": "Price alert", "Priority": "high"}), timeout=15)
        a["done"] = datetime.datetime.now().isoformat(timespec="minutes"); a["price_hit"] = p; changed = True
if changed: json.dump(alerts, open(CFG, "w", encoding="utf-8"), indent=1)

# 11/15: early move alerts (start of a move, not after)
try:
    import runpy; runpy.run_path(os.path.join(ROOT, "tools", "price_move.py"))
except Exception:
    pass
