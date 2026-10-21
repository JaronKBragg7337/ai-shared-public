# Heartbeat News (rendered show) - plan one episode for Unreal.
# Reads the full running order (script.json from episode_script.py: stories + commercials + wires; else the bare episode JSON)
# + the rendered line WAVs (render-voices.mjs / joe_voice.py) and writes, into the audio folder:
#   plan.json      every line's start frame, length, camera and audio; Vex's mouth levels; segment -> wall graphic index
#   walls/NN.png   one LED-wall graphic per segment (same look as the live show's wall), atlas.png = 4-across grid for Unreal
#   episode.wav    the whole soundtrack, lines placed at their start times
#   python episode_plan.py 2026-09-27 C:/Users/lilli/Projects/necklace-unreal/NewsAudio/2026-09-27 [--segs 0,1]
import sys, os, io, json, math, random, wave, struct, urllib.request
from PIL import Image, ImageDraw, ImageFont
DATE, D = sys.argv[1], sys.argv[2]
SEGS = [int(x) for x in sys.argv[sys.argv.index("--segs") + 1].split(",")] if "--segs" in sys.argv else None
FPS, RATE, GAP, SEG_GAP, LEAD = 24, 48000, 0.45, 0.9, 1.0
SCRIPT = os.path.join(D, "script.json")
ep = json.load(open(SCRIPT, encoding="utf-8")) if os.path.exists(SCRIPT) else json.load(urllib.request.urlopen("https://www.heartbeatobservatory.com/news/episodes/%s.json" % DATE))
os.makedirs(os.path.join(D, "walls"), exist_ok=True)

# ---- wall graphics: the same layout as the live show's LED wall (news/studio3d.js drawWall) - a theme colour per kind of
# story, kicker tab + title across the top, stat tiles on the left and bullets on the right (the anchors sit in the middle),
# and for commercials a photo of the page filling the wall under its kicker + title (Jaron 9/27: those were missing).
FD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
def font(w, s):
    try: return ImageFont.truetype(os.path.join(FD, "BarlowCondensed-%s.ttf" % ("ExtraBold" if w >= 800 else "SemiBold")), int(s))
    except Exception: return ImageFont.truetype("C:/Windows/Fonts/ARIALNB.TTF", int(s))
THEMES = {"breaking": ("#5a0710", "#1a0206", "#ff2436", "#e11d2e"), "weather": ("#06394a", "#021520", "#35d0ff", "#0a8fc2"),
          "sports": ("#0b3a1c", "#03140a", "#4be37f", "#119a45"), "open": ("#0e2a6b", "#030a1f", "#ff2e3f", "#e11d2e"),
          "close": ("#0e2a6b", "#030a1f", "#ff2e3f", "#e11d2e"), "story": ("#0c2560", "#020818", "#47a3ff", "#1552d6"),
          "wire": ("#1b1f2e", "#05060b", "#ffb020", "#c77a00"), "ad": ("#3a1b5c", "#0c0518", "#ffcf4a", "#b8860b")}
hexc = lambda h: tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))
def wrap(d, text, f, width):
    words, lines, cur = str(text).split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= width: cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines
def logo(d, x, y, s):
    d.rounded_rectangle((x, y, x + s, y + s), int(s * 0.18), fill=(11, 31, 77), outline=(255, 255, 255), width=max(2, int(s * 0.035)))
    pts = [(x + a * s, y + b * s) for a, b in [(0.08, 0.66), (0.3, 0.66), (0.38, 0.54), (0.47, 0.87), (0.58, 0.45), (0.66, 0.66), (0.92, 0.66)]]
    d.line(pts, fill=(225, 29, 46), width=max(3, int(s * 0.07)), joint="curve")
    d.text((x + s / 2, y + s * 0.36), "HBN", font=font(800, s * 0.3), fill="white", anchor="ms")
_img = {}
def site_image(src):
    if src not in _img:
        try:
            req = urllib.request.Request("https://www.heartbeatobservatory.com" + src, headers={"User-Agent": "hb-news-render"})
            _img[src] = Image.open(io.BytesIO(urllib.request.urlopen(req, timeout=30).read())).convert("RGB")
        except Exception as e: print("no image", src, e); _img[src] = None
    return _img[src]
