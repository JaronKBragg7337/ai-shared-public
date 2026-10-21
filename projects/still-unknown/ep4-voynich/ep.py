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
import re
L = not PORT
# ---------------------------------------------------------------- Still Unknown shared scene kit (eps 4+), part A: helpers
# Same look as ep1-3 (ep_head.py): violet-black void, thin Segoe Light heads, Consolas data, status tags. Data-driven scenes.
def F(sid, f): return SEG[sid]['start'] + f * SEG[sid]['dur'] - BOUND[sid][0]
def ap(t, sid, f, d=0.8): return ease((t - F(sid, f)) / d)

def night(cv, tt, dim=0.5):
    for (x, y, r, b, ph) in STARS:
        tw = 0.65 + 0.35 * math.sin(tt * 1.1 + ph)
        cv.circ((x * W, y * H), r * 0.9, mix(TXT, BG, b * tw * dim))

def poly(cv, pts, fill): cv.d.polygon([cv.P(p) for p in pts], fill=fill)

def stone_card(cv, x, y, w, h, col, a=1.0):
    cv.rect((x, y, x + w, y + h), mix(INK, BG, a * 0.9)); cv.rect((x, y, x + 5, y + h), mix(col, BG, a))

def split_regions():
    """returns (text_x0, text_y0, text_w, art_rect) for rows scenes with an art panel."""
    x0, y0, x1, y1 = CONT
    if L: return x0, y0 + 10, (x1 - x0) * 0.58, (x0 + (x1 - x0) * 0.58 + 50, y0 - 10, x1, y1 - 20)
    return x0, y0 + 360, x1 - x0, (x0, y0 + 30, x1, y0 + 340)

def S_rows(sid, tags, rows, art=None, size=None):
    """tags: [(label,color,frac)] across the top; rows: [(label,color,text,frac)]; art(cv,t,R,sid)."""
    def fn(cv, t, p):
        night(cv, t, 0.5)
        x0, y0, x1, y1 = CONT
        xx = x0
        for lab, col, f in tags:
            w = tag(cv, xx, y0 - 40, lab, col, ap(t, sid, f) if f is not None else ease(t / 0.8), 20)
            xx += (w if w > 0 else 0) + 16
            if w <= 0: break
        tx, ty, tw, R = split_regions() if art else (x0, y0 + 10, x1 - x0, None)
        if not art and not L: tw = x1 - x0
        yy = ty
        sz = size or (36 if L else 32)
        for lab, col, txt, f in rows:
            aa = ap(t, sid, f)
            if aa > 0:
                tag(cv, tx, yy, lab, col, aa, 20)
                yy = cv.para(tx, yy + 50, txt, 'sans', sz, TXT, tw, 1.2, 'l', aa) + (22 if L else 16)
        if art: art(cv, t, R, sid)
    return fn

def S_table(sid, tags, rows, art=None, kw=250, size=None):
    """rows: [(key, text, color, frac, status_label_or_None, status_color)] key in mono left, text right."""
    def fn(cv, t, p):
        night(cv, t, 0.5)
        x0, y0, x1, y1 = CONT
        xx = x0
        for lab, col, f in tags:
            w = tag(cv, xx, y0 - 40, lab, col, ap(t, sid, f) if f is not None else ease(t / 0.8), 20)
            xx += (w if w > 0 else 0) + 16
            if w <= 0: break
        top = y0 + 10
        if art:
            if L: R = (x0, y0 + 10, x1, y0 + 250); top = y0 + 280
            else: R = (x0, y0 + 10, x1, y0 + 250); top = y0 + 270
            art(cv, t, R, sid)
        n = len(rows)
        rh = ((y1 - top) / max(n, 1)) if L else ((y1 - top) / max(n, 1))
        rh = min(rh, 110 if L else 150)
        for i, (k, txt, col, f, st, stc) in enumerate(rows):
            aa = ap(t, sid, f); yy = top + i * rh
            if aa <= 0: continue
            hline(cv, x0, x1, yy - 8, INK2, aa, 1)
            mono(cv, x0 + 6, yy + 4, k, 26 if L else 24, col, aa)
            sz = size or (30 if L else 28)
            if L:
                tw = (x1 - x0 - kw - (260 if st else 0))
                cv.para(x0 + kw, yy, txt, 'sans', sz, TXT, tw, 1.15, 'l', aa)
                if st: tag(cv, x1 - 10, yy + 2, st, stc, aa, 18, 'r')
            else:
                cv.para(x0 + 6, yy + 34, txt, 'sans', sz, TXT, x1 - x0 - 12, 1.15, 'l', aa)
                if st: tag(cv, x1 - 6, yy - 2, st, stc, aa, 16, 'r')
    return fn

