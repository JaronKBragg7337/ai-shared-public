# frames + bed + voices -> captioned, titled H.264 mp4 (16:9) + a 9:16 vertical cut + poster jpg.
#   python finish.py [FRAMES_DIR] [POSTER_FRAME]
# Voices: narration = Kokoro bm_george (audio/n0*.wav, the book's own sentences); dialogue = the locked Chatterbox cast
# (necklace-voices/ep01: Jalen am_michael seed, Mateo am_onyx seed + pitch/EQ "_fx"). Captions and titles are an .ass file
# burned in by libass (Georgia for titles, Segoe UI for captions).
import json, os, subprocess, sys, re
HERE = os.path.dirname(os.path.abspath(__file__))
FR = sys.argv[1] if len(sys.argv) > 1 else "C:/Users/lilli/Renders/necklace-ep1p1/frames"
PF = sys.argv[2] if len(sys.argv) > 2 else "1900"
VO = "C:/Users/lilli/Projects/necklace-voices/ep01/"
DUR = 116.0
NAME = "necklace-ep1-part1"

narr = {s["id"]: s["text"] for s in json.load(open(os.path.join(HERE, "script.json"), encoding="utf8"))}
# (start s, file, who, text)
CUES = [
 (11.5, "audio/n01.wav", None, narr["n01"]), (27.5, "audio/n02.wav", None, narr["n02"]), (37.5, "audio/n03.wav", None, narr["n03"]),
 (46.5, "audio/n04.wav", None, narr["n04"]), (58.4, "audio/n05.wav", None, narr["n05"]), (69.0, "audio/n06.wav", None, narr["n06"]),
 (78.0, "audio/n07.wav", None, narr["n07"]),
 (88.0, VO + "01_mateo_fx.wav", "Mateo", "You look like a man with a story."),
 (90.8, VO + "02_jalen.wav", "Jalen", "Don't we all?"),
 (92.8, VO + "03_mateo_fx.wav", "Mateo", "Some stories are heavier than others, eh?"),
 (95.5, "audio/n09.wav", None, narr["n09"]),
 (104.5, VO + "04_mateo_fx.wav", "Mateo", "The sea... she listens to those heavy stories. Sometimes, she even offers a way to rewrite them."),
]


def dur(path):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path]).decode().strip())


def chunks(text, limit=78):
    """split a long sentence at commas / clause ends into caption-sized pieces"""
    parts = re.split(r"(?<=[,;.?!])\s+", text); out, cur = [], ""
    for p in parts:
        if cur and len(cur) + 1 + len(p) > limit: out.append(cur); cur = p
        else: cur = (cur + " " + p).strip()
    if cur: out.append(cur)
    return out


