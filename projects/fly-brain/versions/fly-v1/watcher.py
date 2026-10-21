#!/usr/bin/env python3
"""
watcher.py - a fly with no hands. Smells EVERY live table-tennis market and writes to the ground.

WHY (Jaron, 2026-09-12 23:30): "No fly should be alone." One trading fly learns from a handful of
$1 presses a night. A watcher smells every live table at once, records what the price did 60 s
and 300 s after each smell, and how the match settled. Every trader that follows learns from
matches it never bet on. Zero money, zero risk. Same brain as fly.py; no desk-trade.py.

WHAT IT WRITES  -> Supabase table fly_ground (the colony's shared ground), one row per sniff:
    the six senses, the fly's valence (what its mushroom body felt), and later the outcomes:
    price 60 s / 300 s after; price the first time the set score changes (price_at_next_set); price when the
    match ends and whether our side won (price_at_end, won_at_end). Added 2026-09-16 after ground-school (EXP2,
    Fly-Lab-2) found 41% of 300 s outcomes flat: table-tennis prices move in steps, and a set is the step.
    Also state/fly-brain/watcher.log.md, one line per sniff.

WHAT IT NEVER DOES: press, size, place, or touch the trader's learned weights. It runs the
brain with its OWN mushroom-body store (watcher.npz) so it can be taught from outcomes without
ever touching money - that is step 2 (a watcher that learns from the ground is a scout in
training). v1 just records.

USAGE
    python watcher.py            # forever
    python watcher.py --once     # one sweep of every live table
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import fly as F                     # noqa: E402  Venue, Nose, parse_score, log helpers, brain modules
from flysim import FlyBrain         # noqa: E402
from mushroom import MushroomBody   # noqa: E402
import calibration as C             # noqa: E402

STATE = F.STATE
LOG = STATE / "watcher.log.md"
TICK = 30.0            # seconds between sweeps (15 s drew venue rate limits 2026-09-13) (each sweep sniffs every live table once)
SIM_STEPS = 250
SEEDS = 2
FOLLOWUP = {"price_after_60s": 60, "price_after_300s": 300}


def log(m):
    line = f"[{F.now().strftime('%Y-%m-%d %H:%M:%S')}Z] {m}"
    print(line, flush=True)
    STATE.mkdir(parents=True, exist_ok=True)
    with open(LOG, "a", encoding="utf-8", newline="\n") as fh:
        fh.write(line + "\n")


def sb(env, method, path, body=None):
    url = f"{env['SUPABASE_URL'].rstrip('/')}/rest/v1/{path}"
    key = env["SUPABASE_SERVICE_ROLE_KEY"]
    req = urllib.request.Request(url, data=json.dumps(body).encode() if body is not None else None, method=method,
                                 headers={"apikey": key, "Authorization": f"Bearer {key}",
                                          "Content-Type": "application/json", "Prefer": "return=representation"})
    with urllib.request.urlopen(req, timeout=45) as r:
        raw = r.read()
        return json.loads(raw) if raw else []


def main():
    ap = argparse.ArgumentParser(description="Watcher fly: smells every live table-tennis market, writes the ground. No hands.")
    ap.add_argument("--once", action="store_true")
    ap.add_argument("--name", default="watcher-1")
    a = ap.parse_args()
    STATE.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("FLY_STATE_DIR", str(STATE))

    log(f"=== {a.name} start | every {TICK}s | sim {SIM_STEPS} x {SEEDS} | no hands ===")
    fb = FlyBrain(graph_path=F.RUNTIME / "build" / "graph.npz")
    mb = MushroomBody(fb, store=STATE / f"{a.name}.npz", sides=F.RUNTIME / "build" / "mb_sides.json")
    gains = C.gains_for(fb, F.GAINS)
    nose = F.Nose(fb)
    rec = C.readout(mb)
    venue = F.Venue()
    env = F.secrets()
    log(f"brain up: {fb.n} neurons | own mushroom store {mb.store.name} ({'loaded' if mb.loaded else 'fresh'})")

    last_set_price = {}     # slug -> (sets tuple, price at that set boundary)
    pending = []            # rows awaiting their 60s/300s follow-ups: (row_id, slug, side, t_written, done:set)
    set_pending = {}        # slug -> list of (row_id, sets tuple at sniff, side); resolved when sets change or match ends
    watched = {}            # slug -> {"player","side","our_idx","event","title"} chosen once per market

    while True:
        t0 = time.time()
        try:
            live = venue.live_table_tennis()
            # ---- follow-ups first: what did each earlier smell lead to?
            still = []
            for rid, slug, side, t_w, done in pending:
                age = time.time() - t_w
                due = [k for k, secs in FOLLOWUP.items() if age >= secs and k not in done]
                if due:
                    try:
                        bk = venue.book(slug)
                        p = bk["ask"] if side == "yes" else bk["short"]
                        sb(env, "PATCH", f"fly_ground?id=eq.{rid}", {k: p for k in due})
                        done |= set(due)
                    except Exception as e:
                        log(f"followup {rid} failed: {e}")
                if len(done) < len(FOLLOWUP) and age < 600:
                    still.append((rid, slug, side, t_w, done))
            pending = still

            # ---- one sniff per live table
            n = 0
            for slug, c in live.items():
                m = c["market"]
                b = (m.get("bestBidQuote") or {}).get("value"); k = (m.get("bestAskQuote") or {}).get("value")
                if not (b and k):
                    continue
                b, k = float(b), float(k)
                sides = [sd.get("description", "") for sd in m.get("marketSides", [])]
                if len(sides) == 2 and ({w.lower() for w in sides[0].split() if len(w) > 2} & {w.lower() for w in sides[1].split() if len(w) > 2}):
                    continue
                if slug not in watched:
                    long_side = next((sd.get("description") for sd in m.get("marketSides", []) if sd.get("long")), None)
                    sc0 = venue.score(c["event"])
                    teams = sc0.get("teams") or sides
                    # the watcher smells from the CHEAPER side, like the trader would
                    if k <= 0.5:
                        side, player = "yes", (long_side or sides[0])
                    else:
                        side, player = "no", next((t for t in sides if t != long_side), sides[-1])
                    our_idx = 0 if (teams and teams[0] and player and player.lower() in teams[0].lower()) else 1
                    watched[slug] = {"player": player, "side": side, "our_idx": our_idx, "event": c["event"], "title": c["title"]}
                    log(f"watching {c['title']} from {player} ({side})")
                w = watched[slug]
                sc = venue.score(w["event"])
                if sc["ended"] or not sc["live"]:
                    # match over: close out every open sniff on this table with the final price and who won
                    try:
                        bk_end = venue.book(slug)
                        p_end = bk_end["ask"] if w["side"] == "yes" else bk_end["short"]
                        so, st_, _, _ = F.parse_score(sc["score"])
                        if w["our_idx"] == 1: so, st_ = st_, so
                        won = (so > st_) if sc["ended"] else None
                        for rid, _, _ in set_pending.pop(slug, []):
                            sb(env, "PATCH", f"fly_ground?id=eq.{rid}", {"price_at_end": p_end, "won_at_end": won})
                        # also close set-boundary for sniffs whose set never changed before the end
                    except Exception as e:
                        log(f"match-end followup for {slug} failed: {e}")
                    watched.pop(slug, None)
                    continue
                bk = venue.book(slug)
                sets_o, sets_t, pts_o, pts_t = F.parse_score(sc["score"])
                if w["our_idx"] == 1:
                    sets_o, sets_t, pts_o, pts_t = sets_t, sets_o, pts_t, pts_o
                spread = (bk["ask"] - bk["bid"]) if (bk["ask"] and bk["bid"]) else None
                price = bk["ask"] if w["side"] == "yes" else bk["short"]
                # ---- set-boundary outcomes for earlier sniffs of this table
                if slug in set_pending and price is not None:
                    keep = []
                    for rid, sets_then, side_then in set_pending[slug]:
                        if (sets_o, sets_t) != sets_then:
                            try:
                                sb(env, "PATCH", f"fly_ground?id=eq.{rid}", {"price_at_next_set": price, "sets_at_next_set": f"{sets_o}-{sets_t}"})
                            except Exception as e:
                                log(f"set-boundary followup {rid} failed: {e}")
                        else:
                            keep.append((rid, sets_then, side_then))
                    set_pending[slug] = keep
                prev = last_set_price.get(slug)
                if prev is None or prev[0] != (sets_o, sets_t):
                    last_set_price[slug] = ((sets_o, sets_t), price); prev = last_set_price[slug]
                dprice = (price - prev[1]) if (price is not None and prev[1] is not None) else 0.0
                senses = {"sets_o": sets_o, "sets_t": sets_t, "pts_o": pts_o, "pts_t": pts_t, "price": price,
                          "dprice": dprice, "spread": spread, "player": w["player"], "holding": False}
                drive = nose.drive(senses)
                vals, fired = [], None
                for sd in range(SEEDS):
                    r = fb.run(drive, steps=SIM_STEPS, gains=gains, record=rec, seed=int(time.time()) % 100000 + sd)
                    vals.append(C.valence(r)); fired = r["_fired"]
                val = float(np.mean(vals))
                kc = int(np.isin(fired, mb.kc).sum())
                F.push_live(env, a.name, "watch", {"title": w["title"], "slug": slug, "player": w["player"], "side": w["side"],
                            "score": sc["score"], "period": sc["period"], "sets": [sets_o, sets_t], "pts": [pts_o, pts_t],
                            "price": price, "dprice": round(dprice, 4), "spread": spread, "valence": round(val, 1), "kc": kc,
                            "tables": len(live), "spikes_per_sec": int(r["_spikes_per_sec"])}, fired, cap=1500)
                row = {"fly": a.name, "slug": slug, "event_slug": w["event"], "title": w["title"], "player": w["player"],
                       "side": w["side"], "sets_o": sets_o, "sets_t": sets_t, "pts_o": pts_o, "pts_t": pts_t,
                       "price": price, "dprice": round(dprice, 4), "spread": spread, "valence": round(val, 2), "kc": kc, "pressed": False}
                try:
                    ins = sb(env, "POST", "fly_ground", row)
                    if ins:
                        pending.append((ins[0]["id"], slug, w["side"], time.time(), set()))
                        set_pending.setdefault(slug, []).append((ins[0]["id"], (sets_o, sets_t), w["side"]))
                except Exception as e:
                    log(f"ground write failed for {slug}: {e}")
                log(f"{w['title'][:30]:30} {sc['period']:3} {sc['score']:>16} | us {sets_o}-{sets_t} {pts_o}-{pts_t} {w['side']} @ {price} d {dprice:+.2f} sp {spread} | KC {kc:3d} | val {val:+6.1f}")
                n += 1
            if n == 0:
                log("no live table tennis right now; waiting")
        except KeyboardInterrupt:
            break
        except Exception as e:
            first = (str(e).splitlines() or [""])[0][:160]   # never the whole HTML body
            log(f"error: {type(e).__name__}: {first}")
            time.sleep(30 if "RateLimit" in type(e).__name__ or "429" in first else 5)   # back off when the venue says so
        if a.once:
            break
        time.sleep(max(0.0, TICK - (time.time() - t0)))
    log(f"{a.name} stopped")


if __name__ == "__main__":
    main()
