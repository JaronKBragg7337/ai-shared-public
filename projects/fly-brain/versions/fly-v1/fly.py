#!/usr/bin/env python3
"""
fly.py - Fly #1. A real fruit-fly brain watching one live table-tennis market.

WHAT THIS IS (Jaron, Q-013, 2026-09-12)
    Not a model, not a bot. 165,122 neurons and 10.2M synapses measured from an actual male
    Drosophila (MaleCNS v1.0), run forward as leaky integrate-and-fire (runtime: fruitflydev/
    flycoinrh, flysim.py + mushroom.py). The only thing that learns is the one place a fly's
    brain learns: Kenyon-cell -> mushroom-body-output synapses, under dopamine.

HOW THE MARKET BECOMES A SMELL
    A fly's mushroom body learns which smells lead to sugar. So the state of the match is
    presented as an odour: each sense drives its own bank of olfactory glomeruli (ORN types)
    at a rate proportional to its value. 53 glomeruli exist in the connectome; ~40 are used.
    The fly never sees a number. It smells "ahead in sets, behind in points, price low, price
    fell since last set, this player" as one compound odour, the way a coin smelled of banana.

WHAT IT DOES
    Every TICK seconds: read score + book (Polymarket US API, the venue's own live feed),
    build the odour, run the brain for one window, read approach-vs-avoid MBON valence.
    valence above PRESS for N ticks  -> buy (harness runs desk-trade.py --by fly-brain)
    holding and valence below LETGO   -> sell (--exit)
    That is the whole output.

WHAT IT FEELS
    Realized P&L on its own trades (ledger) -> dopamine. Profit = PAM (sugar). Loss = PPL1
    (shock). The KC pattern that was active at press time is replayed first so the lesson
    lands on the smell it acted on, not whatever it is sniffing minutes later at settlement
    (the runtime's author flags this exact gap; forget_trace() + replay is the answer here).
    Milestones (Jaron's ladder) fire a LARGE burst and change the fly's world - see LADDER.

WHAT IT NEVER SEES
    Size. The cap lives in state/fly-brain/cap.json, written only by this harness:
    $1/trade, $5 exposure to start; +$1/+$5 per $10 realized; floor $1/$5.

HONEST LABELS (same as the runtime's own): the circuit, the plasticity site, the direction of
the learning rule and the sparse-KC calibration are measured. The reward pairing (P&L ->
dopamine), the sense->glomerulus assignment, the rates, the thresholds and the tick are chosen.

USAGE
    python fly.py --dry-run           # everything except orders; the default
    python fly.py --live              # orders go out (Jaron flips this)
    python fly.py --once              # one tick, print the odour and readout, exit
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
RUNTIME = HERE / "runtime"
AI_SHARED = HERE.parent.parent
STATE = AI_SHARED / "state" / "fly-brain"
TOOLS = AI_SHARED / "tools"
sys.path.insert(0, str(RUNTIME))
sys.path.insert(0, str(TOOLS))

from flysim import FlyBrain            # noqa: E402
from mushroom import MushroomBody      # noqa: E402
import calibration as C                # noqa: E402

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

# ---- chosen constants (say so) ----------------------------------------------------------
LIVE_CACHE_S = 20.0        # reuse another fly's venue scan if it is this fresh (shared cache, 2026-09-16)
TICK = 5.0                 # seconds between sniffs (3 s + watcher drew venue rate limits 2026-09-13; a point takes 10-20 s)
SIM_STEPS = 250            # 50 ms of brain time per sniff (dt = 0.2 ms)
SEEDS = 3                  # average valence over this many Poisson seeds (single-seed swing is ~40 Hz)
PRESS = 20.0               # STARTING valence (Hz) above which the fly wants in - then moved only by its own P&L
LETGO = -15.0              # STARTING valence below which a held position is let go - same
BAR_STEP = 1.0             # Hz the bars move per realized outcome (chosen); bounds below are chosen too
PRESS_BOUNDS = (5.0, 40.0)
LETGO_BOUNDS = (-30.0, -5.0)
CONFIRM = 2                # consecutive ticks required
COOLDOWN = 90.0            # seconds after a refused or completed press before the next attempt
MAX_HZ = 150.0             # a glomerulus fully driven
GAINS = "pn05_apl10_kc03"  # the runtime author's calibrated setting (sparse KCs, 2.8-10.7%)
MIN_MATCH_SECS = 90        # ignore a market until it has been live this long (score feed settles)
CAP_FILE = STATE / "cap.json"           # rebound per mode in main(): cap.live.json / cap.dry.json
MEM_FILE = STATE / "memory.json"        # likewise memory.live.json / memory.dry.json
HOLD_FILE = STATE / "holding.json"      # likewise; the open position survives a restart
LOG = STATE / "log.md"
MILESTONES = STATE / "milestones.md"
GRADS = STATE / "graduates"
LADDER = [(50.0, "graduate v1", "weights checkpoint kept forever"),
          (100.0, "own property", "TODO: clone to a Cloudflare Container (built when earned)"),
          (250.0, "a sibling", "TODO: second fly from this checkpoint on a second market")]


def now():
    return datetime.now(timezone.utc)


def log(m, echo=True):
    line = f"[{now().strftime('%Y-%m-%d %H:%M:%S')}Z] {m}"
    if echo:
        print(line, flush=True)
    STATE.mkdir(parents=True, exist_ok=True)
    with open(LOG, "a", encoding="utf-8", newline="\n") as fh:
        fh.write(line + "\n")


# ---- the venue ---------------------------------------------------------------------------
class Venue:
    """Polymarket US: live score from the event, book from the market. Public, no key."""
    def __init__(self):
        from polymarket_us import PolymarketUS
        self.c = PolymarketUS(timeout=20.0)

    def live_table_tennis(self):
        """Every live table-tennis moneyline. Uses the tag filter the app's Live tab uses
        (events.list tagSlug=table-tennis, up to 3 pages) - keyword search missed 7 of 8 live
        Setka matches on 2026-09-12 14:02 (Jaron: "no live then what are these??").
        Shared cache (2026-09-16): whoever scans writes state/fly-brain/live-tables.json; a reader that finds
        it fresher than LIVE_CACHE_S reuses it instead of hitting the venue (fly + watcher were each scanning
        every tick and drawing rate limits)."""
        cache = STATE / "live-tables.json"
        try:
            if cache.exists() and (time.time() - cache.stat().st_mtime) < LIVE_CACHE_S:
                return json.loads(cache.read_text(encoding="utf-8"))
        except Exception:
            pass
        out = {}
        for off in (0, 100, 200):
            try:
                r = self.c.events.list({"closed": False, "limit": 100, "offset": off, "tagSlug": ["table-tennis"]})
            except Exception:
                break
            evs = r.get("events") or []
            for e in evs:
                if not e.get("live") or e.get("ended"):
                    continue
                for m in e.get("markets") or []:
                    if m.get("marketType") != "moneyline" or m.get("closed"):
                        continue
                    out[m["slug"]] = {"event": e["slug"], "title": e.get("title"), "market": m}
            if len(evs) < 100:
                break
        try:
            STATE.mkdir(parents=True, exist_ok=True)
            tmp = cache.with_suffix(".tmp"); tmp.write_text(json.dumps(out), encoding="utf-8"); tmp.replace(cache)
        except Exception:
            pass
        return out

    def score(self, event_slug):
        e = self.c.events.retrieve_by_slug(event_slug)
        e = e.get("event") or e
        return {"score": e.get("score") or "", "period": e.get("period") or "", "live": bool(e.get("live")),
                "ended": bool(e.get("ended")), "updated": (e.get("eventState") or {}).get("updatedAt"),
                "teams": [t.get("name") for t in (e.get("teams") or [])]}

    def book(self, market_slug):
        md = (self.c.markets.bbo(market_slug) or {}).get("marketData") or {}
        g = lambda k: (md.get(k) or {}).get("value")
        f = lambda x: float(x) if x not in (None, "") else None
        return {"bid": f(g("bestBid")), "ask": f(g("bestAsk")), "short": f(g("shortQuote")),
                "oi": f(md.get("openInterest"))}


def parse_score(s):
    """'11-5, 5-10' -> sets (ours, theirs), current-set points (ours, theirs), points played."""
    sets_o = sets_t = 0
    cur = (0, 0)
    parts = [p.strip() for p in s.split(",") if p.strip()]
    for i, p in enumerate(parts):
        m = re.match(r"^(\d+)\s*-\s*(\d+)$", p)
        if not m:
            continue
        a, b = int(m.group(1)), int(m.group(2))
        done = (max(a, b) >= 11 and abs(a - b) >= 2)
        if done and i < len(parts) - 1 or (done and i == len(parts) - 1):
            if a > b: sets_o += 1
            else: sets_t += 1
            cur = (0, 0)
        else:
            cur = (a, b)
    return sets_o, sets_t, cur[0], cur[1]


# ---- the nose ----------------------------------------------------------------------------
class Nose:
    """Senses -> glomerulus banks -> FlyBrain drive dict. Assignment is CHOSEN and fixed."""
    def __init__(self, fb):
        self.fb = fb
        orn = fb.where(type_re=r"^ORN_")
        self.gl = sorted({t.split("_", 1)[1] for t in fb.types[orn]})   # 53 names
        self.idx = {g: tuple(fb.where(type_re=f"^ORN_{re.escape(g)}$").tolist()) for g in self.gl}
        # banks: name -> list of glomeruli. Disjoint. 4 per signed sense (2 per sign), 5 for a ramp.
        g = iter(self.gl)
        take = lambda n: [next(g) for _ in range(n)]
        self.bank = {
            "sets_ahead": take(3), "sets_behind": take(3),
            "pts_ahead": take(3), "pts_behind": take(3),
            "late_set": take(2),                     # points played in current set (momentum window)
            "price": take(5),                        # ramp: k-th glomerulus on when price > k/5
            "price_up": take(3), "price_down": take(3),
            "spread": take(2),
            "player": take(4),                       # a hash of OUR player's name (memory hook)
            "holding": take(2),                      # the fly can smell that it is already in
        }
        self.player_pool = list(g)                   # remaining glomeruli for player hashes

    def player_odor(self, name):
        h = hashlib.sha1(name.lower().encode()).digest()
        pool = self.bank["player"] + self.player_pool
        picks = sorted({pool[h[i] % len(pool)] for i in range(4)})
        return picks

    def drive(self, s):
        """s: dict of senses -> {tuple(neuron_idx): hz}."""
        d = {}
        def bank(name, level):                      # level 0..1 -> all glomeruli in the bank at level*MAX
            lvl = float(np.clip(level, 0.0, 1.0))
            if lvl <= 0.02: return
            for gl in self.bank[name]:
                d[self.idx[gl]] = lvl * MAX_HZ
        sd = s["sets_o"] - s["sets_t"]
        bank("sets_ahead", sd / 2.0); bank("sets_behind", -sd / 2.0)
        pd = s["pts_o"] - s["pts_t"]
        bank("pts_ahead", pd / 6.0); bank("pts_behind", -pd / 6.0)
        bank("late_set", (s["pts_o"] + s["pts_t"]) / 20.0)
        for k, gl in enumerate(self.bank["price"]):    # thermometer code for price
            if s["price"] is not None and s["price"] > (k + 0.5) / 5.0:
                d[self.idx[gl]] = MAX_HZ * 0.8
        dp = s["dprice"] or 0.0
        bank("price_up", dp / 0.25); bank("price_down", -dp / 0.25)
        bank("spread", (s["spread"] or 0) / 0.05)
        for gl in self.player_odor(s["player"]):
            d[self.idx[gl]] = MAX_HZ * 0.6
        bank("holding", 1.0 if s["holding"] else 0.0)
        return d


# ---- money, memory, ladder (harness-only) ------------------------------------------------
def load_json(p, default):
    try:
        return json.load(open(p, encoding="utf-8"))
    except Exception:
        return default


def save_json(p, obj):
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(obj, fh, indent=1)


def cap_state():
    c = load_json(CAP_FILE, {"per_trade": 1.0, "exposure": 5.0, "realized": 0.0, "milestones": []})
    c.setdefault("press", PRESS); c.setdefault("letgo", LETGO)   # the bars live with the money, per mode
    return c


def apply_realized(cap, pnl):
    """The money rule: +$1/+$5 per $10 realized, symmetric, floored. Returns new milestones."""
    before = cap["realized"]
    cap["realized"] = round(before + pnl, 4)
    tier = int(max(cap["realized"], 0) // 10)
    cap["per_trade"] = 1.0 + tier
    cap["exposure"] = 5.0 + 5 * tier
    # the bars: a win lowers the press bar (that valence earned sugar), a loss raises it; let-go mirrors.
    # Measured by the fly's own outcomes; only the step and the bounds are chosen (Jaron 2026-09-13: measured vs chosen).
    if pnl > 0:
        cap["press"] = max(PRESS_BOUNDS[0], cap.get("press", PRESS) - BAR_STEP)
        cap["letgo"] = max(LETGO_BOUNDS[0], cap.get("letgo", LETGO) - BAR_STEP)
    elif pnl < 0:
        cap["press"] = min(PRESS_BOUNDS[1], cap.get("press", PRESS) + BAR_STEP)
        cap["letgo"] = min(LETGO_BOUNDS[1], cap.get("letgo", LETGO) + BAR_STEP)
    hit = []
    for thr, name, what in LADDER:
        if before < thr <= cap["realized"] and name not in cap["milestones"]:
            cap["milestones"].append(name)
            hit.append((thr, name, what))
    return hit


# ---- the ledger (reward source) -----------------------------------------------------------
def secrets():
    out = {}
    p = Path.home() / ".secrets" / "keys.env"
    if p.exists():
        for line in open(p, encoding="utf-8"):
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                out[k.strip()] = v.strip().strip('"').strip("'")
    return out


def ledger_realized(env, seen_ids, holding):
    """New realized outcomes for the fly's trades since we last looked -> [(id, slug, pnl)].
    Two sources (Codex audit: resolutions alone miss every early exit):
      - resolution rows (venue settled the market): pnl_usd is authoritative
      - a SELL fill on the slug we are holding: pnl = (sell proceeds) - (what we paid)"""
    import urllib.request
    url = f"{env['SUPABASE_URL'].rstrip('/')}/rest/v1/desk_trades?select=id,slug,kind,pnl_usd,cost_usd,price,quantity,note,actor&actor=eq.auto:fly-brain&order=at.desc&limit=80"
    key = env["SUPABASE_SERVICE_ROLE_KEY"]
    req = urllib.request.Request(url, headers={"apikey": key, "Authorization": f"Bearer {key}"})
    with urllib.request.urlopen(req, timeout=30) as r:
        rows = json.load(r)
    out = []
    for r in rows:
        if r["id"] in seen_ids:
            continue
        if r["kind"] == "resolution" and r.get("pnl_usd") is not None:
            out.append((r["id"], r["slug"], float(r["pnl_usd"])))
        elif r["kind"] == "fill" and "SELL" in (r.get("note") or "") and holding and r["slug"] == holding["slug"]:
            proceeds = float(r.get("cost_usd") or 0)          # for a sell the reconciler's cost_usd is the cash received
            paid = float(holding.get("paid") or holding["size"])
            out.append((r["id"], r["slug"], round(proceeds - paid, 4)))
    return out


# ---- the site's window into the fly ----------------------------------------------------------
def post_action(env, **row):
    """One row to fly_actions so /live-systems/flies/ can show what the fly did. Never blocks."""
    try:
        import urllib.request
        url = f"{env['SUPABASE_URL'].rstrip('/')}/rest/v1/fly_actions"
        key = env["SUPABASE_SERVICE_ROLE_KEY"]
        req = urllib.request.Request(url, data=json.dumps(row).encode(), method="POST",
                                     headers={"apikey": key, "Authorization": f"Bearer {key}",
                                              "Content-Type": "application/json", "Prefer": "return=minimal"})
        urllib.request.urlopen(req, timeout=20).read()
    except Exception as e:
        log(f"fly_actions write failed: {e}", echo=False)


# ---- the live feed for the 3D scene ---------------------------------------------------------
_ATLAS_POS = None    # atlas index -> position in the compact atlas (so the scene can look up xyz)


def atlas_lookup():
    global _ATLAS_POS
    if _ATLAS_POS is None:
        try:
            idx = json.load(open(STATE / "atlas.json", encoding="utf-8"))["index"]
            _ATLAS_POS = {int(n): i for i, n in enumerate(idx)}
        except Exception:
            _ATLAS_POS = {}
    return _ATLAS_POS


def push_live(env, fly, mode, state, fired, cap=3000):
    """Overwrite this fly's row in fly_live: senses/feeling + which atlas neurons spiked. Cheap,
    every tick. The scene lights those dots. Sampled to <= cap so the row stays ~10 KB."""
    look = atlas_lookup()
    f = [look[int(n)] for n in fired if int(n) in look]
    if len(f) > cap:
        f = [int(x) for x in np.random.default_rng().choice(f, cap, replace=False)]
    state = dict(state, fired_total=int(len(fired)), fired_shown=len(f))
    try:
        with open(STATE / f"live.{fly}.json", "w", encoding="utf-8") as fh:
            json.dump({"at": now().isoformat(), "mode": mode, "state": state, "fired": f}, fh, separators=(",", ":"))
    except OSError:
        pass
    try:
        import urllib.request
        url = f"{env['SUPABASE_URL'].rstrip('/')}/rest/v1/fly_live?on_conflict=fly"
        key = env["SUPABASE_SERVICE_ROLE_KEY"]
        body = json.dumps({"fly": fly, "at": now().isoformat(), "mode": mode, "state": state, "fired": f}, separators=(",", ":")).encode()
        req = urllib.request.Request(url, data=body, method="POST",
                                     headers={"apikey": key, "Authorization": f"Bearer {key}", "Content-Type": "application/json",
                                              "Prefer": "return=minimal,resolution=merge-duplicates"})
        urllib.request.urlopen(req, timeout=15).read()
    except Exception as e:
        log(f"fly_live push failed: {e}", echo=False)


# ---- hands ----------------------------------------------------------------------------------
def desk_trade(args, live):
    """Run the hands. Returns (ok, text). ok is decided by the EXIT CODE and, when live, by the
    'placed' flag in desk-trade.py's JSON result - never by scanning output for words
    (Codex audit 2026-09-12: a traceback could be mistaken for an accepted order)."""
    py = str(AI_SHARED / "runtime" / "polymarket-us-agent-venv" / "Scripts" / "python.exe")
    if not os.path.exists(py):
        py = "python"
    cmd = [py, str(TOOLS / "desk-trade.py")] + args + ([] if live else ["--dry-run"])
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120)
    except subprocess.TimeoutExpired:
        return False, "desk-trade timed out"
    text = (r.stdout + r.stderr)[-700:]
    if r.returncode != 0:
        return False, f"exit {r.returncode}: {text.strip()[-200:]}"
    if not live:
        return True, text
    m = re.search(r"\{.*\}", r.stdout, re.S)
    try:
        res = json.loads(m.group(0)) if m else {}
        return bool(res.get("placed")), text
    except ValueError:
        return False, "no JSON result from desk-trade: " + text.strip()[-200:]


# ---- main loop -----------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description="Fly #1 - a real fly brain on one live table-tennis market.")
    ap.add_argument("--live", action="store_true", help="orders go out (default: dry run)")
    ap.add_argument("--once", action="store_true", help="one tick and exit")
    ap.add_argument("--slug", help="force a market slug (else: pick the best live one)")
    a = ap.parse_args()
    live = bool(a.live)
    if a.slug and live:
        raise SystemExit("--slug bypasses the market screen and is for DRY RUN only")
    STATE.mkdir(parents=True, exist_ok=True)
    (STATE / "graduates").mkdir(exist_ok=True)
    os.environ.setdefault("FLY_STATE_DIR", str(STATE))
    # Money and memory are per MODE. Dry-run pretend profit must never raise the live cap
    # (Codex audit 2026-09-12). The LEARNED WEIGHTS are shared on purpose - practice counts.
    global CAP_FILE, MEM_FILE, HOLD_FILE
    mode = "live" if live else "dry"
    CAP_FILE = STATE / f"cap.{mode}.json"
    MEM_FILE = STATE / f"memory.{mode}.json"
    HOLD_FILE = STATE / f"holding.{mode}.json"

    log(f"=== fly #1 start | {'LIVE' if live else 'DRY RUN'} | tick {TICK}s | sim {SIM_STEPS} steps x {SEEDS} seeds | gains {GAINS} ===")
    fb = FlyBrain(graph_path=RUNTIME / "build" / "graph.npz")
    mb = MushroomBody(fb, store=STATE / "mb_gains.v2.npz", sides=RUNTIME / "build" / "mb_sides.json")
    gains = C.gains_for(fb, GAINS)
    nose = Nose(fb)
    rec = C.readout(mb)
    log(f"brain up: {fb.n} neurons | KC->MBON synapses {len(mb.pos)} | learned state {'loaded' if mb.loaded else 'fresh'} | events so far {mb.events}")
    venue = Venue()
    env = secrets()
    cap = cap_state(); save_json(CAP_FILE, cap)
    mem = load_json(MEM_FILE, {"players": {}, "seen_ledger_ids": []})
    seen = set(mem["seen_ledger_ids"])

    market = None          # {"slug","event","title","player","start"}
    holding = load_json(HOLD_FILE, None)   # {"slug","side","price","kc","at","size","paid"} - survives restarts
    if holding:
        # Reconcile with the venue: is that position actually still open?
        try:
            pos = {}
            if live:
                r = subprocess.run([sys.executable, str(TOOLS / "desk.py"), "account", "--json"], capture_output=True,
                                   text=True, encoding="utf-8", errors="replace", timeout=60)
                pos = (json.loads(r.stdout).get("positions") or {}).get("positions") or {}
            still = (holding["slug"] in pos) if live else True
            if still:
                log(f"restored holding from disk: {holding['side']} {holding['slug']} @ {holding['price']} (${holding['size']}) - will watch for its exit")
                market = {"slug": holding["slug"], "event": holding.get("event"), "title": holding.get("title", holding["slug"]),
                          "player": holding.get("player", "?"), "side": holding["side"], "our_idx": holding.get("our_idx", 0), "start": time.time()}
            else:
                log(f"holding on disk ({holding['slug']}) is not open at the venue any more - it settled while we were down; reward will arrive from the ledger")
                holding = None; save_json(HOLD_FILE, None)
        except Exception as e:
            log(f"could not reconcile holding with the venue ({e}); keeping it and watching")
    last_set_price = None
    last_sets = None
    streak = 0
    last_save = time.time()
    streak_sign = 0
    cooldown_until = 0.0
    pending_exit = None    # after a live LET GO: the position context kept until the ledger shows the sell
    last_reward_poll = 0.0

    def poll_rewards():
        nonlocal holding, pending_exit, last_reward_poll, cap, seen
        if not live or time.time() - last_reward_poll < 30:
            return
        last_reward_poll = time.time()
        ctx = holding or pending_exit
        for rid, slug, pnl in ledger_realized(env, seen, ctx):
            seen.add(rid)
            size = ctx["size"] if ctx and ctx["slug"] == slug else cap["per_trade"]
            mb.forget_trace()
            if ctx and ctx["slug"] == slug:
                mb.observe(np.asarray(ctx["kc"]))
            hit = mb.dopamine(+1 if pnl > 0 else -1, min(1.0, abs(pnl) / max(size, 0.5)))
            mb.apply()
            hits = apply_realized(cap, pnl); save_json(CAP_FILE, cap)
            log(f"REWARD {slug} realized {pnl:+.2f} -> {'PAM (sugar)' if pnl > 0 else 'PPL1 (shock)'} on {hit} synapses | cap ${cap['per_trade']:.0f}/${cap['exposure']:.0f} realized ${cap['realized']:.2f}")
            post_action(env, fly="fly-1", mode="live", action="reward", slug=slug, pnl=round(pnl, 4),
                        cap_per_trade=cap["per_trade"], cap_exposure=cap["exposure"],
                        note=f"{'sugar' if pnl > 0 else 'shock'} on {hit} synapses; realized to date ${cap['realized']:.2f}")
            mem["players"].setdefault((ctx or {}).get("player") or slug, []).append(round(pnl, 2))
            for thr, name, what in hits:
                for _ in range(3):
                    mb.dopamine(+1, 1.0)
                mb.apply()
                if name == "graduate v1":
                    mb.save(); import shutil
                    shutil.copy(mb.store, GRADS / f"v1-{now().strftime('%Y%m%d-%H%M')}.npz")
                with open(MILESTONES, "a", encoding="utf-8", newline="\n") as fh:
                    fh.write(f"{now().isoformat()} | ${thr:.0f} realized | {name} | {what}\n")
                log(f"MILESTONE ${thr:.0f}: {name} - LARGE burst. {what}")
                post_action(env, fly="fly-1", mode="live", action="milestone", pnl=thr, note=f"{name}: {what}")
            if holding and holding["slug"] == slug:
                holding = None; save_json(HOLD_FILE, None)
            if pending_exit and pending_exit["slug"] == slug:
                pending_exit = None
        mem["seen_ledger_ids"] = sorted(seen)[-500:]; save_json(MEM_FILE, mem)

    while True:
        t0 = time.time()
        try:
            poll_rewards()
            # ---- pick / keep a market
            if market is None:
                cands = venue.live_table_tennis()
                if a.slug and a.slug in cands:
                    cands = {a.slug: cands[a.slug]}
                pick = None
                for slug, c in cands.items():
                    m = c["market"]
                    b = (m.get("bestBidQuote") or {}).get("value"); k = (m.get("bestAskQuote") or {}).get("value")
                    if not (b and k): continue
                    b, k = float(b), float(k)
                    long_side = next((sd.get("description") for sd in m.get("marketSides", []) if sd.get("long")), None)
                    sides = [sd.get("description", "") for sd in m.get("marketSides", [])]
                    if len(sides) == 2 and ({w.lower() for w in sides[0].split() if len(w) > 2} & {w.lower() for w in sides[1].split() if len(w) > 2}):
                        continue   # same-name ambiguity (Jaron 2026-09-11)
                    if not a.slug and (k - b > 0.02 or not (0.20 <= k <= 0.80)): continue   # --slug bypasses the screen (dry-run testing)
                    # The fly bets the cheaper side (there is no edge in buying an 80c favourite for a
                    # fly that learns from sugar). yes = long side at the ask; no = other side at shortQuote.
                    ev = venue.score(c["event"])
                    teams = ev.get("teams") or sides
                    if k <= 0.5:
                        side, player = "yes", (long_side or sides[0])
                    else:
                        side, player = "no", next((t for t in sides if t != long_side), sides[-1])
                    our_idx = 0 if (teams and teams[0] and player and player.lower() in teams[0].lower()) else 1
                    pick = {"slug": slug, "event": c["event"], "title": c["title"], "player": player, "side": side,
                            "our_idx": our_idx, "start": time.time()}
                    break
                if pick is None:
                    log("no live table-tennis market passes the screen; waiting", echo=a.once)
                    if a.once: return
                    time.sleep(15); continue
                market = pick; last_set_price = None; last_sets = None; streak = 0
                log(f"watching {market['title']} | market {market['slug']} | our side = {market['player']} ({market['side'].upper()}, score index {market['our_idx']})")

            # ---- senses
            sc = venue.score(market["event"])
            bk = venue.book(market["slug"])
            if sc["ended"] or not sc["live"]:
                log(f"match over: {market['title']} final {sc['score']}")
                if holding and holding["slug"] == market["slug"]:
                    log("still holding at the end - the venue will settle it; reward arrives via the ledger")
                market = None; continue
            sets_o, sets_t, pts_o, pts_t = parse_score(sc["score"])
            if market["our_idx"] == 1:
                sets_o, sets_t, pts_o, pts_t = sets_t, sets_o, pts_t, pts_o
            spread = (bk["ask"] - bk["bid"]) if (bk["ask"] and bk["bid"]) else None
            price = bk["ask"] if market["side"] == "yes" else bk["short"]   # what one share of OUR side costs
            if last_sets is None or (sets_o, sets_t) != last_sets:
                last_sets = (sets_o, sets_t); last_set_price = price
            dprice = (price - last_set_price) if (price is not None and last_set_price is not None) else 0.0
            senses = {"sets_o": sets_o, "sets_t": sets_t, "pts_o": pts_o, "pts_t": pts_t, "price": price,
                      "dprice": dprice, "spread": spread, "player": market["player"],
                      "holding": bool(holding and holding["slug"] == market["slug"])}

            # ---- sniff
            drive = nose.drive(senses)
            vals = []
            fired = None
            for sd in range(SEEDS):
                r = fb.run(drive, steps=SIM_STEPS, gains=gains, record=rec, seed=int(time.time()) % 100000 + sd)
                vals.append(C.valence(r)); fired = r["_fired"]
            val = float(np.mean(vals))
            mb.observe(fired)                          # eligibility: what the KCs just did
            kc_now = np.intersect1d(fired, mb.kc)
            push_live(env, "fly-1", "live" if live else "dry", {
                "title": market["title"], "slug": market["slug"], "player": market["player"], "side": market["side"],
                "score": sc["score"], "period": sc["period"], "sets": [sets_o, sets_t], "pts": [pts_o, pts_t],
                "price": price, "dprice": round(dprice, 4), "spread": spread, "valence": round(val, 1),
                "seeds": [round(v, 1) for v in vals], "kc": int(len(kc_now)), "holding": bool(holding),
                "cap": [cap["per_trade"], cap["exposure"]], "realized": cap.get("realized", 0.0),
                "press_thr": cap["press"], "letgo_thr": cap["letgo"],
                "mb_events": mb.events, "gain_mean": round(float(mb.gain.mean()), 4),
                "spikes_per_sec": int(r["_spikes_per_sec"]), "mean_mv": round(float(r["_mean_mv"]), 1)}, fired)

            # ---- decide (dumb harness logic around a felt valence)
            sign = 1 if val > cap["press"] else (-1 if val < cap["letgo"] else 0)
            streak = streak + 1 if sign == streak_sign and sign != 0 else (1 if sign != 0 else 0)
            streak_sign = sign
            action = "-"
            if holding is None and sign > 0 and streak >= CONFIRM and price is not None and cap["per_trade"] <= cap["exposure"] and time.time() >= cooldown_until:
                why = f"fly valence {val:+.1f}Hz x{streak} | sets {sets_o}-{sets_t} pts {pts_o}-{pts_t} price {price:.2f} d {dprice:+.2f} spread {spread:.2f}"
                ok, out = desk_trade(["--by", "fly-brain", "--slug", market["slug"], "--side", market["side"],
                                      "--size", f"{cap['per_trade']:.2f}", "--max-size", f"{cap['per_trade']:.2f}",
                                      "--why", why, "--kill", "valence below letgo for 2 ticks"], live)
                if ok:
                    holding = {"slug": market["slug"], "side": market["side"], "price": price, "kc": kc_now.tolist(),
                               "at": now().isoformat(), "size": cap["per_trade"], "paid": cap["per_trade"],
                               "event": market["event"], "title": market["title"], "player": market["player"], "our_idx": market["our_idx"]}
                    save_json(HOLD_FILE, holding)
                action = f"PRESS {market['side'].upper()} ${cap['per_trade']:.2f} @ {price:.2f} {'(dry)' if not live else ''} x{streak} -> {'ok' if ok else 'REFUSED'}: {out.strip()[-110:]}"
                post_action(env, fly="fly-1", mode="live" if live else "dry", action="press" if ok else "refused",
                            slug=market["slug"], title=market["title"], player=market["player"], side=market["side"],
                            price=price, size_usd=cap["per_trade"], valence=round(val, 1), score=sc["score"],
                            sets_o=sets_o, sets_t=sets_t, pts_o=pts_o, pts_t=pts_t,
                            cap_per_trade=cap["per_trade"], cap_exposure=cap["exposure"], note=out.strip()[-160:])
                streak = 0; cooldown_until = time.time() + COOLDOWN
            elif holding is not None and holding["slug"] == market["slug"] and sign < 0 and streak >= CONFIRM:
                why = f"fly valence {val:+.1f}Hz x{streak} | sets {sets_o}-{sets_t} pts {pts_o}-{pts_t} price {price:.2f}"
                pnl = None
                ok, out = desk_trade(["--by", "fly-brain", "--slug", market["slug"], "--side", holding["side"], "--exit",
                                      "--size", f"{holding['size']:.2f}", "--max-size", f"{holding['size']:.2f}", "--why", why], live)
                action = f"LET GO @ {price:.2f} {'(dry)' if not live else ''} x{streak} -> {'ok' if ok else 'FAILED'}: {out.strip()[-110:]}"
                if not ok:
                    streak = 0; cooldown_until = time.time() + COOLDOWN   # still holding; try again after the cooldown
                elif not live:   # dry run: settle it ourselves so learning can be exercised
                    pnl = (price - holding["price"]) / holding["price"] * holding["size"] if price else 0.0
                    mb.forget_trace(); mb.observe(np.asarray(holding["kc"]))
                    mb.dopamine(+1 if pnl > 0 else -1, min(1.0, abs(pnl) / holding["size"])); mb.apply()
                    hits = apply_realized(cap, pnl); save_json(CAP_FILE, cap)
                    action += f" | dry pnl {pnl:+.2f} -> dopamine {'PAM' if pnl > 0 else 'PPL1'} | cap ${cap['per_trade']:.0f}/${cap['exposure']:.0f}"
                post_action(env, fly="fly-1", mode="live" if live else "dry", action="letgo" if ok else "refused",
                            slug=market["slug"], title=market["title"], player=market["player"], side=holding["side"] if holding else None,
                            price=price, size_usd=holding["size"] if holding else None, valence=round(val, 1), score=sc["score"],
                            sets_o=sets_o, sets_t=sets_t, pts_o=pts_o, pts_t=pts_t,
                            pnl=(round(pnl, 4) if (ok and not live) else None),
                            cap_per_trade=cap["per_trade"], cap_exposure=cap["exposure"], note=out.strip()[-160:])
                if ok:
                    if live:
                        pending_exit = holding      # keep the KC pattern until the ledger confirms the sell
                    holding = None; save_json(HOLD_FILE, None); streak = 0; cooldown_until = time.time() + COOLDOWN

            log(f"{market['title'][:34]:34} {sc['period']:3} {sc['score']:>14} | us {sets_o}-{sets_t} {pts_o}-{pts_t} {market['side']} @ {price if price is None else f'{price:.2f}'} d {dprice:+.2f} sp {spread if spread is None else f'{spread:.2f}'} "
                f"| KC {len(kc_now):3d} | val {val:+6.1f} ({'/'.join(f'{v:+.0f}' for v in vals)}) streak {streak_sign:+d}x{streak} | {action}",
                echo=True)


            if time.time() - last_save > 600:
                mb.save(); save_json(MEM_FILE, mem); last_save = time.time()
                log(f"checkpoint | mb events {mb.events} | gain mean {float(mb.gain.mean()):.4f} min {float(mb.gain.min()):.3f}")
        except KeyboardInterrupt:
            break
        except Exception as e:
            first = (str(e).splitlines() or [""])[0][:160]   # never the whole HTML body
            log(f"error: {type(e).__name__}: {first}")
            time.sleep(10 if "RateLimit" in type(e).__name__ or "429" in first else 5)   # back off when the venue says so (watcher waits 30)
        if a.once:
            break
        time.sleep(max(0.0, TICK - (time.time() - t0)))
    mb.save(); save_json(MEM_FILE, mem)
    log("fly #1 stopped; learned state saved")


if __name__ == "__main__":
    main()
