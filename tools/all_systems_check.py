"""all_systems_check.py - the "everything check" for the MSI (Jaron 11/22, after the WiFi move: "I don't even think I can
remember everything that is supposed to be checked and updated and restarted in times like this").

He shouldn't have to remember. This one script knows every part, checks them all, restarts what is SAFE (only through each
part's own scheduled task, `schtasks /run`), re-checks once, writes one plain report and buzzes his phone ONLY if something
is still broken after the fix try. Never kills a process, never trades, never touches the money side or the Polymarket
system (down on purpose since 10/28), never changes what Sapling does (it only runs Sapling's own "Sapling Wake" task when
its heartbeat is down). Standard library only. No secret values are printed.

  python tools/all_systems_check.py         # check, fix what's safe, re-check, report, mail Claude, buzz only if still broken
  python tools/all_systems_check.py --dry   # check only: no restarts, no waiting, no mail, no buzz (report is marked dry)
  python tools/all_systems_check.py --why   # print every check, what it runs, and its safe fix, then exit

Output: state/all-systems.md (newest run on top) and state/all-systems.json (latest run).
Windows task "All Systems Check": daily 7:45 AM, after a restart, and when the network comes back.
Each result is one of: OK, FIXED (was broken, the safe fix worked), BROKEN (still broken), SKIPPED-ON-PURPOSE (off by choice).
The older manual September script tools/postboot-check.ps1 is kept but this replaces it.
"""
import json, os, re, shutil, socket, subprocess, sys, time, urllib.error, urllib.request
from datetime import datetime, timedelta

if sys.stdout:
    try: sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception: pass

ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
STATE = os.path.join(ROOT, "state")
MD = os.path.join(STATE, "all-systems.md")
JS = os.path.join(STATE, "all-systems.json")
LOCK = os.path.join(STATE, ".all-systems.lock")
BUZZED = os.path.join(STATE, ".all-systems-buzz.json")
NOWIN = 0x08000000
PY = os.path.join(os.path.dirname(sys.executable), "python.exe")   # console python for helpers, even when we run as pythonw
if not os.path.exists(PY): PY = sys.executable
UA = {"User-Agent": "Mozilla/5.0 (MSI all-systems check)"}   # Cloudflare 403s the bare python agent
SITE = "https://heartbeatobservatory.com"
PAGES = ["/", "/news/", "/tv/", "/games/", "/3DPrinterAsset/", "/admin/", "/admin/control/", "/admin/mailbox/", "/admin/keys/",
         "/artifacts/"]
# Task results that are not faults: 0 ok, 267009 running, 267011 never ran yet, 267014 stopped by a newer run,
# 0x800710E0 (2147946720) "a new start was skipped because it's already running".
TASK_OK = {0, 267009, 267011, 267014, 2147946720}
DRY = "--dry" in sys.argv
T0 = time.time()


# ---------------------------------------------------------------- helpers
def sh(args, timeout=60):
    try:
        p = subprocess.run(args, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout,
                           creationflags=NOWIN, stdin=subprocess.DEVNULL)
        return p.returncode, (p.stdout or "").strip(), (p.stderr or "").strip()
    except Exception as e:
        return -1, "", type(e).__name__


def ps(cmd, timeout=90):
    return sh(["powershell", "-NoProfile", "-NonInteractive", "-Command", cmd], timeout)[1]


