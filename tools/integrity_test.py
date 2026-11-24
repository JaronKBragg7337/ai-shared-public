"""integrity_test.py - does this machine silently get data wrong under heavy load?

Plain idea: give the computer work where we already know the right answer, make it do that
work over and over on many cores at once, and check every answer. A healthy machine gets
every single answer right, forever. A machine with a weak memory stick, an unstable CPU
(heat, voltage, the known 13th/14th-gen Intel "Vmin" wear) or a bad write path will now and
then get one wrong - quietly. That is exactly the kind of fault behind a JSON row that was
"bad" once and fine afterward, a PNG that ffmpeg could not inflate but PIL could, and an
mp4 with a few bytes turned to zero.

Three kinds of checks, run by several worker processes at the same time:
  memory  fill big RAM buffers with a known pattern (different value at every address),
          read them back right away and again after holding them a while.
  cpu     hashing (sha256, blake2b), zlib compress+inflate (the same code family that
          failed on the PNGs), lzma, big-integer math, integer and float array math -
          every result compared to a reference computed at the start.
  disk    write files with a known pattern, flush them to the drive, read them back past
          the Windows file cache when possible, compare chunk by chunk.

No admin rights, no downloads, standard library + numpy (already installed). It runs at
below-normal priority so Sapling, the Cosmos server and everything else go first, keeps a
core free, caps RAM at 8 GB (default 6 GB), stops early if free RAM gets low, and deletes
its own temp files. It never touches another program.

Usage:
  python tools/integrity_test.py                 # 5 minutes, default load, logs result
  python tools/integrity_test.py --minutes 3
  python tools/integrity_test.py --minutes 30 --priority normal   # harder, nightly
  python tools/integrity_test.py --minutes 1 --inject             # prove it catches errors (not logged)

Exit codes: 0 = clean, 1 = at least one wrong answer or a worker crashed, 2 = the test could
not run properly (e.g. stopped early for low memory) but found nothing wrong.

Logs: state/integrity-log.md (one line per run, newest last) and state/integrity-log.json.
"""
from __future__ import annotations

import argparse
import ctypes
import hashlib
import json
import lzma
import multiprocessing as mp
import os
import queue
import shutil
import sys
import tempfile
import time
import zlib
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOG_MD = ROOT / "state" / "integrity-log.md"
LOG_JSON = ROOT / "state" / "integrity-log.json"
TEMP_ROOT = Path(tempfile.gettempdir()) / "hb-integrity"

MEM_CAP_GB = 8.0
WORKER_OVERHEAD_GB = 0.25      # python + numpy + cpu-test inputs + chunk temporaries
CHUNK = 1 << 22                # 4M uint64 = 32 MB per memory verify chunk
DISK_CHUNK_ELEMS = 1 << 20     # 1M uint64 = 8 MB per disk chunk
MAX_DETAILS = 100
IS_WIN = sys.platform == "win32"

try:
    import numpy as np
except ImportError:  # pragma: no cover
    np = None


# ---------------------------------------------------------------- Windows helpers (ctypes, no admin)

