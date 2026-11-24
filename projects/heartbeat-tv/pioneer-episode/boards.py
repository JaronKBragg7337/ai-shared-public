# Pioneer episode: the four drawn boards (s07, s08, s11, s13) in the house cream-paper look (Science 8.x diagrams).
# Each board animates in step with its lines (timeline.json), keeps the bottom 22% for captions, and shows its source.
#   python boards.py [s07 s08 ...]  -> renders/<id>.mp4 (1920x1080, 24 fps, exact scene frame count)
import json, math, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont
D = os.path.dirname(os.path.abspath(__file__)); TL = json.load(open(os.path.join(D, "timeline.json"), encoding="utf8"))
W, H, FPS = 1920, 1080, 24
CREAM = (243, 237, 224); INK = (46, 40, 34); DIM = (120, 110, 96); RULE = (200, 190, 172); PAPER = (236, 226, 206)
ACC = (190, 112, 30); RED = (176, 62, 48); BLUE = (52, 110, 170); SUN = (236, 170, 40); GREEN = (60, 130, 80)
FD = "C:/Windows/Fonts/"; _f = {}
def F(kind, size):
    k = (kind, size)
    if k not in _f: _f[k] = ImageFont.truetype(FD + {"serif": "georgiab.ttf", "serifr": "georgia.ttf", "sans": "segoeui.ttf", "sansb": "segoeuib.ttf", "sansl": "segoeuil.ttf", "sym": "seguisym.ttf"}[kind], size)
    return _f[k]
def mix(a, b, u): u = max(0.0, min(1.0, u)); return tuple(int(a[i] + (b[i] - a[i]) * u) for i in range(3))
def ease(u): u = max(0.0, min(1.0, u)); return u * u * (3 - 2 * u)
def ramp(t, t0, d=0.6): return ease((t - t0) / d)
class Cv:
    def __init__(s): s.im = Image.new("RGB", (W, H), CREAM); s.d = ImageDraw.Draw(s.im)
    def text(s, xy, txt, kind, size, col, anchor="la", a=1.0):
        if a <= 0.01: return
        s.d.text(xy, txt, font=F(kind, size), fill=mix(CREAM, col, a), anchor=anchor)
    def para(s, x, y, txt, kind, size, col, width, lh=1.3, a=1.0):
        words, line, yy = txt.split(), "", y
        for w_ in words:
            t_ = (line + " " + w_).strip()
            if s.d.textlength(t_, font=F(kind, size)) > width and line: s.text((x, yy), line, kind, size, col, "la", a); yy += size * lh; line = w_
            else: line = t_
        if line: s.text((x, yy), line, kind, size, col, "la", a); yy += size * lh
        return yy
def frame_base(cv, sc, t):
    b = sc["board"]; a = ramp(t, 0.1, 0.8)
    cv.text((W / 2, 52), b["title"], "serif", 60, INK, "ma", a)
    cv.d.line([(W / 2 - 90, 132), (W / 2 + 90, 132)], fill=mix(CREAM, ACC, a), width=4)
    cv.text((W / 2, 808), "Source: " + b["source"], "sansl", 22, DIM, "ma", a)
def bullets(cv, sc, t, x, y, width, size=30, times=None, lh=1.28, gap=18):
    for i, ln in enumerate(sc["board"]["lines"]):
        t0 = times[i] if times else 0.5 + i * 0.8
        a = ramp(t, t0)
        cv.d.ellipse((x, y + size * 0.42, x + 12, y + size * 0.42 + 12), fill=mix(CREAM, ACC, a))
        y = cv.para(x + 28, y, ln, "sans", size, INK, width - 28, lh, a) + gap
    return y
def L(sc, i): return sc["lines"][i]["start"] - sc["start"]    # local start of line i

