"""AI Fund Desk - paper simulation engine (built 2026-11-15, Claude Code; design: projects/ai-fund/DESIGN.md).

One loop does both the forward paper book and the labelled backtest, so they can never disagree on rules.
Per calendar day D (UTC dates; crypto trades every day, ETFs on trading days):
    a. dividends / splits with ex-date D are applied to shares held
    b. orders created before D's open are filled at D's OPEN (+ slippage/fees from execution.PaperBroker)
    c. every book is marked at D's close
    d. risk overlays (sleeve and fund drawdown rules)
    e. signals are computed from closes <= D only, and become orders that can fill no earlier than the next open
Nothing here can place a real order: all fills go through execution.get_broker(), which only knows "paper".
"""
import math
import random
from datetime import datetime, timezone, timedelta

from data import CRYPTO, bar_complete, ETF_SESSION_SECONDS

ETF_REF, CRYPTO_REF = "SPY", "BTC-USD"
TREND_UNI = ["SPY", "QQQ", "EFA", "EEM", "IEF", "TLT", "GLD", "DBC"]
SLEEVES = {   # name -> (asset class, plain description)
    "trend":   ("etf", "Dual momentum: top 3 of 8 ETFs by 12-1 month return, only if they beat T-bills (else BIL). Monthly."),
    "volcore": ("etf", "SPY/AGG/GLD weighted by inverse 60-day volatility, scaled to a target volatility. Weekly."),
    "quality": ("etf", "Quality + low-volatility + dividend ETFs (QUAL, USMV, SCHD), equal weight. Quarterly."),
    "macro":   ("etf", "Regime switch: SPY when credit (HYG/IEF) is above its 50-day average and SPY is above its 200-day; else 50% IEF / 50% GLD. Weekly."),
    "dipbuy":  ("etf", "Buy SPY/QQQ dips (2-day RSI under 10) only in an uptrend (above 200-day); exit when RSI > 60 or after 5 days."),
    "crypto":  ("crypto", "BTC/ETH trend: hold a coin when it is above its 100-day average, sized to a volatility target; else cash."),
}
BENCHES = {
    "spy":  ("etf", "SPY buy-and-hold"),
    "6040": ("etf", "60/40: 60% SPY, 40% AGG, rebalanced monthly"),
    "bil":  ("etf", "Cash / T-bills (BIL)"),
    "btc":  ("crypto", "BTC buy-and-hold"),
}
SYMBOLS = sorted(set(TREND_UNI + ["AGG", "BIL", "HYG", "QUAL", "USMV", "SCHD", "BTC-USD", "ETH-USD"]))


# ----------------------------------------------------------------------------------------------------------- data view
class View:
    """Date-indexed access to cached series, restricted to bars that are complete at now_ts."""

    def __init__(self, series, now_ts):
        self.now_ts = now_ts
        self.bars, self.idx, self.divs, self.splits = {}, {}, {}, {}
        for sym, s in series.items():
            bars = [b for b in s["bars"] if bar_complete(b, sym, now_ts)]
            self.bars[sym] = bars
            self.idx[sym] = {b["date"]: i for i, b in enumerate(bars)}
            self.divs[sym] = s.get("divs", {})
            self.splits[sym] = s.get("splits", {})

    def bar(self, sym, d):
        i = self.idx.get(sym, {}).get(d)
        return None if i is None else self.bars[sym][i]

    def last_close(self, sym, d):
        """Raw close of the last complete bar on or before d (for marking)."""
        i = self.idx.get(sym, {}).get(d)
        if i is None:
            bars = self.bars.get(sym) or []
            lo, hi = 0, len(bars) - 1
            i = -1
            while lo <= hi:                       # binary search last bar date <= d
                mid = (lo + hi) // 2
                if bars[mid]["date"] <= d:
                    i, lo = mid, mid + 1
                else:
                    hi = mid - 1
            if i < 0:
                return None
        return self.bars[sym][i]["close"]

    def adj(self, sym, d, n):
        """Last n adjusted closes up to and including date d (d must be a bar date of sym)."""
        i = self.idx.get(sym, {}).get(d)
        if i is None or i + 1 < n:
            return None
        return [b["adj"] for b in self.bars[sym][i + 1 - n:i + 1]]

    def prev_date(self, sym, d):
        i = self.idx.get(sym, {}).get(d)
        return None if not i else self.bars[sym][i - 1]["date"]

    def etf_day_status(self, d):
        """'trading' if SPY has a complete bar on d; 'closed' if a later SPY bar exists (holiday/weekend) or d is a
        weekend; 'waiting' if it is a weekday with no bar yet (do not process d until the bar shows up)."""
        if d in self.idx[ETF_REF]:
            return "trading"
        if datetime.strptime(d, "%Y-%m-%d").weekday() >= 5:
            return "closed"
        bars = self.bars[ETF_REF]
        return "closed" if bars and bars[-1]["date"] > d else "waiting"


