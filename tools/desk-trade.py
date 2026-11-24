#!/usr/bin/env python3
"""
desk-trade.py - the ONE sanctioned way for a live agent to place a trade from the MSI.

WHO THIS IS FOR
    Agents Jaron has told to trade on their own judgement, in real time, without the approve
    queue - starting with Live Wire (Grok Bot, 2026-09-11: "Auto-trade. If you lose, log what
    happened and why you thought a way."). Speed matters mid-game; a 5-minute approval loop
    does not fit. This command is the compromise: no approval, but ALWAYS a trail.

WHAT IT DOES, IN ORDER
    1. Reads the live book for the slug (bid / ask / short quote) through the local MCP.
    2. Writes a trade_proposals row with verdict='auto' and your name in proposed_by, so the
       trade desk shows who decided and why BEFORE the order exists.
    3. Places the order through the local MCP (credentials never leave the MSI; the venue
       stamps the order AUTOMATIC; the ledger labels it with your name, not Jaron's).
    4. Updates the row with the order id and result. Logs to state/desk-trade.md.

WHAT IT REFUSES
    - size above --max-size (default $10) unless --max-size is raised on the command line
    - a market with no book, or a spread wider than 5c (you would be paying the spread, not
      buying an edge)
    - missing --why. The reason is the whole point. Jaron reads it after a loss.

USAGE (from PowerShell on the MSI, e.g. through the Heartbeat MCP)
    python C:\\Users\\lilli\\AI-Shared\\tools\\desk-trade.py --by grok-bot/live-wire ^
        --slug aec-setkamecz-snimic-moupav-2026-09-11 --side no --size 5 ^
        --why "Moulis down 1-2 in sets and 3-8 in the 4th; price still 0.30 for him" ^
        --kill "if he takes the 4th set, this is wrong - close it"
    Add --dry-run to see everything except the order.
    Add --exit to SELL an existing position on that side instead of buying (close a trade).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
import executor as X  # noqa: E402  (secrets, sb, Mcp, best_ask, build_order live there)

import sys as _sys, os as _os
_sys.path.insert(0, _os.path.dirname(_os.path.realpath(__file__)))
from settings import setting  # Control Room values (/admin/control/), built-in default if unreachable
LOG = os.path.join(ROOT, "state", "desk-trade.md")
MAX_SPREAD = setting("desk_max_spread", 0.05)
# Jaron 2026-09-25: Polymarket pays this month's subscriptions, so it trades short-term - mostly day-of / day-before.
# A market that settles in November or December cannot help a bill due this month. New buys must SETTLE within this
# many days (the venue's real settle time, not the date in the slug: tec-mlb-nlchamp-2026-09-27-atl settles Nov 6).
MAX_DAYS_TO_SETTLE = setting("max_days_to_settle", 14)
VENV_PY = os.path.join(ROOT, "runtime", "polymarket-us-agent-venv", "Scripts", "python.exe")


def settles_at(slug):
    """When this market actually settles (UTC datetime), or None if the venue will not say."""
    code = ("import json,sys\nfrom polymarket_us import PolymarketUS\n"
            "m=PolymarketUS(timeout=30.0).markets.retrieve_by_slug(sys.argv[1])\nm=m.get('market') or m\n"
            "print(json.dumps({'endDate':m.get('endDate'),'gameStartTime':m.get('gameStartTime')}))")
    try:
        import subprocess
        out = subprocess.run([VENV_PY, "-c", code, slug], capture_output=True, text=True, timeout=60).stdout.strip()
        d = json.loads(out.splitlines()[-1])
    except Exception:
        return None
    now = datetime.now(timezone.utc)
    def parse(s):
        try:
            return datetime.fromisoformat(s.replace("Z", "+00:00")) if s else None
        except ValueError:
            return None
    end, gs = parse(d.get("endDate")), parse(d.get("gameStartTime"))
    # a game settles a few hours after it starts; the venue's endDate is a settlement window ~2 weeks later. Use the game time
    # whether it is in the future OR already under way (bug fixed 2026-09-25 7:07 PM: live games were refused as "14+ days out").
    if gs and slug.startswith(("aec-", "asc-", "tsc-", "atc-")) and (end is None or gs < end):   # single games only; futures use endDate
        return gs
    return end


def log(m):
    line = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {m}"
    print(line, flush=True)
    try:
        with open(LOG, "a", encoding="utf-8", newline="\n") as fh:
            fh.write(line + "\n")
    except OSError:
        pass


def _scrub(text):
    r"""2026-09-24: the rationale is shown on the public trades page. Strip local file paths (like C:/Users/...) so the
    machine's folder names never publish. The reasoning itself is left exactly as the agent wrote it."""
    import re
    return re.sub(r"[A-Za-z]:[\\/][^\s|;,]*", "[local path]", text or "")


