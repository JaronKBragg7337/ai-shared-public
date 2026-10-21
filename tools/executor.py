#!/usr/bin/env python3
"""
executor.py — a SCRIPT. Not the fly brain. It does not think. It presses the button.

JARON'S DESIGN, 2026-09-10 22:33:
    "The fly brain doesn't need to be smart at all. It just needs to press a button and make
    it action. The WHY can come from all the other AIs. They give the reasoning and the
    research and the data collection that shows up on the website, I press approve, and
    then the fly brain does that."

CORRECTION 2026-09-10 23:00, from Jaron: this script is NOT the fly brain. Four layers:
    SCRIPTS    - this file, verifier.py. Quick, dumb, kept no matter what. Never grow.
    FLY BRAIN  - a small AGENT that presses the same button but can be taught over time.
                 Grows the workforce. Does not exist yet. The scripts keep running beside it.
    CORTEX     - Scout, Bridge, Codex, Claude Code, ChatGPT. Research, propose, verify, and
                 feed the fly brain its smarts. They CAN trade; it is not their role.
    MANUAL     - Jaron running this through the Grok app. Proven, but manual.

Every intelligent step lives UPSTREAM of this file:
    Scout researches (price-blind)  ->  Bridge proposes (edge > spread)
    -> Claude Code verifies the book independently  ->  Jaron presses Approve on
    /live-systems/trades/.
This script runs AFTER all of that. It has no opinion. It reads the queue, checks the price
has not run away, submits the order, records what happened. Nothing else.

WHY A SCRIPT AND NOT AN AGENT
    Jaron approved a trade and it sat for over an hour, because the executor was Bridge - a
    smart agent that waits to be told things in a chat. Smart executors are slow executors.
    A script polls every few minutes whether or not anyone is talking to it.

WHAT IT WILL AND WILL NOT DO
    - Acts ONLY on rows where verdict='approved' AND verification='match' AND placed=false.
      An unverified approval is not acted on. A mismatch is never acted on.
    - Re-reads the live book before every order. If the ask has moved more than TOLERANCE
      above the approved entry, it does NOT chase - it marks the row and moves on.
    - Never sizes, never picks a side, never chooses a market. Those are all upstream.
    - Records every outcome in the row so the website shows it.

DRY RUN IS THE DEFAULT. It does everything except submit. Pass --live to submit.
    Claude Code wrote this and tested it dry. Claude Code does not run it live - that is
    for the scheduled task (registered by Codex or Jaron) or for Bridge. The plumber does
    not turn on the water.

USAGE
    python tools/executor.py            # dry run: shows exactly what it WOULD place
    python tools/executor.py --live     # submits orders
    python tools/executor.py --live --loop 300   # every 5 minutes, forever
"""

from __future__ import annotations

import argparse
import json
import re
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
SECRETS = os.path.join(os.path.expanduser("~"), ".secrets", "keys.env")
MCP = "http://127.0.0.1:8765/mcp"
TOLERANCE = 0.01      # do not chase more than 1c above the approved entry
STALE_HOURS = 6       # an approval older than this with a moved price expires
LOG = os.path.join(ROOT, "state", "executor.md")


def log(m):
    line = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {m}"
    print(line, flush=True)
    try:
        with open(LOG, "a", encoding="utf-8", newline="\n") as fh:
            fh.write(line + "\n")
    except OSError:
        pass


