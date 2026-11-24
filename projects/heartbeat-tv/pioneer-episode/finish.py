# Pioneer episode (Science 8.11): scenes + source panels + captions + end card + mix -> the 16:9 episode, the vertical short, poster.
#   python finish.py            -> out/science-ep11-pioneer-anomaly.mp4 (1920x1080), -vertical.mp4 (1080x1920 short), .jpg
import json, os, re, subprocess, math, wave, struct
import numpy as np
from PIL import Image, ImageDraw, ImageFont
D = os.path.dirname(os.path.abspath(__file__)); TL = json.load(open(os.path.join(D, "timeline.json"), encoding="utf8"))
FPS, W, H = 24, 1920, 1080; OUT = os.path.join(D, "out"); os.makedirs(OUT, exist_ok=True); WK = os.path.join(D, "work"); os.makedirs(WK, exist_ok=True)
NAME = "science-ep11-pioneer-anomaly"; END_SECS = 9.0
FD = "C:/Windows/Fonts/"
def F(k, s): return ImageFont.truetype(FD + {"serif": "georgiab.ttf", "sans": "segoeui.ttf", "sansb": "segoeuib.ttf", "sansl": "segoeuil.ttf"}[k], s)
def run(c): print(" ".join(str(x) for x in c)[:200], flush=True); subprocess.check_call(c)
CREAM = (243, 237, 224); INK = (46, 40, 34); DIM = (120, 110, 96); ACC = (190, 112, 30)
scenes = TL["scenes"]; TOTAL = TL["seconds"]

# ---- 1. source panels (top-right, translucent) for 3D/studio scenes that carry a board
def wrap(d, txt, f, width):
    out, line = [], ""
    for w_ in txt.split():
        t_ = (line + " " + w_).strip()
        if d.textlength(t_, font=f) > width and line: out.append(line); line = w_
        else: line = t_
    if line: out.append(line)
    return out
panels = []
for sc in scenes:
    b = sc.get("board")
    if not b or sc["place"] == "board": continue
    if sc["id"] in ("s10", "s15"): lines = []          # the LED wall already shows the card; source only
    else: lines = b["lines"]
    im = Image.new("RGBA", (600, 900), (0, 0, 0, 0)); d = ImageDraw.Draw(im); y = 22
    body = []
    body.append(("t", b["title"]))
    for l in lines: body.append(("l", l))
    body.append(("s", "Source: " + b["source"]))
    rows = []
    for k, txt in body:
        f = F("sansb", 30) if k == "t" else F("sans", 24) if k == "l" else F("sansl", 19)
        for i, r in enumerate(wrap(d, txt, f, 540 - (22 if k == "l" else 0))): rows.append((k, r, f, i == 0))
    hgt = 24 + sum((40 if k == "t" else 31 if k == "l" else 25) for k, *_ in rows) + 18
    d.rounded_rectangle((0, 0, 599, hgt), 16, fill=(12, 16, 26, 190), outline=(255, 255, 255, 40), width=2)
    d.rectangle((0, 18, 6, hgt - 18), fill=(225, 29, 46, 230))
    for k, r, f, first in rows:
        x = 30
        if k == "l":
            if first: d.ellipse((30, y + 11, 40, y + 21), fill=(255, 176, 32, 255))
            x = 52
        d.text((x, y), r, font=f, fill=(255, 255, 255, 255) if k != "s" else (200, 205, 215, 255)); y += 40 if k == "t" else 31 if k == "l" else 25
    im = im.crop((0, 0, 600, hgt + 2)); p = os.path.join(WK, "panel_%s.png" % sc["id"]); im.save(p)
    a = sc["start"] + 1.2; bnd = sc["end"] - 0.8
    if sc["id"] == "s05": bnd = min(bnd, sc["start"] + 14.0)     # keep the burned-in labels clear later in the orbit
    panels.append((p, a, bnd, {"s05": "x=48:y=H-h-250", "s09": "x=48:y=420"}.get(sc["id"], "x=W-w-48:y=48")))

