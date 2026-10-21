#!/usr/bin/env python3
"""
desk.py - read the Polymarket US account and markets from the MSI in one command. Read-only.

WHY
    Every AI with a shell on the MSI (Grok app, Grok Bots, Claude phone, ChatGPT via Desktop
    Commander) kept reaching for polymarket.com's public APIs - the WRONG venue. Our account and
    key are on Polymarket US (polymarket.us / api.polymarket.us). The key lives only on the MSI
    and is loaded by the local MCP on 127.0.0.1:8765. This command talks to that MCP so nobody
    needs the key, the JSON-RPC, or to know which site is which.

USAGE (PowerShell on the MSI, e.g. through the Heartbeat MCP or Desktop Commander)
    python C:\\Users\\lilli\\AI-Shared\\tools\\desk.py account          balance, buying power, positions, open orders
    python C:\\Users\\lilli\\AI-Shared\\tools\\desk.py book <slug>      live bid / ask / short quote / open interest
    python C:\\Users\\lilli\\AI-Shared\\tools\\desk.py market <slug>    question, outcomes, which side is "long", status
    python C:\\Users\\lilli\\AI-Shared\\tools\\desk.py search "<words>" find markets (each tagged tradeable / not)
    python C:\\Users\\lilli\\AI-Shared\\tools\\desk.py live             open markets whose game has started (Live Wire's list)
    python C:\\Users\\lilli\\AI-Shared\\tools\\desk.py history [n]      last n account events (fills, resolutions, deposits)
    python C:\\Users\\lilli\\AI-Shared\\tools\\desk.py queue            the trade desk: pending / approved / placed rows
    python C:\\Users\\lilli\\AI-Shared\\tools\\desk.py news "<topic>"   dated headlines (Google News RSS via the MCP)
    add --json to any command for the raw payload

TO TRADE: not here. Use tools/desk-trade.py (trail first, order second), or insert a
trade_proposals row and let the queue run. This file never places, cancels, funds, or withdraws.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import subprocess
from datetime import datetime, timezone

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

# `live` needs the polymarket_us client, which only the venv python has. Re-exec into it so a
# bare `python desk.py live` works from any shell (Grok hit this first, 2026-09-11 15:35).
_VENV_PY = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
                        "runtime", "polymarket-us-agent-venv", "Scripts", "python.exe")
if os.path.exists(_VENV_PY) and os.path.normcase(sys.executable) != os.path.normcase(_VENV_PY):
    try:
        import polymarket_us  # noqa: F401
    except ImportError:
        # Windows execv can detach from the calling tool's output/lifetime. Wait for
        # the child and propagate its exit code while inheriting stdout/stderr.
        raise SystemExit(subprocess.call([_VENV_PY] + sys.argv))

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
import verifier as V  # noqa: E402  (secrets, sb, Mcp)


def money(x):
    try:
        return f"${float(x):.2f}"
    except (TypeError, ValueError):
        return "-"


def cmd_account(m, env, raw):
    bal = m.call("polymarket_account_balances", {})
    pos = m.call("polymarket_positions", {})
    orders = m.call("polymarket_open_orders", {})
    if raw:
        print(json.dumps({"balances": bal, "positions": pos, "open_orders": orders}, indent=1)); return
    b = (bal.get("balances") or [{}])[0]
    print(f"available to trade {money(b.get('buyingPower'))}   (venue 'currentBalance' {money(b.get('currentBalance'))} includes deposits on hold)")
    pm = pos.get("positions") or {}
    print(f"positions: {len(pm)}")
    for slug, p in pm.items():
        md = p.get("marketMetadata") or {}
        sh = float(p.get("netPositionDecimal") or 0)
        print(f"  {'NO ' if sh < 0 else 'YES'} {abs(sh):7.2f} sh  {md.get('title','')[:42]:42} outcome={md.get('outcome','')[:18]:18} "
              f"avg {(p.get('avgPx') or {}).get('value')}  cost {money((p.get('cost') or {}).get('value'))}  now {money((p.get('cashValue') or {}).get('value'))}  [{slug}]")
    ol = orders.get("orders") or []
    print(f"open orders: {len(ol)}")
    for o in ol:
        print(f"  {o.get('intent')} {o.get('leavesQuantity')} @ {(o.get('price') or {}).get('value')} {o.get('marketSlug')} ({o.get('state')})")


def cmd_book(m, env, raw, slug):
    r = m.call("polymarket_bbo", {"slug": slug})
    if raw:
        print(json.dumps(r, indent=1)); return
    md = r.get("marketData") or {}
    g = lambda k: (md.get(k) or {}).get("value")
    print(f"{slug}\n  YES bid {g('bestBid')} / ask {g('bestAsk')}   buy NO costs {g('shortQuote')}   last {g('lastTradePx')}")
    print(f"  open interest {md.get('openInterest')}   depth bid {md.get('bidDepth')} / ask {md.get('askDepth')}   shares traded {md.get('sharesTraded')}")


def cmd_market(m, env, raw, slug):
    r = m.call("polymarket_market", {"slug": slug})
    mk = r.get("market") or r
    if raw:
        print(json.dumps(mk, indent=1)); return
    long_side = next((sd.get("description") for sd in mk.get("marketSides", []) if sd.get("long")), None)
    print(f"{mk.get('question')}  —  {mk.get('title') or ''}")
    print(f"  slug {mk.get('slug')} | category {mk.get('category')} | type {mk.get('sportsMarketType') or mk.get('marketType')}")
    print(f"  outcomes {mk.get('outcomes')} | LONG side (what you buy at the ask) = {long_side}")
    print(f"  active {mk.get('active')} closed {mk.get('closed')} | game start {mk.get('gameStartTime')} | ends {mk.get('endDate')}")
    print(f"  app: https://polymarket.us/event/<event>  (search the title in the app if unsure)")
    d = (mk.get("description") or "").strip()
    if d:
        print("  rules: " + d[:600].replace("\n", " "))


def cmd_search(m, env, raw, q):
    r = m.call("polymarket_search", {"query": q})
    if raw:
        print(json.dumps(r, indent=1)); return
    n = 0
    for ev in (r.get("events") or []):
        for mk in ev.get("markets") or []:
            n += 1
            b = (mk.get("bestBidQuote") or {}).get("value"); a = (mk.get("bestAskQuote") or {}).get("value")
            print(f"  {'ok ' if mk.get('tradeable') else 'NO '} {mk.get('slug'):50} {str(mk.get('question') or ev.get('title'))[:40]:40} bid {b} ask {a} {'' if mk.get('tradeable') else '(' + str(mk.get('tradeable_reason')) + ')'}")
            if n >= 40:
                print("  ..."); return
    if n == 0:
        print("  nothing found")


def cmd_live(m, env, raw):
    from importlib import import_module
    try:
        P = import_module("proposer")
        ms = P.fetch_open_markets()
    except Exception as e:
        print(f"needs the polymarket-us venv python ({e})"); return
    now = datetime.now(timezone.utc)
    out = []
    for mk in ms:
        gs = mk.get("gameStartTime")
        if not gs or mk.get("closed"):
            continue
        try:
            hrs_ago = (now - datetime.fromisoformat(gs.replace("Z", "+00:00"))).total_seconds() / 3600
        except ValueError:
            continue
        # a game is "in progress" if it started in the last 8 hours. Futures carry a gameStartTime
        # months in the past (NFL 2027 showed up as "started") - those are not live games.
        started = 0 <= hrs_ago <= 8
        b = (mk.get("bestBidQuote") or {}).get("value"); a = (mk.get("bestAskQuote") or {}).get("value")
        if started and b and a:
            out.append((gs, mk["slug"], mk.get("question"), b, a))
    if raw:
        print(json.dumps(out, indent=1)); return
    print(f"{len(out)} markets with a game in progress (started ≤ now, still open):")
    for gs, slug, q, b, a in sorted(out, reverse=True)[:40]:
        print(f"  started {gs[11:16]}Z  {slug:48} {str(q)[:38]:38} {b}/{a}")


def cmd_history(m, env, raw, n):
    r = m.call("polymarket_activities", {"limit": n})
    if raw:
        print(json.dumps(r, indent=1)); return
    for a in r.get("activities") or []:
        t = a.get("type", "")
        if t == "ACTIVITY_TYPE_TRADE":
            tr = a["trade"]  # both sides are present; ours is the aggressor only when isAggressor is true
            ex = tr["aggressorExecution"] if tr.get("isAggressor") else tr["passiveExecution"]; o = ex["order"]
            who = "manual (app)" if o.get("manualOrderIndicator", "").endswith("MANUAL") else "api (automatic)"
            print(f"  {ex.get('transactTime','')[:16]} FILL {o.get('intent'):22} {ex.get('lastShares')} @ {ex.get('lastPx',{}).get('value')}  {o.get('marketMetadata',{}).get('title','')[:36]:36} {who}")
        elif t == "ACTIVITY_TYPE_POSITION_RESOLUTION":
            pr = a["positionResolution"]; md = (pr.get("afterPosition") or {}).get("marketMetadata") or {}
            print(f"  {pr.get('updateTime','')[:16]} RESOLVED {md.get('title','')[:40]:40} realized {(pr.get('afterPosition') or {}).get('realized',{}).get('value')}")
        elif "DEPOSIT" in t or "WITHDRAW" in t:
            c = a.get("accountBalanceChange") or {}
            print(f"  {c.get('createTime','')[:16]} {t.replace('ACTIVITY_TYPE_ACCOUNT_','')} {money((c.get('amount') or {}).get('value'))} {c.get('status','').replace('ACCOUNT_BALANCE_CHANGE_STATUS_','').lower()}")


def cmd_queue(m, env, raw):
    rows = V.sb(env, "GET", "trade_proposals?select=id,slug,question,side,entry_price,size_usd,edge,verdict,verification,placed,proposed_by,proposed_at&order=id.desc&limit=40")
    if raw:
        print(json.dumps(rows, indent=1)); return
    for r in rows:
        print(f"  #{r['id']:<3} {r['verdict']:8} {('verified' if r['verification']=='match' else (r['verification'] or 'unverified')):10} {'PLACED' if r['placed'] else '      '} "
              f"{r['side']:3} @ {float(r['entry_price'] or 0):.2f} ${float(r['size_usd'] or 0):.2f} edge {float(r['edge'] or 0):+.2f}  {str(r['question'])[:44]:44} by {r['proposed_by']}")
    print("  approve at https://www.heartbeatobservatory.com/live-systems/trades/")


def cmd_news(m, env, raw, topic):
    r = m.call("research_news", {"query": topic, "limit": 10})
    print(json.dumps(r, indent=1) if raw else (r if isinstance(r, str) else json.dumps(r, indent=1)))


def main():
    ap = argparse.ArgumentParser(description="Read the Polymarket US desk from the MSI. Read-only.")
    ap.add_argument("cmd", choices=["account", "book", "market", "search", "live", "history", "queue", "news", "usage", "rules"])
    ap.add_argument("arg", nargs="?", help="slug / query / count")
    ap.add_argument("--json", action="store_true", help="raw payload")
    a = ap.parse_args()
    if a.cmd == "usage":
        import runpy
        runpy.run_path(os.path.join(os.path.dirname(os.path.realpath(__file__)), "usage.py"), run_name="__main__"); return
    if a.cmd == "rules":   # no network to Polymarket needed: just the Control Room schedule, in plain words
        import desk_schedule as DS
        sched = DS.load()
        if not sched:
            print("DESK RULES: the schedule could not be read from the Control Room right now, so no hours are enforced. Trade as usual; desk-trade.py still applies its other caps."); return
        print(json.dumps(sched, indent=1) if a.json else DS.rules_text(sched, DS.local_now(sched))); return
    env = V.secrets()
    m = V.Mcp()
    if a.cmd == "account": cmd_account(m, env, a.json)
    elif a.cmd == "book": cmd_book(m, env, a.json, a.arg or sys.exit("book needs a slug"))
    elif a.cmd == "market": cmd_market(m, env, a.json, a.arg or sys.exit("market needs a slug"))
    elif a.cmd == "search": cmd_search(m, env, a.json, a.arg or sys.exit("search needs words"))
    elif a.cmd == "live": cmd_live(m, env, a.json)
    elif a.cmd == "history": cmd_history(m, env, a.json, int(a.arg or 20))
    elif a.cmd == "queue": cmd_queue(m, env, a.json)
    elif a.cmd == "news": cmd_news(m, env, a.json, a.arg or sys.exit("news needs a topic"))


if __name__ == "__main__":
    main()
