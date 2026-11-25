"""drive_backup.py - the two nightly backups into Google Drive (G:), with a guard (built 11/23).
RETIRED 11/24 (Jaron: "Google Drive has always had issues"): its 3 tasks are disabled; the off-MSI Supabase backup (tools/offsite_backup.py) is the copy now. Kept, not deleted.

The 11/23 investigation (6 agents, research/fact-checks style notes in state/timeline.md 11/23) found that Drive's local index
goes "corrupt" (SQLite code 11) only inside the running Drive program - every saved copy checks out on disk - and almost always
when robocopy walks G: soon after Drive rebuilt that index: 6 of 7 such runs broke it, against about 1 in 57 on a settled index.
Two of those runs were started by Claude right after a reset. So this wrapper:
  - never backs up while G: is unmounted or Drive's own corruption marker is present
  - after Drive gets a NEW index, waits until a gentle fill (folders listed slowly) has run; only then allows the fast backups
  - never lets the two jobs overlap (a lock; the later job waits up to 90 min)
  - keeps the jobs' own logs out of the mirror (Google rejected half-written log uploads on 11/15)
Usage:
  pythonw drive_backup.py necklace | mirror       tasks "Necklace Unreal Backup" (3:00) / "AI-Shared Mirror" (3:30)
  pythonw drive_backup.py gentle-fill [rate]       task "Drive Gentle Fill" (9 PM): no-op unless the index is new and unfilled
  python  drive_backup.py status
"""
import json, os, subprocess, sys, time
from datetime import datetime

ROOT = r"C:\Users\lilli\AI-Shared"
STATE = os.path.join(ROOT, "state")
LOG = os.path.join(STATE, "drive-backup.log")
IDX = os.path.join(STATE, ".drive-index.json")
LOCK = os.path.join(STATE, ".drive-backup.lock")
DRIVEFS = os.path.expandvars(r"%LOCALAPPDATA%\Google\DriveFS")
G = r"G:\My Drive"
NOWIN = 0x08000000
SETTLED_AFTER_H = 72   # an index this old that was never seen by this guard counts as settled (bootstrap for older indexes)
JOBS = {
    "necklace": (r"C:\Users\lilli\Projects\necklace-unreal", G + r"\necklace-unreal-backup",
                 ["/XD", "DerivedDataCache", "Intermediate", "Saved", ".vs", "Binaries"], os.path.join(STATE, "necklace-backup.log")),
    "mirror": (ROOT, G + r"\AI-Shared-mirror",
               ["/XD", r"runtime\polymarket-us-agent-venv", r"runtime\grok-machine-mcp\node_modules", "node_modules", ".venv", "venv",
                "__pycache__", r"tools\paper-trader",
                "/XF", "*.token", "QwenBridge.token", "Polymarket.txt", "keys.env",
                "mirror.log", "necklace-backup.log", "drive-backup.log", ".drive-backup.lock"],
               os.path.join(STATE, "mirror.log")),
}
FILL_TOPS = [G + r"\necklace-unreal-backup", G + r"\AI-Shared-mirror"]


def log(msg):
    line = datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + msg
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")
    print(line, flush=True)


def load():
    try:
        return json.load(open(IDX, encoding="utf-8"))
    except Exception:
        return {}


def save(st):
    json.dump(st, open(IDX, "w", encoding="utf-8"), indent=1)


def account_dirs():
    return [os.path.join(DRIVEFS, d) for d in (os.listdir(DRIVEFS) if os.path.isdir(DRIVEFS) else [])
            if os.path.isdir(os.path.join(DRIVEFS, d))]


def corrupt():
    return any(os.path.isfile(os.path.join(a, "metadata_sqlite_db_is_corrupted")) for a in account_dirs())


def born_at(acct):
    """When Drive's live index was born = the newest set-aside of an old one. NOT the file's creation time: Windows 'tunnels' the
    old file's creation date onto a file re-created under the same name within seconds (11/23: a fresh index showed June 1)."""
    t = []
    for f in os.listdir(acct):
        if not f.startswith("metadata_sqlite_db"):
            continue
        if ".corrupt." in f:   # Drive's own: metadata_sqlite_db.corrupt.<epoch ms>[...]
            ms = f.split(".corrupt.", 1)[1].split(".")[0]
            if ms.isdigit():
                t.append(int(ms) / 1000)
        if ".bad-" in f:       # ours: <name>.bad-YYYYMMDD-HHMM
            try:
                t.append(datetime.strptime(f.rsplit(".bad-", 1)[1][:13], "%Y%m%d-%H%M").timestamp())
            except ValueError:
                pass
    return max(t) if t else os.path.getctime(os.path.join(acct, "metadata_sqlite_db"))


def index_id():
    """(id, age_hours) of Drive's live index: the account folder + when that index was born."""
    best = None
    for a in account_dirs():
        if os.path.isfile(os.path.join(a, "metadata_sqlite_db")):
            b = born_at(a)
            if best is None or b > best[1]:
                best = (os.path.basename(a), b)
    if not best:
        return None, None
    return f"{best[0]}|{int(best[1])}", (time.time() - best[1]) / 3600