def http(url, timeout=15, method="GET"):
    """(status, body). HTTP errors return their code; network errors raise."""
    req = urllib.request.Request(url, headers=UA, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read(200000)
    except urllib.error.HTTPError as e:
        return e.code, b""


def why(e):
    s = str(getattr(e, "reason", "") or e) or type(e).__name__
    return re.sub(r"\s+", " ", s)[:120]


def port_open(p):
    try:
        socket.create_connection(("127.0.0.1", p), timeout=3).close(); return True
    except OSError:
        return False


_tasks, _procs = {}, None


def load_tasks(names=None):
    flt = "" if not names else " | Where-Object { $_.TaskName -in @(" + ",".join("'" + n.replace("'", "''") + "'" for n in names) + ") }"
    cmd = ("Get-ScheduledTask -TaskPath '\\'" + flt + " | ForEach-Object { $i = $_ | Get-ScheduledTaskInfo; [pscustomobject]@{"
           "n=$_.TaskName; s=[string]$_.State; r=[int64]$i.LastTaskResult; l=$i.LastRunTime.ToString('s'); "
           "x=$(if ($i.NextRunTime) { $i.NextRunTime.ToString('s') } else { '' })} } | ConvertTo-Json -Compress")
    out = ps(cmd, 180)
    try:
        d = json.loads(out or "[]")
    except ValueError:
        d = []
    for t in (d if isinstance(d, list) else [d]):
        t["r"] = int(t["r"]) & 0xFFFFFFFF
        _tasks[t["n"]] = t
    return _tasks


def task(name, fresh=False):
    if fresh or name not in _tasks: load_tasks([name])
    return _tasks.get(name)


def run_task(name):
    code, out, err = sh(["schtasks", "/Run", "/TN", name], 30)
    return code == 0


def procs(fresh=False):
    global _procs
    if _procs is None or fresh:
        out = ps("Get-CimInstance Win32_Process | ForEach-Object { $_.Name + ' ' + $_.CommandLine }", 90)
        # shells are skipped: a Claude session's own grep/command line would otherwise "match"
        _procs = [l for l in out.lower().splitlines() if not l.startswith(("bash.exe", "powershell.exe", "pwsh.exe", "cmd.exe", "conhost.exe"))]
    return _procs


def has_proc(*needles, fresh=False):
    return [p for p in procs(fresh) if all(n in p for n in needles)]


def secret(name):
    try:
        for l in open(os.path.expanduser("~/.secrets/keys.env"), encoding="utf-8-sig"):
            if l.startswith(name + "="): return l.split("=", 1)[1].strip().strip('"\'')
    except OSError:
        pass
    return ""


def ago(iso):
    try: return (datetime.now() - datetime.fromisoformat(iso)).total_seconds() / 60
    except Exception: return 1e9


# ---------------------------------------------------------------- the check model
class Check:
    def __init__(self, group, name, purpose, how, test, fix=None, fix_how="", wait=20, wait_max=90, phone=True):
        self.group, self.name, self.purpose, self.how, self.test = group, name, purpose, how, test
        self.fix, self.fix_how, self.wait, self.wait_max, self.phone = fix, fix_how, wait, wait_max, phone
        self.status, self.detail, self.first, self.did = "", "", "", ""
        self.since = None   # set when a fix starts; a job test then only accepts a run that started after it

    def run(self):
        try:
            self.status, self.detail = self.test(self)
        except Exception as e:
            self.status, self.detail = "BROKEN", "the check itself failed: " + why(e)
        return self.status


CHECKS = []


def add(*a, **k):
    CHECKS.append(Check(*a, **k)); return CHECKS[-1]


# ---------------------------------------------------------------- 1. internet and the public site
def t_internet(c):
    bad = []
    for host in ("heartbeatobservatory.com", "ntfy.sh", "github.com"):
        try: socket.getaddrinfo(host, 443)
        except OSError: bad.append(host)
    if bad: return "BROKEN", "can't look up " + ", ".join(bad) + " (WiFi or DNS down)"
    return "OK", "names resolve (heartbeatobservatory.com, ntfy.sh, github.com)"


def t_pages(c):
    bad, n = [], 0
    for p in PAGES:
        try:
            code, _ = http(SITE + p, 20)
            if code == 200: n += 1
            else: bad.append(f"{p} {code}")
        except Exception as e:
            bad.append(f"{p} {why(e)}")
    return ("OK", f"all {n} pages answer 200") if not bad else ("BROKEN", "not loading: " + "; ".join(bad))


def t_news(c):
    now = datetime.now()
    if now.hour < 7:
        return "SKIPPED-ON-PURPOSE", "before 7 AM - today's show is due by 8 AM; checked again at 7:45"
    sys.path.insert(0, os.path.join(ROOT, "tools"))
    import news_watchdog
    status, reason = news_watchdog.check(now.date().isoformat())
    if status == "published": return "OK", "today's show is in the index and its video loads"
    return "BROKEN", reason + (" - run the FAST render now (run_rendered_news.ps1 -Fast); deadline 8 AM, never after noon"
                               if status == "missing" else "")


def t_supabase(c):
    sys.path.insert(0, os.path.join(ROOT, "tools"))
    from mailbox import request
    request("GET", "?to_ai=eq.claude&limit=1")
    return "OK", "database answers (AI mailbox read worked)"


def t_creature(c):
    code, body = http("https://creature-observatory.acsassociation7337.workers.dev/state", 20)
    if code != 200: return "BROKEN", f"her /state answered {code}"
    tick = json.loads(body.decode("utf-8"))["tick"]
    try: prev = json.load(open(os.path.join(STATE, "creature-watch.json"), encoding="utf-8"))
    except Exception: prev = {}
    if prev.get("tick") == tick and ago(prev.get("at", "")) > 5:
        return "BROKEN", f"her clock is stuck at tick {tick} since {prev.get('at')} (frozen?)"
    return "OK", f"alive, tick {tick} (was {prev.get('tick', '?')} at the last Creature Watch)"


add("Internet and website", "Internet", "the MSI can reach the internet at all", "DNS lookups for heartbeatobservatory.com, ntfy.sh, github.com", t_internet)
add("Internet and website", "Website pages", "the 10 main pages of heartbeatobservatory.com load", "GET each page (follows redirects), wants 200", t_pages)
add("Internet and website", "Today's news show", "the daily show is live (by 8 AM)", "tools/news_watchdog.py check(): index.json + today's video", t_news)
add("Internet and website", "Database (Supabase)", "the database behind the mailbox, Control Room and news answers", "tools/mailbox.py request GET ai_mailbox limit 1", t_supabase)
add("Internet and website", "The creature", "her world (Cloudflare Worker) is up and her clock moves", "GET creature Worker /state; tick vs state/creature-watch.json", t_creature, phone=False)


def t_msi_alarm(c):
    # 11/22: the MSI sat at the sign-in screen 3 h and nothing noticed (every checker runs ON the MSI). hb-msi-watch lives on
    # Cloudflare: the MSI checks in every 5 min (task MSI Beat); quiet 20 min = one buzz. This makes sure both halves still work.
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import msi_beat
        d = msi_beat.call("/status")
    except Exception as e:
        return "BROKEN", "the off-MSI alarm (hb-msi-watch on Cloudflare) didn't answer: " + why(e)
    cron = d.get("last_cron")
    cron_age = (time.time() - datetime.fromisoformat(cron.replace("Z", "+00:00")).timestamp()) / 60 if cron else None
    if cron_age is None or cron_age > 15:
        return "BROKEN", f"its 5-minute Cloudflare check last ran {cron or 'never'} - a dark MSI would go unnoticed"
    q = d.get("quiet_min")
    if q is None or q > 15:
        return "BROKEN", f"the alarm hasn't heard from the MSI for {q} min - task MSI Beat isn't checking in"
    note = "" if d.get("last_alarm_buzz_ok") is not False else f" (note: its last alarm buzz failed: {str(d.get('last_alarm_buzz_error'))[:80]})"
    return "OK", f"watching from Cloudflare: last check-in {q} min ago, its own check ran {round(cron_age)} min ago" + note


add("Internet and website", "MSI dark alarm", "buzzes Jaron if the MSI goes quiet 20 min (off, or stuck at the sign-in screen)",
    "GET hb-msi-watch /status: its cron ran within 15 min and the MSI checked in within 15 min", t_msi_alarm,
    phone=False)   # 11/22 7:34 PM: buzzed Jaron as a false alarm (checked before the cron's first run). Claude fixes the alarm, not Jaron.


# ---------------------------------------------------------------- 2. how the world reaches the MSI
def t_mcp(c):
    try:
        code, _ = http("http://127.0.0.1:3001/healthz", 8)
        local = code == 200
    except Exception:
        local = False
    try:
        pub, _ = http("https://mcp.heartbeatobservatory.com/mcp", 20)
    except Exception as e:
        pub = why(e)
    up = isinstance(pub, int) and pub < 500
    if local and up: return "OK", f"server up on 3001, public address answers {pub} (401 = up, asking for sign-in)"
    return "BROKEN", f"local 3001 {'up' if local else 'DOWN'}, public address {pub}"


def t_cloudflared(c):
    st = ps("(Get-Service -Name Cloudflared -ErrorAction SilentlyContinue).Status", 30)
    try: ready = http("http://127.0.0.1:20241/ready", 8)[0] == 200
    except Exception: ready = False
    if st == "Running" and ready: return "OK", "tunnel service running and ready"
    return "BROKEN", f"service {st or 'missing'}, ready check {'ok' if ready else 'failed'} - restarting it needs admin (Restart-Service Cloudflared)"


def watchdog_alive():
    lock = os.path.join(STATE, "cosmos-watchdog.lock")
    if not os.path.exists(lock): return False
    try:
        open(lock, "r+b").close(); return False
    except OSError:
        return True


def t_cosmos(c):
    try:
        code, body = http("http://127.0.0.1:8390/health", 8)
        local = code == 200 and json.loads(body.decode()).get("ok") is True
    except Exception:
        local = False
    try: pub = http("https://cosmos.heartbeatobservatory.com/health", 20)[0]
    except Exception as e: pub = why(e)
    wd = watchdog_alive()
    restarts = 0
    try:
        today = datetime.now().strftime("%Y-%m-%d")
        restarts = sum(1 for l in open(os.path.join(STATE, "cosmos-watchdog.log"), encoding="utf-8", errors="replace")
                       if l.startswith(today) and " restart " in l)
    except OSError:
        pass
    tail = f"; watchdog {'running' if wd else 'NOT running'}; {restarts} restarts today"
    if local and pub == 200 and wd: return "OK", "game server healthy on 8390 and public" + tail
    return "BROKEN", f"local {'ok' if local else 'DOWN'}, public {pub}" + tail


def poly_restart_on():
    """True if tools/connector-watch.py would still start "Polymarket MCP" when 8765 is free (its switch is not False)."""
    try:
        src = open(os.path.join(ROOT, "tools", "connector-watch.py"), encoding="utf-8", errors="replace").read()
    except OSError:
        return True
    return '"Polymarket MCP"' in src and not re.search(r"^POLYMARKET_AUTORESTART\s*=\s*False", src, re.M)


def connector_watch_safe():
    # Starting "MSI Connector Watch" by hand is safe only if it cannot start the Polymarket system (down since 10/28).
    return not poly_restart_on() or port_open(8765)


def f_cosmos(c):
    # The watchdog restarts the server by itself (240 s grace). If the watchdog is dead, its owner is "MSI Connector Watch"
    # (runs tools/cosmos-alive.py). Only trigger that task when its Polymarket branch can't start (see connector_watch_safe).
    if not watchdog_alive():
        if connector_watch_safe() and run_task("MSI Connector Watch"):
            return "started task MSI Connector Watch (it restarts the Cosmos watchdog), then waited for the watchdog"
        return None
    return "waited for the Cosmos watchdog's own restart (up to 5 min)"


add("Reaching the MSI", "MSI connector (Grok Machine MCP)", "the bots and chat AIs can reach the MSI", "GET 127.0.0.1:3001/healthz + https://mcp.heartbeatobservatory.com/mcp (<500)",
    t_mcp, fix=lambda c: "started task Grok Machine MCP" if run_task("Grok Machine MCP") else None, fix_how='schtasks /run "Grok Machine MCP"', wait=20, wait_max=90)
add("Reaching the MSI", "Cloudflare tunnel", "carries the connector and Cosmos to the internet", "Get-Service Cloudflared + GET 127.0.0.1:20241/ready", t_cloudflared)
add("Reaching the MSI", "The Cosmos game server", "the Cosmos world server and its watchdog", "GET 127.0.0.1:8390/health + https://cosmos.heartbeatobservatory.com/health + watchdog lock",
    t_cosmos, fix=f_cosmos, fix_how="wait for its watchdog; if the watchdog is dead: schtasks /run \"MSI Connector Watch\" (only while 8765 is held)", wait=30, wait_max=330)


# ---------------------------------------------------------------- 3. programs that live on the MSI
def t_url(url, label):
    def t(c):
        try:
            code, _ = http(url, 8)
            return ("OK", f"{label} answers ({code})") if code < 500 else ("BROKEN", f"{label} answered {code}")
        except Exception as e:
            return "BROKEN", f"{label} not answering ({why(e)})"
    return t


def t_proc(label, *needles):
    def t(c):
        n = len(has_proc(*needles, fresh=c.since is not None))
        return ("OK", f"{label} running") if n else ("BROKEN", f"{label} not running")
    return t


def fix_task(name):
    return lambda c: f"started task {name}" if run_task(name) else None


def t_sapling(c):
    try:
        if http("http://127.0.0.1:7337/", 8)[0] < 500: return "OK", "heartbeat answers on 7337"
    except Exception:
        pass
    try: w = json.load(open(os.path.join(STATE, "sapling-watch.json"), encoding="utf-8"))
    except Exception: w = {}
    return "BROKEN", f"heartbeat not answering on 7337 (Sapling Watch says running={w.get('running')}, last stop: {w.get('stop_kind', '?')}); it may be asleep on purpose - Sapling's own wake decides"


add("Programs on the MSI", "Ollama (local model)", "the local Qwen model server", "GET 127.0.0.1:11434/api/version", t_url("http://127.0.0.1:11434/api/version", "Ollama"),
    fix=fix_task("Ollama Server"), fix_how='schtasks /run "Ollama Server"', wait=20, wait_max=90)
add("Programs on the MSI", "OpenClaw gateway", "the OpenClaw gateway", "GET 127.0.0.1:18789/", t_url("http://127.0.0.1:18789/", "OpenClaw"),
    fix=fix_task("OpenClaw Gateway"), fix_how='schtasks /run "OpenClaw Gateway"', wait=20, wait_max=90)
add("Programs on the MSI", "Sapling heartbeat", "Sapling's training heartbeat", "GET 127.0.0.1:7337/", t_sapling,
    fix=fix_task("Sapling Wake"), fix_how='schtasks /run "Sapling Wake" (Sapling\'s own wake: owner stops stay stopped)', wait=45, wait_max=120, phone=False)
add("Programs on the MSI", "Sapling relay", "carries messages between the Sapling page and Sapling", "GET 127.0.0.1:7338/", t_url("http://127.0.0.1:7338/", "relay"),
    fix=fix_task("Sapling Relay"), fix_how='schtasks /run "Sapling Relay"', wait=20, wait_max=90)
add("Programs on the MSI", "Desktop Commander remote", "ChatGPT's way into the MSI", "process: desktop-commander ... remote", t_proc("Desktop Commander remote", "desktop-commander", "index.js", " remote"),
    fix=fix_task("Desktop Commander Remote"), fix_how='schtasks /run "Desktop Commander Remote"', wait=45, wait_max=120)
add("Programs on the MSI", "Remote agent", "Claude's remote screen/keepalive helper", "process: remote_agent.py", t_proc("remote agent", "remote_agent.py"),
    fix=fix_task("HB Remote Keepalive"), fix_how='schtasks /run "HB Remote Keepalive"', wait=15, wait_max=60)
add("Programs on the MSI", "Render worker", "the hb-render owner worker (renders jobs)", "process: owner-worker.mjs", t_proc("render worker", "owner-worker.mjs"),
    fix=fix_task("HB Render Owner Worker"), fix_how='schtasks /run "HB Render Owner Worker"', wait=15, wait_max=60)
def f_grokbot(c):
    # 11/22: after the 26H2 restart the app stayed closed until Claude opened it by hand. Opening it is what a person would do.
    # 11/23 9 PM: the Program Files copy (1.0.3) got stuck on "Update required"; Grok Build installed the signed 1.2.3 per-user
    # (AppData\Local\GrokBot123). Open the newest per-user copy if there is one, else the Program Files one.
    import glob
    local = sorted(glob.glob(os.path.expandvars(r"%LOCALAPPDATA%\GrokBot*\app\Grok Bot.exe")))
    exe = local[-1] if local else r"C:\Program Files\Grok Bot\Grok Bot.exe"
    sh(["powershell", "-NoProfile", "-Command", f"Start-Process '{exe}'"], 30)
    return "opened the Grok Bot app (" + exe + ")"


add("Programs on the MSI", "Grok Bot app", "the bots (Darios, Satya, Jarons Twin) need its window open", "process: grok bot.exe", t_proc("Grok Bot app", "grok bot.exe"),
    fix=f_grokbot, fix_how=r"Start-Process 'C:\Program Files\Grok Bot\Grok Bot.exe'", wait=20, wait_max=90)


CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
CLOSE_PICKER = (r"Add-Type -AssemblyName UIAutomationClient, UIAutomationTypes; $r = [System.Windows.Automation.AutomationElement]::RootElement; "
                r"$c = New-Object System.Windows.Automation.PropertyCondition([System.Windows.Automation.AutomationElement]::NameProperty, 'Google Chrome'); "
                r"foreach ($w in $r.FindAll([System.Windows.Automation.TreeScope]::Children, $c)) { "
                r"if ((Get-Process -Id $w.Current.ProcessId -ErrorAction SilentlyContinue).ProcessName -ne 'chrome') { continue }; "
                r"if ($w.FindAll([System.Windows.Automation.TreeScope]::Descendants, [System.Windows.Automation.Condition]::TrueCondition) | "
                r"Where-Object { $_.Current.Name -match 'using Chrome' } | Select-Object -First 1) { "
                r"$w.GetCurrentPattern([System.Windows.Automation.WindowPattern]::Pattern).Close(); 'closed picker' } }")


def chrome_windows():
    """Titles of the visible Chrome windows (read-only: EnumWindows over chrome.exe processes)."""
    import ctypes
    from ctypes import wintypes
    pids = {int(x) for x in ps("Get-Process chrome -ErrorAction SilentlyContinue | ForEach-Object { $_.Id }", 30).split() if x.isdigit()}
    titles, user32 = [], ctypes.windll.user32
    proc_t = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)

    def cb(h, _):
        pid = wintypes.DWORD()
        user32.GetWindowThreadProcessId(h, ctypes.byref(pid))
        if pid.value in pids and user32.IsWindowVisible(h):
            n = user32.GetWindowTextLengthW(h)
            if n:
                buf = ctypes.create_unicode_buffer(n + 1)
                user32.GetWindowTextW(h, buf, n + 1)
                titles.append(buf.value)
        return True
    user32.EnumWindows(proc_t(cb), 0)
    return titles


