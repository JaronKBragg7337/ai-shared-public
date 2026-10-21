# Heartbeat TV - Still Unknown ep.2 "Coral Castle: one man, 1,100 tons" (CPU only: Pillow + numpy + ffmpeg libx264)
# Own look (NOT the navy/gold/serif History-Science cards): near-black violet void, thin Segoe Light headlines in lowercase,
# Consolas data/sources, full-bleed expanding-universe simulation behind every scene, left-aligned lower-third captions,
# status tags DOCUMENTED / CLAIMED / NOT ESTABLISHED / NOT SETTLED / UNKNOWN; every image is drawn here (no photos).
#   python ep.py land|port [--still SECONDS out.png] [--secs A B] [--out file.mp4]
import json, math, subprocess, sys, random
from multiprocessing import Pool
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

TL = json.load(open('timeline.json'))
TOTAL = TL['total']; SEG = {s['id']: s for s in TL['segs']}
FPS = 30; SS = 2
ORI = 'port' if 'port' in sys.argv[1:2] else 'land'
PORT = ORI == 'port'
W, H = (1080, 1920) if PORT else (1920, 1080)

BG = (5, 6, 14); INK = (16, 14, 34); INK2 = (28, 24, 56)
CYAN = (92, 232, 236); VIO = (168, 140, 255); ROSE = (255, 112, 150); MINT = (128, 240, 196)
TXT = (234, 232, 244); DIM = (134, 132, 156); DIM2 = (80, 78, 100)
FD = 'C:/Windows/Fonts/'
_fc = {}
def font(kind, size):
    k = (kind, size)
    if k not in _fc:
        f = {'light': 'segoeuil.ttf', 'semi': 'segoeuisl.ttf', 'sans': 'segoeui.ttf', 'sansb': 'segoeuib.ttf',
             'mono': 'consola.ttf', 'monob': 'consolab.ttf'}[kind]
        _fc[k] = ImageFont.truetype(FD + f, int(size * SS))
    return _fc[k]

SZ = dict(head=66 if PORT else 76, cap=50 if PORT else 42, src=26 if PORT else 24)
if PORT:
    HEAD = (80, 150, W - 60, 420); CONT = (60, 450, W - 60, 1300); CAP = (80, 1420, W - 80, 1760); SRC = (80, 1800, W - 80, 1900)
else:
    HEAD = (120, 70, 1300, 200); CONT = (120, 230, W - 120, 840); CAP = (150, 870, 1500, 1010); SRC = (1320, 60, W - 60, 180)

def mix(c, d, a): return tuple(int(c[i] * a + d[i] * (1 - a)) for i in range(3))
def ease(x):
    x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)
def clamp01(x): return max(0.0, min(1.0, x))
def lerp(a, b, u): return a + (b - a) * u

def wrap(txt, f, maxw):
    words = txt.split(); lines = []; cur = ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if f.getlength(t) <= maxw * SS or not cur: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

class Cv:
    def __init__(s):
        s.im = Image.new('RGB', (W * SS, H * SS), BG); s.d = ImageDraw.Draw(s.im)
    def P(s, p): return (p[0] * SS, p[1] * SS)
    def rect(s, b, fill, r=0):
        bb = [b[0] * SS, b[1] * SS, b[2] * SS, b[3] * SS]
        if r: s.d.rounded_rectangle(bb, radius=r * SS, fill=fill)
        else: s.d.rectangle(bb, fill=fill)
    def outline(s, b, col, w=2, r=0):
        bb = [b[0] * SS, b[1] * SS, b[2] * SS, b[3] * SS]
        s.d.rounded_rectangle(bb, radius=r * SS, outline=col, width=max(1, int(w * SS)))
    def line(s, pts, col, w):
        s.d.line([s.P(p) for p in pts], fill=col, width=max(1, int(w * SS)), joint='curve')
    def circ(s, c, r, fill):
        s.d.ellipse([(c[0] - r) * SS, (c[1] - r) * SS, (c[0] + r) * SS, (c[1] + r) * SS], fill=fill)
    def ring(s, c, r, col, w=2):
        s.d.ellipse([(c[0] - r) * SS, (c[1] - r) * SS, (c[0] + r) * SS, (c[1] + r) * SS], outline=col, width=max(1, int(w * SS)))
    def text(s, xy, t, kind, size, col, anchor='la', a=1.0):
        if a <= 0: return
        s.d.text(s.P(xy), t, font=font(kind, size), fill=mix(col, BG, a), anchor=anchor)
    def para(s, x, y, t, kind, size, col, maxw, lh=1.25, anchor='l', a=1.0):
        f = font(kind, size); ls = wrap(t, f, maxw)
        if a <= 0: return y + len(ls) * size * lh
        for i, l in enumerate(ls):
            s.d.text(s.P((x, y + i * size * lh)), l, font=f, fill=mix(col, BG, a), anchor={'l': 'la', 'm': 'ma', 'r': 'ra'}[anchor])
        return y + len(ls) * size * lh
    def vtext(s, xy, t, kind, size, col, a=1.0):
        """vertical (rotated 90 deg, reading bottom-to-top) label"""
        f = font(kind, size); w = int(f.getlength(t)) + 4; h = int(size * SS * 1.3)
        im = Image.new('RGB', (w, h), BG); ImageDraw.Draw(im).text((2, 0), t, font=f, fill=mix(col, BG, a))
        im = im.rotate(90, expand=True); s.im.paste(im, s.P(xy))

