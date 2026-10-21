#!/usr/bin/env python3
"""
paper-sync.py — mirror the PAPER trading account into Supabase so Jaron can watch
it from his phone, the same way /qwen shows the live one.

FAKE MONEY ONLY. This reads tools/paper-trader/data/default/paper.db, which is a
local SQLite simulator settling fills against live Polymarket order books. It holds
no credentials and cannot reach the real account.

WHY IT EXISTS
    Jaron: "I don't think I can decide anything until after I see how it would fully
    run in all aspects." Watching it only from the desk defeats that - the whole point
    is seeing it behave while he is away from the computer.

SEPARATION IS THE POINT
    Everything here writes to paper_* tables, never desk_* or qwen_*. A test reading
    must never be mistakable for the live account. If you are extending this and find
    yourself writing to a non-paper table, stop.

    It also NEVER writes back to paper.db. Read-only against the simulator, so it can
    never disturb a run in progress.

USAGE
    python tools/paper-sync.py            # one sync
    python tools/paper-sync.py --loop 60  # every 60s until stopped
"""

from __future__ import annotations

import argparse
import json
import os
import sqlite3
import subprocess
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
PAPER_DB = os.path.join(ROOT, "tools", "paper-trader", "data", "default", "paper.db")
SECRETS = os.path.join(os.path.expanduser("~"), ".secrets", "keys.env")
CLOB = "https://clob.polymarket.com"


def log(m):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {m}", flush=True)


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


def sb(env, method, path, body=None, prefer="resolution=merge-duplicates"):
    url = f"{env['SUPABASE_URL'].rstrip('/')}/rest/v1/{path}"
    key = env["SUPABASE_SERVICE_ROLE_KEY"]
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode() if body is not None else None,
        method=method,
        headers={"apikey": key, "Authorization": f"Bearer {key}",
                 "Content-Type": "application/json", "Prefer": prefer},
    )
    with urllib.request.urlopen(req, timeout=45) as r:
        raw = r.read()
        return json.loads(raw) if raw else []


def portfolio_from_cli():
    """Ask pm-trader for the portfolio instead of pricing positions ourselves.

    The first version of this file looked up midpoints by token_id - but the
    positions table has no token_id, so every lookup silently fell back to entry
    price and the dashboard reported P&L of exactly $0.00 while the real figure
    was -$5.11. A number that is confidently wrong is worse than a missing one.

    pm-trader already resolves live prices and computes unrealized P&L. Use it.
    Returns None if the call fails, and the caller falls back to cost basis and
    SAYS SO rather than pretending.
    """
    exe = os.path.join(ROOT, "tools", "paper-trader", ".venv", "Scripts", "pm-trader.exe")
    if not os.path.exists(exe):
        return None
    env = dict(os.environ)
    env["PM_TRADER_HOME"] = os.path.join(ROOT, "tools", "paper-trader", "data")
    try:
        r = subprocess.run([exe, "portfolio"], capture_output=True, text=True, timeout=180, env=env)
        d = json.loads(r.stdout)
        return d.get("data") if d.get("ok") else None
    except Exception:
        return None