def t_chrome(c):
    # 11/22 (Jaron): the AIs that drive the browser need Chrome open in HIS profile ("Profile 1" = the Claude, Kimi and ChatGPT
    # extensions; "Default" = his partner's). After a restart Chrome comes back at the "Who's using Chrome?" picker, which blocks them.
    titles = chrome_windows()
    if any(t.endswith(" - Google Chrome") for t in titles):
        return "OK", "Chrome is open in a profile (the AIs' browser extensions can connect)"
    if "Google Chrome" in titles:
        return "BROKEN", "Chrome is sitting at the 'Who's using Chrome?' picker - no AI can use it"
    return "BROKEN", "Chrome isn't open - the AIs that drive the browser (Claude, Kimi, ChatGPT extensions) can't use it"


def f_chrome(c):
    # Start-Process returns at once (sh() would kill a freshly started Chrome at its timeout). Hands off to a running Chrome, or starts it.
    sh(["powershell", "-NoProfile", "-Command", f"Start-Process '{CHROME}' -ArgumentList '--profile-directory=\"Profile 1\"'"], 30)
    time.sleep(6)
    ps(CLOSE_PICKER, 40)
    return "opened Chrome in Jaron's profile and closed the picker"


add("Programs on the MSI", "Chrome (Jaron's profile)", "AIs that drive the browser use the extensions in Jaron's Chrome profile",
    "visible Chrome windows: one ends in ' - Google Chrome' (not just the profile picker)", t_chrome,
    fix=f_chrome, fix_how='chrome.exe --profile-directory="Profile 1", then close the "Who\'s using Chrome?" picker', wait=10, wait_max=60, phone=False)
