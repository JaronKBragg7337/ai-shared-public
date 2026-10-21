#!/usr/bin/env python3
"""
verifier.py - the second reflex. Checks a proposal's NUMBERS, not its reasoning.

JARON'S DESIGN, 2026-09-10 late:
    "Can we do both? Scripts going, AND things that can get smart and make decisions,
    while the dumb fast things keep going."
    Yes. This is a dumb fast thing. Scout/Bridge are the things that get smart.

WHAT IT CHECKS, on every proposal with verification IS NULL
    1. Re-reads the live order book through the local MCP (a different route from Bridge,
       which reaches the MSI through the Cloudflare tunnel and PowerShell).
    2. Bid and ask must be within TOLERANCE of what the proposal claims. If Bridge said
       0.09/0.10 and the book says 0.09/0.10 - match. If the book says 0.12/0.15 - mismatch.
    3. Edge is recomputed from Scout's number minus the live ask, and must still beat the
       spread. A proposal whose edge died between proposing and verifying is a mismatch.
    4. The market must still have a book at all.
    Nothing else. It does not ask whether Scout's probability is RIGHT - only a smarter thing
    can do that, and Claude Code still does it when asked. This script is the fast floor
    under that: numbers are real, current, and still add up.

WHAT IT WRITES
    verification = 'match' | 'mismatch', verified_by = 'verifier-script', verified_at,
    verified_bid, verified_ask, verification_note (why). The website shows all of it, and
    executor.py acts only on 'match'.

A mismatch is never final. Bridge can re-propose with fresh numbers and the new row gets
checked again. The old row stays as history.

USAGE
    python tools/verifier.py            # once
    python tools/verifier.py --loop 300 # every 5 minutes, forever
"""

from __future__ import annotations

