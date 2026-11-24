"""Cut a <=2:30 YouTube Short from a finished vertical Heartbeat TV episode.
Keeps whole narration scenes (cut at the scene boundaries the episode's own build uses), drops the rest, then adds a
closing card: "Full episode free at heartbeatobservatory.com" (plain URL), voiced with the show's own voice.
No wording is changed - scenes are kept or dropped whole.   usage: python make_short.py <key> [--list]
"""
import json, os, re, subprocess, sys
from plans import PLANS
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.dirname(os.path.dirname(HERE))          # .../projects
FONT = r"C\:/Windows/Fonts/segoeui.ttf"; FONTB = r"C\:/Windows/Fonts/segoeuib.ttf"

def run(cmd, **k):
    r = subprocess.run(cmd, capture_output=True, text=True, **k)
    if r.returncode: raise SystemExit("FAILED: " + " ".join(cmd)[:300] + "\n" + r.stderr[-1500:])
    return r.stdout

def dur(f): return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]).strip())

def load_timeline(plan):
    d = os.path.join(P, plan["dir"])
    if plan.get("plan_cmd"):                                   # blender episodes: read the cue times out of finish.py (no rendering)
        lines = open(os.path.join(d, "finish.py"), encoding="utf8").read().split(chr(10))
        stop = next((i for i, l in enumerate(lines) if l.startswith('print("retimed length')), None)
        if stop is None: stop = next(i for i, l in enumerate(lines) if l.startswith("CUES = [(shot_start"))
        ns = {"__file__": os.path.join(d, "finish.py"), "__name__": "plan"}; old = (sys.argv, os.getcwd())
        sys.argv = ["finish.py"]; os.chdir(d)
        import io, contextlib
        with contextlib.redirect_stdout(io.StringIO()): exec(compile(chr(10).join(lines[:stop + 1]), "finish.py", "exec"), ns)
        sys.argv = old[0]; os.chdir(old[1])
        texts = {x["id"]: x["text"] for x in json.load(open(os.path.join(d, "script.json"), encoding="utf8"))}
        segs = [dict(id=sid, start=c, dur=dur(os.path.join(d, "audio", "t_%s.wav" % sid)), text=texts[sid]) for c, sid in ns["CUES"]]
        return segs, None
    t = json.load(open(os.path.join(d, "timeline.json"), encoding="utf8"))
    return t["segs"], t.get("total")

def scenes(plan):
    segs, total = load_timeline(plan)
    off = plan.get("off", 0.5)
    src = os.path.join(P, plan["dir"], plan["src"]); T = dur(src)
    res = []
    for i, s in enumerate(segs):
        a = 0.0 if i == 0 else max(0, s["start"] - off)
        b = (segs[i + 1]["start"] - off) if i + 1 < len(segs) else T
        res.append(dict(id=s["id"], cue=s["start"], a=a, b=min(b, T), text=s.get("text", ""), dur=s["dur"]))
    return res, src, T