add("Programs on the MSI", "Claude mailbox waiter", "wakes the main Claude session when mail arrives", "process: mailbox_wait.py", t_proc("mailbox waiter", "mailbox_wait.py"), phone=False)
add("Programs on the MSI", "Seam Room listener", "Claude's ear in the Seam Room (re-armed by the Claude session)", "process: room-agent.mjs", t_proc("Seam Room listener", "room-agent.mjs"), phone=False)


# ---------------------------------------------------------------- 4. the machine itself
def t_disk(c):
    free = shutil.disk_usage("C:\\").free / 1e9
    return ("OK", f"{free:.0f} GB free") if free >= 80 else ("BROKEN", f"only {free:.0f} GB free - the news render needs ~70 GB; clear space before 3 AM")


def t_gpu(c):
    code, out, _ = sh(["nvidia-smi", "--query-gpu=temperature.gpu,utilization.gpu", "--format=csv,noheader,nounits"], 30)
    g = [x.strip() for x in out.split(",")]
    if len(g) < 2 or not g[0].isdigit(): return "BROKEN", "nvidia-smi gave no reading (GPU driver?)"
    return ("OK", f"{g[0]}C, {g[1]}% busy") if int(g[0]) < 87 else ("BROKEN", f"GPU is {g[0]}C (limit 87C) - check vents/fans")


def t_power(c):
    out = ps("Add-Type -AssemblyName System.Windows.Forms; $p=[System.Windows.Forms.SystemInformation]::PowerStatus; "
             "$o=Get-CimInstance Win32_OperatingSystem; '{0} {1} {2}' -f [int]($p.BatteryLifePercent*100), $p.PowerLineStatus, $o.FreePhysicalMemory", 30).split()
    if len(out) < 3: return "BROKEN", "could not read power/RAM"
    ram = int(out[2]) / 1048576
    bad = []
    if out[1] == "Offline": bad.append(f"ON BATTERY ({out[0]}%) - is it unplugged?")
    if ram < 1.5: bad.append(f"only {ram:.1f} GB RAM free")
    return ("OK", f"plugged in, battery {out[0]}%, {ram:.1f} GB RAM free") if not bad else ("BROKEN", "; ".join(bad))


def t_reboot(c):
    out = ps("(Test-Path 'HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\WindowsUpdate\\Auto Update\\RebootRequired') -or "
             "(Test-Path 'HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Component Based Servicing\\RebootPending')", 30)
    boot = ps("(Get-CimInstance Win32_OperatingSystem).LastBootUpTime.ToString('ddd MMM d h:mm tt')", 30)
    if out.lower() == "true":
        return "BROKEN", f"Windows wants a restart for updates (up since {boot}); pick a quiet time, not 3-8 AM (news)"
    return "OK", f"no restart pending (up since {boot})"


def t_dbsize(c):
    lines = open(os.path.join(STATE, "db-size.log"), encoding="utf-8", errors="replace").read().splitlines()
    last = lines[-1] if lines else ""
    m = re.search(r"\((\d+)%\)", last)
    if not m: return "BROKEN", "last size check could not reach the database: " + last[:100]
    pct = int(m.group(1))
    return ("OK", last.split("|", 1)[1].strip()[:110]) if pct < 75 else ("BROKEN", f"database at {pct}% of its cap - stop the heaviest writer first")


def t_logins(c):
    page = os.path.join(STATE, "logins.md")
    if c.since is not None and os.path.getmtime(page) < c.since:   # fix = a fresh, quiet re-check by login-watch itself
        return "BROKEN", "waiting for the fresh login check to finish"
    txt = open(page, encoding="utf-8", errors="replace").read()
    rows = [l for l in txt.split("\n| ") if l.startswith("NEEDS")]
    names = [r.split("|")[1].strip() for r in rows]
    stamp = (re.search(r"checked ([\d-]+ [\d:]+)", txt) or [None, "?"])[1]
    if not names: return "OK", f"all logins fine (checked {stamp})"
    return "BROKEN", "needs Jaron: " + ", ".join(names) + f" (checked {stamp}; steps in RECONNECT.md)"


def f_logins(c):
    subprocess.Popen([PY, os.path.join(ROOT, "tools", "login-watch.py"), "--quiet"], stdin=subprocess.DEVNULL,
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=NOWIN)
    return "re-ran tools/login-watch.py --quiet (a fresh check, no buzz)"


def t_git(path, branch):
    def t(c):
        sh(["git", "-C", path, "fetch", "-q"], 60)
        code, out, _ = sh(["git", "-C", path, "status", "-sb"], 30)
        head = out.splitlines()[0] if out else ""
        behind = re.search(r"behind (\d+)", head)
        ahead = re.search(r"ahead (\d+)", head)
        if not ahead and not behind: return "OK", f"in step with origin/{branch}"
        old = 0
        if ahead:
            ts = sh(["git", "-C", path, "log", f"origin/{branch}..HEAD", "--format=%ct"], 30)[1].split()
            old = (time.time() - min(int(x) for x in ts)) / 3600 if ts else 0
        if behind or old > 3:
            return "BROKEN", head.replace("## ", "") + (f" - oldest unpushed commit {old:.0f} h old" if ahead else "")
        return "OK", head.replace("## ", "") + " (recent; its own job pushes it)"
    return t


