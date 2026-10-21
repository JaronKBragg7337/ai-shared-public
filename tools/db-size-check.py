#!/usr/bin/env python3
"""db-size-check.py - hourly: how full is the Supabase database, and warn loudly before it fills. (Claude Code, 2026-09-23)

Why this exists: on 2026-09-20 the free-tier disk filled silently (fly-school + Qwen bridge loops wrote ~130k rows / 14h), Postgres
crashed into recovery and then read-only mode, and the desk was down three days. Nothing warned anyone. Pro raised the disk to
8 GB with the spend cap ON, which also CAPS it at 8 GB - so a runaway writer will fill it again, just more slowly.

What it does: calls the db_size_report() function (service_role only), appends one line to state/db-size.log, and
  - at >= 75% of the disk cap: writes state/ALERT-DB-DISK.txt (every AI's health read looks for ALERT-* files) and shows a
    Windows notification on the MSI.
  - below 75%: removes a stale ALERT file if present.
It never deletes data. It only reports.
usage: python C:\\Users\\lilli\\AI-Shared\\tools\\db-size-check.py
"""
from __future__ import annotations
import json, os, subprocess, sys
from datetime import datetime
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
import executor as X

CAP_BYTES = 8 * 1024**3          # Pro plan disk with spend cap ON
WARN_AT = 0.75
LOG = os.path.join(X.ROOT, "state", "db-size.log")
ALERT = os.path.join(X.ROOT, "state", "ALERT-DB-DISK.txt")

def notify(title, msg):
    ps = ("Add-Type -AssemblyName System.Windows.Forms; $n = New-Object System.Windows.Forms.NotifyIcon; "
          "$n.Icon = [System.Drawing.SystemIcons]::Warning; $n.Visible = $true; "
          f"$n.ShowBalloonTip(15000, '{title}', '{msg}', 'Warning'); Start-Sleep -Seconds 16; $n.Dispose()")
    subprocess.Popen(["powershell", "-NoProfile", "-WindowStyle", "Hidden", "-Command", ps])

env = X.secrets()
now = datetime.now().strftime("%Y-%m-%d %H:%M")
try:
    r = X.sb(env, "POST", "rpc/db_size_report", {})
except Exception as e:
    with open(LOG, "a", encoding="utf-8") as fh:
        fh.write(f"{now} | UNREACHABLE: {str(e)[:120]}\n")
    print("unreachable"); sys.exit(1)

used = int(r["db_bytes"]); pct = used / CAP_BYTES
top = ", ".join(f"{t['table_name']} {t['bytes']/1024**2:.0f}MB" for t in (r.get("top_tables") or [])[:3])
line = f"{now} | {used/1024**3:.2f} GB of 8 GB ({pct:.0%}) | biggest: {top}"
with open(LOG, "a", encoding="utf-8") as fh:
    fh.write(line + "\n")
print(line)

if pct >= WARN_AT:
    with open(ALERT, "w", encoding="utf-8") as fh:
        fh.write(f"DATABASE DISK {pct:.0%} FULL as of {now}.\n{line}\n"
                 "At 100% Postgres crashes and goes read-only, as on 2026-09-20. Find the table growing fastest (biggest list above) "
                 "and stop its writer before deciding what to delete. Deleting is Jaron's call.\n")
    notify("Database disk filling", f"{pct:.0%} of 8 GB used. Biggest: {top[:80]}")
elif os.path.exists(ALERT):
    os.remove(ALERT)
