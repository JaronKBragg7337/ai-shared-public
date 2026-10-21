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

# Still Unknown ep 5 body: "72 seconds from somewhere" (the 1977 Wow! signal). Scenes + sources; framework in su_kit_a/b.
EP = 5

def art_transit(cv, t, R, sid):
    x0, y0, x1, y1 = R; a = ease(t / 1.0)
    cx = (x0 + x1) / 2; sy = y0 + 110 if L else y0 + 50
    # sky strip drifting past a fixed beam
    hh = 70 if L else 40
    cv.rect((x0, sy - hh, x1, sy + hh), mix(INK, BG, a * 0.9))
    rr = random.Random(5)
    ph = (t * 0.09) % 1.0
    for i in range(40):
        sx = x0 + ((rr.random() - ph * 1.0) % 1.0) * (x1 - x0); syy = sy - 60 + rr.random() * 120
        cv.circ((sx, syy), 1.8, mix(TXT, BG, a * 0.6))
    src = x0 + (1.0 - ((t * 0.09) % 1.0)) * (x1 - x0) * 0.0 + (x1 - x0) * (1.0 - ph)
    cv.circ((src, sy), 8, mix(ROSE, BG, a)); cv.ring((src, sy), 14, mix(ROSE, BG, a * 0.5), 2)
    bw = 120 if L else 100
    cv.outline((cx - bw / 2, sy - hh, cx + bw / 2, sy + hh), mix(CYAN, BG, a), 3)
    cv.text((cx, sy - hh - 12), 'fixed beam', 'mono', 18, CYAN, 'ms', a)
    cv.text((x0 + 8, sy + hh + 8), 'the Earth turns; the sky drifts through the beam', 'mono', 18, DIM, 'la', a)
    # intensity as the source crosses
    cy0 = y0 + (360 if L else 215); ch = 150 if L else 65
    cv.line([(x0, cy0), (x1, cy0)], mix(DIM2, BG, a), 2)
    pts = []
    for i in range(101):
        u = i / 100.0; px = x0 + u * (x1 - x0); pts.append((px, cy0 - ch * math.exp(-((u - 0.5) / 0.17) ** 2)))
    cu = (cx + (x1 - x0) / 2 - src) / (x1 - x0) if False else 0
    prog = clamp01(((x1 - src) / (x1 - x0)))
    n = max(2, int(101 * prog))
    cv.line(pts[:n], mix(MINT, BG, a), 4)
    mono(cv, x0, cy0 + 14, '0 s', 18, DIM, a); mono(cv, x1, cy0 + 14, '72 s', 18, DIM, a, 'ra'); mono(cv, cx, cy0 + 14, 'time in view', 18, DIM, a, 'ma')
    mono(cv, x0, cy0 + 44, 'SCHEMATIC, not the real data', 17, DIM, a)

def art_printout(cv, t, R, sid):
    x0, y0, x1, y1 = R; a = ease(t / 1.0)
    chars = [('6', 6), ('E', 14), ('Q', 26), ('U', 30), ('J', 19), ('5', 5)]
    cw = (x1 - x0) / 6.0; base = y0 + (330 if L else 270); hmax = 230 if L else 170
    mono(cv, x0, y0 - 4, 'EHMAN\'S PRINTOUT CODE', 20, CYAN, a)
    for i, (c, v) in enumerate(chars):
        u = ap(t, sid, 0.1 + 0.07 * i, 0.9)
        cx = x0 + cw * (i + 0.5)
        cv.text((cx, y0 + (40 if L else 26)), c, 'monob', 70 if L else 44, TXT if c != 'U' else ROSE, 'ma', u)
        hh = hmax * v / 30.0 * u
        cv.rect((cx - cw * 0.3, base - hh, cx + cw * 0.3, base), mix(ROSE if c == 'U' else CYAN, BG, a * 0.85))
        cv.text((cx, base + 10), str(v), 'mono', 22, DIM, 'ma', u)
    mono(cv, x0, base + 44, 'scale: multiples of the background noise (E = 14, Q = 26, U = 30)', 18, DIM, a)

