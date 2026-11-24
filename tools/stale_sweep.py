#!/usr/bin/env python
"""stale_sweep.py - list lines in the files AIs read first that MAY be out of date.

Why: bots and AIs read AGENTS.md, the maps, runbooks and the open list to learn the current state. A line like
"not yet done" that was fixed last week makes them report old facts (10/21: "Postiz bill missing", "Anthropic key broken").

What it does (read-only except its two output files):
  - scans a fixed set of status files (see SCAN_GLOBS) line by line
  - flags a line when it has: a waiting/pending phrase, a date that already passed next to a due/expires/renews word,
    an old date (> STALE_DAYS) in a present-tense "waiting" line, a `path` that no longer exists, or a
    scheduled-task name ("task 'X'") that is not registered in Windows
  - writes state/STALE-CANDIDATES.md  (an AI reviews it weekly, fixes lines in place, logs the changes in
    state/STALE-SWEEP-<date>.md and adds one line to state/timeline.md)
It never edits the scanned files and never prints secrets. Safe to run any time.

Run:  python tools/stale_sweep.py            (weekly, Windows task "Stale Sweep", Sunday 5 AM, via pythonw)
"""
import datetime as dt
import glob
import os
import re
import subprocess
import sys
import traceback

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
OUT = os.path.join(ROOT, "state", "STALE-CANDIDATES.md")
LOG = os.path.join(ROOT, "state", "stale-sweep.log")
STALE_DAYS = 14
MAX_PER_FILE = 45
MAX_SNIPPET = 230

SCAN_GLOBS = [
    "AGENTS.md", "README.md", "RECONNECT.md", "WHEN-IT-BREAKS.md", "OPERATING-MAP.md", "JARONS-MAP.md",
    "working-with-jaron.md", "INDEX.json", "decisions/OPEN-QUESTIONS.md",
    "state/open-list.md", "state/models.md", "state/MONEY-LOOP.md", "state/SCHEDULE.md",
    "projects/runs-without-jaron/*.md", "projects/*/README.md", "projects/*/RUNBOOK.md", "projects/*/NEXT.md",
    "agents/*/README.md",
]
# never scanned: logs/histories that are supposed to stay old
SKIP_PARTS = ("timeline.md", "bot-chat.md", "handoffs", "build-ledger", "STALE-", "projects/life", "projects\\life",
              "node_modules", ".bak", "research")

WAIT_RE = re.compile(
    r"\b(not yet|pending|waiting( on| for)?|awaiting|TODO|until|upcoming|tomorrow|this week|next week|"
    r"in progress|being built|down right now)\b", re.I)
DONE_RE = re.compile(r"\b(DONE|RESOLVED|SUPERSEDED|ANSWERED|FIXED|history|was fixed|stale-sweep)\b", re.I)
DUE_RE = re.compile(r"\b(due|expires?|expiring|renews?|renewal|deadline|resets?|trial ends)\b", re.I)
DATE_ISO = re.compile(r"\b(20\d\d)-(\d\d)-(\d\d)\b")
DATE_MD = re.compile(r"(?<![\d./$])(1[0-2]|[1-9])/([12]\d|3[01]|[1-9])(?![\d/])")
PATH_RE = re.compile(r"`([A-Za-z0-9_./\\-]+\.(?:md|py|json|ps1|mjs|js|txt|cmd|sql|jsonl|yaml|yml))`")
TASK_RE = re.compile(r"\btasks?\s+[\"'‘“]([A-Z][A-Za-z0-9 :/+-]{2,40})[\"'’”]")


def today():
    return dt.date.today()


def registered_tasks():
    try:
        out = subprocess.run(["schtasks", "/query", "/fo", "csv", "/nh"], capture_output=True, text=True,
                             timeout=60, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0)).stdout
        names = set()
        for ln in out.splitlines():
            m = re.match(r'"\\?([^"]+)"', ln)
            if m:
                names.add(m.group(1).split("\\")[-1].strip().lower())
        return names
    except Exception:
        return set()


def line_dates(line, ref):
    found = []
    for m in DATE_ISO.finditer(line):
        try:
            found.append(dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3))))
        except ValueError:
            pass
    for m in DATE_MD.finditer(line):
        mo, d = int(m.group(1)), int(m.group(2))
        for yr in (ref.year, ref.year - 1):
            try:
                cand = dt.date(yr, mo, d)
            except ValueError:
                continue
            # month/day with no year: take the occurrence nearest to today (within +-200 days)
            if abs((cand - ref).days) <= 200:
                found.append(cand)
                break
    return found


