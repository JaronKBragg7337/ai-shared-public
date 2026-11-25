"""data_hunt.py - catch the exact bytes when the MSI gets data wrong, and what the machine was doing.

Why this exists (Fable, Tue 11/24/2026): the nightly self-test (integrity_test.py) has come back clean six
times, yet real work keeps getting hurt: a PNG that ffmpeg could not read seconds after it was written, video
files with single bytes turned to zero, a database index that went bad only inside the running program. The
nightly test loads every core at once on a cool machine and reads its files back PAST the Windows file cache.
The real damage happened in the cache-and-memory path, in short bursts, while the machine was busy and hot.

So this test watches the paths the real failures went through, and when something is wrong it writes down
exactly WHICH bytes, at which positions, what they should have been and what they were. The pattern of the
damage is what tells the suspects apart:
  - the same byte position in every 8 bytes      -> a memory stick's data line (RAM)
  - an even stride, always zeros                 -> a program (a driver) writing where it should not
  - no pattern, or only in the answers of a core -> the processor itself

Four watchers run side by side (each can be switched off):
  hold     keep big blocks of known data in memory and re-check every byte, again and again
  cache    keep known files in the Windows file cache and re-read them the ordinary way; if a read is
           wrong, read the same spot straight from the drive to see whether the drive copy is wrong too
  fresh    write a new file, and have a SECOND program read it at once (what ffmpeg does to a new frame);
           every 4th file is a real PNG that the real ffmpeg decodes
  percore  short bursts of work with a known answer on one processor core at a time, with rests between

No admin rights, no downloads. It deletes its own files. Heat, speed and the graphics card are logged every
5 seconds so a hit can be matched to what the machine was doing.

Usage:
  python tools/data_hunt.py --minutes 10 --label idle
  python tools/data_hunt.py --minutes 10 --label "intel graphics busy"
  python tools/data_hunt.py --minutes 1 --inject        # plant one fake error per watcher; proves it catches them
Exit codes: 0 clean, 1 at least one hit (or a watcher died), 2 could not run properly.
Logs: state/msi-data-hunt-log.jsonl (every detail), state/msi-data-hunt-runs.md (one line per run).
"""
from __future__ import annotations

import argparse
import ctypes
import hashlib
import json
import multiprocessing as mp
import os
import queue
import random
import shutil
import struct
import subprocess
import sys
import tempfile
import time
import zlib
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import integrity_test as it  # noqa: E402  (the known patterns, the answer checks, the past-the-cache reader)

np = it.np
ROOT = Path(__file__).resolve().parent.parent
LOG_JSONL = ROOT / "state" / "msi-data-hunt-log.jsonl"
LOG_MD = ROOT / "state" / "msi-data-hunt-runs.md"
# Helper programs (ffmpeg, nvidia-smi) are started with "no window". Started from a windowless program (pythonw, the
# Task Scheduler) each launch otherwise gets a brand-new console = a new Windows Terminal tab: 1.7 s each (11/24).
NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)
MB8 = 8 * 2**20                 # files are written and checked 8 MB at a time
ELEMS8 = MB8 // 8               # that many 8-byte numbers
MAX_LIST = 200                  # how many damaged positions to write down per hit


# ---------------------------------------------------------------- describing damage

def describe(expected, got, base_offset: int = 0, address: int | None = None) -> dict:
    """Compare two byte strings and write down every way they differ."""
    e = np.frombuffer(expected, dtype=np.uint8) if isinstance(expected, (bytes, bytearray)) else expected
    g = np.frombuffer(got, dtype=np.uint8) if isinstance(got, (bytes, bytearray)) else got
    n = min(e.size, g.size)
    bad = np.flatnonzero(e[:n] != g[:n])
    out = {"bytes_wrong": int(bad.size), "length_expected": int(e.size), "length_got": int(g.size)}
    if not bad.size:
        return out
    first, last = int(bad[0]), int(bad[-1])
    offs = [int(b) + base_offset for b in bad[:MAX_LIST]]
    where = [o + address for o in offs] if address is not None else offs      # real memory address, or place in the file
    lo, hi = max(0, first - 24), min(n, first + 40)
    out.update(
        first_offset=offs[0], last_offset=last + base_offset, span_bytes=last - first + 1,
        offsets=offs, expected=[int(v) for v in e[bad[:MAX_LIST]]], got=[int(v) for v in g[bad[:MAX_LIST]]],
        became_zero=int((g[bad] == 0).sum()), became_ff=int((g[bad] == 255).sum()),
        bits_flipped=[bin(int(a) ^ int(b)).count("1") for a, b in zip(e[bad[:50]], g[bad[:50]])],
        position_in_8=sorted({w % 8 for w in where}), position_in_64=sorted({w % 64 for w in where})[:64],
        position_in_page=[w % 4096 for w in where[:50]],
        gaps_between=[offs[i + 1] - offs[i] for i in range(min(len(offs) - 1, 49))],
        window_expected=bytes(e[lo:hi]).hex(), window_got=bytes(g[lo:hi]).hex(), window_starts_at=lo + base_offset)
    return out