# -------------------------------------------------------------------------------------------------------- math helpers
def sma(xs):
    return sum(xs) / len(xs)


def rets(xs):
    return [xs[i] / xs[i - 1] - 1 for i in range(1, len(xs))]


def stdev(xs):
    if len(xs) < 2:
        return 0.0
    m = sma(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / (len(xs) - 1))


def rsi2(closes):
    """Wilder RSI with period 2 over the given closes (needs ~20 for the smoothing to settle)."""
    gains = losses = 0.0
    n = 2
    ch = rets_abs = [closes[i] - closes[i - 1] for i in range(1, len(closes))]
    g = [max(c, 0) for c in ch]
    l_ = [max(-c, 0) for c in ch]
    gains, losses = sma(g[:n]), sma(l_[:n])
    for i in range(n, len(ch)):
        gains = (gains * (n - 1) + g[i]) / n
        losses = (losses * (n - 1) + l_[i]) / n
    if losses == 0:
        return 100.0
    return 100 - 100 / (1 + gains / losses)


def first_of_period(view, sym, d, kind):
    p = view.prev_date(sym, d)
    if p is None:
        return True
    a, b = datetime.strptime(p, "%Y-%m-%d"), datetime.strptime(d, "%Y-%m-%d")
    if kind == "month":
        return a.month != b.month
    if kind == "quarter":
        return a.month != b.month and b.month in (1, 4, 7, 10)
    if kind == "week":
        return a.isocalendar()[1] != b.isocalendar()[1]
    return True