def sync(env) -> dict:
    if not os.path.exists(PAPER_DB):
        raise SystemExit(f"paper.db not found at {PAPER_DB} - has the paper account been created?")

    # read-only connection: this must never modify the simulator
    con = sqlite3.connect(f"file:{PAPER_DB}?mode=ro", uri=True)
    con.row_factory = sqlite3.Row

    acct = dict(con.execute("select * from account limit 1").fetchone() or {})
    positions = [dict(r) for r in con.execute("select * from positions")]
    trades = [dict(r) for r in con.execute("select * from trades order by id desc limit 200")]
    con.close()

    # Value open positions at live midpoints where we can get them, falling back to
    # entry price. Falling back is stated in the row rather than hidden, so a stale
    # price never silently reads as a real one.
    live = portfolio_from_cli()
    priced_live = live is not None
    by_key = {}
    if priced_live:
        for row in live:
            by_key[(row.get("market_slug"), row.get("outcome"))] = row

    pos_rows, positions_value = [], 0.0
    for p in positions:
        shares = float(p.get("shares") or 0)
        entry = float(p.get("avg_entry_price") or 0)
        cost = float(p.get("total_cost") or 0)
        lr = by_key.get((p.get("market_slug"), p.get("outcome")))
        if lr:
            priced = float(lr.get("live_price") or entry)
            value = float(lr.get("current_value") or shares * priced)
            upnl = float(lr.get("unrealized_pnl") or (value - cost))
        else:
            priced, value, upnl = entry, cost, 0.0
        positions_value += value
        pos_rows.append({
            "market_condition_id": p.get("market_condition_id"),
            "outcome": p.get("outcome"),
            "market_question": p.get("market_question"),
            "market_slug": p.get("market_slug"),
            "shares": shares,
            "avg_entry_price": entry,
            "total_cost": cost,
            "current_price": priced,
            "current_value": round(value, 6),
            "unrealized_pnl": round(upnl, 6),
            "synced_at": datetime.now(timezone.utc).isoformat(),
        })

    cash = float(acct.get("cash") or 0)
    start = float(acct.get("starting_balance") or 0)
    total = cash + positions_value

    state = {
        "id": "current",
        "starting_balance": start,
        "cash": cash,
        "positions_value": round(positions_value, 6),
        "total_value": round(total, 6),
        "pnl": round(total - start, 6),
        "open_positions": len(pos_rows),
        "trade_count": len(trades),
        "synced_at": datetime.now(timezone.utc).isoformat(),
        "note": ("PAPER TRADING - simulated money, live Polymarket prices" if priced_live
                 else "PAPER TRADING - LIVE PRICING UNAVAILABLE, positions shown at cost basis"),
    }

    sb(env, "POST", "paper_state", state)
    sb(env, "DELETE", "paper_positions?market_condition_id=neq.__none__", prefer="return=minimal")
    if pos_rows:
        sb(env, "POST", "paper_positions", pos_rows)

    if trades:
        sb(env, "POST", "paper_trades", [{
            "id": t.get("id"),
            "market_condition_id": t.get("market_condition_id"),
            "market_question": t.get("market_question"),
            "market_slug": t.get("market_slug"),
            "outcome": t.get("outcome"),
            "side": t.get("side"),
            "order_type": t.get("order_type"),
            "avg_price": t.get("avg_price"),
            "amount_usd": t.get("amount_usd"),
            "shares": t.get("shares"),
            "slippage": t.get("slippage"),
            "levels_filled": t.get("levels_filled"),
            "is_partial": bool(t.get("is_partial")),
            "created_at": t.get("created_at"),
            "synced_at": datetime.now(timezone.utc).isoformat(),
        } for t in trades])

    return state


def main():
    ap = argparse.ArgumentParser(description="Mirror the paper trading account to Supabase.")
    ap.add_argument("--loop", type=int, metavar="SECONDS",
                    help="sync repeatedly every N seconds instead of once")
    a = ap.parse_args()

    env = secrets()
    for k in ("SUPABASE_URL", "SUPABASE_SERVICE_ROLE_KEY"):
        if not env.get(k):
            raise SystemExit(f"{k} missing from {SECRETS}")

    while True:
        try:
            s = sync(env)
            log(f"synced: cash ${s['cash']:,.2f} | positions ${s['positions_value']:,.2f} "
                f"| total ${s['total_value']:,.2f} | P&L ${s['pnl']:+,.2f} "
                f"| {s['open_positions']} open, {s['trade_count']} trades")
        except urllib.error.HTTPError as e:
            log(f"HTTP {e.code}: {e.read()[:200].decode('utf-8', 'replace')}")
        except Exception as e:
            log(f"sync failed: {e}")
        if not a.loop:
            break
        time.sleep(a.loop)


if __name__ == "__main__":
    main()
