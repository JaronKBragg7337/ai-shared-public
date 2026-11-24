"""game_reel.py - record a game's director mode as a vertical highlight reel (1080x1920, H.264, 30 fps).

Reusable for any game that has a director mode: the page sets window.__reel = {marks: [{name, t}], done, error?}
(t = Date.now() at each scene start) and flips done=true at the end.

    python tools/game_reel.py                      # The Hedge (defaults)
    python tools/game_reel.py --game games/hedge-maze --name hedge-reel --method cdp

What it does:
1. Serves the site repo locally (http://127.0.0.1:<port>/).
2. Opens a HEADED Chromium (real GPU; headless rendered dark/slow on the MSI) at a phone viewport
   (432x768 CSS, deviceScaleFactor 2.5 -> 1080x1920, touch on) and loads <game>/?director=1.
3. Records it: --method pw = Playwright record_video; --method cdp (default) = our own CDP screencast at JPEG q90,
   every frame with its real timestamp (sharper than Playwright's VP8 video).
4. ffmpeg: trims to the first..last scene mark, scales to 1080x1920, 30 fps CFR, fades in/out, adds a generated
   ambience + heartbeat bed (browser audio can't be captured this way), H.264 CRF 18, faststart.
5. Writes <out>/<name>.mp4 + <name>-1..3.jpg stills and a <name>.json with the scene timeline; checks for black frames.

GPU time rule (AGENTS.md): the MSI GPU belongs to the news from 2:45 AM. This script refuses to start a recording
between 2:40 AM and 7:30 AM local unless --force-time is passed.
"""
import argparse, base64, datetime as dt, functools, http.server, json, os, shutil, socketserver, subprocess, sys, threading, time
from pathlib import Path

SITE = Path(r"C:\Users\lilli\Projects\heartbeat-observatory")
OUT = Path(r"C:\Users\lilli\AI-Shared\state\moments\media")


def ffbin(name):
    p = shutil.which(name)
    if p:
        return p
    for c in Path(os.path.expanduser(r"~\AppData\Local\Microsoft\WinGet\Packages")).glob(f"Gyan.FFmpeg*/**/bin/{name}.exe"):
        return str(c)
    sys.exit(f"{name} not found")


FFMPEG, FFPROBE = ffbin("ffmpeg"), ffbin("ffprobe")


def serve(root, port):
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(root))
    handler.log_message = lambda *a, **k: None
    socketserver.TCPServer.allow_reuse_address = True
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", port), handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv


def time_ok(force):
    now = dt.datetime.now().time()
    blocked = dt.time(2, 40) <= now < dt.time(7, 30)
    if blocked and not force:
        sys.exit(f"{now:%H:%M} is inside the GPU news window (2:40-7:30 AM). Run after 7:30 AM (or --force-time).")