def read_past_cache(path: Path) -> bytes | None:
    """The whole file straight from the drive (Windows flushes its own pending writes first)."""
    try:
        parts, mode = [], None
        for b, mode in it.read_uncached(path, MB8):
            parts.append(b)
        return b"".join(parts) if mode == "uncached" else None
    except OSError:
        return None


def chunk_bytes(seed: int, index: int) -> bytes:
    return it.pattern(0, seed, index * ELEMS8, ELEMS8).tobytes()


# ---------------------------------------------------------------- watcher: hold (memory)

def hold_worker(wid: int, cfg: dict, q, stop) -> None:
    n = int(cfg["mem_gb_each"] * 2**30) // 8
    n = max(it.CHUNK, n - n % it.CHUNK)
    seed = 0xA11CE000 + wid
    stats = {"watcher": "hold", "worker": wid, "passes": 0, "gb_checked": 0.0, "hits": 0}
    try:
        buf = np.empty(n, dtype=np.uint64)
    except MemoryError:
        q.put({"type": "note", "msg": f"hold {wid}: could not get {n * 8 / 2**30:.1f} GB of memory"})
        q.put({"type": "done", **stats})
        return
    for s in range(0, n, it.CHUNK):
        buf[s:s + it.CHUNK] = it.pattern(0, seed, s, it.CHUNK)
    base = buf.ctypes.data
    if cfg["inject"] and wid == 0:
        b8 = buf.view(np.uint8)
        for off in (1_000_003, 1_000_011, 1_004_099):      # three single bytes -> zero, like the damaged video
            b8[off] = 0
    while time.time() < cfg["deadline"] and not stop.is_set():
        for s in range(0, n, it.CHUNK):
            snap = buf[s:s + it.CHUNK].copy()                 # one look at the memory
            exp = it.pattern(0, seed, s, it.CHUNK)
            if not np.array_equal(snap, exp):
                exp2 = it.pattern(0, seed, s, it.CHUNK)       # was the ANSWER worked out wrong?
                if not np.array_equal(exp, exp2):
                    stats["hits"] += 1
                    q.put({"type": "hit", "watcher": "hold", "worker": wid, "what": "the known pattern came out "
                           "different when worked out twice (a processor answer was wrong)",
                           **describe(exp.view(np.uint8), exp2.view(np.uint8), s * 8)})
                    exp = it.pattern(0, seed, s, it.CHUNK)
                second = buf[s:s + it.CHUNK].copy()           # a second look at the same memory
                d = describe(exp.view(np.uint8), snap.view(np.uint8), s * 8, base)
                if d["bytes_wrong"]:
                    stats["hits"] += 1
                    still = not np.array_equal(second, exp)
                    q.put({"type": "hit", "watcher": "hold", "worker": wid, "still_wrong_on_second_look": still,
                           "what": ("the stored bytes changed in memory" if still else
                                    "the bytes read wrong once and right the second time (a bad read or copy)"),
                           "memory_address_of_first": hex(base + d["first_offset"]), **d})
                buf[s:s + it.CHUNK] = it.pattern(0, seed, s, it.CHUNK)      # mend, so one fault is one report
            if time.time() >= cfg["deadline"] or stop.is_set():
                break
        else:
            stats["passes"] += 1
        stats["gb_checked"] += n * 8 / 2**30
        q.put({"type": "progress", **stats})
        time.sleep(cfg["hold_pause"])
    q.put({"type": "done", **stats})


# ---------------------------------------------------------------- watcher: cache (held files)

