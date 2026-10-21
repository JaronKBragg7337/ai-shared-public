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
import re, os
L = not PORT
BDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'blender')

# ------------------------------------------------------------------ helpers
def count(v, t, t0, dur=1.2, fmt='{:,.0f}'): return fmt.format(v * ease((t - t0) / dur))
def poly(cv, pts, fill): cv.d.polygon([cv.P(p) for p in pts], fill=fill)
def F(sid, f): return SEG[sid]['start'] + f * SEG[sid]['dur'] - BOUND[sid][0]
def ap(t, sid, f, d=0.8): return ease((t - F(sid, f)) / d)

def night(cv, tt, dim=0.5):
    for (x, y, r, b, ph) in STARS:
        tw = 0.65 + 0.35 * math.sin(tt * 1.1 + ph)
        cv.circ((x * W, y * H), r * 0.9, mix(TXT, BG, b * tw * dim))

def bshot(cv, name, t, box, n, fps=24, a=1.0):
    """paste a looping Blender frame (rendered 1280x720) into box (x, y, w, h)."""
    x, y, w, h = box
    idx = int(t * fps) % n + 1
    p = os.path.join(BDIR, name, f'f{idx:04d}.png')
    if not os.path.exists(p): cv.rect((x, y, x + w, y + h), INK); return
    im = Image.open(p).convert('RGB').resize((int(w * SS), int(h * SS)), Image.BILINEAR)
    if a < 1: im = Image.blend(Image.new('RGB', im.size, BG), im, a)
    cv.im.paste(im, (int(x * SS), int(y * SS)))
    cv.outline((x, y, x + w, y + h), mix(INK2, BG, a), 2)

def fact_rows(cv, t, sid, x, y, rows, w, step, big_sz=50, small=26, col=CYAN):
    """rows: (big text, small caption, fraction).  big text in light, caption in sans dim"""
    for i, (b, s, f) in enumerate(rows):
        a = ap(t, sid, f)
        if a <= 0: continue
        yy = y + i * step
        cv.rect((x, yy + 4, x + 5, yy + step - 22), mix(col, BG, a))
        cv.text((x + 22, yy), b, 'light', big_sz, TXT, 'la', a)
        cv.para(x + 22, yy + big_sz * 1.2, s, 'sans', small, DIM, w - 30, 1.2, 'l', a)

def shot_scene(cv, t, sid, name, n, rows, ilabel, big_sz=50):
    night(cv, t, 0.35)
    x0, y0, x1, y1 = CONT
    if L:
        bw = 1084; bh = 610
        bshot(cv, name, t, (x0, y0, bw, bh), n, a=ease(t / 0.6))
        tag(cv, x0 + 14, y0 + 14, ilabel, CYAN, ease(t / 0.8), 20)
        fact_rows(cv, t, sid, x0 + bw + 50, y0 + 20, rows, x1 - (x0 + bw + 50), 200, big_sz, 26)
    else:
        bw = x1 - x0; bh = int(bw * 9 / 16)
        bshot(cv, name, t, (x0, y0, bw, bh), n, a=ease(t / 0.6))
        tag(cv, x0 + 14, y0 + 14, ilabel, CYAN, ease(t / 0.8), 20)
        fact_rows(cv, t, sid, x0 + 10, y0 + bh + 40, rows, bw - 20, 100, 44, 24)

def vibe_icon(cv, cx, by, s, t, a=1.0):
    stone_c = INK2
    cv.rect((cx - 170 * s, by - 90 * s, cx + 170 * s, by), mix(stone_c, BG, a)); cv.outline((cx - 170 * s, by - 90 * s, cx + 170 * s, by), mix(DIM, BG, a * 0.8), 2)
    j = math.sin(t * 50) * 3 * s
    tx0, tx1 = cx - 36 * s, cx + 36 * s; ty = by - 90 * s - 5 * s + j
    cv.rect((tx0, ty - 150 * s, tx1, ty), mix(VIO, BG, a))
    cv.rect((tx0 - 6, ty, tx1 + 6, ty + 18 * s), mix(CYAN, BG, a * 0.7))
    for k in range(4):
        u = ((t * 0.9 + k / 4) % 1.0)
        cv.ring((cx, ty - 150 * s), 30 * s + u * 190 * s, mix(CYAN, BG, a * (1 - u) * 0.7), 2)

def stone_slab(cv, x0, y0, x1, y1, a=1.0):
    cv.rect((x0, y0, x1, y1), mix(INK2, BG, a)); cv.outline((x0, y0, x1, y1), mix(DIM, BG, a * 0.8), 2)

