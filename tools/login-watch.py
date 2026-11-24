"""login-watch.py - checks every login/connection the system depends on, writes state/logins.md, and buzzes Jaron's phone
(ntfy) when one is broken or about to run out, naming the RECONNECT.md section to follow (2026-10-08, Claude Code).

Jaron: "there's gonna be random days things just disconnect and I'm unaware until I get to the MSI." Runs as the Windows task
"Login Watch" (daily 5:50 AM; runs late after a restart). No secrets are printed; only names and dates.
  python tools/login-watch.py          # check, write state/logins.md, buzz on problems (once a day per problem)
  python tools/login-watch.py --quiet  # check and write the page, no buzz
"""
import json, os, subprocess, sys, time, urllib.request
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
HOME = os.path.expanduser("~")
PAGE = os.path.join(ROOT, "state", "logins.md")
SENT = os.path.join(ROOT, "state", "login-alerts.log")
WARN_DAYS = 5


def keys():
    env = {}
    for line in open(os.path.join(HOME, ".secrets", "keys.env"), encoding="utf-8-sig"):
        if "=" in line and not line.lstrip().startswith("#"):
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"')
    return env


def days_left(ts):
    return (ts - time.time()) / 86400


def sh(cmd, env=None, timeout=90):
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout,
                           env={**os.environ, **(env or {})}, shell=isinstance(cmd, str))
        return p.returncode, (p.stdout + p.stderr).strip()
    except Exception as e:
        return 1, str(e)


# each check returns (name, ok, detail, how-long-it-lasts, RECONNECT section)
def claude_jobs():
    tok = keys().get("CLAUDE_CODE_OAUTH_TOKEN")
    if not tok:
        return False, "no token saved"
    rc, out = sh(["claude", "--model", "haiku", "-p", "Reply with just: ok"], {"CLAUDE_CODE_OAUTH_TOKEN": tok}, 120)
    return ("ok" in out.lower() and "error" not in out.lower()), "answered" if "ok" in out.lower() else out[:120]


def codex():
    rc, out = sh(["codex", "login", "status"])
    return rc == 0 and "not logged" not in out.lower(), out.splitlines()[0][:100] if out else "no answer"


def grok_cli():
    f = os.path.join(HOME, ".grok", "auth.json")
    if not os.path.exists(f):
        return False, "no login file"
    d = json.load(open(f, encoding="utf-8"))
    has_refresh = any(isinstance(v, dict) and v.get("refresh_token") for v in d.values())
    age = days_left(os.path.getmtime(f)) * -1
    return has_refresh, f"refreshes itself when used; last refreshed {age:.0f} days ago"


def connector_signins():
    f = os.path.expandvars(r"%LOCALAPPDATA%\GrokMachineMcp\oauth-state.json")
    st = json.load(open(f, encoding="utf-8"))
    names = {c["client_id"]: c["client_name"] for c in st["clients"].values()}
    best = {}
    for r in st["refreshTokens"].values():
        n = names.get(r["client_id"], "?")
        best[n] = max(best.get(n, 0), r["expires_at"])
    out = []
    for app, label in [("Claude", "Claude chat -> MSI connector (Heartbeat MAI)"), ("Grok", "Grok chat -> MSI connector (Grok Machine)"),
                       ("Cursor", "Grok Bot -> MSI connector (msi-heartbeat)")]:
        e = best.get(app)
        if not e:
            out.append((label, False, "not signed in", "30 days from last use, renews when used", 3))
        else:
            d = days_left(e)
            out.append((label, d > WARN_DAYS, f"signed in until {datetime.fromtimestamp(e):%b %d} ({d:.0f} days)",
                        "30 days from last use, renews when used", 3))
    return out


def desktop_commander():
    rc, out = sh('powershell -NoProfile -Command "@(Get-CimInstance Win32_Process | Where-Object { $_.Name -eq \'node.exe\' -and $_.CommandLine -match \'commander\' -and $_.CommandLine -match \' remote\' }).Count"')
    n = int(out.strip() or 0) if out.strip().isdigit() else 0
    return n > 0, "running" if n else "not running (stops at every restart)"