def cache_worker(cfg: dict, q, stop) -> None:
    folder = Path(cfg["dir"]) / "held"
    folder.mkdir(parents=True, exist_ok=True)
    per_file = cfg["held_file_mb"] // 8
    count = max(1, int(cfg["held_gb"] * 1024) // cfg["held_file_mb"])
    stats = {"watcher": "cache", "files": count, "passes": 0, "gb_checked": 0.0, "hits": 0}

    def write(i: int) -> None:
        with open(folder / f"held-{i}.bin", "wb") as f:      # the ordinary way: no flush asked for
            for ci in range(per_file):
                f.write(chunk_bytes(0xF11E0000 + i, ci))

    try:
        for i in range(count):
            write(i)
            if stop.is_set():
                break
        if cfg["inject"]:
            with open(folder / "held-0.bin", "r+b") as f:
                for off in (5_000_001, 5_000_017, 5_003_333):
                    f.seek(off)
                    f.write(b"\x00")
        while time.time() < cfg["deadline"] and not stop.is_set():
            for i in range(count):
                path = folder / f"held-{i}.bin"
                with open(path, "rb") as f:
                    for ci in range(per_file):
                        got = f.read(MB8)
                        exp = chunk_bytes(0xF11E0000 + i, ci)
                        if got != exp:
                            if chunk_bytes(0xF11E0000 + i, ci) != exp:
                                exp = chunk_bytes(0xF11E0000 + i, ci)
                                q.put({"type": "note", "msg": "cache: a known pattern came out different twice"})
                            d = describe(exp, got, ci * MB8)
                            with open(path, "rb") as f2:              # second ordinary read
                                f2.seek(ci * MB8)
                                again = f2.read(MB8)
                            whole = read_past_cache(path)             # straight from the drive
                            drive = None if whole is None else whole[ci * MB8:(ci + 1) * MB8]
                            stats["hits"] += 1
                            q.put({"type": "hit", "watcher": "cache", "file": path.name,
                                   "still_wrong_on_second_read": again != exp,
                                   "drive_copy_wrong": None if drive is None else drive != exp,
                                   "what": "a file kept in the Windows file cache read back different from what was written",
                                   **d})
                            write(i)                                   # mend
                            break
                stats["gb_checked"] += per_file * 8 / 1024
                if time.time() >= cfg["deadline"] or stop.is_set():
                    break
            else:
                stats["passes"] += 1
            q.put({"type": "progress", **stats})
            time.sleep(cfg["cache_pause"])
    except OSError as e:
        q.put({"type": "note", "msg": f"cache watcher stopped: {e}"})
    finally:
        shutil.rmtree(folder, ignore_errors=True)
    q.put({"type": "done", **stats})


# ---------------------------------------------------------------- watcher: fresh (new file, read at once)

def reader_main(inq, outq) -> None:
    """The second program: opens the file it is told about, reads all of it, says what it saw."""
    while True:
        path = inq.get()
        if path is None:
            return
        err = None
        for _ in range(5):
            try:
                with open(path, "rb") as f:
                    data = f.read()
                outq.put((len(data), hashlib.blake2b(data).hexdigest(), None))
                break
            except OSError as e:          # something (the virus scanner) held the file for a moment
                err = str(e)
                time.sleep(0.05)
        else:
            outq.put((0, None, err))


def make_png(seed: int, rng: random.Random | None = None, h: int = 1080) -> bytes:
    """A real PNG the size of a video frame, made here so every byte of the file is known."""
    w, h = 1920, (rng.choice([270, 540, 1080, 1080, 1080, 2160]) if rng else h)
    px = (it.pattern(0, seed, 0, (w * 3 * h + 7) // 8).view(np.uint8)[: w * 3 * h] & 0x1F).reshape(h, w * 3)
    raw = np.concatenate([np.zeros((h, 1), dtype=np.uint8), px], axis=1).tobytes()     # filter byte 0 on every row
    def part(kind: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data))
    return (b"\x89PNG\r\n\x1a\n" + part(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
            + part(b"IDAT", zlib.compress(raw, 1)) + part(b"IEND", b""))


def fresh_worker(cfg: dict, q, stop) -> None:
    folder = Path(cfg["dir"]) / "fresh"
    keep = Path(cfg["evidence"])
    folder.mkdir(parents=True, exist_ok=True)
    rng = random.Random(20261124)
    ctx = mp.get_context("spawn")
    inq, outq = ctx.Queue(), ctx.Queue()
    reader = ctx.Process(target=reader_main, args=(inq, outq), daemon=True)
    reader.start()
    ffmpeg = cfg["ffmpeg"]
    stats = {"watcher": "fresh", "files": 0, "gb_written": 0.0, "pngs_decoded": 0, "later_looks": 0, "hits": 0}
    ring: list[tuple[Path, str, float]] = []           # files kept a little while for a second look
    t0, n = time.time(), 0

    def hit(what: str, path: Path, exp: bytes, extra: dict) -> None:
        stats["hits"] += 1
        try:
            with open(path, "rb") as f:
                now = f.read()
        except OSError:
            now = b""
        drive = read_past_cache(path)
        saved = None
        try:
            keep.mkdir(parents=True, exist_ok=True)
            saved = keep / f"{datetime.now():%Y%m%d-%H%M%S}-{path.name}"
            shutil.copyfile(path, saved)
            (saved.with_suffix(saved.suffix + ".expected")).write_bytes(exp)
        except OSError:
            saved = None
        q.put({"type": "hit", "watcher": "fresh", "file": path.name, "what": what,
               "ordinary_read_now_wrong": now != exp, "drive_copy_wrong": None if drive is None else drive != exp,
               "kept_copy": str(saved) if saved else None, **extra, **describe(exp, now)})

    try:
        while time.time() < cfg["deadline"] and not stop.is_set():
            n += 1
            is_png = n % 4 == 0
            if is_png:
                exp = make_png(n, rng)
            else:
                size = rng.randint(64 * 1024, 12 * 2**20)
                exp = it.pattern(0, 0xF4E5000000 + n, 0, (size + 7) // 8).tobytes()[:size]
            want = hashlib.blake2b(exp).hexdigest()
            path = folder / (f"f{n}.png" if is_png else f"f{n}.bin")
            data = exp
            if cfg["inject"] and n == 2:
                data = exp[:70_001] + b"\x00" + exp[70_002:]
            with open(path, "wb") as f:                 # the ordinary way, then closed
                f.write(data)
            inq.put(str(path))
            try:
                got_len, got_hash, err = outq.get(timeout=120)
            except queue.Empty:
                q.put({"type": "note", "msg": "fresh: the reading program did not answer in 2 minutes"})
                break
            stats["files"] += 1
            stats["gb_written"] += len(exp) / 2**30
            if err:
                q.put({"type": "note", "msg": f"fresh: could not open {path.name}: {err}"})
            elif got_hash != want:
                hit("a second program read a just-written file and saw different bytes", path, exp,
                    {"reader_saw_length": got_len, "written_length": len(exp)})
            if is_png and ffmpeg and not stop.is_set():
                r = subprocess.run([ffmpeg, "-v", "error", "-nostdin", "-i", str(path), "-f", "null", "-"],
                                   capture_output=True, text=True, errors="replace", creationflags=NO_WINDOW)
                stats["pngs_decoded"] += 1
                if r.returncode != 0 or r.stderr.strip():
                    fails = 0
                    for _ in range(5):
                        r2 = subprocess.run([ffmpeg, "-v", "error", "-nostdin", "-i", str(path), "-f", "null", "-"],
                                            capture_output=True, text=True, errors="replace", creationflags=NO_WINDOW)
                        fails += r2.returncode != 0 or bool(r2.stderr.strip())
                    hit("the real ffmpeg could not decode a just-written PNG", path, exp,
                        {"ffmpeg_said": r.stderr.strip()[:300], "ffmpeg_exit": r.returncode & 0xFFFFFFFF,
                         "failed_again_out_of_5": fails})
            ring.append((path, want, time.time()))
            while ring and (len(ring) > 24 or time.time() - ring[0][2] > 30):
                old, old_hash, _ = ring.pop(0)
                try:
                    with open(old, "rb") as f:
                        later = f.read()
                    stats["later_looks"] += 1
                    if hashlib.blake2b(later).hexdigest() != old_hash:
                        seed_n = int(old.stem[1:])
                        q.put({"type": "note", "msg": f"fresh: {old.name} was right at first and wrong later (file {seed_n})"})
                        stats["hits"] += 1
                        q.put({"type": "hit", "watcher": "fresh", "file": old.name,
                               "what": "a file that read right at first read wrong half a minute later",
                               "bytes_wrong": -1})
                    old.unlink()
                except OSError:
                    pass
            if n % 20 == 0:
                q.put({"type": "progress", **stats})
            ahead = stats["gb_written"] * 1024 / cfg["fresh_mb_s"] - (time.time() - t0)
            if ahead > 0:
                time.sleep(min(ahead, 2.0))
    finally:
        inq.put(None)
        reader.join(timeout=5)
        if reader.is_alive():
            reader.terminate()
        shutil.rmtree(folder, ignore_errors=True)
    q.put({"type": "done", **stats})


# ---------------------------------------------------------------- watcher: percore (bursts, one core at a time)

def percore_worker(cfg: dict, refs: dict, q, stop) -> None:
    k32 = it._k32
    k32.GetCurrentThread.restype = ctypes.c_void_p
    k32.SetThreadAffinityMask.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
    k32.SetThreadAffinityMask.restype = ctypes.c_size_t
    inp = it.build_inputs()
    cores = list(range(os.cpu_count() or 1))
    rng = random.Random(7)
    per = {c: [0, 0] for c in cores}                     # core -> [answers checked, answers wrong]
    stats = {"watcher": "percore", "answers": 0, "rounds": 0, "hits": 0}
    first = True
    while time.time() < cfg["deadline"] and not stop.is_set():
        rng.shuffle(cores)
        for c in cores:
            if not k32.SetThreadAffinityMask(k32.GetCurrentThread(), 1 << c):
                continue
            end = time.perf_counter() + cfg["burst_s"]
            while True:
                for name, fn in it.CPU_TESTS.items():
                    try:
                        r, err = fn(inp), None
                    except Exception as e:               # a decode error here is itself a wrong answer
                        r, err = None, f"{type(e).__name__}: {e}"
                    plant = cfg["inject"] and first and name == "zlib"
                    want = refs[name] + ("-INJECTED" if plant else "")
                    first = first and not plant
                    per[c][0] += 1
                    stats["answers"] += 1
                    if r != want:
                        per[c][1] += 1
                        stats["hits"] += 1
                        q.put({"type": "hit", "watcher": "percore", "core": c, "test": name,
                               "what": f"processor core {c} gave a wrong answer on a job with a known answer",
                               "expected": str(want)[:80], "got": str(r)[:80], "error": err, "bytes_wrong": -1})
                if time.perf_counter() >= end:
                    break
            time.sleep(rng.uniform(0.0, cfg["burst_rest_s"]))     # let the core rest, then wake the next one
            if time.time() >= cfg["deadline"] or stop.is_set():
                break
        stats["rounds"] += 1
        q.put({"type": "progress", **stats})
    stats["per_core"] = {str(c): v for c, v in sorted(per.items())}
    q.put({"type": "done", **stats})


# ---------------------------------------------------------------- heat, speed, graphics card

class _PdhValue(ctypes.Structure):
    _fields_ = [("CStatus", ctypes.c_ulong), ("doubleValue", ctypes.c_double)]


class Sensors:
    """What Windows will tell an ordinary program: the heat zone, how busy and how fast the processor is."""
    PATHS = {"zone": r"\Thermal Zone Information(\_TZ.THRM)\High Precision Temperature",
             "busy": r"\Processor Information(_Total)\% Processor Utility",
             "speed": r"\Processor Information(_Total)\% Processor Performance"}

    def __init__(self) -> None:
        self.counters, self.next_gpu, self.gpu = {}, 0.0, {}
        try:
            self.pdh = ctypes.WinDLL("pdh")
            self.pdh.PdhOpenQueryW.argtypes = [ctypes.c_wchar_p, ctypes.c_size_t, ctypes.POINTER(ctypes.c_void_p)]
            self.pdh.PdhAddEnglishCounterW.argtypes = [ctypes.c_void_p, ctypes.c_wchar_p, ctypes.c_size_t,
                                                       ctypes.POINTER(ctypes.c_void_p)]
            self.pdh.PdhCollectQueryData.argtypes = [ctypes.c_void_p]
            self.pdh.PdhGetFormattedCounterValue.argtypes = [ctypes.c_void_p, ctypes.c_ulong, ctypes.c_void_p,
                                                             ctypes.POINTER(_PdhValue)]
            self.query = ctypes.c_void_p()
            if self.pdh.PdhOpenQueryW(None, 0, ctypes.byref(self.query)) == 0:
                for key, path in self.PATHS.items():
                    h = ctypes.c_void_p()
                    if self.pdh.PdhAddEnglishCounterW(self.query, path, 0, ctypes.byref(h)) == 0:
                        self.counters[key] = h
                self.pdh.PdhCollectQueryData(self.query)
        except (OSError, AttributeError):
            self.counters = {}

    def read(self) -> dict:
        out = {"t": datetime.now().strftime("%H:%M:%S")}
        if self.counters:
            self.pdh.PdhCollectQueryData(self.query)
            for key, h in self.counters.items():
                v = _PdhValue()
                if self.pdh.PdhGetFormattedCounterValue(h, 0x200, None, ctypes.byref(v)) == 0:
                    out[key] = round(v.doubleValue / 10 - 273.15, 1) if key == "zone" else round(v.doubleValue)
        if time.time() >= self.next_gpu:
            self.next_gpu = time.time() + 10
            try:
                r = subprocess.run(["nvidia-smi", "--query-gpu=temperature.gpu,utilization.gpu,power.draw",
                                    "--format=csv,noheader,nounits"], capture_output=True, text=True, timeout=8,
                                   creationflags=NO_WINDOW)
                a = [x.strip() for x in r.stdout.strip().split(",")]
                self.gpu = {"gpu_c": float(a[0]), "gpu_busy": float(a[1]), "gpu_w": float(a[2])}
            except (OSError, ValueError, IndexError, subprocess.SubprocessError):
                self.gpu = {}
        out.update(self.gpu)
        return out


def runs_header() -> None:
    """Start the one-line-per-run table if it is not there yet (the ffmpeg yardstick writes into it too)."""
    if not LOG_MD.exists():
        LOG_MD.parent.mkdir(parents=True, exist_ok=True)
        LOG_MD.write_text("# MSI data hunt - test runs (tools/data_hunt.py and tools/ffmpeg_png_probe.py; newest last)\n\n"
                          "One line per run. Every detail of a hit is in state/msi-data-hunt-log.jsonl.\n\n"
                          "| When | What the machine was doing | Min | Result | Hits | Heat zone C (low/avg/high) | "
                          "Processor busy % (avg) | Graphics card C / busy % (high) | Checked |\n|---|---|---|---|---|---|---|---|---|\n",
                          encoding="utf-8")


def spread(samples: list, key: str):
    vals = [s[key] for s in samples if key in s]
    return None if not vals else {"low": min(vals), "avg": round(sum(vals) / len(vals), 1), "high": max(vals)}


# ---------------------------------------------------------------- parent

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--minutes", type=float, default=10.0)
    ap.add_argument("--label", default="", help="what the machine is doing during this run, in plain words")
    ap.add_argument("--mem-gb", type=float, default=4.0, help="memory held and re-checked (two holders share it)")
    ap.add_argument("--held-gb", type=float, default=2.0, help="files kept in the Windows file cache")
    ap.add_argument("--fresh-mb-s", type=float, default=8.0, help="how fast new files are written")
    ap.add_argument("--burst-s", type=float, default=0.5, help="length of each one-core burst")
    ap.add_argument("--skip", default="", help="comma list of watchers to leave out: hold,cache,fresh,percore,ffmpeg")
    ap.add_argument("--dir", default=str(Path(tempfile.gettempdir()) / "hb-data-hunt"))
    ap.add_argument("--inject", action="store_true", help="plant one fake error per watcher (not logged)")
    ap.add_argument("--no-log", action="store_true")
    args = ap.parse_args()
    if np is None:
        print("numpy is not installed; this test needs it.")
        return 2
    skip = {s.strip() for s in args.skip.split(",") if s.strip()}
    free = it.avail_mem_gb()
    mem_gb = max(0.0, min(args.mem_gb, free - 6.0))            # always leave 6 GB for everything else
    held_gb = max(0.0, min(args.held_gb, free - mem_gb - 5.0))
    run_dir = Path(args.dir) / f"run-{datetime.now():%Y%m%d-%H%M%S}-{os.getpid()}"
    run_dir.mkdir(parents=True, exist_ok=True)
    evidence = run_dir / "evidence" if args.inject else ROOT / "state" / "msi-data-hunt-evidence"   # planted errors are not evidence
    ffmpeg = None if "ffmpeg" in skip else shutil.which("ffmpeg")
    refs = it.compute_refs()
    refs_again = it.compute_refs()
    started, deadline = datetime.now(), time.time() + args.minutes * 60
    cfg = {"deadline": deadline, "inject": args.inject, "dir": str(run_dir), "evidence": str(evidence),
           "mem_gb_each": mem_gb / 2, "hold_pause": 1.5, "held_gb": held_gb, "held_file_mb": 64, "cache_pause": 2.0,
           "fresh_mb_s": args.fresh_mb_s, "ffmpeg": ffmpeg, "burst_s": args.burst_s, "burst_rest_s": 0.12}
    ctx = mp.get_context("spawn")
    q, stop = ctx.Queue(), ctx.Event()
    procs = {}
    if "hold" not in skip and mem_gb >= 0.5:
        for w in range(2):
            procs[f"hold-{w}"] = ctx.Process(target=hold_worker, args=(w, cfg, q, stop), daemon=True)
    if "cache" not in skip and held_gb >= 0.25:
        procs["cache"] = ctx.Process(target=cache_worker, args=(cfg, q, stop), daemon=True)
    if "fresh" not in skip:
        procs["fresh"] = ctx.Process(target=fresh_worker, args=(cfg, q, stop))      # not daemon: it has a child
    if "percore" not in skip:
        procs["percore"] = ctx.Process(target=percore_worker, args=(cfg, refs, q, stop), daemon=True)
    print(f"data_hunt: {args.minutes} min, label '{args.label}', watchers: {', '.join(procs) or 'none'}; "
          f"memory held {mem_gb:.1f} GB, files held {held_gb:.1f} GB, new files {args.fresh_mb_s} MB/s, "
          f"ffmpeg {'yes' if ffmpeg else 'no'}{', INJECT mode' if args.inject else ''}", flush=True)

    hits, notes, done, progress, samples = [], [], {}, {}, []
    for k in refs:
        if refs[k] != refs_again[k]:
            hits.append({"watcher": "start", "what": f"the known answer for {k} came out different twice", "bytes_wrong": -1})
    sensors = Sensors()
    next_sample, next_print = 0.0, time.time() + 30
    try:
        for p in procs.values():
            p.start()
        while any(p.is_alive() for p in procs.values()) or not q.empty():
            try:
                msg = q.get(timeout=1.0)
            except queue.Empty:
                msg = None
            now = time.time()
            if now >= next_sample:
                samples.append(sensors.read())
                next_sample = now + 5
            if msg:
                t = msg.pop("type")
                if t == "hit":
                    msg["at"] = datetime.now().isoformat(timespec="seconds")
                    msg["machine_then"] = samples[-1] if samples else {}
                    hits.append(msg)
                    brief = {k: v for k, v in msg.items() if k in ("file", "core", "test", "bytes_wrong", "became_zero",
                             "position_in_8", "gaps_between", "still_wrong_on_second_look", "drive_copy_wrong",
                             "ffmpeg_said", "failed_again_out_of_5")}
                    print(f"  HIT [{msg['at'][11:]}] {msg['watcher']}: {msg['what']}  {json.dumps(brief)[:400]}", flush=True)
                elif t == "note":
                    notes.append(msg["msg"])
                    print(f"  note: {msg['msg']}", flush=True)
                elif t == "progress":
                    progress[(msg["watcher"], msg.get("worker"))] = msg
                elif t == "done":
                    done[(msg["watcher"], msg.get("worker"))] = msg
            if it.avail_mem_gb() < 2.0 and not stop.is_set():
                notes.append("stopped early: free memory fell under 2 GB")
                stop.set()
            if now >= next_print and now < deadline:
                s = samples[-1] if samples else {}
                print(f"  ... {(deadline - now) / 60:.1f} min left, {len(hits)} hits, heat zone {s.get('zone')} C, "
                      f"processor {s.get('busy')}% busy, graphics card {s.get('gpu_c')} C {s.get('gpu_busy')}%", flush=True)
                next_print = now + 30
            if now > deadline + 240:
                stop.set()
            if now > deadline + 360:
                break
    except KeyboardInterrupt:
        stop.set()
        notes.append("stopped by hand")
    finally:
        for name, p in procs.items():
            p.join(timeout=20)
            if p.is_alive():
                p.terminate()
                notes.append(f"{name} did not stop by itself")
        shutil.rmtree(run_dir, ignore_errors=True)
        try:
            Path(args.dir).rmdir()
        except OSError:
            pass
    for name, p in procs.items():
        if p.exitcode not in (0, None):
            code = p.exitcode & 0xFFFFFFFF
            hits.append({"watcher": name, "what": f"the watcher itself died (exit {hex(code)})", "bytes_wrong": -1,
                         "at": datetime.now().isoformat(timespec="seconds")})

    finals = {k: v for k, v in {**progress, **done}.items()}
    def total(watcher: str, key: str):
        return sum((v.get(key) or 0) for (w, _), v in finals.items() if w == watcher)
    never = [n for n in ("hold", "cache", "fresh", "percore")
             if any(k.startswith(n) for k in procs) and not any(w == n for (w, _) in done)]
    result = "HITS" if hits else ("INCOMPLETE" if never or any("stopped early" in n for n in notes) else "CLEAN")
    ended = datetime.now()
    run = {"started": started.isoformat(timespec="seconds"), "ended": ended.isoformat(timespec="seconds"),
           "minutes": round((ended - started).total_seconds() / 60, 1), "label": args.label, "result": result,
           "inject": args.inject, "hits": hits, "notes": notes,
           "checked": {"memory_gb_held": round(mem_gb, 1), "memory_gb_reads": round(total("hold", "gb_checked"), 1),
                       "cache_gb_held": round(held_gb, 1), "cache_gb_reads": round(total("cache", "gb_checked"), 1),
                       "fresh_files": total("fresh", "files"), "fresh_gb": round(total("fresh", "gb_written"), 2),
                       "pngs_decoded_by_ffmpeg": total("fresh", "pngs_decoded"), "later_looks": total("fresh", "later_looks"),
                       "core_answers": total("percore", "answers"), "core_rounds": total("percore", "rounds")},
           "per_core": next((v.get("per_core") for (w, _), v in done.items() if w == "percore"), None),
           "machine": {"heat_zone_c": spread(samples, "zone"), "processor_busy_pct": spread(samples, "busy"),
                       "processor_speed_pct": spread(samples, "speed"), "graphics_card_c": spread(samples, "gpu_c"),
                       "graphics_card_busy_pct": spread(samples, "gpu_busy"), "graphics_card_watts": spread(samples, "gpu_w")},
           "samples": samples[:: max(1, len(samples) // 120)], "watchers_that_never_finished": never}
    c, m = run["checked"], run["machine"]
    print(f"\nRESULT: {result} - {len(hits)} hits")
    print(f"  memory: {c['memory_gb_reads']} GB of reads over {c['memory_gb_held']} GB held | file cache: {c['cache_gb_reads']} GB "
          f"of reads over {c['cache_gb_held']} GB held | new files: {c['fresh_files']} ({c['fresh_gb']} GB), "
          f"{c['pngs_decoded_by_ffmpeg']} PNGs through ffmpeg | one-core answers: {c['core_answers']}")
    print(f"  machine: heat zone {m['heat_zone_c']} C, processor busy {m['processor_busy_pct']} %, "
          f"graphics card {m['graphics_card_c']} C / {m['graphics_card_busy_pct']} %")
    if not (args.no_log or args.inject):
        LOG_JSONL.parent.mkdir(parents=True, exist_ok=True)
        with open(LOG_JSONL, "a", encoding="utf-8") as f:
            f.write(json.dumps(run) + "\n")
        runs_header()
        z, b, g, gb = m["heat_zone_c"] or {}, m["processor_busy_pct"] or {}, m["graphics_card_c"] or {}, m["graphics_card_busy_pct"] or {}
        with open(LOG_MD, "a", encoding="utf-8") as f:
            f.write(f"| {started:%m/%d %H:%M} | {args.label or '-'} | {run['minutes']} | **{result}** | {len(hits)} | "
                    f"{z.get('low')}/{z.get('avg')}/{z.get('high')} | {b.get('avg')} | {g.get('high')} / {gb.get('high')} | "
                    f"memory {c['memory_gb_reads']} GB, file cache {c['cache_gb_reads']} GB, {c['fresh_files']} new files, "
                    f"{c['pngs_decoded_by_ffmpeg']} PNGs, {c['core_answers']} core answers |\n")
        print(f"  logged to {LOG_MD.relative_to(ROOT)} and {LOG_JSONL.relative_to(ROOT)}")
    return 1 if hits else (2 if result == "INCOMPLETE" else 0)


if __name__ == "__main__":
    sys.exit(main())