# ------------------------------------------------------------------ scenes
def sc_title(cv, t, p):
    night(cv, t, 0.9)
    y0 = 300 if PORT else 250
    mono(cv, HEAD[0], y0, 'HEARTBEAT TV  /  CH 10  /  STILL UNKNOWN  /  EP 03', 28 if PORT else 26, CYAN, ease(t / 1.0))
    sz = 110 if PORT else 128
    lines = ('can vibration', 'cut stone?')
    for k, l in enumerate(lines): big(cv, HEAD[0], y0 + 60 + k * sz * 1.05, l, sz, TXT, ease((t - 0.3 - k * 0.25) / 1.2))
    yy = y0 + 60 + len(lines) * sz * 1.05 + 40
    mono(cv, HEAD[0], yy, 'engineering that is published, claims that are not', 24, DIM, ease((t - 1.5) / 1.0))
    ty = yy + 70
    x = HEAD[0]
    for i, (lab, col, f) in enumerate((('DOCUMENTED', MINT, 0.30), ('CLAIMED', VIO, 0.55), ('NOT ESTABLISHED', ROSE, 0.75))):
        aa = ap(t, 's1', f, 0.8)
        if PORT: tag(cv, HEAD[0], ty + i * 62, lab, col, aa)
        else:
            w = tag(cv, x, ty, lab, col, aa); x += (w if w > 0 else 0) + 20
    if L: vibe_icon(cv, 1560, 860, 1.5, t, ease(t / 1.5))
    else: vibe_icon(cv, W / 2, 1330, 1.3, t, ease(t / 1.5))

def sc_usm(cv, t, p):
    shot_scene(cv, t, 's2', 'usm', 48, [('typically 20-40 kHz', 'how often the tool vibrates, per second', 0.25),
                                       ('a tiny stroke', 'micrometres up to about 0.1 mm', 0.5),
                                       ('grit + water', 'silicon carbide or boron carbide slurry', 0.7)], 'ILLUSTRATION  /  SLOWED DOWN')

def sc_grit(cv, t, p):
    night(cv, t, 0.35)
    x0, y0, x1, y1 = CONT
    if L: dx0, dy0, dw, dh = x0, y0, 1100, 610
    else: dx0, dy0, dw, dh = x0, y0, x1 - x0, 620
    cv.rect((dx0, dy0, dx0 + dw, dy0 + dh), mix(INK, BG, 0.9))
    tag(cv, dx0 + 14, dy0 + 14, 'ILLUSTRATION  /  NOT TO SCALE', CYAN, ease(t / 0.8), 20)
    sy = dy0 + dh * 0.62                        # stone surface
    cxm = dx0 + dw * (0.66 if L else 0.72)
    depth = 26 * ease(t / 14.0) + 6
    cw = dw * (0.26 if L else 0.24)
    # stone body with a cavity
    cv.rect((dx0, sy, dx0 + dw, dy0 + dh), mix(INK2, BG, 1.0))
    cv.rect((cxm - cw / 2, sy, cxm + cw / 2, sy + depth), mix(INK, BG, 1.0))
    hline(cv, dx0, cxm - cw / 2, sy, DIM, 0.9, 2); hline(cv, cxm + cw / 2, dx0 + dw, sy, DIM, 0.9, 2)
    cv.line([(cxm - cw / 2, sy), (cxm - cw / 2, sy + depth), (cxm + cw / 2, sy + depth), (cxm + cw / 2, sy)], mix(DIM, BG, 0.9), 2)
    ph = t * 2 * math.pi * 1.1
    z = (0.5 - 0.5 * math.cos(ph))              # 0 = tool at the top of its stroke, 1 = bottom
    gap_top = sy - 120; gap_bot = sy + depth - 34
    ty = gap_top + (gap_bot - gap_top) * z * 0.5 + 0
    tool_bot = sy + depth - 150 + 110 * z
    cv.rect((cxm - cw / 2 + 8, tool_bot - 260, cxm + cw / 2 - 8, tool_bot), (84, 94, 120)); cv.outline((cxm - cw / 2 + 8, tool_bot - 260, cxm + cw / 2 - 8, tool_bot), mix(TXT, BG, 0.6), 2)
    # grit grains between tool and stone floor
    rngl = random.Random(5)
    floor = sy + depth
    for i in range(22):
        gx = cxm - cw / 2 + 26 + (cw - 52) * (i + 0.5) / 22 + rngl.uniform(-6, 6)
        off = rngl.uniform(0, 0.5)
        zz = (0.5 - 0.5 * math.cos(ph + off * 2.0))
        gy = floor - 12 - max(0, floor - tool_bot - 28) * (0.5 - 0.5 * math.cos(ph + off * 2.0)) ** 1.5
        cv.circ((gx, gy), 9, mix(CYAN, BG, 0.95))
        # chips leaving on impacts
        u = (t * 1.1 + off) % 1.0
        if u < 0.5:
            for k in range(2):
                ang = -1.1 + k * 2.2 + rngl.uniform(-0.3, 0.3)
                cv.circ((gx + math.cos(ang) * u * 90, floor - 10 + math.sin(ang) * u * 90 * 0.6 + 140 * u * u), 3.2 * (1 - 2 * u) + 0.5, mix(TXT, BG, 0.8 * (1 - 2 * u)))
    # labels
    a1 = ap(t, 's3', 0.22); a2 = ap(t, 's3', 0.45); a3 = ap(t, 's3', 0.72)
    lx = dx0 + dw - 20
    cv.text((dx0 + 24, tool_bot - 150) if False else (dx0 + 24, dy0 + 80), 'steel tool: vibrates, shapes', 'mono', 26, TXT, 'la', a1)
    cv.text((dx0 + 24, dy0 + 118), 'ordinary steel, softer than the work', 'mono', 22, DIM, 'la', a1)
    cv.text((dx0 + 24, dy0 + 170), 'loose grit: most of the cutting', 'mono', 26, CYAN, 'la', a2)
    cv.text((dx0 + 24, dy0 + 208), 'hard, hit again and again', 'mono', 22, DIM, 'la', a2)
    cv.text((dx0 + 24, dy0 + 260), 'each hit chips off a speck', 'mono', 26, MINT, 'la', a3)
    cv.text((dx0 + 24, dy0 + 298), 'millions of specks = a hole', 'mono', 22, DIM, 'la', a3)
    if L:
        fact_rows(cv, t, 's3', x0 + 1150, y0 + 40, [('the loose grit', 'does most of the cutting; the tool supplies and shapes the impacts', 0.3), ('brittle', 'hard, brittle work chips; it does not melt or tear', 0.6)], x1 - (x0 + 1150), 200, 56, 26)
    else:
        fact_rows(cv, t, 's3', x0 + 10, y0 + dh + 30, [('the loose grit does most of the cutting', 'brittle work chips; it does not melt or tear', 0.3)], x1 - x0 - 20, 140, 44, 26)

