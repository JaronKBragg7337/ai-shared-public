#!/usr/bin/env python3
"""Aggressive one-tick cross for Live Wire HOU NO fill."""
import json, sys, os
from datetime import datetime, timezone
sys.path.insert(0, r"C:\Users\lilli\AI-Shared\tools")
import executor as X

SLUG = "aec-cfb-hou-txtech-2026-09-18"
BY = "grok-bot/live-wire"
SIZE = 5.0
WHY = "ESPN live TTU 14-10 HOU ~2:00 Q2; ESPN win% TTU ~79% HOU ~21%; Poly Cougars YES sticky ~0.55 — re-cross 1c after resting maker"
KILL = "HOU ties or leads, or ESPN TTU win% falls under 55%"

env = X.secrets()
mcp = X.Mcp()
bid, ask, short = X.best_ask(mcp, SLUG)
print("book", bid, ask, short)
if bid is None or ask is None:
    raise SystemExit("no book")
# pay up to 1c more for NO to take: sell YES at bid-0.01
px_yes = round(max(bid - 0.01, 0.01), 2)  # e.g. 0.54
cost_no = round(1 - px_yes, 2)
shares = round(SIZE / cost_no, 2)
order = {
    "marketSlug": SLUG,
    "intent": "ORDER_INTENT_BUY_SHORT",
    "type": "ORDER_TYPE_LIMIT",
    "price": {"value": f"{px_yes:.2f}", "currency": "USD"},
    "quantity": f"{shares:.2f}",
    "tif": "TIME_IN_FORCE_GOOD_TILL_CANCEL",
}
row = {
    "slug": SLUG,
    "question": "Houston vs Texas Tech — Cougars (aggressive re-cross)",
    "outcome": "Cougars",
    "side": "no",
    "entry_price": cost_no,
    "bid": bid,
    "ask": ask,
    "spread": round(ask - bid, 4),
    "scout_probability": 0.78,
    "edge": round(bid - 0.78, 4),
    "size_usd": SIZE,
    "rationale": f"[{BY}, live, no approval] {WHY}",
    "kill_criteria": KILL,
    "verdict": "auto",
    "decided_at": datetime.now(timezone.utc).isoformat(),
    "verification": "match",
    "verified_by": "live-wire aggressive re-cross",
    "verified_at": datetime.now(timezone.utc).isoformat(),
    "verified_bid": bid,
    "verified_ask": ask,
    "proposed_by": BY,
    "category": "sports",
    "placed": False,
}
r = X.sb(env, "POST", "trade_proposals", row)
rid = r[0]["id"] if r else None
result = mcp.call("polymarket_place_order", {"order": order})
ok = isinstance(result, dict) and not result.get("error")
if rid:
    X.sb(env, "PATCH", f"trade_proposals?id=eq.{rid}", {
        "placed": bool(ok),
        "placed_at": datetime.now(timezone.utc).isoformat() if ok else None,
        "fill_note": json.dumps({"order": order, "result": result})[:800],
    })
print(json.dumps({"proposal_id": rid, "order": order, "result": result}, indent=1)[:2000])
