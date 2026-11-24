"""Crypto up/down board for Jarons Twin (Jaron 10/22: "hook it to the right things so it's easier to read").
One screen per coin: the open Polymarket US up/down markets (15 min, hourly, daily), what each one is measured against
(the coin's price when the window opened), where the price is now, time left, short-term momentum, and the book.
Read only. Prices come from Kraken's free public API (no key) as a close stand-in for CF Benchmarks, which settles them.

    python tools/crypto_view.py            all four coins
    python tools/crypto_view.py btc        one coin
    python tools/crypto_view.py corr       only the 24 h correlation reading (also written to state/crypto-correlation.json)
"""
import json, math, re, sys, os, urllib.request
from datetime import datetime, timezone, timedelta

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
import verifier as V  # noqa: E402
import crypto_signals as SIG  # noqa: E402
from settings import setting  # noqa: E402

COINS = {"btc": ("XBTUSD", "bitcoin up or down"), "eth": ("ETHUSD", "ethereum up or down"),
         "sol": ("SOLUSD", "solana up or down"), "xrp": ("XRPUSD", "xrp up or down")}
SPAN = {"15m": timedelta(minutes=15), "1h": timedelta(hours=1), "1d": timedelta(days=1)}
SLUG = re.compile(r"-updown-(15m|1h|1d)-(\d{4}-\d{2}-\d{2})-(\d{2})(\d{2})z$")


def kraken(path):
    return json.loads(urllib.request.urlopen("https://api.kraken.com/0/public/" + path, timeout=15).read())["result"]


def candles(pair, minutes):
    r = kraken(f"OHLC?pair={pair}&interval={minutes}")
    return next(v for k, v in r.items() if k != "last")   # [time, open, high, low, close, vwap, volume, count]


def blend(coin):
    """BRTI-style stand-in (Twin 10/22 #2): median of Coinbase, Kraken, Bitstamp, Gemini spot - CF Benchmarks' real-time
    index is built from these same exchanges; the official index itself isn't free to read."""
    sym = coin.upper(); px = []
    for url, get in ((f"https://api.coinbase.com/v2/prices/{sym}-USD/spot", lambda j: j["data"]["amount"]),
                     (f"https://www.bitstamp.net/api/v2/ticker/{coin}usd/", lambda j: j["last"]),
                     (f"https://api.gemini.com/v1/pubticker/{coin}usd", lambda j: j["last"])):
        try: px.append(float(get(json.loads(urllib.request.urlopen(url, timeout=8).read()))))
        except Exception: pass
    return px


def fair_up(spot, base, sigma_min, minutes_left):
    """Twin #3: chance the price ends >= the open, from realized 1-min volatility (simple random-walk model)."""
    if minutes_left <= 0 or sigma_min <= 0: return 1.0 if spot >= base else 0.0
    z = math.log(spot / base) / (sigma_min * math.sqrt(minutes_left))
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


FUT = {"btc": "PF_XBTUSD", "eth": "PF_ETHUSD", "sol": "PF_SOLUSD", "xrp": "PF_XRPUSD"}
OI_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "state", "crypto-oi-last.json")


def getj(url):   # Coinbase Exchange refuses requests without a User-Agent
    return json.loads(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "hb-crypto-view/1"}), timeout=10).read())


