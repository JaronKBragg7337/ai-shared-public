# cosmos-alive.py - G-14. Called at the start of every "MSI Connector Watch" run (every 30 min, via connector-watch-ntfy.py).
# Two jobs, both safe:
#  1. The watchdog (tools/cosmos-watchdog.ps1) died unnoticed twice. If its lock file is not held, start it again, hidden.
#     The watchdog itself allows one instance only, so this can never double up.
#  2. If the Cosmos server on 127.0.0.1:8390 is still not healthy after the watchdog's restart window, buzz Jaron's phone
#     (tools/ntfy-say.py), at most once per 3 hours. A healthy server makes no noise at all. Fixed words only, no secrets.
import json, os, subprocess, sys, time, urllib.request
from datetime import datetime
ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
LOCK = os.path.join(ROOT, "state", "cosmos-watchdog.lock")
LOG = os.path.join(ROOT, "state", "cosmos-alive.log")
STAMP = os.path.join(ROOT, "state", ".cosmos-alive-buzz")   # machine-written
WATCHDOG = os.path.join(ROOT, "tools", "cosmos-watchdog.ps1")

def log(msg):
    with open(LOG, "a", encoding="utf-8") as f: f.write(f"{datetime.now():%Y-%m-%d %H:%M:%S}  {msg}\n")

def healthy():
    try:
        with urllib.request.urlopen("http://127.0.0.1:8390/health", timeout=8) as r:
            return r.status == 200 and json.loads(r.read().decode()).get("ok") is True
    except Exception:
        return False

def watchdog_alive():
    # The watchdog holds the lock file open with no sharing. If we can open it, nobody holds it.
    if not os.path.exists(LOCK): return False
    try:
        f = open(LOCK, "r+b"); f.close()
        return False
    except PermissionError:
        return True
    except OSError:
        return True

def start_watchdog():
    flags = 0x08000000 | 0x00000008  # CREATE_NO_WINDOW | DETACHED_PROCESS
    subprocess.Popen(["powershell.exe", "-NoProfile", "-WindowStyle", "Hidden", "-ExecutionPolicy", "Bypass", "-File", WATCHDOG],
                     creationflags=flags, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, close_fds=True)

if "--test" in sys.argv:
    print("healthy:", healthy(), " watchdog_alive:", watchdog_alive()); sys.exit()

if not watchdog_alive():
    log("watchdog not running; starting it")
    start_watchdog()
    time.sleep(20)

if healthy(): sys.exit()
# Not healthy. The watchdog needs up to ~90 s to notice plus a start grace of up to 4 min. Wait, then look again.
time.sleep(300)
if healthy():
    log("server was down, came back on its own"); sys.exit()
last = 0
try: last = float(open(STAMP).read().strip())
except Exception: pass
if time.time() - last < 3 * 3600:
    log("server still down; buzz already sent in the last 3 hours"); sys.exit()
state = "watchdog running" if watchdog_alive() else "watchdog NOT running"
log(f"server down after the restart window ({state}); buzzing")
subprocess.run([sys.executable, os.path.join(ROOT, "tools", "ntfy-say.py"), "Cosmos server down",
                f"The Cosmos authority server on the MSI is not answering ({state}). Tell Claude to restart it."], timeout=60)
open(STAMP, "w").write(str(time.time()))