def art_freq(cv, t, R, sid):
    x0, y0, x1, y1 = R; a = ease(t / 1.0)
    f0, f1 = 1420.30, 1420.80
    ax0, ax1 = x0 + 30, x1 - 30; ay = y0 + (150 if L else 150)
    def X(f): return ax0 + (f - f0) / (f1 - f0) * (ax1 - ax0)
    cv.line([(ax0, ay), (ax1, ay)], mix(DIM2, BG, a), 3)
    for f in (1420.3, 1420.4, 1420.5, 1420.6, 1420.7, 1420.8):
        cv.line([(X(f), ay - 7), (X(f), ay + 7)], mix(DIM, BG, a), 2); cv.text((X(f), ay + 12), f'{f:.1f}', 'mono', 18, DIM, 'ma', a)
    cv.text((ax1, ay + 40), 'MHz', 'mono', 18, DIM, 'ra', a)
    items = [(1420.4058, 'hydrogen line', MINT, 0.05, -30), (1420.4556, '1977 estimate', CYAN, 0.3, -66)]
    if sid == 's11': items.append((1420.726, '2025 preprint', VIO, 0.35, -30))
    for f, nm, col, fr, dy in items:
        u = ap(t, sid, fr, 0.9)
        cv.line([(X(f), ay), (X(f), ay + dy)], mix(col, BG, u), 4); cv.circ((X(f), ay), 7, mix(col, BG, u))
        right = f > 1420.42 and f < 1420.6
        cv.text((X(f) + (10 if right else -10), ay + dy - 28), nm, 'monob', 20, col, 'la' if right else 'ra', u)
    mono(cv, ax0, ay + 70, 'one channel = 10 kHz wide (0.010 MHz)', 18, DIM, a)

def art_horns(cv, t, R, sid):
    x0, y0, x1, y1 = R; a = ease(t / 1.0)
    lx = x0 + 150; lw = x1 - lx - 20
    for k, (nm, yy) in enumerate((('horn A', y0 + 40), ('horn B', y0 + 150))):
        mono(cv, x0, yy + 30, nm, 22, TXT, a)
        cv.line([(lx, yy + 90), (lx + lw, yy + 90)], mix(DIM2, BG, a), 2)
    # observed bump in one horn, expected bump (dashed) in the other
    pts = [(lx + lw * (0.15 + 0.3 * i / 60), y0 + 130 - 80 * math.exp(-((i / 60 - 0.5) / 0.17) ** 2)) for i in range(61)]
    n = max(2, int(61 * ap(t, sid, 0.3, 1.5)))
    cv.line(pts[:n], mix(MINT, BG, a), 4)
    ex = [(lx + lw * (0.55 + 0.3 * i / 60), y0 + 240 - 80 * math.exp(-((i / 60 - 0.5) / 0.17) ** 2)) for i in range(61)]
    ua = ap(t, sid, 0.65, 1.2)
    for i in range(0, 60, 4): cv.line(ex[i:i + 2], mix(ROSE, BG, ua * 0.9), 3)
    cv.text((lx + lw * 0.2, y0 + 70), 'seen', 'monob', 22, MINT, 'la', ap(t, sid, 0.4))
    cv.text((lx + lw * 0.6, y0 + 175), 'expected, not seen', 'monob', 22, ROSE, 'la', ua)
    mono(cv, x0, y0 + 280, 'SCHEMATIC: a steady source should cross both horns', 17, DIM, a)

SC = {}
SC['s1'] = S_title('s1', 5, ('72 seconds', 'from somewhere'), ('72 seconds', 'from', 'somewhere'), 'The 1977 Wow! signal, Big Ear radio telescope, Ohio State',
                   (('DOCUMENTED', MINT, 0.3), ('PROPOSED', VIO, 0.5), ('DISPUTED', ROSE, 0.7), ('UNKNOWN', ROSE, 0.88)), art_transit)
SC['s2'] = S_rows('s2', [('DOCUMENTED', MINT, None)], [
    ('DOCUMENTED', MINT, 'Big Ear, Ohio State University, Delaware, Ohio. A fixed design: tilts in altitude, cannot follow a star.', 0.12),
    ('DOCUMENTED', MINT, 'The Earth\'s rotation carries the sky through the view. Any point takes 72 seconds to cross.', 0.45),
    ('NOTE', CYAN, '72 s is the time a steady source stays in view, not a measured lifetime of a transmitter.', 0.75)], art_transit)
SC['s3'] = S_rows('s3', [('DOCUMENTED', MINT, None), ('NOT A MESSAGE', ROSE, 0.55)], [
    ('DOCUMENTED', MINT, 'Printout numbers = signal strength in multiples of the background noise: 1 to 9, then letters.', 0.1),
    ('DOCUMENTED', MINT, 'The code read 6 E Q U J 5: rose to a peak at U (about 30 on that scale), then fell.', 0.38),
    ('REPORTED', CYAN, 'A smooth rise and fall, as a steady source drifting through the beam would give.', 0.7)], art_printout)