def seams(im, W, H):   # LED cabinet seams and per-cabinet colour variance: real walls never match perfectly
    d = ImageDraw.Draw(im, "RGBA"); r = random.Random(3); cw, ch = W / 14, H / 6
    for y in range(6):
        for x in range(14):
            v = r.random(); d.rectangle((x * cw, y * ch, (x + 1) * cw, (y + 1) * ch), fill=(255, 255, 255, int((v - 0.5) * 0.05 * 255)) if v > 0.5 else (0, 0, 0, int((0.5 - v) * 0.08 * 255)))
    for x in range(1, 14): d.rectangle((x * cw - 1, 0, x * cw + 1, H), fill=(0, 0, 0, 140))
    for y in range(1, 6): d.rectangle((0, y * ch - 1, W, y * ch + 1), fill=(0, 0, 0, 140))
def kicker(d, text, x, y, u, color):
    kf = font(800, 58 * u); kw = d.textlength(text, font=kf) + 60 * u
    d.rectangle((x, y, x + kw, y + 84 * u), fill=color); d.text((x + 30 * u, y + 44 * u), text, font=kf, fill="white", anchor="lm")
def wall(seg, path):
    W, H = 2800, 1200; u = W / 2048; g = seg.get("graphic") or {}
    imgs = g.get("images") or ([g["image"]] if g.get("image") else [])
    shot = site_image(imgs[0]) if seg.get("kind") == "ad" and imgs else None
    if shot:   # a commercial: the page itself fills the wall, darkened at the bottom under its kicker and title
        s_ = max(W / shot.width, H / shot.height); sh = shot.resize((int(shot.width * s_) + 1, int(shot.height * s_) + 1), Image.LANCZOS)
        im = Image.new("RGB", (W, H)); im.paste(sh, ((W - sh.width) // 2, (H - sh.height) // 2))
        d = ImageDraw.Draw(im, "RGBA")
        for y in range(int(H * 0.62), H): d.line((0, y, W, y), fill=(0, 0, 0, int(0.72 * 255 * (y - H * 0.62) / (H * 0.38))))
        kicker(d, str(g.get("kicker") or "COMMERCIAL").upper(), 90 * u, H - 250 * u, u, hexc(THEMES["ad"][3]))
        d.text((90 * u, H - 100 * u), str(g.get("title") or "").upper(), font=font(800, 104 * u), fill="white", anchor="lm")
        logo(d, W - 250 * u, 48 * u, 160 * u); seams(im, W, H); im.save(path); return
    a, b, acc, kc = [hexc(c) for c in THEMES.get(seg.get("kind"), THEMES["story"])]
    im = Image.new("RGB", (W, H)); d = ImageDraw.Draw(im, "RGBA")
    for y in range(H):
        t = y / H; d.line((0, y, W, y), fill=tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3)))
    glow = Image.new("L", (W, H)); gd = ImageDraw.Draw(glow)
    for r_ in range(int(W * 0.6), 0, -12): gd.ellipse((W * 0.5 - r_, H * 0.25 - r_, W * 0.5 + r_, H * 0.25 + r_), fill=int(36 * (1 - r_ / (W * 0.6))))
    im.paste(Image.new("RGB", (W, H), (255, 255, 255)), (0, 0), glow); d = ImageDraw.Draw(im, "RGBA")
    for x in range(-H, W, int(28 * u)): d.line((x, H, x + H, 0), fill=(255, 255, 255, 9), width=max(1, int(2 * u)))
    for la in range(-80, 81, 8):   # dotted globe watermark, behind the anchors
        for lo in range(0, 360, 8):
            A, B = math.radians(lo), math.radians(la)
            if math.cos(B) * math.cos(A) < 0: continue
            cx, cy = W * 0.5 + math.cos(B) * math.sin(A) * 300 * u, H * 0.74 - math.sin(B) * 300 * u
            d.ellipse((cx - 3 * u, cy - 3 * u, cx + 3 * u, cy + 3 * u), fill=(255, 255, 255, 18))
    kicker(d, str(g.get("kicker") or seg.get("category") or "HEARTBEAT NEWS").upper(), 90 * u, 62 * u, u, kc)
    logo(d, W - 250 * u, 48 * u, 160 * u)
    title = str(g.get("title") or seg.get("headline") or "").upper()
    for ts in range(118, 63, -6):   # shrink the title until it fits in two lines
        tf = font(800, ts * u); tl = wrap(d, title, tf, W - 480 * u)
        if len(tl) <= 2: break
    tl = tl[:2]
    for i, ln in enumerate(tl): d.text((90 * u, 238 * u + i * ts * u), ln, font=tf, fill="white", anchor="lm")
    d.rectangle((90 * u, 300 * u + (len(tl) - 1) * ts * u, 310 * u, 308 * u + (len(tl) - 1) * ts * u), fill=acc)
    for i, st in enumerate((g.get("stats") or [])[:4]):   # stat tiles, left
        x, y = 90 * u, (430 + i * 105) * u
        d.rectangle((x, y, x + 560 * u, y + 92 * u), fill=(0, 0, 0, 97)); d.rectangle((x, y, x + 8 * u, y + 92 * u), fill=acc)
        d.text((x + 28 * u, y + 28 * u), str(st.get("label", "")).upper(), font=font(600, 34 * u), fill=(255, 255, 255, 180), anchor="lm")
        val, vs = str(st.get("value", "")), 50
        while d.textlength(val, font=font(800, vs * u)) > 520 * u and vs > 28: vs -= 2
        d.text((x + 28 * u, y + 66 * u), val, font=font(800, vs * u), fill="white", anchor="lm")
    bf = font(600, 40 * u); by = 440 * u
    for bl in (g.get("bullets") or [])[:4]:   # bullets, right
        lines = wrap(d, bl, bf, 560 * u)[:2]
        if by + len(lines) * 46 * u > H - 40 * u: break
        d.rectangle((W - 700 * u, by - 10 * u, W - 684 * u, by + 6 * u), fill=acc)
        for j, ln in enumerate(lines): d.text((W - 665 * u, by + j * 46 * u), ln, font=bf, fill="white", anchor="lm")
        by += (len(lines) * 46 + 34) * u
    seams(im, W, H); im.save(path)