import argparse
import json
import os
import re
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
TOLERANCE = 0.01      # bid/ask may differ from the claim by at most 1c
LOG = os.path.join(ROOT, "state", "verifier.md")


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
    if os.path.exists(SECRETS):
        with open(SECRETS, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if "=" in line and not line.startswith("#"):
                    k, v = line.split("=", 1)
                    out[k.strip()] = v.strip().strip('"').strip("'")
    return out


def sb(env, method, path, body=None, upsert=False):
    url = f"{env['SUPABASE_URL'].rstrip('/')}/rest/v1/{path}"
    key = env["SUPABASE_SERVICE_ROLE_KEY"]
    prefer = "return=representation" + (",resolution=merge-duplicates" if upsert else "")
    req = urllib.request.Request(
        url, data=json.dumps(body).encode() if body is not None else None, method=method,
        headers={"apikey": key, "Authorization": f"Bearer {key}",
                 "Content-Type": "application/json", "Prefer": prefer})
    with urllib.request.urlopen(req, timeout=45) as r:
        raw = r.read()
        return json.loads(raw) if raw else []


class Mcp:
    def __init__(self):
        self.sid = None
        self._rpc({"jsonrpc": "2.0", "id": 1, "method": "initialize",
                   "params": {"protocolVersion": "2025-06-18", "capabilities": {},
                              "clientInfo": {"name": "verifier", "version": "1"}}})

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


def book(mcp, slug):
    r = mcp.call("polymarket_bbo", {"slug": slug})
    md = r.get("marketData", {}) if isinstance(r, dict) else {}
    ask = (md.get("bestAsk") or {}).get("value")
    bid = (md.get("bestBid") or {}).get("value")
    return (float(bid) if bid else None), (float(ask) if ask else None)


def f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def check(row, bid, ask):
    """Return (verdict, note). Pure arithmetic - no judgement about the research."""
    problems = []
    if ask is None or bid is None:
        return "mismatch", "no live book (bid or ask missing) - market may be closed or never traded"
    cb, ca = f(row.get("bid")), f(row.get("ask"))
    if cb is not None and abs(cb - bid) > TOLERANCE:
        problems.append(f"bid claimed {cb:.2f}, live {bid:.2f}")
    if ca is not None and abs(ca - ask) > TOLERANCE:
        problems.append(f"ask claimed {ca:.2f}, live {ask:.2f}")
    p = f(row.get("scout_probability"))
    spread = ask - bid
    if row.get("side_open"):
        # owner picks the side (politics / AI / chips): the edge is not the gate, Jaron is. Only the book is checked.
        if problems:
            return "mismatch", "; ".join(problems)
        return "match", f"live book {bid:.2f}/{ask:.2f} agrees with claim; side open - owner decides, edge not gated"
    if p is None:
        problems.append("no scout_probability on the row - cannot recompute edge")
    else:
        # yes: pay the ask, edge = p - ask.   no: pay (1 - bid), edge = (1 - p) - (1 - bid) = bid - p
        edge = (p - ask) if row.get("side") == "yes" else (bid - p)
        if edge <= spread:
            problems.append(f"edge {edge:.3f} does not beat spread {spread:.3f} on the live book")
    if problems:
        return "mismatch", "; ".join(problems)
    return "match", f"live book {bid:.2f}/{ask:.2f} agrees with claim; edge still beats spread {spread:.2f}"


def snapshot_account(env, mcp):
    """Publish balance / positions / open orders to desk_account so the trades page can show
    them (Jaron 2026-09-11: the Qwen page had the account, the trades page did not; one page for
    every proposer). Identity fields are never copied - numbers and market titles only."""
    try:
        bal = mcp.call("polymarket_account_balances", {})
        pos = mcp.call("polymarket_positions", {})
        orders = mcp.call("polymarket_open_orders", {})
    except Exception as e:
        log(f"account snapshot skipped: {e}")
        return
    b = (bal.get("balances") or [{}])[0] if isinstance(bal, dict) else {}
    plist = []
    pmap = pos.get("positions") if isinstance(pos, dict) else None
    for slug, p in (pmap or {}).items() if isinstance(pmap, dict) else []:
        md = p.get("marketMetadata") or {}
        plist.append({"slug": slug, "title": md.get("title"), "outcome": md.get("outcome"),
                      "shares": p.get("netPositionDecimal") or p.get("netPosition"),
                      "avg_px": (p.get("avgPx") or {}).get("value"),
                      "cost": (p.get("cost") or {}).get("value"),
                      "value": (p.get("cashValue") or {}).get("value"),
                      "realized": (p.get("realized") or {}).get("value")})
    olist = []
    oraw = orders.get("orders") if isinstance(orders, dict) else None
    for o in (oraw or []) if isinstance(oraw, list) else []:
        md = o.get("marketMetadata") or {}
        olist.append({"slug": o.get("marketSlug"), "title": md.get("title"), "intent": o.get("intent"),
                      "price": (o.get("price") or {}).get("value"), "quantity": o.get("leavesQuantity") or o.get("quantity"),
                      "state": o.get("state")})
    sb(env, "POST", "desk_account?on_conflict=id", {
        "id": "polymarket-us", "balance_usd": b.get("currentBalance"), "buying_power": b.get("buyingPower"),
        "positions": plist, "open_orders": olist, "positions_count": len(plist), "open_orders_count": len(olist),
        "source": "verifier.py via local MCP", "updated_at": datetime.now(timezone.utc).isoformat(),
    }, upsert=True)


def _f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None



# Windows Jaron has declared as "demo" (showing friends Polymarket, not the system). Fills in these windows are lane
# "jaron-manual (demo)" and their resolutions follow (a resolution inherits its fills' lane). Add a window here, never
# by hand-editing rows: the verifier rewrites actors on every pass. UTC ISO bounds, [start, end).
DEMO_WINDOWS = [("2026-09-14T00:00:00", "2026-09-14T06:00:00")]   # Sat night 8 PM-2 AM ET, Jaron 2026-09-14 06:35


def manual_lane(at):
    a = (at or "")[:19]
    return "jaron-manual (demo)" if any(s <= a < e for s, e in DEMO_WINDOWS) else "jaron-manual"

def reconcile_trades(env, mcp):
    """Write every account event to desk_trades, labelled by WHO did it.

    Jaron 2026-09-11: "if I make a play it should be recorded ... if it wasn't proposed to be
    approved then it automatically knows it was me. It should also be reflected on the website."
    He was right, and the venue agrees: every order carries manualOrderIndicator. His app orders
    are MANUAL_ORDER_INDICATOR_MANUAL; everything the executor sends is _AUTOMATIC. So:
        system           = the order id is in a trade_proposals fill_note (went through the queue)
        jaron-manual     = MANUAL (the app)
        ai-outside-queue = AUTOMATIC but no proposal behind it (an AI traded without approval)
        unknown          = anything else - visible, never hidden
    Which execution is ours: the one whose order id we know; else the aggressor (both the app
    and the executor send marketable limits). The passive side is the counterparty."""
    try:
        acts = mcp.call("polymarket_activities", {"limit": 100}).get("activities") or []
    except Exception as e:
        log(f"reconcile skipped: {e}")
        return
    props = sb(env, "GET", "trade_proposals?select=id,slug,fill_note,verdict,proposed_by&placed=eq.true")
    order_to_prop, prop_actor = {}, {}
    for pr in props:
        m = re.search(r'"id":\s*"([A-Z0-9]{8,})"', pr.get("fill_note") or "")
        if m:
            order_to_prop[m.group(1)] = pr["id"]
            # verdict 'auto' = a live agent traded on its own judgement via desk-trade.py
            # (no approval, but a full trail). Label it with the agent's name, not 'system'.
            prop_actor[pr["id"]] = (f"auto:{pr.get('proposed_by') or 'unknown'}" if pr.get("verdict") == "auto" else "system")
    # Claims: a live agent that traded in ITS OWN BROWSER on Jaron's login (venue stamps MANUAL)
    # can claim the fill by appending one JSON line to state/agent-claims.jsonl:
    #   {"by":"grok-bot/live-wire","slug":"<slug>","at":"<ISO UTC when placed>","why":"..."}
    # A MANUAL fill on that slug within 15 minutes of `at` is labelled auto:<by>, not jaron-manual.
    # Jaron 2026-09-11 20:40: eyes on the bot's computer, hands preferably on the MSI, but never
    # let a browser trade get credited to him by accident.
    claims = []
    cpath = os.path.join(ROOT, "state", "agent-claims.jsonl")
    if os.path.exists(cpath):
        for line in open(cpath, encoding="utf-8", errors="replace"):
            line = line.strip()
            if line:
                try:
                    c = json.loads(line)
                    c["_at"] = datetime.fromisoformat(str(c["at"]).replace("Z", "+00:00"))
                    claims.append(c)
                except Exception:
                    pass

    def claimed_by(slug, when_iso):
        try:
            t = datetime.fromisoformat(str(when_iso).replace("Z", "+00:00"))
        except Exception:
            return None
        for c in claims:
            if c.get("slug") == slug and abs((t - c["_at"]).total_seconds()) <= 900:
                return f"auto:{c.get('by', 'unknown')}"
        return None

    rows, fills_by_slug = [], {}
    # fills first so a resolution in the same batch can inherit its actor from them
    acts = sorted(acts, key=lambda a: 0 if a.get("type") == "ACTIVITY_TYPE_TRADE" else 1)
    for a in acts:
        t = a.get("type", "")
        if t == "ACTIVITY_TYPE_TRADE":
            tr = a["trade"]
            execs = [tr.get("aggressorExecution"), tr.get("passiveExecution")]
            ours = next((e for e in execs if e and e.get("order", {}).get("id") in order_to_prop), None)                    or (tr.get("aggressorExecution") if tr.get("isAggressor", True) else tr.get("passiveExecution")) or execs[0]   # our side = aggressor only when we were the aggressor (resting orders are passive; fixed 10/12)
            if not ours:
                continue
            o = ours.get("order", {})
            order_action = o.get("action", "")
            action = ("buy" if order_action == "ORDER_ACTION_BUY" else
                      "sell" if order_action == "ORDER_ACTION_SELL" else None)
            if action is None:
                intent = o.get("intent", "")
                action = ("buy" if intent in ("ORDER_INTENT_BUY_LONG", "ORDER_INTENT_BUY_SHORT") else
                          "sell" if intent in ("ORDER_INTENT_SELL_LONG", "ORDER_INTENT_SELL_SHORT") else None)
            md = o.get("marketMetadata") or {}
            px = _f((ours.get("lastPx") or {}).get("value"))
            qty = _f(ours.get("lastShares"))
            no_side = o.get("outcomeSide") == "OUTCOME_SIDE_NO"
            cost_each = (1 - px) if (no_side and px is not None) else px
            fee = _f((ours.get("commissionNotionalCollected") or {}).get("value")) or 0.0
            ind = o.get("manualOrderIndicator", "")
            if o.get("id") in order_to_prop:
                actor = prop_actor.get(order_to_prop[o.get("id")], "system")
            elif ind.endswith("_MANUAL"):
                actor = claimed_by(o.get("marketSlug"), ours.get("transactTime")) or manual_lane(ours.get("transactTime"))
            elif ind.endswith("_AUTOMATIC"):
                # An API order with NO proposal behind it: some AI traded outside the approve
                # queue (Claude on the phone, the Grok app, Bridge by hand...). Jaron's point
                # exactly - it must show, and it must not be dressed up as 'system'.
                actor = "ai-outside-queue"
            else:
                actor = "unknown"
            row = {"id": tr["id"], "kind": "fill", "at": ours.get("transactTime"),
                   "slug": o.get("marketSlug"), "title": md.get("title"), "outcome": md.get("outcome"),
                   "side": "no" if no_side else "yes", "price": round(cost_each, 4) if cost_each is not None else None,
                   "action": action,
                   "quantity": qty, "cost_usd": round(cost_each * qty + (fee if action != "sell" else -fee), 4)
                   if (cost_each is not None and qty) else None,
                   "actor": actor, "proposal_id": order_to_prop.get(o.get("id")), "order_id": o.get("id"),
                   "note": f"{o.get('intent')} limit {(o.get('price') or {}).get('value')} · {ind.replace('MANUAL_ORDER_INDICATOR_', '').lower()} · fee {fee:.2f}"}
            rows.append(row)
            fills_by_slug.setdefault(row["slug"], set()).add(actor)
        elif t == "ACTIVITY_TYPE_POSITION_RESOLUTION":
            pr = a["positionResolution"]
            after = pr.get("afterPosition") or {}
            md = after.get("marketMetadata") or (pr.get("beforePosition") or {}).get("marketMetadata") or {}
            slug = pr.get("marketSlug")
            actors = fills_by_slug.get(slug) or {r["actor"] for r in sb(env, "GET", f"desk_trades?select=actor&slug=eq.{slug}&kind=eq.fill")}
            actor = next(iter(actors)) if len(actors) == 1 else ("mixed" if actors else "unknown")
            rows.append({"id": f"res-{slug}-{pr.get('updateTime', '')[:19]}", "kind": "resolution", "at": pr.get("updateTime"),
                         "slug": slug, "title": md.get("title"), "outcome": md.get("outcome"), "side": None,
                         "price": None, "quantity": _f((pr.get("beforePosition") or {}).get("netPositionDecimal")),
                         "cost_usd": _f(((pr.get("beforePosition") or {}).get("cost") or {}).get("value")),
                         "pnl_usd": _f((after.get("realized") or {}).get("value")), "actor": actor,
                         "note": f"resolved; realized {(after.get('realized') or {}).get('value')}"})
        elif t in ("ACTIVITY_TYPE_ACCOUNT_DEPOSIT", "ACTIVITY_TYPE_ACCOUNT_WITHDRAWAL"):
            c = a.get("accountBalanceChange") or {}
            rows.append({"id": f"bal-{c.get('transactionId')}", "kind": "deposit" if "DEPOSIT" in t else "withdrawal",
                         "at": c.get("createTime"), "cost_usd": _f((c.get("amount") or {}).get("value")),
                         "actor": "jaron-manual", "note": (c.get("status") or "").replace("ACCOUNT_BALANCE_CHANGE_STATUS_", "").lower()})
    if rows:
        # PostgREST bulk upsert needs identical key sets on every object
        cols = ("id", "kind", "at", "slug", "title", "outcome", "side", "action", "price", "quantity",
                "cost_usd", "pnl_usd", "actor", "proposal_id", "order_id", "note")
        rows = [{c: r.get(c) for c in cols} for r in rows]
        sb(env, "POST", "desk_trades?on_conflict=id", rows, upsert=True)
        manual = sum(1 for r in rows if r["kind"] == "fill" and r["actor"] == "jaron-manual")
        system = sum(1 for r in rows if r["kind"] == "fill" and r["actor"] == "system")
        log(f"reconciled {len(rows)} account events: fills system={system} manual={manual}")


def run_once(env):
    mcp = Mcp()
    snapshot_account(env, mcp)
    reconcile_trades(env, mcp)
    rows = sb(env, "GET", "trade_proposals?verification=is.null&verdict=eq.pending&select=*")
    if not rows:
        log("nothing to verify")
        return
    for row in rows:
        rid = row["id"]
        try:
            bid, ask = book(mcp, row["slug"])
        except Exception as e:
            log(f"#{rid} {row['slug']}: book read failed ({e}) - leaving unverified for next cycle")
            continue
        if bid is None and ask is None:
            # Venue down (maintenance 2026-09-11 04:00-07:00 ET) or market not quoting: that is
            # not a mismatch, it is "not now". Leave it unverified and try again in 5 minutes.
            log(f"#{rid} {row['slug']}: no book at all - venue quiet? leaving unverified")
            continue
        verdict, note = check(row, bid, ask)
        sb(env, "PATCH", f"trade_proposals?id=eq.{rid}", {
            "verification": verdict,
            "verified_by": "verifier-script",
            "verified_at": datetime.now(timezone.utc).isoformat(),
            "verified_bid": bid, "verified_ask": ask,
            "verification_note": note,
        })
        log(f"#{rid} {row['slug']} {row.get('side')} -> {verdict.upper()}: {note}")
        if str(row.get("proposed_by") or "").startswith("proposer-script"):
            if verdict == "match":
                auto_approve(env, row)
            else:
                # 2026-09-25 (Jaron: no approve buttons anywhere): a DeepSeek row that fails its check is closed, not parked
                # in a queue for a human. The proposer re-proposes with fresh numbers if the edge is still there.
                close_row(env, row, f"verifier: {note} - closed, no human queue")


# 2026-09-24 (Jaron): no human approvals. Any AI whose provider allows it may trade, and DeepSeek's terms do. So a DeepSeek
# proposal whose numbers the verifier just confirmed is decided by DeepSeek itself: verdict 'auto', decided_by 'deepseek-auto',
# and the executor places it. Structure, not caution: a daily budget keeps DeepSeek from spending Live Wire's buying power.
import sys as _sys, os as _os
_sys.path.insert(0, _os.path.dirname(_os.path.realpath(__file__)))
from settings import setting  # Control Room values (/admin/control/), built-in default if unreachable
DEEPSEEK_DAILY_BUDGET_USD = setting("deepseek_daily_budget_usd", 10.0)   # change freely; Jaron's call


MAX_DAYS_TO_SETTLE = setting("max_days_to_settle", 14)   # Jaron 2026-09-25; same number as desk-trade.py and proposer.py


def settles_too_late(row):
    s = row.get("settles_at")
    try:
        when = datetime.fromisoformat(str(s).replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return False
    if when.tzinfo is None:
        when = when.replace(tzinfo=timezone.utc)
    return (when - datetime.now(timezone.utc)).total_seconds() > MAX_DAYS_TO_SETTLE * 86400


def close_row(env, row, why):
    sb(env, "PATCH", f"trade_proposals?id=eq.{row['id']}&verdict=eq.pending", {
        "verdict": "expired", "decided_by": "deepseek-closed", "decided_at": datetime.now(timezone.utc).isoformat(),
        "decision_note": why})
    log(f"#{row['id']} CLOSED: {why}")


def auto_approve(env, row):
    today = datetime.now().astimezone().strftime("%Y-%m-%d")
    spent_rows = sb(env, "GET", "trade_proposals?select=size_usd,decided_at&decided_by=eq.deepseek-auto")
    spent = sum(float(r.get("size_usd") or 0) for r in spent_rows
                if (r.get("decided_at") or "").startswith(today) or
                   (r.get("decided_at") and datetime.fromisoformat(r["decided_at"].replace("Z", "+00:00")).astimezone().strftime("%Y-%m-%d") == today))
    size = float(row.get("size_usd") or 0)
    if spent + size > DEEPSEEK_DAILY_BUDGET_USD:
        # 2026-09-25: used to be "left pending", which built a queue Bridge then announced as "approve at...". No queue.
        close_row(env, row, f"DeepSeek's ${DEEPSEEK_DAILY_BUDGET_USD:.0f}/day budget was used (${spent:.2f} today) - closed, not queued")
        return
    if settles_too_late(row):
        close_row(env, row, f"settles {str(row.get('settles_at'))[:10]}, more than {MAX_DAYS_TO_SETTLE} days out - Polymarket is short-term")
        return
    sb(env, "PATCH", f"trade_proposals?id=eq.{row['id']}&verdict=eq.pending", {
        "verdict": "auto", "decided_by": "deepseek-auto", "decided_at": datetime.now(timezone.utc).isoformat(),
        "decision_note": f"DeepSeek trades on its own (no human approval, 2026-09-24). Budget ${spent + size:.2f} of ${DEEPSEEK_DAILY_BUDGET_USD:.0f} today.",
    })
    log(f"#{row['id']} AUTO-APPROVED for DeepSeek: ${size:.2f} (today ${spent + size:.2f}/{DEEPSEEK_DAILY_BUDGET_USD:.0f})")


def main():
    ap = argparse.ArgumentParser(description="Verify the numbers on pending trade proposals. Dumb by design.")
    ap.add_argument("--loop", type=int, metavar="SECONDS", help="poll repeatedly")
    a = ap.parse_args()
    env = secrets()
    for k in ("SUPABASE_URL", "SUPABASE_SERVICE_ROLE_KEY"):
        if not env.get(k):
            raise SystemExit(f"{k} missing from {SECRETS}")
    log(f"=== verifier start | loop={a.loop or 'once'} ===")
    while True:
        failed = False
        try:
            run_once(env)
        except urllib.error.HTTPError as e:
            log(f"HTTP {e.code}: {e.read()[:200].decode('utf-8', 'replace')}")
            failed = True
        except Exception as e:
            log(f"error: {e}")
            failed = True
        if not a.loop:
            if failed:
                raise SystemExit(1)
            break
        time.sleep(a.loop)


if __name__ == "__main__":
    main()
