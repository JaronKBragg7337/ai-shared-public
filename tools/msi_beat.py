"""msi_beat.py - the MSI checks in with its off-machine alarm (hb-msi-watch on Cloudflare) every 5 minutes. Built 11/22.

Why: on 11/22 a Windows update restarted the MSI and it sat at the sign-in screen for 3 hours. Every checker we had runs ON the
MSI, so nothing noticed. This check-in only happens while the MSI is on and signed in; if it stops for 20 minutes the Worker
buzzes Jaron's phone once, and once more when it's back. Task "MSI Beat" (every 5 min + at logon). Reads one key name from
keys.env internally (HB_MSI_BEAT_TOKEN) and never prints it.

  pythonw msi_beat.py          check in (the task)
  python  msi_beat.py status   print what the alarm sees (last check-in, minutes quiet, alarm out?)
"""
import json, os, sys, urllib.request
from datetime import datetime, timezone

URL = "https://hb-msi-watch.acsassociation7337.workers.dev"
LOG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "state", "msi-beat.log")


def token():
    for line in open(os.path.expanduser("~/.secrets/keys.env"), encoding="utf-8"):
        if line.startswith("HB_MSI_BEAT_TOKEN="):
            return line.split("=", 1)[1].strip().strip('"')
    return ""


def boot_time():
    try:
        import ctypes
        up_ms = ctypes.windll.kernel32.GetTickCount64()
        return datetime.fromtimestamp(datetime.now().timestamp() - up_ms / 1000, timezone.utc).isoformat(timespec="seconds")
    except Exception:
        return None


def call(path, body=None):
    req = urllib.request.Request(URL + path, method="POST" if body is not None else "GET",
                                 data=json.dumps(body).encode() if body is not None else None,
                                 headers={"Authorization": "Bearer " + token(), "Content-Type": "application/json",
                                          "User-Agent": "hb-msi-beat"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode("utf-8"))


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "status":
        print(json.dumps(call("/status"), indent=1))
        return
    try:
        call("/beat", {"boot": boot_time()})
    except Exception as e:  # a missed beat is fine; 4 in a row is what the alarm is for
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(datetime.now().strftime("%Y-%m-%d %H:%M ") + "beat failed: " + str(e)[:200] + "\n")


if __name__ == "__main__":
    main()
