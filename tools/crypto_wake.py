"""Price watcher that wakes Jarons Twin on a big move (the Twin's idea 10/22: "wake me only on a big move, beats a timer").
Runs every minute (task "Crypto Wake"). For BTC/ETH/SOL/XRP it checks the last 5 minutes on Coinbase. If a coin moved
more than WAKE_PCT, or a 15-minute window has 7-9 minutes left with the price sitting within 0.05% of its open
(a coin flip about to land), it POSTs one short line to the Twin's webhook routine. At most one wake per 10 minutes.
URL: state/twin-webhook-url.txt. Key: keys.env TWIN_WEBHOOK_AUTH (from Key Drop; never printed).
Log: state/crypto-wake.log."""
import json, os, re, sys, time, urllib.request
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
WAKE_PCT = 0.35          # % move in 5 minutes that counts as big
COOLDOWN = 600           # seconds between wakes
STAMP = os.path.join(ROOT, "state", ".crypto-wake-last")
LOG = os.path.join(ROOT, "state", "crypto-wake.log")


try:
    sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
    from settings import setting
    SHOW_15M = setting("crypto_15m_enabled", True) not in (False, 0, "0", "false")   # off in the v2 hourly test
except Exception:
    SHOW_15M = True


def getj(url):
    return json.loads(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "hb-crypto-wake/1"}), timeout=10).read())


def candles(sym):   # Coinbase: [time, low, high, open, close, volume], newest first
    return getj(f"https://api.exchange.coinbase.com/products/{sym}-USD/candles?granularity=60")[:16]


def main():
    now = datetime.now(timezone.utc)
    reasons = []
    for sym in ("BTC", "ETH", "SOL", "XRP"):
        try:
            c = candles(sym)
            last, five = float(c[0][4]), float(c[5][4])
            move = (last / five - 1) * 100
            if abs(move) >= WAKE_PCT:
                reasons.append(f"{sym} {move:+.2f}% in 5 min (now {last:,.4f})")
            mins_into = now.minute % 15
            if 6 <= mins_into <= 8 and SHOW_15M:   # 9-7 min left: before the 6-min decision deadline (Twin caught it 10/22)
                opened = next((float(k[3]) for k in c if int(k[0]) == int(now.timestamp()) // 900 * 900), None)
                if opened and abs(last / opened - 1) * 100 <= 0.05:
                    reasons.append(f"{sym} 15m window {15 - mins_into} min left, price {last:,.4f} vs open {opened:,.4f} (coin flip)")
        except Exception as e:
            continue
    if not reasons: return
    if os.path.exists(STAMP) and time.time() - os.path.getmtime(STAMP) < COOLDOWN: return
    url = re.search(r"https://\S+", open(os.path.join(ROOT, "state", "twin-webhook-url.txt"), encoding="utf-8").read()).group(0)
    key = next((l.split("=", 1)[1].strip() for l in open(os.path.expanduser("~/.secrets/keys.env"), encoding="utf-8-sig")
                if l.startswith(("TWIN_WEBHOOK_AUTH=", "TWIN_WEBHOOK_KEY="))), "")
    if not key: return
    text = "Price wake from the MSI watcher: " + "; ".join(reasons) + ". Run crypto_view.py and make your calls (--by jarons-twin)."
    body = json.dumps({"text": text, "message": text}).encode()
    try:
        r = urllib.request.urlopen(urllib.request.Request(url, data=body, method="POST", headers={
            "Authorization": "Bearer " + key, "Content-Type": "application/json"}), timeout=20)
        status = r.status
    except urllib.error.HTTPError as e:
        status = e.code
    open(STAMP, "w").write(str(now))
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(f"{now:%Y-%m-%d %H:%M} UTC | HTTP {status} | {text[:200]}\n")


if __name__ == "__main__":
    main()
