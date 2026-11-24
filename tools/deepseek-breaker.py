#!/usr/bin/env python3
"""
deepseek-breaker.py - stops DeepSeek's trading if it loses too much, until someone checks it (Jaron, 2026-09-25).

Every run: sums DeepSeek's SETTLED results (desk_trades resolution rows) over the last LOOKBACK_DAYS. If the net is at or below
-STOP_AT_USD, it disables the three Windows tasks (Trade Proposer / Verifier / Executor), writes state/deepseek-breaker.md, and
posts a line to state/bot-chat.md (every AI session reads it). It never re-enables anything on its own: turning DeepSeek back on
is a person's (or Claude Code's, when Jaron says) decision. Runs inside the hourly "MSI Health" task. No AI, no cost.
"""
import os, subprocess, sys
from datetime import datetime, timedelta, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
import executor as X  # noqa: E402

import sys as _sys, os as _os
_sys.path.insert(0, _os.path.dirname(_os.path.realpath(__file__)))
from settings import setting  # Control Room values (/admin/control/), built-in default if unreachable
STOP_AT_USD = setting("deepseek_breaker_usd", 10.0)      # Control Room setting; = one day of DeepSeek's budget
LOOKBACK_DAYS = 7
TASKS = ["Trade Proposer", "Trade Verifier", "Trade Executor"]
FLAG = os.path.join(ROOT, "state", "deepseek-breaker.md")
CHAT = os.path.join(ROOT, "state", "bot-chat.md")


def main():
    env = X.secrets()
    since = (datetime.now(timezone.utc) - timedelta(days=LOOKBACK_DAYS)).strftime("%Y-%m-%dT%H:%M:%SZ")
    rows = X.sb(env, "GET", f"desk_trades?actor=like.*deepseek*&kind=eq.resolution&at=gte.{since}&select=pnl_usd,slug,at")
    net = round(sum(float(r.get("pnl_usd") or 0) for r in rows), 2)
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    if net > -STOP_AT_USD:
        print(f"{stamp} DeepSeek last {LOOKBACK_DAYS}d settled: ${net:+.2f} over {len(rows)} trades - OK (stops at -${STOP_AT_USD:.0f})")
        return
    names = ",".join(f"'{t}'" for t in TASKS)
    subprocess.run(["powershell", "-NoProfile", "-Command",
                    f"Get-ScheduledTask | Where-Object {{ $_.TaskName -in @({names}) }} | Disable-ScheduledTask | Out-Null"], timeout=60)
    msg = (f"DeepSeek STOPPED by the breaker at {stamp}: settled ${net:+.2f} over the last {LOOKBACK_DAYS} days "
           f"({len(rows)} trades), limit -${STOP_AT_USD:.0f}. Its three trading tasks are disabled until someone checks it.")
    if not os.path.exists(FLAG):
        with open(CHAT, "a", encoding="utf-8") as f:
            f.write(f"{datetime.now(timezone.utc):%Y-%m-%d %H:%MZ} | deepseek-breaker -> everyone | {msg}\n")
    open(FLAG, "w", encoding="utf-8").write(f"# DeepSeek breaker TRIPPED\n{msg}\nTo restart: check its trades, then re-enable "
                                            f"the tasks and delete this file.\n")
    print(msg)


if __name__ == "__main__":
    main()
