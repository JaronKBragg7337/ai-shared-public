"""AI Fund Desk - hourly run (Windows task "HB AI Fund"). PAPER ONLY. Built 2026-11-15 by Claude Code.

    python tools/ai_fund/run.py               # full hourly run: data -> checks -> forward books -> backtest -> summary -> tuner -> Supabase
    python tools/ai_fund/run.py --no-tuner    # skip the hourly AI judgement
    python tools/ai_fund/run.py --no-push     # do not write to Supabase

Writes: state/ai-fund/forward.json (books), backtest.json, summary.json (dashboard payload), SUMMARY.md, runs.log,
fedodds.jsonl. Pushes the compact summary to Supabase public.ai_fund_snapshots (RLS: admins only).
No GPU, no real orders, no money moves. Design: projects/ai-fund/DESIGN.md.
"""
import argparse
import copy
import json
import os
import re
import sys
import time
import traceback
import urllib.request
from datetime import datetime, timezone, timedelta

HERE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, HERE)
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

import data as D        # noqa: E402
import engine as E      # noqa: E402
from execution import get_broker   # noqa: E402

ROOT = D.ROOT
OUT = os.path.join(ROOT, "state", "ai-fund")
CFG = os.path.join(ROOT, "projects", "ai-fund", "config.json")
FORWARD = os.path.join(OUT, "forward.json")
BACKTEST = os.path.join(OUT, "backtest.json")
SUMMARY = os.path.join(OUT, "summary.json")
SUMMARY_MD = os.path.join(OUT, "SUMMARY.md")
RUNLOG = os.path.join(OUT, "runs.log")
FEDLOG = os.path.join(OUT, "fedodds.jsonl")
FORWARD_START = "2026-11-13"     # signals from the last US close before the build; nothing fills before the build time
BACKTEST_START = "2025-01-02"
SECRETS = os.path.join(os.path.expanduser("~"), ".secrets", "keys.env")
SLEEVE_BENCH = {"trend": "6040", "volcore": "6040", "quality": "spy", "macro": "6040", "dipbuy": "bil", "crypto": "btc"}


