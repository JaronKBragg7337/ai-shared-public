# frames (Blender every 2nd frame + Pillow diagram/end card at 24 fps) + Kokoro narration + music bed -> captioned H.264 mp4 (16:9),
# a 9:16 vertical cut (letterboxed over a blurred copy, captions under the picture) and a poster jpg.
#   python finish.py [FRAMES_DIR] [POSTER_FRAME] [--redo]
# Blender segments are 12 fps on disk (odd frames); they are motion-interpolated to 24 fps here (slow pans, static plants:
# minterpolate is clean on them). Titles, captions, the on-screen source lines and ESTIMATE tags are an .ass burned by libass.
import json, os, subprocess, sys, re, numpy as np, wave
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from shots import SHOTS, FPS
FR = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else "C:/Users/lilli/Renders/highway-ep4/frames"
PF = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith("--") else "3701"
NAME = "science-ep4-highway-disappears"
DUR = sum(sh["dur"] for sh in SHOTS)
W0 = os.path.join(HERE, "work"); os.makedirs(W0, exist_ok=True)
narr = {s["id"]: s["text"] for s in json.load(open(os.path.join(HERE, "script.json"), encoding="utf8"))}
# (start s, id)
CUES = [(1.5, "n01"), (23.0, "n02"), (43.0, "n03"), (62.5, "n04"), (89.5, "n05"), (113.5, "n06"), (140.5, "n07"), (168.5, "n08"), (191.0, "n09"), (218.5, "n10"), (246.5, "n11")]
# on-screen stage label + source line: (start, end, label, source)
STAGE = [
 (0, 21, "YEAR 0", "A simulation. Central Indiana interstate, 3+3 lanes. Timings are estimates from the sources shown on screen."),
 (21, 42, "FIRST SUMMER", "Mowing stops; roadside grass reaches 0.5-1 m by late summer (FHWA / INDOT roadside vegetation guidance)."),
 (42, 62, "FIRST FALL", "Leaf litter and blocked inlets: FHWA drainage maintenance guidance; leaf fall in Indiana is Oct-Nov."),
 (62, 79, "FIRST WINTER", "Freeze-thaw: Gerber, Wilen, Dufresne & Style 2023 (PRL 131, 208201); 25-40 freeze-thaw swings a winter at Indianapolis = ROUGH ESTIMATE."),
 (113, 139, "YEARS 2-5", "Asphalt design life ~20 yr with maintenance (Asphalt Institute; FHWA). Mosses/lichens on old asphalt: Lutz 2022 (abandoned Hwy 16, BC). Pothole timing = ESTIMATE."),
 (139, 168, "YEARS 5-20", "Pripyat: Lacan, McBride & De Witt 2015 (Urban For. Urban Green. 14) - up to 8,980 Norway maple seedlings/ha. Indiana old fields: Purdue / Ind. Acad. Sci."),
 (168, 187, "YEARS 5-20", "Marking life 0.5-3 yr for paint (FHWA SA-14-017). Fire response: USFS FEIS (sumac resprouts) / Silvics (young cottonwood fire-susceptible). Fire = ESTIMATE."),
 (187, 215, "YEARS 20-50", "Rust takes 2-6x the volume of the steel it replaces (Zhao et al. 2011, Corrosion Science; FHWA RD-98-088). AASHTO LRFD: 75-yr design life with inspection."),
 (215, 242, "YEARS 20-50+", "Heyne 2000 (abandoned paved roads, Puerto Rico: forest-like soil ~11 yr, forest structure ~30 yr); Pripyat empty since 1986. Indiana timing = ESTIMATE."),
]

def dur(path): return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path]).decode().strip())
def chunks(text, limit=80):
    parts = re.split(r"(?<=[,;.?!])\s+", text); out, cur = [], ""
    for p in parts:
        if cur and len(cur) + 1 + len(p) > limit: out.append(cur); cur = p
        else: cur = (cur + " " + p).strip()
    if cur: out.append(cur)
    return out
