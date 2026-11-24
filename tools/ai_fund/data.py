"""AI Fund Desk - free market data (paper only). Built 2026-11-15 by Claude Code for the AI Fund Desk.

Sources (all free, public, no key): Yahoo chart API (daily bars + dividends/splits, live price), Coinbase public
spot (crypto cross-check + live mark), Kalshi public markets (Fed-rate odds, READ ONLY, used as a signal for the shadow
sleeve; nothing is ever traded on a prediction market - company policy P-0112).

Look-ahead rules live here (Codex, team-ideas-2026-11-15.md):
  * a daily ETF bar is "complete" only 15 min after its 16:00 ET close; a crypto UTC-day bar only after 00:00 UTC next day
  * the still-forming bar Yahoo returns for today is never used for a signal
Cache: state/ai-fund/cache/<symbol>.json (full 5y history refreshed once a day, 5-day tail refreshed every run).
"""
import json
import os
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone, timedelta

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
CACHE = os.path.join(ROOT, "state", "ai-fund", "cache")
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) hb-ai-fund/1.0"}
CRYPTO = {"BTC-USD", "ETH-USD"}
ETF_SESSION_SECONDS = 6.5 * 3600 + 15 * 60     # 9:30 open -> 16:00 close + 15 min settle buffer


def _get(url, timeout=30):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def _yahoo(symbol, rng):
    q = urllib.parse.quote(symbol)
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{q}?range={rng}&interval=1d&events=div%7Csplit"
    last = None
    for attempt in range(3):
        try:
            return _get(url)["chart"]["result"][0]
        except Exception as e:   # noqa: BLE001 - network: retry, then give up and let the caller flag stale data
            last = e
            time.sleep(2 + attempt * 3)
    raise RuntimeError(f"yahoo {symbol}: {last}")


def _parse(res, symbol):
    ts = res.get("timestamp") or []
    q = res["indicators"]["quote"][0]
    adj = (res["indicators"].get("adjclose") or [{}])[0].get("adjclose") or q["close"]
    bars = []
    for i, t in enumerate(ts):
        o, c, a = q["open"][i], q["close"][i], adj[i]
        if o is None or c is None or a is None or o <= 0 or c <= 0:
            continue                                  # never forward-fill a missing bar into a trade
        bars.append({"t": int(t), "date": _bar_date(int(t), symbol), "open": float(o), "close": float(c),
                     "adj": float(a), "high": float(q["high"][i] or c), "low": float(q["low"][i] or c)})
    ev = res.get("events") or {}
    divs = {_bar_date(int(v["date"]), symbol): float(v["amount"]) for v in (ev.get("dividends") or {}).values()}
    splits = {_bar_date(int(v["date"]), symbol): float(v["numerator"]) / float(v["denominator"])
              for v in (ev.get("splits") or {}).values() if v.get("denominator")}
    meta = res.get("meta") or {}
    return {"symbol": symbol, "bars": bars, "divs": divs, "splits": splits,
            "live": meta.get("regularMarketPrice"), "live_t": meta.get("regularMarketTime")}


def _bar_date(t, symbol):
    if symbol in CRYPTO:
        return datetime.fromtimestamp(t, timezone.utc).strftime("%Y-%m-%d")
    # ETF bars are stamped at the 9:30 ET open; ET date = UTC date for any time between 13:30 and 21:00 UTC
    return datetime.fromtimestamp(t, timezone.utc).strftime("%Y-%m-%d")


def bar_complete(bar, symbol, now_ts):
    if symbol in CRYPTO:
        return now_ts >= bar["t"] + 86400
    return now_ts >= bar["t"] + ETF_SESSION_SECONDS


def bar_open_ts(bar):
    return bar["t"]