def path_exists(p, filedir=None):
    p = p.replace("\\", "/")
    home = os.path.expanduser("~")
    for base in (filedir or ROOT, ROOT, os.path.join(ROOT, "tools"), os.path.join(ROOT, "state"), os.path.join(ROOT, "projects"),
                 os.path.join(home, "Projects"), os.path.join(home, "Projects", "heartbeat-observatory"),
                 os.path.join(home, "Projects", "watch")):
        if os.path.exists(os.path.join(base, p)):
            return True
    # absolute paths, other machines' paths, and bare file names (no folder) are not judged
    return ":" in p or p.startswith("~") or p.startswith("/") or "/" not in p


def scan_file(path, rel, tasks, ref):
    hits = []
    try:
        with open(path, encoding="utf-8-sig", errors="replace") as f:
            lines = f.read().splitlines()
    except Exception:
        return hits
    for i, raw in enumerate(lines, 1):
        line = raw.strip()
        if len(line) < 12 or DONE_RE.search(line) or line[0] in "#=":
            continue
        reasons = []
        wait = WAIT_RE.search(line)
        dates = line_dates(line, ref)
        if wait and dates:
            oldest = min(dates)
            age = (ref - oldest).days
            if DUE_RE.search(line) and any(d < ref for d in dates):
                reasons.append("date already passed next to a due/expires/renews word")
            elif age > STALE_DAYS:
                reasons.append(f"'{wait.group(0)}' with a date {age} days old")
        elif wait and wait.group(0).lower() in ("not yet", "pending", "todo", "awaiting", "waiting",
                                                "waiting on", "waiting for", "down right now"):
            reasons.append(f"present-tense '{wait.group(0)}' (check it is still true)")
        for m in PATH_RE.finditer(line):
            if not path_exists(m.group(1), os.path.dirname(path)):
                reasons.append(f"file not found: {m.group(1)}")
        if tasks:
            for m in TASK_RE.finditer(line):
                if m.group(1).strip().lower() not in tasks:
                    reasons.append(f"scheduled task not registered: {m.group(1).strip()}")
        if reasons:
            snip = line if len(line) <= MAX_SNIPPET else line[:MAX_SNIPPET] + "..."
            hits.append((i, "; ".join(dict.fromkeys(reasons)), snip))
    return hits


def main():
    ref = today()
    tasks = registered_tasks()
    files = []
    for g in SCAN_GLOBS:
        for p in sorted(glob.glob(os.path.join(ROOT, g))):
            rel = os.path.relpath(p, ROOT)
            if os.path.isfile(p) and not any(s in rel for s in SKIP_PARTS) and rel not in files:
                files.append(rel)
    out = []
    total = 0
    for rel in files:
        hits = scan_file(os.path.join(ROOT, rel), rel, tasks, ref)
        if not hits:
            continue
        total += len(hits)
        out.append(f"\n## {rel}  ({len(hits)} candidates)\n")
        for i, why, snip in hits[:MAX_PER_FILE]:
            out.append(f"- L{i}: [{why}] {snip}")
        if len(hits) > MAX_PER_FILE:
            out.append(f"- ... {len(hits) - MAX_PER_FILE} more in this file (raise MAX_PER_FILE or fix the top ones first)")
    head = [
        f"# Stale-line candidates - generated {dt.datetime.now():%Y-%m-%d %H:%M} by tools/stale_sweep.py",
        "",
        f"{total} candidate lines in {len(files)} scanned files. These are GUESSES: a hit only means 'look at this line'.",
        "Weekly job for an AI (not Jaron): check each hit against state/timeline.md (newest lines) and the live state.",
        "Fix present-tense claims IN PLACE (keep history, never answer an open question for Jaron), then write",
        "state/STALE-SWEEP-<date>.md (file, old -> new, which timeline line proves it, what you were unsure about)",
        "and add one line to state/timeline.md. Lines already marked DONE/RESOLVED/SUPERSEDED are skipped.",
        f"Scheduled-task check: {'on (' + str(len(tasks)) + ' tasks read)' if tasks else 'OFF (could not read Windows tasks)'}.",
    ]
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(head + out) + "\n")
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(f"{dt.datetime.now():%Y-%m-%d %H:%M} ok {total} candidates in {len(files)} files\n")
    return total


if __name__ == "__main__":
    try:
        n = main()
        if sys.stdout and sys.stdout.isatty():
            print(f"{n} candidates -> {OUT}")
    except Exception:
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(f"{dt.datetime.now():%Y-%m-%d %H:%M} ERROR\n{traceback.format_exc()}\n")
        raise