def index_state():
    """Current index + whether it is filled (settled). Records a new index the first time it is seen."""
    idx, age = index_id()
    st = load()
    if idx and st.get("index") != idx:
        st = {"index": idx, "first_seen": datetime.now().isoformat(timespec="seconds"),
              "filled": bool(age is not None and age > SETTLED_AFTER_H),
              "why": f"older than {SETTLED_AFTER_H} h when first seen" if age and age > SETTLED_AFTER_H else "new index"}
        save(st)
    return idx, age, st


def ready(what):
    if not os.path.isdir(G):
        return log(f"{what}: skipped - G: is not mounted")
    if corrupt():
        return log(f"{what}: skipped - Drive marked its index corrupt (the everything check resets it once a day)")
    idx, age, st = index_state()
    if not idx:
        return log(f"{what}: skipped - no Drive index found")
    return idx, age, st


def take_lock(wait_min=90):
    t0 = time.time()
    while os.path.exists(LOCK):
        try:
            if time.time() - os.path.getmtime(LOCK) > 6 * 3600:
                break   # stale lock from a crashed run
        except OSError:
            break
        if time.time() - t0 > wait_min * 60:
            return False
        time.sleep(30)
    open(LOCK, "w").write(f"{os.getpid()} {datetime.now().isoformat(timespec='seconds')}")
    return True


def backup(job):
    r = ready(job)
    if not r:
        return 0
    idx, age, st = r
    if not st.get("filled"):
        return log(f"{job}: skipped - Drive's index is new ({age:.1f} h) and not filled yet; the gentle fill runs at 9 PM "
                   "(a fast backup on a fresh index broke it 6 of 7 times)") or 0
    if not take_lock():
        return log(f"{job}: skipped - the other backup was still running after 90 min") or 0
    try:
        src, dst, extra, joblog = JOBS[job]
        args = ["robocopy", src, dst, "/MIR", "/R:1", "/W:2"] + extra + ["/NP", "/NJH", "/LOG+:" + joblog]
        t0 = time.time()
        rc = subprocess.run(args, creationflags=NOWIN, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode
        broke = corrupt()
        log(f"{job}: robocopy exit {rc} in {(time.time() - t0) / 60:.1f} min" + (" - AND Drive marked its index corrupt during it" if broke else ""))
        if broke:
            st.update(filled=False, broke_during=job, broke_at=datetime.now().isoformat(timespec="seconds")); save(st)
        return 0 if rc < 8 else rc
    finally:
        try:
            os.remove(LOCK)
        except OSError:
            pass


def gentle_fill(rate=4.0):
    r = ready("gentle-fill")
    if not r:
        return 0
    idx, age, st = r
    if st.get("filled"):
        return log(f"gentle-fill: nothing to do - the index is already filled ({st.get('why', '')})") or 0
    if not take_lock(wait_min=10):
        return log("gentle-fill: skipped - a backup is running") or 0
    n, t0 = 0, time.time()
    try:
        log(f"gentle-fill: start (index {age:.1f} h old, {rate} folder listings a second)")
        for top in FILL_TOPS:
            stack = [top] if os.path.isdir(top) else []
            while stack:
                d = stack.pop()
                try:
                    with os.scandir(d) as it:
                        stack.extend(e.path for e in it if e.is_dir(follow_symlinks=False))
                except OSError as e:
                    log(f"gentle-fill: could not list {d[len(G):][:80]}: {e}")
                n += 1
                time.sleep(1.0 / rate)
                if n % 100 == 0 and (corrupt() or not os.path.isdir(G)):
                    st.update(filled=False, fill_broke_at=datetime.now().isoformat(timespec="seconds"), fill_listings=n); save(st)
                    return log(f"gentle-fill: Drive broke its index after {n} slow listings ({(time.time() - t0) / 60:.0f} min) - "
                               "so even slow listing on a fresh index breaks it (useful for the MSI data-error hunt)") or 0
        time.sleep(60)
        if corrupt():
            st.update(filled=False, fill_broke_at=datetime.now().isoformat(timespec="seconds"), fill_listings=n); save(st)
            return log(f"gentle-fill: finished {n} listings but Drive marked the index corrupt right after") or 0
        st.update(filled=True, why="gentle fill", filled_at=datetime.now().isoformat(timespec="seconds"), fill_listings=n,
                  fill_minutes=round((time.time() - t0) / 60, 1))
        save(st)
        return log(f"gentle-fill: done - {n} folder listings in {(time.time() - t0) / 60:.0f} min, index still clean; backups allowed") or 0
    finally:
        try:
            os.remove(LOCK)
        except OSError:
            pass


def status():
    idx, age, st = index_state() if account_dirs() else (None, None, load())
    print(json.dumps({"G_mounted": os.path.isdir(G), "corrupt_marker": corrupt(), "index": idx,
                      "index_age_h": round(age, 1) if age is not None else None, "state": st,
                      "lock": os.path.exists(LOCK)}, indent=1))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    if cmd in JOBS:
        sys.exit(backup(cmd))
    if cmd == "gentle-fill":
        sys.exit(gentle_fill(float(sys.argv[2]) if len(sys.argv) > 2 else 4.0))
    status()