# ------------------------------------------------------------------------------------------------------------ signals
def signal(name, view, d, book, cfg):
    """Return new target weights (sym -> fraction of sleeve capital) or None for 'no change today'."""
    first = book.get("targets") is None
    if name == "trend":
        if not (first or first_of_period(view, "SPY", d, "month")):
            return None
        def mom(s):
            a = view.adj(s, d, 253)
            return None if a is None else a[-22] / a[0] - 1          # 12-1 month: t-252 -> t-21
        bil = mom("BIL")
        scored = sorted(((mom(s), s) for s in TREND_UNI if mom(s) is not None), reverse=True)
        t = {}
        for sc, s in scored[:3]:
            if bil is None or sc > bil:
                t[s] = t.get(s, 0) + 1 / 3
            else:
                t["BIL"] = t.get("BIL", 0) + 1 / 3
        if len(scored) < 3:
            t["BIL"] = t.get("BIL", 0) + (3 - len(scored)) / 3
        return t
    if name == "volcore":
        if not (first or first_of_period(view, "SPY", d, "week")):
            return None
        syms = ["SPY", "AGG", "GLD"]
        rs = {}
        for s in syms:
            a = view.adj(s, d, 61)
            if a is None:
                return {"BIL": 1.0}
            rs[s] = rets(a)
        vol = {s: stdev(rs[s]) * math.sqrt(252) for s in syms}
        inv = {s: 1 / vol[s] for s in syms if vol[s] > 0}
        tot = sum(inv.values())
        w = {s: inv[s] / tot for s in inv}
        n = len(rs["SPY"])
        means = {s: sma(rs[s]) for s in syms}
        var = 0.0
        for a_ in syms:
            for b_ in syms:
                cov = sum((rs[a_][i] - means[a_]) * (rs[b_][i] - means[b_]) for i in range(n)) / (n - 1)
                var += w.get(a_, 0) * w.get(b_, 0) * cov
        pvol = math.sqrt(max(var, 0)) * math.sqrt(252)
        k = min(1.0, cfg["voltarget"]["volcore"] / pvol) if pvol > 0 else 1.0
        t = {s: w[s] * k for s in w}
        t["BIL"] = 1 - sum(t.values())
        return t
    if name == "quality":
        if not (first or first_of_period(view, "SPY", d, "quarter")):
            return None
        return {"QUAL": 1 / 3, "USMV": 1 / 3, "SCHD": 1 / 3}
    if name == "macro":
        if not (first or first_of_period(view, "SPY", d, "week")):
            return None
        h, i_, s = view.adj("HYG", d, 50), view.adj("IEF", d, 50), view.adj("SPY", d, 200)
        if h is None or i_ is None or s is None:
            return None
        ratio = [a / b for a, b in zip(h, i_)]
        on = ratio[-1] > sma(ratio) and s[-1] > sma(s)
        t = {"SPY": 1.0} if on else {"IEF": 0.5, "GLD": 0.5}
        return None if (not first and t == book.get("targets")) else t
    if name == "dipbuy":
        cur = dict(book.get("targets") or {})
        held = book.setdefault("held_days", {})
        changed = first
        for s in ("SPY", "QQQ"):
            a = view.adj(s, d, 200)
            if a is None:
                continue
            r = rsi2(a[-25:])
            if s in cur:
                held[s] = held.get(s, 0) + 1
                if r > 60 or held[s] >= 5:
                    cur.pop(s)
                    held.pop(s, None)
                    changed = True
            elif r < 10 and a[-1] > sma(a):
                cur[s] = 0.5
                held[s] = 0
                changed = True
        return cur if changed else None
    if name == "crypto":
        cur = book.get("targets")
        t = {}
        for s in ("BTC-USD", "ETH-USD"):
            a = view.adj(s, d, 101)
            if a is None:
                continue
            if a[-1] > sma(a[-100:]):
                v = stdev(rets(a[-31:])) * math.sqrt(365)
                t[s] = 0.5 * (min(1.0, cfg["voltarget"]["crypto"] / v) if v > 0 else 1.0)
        if cur is None:
            return t
        if set(t) != set(cur):
            return t                                    # a coin switched on/off
        if datetime.strptime(d, "%Y-%m-%d").weekday() == 0:   # weekly resize only if the size moved > 25%
            if any(abs(t[s] - cur[s]) > 0.25 * max(cur[s], 1e-9) for s in t):
                return t
        return None
    # benchmarks
    if name == "spy":
        return {"SPY": 1.0} if first else None
    if name == "bil":
        return {"BIL": 1.0} if first else None
    if name == "btc":
        return {"BTC-USD": 1.0} if first else None
    if name == "6040":
        return {"SPY": 0.6, "AGG": 0.4} if (first or first_of_period(view, "SPY", d, "month")) else None
    raise KeyError(name)


# -------------------------------------------------------------------------------------------------------------- books
def new_book(name, asset, cash):
    return {"name": name, "asset": asset, "cash": cash, "pos": {}, "cost": {}, "pending": None, "targets": None,
            "eq": [], "peak": cash, "scale": 1.0, "status": "active", "paused_on": None,
            "trades": {"n": 0, "wins": 0, "fees": 0.0, "realized": 0.0, "divs": 0.0}, "last": None, "held_days": {}}


def new_portfolio(kind, cfg, start, overlays=True, sleeve_names=None, weights=None):
    cap = cfg["capital"]
    weights = weights or cfg["weights"]
    names = sleeve_names or list(SLEEVES)
    sl = {n: new_book(n, SLEEVES[n][0], cap * weights.get(n, 0)) for n in names}
    return {"kind": kind, "start": start, "overlays": overlays, "reserve": cap - sum(b["cash"] for b in sl.values()),
            "sleeves": sl, "eq": [], "peak": cap, "scale": 1.0, "halted": False, "last": None,
            "weights": dict(weights), "events": []}


