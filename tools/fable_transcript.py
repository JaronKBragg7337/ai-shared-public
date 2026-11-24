"""fable_transcript.py - save each day's Fable chat (words only) next to the bots' transcripts (Jaron 11/23 4:54 PM).

Finds every Claude Code session file in this project that ran on Fable today and writes the words (what Jaron said, what
Fable said, with times) to transcripts/fable-<session>/<date>.md via tools/transcript_text.py. Task "Fable Transcript",
10:45 PM nightly (before the 10:55 PM nightly save commits it). Also runnable any time: python tools/fable_transcript.py [YYYY-MM-DD]
"""
import os, subprocess, sys
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJ = os.path.expanduser(r"~\.claude\projects\C--Users-lilli-AI-Shared")
day = sys.argv[1] if len(sys.argv) > 1 else date.today().isoformat()


def is_fable_today(path):
    fable = other = 0
    seen_day = False
    with open(path, encoding="utf-8", errors="ignore") as f:
        for line in f:
            if '"timestamp":"' + day in line:
                seen_day = True
            if '"model":"claude-fable' in line:
                fable += 1
            elif '"model":"claude-' in line:
                other += 1
    return seen_day and fable > other and fable > 5


for name in os.listdir(PROJ):
    p = os.path.join(PROJ, name)
    if not name.endswith(".jsonl") or os.path.getsize(p) > 2_000_000_000:   # skip the 3 GB main Opus file
        continue
    if os.path.getmtime(p) < __import__("time").time() - 3 * 86400 or not is_fable_today(p):
        continue
    out = os.path.join(ROOT, "transcripts", "fable-" + name[:8], day + ".md")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    r = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "transcript_text.py"), "--file", p, "--date", day, "--out", out],
                       capture_output=True, text=True)
    print((r.stdout or r.stderr).strip()[-200:])
