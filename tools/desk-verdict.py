#!/usr/bin/env python3
"""
desk-verdict.py - a Grok bot approves or declines a queued proposal, instead of Jaron clicking a page.

Jaron, 2026-09-19: "I don't want to approve anything anymore. Grok bot should do it. If grok bot can legally do it, it's allowed."
The approval page stays as a window; this is the door. Same trail as desk-trade.py: who decided, why, when.

WHAT IT DOES
    Reads the pending proposals (verdict = 'pending') from trade_proposals, or one by id, and sets the verdict with the
    deciding agent's name and reason. The executor then places approved rows exactly as it does today (verification must match).

USAGE (from PowerShell on the MSI, e.g. through the Heartbeat MCP)
    python C:\\Users\\lilli\\AI-Shared\\tools\\desk-verdict.py list
    python C:\\Users\\lilli\\AI-Shared\\tools\\desk-verdict.py approve 71 --by grok-bot/live-wire --why "book still 0.37 vs assembled 0.62; market-feed: FOMC hiked 25bp, rule resolves this NO"
    python C:\\Users\\lilli\\AI-Shared\\tools\\desk-verdict.py decline 72 --by grok-bot/live-wire --why "edge gone after the injury report"
    --why is required. It is the whole point. Jaron reads it after a loss.
"""
from __future__ import annotations
import argparse, json, os, sys, urllib.request
from datetime import datetime, timezone

for _s in (sys.stdout, sys.stderr):
    try: _s.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError): pass
ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
SECRETS = os.path.join(os.path.expanduser("~"), ".secrets", "keys.env")
LOG = os.path.join(ROOT, "state", "desk-verdict.md")


def secrets():
    out = {}
    if os.path.exists(SECRETS):
        for line in open(SECRETS, encoding="utf-8"):
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1); out[k.strip()] = v.strip().strip('"').strip("'")
    return out


def sb(env, method, path, body=None):
    url = f"{env['SUPABASE_URL'].rstrip('/')}/rest/v1/{path}"; key = env["SUPABASE_SERVICE_ROLE_KEY"]
    req = urllib.request.Request(url, data=json.dumps(body).encode() if body is not None else None, method=method,
                                 headers={"apikey": key, "Authorization": f"Bearer {key}", "Content-Type": "application/json", "Prefer": "return=representation"})
    with urllib.request.urlopen(req, timeout=45) as r:
        raw = r.read(); return json.loads(raw) if raw else []


def log(m):
    line = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {m}"; print(line, flush=True)
    try:
        with open(LOG, "a", encoding="utf-8", newline="\n") as fh: fh.write(line + "\n")
    except OSError: pass


def main():
    ap = argparse.ArgumentParser(description="Approve or decline a queued trade proposal, with a name and a reason.")
    ap.add_argument("cmd", choices=["list", "approve", "decline"])
    ap.add_argument("id", nargs="?", type=int)
    ap.add_argument("--by", help="who is deciding, e.g. grok-bot/live-wire")
    ap.add_argument("--why", help="the reason, in words")
    a = ap.parse_args(); env = secrets()
    if not env.get("SUPABASE_SERVICE_ROLE_KEY"):
        sys.exit("SUPABASE_SERVICE_ROLE_KEY is empty in ~/.secrets/keys.env - the desk cannot write verdicts from here yet")
    if a.cmd == "list":
        rows = sb(env, "GET", "trade_proposals?verdict=eq.pending&select=id,slug,question,side,entry_price,bid,ask,edge,confidence,researcher,proposed_at,settles_at,verification&order=id.desc")
        for r in rows:
            print(f"#{r['id']} {r['slug']} {r['side']} @ {r.get('entry_price')} (book {r.get('bid')}/{r.get('ask')}) edge {r.get('edge')} conf {r.get('confidence')} by {r.get('researcher')} verif {r.get('verification')} settles {r.get('settles_at')}")
        if not rows: print("nothing pending")
        return
    if a.id is None or not a.by or not a.why: sys.exit("approve/decline need an id, --by and --why")
    verdict = "approved" if a.cmd == "approve" else "rejected"
    now = datetime.now(timezone.utc).isoformat()
    rows = sb(env, "PATCH", f"trade_proposals?id=eq.{a.id}&verdict=eq.pending",
              {"verdict": verdict, "decided_by": a.by, "decided_at": now, "decision_note": a.why})
    if not rows: sys.exit(f"#{a.id} is not pending (already decided, or no such row)")
    log(f"#{a.id} {rows[0].get('slug')} -> {verdict.upper()} by {a.by}: {a.why}")


if __name__ == "__main__":
    main()