def main():
    key = sys.argv[1]; plan = PLANS[key]
    sc, src, T = scenes(plan)
    if "--list" in sys.argv:
        for s in sc: print(s["id"], "%.1f-%.1f (%.1fs)" % (s["a"], s["b"], s["b"] - s["a"]), s["text"][:plan.get("w", 150)])
        return
    keep = plan["keep"]; by = {s["id"]: s for s in sc}
    ranges = []                                              # merge neighbours
    for k in keep:
        s = dict(by[k])
        if k in plan.get("trim", {}):                        # end the scene after N sentences of its narration (pause detect on the clean voice clip)
            wav = os.path.join(P, plan["dir"], "audio", "t_%s.wav" % k)
            if not os.path.exists(wav): wav = os.path.join(P, plan["dir"], "audio", "%s.wav" % k)
            o = subprocess.run(["ffmpeg", "-v", "info", "-i", wav, "-af", "silencedetect=noise=-35dB:d=0.45", "-f", "null", "-"], capture_output=True, text=True).stderr
            st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", o)]
            en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", o)]
            lead = 0.0
            if st and st[0] < 0.05: lead = en[0]; st = st[1:]
            s["b"] = s["cue"] + st[plan["trim"][k] - 1] - lead + 0.45; print("trim", k, "after sentence", plan["trim"][k], "at %.1f" % s["b"])
        if ranges and abs(ranges[-1][1] - s["a"]) < 0.01: ranges[-1][1] = s["b"]
        else: ranges.append([s["a"], s["b"]])
    body = sum(b - a for a, b in ranges)
    probe = run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=width,height", "-of", "csv=p=0", src]).strip().split(",")
    W, H = int(probe[0]), int(probe[1])
    work = os.path.join(HERE, "work"); os.makedirs(work, exist_ok=True)
    body_f = os.path.join(work, key + "-body.mp4"); end_f = os.path.join(work, key + "-end.mp4")
    fc = []; n = len(ranges); FD = 0.12
    for i, (a, b) in enumerate(ranges):
        v = "[0:v]trim=%.3f:%.3f,setpts=PTS-STARTPTS" % (a, b)
        for (x, y, w, h) in plan.get("delogo", []): v += ",delogo=x=%d:y=%d:w=%d:h=%d" % (x, y, w, h)
        if i > 0: v += ",fade=t=in:st=0:d=%.2f" % FD
        v += ",fade=t=out:st=%.3f:d=%.2f" % (b - a - FD, FD)
        fc.append(v + "[v%d]" % i)
        au = "[0:a]atrim=%.3f:%.3f,asetpts=PTS-STARTPTS" % (a, b)
        if i > 0: au += ",afade=t=in:st=0:d=0.15"
        au += ",afade=t=out:st=%.3f:d=%.2f" % (b - a - 0.4, 0.4)
        fc.append(au + "[a%d]" % i)
    fc.append("".join("[v%d][a%d]" % (i, i) for i in range(n)) + "concat=n=%d:v=1:a=1[v][a]" % n)
    run(["ffmpeg", "-y", "-v", "error", "-i", src, "-filter_complex", ";".join(fc), "-map", "[v]", "-map", "[a]", "-r", "30",
         "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-pix_fmt", "yuv420p", "-profile:v", "high",
         "-c:a", "aac", "-b:a", "160k", "-ar", "44100", "-ac", "2", body_f])
    # closing card: show background colour, plain URL, voiced line
    px = os.path.join(work, key + "-px.png")
    run(["ffmpeg", "-y", "-v", "error", "-ss", "30", "-i", src, "-frames:v", "1", "-vf", "crop=8:8:%d:%d,scale=1:1" % (W - 12, int(H * .55)), px])
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", px, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    r, g, b = raw[0], raw[1], raw[2]; lum = .299 * r + .587 * g + .114 * b
    bg = "0x%02x%02x%02x" % (r, g, b); fg = "0x1a1a1a" if lum > 140 else "0xf2efe8"; ac = "0x9a6a1f" if lum > 140 else "0xe8b04a"
    wav = os.path.join(HERE, "audio", "end_%s.wav" % plan.get("voice", "bm_george")); vd = dur(wav); a family friend = vd + 1.6
    sz = W / 1080.0
    def dt(txt, y, size, col, font): return ("drawtext=fontfile='%s':text='%s':fontcolor=%s:fontsize=%d:x=(w-text_w)/2:y=%d" % (font, txt, col, int(size * sz), int(H * y)))
    vf = ",".join([dt("Heartbeat TV", .30, 46, ac, FONT), dt(plan["series"], .35, 60, fg, FONTB),
                   dt("Full episode free at", .47, 52, fg, FONT), dt("heartbeatobservatory.com", .52, 66, ac, FONTB),
                   dt("Made with AI by Heartbeat Observatory", .90, 34, fg, FONT)])
    run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", "color=c=%s:s=%dx%d:r=30:d=%.2f" % (bg, W, H, a family friend), "-i", wav,
         "-vf", vf + ",fade=t=in:st=0:d=0.3", "-af", "adelay=500|500,apad,aresample=44100", "-t", "%.2f" % a family friend, "-ac", "2",
         "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-pix_fmt", "yuv420p", "-profile:v", "high", "-c:a", "aac", "-b:a", "160k", "-ar", "44100", end_f])
    out = os.path.join(P, plan["dir"], plan["out"])
    lst = os.path.join(work, key + "-list.txt"); open(lst, "w").write("file '%s'\nfile '%s'\n" % (body_f.replace("\\", "/"), end_f.replace("\\", "/")))
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", "-movflags", "+faststart", out])
    print(key, "->", out, "%.1f s (body %.1f + card %.1f)" % (dur(out), body, a family friend), "scenes kept:", ",".join(keep))

main()