def S_title(sid, ep_no, lines_land, lines_port, sub, tags, art=None):
    def fn(cv, t, p):
        night(cv, t, 0.9)
        y0 = 300 if PORT else 250
        mono(cv, HEAD[0], y0, f'HEARTBEAT TV  /  CH 10  /  STILL UNKNOWN  /  EP {ep_no:02d}', 28 if PORT else 26, CYAN, ease(t / 1.0))
        sz = 100 if PORT else 118
        lines = lines_port if PORT else lines_land
        for k, l in enumerate(lines): big(cv, HEAD[0], y0 + 60 + k * sz * 1.05, l, sz, TXT, ease((t - 0.3 - k * 0.25) / 1.2))
        yy = y0 + 60 + len(lines) * sz * 1.05 + 40
        mono(cv, HEAD[0], yy, sub, 24, DIM, ease((t - 1.5) / 1.0))
        ty = yy + 70; x = HEAD[0]
        for i, (lab, col, f) in enumerate(tags):
            aa = ap(t, sid, f, 0.8)
            if PORT: tag(cv, HEAD[0], ty + i * 62, lab, col, aa)
            else:
                w = tag(cv, x, ty, lab, col, aa); x += (w if w > 0 else 0) + 20
        if art and L: art(cv, t, (1100, 150, W - 60, 900), sid)
    return fn

def S_close(sid, l1, l2, tg1, tg2, last, art=None):
    def fn(cv, t, p):
        night(cv, t, 0.7)
        x0, y0, x1, y1 = CONT
        sz = 120 if L else 100
        big(cv, x0, y0 + 20, l1, sz, TXT, ap(t, sid, 0.30))
        big(cv, x0, y0 + 20 + sz * 1.2, l2, sz, TXT, ap(t, sid, 0.42))
        tag(cv, x0, y0 + 20 + sz * 2.6, tg1, ROSE, ap(t, sid, 0.34), 24); tag(cv, x0 + 330, y0 + 20 + sz * 2.6, tg2, MINT, ap(t, sid, 0.46), 24)
        cv.para(x0, y0 + 20 + sz * 3.4, last, 'light', 36 if L else 34, CYAN, x1 - x0, 1.25, 'l', ap(t, sid, 0.7, 1.2))
        if art: art(cv, t, (1300, 100, W - 60, 800) if L else (600, 1050, W - 60, 1300), sid)
    return fn

def sc_end(cv, t, p):
    night(cv, t, 0.7)
    a = ease(t / 1.0)
    y = 160 if PORT else 70
    mono(cv, HEAD[0], y, 'HEARTBEAT TV  /  CH 10', 26, CYAN, a)
    big(cv, HEAD[0], y + 40, 'still unknown', 110, TXT, a)
    mono(cv, HEAD[0], y + 170, 'heartbeatobservatory.com', 34, CYAN, a)
    yy = y + 240
    mono(cv, HEAD[0], yy, 'SOURCES', 22, DIM, ease((t - 0.6) / 1)); yy += 40
    for i, s in enumerate(SOURCES):
        yy = cv.para(HEAD[0], yy, s, 'mono', 21 if PORT else 22, TXT, (W - 2 * HEAD[0]) * (1 if PORT else 0.95), 1.25, 'l', ease((t - 0.8 - i * 0.15) / 0.8)) + 10

def rrect(cv, b, fill, edge=None, a=1.0, w=2):
    cv.rect(b, mix(fill, BG, a));
    if edge: cv.outline(b, mix(edge, BG, a), w)

# Still Unknown ep 4 body: "The book nobody can read" (Voynich MS 408). Scenes + sources; framework in su_kit_a/b.
EP = 4
RG = random.Random(408)

