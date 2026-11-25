"""ffmpeg_png_probe.py - the yardstick for the MSI's wrong-answer fault (Fable, Tue 11/24/2026).

What it does: makes one PNG picture the size of a video frame (every byte known, checked with Python's own
decoder first), then asks the REAL ffmpeg to decode that same good file again and again and counts how often
ffmpeg says it is broken ("inflate returned error -3") or crashes. On a healthy machine the count is zero,
always: same program, same file, same answer. On the MSI on 11/24 it failed about 1 time in 4.

It can hold ffmpeg on one processor core at a time, so the count per core shows WHERE the wrong answers
come from. That makes this the test to run before and after any fix (new BIOS, turbo off, cooler machine):
a fix is real when this reads zero.

A clean result only counts if the test really ran flat out, because the fault only shows at top speed. So with
--per-core the yardstick also reads how fast each fast core really ran while it was being tested (Windows' own
counters) and compares that with the top speed the settings allow (the cap, tools/msi_speed_cap.py). A run
that was held back says NOT A FAIR TEST instead of CLEAN.

Two things keep a run started by the Task Scheduler as fast as a run by hand (learned 11/24, state/msi-data-hunt.md):
  - ffmpeg is started with no console at all. Started from a windowless program (pythonw, the Task Scheduler)
    each launch otherwise gets a brand-new console. On 11/24 every one of those became a Windows Terminal tab:
    1,008 tabs, a 30-minute run, and the terminal program crashed closing them.
  - the yardstick tells Windows not to slow it down to save power, and tells it the same for every ffmpeg before
    that ffmpeg runs its first instruction. Windows slows a windowless program the scheduler started, and the
    programs it starts, to about 1.2 GHz otherwise (measured), far below the speed where the fault shows.

Usage:
  python tools/ffmpeg_png_probe.py                    # 60 tries each: as-is, one thread, fast cores, small cores
  python tools/ffmpeg_png_probe.py --per-core 24      # the daily check: also 24 tries on each core, one at a time
  python tools/ffmpeg_png_probe.py --tries 200 --only default
  python tools/ffmpeg_png_probe.py --per-core 6 --eco --no-log   # test of the test: slowed on purpose, must say NOT A FAIR TEST
Exit code: 0 = clean (and, with --per-core, a fair test), 1 = at least one try failed, 2 = no failure seen but
not a fair test, or the test could not start.
Log: state/msi-data-hunt-log.jsonl (kind "ffmpeg-probe") and a line in state/msi-data-hunt-runs.md.
"""
from __future__ import annotations

import argparse
import ctypes
import json
import os
import shutil
import struct
import subprocess
import sys
import tempfile
import threading
import time
import zlib
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import data_hunt as dh  # noqa: E402
import msi_speed_cap  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
FAIR_SHARE = 0.92        # with a cap set, a fair test gets each fast core to at least this share of the cap
FAST_ABOVE_MHZ = 5100    # with no cap set, the fault shows above about this speed; a fair test has to get there
# How ffmpeg is started: with no console at all (0x8) and paused (0x4) until it has been told "full speed".
# Measured 11/24 on a healthy fast core, started by the Task Scheduler, cap 4.6 GHz, seconds per launch / speed:
#   plain launch 0.24 s / 2.0-3.0 GHz; "no window" 0.42 s / 1.0 GHz; "no window" + told full speed 0.15 s / 4.05 GHz
#   (the hidden console helper Windows starts beside each ffmpeg is slowed too); this way 0.115 s / 4.47 GHz,
#   the same as a run by hand (0.117 s / 4.46 GHz).
LAUNCH = 0x8 | 0x4