if IS_WIN:
    from ctypes import wintypes

    _k32 = ctypes.WinDLL("kernel32", use_last_error=True)
    _psapi = ctypes.WinDLL("psapi", use_last_error=True)

    class _MEMSTAT(ctypes.Structure):
        _fields_ = [("dwLength", wintypes.DWORD), ("dwMemoryLoad", wintypes.DWORD),
                    ("ullTotalPhys", ctypes.c_ulonglong), ("ullAvailPhys", ctypes.c_ulonglong),
                    ("ullTotalPageFile", ctypes.c_ulonglong), ("ullAvailPageFile", ctypes.c_ulonglong),
                    ("ullTotalVirtual", ctypes.c_ulonglong), ("ullAvailVirtual", ctypes.c_ulonglong),
                    ("ullAvailExtendedVirtual", ctypes.c_ulonglong)]

    class _PMC(ctypes.Structure):
        _fields_ = [("cb", wintypes.DWORD), ("PageFaultCount", wintypes.DWORD),
                    ("PeakWorkingSetSize", ctypes.c_size_t), ("WorkingSetSize", ctypes.c_size_t),
                    ("QuotaPeakPagedPoolUsage", ctypes.c_size_t), ("QuotaPagedPoolUsage", ctypes.c_size_t),
                    ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t), ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
                    ("PagefileUsage", ctypes.c_size_t), ("PeakPagefileUsage", ctypes.c_size_t)]

    _k32.GetCurrentProcess.restype = wintypes.HANDLE
    _k32.SetPriorityClass.argtypes = [wintypes.HANDLE, wintypes.DWORD]
    _psapi.GetProcessMemoryInfo.argtypes = [wintypes.HANDLE, ctypes.POINTER(_PMC), wintypes.DWORD]
    _k32.GetSystemTimes.argtypes = [ctypes.POINTER(ctypes.c_ulonglong)] * 3
    _k32.CreateFileW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD, wintypes.LPVOID,
                                 wintypes.DWORD, wintypes.DWORD, wintypes.HANDLE]
    _k32.CreateFileW.restype = wintypes.HANDLE
    _k32.ReadFile.argtypes = [wintypes.HANDLE, wintypes.LPVOID, wintypes.DWORD,
                              ctypes.POINTER(wintypes.DWORD), wintypes.LPVOID]
    _k32.CloseHandle.argtypes = [wintypes.HANDLE]
    _k32.VirtualAlloc.argtypes = [wintypes.LPVOID, ctypes.c_size_t, wintypes.DWORD, wintypes.DWORD]
    _k32.VirtualAlloc.restype = ctypes.c_void_p
    _k32.VirtualFree.argtypes = [wintypes.LPVOID, ctypes.c_size_t, wintypes.DWORD]


def avail_mem_gb() -> float:
    if IS_WIN:
        st = _MEMSTAT()
        st.dwLength = ctypes.sizeof(st)
        _k32.GlobalMemoryStatusEx(ctypes.byref(st))
        return st.ullAvailPhys / 2**30
    try:
        return os.sysconf("SC_AVPHYS_PAGES") * os.sysconf("SC_PAGE_SIZE") / 2**30
    except (ValueError, OSError, AttributeError):
        return 8.0


def own_peak_mem_gb() -> float:
    if not IS_WIN:
        return 0.0
    pmc = _PMC()
    pmc.cb = ctypes.sizeof(pmc)
    if _psapi.GetProcessMemoryInfo(_k32.GetCurrentProcess(), ctypes.byref(pmc), pmc.cb):
        return pmc.PeakWorkingSetSize / 2**30
    return 0.0


def system_times():
    """(idle, total) 100-ns ticks for the whole machine, or None."""
    if not IS_WIN:
        return None
    idle, kern, user = ctypes.c_ulonglong(), ctypes.c_ulonglong(), ctypes.c_ulonglong()
    if not _k32.GetSystemTimes(ctypes.byref(idle), ctypes.byref(kern), ctypes.byref(user)):
        return None
    return idle.value, kern.value + user.value  # kernel time includes idle


def set_low_priority(level: str) -> None:
    if IS_WIN and level == "below_normal":
        _k32.SetPriorityClass(_k32.GetCurrentProcess(), 0x00004000)  # BELOW_NORMAL_PRIORITY_CLASS
    elif not IS_WIN and level == "below_normal":
        try:
            os.nice(5)
        except OSError:
            pass


def read_uncached(path: Path, chunk_bytes: int):
    """Yield the file in chunks, bypassing the Windows file cache (true read from the drive).
    Falls back to an ordinary read. Yields (bytes, mode)."""
    if IS_WIN:
        h = _k32.CreateFileW(str(path), 0x80000000, 0x1, None, 3, 0x20000000, None)  # GENERIC_READ, SHARE_READ, OPEN_EXISTING, NO_BUFFERING
        if h is not None and h != wintypes.HANDLE(-1).value:
            buf = _k32.VirtualAlloc(None, chunk_bytes, 0x3000, 0x04)
            try:
                if buf:
                    got = wintypes.DWORD(0)
                    while True:
                        if not _k32.ReadFile(h, buf, chunk_bytes, ctypes.byref(got), None):
                            raise OSError(f"ReadFile failed, winerror {ctypes.get_last_error()}")
                        if got.value == 0:
                            return
                        yield ctypes.string_at(buf, got.value), "uncached"
            finally:
                if buf:
                    _k32.VirtualFree(buf, 0, 0x8000)
                _k32.CloseHandle(h)
            return
    with open(path, "rb") as f:
        while True:
            b = f.read(chunk_bytes)
            if not b:
                return
            yield b, "cached"


