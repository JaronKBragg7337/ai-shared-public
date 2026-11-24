"""Log when a job moves from one AI/model to another (stuck, out of usage, wrong tool, quality).

Usage:
  python tools/handoff_log.py "<job>" --from "<ai/model>" --to "<ai/model>" --why stuck|usage|access|quality|other --note "<plain words>"
Writes one line to state/job-handoffs.md (newest last) and state/job-handoffs.jsonl.
The usage ledger (tools/usage_ledger.py) shows tokens per job and model; this file shows WHY work changed hands.
"""
import argparse, json, os
from datetime import datetime
from zoneinfo import ZoneInfo

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD = os.path.join(ROOT, "state", "job-handoffs.md")
JL = os.path.join(ROOT, "state", "job-handoffs.jsonl")

def main():
    p = argparse.ArgumentParser()
    p.add_argument("job"); p.add_argument("--from", dest="src", required=True); p.add_argument("--to", dest="dst", required=True)
    p.add_argument("--why", choices=["stuck", "usage", "access", "quality", "other"], required=True)
    p.add_argument("--note", default=""); p.add_argument("--at", default="")
    a = p.parse_args()
    at = a.at or datetime.now(ZoneInfo("America/Indiana/Indianapolis")).strftime("%Y-%m-%d %H:%M")
    if not os.path.exists(MD):
        with open(MD, "w", encoding="utf-8") as f:
            f.write("# Job handoffs between AIs\n\nWhen a job moves from one AI or model to another, and why. Tokens per job live in state/usage-ledger.md.\n\n| When | Job | From | To | Why | Note |\n| --- | --- | --- | --- | --- | --- |\n")
    clean = lambda s: s.replace("|", "/").replace("\n", " ")
    with open(MD, "a", encoding="utf-8") as f:
        f.write(f"| {at} | {clean(a.job)} | {clean(a.src)} | {clean(a.dst)} | {a.why} | {clean(a.note)} |\n")
    with open(JL, "a", encoding="utf-8") as f:
        f.write(json.dumps({"at": at, "job": a.job, "from": a.src, "to": a.dst, "why": a.why, "note": a.note}) + "\n")
    print("logged:", a.job, a.src, "->", a.dst, a.why)

if __name__ == "__main__":
    main()