def book_value(b, view, d):
    v = b["cash"]
    for s, q in b["pos"].items():
        px = view.last_close(s, d)
        if px is not None:
            v += q * px
    return v


def fill_order(b, pf, view, d, broker, eff_scale):
    """Fill b['pending'] at the open of date d. Sells first, then capital transfer, then buys."""
    o = b["pending"]
    syms = set(o["targets"]) | set(b["pos"])
    opens = {}
    for s in syms:
        bar = view.bar(s, d)
        if bar is None:
            return False                                  # a needed symbol has no bar today - wait (never forward-fill)
        opens[s] = bar["open"]
    eq = b["cash"] + sum(q * opens[s] for s, q in b["pos"].items())
    cap = o.get("capital")
    inv = eq if cap is None else cap
    if b["status"] != "active":
        inv = 0.0 if b["status"] == "retired" else (eq if cap is None else cap)
    want = {s: (o["targets"].get(s, 0) * inv * eff_scale) / opens[s] for s in syms}
    if b["status"] == "paused":
        want = {s: 0.0 for s in syms}
    min_trade = max(25.0, 0.005 * max(inv, 1))
    # sells
    for s in sorted(syms):
        have = b["pos"].get(s, 0.0)
        dq = want[s] - have
        if dq < 0 and (abs(dq) * opens[s] >= min_trade or want[s] == 0):
            f = broker.fill(s, "sell", -dq, opens[s], b["asset"])
            b["cash"] += f.qty * f.price - f.fee
            b["trades"]["costs"] = b["trades"].get("costs", 0.0) + f.fee + f.qty * (f.ref_price - f.price)
            pnl = (f.price - b["cost"].get(s, f.price)) * f.qty - f.fee
            t = b["trades"]
            t["n"] += 1
            t["wins"] += 1 if pnl > 0 else 0
            t["fees"] += f.fee
            t["realized"] += pnl
            b["pos"][s] = have - f.qty
            if b["pos"][s] <= 1e-9:
                b["pos"].pop(s)
                b["cost"].pop(s, None)
    # capital transfer with the fund reserve
    if pf is not None and cap is not None:
        cur = b["cash"] + sum(q * opens[s] for s, q in b["pos"].items())
        delta = cap - cur
        if delta > 0:
            take = min(delta, pf["reserve"])
            pf["reserve"] -= take
            b["cash"] += take
            b["flow"] = b.get("flow", 0.0) + take
        elif delta < 0:
            give = min(-delta, b["cash"])
            b["cash"] -= give
            pf["reserve"] += give
            b["flow"] = b.get("flow", 0.0) - give
    # buys (limited by cash)
    for s in sorted(syms):
        have = b["pos"].get(s, 0.0)
        dq = want[s] - have
        if dq > 0 and dq * opens[s] >= min_trade:
            c = broker.costs[b["asset"]]
            unit = opens[s] * (1 + c["slip_bps"] * broker.stress / 1e4) * (1 + c["fee_bps"] * broker.stress / 1e4)
            dq = min(dq, max(b["cash"], 0) / unit)
            if dq * opens[s] < min_trade:
                continue
            f = broker.fill(s, "buy", dq, opens[s], b["asset"])
            b.setdefault("splits_known", {})[s] = sorted(view.splits.get(s, {}))
            b["trades"]["costs"] = b["trades"].get("costs", 0.0) + f.fee + f.qty * (f.price - f.ref_price)
            b["cash"] -= f.qty * f.price + f.fee
            b["trades"]["fees"] += f.fee
            old = b["pos"].get(s, 0.0)
            b["cost"][s] = (b["cost"].get(s, 0) * old + f.price * f.qty) / (old + f.qty)
            b["pos"][s] = old + f.qty
    b["pending"] = None
    return True


def queue(b, targets, created, capital=None):
    prev = b.get("pending") or {}
    b["pending"] = {"targets": dict(targets), "created": created,
                    "capital": capital if capital is not None else prev.get("capital")}