def marks(cv, x, y, w, a, col=DIM, size=14, seed=0):
    """a line of invented marks (NOT the real script): short strokes and loops."""
    r = random.Random(seed); xx = x
    while xx < x + w - size:
        k = r.randint(0, 3)
        if k == 0: cv.line([(xx, y + size), (xx, y)], mix(col, BG, a), 2)
        elif k == 1: cv.ring((xx + size * 0.4, y + size * 0.5), size * 0.4, mix(col, BG, a), 2)
        elif k == 2: cv.line([(xx, y + size), (xx + size * 0.5, y), (xx + size, y + size)], mix(col, BG, a), 2)
        else: cv.line([(xx, y + size * 0.5), (xx + size * 0.8, y + size * 0.5), (xx + size * 0.4, y + size)], mix(col, BG, a), 2)
        xx += size * (1.1 + r.random() * 0.8) + (size * 0.8 if r.random() < 0.18 else 0)

def art_pages(cv, t, R, sid):
    x0, y0, x1, y1 = R; a = ease(t / 1.4)
    pw = (x1 - x0 - 30) / 2; ph = min(y1 - y0 - 40, pw * 1.35)
    for k in range(2):
        px = x0 + k * (pw + 30); py = y0 + 10
        rrect(cv, (px, py, px + pw, py + ph), INK, DIM2, a)
        if k == 0:   # a plant drawn simply, and text lines
            cx = px + pw / 2
            cv.line([(cx, py + ph * 0.52), (cx + 6, py + ph * 0.34), (cx - 4, py + ph * 0.16)], mix(MINT, BG, a * 0.8), 3)
            for j, (dx, dy) in enumerate(((-34, 0.44), (30, 0.38), (-30, 0.30), (28, 0.24), (-24, 0.18))):
                cv.line([(cx, py + ph * dy + 14), (cx + dx, py + ph * dy - 10)], mix(MINT, BG, a * 0.8), 3)
            for r in range(6): marks(cv, px + 16, py + ph * 0.62 + r * 24, pw - 32, a * 0.8, DIM, 13, r)
        else:        # a chart of rings and text
            cx, cy = px + pw / 2, py + ph * 0.3
            for rr in (22, 44, 66): cv.ring((cx, cy), rr, mix(VIO, BG, a * 0.8), 2)
            for q in range(8): cv.circ((cx + 66 * math.cos(q * 0.785), cy + 66 * math.sin(q * 0.785)), 4, mix(CYAN, BG, a))
            for r in range(6): marks(cv, px + 16, py + ph * 0.62 + r * 24, pw - 32, a * 0.8, DIM, 13, r + 20)
    mono(cv, x0, y0 + ph + 22, 'ILLUSTRATION: invented marks and simple drawings, not the real pages', 17, DIM, a)

def art_book(cv, t, R, sid):
    x0, y0, x1, y1 = R; a = ease(t / 1.0)
    bw, bh = 300, 400
    bx = (x0 + x1) / 2 - bw / 2 if L else x0 + 40; by = y0 + 30 if L else y0 + 5
    if not L: bw, bh = 200, 270
    rrect(cv, (bx, by, bx + bw, by + bh), INK2, VIO, a, 3)
    cv.rect((bx, by, bx + 18, by + bh), mix(VIO, BG, a * 0.8))
    cv.text((bx + bw / 2 + 8, by + bh * 0.4), 'MS 408', 'monob', 34 if L else 26, TXT, 'mm', a)
    cv.text((bx + bw / 2 + 8, by + bh * 0.4 + 44), 'Beinecke Library', 'mono', 20 if L else 16, DIM, 'mm', a)
    cv.text((bx + bw / 2 + 8, by + bh * 0.4 + 70), 'Yale', 'mono', 20 if L else 16, DIM, 'mm', a)
    mono(cv, bx + (bw + 30 if not L else -20), by + (bh + 20 if L else 60), 'schematic book, not to scale', 17, DIM, a)

def art_dating(cv, t, R, sid):
    x0, y0, x1, y1 = R; a = ease(t / 1.0)
    ax0, ax1 = x0 + 30, x1 - 30; ay = y0 + (230 if L else 200)
    def X(yr): return ax0 + (yr - 1380) / (1460 - 1380) * (ax1 - ax0)
    cv.line([(ax0, ay), (ax1, ay)], mix(DIM2, BG, a), 3)
    for yr in range(1380, 1461, 20):
        cv.line([(X(yr), ay - 8), (X(yr), ay + 8)], mix(DIM, BG, a), 2); cv.text((X(yr), ay + 14), str(yr), 'mono', 20, DIM, 'ma', a)
    u = ap(t, sid, 0.12, 1.2)
    cv.rect((X(1404), ay - 46, X(1404) + (X(1438) - X(1404)) * u, ay - 4), mix(MINT, BG, 0.9 * a))
    cv.text(((X(1404) + X(1438)) / 2, ay - 80), 'vellum: 1404 to 1438', 'monob', 24, MINT, 'mm', u)
    mono(cv, ax0, y0 + 10, 'RADIOCARBON, UNIVERSITY OF ARIZONA, 2009', 20, CYAN, a)