def sc_history(cv, t, p):
    night(cv, t, 0.3)
    x0, y0, x1, y1 = CONT
    evs = [('1927', 'Wood and Loomis credited with first discussing it', 0.20, MINT),
           ('1945', 'British patent application GB 602,801, later tied to Balamuth', 0.38, MINT),
           ('1952', 'US 2,580,716 to Balamuth listed as issued', 0.52, MINT),
           ('1950s', 'machines appear (early to mid decade)', 0.66, VIO),
           ('1998', 'Thoe, Aspinwall & Wise review the field', 0.80, MINT)]
    tag(cv, x0, y0, 'DOCUMENTED', MINT, ease(t / 0.8), 22)
    if L:
        ly = y0 + 300; n = len(evs); step = (x1 - x0 - 260) / (n - 1)
        cv.line([(x0, ly), (x1 - 80, ly)], INK2, 3)
        for i, (yr, txt, f, col) in enumerate(evs):
            a = ap(t, 's4', f); px = x0 + 20 + i * step
            if a <= 0: continue
            cv.circ((px, ly), 11, mix(col, BG, a)); big(cv, px - 6, ly - 130, yr, 64, TXT, a)
            cv.para(px - 6, ly + 36, txt, 'sans', 28, TXT, step - 30, 1.25, 'l', a)
        note = 'nobody\'s personal discovery: decades of engineering'
        mono(cv, x0, y0 + 570, note, 26, CYAN, ap(t, 's4', 0.88))
    else:
        lx = x0 + 40; n = len(evs); step = 150
        cv.line([(lx, y0 + 70), (lx, y0 + 70 + step * (n - 1) + 20)], INK2, 3)
        for i, (yr, txt, f, col) in enumerate(evs):
            a = ap(t, 's4', f); py = y0 + 70 + i * step
            if a <= 0: continue
            cv.circ((lx, py), 11, mix(col, BG, a)); big(cv, lx + 40, py - 34, yr, 56, TXT, a)
            cv.para(lx + 40, py + 34, txt, 'sans', 26, TXT, x1 - lx - 60, 1.2, 'l', a)
        mono(cv, x0, y0 + 70 + step * n + 10, 'nobody\'s personal discovery', 24, CYAN, ap(t, 's4', 0.88))

def sc_limits(cv, t, p):
    night(cv, t, 0.3)
    x0, y0, x1, y1 = CONT
    good = ['glass', 'ceramics', 'gemstones', 'stone']
    bad = ['ductile metals (they deform)', 'deep holes (slurry cannot reach)', 'large blocks', 'slow: micrometres at a time']
    cw = (x1 - x0 - 60) / 2 if L else (x1 - x0)
    def col(cx, cy, title, items, tcol, f0):
        a = ap(t, 's5', f0)
        tag(cv, cx, cy, title, tcol, a, 24)
        for i, it in enumerate(items):
            aa = ap(t, 's5', f0 + 0.05 + i * 0.07)
            big(cv, cx, cy + 70 + i * 82, it, 50 if L else 46, TXT, aa)
    if L:
        col(x0, y0 + 10, 'WORKS WELL ON', good, MINT, 0.12); col(x0 + cw + 60, y0 + 10, 'POOR OR SLOW', bad, ROSE, 0.45)
        mono(cv, x0, y0 + 480, 'holes and cavities, not documented for quarrying blocks. needs power + a transducer', 24, CYAN, ap(t, 's5', 0.78))
    else:
        col(x0, y0, 'WORKS WELL ON', good, MINT, 0.12); col(x0, y0 + 430, 'POOR OR SLOW', bad, ROSE, 0.45)
        cv.para(x0, y0 + 830, 'holes and cavities; needs power + a transducer', 'mono', 22, CYAN, x1 - x0, 1.25, 'l', ap(t, 's5', 0.78))