def completion_ts(view, asset, d):
    ref = ETF_REF if asset == "etf" else CRYPTO_REF
    bar = view.bar(ref, d)
    if bar is None:
        return int(datetime.strptime(d, "%Y-%m-%d").replace(tzinfo=timezone.utc).timestamp()) + 86400
    return bar["t"] + (86400 if asset == "crypto" else int(ETF_SESSION_SECONDS))


def step_book(name, b, pf, view, d, broker, cfg, eff_scale, not_before=0):
    """One day for one book. Returns True if the book's asset class traded on d."""
    asset = b["asset"]
    if asset == "etf" and view.etf_day_status(d) != "trading":
        return False
    if asset == "crypto" and view.bar(CRYPTO_REF, d) is None:
        return False
    # a. corporate actions on shares held into d
    for s in list(b["pos"]):
        sp = view.splits.get(s, {}).get(d)
        # Yahoo history is split-adjusted, so shares bought on adjusted prices are already in post-split units. Only a
        # split that was NOT in the data when the shares were bought (forward book, live split) changes the share count.
        if sp and d not in b.setdefault("splits_known", {}).get(s, []):
            b["pos"][s] *= sp
            b["cost"][s] = b["cost"].get(s, 0) / sp
        dv = view.divs.get(s, {}).get(d)
        if dv:
            b["cash"] += b["pos"][s] * dv
            b["trades"]["divs"] += b["pos"][s] * dv
    # b. fills at the open (only orders created before this open)
    ref = view.bar(ETF_REF if asset == "etf" else CRYPTO_REF, d)
    if b["pending"] and ref and ref["t"] >= b["pending"]["created"] and ref["t"] >= not_before:
        fill_order(b, pf, view, d, broker, eff_scale)
    # e. signals at the close (computed before overlays so dipbuy's day count moves once per day)
    if b["status"] != "retired":
        t = signal(name, view, d, b, cfg)
        if t is not None:
            b["targets"] = t
            if b["status"] == "active":
                queue(b, t, completion_ts(view, asset, d))
    b["last"] = d
    return True


def mark(b, view, d):
    """Append [date, value, index]. The index strips capital moved in/out by the fund (flows), so a sleeve's
    returns, drawdown and verdict measure its trading, not the money the fund handed it."""
    v = book_value(b, view, d)
    if b["eq"]:
        prev_v, prev_i = b["eq"][-1][1], b["eq"][-1][2]
        idx = prev_i * ((v - b.get("flow", 0.0)) / prev_v) if prev_v > 0 else prev_i
    else:
        idx = 1.0
    b["flow"] = 0.0
    b["eq"].append([d, round(v, 2), round(idx, 8)])
    b["ipeak"] = max(b.get("ipeak", 1.0), idx)
    b["peak"] = max(b["peak"], v)
    return v


def overlays(name, b, view, d, cfg, shadow, log):
    """Sleeve drawdown rules (DeepSeek + Fable): -10% halves, -15% pauses (flat), -25% retires. Resume needs 20 days
    paused AND the untouched shadow copy of the sleeve making a new 60-day high."""
    r = cfg["risk"]
    v = b["eq"][-1][1]
    idx = b["eq"][-1][2]
    dd = idx / b.get("ipeak", 1.0) - 1
    ts = completion_ts(view, b["asset"], d)
    if b["status"] == "active":
        if dd <= r["sleeve_retire_dd"]:
            b["status"] = "retired"
            queue(b, {}, ts)
            log(d, name, f"retired: drawdown {dd:.1%} hit the {r['sleeve_retire_dd']:.0%} line")
        elif dd <= r["sleeve_pause_dd"]:
            b["status"], b["paused_on"] = "paused", d
            queue(b, {}, ts)
            log(d, name, f"paused (went to cash): drawdown {dd:.1%} hit the {r['sleeve_pause_dd']:.0%} line")
        elif dd <= r["sleeve_halve_dd"] and b["scale"] == 1.0:
            b["scale"] = 0.5
            if b["targets"]:
                queue(b, b["targets"], ts)
            log(d, name, f"size halved: drawdown {dd:.1%} hit the {r['sleeve_halve_dd']:.0%} line")
        elif dd > r["sleeve_halve_dd"] / 2 and b["scale"] < 1.0:
            b["scale"] = 1.0
            if b["targets"]:
                queue(b, b["targets"], ts)
            log(d, name, f"size restored: drawdown back to {dd:.1%}")
    elif b["status"] == "paused" and shadow is not None:
        days = sum(1 for e in b["eq"] if e[0] > b["paused_on"])
        se = [e[1] for e in shadow["eq"][-60:]]
        if days >= r["resume_min_days"] and se and se[-1] >= max(se):
            b["status"], b["scale"], b["peak"], b["ipeak"] = "active", 1.0, v, idx
            b["targets"] = dict(shadow.get("targets") or {})
            queue(b, b["targets"], ts)
            log(d, name, f"resumed after {days} days: its shadow copy made a new 60-day high")


