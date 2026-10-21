#!/usr/bin/env python3
"""desk-trail-sync.py - replay the offline trade trail into Supabase once it is reachable again. (Claude Code, 2026-09-20)
desk-trade.py writes to state/desk-trail-offline.jsonl when Supabase is down, so a trade never waits on the cloud. This copies
those rows into trade_proposals (one INSERT per proposal row; the matching "_offline_update_for" line becomes its placed/fill_note),
then moves the file to state/desk-trail-offline.synced-<timestamp>.jsonl. Safe to run any time: nothing to do = nothing done.
usage: python C:\\Users\\lilli\\AI-Shared\\tools\\desk-trail-sync.py
"""
from __future__ import annotations
import json, os, sys
from datetime import datetime
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
import executor as X

path = os.path.join(X.ROOT, "state", "desk-trail-offline.jsonl")
if not os.path.exists(path) or os.path.getsize(path) == 0:
    print("nothing offline"); sys.exit(0)
env = X.secrets()
try:
    X.sb(env, "GET", "trade_proposals?select=id&limit=1")
except Exception as e:
    print("Supabase still unreachable:", str(e)[:120]); sys.exit(1)
lines = [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]
rows = [l for l in lines if "_offline" in l]; updates = [l for l in lines if "_offline_update_for" in l]
done = 0
for row in rows:
    meta = row.pop("_offline"); key = (row["slug"], row["side"], meta["by"], row["decided_at"])
    upd = next((u for u in updates if (u["_offline_update_for"]["slug"], u["_offline_update_for"]["side"], u["_offline_update_for"]["by"], u["_offline_update_for"]["at"]) == key), None)
    if upd:
        row.update({k: v for k, v in upd.items() if k != "_offline_update_for"})
    row["verification_note"] = (row.get("verification_note") or "") + f" | trail written offline at {meta['at']} ({meta['reason'][:60]}), synced {datetime.now().isoformat(timespec='seconds')}"
    r = X.sb(env, "POST", "trade_proposals", row); done += 1
    print(f"synced #{r[0]['id'] if r else '?'} {row['slug']} {row['side']} by {meta['by']}")
os.replace(path, path.replace(".jsonl", f".synced-{datetime.now().strftime('%Y%m%d-%H%M%S')}.jsonl"))
print(f"{done} row(s) synced; file archived")
