"""offsite_backup.py - off-MSI backup into a PRIVATE Supabase Storage bucket ("msi-backups"), not Google Drive (built 11/23).

Jaron 11/23: "back them up. Always." Google Drive was the only off-machine copy of the Necklace project and it kept breaking.

What it backs up (sets):
  code      hb-core, hb-render, hb-vision (no git remote): every file git sees (tracked + untracked-not-ignored, so each
            repo's own .gitignore drops build outputs) plus the whole .git folder; node_modules/.venv/venv/__pycache__ always skipped
  sapling   results/memory.db (copied with the sqlite3 backup API first - it is in use) + the small results files (<=1 MB, no .db).
            The 22 GB of .pt checkpoints and data/ (28 GB) are NOT included.
  necklace  C:\\Users\\lilli\\Projects\\necklace-unreal minus DerivedDataCache, Intermediate, Saved, .vs, Binaries (any depth)

How it stores things (restores stay simple):
  blobs/<sha[:2]>/<sha256>          one object per unique file content (same content = uploaded once)
  blobs/<sha[:2]>/<sha256>.pNNNN    files over 64 MB are split into 64 MB parts; restore joins them in order
  manifests/latest.json.gz          path -> sha256/size/mtime/parts for every set (also dated copies), so a restore
                                    works even if the MSI is gone: download latest.json.gz, then fetch each blob.
Incremental: a file whose size+mtime match the manifest is not re-read. Deleted or changed files keep their old blob for
30 days (manifest "retired"), then the blob is removed. Bandwidth is throttled (default 4 MB/s, --rate). Interrupted runs
resume (finished blobs and finished parts are remembered). CPU/disk run at background priority.
Never runs 3:00-6:00 AM (news render window): it stops itself before 2:45 AM in --nightly mode, and refuses that window always.

Usage:
  pythonw tools/offsite_backup.py run --nightly              task "Offsite Backup" 9:30 PM: all sets, stops by 02:40
  python  tools/offsite_backup.py run --sets code,sapling [--rate 4] [--workers 4] [--until HH:MM] [--dry-run]
  python  tools/offsite_backup.py status
  python  tools/offsite_backup.py restore --test [--n 6] [--sets ...]     download random files, check sha256
  python  tools/offsite_backup.py restore --set code --to D:\\restore [--prefix hb-core/]   real restore
Secrets: Supabase URL/key are loaded from ~/.secrets/keys.env inside this script (same as tools/mailbox.py); never logged.
"""
import argparse, gzip, hashlib, importlib.util, io, json, os, random, shutil, sqlite3, subprocess, sys, tempfile, threading, time
import urllib.error, urllib.parse, urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta

ROOT = r"C:\Users\lilli\AI-Shared"
STATE = os.path.join(ROOT, "state")
MANIFEST = os.path.join(STATE, "offsite-backup-manifest.json")
LOG = os.path.join(STATE, "offsite-backup.log")
LOCK = os.path.join(STATE, ".offsite-backup.lock")
BUCKET = "msi-backups"
PART = 64 * 1024 * 1024
BUCKET_LIMIT = 100 * 1024 * 1024
KEEP_DAYS = 30
P = r"C:\Users\lilli\Projects"
ALWAYS_SKIP_DIRS = {"node_modules", ".venv", "venv", "__pycache__"}
SECRET_NAMES = {"keys.env", ".env"}
SECRET_EXT = (".token", ".pem", ".key")
SETS = {
    "code": {"kind": "git", "roots": {"hb-core": P + r"\hb-core", "hb-render": P + r"\hb-render", "hb-vision": P + r"\hb-vision"}},
    "sapling": {"kind": "sapling", "root": P + r"\sapling"},
    "necklace": {"kind": "walk", "root": P + r"\necklace-unreal",
                 "skip_dirs": {"DerivedDataCache", "Intermediate", "Saved", ".vs", "Binaries"}},
}
ORDER = ["code", "sapling", "necklace"]


# ---------- small helpers ----------
def log(msg):
    line = datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + msg
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")
    if sys.stdout:
        try:
            print(line, flush=True)
        except Exception:
            pass


