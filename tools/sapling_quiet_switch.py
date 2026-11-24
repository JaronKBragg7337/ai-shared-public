"""sapling_quiet_switch.py - Jaron's "quiet switch" for Sapling (11/20/2026, 1:33 AM).

Jaron: "You go 2-3 days not hearing from me, have Kimi run that plan" = the 350M Sapling trained on the MSI over time
(projects/strategy/SAPLING-CONVERSATION-BRIEF-2026-11-19.md, option D + the DECIDED section with his three pause rules).

Runs as the Windows task "Sapling Quiet Switch" every 6 hours. It reads state/jaron-last-seen.txt (written by the Claude Code
stamp-time hook on each of Jaron's own messages; background notifications don't count). If that is older than QUIET_HOURS and
the switch hasn't fired before, it starts Kimi once on the plan, then tells Jaron (ntfy) and Claude (mailbox). It fires once:
state/sapling-quiet-switch.json records it. Delete that file to re-arm.
Usage: sapling_quiet_switch.py [--dry-run]
"""
import json, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path

AI = Path(r"C:\Users\lilli\AI-Shared")
SEEN = AI / "state" / "jaron-last-seen.txt"
FLAG = AI / "state" / "sapling-quiet-switch.json"
LOG = AI / "state" / "sapling-quiet-switch.log"
PY = r"C:\Users\lilli\scoop\apps\python312\current\python.exe"
KIMI = Path.home() / ".kimi-code" / "bin" / "kimi.exe"
SAPLING = Path(r"C:\Users\lilli\Projects\sapling")
QUIET_HOURS = 60   # "2-3 days": 2.5 days
DRY = "--dry-run" in sys.argv
NOWIN = 0x08000000

PROMPT = """You are Kimi, Sapling's owner AI. Jaron set a quiet switch on 11/20/2026: if he went 2-3 days without messaging Claude,
you start the plan he approved. That has happened, so this is his go.

THE PLAN: train a ~350M Sapling ON THE MSI ITSELF over time (laptop RTX 4060, 8 GB), not on RunPod. Read
C:/Users/lilli/AI-Shared/projects/strategy/SAPLING-CONVERSATION-BRIEF-2026-11-19.md first (especially "Option D" and "DECIDED").
Start from your 11/2 350M pilot work and the clean bundle where that makes sense; human-written data only (no AI-written text).

JARON'S THREE PAUSE RULES (must be built in, not just remembered):
1. Pause when the MSI GPU is needed for builds (renders, game/browser tests). Simplest: train only when the GPU has no other
   heavy process, and stop cleanly when one appears.
2. Mind Kimi usage: you also run the 3 AM First Light news desk, so this training must not use the Kimi meter the news needs.
   Run the training as a local Python job; don't keep a Kimi session open for it.
3. Never during the news: the GPU belongs to the news render 2:40-7:30 AM (Sapling already yields via tools/gpu_yield.py; keep that).

HOW: set up the training as a resumable local job with checkpoints (8-bit optimizer / gradient checkpointing as needed to fit 8 GB),
run by a Windows scheduled task that resumes from the last checkpoint, plus exams and the fixed ~20-prompt conversation test at each
checkpoint. Keep the live 98.6M Sapling running until a 350M checkpoint beats it. No RunPod spend. Log everything in the Sapling
repo (CHANGELOG, RUN-TIMES) and write a short status line to C:/Users/lilli/AI-Shared/state/sapling-status.md's notes when set up.
When the job is set up and its first chunk ran, send Claude a mailbox note:
python C:/Users/lilli/AI-Shared/tools/mailbox.py send --from kimi --to claude --subject "Sapling 350M on the MSI started" --body "<what you set up, ETA, how to pause>"
Then end this session; the scheduled task carries the training."""


def log(line):
    with LOG.open("a", encoding="utf-8") as fh:
        fh.write(f"{datetime.now():%Y-%m-%d %H:%M} | {line}\n")


def main():
    if FLAG.exists():
        return log("already fired; nothing to do") if not DRY else print("already fired")
    try:
        seen = datetime.fromisoformat(SEEN.read_text(encoding="utf-8").strip().replace("Z", "+00:00"))
    except (OSError, ValueError):
        return log("no last-seen stamp yet; waiting") if not DRY else print("no stamp")
    quiet = (datetime.now(timezone.utc) - seen).total_seconds() / 3600
    if quiet < QUIET_HOURS:
        msg = f"quiet {quiet:.1f} h of {QUIET_HOURS}; not yet"
        return print(msg) if DRY else log(msg)
    if DRY:
        return print(f"WOULD FIRE: quiet {quiet:.1f} h; would start Kimi in {SAPLING}")
    out = open(AI / "state" / "sapling-quiet-switch-kimi.log", "w", encoding="utf-8")
    p = subprocess.Popen([str(KIMI), "-p", PROMPT], cwd=SAPLING, stdout=out, stderr=subprocess.STDOUT, creationflags=NOWIN)
    FLAG.write_text(json.dumps({"fired": datetime.now().isoformat(timespec="minutes"), "quiet_hours": round(quiet, 1), "kimi_pid": p.pid}), encoding="utf-8")
    log(f"FIRED: quiet {quiet:.1f} h; Kimi started (PID {p.pid})")
    note = (f"Jaron hasn't messaged in {quiet:.0f} hours, so the Sapling quiet switch fired: Kimi is setting up the 350M training "
            "on the MSI (his three pause rules). Delete state/sapling-quiet-switch.json to re-arm.")
    subprocess.run([PY, str(AI / "tools" / "mailbox.py"), "send", "--from", "sapling-switch", "--to", "claude",
                    "--subject", "Sapling quiet switch fired: Kimi starting the 350M", "--body", note], capture_output=True, timeout=60, creationflags=NOWIN)
    subprocess.run([PY, str(AI / "tools" / "ntfy-say.py"), "Sapling",
                    "You've been quiet a couple of days, so Kimi is starting Sapling's 350M training on the MSI, like you set up. It pauses for builds, the news and Kimi's news work."],
                   capture_output=True, timeout=60, creationflags=NOWIN)


if __name__ == "__main__":
    main()