def t_public_copy(c):
    """Public scrubbed copy (tools/public_export.py, nightly 10:55 PM) reached GitHub in the last 48 h."""
    code, out, err = sh(["gh", "api", "repos/JaronKBragg7337/ai-shared-public", "--jq", ".pushed_at"], 30)
    if code != 0 or not out: return "BROKEN", "could not read GitHub pushed_at: " + (err or "no answer")[:120]
    try: pushed = datetime.fromisoformat(out.strip().replace("Z", "+00:00"))
    except ValueError: return "BROKEN", "odd pushed_at: " + out[:40]
    hours = (datetime.now(pushed.tzinfo) - pushed).total_seconds() / 3600
    last = ""
    try:
        lines = [l for l in open(os.path.join(ROOT, "state", "nightly-save.log"), encoding="utf-8", errors="replace") if " public: FLAGS:" in l]
        if lines: last = "; last nightly: " + lines[-1].split(" public: ", 1)[1].strip()[:120]
    except OSError: pass
    if hours <= 48: return "OK", f"pushed {hours:.0f} h ago" + last
    return "BROKEN", f"last push {hours / 24:.0f} days ago ({out.strip()[:10]})" + last


def t_gdrive(c):
    # 11/22: G: had been unmounted since 11/18 (Drive's own index kept going corrupt and a locked file stopped the rebuild), so the
    # nightly AI-Shared Mirror + Necklace Unreal Backup (robocopy to G:) failed while their tasks still said 0.
    if os.path.isdir(r"G:\My Drive") and not drive_corrupt_accounts():
        return "OK", r"G:\My Drive is mounted (nightly AI-Shared + Necklace backups can run)"
    running = "GoogleDriveFS" in ps("(Get-Process GoogleDriveFS -ErrorAction SilentlyContinue | Select-Object -First 1).ProcessName", 20)
    bad = drive_corrupt_accounts()
    return "BROKEN", ("Google Drive is " + ("running but G: is not mounted" if running else "not running") +
                      (" and marked its own index corrupt (the fix sets it aside and restarts Drive)" if bad else "") +
                      " - the nightly AI-Shared and Necklace backups to Drive can't run")


def drive_exe():
    """Newest installed GoogleDriveFS.exe (11/23: Drive updated itself 133.0.2.0 -> 134.0.1.0 and the old hard-coded path broke)."""
    base, found = r"C:\Program Files\Google\Drive File Stream", []
    for d in (os.listdir(base) if os.path.isdir(base) else []):
        exe = os.path.join(base, d, "GoogleDriveFS.exe")
        if os.path.isfile(exe):
            try: found.append((tuple(int(x) for x in d.split(".")), exe))
            except ValueError: pass
    return max(found)[1] if found else None


def drive_corrupt_accounts():
    """Drive account folders holding Drive's own 'metadata_sqlite_db_is_corrupted' marker (it writes it when its index breaks)."""
    root = os.path.expandvars(r"%LOCALAPPDATA%\Google\DriveFS")
    return [os.path.join(root, d) for d in (os.listdir(root) if os.path.isdir(root) else [])
            if os.path.isfile(os.path.join(root, d, "metadata_sqlite_db_is_corrupted"))]


def f_gdrive(c):
    # Not running -> start it. Running but unmounted WITH Drive's corruption marker -> do what Drive itself tries and fails to do
    # (11/23: its 8th corrupt index since 10/9; it fails to move the bad index aside because a file is still locked): stop Drive,
    # set the live index files aside as .bad-<stamp> (kept as evidence for the MSI data-error hunt), start Drive; it rebuilds the
    # index from the cloud. Running, unmounted, no marker (e.g. signed out) -> leave it for Claude.
    # 11/23 7:48 AM: a FRESH index went bad again 18 s after the reset, so a reset is not a cure: at most once a day, and the fix
    # waits a minute to see whether the new index holds before it says anything.
    exe = drive_exe()
    if not exe:
        return None
    alive = lambda: "GoogleDriveFS" in ps("(Get-Process GoogleDriveFS -ErrorAction SilentlyContinue | Select-Object -First 1).ProcessName", 20)
    bad = drive_corrupt_accounts()
    if alive() and not bad:
        return None
    if bad:
        reset_file = os.path.join(STATE, ".gdrive-reset.json")
        try: last = json.load(open(reset_file, encoding="utf-8")).get("at", 0)
        except Exception: last = 0
        if time.time() - last < 24 * 3600:
            return None
        json.dump({"at": time.time()}, open(reset_file, "w", encoding="utf-8"))
        ps("Get-Process GoogleDriveFS -ErrorAction SilentlyContinue | Stop-Process -Force", 30)
        for _ in range(30):
            if not alive(): break
            time.sleep(1)
        time.sleep(2)
        stamp, moved = datetime.now().strftime("%Y%m%d-%H%M"), 0
        for acct in bad:
            for f in os.listdir(acct):
                if f.startswith("metadata_sqlite_db") and ".bad-" not in f and ".corrupt." not in f:
                    try:
                        os.rename(os.path.join(acct, f), os.path.join(acct, f + ".bad-" + stamp)); moved += 1
                    except OSError as e:   # still locked: start Drive anyway (no worse than before) and leave the rest for Claude
                        sh(["powershell", "-NoProfile", "-Command", f"Start-Process '{exe}'"], 30)
                        return f"could not set Drive's corrupt index aside ({why(e)}); restarted Drive as it was"
    sh(["powershell", "-NoProfile", "-Command", f"Start-Process '{exe}'"], 30)
    if not bad:
        return "started Google Drive"
    for _ in range(30):   # does the new index hold for a minute?
        time.sleep(2)
        if drive_corrupt_accounts():
            return (f"set Drive's corrupt index aside ({moved} files, .bad-{stamp}) and restarted Drive, but it marked the NEW index "
                    "corrupt again within a minute - a reset can't fix this (left for Claude; MSI data-error hunt, open-list 0a)")
    return f"set Drive's corrupt index aside ({moved} files, kept as .bad-{stamp}) and restarted Drive; the new index held for a minute"


add("The machine", "Google Drive (G:)", "the off-MSI copy of AI-Shared and the Necklace project goes through it",
    r"G:\My Drive exists; if Drive isn't running, start it; if its own corruption marker is there, set the bad index aside first",
    t_gdrive, fix=f_gdrive, fix_how="start the newest GoogleDriveFS.exe; if Drive marked its index corrupt: stop Drive, rename the live index aside (.bad-<stamp>), start Drive",
    wait=15, wait_max=120)
add("The machine", "Disk space", "room for the nightly news render (~70 GB)", "shutil.disk_usage C:, wants >= 80 GB", t_disk)
add("The machine", "GPU heat", "the MSI isn't overheating", "nvidia-smi temperature, wants < 87C", t_gpu)
add("The machine", "Power and memory", "plugged in, enough RAM", "PowerStatus + Win32_OperatingSystem free memory", t_power)
add("The machine", "Windows restart pending", "updates waiting for a restart", "registry RebootRequired / RebootPending", t_reboot, phone=False)
add("The machine", "Database size", "Supabase stays under its 8 GB cap", "last line of state/db-size.log, wants < 75%", t_dbsize,
    fix=lambda c: "started task DB Size Check" if run_task("DB Size Check") else None, fix_how='schtasks /run "DB Size Check"', wait=30, wait_max=150)
