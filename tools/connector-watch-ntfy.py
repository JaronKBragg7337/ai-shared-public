# Runs connector-watch.py from a Windows timer (no Claude usage). On PROBLEM, pushes one line to Jaron's phone through
# ntfy (topic NTFY_TOPIC in ~/.secrets/keys.env), at most once per 3 hours per problem; logs to state/connector-alerts.log.
import os, re, subprocess, sys, urllib.request
from datetime import datetime, timedelta
ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
LOG = os.path.join(ROOT, "state", "connector-alerts.log")
def topic():
    for line in open(os.path.expanduser("~/.secrets/keys.env"), encoding="utf-8-sig"):
        if line.startswith("NTFY_TOPIC="): return line.split("=", 1)[1].strip()
def push(msg, title="MSI watch"):
    req = urllib.request.Request("https://ntfy.sh/" + topic(), data=msg.encode(), headers={"Title": title, "Priority": "high"})
    urllib.request.urlopen(req, timeout=20)
if len(sys.argv) > 1 and sys.argv[1] == "--test":
    push("Test buzz from the MSI. If you see this, alerts work.", "MSI watch test"); print("sent"); sys.exit()
import time
def check():
    return subprocess.run([sys.executable, os.path.join(ROOT, "tools", "connector-watch.py")], capture_output=True, text=True, timeout=120).stdout.strip()
out = check()
if not out.startswith("PROBLEM"): sys.exit()
time.sleep(240)  # a deploy restarts the game server on purpose; the watchdog brings it back within ~4 min - only alert if it's still down
out = check()
if not out.startswith("PROBLEM"): sys.exit()
out = out.replace("Claude should restart it", "still down after 4 min (the watchdog didn't bring it back) - tell Claude")
key = re.sub(r"\d+", "#", out)[:120]
now = datetime.now()
if os.path.exists(LOG):
    for line in open(LOG, encoding="utf-8").readlines()[-50:]:
        m = re.match(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2})\s+(.*)", line)
        if m and re.sub(r"\d+", "#", m[2])[:120] == key and now - datetime.strptime(m[1], "%Y-%m-%d %H:%M") < timedelta(hours=3):
            sys.exit()
push(out[:300])
open(LOG, "a", encoding="utf-8").write(f"{now:%Y-%m-%d %H:%M} {out[:300]}\n")