def s07(cv, sc, t):
    frame_base(cv, sc, t)
    # map: Sun, Earth orbit, dotted path out to Pioneer
    sx, sy = 260, 470; a = ramp(t, 0.3)
    for r in range(46, 20, -4): cv.d.ellipse((sx - r, sy - r, sx + r, sy + r), fill=mix(CREAM, mix(CREAM, SUN, 0.25 + (46 - r) / 40), a))
    cv.d.ellipse((sx - 70, sy - 70, sx + 70, sy + 70), outline=mix(CREAM, RULE, a), width=2)
    cv.d.ellipse((sx + 64, sy - 8, sx + 80, sy + 8), fill=mix(CREAM, BLUE, a)); cv.text((sx + 72, sy + 18), "Earth", "sans", 22, INK, "ma", a)
    cv.text((sx, sy + 60 + 40), "Sun", "sansb", 24, INK, "ma", a)
    px, py = 1080, 370
    u = ramp(t, 1.0, 2.0)
    for k in range(0, int(40 * u)):
        xx = sx + 90 + (px - sx - 90) * k / 40; yy = sy - (sy - py) * k / 40 - 40 * math.sin(math.pi * k / 40)
        cv.d.ellipse((xx - 3, yy - 3, xx + 3, yy + 3), fill=mix(CREAM, DIM, a))
    cv.d.polygon([(px - 16, py), (px, py - 16), (px + 16, py), (px, py + 16)], fill=mix(CREAM, INK, u)); cv.text((px, py - 50), "Pioneer", "sansb", 24, INK, "ma", u)
    # radio waves travelling home (line 0)
    if t > L(sc, 0):
        for k in range(4):
            ph = ((t - L(sc, 0)) * 0.35 + k / 4) % 1.0; cx = px + (sx + 80 - px) * ph; cy = py + (sy - py) * ph
            r = 22; cv.d.arc((cx - r, cy - r, cx + r, cy + r), 120, 240, fill=mix(CREAM, BLUE, ramp(t, L(sc, 0)) * (1 - ph * 0.6)), width=4)
        cv.text((680, 520), "radio signal home: its pitch tells the speed", "sans", 24, BLUE, "ma", ramp(t, L(sc, 0) + 0.8))
    # predicted vs real (line 1-2)
    u2 = ramp(t, L(sc, 1) + 2.5, 1.5)
    if u2 > 0:
        off = 46 * u2
        cv.d.ellipse((px + 80 - 10, py + 80 - 10, px + 80 + 10, py + 80 + 10), outline=mix(CREAM, DIM, u2), width=3)
        cv.text((px + 80, py + 108), "where the math said", "sans", 20, DIM, "ma", u2)
        rx = px + 80 - off; cv.d.ellipse((rx - 10, py + 80 - 10, rx + 10, py + 80 + 10), fill=mix(CREAM, RED, u2))
        cv.text((rx - 16, py + 72), "where it really was", "sansb", 20, RED, "ra", u2)
        cv.d.line([(px + 60, py + 80), (rx + 14, py + 80)], fill=mix(CREAM, RED, u2), width=3)
        cv.text((px + 80 - 23, py + 140), "(gap drawn huge)", "sansl", 18, DIM, "ma", u2)
        cv.text((sx + 110, sy - 150), "a tiny tug back, roughly toward the Sun", "sansb", 24, RED, "la", ramp(t, L(sc, 2)))
    # the number and the facts (line 3)
    bullets(cv, sc, t, 1290, 200, 560, 27, [L(sc, 0) + 0.3, L(sc, 3) + 0.5, L(sc, 1) + 0.5, L(sc, 1) + 3.0, L(sc, 1) + 3.6])
    u3 = ramp(t, L(sc, 3) + 1.5, 1.0)
    if u3 > 0:
        cv.d.rounded_rectangle((330, 610, 1210, 730), 18, fill=mix(CREAM, PAPER, u3), outline=mix(CREAM, ACC, u3), width=3)
        cv.text((770, 628), "about 0.00000000087 m/s every second", "serifr", 40, INK, "ma", u3)
        cv.text((770, 684), "John Anderson's team, JPL (1998, 2002)", "sans", 24, DIM, "ma", u3)