# ------------------------------------------------------------------ the universe behind everything
R = random.Random(7)
STARS = [(R.random(), R.random(), R.uniform(0.6, 2.2), R.uniform(0.25, 1.0), R.uniform(0, 6.28)) for _ in range(420)]
GAL = []
for i in range(260):   # comoving positions in a disc, projected; a(t) scales them from the centre
    r = R.uniform(0.04, 1.0) ** 0.7; th = R.uniform(0, 6.283)
    GAL.append((r * math.cos(th), r * math.sin(th), R.uniform(2.0, 5.5), R.choice([CYAN, VIO, TXT, TXT, DIM]), R.uniform(0, 6.28)))

def universe(cv, tt, a_glow=1.0, scale=1.0, accel=0.0, dim=1.0):
    """starfield + galaxies drifting outward: positions scale with a(t) = scale*(1 + 0.012 tt + accel*tt^2)."""
    cx, cy = W / 2, H * 0.5
    for (x, y, r, b, ph) in STARS:
        tw = 0.65 + 0.35 * math.sin(tt * 1.3 + ph)
        cv.circ((x * W, y * H), r * 0.9, mix(TXT, BG, b * tw * min(1.0, 0.9 * dim + 0.25)))
    a = scale * (1 + 0.012 * tt + accel * tt * tt)
    span = max(W, H) * 0.62
    for (x, y, r, col, ph) in GAL:
        px, py = cx + x * span * a, cy + y * span * a
        if -40 < px < W + 40 and -40 < py < H + 40:
            d = math.hypot(x, y)
            al = (0.45 + 0.55 * (1 - d)) * min(1.0, dim * 1.6) * a_glow
            cv.circ((px, py), r * (0.8 + 0.4 * a), mix(col, BG, al))
            cv.circ((px, py), r * 2.2, mix(col, BG, al * 0.12))

def tag(cv, x, y, label, col, a=1.0, size=22, anchor='l'):
    """status tag: thin mono, square corners, coloured left bar - deliberately not the History rounded badge."""
    f = font('monob', size); w = f.getlength(label) / SS + 30; h = size + 16
    if a <= 0: return w
    x0 = x if anchor == 'l' else (x - w if anchor == 'r' else x - w / 2)
    cv.rect((x0, y, x0 + w, y + h), mix(INK2, BG, a))
    cv.rect((x0, y, x0 + 5, y + h), mix(col, BG, a))
    cv.text((x0 + 18, y + 7), label, 'monob', size, col, 'la', a)
    return w

def hline(cv, x0, x1, y, col, a=1.0, w=1): cv.line([(x0, y), (x1, y)], mix(col, BG, a), w)

def rule(cv, t, t0, y, x0=None, x1=None, col=CYAN):
    u = ease((t - t0) / 0.8); x0 = CONT[0] if x0 is None else x0; x1 = CONT[2] if x1 is None else x1
    if u > 0: cv.line([(x0, y), (x0 + (x1 - x0) * u, y)], mix(col, BG, 0.8), 2)

def big(cv, x, y, s, size, col, a=1.0, anchor='la'): cv.text((x, y), s, 'light', size, col, anchor, a)
def mono(cv, x, y, s, size, col, a=1.0, anchor='la'): cv.text((x, y), s, 'mono', size, col, anchor, a)

HUDF = None