# ---------------------------------------------------------------- deterministic patterns

if np is not None:
    _G = np.uint64(0x9E3779B97F4A7C15)
    _C1 = np.uint64(0xBF58476D1CE4E5B9)
    _C2 = np.uint64(0x94D049BB133111EB)
    _S30, _S27, _S31 = np.uint64(30), np.uint64(27), np.uint64(31)
    _ALT_A = np.uint64(0xAAAAAAAAAAAAAAAA)
    _ALT_5 = np.uint64(0x5555555555555555)
    _ONE, _M63 = np.uint64(1), np.uint64(63)


def splitmix(idx, seed: int):
    z = idx * _G + np.uint64(seed & 0xFFFFFFFFFFFFFFFF)
    z ^= z >> _S30
    z *= _C1
    z ^= z >> _S27
    z *= _C2
    z ^= z >> _S31
    return z


PATTERNS = ["scramble", "inverse-scramble", "checkerboard", "walking-ones"]


def pattern(kind: int, seed: int, start: int, count: int):
    idx = np.arange(start, start + count, dtype=np.uint64)
    if kind == 0:
        return splitmix(idx, seed)
    if kind == 1:
        return ~splitmix(idx, seed)
    if kind == 2:
        return np.where((idx & _ONE).astype(bool), _ALT_A, _ALT_5)
    return _ONE << (idx & _M63)


# ---------------------------------------------------------------- CPU checks (all deterministic)

def build_inputs() -> dict:
    data8 = splitmix(np.arange(1 << 20, dtype=np.uint64), 7).tobytes()           # 8 MB, random-looking
    # semi-compressible 8 MB: low-entropy bytes + repeated text, like image/video data
    low = (splitmix(np.arange(1 << 20, dtype=np.uint64), 11) & np.uint64(0x0303030303030303)).tobytes()
    text = (b"Heartbeat Observatory integrity check - the quick brown fox 0123456789\n" * 120000)[: 1 << 23]
    semi = low[: 1 << 22] + text[: 1 << 22]
    return {"data8": data8, "semi": semi, "small": data8[: 1 << 20]}


def _cpu_sha(inp):
    h = hashlib.sha256(inp["data8"]).digest()
    for _ in range(3):
        h = hashlib.sha256(h + inp["data8"]).digest()
    return h.hex()


def _cpu_blake(inp):
    return hashlib.blake2b(inp["data8"] + inp["semi"]).hexdigest()


def _cpu_zlib(inp):
    c = zlib.compress(inp["semi"], 6)
    d = zlib.decompress(c)                      # same inflate family ffmpeg/PNG use
    ok = d == inp["semi"]
    return f"{len(c)}:{zlib.crc32(c):08x}:{'roundtrip-ok' if ok else 'ROUNDTRIP-WRONG'}"


def _cpu_zlib_stream(inp):
    # small blocks with flushes, closer to how PNG/IDAT streams are written and read
    co = zlib.compressobj(9, zlib.DEFLATED, 15)
    parts = [co.compress(inp["semi"][i:i + 65536]) + co.flush(zlib.Z_SYNC_FLUSH)
             for i in range(0, 1 << 21, 65536)]
    parts.append(co.flush())
    c = b"".join(parts)
    do = zlib.decompressobj(15)
    d = b"".join(do.decompress(c[i:i + 4096]) for i in range(0, len(c), 4096)) + do.flush()
    ok = d == inp["semi"][: 1 << 21]
    return f"{len(c)}:{zlib.crc32(c):08x}:{'roundtrip-ok' if ok else 'ROUNDTRIP-WRONG'}"


def _cpu_lzma(inp):
    c = lzma.compress(inp["small"][:1 << 19] + inp["semi"][:1 << 19], preset=1)
    ok = lzma.decompress(c) == inp["small"][:1 << 19] + inp["semi"][:1 << 19]
    return f"{hashlib.sha256(c).hexdigest()[:32]}:{'roundtrip-ok' if ok else 'ROUNDTRIP-WRONG'}"


def _cpu_bigint(inp):
    m = (1 << 2048) - 1557
    r = pow(0x1234567890ABCDEF, (1 << 16) + 12345, m)
    r = (r * pow(3, 40000, m) + 17) % m
    return hex(r)[-64:]