segs = [(i, s) for i, s in enumerate(ep["segments"]) if (SEGS is None or i in SEGS)]
# atlas: 4 across and as many rows as needed, always 8192 x 4096 (power of two, so Unreal keeps mips and full quality)
COLS = 4; ROWS = max(1, math.ceil(len(segs) / COLS)); CW, CH = 8192 // COLS, 4096 // ROWS
atlas = Image.new("RGB", (8192, 4096))
for k, (i, s) in enumerate(segs):
    p = os.path.join(D, "walls", "%02d.png" % i); wall(s, p)
    atlas.paste(Image.open(p).resize((CW, CH), Image.LANCZOS), ((k % COLS) * CW, (k // COLS) * CH))
atlas.save(os.path.join(D, "walls", "atlas.png"))
if "--walls-only" in sys.argv: sys.exit(0)

# ---- timing, cameras, audio
man = {m["file"]: m for w in ("vex", "joe") for m in json.load(open(os.path.join(D, "manifest_%s.json" % w)))}
def read_wav(p):
    w = wave.open(p); n = w.getnframes(); sr = w.getframerate(); ch = w.getnchannels(); raw = w.readframes(n); w.close()
    s = struct.unpack("<%dh" % (n * ch), raw)[::ch]
    if sr != RATE: s = [s[int(i * sr / RATE)] for i in range(int(n * RATE / sr))]
    return s
t = LEAD; plan = {"date": DATE, "fps": FPS, "wall_grid": [COLS, ROWS], "lines": [], "segments": []}; track = []
for k, (i, s) in enumerate(segs):
    if not s.get("lines"): continue
    plan["segments"].append({"seg": i, "id": s.get("id"), "wall": k, "start": int(t * FPS)})
    for li, l in enumerate(s["lines"]):
        f = "%02d_%02d_%s.wav" % (i, li, l["who"]); samples = read_wav(os.path.join(D, f))
        dur = len(samples) / RATE
        cam = l.get("shot") or (("wide" if s.get("kind") in ("ad", "weather") else "two") if li == 0 else l["who"])   # commercials + weather open on the wall, like the live show
        lev = []
        if l["who"] == "vex":
            hop = RATE // FPS
            for a in range(0, len(samples), hop):
                seg_ = samples[a:a + hop]; lev.append(round(min(1.0, math.sqrt(sum(x * x for x in seg_) / max(1, len(seg_))) / 32768 * 5.0), 3))
        plan["lines"].append({"seg": i, "line": li, "who": l["who"], "file": f, "start": int(round(t * FPS)), "frames": int(math.ceil(dur * FPS)), "camera": cam, "levels": lev})
        track.append((int(t * RATE), samples)); t += dur + GAP
    t += SEG_GAP - GAP
plan["frames"] = int(math.ceil((t + 0.6) * FPS))
out = [0] * int((t + 0.6) * RATE)
for at, smp in track:
    for j, v in enumerate(smp):
        if at + j < len(out): out[at + j] = max(-32767, min(32767, out[at + j] + v))
w = wave.open(os.path.join(D, "episode.wav"), "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(RATE)
w.writeframes(struct.pack("<%dh" % len(out), *out)); w.close()
json.dump(plan, open(os.path.join(D, "plan.json"), "w"), indent=1)
print("plan: %d lines, %d segments, %d frames (%.1f s)" % (len(plan["lines"]), len(plan["segments"]), plan["frames"], plan["frames"] / FPS))
