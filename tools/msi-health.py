#!/usr/bin/env python3
"""
msi-health.py - free replacement for Bridge's hourly Grok health check (2026-09-25, Claude Code).

Checks the MSI's always-on ports and every ENABLED scheduled job that belongs to the system. Writes the current picture to
state/msi-health-now.md every run, and appends a line to state/msi-health.md ONLY when something changed (so the log stays short).
No AI, no cost. Windows task "MSI Health", hourly.
"""
import json, os, socket, subprocess
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
NOW_MD = os.path.join(ROOT, "state", "msi-health-now.md")
LOG_MD = os.path.join(ROOT, "state", "msi-health.md")
LAST = os.path.join(ROOT, "state", "msi-health-last.json")

PORTS = {11434: "Ollama", 18789: "OpenClaw", 8765: "Polymarket MCP", 3001: "msi-heartbeat connector"}
TASKS = ["Watch Codex Writer", "Watch DeepSeek Reader", "Heartbeat News Writer", "Watch Funding Lane", "Live Board",
         "DB Size Check", "Usage Snapshot", "AI-Shared Mirror", "Polymarket MCP", "Grok Machine MCP", "Ollama Server",
         "MSI Health", "Trade Proposer", "Trade Verifier", "Trade Executor"]
# results that are not faults: 0 ok, 0x41301 still running, 0x41303 never run yet, 1 = robocopy "files copied" for the mirror
OK = {0, 0x41301, 0x41303}
# Grok Machine MCP runs forever and re-triggers every 10 min with IgnoreNew; Windows logs the skipped re-trigger as 0x800710E0.
OK_EXTRA = {"AI-Shared Mirror": {1, 2, 3}, "Grok Machine MCP": {0x800710E0}}


def port_up(p):
    try:
        with socket.create_connection(("127.0.0.1", p), timeout=2):
            return True
    except OSError:
        return False


def tasks():
    names = ",".join(f"'{t}'" for t in TASKS)
    ps = (f"Get-ScheduledTask | Where-Object {{ $_.TaskName -in @({names}) }} | ForEach-Object {{ $i = $_ | Get-ScheduledTaskInfo; "
          "[pscustomobject]@{n=$_.TaskName; s=[string]$_.State; r=$i.LastTaskResult; t=[string]$i.LastRunTime} } | ConvertTo-Json")
    out = subprocess.run(["powershell", "-NoProfile", "-Command", ps], capture_output=True, text=True, timeout=60).stdout
    d = json.loads(out or "[]")
    return d if isinstance(d, list) else [d]


def main():
    problems = []
    for p, name in PORTS.items():
        if not port_up(p):
            problems.append(f"port {p} ({name}) DOWN")
    for t in tasks():
        if t["s"] == "Disabled":
            continue          # disabled on purpose (e.g. DeepSeek paused) - not a fault
        if t["r"] not in OK and t["r"] not in OK_EXTRA.get(t["n"], set()):
            problems.append(f"{t['n']}: last result 0x{t['r']:X} at {t['t']}")
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    status = "OK" if not problems else "PROBLEM: " + "; ".join(problems)
    open(NOW_MD, "w", encoding="utf-8").write(f"# MSI health - {stamp}\n{status}\n")
    prev = None
    try:
        prev = json.load(open(LAST, encoding="utf-8")).get("status")
    except (OSError, ValueError):
        pass
    if status != prev:
        with open(LOG_MD, "a", encoding="utf-8") as f:
            f.write(f"{stamp} | {status}\n")
    json.dump({"status": status, "at": stamp}, open(LAST, "w", encoding="utf-8"))
    print(stamp, status)
    # public system page. Also published every 5 minutes by the Crew Publish task
    # (tools/crew-publish-loop.ps1 if that task cannot be created). This hourly run is the backup.
    subprocess.run(["python", os.path.join(ROOT, "tools", "publish-crew.py")], timeout=300)
    # DeepSeek loss breaker rides along hourly (tools/deepseek-breaker.py)
    subprocess.run(["python", os.path.join(ROOT, "tools", "deepseek-breaker.py")], timeout=120)
    flag = os.path.join(ROOT, "state", "deepseek-breaker.md")
    if os.path.exists(flag):
        with open(NOW_MD, "a", encoding="utf-8") as f:
            f.write("DEEPSEEK BREAKER TRIPPED - see state/deepseek-breaker.md\n")


if __name__ == "__main__":
    main()