def _cpu_npint(inp):
    a = splitmix(np.arange(1 << 21, dtype=np.uint64), 99)
    b = splitmix(a, 5)
    s = np.add.reduce(a * b, dtype=np.uint64)        # wraps mod 2^64, exact
    x = np.bitwise_xor.reduce(a ^ (b >> np.uint64(7)))
    return f"{int(s):016x}:{int(x):016x}"


def _cpu_npfloat(inp):
    a = splitmix(np.arange(1 << 21, dtype=np.uint64), 123)
    x = (a >> np.uint64(11)).astype(np.float64) * (2.0 ** -53)   # exact
    y = np.sqrt(x * x + 1.0) / (x + 0.5) - x * 0.25              # every op exactly rounded (IEEE)
    return f"{int(np.bitwise_xor.reduce(y.view(np.uint64))):016x}"


CPU_TESTS = {"sha256": _cpu_sha, "blake2b": _cpu_blake, "zlib": _cpu_zlib, "zlib-stream": _cpu_zlib_stream,
             "lzma": _cpu_lzma, "bigint": _cpu_bigint, "np-int": _cpu_npint, "np-float": _cpu_npfloat}


def compute_refs() -> dict:
    inp = build_inputs()
    return {name: fn(inp) for name, fn in CPU_TESTS.items()}


# ---------------------------------------------------------------- worker

def _hex(v) -> str:
    return f"0x{int(v):016x}"