def record(args, workdir):
    from playwright.sync_api import sync_playwright
    url = f"http://127.0.0.1:{args.port}/{args.game.strip('/')}/?director=1"
    frames_dir = workdir / "frames"; frames_dir.mkdir(parents=True, exist_ok=True)
    frames = []  # (timestamp_seconds_epoch, path)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, args=[
            "--ignore-gpu-blocklist", "--enable-gpu-rasterization", "--use-angle=d3d11",
            "--autoplay-policy=no-user-gesture-required", "--disable-background-timer-throttling",
            "--disable-renderer-backgrounding", "--disable-backgrounding-occluded-windows", "--window-position=0,0"])
        ctx_kw = dict(viewport={"width": args.w, "height": args.h}, device_scale_factor=args.dpr, has_touch=True, is_mobile=True,
                      user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1")
        if args.method == "pw":
            ctx_kw.update(record_video_dir=str(workdir / "pw"), record_video_size={"width": round(args.w * args.dpr), "height": round(args.h * args.dpr)})
        ctx = browser.new_context(**ctx_kw)
        page = ctx.new_page()
        t_video0 = time.time()
        page.on("console", lambda m: m.type in ("error", "warning") and print("  [page]", m.type, m.text[:200]))
        cdp = None
        if args.method == "cdp":
            cdp = ctx.new_cdp_session(page)
            def on_frame(ev):
                n = len(frames)
                fp = frames_dir / f"f{n:05d}.jpg"
                fp.write_bytes(base64.b64decode(ev["data"]))
                frames.append((ev["metadata"].get("timestamp", time.time()), fp))
                try:
                    cdp.send("Page.screencastFrameAck", {"sessionId": ev["sessionId"]})
                except Exception:
                    pass
            cdp.on("Page.screencastFrame", on_frame)
        page.goto(url, wait_until="domcontentloaded")
        if cdp:
            cdp.send("Page.startScreencast", {"format": "jpeg", "quality": 90, "maxWidth": round(args.w * args.dpr), "maxHeight": round(args.h * args.dpr), "everyNthFrame": 1})
        page.wait_for_function("window.__reel && window.__reel.done", timeout=args.timeout * 1000, polling=500)
        reel = page.evaluate("window.__reel")
        fps = page.evaluate("window.hedge && window.hedge.game ? window.hedge.game.fps : null")
        if cdp:
            try: cdp.send("Page.stopScreencast")
            except Exception: pass
            time.sleep(0.3)
        video = page.video
        ctx.close(); browser.close()
        vpath = Path(video.path()) if (video and args.method == "pw") else None
    return reel, frames, vpath, t_video0, fps


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        print(r.stderr[-2500:]); sys.exit("ffmpeg failed")
    return r


def audio_bed(path, secs):
    # low wind/rumble + a slow double-thump heartbeat (~62 bpm), generated so the reel isn't silent
    beat = "0.9*sin(2*PI*52*t)*exp(-22*mod(t,0.97))+0.6*sin(2*PI*46*t)*exp(-26*mod(t-0.28,0.97))*gt(mod(t,0.97),0.28)"
    run([FFMPEG, "-y", "-f", "lavfi", "-i", f"anoisesrc=color=brown:amplitude=0.22:duration={secs}:sample_rate=48000",
         "-f", "lavfi", "-i", f"aevalsrc='{beat}':d={secs}:s=48000",
         "-filter_complex", "[0]lowpass=f=420,volume=0.55,tremolo=f=0.13:d=0.5[w];[1]lowpass=f=160,volume=0.9[b];[w][b]amix=inputs=2:normalize=0,"
         f"afade=t=in:d=1,afade=t=out:st={max(0, secs - 1.5)}:d=1.5,alimiter=limit=0.8[a]", "-map", "[a]", "-ac", "2", "-c:a", "aac", "-b:a", "160k", str(path)])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="games/hedge-maze")
    ap.add_argument("--name", default="hedge-reel")
    ap.add_argument("--out", default=str(OUT))
    ap.add_argument("--site", default=str(SITE))
    ap.add_argument("--method", choices=["cdp", "pw"], default="cdp")
    ap.add_argument("--port", type=int, default=8791)
    ap.add_argument("--w", type=int, default=432); ap.add_argument("--h", type=int, default=768); ap.add_argument("--dpr", type=float, default=2.5)
    ap.add_argument("--timeout", type=int, default=150)
    ap.add_argument("--stills", default="", help="comma list of scene-mark names to grab stills from (default: picks 3)")
    ap.add_argument("--force-time", action="store_true")
    args = ap.parse_args()
    time_ok(args.force_time)
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True)
    work = Path(os.environ.get("TEMP", ".")) / f"game_reel_{args.name}"
    shutil.rmtree(work, ignore_errors=True); work.mkdir(parents=True)
    srv = serve(args.site, args.port)
    print(f"[{dt.datetime.now():%H:%M:%S}] recording {args.game} ({args.method}) ...")
    reel, frames, vpath, t0, fps = record(args, work)
    srv.shutdown()
    print(f"[{dt.datetime.now():%H:%M:%S}] recorded. page fps~{fps}  marks={len(reel['marks'])}  error={reel.get('error')}")
    marks = reel["marks"]
    if not marks:
        sys.exit("no scene marks from the page")
    start_epoch = marks[0]["t"] / 1000 - 0.15
    end_epoch = marks[-1]["t"] / 1000 + 0.2
    raw = work / "raw.mp4"
    if args.method == "cdp":
        fr = [(ts, p) for ts, p in frames if start_epoch - 0.5 <= ts <= end_epoch + 0.5]
        if len(fr) < 30:
            sys.exit(f"only {len(fr)} screencast frames in range - capture failed")
        lst = work / "frames.txt"
        with lst.open("w") as f:
            for i, (ts, p) in enumerate(fr):
                nxt = fr[i + 1][0] if i + 1 < len(fr) else ts + 1 / 30
                f.write(f"file '{p.as_posix()}'\nduration {max(0.001, nxt - ts):.4f}\n")
            f.write(f"file '{fr[-1][1].as_posix()}'\n")
        offset = start_epoch - fr[0][0]
        span = fr[-1][0] - fr[0][0]
        print(f"  {len(fr)} frames over {span:.1f}s = {len(fr) / max(span, 0.1):.1f} captured fps")
        run([FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-vf", "fps=30", "-c:v", "libx264", "-crf", "12", "-preset", "fast", "-pix_fmt", "yuv420p", str(raw)])
        ss = max(0.0, offset)
    else:
        if not vpath or not vpath.exists() or vpath.stat().st_size < 10000:
            sys.exit(f"Playwright video missing/empty: {vpath}")
        run([FFMPEG, "-y", "-i", str(vpath), "-vf", "fps=30", "-c:v", "libx264", "-crf", "12", "-preset", "fast", "-pix_fmt", "yuv420p", str(raw)])
        ss = max(0.0, start_epoch - t0)
    dur = end_epoch - start_epoch
    bed = work / "bed.m4a"; audio_bed(bed, dur + 1)
    final = out / f"{args.name}.mp4"
    vf = f"scale=1080:1920:flags=lanczos,setsar=1,fps=30,fade=t=in:d=0.35,fade=t=out:st={max(0, dur - 0.6):.2f}:d=0.6"
    run([FFMPEG, "-y", "-ss", f"{ss:.3f}", "-t", f"{dur:.3f}", "-i", str(raw), "-i", str(bed), "-map", "0:v", "-map", "1:a",
         "-vf", vf, "-c:v", "libx264", "-profile:v", "high", "-crf", "18", "-preset", "slow", "-pix_fmt", "yuv420p", "-r", "30",
         "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", str(final)])
    # timeline relative to the final video
    tl = [{"name": m["name"], "at": round(m["t"] / 1000 - start_epoch, 2)} for m in marks]
    (out / f"{args.name}.json").write_text(json.dumps({"video": str(final), "made": dt.datetime.now().isoformat(timespec="seconds"), "method": args.method, "page_fps": fps, "scenes": tl}, indent=1))
    # stills
    names = [s for s in args.stills.split(",") if s] or None
    picks = []
    if names:
        for n in names:
            m = next((x for x in tl if x["name"] == n), None)
            if m: picks.append(m["at"] + 1.6)
    else:
        def at(prefix, add):
            m = next((x for x in tl if x["name"].startswith(prefix)), None)
            return m["at"] + add if m else None
        picks = [x for x in (at("spotted", 2.6), at("trap:darios", 1.9), at("shadow", 2.6)) if x is not None]
        if len(picks) < 3: picks += [dur * f for f in (0.25, 0.5, 0.75)][: 3 - len(picks)]
    for i, t in enumerate(picks[:3], 1):
        run([FFMPEG, "-y", "-ss", f"{t:.2f}", "-i", str(final), "-frames:v", "1", "-q:v", "2", str(out / f"{args.name}-{i}.jpg")])
    # check
    pr = json.loads(run([FFPROBE, "-v", "error", "-show_entries", "format=duration,size:stream=width,height,r_frame_rate,codec_name", "-of", "json", str(final)]).stdout)
    bl = run([FFMPEG, "-i", str(final), "-vf", "blackdetect=d=1.2:pix_th=0.06", "-an", "-f", "null", "-"]).stderr
    blacks = [l for l in bl.splitlines() if "black_start" in l]
    print(json.dumps(pr["format"]), [ (s.get("codec_name"), s.get("width"), s.get("height"), s.get("r_frame_rate")) for s in pr["streams"]])
    print("black stretches >1.2s:", blacks or "none")
    print("scenes:", ", ".join(f"{x['name']}@{x['at']}" for x in tl))
    print("wrote", final)


if __name__ == "__main__":
    main()
