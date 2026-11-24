"""transcript_text.py - the words only from a Claude Code transcript (Jaron 11/13: "skip the screenshots, keep the conversation").
After a compaction, a new context can re-read a whole day of the real conversation at a fraction of the size:
no images, no tool calls, no tool output - just what Jaron said and what Claude said back, with times.
  python tools/transcript_text.py --date 2026-11-13                 # one day (Fort Wayne time) to stdout
  python tools/transcript_text.py --date 2026-11-13 --out FILE.md   # save it
  python tools/transcript_text.py --from "2026-11-13 09:00" --to "2026-11-13 12:00"
  python tools/transcript_text.py --grep relay --date 2026-11-13    # only turns containing a word
Default transcript: the main session's .jsonl. Streams line by line (the file is several GB).
"""
import argparse, json, sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
MAIN = Path.home() / ".claude/projects/C--Users-lilli-AI-Shared/6cacb0b9-dd02-46b4-88e9-fcea9022ace0.jsonl"
SKIP_PREFIXES = ("<system-reminder>", "<task-notification>", "[SYSTEM NOTIFICATION")


def local(ts):
    t = datetime.fromisoformat(ts.replace("Z", "+00:00"))
    # Fort Wayne: EST (UTC-5) Nov-Mar, EDT (UTC-4) otherwise - close enough for day slicing
    off = -5 if t.month in (11, 12, 1, 2) or (t.month == 3 and t.day < 9) else -4
    return t.astimezone(timezone(timedelta(hours=off))).replace(tzinfo=None)


def words(content):
    if isinstance(content, str):
        return [content]
    out = []
    for part in content or []:
        if isinstance(part, dict) and part.get("type") == "text":
            out.append(part.get("text", ""))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", default=str(MAIN))
    ap.add_argument("--date")
    ap.add_argument("--from", dest="start")
    ap.add_argument("--to", dest="end")
    ap.add_argument("--grep")
    ap.add_argument("--out")
    a = ap.parse_args()
    lo = datetime.fromisoformat(a.start) if a.start else (datetime.fromisoformat(a.date) if a.date else datetime.min)
    hi = datetime.fromisoformat(a.end) if a.end else (lo + timedelta(days=1) if a.date else datetime.max)
    lines, n = [], 0
    with open(a.file, encoding="utf-8", errors="replace") as f:
        for raw in f:
            if '"timestamp"' not in raw or ('"type":"user"' not in raw and '"type":"assistant"' not in raw):
                continue
            try:
                r = json.loads(raw)
            except Exception:
                continue
            if r.get("type") not in ("user", "assistant") or "timestamp" not in r:
                continue
            t = local(r["timestamp"])
            if not (lo <= t < hi):
                continue
            msg = r.get("message") or {}
            for w in words(msg.get("content")):
                w = w.strip()
                if not w or w.startswith(SKIP_PREFIXES):
                    continue
                if a.grep and a.grep.lower() not in w.lower():
                    continue
                who = "Jaron" if r["type"] == "user" else "Claude"
                lines.append(f"**{t:%H:%M} {who}:** {w}\n")
                n += 1
    text = "\n".join(lines)
    if a.out:
        Path(a.out).write_text(text, encoding="utf-8")
        print(f"wrote {a.out}: {n} turns, {len(text):,} chars (~{len(text)//4:,} tokens)")
    else:
        print(text)


if __name__ == "__main__":
    main()