def worker_main(wid: int, cfg: dict, refs: dict, q, stop_ev) -> None:
    set_low_priority(cfg["priority"])
    if cfg.get("affinity") and IS_WIN:   # pin to chosen cores (e.g. P-cores only vs E-cores only)
        _k32.SetProcessAffinityMask.argtypes = [wintypes.HANDLE, ctypes.c_size_t]
        if not _k32.SetProcessAffinityMask(_k32.GetCurrentProcess(), cfg["affinity"]):
            q.put({"type": "note", "worker": wid, "msg": f"affinity skipped, winerror {ctypes.get_last_error()}"})
    deadline = cfg["deadline"]
    stats = {"mem_gb_verified": 0.0, "mem_passes": 0, "cpu_checks": 0, "disk_gb": 0.0, "disk_files": 0,
             "disk_read_mode": None, "errors": 0}

    def done() -> bool:
        return time.time() >= deadline or stop_ev.is_set()

    def report(kind: str, **details) -> None:
        stats["errors"] += 1
        q.put({"type": "mismatch", "t": datetime.now().isoformat(timespec="seconds"), "worker": wid,
               "kind": kind, **details})

    inp = build_inputs()
    n = int(cfg["buf_gb"] * 2**30) // 8
    n -= n % CHUNK
    n = max(n, CHUNK)
    try:
        buf = np.empty(n, dtype=np.uint64)
    except MemoryError:
        q.put({"type": "note", "worker": wid, "msg": f"could not get {n * 8 / 2**30:.2f} GB of RAM; memory check skipped"})
        buf = None
    disk_left = cfg["disk_gb_per_worker"]
    workdir = Path(cfg["tempdir"])
    cycle = 0
    inject = cfg["inject"] and wid == 0

    def fill(kind: int, seed: int) -> bool:
        for s in range(0, n, CHUNK):
            if stop_ev.is_set():
                return False
            buf[s:s + CHUNK] = pattern(kind, seed, s, CHUNK)
        return True

    def verify(kind: int, seed: int, when: str) -> None:
        for s in range(0, n, CHUNK):
            exp = pattern(kind, seed, s, CHUNK)
            got = buf[s:s + CHUNK]
            neq = got != exp
            if neq.any():
                bad = np.flatnonzero(neq)
                again = buf[s:s + CHUNK][bad[:5]]
                first = int(bad[0])
                xor = int(got[first]) ^ int(exp[first])
                report("memory", pattern=PATTERNS[kind], when=when, words_wrong=int(bad.size),
                       byte_offset=(s + first) * 8, expected=_hex(exp[first]), got=_hex(got[first]),
                       bits_flipped=bin(xor).count("1"), xor=_hex(xor),
                       still_wrong_on_reread=bool(int(again[0]) != int(exp[first])),
                       note="reread fine = a read went wrong (CPU/cache/bus); still wrong = the stored value changed")
                buf[s:s + CHUNK] = exp      # repair so the same fault is not reported every pass
        stats["mem_gb_verified"] += n * 8 / 2**30
        stats["mem_passes"] += 1

    def cpu_batch(seconds: float) -> None:
        end = min(time.time() + seconds, deadline)
        while time.time() < end and not stop_ev.is_set():
            for name, fn in CPU_TESTS.items():
                try:
                    r = fn(inp)
                    err = None
                except Exception as e:  # a decode error here is itself a wrong answer
                    r, err = None, f"{type(e).__name__}: {e}"
                want = refs[name]
                if inject and name == "zlib" and stats["cpu_checks"] < len(CPU_TESTS):
                    want = want + "-INJECTED"
                stats["cpu_checks"] += 1
                if r != want:
                    report("cpu", test=name, expected=str(want)[:80], got=str(r)[:80], error=err)

    def disk_cycle() -> float:
        chunks = cfg["disk_mb"] // 8
        path = workdir / f"w{wid}-c{cycle}.bin"
        seed = (wid << 32) | cycle
        hashes = []
        try:
            with open(path, "wb", buffering=0) as f:
                for ci in range(chunks):
                    b = pattern(0, seed ^ 0xD15C, ci * DISK_CHUNK_ELEMS, DISK_CHUNK_ELEMS).tobytes()
                    hashes.append(hashlib.sha256(b).digest())
                    f.write(b)
                f.flush()
                os.fsync(f.fileno())
            if inject and cycle == 0:
                with open(path, "r+b") as f:       # turn 11 bytes to zero, like the bad mp4
                    f.seek(3 * 8 * 2**20 + 777)
                    f.write(b"\x00" * 11)
                    f.flush()
                    os.fsync(f.fileno())
            got_chunks = 0
            for ci, (b, mode) in enumerate(read_uncached(path, 8 * 2**20)):
                got_chunks = ci + 1
                stats["disk_read_mode"] = mode
                if ci >= len(hashes) or hashlib.sha256(b).digest() != hashes[ci]:
                    exp = pattern(0, seed ^ 0xD15C, ci * DISK_CHUNK_ELEMS, DISK_CHUNK_ELEMS).tobytes()
                    e8 = np.frombuffer(exp, dtype=np.uint8)
                    g8 = np.frombuffer(b.ljust(len(exp), b"\x00")[: len(exp)], dtype=np.uint8)
                    diff = np.flatnonzero(e8 != g8)
                    with open(path, "rb") as f:     # second look through the normal (cached) path
                        f.seek(ci * len(exp))
                        again = f.read(len(exp))
                    report("disk", file_chunk=ci, byte_offset=ci * len(exp) + (int(diff[0]) if diff.size else 0),
                           bytes_wrong=int(diff.size), bytes_now_zero=int((g8[diff] == 0).sum()) if diff.size else 0,
                           read_mode=mode, short_read=len(b) != len(exp),
                           still_wrong_on_reread=hashlib.sha256(again).digest() != hashes[ci] if ci < len(hashes) else True)
            if got_chunks < len(hashes):   # file came back shorter than written: missing chunks never compared
                report("disk", file_chunk=got_chunks, byte_offset=got_chunks * 8 * 2**20,
                       bytes_wrong=(len(hashes) - got_chunks) * 8 * 2**20, bytes_now_zero=0,
                       read_mode=stats["disk_read_mode"], short_read=True, still_wrong_on_reread=None,
                       note=f"read back only {got_chunks} of {len(hashes)} chunks")
            stats["disk_files"] += 1
            return chunks * 8 / 1024
        except OSError as e:
            q.put({"type": "note", "worker": wid, "msg": f"disk check skipped this cycle: {e}"})
            return 0.0
        finally:
            try:
                path.unlink()
            except OSError:
                pass

    try:
        while not done():
            kind = cycle % len(PATTERNS)
            seed = (wid * 1_000_003 + cycle * 7919) & 0xFFFFFFFF
            filled = buf is not None and fill(kind, seed)
            if filled:
                if inject and cycle == 0:
                    buf[12345] ^= np.uint64(1 << 37)     # one flipped bit, like a weak RAM cell
                verify(kind, seed, "right after writing")
            cpu_batch(cfg["cpu_seconds"])
            if disk_left >= cfg["disk_mb"] / 1024 and not done():
                wrote = disk_cycle()
                disk_left -= wrote
                stats["disk_gb"] += wrote
            if filled and not stop_ev.is_set():
                verify(kind, seed, "after holding it while other work ran")
            cycle += 1
            q.put({"type": "progress", "worker": wid, "cycle": cycle, **stats})
    except MemoryError:
        q.put({"type": "note", "worker": wid, "msg": "ran out of memory; stopped early (not a hardware error)"})
    t = os.times()
    stats.update(cpu_seconds=round(t.user + t.system, 1), peak_mem_gb=round(own_peak_mem_gb(), 2), cycles=cycle)
    q.put({"type": "done", "worker": wid, **stats})


