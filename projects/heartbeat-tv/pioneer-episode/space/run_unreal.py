# Launch Unreal for the space scenes while holding UNREAL.lock (PRODUCTION.md protocol).
# Waits while the lock is fresh (< 90 min) or any UnrealEditor is running; refreshes our lock every 5 min; deletes it on exit.
# Hard stop: kills only OUR Unreal at 02:15 (GPU must be free by 02:20).
# Usage: python run_unreal.py [ENV=VAL ...]     (env vars are passed to build.py, e.g. PIO_TEST=1 PIO_SCENES=s04)
import os, sys, time, subprocess, datetime
HERE = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
LOCK = HERE + "/../UNREAL.lock"
UE = r"C:\Program Files\Epic Games\UE_5.8\Engine\Binaries\Win64\UnrealEditor.exe"
PROJ = r"C:\Users\lilli\Projects\necklace-unreal\NecklaceFilm.uproject"
ME = "space builder agent (Claude, truck+space scenes)"
def log(m): print(time.strftime("%H:%M:%S"), m, flush=True)
def unreal_running():
    out = subprocess.run(["tasklist", "/FI", "IMAGENAME eq UnrealEditor.exe", "/NH"], capture_output=True, text=True).stdout
    return "UnrealEditor.exe" in out
def take_lock():
    while True:
        if os.path.exists(LOCK):
            age = time.time() - os.path.getmtime(LOCK)
            try: who = open(LOCK).read().strip()
            except Exception: who = "?"
            if age < 90 * 60 or unreal_running():
                log("lock held (%s, %.0f min old) - waiting" % (who[:80], age / 60)); time.sleep(60); continue
            log("stale lock (%.0f min, no Unreal running) - taking it" % (age / 60))
            try: os.remove(LOCK)
            except Exception: pass
        if unreal_running(): log("an Unreal is running without a lock - waiting"); time.sleep(60); continue
        try:
            fd = os.open(LOCK, os.O_CREAT | os.O_EXCL | os.O_WRONLY); os.write(fd, ("%s since %s pid %d\n" % (ME, datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), os.getpid())).encode()); os.close(fd)
            log("lock taken"); return
        except FileExistsError: time.sleep(5)
def refresh():
    try:
        with open(LOCK, "w") as f: f.write("%s since %s pid %d (refreshed %s)\n" % (ME, START, os.getpid(), datetime.datetime.now().strftime("%H:%M")))
    except Exception as e: log("refresh failed %r" % e)
env = dict(os.environ)
for a in sys.argv[1:]:
    k, v = a.split("=", 1); env[k] = v
take_lock(); START = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
try:
    p = subprocess.Popen([UE, PROJ, '-ExecCmds=py %s/build_safe.py' % HERE], env=env)
    log("Unreal pid %d" % p.pid); last = time.time(); T0 = time.time()
    while p.poll() is None:
        time.sleep(10)
        if time.time() - last > 300: refresh(); last = time.time()
        now = datetime.datetime.now()
        if time.time() - T0 > float(env.get('MAXMIN', '600')) * 60: log('MAXMIN reached - ending our Unreal'); p.kill(); break
        if now.hour == 2 and now.minute >= 15: log("02:15 hard stop - ending our Unreal"); p.kill(); break
    log("Unreal exited %s" % p.returncode)
finally:
    try:
        if ME in open(LOCK).read(): os.remove(LOCK); log("lock released")
    except Exception as e: log("release %r" % e)