def art_zipf(cv, t, R, sid):
    x0, y0, x1, y1 = R; a = ease(t / 1.0)
    px0, py0, px1, py1 = x0 + 60, y0 + 40, x1 - 20, y1 - 70
    cv.line([(px0, py0), (px0, py1), (px1, py1)], mix(DIM, BG, a), 2)
    pts = []
    for i in range(1, 60):
        xr = i / 59.0; fx = px0 + (px1 - px0) * math.log(1 + 40 * xr) / math.log(41)
        fy = py1 - (py1 - py0) * (1 - math.log(1 + 40 * xr) / math.log(41)) ** 1.6
        pts.append((fx, py0 + (py1 - py0) * (1 - (1 - xr) ** 0.55) * 0 + (py1 - py0) * (1 - 1 / (1 + 6 * xr)) * 0.0 + (py1 - fy) * 0 + (py1 - py0) * 0))
    # simple schematic: steep fall then long tail
    curve = [(px0 + (px1 - px0) * s, py0 + (py1 - py0) * (1 - 1 / (1 + 12 * s)) * 0.92) for s in [i / 60 for i in range(61)]]
    n = int(len(curve) * ease(t / 2.0))
    if n > 1: cv.line(curve[:n], mix(CYAN, BG, a), 4)
    cv.text((px0 - 12, py0), 'common', 'mono', 18, DIM, 'rm', a); cv.text((px0 - 12, py1), 'rare', 'mono', 18, DIM, 'rm', a)
    cv.text((px1, py1 + 14), 'words, ranked', 'mono', 18, DIM, 'ra', a)
    mono(cv, px0, py1 + 40, 'SCHEMATIC of a Zipf-like curve, not the real data', 17, DIM, a)

def art_entropy(cv, t, R, sid):
    x0, y0, x1, y1 = R; a = ease(t / 1.0)
    bx = x0 + (330 if L else 270); full = (x1 - bx - 40)
    mono(cv, x0, y0, 'CONDITIONAL ENTROPY (letters), bits', 20, CYAN, a)
    rows = [('Voynich text (B and L 2021)', 2.0, ROSE, 1.0), ('natural-language samples', 2.0, MINT, 0.0)]
    for i, (nm, v, col, solid) in enumerate(rows):
        yy = y0 + 50 + i * (90 if L else 80); u = ap(t, sid, 0.25 + 0.2 * i, 1.0)
        cv.text((x0, yy + 22), nm, 'sans', 22 if L else 20, TXT, 'lm', a)
        w = full * 0.45 * u
        cv.rect((bx, yy, bx + w, yy + 44), mix(col, BG, a * 0.85))
        if solid == 0.0:
            for k in range(6): cv.rect((bx + w + k * 26, yy, bx + w + k * 26 + 14, yy + 44), mix(col, BG, a * 0.85 * (1 - k / 6.5) * u))
            cv.text((bx + w + 170, yy + 22), 'higher', 'monob', 22, MINT, 'lm', u * a)
        else:
            cv.text((bx + w + 14, yy + 22), 'about 2', 'monob', 24, TXT, 'lm', u * a)
    mono(cv, x0, y0 + 50 + 2 * (90 if L else 80) + 10, 'not to scale: the language bar only shows "higher"', 17, DIM, a)

def art_sing(cv, t, R, sid):
    x0, y0, x1, y1 = R; a = ease(t / 1.0)
    sz = 70 if L else 56
    for row, (lab, order) in enumerate((('MADE AS', (1, 2, 3, 4)), ('BOUND AS', (3, 1, 4, 2)))):
        yy = y0 + 20 + row * (sz + 90)
        aa = a if row == 0 else ap(t, sid, 0.55, 1.0)
        mono(cv, x0, yy - 4, lab, 20, CYAN if row == 0 else ROSE, aa)
        for k, n in enumerate(order):
            bx = x0 + 180 + k * (sz + 16)
            rrect(cv, (bx, yy, bx + sz * 0.8, yy + sz), INK2, DIM, aa)
            cv.text((bx + sz * 0.4, yy + sz / 2), str(n), 'monob', 28, TXT, 'mm', aa)
    mono(cv, x0, y0 + 20 + 2 * (sz + 90), 'SCHEMATIC of the idea only: not the real order', 17, DIM, a)