def sc_aswan(cv, t, p):
    shot_scene(cv, t, 's6', 'saw', 72, [('1999, Aswan', 'Denys Stocks tests copper and sand on quarry granite', 0.35),
                                       ('1.8 m copper blade', 'about 15 cm wide, 6 mm thick', 0.52),
                                       ('quartz sand, 2 people', 'pulled back and forth', 0.72)], 'ILLUSTRATION  /  NOT TO SCALE', 46)

def sc_rate(cv, t, p):
    night(cv, t, 0.3)
    x0, y0, x1, y1 = CONT
    tag(cv, x0, y0, 'PUBLISHED EXPERIMENT', MINT, ease(t / 0.8), 22)
    a = ap(t, 's7', 0.10)
    v = count(12, t, F('s7', 0.10), 1.4)
    if L:
        big(cv, x0, y0 + 50, v, 180, AMBER if False else CYAN, a); mono(cv, x0 + 10, y0 + 260, 'cm3 of granite per hour, dry or wet', 30, TXT, a)
        rows = [('experience could double it', 'Stocks\'s suggestion, not a measurement', 0.45), ('copper wore away too', 'the sand cuts; the soft copper carries it', 0.62),
                ('shows what can work', 'not what the Egyptians did', 0.80)]
        fact_rows(cv, t, 's7', x0, y0 + 330, rows, 900, 90, 38, 24)
        # cube
        cx, cy, s = 1450, y0 + 330, 150
        ac = ap(t, 's7', 0.35)
        pts = lambda dx, dy: (cx + dx, cy + dy)
        top = [pts(0, -s * .5), pts(s * .87, -s * .5 + s * .5), pts(0, s * .5 - s * .5 + s * .5), pts(-s * .87, -s * .5 + s * .5)]
        top = [pts(0, 0), pts(s * .87, s * .5), pts(0, s), pts(-s * .87, s * .5)]
        left = [pts(-s * .87, s * .5), pts(0, s), pts(0, s * 2), pts(-s * .87, s * 1.5)]
        right = [pts(s * .87, s * .5), pts(0, s), pts(0, s * 2), pts(s * .87, s * 1.5)]
        poly(cv, top, mix(INK2, BG, ac)); poly(cv, left, mix(INK, BG, ac)); poly(cv, right, mix(VIO, BG, ac * 0.6))
        for q in (top, left, right): cv.line(q + [q[0]], mix(TXT, BG, ac * 0.8), 2)
        mono(cv, cx, cy + s * 2 + 24, '= a cube about 2.3 cm on a side', 22, TXT, ac, 'ma'); mono(cv, cx, cy + s * 2 + 54, 'our arithmetic: 12^(1/3)', 20, DIM, ac, 'ma')
    else:
        big(cv, x0, y0 + 10, v, 150, CYAN, a); mono(cv, x0 + 10, y0 + 190, 'cm3 of granite per hour', 28, TXT, a); mono(cv, x0 + 10, y0 + 226, 'dry or wet', 24, DIM, a)
        rows = [('experience could double it', 'Stocks\'s suggestion', 0.45), ('copper wore away too', 'sand cuts; soft copper carries it', 0.62), ('shows what can work', 'not what the Egyptians did', 0.80)]
        fact_rows(cv, t, 's7', x0, y0 + 300, rows, x1 - x0, 130, 42, 26)
        mono(cv, x0, y0 + 720, '12 cm3 = a cube about 2.3 cm on a side (our arithmetic)', 20, DIM, ap(t, 's7', 0.4))