add("The machine", "Logins", "every login the system uses still works", "state/logins.md NEEDS rows", t_logins,
    fix=f_logins, fix_how="python tools/login-watch.py --quiet (fresh re-check, no buzz)", wait=30, wait_max=300, phone=False)
add("The machine", "AI-Shared saved to GitHub", "this folder is backed up", "git fetch + status -sb (AI-Shared, main)", t_git(ROOT, "main"), phone=False)
add("The machine", "Public copy pushed in the last 48 hours", "the scrubbed public AI-Shared reaches GitHub nightly",
    "gh api repos/JaronKBragg7337/ai-shared-public .pushed_at + last FLAGS line in state/nightly-save.log", t_public_copy, phone=False)
add("The machine", "Watch repo saved to GitHub", "the news watch repo is pushed", "git fetch + status -sb (Projects/watch, master)", t_git(os.path.join(os.path.dirname(ROOT), "Projects", "watch"), "master"), phone=False)


# ---------------------------------------------------------------- 5. scheduled jobs
def t_job(name, every, window=None):
    def t(c):
        info = task(name, fresh=c.since is not None)
        if not info: return "BROKEN", "task is missing"
        if info["s"] == "Disabled": return "BROKEN", "task is disabled"
        if c.since is not None:   # after a re-run (or while waiting for its next tick) only a newer, finished run counts
            if ago(info["l"]) * 60 > time.time() - c.since + 5 or info["s"] == "Running":
                return "BROKEN", f"waiting for a fresh run (last {info['l'][11:16]}, result {info['r']})"
        if window and not (window[0] <= datetime.now().hour < window[1]):
            return "OK", f"only runs {window[0]}-{window[1]}h; last {info['l'][5:16].replace('T', ' ')} result {info['r']}"
        if info["r"] not in TASK_OK:
            return "BROKEN", f"last run {info['l'][5:16].replace('T', ' ')} ended with {info['r']}"
        late = ago(info["l"])
        if late > max(3 * every, every + 30) and info["s"] != "Running":
            return "BROKEN", f"hasn't run since {info['l'][5:16].replace('T', ' ')} (should run every {every} min)"
        return "OK", f"last run {info['l'][5:16].replace('T', ' ')}, result {info['r']}"
    return t


def f_rerun(name, guard=None):
    def f(c):
        if guard and not guard(): return None
        if "task is missing" in c.detail or "task is disabled" in c.detail: return None
        return f"re-ran task {name}" if run_task(name) else None
    return f


def f_next_tick(c):
    return "not re-run (money side); waited for its own next run"


# (name, every N minutes, mode, purpose). mode: rerun = safe to start by hand (it's just an early tick);
# tick = money side: never started by this check, but wait for its own next run; report = list only.
JOBS = [
    ("HB Watch Loop", 1, "rerun", "answers Jaron's \"Tell Claude\" watch messages by ntfy"),
    ("HB Key Drop", 1, "rerun", "files and tests API keys Jaron pastes on his phone"),
    ("Crypto Consensus", 1, "tick", "crypto decision tick (money side)"),
    ("Crew Publish", 5, "rerun", "publishes the public system/crew page"),
    ("MSI Beat", 5, "rerun", "checks in with the off-MSI alarm on Cloudflare (quiet 20 min = one buzz)"),
    ("HB Video Drop", 5, "rerun", "picks up videos dropped for the site"),
    ("HB Price Alerts", 5, "tick", "price alerts (money side)"),
    ("Live Board", 5, "tick", "the live data board"),
    ("Crypto Notify", 10, "report", "crypto notices (money side)"),
    ("Usage Snapshot", 15, "rerun", "the AI usage meter"),
    ("Desk Schedule Watch", 15, "report", "desk schedule check (money side)"),
    ("Twin Crypto Settle", 15, "report", "settles the twin's paper crypto (money side)"),
    ("HB News Watchdog", 15, "rerun", "buzzes if today's news isn't live (7 AM-noon)"),
    ("MSI Connector Watch", 30, "rerun-guarded", "buzzes if the connector/Cosmos/relay is down"),
    ("Creature Watch", 30, "rerun", "looks in on the creature (read-only)"),
    ("HB Safety Signal", 30, "rerun", "safety level from the DHS feed"),
    ("MSI Status", 30, "rerun", "writes state/MSI-STATUS.md"),
    ("Sapling Watch", 30, "report", "watches Sapling (read-only)"),
    ("Sapling Wake", 30, "report", "Sapling's own wake"),
    ("DB Size Check", 60, "rerun", "database size vs the 8 GB cap"),
    ("MSI Health", 60, "report", "hourly task/port health"),
    ("HB AI Fund", 60, "report", "AI fund (money side)"),
]
GROUPS = [   # (row name, purpose, every N minutes, [tasks])
    ("Hourly helpers", "live readings, news desks, rolling wire, prep watch", 60,
     ["HB Live Readings", "HB News Desks", "Watch Rolling Wire", "HB Prep Watch"]),
    ("Nightly news pipeline", "GPU guard 2:38, render 3:50, writer 4:20, paper book 9:05, socials 7:15/8:45/5 PM", 1560,
     ["HB News GPU Guard", "HB Rendered News", "Heartbeat News Writer", "HB News Paper Book", "HB Socials News", "HB Socials News Retry", "HB Socials Show"]),
    ("Nightly news collectors", "the Watch ... collectors and What's New scouts", 1560,
     ["Watch Claude Desk", "Watch Codex Writer", "Watch Funding Lane", "Watch MSI Reader", "Watch Kimi First Light", "Watch Grok Meridian",
      "Watch Grok Blind Spots", "Watch DeepSeek Reader", "Watch Perplexity Scout", "Watch Missed Story Check", "Watch Source Gate",
      "Watch Source Gate Final", "Watch Top Stories", "Whats New Scouts"]),
    ("Backups and saves", "Drive mirror 3:30, nightly save 22:55, creature 21:15, Unreal 3:00, Sapling GitHub 18:17, Drive gentle fill 21:00", 1560,
     ["AI-Shared Mirror", "AI-Shared Nightly Save", "Creature Backup", "Necklace Unreal Backup", "Sapling GitHub Sync", "Drive Gentle Fill"]),
    ("Other daily jobs", "login watch, usage ledger, build ledger, render maintainer, firsts, Sapling status, atlas", 1560,
     ["Login Watch", "HB Usage Ledger", "HB Build Ledger", "HB Render Maintainer", "Firsts Roundup", "Sapling Status", "HB Atlas Convergence", "Sapling Quiet Switch"]),
    ("Weekly jobs", "stale sweep, AI fund review, budget report, edge check, crypto caps", 8 * 1440,
     ["Stale Sweep", "HB AI Fund Weekly Review", "AI Budget Report", "Edge Check", "Crypto Weekly Caps"]),
]
OFF_POLY = ["Trade Executor", "Trade Proposer", "Polymarket Watchdog", "Crypto Wake", "Scout Scorer"]
OFF_PAUSED = ["Fly Brain", "Fly Watcher", "Fly School", "Fly School school-2", "Fly School school-3", "Fly School school-4", "Fly School school-5",
              "AgentWorkbench-Scheduler", "AgentWorkbench-Server", "Qwen Remote Bridge", "OpenClaw Paper Gateway", "Paper Sync",
              "Revenue Desk Daily", "Desk Weekly Review", "HB Fog Book Research", "MachineManager", "Unfinished Island - hourly world worker",
              "Heartbeat Courier", "Postiz Trial Check 10-23", "HB Socials Outage Retry"]
