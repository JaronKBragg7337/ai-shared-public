"""
crypto_decide.py - the crew's consensus trade for Polymarket US crypto up/down windows (BTC/ETH/SOL/XRP).
Approved by Jaron 2026-10-22 6:30 PM (decisions/CRYPTO-LANE-PLAN-2026-10-22.md). Live start: Control Room `crypto_lane_start`.

Runs every 5 minutes as the Windows task "Crypto Consensus" (pythonw, hidden). For each OPEN window that one of the three
bots (darios-twin, satya-twin, jarons-twin) has called in state/twin-crypto-paper.jsonl:

  when it decides   hourly: 6 min or less left | daily: 2 h or less left | 15 min: 6 min or less left, or as soon as all
                    three have called. Each window is decided ONCE (the decision is final; a later call is ignored).
  the rule (v2)     passing is allowed - every window is the bots' choice. All callers on one side (one bot alone is enough,
                    the others passed) -> one live trade, size = average of the callers' sizes (each clipped to its own cap).
                    Any up-vs-down disagreement, or everyone passing -> no trade, logged. 15m/1d can be switched off in the
                    Control Room (crypto_15m_enabled / crypto_1d_enabled). No 15m buy under 0.25 with under 5 minutes left.
                    The stop counts OPEN risk: settled P&L minus the cost of unsettled positions.
  real fills        every pass first writes the ledger's real fill, any exit, the settlement and hold-vs-exit P&L into each
                    placed row of state/crypto-consensus.jsonl (reconcile_fills).
  one position      a window that already holds a position, or was already traded, is never traded again.
  open-risk limit   all crypto at risk (positions + resting buys) plus this trade <= Control Room `crypto_max_open_usd`
                    (the trade is shrunk to the room left; under $0.50 of room = no trade). A coin whose 24 h correlation with
                    EVERY other coin is below `crypto_decouple_corr` (state/crypto-correlation.json, from crypto_view.py) is its
                    own risk: it is not counted in the shared limit and gets its own limit of the same size.
  before the start  `crypto_lane_start` not reached (Indianapolis date) -> DRY RUN: it asks desk-trade.py to --dry-run
                    (full checks, no order) and logs what it would do. Nothing is placed.
  real orders       ONLY through tools/desk-trade.py --by crew-consensus, with a --why listing the three calls.

    python tools/crypto_decide.py              one pass (what the task runs)
    python tools/crypto_decide.py --dry        force a dry run even after the start date
    python tools/crypto_decide.py --weekly     Monday 6 AM: step each bot's cap +$1 (net-positive week) / -$1 (losing week)
    python tools/crypto_decide.py --calls F --decisions F --md F --state-dir D   test against other files (never the real ones)

Log: state/crypto-consensus.md (plain words) + state/crypto-consensus.jsonl (one line per decision).
"""
import argparse, json, os, re, subprocess, sys, time
from datetime import datetime, timezone, timedelta

HERE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.dirname(HERE)
for _s in (sys.stdout, sys.stderr):
    try: _s.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError): pass

import crypto_view as CV      # noqa: E402
import crypto_paper as CP     # noqa: E402
import desk_schedule as DS    # noqa: E402
from settings import setting  # noqa: E402

CALLS = CP.LOG
DECISIONS = os.path.join(ROOT, "state", "crypto-consensus.jsonl")
MD = os.path.join(ROOT, "state", "crypto-consensus.md")
CORR = CV.CORR_FILE
LOCK = os.path.join(ROOT, "state", ".crypto-decide.lock")
DECIDE_MIN = {"1h": 7, "1d": 120, "15m": 6}        # minutes left at which the crew decides (1h = 7: Satya runs at :52 = 8 left, so he is in)
FRESH_MIN = {"15m": 5, "1h": 30}                  # a call older than this (minutes) counts as a pass
MIN_TRADE = 0.5                                   # desk-trade refuses less than this much room
DEFAULT_CAPS = {"darios-twin": 3, "satya-twin": 3, "jarons-twin": 3}