def run_portfolio(pf, view, dates, cfg, broker, shadows=None, not_before=0):
    """Advance a whole portfolio (fund / twin) over dates. shadows: name -> raw book (for resume rule)."""
    def log(d, who, msg):
        pf["events"].append([d, who, msg])
    for d in dates:
        if pf["last"] and d <= pf["last"]:
            continue
        if view.etf_day_status(d) == "waiting" or view.bar(CRYPTO_REF, d) is None:
            break                                          # wait for complete data before booking this day
        wcfg = cfg
        # capital reallocation: monthly, or when the weights in config changed
        month_turn = view.etf_day_status(d) == "trading" and first_of_period(view, "SPY", d, "month") and pf["eq"]
        if pf["eq"] and (month_turn or wcfg["weights"] != pf["weights"]):
            if wcfg["weights"] != pf["weights"]:
                log(d, "fund", "weights changed -> sleeves re-sized at the next open: " +
                    ", ".join(f"{k} {pf['weights'].get(k, 0):.0%}->{v:.0%}" for k, v in wcfg["weights"].items()
                              if abs(v - pf["weights"].get(k, 0)) > 1e-9))
            pf["weights"] = dict(wcfg["weights"])
            fe = pf["eq"][-1][1]
            for n, b in pf["sleeves"].items():
                if b["status"] == "paused":
                    continue
                capn = 0.0 if b["status"] == "retired" else pf["weights"].get(n, 0) * fe
                queue(b, b["targets"] or {}, completion_ts(view, b["asset"], pf["last"] or d) - 1, capital=capn)
        for n, b in pf["sleeves"].items():
            eff = b["scale"] * pf["scale"] if pf["overlays"] else 1.0
            step_book(n, b, pf, view, d, broker, cfg, eff, not_before)
            mark(b, view, d)
            if pf["overlays"]:
                overlays(n, b, view, d, cfg, (shadows or {}).get(n), log)
        fv = pf["reserve"] + sum(b["eq"][-1][1] for b in pf["sleeves"].values())
        pf["eq"].append([d, round(fv, 2), round(fv / pf["eq"][0][1], 8) if pf["eq"] else 1.0])
        pf["peak"] = max(pf["peak"], fv)
        if pf["overlays"]:
            fund_overlay(pf, view, d, cfg, log)
        pf["last"] = d
    return pf


def fund_overlay(pf, view, d, cfg, log):
    r = cfg["risk"]
    dd = pf["eq"][-1][1] / pf["peak"] - 1
    old = pf["scale"]
    if pf["halted"]:
        if cfg.get("fund_halt_reset"):
            pf["halted"], pf["scale"], pf["peak"] = False, 1.0, pf["eq"][-1][1]
            log(d, "fund", "halt cleared by the weekly review (fund_halt_reset)")
    elif dd <= r["fund_halt_dd"]:
        pf["halted"], pf["scale"] = True, 0.0
        log(d, "fund", f"HALTED to cash: fund drawdown {dd:.1%} hit {r['fund_halt_dd']:.0%}; waits for the weekly review")
    elif dd <= r["fund_halve_dd"] and pf["scale"] == 1.0:
        pf["scale"] = 0.5
        log(d, "fund", f"all sleeves halved: fund drawdown {dd:.1%} hit {r['fund_halve_dd']:.0%}")
    elif dd > r["fund_halve_clear_dd"] and pf["scale"] == 0.5:
        pf["scale"] = 1.0
        log(d, "fund", f"full size again: fund drawdown back to {dd:.1%}")
    if pf["scale"] != old:
        for b in pf["sleeves"].values():
            if b["targets"] and b["status"] == "active":
                queue(b, b["targets"], completion_ts(view, b["asset"], d))