def sc_pass(cv, t, p): pass

SC = {}
SC['s1'] = S_title('s1', 4, ('the book nobody', 'can read'), ('the book', 'nobody', 'can read'), 'Beinecke MS 408, Yale: what is established, claimed, open',
                   (('DOCUMENTED', MINT, 0.3), ('CLAIMED', VIO, 0.45), ('DISPUTED', ROSE, 0.62), ('UNKNOWN', ROSE, 0.85)), art_pages)
SC['s2'] = S_rows('s2', [('DOCUMENTED', MINT, None)], [
    ('DOCUMENTED', MINT, 'Beinecke MS 408, Yale. About 240 pages survive; about 272 is a reconstruction from gaps.', 0.12),
    ('DOCUMENTED', MINT, 'Handwritten on vellum, in a script Yale describes as unidentified. Plants, star charts, small bathing figures.', 0.45),
    ('DOCUMENTED', MINT, 'Named for Wilfrid Voynich, the dealer who bought it in 1912.', 0.78)], art_book)
SC['s3'] = S_rows('s3', [('DOCUMENTED', MINT, None), ('NOT ESTABLISHED: WHO, WHY', ROSE, 0.8)], [
    ('DOCUMENTED', MINT, 'Radiocarbon, University of Arizona, 2009: the sampled vellum dates to 1404 to 1438.', 0.1),
    ('DOCUMENTED', MINT, 'That dates the animal skin, not the writing on it.', 0.4),
    ('REPORTED', CYAN, 'Ink and paint analyses: materials consistent with the period. A modern forgery is difficult to argue.', 0.62)], art_dating)
SC['s4'] = S_table('s4', [('DOCUMENTED: 1639, 1912, 1969', MINT, None), ('CLAIMED: RUDOLF, BACON', VIO, 0.3)], [
    ('1639', 'Georg Baresch, Prague, writes to Athanasius Kircher: the earliest known mention', MINT, 0.12, 'DOCUMENTED', MINT),
    ('1665/66', 'Jan Marci relays a story told to him: Emperor Rudolf II paid 600 ducats; Roger Bacon wrote it', VIO, 0.32, 'CLAIMED', VIO),
    ('now', 'No independent record confirms the story. The Bacon idea is largely discredited', ROSE, 0.5, 'DISPUTED', ROSE),
    ('1912', 'Wilfrid Voynich buys the book', MINT, 0.68, 'DOCUMENTED', MINT),
    ('1969', 'The dealer H. P. Kraus donates it to Yale', MINT, 0.84, 'DOCUMENTED', MINT)])
SC['s5'] = S_rows('s5', [('MEASURED', MINT, None), ('COUNTS VARY', CYAN, 0.2)], [
    ('MEASURED', MINT, 'About 170,000 characters; about 38,000 transcribed words; about 8,000 different forms. A word = a string between spaces.', 0.08),
    ('MEASURED', MINT, 'Word frequencies are roughly Zipf-like, as in natural languages. Related words cluster in related places.', 0.4),
    ('NOT PROOF', ROSE, 'Patterns like these do not by themselves prove a language.', 0.78)], art_zipf)
SC['s6'] = S_rows('s6', [('MEASURED', MINT, None), ('ARGUED', VIO, 0.7)], [
    ('MEASURED', MINT, 'Bowern and Lindemann 2021: conditional entropy about 2 bits, lower than their language samples.', 0.08),
    ('MEASURED', MINT, 'Some characters appear almost only at the start or end of words.', 0.34),
    ('MEASURED', MINT, 'Two varieties, A and B, with different profiles (Currier).', 0.52),
    ('ARGUED', VIO, 'Five scribes, from the handwriting (Fagin Davis 2020).', 0.74)], art_entropy)
SC['s7'] = S_rows('s7', [('INTERPRETATION', VIO, None)], [
    ('MEASURED', MINT, 'Language-like in some ways: word frequencies, clustering.', 0.15),
    ('MEASURED', MINT, 'Unlike the languages it has been tested against in others: very predictable letters.', 0.42),
    ('NOT ESTABLISHED', ROSE, 'No proposed reading has been broadly accepted. This describes the data. It is not an explanation.', 0.7)])