def ts(s): return "%d:%02d:%05.2f" % (int(s // 3600), int(s % 3600 // 60), s % 60)
def esc(s): return s.replace("{", "(").replace("}", ")")

def ass(vertical=False):
    W, H = (720, 1280) if vertical else (1280, 720)
    cs = 30 if vertical else 26
    cap_margin = 290 if vertical else 46
    stage_mv = 120 if vertical else 30
    src_mv = 154 if vertical else 62
    ml = 24 if vertical else 36
    head = "\n".join([
        "[Script Info]", "ScriptType: v4.00+", "PlayResX: %d" % W, "PlayResY: %d" % H, "WrapStyle: 0", "ScaledBorderAndShadow: yes", "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
        "Style: Narr,Segoe UI,%d,&H00F4EEE2,&H00FFFFFF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,1.6,1,2,60,60,%d,1" % (cs, cap_margin),
        "Style: Title,Georgia,%d,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,2,2,5,40,40,0,1" % int(cs * 2.6),
        "Style: Sub,Georgia,%d,&H00F4EEE2,&H00FFFFFF,&H00000000,&H80000000,0,1,0,0,100,100,0,0,1,1.5,1.5,5,40,40,0,1" % int(cs * 1.15),
        "Style: Kicker,Segoe UI,%d,&H0034B1F2,&H00FFFFFF,&H00000000,&H80000000,1,0,0,0,100,100,2,0,1,1.4,1,5,40,40,0,1" % int(cs * .9),
        "Style: Stage,Segoe UI,%d,&H0034B1F2,&H00FFFFFF,&H00000000,&H80000000,1,0,0,0,100,100,1.5,0,1,1.5,1,7,%d,40,%d,1" % (int(cs * .95), ml, stage_mv),
        "Style: Src,Segoe UI,%d,&H00E6E0D6,&H00FFFFFF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,1.2,1,7,%d,40,%d,1" % (int(cs * .62), ml, src_mv),
        "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Text", ""])
    ev = []
    cy = H * .42 if vertical else H * .30
    nl = "\\N" if vertical else " "
    if vertical:   # 9:16: the title takes two lines, so the kicker sits higher and the subtitle well below it
        ev.append("Dialogue: 1,%s,%s,Kicker,,0,0,0,{\\an5\\pos(%g,%g)\\fad(1200,1200)}HEARTBEAT TV  ·  SCIENCE  ·  8.4" % (ts(1.0), ts(9.5), W / 2, cy - cs * 5.2))
        ev.append("Dialogue: 1,%s,%s,Title,,0,0,0,{\\an5\\pos(%g,%g)\\fad(1200,1200)}How a highway\\Ndisappears" % (ts(1.5), ts(9.5), W / 2, cy - cs * 1.2))
        ev.append("Dialogue: 1,%s,%s,Sub,,0,0,0,{\\an5\\pos(%g,%g)\\fs%d\\fad(1200,1200)}Season by season, year by year,\\Nif everyone stopped driving it and fixing it.\\NA simulation; timings are estimates." % (ts(2.5), ts(9.5), W / 2, cy + cs * 4.0, int(cs * 1.0)))
    else:
        ev.append("Dialogue: 1,%s,%s,Kicker,,0,0,0,{\\an5\\pos(%g,%g)\\fad(1200,1200)}HEARTBEAT TV  ·  SCIENCE  ·  8.4" % (ts(1.0), ts(9.5), W / 2, cy - cs * 3.4))
        ev.append("Dialogue: 1,%s,%s,Title,,0,0,0,{\\an5\\pos(%g,%g)\\fad(1200,1200)}How a highway disappears" % (ts(1.5), ts(9.5), W / 2, cy - cs * .6))
        ev.append("Dialogue: 1,%s,%s,Sub,,0,0,0,{\\an5\\pos(%g,%g)\\fad(1200,1200)}Season by season, year by year, if everyone stopped%sdriving it and fixing it. A simulation; timings are estimates." % (ts(2.5), ts(9.5), W / 2, cy + cs * 1.9, nl))
    for s0, s1, lab, src in STAGE:
        ev.append("Dialogue: 1,%s,%s,Stage,,0,0,0,{\\fad(400,400)}%s" % (ts(s0 + .3), ts(s1 - .3), esc(lab)))
        ev.append("Dialogue: 1,%s,%s,Src,,0,0,0,{\\fad(400,400)}%s" % (ts(s0 + .6), ts(s1 - .3), esc(src)))
    for start, sid in CUES:
        d = dur(os.path.join(HERE, "audio", "t_%s.wav" % sid)); text = narr[sid]
        pieces = chunks(text); total = sum(len(p) for p in pieces); t0 = start
        for p in pieces:
            d_ = d * len(p) / total
            ev.append("Dialogue: 0,%s,%s,Narr,,0,0,0,%s" % (ts(t0), ts(min(t0 + d_ + .2, DUR)), esc(p)))
            t0 += d_
    return head + "\n".join(ev) + "\n"

def run(cmd): print(" ".join(cmd)[:220], flush=True); subprocess.check_call(cmd)

# ---- trim the Kokoro clips (lead/tail silence) like tv-lib/prep.py
for _, sid in CUES:
    out = os.path.join(HERE, "audio", "t_%s.wav" % sid)
    if not os.path.exists(out):
        run(["ffmpeg", "-y", "-v", "error", "-i", os.path.join(HERE, "audio", sid + ".wav"), "-af",
             "silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.05,areverse,silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.1,areverse", "-ar", "24000", "-ac", "1", out])
# ---- if a re-voiced clip is longer than its cue window, slow the video under it (tv-lib/retime.py; no re-render)
sys.path.insert(0, "C:/Users/lilli/AI-Shared/projects/tv-lib"); import retime
RT = retime.plan(CUES, DUR, {sid: dur(os.path.join(HERE, "audio", "t_%s.wav" % sid)) for _, sid in CUES})
CUES = RT.cues; STAGE = [(RT.m(a), RT.m(b), l, s_) for a, b, l, s_ in STAGE]; DUR = RT.dur
print("retimed length %.1fs; cues" % DUR, [(round(c, 1), i) for c, i in CUES])
open(os.path.join(HERE, "caps.ass"), "w", encoding="utf8").write(ass(False))
open(os.path.join(HERE, "caps_v.ass"), "w", encoding="utf8").write(ass(True))
if "--caps-only" in sys.argv: sys.exit(0)

# ---- music bed: slow pad (same chords as tv-lib, lower and sparser), CC0, generated here
bed = os.path.join(W0, "bed.wav")
if not os.path.exists(bed):
    sr = 44100; n = int(DUR * sr); x = np.arange(n) / sr
    chords = [[220.0, 261.63, 329.63], [174.61, 220.0, 261.63], [130.81, 164.81, 196.0, 261.63], [196.0, 246.94, 293.66]]
    L = np.zeros(n); R = np.zeros(n); bar = 10.0
    for i in range(int(DUR / bar) + 2):
        t0 = i * bar; a = int(t0 * sr); b = min(n, int((t0 + bar + 2.0) * sr))
        if a >= n: break
        tt = np.arange(b - a) / sr; env = np.minimum(1, tt / 2.5) * np.minimum(1, (bar + 2.0 - tt) / 2.0)
        for k, f in enumerate(chords[i % 4]):
            for det, pan in ((0.997, 0.35), (1.003, 0.65)):
                w = np.sin(2 * np.pi * f * det * tt + k) * env * 0.05 * (1 + 0.3 * np.sin(2 * np.pi * 0.09 * tt + k))
                L[a:b] += w * (1 - pan); R[a:b] += w * pan
            bass = np.sin(2 * np.pi * (f / 2) * tt) * env * 0.03; L[a:b] += bass; R[a:b] += bass
    fade = np.minimum(1, x / 2.0) * np.minimum(1, (DUR - x) / 3.0)
    st = np.stack([L * fade, R * fade], 1); st = st / np.abs(st).max() * 0.9
    with wave.open(bed, "wb") as w_:
        w_.setnchannels(2); w_.setsampwidth(2); w_.setframerate(sr); w_.writeframes((st * 32767).astype("<i2").tobytes())

# ---- audio mix: bed low + narration at its cues, one loudness pass
ins = ["-i", bed]; fl = []; names = []
for i, (start, sid) in enumerate(CUES):
    ins += ["-i", os.path.join(HERE, "audio", "t_%s.wav" % sid)]; ms = int(start * 1000)
    fl.append("[%d:a]aformat=sample_rates=48000:channel_layouts=stereo,adelay=%d|%d,volume=1.0[v%d]" % (i + 1, ms, ms, i)); names.append("[v%d]" % i)
fl.append("[0:a]volume=0.16[bed]")
fl.append("[bed]%samix=inputs=%d:normalize=0:duration=first,loudnorm=I=-16:TP=-1.5:LRA=11,afade=t=out:st=%g:d=2.5[a]" % ("".join(names), len(names) + 1, DUR - 2.5))
mix = os.path.join(W0, "mix.wav")
run(["ffmpeg", "-y", "-loglevel", "error"] + ins + ["-filter_complex", ";".join(fl), "-map", "[a]", "-ar", "48000", mix])

# ---- video: segments in shot order. Blender runs = odd frames at 12 fps -> minterpolate 24; Pillow runs = 24 fps as is.
segs = []; f = 1; cur = None
for sh in SHOTS:
    n = int(round(sh["dur"] * FPS)); kind = "pil" if sh["cam"] is None else "bl"
    if cur and cur[0] == kind: cur[2] = f + n - 1
    else:
        cur = [kind, f, f + n - 1]; segs.append(cur)
    f += n
parts = []
for i, (kind, fa, fb) in enumerate(segs):
    out = os.path.join(W0, "seg%02d.mp4" % i); parts.append(out)
    if os.path.exists(out) and "--redo" not in sys.argv: continue
    if kind == "bl":
        lst = os.path.join(W0, "seg%02d.txt" % i)
        with open(lst, "w") as fh:
            for fr in range(fa if fa % 2 == 1 else fa + 1, fb + 1, 2):
                fh.write("file '%s'\nduration %f\n" % (os.path.join(FR, "f_%04d.png" % fr).replace("\\", "/"), 2.0 / FPS))
        run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-vf",
             "minterpolate=fps=%d:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1,tpad=stop_mode=clone:stop_duration=0.5,format=yuv420p" % FPS, "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-frames:v", str(fb - fa + 1), out])
    else:
        run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-start_number", str(fa), "-i", os.path.join(FR, "f_%04d.png"), "-frames:v", str(fb - fa + 1),
             "-vf", "format=yuv420p", "-c:v", "libx264", "-preset", "medium", "-crf", "16", out])