k32 = ctypes.WinDLL("kernel32", use_last_error=True)
k32.GetCurrentProcess.restype = ctypes.c_void_p
k32.SetProcessAffinityMask.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
k32.GetProcessAffinityMask.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_size_t), ctypes.POINTER(ctypes.c_size_t)]
k32.SetProcessInformation.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p, ctypes.c_ulong]
k32.OpenProcess.restype = ctypes.c_void_p
k32.OpenProcess.argtypes = [ctypes.c_ulong, ctypes.c_int, ctypes.c_ulong]
k32.CloseHandle.argtypes = [ctypes.c_void_p]
k32.GetPriorityClass.restype = ctypes.c_ulong
k32.GetPriorityClass.argtypes = [ctypes.c_void_p]
k32.SetPriorityClass.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
ntdll = ctypes.WinDLL("ntdll")
ntdll.NtResumeProcess.argtypes = [ctypes.c_void_p]


class _Throttle(ctypes.Structure):          # Windows' PROCESS_POWER_THROTTLING_STATE
    _fields_ = [("Version", ctypes.c_ulong), ("ControlMask", ctypes.c_ulong), ("StateMask", ctypes.c_ulong)]


class _Power(ctypes.Structure):             # Windows' SYSTEM_POWER_STATUS
    _fields_ = [("ACLineStatus", ctypes.c_ubyte), ("BatteryFlag", ctypes.c_ubyte), ("BatteryLifePercent", ctypes.c_ubyte),
                ("SystemStatusFlag", ctypes.c_ubyte), ("BatteryLifeTime", ctypes.c_ulong), ("BatteryFullLifeTime", ctypes.c_ulong)]


def hold_on(mask: int) -> bool:
    """Keep this program, and every program it starts, on the cores in the mask."""
    return bool(k32.SetProcessAffinityMask(k32.GetCurrentProcess(), mask))


def speed_mode(handle, eco: bool = False) -> bool:
    """Tell Windows a program must not be slowed down to save power. eco=True asks for the opposite; that is
    only for testing that the yardstick notices a run that was held back."""
    state = _Throttle(1, 1, 1 if eco else 0)       # version 1; 1 = "running speed" is decided here; slowed or not
    return bool(k32.SetProcessInformation(handle, 4, ctypes.byref(state), ctypes.sizeof(state)))    # 4 = power throttling


def flat_out(eco: bool = False) -> None:
    """This program itself: no power saving, and ordinary priority if the scheduler started it lower."""
    me = k32.GetCurrentProcess()
    speed_mode(me, eco)
    if not eco and k32.GetPriorityClass(me) in (0x40, 0x4000):        # idle or below normal
        k32.SetPriorityClass(me, 0x20)                                 # normal


def cap_now() -> int:
    """The top speed in MHz the settings allow the fast cores right now; 0 = no cap (or it could not be read)."""
    v = msi_speed_cap.read()
    if not v:
        return 0
    power = _Power()
    on_battery = bool(k32.GetSystemPowerStatus(ctypes.byref(power))) and power.ACLineStatus == 0
    return v[1] if on_battery else v[0]