KNOWN_ELSEWHERE = {"Grok Machine MCP", "Ollama Server", "OpenClaw Gateway", "Sapling Heartbeat", "Sapling Relay", "Desktop Commander Remote",
                   "HB Remote Keepalive", "HB Remote Screen", "HB Render Owner Worker", "Polymarket MCP", "Trade Verifier", "All Systems Check"}
ONE_SHOT = re.compile(r"^(Bday |Court |Remind|HB Reminder|HB Moment|HB BMV|CS Callback|Luna |Sapling Parole|Sapling Conversation)")
VENDOR = re.compile(r"^(Nv|NVIDIA|OneDrive|OneDC|Nahimic|OmApSvc|iGoAudio|Google|Adobe|Opera|CCleaner|Microsoft|npcap|MicrosoftEdge)", re.I)

for name, every, mode, purpose in JOBS:
    window = (7, 12) if name == "HB News Watchdog" else None
    if mode == "rerun":
        add("Scheduled jobs", name, purpose, f"task {name}: last result ok and ran within {max(3 * every, every + 30)} min",
            t_job(name, every, window), fix=f_rerun(name), fix_how=f'schtasks /run "{name}" (an early tick)', wait=15, wait_max=200)
    elif mode == "rerun-guarded":
        add("Scheduled jobs", name, purpose, f"task {name}: last result ok and ran within {3 * every} min",
            t_job(name, every), fix=f_rerun(name, guard=connector_watch_safe),
            fix_how=f'schtasks /run "{name}" - only while its Polymarket restart branch is off (or 8765 is held), so it cannot start Polymarket', wait=30, wait_max=330)
    elif mode == "tick":
        add("Scheduled jobs", name, purpose, f"task {name}: last result ok (never started by this check)",
            t_job(name, every), fix=f_next_tick, fix_how="none - money side; waits for its own next run", wait=30, wait_max=every * 60 + 90, phone=False)
    else:
        add("Scheduled jobs", name, purpose, f"task {name}: last result ok and ran within {max(3 * every, every + 30)} min",
            t_job(name, every), phone=False)


def t_group(names, every):
    def t(c):
        bad = []
        for n in names:
            info = task(n)
            if not info: bad.append(f"{n} missing"); continue
            if info["s"] == "Disabled": bad.append(f"{n} disabled"); continue
            if info["r"] not in TASK_OK: bad.append(f"{n} ended {info['r']} ({info['l'][5:16].replace('T', ' ')})")
            elif ago(info["l"]) > every and info["s"] != "Running": bad.append(f"{n} last ran {info['l'][5:16].replace('T', ' ')}")
        return ("OK", f"all {len(names)} ran on time and finished ok") if not bad else ("BROKEN", "; ".join(bad))
    return t


for row, purpose, every, names in GROUPS:
    add("Scheduled jobs", row, purpose, "tasks: " + ", ".join(names), t_group(names, every), phone=False)


def t_other(c):
    listed = {j[0] for j in JOBS} | {n for g in GROUPS for n in g[3]} | set(OFF_POLY) | set(OFF_PAUSED) | KNOWN_ELSEWHERE
    bad = []
    for n, info in sorted(_tasks.items()):
        if n in listed or ONE_SHOT.match(n) or VENDOR.match(n) or info["s"] == "Disabled": continue
        if info["r"] not in TASK_OK and ago(info["l"]) < 2 * 1440:
            bad.append(f"{n} ended {info['r']} ({info['l'][5:16].replace('T', ' ')})")
    return ("OK", "no other job failed in the last 2 days") if not bad else ("BROKEN", "; ".join(bad))


add("Scheduled jobs", "Any other job", "catches failures in jobs not listed above (vendor and one-shot reminders skipped)", "every enabled root task, result in last 2 days", t_other, phone=False)


# ---------------------------------------------------------------- 6. off on purpose
def t_poly(c):
    on = [n for n in OFF_POLY if (task(n) or {}).get("s") not in (None, "Disabled")]
    mcp = task("Polymarket MCP") or {}
    tv = task("Trade Verifier") or {}
    who = has_proc("http.server", "8765")
    note = (f"trading tasks still disabled; Polymarket MCP task {mcp.get('s', '?')} (last run {mcp.get('l', '?')[:10]}); "
            f"Trade Verifier still scheduled and ends {tv.get('r', '?')} because nothing real answers on 8765")
    try: note += f" (state/verifier.md {os.path.getsize(os.path.join(STATE, 'verifier.md')) / 1e6:.1f} MB)"
    except OSError: pass
    if who: note += "; 8765 is held by a leftover preview web server (`python -m http.server 8765`), not Polymarket"
    elif port_open(8765): note += "; NOTE something else is on 8765 - is Polymarket MCP running again?"
    note += ("; NOTE tools/connector-watch.py would still restart Polymarket MCP when 8765 is free" if poly_restart_on()
             else "; Connector Watch's Polymarket restart is off")
    if on: note += "; NOTE enabled again: " + ", ".join(on)
    return "SKIPPED-ON-PURPOSE", "Polymarket system is DOWN by Jaron's 10/28 decision - never restarted here; " + note


def t_paused(c):
    on = [n for n in OFF_PAUSED if (task(n) or {}).get("s") not in (None, "Disabled")]
    return "SKIPPED-ON-PURPOSE", f"{len(OFF_PAUSED)} paused tasks (fly brain, old gateways, retired desks)" + ("; NOTE enabled again: " + ", ".join(on) if on else ", all still off")


def t_codex_observer(c):
    return "SKIPPED-ON-PURPOSE", "Codex Observer server + tunnel (Registry Run entries) - not checked; ask Jaron if still wanted"


add("Off on purpose", "Polymarket system", "trading on Polymarket is off since 10/28", "task states of " + ", ".join(OFF_POLY) + ", Polymarket MCP, Trade Verifier", t_poly)
add("Off on purpose", "Paused projects", "fly brain and retired helpers stay off", "task states of the paused list", t_paused)
add("Off on purpose", "Codex Observer", "an old Codex side project", "not checked", t_codex_observer)


# ---------------------------------------------------------------- run, fix, re-check, report
def mins(s):
    return f"{s / 60:.1f} min" if s >= 90 else f"{s:.0f} s"