def now_utc():
    return datetime.now(timezone.utc)


def log(md_path, msg):
    line = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
    print(line, flush=True)
    try:
        with open(md_path, "a", encoding="utf-8", newline="\n") as f: f.write(line + "\n")
    except OSError: pass


# ---- inputs ---------------------------------------------------------------------------------------------------------
def read_jsonl(path):
    out = []
    if os.path.exists(path):
        for l in open(path, encoding="utf-8"):
            l = l.strip()
            if l:
                try: out.append(json.loads(l))
                except ValueError: pass
    return out


def caps_now():
    v = setting("crypto_bot_caps", DEFAULT_CAPS)
    if isinstance(v, str):
        try: v = json.loads(v)
        except ValueError: v = DEFAULT_CAPS
    if not isinstance(v, dict): return {b: 0.0 for b in CP.BOTS}      # a bare 0 = paused
    return {b: float(v.get(b, 0)) for b in CP.BOTS}


def record(calls, bot, tf):
    """(settled paper pnl, wins, n) for this bot on this window type - the 'better record' for the 1-vs-1 tiebreak."""
    d = [r for r in calls if CP.by_of(r) == bot and r["tf"] == tf and "result" in r]
    return sum(r.get("pnl", 0) for r in d), sum(r["result"] == "win" for r in d), len(d)


def correlation(path=None):
    """{coin: best correlation with any other coin} - refreshed from Kraken/Coinbase when the file is over an hour old."""
    path = path or CORR
    try:
        c = json.load(open(path))
        if (now_utc() - datetime.fromisoformat(c["at"])).total_seconds() < 3600: return c.get("max_with_others") or {}
    except Exception:
        pass
    try:
        return CV.correlations(write=(path == CORR)).get("max_with_others") or {}
    except Exception:
        return {}    # unreadable: nothing is treated as decoupled (the conservative way)


def exposure(mcp):
    """Dollars at risk now in crypto up/down windows, by coin: position cost + resting buy orders."""
    by_coin = {}
    now = now_utc()
    def add(slug, usd):
        w = CV.window(slug)
        if not w or w[2] <= now: return
        c = CP.coin_of(slug); by_coin[c] = by_coin.get(c, 0.0) + usd
    pos = (mcp.call("polymarket_positions", {}).get("positions") or {})
    for slug, p in pos.items():
        add(slug, abs(float((p.get("cost") or {}).get("value") or 0)))
    try:
        for o in (mcp.call("polymarket_open_orders", {}).get("orders") or []):
            if "BUY" in str(o.get("intent")):
                add(o.get("marketSlug") or "", float(o.get("leavesQuantity") or 0) * float((o.get("price") or {}).get("value") or 0))
    except Exception:
        pass
    return by_coin, set(pos)


# ---- real fills -----------------------------------------------------------------------------------------------------
def _fill_sum(fl):
    sh = sum(float(x["quantity"] or 0) for x in fl)
    fees = sum(float(m.group(1)) for x in fl for m in [re.search(r"fee ([0-9.]+)", x.get("note") or "")] if m)
    return {"price": round(sum(float(x["price"] or 0) * float(x["quantity"] or 0) for x in fl) / sh, 4) if sh else None,
            "shares": round(sh, 2), "usd": round(sum(float(x["cost_usd"] or 0) for x in fl), 4), "fees": round(fees, 2),
            "n": len(fl), "at": min(x["at"] for x in fl)}