def is_tennis(slug):
    return any(t in slug for t in ("-atp-", "-wta-", "-itf-"))


def caps(env, slug, cost):
    """Control Room size caps that apply to this bet: [(reason, dollars)]. Tennis is capped while it learns and the cap lifts
    itself once tennis settles in profit over the review count; long shots (bought under longshot_price) are capped always.
    If the record can't be read, the tennis cap stays on."""
    out = []
    if is_tennis(slug):
        since = setting("tennis_cap_since", "2026-09-29T12:40:00Z")
        need = setting("tennis_cap_review_trades", 20)
        lifted = False
        try:
            rows = X.sb(env, "GET", f"desk_trades?select=slug,pnl_usd&actor=eq.auto:grok-bot/live-wire&kind=eq.resolution&at=gte.{since}")
            ten = [float(r["pnl_usd"] or 0) for r in rows if is_tennis(r.get("slug") or "")]
            lifted = len(ten) >= need and sum(ten) > 0
        except Exception:
            pass
        if not lifted:
            out.append(("tennis cap while tennis learns", setting("tennis_max_size_usd", 5.0)))
    # 2026-10-22: the $1 BTC trend-test cap (btc_max_size_usd) is retired. Crypto is now sized by the crew lane: each bot's own
    # cap (crypto_bot_caps) and the shared open-risk limit (crypto_max_open_usd), both enforced by tools/crypto_decide.py.
    if cost < setting("longshot_price", 0.10):
        out.append((f"long shot under {setting('longshot_price', 0.10):.2f}", setting("longshot_max_size_usd", 2.0)))
    return out


