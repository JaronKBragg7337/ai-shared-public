# Pillow boards for Science 8.10 Antarctica Part 2: the sky in the ice (cream-paper look, same family as ep6-ep9).  python diagram.py [FRAMES_DIR] [--force] [--only=name] [--preview]
import math, os, sys, random
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shots import SHOTS, FPS
OUT = next((a for a in sys.argv[1:] if not a.startswith("--")), "C:/Users/lilli/Renders/antarctica-p2/frames")
W, H, SS = 1280, 720, 2
CREAM = (243, 237, 224); INK = (46, 40, 34); DIM = (120, 110, 96); RULE = (200, 190, 172); PAPER = (236, 226, 206)
AMBER = (196, 120, 28); RED = (178, 70, 52); BLUE = (62, 110, 170); MARS = (196, 110, 62); MARSD = (150, 78, 44)
MOON = (118, 110, 100); MOOND = (80, 74, 68); CAP = (240, 240, 236)
FD = "C:/Windows/Fonts/"
_f = {}
def font(kind, size):
    k = (kind, size)
    if k not in _f: _f[k] = ImageFont.truetype(FD + {"serif": "georgiab.ttf", "serifr": "georgia.ttf", "sans": "segoeui.ttf", "sansb": "segoeuib.ttf", "sansl": "segoeuil.ttf"}[kind], size * SS)
    return _f[k]
def ease(x): x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)
def mix(a, b, u): return tuple(int(a[i] + (b[i] - a[i]) * u) for i in range(3))

class Cv:
    def __init__(s):
        s.im = Image.new("RGB", (W * SS, H * SS), CREAM); s.d = ImageDraw.Draw(s.im)
    def P(s, p): return (p[0] * SS, p[1] * SS)
    def poly(s, pts, fill, outline=None, w=2): s.d.polygon([s.P(p) for p in pts], fill=fill, outline=outline, width=w * SS if outline else 0)
    def line(s, pts, col, w=2): s.d.line([s.P(p) for p in pts], fill=col, width=w * SS, joint="curve")
    def dashed(s, pts, col, w=2, dash=8, gap=6):
        for a, b in zip(pts, pts[1:]):
            L_ = math.hypot(b[0] - a[0], b[1] - a[1]); n = max(1, int(L_ / (dash + gap)))
            if L_ < 1e-6: continue
            for i in range(n):
                u0 = i * (dash + gap) / L_; u1 = min(1, (i * (dash + gap) + dash) / L_)
                s.line([(a[0] + (b[0] - a[0]) * u0, a[1] + (b[1] - a[1]) * u0), (a[0] + (b[0] - a[0]) * u1, a[1] + (b[1] - a[1]) * u1)], col, w)
    def rect(s, b, fill, outline=None, w=2, r=0):
        bb = [b[0] * SS, b[1] * SS, b[2] * SS, b[3] * SS]
        s.d.rounded_rectangle(bb, radius=r * SS, fill=fill, outline=outline, width=w * SS if outline else 0)
    def circ(s, c, r, fill, outline=None, w=2): s.d.ellipse([(c[0] - r) * SS, (c[1] - r) * SS, (c[0] + r) * SS, (c[1] + r) * SS], fill=fill, outline=outline, width=w * SS if outline else 0)
    def ring(s, c, r, col, w=2): s.circ(c, r, None, col, w)
    def arc(s, c, r, a0, a1, col, w=2): s.d.arc([(c[0] - r) * SS, (c[1] - r) * SS, (c[0] + r) * SS, (c[1] + r) * SS], a0, a1, fill=col, width=w * SS)
    def text(s, xy, t, kind, size, col, anchor="la", a=1.0): s.d.text(s.P(xy), t, font=font(kind, size), fill=mix(CREAM, col, a), anchor=anchor)
    def para(s, x, y, t, kind, size, col, maxw, lh=1.3, anchor="l", a=1.0):
        f = font(kind, size); words = t.split(); lines = []; cur = ""
        for w_ in words:
            tt = (cur + " " + w_).strip()
            if f.getlength(tt) <= maxw * SS or not cur: cur = tt
            else: lines.append(cur); cur = w_
        if cur: lines.append(cur)
        for i, l in enumerate(lines): s.d.text(s.P((x, y + i * size * lh)), l, font=f, fill=mix(CREAM, col, a), anchor="ma" if anchor == "m" else "la")
        return y + len(lines) * size * lh
    def tag(s, cx, cy, t, a=1.0, wdt=150, col=AMBER):
        s.rect((cx - wdt / 2, cy - 15, cx + wdt / 2, cy + 15), mix(CREAM, (236, 220, 190), a), outline=mix(CREAM, col, a), w=2, r=8)
        s.text((cx, cy - 10), t, "sansb", 16, col, "ma", a)
    def arrow(s, a_, b_, col, w=3, head=9):
        s.line([a_, b_], col, w)
        ang = math.atan2(b_[1] - a_[1], b_[0] - a_[0])
        s.poly([b_, (b_[0] - head * math.cos(ang - .5), b_[1] - head * math.sin(ang - .5)), (b_[0] - head * math.cos(ang + .5), b_[1] - head * math.sin(ang + .5))], col)
    def potato(s, c, r, col, outline, rot=0.0, a=1.0, seed=3, w=2):
        rs = random.Random(seed); pts = []
        for i in range(40):
            t = 2 * math.pi * i / 40
            rr = r * (1 + .08 * math.sin(3 * t + seed) + .05 * math.cos(5 * t + 1.3 * seed))
            pts.append((c[0] + rr * 1.18 * math.cos(t + rot), c[1] + rr * .9 * math.sin(t + rot)))
        s.poly(pts, mix(CREAM, col, a), mix(CREAM, outline, a), w)
    def header(s, title, sub, a):
        s.text((W / 2, 30), title, "serif", 40, INK, "ma", a)
        s.text((W / 2, 84), sub, "sans", 19, DIM, "ma", a)
        s.line([(W / 2 - 70, 116), (W / 2 + 70, 116)], mix(CREAM, AMBER, a), 3)