def reconcile_fills(path):
    """Jaron 10/23 step 1: for every PLACED decision, write what really happened into state/crypto-consensus.jsonl:
      fill    = the buys (price vwap, shares, cost with fees)         exit = any sell before the close (price, shares, proceeds)
      settled = the ledger's resolution P&L for the window            hold_pnl = what holding to the close paid (swing-vs-hold data)
    Matched by order id (by slug for older rows) from Supabase desk_trades. Settled rows are left alone, so this stays cheap."""
    recs = read_jsonl(path)
    todo = [r for r in recs if r.get("placed") and not r.get("done")]
    if not todo: return 0
    slugs = sorted({r["slug"] for r in todo})
    inlist = ",".join('"%s"' % s_ for s_ in slugs)
    rows = _sb_get("desk_trades?slug=in.(" + inlist + ")&actor=ilike.*crew-consensus*&select=kind,at,slug,side,price,quantity,cost_usd,pnl_usd,order_id,note,action&limit=1000")
    ex_log = {r["slug"]: r for r in read_jsonl(os.path.join(ROOT, "state", "crypto-exits.jsonl")) if r.get("placed")}
    went = {r["slug"]: r.get("went") for r in CP.rows() if r.get("went")}     # window outcome from the paper settle (Kraken stand-in)
    changed, now = 0, now_utc()
    for r in todo:
        mine = [x for x in rows if x["slug"] == r["slug"]]
        buys = [x for x in mine if x["kind"] == "fill" and (x.get("action") or "buy") == "buy" and (not r.get("order_id") or x.get("order_id") == r["order_id"])]
        sells = [x for x in mine if x["kind"] == "fill" and x.get("action") == "sell"]
        res = [x for x in mine if x["kind"] == "resolution"]
        new = {}
        if buys: new["fill"] = _fill_sum(buys)
        f = new.get("fill") or r.get("fill")
        if sells:
            new["exit"] = _fill_sum(sells)
            if r["slug"] in ex_log: new["exit"].update(by=ex_log[r["slug"]]["by"], why=ex_log[r["slug"]]["why"][:200])
        if res: new["settled"] = {"pnl": round(sum(float(x["pnl_usd"] or 0) for x in res), 4), "at": max(x["at"] for x in res)}
        fin = None
        if f and sells:
            ex = new["exit"]
            realized = ex["usd"] - ex["shares"] * (f["usd"] / f["shares"]) if f["shares"] else 0
            if ex["shares"] >= 0.98 * f["shares"]: fin = realized      # fully sold before the close
            elif res: fin = realized + new["settled"]["pnl"]
        elif res:
            fin = new["settled"]["pnl"]
        if fin is not None: new["final_pnl"] = round(fin, 4)
        w = CV.window(r["slug"])
        over = bool(w) and (now - w[2]).total_seconds() > 600
        if f and w and went.get(r["slug"]) and sells:   # swing-vs-hold data: what holding to the close would have paid
            won = went[r["slug"]] == r["side"]
            new["hold_pnl"] = round((f["shares"] if won else 0) - f["usd"], 4)
        if not buys and over and not f: new["unfilled"] = True; new["done"] = True
        elif fin is not None and (not sells or "hold_pnl" in new or "hold_pnl" in r): new["done"] = True
        if new and any(r.get(k) != v for k, v in new.items()):
            r.update(new); changed += 1
    if changed:
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            for r in recs: f.write(json.dumps(r) + "\n")
        os.replace(tmp, path)
    return changed


# ---- the rule -------------------------------------------------------------------------------------------------------
def consensus(slug_calls, caps, calls_all, tf):
    """slug_calls: {bot: call row}. Returns (side 'up'/'down'/None, size, reason). Missing calls count as a pass."""
    c = {b: slug_calls.get(b) for b in CP.BOTS}
    # 10/22 freshness rule (Jaron OK 8:32 PM): on 15m/1h windows a call older than FRESH_MIN minutes counts as a pass, so a stale
    # call can't pair with a fresh one (the 7 PM XRP trade paired a 16-min-old momentum call with a new long-shot call).
    if tf in FRESH_MIN:
        now_ = now_utc()
        for b, r in list(c.items()):
            if r and (now_ - datetime.fromisoformat(r["at"])).total_seconds() / 60 > FRESH_MIN[tf]:
                c[b] = None
    sides = {b: (r["side"] if r else "pass") for b, r in c.items()}
    sized = lambda b: min(float(c[b].get("size") or 0), caps[b])
    up = [b for b in CP.BOTS if sides[b] == "up"]; down = [b for b in CP.BOTS if sides[b] == "down"]
    # 10/23 v2: passing is allowed. Any disagreement = no trade. One bot alone (the others passed or are silent) CAN trade.
    if up and down: return None, 0, "bots disagree (" + ", ".join(f"{b} {sides[b]}" for b in CP.BOTS) + ") - no trade"
    if not up and not down: return None, 0, "all pass (or no calls)"
    side, who = ("up", up) if up else ("down", down)
    size = round(sum(sized(b) for b in who) / len(who), 2)
    return side, size, (f"{len(who)} of 3 call {side.upper()} ({', '.join(who)}), none against" if len(who) > 1
                        else f"{who[0]} alone calls {side.upper()}, the others passed")


