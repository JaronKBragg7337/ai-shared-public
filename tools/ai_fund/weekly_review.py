"""AI Fund Desk - weekly deep review by Fable 5.2 (Windows task "HB AI Fund Weekly Review", Sundays 05:00).

Jaron 11/15: Fable is the weekly deep reviewer (the step that may propose CODE changes); the hourly judgement stays on a
cheap model. Fable has its own usage limit, so this is ONE deep call a week. Fable writes a proposal file only:
projects/ai-fund/proposals/YYYY-MM-DD.md. It does not edit code or config; Claude applies accepted proposals and re-runs
the backtest + frozen twin before they count (Qwen's skeptic point). A mailbox note tells Claude the proposal is ready.
    python tools/ai_fund/weekly_review.py [--dry]
"""
import os
import subprocess
import sys
from datetime import datetime

HERE = os.path.dirname(os.path.realpath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
PROPOSALS = os.path.join(ROOT, "projects", "ai-fund", "proposals")
SECRETS = os.path.join(os.path.expanduser("~"), ".secrets", "keys.env")
CLAUDE = os.path.join(os.path.expanduser("~"), ".local", "bin", "claude.exe")
LOG = os.path.join(ROOT, "state", "ai-fund", "runs.log")


def token():
    for line in open(SECRETS, encoding="utf-8"):
        if line.startswith("CLAUDE_CODE_OAUTH_TOKEN="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None


def main(dry=False):
    day = datetime.now().strftime("%Y-%m-%d")
    os.makedirs(PROPOSALS, exist_ok=True)
    out = os.path.join(PROPOSALS, f"{day}.md")
    brief = f"""You are Fable, the weekly deep reviewer of the AI Fund Desk - a PAPER-ONLY simulated fund (no real money, no orders,
no exchange account). Today is {day}. Read these files (all under C:\\Users\\lilli\\AI-Shared):
  projects/ai-fund/DESIGN.md, projects/ai-fund/config.json, projects/ai-fund/CHANGELOG.md,
  state/ai-fund/SUMMARY.md, state/ai-fund/summary.json, state/ai-fund/tuner-log.jsonl (last ~170 lines),
  tools/ai_fund/engine.py, tools/ai_fund/run.py, tools/ai_fund/tuner.py, earlier files in projects/ai-fund/proposals/.
Then write ONE file: projects/ai-fund/proposals/{day}.md. Do not edit any other file (Claude applies what is accepted).
In it, plain words, short:
 1. How the live paper book did this week vs the frozen twin and each benchmark; data problems seen.
 2. Is the hourly tuner helping (tuned fund vs frozen twin)? Keep, tighten, or switch off - and why.
 3. Up to 3 proposed changes (code or config), each with: exact change, the evidence, the risk of fooling ourselves
    (hindsight/overfitting), and how to check it after (backtest + twin re-run). "No change" is a fine answer.
 4. Sleeves that should be paused/retired/re-enabled under the verdict rules, and whether fund_halt_reset should be set.
 5. Anything the builders missed.
Rules: paper only; never suggest real orders or Polymarket money (company policy P-0112); free data only."""
    if dry:
        print(brief)
        return
    tok = token()
    if not tok:
        raise SystemExit("no CLAUDE_CODE_OAUTH_TOKEN in keys.env (name only)")
    envv = dict(os.environ, CLAUDE_CODE_OAUTH_TOKEN=tok)
    exe = CLAUDE if os.path.exists(CLAUDE) else "claude"
    r = subprocess.run([exe, "-p", "--model", "claude-fable-5-2", "--effort", "high", "--permission-mode", "acceptEdits",
                        "--add-dir", ROOT], input=brief, text=True, encoding="utf-8", capture_output=True, env=envv,
                       timeout=3600, cwd=ROOT)
    ok = os.path.exists(out)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now():%Y-%m-%d %H:%M:%S} | weekly review (Fable): {'wrote ' + out if ok else 'NO FILE, exit ' + str(r.returncode) + ' ' + (r.stderr or r.stdout)[-200:]}\n")
    subj = "AI Fund weekly review ready" if ok else "AI Fund weekly review FAILED"
    body = (f"Fable's weekly proposal: projects/ai-fund/proposals/{day}.md. Apply what holds up, re-run backtest + twin, log in CHANGELOG.md."
            if ok else f"Fable run wrote no proposal (exit {r.returncode}). See state/ai-fund/runs.log.")
    subprocess.run([sys.executable, os.path.join(ROOT, "tools", "mailbox.py"), "send", "--from", "ai-fund-weekly",
                    "--to", "claude", "--subject", subj, "--body", body], capture_output=True, timeout=60)


if __name__ == "__main__":
    main("--dry" in sys.argv)