# ---- 2. captions (ASS), from the line timings; long lines split at sentence/comma breaks into <= 2-line pieces
def pieces(text, limit=84):
    parts = re.split(r"(?<=[.!?:])\s+", text.strip()); out = []
    for p in parts:
        while len(p) > limit:
            cut = p.rfind(",", 0, limit); cut = cut if cut > 30 else p.rfind(" ", 0, limit)
            out.append(p[:cut + 1].strip()); p = p[cut + 1:].strip()
        if p: out.append(p)
    merged = []
    for p in out:
        if merged and len(merged[-1]) + len(p) + 1 <= limit and not merged[-1].endswith((".", "!", "?")): merged[-1] += " " + p
        else: merged.append(p)
    return merged
def ts(s): return "%d:%02d:%05.2f" % (int(s // 3600), int(s % 3600 // 60), s % 60)
def ass(vertical):
    if vertical: hdr_size, mv, wrapw = 58, 330, 1080
    else: hdr_size, mv, wrapw = 50, 60, 1920
    out = ["[Script Info]", "ScriptType: v4.00+", "PlayResX: %d" % (1080 if vertical else 1920), "PlayResY: %d" % (1920 if vertical else 1080), "WrapStyle: 0", "",
           "[V4+ Styles]", "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
           "Style: Joe,Segoe UI Semibold,%d,&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,0,0,0,0,100,100,0,0,3,10,0,2,90,90,%d,1" % (hdr_size, mv),
           "Style: Vex,Segoe UI Semibold,%d,&H00FFE7B0,&H00FFFFFF,&H00000000,&H96000000,0,0,0,0,100,100,0,0,3,10,0,2,90,90,%d,1" % (hdr_size, mv), "",
           "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
    ev = []
    for sc in scenes:
        for ln in sc["lines"]:
            ps = pieces(ln["text"]); tot = sum(len(p) for p in ps); t = ln["start"]
            for p in ps:
                d_ = ln["dur"] * len(p) / tot; ev.append((t, t + d_, "Joe" if ln["who"] == "joe" else "Vex", p)); t += d_
    for i, (a, b, st, txt) in enumerate(ev):
        nxt = ev[i + 1][0] if i + 1 < len(ev) else b + 0.4
        b2 = min(max(b, a + 1.0) + 0.25, nxt - 0.02)
        out.append("Dialogue: 0,%s,%s,%s,,0,0,0,,%s" % (ts(a), ts(b2), st, txt.replace("{", "(").replace("}", ")")))
    return "\n".join(out) + "\n", ev
caps, EV = ass(False); open(os.path.join(WK, "caps.ass"), "w", encoding="utf8").write(caps)

# ---- 3. end card (cream, all sources + credits)
srcs = []
for sc in scenes:
    b = sc.get("board")
    if b:
        for s_ in re.split(r";\s*", b["source"]):
            s_ = s_.strip()
            if s_ and not s_.startswith("Our math") and s_ not in srcs: srcs.append(s_)
im = Image.new("RGB", (W, H), CREAM); d = ImageDraw.Draw(im)
d.text((W / 2, 70), "Science 8.11 · The Pioneer Anomaly", font=F("serif", 56), fill=INK, anchor="ma")
d.line([(W / 2 - 110, 150), (W / 2 + 110, 150)], fill=ACC, width=4)
d.text((W / 2, 178), "Mostly solved: uneven heat from the spacecraft itself. No new physics needed.", font=F("sans", 30), fill=INK, anchor="ma")
d.text((150, 250), "Sources", font=F("sansb", 30), fill=INK)
y = 300
for s_ in srcs: d.text((150, y), s_, font=F("sans", 22), fill=INK); y += 33
y += 24
cred = ["Hosts: Alien Joe and Robot Vex of Heartbeat News. Episode idea: Grok, on X.",
        "Script and research: Claude (Opus 5.5). Fact check: Codex. Studio scenes and movement: Claude Fable. Space scenes: Claude (Opus 5.5).",
        "Voices: Kokoro (Joe) and the Heartbeat News voice chain. Rendered in Unreal Engine 5.8 on the Heartbeat MSI.",
        "Every 3D shot is an illustration, not real footage. Heat views are false color. Distances not to scale."]
for c in cred:
    for r in wrap(d, c, F("sansl", 23), 1620): d.text((150, y), r, font=F("sansl", 23), fill=DIM); y += 32
d.text((W / 2, 1000), "heartbeatobservatory.com", font=F("sansb", 30), fill=ACC, anchor="ma")
im.save(os.path.join(WK, "endcard.png"))

# ---- 4. sound: dialogue + soft pad + liftoff rumble (s03) -> mix.wav (48 kHz stereo)
R = 48000; N = int((TOTAL + END_SECS) * R)
w = wave.open(os.path.join(D, "voices", "dialogue.wav")); dia = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
v = np.zeros(N, np.float32); v[:min(N, len(dia))] = dia[:N]
tt = np.arange(N) / R; pad = np.zeros(N, np.float32)
chords = [(110.0, 164.81, 220.0, 277.18), (98.0, 146.83, 196.0, 246.94), (87.31, 130.81, 174.61, 220.0), (98.0, 146.83, 196.0, 293.66)]
seg = 8.0
for i in range(int(N / R / seg) + 1):
    a, b = int(i * seg * R), min(N, int((i + 1) * seg * R + 2 * R))
    if a >= N: break
    t_ = np.arange(b - a) / R; env = np.minimum(1, t_ / 2.5) * np.minimum(1, np.maximum(0, (b - a) / R - t_) / 2.5)
    for f in chords[i % 4]: pad[a:b] += np.sin(2 * np.pi * f * t_ + i) * env * 0.012
    pad[a:b] += np.sin(2 * np.pi * chords[i % 4][0] / 2 * t_) * env * 0.01
# duck the pad under speech
lvl = np.convolve(np.abs(v), np.ones(4800) / 4800, mode="same"); duck = 1 - 0.55 * np.minimum(1, lvl * 40)
mixm = v * 0.95 + pad * duck
s03 = next(s for s in scenes if s["id"] == "s03"); la = s03["start"] + 100 / FPS; lb = s03["start"] + 330 / FPS
rng = np.random.default_rng(1); ia, ib = int(la * R), int(lb * R); noise = np.cumsum(rng.standard_normal(ib - ia)).astype(np.float32)
noise -= np.convolve(noise, np.ones(2400) / 2400, mode="same"); noise /= (np.abs(noise).max() + 1e-9)
t_ = np.arange(ib - ia) / R; envr = np.minimum(1, t_ / 0.4) * np.minimum(1, (t_[-1] - t_) / 2.5)
mixm[ia:ib] += noise * envr * 0.18
end0 = int(TOTAL * R); fo = np.ones(N, np.float32); fo[end0 + int(6 * R):] = np.linspace(1, 0, N - end0 - int(6 * R)); mixm *= fo
mixm = np.clip(mixm, -0.98, 0.98); st = (np.stack([mixm, mixm], 1) * 32767).astype(np.int16)
w = wave.open(os.path.join(WK, "mix.wav"), "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(R); w.writeframes(st.tobytes()); w.close()

# ---- 5. picture: concat scenes + end card, overlays, captions -> main mp4
lst = os.path.join(WK, "concat.txt")
run(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-framerate", str(FPS), "-i", os.path.join(WK, "endcard.png"), "-t", str(END_SECS), "-vf", "fade=in:0:12,format=yuv420p", "-c:v", "libx264", "-crf", "16", "-r", str(FPS), os.path.join(WK, "endcard.mp4")])
with open(lst, "w") as f:
    for sc in scenes: f.write("file '%s'\n" % os.path.join(D, "renders", sc["id"] + ".mp4").replace("\\", "/"))
    f.write("file '%s'\n" % os.path.join(WK, "endcard.mp4").replace("\\", "/"))
inp = ["-f", "concat", "-safe", "0", "-i", lst]
fc = "[0:v]setpts=N/(%d*TB)[v0]" % FPS; last = "v0"
for i, (p, a, b, pos) in enumerate(panels):
    inp += ["-loop", "1", "-framerate", str(FPS), "-t", "%.2f" % (TOTAL + END_SECS), "-i", p]; nl = "v%d" % (i + 1)
    fc += ";[%d:v]format=rgba,fade=in:st=%.2f:d=0.5:alpha=1,fade=out:st=%.2f:d=0.5:alpha=1[p%d];[%s][p%d]overlay=%s:enable='between(t,%.2f,%.2f)'[%s]" % (i + 1, a, b - 0.5, i, last, i, pos, a, b, nl)
    last = nl
capf = os.path.join(WK, "caps.ass").replace("\\", "/").replace(":", "\\:")
fc += ";[%s]subtitles='%s'[vout]" % (last, capf)
inp += ["-i", os.path.join(WK, "mix.wav")]
main = os.path.join(OUT, NAME + ".mp4")
run(["ffmpeg", "-y", "-v", "error"] + inp + ["-filter_complex", fc, "-map", "[vout]", "-map", "%d:a" % (len(panels) + 1),
     "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-r", str(FPS), "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", main])
# poster: s04 (van beside Pioneer) with the title
s04 = next(s for s in scenes if s["id"] == "s04")
run(["ffmpeg", "-y", "-v", "error", "-ss", "%.2f" % (s04["start"] + 20), "-i", os.path.join(D, "renders", "s04.mp4").replace("s04.mp4", "s04.mp4"), "-frames:v", "1", "-vf", "scale=1280:-1", os.path.join(WK, "poster_raw.png")]) if False else None
run(["ffmpeg", "-y", "-v", "error", "-ss", "20", "-i", os.path.join(D, "renders", "s04.mp4"), "-frames:v", "1", "-vf", "scale=1280:720", os.path.join(WK, "poster_raw.png")])
pi = Image.open(os.path.join(WK, "poster_raw.png")).convert("RGB"); pd = ImageDraw.Draw(pi, "RGBA")
pd.rectangle((0, 560, 1280, 720), fill=(8, 10, 18, 200)); pd.text((40, 578), "The Pioneer Anomaly", font=F("serif", 56), fill=(255, 255, 255))
pd.text((42, 650), "Science 8.11 · a news crew field trip · mostly solved", font=F("sans", 28), fill=(255, 200, 120))
pi.save(os.path.join(OUT, NAME + ".jpg"), quality=90)

# ---- 6. vertical short (1080x1920): hook from s01, the anomaly (s07), the heat answer (s12), the close (s15)
s01 = scenes[0]; pick = [(s01["lines"][2]["start"] - 0.3, s01["lines"][4]["start"] + s01["lines"][4]["dur"] + 0.4)]
for sid in ("s07", "s12", "s15"):
    sc = next(s for s in scenes if s["id"] == sid); pick.append((sc["start"], sc["end"] if sid != "s15" else min(TOTAL, sc["end"])))
vparts = []
for i, (a, b) in enumerate(pick):
    o = os.path.join(WK, "vpart%d.mp4" % i)
    run(["ffmpeg", "-y", "-v", "error", "-ss", "%.3f" % a, "-to", "%.3f" % b, "-i", main.replace(".mp4", "_clean.mp4") if False else main, "-c:v", "libx264", "-crf", "18", "-c:a", "aac", "-b:a", "160k", o])
    vparts.append(o)
vl = os.path.join(WK, "vconcat.txt"); open(vl, "w").write("".join("file '%s'\n" % p.replace("\\", "/") for p in vparts))
top = Image.new("RGB", (1080, 1920), (8, 10, 18)); td = ImageDraw.Draw(top)
td.text((540, 300), "The Pioneer Anomaly", font=F("serif", 74), fill=(255, 255, 255), anchor="ma")
td.text((540, 400), "Science 8.11 · Heartbeat TV", font=F("sans", 40), fill=(255, 190, 110), anchor="ma")
td.text((540, 1560), "Full episode: heartbeatobservatory.com", font=F("sansb", 40), fill=(255, 255, 255), anchor="ma")
top.save(os.path.join(WK, "vbg.png"))
vert = os.path.join(OUT, NAME + "-vertical.mp4")
run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", vl, "-loop", "1", "-i", os.path.join(WK, "vbg.png"),
     "-filter_complex", "[0:v]scale=1080:-2,setsar=1[m];[1:v][m]overlay=0:(H-h)/2:shortest=1,format=yuv420p[v]", "-map", "[v]", "-map", "0:a",
     "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", vert])
print("done", main, vert)
