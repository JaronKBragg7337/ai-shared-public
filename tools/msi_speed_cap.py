"""msi_speed_cap.py - the top-speed cap for the MSI's fast processor cores.

Why: on Tue 11/24/2026 one fast core (Windows' logical 10 and 11) was found to give wrong answers when it runs
flat out, above about 5.1 GHz (state/msi-data-hunt.md). Holding the fast cores under that speed is the fix that
needs no admin rights, no restart and no new parts. It is one Windows power setting ("Maximum processor
frequency" for the fast cores) and it is undone in seconds.

  python tools/msi_speed_cap.py status      # what the cap is now
  python tools/msi_speed_cap.py set 4600    # cap the fast cores at 4600 MHz (plugged in and on battery)
  python tools/msi_speed_cap.py off         # no cap: how the MSI was before 11/24/2026

Always check a change with the yardstick:  python tools/ffmpeg_png_probe.py --per-core 24   (0 failures = good)
Exit code of "status": 0 = a cap is set, 1 = no cap, 2 = could not read it.
"""
from __future__ import annotations

import re
import subprocess
import sys

FAST_CORES = "75b0ae3f-bce0-45a7-8c89-c9611c25e101"     # "Maximum processor frequency for Processor Power Efficiency Class 1"
GROUP = "SUB_PROCESSOR"


def run(*args: str) -> subprocess.CompletedProcess:
    # "no window": started from a windowless program, powercfg would otherwise open a new terminal tab each time
    return subprocess.run(["powercfg", *args], capture_output=True, text=True, errors="replace",
                          creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))


def read() -> tuple[int, int] | None:
    out = run("/qh", "SCHEME_CURRENT", GROUP, FAST_CORES).stdout
    ac = re.search(r"Current AC Power Setting Index:\s*0x([0-9a-fA-F]+)", out)
    dc = re.search(r"Current DC Power Setting Index:\s*0x([0-9a-fA-F]+)", out)
    return (int(ac.group(1), 16), int(dc.group(1), 16)) if ac and dc else None


def say(v: tuple[int, int] | None) -> str:
    if v is None:
        return "could not read the setting"
    words = [("no cap" if x == 0 else f"{x} MHz ({x / 1000:.1f} GHz)") for x in v]
    return f"fast cores' top speed: plugged in = {words[0]}, on battery = {words[1]}"


def write(mhz: int) -> bool:
    for flag in ("/setacvalueindex", "/setdcvalueindex"):
        r = run(flag, "SCHEME_CURRENT", GROUP, FAST_CORES, str(mhz))
        if r.returncode:
            print("Windows refused:", (r.stdout + r.stderr).strip()[:200])
            return False
    return run("/setactive", "SCHEME_CURRENT").returncode == 0      # makes the new value take hold now


def main() -> int:
    what = sys.argv[1] if len(sys.argv) > 1 else "status"
    before = read()
    if what == "status":
        print(say(before))
        return 2 if before is None else (0 if before[0] else 1)
    if what == "off":
        mhz = 0
    elif what == "set" and len(sys.argv) > 2 and sys.argv[2].isdigit() and 3000 <= int(sys.argv[2]) <= 6000:
        mhz = int(sys.argv[2])
    else:
        print(__doc__)
        return 2
    print("before:", say(before))
    ok = write(mhz)
    print("after: ", say(read()))
    return 0 if ok and read() == (mhz, mhz) else 2


if __name__ == "__main__":
    sys.exit(main())
