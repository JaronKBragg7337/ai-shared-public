# Heartbeat News (rendered show) - put a finished episode video in Supabase Storage (bucket news-video, public read).
#   python publish_video.py 2026-09-27 EPISODE.mp4 [POSTER.jpg] [plan.json] [VERTICAL_DIR]  -> news-video/2026-09-27.mp4 (+ .jpg, + .timing.json) and index.json
#   VERTICAL_DIR (from make_vertical.py) adds 2026-09-27-vertical.mp4 (whole show, 9:16) and 2026-09-27-short.mp4 (headlines, for social).
# The timing file lets the news page run its live graphics (rundown, subtitles, lower thirds) in step with the video.
# Uses the MSI's service key from the same secrets file the other tools read (names only; values never printed). Keeps 14 days.
import os, sys, json, urllib.request, urllib.error
sys.path.insert(0, "C:/Users/lilli/AI-Shared/tools")
import settings as S
env = S._env(); URL, KEY = env["SUPABASE_URL"].rstrip("/"), env["SUPABASE_SERVICE_ROLE_KEY"]
B = "news-video"; H = {"apikey": KEY, "Authorization": "Bearer " + KEY}
def put(name, data, ctype):
    r = urllib.request.Request(f"{URL}/storage/v1/object/{B}/{name}", data=data, method="POST", headers={**H, "Content-Type": ctype, "x-upsert": "true", "Cache-Control": "3600"})
    # big uploads sometimes drop mid-way (9/27, 10/20, 10/21: SSL EOF on the 120-135 MB show). 10/21: 4 quick tries all failed at
    # 5:47 AM and the show only went live when Claude re-ran it at 6:04. Now 8 tries, waits growing to ~2 min.
    import time
    for k in range(8):
        try: urllib.request.urlopen(r, timeout=900).read(); break
        except Exception as e:
            if k == 7: raise
            print("upload retry", name, e); time.sleep(min(15 * (k + 1), 120))
    print("uploaded", name, len(data))
def get_index():
    try: return json.loads(urllib.request.urlopen(f"{URL}/storage/v1/object/public/{B}/index.json?t={os.getpid()}").read())
    except Exception: return {"episodes": []}
def delete(names):
    # 10/18: this crashed the publish step on 5 of 7 days (after the upload, before index.json), so the day's video never
    # became "latest" and the run stopped before deleting its 50-60 GB of frames. Old-file cleanup must never block publishing.
    if not names: return
    try:
        r = urllib.request.Request(f"{URL}/storage/v1/object/{B}", data=json.dumps({"prefixes": names}).encode(), method="DELETE", headers={**H, "Content-Type": "application/json"})
        urllib.request.urlopen(r, timeout=60).read(); print("removed", names)
    except Exception as e:
        print("old-file cleanup skipped:", e)
date, mp4 = sys.argv[1], sys.argv[2]; poster = sys.argv[3] if len(sys.argv) > 3 else None; planf = sys.argv[4] if len(sys.argv) > 4 else None
vdir = sys.argv[5] if len(sys.argv) > 5 else None
def same_size(name, path):   # 10/20: the extras pass re-uploaded the 122 MB show and kept dropping (SSL EOF); skip what's already there
    try:
        r = urllib.request.urlopen(urllib.request.Request(f"{URL}/storage/v1/object/public/{B}/{name}", method="HEAD"), timeout=30)
        return int(r.headers.get("Content-Length", -1)) == os.path.getsize(path)
    except Exception: return False
if same_size(f"{date}.mp4", mp4): print("already uploaded", f"{date}.mp4")
else: put(f"{date}.mp4", open(mp4, "rb").read(), "video/mp4")
if poster: put(f"{date}.jpg", open(poster, "rb").read(), "image/jpeg")
timing = None
if planf:
    pl = json.load(open(planf)); fps = pl["fps"]; ids = {g["seg"]: g["id"] for g in pl["segments"]}
    tj = {"fps": fps, "lines": [{"seg": ids.get(l["seg"]), "li": l["line"], "who": l["who"], "camera": l["camera"],
                                 "start": round(l["start"] / fps, 3), "dur": round(l["frames"] / fps, 3)} for l in pl["lines"]]}
    # the running order the video was made from (stories + commercials + wires), so the page shows the same rundown, the
    # same commercial banners and the same words in the subtitles as the video
    sc = os.path.join(os.path.dirname(planf), "script.json")
    if os.path.exists(sc): tj["segments"] = json.load(open(sc, encoding="utf-8"))["segments"]
    put(f"{date}.timing.json", json.dumps(tj, ensure_ascii=False).encode("utf-8"), "application/json"); timing = f"{URL}/storage/v1/object/public/{B}/{date}.timing.json"
extra = {}
if vdir:
    for kind in ("vertical", "short"):
        f = os.path.join(vdir, kind + ".mp4")
        if os.path.exists(f):
            put(f"{date}-{kind}.mp4", open(f, "rb").read(), "video/mp4"); extra[kind] = f"{URL}/storage/v1/object/public/{B}/{date}-{kind}.mp4"
idx = get_index(); eps = [e for e in idx.get("episodes", []) if e.get("date") != date]
eps.insert(0, {"date": date, "video": f"{URL}/storage/v1/object/public/{B}/{date}.mp4", "poster": f"{URL}/storage/v1/object/public/{B}/{date}.jpg" if poster else None, "bytes": os.path.getsize(mp4), "timing": timing, **extra})
eps.sort(key=lambda e: e["date"], reverse=True); old = eps[14:]; eps = eps[:14]
delete([f"{e['date']}{x}" for e in old for x in (".mp4", ".jpg", "-vertical.mp4", "-short.mp4")])
put("index.json", json.dumps({"latest": eps[0]["date"], "episodes": eps}, indent=1).encode(), "application/json")
print("latest", eps[0]["video"])
