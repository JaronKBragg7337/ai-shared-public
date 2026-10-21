"""append-guard.py - keeps append-only logs append-only (2026-10-09, Claude Code).

Darios Twin wiped state/live-wire.md twice in two days (10/8 7:40 PM, 10/9 9:58 PM) by rewriting it instead of appending.
Asking nicely didn't hold, so this makes it structural: every run, each guarded file is compared with a shadow copy. If the
file no longer starts with everything the shadow had (it was rewritten or cut), the shadow is put back and only the genuinely
new lines are appended after it. Then the shadow is refreshed. Runs from connector-watch (every 30 min); safe to run anytime.
"""
import os, shutil, time
ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
GUARDED = ["state/live-wire.md", "state/bot-chat.md"]
SHADOW_DIR = os.path.join(ROOT, "state", ".append-guard")
LOG = os.path.join(ROOT, "state", "append-guard.log")


def guard(rel):
    path, shadow = os.path.join(ROOT, rel), os.path.join(SHADOW_DIR, rel.replace("/", "__"))
    if not os.path.exists(path):
        return None
    cur = open(path, encoding="utf-8", errors="replace").read()
    if os.path.exists(shadow):
        old = open(shadow, encoding="utf-8", errors="replace").read()
        if not cur.startswith(old.rstrip("\n")):
            old_lines = set(old.splitlines())
            new = [l for l in cur.splitlines() if l not in old_lines]
            stamp = time.strftime("%Y-%m-%d %H:%M")
            shutil.copy2(path, path + f".rewritten-{time.strftime('%Y%m%d-%H%M')}")
            fixed = old.rstrip("\n") + "\n" + (f"# {stamp} append-guard: file was rewritten, history restored; new lines follow\n" if new else "") + ("\n".join(new) + "\n" if new else "")
            open(path, "w", encoding="utf-8").write(fixed)
            with open(LOG, "a", encoding="utf-8") as f:
                f.write(f"{stamp} restored {rel}: kept {len(old.splitlines())} old lines, re-added {len(new)} new\n")
            cur = fixed
    os.makedirs(SHADOW_DIR, exist_ok=True)
    open(shadow, "w", encoding="utf-8").write(cur)
    return True


if __name__ == "__main__":
    for r in GUARDED:
        guard(r)
