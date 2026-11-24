"""crypto_signals.py - the few signals that matter for 15m/1h up/down (Jaron 10/23: Polymarket's price lags the real market;
the lag is the edge). Free sources only. Used by crypto_view.py. Each function returns short text lines (or [] when quiet).

  lag_line      real-money spot (Coinbase + Kraken, each against its OWN window open, so exchange basis cancels) -> fair chance
                Up, vs what Polymarket asks for Up / Down right now. Prints only when the gap is >= LAG_MIN.
  flow_line     last ~2 min of taker trades on Coinbase + Kraken: buy vs sell dollars and the biggest print.
  fake_line     a sharp spike that looks fake: thin volume, one exchange only, or already fading.
  events_lines  scheduled market movers (FOMC / CPI / jobs) as "in X min/h", from a hardcoded official calendar.
  news_lines    latest crypto headlines (CoinDesk + Cointelegraph RSS) and ETF-flow headlines (Google News RSS), cached 5 min.
"""
import json, math, os, re, time, urllib.request
from datetime import datetime, timezone, timedelta
from email.utils import parsedate_to_datetime
from xml.etree import ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
LAG_MIN = 0.08          # a gap of 8 cents or more is worth printing
FLOW_MIN = 120          # seconds of trades to read (the 'last 1-3 minutes')
UA = {"User-Agent": "Mozilla/5.0 hb-crypto-signals/1"}

# Official dates, verified 2026-10-23: FOMC (federalreserve.gov/monetarypolicy/fomccalendars.htm - decision 2:00 PM ET on the
# 2nd day), BLS CPI + Employment Situation (bls.gov/schedule/news_release/) - all 8:30 AM ET. Times below are UTC (ET = UTC-4
# until Nov 1, UTC-5 after). Add the next ones when these pass.
EVENTS = [
    ("FOMC rate decision", "2026-10-28T18:00:00+00:00"),
    ("Jobs report (Oct)", "2026-11-06T13:30:00+00:00"),
    ("CPI inflation (Oct)", "2026-11-10T13:30:00+00:00"),
    ("Jobs report (Nov)", "2026-12-04T13:30:00+00:00"),
    ("FOMC rate decision", "2026-12-09T19:00:00+00:00"),
    ("CPI inflation (Nov)", "2026-12-10T13:30:00+00:00"),
]


def _get(url, timeout=10):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout).read()


def _getj(url, timeout=10):
    return json.loads(_get(url, timeout))


def _phi(z):
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


