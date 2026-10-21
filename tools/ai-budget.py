# The AI budget report - step 1 of Jaron's plan (9/29): the system watches each AI's cost, usage and output, next to what
# the trader earns, so that within ~3 months it can say "this month we need this plan, not that one" and pay for it itself.
#   cost:     state/subscriptions.json (monthly plans)            target: Control Room row builder_toolset_target
#   usage:    state/usage-live.json (Claude estimate, Codex meter) + state/grok-usage.md (Jaron's Grok meter readings)
#   output:   commits per AI this month, from the Co-Authored-By lines in every git repo under C:/Users/lilli/Projects
#   earnings: tools/grok-money.py (the trader's settled profit this month)
# Writes state/ai-budget.md. Run any time; the weekly task runs it Monday mornings.
import json, os, re, subprocess, sys, collections
from datetime import datetime, timezone, timedelta

ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
from settings import setting  # noqa: E402

ET = timezone(timedelta(hours=-4))
now = datetime.now(ET)
month0 = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
S = lambda *p: os.path.join(ROOT, "state", *p)


def load(path, default):
    try:
        return json.load(open(path, encoding="utf-8-sig"))
    except Exception:
        return default


subs = load(S("subscriptions.json"), {})
usage = load(S("usage-live.json"), {})

# --- usage, as "% of this week's allowance used"
use = {}
c = usage.get("claude", {}).get("week", {})
if c.get("est_used_pct") is not None:
    use["Claude"] = f"{c['est_used_pct']:.0f}% of the week (estimate from local logs)"
x = usage.get("codex", {})
if x.get("weekly_used_pct") is not None:
    use["Codex"] = f"{x['weekly_used_pct']:.0f}% of the week (meter), resets {x.get('weekly_resets_at', '')[:10]}"
g = None
try:
    for line in open(S("grok-usage.md"), encoding="utf-8"):
        m = re.match(r"(\d{4}-\d{2}-\d{2})\s*\|\s*(\d+)%\s*\|\s*(.*)", line)
        if m:
            g = m
    if g:
        use["Grok"] = f"{g[2]}% of the week on {g[1]} ({g[3].strip()}) - Jaron's reading"
except OSError:
    pass

# --- output: commits this month per AI, across every repo in Projects
out = collections.Counter()
proj = r"C:\Users\lilli\Projects"
for d in sorted(os.listdir(proj)):
    p = os.path.join(proj, d)
    if not os.path.isdir(os.path.join(p, ".git")) and not os.path.isfile(os.path.join(p, ".git")):
        continue
    try:
        log = subprocess.run(["git", "-C", p, "log", "--all", f"--since={month0:%Y-%m-%d}", "--format=%(trailers:key=Co-Authored-By,valueonly)%x1e"],
                             capture_output=True, text=True, timeout=60).stdout
    except Exception:
        continue
    seen = set()
    for block in log.split("\x1e"):
        for who in block.strip().splitlines():
            name = re.sub(r"\s*<.*", "", who).strip()
            if name:
                out[name] += 1
fam = collections.Counter()
for k, v in out.items():
    fam["Claude" if k.startswith("Claude") else "Codex" if "codex" in k.lower() or "gpt" in k.lower() else k] += v

# --- earnings: the trader's settled profit this month
earn = None
try:
    subprocess.run([sys.executable, os.path.join(ROOT, "tools", "grok-money.py")], capture_output=True, timeout=180)
    for line in open(S("grok-money.md"), encoding="utf-8"):
        if line.startswith(f"| {now:%Y-%m} |"):
            earn = line.split("|")[2].strip()
except Exception:
    pass

# --- report
bills = sum(float(r.get("usd") or 0) for r in subs.get("monthly", []))
L = [f"# AI budget report - {now:%Y-%m-%d %H:%M} ET (tools/ai-budget.py)", "",
     "Step 1 of Jaron's plan (9/29): measure cost, usage and output per AI next to what the trader earns. Step 2 (after ~1-2",
     "months of data): the report recommends next month's plans. Step 3: the system pays and changes plans itself.", "",
     "## Money", "",
     f"- Monthly bills on record: ${bills:.0f} ({', '.join(f'{r.get(chr(110)+chr(97)+chr(109)+chr(101))} ${r.get(chr(117)+chr(115)+chr(100))}' for r in subs.get('monthly', []))})",
     f"- Trader's settled profit this month: {earn or 'n/a'}",
     f"- Target (Jaron): {setting('builder_toolset_target', 'not set')}", "",
     "## Each AI this month", "", "| AI | plan | usage (latest) | commits this month |", "|---|---|---|---|"]
plans = {"Claude": "Claude", "Codex": "ChatGPT", "Grok": "Grok"}
for ai, key in plans.items():
    plan = next((f"{r.get('plan')} ${r.get('usd')}" for r in subs.get("monthly", []) if key.lower() in r.get("name", "").lower()), "?")
    L.append(f"| {ai} | {plan} | {use.get(ai, 'not measured')} | {fam.get(ai, 0)} |")
L += ["", "Commits by model: " + ", ".join(f"{k} {v}" for k, v in out.most_common()) if out else "", "",
      "## What the numbers say (automatic, plain rules)", ""]
flags = []
for ai, txt in use.items():
    m = re.match(r"(\d+)%", txt)
    if not m:
        continue
    p = int(m[1])
    if p >= 80:
        flags.append(f"- {ai} is at {p}% of its week: it is being used to the limit - a bigger plan would get used.")
    elif p <= 20:
        flags.append(f"- {ai} is at {p}% of its week: lots of room left - point more work at it before paying for more.")
L += flags or ["- Nothing stands out yet."]
L += ["", "Grok Bot's own usage is not readable by a script; add each reading to state/grok-usage.md."]
open(S("ai-budget.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
print("\n".join(L))