def extras(coin, spot):
    """The free three (Jaron 10/22): futures funding + open-interest change, options-implied volatility, multi-exchange books.
    Returns (text lines, implied 1-min sigma or None)."""
    out, iv_sigma = [], None
    try:   # Kraken Futures perpetuals: who is paying whom, and is money piling in or leaving
        t = next(x for x in getj("https://futures.kraken.com/derivatives/api/v3/tickers")["tickers"] if x["symbol"] == FUT[coin])
        rel = float(t["fundingRate"]) / float(t["markPrice"]) * 100
        oi = float(t["openInterest"])
        try: last = json.load(open(OI_FILE))
        except Exception: last = {}
        prev = last.get(coin)
        chg = f"{(oi / prev['oi'] - 1) * 100:+.2f}% since {prev['at'][11:16]} UTC" if prev else "first reading"
        last[coin] = {"oi": oi, "at": datetime.now(timezone.utc).isoformat()}
        json.dump(last, open(OI_FILE, "w"))
        lean = "longs paying shorts (crowd leans UP)" if rel > 0 else "shorts paying longs (crowd leans DOWN)"
        out.append(f"futures: funding {rel:+.4f}%/h, {lean} | open interest {oi:,.0f} ({chg})")
    except Exception as e:
        out.append(f"futures: n/a ({type(e).__name__})")
    if coin in ("btc", "eth"):   # Deribit DVOL = what options traders expect over the next 30 days, annualized
        try:
            now_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
            d = getj(f"https://www.deribit.com/api/v2/public/get_volatility_index_data?currency={coin.upper()}"
                     f"&resolution=60&start_timestamp={now_ms - 600000}&end_timestamp={now_ms}")["result"]["data"]
            dvol = float(d[-1][4]); iv_sigma = dvol / 100 / math.sqrt(525600)
            out.append(f"options: implied volatility {dvol:.1f}% a year (Deribit DVOL) = about {iv_sigma * 100:.3f}% per minute")
        except Exception as e:
            out.append(f"options: n/a ({type(e).__name__})")
    try:   # order books near the price: who is stacked closer - buyers or sellers
        books = []
        cb = getj(f"https://api.exchange.coinbase.com/products/{coin.upper()}-USD/book?level=2")
        books.append(("Coinbase", [(float(p), float(q)) for p, q, *_ in cb["bids"]], [(float(p), float(q)) for p, q, *_ in cb["asks"]]))
        kr = next(iter(getj(f"https://api.kraken.com/0/public/Depth?pair={COINS[coin][0]}&count=200")["result"].values()))
        books.append(("Kraken", [(float(p), float(q)) for p, q, _ in kr["bids"]], [(float(p), float(q)) for p, q, _ in kr["asks"]]))
        bid_usd = ask_usd = 0.0; wall = (0, "", 0.0)
        for name, bids, asks in books:
            for side, levels in (("buy", bids), ("sell", asks)):
                for p, q in levels:
                    if abs(p / spot - 1) > 0.002: continue
                    usd = p * q
                    if side == "buy": bid_usd += usd
                    else: ask_usd += usd
                    if usd > wall[0]: wall = (usd, f"{name} {side} wall ${usd:,.0f} at {p:,.4f}", p)
        tilt = bid_usd / (bid_usd + ask_usd) if bid_usd + ask_usd else 0.5
        out.append(f"books within 0.2% (Coinbase+Kraken): buyers ${bid_usd:,.0f} vs sellers ${ask_usd:,.0f} -> {tilt:.0%} buy side | biggest: {wall[1]}")
    except Exception as e:
        out.append(f"books: n/a ({type(e).__name__})")
    return out, iv_sigma


def et(t):
    return (t - timedelta(hours=4)).strftime("%I:%M %p").lstrip("0") + " ET"   # EDT until Nov 1


def window(slug):
    m = SLUG.search(slug)
    if not m: return None
    start = datetime.strptime(f"{m.group(2)} {m.group(3)}{m.group(4)}", "%Y-%m-%d %H%M").replace(tzinfo=timezone.utc)
    return m.group(1), start, start + SPAN[m.group(1)]


def price_at(pair, t):
    """open price of the candle that starts at t (1-minute candles reach back 12 h; older windows use 1-hour)."""
    for minutes in (1, 60):
        for c in candles(pair, minutes):
            if int(c[0]) == int(t.timestamp()): return float(c[1])
    return None


def book_prices(mcp, slug):
    """(Up ask, Down cost) - the prices a buyer would really pay right now; None for a side nobody is selling."""
    md = (mcp.call("polymarket_bbo", {"slug": slug}).get("marketData") or {})
    def px(k):
        try:
            v = float((md.get(k) or {}).get("value"))
            return v if 0 < v < 1 else None
        except (TypeError, ValueError):
            return None
    return px("bestAsk"), px("shortQuote"), md


def enabled_tfs():
    """Window types the lane trades right now (Control Room rows crypto_15m_enabled / crypto_1d_enabled; hourly is always on)."""
    on = {"1h"}
    if setting("crypto_15m_enabled", True) not in (False, "false", "False", 0): on.add("15m")
    if setting("crypto_1d_enabled", True) not in (False, "false", "False", 0): on.add("1d")
    return on


