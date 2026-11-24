"""Is the MSI reachable by the bots? Prints OK or a plain problem line. No AI, no cost.
Checks: the Cloudflare tunnel to the MSI connector answers (401 = up and asking for login; 5xx/timeout = down), and the Grok
traders have written to bot-chat.md / live-wire.md recently (they reach the MSI only through the connector, so silence while
their routines should be running means the connector lost its authorization)."""
import os, re, time, json, urllib.request, urllib.error
from datetime import datetime, timezone
ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
problems = []
try:
    urllib.request.urlopen("https://mcp.heartbeatobservatory.com/mcp", timeout=15)
except urllib.error.HTTPError as e:
    if e.code >= 500: problems.append(f"connector tunnel down (HTTP {e.code})")
except Exception as e:
    problems.append(f"connector tunnel unreachable ({type(e).__name__})")
try:
    urllib.request.urlopen(urllib.request.Request("https://cosmos.heartbeatobservatory.com/health", headers={"User-Agent": "Mozilla/5.0 connector-watch"}), timeout=15)
except Exception as e:
    problems.append(f"The Cosmos game server is not answering ({type(e).__name__}) - Claude should restart it")
import socket, subprocess
try:   # keep live-wire.md / bot-chat.md append-only (Darios rewrote live-wire.md twice: 10/8, 10/9)
    subprocess.run([__import__('sys').executable, os.path.join(ROOT, 'tools', 'append-guard.py')], timeout=60)
except Exception:
    pass
# The Polymarket service (port 8765, task "Polymarket MCP") is DOWN on purpose since Jaron's 10/28 decision (P-0112, AGENTS.md):
# this watch no longer restarts it or buzzes about it. Turned off 11/22 by the everything-check review (it had been starting
# "Polymarket MCP" whenever 8765 was free). Kept, not deleted: set POLYMARKET_AUTORESTART = True only if Jaron restarts it.
POLYMARKET_AUTORESTART = False
if POLYMARKET_AUTORESTART:
    try:   # the Polymarket service desk.py / desk-trade.py talk to (10/8: down all day unnoticed; bots could not trade or see positions)
        socket.create_connection(("127.0.0.1", 8765), timeout=5).close()
    except OSError:
        subprocess.run(["schtasks", "/Run", "/TN", "Polymarket MCP"], capture_output=True)   # start it, then re-check
        time.sleep(15)
        try:
            socket.create_connection(("127.0.0.1", 8765), timeout=5).close()
        except OSError:
            problems.append("the Polymarket trading service (port 8765) is down and did not restart - bots cannot trade; tell Claude")
now = time.time()
lw =os.path.join(ROOT, "state", "live-wire.md")
age_lw = (now - os.path.getmtime(lw)) / 60 if os.path.exists(lw) else 9999
last = {}
for line in open(os.path.join(ROOT, "state", "bot-chat.md"), encoding="utf-8", errors="ignore").read().splitlines()[-400:]:
    m = re.match(r"(\d{4}-\d\d-\d\d[T ]\d\d:\d\d(?::\d\d)?Z?)\s*\|\s*([^|]+?)\s*->", line)
    if not m: continue
    ts = m.group(1).replace(" ", "T").rstrip("Z")
    try: t = datetime.fromisoformat(ts).replace(tzinfo=timezone.utc).timestamp()
    except ValueError: continue
    who = m.group(2).lower()
    for bot in ("darios", "demis", "satya", "grok-bot"):
        if bot in who: last[bot] = max(last.get(bot, 0), t)
newest = max([v for v in last.values()] + [now - age_lw * 60])
quiet = (now - newest) / 60
# 10/17 (Jaron: "does it alert when they CAN'T reach it, or when they just haven't?" - it was the second, so quiet bots doing
# games set it off). Now it tells three cases apart, using what the connector server records (state/connector-hits.json):
#   can't reach the MSI from the internet -> alert;  Grok came but its sign-in expired -> alert (re-authorize);
#   nobody tried -> the bots are just quiet: no buzz unless it lasts 12 hours.
if quiet > 75:
    try:
        reach = urllib.request.urlopen(urllib.request.Request("https://mcp.heartbeatobservatory.com/.well-known/oauth-authorization-server",
            headers={"User-Agent": "Mozilla/5.0 (MSI connector watch)"}), timeout=20).status == 200   # Cloudflare 403s the bare python agent
    except Exception:
        reach = False
    try: hits = json.load(open(os.path.join(ROOT, "state", "connector-hits.json")))
    except Exception: hits = {}
    def ago(k):
        v = hits.get(k)
        return (now - datetime.fromisoformat(v.replace("Z", "+00:00")).timestamp()) / 60 if v else 1e9
    if not reach:
        problems.append("the MSI connector can't be reached from the internet (tunnel or server down) - tell Claude")
    elif ago("last_expired_token") < quiet and ago("last_expired_token") < ago("last_ok"):
        problems.append(f"a Grok trader tried to reach the MSI {ago('last_expired_token'):.0f} min ago but its sign-in has expired - re-authorize the connector in the Grok app")
    elif quiet > 720 and not os.path.exists(os.path.join(ROOT, "state", "grok-routines-off"))             and not (datetime.now().weekday() in (0, 1, 2, 3) and datetime.now().weekday() * 24 + datetime.now().hour < 3 * 24 + 14):
        # 10/21: the trading routines run Thu-Sun noon-1 AM (10/15), so Mon-Wed silence is the schedule, not a problem.
        # Only alert once Thursday's first run should have happened (Thu 2 PM local).   # flag file = routines off on purpose: no quiet note
        problems.append(f"the Grok traders have been quiet for {quiet / 60:.0f} h (the connector is up and nobody failed to sign in) - check their routines are on in the Grok app")
# 10/19: the Sapling relay (website <-> Sapling) died silently on 10/17 and Jaron's message sat unanswered. Restart it once
# (safe repair, it's just the messenger), alert only if it won't come back.
try:
    out = subprocess.run(["powershell", "-NoProfile", "-Command",
        "Get-CimInstance Win32_Process -Filter \"Name like 'python%'\" | Where-Object { $_.CommandLine -match 'owner_relay' } | Measure-Object | % Count"],
        capture_output=True, text=True, timeout=60, creationflags=0x08000000).stdout.strip()
    if out == "0":
        subprocess.run(["schtasks", "/Run", "/TN", "Sapling Relay"], capture_output=True, creationflags=0x08000000)
        time.sleep(20)
        out = subprocess.run(["powershell", "-NoProfile", "-Command",
            "Get-CimInstance Win32_Process -Filter \"Name like 'python%'\" | Where-Object { $_.CommandLine -match 'owner_relay' } | Measure-Object | % Count"],
            capture_output=True, text=True, timeout=60, creationflags=0x08000000).stdout.strip()
        if out == "0":
            problems.append("the Sapling relay is down and did not restart - the Sapling page can't reach Sapling; tell Claude")
except Exception:
    pass
# 10/18: the news render needs ~70 GB of room for its frames; the disk filled on 10/18 and killed the 3 AM render.
try:
    import shutil
    free_gb = shutil.disk_usage("C:\\").free / 1e9
    if free_gb < 80:
        problems.append(f"the MSI has only {free_gb:.0f} GB free - the news render needs ~70 GB; tell Claude to clear space before 3 AM")
except Exception:
    pass
print("OK" if not problems else "PROBLEM: " + "; ".join(problems))