class SpeedWatch:
    """How fast one core really ran while it was at work. Windows' own counters; no admin rights needed."""
    WHAT = ("% Processor Performance", "Processor Frequency", "% Processor Utility")

    def __init__(self, cores: int) -> None:
        self.h, self.samples, self.on, self.thread, self.query = {}, [], False, None, ctypes.c_void_p()
        try:
            self.pdh = ctypes.WinDLL("pdh")
            self.pdh.PdhOpenQueryW.argtypes = [ctypes.c_wchar_p, ctypes.c_size_t, ctypes.POINTER(ctypes.c_void_p)]
            self.pdh.PdhAddEnglishCounterW.argtypes = [ctypes.c_void_p, ctypes.c_wchar_p, ctypes.c_size_t,
                                                       ctypes.POINTER(ctypes.c_void_p)]
            self.pdh.PdhCollectQueryData.argtypes = [ctypes.c_void_p]
            self.pdh.PdhGetFormattedCounterValue.argtypes = [ctypes.c_void_p, ctypes.c_ulong, ctypes.c_void_p,
                                                             ctypes.POINTER(dh._PdhValue)]
            if self.pdh.PdhOpenQueryW(None, 0, ctypes.byref(self.query)) == 0:
                for c in range(cores):
                    for what in self.WHAT:
                        h = ctypes.c_void_p()
                        if self.pdh.PdhAddEnglishCounterW(self.query, rf"\Processor Information(0,{c})\{what}", 0,
                                                          ctypes.byref(h)) == 0:
                            self.h[(c, what)] = h
                self.pdh.PdhCollectQueryData(self.query)
        except (OSError, AttributeError):
            self.h = {}

    def _value(self, key):
        v = dh._PdhValue()
        ok = key in self.h and self.pdh.PdhGetFormattedCounterValue(self.h[key], 0x200, None, ctypes.byref(v)) == 0
        return v.doubleValue if ok else None

    def _loop(self, core: int) -> None:
        while self.on:
            time.sleep(0.25)
            self.pdh.PdhCollectQueryData(self.query)
            share, base, busy = (self._value((core, what)) for what in self.WHAT)
            if share and base and busy and busy > 40:            # only while that core is really at work
                self.samples.append(share * base / 100.0)        # share of the nameplate speed x nameplate MHz

    def start(self, core: int) -> None:
        self.samples, self.on = [], bool(self.h)
        if self.on:
            self.thread = threading.Thread(target=self._loop, args=(core,), daemon=True)
            self.thread.start()

    def stop(self) -> dict:
        if self.on:
            self.on = False
            self.thread.join(timeout=2)
        s, self.samples = sorted(self.samples), []
        return {"mhz": round(s[len(s) // 2]) if s else 0, "top_mhz": round(s[-1]) if s else 0, "readings": len(s)}


def tries(ffmpeg: str, png: Path, n: int, extra: list[str], eco: bool = False) -> dict:
    out = {"tries": 0, "failed": 0, "inflate_error": 0, "crashed": 0, "other": 0, "says": {}}
    for _ in range(n):
        # Started paused, told "full speed", then let go: ffmpeg is never slowed, not even for its first moment.
        p = subprocess.Popen([ffmpeg, "-v", "error", "-nostdin", *extra, "-i", str(png), "-f", "null", "-"],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, errors="replace",
                             creationflags=LAUNCH)
        h = k32.OpenProcess(0x0200 | 0x0800, False, p.pid)     # allowed to change its settings and to let it run
        speed_mode(h or int(p._handle), eco)
        if ntdll.NtResumeProcess(h or int(p._handle)) != 0:    # could not let it run: do not leave it hanging
            p.kill()
        if h:
            k32.CloseHandle(h)
        said = p.communicate()[1].strip()
        out["tries"] += 1
        if p.returncode == 0 and not said:
            continue
        out["failed"] += 1
        code = p.returncode & 0xFFFFFFFF
        if code >= 0xC0000000:
            out["crashed"] += 1
            key = f"crashed {hex(code)}"
        elif "inflate returned error" in said:
            out["inflate_error"] += 1
            key = said.split("inflate returned error")[1].split()[0].join(["inflate returned error ", ""])
        else:
            out["other"] += 1
            key = said.splitlines()[0][-80:] if said else f"exit {code}"
        out["says"][key] = out["says"].get(key, 0) + 1
    return out


def add_up(old: dict | None, new: dict) -> dict:
    """A core tested a second time: the counts add up, the better speed reading stays."""
    if not old:
        return new
    for key in ("tries", "failed", "inflate_error", "crashed", "other", "seconds"):
        new[key] = round(old[key] + new[key], 2)
    for key, n in old["says"].items():
        new["says"][key] = new["says"].get(key, 0) + n
    if old["mhz"] > new["mhz"]:
        new.update(mhz=old["mhz"], top_mhz=old["top_mhz"], readings=old["readings"])
    new["goes"] = old.get("goes", 1) + 1
    return new


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--tries", type=int, default=60)
    ap.add_argument("--per-core", type=int, default=0, help="also this many tries on each core, one core at a time")
    ap.add_argument("--only", default="", help="comma list: default,one-thread,fast-cores,small-cores,plain-math")
    ap.add_argument("--label", default="")
    ap.add_argument("--no-log", action="store_true")
    ap.add_argument("--eco", action="store_true",
                    help="test of the test: ask Windows to slow this run down; the yardstick must then say NOT A FAIR TEST")
    args = ap.parse_args()
    flat_out(args.eco)
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        print("ffmpeg not found")
        return 2
    png_bytes = dh.make_png(20261124)
    i = png_bytes.index(b"IDAT")
    n = struct.unpack(">I", png_bytes[i - 4:i])[0]
    for _ in range(3):                                   # the file is good: Python's own decoder agrees, three times
        if len(zlib.decompress(png_bytes[i + 4:i + 4 + n])) != 1080 * (1920 * 3 + 1):
            print("the test picture did not check out; stopping")
            return 2
    folder = Path(tempfile.mkdtemp(prefix="hb-ffprobe-"))
    png = folder / "frame.png"
    png.write_bytes(png_bytes)
    if png.read_bytes() != png_bytes:
        print("the test picture read back different from what was written; stopping (that itself is a finding)")
        return 2

    cores = os.cpu_count() or 1
    everything = (1 << cores) - 1
    fast = [c for c in range(cores) if cores == 32 and c < 16]      # this machine: logical 0-15 are the fast cores
    mine, system = ctypes.c_size_t(), ctypes.c_size_t()
    k32.GetProcessAffinityMask(k32.GetCurrentProcess(), ctypes.byref(mine), ctypes.byref(system))
    home = mine.value or everything
    sensors = dh.Sensors()
    watch = SpeedWatch(cores) if args.per_core else None
    time.sleep(1.0)
    start = sensors.read()
    cap = cap_now()
    need = round(FAIR_SHARE * cap) if cap else FAST_ABOVE_MHZ
    plans = {"default": (home, []), "one-thread": (home, ["-threads", "1"]),
             "fast-cores": (0xFFFF & everything, []), "small-cores": (0xFFFF0000 & everything, []),
             "plain-math": (home, ["-cpuflags", "0"])}
    only = [s.strip() for s in args.only.split(",") if s.strip()] or ["default", "one-thread", "fast-cores", "small-cores"]
    results, per_core, held_back = {}, {}, []
    began, clock = datetime.now(), time.perf_counter()
    print(f"ffmpeg_png_probe: {ffmpeg}\n  picture {len(png_bytes)} bytes (checked good); heat zone {start.get('zone')} C, "
          f"processor {start.get('busy')}% busy; fast cores' cap: {f'{cap} MHz' if cap else 'none'}"
          f"{'; SLOWED ON PURPOSE (--eco)' if args.eco else ''}", flush=True)

    def one_core(c: int) -> None:
        if not hold_on(1 << c):
            return
        if c in fast:                  # only the fast cores: for the small cores Windows scales this counter differently
            watch.start(c)
        t = time.perf_counter()
        r = tries(ffmpeg, png, args.per_core, [], args.eco)
        r["seconds"] = round(time.perf_counter() - t, 2)
        r.update(watch.stop())
        per_core[c] = r = add_up(per_core.get(c), r)
        ran = f"ran {r['mhz'] / 1000:.2f} GHz, " if c in fast else ""
        print(f"  core {c:2} ({'fast' if c in fast else 'small'})  {r['failed']:3} of {r['tries']} failed  "
              f"{ran}{r['seconds']:.1f} s  {r['says'] or ''}", flush=True)

    def slow_ones() -> list[int]:
        # a core with failures is left out: crash handling muddies its speed reading, and it has failed anyway
        return [c for c in fast if c in per_core and not per_core[c]["failed"]
                and (not per_core[c]["readings"] or per_core[c]["mhz"] < need)]

    try:
        for name in only:
            mask, extra = plans[name]
            if not mask or not hold_on(mask):
                continue
            results[name] = tries(ffmpeg, png, args.tries, extra, args.eco)
            r = results[name]
            print(f"  {name:12} {r['failed']:3} of {r['tries']} failed  {r['says'] or ''}", flush=True)
        if args.per_core:
            for c in range(cores):
                one_core(c)
            again = slow_ones()                    # a core that did not get up to speed gets one more go:
            if again:                              # the machine may just have been busy for a moment
                print(f"  not up to speed (needed {need / 1000:.2f} GHz), once more: cores {' '.join(map(str, again))}", flush=True)
                for c in again:
                    one_core(c)
            held_back = slow_ones()
    finally:
        if watch:
            watch.stop()
        hold_on(home)
        shutil.rmtree(folder, ignore_errors=True)
    end = sensors.read()
    minutes = round((time.perf_counter() - clock) / 60, 1)
    failed = sum(r["failed"] for r in results.values()) + sum(r["failed"] for r in per_core.values())
    total = sum(r["tries"] for r in results.values()) + sum(r["tries"] for r in per_core.values())
    ran = sorted(per_core[c]["mhz"] for c in fast if c in per_core and per_core[c]["readings"] and not per_core[c]["failed"])
    speed = ""
    if args.per_core and fast:
        which = "the fast cores that passed" if failed else "fast cores"
        speed = (f"{which} ran {ran[0] / 1000:.2f} to {ran[-1] / 1000:.2f} GHz" if ran else "no speed reading")
        speed += f", a fair test needs {need / 1000:.2f} ({f'cap {cap / 1000:.1f}' if cap else 'no cap set'})"
        if held_back:
            speed += f"; HELD BACK: cores {' '.join(map(str, held_back))}"
    verdict = "FAILS" if failed else ("NOT A FAIR TEST" if held_back else "CLEAN")
    print(f"TOTAL: {failed} of {total} failed in {minutes} min. Heat zone at the end {end.get('zone')} C. {speed}")
    print(f"RESULT: {verdict}" + (" - the fast cores did not get up to speed, so a clean count proves nothing; "
                                  "find what slowed the run and run it again" if verdict == "NOT A FAIR TEST" else ""))
    if not args.no_log:
        label = (args.label or "-") + (" (slowed on purpose, --eco)" if args.eco else "")
        run = {"kind": "ffmpeg-probe", "started": began.isoformat(timespec="seconds"),
               "ended": datetime.now().isoformat(timespec="seconds"), "label": label, "ffmpeg": ffmpeg,
               "results": results, "per_core": {str(c): r for c, r in per_core.items()},
               "failed": failed, "tries": total, "minutes": minutes, "cap_mhz": cap, "need_mhz": need,
               "held_back": held_back, "verdict": verdict, "machine_start": start, "machine_end": end}
        with open(dh.LOG_JSONL, "a", encoding="utf-8") as f:
            f.write(json.dumps(run) + "\n")
        dh.runs_header()
        ways = ", ".join(f"{k} {v['failed']}/{v['tries']}" for k, v in results.items())
        twice = [str(c) for c, r in per_core.items() if r.get("goes", 1) > 1]
        cores_line = ("; failed per core 0-" + str(len(per_core) - 1) + " (of " + str(args.per_core) + " each): "
                      + " ".join(str(r["failed"]) for r in per_core.values())
                      + (f" (tested twice: {' '.join(twice)})" if twice else "") + "; " + speed) if per_core else ""
        with open(dh.LOG_MD, "a", encoding="utf-8") as f:
            f.write(f"| {began:%m/%d %H:%M} | ffmpeg yardstick: {label} | {minutes} | **{verdict}** | {failed} of {total} | "
                    f"{start.get('zone')}/-/{end.get('zone')} | {start.get('busy')} | - | {ways}{cores_line} |\n")
    return 1 if failed else (2 if held_back else 0)


if __name__ == "__main__":
    sys.exit(main())
