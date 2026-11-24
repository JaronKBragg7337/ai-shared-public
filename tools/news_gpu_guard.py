"""News GPU guard (Jaron 11/1: "as long as Kimi doesn't mess up the news").
The news render owns the MSI GPU from 2:40 to 7:30 AM. The pipeline already stops the Sapling heartbeat itself (gpu_yield),
but a side job (a Kimi training run on a copied checkpoint, any other python on the GPU) would not be stopped.
Runs as Windows task "HB News GPU Guard" at 2:38 AM daily: ends every python process on the GPU EXCEPT the heartbeat,
killed by PID only, logged to state/news-gpu-guard.log, and a mailbox note to its owner (kimi) so it knows why.
  python tools/news_gpu_guard.py          # do it
  python tools/news_gpu_guard.py --dry    # only list what it would stop
"""
import os, subprocess, sys
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(ROOT, "state", "news-gpu-guard.log")
KEEP = ("sapling.heartbeat",)   # the pipeline stops the heartbeat gracefully itself


def cmdline(pid):
    r = subprocess.run(["powershell", "-NoProfile", "-Command",
                        f"(Get-CimInstance Win32_Process -Filter 'ProcessId={pid}').CommandLine"],
                       capture_output=True, text=True)
    return (r.stdout or "").strip()


def main(dry):
    out = subprocess.run(["nvidia-smi", "--query-compute-apps=pid,process_name", "--format=csv,noheader"],
                         capture_output=True, text=True).stdout
    stopped = []
    for line in out.splitlines():
        try:
            pid, name = [x.strip() for x in line.split(",", 1)]
        except ValueError:
            continue
        if "python" not in name.lower():
            continue
        cl = cmdline(pid)
        if any(k in cl for k in KEEP):
            continue
        if not dry:
            subprocess.run(["taskkill", "/PID", pid, "/T", "/F"], capture_output=True)
        stopped.append(f"{pid} {cl[:200]}")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(f"{now} {'DRY ' if dry else ''}stopped {len(stopped)}: {' | '.join(stopped) or '-'}\n")
    print(f"{'would stop' if dry else 'stopped'} {len(stopped)}")
    for s in stopped:
        print(" ", s)
    if stopped and not dry:
        subprocess.run([sys.executable, os.path.join(ROOT, "tools", "mailbox.py"), "send", "--from", "news-gpu-guard",
                        "--to", "kimi", "--subject", "GPU job stopped for the news render",
                        "--body", "2:38 AM guard: the news render owns the GPU 2:40-7:30 AM, so these were stopped (by PID): "
                        + " | ".join(stopped) + ". Resume after 7:30 AM from your last checkpoint."],
                       capture_output=True)


if __name__ == "__main__":
    main("--dry" in sys.argv)