def secrets() -> dict:
    out = {}
    # keys.env holds most keys; kraken.env (added 2026-09-24) is kept separate so Jaron can open it alone and paste.
    for SECRETS in (os.path.join(os.path.dirname(globals()["SECRETS"]), "keys.env"),
                    os.path.join(os.path.dirname(globals()["SECRETS"]), "kraken.env")):
        if not os.path.exists(SECRETS):
            continue
        with open(SECRETS, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if "=" in line and not line.startswith("#"):
                    k, v = line.split("=", 1)
                    out[k.strip()] = v.strip().strip('"').strip("'")
    return out


def sb(env, method, path, body=None):
    url = f"{env['SUPABASE_URL'].rstrip('/')}/rest/v1/{path}"
    key = env["SUPABASE_SERVICE_ROLE_KEY"]
    req = urllib.request.Request(
        url, data=json.dumps(body).encode() if body is not None else None, method=method,
        headers={"apikey": key, "Authorization": f"Bearer {key}",
                 "Content-Type": "application/json", "Prefer": "return=representation"})
    with urllib.request.urlopen(req, timeout=45) as r:
        raw = r.read()
        return json.loads(raw) if raw else []


def sb_all(env, path, page=1000):
    """GET every row for a PostgREST path. Supabase caps one response at 1000 rows no matter what limit= says, so a bare
    `limit=5000` silently returned an arbitrary 1000 of desk_trades (fills without their resolutions - the 10/11 bug).
    Pages with a stable order (at, id) until a short page comes back."""
    sep = "&" if "?" in path else "?"
    out, off = [], 0
    while True:
        chunk = sb(env, "GET", f"{path}{sep}order=at.asc,id.asc&limit={page}&offset={off}")
        out += chunk
        if len(chunk) < page:
            return out
        off += page


class Mcp:
    """Minimal Streamable-HTTP MCP client against the local Polymarket service."""
    def __init__(self):
        self.sid = None
        self._rpc({"jsonrpc": "2.0", "id": 1, "method": "initialize",
                   "params": {"protocolVersion": "2025-06-18", "capabilities": {},
                              "clientInfo": {"name": "executor", "version": "1"}}})

    def _rpc(self, payload):
        h = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream"}
        if self.sid:
            h["Mcp-Session-Id"] = self.sid
        req = urllib.request.Request(MCP, data=json.dumps(payload).encode(), headers=h)
        with urllib.request.urlopen(req, timeout=90) as r:
            if r.headers.get("Mcp-Session-Id"):
                self.sid = r.headers["Mcp-Session-Id"]
            raw = r.read().decode("utf-8", "replace")
            for line in raw.splitlines():
                if line.startswith("data: "):
                    return json.loads(line[6:])
            return json.loads(raw) if raw.strip() else None

    def call(self, name, args):
        r = self._rpc({"jsonrpc": "2.0", "id": 2, "method": "tools/call",
                       "params": {"name": name, "arguments": args}})
        try:
            return json.loads(r["result"]["content"][0]["text"])
        except Exception:
            return r


def best_ask(mcp, slug):
    """Returns (bid, ask, short) - all on the YES book except `short`, which is the venue's own
    quote for buying NO (shortQuote, ~= 1 - bid). A NO order is priced off `short`, never the
    YES ask: on 2026-09-11 the first NO proposals (Canelo at 0.27) would have sat forever
    because this compared the YES ask 0.75 against an entry of 0.27 and called it 'moved'."""
    r = mcp.call("polymarket_bbo", {"slug": slug})
    md = r.get("marketData", {}) if isinstance(r, dict) else {}
    ask = (md.get("bestAsk") or {}).get("value")
    bid = (md.get("bestBid") or {}).get("value")
    short = (md.get("shortQuote") or {}).get("value")
    bid = float(bid) if bid else None
    ask = float(ask) if ask else None
    short = float(short) if short else (round(1 - bid, 4) if bid is not None else None)
    return bid, ask, short


def build_order(row, cost):
    """Approved side + verified cost -> the exact retail order object. No judgement here.
    `cost` is what one share of the chosen side costs: YES ask for yes, shortQuote for no.

    PRICE CONVENTION (learned from Jaron's own app orders, 2026-09-11, /v1/portfolio/activities):
    a BUY_SHORT limit's `price` is on the YES scale - it is the price you SELL yes at, i.e.
    1 - (what you pay for no). His "$1 at 8%" buy went out as BUY_SHORT price 0.82. Sending the
    NO price (0.27) is accepted and usually fills, but it is not a real limit: it means "sell yes
    at >= 0.27", which on a moved book could pay far more for NO than was approved."""
    intent = "ORDER_INTENT_BUY_LONG" if row["side"] == "yes" else "ORDER_INTENT_BUY_SHORT"
    cost = round(cost, 2)
    price = cost if row["side"] == "yes" else round(1 - cost, 2)
    shares = round(float(row["size_usd"]) / cost, 2)
    return {
        "marketSlug": row["slug"],
        "intent": intent,
        "type": "ORDER_TYPE_LIMIT",
        "price": {"value": f"{price:.2f}", "currency": "USD"},
        "quantity": f"{shares:.2f}",
        "tif": "TIME_IN_FORCE_GOOD_TILL_CANCEL",
    }


# 2026-09-23 (Claude Code): skip markets whose date in the slug is well past. Settled games have no book, and re-asking
# for ~30 of them every 5 minutes tripped Polymarket's rate limit (Cloudflare HTML error pages), which also starved the
# live price reads Live Wire and the verifier need. Nothing is marked or changed on these rows; they are just not polled.
_SLUG_DATE = re.compile(r"(\d{4}-\d{2}-\d{2})")
def slug_is_past(slug, grace_days=2):
    m = _SLUG_DATE.search(slug or "")
    if not m:
        return False
    try:
        d = datetime.fromisoformat(m.group(1)).replace(tzinfo=timezone.utc)
    except ValueError:
        return False
    return (datetime.now(timezone.utc) - d).total_seconds() > grace_days * 86400


def run_once(env, live):
    rows = sb(env, "GET", "trade_proposals?or=(verdict.eq.approved,and(verdict.eq.auto,decided_by.eq.deepseek-auto))&placed=eq.false&verification=eq.match&select=*")
    if not rows:
        log("nothing approved and unplaced")
        return
    mcp = Mcp()
    for row in rows:
        rid = row["id"]
        if slug_is_past(row["slug"]):
            continue
        approved_at = datetime.fromisoformat(row["decided_at"].replace("Z", "+00:00"))
        age_h = (datetime.now(timezone.utc) - approved_at).total_seconds() / 3600
        bid, ask, short = best_ask(mcp, row["slug"])
        entry = float(row["entry_price"])
        cost = ask if row["side"] == "yes" else short      # what one share of OUR side costs now
        if cost is None:
            log(f"#{rid} {row['slug']}: no quote on the book for side {row['side']} - skipping this cycle")
            continue
        if cost > entry + TOLERANCE:
            note = f"price moved: approved at {entry:.2f}, {row['side']} now costs {cost:.2f} (+{cost-entry:.2f}), tolerance {TOLERANCE:.2f}"
            if age_h > STALE_HOURS:
                sb(env, "PATCH", f"trade_proposals?id=eq.{rid}", {"verdict": "expired", "fill_note": note + " - expired"})
                log(f"#{rid} EXPIRED after {age_h:.1f}h: {note}")
            else:
                log(f"#{rid} waiting: {note}")
            continue

        order = build_order(row, cost)
        if not live:
            log(f"#{rid} DRY RUN - would submit: {json.dumps(order)}   (yes book {bid}/{ask}, short {short})")
            continue

        result = mcp.call("polymarket_place_order", {"order": order})
        ok = isinstance(result, dict) and not result.get("error") and "error" not in json.dumps(result).lower()[:200]
        note = json.dumps(result)[:400]
        sb(env, "PATCH", f"trade_proposals?id=eq.{rid}", {
            "placed": bool(ok),
            "placed_at": datetime.now(timezone.utc).isoformat() if ok else None,
            "fill_note": ("submitted " + json.dumps(order) + " -> " + note) if ok else ("SUBMIT FAILED: " + note),
        })
        log(f"#{rid} {'PLACED' if ok else 'FAILED'}: {order['intent']} {order['quantity']} @ {order['price']['value']} -> {note[:160]}")



# ---- exits: approved positions no longer ride to resolution ------------------------------------------------
# Jaron 2026-09-16, after a week of manual trading: "sell into the spike; the resolution is not the exit. A human
# can't watch six positions; a script can." Defaults are CHOSEN (25 / 50, written as chosen on the card) and
# owner-editable per row. Same order path desk-trade.py --exit uses: SELL_LONG for yes at the bid; SELL_SHORT for
# no at the YES ask (economically a buy-back). One exit per row; the verifier reconciles the fill as usual.
def run_exits(env, live):
    mcp = Mcp()
    rows = sb(env, "GET", "trade_proposals?or=(verdict.eq.approved,and(verdict.eq.auto,decided_by.eq.deepseek-auto))&placed=eq.true&exit_placed_at=is.null&select=*")
    for row in rows:
        rid = row["id"]; slug = row["slug"]; side = row["side"]
        if slug_is_past(slug):
            continue
        entry = float(row.get("entry_price") or 0)
        tp = float(row.get("take_profit_pct") if row.get("take_profit_pct") is not None else 25)
        lg = float(row.get("let_go_pct") if row.get("let_go_pct") is not None else 50)
        if not entry:
            continue
        try:
            bid, ask, short = best_ask(mcp, slug)
        except Exception as e:
            log(f"#{rid} exit check: no book ({e})"); continue
        if bid is None or ask is None:
            continue
        # what our side would fetch now: yes -> sell at bid; no -> our short is worth (1 - ask)
        now = bid if side == "yes" else round(1 - ask, 4)
        px_exit = bid if side == "yes" else ask
        up = now >= entry * (1 + tp / 100)
        down = now <= entry * (1 - lg / 100)
        if not (up or down):
            continue
        why = f"take-profit {tp:.0f}%: {side} worth {now:.2f} vs entry {entry:.2f}" if up else f"let-go {lg:.0f}%: {side} worth {now:.2f} vs entry {entry:.2f}"
        shares = round(float(row.get("size_usd") or 0) / entry, 2)
        intent = "ORDER_INTENT_SELL_LONG" if side == "yes" else "ORDER_INTENT_SELL_SHORT"
        order = {"marketSlug": slug, "intent": intent, "type": "ORDER_TYPE_LIMIT",
                 "price": {"value": f"{px_exit:.2f}", "currency": "USD"}, "quantity": f"{shares:.2f}",
                 "tif": "TIME_IN_FORCE_GOOD_TILL_CANCEL"}
        if not live:
            log(f"#{rid} EXIT DRY RUN ({why}) - would submit: {json.dumps(order)}"); continue
        result = mcp.call("polymarket_place_order", {"order": order})
        ok = isinstance(result, dict) and not result.get("error") and "error" not in json.dumps(result).lower()[:200]
        note = json.dumps(result)[:300]
        sb(env, "PATCH", f"trade_proposals?id=eq.{rid}", {
            "exit_placed_at": datetime.now(timezone.utc).isoformat() if ok else None,
            "exit_note": (f"{why} -> submitted {json.dumps(order)} -> {note}") if ok else f"{why} -> EXIT FAILED: {note}"})
        log(f"#{rid} EXIT {'PLACED' if ok else 'FAILED'}: {why} | {order['intent']} {order['quantity']} @ {order['price']['value']} -> {note[:120]}")

def main():
    ap = argparse.ArgumentParser(description="Place approved, verified trade proposals. Dumb by design.")
    ap.add_argument("--live", action="store_true", help="actually submit orders (default is dry run)")
    ap.add_argument("--loop", type=int, metavar="SECONDS", help="poll repeatedly")
    a = ap.parse_args()
    env = secrets()
    for k in ("SUPABASE_URL", "SUPABASE_SERVICE_ROLE_KEY"):
        if not env.get(k):
            raise SystemExit(f"{k} missing from {SECRETS}")
    log(f"=== executor start | mode={'LIVE' if a.live else 'DRY RUN'} | loop={a.loop or 'once'} ===")
    while True:
        try:
            run_once(env, a.live)
            run_exits(env, a.live)
        except urllib.error.HTTPError as e:
            log(f"HTTP {e.code}: {e.read()[:200].decode('utf-8', 'replace')}")
        except Exception as e:
            log(f"error: {e}")
        if not a.loop:
            break
        time.sleep(a.loop)


if __name__ == "__main__":
    main()