def log(msg):
    os.makedirs(OUT, exist_ok=True)
    line = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | {msg}"
    print(line, flush=True)
    with open(RUNLOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def env():
    out = {}
    try:
        for line in open(SECRETS, encoding="utf-8"):
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                out[k.strip()] = v.strip().strip('"').strip("'")
    except OSError:
        pass
    return out


# ------------------------------------------------------------------------------------------------------------- config
def get_path(cfg, key):
    a, b = key.split(".", 1)
    return cfg[a][b]


def set_path(cfg, key, val):
    a, b = key.split(".", 1)
    cfg[a][b] = val


def load_config():
    """Load and re-clamp: nothing can escape the bounds, whoever edited the file."""
    cfg = json.load(open(CFG, encoding="utf-8"))
    if cfg.get("mode") != "paper":
        raise SystemExit("config.mode is not 'paper' - refusing to run")
    for k in cfg["tunable"]:
        lo, hi = cfg["bounds"][k]
        v = get_path(cfg, k)
        if v < lo or v > hi:
            set_path(cfg, k, min(hi, max(lo, v)))
    tot = sum(cfg["weights"].values())
    cap = 1 - cfg["min_reserve"]
    if tot > cap + 1e-9:
        for k in cfg["weights"]:
            cfg["weights"][k] = round(cfg["weights"][k] * cap / tot, 4)
    return cfg


# --------------------------------------------------------------------------------------------------------- data checks
def data_checks(series, now_ts):
    """Codex's three hourly checks: (1) freshness / expected bars, (2) duplicates + OHLC validity + jumps,
    (3) cross-source price check (Yahoo vs Coinbase for crypto)."""
    flags, fresh = [], {}
    today = datetime.fromtimestamp(now_ts, timezone.utc).date()
    for sym, s in series.items():
        bars = [b for b in s["bars"] if D.bar_complete(b, sym, now_ts)]
        if not bars:
            flags.append(f"{sym}: no complete bars")
            continue
        last = datetime.strptime(bars[-1]["date"], "%Y-%m-%d").date()
        fresh[sym] = bars[-1]["date"]
        limit = 2 if sym in D.CRYPTO else 5
        if (today - last).days > limit:
            flags.append(f"{sym}: stale, last complete bar {bars[-1]['date']}")
        dates = [b["date"] for b in bars[-300:]]
        if len(dates) != len(set(dates)):
            flags.append(f"{sym}: duplicate bar dates")
        for b in bars[-30:]:
            if not (b["low"] * 0.999 <= min(b["open"], b["close"]) and max(b["open"], b["close"]) <= b["high"] * 1.001):
                flags.append(f"{sym}: bad OHLC on {b['date']}")
                break
        for a, b in zip(bars[-30:], bars[-29:]):
            jump = abs(b["close"] / a["close"] - 1)
            if jump > (0.25 if sym in D.CRYPTO else 0.12):
                flags.append(f"{sym}: {jump:.0%} one-day move on {b['date']} (check for a bad print)")
        if s.get("error"):
            flags.append(f"{sym}: fetch error, using cache ({s['error'][:80]})")
    live = {}
    for sym in D.CRYPTO:
        cb = D.coinbase_spot(sym)
        yl = series.get(sym, {}).get("live")
        live[sym] = cb or yl
        if cb and yl and abs(cb / yl - 1) > 0.015:
            flags.append(f"{sym}: Yahoo {yl:,.0f} vs Coinbase {cb:,.0f} differ by {abs(cb / yl - 1):.1%}")
        if not cb:
            flags.append(f"{sym}: Coinbase spot unavailable")
    return flags, fresh, live


# ------------------------------------------------------------------------------------------------------------- forward
def init_forward(cfg, now_ts):
    frozen = copy.deepcopy(cfg)
    st = {"version": 1, "created": datetime.fromtimestamp(now_ts, timezone.utc).isoformat(timespec="seconds"),
          "not_before": int(now_ts), "start": FORWARD_START, "config_frozen": frozen,
          "fund": E.new_portfolio("fund", cfg, FORWARD_START),
          "twin": E.new_portfolio("twin", frozen, FORWARD_START),
          "raw": {n: E.new_book(n, E.SLEEVES[n][0], cfg["capital"] * cfg["weights"][n]) for n in E.SLEEVES},
          "bench": {n: E.new_book(n, a, cfg["capital"]) for n, (a, _) in E.BENCHES.items()},
          "fed": {"open": None, "closed": [], "pnl": 0.0}}
    return st


def advance_forward(st, view, cfg, broker):
    dates = E.calendar(view, st["start"])
    nb = st["not_before"]
    for n, b in st["raw"].items():
        E.run_book(n, b, view, dates, cfg, broker, nb)
    for n, b in st["bench"].items():
        E.run_book(n, b, view, dates, cfg, broker, nb)
    E.run_portfolio(st["fund"], view, dates, cfg, broker, shadows=st["raw"], not_before=nb)
    E.run_portfolio(st["twin"], view, dates, st["config_frozen"], broker, shadows=st["raw"], not_before=nb)
    return st


# ------------------------------------------------------------------------------------------------------------ backtest
def run_backtest(view, cfg_base, last_etf):
    if os.path.exists(BACKTEST):
        try:
            old = json.load(open(BACKTEST, encoding="utf-8"))
            if old.get("through_etf") == last_etf and old.get("cfg_hash") == _hash(cfg_base):
                return old
        except ValueError:
            pass
    t0 = time.time()
    dates = E.calendar(view, BACKTEST_START)
    out = {"through_etf": last_etf, "cfg_hash": _hash(cfg_base), "start": BACKTEST_START,
           "label": "BACKTEST - same engine and costs, but the rules were picked by AIs who already know this history. "
                    "Not evidence; only the forward paper book counts."}
    res = {}
    for stress in (1.0, 3.0):
        br = get_broker(cfg_base, stress)
        pf = E.new_portfolio("bt", cfg_base, BACKTEST_START)
        raw = {n: E.new_book(n, E.SLEEVES[n][0], cfg_base["capital"] * cfg_base["weights"][n]) for n in E.SLEEVES}
        for n, b in raw.items():
            E.run_book(n, b, view, dates, cfg_base, br)
        E.run_portfolio(pf, view, dates, cfg_base, br, shadows=raw)
        res[stress] = (pf, raw)
    br = get_broker(cfg_base, 1.0)
    bench = {n: E.run_book(n, E.new_book(n, a, cfg_base["capital"]), view, dates, cfg_base, br) for n, (a, _) in E.BENCHES.items()}
    pf, raw = res[1.0]
    bil_ann = E.metrics(bench["bil"]["eq"])["ann"]
    out["fund"] = E.metrics(pf["eq"], bil_ann)
    out["fund_stress3x"] = E.metrics(res[3.0][0]["eq"], bil_ann)
    out["bench"] = {n: E.metrics(b["eq"], bil_ann) for n, b in bench.items()}
    out["sleeves"] = {}
    for n, b in pf["sleeves"].items():
        m = E.metrics(b["eq"], bil_ann)
        t = b["trades"]
        m.update({"trades": t["n"], "win_rate": round(t["wins"] / t["n"], 3) if t["n"] else None, "fees": round(t["fees"], 2),
                  "status": b["status"], "p_beat": E.p_beat(b["eq"], bench[SLEEVE_BENCH[n]]["eq"]),
                  "raw": E.metrics(raw[n]["eq"], bil_ann)})
        out["sleeves"][n] = m
    out["p_beat_fund_vs_6040"] = E.p_beat(pf["eq"], bench["6040"]["eq"])
    out["events"] = pf["events"][-40:]

    def weekly(eq):
        return [e for i, e in enumerate(eq) if i % 7 == 0 or i == len(eq) - 1]
    out["series"] = {"fund": weekly(pf["eq"]), "stress3x": weekly(res[3.0][0]["eq"]),
                     **{n: weekly(b["eq"]) for n, b in bench.items()}}
    out["seconds"] = round(time.time() - t0, 1)
    json.dump(out, open(BACKTEST, "w", encoding="utf-8"))
    return out


def _hash(cfg):
    import hashlib
    keep = {k: cfg[k] for k in ("weights", "voltarget", "costs", "risk", "capital")}
    return hashlib.sha1(json.dumps(keep, sort_keys=True).encode()).hexdigest()[:12]


# ---------------------------------------------------------------------------------------------- shadow: Fed odds vs IEF
def fed_shadow(st, live_ief):
    """Kimi's idea, zero capital: when the Kalshi-implied post-meeting rate moves >= 0.10 pt in an hour while IEF moved
    <= 0.1%, take a $10,000 SHADOW position in IEF (long if cuts got priced, short if hikes), exit after 4 hours."""
    f = st["fed"]
    now = time.time()
    try:
        k = D.kalshi_fed()
    except Exception as e:   # noqa: BLE001
        k = None
        f["error"] = str(e)[:120]
    hr = None
    try:
        res = D._get("https://query1.finance.yahoo.com/v8/finance/chart/IEF?range=2d&interval=1h")["chart"]["result"][0]
        pts = [(t, c) for t, c in zip(res.get("timestamp") or [], res["indicators"]["quote"][0]["close"]) if c is not None]
        hr = pts[-2:] if len(pts) >= 2 else None
        mkt_t = res["meta"].get("regularMarketTime") or 0
    except Exception:   # noqa: BLE001
        mkt_t = 0
    market_open = now - mkt_t < 20 * 60
    if k:
        with open(FEDLOG, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(k) + "\n")
        f["last"] = k
    px = live_ief if market_open else None
    if f.get("open") and px and now - f["open"]["t"] >= 4 * 3600:
        o = f["open"]
        r = (px / o["px"] - 1) * (1 if o["side"] == "long" else -1) - 0.001
        pnl = round(10000 * r, 2)
        f["closed"].append({**o, "exit": px, "exit_at": datetime.now(timezone.utc).isoformat(timespec="minutes"), "pnl": pnl})
        f["pnl"] = round(f["pnl"] + pnl, 2)
        f["open"] = None
    prev = f.get("prev")
    if k and prev and px and not f.get("open") and now - prev["ts"] <= 90 * 60 and hr:
        dr = k["implied_rate"] - prev["rate"]
        ief_1h = hr[-1][1] / hr[-2][1] - 1
        if abs(dr) >= 0.10 and abs(ief_1h) <= 0.001 and k["event"] == prev.get("event"):
            f["open"] = {"t": now, "at": datetime.now(timezone.utc).isoformat(timespec="minutes"), "px": px,
                         "side": "long" if dr < 0 else "short", "why": f"implied rate {prev['rate']:.2f}->{k['implied_rate']:.2f}, IEF 1h {ief_1h:+.2%}"}
    if k:
        f["prev"] = {"ts": now, "rate": k["implied_rate"], "event": k["event"]}
    f["closed"] = f["closed"][-50:]


# ---------------------------------------------------------------------------------------------- comparison rows
def comparison_rows():
    rows = []
    try:
        t = open(os.path.join(ROOT, "state", "news-paper-book.md"), encoding="utf-8").read()
        upd = re.search(r"updated ([0-9-]+ [0-9:]+)", t)
        s = re.search(r"Settled paper P&L: \$([+-][0-9,]+\.[0-9]+); matched SPY: \$([+-][0-9,]+\.[0-9]+)", t)
        o = re.search(r"Open paper P&L: \$([+-][0-9,]+\.[0-9]+); matched SPY: \$([+-][0-9,]+\.[0-9]+)", t)
        runs = re.search(r"Runs: (\d+)\. Passes: (\d+)\..*?Settled: (\d+)", t)
        if s and o:
            pnl = float(s.group(1).replace(",", "")) + float(o.group(1).replace(",", ""))
            spy = float(s.group(2).replace(",", "")) + float(o.group(2).replace(",", ""))
            rows.append({"name": "News paper book (local model reads headlines)", "basis": "$10,000 paper, ETF calls",
                         "pnl": round(pnl, 2), "vs": round(spy, 2), "vs_label": "same dollars in SPY",
                         "note": f"{runs.group(3) if runs else '?'} settled so far; updated {upd.group(1) if upd else '?'}"})
    except Exception as e:   # noqa: BLE001
        rows.append({"name": "News paper book", "note": f"could not read: {e}"[:120]})
    try:
        t = open(os.path.join(ROOT, "state", "twin-crypto-paper.md"), encoding="utf-8").read()
        upd = re.search(r"updated ([0-9-]+ [0-9:]+ UTC)", t)
        tot, n = 0.0, 0
        for m in re.finditer(r"^\| (\w+-twin) \| [^|]+ \| (\d+) \| \d+ \| (\d+) \| [^|]+ \| \$([+-][0-9.,]+) \|", t, re.M):
            tot += float(m.group(4).replace(",", ""))
            n += int(m.group(3))
        rows.append({"name": "Crypto twins up/down paper (Darios, Satya, Jarons Twin)", "basis": "$2 per call, prediction-style",
                     "pnl": round(tot, 2), "vs": None, "vs_label": "",
                     "note": f"{n} settled calls; last update {upd.group(1) if upd else '?'} (paper only)"})
    except Exception as e:   # noqa: BLE001
        rows.append({"name": "Crypto twins paper", "note": f"could not read: {e}"[:120]})
    return rows


# ---------------------------------------------------------------------------------------------------------- summary
def live_value(b, series, live_crypto):
    v = b["cash"]
    for s, q in b["pos"].items():
        px = live_crypto.get(s) if s in D.CRYPTO else series[s].get("live")
        if px is None:
            bars = series[s]["bars"]
            px = bars[-1]["close"] if bars else 0
        v += q * px
    return v


def build_summary(st, bt, cfg, series, flags, fresh, live_crypto, now_ts):
    bench = st["bench"]
    bil_ann_bt = bt["bench"]["bil"]["ann"]
    fund = st["fund"]
    out = {"updated": datetime.fromtimestamp(now_ts, timezone.utc).isoformat(timespec="seconds"), "mode": "paper",
           "capital": cfg["capital"], "forward_start": st["start"], "built": st["created"]}
    fm = E.metrics(fund["eq"])
    fl = fund["reserve"] + sum(live_value(b, series, live_crypto) for b in fund["sleeves"].values())
    out["fund"] = {**fm, "live_value": round(fl, 2), "scale": fund["scale"], "halted": fund["halted"],
                   "reserve": round(fund["reserve"], 2), "events": fund["events"][-12:]}
    out["twin"] = {**E.metrics(st["twin"]["eq"]),
                   "live_value": round(st["twin"]["reserve"] + sum(live_value(b, series, live_crypto) for b in st["twin"]["sleeves"].values()), 2)}
    out["bench"] = {n: {"label": E.BENCHES[n][1], **E.metrics(b["eq"]), "live_value": round(live_value(b, series, live_crypto), 2)}
                    for n, b in bench.items()}
    sl = []
    for n, b in fund["sleeves"].items():
        m = E.metrics(b["eq"])
        t = b["trades"]
        pb = E.p_beat(b["eq"], bench[SLEEVE_BENCH[n]]["eq"])
        days = len(b["eq"])
        v = cfg["verdict"]
        if b["status"] == "retired":
            verdict = "retired"
        elif days < v["min_days"] or pb is None:
            verdict = f"unproven ({days} of {v['min_days']} days)"
        elif pb >= v["p_beat"]:
            verdict = f"beating its benchmark (p={pb:.2f})"
        else:
            verdict = f"not yet beating its benchmark (p={pb:.2f})"
        pos = []
        lv = live_value(b, series, live_crypto)
        for s, q in sorted(b["pos"].items()):
            px = live_crypto.get(s) if s in D.CRYPTO else series[s].get("live")
            val = q * (px or 0)
            pos.append({"sym": s, "qty": round(q, 6), "price": px, "value": round(val, 2),
                        "weight": round(val / lv, 4) if lv else 0, "cost": round(b["cost"].get(s, 0), 4)})
        btm = bt["sleeves"].get(n, {})
        sl.append({"name": n, "desc": E.SLEEVES[n][1], "weight": cfg["weights"][n], "status": b["status"], "scale": b["scale"],
                   "bench": SLEEVE_BENCH[n], "metrics": m, "live_value": round(lv, 2), "trades": t["n"],
                   "win_rate": round(t["wins"] / t["n"], 3) if t["n"] else None, "fees": round(t["fees"], 2),
                   "divs": round(t["divs"], 2), "p_beat": pb, "verdict": verdict, "positions": pos,
                   "pending": bool(b["pending"]), "targets": {k: round(x, 4) for k, x in (b["targets"] or {}).items()},
                   "backtest": {k: btm.get(k) for k in ("ann", "maxdd", "sharpe", "trades", "win_rate", "p_beat", "total")}})
    out["sleeves"] = sl
    out["series"] = {"fund": fund["eq"][-400:], "twin": st["twin"]["eq"][-400:], **{n: b["eq"][-400:] for n, b in bench.items()}}
    out["backtest"] = {k: bt[k] for k in ("label", "start", "fund", "fund_stress3x", "bench", "series", "p_beat_fund_vs_6040")}
    # could this pay the subs?
    lo, hi = cfg["subs_month_low"], cfg["subs_month_high"]
    mid = (lo + hi) / 2
    use_fwd = fm["days"] >= 60 and fm["ann"] is not None
    ann = fm["ann"] if use_fwd else bt["fund"]["ann"]
    src = "live paper" if use_fwd else "backtest - the live book is too young to annualize"
    bil = bil_ann_bt or 0.04
    subs = {"month_low": lo, "month_high": hi, "ann_used": ann, "source": src, "tbill_ann": bil,
            "maxdd_used": fm["maxdd"] if use_fwd else bt["fund"]["maxdd"]}
    if ann and ann > 0:
        subs["monthly_at_capital"] = round(cfg["capital"] * ann / 12, 2)
        subs["capital_needed_mid"] = round(mid * 12 / ann, -2)
        subs["capital_needed_range"] = [round(lo * 12 / ann, -2), round(hi * 12 / ann, -2)]
    subs["plan"] = [round(mid * 12 / 0.07, -2), round(mid * 12 / 0.05, -2)]     # Grok/Fable honest range 5-7%/yr
    subs["tbill_capital_needed_mid"] = round(mid * 12 / bil, -2) if bil > 0 else None
    st3 = bt["fund_stress3x"]["ann"]
    subs["stress3x_ann"] = st3
    out["subs"] = subs
    out["freshness"] = {"last_complete": fresh, "flags": flags,
                        "spy_last": fresh.get("SPY"), "btc_last": fresh.get("BTC-USD")}
    out["compare"] = comparison_rows()
    f = st["fed"]
    out["shadow_fed"] = {"last": f.get("last"), "open": f.get("open"), "closed": f.get("closed", [])[-5:],
                         "pnl": f.get("pnl", 0.0), "n": len(f.get("closed", [])), "error": f.get("error")}
    return out


def write_md(s):
    f = s["fund"]
    lines = [f"# AI Fund Desk - paper only (updated {s['updated']})", "",
             "No real money. No orders. Paper books on free data; dashboard: heartbeatobservatory.com/admin/fund/ (admins only).",
             f"Forward paper book started from the {s['forward_start']} close with ${s['capital']:,.0f}; nothing filled before the build.", "",
             "## Now (live marks)",
             "| Book | Value now | Return (closes) | Max drawdown |", "|---|---|---|---|",
             f"| AI fund | ${f['live_value']:,.0f} | {f['total']:+.2%} | {f['maxdd']:.1%} |",
             f"| Frozen twin (no tuning) | ${s['twin']['live_value']:,.0f} | {s['twin']['total']:+.2%} | {s['twin']['maxdd']:.1%} |"]
    for n, b in s["bench"].items():
        lines.append(f"| {b['label']} | ${b['live_value']:,.0f} | {b['total']:+.2%} | {b['maxdd']:.1%} |")
    lines += ["", "## Sleeves", "| Sleeve | Weight | Status | Value now | Trades | Win rate | Verdict |", "|---|---|---|---|---|---|---|"]
    for x in s["sleeves"]:
        wr = f"{x['win_rate']:.0%}" if x["win_rate"] is not None else "-"
        lines.append(f"| {x['name']} | {x['weight']:.0%} | {x['status']}{' (half size)' if x['scale'] < 1 else ''} | ${x['live_value']:,.0f} | {x['trades']} | {wr} | {x['verdict']} |")
    bt = s["backtest"]
    lines += ["", f"## Backtest since {bt['start']} (label: not evidence)", bt["label"], "",
              "| Book | Yearly return | Max drawdown | Sharpe |", "|---|---|---|---|",
              f"| AI fund | {_pct(bt['fund']['ann'])} | {bt['fund']['maxdd']:.1%} | {bt['fund']['sharpe']} |",
              f"| AI fund at 3x costs | {_pct(bt['fund_stress3x']['ann'])} | {bt['fund_stress3x']['maxdd']:.1%} | {bt['fund_stress3x']['sharpe']} |"]
    for n, b in bt["bench"].items():
        lines.append(f"| {s['bench'][n]['label']} | {_pct(b['ann'])} | {b['maxdd']:.1%} | {b['sharpe']} |")
    u = s["subs"]
    lines += ["", "## Could this pay the subs?", subs_line(s), "",
              "## Other paper books (comparison rows)"]
    for r in s["compare"]:
        lines.append(f"- {r.get('name')}: {('$%+.2f' % r['pnl']) if r.get('pnl') is not None else ''} {r.get('note', '')}")
    lines += ["", "## Data checks", *(f"- {x}" for x in (s["freshness"]["flags"] or ["all clear"]))]
    open(SUMMARY_MD, "w", encoding="utf-8").write("\n".join(lines) + "\n")


def _pct(x):
    return "-" if x is None else f"{x:+.1%}"


def subs_line(s):
    u = s["subs"]
    if not u.get("ann_used") or u["ann_used"] <= 0:
        return (f"Not on current numbers: the {u['source']} return is {_pct(u.get('ann_used'))}/yr. "
                f"T-bills alone would need about ${u['tbill_capital_needed_mid']:,.0f} for ${(u['month_low'] + u['month_high']) / 2:.0f}/month.")
    return (f"At {_pct(u['ann_used'])}/yr ({u['source']}), ${s['capital']:,.0f} makes about ${u['monthly_at_capital']:,.0f}/month. "
            f"Covering ${u['month_low']}-{u['month_high']}/month would take about ${u['capital_needed_range'][0]:,.0f}-"
            f"{u['capital_needed_range'][1]:,.0f}, with drawdowns like {u['maxdd_used']:.0%}. "
            f"Planning at the team's honest 5-7%/yr instead: ${u['plan'][0]:,.0f}-{u['plan'][1]:,.0f}. "
            f"T-bills alone: about ${u['tbill_capital_needed_mid']:,.0f} with almost no drawdown. "
            f"At 3x trading costs the fund's return is {_pct(u.get('stress3x_ann'))}/yr.")


# ------------------------------------------------------------------------------------------------------------ supabase
def push(summary):
    e = env()
    url, key = e.get("SUPABASE_URL"), e.get("SUPABASE_SERVICE_ROLE_KEY")
    if not (url and key):
        return "no Supabase keys"
    h = {"apikey": key, "Authorization": f"Bearer {key}", "Content-Type": "application/json", "Prefer": "return=minimal"}
    body = json.dumps({"kind": "hourly", "payload": summary}).encode()
    req = urllib.request.Request(f"{url.rstrip('/')}/rest/v1/ai_fund_snapshots", data=body, headers=h, method="POST")
    urllib.request.urlopen(req, timeout=30).read()
    cutoff = (datetime.now(timezone.utc) - timedelta(days=14)).strftime("%Y-%m-%dT%H:%M:%SZ")
    req = urllib.request.Request(f"{url.rstrip('/')}/rest/v1/ai_fund_snapshots?at=lt.{cutoff}", headers=h, method="DELETE")
    try:
        urllib.request.urlopen(req, timeout=30).read()
    except Exception:   # noqa: BLE001 - pruning is best effort
        pass
    return f"pushed {len(body) // 1024} KB"


# ---------------------------------------------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-tuner", action="store_true")
    ap.add_argument("--no-push", action="store_true")
    a = ap.parse_args()
    t0 = time.time()
    os.makedirs(OUT, exist_ok=True)
    cfg = load_config()
    now_ts = time.time()
    series = {}
    for s in E.SYMBOLS:
        try:
            series[s] = D.load(s, now_ts)
        except Exception as e:   # noqa: BLE001
            log(f"DATA FAIL {s}: {e}")
            raise SystemExit(1)
    flags, fresh, live_crypto = data_checks(series, now_ts)
    view = E.View(series, now_ts)
    broker = get_broker(cfg)
    st = json.load(open(FORWARD, encoding="utf-8")) if os.path.exists(FORWARD) else init_forward(cfg, now_ts)
    advance_forward(st, view, cfg, broker)
    ev = st["fund"]["events"]
    new = ev[st.get("events_logged", 0):]
    if new:
        with open(os.path.join(ROOT, "projects", "ai-fund", "CHANGELOG.md"), "a", encoding="utf-8") as fh:
            for d_, who, msg in new:
                fh.write(f"- {d_} (close) | engine | {who} | {msg}\n")
        st["events_logged"] = len(ev)
    bt = run_backtest(view, st["config_frozen"], fresh.get("SPY"))
    ief = series["IEF"].get("live")
    fed_shadow(st, ief)
    tmp = FORWARD + ".tmp"
    json.dump(st, open(tmp, "w", encoding="utf-8"))
    os.replace(tmp, FORWARD)
    summary = build_summary(st, bt, cfg, series, flags, fresh, live_crypto, now_ts)
    tune = None
    if not a.no_tuner:
        try:
            import tuner
            tune = tuner.hourly(summary, cfg)
        except Exception as e:   # noqa: BLE001
            tune = {"decision": "error", "note": f"tuner failed: {e}"[:200]}
            log("TUNER ERROR " + traceback.format_exc().splitlines()[-1])
    summary["tuner"] = tune or _last_tuner()
    summary["last_change"] = _last_change()
    json.dump(summary, open(SUMMARY, "w", encoding="utf-8"), indent=1)
    write_md(summary)
    pushed = "skipped"
    if not a.no_push:
        try:
            pushed = push(summary)
        except Exception as e:   # noqa: BLE001
            pushed = f"push failed: {e}"[:160]
    f = summary["fund"]
    log(f"ok {time.time() - t0:.0f}s | fund ${f['live_value']:,.0f} (closes {f['total']:+.2%}) | twin ${summary['twin']['live_value']:,.0f} | "
        f"SPY ${summary['bench']['spy']['live_value']:,.0f} | tuner {(tune or {}).get('decision', '-')} | flags {len(flags)} | {pushed}")


def _last_tuner():
    p = os.path.join(OUT, "tuner-log.jsonl")
    if not os.path.exists(p):
        return None
    lines = open(p, encoding="utf-8").read().strip().splitlines()
    return json.loads(lines[-1]) if lines else None


def _last_change():
    p = os.path.join(OUT, "changes.jsonl")
    if not os.path.exists(p):
        return None
    lines = open(p, encoding="utf-8").read().strip().splitlines()
    return json.loads(lines[-1]) if lines else None


if __name__ == "__main__":
    main()