def _sb_get(path):
    import urllib.request
    env = {}
    for l in open(os.path.expanduser("~/.secrets/keys.env"), encoding="utf-8-sig"):
        if "=" in l and not l.startswith("#"): k, v = l.strip().split("=", 1); env[k] = v.strip()
    key = env["SUPABASE_SERVICE_ROLE_KEY"]
    return json.loads(urllib.request.urlopen(urllib.request.Request(env["SUPABASE_URL"].rstrip("/") + "/rest/v1/" + path,
                      headers={"apikey": key, "Authorization": "Bearer " + key}), timeout=20).read())


def lane_start():
    """Control Room crypto_lane_start: a date or a full timestamp (Z). Returns an ISO string for the ledger filter."""
    v = str(setting("crypto_lane_start", "2026-10-26")).strip()
    return v if len(v) > 10 else v + "T00:00:00Z"


def crypto_lane_pnl(since):
    """(settled money, money still open) of the crypto lane's own live trades since `since`. Open = bought but no resolution yet
    (worst case: it all loses). Jaron 10/23: the stop counts open risk, so trades already open can't run past the limit."""
    base = f"desk_trades?slug=like.*-updown-*&at=gte.{since}&actor=not.ilike.*manual*"
    res = _sb_get(base + "&kind=eq.resolution&select=slug,pnl_usd")
    fills = _sb_get(base + "&kind=eq.fill&action=eq.buy&select=slug,cost_usd")
    mine = {f["slug"] for f in fills}
    res = [r for r in res if r["slug"] in mine]       # a position bought BEFORE the restart belongs to the old lane
    done = {r["slug"] for r in res}
    settled = round(sum(float(r.get("pnl_usd") or 0) for r in res), 2)
    open_cost = round(sum(float(f.get("cost_usd") or 0) for f in fills if f["slug"] not in done), 2)
    return settled, open_cost


def live_mode():
    """Returns (mode, note, room). Lane worst case = settled P&L minus the cost of everything still open. Phase 1 = crew consensus
    until that is down crypto_phase1_loss_usd (999 in the v2 test = never switches); at crypto_phase2_loss_usd everything stops.
    `room` = dollars a NEW trade may still risk before the worst case reaches the stop."""
    since = lane_start()
    try: settled, open_cost = crypto_lane_pnl(since)
    except Exception as e: return "consensus", f"lane P&L unreadable ({type(e).__name__}) - staying in consensus", 0.0
    worst = settled - open_cost
    p1, p2 = float(setting("crypto_phase1_loss_usd", 999)), float(setting("crypto_phase2_loss_usd", 10))
    room = round(p2 + worst, 2)
    desc = f"settled {settled:+.2f}, open ${open_cost:.2f} -> worst case {worst:+.2f}"
    if worst <= -p2: return "stopped", f"crypto lane {desc} (stop at -${p2:g}); stopped to talk it over", 0.0
    if worst <= -p1: return "twin", f"crypto lane {desc} - phase 2: Jarons Twin alone", room
    return "consensus", f"crypto lane {desc}; ${room:.2f} of room before the stop", room


