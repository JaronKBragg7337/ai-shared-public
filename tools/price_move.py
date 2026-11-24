"""price_move.py - EARLY move alert (Jaron 11/15 4:31 AM: "I get the notification way after it happened").
Runs every 5 min inside HB Price Alerts' schedule (called at the end of price_alert.py). Keeps ~30 min of prices
per coin; buzzes once when a coin moves >= THRESH % within 15 min (the START of a move), then stays quiet
for COOLDOWN minutes for that coin. Alerts only, never trades. Coinbase public spot, no key.
Edit COINS / THRESH below. State: state/price-move.json
"""
import os, json, time, urllib.request
ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
ST = os.path.join(ROOT, "state", "price-move.json")
SEC = os.path.join(os.path.expanduser("~"), ".secrets", "keys.env")
COINS = ["BTC", "ETH", "SOL", "XRP"]
THRESH = {"BTC": 1.5, "ETH": 2.0, "SOL": 2.5, "XRP": 2.5}
WINDOW, COOLDOWN = 15 * 60, 120 * 60

def topic():
    for l in open(SEC, encoding="utf-8"):
        if l.startswith("NTFY_TOPIC="): return l.split("=", 1)[1].strip()

def price(sym):
    r = urllib.request.urlopen("https://api.coinbase.com/v2/prices/%s-USD/spot" % sym, timeout=15)
    return float(json.load(r)["data"]["amount"])

st = json.load(open(ST, encoding="utf-8")) if os.path.exists(ST) else {}
now = time.time()
for c in COINS:
    try: p = price(c)
    except Exception: continue
    s = st.setdefault(c, {"hist": [], "last_alert": 0})
    s["hist"] = [h for h in s["hist"] if now - h[0] <= 30 * 60] + [[now, p]]
    old = [h for h in s["hist"] if now - h[0] <= WINDOW + 60]
    base = old[0][1] if old else p
    pct = (p / base - 1) * 100
    if abs(pct) >= THRESH[c] and now - s["last_alert"] >= COOLDOWN:
        mins = int((now - old[0][0]) / 60) if old else 0
        msg = "%s %s %.1f%% in %d min: $%s -> $%s (move just starting)" % (c, "UP" if pct > 0 else "DOWN", abs(pct), max(mins, 1), f"{base:,.2f}", f"{p:,.2f}")
        urllib.request.urlopen(urllib.request.Request("https://ntfy.sh/" + topic(), msg.encode(), {"Title": "Price moving", "Priority": "default"}), timeout=15)
        s["last_alert"] = now
json.dump(st, open(ST, "w", encoding="utf-8"))