def sc_family(cv, t, p):
    night(cv, t, 0.3)
    x0, y0, x1, y1 = CONT
    tag(cv, x0, y0, 'ILLUSTRATION  /  OUR ESTIMATE', CYAN, ease(t / 0.8), 20)
    lw = x1 - x0 - 40
    # lane A: copper + sand by hand
    ya = y0 + (110 if L else 100); yb = ya + (250 if L else 330)
    aA = ap(t, 's8', 0.06); aB = ap(t, 's8', 0.30)
    cv.text((x0, ya - 6), 'copper + sand, by hand', 'sansb', 32, TXT, 'la', aA)
    cv.text((x0, ya + 40), 'about 1-2 strokes a second', 'mono', 24, DIM, 'la', aA)
    trackx0 = x0 + 20; trackx1 = x1 - 20; ty = ya + 110
    cv.line([(trackx0, ty + 30), (trackx1, ty + 30)], mix(INK2, BG, aA), 4)
    pos = 0.5 - 0.5 * math.cos(t * 2 * math.pi * 1.5)
    bx = trackx0 + (trackx1 - trackx0 - 160) * pos
    cv.rect((bx, ty, bx + 160, ty + 24), mix(AMBER if False else ROSE, BG, aA))
    # lane B: ultrasonic
    cv.text((x0, yb - 6), 'ultrasonic machining', 'sansb', 32, TXT, 'la', aB)
    cv.text((x0, yb + 40), '20,000+ strokes a second, tiny strokes (drawn as a blur)', 'mono', 24, DIM, 'la', aB)
    ty = yb + 110
    cv.line([(trackx0, ty + 30), (trackx1, ty + 30)], mix(INK2, BG, aB), 4)
    cx = (trackx0 + trackx1) / 2
    for k in range(6):
        off = math.sin(t * 90 + k * 1.3) * 22
        cv.rect((cx - 80 + off, ty + 2 * k - 6, cx + 80 + off, ty + 2 * k + 18), mix(CYAN, BG, aB * 0.30))
    cv.rect((cx - 80, ty, cx + 80, ty + 24), mix(CYAN, BG, aB * 0.55))
    # ratio
    ar = ap(t, 's8', 0.62)
    if L: big(cv, x1 - 560, y0 + 370, '~ 10,000 x', 110, TXT, ar); mono(cv, x1 - 556, y0 + 500, 'the vibration rate, not cutting speed (our arithmetic)', 22, CYAN, ar)
    else:
        big(cv, x0, yb + 220, '~ 10,000 x', 100, TXT, ar); mono(cv, x0 + 4, yb + 340, 'the vibration rate (our arithmetic)', 24, CYAN, ar)

def sc_dunn(cv, t, p):
    night(cv, t, 0.3)
    x0, y0, x1, y1 = CONT
    tag(cv, x0, y0, 'CLAIMED', VIO, ease(t / 0.8), 22); tag(cv, x0 + 190, y0, 'NOT ESTABLISHED', ROSE, ap(t, 's9', 0.75), 22)
    mono(cv, x0 + (480 if L else 0), y0 + (6 if L else 56), 'C. Dunn, "Advanced Machining in Ancient Egypt", Analog, Aug 1984', 20 if L else 18, DIM, ease(t / 1.0))
    bw = 640 if L else 600
    yy = y0 + (90 if L else 120)
    rows = [('granite core, spiral cut (Petrie)', 0.100, '0.100 in per turn', 0.28, VIO), ('modern diamond drill (figure given to Dunn, 1983)', 0.0002, '0.0002 in per turn', 0.48, CYAN)]
    for i, (lab, val, txt, f, col) in enumerate(rows):
        a = ap(t, 's9', f); y = yy + i * 150
        cv.text((x0, y), lab, 'sans', 28 if L else 26, TXT, 'la', a)
        u = ease((t - F('s9', f) - 0.2) / 1.0)
        w = max(3, bw * (val / 0.1) * u)
        cv.rect((x0, y + 46, x0 + w, y + 86), mix(col, BG, a)); mono(cv, x0 + w + 16, y + 52, txt, 26, col, a)
    ar = ap(t, 's9', 0.62)
    big(cv, x0, yy + 320, 'ratio about 500 x', 70 if L else 64, TXT, ar)
    mono(cv, x0, yy + 320 + (96 if L else 90), 'Dunn infers ultrasonic drilling', 26, VIO, ar)
    a2 = ap(t, 's9', 0.78)
    if L:
        cv.rect((x0 + 980, y0 + 90, x0 + 984, y1 - 20), mix(INK2, BG, a2))
        cv.text((x0 + 1020, y0 + 90), 'the other side', 'sansb', 32, TXT, 'la', a2)
        cv.para(x0 + 1020, y0 + 140, 'Experimental archaeologists have drilled granite with copper tube and sand (Stocks).', 'sans', 28, TXT, 640, 1.25, 'l', a2)
        cv.para(x0 + 1020, y0 + 300, 'In the literature we read: no ancient transducer, power source or text describing one.', 'sans', 28, ROSE, 640, 1.25, 'l', ap(t, 's9', 0.88))
    else:
        cv.para(x0, yy + 520, 'Experimental archaeologists drilled granite with copper tube + sand (Stocks). No ancient transducer, power source or text in the literature we read.', 'sans', 26, TXT, x1 - x0, 1.25, 'l', a2)