SC['s8'] = S_table('s8', [('CLAIMED', VIO, None), ('DISCREDITED', ROSE, 0.45)], [
    ('1921', 'William Newbold, University of Pennsylvania: a hidden second script of microscopic shorthand', VIO, 0.12, 'CLAIMED', VIO),
    ('1931', 'John Manly, University of Chicago, in Speculum: a critique that dismantled the readings', MINT, 0.45, 'DOCUMENTED', MINT),
    ('result', 'Newbold\'s readings were not accepted. The pattern: a confident claim, then specialist critique.', ROSE, 0.75, 'DISCREDITED', ROSE)])
SC['s9'] = S_table('s9', [('CLAIMED', VIO, None), ('NONE BROADLY ACCEPTED', ROSE, 0.5)], [
    ('2013', 'Tucker and Talbert: Nahuatl, the Aztec language', VIO, 0.1, 'CLAIMED', VIO),
    ('2017', 'Nicholas Gibbs, Times Literary Supplement: abbreviated Latin on women\'s health', VIO, 0.28, 'CLAIMED', VIO),
    ('2017', 'Kondrak and Hauer: Hebrew with scrambled letters, by computer', VIO, 0.46, 'CLAIMED', VIO),
    ('2018', 'Ahmet Ardic: an old Turkic language', VIO, 0.64, 'CLAIMED', VIO),
    ('2019', 'Gerard Cheshire: a proto-Romance language', VIO, 0.82, 'CLAIMED', VIO)])
SC['s10'] = S_rows('s10', [('DISPUTED', ROSE, None)], [
    ('DISPUTED', ROSE, 'Lisa Fagin Davis on Gibbs: the method does not produce Latin that makes sense. On Cheshire: a circular method.', 0.1),
    ('DISPUTED', ROSE, 'M. Pharao Hansen on Tucker and Talbert: the readings are pure speculation.', 0.4),
    ('THE TEST', MINT, 'A credible decipherment: others get the same readable text, and it predicts pages nobody has read. None of these has met that.', 0.62)])
SC['s11'] = S_rows('s11', [('HOAX?', CYAN, None), ('NOT SETTLED', ROSE, 0.6)], [
    ('2003, RUGG', CYAN, 'A table of word parts and a card with holes (a Cardan grille) can generate text with some similar features. Shows a method is possible; not that it was used.', 0.1),
    ('2013, MONTEMURRO AND ZANETTE', VIO, 'Word patterns they argue are unlikely in a hoax. How much this proves is debated.', 0.6)])
SC['s12'] = S_rows('s12', [('CIPHER?', CYAN, None), ('ARGUED', VIO, 0.55)], [
    ('2025, GRESHKO, CRYPTOLOGIA', CYAN, 'The Naibbe cipher turns Latin or Italian into text reproducing some measured properties of the Voynich. A proof of concept, not a solution.', 0.12),
    ('2026, LAYFIELD AND DAVIS', VIO, 'Pages made as four-page units, bound out of order in the 15th century. Their argument, not a settled fact. "We do not know if it is a code."', 0.58)], art_sing)
SC['s13'] = S_rows('s13', [('OPEN', ROSE, None)], [
    ('NO PROOF', ROSE, 'A natural language in an invented script?   A cipher of a known language?', 0.12),
    ('NO PROOF', ROSE, 'A constructed language?   Meaningless text, a hoax?', 0.4),
    ('UNKNOWN', ROSE, 'Who made it, where, and why. Many plants are not confidently matched to real species. What the baths and charts were for.', 0.62)])
SC['s14'] = S_rows('s14', [('THE LEDGER', CYAN, None)], [
    ('DOCUMENTED', MINT, 'Vellum dated 1404 to 1438. In Prague by 1639. Held by Yale.', 0.12),
    ('MEASURED', MINT, 'Language-like word statistics, low letter entropy, two text varieties, several hands.', 0.3),
    ('CLAIMED', VIO, 'Every decipherment so far.', 0.5),
    ('COMPETING', CYAN, 'Hoax, cipher, language: unequal support.', 0.62),
    ('UNKNOWN', ROSE, 'What it says, if anything. Who made it.', 0.78)])
SC['s15'] = S_close('s15', 'not established.', 'not ruled out.', 'NOT ESTABLISHED', 'NOT RULED OUT', 'a credible solution would give coherent text that others can reproduce. the scans are free online at yale.')
SC['s16'] = sc_end