def ts(s):
    h = int(s // 3600); m = int(s % 3600 // 60); sec = s % 60
    return f"{h}:{m:02d}:{sec:05.2f}"


def esc(s): return s.replace("{", "(").replace("}", ")")


def ass(vertical=False):
    W, H = (720, 1280) if vertical else (1280, 720)
    cap_size = 30 if vertical else 26
    cap_margin = 300 if vertical else 48          # vertical: captions sit under the letterboxed picture
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Narr,Segoe UI,{cap_size},&H00F2EADC,&H00FFFFFF,&H00000000,&H80000000,0,1,0,0,100,100,0,0,1,1.4,1,2,60,60,{cap_margin},1
Style: Line,Segoe UI,{cap_size},&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,1.4,1,2,60,60,{cap_margin},1
Style: Title,Georgia,{int(cap_size * 2.5)},&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,2,2,5,40,40,0,1
Style: Sub,Georgia,{int(cap_size * 1.3)},&H00F2EADC,&H00FFFFFF,&H00000000,&H80000000,0,1,0,0,100,100,0,0,1,1.5,1.5,5,40,40,0,1
Style: Small,Segoe UI Light,{int(cap_size * 0.95)},&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,1,1,5,40,40,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Text
"""
    ev = []
    cy = H * 0.5 if vertical else H * 0.26
    ev.append(f"Dialogue: 0,{ts(2.5)},{ts(9.5)},Title,,0,0,0,{{\\an5\\pos({W/2},{cy - cap_size*1.6})\\fad(1500,1500)}}The Necklace")
    ev.append(f"Dialogue: 0,{ts(3.5)},{ts(9.5)},Sub,,0,0,0,{{\\an5\\pos({W/2},{cy + cap_size*1.3})\\fad(1500,1500)}}Episode 1 · Rum and Regret in Rosetown{'\\N' if vertical else ' · '}Part 1")
    ey = H * 0.5 if vertical else H * 0.36
    ev.append(f"Dialogue: 0,{ts(111.0)},{ts(DUR)},Title,,0,0,0,{{\\an5\\pos({W/2},{ey - cap_size*1.6})\\fad(1500,0)}}The Necklace")
    ev.append(f"Dialogue: 0,{ts(112.0)},{ts(DUR)},Small,,0,0,0,{{\\an5\\pos({W/2},{ey + cap_size*1.1})\\fad(1500,0)}}From the book by Jaron Bragg · Heartbeat Observatory{'\\N' if vertical else '   ·   '}Part 2 follows")
    for start, f, who, text in CUES:
        d = dur(os.path.join(HERE, f) if not os.path.isabs(f) else f)
        pieces = chunks(text) if who is None else [text]
        total = sum(len(p) for p in pieces); t0 = start
        for p in pieces:
            d_ = d * len(p) / total
            txt = esc(p) if who is None else f"{{\\c&HB0C8E6&}}{who}:{{\\c&HFFFFFF&}} {esc(p)}"
            ev.append(f"Dialogue: 0,{ts(t0)},{ts(min(t0 + d_ + 0.25, DUR))},{'Narr' if who is None else 'Line'},,0,0,0,{txt}")
            t0 += d_
    return head + "\n".join(ev) + "\n"


open(os.path.join(HERE, "caps.ass"), "w", encoding="utf8").write(ass(False))
open(os.path.join(HERE, "caps_v.ass"), "w", encoding="utf8").write(ass(True))

# ---- audio: bed + each voice at its cue (narration a touch under the cast), one loudness pass
ins = ["-i", os.path.join(HERE, "bed.wav")]; fl = []; names = []
for i, (start, f, who, _) in enumerate(CUES):
    ins += ["-i", (os.path.join(HERE, f) if not os.path.isabs(f) else f)]
    ms = int(start * 1000); g = 1.0 if who is None else 1.15
    fl.append(f"[{i+1}:a]aformat=sample_rates=48000:channel_layouts=stereo,adelay={ms}|{ms},volume={g}[v{i}]"); names.append(f"[v{i}]")
fl.append(f"[0:a]volume=0.9[bed]")
fl.append(f"[bed]{''.join(names)}amix=inputs={len(names)+1}:normalize=0:duration=first,loudnorm=I=-16:TP=-1.5:LRA=11,afade=t=out:st={DUR-2.5}:d=2.5[a]")
subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error"] + ins + ["-filter_complex", ";".join(fl), "-map", "[a]", "-ar", "48000", os.path.join(HERE, "mix.wav")])
print("mix.wav")

# ---- 16:9: frames + captions, fade in/out
caps = os.path.join(HERE, "caps.ass").replace("\\", "/").replace(":", "\\:")
caps_v = os.path.join(HERE, "caps_v.ass").replace("\\", "/").replace(":", "\\:")
out = os.path.join(HERE, NAME + ".mp4")
subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "24", "-i", os.path.join(FR, "f_%04d.png"), "-i", os.path.join(HERE, "mix.wav"),
    "-filter_complex", f"[0]fade=t=in:st=0:d=1.5,fade=t=out:st={DUR-1.5}:d=1.5,subtitles='{caps}',format=yuv420p[v]",
    "-map", "[v]", "-map", "1:a", "-c:v", "libx264", "-preset", "slow", "-crf", "21", "-profile:v", "high", "-movflags", "+faststart", "-c:a", "aac", "-b:a", "160k", "-shortest", out])
print(out)
# ---- 9:16: the picture letterboxed over a blurred, darkened copy of itself; captions under the picture
outv = os.path.join(HERE, NAME + "-vertical.mp4")
subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "24", "-i", os.path.join(FR, "f_%04d.png"), "-i", os.path.join(HERE, "mix.wav"),
    "-filter_complex", f"[0]fade=t=in:st=0:d=1.5,fade=t=out:st={DUR-1.5}:d=1.5,split[a][b];[a]scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,gblur=sigma=28,eq=brightness=-0.12[bg];[b]scale=720:-2[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2-40,subtitles='{caps_v}',format=yuv420p[v]",
    "-map", "[v]", "-map", "1:a", "-c:v", "libx264", "-preset", "slow", "-crf", "22", "-profile:v", "high", "-movflags", "+faststart", "-c:a", "aac", "-b:a", "160k", "-shortest", outv])
print(outv)
subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-i", os.path.join(FR, f"f_{int(PF):04d}.png"), "-vf", "scale=1280:-1", "-q:v", "3", os.path.join(HERE, NAME + ".jpg")])
for p in (out, outv, os.path.join(HERE, NAME + ".jpg")): print(p, round(os.path.getsize(p) / 1e6, 2), "MB")
