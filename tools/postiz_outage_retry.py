"""Postiz outage retry (10/21: platform.postiz.com + api.postiz.com went down ~5 PM, the 6 PM show post failed).
Runs every 20 min from the task "HB Socials Outage Retry". When Postiz answers again, posts the missed show once, then
disables its own task. Buzzes Jaron only if Postiz is back but still refuses the sign-in (then a new login is needed)."""
import os, subprocess, sys
AI = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
NOWIN = 0x08000000
POSTIZ = ["node", os.path.expandvars(r"%APPDATA%\npm\node_modules\postiz\dist\index.js")]
r = subprocess.run([*POSTIZ, "integrations:list"], capture_output=True, text=True, encoding="utf-8", timeout=120, creationflags=NOWIN)
out = (r.stdout + r.stderr)
log = open(os.path.join(AI, "state", "social-posts.log"), "a", encoding="utf-8")
import datetime; now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
if "Application not found" in out or "ECONN" in out or "fetch failed" in out or r.returncode != 0:
    log.write(f"{now} outage retry: Postiz still down ({out.strip()[:80]})\n"); sys.exit(0)
log.write(f"{now} outage retry: Postiz back - posting the missed show\n"); log.close()
subprocess.run([sys.executable, os.path.join(AI, "tools", "social_daily.py"), "show"], creationflags=NOWIN, timeout=1800)
subprocess.run(["schtasks", "/change", "/tn", "HB Socials Outage Retry", "/disable"], creationflags=NOWIN)