SOURCES = [
    'Beinecke Rare Book and Manuscript Library, Yale: MS 408 catalogue record and digital scans (beinecke.library.yale.edu). Yale News, 31 Oct 2016 (facsimile; materials analysis)',
    'Hodgins et al., University of Arizona radiocarbon dating of the vellum, 2009 (1404-1438). Wikipedia "Voynich manuscript" (provenance and claims summary; read 2026-10-20)',
    'Reddy and Knight 2011, ACL workshop; Bowern and Lindemann 2021, Annual Review of Linguistics 7; Montemurro and Zanette 2013, PLoS ONE; L. Fagin Davis 2020 (scribes)',
    'Manly 1931, Speculum (Newbold); G. Rugg 2003-04; Tucker and Talbert 2013; Gibbs, TLS, 5 Sep 2017; Hauer and Kondrak (TACL); Ardic 2018; Cheshire 2019, Romance Studies',
    'M. Greshko, "The Naibbe cipher", Cryptologia 2025; C. Layfield and L. Fagin Davis, "Singulion structure and the Voynich Manuscript", Digital Medievalist 19 (2026)',
    'Every picture here is drawn for this episode: invented marks stand in for the script. No photographs.']

SCENES = [
    ('s1', None, 'MS 408, Beinecke Library, Yale. Radiocarbon: vellum 1404 to 1438', SC['s1']),
    ('s2', 'the object', 'Beinecke Library, Yale: MS 408 record', SC['s2']),
    ('s3', 'its age', 'University of Arizona radiocarbon study, 2009; ink and paint analyses', SC['s3']),
    ('s4', 'its history', 'Beinecke record; Wikipedia "Voynich manuscript" (provenance)', SC['s4']),
    ('s5', 'the text', 'Reddy and Knight 2011; Montemurro and Zanette 2013. Counts vary by transcription', SC['s5']),
    ('s6', 'a strange text', 'Bowern and Lindemann 2021, Annual Review of Linguistics; Fagin Davis 2020', SC['s6']),
    ('s7', 'the problem', 'Our summary of the studies above', SC['s7']),
    ('s8', 'the solutions, part 1', 'Manly 1931, Speculum; Wikipedia "Voynich manuscript"', SC['s8']),
    ('s9', 'the solutions, part 2', 'Press and journal accounts as summarized on Wikipedia, read 2026-10-20', SC['s9']),
    ('s10', 'why specialists objected', 'L. Fagin Davis on Gibbs and Cheshire (Ars Technica, 2019); M. Pharao Hansen on Tucker and Talbert', SC['s10']),
    ('s11', 'a hoax?', 'G. Rugg 2003-04; Montemurro and Zanette 2013, PLoS ONE', SC['s11']),
    ('s12', 'a cipher? a binding error?', 'Greshko 2025, Cryptologia; Layfield and Davis 2026, Digital Medievalist', SC['s12']),
    ('s13', 'what is open', 'Status as of October 2026', SC['s13']),
    ('s14', None, 'Status as of October 2026', SC['s14']),
    ('s15', None, None, SC['s15']),
    ('s16', None, None, SC['s16']),
]

# part B: subtitles + frame + render framework (from ep2)
def _subs(text):
    out = []
    for s in re.split(r'(?<=[.?!])\s+', text.strip()):
        parts = [s]
        while True:
            nxt = []; changed = False
            for q in parts:
                if len(q) > 96:
                    cs = [m.end() for m in re.finditer(r'[,:] ', q)]
                    if cs:
                        k = min(cs, key=lambda c: abs(c - len(q) / 2)); nxt += [q[:k].strip(), q[k:].strip()]; changed = True; continue
                nxt.append(q)
            parts = nxt
            if not changed: break
        out += parts
    return out
SUBS = {s['id']: _subs(s['text']) for s in TL['segs']}

# ------------------------------------------------------------------ framework
bounds = []
for i, (sid, *_r) in enumerate(SCENES):
    s0 = 0.0 if i == 0 else SEG[sid]['start'] - 0.5
    s1 = TOTAL if i == len(SCENES) - 1 else SEG[SCENES[i + 1][0]]['start'] - 0.5
    bounds.append((s0, s1))
BOUND = {sid: b for (sid, *_r), b in zip(SCENES, bounds)}