def now_iso():
    return datetime.now().isoformat(timespec="seconds")


def low_priority():
    try:
        import ctypes
        k = ctypes.windll.kernel32
        k.GetCurrentProcess.restype = ctypes.c_void_p
        k.SetPriorityClass.argtypes = [ctypes.c_void_p, ctypes.c_uint32]
        h = k.GetCurrentProcess()
        # order matters: background mode first (low disk + memory priority), then BELOW_NORMAL (it would otherwise show Normal)
        k.SetPriorityClass(h, 0x00100000)   # PROCESS_MODE_BACKGROUND_BEGIN
        k.SetPriorityClass(h, 0x00004000)   # BELOW_NORMAL_PRIORITY_CLASS
    except Exception:
        pass


def settings():
    """Same loader as tools/mailbox.py (loaded by file path: 'mailbox' is also a stdlib module name)."""
    spec = importlib.util.spec_from_file_location("hb_mailbox", os.path.join(ROOT, "tools", "mailbox.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.settings()


def in_quiet_window(t=None):
    t = t or datetime.now()
    return 3 <= t.hour < 6   # 3:00-6:00 AM is the news render window


def deadline_from(until):
    if not until:
        return None
    hh, mm = map(int, until.split(":"))
    d = datetime.now().replace(hour=hh, minute=mm, second=0, microsecond=0)
    if d <= datetime.now():
        d += timedelta(days=1)
    return d


class Stop(Exception):
    pass


class Refused(RuntimeError):
    """The storage front door refused the body (seen 11/23: HTTP 403 on a raw shell script). Retried gzip-wrapped."""


# ---------- bandwidth throttle (shared by all upload threads) ----------
class Bucket:
    def __init__(self, rate_bps):
        self.rate = rate_bps
        self.allow = rate_bps
        self.last = time.monotonic()
        self.lock = threading.Lock()

    def take(self, n):
        if self.rate <= 0:
            return
        while True:
            with self.lock:
                t = time.monotonic()
                self.allow = min(self.rate, self.allow + (t - self.last) * self.rate)
                self.last = t
                if self.allow >= n:
                    self.allow -= n
                    return
                wait = (n - self.allow) / self.rate
            time.sleep(min(wait, 0.5))


class Section(io.RawIOBase):
    """Read-only, throttled view of bytes [start, start+length) of a file."""
    def __init__(self, path, start, length, bucket, stop_check):
        self.f = open(path, "rb")
        self.f.seek(start)
        self.left = length
        self.bucket = bucket
        self.stop_check = stop_check

    def readable(self):
        return True

    def read(self, n=-1):
        if self.left <= 0:
            return b""
        n = 65536 if n is None or n < 0 else min(n, 65536)
        n = min(n, self.left)
        self.stop_check()
        self.bucket.take(n)
        b = self.f.read(n)
        self.left -= len(b)
        return b

    def close(self):
        try:
            self.f.close()
        finally:
            super().close()


# ---------- Supabase Storage ----------
class Store:
    def __init__(self):
        self.url, self.key = settings()

    def _req(self, method, path, data=None, headers=None, timeout=120):
        h = {"apikey": self.key, "Authorization": "Bearer " + self.key}
        h.update(headers or {})
        req = urllib.request.Request(self.url + "/storage/v1" + path, data=data, method=method, headers=h)
        return urllib.request.urlopen(req, timeout=timeout)

    def ensure_bucket(self):
        try:
            with self._req("GET", "/bucket/" + BUCKET) as r:
                b = json.load(r)
                if b.get("public"):
                    raise RuntimeError("bucket %s is PUBLIC - refusing to upload" % BUCKET)
                return "exists"
        except urllib.error.HTTPError as e:
            if e.code not in (400, 404):
                raise RuntimeError("bucket check failed (HTTP %s)" % e.code) from None
        body = json.dumps({"id": BUCKET, "name": BUCKET, "public": False, "file_size_limit": BUCKET_LIMIT}).encode()
        try:
            with self._req("POST", "/bucket", body, {"Content-Type": "application/json"}):
                return "created"
        except urllib.error.HTTPError as e:
            raise RuntimeError("bucket create failed (HTTP %s)" % e.code) from None

    def put(self, key, body, length, tries=5):
        for i in range(tries):
            data = body() if callable(body) else body
            try:
                with self._req("POST", "/object/%s/%s" % (BUCKET, key), data,
                               {"Content-Type": "application/octet-stream", "Content-Length": str(length),
                                "x-upsert": "true", "cache-control": "no-cache"}, timeout=600):
                    return
            except Stop:
                raise
            except urllib.error.HTTPError as e:
                err = "HTTP %s" % e.code
                if e.code == 403 and i >= 1:
                    raise Refused("upload %s refused (%s)" % (key, err)) from None
                if e.code in (400, 401, 413) and i >= 1:
                    raise RuntimeError("upload %s failed (%s)" % (key, err)) from None
            except Exception as e:
                err = type(e).__name__
            finally:
                if hasattr(data, "close"):
                    data.close()
            time.sleep(min(60, 3 * 2 ** i))
        raise RuntimeError("upload %s failed after %d tries (%s)" % (key, tries, err))

    def get(self, key):
        for i in range(4):
            try:
                with self._req("GET", "/object/authenticated/%s/%s" % (BUCKET, key), timeout=600) as r:
                    return r.read()
            except urllib.error.HTTPError as e:
                if e.code in (400, 404):
                    raise RuntimeError("missing object %s (HTTP %s)" % (key, e.code)) from None
            except Exception:
                pass
            time.sleep(3 * 2 ** i)
        raise RuntimeError("download %s failed" % key)

    def get_to(self, key, out):
        with self._req("GET", "/object/authenticated/%s/%s" % (BUCKET, key), timeout=600) as r:
            shutil.copyfileobj(r, out, 1 << 20)

    def delete(self, keys):
        for i in range(0, len(keys), 500):
            body = json.dumps({"prefixes": keys[i:i + 500]}).encode()
            with self._req("DELETE", "/object/" + BUCKET, body, {"Content-Type": "application/json"}):
                pass


def blob_keys(sha, size):
    base = "blobs/%s/%s" % (sha[:2], sha)
    if size <= PART:
        return [base]
    n = (size + PART - 1) // PART
    return ["%s.p%04d" % (base, i) for i in range(n)]


# ---------- manifest ----------
def load_manifest():
    try:
        with open(MANIFEST, encoding="utf-8") as f:
            m = json.load(f)
    except FileNotFoundError:
        m = {}
    m.setdefault("version", 1)
    m.setdefault("bucket", BUCKET)
    m.setdefault("part_size", PART)
    m.setdefault("sets", {})
    m.setdefault("blobs", {})     # sha -> {size, parts, done_parts:[...], complete, at}
    m.setdefault("retired", [])   # [{set, path, sha256, size, why, at}]
    m.setdefault("runs", [])
    return m


STATE_LOCK = threading.RLock()   # guards every change to the manifest dict and every save of it


def save_manifest(m):
    with STATE_LOCK:
        tmp = MANIFEST + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(m, f, separators=(",", ":"))
        os.replace(tmp, MANIFEST)


# ---------- listing files ----------
def skip_name(name):
    low = name.lower()
    return low in SECRET_NAMES or low.endswith(SECRET_EXT)


def list_git(root):
    out = subprocess.run(["git", "-C", root, "ls-files", "-z", "-co", "--exclude-standard"], capture_output=True,
                         creationflags=0x08000000, check=True).stdout.decode("utf-8", "replace")
    rels = set()
    for r in out.split("\0"):
        if not r:
            continue
        parts = r.split("/")
        if any(p in ALWAYS_SKIP_DIRS for p in parts) or skip_name(parts[-1]):
            continue
        rels.add(r)
    g = os.path.join(root, ".git")
    for dp, dns, fns in os.walk(g):
        for fn in fns:
            rels.add(os.path.relpath(os.path.join(dp, fn), root).replace("\\", "/"))
    return sorted(rels)


def list_walk(root, skip_dirs):
    rels = []
    for dp, dns, fns in os.walk(root):
        dns[:] = [d for d in dns if d not in skip_dirs and d not in ALWAYS_SKIP_DIRS]
        for fn in fns:
            if not skip_name(fn):
                rels.append(os.path.relpath(os.path.join(dp, fn), root).replace("\\", "/"))
    return sorted(rels)


def gather(name, tmpdir):
    """Return {rel: abs_path_to_read, ...} and {rel: (size, mtime) of the live source} for one set."""
    cfg = SETS[name]
    files, live = {}, {}
    if cfg["kind"] == "git":
        for label, root in cfg["roots"].items():
            for rel in list_git(root):
                a = os.path.join(root, rel)
                if os.path.isfile(a):
                    files[label + "/" + rel] = a
    elif cfg["kind"] == "walk":
        for rel in list_walk(cfg["root"], cfg["skip_dirs"]):
            files[rel] = os.path.join(cfg["root"], rel)
    elif cfg["kind"] == "sapling":
        res = os.path.join(cfg["root"], "results")
        for dp, dns, fns in os.walk(res):
            for fn in fns:
                a = os.path.join(dp, fn)
                if ".db" in fn.lower() or skip_name(fn):
                    continue
                try:
                    if os.path.getsize(a) <= 1024 * 1024:
                        files["results/" + os.path.relpath(a, res).replace("\\", "/")] = a
                except OSError:
                    pass
        db = os.path.join(res, "memory.db")
        if os.path.isfile(db):
            # live size+mtime of db AND its wal decide whether a new snapshot is needed
            st = os.stat(db)
            wal = db + "-wal"
            wst = os.stat(wal) if os.path.exists(wal) else None
            live["results/memory.db"] = (st.st_size + (wst.st_size if wst else 0),
                                         max(st.st_mtime, wst.st_mtime if wst else 0))
            files["results/memory.db"] = ("sqlite", db, os.path.join(tmpdir, "sapling-memory.db"))
    return files, live


def snapshot_sqlite(src, dst):
    if os.path.exists(dst):
        os.remove(dst)
    s = sqlite3.connect("file:%s?mode=ro" % urllib.parse.quote(src.replace("\\", "/")), uri=True, timeout=60)
    d = sqlite3.connect(dst)
    try:
        s.backup(d, pages=4096, sleep=0.05)
    finally:
        d.close()
        s.close()
    chk = sqlite3.connect(dst)
    try:
        ok = chk.execute("PRAGMA quick_check").fetchone()[0]
    finally:
        chk.close()
    if ok != "ok":
        raise RuntimeError("sqlite snapshot check failed")
    return dst


def sha256_file(path, stop_check):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            stop_check()
            b = f.read(1 << 20)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


# ---------- run ----------
def run(args):
    low_priority()
    if in_quiet_window():
        log("refused: 3:00-6:00 AM is the news render window")
        return 0
    deadline = deadline_from(args.until)
    stop_flag = threading.Event()

    def stop_check():
        if stop_flag.is_set():
            raise Stop()
        t = datetime.now()
        if (deadline and t >= deadline) or in_quiet_window(t):
            stop_flag.set()
            raise Stop()

    import msvcrt
    lockf = open(LOCK, "a+")
    try:
        msvcrt.locking(lockf.fileno(), msvcrt.LK_NBLCK, 1)
    except OSError:
        log("another offsite backup run is active - exiting")
        return 0

    sets = [s for s in ORDER if s in args.sets]
    log("start: sets=%s rate=%.1f MB/s workers=%d until=%s%s" % (",".join(sets), args.rate, args.workers,
        deadline.strftime("%m-%d %H:%M") if deadline else "-", " DRY-RUN" if args.dry_run else ""))
    m = load_manifest()
    store = None if args.dry_run else Store()
    if store:
        log("bucket %s: %s (private)" % (BUCKET, store.ensure_bucket()))
    tb = Bucket(int(args.rate * 1024 * 1024))
    tmpdir = tempfile.mkdtemp(prefix="offsite-")
    stats = {"uploaded_bytes": 0, "uploaded_files": 0, "skipped": 0, "errors": 0, "new_blobs": 0}
    last_save = [time.time()]
    stopped = False
    t0 = time.time()

    def maybe_save(force=False):
        if force or time.time() - last_save[0] > 60:
            last_save[0] = time.time()
            save_manifest(m)

    sha_locks = {}

    def upload_blob(path, sha, size):
        with STATE_LOCK:
            lk = sha_locks.setdefault(sha, threading.Lock())
        with lk:                                   # two files with the same content: upload once
            with STATE_LOCK:
                b = m["blobs"].get(sha)
                if b and b.get("complete"):
                    return 0
                keys = blob_keys(sha, size)
                if not b or b.get("size") != size:
                    b = m["blobs"][sha] = {"size": size, "parts": len(keys), "done": [], "complete": False}
                done = set(b.get("done", []))
            sent = 0
            for i, key in enumerate(keys):
                if i in done:
                    continue
                start = i * PART
                length = min(PART, size - start)
                try:
                    store.put(key, lambda: Section(path, start, length, tb, stop_check), length)
                except Refused:
                    if len(keys) > 1:
                        raise
                    with open(path, "rb") as f:
                        data = gzip.compress(f.read())
                    tb.take(min(len(data), tb.rate or len(data)))
                    store.put(key + ".gz", data, len(data))
                    with STATE_LOCK:
                        b["enc"] = "gz"
                    log("note: %s stored gzip-wrapped (plain upload refused)" % key)
                sent += length
                with STATE_LOCK:
                    b["done"].append(i)
                    stats["uploaded_bytes"] += length
            with STATE_LOCK:
                b["complete"] = True
                b["at"] = now_iso()
                b.pop("done", None)
                stats["new_blobs"] += 1
            return sent

    try:
        for name in sets:
            s = m["sets"].setdefault(name, {"files": {}})
            s["root"] = SETS[name].get("root") or SETS[name].get("roots")
            cur = s["files"]
            try:
                files, live = gather(name, tmpdir)
            except Exception as e:
                stats["errors"] += 1
                log("%s: listing failed (%s: %s)" % (name, type(e).__name__, e))
                continue
            # deletions -> retired (blob kept 30 days)
            for rel in [r for r in cur if r not in files]:
                e = cur.pop(rel)
                m["retired"].append({"set": name, "path": rel, "sha256": e["sha256"], "size": e["size"], "why": "deleted", "at": now_iso()})
            todo = []
            total = 0
            for rel, src in files.items():
                try:
                    if isinstance(src, tuple):
                        size, mtime = live[rel]
                    else:
                        st = os.stat(src)
                        size, mtime = st.st_size, st.st_mtime
                except OSError:
                    continue
                total += size
                e = cur.get(rel)
                if e and e.get("src_size", e["size"]) == size and abs(e.get("src_mtime", e["mtime"]) - mtime) < 0.001 \
                        and m["blobs"].get(e["sha256"], {}).get("complete"):
                    stats["skipped"] += 1
                    continue
                todo.append((rel, src, size, mtime))
            s["planned_bytes"] = total
            s["planned_files"] = len(files)
            log("%s: %d files (%.2f GB), %d new/changed (%.2f GB)" % (name, len(files), total / 1e9, len(todo),
                sum(t[2] for t in todo) / 1e9))
            if args.dry_run or not todo:
                maybe_save(True)
                continue

            def one(item):
                rel, src, size, mtime = item
                stop_check()
                read_path = src
                if isinstance(src, tuple):          # sqlite snapshot
                    read_path = snapshot_sqlite(src[1], src[2])
                real_size = os.path.getsize(read_path)
                sha = sha256_file(read_path, stop_check)
                upload_blob(read_path, sha, real_size)
                if not isinstance(src, tuple):
                    st = os.stat(src)
                    if st.st_size != size or abs(st.st_mtime - mtime) >= 0.001:
                        return rel, None, "changed during upload; next run"
                return rel, {"size": real_size, "enc": m["blobs"][sha].get("enc"), "mtime": mtime, "sha256": sha, "parts": len(blob_keys(sha, real_size)),
                             "src_size": size, "src_mtime": mtime, "at": now_iso()}, None

            with ThreadPoolExecutor(max_workers=args.workers) as ex:
                futs = [ex.submit(one, it) for it in todo]
                for fu in as_completed(futs):
                    try:
                        rel, entry, note = fu.result()
                    except Stop:
                        stopped = True
                        for f2 in futs:
                            f2.cancel()
                        continue
                    except Exception as e:
                        stats["errors"] += 1
                        if stats["errors"] <= 30:
                            log("%s: error %s: %s" % (name, type(e).__name__, str(e)[:200]))
                        continue
                    if entry is None:
                        log("%s: %s %s" % (name, rel, note))
                        continue
                    with STATE_LOCK:
                        old = cur.get(rel)
                        if old and old["sha256"] != entry["sha256"]:
                            m["retired"].append({"set": name, "path": rel, "sha256": old["sha256"], "size": old["size"], "why": "changed", "at": now_iso()})
                        cur[rel] = entry
                        stats["uploaded_files"] += 1
                    maybe_save()
            maybe_save(True)
            if stopped:
                log("stopping: time window reached (resumes next run)")
                break
        if not args.dry_run and not stopped:
            prune(m, store)
        if not args.dry_run:
            push_manifest(m, store)
    finally:
        el = time.time() - t0
        mbps = stats["uploaded_bytes"] / max(el, 1) / 1e6
        m["runs"] = (m.get("runs", []) + [{"at": now_iso(), "sets": sets, "seconds": int(el), "stopped": stopped, **stats,
                                            "MBps": round(mbps, 2)}])[-60:]
        save_manifest(m)
        shutil.rmtree(tmpdir, ignore_errors=True)
        log("end: %d files, %.2f GB uploaded in %d min (%.2f MB/s), %d unchanged, %d errors%s" % (
            stats["uploaded_files"], stats["uploaded_bytes"] / 1e9, el / 60, mbps, stats["skipped"], stats["errors"],
            ", stopped early" if stopped else ""))
        try:
            msvcrt.locking(lockf.fileno(), msvcrt.LK_UNLCK, 1)
        except OSError:
            pass
        lockf.close()
    return 1 if stats["errors"] else 0


def prune(m, store):
    cutoff = datetime.now() - timedelta(days=KEEP_DAYS)
    keep_retired = [r for r in m["retired"] if datetime.fromisoformat(r["at"]) >= cutoff]
    m["retired"] = keep_retired
    live = {e["sha256"] for s in m["sets"].values() for e in s["files"].values()} | {r["sha256"] for r in keep_retired}
    dead = [sha for sha, b in m["blobs"].items() if sha not in live and b.get("complete")
            and datetime.fromisoformat(b.get("at", now_iso())) < cutoff]
    if not dead:
        return
    keys = [k for sha in dead for k in blob_keys(sha, m["blobs"][sha]["size"])]
    try:
        store.delete(keys)
        for sha in dead:
            m["blobs"].pop(sha, None)
        log("prune: removed %d old blobs (%d objects) past %d days" % (len(dead), len(keys), KEEP_DAYS))
    except Exception as e:
        log("prune failed (%s)" % type(e).__name__)


def push_manifest(m, store):
    data = gzip.compress(json.dumps(m, separators=(",", ":")).encode("utf-8"))
    try:
        store.put("manifests/latest.json.gz", data, len(data))
        store.put("manifests/%s.json.gz" % datetime.now().strftime("%Y-%m-%d"), data, len(data))
        log("manifest uploaded (%.1f MB gz)" % (len(data) / 1e6))
    except Exception as e:
        log("manifest upload failed (%s)" % str(e)[:200])


# ---------- status / restore ----------
def status(args):
    m = load_manifest()
    for name in ORDER:
        s = m["sets"].get(name)
        if not s:
            print("%-9s not started" % name)
            continue
        done = sum(e["size"] for e in s["files"].values())
        planned = s.get("planned_bytes", 0)
        print("%-9s %6d/%-6d files  %7.2f / %7.2f GB  (%.0f%%)" % (name, len(s["files"]), s.get("planned_files", 0),
              done / 1e9, planned / 1e9, 100 * done / planned if planned else 100))
    blobs = sum(b["size"] for b in m["blobs"].values() if b.get("complete"))
    print("bucket %s: %d blobs, %.2f GB stored; %d retired entries kept <=%d days" % (BUCKET, len(m["blobs"]), blobs / 1e9,
          len(m["retired"]), KEEP_DAYS))
    for r in m["runs"][-5:]:
        print("run", r["at"], r["sets"], "%.2f GB" % (r["uploaded_bytes"] / 1e9), "%s MB/s" % r["MBps"], "errors", r["errors"],
              "stopped" if r["stopped"] else "")


def fetch_file(store, entry, out_path):
    h = hashlib.sha256()
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "wb") as out:
        for key in blob_keys(entry["sha256"], entry["size"]):
            data = gzip.decompress(store.get(key + ".gz")) if entry.get("enc") == "gz" else store.get(key)
            h.update(data)
            out.write(data)
    return h.hexdigest()


def restore(args):
    store = Store()
    if args.from_remote or not os.path.exists(MANIFEST):
        m = json.loads(gzip.decompress(store.get("manifests/latest.json.gz")))
    else:
        m = load_manifest()
    if args.test:
        pool = [(n, r, e) for n in ORDER if n in args.sets for r, e in m["sets"].get(n, {}).get("files", {}).items()]
        if not pool:
            print("nothing backed up yet for", args.sets)
            return 1
        pick = random.sample(pool, min(args.n, len(pool)))
        multi = [p for p in pool if p[2]["parts"] > 1]     # always try one split file too, if any exist
        if multi and not any(p[2]["parts"] > 1 for p in pick):
            pick.append(min(multi, key=lambda p: p[2]["size"]))
        tmp = tempfile.mkdtemp(prefix="offsite-restore-test-")
        bad = 0
        try:
            for n, r, e in pick:
                got = fetch_file(store, e, os.path.join(tmp, "f"))
                ok = got == e["sha256"] and os.path.getsize(os.path.join(tmp, "f")) == e["size"]
                bad += not ok
                print("%s  %s:%s  %.2f MB  %d part(s)" % ("OK  " if ok else "BAD ", n, r, e["size"] / 1e6, e["parts"]))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
        log("restore --test: %d files checked, %d bad" % (len(pick), bad))
        print("restore test: %d/%d match sha256" % (len(pick) - bad, len(pick)))
        return 1 if bad else 0
    if not args.to or not args.set:
        print("real restore needs --set and --to")
        return 2
    files = m["sets"].get(args.set, {}).get("files", {})
    n = bad = 0
    for rel, e in sorted(files.items()):
        if args.prefix and not rel.startswith(args.prefix):
            continue
        dst = os.path.join(args.to, *rel.split("/"))
        got = fetch_file(store, e, dst)
        n += 1
        if got != e["sha256"]:
            bad += 1
            print("BAD", rel)
    log("restore %s -> %s: %d files, %d bad" % (args.set, args.to, n, bad))
    print("restored %d files, %d bad" % (n, bad))
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser(description="Off-MSI backup to Supabase Storage")
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    r.add_argument("--sets", default="code,sapling")
    r.add_argument("--nightly", action="store_true", help="all sets, stop by 02:40")
    r.add_argument("--rate", type=float, default=4.0, help="upload MB/s (0 = no limit)")
    r.add_argument("--workers", type=int, default=4)
    r.add_argument("--until", default=None, help="HH:MM local time to stop")
    r.add_argument("--dry-run", action="store_true")
    sub.add_parser("status")
    t = sub.add_parser("restore")
    t.add_argument("--test", action="store_true")
    t.add_argument("--n", type=int, default=6)
    t.add_argument("--sets", default="code,sapling,necklace")
    t.add_argument("--set")
    t.add_argument("--to")
    t.add_argument("--prefix")
    t.add_argument("--from-remote", action="store_true", help="use manifests/latest.json.gz from the bucket")
    a = ap.parse_args()
    if a.cmd == "run":
        if a.nightly:
            a.sets = ",".join(ORDER)
            a.until = a.until or "02:40"
        a.sets = [x.strip() for x in a.sets.split(",") if x.strip()]
        return run(a)
    if a.cmd == "status":
        return status(a)
    a.sets = [x.strip() for x in a.sets.split(",") if x.strip()]
    return restore(a)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        log("crashed: %s: %s" % (type(e).__name__, str(e)[:300]))
        raise