def first_come(bc, caps):
    """Jaron 10/23 12:24 AM: 15-minute windows are free ball - the first bot to call a side takes it, no agreement, no waiting.
    One position per window still holds, so a bot that sees the same play later must find another coin."""
    now_ = now_utc()
    live = [(r["at"], b, r) for b, r in bc.items() if r and r.get("side") in ("up", "down")
            and (now_ - datetime.fromisoformat(r["at"])).total_seconds() / 60 <= FRESH_MIN["15m"]]
    if not live: return None, 0, "no fresh call"
    at, b, r = sorted(live)[0]
    return r["side"], round(min(float(r.get("size") or caps.get(b, 3)), caps.get(b, 3)), 2), f"15m free ball: {b} called {r['side'].upper()} first"


def decide_due(tf, left_min, n_calls, bc=None):
    # 10/22 (Jaron: "15 minutes moves fast"): 15m and hourly decide the moment two calls agree on a side - no waiting for the clock.
    if tf == "15m":   # free ball: decide only when a FRESH side call exists, so a stale/pass call never closes the window early
        now_ = now_utc()
        return bool(bc) and any(r and r.get("side") in ("up", "down") and
                                (now_ - datetime.fromisoformat(r["at"])).total_seconds() / 60 <= FRESH_MIN["15m"] for r in bc.values())
    if bc and tf in ("15m", "1h"):
        sides = [r["side"] for r in bc.values() if r["side"] in ("up", "down")]
        if len(sides) >= 2 and len(set(sides)) == 1: return True      # two or more agree and nobody is against
        # 10/23 (Jaron: act in the moment): one fresh side call with nobody against trades right away, at the price it was
        # called - not 26 minutes later at whatever the price has become (the 8:27 ETH call was placed at 8:53).
        if tf == "1h" and len(sides) == 1:
            now_ = now_utc()
            r = next(r for r in bc.values() if r["side"] in ("up", "down"))
            if (now_ - datetime.fromisoformat(r["at"])).total_seconds() / 60 <= 3: return True
    return left_min <= DECIDE_MIN[tf] or (tf == "15m" and n_calls >= 3)


def why_text(slug_calls, reason):
    parts = []
    for b in CP.BOTS:
        r = slug_calls.get(b)
        parts.append(f"{b} ({CP.LENS[b]}): " + (f"{r['side'].upper()} ${r.get('size')} - {r['why'][:70]}" if r else "no call"))
    return f"Crew consensus - {reason}. " + " | ".join(parts)