SC['s4'] = S_rows('s4', [('DOCUMENTED', MINT, None), ('FIRST ESTIMATE', CYAN, 0.7)], [
    ('MEASURED', MINT, 'Narrow: inside one 10 kHz channel.', 0.1),
    ('MEASURED', MINT, 'Very near 1420 MHz, the radio frequency of neutral hydrogen. Radio rules reserve this band for astronomy; interference cannot be ruled out entirely.', 0.3),
    ('REPORTED', CYAN, 'First published estimate: 1420.4556 MHz. It is revised in 2025.', 0.72)], art_freq)
SC['s5'] = S_rows('s5', [('DOCUMENTED', MINT, None), ('NOT SETTLED', ROSE, 0.6)], [
    ('DOCUMENTED', MINT, 'Sagittarius, a few degrees from Chi Sagittarii. Two feed horns feeding one switched receiver.', 0.1),
    ('DOCUMENTED', MINT, 'It appeared in one horn, not the other. The records did not preserve which: two possible positions.', 0.4),
    ('PUZZLE', ROSE, 'A source that kept shining at the same strength should have shown up in both.', 0.72)], art_horns)
SC['s6'] = S_table('s6', [('DOCUMENTED', MINT, None), ('NO REPEAT FOUND', ROSE, 0.2)], [
    ('1977-78', 'Ehman and the Big Ear team, following months', MINT, 0.08, 'NOTHING', ROSE),
    ('1987, 1989', 'Robert Gray, META array', MINT, 0.22, 'NOTHING', ROSE),
    ('mid 1990s', 'Gray, Very Large Array: more sensitive than Big Ear', MINT, 0.38, 'NOTHING', ROSE),
    ('1998-99', 'Gray and Ellingsen: six long sessions on another dish', MINT, 0.55, 'NOTHING SIMILAR', ROSE),
    ('2022', 'Breakthrough Listen: that region searched', MINT, 0.76, 'NO CANDIDATES', ROSE)])
SC['s7'] = S_rows('s7', [('PROPOSED', VIO, None)], [
    ('NEAR EARTH', CYAN, 'Ehman suggested space debris in 1994; he later judged that much less likely. No specific terrestrial source has been shown.', 0.12),
    ('NATURAL, DISTANT', VIO, 'A natural source far away. Several versions proposed (next scenes).', 0.45),
    ('A TRANSMISSION', ROSE, 'Some have proposed another civilization. The evidence for it is the signal itself, and nothing else.', 0.68)])
SC['s8'] = S_rows('s8', [('PROPOSED', VIO, None), ('PAPERS: 2017', CYAN, 0.5)], [
    ('PARIS, 2017', VIO, 'Hydrogen cloud around a comet. Antonio Paris, then at St. Petersburg College, Florida.', 0.1),
    ('PARIS, 2017', VIO, 'Comets 266P/Christensen and 335P/Gibbs, which he said were in that part of the sky in 1977.', 0.4),
    ('REPORTED', CYAN, 'He reported a signal near the hydrogen frequency while observing 266P in 2017.', 0.72)])
SC['s9'] = S_rows('s9', [('DISPUTED', ROSE, None)], [
    ('OBJECTION', ROSE, 'Critics, including people from the original Big Ear team: the comets were not in the beam at the right time.', 0.1),
    ('OBJECTION', ROSE, 'Comet hydrogen is not known to give a signal that narrow and that strong.', 0.4),
    ('OBJECTION', ROSE, 'It does not explain why only one horn saw it.', 0.62),
    ('STATUS', CYAN, 'A proposal, not a finding.', 0.82)])
SC['s10'] = S_rows('s10', [('NEWER WORK', CYAN, None)], [
    ('CALEBALLERO 2022'.replace('CALEBALLERO', 'CABALLERO'), CYAN, 'Three Sun-like stars inside the possible patch, the best known about 1,800 light years away: places worth a look. A candidate star is not evidence of a transmitter.', 0.1),
    ('MENDEZ ET AL., 2024', VIO, 'Hypothesis: a natural flare, such as a magnetar, lights a cold hydrogen cloud into a narrow beam: a natural maser. Using Arecibo. No flare tied to 1977.', 0.55)])
SC['s11'] = S_rows('s11', [('PREPRINT 2025', VIO, None), ('NOT PEER REVIEWED, OCT 2026', ROSE, 0.3)], [
    ('ARCHIVE', CYAN, '75,000+ pages of old records digitized. Found a clock offset and an inverted channel order in the 1977 analysis.', 0.08),
    ('REVISED', VIO, 'Frequency 1420.726 MHz (was 1420.4556). Peak more than 250 Jy, higher than earlier estimates.', 0.4),
    ('THEIR CONCLUSION', CYAN, 'A natural hydrogen source most likely. Their results do not show an extraterrestrial signal.', 0.7)], art_freq)