# ---- a) LAG ---------------------------------------------------------------------------------------------------------------
def coinbase_open(coin, t):
    """Coinbase 1-minute candle open at t (UTC datetime), or None."""
    try:
        s = t.strftime("%Y-%m-%dT%H:%M:%SZ"); e = (t + timedelta(minutes=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
        rows = _getj(f"https://api.exchange.coinbase.com/products/{coin.upper()}-USD/candles?granularity=60&start={s}&end={e}")
        for c in rows:
            if int(c[0]) == int(t.timestamp()): return float(c[3])
    except Exception:
        pass
    return None


def move_since_open(coin, kraken_spot, kraken_open, start):
    """Average of (Coinbase spot / Coinbase open) and (Kraken spot / Kraken open) - each against its own open, so the gap
    between exchanges cancels. Returns (ratio, note)."""
    ratios = []
    if kraken_open: ratios.append(kraken_spot / kraken_open)
    try:
        cb_spot = float(_getj(f"https://api.coinbase.com/v2/prices/{coin.upper()}-USD/spot")["data"]["amount"])
        cb_open = coinbase_open(coin, start)
        if cb_open: ratios.append(cb_spot / cb_open)
    except Exception:
        pass
    if not ratios: return None
    return sum(ratios) / len(ratios)


def gap(ratio, sigma, minutes_left, up_ask, down_cost):
    """Returns (fair_up, edge_up, edge_down). edge = fair chance of that side minus what Polymarket asks for it."""
    if ratio is None or sigma <= 0: return None
    if minutes_left <= 0.05: fair = 1.0 if ratio >= 1 else 0.0
    else: fair = _phi(math.log(ratio) / (sigma * math.sqrt(minutes_left)))
    eu = (fair - up_ask) if up_ask else None
    ed = ((1 - fair) - down_cost) if down_cost else None
    return fair, eu, ed


def lag_line(ratio, sigma, minutes_left, up_ask, down_cost):
    g = gap(ratio, sigma, minutes_left, up_ask, down_cost)
    if not g: return None
    fair, eu, ed = g
    best = max((e, s) for e, s in ((eu, "Up"), (ed, "Down")) if e is not None) if (eu is not None or ed is not None) else None
    if not best or best[0] < LAG_MIN: return None
    e, s = best
    if s == "Up":
        return f"POLY LAGS: spot says Up {fair:.0%}, Poly asks {up_ask:.2f} for Up -> {e * 100:.0f}c gap (Up looks cheap)"
    return f"POLY LAGS: spot says Down {1 - fair:.0%}, Poly asks {down_cost:.2f} for Down -> {e * 100:.0f}c gap (Down looks cheap)"


# ---- b) FLOW --------------------------------------------------------------------------------------------------------------
def flow_line(coin, pair):
    now = time.time(); buy = sell = 0.0; big = (0.0, "", "")
    n = 0
    try:   # Coinbase: 'side' is the MAKER side, so a 'sell' maker = a taker BUY
        for t in _getj(f"https://api.exchange.coinbase.com/products/{coin.upper()}-USD/trades?limit=1000"):
            ts = datetime.fromisoformat(t["time"].replace("Z", "+00:00")).timestamp()
            if now - ts > FLOW_MIN: break
            usd = float(t["price"]) * float(t["size"]); taker = "buy" if t["side"] == "sell" else "sell"; n += 1
            if taker == "buy": buy += usd
            else: sell += usd
            if usd > big[0]: big = (usd, taker, "Coinbase")
    except Exception:
        pass
    try:
        r = _getj(f"https://api.kraken.com/0/public/Trades?pair={pair}&since={int(now - FLOW_MIN)}000000000")
        for t in next(v for k, v in r["result"].items() if k != "last"):
            usd = float(t[0]) * float(t[1]); taker = "buy" if t[3] == "b" else "sell"; n += 1
            if taker == "buy": buy += usd
            else: sell += usd
            if usd > big[0]: big = (usd, taker, "Kraken")
    except Exception:
        pass
    tot = buy + sell
    if not n or tot <= 0: return "FLOW: n/a"
    pct = buy / tot
    lean = "real money BUYING" if pct >= 0.62 else "real money SELLING" if pct <= 0.38 else "balanced"
    k = lambda v: f"${v / 1000:,.0f}k" if v >= 10000 else f"${v:,.0f}"
    return (f"FLOW last {FLOW_MIN // 60} min (Coinbase+Kraken taker trades): buys {k(buy)} vs sells {k(sell)} ({pct:.0%} buy) -> {lean}"
            f" | biggest print {big[1]} {k(big[0])} on {big[2]}")


# ---- c) PUMP-FAKE ---------------------------------------------------------------------------------------------------------
def fake_line(coin, kr_hist, sigma):
    """kr_hist: Kraken 1-min candles [t, o, h, l, c, vwap, vol, n], oldest first. Looks at the last 5 minutes vs the 2 hours before."""
    try:
        if len(kr_hist) < 40: return None
        last5, base = kr_hist[-5:], kr_hist[:-5]
        p0, p1 = float(last5[0][1]), float(last5[-1][4])
        mv = (p1 / p0 - 1)
        z = abs(mv) / (sigma * math.sqrt(5)) if sigma else 0
        if z < 2.5: return None
        up = mv > 0
        why = []
        vol5 = sum(float(c[6]) for c in last5) / 5
        vols = sorted(float(c[6]) for c in base)
        med = vols[len(vols) // 2] if vols else 0
        if med and vol5 < 1.5 * med: why.append(f"thin volume ({vol5 / med:.1f}x a normal minute)")
        peak = max(float(c[2]) for c in last5) if up else min(float(c[3]) for c in last5)
        full = abs(peak / p0 - 1)
        back = abs(peak / p1 - 1)
        if full > 0 and back / full >= 0.35: why.append(f"already fading ({back / full:.0%} of the spike given back)")
        try:   # one exchange only: Coinbase 5-min move vs Kraken's
            cb = _getj(f"https://api.exchange.coinbase.com/products/{coin.upper()}-USD/candles?granularity=60")[:6]
            cmv = float(cb[0][4]) / float(cb[5][4]) - 1
            if abs(mv) > 0 and (abs(cmv) < 0.4 * abs(mv) or (cmv > 0) != (mv > 0)):
                why.append(f"Kraken moved {mv * 100:+.2f}% but Coinbase only {cmv * 100:+.2f}% (one exchange)")
            elif abs(cmv) > 0 and abs(mv) < 0.4 * abs(cmv):
                why.append(f"Coinbase moved {cmv * 100:+.2f}% but Kraken only {mv * 100:+.2f}% (one exchange)")
        except Exception:
            pass
        if not why: return f"SPIKE {mv * 100:+.2f}% in 5 min ({z:.1f}x normal) with real volume on both exchanges - looks genuine"
        return f"POSSIBLE FAKE MOVE: {mv * 100:+.2f}% in 5 min ({z:.1f}x normal) but " + "; ".join(why)
    except Exception:
        return None


# ---- d) EVENTS + NEWS -----------------------------------------------------------------------------------------------------
def events_lines(now=None):
    now = now or datetime.now(timezone.utc)
    out = []
    for name, iso in EVENTS:
        t = datetime.fromisoformat(iso); m = (t - now).total_seconds() / 60
        if m < -30: continue
        if m <= 0: out.append(f"EVENT NOW: {name} (released {-m:.0f} min ago) - expect wild moves")
        elif m <= 180: out.append(f"EVENT in {m:.0f} min: {name} - prices can jump; don't trust small edges")
        elif m <= 72 * 60: out.append(f"event in {m / 60:.0f} h: {name}")
        if len(out) >= 2: break
    if not out:
        nxt = next(((n, datetime.fromisoformat(i)) for n, i in EVENTS if datetime.fromisoformat(i) > now), None)
        if nxt: out.append(f"no scheduled event soon (next: {nxt[0]} on {nxt[1]:%b %d}, {(nxt[1] - now).total_seconds() / 86400:.0f} days)")
    return out


NEWS_CACHE = os.path.join(ROOT, "state", "crypto-news-cache.json")
FEEDS = [("CoinDesk", "https://www.coindesk.com/arc/outboundfeeds/rss/"), ("Cointelegraph", "https://cointelegraph.com/rss")]
ETF_FEED = "https://news.google.com/rss/search?q=bitcoin+OR+ethereum+ETF+flows+when:1d&hl=en-US&gl=US&ceid=US:en"


def _rss(url, src, limit=12):
    items = []
    root = ET.fromstring(_get(url, 12))
    for it in root.iter("item"):
        try:
            t = (it.findtext("title") or "").strip()
            d = parsedate_to_datetime(it.findtext("pubDate")).astimezone(timezone.utc)
            items.append({"t": t, "at": d.isoformat(), "src": src})
        except Exception:
            continue
        if len(items) >= limit: break
    return items


def news_items():
    try:
        c = json.load(open(NEWS_CACHE))
        if time.time() - c["ts"] < 300: return c["news"], c["etf"]
    except Exception:
        pass
    news, etf = [], []
    for src, url in FEEDS:
        try: news += _rss(url, src)
        except Exception: pass
    try: etf = [i for i in _rss(ETF_FEED, "news", 15) if re.search(r"\bETF", i["t"])]
    except Exception: pass
    try: json.dump({"ts": time.time(), "news": news, "etf": etf}, open(NEWS_CACHE, "w"))
    except OSError: pass
    return news, etf


def news_lines(now=None, n=4, max_hours=6):
    now = now or datetime.now(timezone.utc)
    news, etf = news_items()
    def age(i):
        m = (now - datetime.fromisoformat(i["at"])).total_seconds() / 60
        return f"{m:.0f} min ago" if m < 90 else f"{m / 60:.0f} h ago"
    fresh = sorted((i for i in news if (now - datetime.fromisoformat(i["at"])).total_seconds() < max_hours * 3600),
                   key=lambda i: i["at"], reverse=True)[:n]
    out = [f"  - {i['t'][:110]} ({i['src']}, {age(i)})" for i in fresh] or ["  - no crypto headlines in the last %d h" % max_hours]
    fe = sorted(etf, key=lambda i: i["at"], reverse=True)[:2]
    if fe: out += ["ETF flows:"] + [f"  - {re.sub(r' - [^-]+$', '', i['t'])[:110]} ({age(i)})" for i in fe]
    return out