def chatgpt_heartbeat():
    # ChatGPT's daily scheduled task (9 PM) appends a line here through Desktop Commander. No line in 30 hours = the task
    # didn't run or couldn't reach the MSI. Only checked once the file exists (Jaron 10/8: "if it doesn't go off, that's the sign").
    f = os.path.join(ROOT, "state", "chatgpt-heartbeat.md")
    if os.path.exists(os.path.join(ROOT, "state", "chatgpt-heartbeat.PAUSED")):
        return True, "paused: scheduled ChatGPT tasks can't reach the MSI (2 nights, 10/8-10/9); normal chats can"
    if not os.path.exists(f):
        first_due = datetime(2026, 10, 9, 3, 0).timestamp()   # first run was due 10/8 9 PM; give it 6 h
        if time.time() < first_due:
            return True, "not set up yet (waiting for the first daily run)"
        return False, "never checked in - the 9 PM ChatGPT task has not written its file yet (task off, or it can't reach the MSI)"
    hours = (time.time() - os.path.getmtime(f)) / 3600
    return hours < 30, f"last check-in {hours:.0f} hours ago"


def github():
    rc, out = sh(["gh", "auth", "status"])
    return rc == 0, "logged in" if rc == 0 else out[:100]


def deepseek():
    k = keys().get("DEEPSEEK_API_KEY")
    r = urllib.request.Request("https://api.deepseek.com/user/balance", headers={"Authorization": f"Bearer {k}"})
    d = json.load(urllib.request.urlopen(r, timeout=30))
    bal = sum(float(b.get("total_balance", 0)) for b in d.get("balance_infos", []))
    return bal > 1, f"${bal:.2f} left"


def anthropic_api():
    k = keys()
    h = {"x-api-key": k["ANTHROPIC_API_KEY"], "anthropic-version": "2023-06-01"}
    if k.get("ANTHROPIC_WORKSPACE_ID"):
        h["anthropic-workspace-id"] = k["ANTHROPIC_WORKSPACE_ID"]
    urllib.request.urlopen(urllib.request.Request("https://api.anthropic.com/v1/models", headers=h), timeout=30)
    return True, "key works (credit balance isn't readable by key; check console.anthropic.com)"


def run_all():
    rows = []
    def add(name, fn, lasts, sec):
        try:
            ok, detail = fn()
        except Exception as e:
            ok, detail = False, f"check failed: {str(e)[:100]}"
        rows.append((name, ok, detail, lasts, sec))
    add("Claude login for MSI jobs (scout)", claude_jobs, "about 1 year (made 2026-10-08)", 1)
    add("Codex (Luna/Sol) login", codex, "renews itself when used; re-login if unused for weeks", 2)
    add("Grok Build login", grok_cli, "renews itself when used", 6)
    try:
        rows += connector_signins()
    except Exception as e:
        rows.append(("MSI connector sign-ins", False, f"check failed: {e}", "30 days from last use", 3))
    add("ChatGPT -> MSI (Desktop Commander remote)", desktop_commander, "until the MSI restarts or the window closes", 7)
    add("ChatGPT daily task (bank ledger + check-in)", chatgpt_heartbeat, "should check in every night at 9 PM", 7)
    add("GitHub (site deploys)", github, "stays until revoked", 0)
    add("DeepSeek API (balance)", deepseek, "until the money runs out", 5)
    add("Claude API key", anthropic_api, "until revoked; credit can run out", 5)
    return rows


def main():
    rows = run_all()
    now = datetime.now()
    lines = [f"# Logins and connections - checked {now:%Y-%m-%d %H:%M} (tools/login-watch.py, daily 5:50 AM)", "",
             "| | What | Status | Lasts | Fix (RECONNECT.md) |", "|---|---|---|---|---|"]
    for name, ok, detail, lasts, sec in rows:
        lines.append(f"| {'OK' if ok else 'NEEDS YOU'} | {name} | {detail} | {lasts} | {('section ' + str(sec)) if sec else 'tell Claude'} |")
    open(PAGE, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print("\n".join(lines))
    bad = [r for r in rows if not r[1]]
    if not bad or "--quiet" in sys.argv:
        return
    today = f"{now:%Y-%m-%d}"
    sent = open(SENT, encoding="utf-8").read() if os.path.exists(SENT) else ""
    fresh = [r for r in bad if f"{today} {r[0]}" not in sent]
    if not fresh:
        return
    msg = "\n".join(f"- {r[0]}: {r[2]} -> RECONNECT.md section {r[4]}" if r[4] else f"- {r[0]}: {r[2]} -> tell Claude" for r in fresh)
    topic = keys().get("NTFY_TOPIC")
    urllib.request.urlopen(urllib.request.Request("https://ntfy.sh/" + topic, data=("Needs you at the MSI:\n" + msg).encode(),
                                                  headers={"Title": "Login watch", "Priority": "high"}), timeout=20)
    with open(SENT, "a", encoding="utf-8") as f:
        for r in fresh:
            f.write(f"{today} {r[0]}\n")


if __name__ == "__main__":
    main()
