"""drive_weekly_copy.py - keep Google Drive as a SECOND cloud copy, the gentle way (Jaron 11/24 8:01 AM).

Jaron: "if some things are working and some things weren't, shouldn't we keep it for at least the backup for the things that does
work?" What broke Drive was robocopy walking/writing tens of thousands of files into G: (its local index went corrupt; see
tools/drive_backup.py, retired 11/24). This job writes ONE file a week instead: a git bundle of AI-Shared (the whole history in a
single file, ~80 MB; restore with `git clone <file>`). The main off-MSI copy stays tools/offsite_backup.py (Supabase, nightly).

Task "Drive Weekly Copy", Sunday 9:00 PM. If G: is not mounted it tries Drive's own reset once (the everything check's fix) and
otherwise skips and logs; a skipped week is fine because Supabase has the real copy. Keeps the newest 4 bundles in Drive.
Usage: python tools/drive_weekly_copy.py [--status]
"""
import os, shutil, subprocess, sys, time
from datetime import datetime

ROOT = r"C:\Users\lilli\AI-Shared"
DST = r"G:\My Drive\AI-Shared-weekly"
LOG = os.path.join(ROOT, "state", "drive-weekly.log")
TMP = os.path.join(os.environ.get("TEMP", r"C:\Windows\Temp"), "ai-shared-weekly.bundle")
KEEP = 4


def log(msg):
    line = datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + msg
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")
    print(line, flush=True)


def mounted():
    return os.path.isdir(r"G:\My Drive")


def try_reset():
    sys.path.insert(0, os.path.join(ROOT, "tools"))
    try:
        import all_systems_check as a
        return a.f_gdrive(None)
    except Exception as e:
        return f"reset not possible: {e}"


def main():
    if "--status" in sys.argv:
        print("G: mounted:", mounted()); print(open(LOG, encoding="utf-8").read()[-1500:] if os.path.exists(LOG) else "no runs yet"); return 0
    if not mounted():
        r = try_reset()
        time.sleep(90)
        if not mounted():
            return log(f"skipped - G: is not mounted (Drive reset said: {str(r)[:160]}); Supabase still has the nightly copy") or 0
    subprocess.run(["git", "-C", ROOT, "bundle", "create", TMP, "--all"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=0x08000000)
    os.makedirs(DST, exist_ok=True)
    name = "AI-Shared-" + datetime.now().strftime("%Y-%m-%d") + ".bundle"
    shutil.copyfile(TMP, os.path.join(DST, name))
    size = os.path.getsize(TMP) / 1e6
    os.remove(TMP)
    old = sorted(f for f in os.listdir(DST) if f.startswith("AI-Shared-") and f.endswith(".bundle"))[:-KEEP]
    for f in old:
        os.remove(os.path.join(DST, f))
    log(f"copied {name} ({size:.0f} MB) into Drive; removed {len(old)} older; keeping the newest {KEEP}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