def subtitle_at(sid, tt):
    seg = SEG[sid]; subs = SUBS[sid]; rel = tt - seg['start']
    if not subs or rel < -0.1 or rel > seg['dur'] + 0.8: return None
    tot = sum(len(s) for s in subs); acc = 0
    for s in subs:
        acc += len(s); b = acc / tot * seg['dur']
        if rel <= b + (0.8 if s is subs[-1] else 0): return s
    return subs[-1]

def frame(tt):
    cv = Cv()
    for i, (sid, head, src, fn) in enumerate(SCENES):
        s0, s1 = bounds[i]
        if s0 <= tt < s1 or (i == len(SCENES) - 1 and tt >= s0): break
    t = tt - s0; p = clamp01(t / max(0.1, s1 - s0 - 0.6))
    fn(cv, t, p)
    cv.rect((0, 0, 6, H), INK2)
    cv.vtext((14, H - (300 if PORT else 260)), 'STILL UNKNOWN', 'mono', 20, DIM, 0.8)
    mono(cv, 16, 30, f'{i + 1:02d}/{len(SCENES):02d}', 20, DIM, 0.8)
    if head:
        a = ease(t / 0.6)
        f = font('light', SZ['head']); ls = wrap(head, f, HEAD[2] - HEAD[0])
        for k, l in enumerate(ls): cv.text((HEAD[0], HEAD[1] + k * SZ['head'] * 1.1), l, 'light', SZ['head'], TXT, 'la', a)
        cv.rect((HEAD[0], HEAD[1] - 14, HEAD[0] + 44 * a, HEAD[1] - 11), mix(CYAN, BG, a))
    sub = subtitle_at(sid, tt)
    if sub:
        f = font('sans', SZ['cap']); ls = wrap(sub, f, CAP[2] - CAP[0] - 30); n = len(ls)
        lh = SZ['cap'] * 1.28; y0 = CAP[3] - n * lh - 10 if not PORT else CAP[1] + 10
        cv.rect((CAP[0] - 30, y0 - 10, CAP[0] - 30 + 5, y0 + n * lh + 4), CYAN)
        for k, l in enumerate(ls):
            tw = f.getlength(l) / SS
            cv.rect((CAP[0] - 12, y0 + k * lh + 4, CAP[0] + tw + 14, y0 + (k + 1) * lh + 2), mix(BG, INK, 0.72))
            cv.text((CAP[0], y0 + k * lh), l, 'sans', SZ['cap'], TXT, 'la')
    if src:
        a = ease(t / 1.2)
        mono(cv, SRC[0] if PORT else SRC[2], SRC[1], 'SOURCE', 18, CYAN, a, 'la' if PORT else 'ra')
        f = font('mono', SZ['src']); ls = wrap(src, f, SRC[2] - SRC[0])[:3]
        for k, l in enumerate(ls): cv.text((SRC[0] if PORT else SRC[2], SRC[1] + 26 + k * SZ['src'] * 1.25), l, 'mono', SZ['src'], DIM, 'la' if PORT else 'ra', a)
    im = cv.im.reduce(SS)
    fa = min(1.0, t / 0.35, (s1 - tt) / 0.35 if i < len(SCENES) - 1 else (TOTAL - tt) / 1.2)
    if fa < 1.0: im = Image.blend(Image.new('RGB', im.size, BG), im, max(0.0, fa))
    return im

def work(n): return frame(n / FPS).tobytes()

def main():
    if '--still' in sys.argv:
        i = sys.argv.index('--still'); frame(float(sys.argv[i + 1])).save(sys.argv[i + 2]); return
    out = sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else f'video_{ORI}.mp4'
    a, b = 0, int(TOTAL * FPS)
    if '--secs' in sys.argv:
        i = sys.argv.index('--secs'); a, b = int(float(sys.argv[i + 1]) * FPS), int(float(sys.argv[i + 2]) * FPS)
    ff = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                           '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
    pool = Pool(8)
    try:
        for k, buf in enumerate(pool.imap(work, range(a, b), chunksize=4)):
            ff.stdin.write(buf)
            if k % 600 == 0: print(k, '/', b - a, flush=True)
        pool.close(); pool.join()
    except Exception as e:
        print('pool error:', repr(e), flush=True)
    finally:
        try: ff.stdin.close()
        except Exception: pass
        ff.wait(); print('ffmpeg exit', ff.returncode, flush=True)

if __name__ == '__main__': main()