def sc_sound(cv, t, p):
    night(cv, t, 0.3)
    x0, y0, x1, y1 = CONT
    tag(cv, x0, y0, 'CLAIMED', VIO, ease(t / 0.8), 22); tag(cv, x0 + 190, y0, 'NOT ESTABLISHED', ROSE, ap(t, 's10', 0.25), 22)
    # standing-wave diagram
    if L: dx0, dy0, dw, dh = x0, y0 + 80, 940, 330
    else: dx0, dy0, dw, dh = x0, y0 + 80, x1 - x0, 300
    cv.rect((dx0, dy0, dx0 + dw, dy0 + 26), mix(VIO, BG, 0.9)); cv.rect((dx0, dy0 + dh - 26, dx0 + dw, dy0 + dh), mix(DIM, BG, 0.9))
    cv.text((dx0 + 10, dy0 + 30), 'transducer', 'mono', 20, DIM, 'la'); cv.text((dx0 + 10, dy0 + dh - 54), 'reflector', 'mono', 20, DIM, 'la')
    mid = dy0 + dh / 2; amp = 70 * ease(t / 1.2)
    for k in range(2):
        pts = []
        for i in range(0, 201):
            x = dx0 + 40 + (dw - 80) * i / 200
            pts.append((x, mid + math.sin(math.pi * 2 * i / 200 * 4) * 0))
        cv.line([(dx0 + 40, mid), (dx0 + dw - 40, mid)], mix(INK2, BG, 0.9), 1)
    # vertical standing wave (pressure envelope) between the plates
    for i in range(9):
        px = dx0 + 60 + (dw - 120) * i / 8
        h = amp * abs(math.cos(math.pi * i / 4 * 1.0)) * math.sin(t * 9 + 0)
        cv.line([(px, mid - h), (px, mid + h)], mix(CYAN, BG, 0.6), 3)
    bx = dx0 + 60 + (dw - 120) * 4 / 8
    ab = ap(t, 's10', 0.40)
    cv.circ((bx, mid), 12, mix(TXT, BG, ab))
    mono(cv, bx + 24, mid - 128, '0.6 g foam ball, 30 mm', 22, TXT, ab); mono(cv, bx + 24, mid - 100, 'one published far-field demonstration', 20, DIM, ab)
    a2 = ap(t, 's10', 0.62)
    if L: tx, ty, tw = x0 + 1000, y0 + 80, x1 - (x0 + 1000)
    else: tx, ty, tw = x0, dy0 + dh + 30, x1 - x0
    cv.text((tx, ty), 'close range (near field)', 'sansb', 30, TXT, 'la', a2)
    cv.para(tx, ty + 44, 'has carried several kilograms, but only tens to hundreds of micrometres above the surface', 'sans', 26, DIM, tw, 1.2, 'l', a2)
    a3 = ap(t, 's10', 0.20)
    if L:
        cv.para(x0, y0 + 460, 'a modern story, usually set in Tibet: drums and trumpets float stones. No film, measurement or physical trace found that we could check. The same idea met Coral Castle in episode 10.2.', 'sans', 28, TXT, 940, 1.25, 'l', a3)
    else:
        cv.para(x0, ty + 190, 'a modern story, usually set in Tibet: drums and trumpets float stones. No film, measurement or trace we could check. Same idea at Coral Castle, ep 10.2.', 'sans', 26, TXT, tw, 1.25, 'l', a3)

def sc_arith(cv, t, p):
    night(cv, t, 0.3)
    x0, y0, x1, y1 = CONT
    tag(cv, x0, y0, 'OUR ARITHMETIC  /  ROUGH', CYAN, ease(t / 0.8), 22)
    steps = [('block: about 2.3 t (estimate)', 'weight  =  22.6 kN', 0.12, TXT),
             ('hold it under 1 m2, perfect reflection', 'pressure 22.6 kPa = 2I/c  ->  I = 3.9 MW/m2', 0.30, TXT),
             ('sound pressure needed', 'about 40 kPa rms  =  about 186 dB', 0.48, MINT),
             ('air\'s own limit', 'about 191-194 dB: the low-pressure half reaches vacuum', 0.64, ROSE),
             ('mass ratio to the foam ball', '2.3 t / 0.6 g  =  about 3.8 million x', 0.80, VIO)]
    sw = 980 if L else (x1 - x0)
    for i, (a_, b_, f, col) in enumerate(steps):
        a = ap(t, 's11', f); yy = y0 + 60 + i * (105 if L else 140)
        cv.rect((x0, yy + 2, x0 + 5, yy + (84 if L else 120)), mix(col, BG, a))
        cv.text((x0 + 22, yy), a_, 'sansb', 28 if L else 26, TXT, 'la', a)
        if L: mono(cv, x0 + 22, yy + 40, b_, 26, col, a)
        else: cv.para(x0 + 22, yy + 36, b_, 'mono', 21, col, sw - 30, 1.25, 'l', a)
    if L:
        # dB gauge
        gx = x0 + 1180; gy0 = y0 + 40; gy1 = y1 - 30
        def Y(db): return gy1 - (db - 120) / 80 * (gy1 - gy0)
        ag = ap(t, 's11', 0.45)
        cv.rect((gx, gy0, gx + 10, gy1), mix(INK2, BG, ag))
        for db, lab, col in ((194, '191-194 dB  air limit', ROSE), (186, '186 dB  needed (rough)', MINT)):
            cv.circ((gx + 5, Y(db)), 10, mix(col, BG, ag)); cv.text((gx + 36, Y(db) - 16), lab, 'mono', 24, col, 'la', ag)
        cv.text((gx - 10, gy1 + 4), '120 dB', 'mono', 18, DIM, 'ra', ag)