def main():
    ap = argparse.ArgumentParser(description="Place one trade from the MSI with a full trail. No approval step.")
    ap.add_argument("--by", required=True, help="who is deciding, e.g. grok-bot/live-wire")
    ap.add_argument("--slug", required=True)
    ap.add_argument("--side", required=True, choices=["yes", "no"])
    ap.add_argument("--size", required=True, type=float, help="dollars")
    ap.add_argument("--why", required=True, help="the reasoning, one or two sentences")
    ap.add_argument("--kill", default="", help="what would make this wrong")
    ap.add_argument("--p", type=float, default=None, help="your own probability for the side, 0-1, if you have one")
    ap.add_argument("--max-size", type=float, default=setting("desk_max_size_usd", 10.0))
    ap.add_argument("--exit", action="store_true", help="SELL this side (close) instead of buying")
    ap.add_argument("--target", type=float, default=None,
                    help="with --exit: an auto-sell target (price of YOUR side, 0-1). The sell rests on the book and fills by itself if the price gets there (Polymarket's 'Auto sell if you're up')")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    if a.by.lower().startswith(("claude", "codex", "chatgpt", "openai", "anthropic")):
        raise SystemExit(f"refused: {a.by} may not trade (Q-018: OpenAI and Anthropic products never touch money)")
    if a.size > a.max_size:
        raise SystemExit(f"refused: size ${a.size:.2f} is above --max-size ${a.max_size:.2f}")
    if len(a.why.strip()) < 15:
        raise SystemExit("refused: --why is too short to be a reason")

    sched, lane_cap_usd = None, None
    if not a.exit:   # the weekly schedule (Control Room `desk_schedule`): NEW positions only; exits are never blocked.
        try:         # If the schedule can't be read or fails, fall through to the old behaviour - never block everything.
            import desk_schedule as DS
            sched = DS.load()
            if sched:
                now_l = DS.local_now(sched)
                msg = DS.refusal(sched, a.slug, now_l)
                if msg:
                    raise SystemExit(msg)
                lane_cap_usd = DS.lane_cap(sched, a.slug, now_l)
        except SystemExit:
            raise
        except Exception as e:
            print(f"note: desk schedule not applied ({str(e)[:80]})")

    env = X.secrets()
    mcp = X.Mcp()
    bid, ask, short = X.best_ask(mcp, a.slug)
    if bid is None or ask is None:
        raise SystemExit(f"refused: no live book for {a.slug}")
    spread = round(ask - bid, 4)
    if spread > MAX_SPREAD:
        raise SystemExit(f"refused: spread {spread:.2f} is wider than {MAX_SPREAD:.2f} - you would be paying the spread")
    if not a.exit:   # closing a position is always allowed, whatever its date
        when = settles_at(a.slug)
        if when is None:
            raise SystemExit(f"refused: could not read when {a.slug} settles - short-term rule needs that date")
        days = (when - datetime.now(timezone.utc)).total_seconds() / 86400
        if days > MAX_DAYS_TO_SETTLE:
            raise SystemExit(f"refused: {a.slug} settles {when:%Y-%m-%d}, {days:.0f} days out. Polymarket is short-term "
                             f"(settles within {MAX_DAYS_TO_SETTLE} days) - it pays this month's bills.")
    cost = ask if a.side == "yes" else short
    # one bot per game (Jaron 10/2) - OFF since 10/11 (Jaron: "loosen up"; Darios: it blocked adding/fading good swings).
    # The per-game cap (game_cap_pct) still limits the total in one game. Control Room row one_bot_per_game turns it back on.
    if not a.exit and a.by.startswith("grok-bot/") and setting("one_bot_per_game", False):
        try:
            import re as _re
            base = _re.sub(r"^a[a-z]c-", "", a.slug); base = _re.sub(r"-(neg|pos)-\d+pt\d+$", "", base)   # one game across its markets (winner, spread, total)
            rows = X.sb(env, "GET", f"desk_trades?select=actor,kind,action,quantity,slug&slug=like.*{base}*&actor=like.auto:grok-bot*")
            if not any(r["kind"] == "resolution" for r in rows):
                held = {}
                for r in rows:
                    if r["kind"] != "fill" or r["actor"] == f"auto:{a.by}": continue
                    q = abs(float(r.get("quantity") or 0))
                    held[r["actor"]] = held.get(r["actor"], 0) + (q if (r.get("action") or "buy") == "buy" else -q)
                owner = next((k for k, v in held.items() if v > 0.01), None)
                if owner:
                    raise SystemExit(f"refused: {owner.split('/')[-1]} already holds this game - pick another game")
        except SystemExit:
            raise
        except Exception:
            pass
    if not a.exit:   # size caps from the Control Room (Jaron's yes 2026-09-29): shrink the bet, never block it
        capped = caps(env, a.slug, cost)
        try:   # one-game cap as a share of the account (Jaron 10/9 after FAMU: $29 of $49 on one game). Grows with the account.
            b = (mcp.call("polymarket_account_balances", {}).get("balances") or [{}])[0]
            pm = mcp.call("polymarket_positions", {}).get("positions") or {}
            held = sum(abs(float((p.get("cost") or {}).get("value") or 0)) for p in pm.values())
            bankroll = float(b.get("buyingPower") or 0) + held
            game_cap = max(setting("game_cap_min_usd", 5.0), bankroll * setting("game_cap_pct", 35) / 100)
            capped.append((f"one game is at most {setting('game_cap_pct', 35):g}% of the ${bankroll:.0f} account", round(game_cap, 2)))
        except Exception as e:
            print(f"note: one-game cap not applied ({str(e)[:60]})")
        if lane_cap_usd is not None:
            capped.append((f"schedule cap ${lane_cap_usd:g} for this lane right now", lane_cap_usd))
        if capped:   # caps are per MATCH, not per order: two $5 buys on one tennis match made $10 (Paolini, 2026-10-02)
            try:
                p = (mcp.call("polymarket_positions", {}).get("positions") or {}).get(a.slug) or {}
                already = abs(float((p.get("cost") or {}).get("value") or 0))
            except Exception:
                already = 0.0
            capped = [(w, max(0.0, c - already)) for w, c in capped]
        for why_cap, cap in capped:
            if cap < 0.5:
                raise SystemExit(f"refused: {why_cap} - this market already holds its cap")
            if a.size > cap:
                print(f"note: size ${a.size:.2f} cut to ${cap:.2f} - {why_cap} (Control Room)")
                a.why = f"{a.why} [size cut ${a.size:.2f}->${cap:.2f}: {why_cap}]"
                a.size = cap
    shares = round(a.size / cost, 2)

    if a.exit:
        # close: sell what we hold on that side. SELL_LONG for yes, SELL_SHORT for no. Price on the
        # YES scale for shorts, same convention as buying (see executor.build_order).
        intent = "ORDER_INTENT_SELL_LONG" if a.side == "yes" else "ORDER_INTENT_SELL_SHORT"
        # Confirmed from Jaron's own Smyk sale 2026-09-11 08:53: SELL_LONG limit is on the YES scale,
        # the minimum you accept (his 0.30 filled at the 0.40 bid). SELL_SHORT is economically a
        # buy-back of YES, so its limit is the most you will pay: the YES ask.
        px = bid if a.side == "yes" else ask
        if a.target:   # 10/23 (Jaron): resting auto-sell - the order waits at the target instead of selling at today's price
            if not 0.01 <= a.target <= 0.99: raise SystemExit("refused: --target must be between 0.01 and 0.99")
            px = a.target if a.side == "yes" else round(1 - a.target, 2)
        # Never sell more than we hold: an exit sized in dollars once sold past zero and flipped a $5 NO into a ~$65 YES
        # (Darios Twin, 2026-10-02). Cap the quantity to the shares held on that side; refuse if nothing is held there.
        held = float(((mcp.call("polymarket_positions", {}).get("positions") or {}).get(a.slug) or {}).get("netPositionDecimal") or 0)
        held_side = held if a.side == "yes" else -held
        if held_side <= 0:
            raise SystemExit(f"refused: no {a.side.upper()} position held on {a.slug} to exit")
        if shares > held_side:
            print(f"note: exit cut from {shares:.2f} to the {held_side:.2f} shares held")
            shares = int(held_side * 100) / 100   # round down so the formatted quantity never exceeds what is held
        order = {"marketSlug": a.slug, "intent": intent, "type": "ORDER_TYPE_LIMIT",
                 "price": {"value": f"{px:.2f}", "currency": "USD"}, "quantity": f"{shares:.2f}",
                 "tif": "TIME_IN_FORCE_GOOD_TILL_CANCEL"}
    else:
        order = X.build_order({"side": a.side, "slug": a.slug, "size_usd": a.size}, cost)

    md = {}
    try:
        m = mcp.call("polymarket_market", {"slug": a.slug})
        md = (m.get("market") or m) if isinstance(m, dict) else {}
    except Exception:
        pass
    question = md.get("question") or a.slug
    long_side = next((sd.get("description") for sd in md.get("marketSides", []) if sd.get("long")), None)
    outcome = long_side if long_side and long_side != "Yes" else (md.get("title") or "Yes")

    row = {
        "slug": a.slug, "question": f"{question} — {outcome}" if outcome != question else question, "outcome": outcome,
        "side": a.side, "entry_price": round(cost, 4), "bid": bid, "ask": ask, "spread": spread,
        "scout_probability": a.p, "scout_confidence": None,
        "edge": (round((a.p - cost), 4) if (a.p is not None and a.side == "yes") else round((bid - a.p), 4) if a.p is not None else None),
        "size_usd": a.size, "open_interest": None,
        "rationale": f"[{a.by}, live, no approval] {'EXIT: ' if a.exit else ''}{_scrub(a.why)}",
        "kill_criteria": a.kill or None,
        "verdict": "auto", "decided_at": datetime.now(timezone.utc).isoformat(),
        "verification": "match", "verified_by": "desk-trade.py (same-second book read)",
        "verified_at": datetime.now(timezone.utc).isoformat(), "verified_bid": bid, "verified_ask": ask,
        "verification_note": "read at placement; no second agent - this was a live, self-directed trade",
        "proposed_by": a.by, "category": md.get("category"),
        "market_type": md.get("sportsMarketType") or md.get("marketType"),
        "placed": False,
    }
    if a.dry_run:
        log(f"DRY RUN {a.by}: {json.dumps(order)} | book {bid}/{ask} short {short} | row would be: {json.dumps(row)[:300]}")
        return
    # 2026-09-20: the receipt must never stand in front of the trade. If Supabase is down (it was, disk full, all day),
    # write the same row to state/desk-trail-offline.jsonl and place anyway; tools/desk-trail-sync.py replays it later.
    rid = None; offline = False
    try:
        r = X.sb(env, "POST", "trade_proposals", row)
        rid = r[0]["id"] if r else None
    except Exception as e:
        offline = True
        row["_offline"] = {"reason": str(e)[:200], "at": datetime.now(timezone.utc).isoformat(), "by": a.by}
        with open(os.path.join(X.ROOT, "state", "desk-trail-offline.jsonl"), "a", encoding="utf-8") as fh:
            fh.write(json.dumps(row) + "\n")
        log(f"SUPABASE DOWN ({str(e)[:80]}) - trail written offline; placing anyway")
    result = mcp.call("polymarket_place_order", {"order": order})
    ok = isinstance(result, dict) and not result.get("error") and "error" not in json.dumps(result).lower()[:200]
    note = json.dumps(result)[:400]
    upd = {"placed": bool(ok), "placed_at": datetime.now(timezone.utc).isoformat() if ok else None,
           "fill_note": ("submitted " + json.dumps(order) + " -> " + note) if ok else ("SUBMIT FAILED: " + note)}
    if rid and not offline:
        try:
            X.sb(env, "PATCH", f"trade_proposals?id=eq.{rid}", upd)
        except Exception as e:
            offline = True; log(f"SUPABASE DOWN on update ({str(e)[:80]}) - result written offline")
    if offline:
        with open(os.path.join(X.ROOT, "state", "desk-trail-offline.jsonl"), "a", encoding="utf-8") as fh:
            fh.write(json.dumps({"_offline_update_for": {"slug": a.slug, "side": a.side, "by": a.by, "at": row["decided_at"]}, **upd}) + "\n")
    log(f"#{rid} {a.by} {'EXIT ' if a.exit else ''}{a.side.upper()} {a.slug} ${a.size:.2f} @ {cost:.2f} -> {'PLACED' if ok else 'FAILED'} {note[:140]} | why: {a.why[:120]}")
    print(json.dumps({"proposal_id": rid, "placed": bool(ok), "order": order, "result": result}, indent=1)[:1500])


if __name__ == "__main__":
    main()