def run_book(name, b, view, dates, cfg, broker, not_before=0):
    """Single-book runner (benchmarks and raw shadow sleeves): no overlays, no reserve."""
    for d in dates:
        if b["last"] and d <= b["last"]:
            continue
        if view.etf_day_status(d) == "waiting" or view.bar(CRYPTO_REF, d) is None:
            break
        step_book(name, b, None, view, d, broker, cfg, 1.0, not_before)
        mark(b, view, d)
        b["last"] = d
    return b


def calendar(view, start, end=None):
    d = datetime.strptime(start, "%Y-%m-%d")
    last = view.bars[CRYPTO_REF][-1]["date"] if view.bars[CRYPTO_REF] else start
    end = end or last
    out = []
    while d.strftime("%Y-%m-%d") <= end:
        out.append(d.strftime("%Y-%m-%d"))
        d += timedelta(days=1)
    return out


# ------------------------------------------------------------------------------------------------------------ metrics
def metrics(eq, bil_ann=None):
    """eq: [[date, value], ...] on the daily calendar."""
    if len(eq) < 2:
        v = eq[-1][1] if eq else None
        return {"value": v, "total": 0.0, "days": len(eq), "ann": None, "vol": None, "maxdd": 0.0, "dd": 0.0, "sharpe": None}
    vals = [e[2] if len(e) > 2 else e[1] for e in eq]
    r = [vals[i] / vals[i - 1] - 1 for i in range(1, len(vals)) if vals[i - 1] > 0]
    days = (datetime.strptime(eq[-1][0], "%Y-%m-%d") - datetime.strptime(eq[0][0], "%Y-%m-%d")).days
    total = vals[-1] / vals[0] - 1
    ann = (1 + total) ** (365 / days) - 1 if days >= 30 and total > -1 else None
    vol = stdev(r) * math.sqrt(365) if len(r) > 5 else None
    peak, mdd = vals[0], 0.0
    for v in vals:
        peak = max(peak, v)
        mdd = min(mdd, v / peak - 1)
    sharpe = (ann - (bil_ann or 0)) / vol if (ann is not None and vol) else None
    return {"value": round(eq[-1][1], 2), "total": round(total, 5), "days": days, "ann": None if ann is None else round(ann, 5),
            "vol": None if vol is None else round(vol, 4), "maxdd": round(mdd, 5), "dd": round(vals[-1] / max(vals) - 1, 5),
            "sharpe": None if sharpe is None else round(sharpe, 3)}


def p_beat(eq_a, eq_b, block=7, reps=1000, seed=7):
    """Block-bootstrap probability that the mean daily excess return of a over b is > 0 (Fable's verdict test)."""
    db = {e[0]: (e[2] if len(e) > 2 else e[1]) for e in eq_b}
    pairs = [((e[2] if len(e) > 2 else e[1]), db[e[0]]) for e in eq_a if e[0] in db]
    if len(pairs) < 21:
        return None
    ex = [(pairs[i][0] / pairs[i - 1][0]) - (pairs[i][1] / pairs[i - 1][1]) for i in range(1, len(pairs))]
    n = len(ex)
    rnd = random.Random(seed)
    wins = 0
    for _ in range(reps):
        tot, k = 0.0, 0
        while k < n:
            st = rnd.randrange(0, n)
            for j in range(block):
                if k >= n:
                    break
                tot += ex[(st + j) % n]
                k += 1
        wins += tot > 0
    return round(wins / reps, 3)