def sc_settle(cv, t, p):
    night(cv, t, 0.3)
    x0, y0, x1, y1 = CONT
    cards = [('CUTTING', CYAN, ['independent labs compare tool marks on ancient stone with marks from known methods']),
             ('LIFTING', VIO, ['a recorded demonstration: a stone of known weight, measured sound levels, a second team repeating it']),
             ('BENCH TEST', MINT, ['copper, grit, soft stone. Same minutes, vibration on vs off. Measure the groove. Our rough plan uses an ultrasonic cleaner: not a real machining rig, a first look only.', 'PLAN, NOT RUN'])]
    n = 3; gap = 28
    for i, (tt_, col, lines) in enumerate(cards):
        a = ap(t, 's12', 0.08 + i * 0.27)
        if L:
            w = (x1 - x0 - gap * 2) / 3; bx = (x0 + i * (w + gap), y0 + 10, x0 + i * (w + gap) + w, y0 + 590)
        else:
            h = (y1 - y0 - gap * 2) / 3; bx = (x0, y0 + i * (h + gap), x1, y0 + i * (h + gap) + h)
        cv.rect(bx, mix(INK, BG, a * 0.9)); cv.rect((bx[0], bx[1], bx[0] + 5, bx[3]), mix(col, BG, a))
        tag(cv, bx[0] + 24, bx[1] + 20, tt_, col, a, 24)
        yy = cv.para(bx[0] + 24, bx[1] + 92, lines[0], 'sans', 34 if L else 30, TXT, bx[2] - bx[0] - 48, 1.25, 'l', a)
        if len(lines) > 1: tag(cv, bx[0] + 24, bx[3] - 70, lines[1], ROSE, a, 20)

LEDGER = [('DOCUMENTED', MINT, 'ultrasonic machining cuts hard, brittle materials. Some Egyptian granite has saw cuts; copper + sand cut granite, slowly (Stocks)', 0.10),
          ('DISPUTED', VIO, 'how Egyptian drill holes in granite were made, and the 500 x feed-rate reading', 0.30),
          ('CLAIMED', VIO, 'that ancient builders used ultrasonic tools', 0.48),
          ('NOT ESTABLISHED', ROSE, 'that sound cut or lifted pyramid stones', 0.64),
          ('UNKNOWN HERE', ROSE, 'does vibration speed up copper + sand? Our test is not run', 0.82)]

def sc_ledger(cv, t, p):
    night(cv, t, 0.3)
    x0, y0, x1, y1 = CONT
    big(cv, x0, y0 + 0, 'the ledger', 56 if PORT else 60, TXT, ease(t / 1.0))
    step = 150 if PORT else 100
    for i, (st, col, txt, f) in enumerate(LEDGER):
        a = ap(t, 's13', f)
        if a <= 0: continue
        yy = y0 + 90 + i * step
        hline(cv, x0, x1, yy, INK2, a, 1)
        tag(cv, x0, yy + 16, st, col, a, 22)
        if L: cv.para(x0 + 390, yy + 14, txt, 'light', 36, TXT, x1 - x0 - 400, 1.1, 'l', a)
        else: cv.para(x0, yy + 76, txt, 'light', 33, TXT, x1 - x0, 1.1, 'l', a)

def sc_close(cv, t, p):
    night(cv, t, 0.8)
    x0, y0, x1, y1 = CONT
    sz = 84 if L else 72
    big(cv, x0, y0 + 0, 'ultrasonic machining cuts stone,', sz, TXT, ap(t, 's14', 0.10)); big(cv, x0, y0 + sz * 1.1, 'with grit and a transducer.', sz, TXT, ap(t, 's14', 0.16))
    tag(cv, x0, y0 + sz * 2.4, 'DOCUMENTED', MINT, ap(t, 's14', 0.20), 24)
    yy = y0 + sz * 2.4 + 80
    big(cv, x0, yy, 'in the pyramid age: not established.', 52 if L else 46, TXT, ap(t, 's14', 0.40))
    big(cv, x0, yy + 76, 'sound-lifted blocks: not established.', 52 if L else 46, TXT, ap(t, 's14', 0.62))
    big(cv, x0, yy + 170, 'not ruled out, either.', 52 if L else 46, TXT, ap(t, 's14', 0.80))
    big(cv, x0, yy + 260, 'someone watching might be the one who shows us.', 34 if L else 30, CYAN, ap(t, 's14', 0.92, 1.2))

