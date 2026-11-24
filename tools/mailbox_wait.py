"""mailbox_wait.py - waits quietly until a NEW message for Claude lands in ai_mailbox, prints it, and exits (Jaron 10/28).
The main Claude Code session runs this in the background; its exit wakes the session, so the session only spends usage
when someone (Jaron by voice, or another AI) actually says something. Checks every 20 s, no Claude calls while waiting.
  python tools/mailbox_wait.py            # blocks until something new arrives (max 55 min), prints the messages as JSON
  python tools/mailbox_wait.py --to chatgpt --minutes 4   # another AI waits for ITS mail (11/13: ChatGPT relay test)
"""
import json, sys, time, urllib.parse
if sys.stdout: sys.stdout.reconfigure(encoding="utf-8")   # 11/22: pythonw (Task Scheduler) has no stdout; this line crashed every pythonw caller since 11/10
sys.path.insert(0, __file__.rsplit("\\", 1)[0].rsplit("/", 1)[0])
from mailbox import request

args = sys.argv[1:]
who = args[args.index("--to") + 1] if "--to" in args else "claude"
mins = float(args[args.index("--minutes") + 1]) if "--minutes" in args else 55
q = "?" + urllib.parse.urlencode({"to_ai": "eq." + who, "status": "eq.new", "order": "created_at.asc", "limit": "10"})
end = time.time() + mins * 60
while time.time() < end:
    try:
        rows = request("GET", q)
    except Exception as e:
        rows = []
    if rows:
        print(json.dumps([{"id": r["id"], "from": r["from_ai"], "at": r["created_at"], "subject": r["subject"], "body": r["body"]} for r in rows], ensure_ascii=False, indent=1))
        sys.exit(0)
    time.sleep(20 if who == "claude" else 5)
print(f"[]  ({mins:g} min, nothing new)")
