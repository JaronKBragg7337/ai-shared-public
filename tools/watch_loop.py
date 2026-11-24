"""watch_loop.py - the helper loop for "Tell Claude" (2026-10-28, Claude Code).
Jaron speaks into his phone/watch -> watch-inbox function -> ai_mailbox (from jaron-*, to claude, status new).
This script (Windows task "HB Watch Loop", every minute, hidden) picks up new messages, has Claude answer in a few
plain sentences with today's context, buzzes the answer back (tools/watch_reply.py -> ntfy "Claude"), logs the
exchange in state/watch-chat.md and marks the message read. The main Claude Code session reads watch-chat.md, so
real work asked for here gets picked up there. Nothing new = no Claude call, so idle minutes cost nothing.
  python tools/watch_loop.py          # one pass
  python tools/watch_loop.py --dry    # show what would be answered, send nothing
"""
import os, shutil, subprocess, sys, time, urllib.parse
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from mailbox import request  # noqa: E402
from watch_reply import keys, reply  # noqa: E402

LOG = os.path.join(ROOT, "state", "watch-chat.md")
LOCK = os.path.join(ROOT, "state", ".watch-loop.lock")
MAIN = os.path.join(ROOT, "state", "watch-main.on")   # present = the main Claude Code session answers instead (Jaron 10/28 test)


def tail(path, n):
    try:
        return "".join(open(path, encoding="utf-8", errors="replace").readlines()[-n:])
    except OSError:
        return ""


def answer(msg):
    today = datetime.now().strftime("%Y-%m-%d")
    prompt = (
        "You are Claude, Jaron's AI partner and the orchestrator of his company, Heartbeat Observatory. He just spoke this "
        "into his phone or Apple Watch while out (roofer in Fort Wayne, often on a scooter):\n\n"
        f"\"{msg['body']}\"\n\n"
        "Reply as a phone notification: 1-3 short plain sentences, warm, no jargon, no markdown, no em dashes. "
        "If he asks for real work (a build, a fix, a change), say it's logged and the main session will do it; don't promise "
        "a time. Never include secrets, keys or addresses. If it's just an update, acknowledge it like a friend would.\n\n"
        "Recent watch chat:\n" + tail(LOG, 12) +
        "\nToday so far (his day log):\n" + tail(os.path.join(ROOT, "projects", "reality-agent", "day-log", today + ".md"), 8) +
        "\nRecent company timeline:\n" + tail(os.path.join(ROOT, "state", "timeline.md"), 8)
    )
    env = {**os.environ, "CLAUDE_CODE_OAUTH_TOKEN": keys().get("CLAUDE_CODE_OAUTH_TOKEN", "")}
    exe = shutil.which("claude") or "claude"   # prompt goes in on stdin so quotes/newlines survive Windows
    p = subprocess.run([exe, "--model", "sonnet", "-p"], input=prompt, capture_output=True, text=True, encoding="utf-8",
                       errors="replace", timeout=180, env=env, cwd=ROOT,
                       creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    out = (p.stdout or "").strip()
    if p.returncode != 0 or not out or "error" in out.lower()[:40]:
        return "Got it, it's in the mailbox. The quick-reply brain hiccuped, so the main session will answer."
    return out[:600]


def main(dry=False):
    # Main session on: it answers. Backup: anything still unread after 5 min (main busy, compacting or closed) gets the quick answer.
    stale_only = os.path.exists(MAIN)
    if os.path.exists(LOCK) and time.time() - os.path.getmtime(LOCK) < 600:
        return
    open(LOCK, "w").close()
    try:
        q = urllib.parse.urlencode({"to_ai": "eq.claude", "status": "eq.new", "from_ai": "like.jaron-*",
                                    "order": "created_at.asc", "limit": "5"})
        for msg in request("GET", "?" + q):
            if stale_only:
                age = time.time() - datetime.fromisoformat(msg["created_at"].replace("Z", "+00:00")).timestamp()
                if age < 300:
                    continue
            if dry:
                print("would answer:", msg["body"][:80])
                continue
            text = answer(msg)
            reply(text)
            stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            with open(LOG, "a", encoding="utf-8") as f:
                f.write(f"- {stamp} Jaron ({msg['from_ai']}): {msg['body']}\n  Claude: {text}\n")
            request("PATCH", "?id=eq." + msg["id"], {"status": "read"})
    finally:
        os.remove(LOCK)


if __name__ == "__main__":
    main("--dry" in sys.argv)