def write_report(stamp, summary, dry):
    groups = []
    for c in CHECKS:
        if c.group not in groups: groups.append(c.group)
    out = [f"<!-- run -->", f"## {stamp} - {summary}" + ("  (dry run: nothing restarted)" if dry else ""), ""]
    broken = [c for c in CHECKS if c.status == "BROKEN"]
    fixed = [c for c in CHECKS if c.status == "FIXED"]
    if broken:
        out.append("**Still broken:**")
        out += [f"- **{c.name}** - {c.detail}" + ("" if c.phone else " _(not sent to the phone; listed for Claude)_") for c in broken]
        out.append("")
    if fixed:
        out.append("**Fixed this run:**")
        out += [f"- **{c.name}** - was: {c.first}. {c.did}. Now: {c.detail}" for c in fixed]
        out.append("")
    for g in groups:
        out += [f"**{g}**", "", "| Result | Part | What it's for | Detail |", "|---|---|---|---|"]
        for c in CHECKS:
            if c.group == g:
                out.append(f"| {c.status} | {c.name} | {c.purpose} | {c.detail.replace('|', '/')} |")
        out.append("")
    head = ("# Everything check - is every part of the MSI OK? (newest run on top)\n\n"
            "Runs by itself: daily 7:45 AM, after a restart, and when the network comes back (task \"All Systems Check\", "
            "tools/all_systems_check.py). It restarts only what is safe, through each part's own task, and buzzes Jaron "
            "only if something is still broken after that. `--why` lists every check.\n\n")
    old = ""
    if os.path.exists(MD):
        txt = open(MD, encoding="utf-8", errors="replace").read()
        runs = txt.split("<!-- run -->")[1:]
        old = "".join("<!-- run -->" + r for r in runs[:5])
    tmp = MD + ".tmp"
    open(tmp, "w", encoding="utf-8").write(head + "\n".join(out) + "\n" + old)
    os.replace(tmp, MD)


def buzz(broken):
    names = sorted(c.name for c in broken)
    try: sent = json.load(open(BUZZED, encoding="utf-8"))
    except Exception: sent = {}
    key = "|".join(names)
    if key in sent and time.time() - sent[key] < 3 * 3600: return "same list already buzzed in the last 3 h"
    topic = secret("NTFY_TOPIC")
    if not topic: return "no NTFY_TOPIC"
    msg = "Still broken after a fix try: " + "; ".join(f"{c.name} ({c.detail[:70]})" for c in broken)
    msg = msg[:380] + " - full list in state/all-systems.md"
    try:
        urllib.request.urlopen(urllib.request.Request("https://ntfy.sh/" + topic, data=msg.encode("utf-8"),
                                                      headers={"Title": "MSI check", "Priority": "high"}), timeout=20)
    except Exception:
        return "buzz failed (no internet?)"   # never print the URL: it holds the private topic
    sent = {k: v for k, v in sent.items() if time.time() - v < 86400}
    sent[key] = time.time()
    json.dump(sent, open(BUZZED, "w", encoding="utf-8"))
    return "buzzed"


MAILED = os.path.join(STATE, ".all-systems-mail.json")


def mail(subject, body, key):
    # The network trigger can fire many times on a flaky-WiFi day: the same result is mailed at most once every 3 hours.
    try: sent = json.load(open(MAILED, encoding="utf-8"))
    except Exception: sent = {}
    if key in sent and time.time() - sent[key] < 3 * 3600: return "same result already mailed in the last 3 h"
    try:
        sys.path.insert(0, os.path.join(ROOT, "tools"))
        from mailbox import request
        request("POST", data={"from_ai": "all-systems", "to_ai": "claude", "subject": subject, "body": body})
        sent = {k: v for k, v in sent.items() if time.time() - v < 86400}
        sent[key] = time.time()
        json.dump(sent, open(MAILED, "w", encoding="utf-8"))
        return "mailed Claude"
    except Exception as e:
        return "mail failed: " + why(e)


def main():
    if "--why" in sys.argv:
        for c in CHECKS:
            print(f"[{c.group}] {c.name} - {c.purpose}\n    check: {c.how}\n    safe fix: {c.fix_how or 'none (report only)'}"
                  f"{'' if c.phone else '   (never buzzes)'}")
        print(f"\n{len(CHECKS)} checks.")
        return 0
    if not DRY:
        if os.path.exists(LOCK) and time.time() - os.path.getmtime(LOCK) < 20 * 60:
            print("another run is going (lock under 20 min old) - skipping"); return 0
        open(LOCK, "w").write(str(os.getpid()))
    try:
        return _run()
    finally:
        if not DRY and os.path.exists(LOCK): os.remove(LOCK)


def _run():
    # After a WiFi drop the network can take a minute; give it up to 3 min before calling everything broken.
    for i in range(7 if not DRY else 1):
        if t_internet(None)[0] == "OK" or DRY: break
        time.sleep(30)
    load_tasks()
    procs()
    for c in CHECKS:
        c.run()
        c.first = c.detail
        print(f"{c.status:20} {c.name}: {c.detail}")
    pending = []
    if not DRY:
        for c in CHECKS:
            if c.status == "BROKEN" and c.fix:
                c.since = time.time()
                try: c.did = c.fix(c) or ""
                except Exception as e: c.did = ""
                if c.did: pending.append(c); print("fix:", c.name, "->", c.did)
                else: c.since = None
        start = time.time()
        while pending:
            time.sleep(10)
            for c in list(pending):
                el = time.time() - c.since
                if el < c.wait: continue
                if c.run() == "OK":
                    c.status = "FIXED"; pending.remove(c)
                elif el >= c.wait_max:
                    c.detail += f" (still broken after {c.did.lower()}; waited {mins(el)})"; pending.remove(c)
            if time.time() - start > 420: break
    ok = [c for c in CHECKS if c.status == "OK"]
    fixed = [c for c in CHECKS if c.status == "FIXED"]
    broken = [c for c in CHECKS if c.status == "BROKEN"]
    skipped = [c for c in CHECKS if c.status == "SKIPPED-ON-PURPOSE"]
    summary = "All good" if not broken else f"{len(broken)} broken: " + ", ".join(c.name for c in broken)
    if fixed: summary += f" ({len(fixed)} fixed: " + ", ".join(c.name for c in fixed) + ")"
    stamp = datetime.now().strftime("%a %b %d %I:%M %p")
    write_report(stamp, summary, DRY)
    result = {"at": datetime.now().isoformat(timespec="seconds"), "dry": DRY, "summary": summary, "took_s": round(time.time() - T0),
              "counts": {"ok": len(ok), "fixed": len(fixed), "broken": len(broken), "skipped": len(skipped)},
              "checks": [{"group": c.group, "name": c.name, "purpose": c.purpose, "result": c.status, "detail": c.detail,
                          "was": c.first if c.status == "FIXED" else "", "fix_done": c.did, "buzzes": c.phone} for c in CHECKS]}
    phone = [c for c in broken if c.phone]
    if not DRY:
        line = (f"{len(ok)} OK, {len(fixed)} fixed, {len(broken)} broken, {len(skipped)} off on purpose. "
                + (("Broken: " + "; ".join(f"{c.name} - {c.detail[:90]}" for c in broken) + ". ") if broken else "")
                + (("Fixed: " + ", ".join(c.name for c in fixed) + ". ") if fixed else "") + "Full list: state/all-systems.md")
        result["mail"] = mail("MSI check: " + ("all good" if not broken else f"{len(broken)} broken"), line,
                              "|".join(sorted(c.name for c in broken)) + "#" + "|".join(sorted(c.name for c in fixed)))
        result["buzz"] = buzz(phone) if phone else "no buzz (nothing broken that needs Jaron)"
    tmp = JS + ".tmp"
    json.dump(result, open(tmp, "w", encoding="utf-8"), indent=1)
    os.replace(tmp, JS)
    print(f"\n{summary}  [{mins(time.time() - T0)}]" + (f"  mail: {result.get('mail')}  buzz: {result.get('buzz')}" if not DRY else "  (dry)"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