# ---- one pass -------------------------------------------------------------------------------------------------------
def run(a):
    md = a.md
    sched = DS.load()
    today = DS.local_now(sched).date().isoformat()
    start = lane_start()[:10]
    live = (today >= start) and not a.dry
    mode = "LIVE" if live else "DRY RUN"
    if a.calls is None and live:
        try: reconcile_fills(a.decisions)
        except Exception as e: log(md, f"fill reconcile skipped ({type(e).__name__}: {str(e)[:80]})")
    calls = [r for r in (CP.rows() if a.calls is None else read_jsonl(a.calls)) if not r.get("excluded")]   # no-book calls are not calls
    tfs_on = CV.enabled_tfs()
    decided = {d["slug"] for d in read_jsonl(a.decisions) if d.get("mode") == mode or d.get("placed")}
    now = now_utc()
    by_slug = {}
    for r in calls:
        by_slug.setdefault(r["slug"], {})[CP.by_of(r)] = r
    phase, phase_note, lane_room = live_mode() if (a.calls is None) else ("consensus", "test files", 999.0)
    if phase == "stopped":
        flag2 = os.path.join(ROOT, "state", ".crypto-phase-stop-notified")
        if not os.path.exists(flag2):
            log(md, f"{mode}: STOPPED - {phase_note}")
            if live:
                try: subprocess.run([sys.executable, os.path.join(HERE, "ntfy-say.py"), "Crypto lane stopped", phase_note], timeout=30)
                except Exception: pass
            open(flag2, "w").write(now.isoformat())
        return
    flagp = os.path.join(ROOT, "state", ".crypto-phase")
    if (open(flagp).read().strip() if os.path.exists(flagp) else "consensus") != phase:
        log(md, f"{mode}: PHASE CHANGE -> {phase} ({phase_note})")
        if live and a.calls is None:
            try: subprocess.run([sys.executable, os.path.join(HERE, "ntfy-say.py"), "Crypto lane phase change", phase_note], timeout=30)
            except Exception: pass
        open(flagp, "w").write(phase)
    if phase == "twin":   # phase 2: only the Twin's own calls count, decided as soon as it calls (like its paper record)
        by_slug = {s_: {"jarons-twin": bc["jarons-twin"]} for s_, bc in by_slug.items() if "jarons-twin" in bc and bc["jarons-twin"]["side"] != "pass"}
    todo = []
    for slug, bc in by_slug.items():
        if slug in decided: continue
        w = CV.window(slug)
        if not w or not (w[1] <= now < w[2]): continue
        tf, _, end = w
        if tf not in tfs_on: continue      # switched off in the Control Room (crypto_15m_enabled / crypto_1d_enabled)
        left = (end - now).total_seconds() / 60
        if phase == "twin" or decide_due(tf, left, len(bc), bc) or (tf in ("1h", "1d") and left <= DECIDE_MIN[tf]):
            todo.append((end, slug, tf, left, bc))
    if not todo:
        return
    caps = caps_now()
    max_open = float(setting("crypto_max_open_usd", 25))
    thr = float(setting("crypto_decouple_corr", 0.5))
    corr = correlation(a.corr)
    from executor import Mcp   # noqa: E402  (same local Polymarket MCP desk-trade uses)
    mcp = Mcp()
    stop = float(setting("crypto_stop_account_usd", 65))
    try:   # hard stop (Jaron 10/22 6:33 PM): account value = cash + open position value, same read as desk.py account
        b = (mcp.call("polymarket_account_balances", {}).get("balances") or [{}])[0]
        pos = mcp.call("polymarket_positions", {}).get("positions") or {}
        acct = float(b.get("buyingPower") or 0) + sum(float((p.get("cashValue") or {}).get("value") or 0) for p in pos.values())
    except Exception as e:
        log(md, f"{mode}: account unreadable ({type(e).__name__}) - placing nothing this pass"); return
    flag = os.path.join(ROOT, "state", ".crypto-stop-notified")
    if acct <= stop:
        line = f"stopped: account at ${acct:.2f} <= ${stop:g}"
        if not os.path.exists(flag):
            log(md, f"{mode} {line} - crypto lane places nothing until the Control Room row crypto_stop_account_usd is changed")
            if live and a.calls is None:
                try:
                    subprocess.run([sys.executable, os.path.join(HERE, "ntfy-say.py"), "Crypto lane stopped", line], timeout=30)
                    open(flag, "w").write(now.isoformat())
                except Exception: pass
        return
    if os.path.exists(flag) and a.calls is None:
        os.remove(flag)
    exp, held_slugs = exposure(mcp)
    for end, slug, tf, left, bc in sorted(todo):
        coin = CP.coin_of(slug)
        rec = {"at": now.isoformat(timespec="seconds"), "mode": mode, "slug": slug, "coin": coin, "tf": tf,
               "min_left": round(left, 1), "calls": {b: (bc[b]["side"], bc[b].get("size")) for b in bc}, "placed": False}
        def finish(outcome, note):
            rec.update(outcome=outcome, note=note)
            with open(a.decisions, "a", encoding="utf-8") as f: f.write(json.dumps(rec) + "\n")
            log(md, f"{mode} {coin.upper()} {tf} {slug} ({left:.0f} min left): {outcome.upper()} - {note}")
        if slug in held_slugs:
            finish("pass", "this window already holds a position - one live position per window"); continue
        if left < 1:
            finish("pass", "under a minute left - too late to place"); continue
        if phase == "twin":
            r_ = bc["jarons-twin"]; side = r_["side"]
            size = min(float(r_.get("size") or caps.get("jarons-twin", 3)), float(caps.get("jarons-twin", 3)))
            reason = f"phase 2 (Twin alone): {side.upper()} ${size:.2f}"
        elif tf == "15m":
            side, size, reason = first_come(bc, caps)
        else:
            side, size, reason = consensus(bc, caps, calls, tf)      # passing is allowed (Jaron 10/23 v2)
        if side is None:
            finish("pass", reason); continue
        if size > lane_room:     # worst case (settled minus open cost) must stay inside the lane stop
            if lane_room < MIN_TRADE:
                finish("pass", f"{reason}; lane worst case leaves ${max(lane_room, 0):.2f} before the stop - too little"); continue
            reason += f" [size cut ${size:.2f}->${lane_room:.2f}: lane stop room]"; size = round(lane_room, 2)
        decoupled = corr.get(coin) is not None and corr[coin] < thr
        mine = exp.get(coin, 0.0) if decoupled else sum(v for c, v in exp.items() if not (corr.get(c) is not None and corr[c] < thr))
        room = round(max_open - mine, 2)
        bucket = f"{coin.upper()} on its own (24 h correlation {corr[coin]:.2f} < {thr:g})" if decoupled else "shared crypto"
        if room < MIN_TRADE:
            finish("pass", f"{reason}; {bucket} risk ${mine:.2f} already at the ${max_open:g} limit"); continue
        if size > room:
            reason += f" [size cut ${size:.2f}->${room:.2f}: {bucket} limit ${max_open:g}, ${mine:.2f} at risk]"
            size = room
        if size < MIN_TRADE:
            finish("pass", f"{reason}; size ${size:.2f} is under the ${MIN_TRADE} minimum"); continue
        # 10/22 price guard: the calls may be minutes old. If the side now costs more than 5 cents above what the agreeing bots
        # priced it at, the edge they saw is likely gone - pass.
        try:
            md_ = (mcp.call("polymarket_bbo", {"slug": slug}).get("marketData") or {})
            now_px = float((md_.get("bestAsk" if side == "up" else "shortQuote") or {}).get("value"))
        except Exception:
            now_px = None
        # 10/23 no late long shots: a 15m buy under 0.25 with under 5 minutes left is refused, as code.
        chk_px = now_px if now_px else max([float(r.get("price") or 0) for r in bc.values() if r["side"] == side and r.get("price")] or [0])
        if tf == "15m" and left < 5 and 0 < chk_px < 0.25:
            finish("pass", f"{reason}; late long shot refused: 15m {side} at {chk_px:.2f} (< 0.25) with {left:.1f} min left"); continue
        agree_px = [float(r.get("price") or 0) for r in bc.values() if r["side"] == side and r.get("price")]
        if now_px and agree_px and now_px > max(agree_px) + 0.03:
            finish("pass", f"{reason}; price moved: {side} now {now_px:.2f} vs called at {max(agree_px):.2f} (+3c guard)"); continue
        yn = "yes" if side == "up" else "no"
        cmd = [sys.executable, os.path.join(HERE, "desk-trade.py"), "--by", "crew-consensus", "--slug", slug, "--side", yn,
               "--size", f"{size:.2f}", "--why", why_text(bc, reason),
               "--kill", f"if the {coin.upper()} price ends the window on the other side of its open, this is wrong (paper-scored the same way)"]
        if not live: cmd.append("--dry-run")
        try:
            out = subprocess.run(cmd, capture_output=True, text=True, timeout=240, cwd=ROOT)
            text = ((out.stdout or "") + (out.stderr or "")).strip()
        except Exception as e:
            out, text = None, f"desk-trade could not run: {type(e).__name__}"
        ok = out is not None and out.returncode == 0
        last = " / ".join(l for l in text.splitlines() if l.strip())[-420:]
        rec.update(side=side, desk_side=yn, size=size, reason=reason, desk_output=last[-300:])
        m_ = re.search(r'"result":\s*\{\s*"id":\s*"([A-Z0-9]+)"', text); p_ = re.search(r'"proposal_id":\s*(\d+)', text)
        if m_: rec["order_id"] = m_.group(1)
        if p_: rec["proposal_id"] = int(p_.group(1))
        if live and ok and '"placed": true' in text.lower().replace("'", '"'):
            rec["placed"] = True; exp[coin] = exp.get(coin, 0.0) + size
            finish("traded", f"{side.upper()} ${size:.2f} - {reason}")
        elif not live and ok:
            exp[coin] = exp.get(coin, 0.0) + size   # a dry run counts its own would-be trades toward the limit
            finish("would_trade", f"{side.upper()} ${size:.2f} (desk-trade dry run passed) - {reason}")
        else:
            if "no live book" in last and left > 2:   # 10/23 2 AM: hourly books empty out near the close - retry next minute, don't close the window
                log(md, f"{mode} {coin.upper()} {tf} {slug} ({left:.0f} min left): no live book yet - will retry"); continue
            finish("refused", f"{side.upper()} ${size:.2f} wanted - {reason}; desk-trade said: {last[-200:]}")