def load(symbol, now_ts=None, refresh=True):
    """Return the cached series for symbol, refreshed. Bars include the still-forming one; callers filter by bar_complete."""
    os.makedirs(CACHE, exist_ok=True)
    path = os.path.join(CACHE, symbol.replace("^", "_") + ".json")
    cached = None
    if os.path.exists(path):
        try:
            cached = json.load(open(path, encoding="utf-8"))
        except ValueError:
            cached = None
    if not refresh and cached:
        return cached
    full_due = (not cached) or (time.time() - cached.get("full_at", 0) > 20 * 3600)
    try:
        res = _parse(_yahoo(symbol, "5y" if full_due else "1mo"), symbol)
    except Exception as e:   # noqa: BLE001
        if cached:
            cached["error"] = str(e)[:200]
            return cached
        raise
    if full_due or not cached:
        out = res
        out["full_at"] = time.time()
    else:
        by_date = {b["date"]: b for b in cached["bars"]}
        for b in res["bars"]:
            by_date[b["date"]] = b               # tail overwrites (fixes revised / still-forming bars)
        out = dict(cached)
        out["bars"] = sorted(by_date.values(), key=lambda b: b["t"])
        out["divs"] = {**cached.get("divs", {}), **res["divs"]}
        out["splits"] = {**cached.get("splits", {}), **res["splits"]}
        out["live"], out["live_t"] = res["live"], res["live_t"]
        # adjusted closes are back-adjusted on each new dividend: when the tail's adj ratio drifts, take a full refresh next run
    out["fetched_at"] = time.time()
    out.pop("error", None)
    json.dump(out, open(path, "w", encoding="utf-8"))
    return out


def coinbase_spot(symbol):
    try:
        d = _get(f"https://api.coinbase.com/v2/prices/{symbol}/spot", timeout=15)
        return float(d["data"]["amount"])
    except Exception:   # noqa: BLE001
        return None


def kalshi_fed():
    """Public Kalshi KXFED prices -> implied upper-bound rate after the next FOMC meeting. Read only."""
    base = "https://api.elections.kalshi.com/trade-api/v2"
    ev = _get(f"{base}/events?series_ticker=KXFED&status=open&limit=20", timeout=20).get("events") or []
    if not ev:
        return None
    ev_tickers = [e["event_ticker"] for e in ev]
    best = None
    for et in ev_tickers:
        ms = _get(f"{base}/markets?event_ticker={urllib.parse.quote(et)}&limit=100", timeout=20).get("markets") or []
        if not ms:
            continue
        close = min(m.get("close_time", "9999") for m in ms)
        if close < datetime.now(timezone.utc).isoformat():
            continue
        if best is None or close < best[0]:
            best = (close, et, ms)
    if not best:
        return None
    close, et, ms = best
    pts = []
    for m in ms:
        k = m.get("floor_strike")
        if k is None:
            continue
        bid, ask = m.get("yes_bid_dollars"), m.get("yes_ask_dollars")
        try:
            p = (float(bid) + float(ask)) / 2 if bid not in (None, "") and ask not in (None, "") else float(m.get("last_price_dollars") or 0)
        except (TypeError, ValueError):
            continue
        pts.append((float(k), max(0.0, min(1.0, p))))
    if len(pts) < 3:
        return None
    pts.sort()
    # P(rate > k) for ascending strikes -> expected rate = k_min + sum P(>k_i) * (k_{i+1} - k_i)
    exp = pts[0][0]
    for (k0, p0), (k1, _p1) in zip(pts, pts[1:]):
        exp += p0 * (k1 - k0)
    return {"event": et, "meeting_close": close, "implied_rate": round(exp, 4), "strikes": len(pts),
            "at": datetime.now(timezone.utc).isoformat(timespec="seconds")}


def yahoo_hourly_last(symbol):
    """Latest 1h bar close (for the shadow Fed-odds sleeve). Returns (ts, close) of the last COMPLETE hour or None."""
    q = urllib.parse.quote(symbol)
    try:
        res = _get(f"https://query1.finance.yahoo.com/v8/finance/chart/{q}?range=2d&interval=1h")["chart"]["result"][0]
    except Exception:   # noqa: BLE001
        return None
    ts, cl = res.get("timestamp") or [], res["indicators"]["quote"][0]["close"]
    now = time.time()
    out = [(t, c) for t, c in zip(ts, cl) if c is not None and t + 3600 <= now]
    return out[-1] if out else None