def s08(cv, sc, t):
    frame_base(cv, sc, t)
    # 1. gravity vs pull (line 1)
    a = ramp(t, L(sc, 1))
    cv.text((160, 190), "Earth's gravity", "serif", 32, INK, "la", a)
    cv.d.rectangle((160, 250, 160 + int(1580 * ease((t - L(sc, 1)) / 2.0)), 290), fill=mix(CREAM, BLUE, a))
    cv.text((160, 300), "9.81 m/s²", "sansb", 24, BLUE, "la", a)
    cv.text((160, 350), "Pioneer's extra pull", "serif", 32, INK, "la", ramp(t, L(sc, 1) + 1.2))
    cv.d.rectangle((160, 410, 162, 450), fill=mix(CREAM, RED, ramp(t, L(sc, 1) + 1.2)))
    cv.text((180, 412), "about 11 billion times smaller (a bar this long would be 0.0000001 pixels)", "sans", 24, RED, "la", ramp(t, L(sc, 1) + 1.8))
    # 2. after 1 year (line 3): Chicago -> Detroit
    u = ramp(t, L(sc, 3) + 2.0)
    if u > 0:
        x0, y0, x1, y1 = 180, 620, 620, 560
        cv.d.ellipse((x0 - 9, y0 - 9, x0 + 9, y0 + 9), fill=mix(CREAM, INK, u)); cv.text((x0, y0 + 18), "Chicago", "sans", 22, INK, "ma", u)
        k = ramp(t, L(sc, 3) + 2.4, 1.6); cv.d.line([(x0, y0), (x0 + (x1 - x0) * k, y0 + (y1 - y0) * k)], fill=mix(CREAM, ACC, u), width=5)
        cv.d.ellipse((x1 - 9, y1 - 9, x1 + 9, y1 + 9), fill=mix(CREAM, INK, k)); cv.text((x1, y1 + 18), "Detroit", "sans", 22, INK, "ma", k)
        cv.text((400, 500), "after 1 year: about 435 km off", "sansb", 28, ACC, "ma", u)
    # 3. after 10 years (line 4): a ring once around Earth
    u = ramp(t, L(sc, 4) + 2.5)
    if u > 0:
        cx, cy, r = 1030, 600, 95
        cv.d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=mix(CREAM, (150, 185, 215), u))
        k = ramp(t, L(sc, 4) + 3.0, 2.0); cv.d.arc((cx - r - 18, cy - r - 18, cx + r + 18, cy + r + 18), -90, -90 + 360 * k, fill=mix(CREAM, RED, u), width=6)
        cv.text((cx, cy + r + 30), "after 10 years: about 43,500 km off", "sansb", 26, RED, "ma", u)
        cv.text((cx, cy + r + 66), "Earth is about 40,000 km around", "sans", 22, DIM, "ma", u)
    bullets(cv, sc, t, 1330, 500, 520, 23, [L(sc, 1), L(sc, 3) + 2.0, L(sc, 4) + 2.5, L(sc, 5), L(sc, 3)], 1.25, 10)

def s11(cv, sc, t):
    frame_base(cv, sc, t)
    # staircase with tape boxes under it (line 1)
    a = ramp(t, L(sc, 1) + 2.0)
    for i in range(7): cv.d.rectangle((140 + i * 70, 640 - i * 60, 210 + i * 70, 650 - i * 60 + 10), fill=mix(CREAM, DIM, a))
    cv.d.line([(140, 650), (630, 230)], fill=mix(CREAM, DIM, a), width=6)
    for i, (bx, by) in enumerate([(170, 560), (270, 560), (370, 560), (220, 480), (320, 480)]):
        u = ramp(t, L(sc, 1) + 2.4 + i * 0.25)
        cv.d.rectangle((bx, by, bx + 90, by + 76), fill=mix(CREAM, (206, 176, 128), u), outline=mix(CREAM, INK, u), width=2)
        cv.d.ellipse((bx + 14, by + 20, bx + 40, by + 46), outline=mix(CREAM, INK, u), width=3); cv.d.ellipse((bx + 50, by + 20, bx + 76, by + 46), outline=mix(CREAM, INK, u), width=3)
    cv.text((330, 700), "old tapes in boxes, some under a staircase", "sans", 24, INK, "ma", a)
    # laptop + progress bar (lines 2-3)
    u = ramp(t, L(sc, 2))
    cv.d.rounded_rectangle((760, 300, 1160, 540), 12, fill=mix(CREAM, (60, 64, 72), u)); cv.d.rectangle((740, 540, 1180, 560), fill=mix(CREAM, (90, 94, 102), u))
    lines_ = ["TELEMETRY  P10  1979-04-02", "RTG1 TEMP ....  OK", "BUS TEMP .....  OK", "DOPPLER ......  OK"]
    for i, s_ in enumerate(lines_): cv.text((790, 330 + i * 40), s_, "sans", 22, (150, 230, 160), "la", u * ramp(t, L(sc, 2) + 0.6 + i * 0.4))
    k = ease((t - L(sc, 3)) / 5.0)
    if k > 0:
        cv.d.rounded_rectangle((760, 610, 1160, 650), 10, outline=mix(CREAM, INK, 1), width=2)
        cv.d.rounded_rectangle((764, 614, 764 + int(392 * k), 646), 8, fill=ACC)
        cv.text((960, 662), "%d GB" % int(round(43 * k)) + ("+" if k > 0.99 else ""), "sansb", 26, INK, "ma", 1)
    bullets(cv, sc, t, 1260, 200, 600, 25, [L(sc, 1), L(sc, 2), L(sc, 1) + 2.0, L(sc, 3) + 2.0, L(sc, 3) + 0.2], 1.25, 14)