SC['s12'] = S_rows('s12', [('DISPUTED', ROSE, None)], [
    ('CAUTION', ROSE, 'Gerry Harp, who worked on the Allen Telescope Array: the signal failed even simple tests used to exclude interference.', 0.12),
    ('CAUTION', ROSE, 'Others: failing to repeat shows the event was rare, not what caused it.', 0.45),
    ('STATUS', CYAN, 'One event, no repeat: every explanation is a hypothesis.', 0.72)])
SC['s13'] = S_rows('s13', [('WHAT WOULD SETTLE IT', MINT, None)], [
    ('1', MINT, 'A repeat from the same patch of sky.', 0.12),
    ('2', MINT, 'Independent checks of the 1977 numbers by teams other than the one that reanalyzed them.', 0.35),
    ('3', MINT, 'Searching the Ohio archive (40,000+ narrowband events logged) for other one-off signals like it. Most of it is unexplored.', 0.6)])
SC['s14'] = S_rows('s14', [('THE LEDGER', CYAN, None)], [
    ('DOCUMENTED', MINT, 'A narrow signal near the hydrogen frequency, over the 72 s a source takes to cross the view, peak about 30 on the printout scale.', 0.1),
    ('DOCUMENTED', MINT, 'Repeated searches found no repeat.', 0.3),
    ('DISPUTED', ROSE, 'The comet idea. The meaning of the reanalysis.', 0.42),
    ('PROPOSED', VIO, 'A natural flare from a hydrogen cloud.', 0.56),
    ('CLAIMED', VIO, 'A message from another civilization: no evidence beyond the signal itself.', 0.68),
    ('UNKNOWN', ROSE, 'What it was.', 0.85)], size=(32 if L else 28))
SC['s15'] = S_close('s15', 'not established.', 'not ruled out.', 'NOT ESTABLISHED', 'NOT RULED OUT', 'one signal, seen once. a natural source fits best to one group; others are not convinced. an artificial origin is neither shown nor excluded.')
SC['s16'] = sc_end

SOURCES = [
    'Wikipedia "Wow! signal" (read 2026-10-20). Ohio State Big Ear archive (bigear.org): J. Ehman on the 6EQUJ5 printout; R. Gray and S. Ellingsen, search paper (1998-99 sessions)',
    'A. Paris, arXiv:1706.03259 (observations of 266P) and arXiv:1706.04642 (comet proposal), 2017',
    'A. Caballero, International Journal of Astrobiology, 2022 (candidate stars). Breakthrough Listen 2022 search, as summarized in Wikipedia',
    'A. Mendez et al., arXiv:2408.08513 (2024, maser-flare hypothesis); "Arecibo Wow! II", arXiv:2508.10657 (2025 preprint, not peer reviewed when checked)',
    'A. Mendez, R. Dixon, R. Childers, "The Ohio SETI Program: the last decades", arXiv:2606.11102 (2026); G. Harp comment, centauri-dreams.org, 15 Apr 2025',
    'All pictures are schematic drawings made for this episode, not data plots. No photographs.']

SCENES = [
    ('s1', None, 'Wow! signal, 15 Aug 1977, Big Ear, Ohio State University', SC['s1']),
    ('s2', 'the telescope', 'Wikipedia "Wow! signal"; Ohio State Big Ear archive', SC['s2']),
    ('s3', 'six, e, q, u, j, five', 'J. Ehman\'s explanation of the printout, bigear.org', SC['s3']),
    ('s4', 'what was measured', 'Wikipedia "Wow! signal"; Ohio State Big Ear archive', SC['s4']),
    ('s5', 'where, and the puzzle', 'Gray and Ellingsen; Wikipedia "Wow! signal"', SC['s5']),
    ('s6', 'looking again', 'Gray and Ellingsen; Wikipedia "Wow! signal" (searches 1977 to 2022)', SC['s6']),
    ('s7', 'what could it be?', 'Ehman, as summarized in Wikipedia "Wow! signal"', SC['s7']),
    ('s8', 'the comet idea', 'A. Paris 2017, arXiv:1706.03259 and 1706.04642', SC['s8']),
    ('s9', 'why it was disputed', 'Wikipedia "Wow! signal" (critics, incl. Big Ear team members)', SC['s9']),
    ('s10', 'newer work', 'Caballero 2022; Mendez et al. 2024 (arXiv:2408.08513)', SC['s10']),
    ('s11', 'the 2025 reanalysis', 'Mendez et al., arXiv:2508.10657 (preprint)', SC['s11']),
    ('s12', 'caution', 'G. Harp via centauri-dreams.org, 2025', SC['s12']),
    ('s13', 'what would settle it', 'Mendez, Dixon, Childers, arXiv:2606.11102 (40,000+ events)', SC['s13']),
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