SOURCES = [
    'Thoe, Aspinwall & Wise (1998) "Review on ultrasonic machining", Int. J. Machine Tools & Manufacture 38(4):239-255, doi 10.1016/S0890-6955(97)00036-9 (abstract/citation only; full text not read)',
    'Stocks, D. A. (2001) "Testing ancient Egyptian granite-working methods in Aswan, Upper Egypt", Antiquity 75:89-94, doi 10.1017/S0003598X00052777; figures via Hall of Ma\'at summary (full text paywalled). Book: Experiments in Egyptian Archaeology (Routledge)',
    'Dunn, C. "Advanced Machining in Ancient Egypt", Analog, Aug 1984 (text at gizapower.com): Petrie 0.100 in/turn; 0.0002 in/turn modern; ~500 x; proposes ultrasonic drilling',
    'Ultrasonic machining: Wikipedia (citing Kalpakjian 2008): typically 20-40 kHz, amplitude, SiC/B4C slurry, materials. Patents: GB 602,801 (Balamuth, priority 1945-04-14, Google Patents); US 2,580,716 (1952) as cited by a later patent. Wood & Loomis 1927: secondary sources',
    'Acoustic levitation: Wikipedia (0.6 g, 30 mm foam sphere; near-field several kg); Andrade et al., ICSV24 (2017), 50 mm sphere. Pyramid block mass ~2.3 t: encyclopedic estimates. Our arithmetic: radiation pressure 2I/c, SPL re 20 uPa. Details: SOURCES.md']
def sc_end(cv, t, p):
    night(cv, t, 0.7)
    a = ease(t / 1.0)
    y = 120 if PORT else 60
    mono(cv, HEAD[0], y, 'HEARTBEAT TV  /  CH 10', 26, CYAN, a)
    big(cv, HEAD[0], y + 36, 'still unknown', 100, TXT, a)
    mono(cv, HEAD[0], y + 160, 'heartbeatobservatory.com', 32, CYAN, a)
    yy = y + 215
    mono(cv, HEAD[0], yy, 'SOURCES', 22, DIM, ease((t - 0.6) / 1)); yy += 34
    for i, s in enumerate(SOURCES):
        yy = cv.para(HEAD[0], yy, s, 'mono', 21 if PORT else 24, TXT, (W - 2 * HEAD[0]) * (1 if PORT else 0.95), 1.22, 'l', ease((t - 0.8 - i * 0.15) / 0.8)) + 8

# (segment id, headline, source line, draw fn)
SCENES = [
    ('s1', None, 'Status as of October 2026', sc_title),
    ('s2', 'ultrasonic machining', 'Thoe et al. 1998 (doi 10.1016/S0890-6955(97)00036-9); Wikipedia "Ultrasonic machining"', sc_usm),
    ('s3', 'mostly the grit', 'Thoe et al. 1998; Wikipedia "Ultrasonic machining". Diagram is schematic', sc_grit),
    ('s4', 'published since the 1920s', 'Google Patents GB602801A; US 2,580,716 as cited by a later patent; Thoe et al. 1998', sc_history),
    ('s5', 'where it works, where it does not', 'Wikipedia "Ultrasonic machining"; Thoe et al. 1998', sc_limits),
    ('s6', 'copper and sand, at aswan', 'Stocks, Antiquity 75:89-94 (2001), via Hall of Ma\'at summary', sc_aswan),
    ('s7', 'what the experiment found', 'Stocks, Antiquity 75:89-94 (2001); 2.3 cm cube is our arithmetic', sc_rate),
    ('s8', 'same family, different speed', 'Our estimate for hand strokes; ultrasonic range from Wikipedia "Ultrasonic machining"', sc_family),
    ('s9', 'the claim: ultrasonic in egypt', 'C. Dunn, Analog, Aug 1984 (gizapower.com); Stocks 2001', sc_dunn),
    ('s10', 'the claim: sound lifts stone', 'Wikipedia "Acoustic levitation"; Andrade et al., ICSV24 (2017)', sc_sound),
    ('s11', 'a rough check', 'Our arithmetic; block mass ~2.3 t is an estimate; assumes perfect reflection, no losses', sc_arith),
    ('s12', 'what a strong test looks like', 'The bench-test plan is Heartbeat\'s own and uses a cleaner, not a machining rig; not run', sc_settle),
    ('s13', None, 'Status as of October 2026', sc_ledger),
    ('s14', None, None, sc_close),
    ('s15', None, None, sc_end),
]

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