def board(coin, mcp, now):
    pair, query = COINS[coin]
    spot = float(next(iter(kraken(f"Ticker?pair={pair}").values()))["c"][0])
    hist = candles(pair, 1)[-121:]
    rets = [math.log(float(b[4]) / float(a[4])) for a, b in zip(hist, hist[1:]) if float(a[4]) > 0]
    mu = sum(rets) / len(rets); sigma = math.sqrt(sum((r - mu) ** 2 for r in rets) / max(len(rets) - 1, 1))
    others = blend(coin)
    mid = sorted(others + [spot])[len(others + [spot]) // 2]
    one = hist[-16:]
    mom5 = (spot / float(one[-6][4]) - 1) * 100 if len(one) > 6 else 0
    mom15 = (spot / float(one[0][1]) - 1) * 100
    print(f"\n{coin.upper()}  Kraken {spot:,.4f} | blended {mid:,.4f} (median of Coinbase/Bitstamp/Gemini/Kraken, closer to the "
          f"settlement index) | last 5 min {mom5:+.2f}% | last 15 min {mom15:+.2f}% | 1-min volatility {sigma * 100:.3f}%")
    spot = mid
    kr_spot = float(next(iter(kraken(f"Ticker?pair={pair}").values()))["c"][0])
    for l in (SIG.flow_line(coin, pair), SIG.fake_line(coin, hist, sigma)):
        if l: print("  " + l)
    more, iv = extras(coin, spot)
    for l in more: print("  " + l)
    tfs = enabled_tfs()
    sym = {"btc": "BTC", "eth": "ETH", "sol": "SOL", "xrp": "XRP"}[coin]
    events = []   # one search doesn't return every timeframe (10/22: ETH/SOL hourly+daily missing) - ask per timeframe
    for q in (query, f"{sym} hourly up or down", f"{sym} daily up or down"):
        events += mcp.call("polymarket_search", {"query": q}).get("events") or []
    seen, slugs = [], set()
    for ev in events:
        for mk in ev.get("markets") or []:
            w = window(mk.get("slug") or "")
            if not w or not mk.get("tradeable") or mk["slug"] in slugs: continue
            slugs.add(mk["slug"])
            tf, start, end = w
            if not (start <= now < end) or tf not in tfs: continue
            seen.append((tf, mk, start, end))
    if not seen: print("  no open up/down market found right now"); return
    for tf, mk, start, end in sorted(seen, key=lambda x: list(SPAN).index(x[0])):
        base = price_at(pair, start)
        left = int((end - now).total_seconds() // 60)
        up_ask = down_cost = None
        try:   # Twin #1: the Down side's real price + depth (buying Down = the short quote)
            up_ask, down_cost, md = book_prices(mcp, mk["slug"])
            g = lambda k: (md.get(k) or {}).get("value")
            book = f"Up bid {g('bestBid')} / ask {g('bestAsk')} | Down costs {g('shortQuote')} | depth bid {md.get('bidDepth')} / ask {md.get('askDepth')}"
            if up_ask is None and down_cost is None: book += "  (NO BOOK: nothing to buy - do not call)"
        except Exception:
            book = f"Up bid {(mk.get('bestBidQuote') or {}).get('value')} / ask {(mk.get('bestAskQuote') or {}).get('value')}"
        if base:
            f = fair_up(spot, base, sigma, (end - now).total_seconds() / 60)
            fiv = f" (options-implied: {fair_up(spot, base, iv, (end - now).total_seconds() / 60):.0%})" if iv else ""
            move = f"{(spot / base - 1) * 100:+.3f}% vs open {base:,.4f} -> {'UP so far' if spot >= base else 'DOWN so far'} | fair chance Up {f:.0%}{fiv}"
        else:
            move = "open price not found"
        print(f"  {tf:>3}  {et(start)}-{et(end)}  {left:>4} min left  {move}")
        print(f"        {book}   {mk['slug']}")
        if base:
            lag = SIG.lag_line(SIG.move_since_open(coin, kr_spot, base, start), max(iv or 0, sigma), (end - now).total_seconds() / 60, up_ask, down_cost)
            if lag: print("        >>> " + lag)


CORR_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "state", "crypto-correlation.json")


def minute_closes(coin, hours=24):
    """{unix minute: close} for the last `hours` of 1-minute candles. Kraken's OHLC keeps only 12 h of 1-minute candles, so the
    full 24 h is paged from Coinbase Exchange (free, 300 per page); if that fails, Kraken's 12 h of 1-minute candles is used."""
    out = {}
    try:
        end = datetime.now(timezone.utc).replace(second=0, microsecond=0)
        t = end - timedelta(hours=hours)
        while t < end:
            t2 = min(t + timedelta(minutes=299), end)
            rows = getj(f"https://api.exchange.coinbase.com/products/{coin.upper()}-USD/candles?granularity=60"
                        f"&start={t.strftime('%Y-%m-%dT%H:%M:%SZ')}&end={t2.strftime('%Y-%m-%dT%H:%M:%SZ')}")
            for c in rows: out[int(c[0])] = float(c[4])
            t = t2 + timedelta(minutes=1)
        if len(out) > hours * 60 * 0.8: return out, "Coinbase 1-min"
    except Exception:
        pass
    return {int(c[0]): float(c[4]) for c in candles(COINS[coin][0], 1)}, "Kraken 1-min (12 h only)"


def pearson(x, y):
    n = len(x)
    if n < 30: return None
    mx, my = sum(x) / n, sum(y) / n
    sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
    sx = math.sqrt(sum((a - mx) ** 2 for a in x)); sy = math.sqrt(sum((b - my) ** 2 for b in y))
    return sxy / (sx * sy) if sx and sy else None


def correlations(write=True):
    """Rolling 24 h correlation of 1-minute returns between every coin pair (Jaron 10/22: coins may split away, e.g. QNT -
    measure it, don't assume it). Writes state/crypto-correlation.json for crypto_decide's shared-cap logic.
    Returns the dict: {"at", "source", "pairs": {"btc-eth": r}, "max_with_others": {"btc": r}}."""
    series, src = {}, set()
    for c in COINS:
        series[c], s = minute_closes(c); src.add(s)
    def rets(c):
        d = series[c]
        return {t: math.log(d[t] / d[t - 60]) for t in d if t - 60 in d and d[t - 60] > 0}
    R = {c: rets(c) for c in COINS}
    pairs = {}
    cl = list(COINS)
    for i, a in enumerate(cl):
        for b in cl[i + 1:]:
            ts = sorted(set(R[a]) & set(R[b]))
            r = pearson([R[a][t] for t in ts], [R[b][t] for t in ts])
            if r is not None: pairs[f"{a}-{b}"] = round(r, 3)
    mx = {}
    for c in cl:
        v = [r for k, r in pairs.items() if c in k.split("-")]
        if v: mx[c] = round(max(v), 3)
    out = {"at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "window_hours": 24, "source": " + ".join(sorted(src)),
           "pairs": pairs, "max_with_others": mx}
    if write:
        try: json.dump(out, open(CORR_FILE, "w"), indent=1)
        except OSError: pass
    return out


def corr_line(c):
    p = " ".join(f"{k.upper().replace('-', '/')} {v:.2f}" for k, v in c["pairs"].items())
    least = min(c["max_with_others"].items(), key=lambda kv: kv[1]) if c["max_with_others"] else None
    return (f"CORRELATION 24 h of 1-min returns ({c['source']}): {p}" +
            (f" | most independent coin: {least[0].upper()} (best match to any other {least[1]:.2f})" if least else ""))


def main():
    now = datetime.now(timezone.utc)
    if sys.argv[1:] == ["corr"]:
        print(corr_line(correlations())); return
    mcp = V.Mcp()
    for l in SIG.events_lines(now): print(l)
    print("Latest crypto headlines:"); print(chr(10).join(SIG.news_lines(now)))
    for coin in (sys.argv[1:] or COINS):
        try: board(coin.lower(), mcp, now)
        except Exception as e: print(f"\n{coin.upper()}: could not read ({type(e).__name__}: {str(e)[:120]})")
    print("\nSettles on CF Benchmarks real-time index; Kraken shown here as a close stand-in. Read only.")


if __name__ == "__main__":
    main()