def s13(cv, sc, t):
    frame_base(cv, sc, t)
    cards = [("Germany, 2011", "Rievers & Lämmerzahl", "heat likely explains it", L(sc, 0) + 1.5),
             ("Portugal, 2012", "Francisco et al.", "heat: 44% to 96% (at 26 years)", L(sc, 0) + 5.0),
             ("JPL team, 2012", "Turyshev et al.", "heat model: about 80%", L(sc, 1) + 1.0)]
    for i, (h, who, res, t0) in enumerate(cards):
        u = ramp(t, t0); x = 120 + i * 360
        cv.d.rounded_rectangle((x, 190, x + 330, 420), 14, fill=mix(CREAM, PAPER, u), outline=mix(CREAM, RULE, u), width=3)
        cv.text((x + 20, 210), h, "serif", 28, INK, "la", u); cv.text((x + 20, 256), who, "sans", 22, DIM, "la", u)
        cv.para(x + 20, 310, res, "sansb", 24, ACC if i == 2 else INK, 290, 1.25, u)
    # the 80% bar (line 2-3)
    u = ramp(t, L(sc, 2)); x0, x1, y = 160, 1180, 520
    if u > 0:
        cv.text((x0, y - 50), "The pull measured from the radio data = 100%", "sans", 24, INK, "la", u)
        cv.d.rectangle((x0, y, x1, y + 70), outline=mix(CREAM, INK, u), width=3)
        k = ease((t - L(sc, 2)) / 1.5); xm = x0 + (x1 - x0) * 0.8
        cv.d.rectangle((x0 + 3, y + 3, x0 + 3 + (xm - x0 - 3) * k, y + 67), fill=ACC)
        c1 = x0 + (x1 - x0) * 0.35
        cv.d.line([(c1, y + 3), (c1, y + 67)], fill=CREAM, width=3)
        cv.text(((x0 + c1) / 2, y + 18), "RTGs ~35", "sansb", 24, CREAM, "ma", k); cv.text(((c1 + xm) / 2, y + 18), "electronics ~45", "sansb", 24, CREAM, "ma", k)
        v = ramp(t, L(sc, 3))
        for xx in range(int(xm) + 6, x1, 14): cv.d.line([(xx, y + 67), (xx + 14, y + 3)], fill=mix(CREAM, RULE, v), width=3)
        cv.text(((xm + x1) / 2, y + 86), "inside the error bars", "sansb", 22, DIM, "ma", v)
        cv.text((x0 + (xm - x0) / 2, y + 86), "heat model: about 80%", "sansb", 24, ACC, "ma", k)
    u = ramp(t, L(sc, 4) + 1.5)
    if u > 0:
        cv.d.rounded_rectangle((350, 680, 990, 744), 32, outline=mix(CREAM, GREEN, u), width=3, fill=mix(CREAM, (226, 236, 222), u))
        cv.text((670, 692), "MOSTLY SOLVED · NO NEW PHYSICS", "sansb", 28, GREEN, "ma", u)
    bullets(cv, sc, t, 1290, 190, 570, 22, [c[3] for c in cards] + [L(sc, 2) + 1.0, L(sc, 3) + 0.5], 1.22, 10)

DRAW = {"s07": s07, "s08": s08, "s11": s11, "s13": s13}
if __name__ == "__main__":
    os.makedirs(os.path.join(D, "renders"), exist_ok=True)
    ids = sys.argv[1:] or list(DRAW)
    for sid in ids:
        sc = next(s for s in TL["scenes"] if s["id"] == sid); n = sc["f1"] - sc["f0"]
        if "--still" in sys.argv: continue
        out = os.path.join(D, "renders", sid + ".mp4")
        p = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "%dx%d" % (W, H), "-r", str(FPS), "-i", "-",
                              "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
        for f in range(n):
            cv = Cv(); DRAW[sid](cv, sc, f / FPS); p.stdin.write(cv.im.tobytes())
            if f in (int(n * 0.35), n - 1): cv.im.save(os.path.join(D, "qa", "%s_%d.png" % (sid, f)))
        p.stdin.close(); p.wait(); print(sid, n, "frames")
