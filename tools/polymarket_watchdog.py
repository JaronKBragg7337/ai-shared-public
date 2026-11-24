"""Polymarket service watchdog (10/23 12:36 AM the local Polymarket service on 127.0.0.1:8765 died and every trading tool stopped;
its task only starts at logon). Every 2 minutes (task "Polymarket Watchdog"): if nothing answers on 8765, start the "Polymarket MCP"
task and log it; buzz Jaron's phone only if it is still down after the restart."""
import os, socket, subprocess, sys, time, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
LOG = os.path.join(ROOT, "state", "polymarket-watchdog.log")
NOWIN = 0x08000000


def up():
    try: socket.create_connection(("127.0.0.1", 8765), timeout=3).close(); return True
    except OSError: return False


if not up():
    subprocess.run(["schtasks", "/Run", "/TN", "Polymarket MCP"], capture_output=True, creationflags=NOWIN)
    ok = False
    for _ in range(15):
        time.sleep(3)
        if up(): ok = True; break
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(f"{datetime.datetime.now():%Y-%m-%d %H:%M} service was down -> restarted: {'OK' if ok else 'STILL DOWN'}\n")
    if not ok:
        subprocess.run([sys.executable, os.path.join(ROOT, "tools", "ntfy-say.py"), "Polymarket service down",
                        "the trading service on the MSI did not come back after a restart - trades are paused"], timeout=30)