# ---- weekly cap step ------------------------------------------------------------------------------------------------
def weekly(a):
    """Each bot's cap +$1 after a net-positive settled week, -$1 after a losing week; floor $1, ceiling desk_max_size_usd.
    The week = settled calls of the last 7 days that are on/after crypto_lane_start (the live trade is made from those same
    calls at the same prices, so counting the paper calls IS counting the live ones; per-bot live P&L cannot be separated)."""
    start = datetime.fromisoformat(lane_start().replace("Z", "+00:00"))
    since = max(now_utc() - timedelta(days=7), start)
    ceil = float(setting("desk_max_size_usd", 10))
    caps = caps_now(); new = dict(caps)
    CP.cmd_settle(argparse.Namespace())
    calls = CP.rows() if a.calls is None else read_jsonl(a.calls)
    for b in CP.BOTS:
        d = [r for r in calls if CP.by_of(r) == b and "result" in r and datetime.fromisoformat(r["end"]) >= since]
        net = sum(r.get("pnl", 0) for r in d)
        if d and net > 0: new[b] = min(ceil, caps[b] + 1)
        elif d and net < 0: new[b] = max(1.0, caps[b] - 1)
        log(a.md, f"WEEKLY {b}: {len(d)} settled calls since {since:%Y-%m-%d}, net ${net:+.2f} -> cap ${caps[b]:g} -> ${new[b]:g}")
    if new != caps and not a.dry:
        sys.path.insert(0, HERE)
        import executor as X
        X.sb(X.secrets(), "PATCH", "system_settings?key=eq.crypto_bot_caps",
             {"value": {b: int(v) if float(v).is_integer() else v for b, v in new.items()}, "updated_by": "crypto_decide.py --weekly"})
        log(a.md, f"WEEKLY caps written to the Control Room: {new}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true", help="force a dry run (weekly: show, don't write)")
    ap.add_argument("--weekly", action="store_true")
    ap.add_argument("--calls", default=None); ap.add_argument("--decisions", default=DECISIONS)
    ap.add_argument("--md", default=MD); ap.add_argument("--corr", default=None)
    a = ap.parse_args()
    if os.path.exists(LOCK) and time.time() - os.path.getmtime(LOCK) < 600 and a.calls is None:
        return   # another pass is still running
    try:
        if a.calls is None: open(LOCK, "w").write(str(os.getpid()))
        (weekly if a.weekly else run)(a)
    finally:
        if a.calls is None and os.path.exists(LOCK): os.remove(LOCK)


if __name__ == "__main__":
    main()