# ---------------------------------------------------------------- parent

def write_logs(run: dict) -> None:
    LOG_MD.parent.mkdir(parents=True, exist_ok=True)
    if not LOG_MD.exists():
        LOG_MD.write_text(
            "# Integrity self-test log\n\n"
            "Written by `tools/integrity_test.py` (how to read it: top of that file, and below). Newest last.\n"
            "CLEAN = every memory read, CPU answer and disk read-back was right. ANY wrong answer on a clean\n"
            "machine is not normal: one is a warning, two in different runs means hardware.\n\n", encoding="utf-8")
    m = run["mismatches"]
    kinds = ", ".join(f"{k} {v}" for k, v in run["mismatch_by_kind"].items()) or "none"
    line = (f"- {run['started'][:16].replace('T', ' ')} | **{run['result']}** | {run['minutes']} min | "
            f"{run['workers']} workers, {run['priority']} | RAM {run['mem_gb_planned']} GB, {run['mem_passes']} passes "
            f"({run['mem_gb_verified']:.0f} GB checked) | {run['cpu_checks']} CPU answers | "
            f"disk {run['disk_gb']:.1f} GB written+read ({run['disk_read_mode'] or 'n/a'}) | "
            f"wrong: {m} ({kinds}) | whole-machine CPU {run['system_cpu_pct']}% | {run['note'] or ''}".rstrip(" |") + "\n")
    with open(LOG_MD, "a", encoding="utf-8") as f:
        f.write(line)
    data = {"runs": []}
    if LOG_JSON.exists():
        try:
            data = json.loads(LOG_JSON.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            data = {"runs": []}
    data.setdefault("runs", []).append(run)
    data["runs"] = data["runs"][-365:]
    data["updated"] = run["ended"]
    LOG_JSON.write_text(json.dumps(data, indent=1), encoding="utf-8")


def main() -> int:
    cores = os.cpu_count() or 4
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--minutes", type=float, default=5.0)
    ap.add_argument("--workers", type=int, default=max(1, min(8, (cores - 1) // 4)),
                    help="worker processes (default: one per ~4 logical cores, max 8)")
    ap.add_argument("--mem-gb", type=float, default=6.0, help=f"total RAM to test (capped at {MEM_CAP_GB:.0f})")
    ap.add_argument("--disk-mb", type=int, default=128, help="file size per disk check (multiple of 8)")
    ap.add_argument("--disk-gb-max", type=float, default=None, help="total disk writes per run (default 1.2 GB per minute, max 24)")
    ap.add_argument("--cpu-seconds", type=float, default=8.0, help="CPU checks per cycle")
    ap.add_argument("--priority", choices=["below_normal", "normal"], default="below_normal")
    ap.add_argument("--inject", action="store_true", help="plant one fake error of each kind to prove detection (not logged)")
    ap.add_argument("--no-log", action="store_true")
    ap.add_argument("--affinity", type=lambda s: int(s, 16), default=0,
                    help="hex core mask for the workers, e.g. FFFF = logical 0-15 (usually the P-cores on a 14900HX; check first), "
                         "FFFF0000 = logical 16-31 (E-cores). Low priority alone lets Windows park work on E-cores.")
    args = ap.parse_args()
    if np is None:
        print("numpy is not installed; this test needs it (no downloads allowed by design).")
        return 2

    workers = max(1, min(args.workers, cores - 1))
    avail0 = avail_mem_gb()
    mem_gb = min(args.mem_gb, MEM_CAP_GB, max(0.5, avail0 - 4.0))   # always leave 4 GB for everything else
    buf_gb = max(0.1, mem_gb / workers - WORKER_OVERHEAD_GB)
    disk_mb = max(8, args.disk_mb - args.disk_mb % 8)
    disk_max = args.disk_gb_max if args.disk_gb_max is not None else min(24.0, 1.2 * args.minutes)
    disk_max = max(disk_max, workers * disk_mb / 1024)   # at least one file per worker, or short runs never test the disk
    log = not (args.no_log or args.inject)

    set_low_priority(args.priority)
    print(f"integrity_test: {args.minutes} min, {workers} workers on {cores} logical cores, "
          f"RAM {mem_gb:.1f} GB ({buf_gb:.2f} GB buffer each; {avail0:.1f} GB was free), "
          f"disk up to {disk_max:.1f} GB, priority {args.priority}{', INJECT mode' if args.inject else ''}", flush=True)

    refs = compute_refs()
    refs2 = compute_refs()
    pre = [{"type": "mismatch", "t": datetime.now().isoformat(timespec="seconds"), "worker": -1, "kind": "cpu",
            "test": k, "expected": refs[k][:80], "got": refs2[k][:80], "error": "reference computed twice, differed"}
           for k in refs if refs[k] != refs2[k]]

    run_id = datetime.now().strftime("%Y%m%d-%H%M%S")
    tdir = TEMP_ROOT / f"run-{run_id}-{os.getpid()}"
    tdir.mkdir(parents=True, exist_ok=True)
    started = datetime.now()
    deadline = time.time() + args.minutes * 60
    cfg = {"deadline": deadline, "buf_gb": buf_gb, "disk_mb": disk_mb, "disk_gb_per_worker": disk_max / workers,
           "cpu_seconds": args.cpu_seconds, "priority": args.priority, "tempdir": str(tdir), "inject": args.inject,
           "affinity": args.affinity}

    ctx = mp.get_context("spawn")
    q = ctx.Queue()
    stop_ev = ctx.Event()
    procs = [ctx.Process(target=worker_main, args=(i, cfg, refs, q, stop_ev), daemon=True) for i in range(workers)]
    st0 = system_times()
    mismatches, notes, done_msgs, last_progress = list(pre), [], {}, {}
    total_mismatch = len(pre)
    by_kind: dict = {}
    for m in pre:
        by_kind[m["kind"]] = by_kind.get(m["kind"], 0) + 1
    min_avail, aborted, next_print = avail0, None, time.time() + 30
    try:
        for p in procs:
            p.start()
        while any(p.is_alive() for p in procs) or not q.empty():
            try:
                msg = q.get(timeout=1.0)
            except queue.Empty:
                msg = None
            if msg:
                t = msg.pop("type")
                if t == "mismatch":
                    total_mismatch += 1
                    by_kind[msg["kind"]] = by_kind.get(msg["kind"], 0) + 1
                    if len(mismatches) < MAX_DETAILS:
                        mismatches.append(msg)
                    print(f"  WRONG [{msg['t']}] worker {msg['worker']} {msg['kind']}: "
                          f"{json.dumps({k: v for k, v in msg.items() if k not in ('t', 'worker', 'kind', 'note')})}", flush=True)
                elif t == "note":
                    notes.append(f"w{msg['worker']}: {msg['msg']}")
                    print(f"  note: worker {msg['worker']}: {msg['msg']}", flush=True)
                elif t == "progress":
                    last_progress[msg["worker"]] = msg
                elif t == "done":
                    done_msgs[msg["worker"]] = msg
            a = avail_mem_gb()
            min_avail = min(min_avail, a)
            if a < 1.5 and not stop_ev.is_set():
                aborted = f"stopped early: free RAM fell to {a:.1f} GB (giving it back to the other programs)"
                print("  " + aborted, flush=True)
                stop_ev.set()
            now = time.time()
            if now >= next_print and now < deadline:
                left = (deadline - now) / 60
                print(f"  ... {left:.1f} min left, {total_mismatch} wrong so far, free RAM {a:.1f} GB", flush=True)
                next_print = now + 30
            if now > deadline + 180 and not stop_ev.is_set():
                stop_ev.set()
            if now > deadline + 300:
                for p in procs:
                    if p.is_alive():
                        p.terminate()
                        notes.append(f"worker {procs.index(p)} hung and was stopped")
                break
    except KeyboardInterrupt:
        stop_ev.set()
        aborted = "stopped by Ctrl-C"
        for p in procs:
            p.join(timeout=30)
    finally:
        for p in procs:
            p.join(timeout=10)
        shutil.rmtree(tdir, ignore_errors=True)
        try:
            TEMP_ROOT.rmdir()   # only if empty
        except OSError:
            pass
    st1 = system_times()

    for i, p in enumerate(procs):
        if i not in done_msgs and p.exitcode not in (0, None):
            code = p.exitcode & 0xFFFFFFFF if p.exitcode < 0 or p.exitcode > 255 else p.exitcode
            total_mismatch += 1
            by_kind["crash"] = by_kind.get("crash", 0) + 1
            mismatches.append({"t": datetime.now().isoformat(timespec="seconds"), "worker": i, "kind": "crash",
                               "exitcode": hex(code),
                               "note": "the worker died on its own (0xc0000005 = access violation, like the ffmpeg segfault)"})

    finals = [done_msgs.get(i) or last_progress.get(i) or {} for i in range(workers)]
    s = lambda key: sum((f.get(key) or 0) for f in finals)
    sys_cpu = None
    if st0 and st1 and st1[1] > st0[1]:
        sys_cpu = round(100 * (1 - (st1[0] - st0[0]) / (st1[1] - st0[1])))
    ended = datetime.now()
    skipped = [n for n in notes if "skipped" in n or "stopped early" in n or "hung" in n]
    if not s("disk_files"):
        skipped.append("disk check never ran")
    if not s("mem_passes"):
        skipped.append("memory check never ran")
    if skipped and not aborted:   # a check that never ran must not be reported as CLEAN
        aborted = "some checks did not run: " + "; ".join(skipped[:3])
    result = "WRONG ANSWERS" if total_mismatch else ("INCOMPLETE" if aborted else "CLEAN")
    run = {
        "started": started.isoformat(timespec="seconds"), "ended": ended.isoformat(timespec="seconds"),
        "minutes": round((ended - started).total_seconds() / 60, 1), "result": result, "inject": args.inject,
        "workers": workers, "logical_cores": cores, "priority": args.priority, "affinity": hex(args.affinity) if args.affinity else None,
        "mem_gb_planned": round(mem_gb, 1), "free_ram_gb_start": round(avail0, 1), "free_ram_gb_min": round(min_avail, 1),
        "mem_passes": int(s("mem_passes")), "mem_gb_verified": round(s("mem_gb_verified"), 1),
        "cpu_checks": int(s("cpu_checks")), "disk_gb": round(s("disk_gb"), 2),
        "disk_files": int(s("disk_files")),
        "disk_read_mode": next((f.get("disk_read_mode") for f in finals if f.get("disk_read_mode")), None),
        "worker_cpu_seconds": round(s("cpu_seconds"), 1), "worker_peak_mem_gb_sum": round(s("peak_mem_gb"), 2),
        "system_cpu_pct": sys_cpu, "mismatches": total_mismatch, "mismatch_by_kind": by_kind,
        "details": mismatches[:MAX_DETAILS], "notes": notes, "note": aborted,
        "python": sys.version.split()[0], "numpy": np.__version__,
    }
    print(f"\nRESULT: {result} - {total_mismatch} wrong answers {by_kind or ''}")
    print(f"  checked {run['mem_gb_verified']:.0f} GB of RAM reads in {run['mem_passes']} passes, "
          f"{run['cpu_checks']} CPU answers, {run['disk_gb']:.1f} GB disk write+read ({run['disk_read_mode']})")
    print(f"  used: {run['worker_cpu_seconds']} CPU-seconds, peak RAM {run['worker_peak_mem_gb_sum']} GB (all workers), "
          f"whole-machine CPU {sys_cpu}% average, free RAM low point {min_avail:.1f} GB")
    if log:
        write_logs(run)
        print(f"  logged to {LOG_MD.relative_to(ROOT)} and {LOG_JSON.relative_to(ROOT)}")
    if total_mismatch:
        return 1
    return 2 if aborted else 0


if __name__ == "__main__":
    sys.exit(main())