cat = os.path.join(W0, "cat.txt")
with open(cat, "w") as fh:
    for p in parts: fh.write("file '%s'\n" % p.replace("\\", "/"))
full = os.path.join(W0, "full.mp4")
run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", cat, "-c", "copy", full])
full = retime.apply(full, RT, W0)
print("full", dur(full))

caps = os.path.join(HERE, "caps.ass").replace("\\", "/").replace(":", "\\:")
caps_v = os.path.join(HERE, "caps_v.ass").replace("\\", "/").replace(":", "\\:")
out = os.path.join(HERE, NAME + ".mp4")
if "--vertical-only" not in sys.argv: run(["ffmpeg", "-y", "-loglevel", "error", "-i", full, "-i", mix, "-filter_complex", "[0]fade=t=in:st=0:d=1.2,fade=t=out:st=%g:d=1.5,subtitles='%s',format=yuv420p[v]" % (DUR - 1.5, caps),
     "-map", "[v]", "-map", "1:a", "-c:v", "libx264", "-preset", "slow", "-crf", "23", "-profile:v", "high", "-movflags", "+faststart", "-c:a", "aac", "-b:a", "160k", "-shortest", out])
outv = os.path.join(HERE, NAME + "-vertical.mp4")
run(["ffmpeg", "-y", "-loglevel", "error", "-i", full, "-i", mix, "-filter_complex",
     "[0]fade=t=in:st=0:d=1.2,fade=t=out:st=%g:d=1.5,split[a][b];[a]scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,gblur=sigma=28,eq=brightness=-0.12[bg];[b]scale=720:-2[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2-40,subtitles='%s',format=yuv420p[v]" % (DUR - 1.5, caps_v),
     "-map", "[v]", "-map", "1:a", "-c:v", "libx264", "-preset", "slow", "-crf", "22", "-profile:v", "high", "-movflags", "+faststart", "-c:a", "aac", "-b:a", "160k", "-shortest", outv])
if "--vertical-only" not in sys.argv: run(["ffmpeg", "-y", "-loglevel", "error", "-i", os.path.join(FR, "f_%04d.png" % int(PF)), "-vf", "scale=1280:-1", "-q:v", "3", os.path.join(HERE, NAME + ".jpg")])
for p in (out, outv, os.path.join(HERE, NAME + ".jpg")): print(p, round(os.path.getsize(p) / 1e6, 2), "MB")
