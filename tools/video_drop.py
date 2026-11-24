"""Video drop, MSI side (Jaron 10/25: record test videos on the phone and get them to the MSI "kind of like key drop").
heartbeatobservatory.com/admin/video-drop/ uploads to the private Supabase bucket video-drops (admins only) and logs a row in
video_drops. This script (task "HB Video Drop", every 5 min): 1. fetches waiting rows (service role), 2. downloads each file to
C:/Users/lilli/media/video-drops/<date>/, 3. deletes the cloud copy, 4. marks the row done/failed, 5. buzzes Jaron.
First use: the walking-video test for the fourth piece (AI-Shared/projects/strategy/FOURTH-PIECE.md)."""
import os, json, datetime, re, subprocess, urllib.request, urllib.parse

HOME = os.path.expanduser("~"); SEC = os.path.join(HOME, ".secrets")
ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
LOG = os.path.join(ROOT, "state", "video-drop.log")
OUT = os.path.join(HOME, "media", "video-drops")


def env():
    e = {}
    for l in open(os.path.join(SEC, "keys.env"), encoding="utf-8"):
        if "=" in l and not l.startswith("#"): k, v = l.strip().split("=", 1); e[k] = v.strip()
    return e


E = env(); BASE = E["SUPABASE_URL"].rstrip("/"); SR = E["SUPABASE_SERVICE_ROLE_KEY"]
H = {"apikey": SR, "Authorization": "Bearer " + SR}


def log(m):
    open(LOG, "a", encoding="utf-8").write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M ") + m + "\n")


def buzz(m):
    try: urllib.request.urlopen(urllib.request.Request("https://ntfy.sh/" + E["NTFY_TOPIC"], m.encode(), {"Title": "Video drop"}), timeout=15)
    except Exception: pass


def call(method, url, body=None, raw=False):
    hd = dict(H, **({"Content-Type": "application/json"} if body is not None else {}))
    r = urllib.request.urlopen(urllib.request.Request(url, json.dumps(body).encode() if body is not None else None, hd, method=method), timeout=600)
    return r if raw else json.loads(r.read() or "null")


def mark(rid, status, note):
    call("PATCH", BASE + "/rest/v1/video_drops?id=eq." + str(rid),
         {"status": status, "msi_note": note, "done_at": datetime.datetime.now(datetime.timezone.utc).isoformat()})


VISION = os.path.join(HOME, "Projects", "hb-vision")


def track(video):
    """Every dropped video goes through the skeleton tracker (hb-vision run.py) in the background; buzz when it's done."""
    py = os.path.join(VISION, ".venv", "Scripts", "python.exe")
    if not os.path.exists(py): return
    stem = os.path.splitext(os.path.basename(video))[0]
    cmd = ('"%s" "%s" "%s" && "%s" -c "import urllib.request;urllib.request.urlopen(urllib.request.Request(\'https://ntfy.sh/%s\','
           'b\'Skeleton video ready: %s\',{\'Title\':\'Video drop\'}),timeout=15)"') % (py, os.path.join(VISION, "run.py"), video, py, E["NTFY_TOPIC"], stem)
    subprocess.Popen(cmd, shell=True, cwd=VISION, creationflags=0x08000000,
                     stdout=open(os.path.join(ROOT, "state", "video-track.log"), "a"), stderr=subprocess.STDOUT)
    log("tracking started for " + stem)


def main():
    rows = call("GET", BASE + "/rest/v1/video_drops?status=eq.waiting&order=created_at&select=id,path,file_name,note")
    got = []
    for r in rows or []:
        try:
            day, name = r["path"].split("/", 1)
            safe = re.sub(r"[^A-Za-z0-9._-]+", "_", r.get("file_name") or name)
            folder = os.path.join(OUT, day); os.makedirs(folder, exist_ok=True)
            dest = os.path.join(folder, name.split(".")[0] + "-" + safe)
            src = call("GET", BASE + "/storage/v1/object/video-drops/" + urllib.parse.quote(r["path"]), raw=True)
            with open(dest, "wb") as f:
                while True:
                    b = src.read(1 << 20)
                    if not b: break
                    f.write(b)
            if r.get("note"): open(dest + ".note.txt", "w", encoding="utf-8").write(r["note"] + "\n")
            call("DELETE", BASE + "/storage/v1/object/video-drops/" + urllib.parse.quote(r["path"]), raw=True)
            size = os.path.getsize(dest)
            mark(r["id"], "done", "Saved on the MSI (%.0f MB); cloud copy deleted." % (size / 1048576))
            log("done %s -> %s (%d bytes) note=%s" % (r["path"], dest, size, r.get("note")))
            got.append(r.get("note") or r.get("file_name") or "video")
            if dest.lower().endswith((".mov", ".mp4", ".m4v", ".webm")): track(dest)
        except Exception as ex:
            mark(r["id"], "failed", "MSI couldn't pull it: " + str(ex)[:200])
            log("failed %s: %s" % (r.get("path"), ex))
            buzz("Video drop failed: " + (r.get("file_name") or "file") + ". Check /admin/video-drop/.")
    if got:
        buzz("%d video%s on the MSI: %s" % (len(got), "" if len(got) == 1 else "s", "; ".join(got)[:200]))


if __name__ == "__main__":
    main()
