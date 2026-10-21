# Heartbeat TV - Space Now 11.1 "MMX: ten grams from Phobos" (CPU only: Pillow + ffmpeg libx264)
# The Space Now look (NOT History/Science navy+gold, NOT Open Questions' split screen, NOT Still Unknown's violet void):
# deep ink sky with a sparse warm starfield, launch-orange accents, Bahnschrift headlines, Cascadia Mono data, a
# "mission clock" rail 2026-2031 on every scene with a marker that moves as the story moves, centred captions in a band,
# status chips KNOWN / PUBLISHED PLAN / OPEN / MODEL. Every picture is drawn here (no photos).
#   python ep.py land|port [--still SECONDS out.png] [--secs A B] [--out file.mp4]
import json, math, subprocess, sys, random, re, os
from multiprocessing import Pool
from PIL import Image, ImageDraw, ImageFont

TL = json.load(open('timeline.json'))
TOTAL = TL['total']; SEG = {s['id']: s for s in TL['segs']}
FPS = 30; SS = 2
ORI = 'port' if 'port' in sys.argv[1:2] else 'land'
PORT = ORI == 'port'; L = not PORT
W, H = (1080, 1920) if PORT else (1920, 1080)

BG = (10, 13, 22); INK = (18, 23, 36); INK2 = (30, 38, 56); PANEL = (24, 30, 46)
ORANGE = (255, 150, 70); EMBER = (232, 96, 60); CREAM = (244, 236, 222); SAND = (208, 186, 150)
BLUE = (118, 160, 212); MARS = (196, 108, 62); GREEN = (132, 206, 140); DIM = (142, 148, 164); DIM2 = (84, 90, 108)
FD = 'C:/Windows/Fonts/'
_fc = {}
def font(kind, size):
    k = (kind, size)
    if k not in _fc:
        f = {'head': 'bahnschrift.ttf', 'mono': 'CascadiaMono.ttf', 'sans': 'segoeui.ttf', 'sansb': 'segoeuib.ttf',
             'light': 'segoeuil.ttf'}[kind]
        ft = ImageFont.truetype(FD + f, int(size * SS))
        if kind == 'head':
            try: ft.set_variation_by_name('SemiBold')
            except Exception: pass
        _fc[k] = ft
    return _fc[k]

SZ = dict(head=64 if PORT else 72, cap=52 if PORT else 46, src=25 if PORT else 24)
if PORT:
    HEAD = (60, 170, W - 60, 420); CONT = (50, 440, W - 50, 1270); CAP = (60, 1310, W - 60, 1740); SRC = (60, 1790, W - 60, 1900)
    RAIL = (60, 118, W - 60)
else:
    HEAD = (90, 70, 1250, 200); CONT = (90, 215, W - 90, 835); CAP = (180, 860, W - 180, 1000); SRC = (90, 1012, W - 90, 1072)
    RAIL = (1330, 92, W - 90)

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
    def poly(s, pts, fill, edge=None, w=1):
        s.d.polygon([s.P(p) for p in pts], fill=fill, outline=edge, width=max(1, int(w * SS)) if edge else 0)
    def circ(s, c, r, fill):
        s.d.ellipse([(c[0] - r) * SS, (c[1] - r) * SS, (c[0] + r) * SS, (c[1] + r) * SS], fill=fill)
    def ring(s, c, r, col, w=2):
        s.d.ellipse([(c[0] - r) * SS, (c[1] - r) * SS, (c[0] + r) * SS, (c[1] + r) * SS], outline=col, width=max(1, int(w * SS)))
    def arc(s, c, r, a0, a1, col, w=2):
        s.d.arc([(c[0] - r) * SS, (c[1] - r) * SS, (c[0] + r) * SS, (c[1] + r) * SS], a0, a1, fill=col, width=max(1, int(w * SS)))
    def text(s, xy, t, kind, size, col, anchor='la', a=1.0):
        if a <= 0: return
        s.d.text(s.P(xy), t, font=font(kind, size), fill=mix(col, BG, a), anchor=anchor)
    def para(s, x, y, t, kind, size, col, maxw, lh=1.25, anchor='l', a=1.0):
        f = font(kind, size); ls = wrap(t, f, maxw)
        if a <= 0: return y + len(ls) * size * lh
        for i, l in enumerate(ls):
            s.d.text(s.P((x, y + i * size * lh)), l, font=f, fill=mix(col, BG, a), anchor={'l': 'la', 'm': 'ma', 'r': 'ra'}[anchor])
        return y + len(ls) * size * lh

# ------------------------------------------------------------------ shared pieces
R = random.Random(11)
STARS = [(R.random(), R.random(), R.uniform(0.5, 1.9), R.uniform(0.2, 0.9), R.uniform(0, 6.28), R.random() < 0.15) for _ in range(300)]
def sky(cv, tt, dim=0.8):
    for (x, y, r, b, ph, warm) in STARS:
        tw = 0.7 + 0.3 * math.sin(tt * 0.9 + ph)
        cv.circ((x * W, y * H), r, mix(SAND if warm else CREAM, BG, b * tw * dim))

def F(sid, f): return SEG[sid]['start'] + f * SEG[sid]['dur'] - BOUND[sid][0]
def ap(t, sid, f, d=0.8): return ease((t - F(sid, f)) / d)
def count(v, t, t0, dur=1.2, fmt='{:,.0f}'): return fmt.format(v * ease((t - t0) / dur))

def chip(cv, x, y, label, col, a=1.0, size=22, anchor='l'):
    """status chip: rounded, outlined, mono caps - the Space Now status mark."""
    f = font('mono', size); w = f.getlength(label) / SS + 34; h = size + 18
    if a <= 0: return w
    x0 = x if anchor == 'l' else (x - w if anchor == 'r' else x - w / 2)
    cv.rect((x0, y, x0 + w, y + h), mix(mix(col, BG, 0.18), BG, a), 8)
    cv.outline((x0, y, x0 + w, y + h), mix(col, BG, a), 2, 8)
    cv.text((x0 + 17, y + 8), label, 'mono', size, col, 'la', a)
    return w

def card(cv, b, a=1.0, col=None, r=14):
    cv.rect(b, mix(PANEL, BG, a), r); cv.outline(b, mix(col or INK2, BG, a), 2, r)

def big(cv, x, y, s, size, col, a=1.0, anchor='la'): cv.text((x, y), s, 'head', size, col, anchor, a)
def mono(cv, x, y, s, size, col, a=1.0, anchor='la'): cv.text((x, y), s, 'mono', size, col, anchor, a)

def rail(cv, x0, x1, y, year, a=1.0, big_=False, marks=None, col=ORANGE):
    """mission clock 2026..2031; year = marker position (float year) or None."""
    if a <= 0: return
    cv.line([(x0, y), (x1, y)], mix(DIM2, BG, a), 3 if big_ else 2)
    for k in range(6):
        x = x0 + (x1 - x0) * k / 5
        cv.line([(x, y - (10 if big_ else 6)), (x, y + (10 if big_ else 6))], mix(DIM, BG, a), 2)
        mono(cv, x, y + (16 if big_ else 10), str(2026 + k), 26 if big_ else 16, DIM, a, 'ma')
    for (yr, lab, c, aa) in (marks or []):
        if aa <= 0: continue
        x = x0 + (x1 - x0) * (yr - 2026) / 5
        cv.circ((x, y), 9, mix(c, BG, aa)); cv.line([(x, y - 14), (x, y - 44)], mix(c, BG, aa), 2)
        mono(cv, x, y - 72, lab, 20, c, aa, 'ma')
    if year is not None:
        x = x0 + (x1 - x0) * (year - 2026) / 5
        cv.circ((x, y), 16 if big_ else 11, mix(col, BG, 0.25 * a)); cv.circ((x, y), 8 if big_ else 5, mix(col, BG, a))

def stat_rows(cv, t, sid, x, y, rows, w, step, big_sz=48, small=24, col=ORANGE):
    """rows: (big text, small caption, fraction of segment when it appears)"""
    for i, (b, s, f) in enumerate(rows):
        a = ap(t, sid, f)
        if a <= 0: continue
        yy = y + i * step
        cv.rect((x, yy + 6, x + 5, yy + step - 24), mix(col, BG, a))
        big(cv, x + 22, yy, b, big_sz, CREAM, a)
        cv.para(x + 22, yy + big_sz * 1.15, s, 'sans', small, DIM, w - 30, 1.2, 'l', a)

def rocket(cv, x, yb, h, a=1.0, labels=None, t=0):
    """H3-24L silhouette: long fairing, core, 4 boosters (2 visible each side), 2 engines. (x,yb) = base centre."""
    if a <= 0: return
    cw = h * 0.085; fh = h * 0.36; bw = cw * 0.55; bh = h * 0.42
    core = mix((206, 208, 214), BG, a); dark = mix((120, 124, 134), BG, a); orng = mix(ORANGE, BG, a)
    # boosters
    for sx in (-1, 1):
        bx = x + sx * (cw * 0.95)
        cv.rect((bx - bw / 2, yb - bh, bx + bw / 2, yb), dark, 6)
        cv.poly([(bx - bw / 2, yb - bh), (bx, yb - bh - bw * 1.3), (bx + bw / 2, yb - bh)], dark)
        cv.poly([(bx - bw * 0.35, yb), (bx + bw * 0.35, yb), (bx + bw * 0.5, yb + bw * 0.5), (bx - bw * 0.5, yb + bw * 0.5)], orng)
    # core
    cv.rect((x - cw / 2, yb - h + fh, x + cw / 2, yb), core)
    cv.rect((x - cw / 2, yb - h + fh, x + cw / 2, yb - h + fh + 6), mix(EMBER, BG, a))
    # fairing (long)
    cv.rect((x - cw / 2, yb - h + fh * 0.45, x + cw / 2, yb - h + fh), core)
    cv.poly([(x - cw / 2, yb - h + fh * 0.45), (x, yb - h), (x + cw / 2, yb - h + fh * 0.45)], core)
    # engines
    for sx in (-0.5, 0.5):
        ex = x + sx * cw * 0.45
        cv.poly([(ex - cw * 0.16, yb), (ex + cw * 0.16, yb), (ex + cw * 0.24, yb + cw * 0.45), (ex - cw * 0.24, yb + cw * 0.45)], orng)
    if labels:
        lx = x + cw * 1.6
        for (ly, txt) in labels:
            yy = yb - h + fh * ly if ly <= 1 else yb - (ly - 1) * (h - fh)
            cv.line([(x + cw * 0.9, yy), (lx, yy)], mix(DIM, BG, a), 2)
            mono(cv, lx + 10, yy - 12, txt, 22, SAND, a)

def phobos(cv, cx, cy, r, a=1.0, seed=3, stickney=True):
    rr = random.Random(seed); pts = []
    for k in range(48):
        th = k / 48 * 2 * math.pi
        rad = r * (1 + 0.16 * math.sin(2 * th + 0.8) + 0.07 * math.sin(5 * th + 2) + rr.uniform(-0.02, 0.02))
        pts.append((cx + rad * math.cos(th), cy + rad * 0.82 * math.sin(th)))
    cv.poly(pts, mix((66, 60, 58), BG, a), mix((104, 96, 92), BG, a), 2)
    if stickney: cv.circ((cx - r * 0.45, cy - r * 0.2), r * 0.3, mix((48, 44, 44), BG, a)); cv.ring((cx - r * 0.45, cy - r * 0.2), r * 0.3, mix((88, 82, 80), BG, a), 2)
    for (dx, dy, cr) in ((0.3, 0.3, 0.1), (0.5, -0.3, 0.07), (0.05, 0.5, 0.06), (0.6, 0.15, 0.05)):
        cv.circ((cx + dx * r, cy + dy * r), r * cr, mix((50, 46, 46), BG, a))

def mars_arc(cv, cx, cy, r, a=1.0):
    if a <= 0: return
    a *= 0.72
    cv.circ((cx, cy), r, mix(MARS, BG, a))
    cv.circ((cx - r * 0.25, cy - r * 0.3), r * 0.22, mix((176, 92, 54), BG, a)); cv.circ((cx + r * 0.3, cy - r * 0.1), r * 0.16, mix((150, 80, 50), BG, a))
    cv.ring((cx, cy), r + 6, mix((236, 170, 120), BG, 0.25 * a), 6)

def lander(cv, cx, gy, s, a=1.0, arm=0.0, puff=0.0):
    """exploration module on the surface. s = scale (body half-width). arm 0..1 = corer going down. puff 0..1 = P-SMP gas."""
    if a <= 0: return
    body = mix((200, 204, 210), BG, a); gold = mix((214, 170, 90), BG, a); dk = mix((120, 124, 134), BG, a)
    by = gy - s * 1.1
    cv.rect((cx - s, by - s * 0.8, cx + s, by), body, 8)
    cv.rect((cx - s * 0.9, by - s * 0.78, cx + s * 0.9, by - s * 0.5), gold)
    # solar wings (return module above)
    cv.rect((cx - s * 2.6, by - s * 1.25, cx - s * 1.1, by - s * 1.0), mix(BLUE, BG, a))
    cv.rect((cx + s * 1.1, by - s * 1.25, cx + s * 2.6, by - s * 1.0), mix(BLUE, BG, a))
    cv.rect((cx - s * 0.5, by - s * 1.3, cx + s * 0.5, by - s * 0.8), body, 6)
    # legs
    for sx in (-1, 1):
        cv.line([(cx + sx * s * 0.8, by), (cx + sx * s * 1.7, gy)], dk, 6)
        cv.line([(cx + sx * s * 0.8, by - s * 0.4), (cx + sx * s * 1.7, gy)], dk, 4)
        cv.rect((cx + sx * s * 1.7 - s * 0.22, gy - 6, cx + sx * s * 1.7 + s * 0.22, gy + 4), dk, 4)
    # arm + corer
    ax = cx - s * 0.3; ay = by
    reach = s * 1.05 * arm
    cv.line([(ax, ay), (ax - s * 0.9, ay + s * 0.3 + reach * 0.3)], gold, 6)
    tip = (ax - s * 0.9, ay + s * 0.3 + reach * 0.3)
    cv.line([tip, (tip[0], tip[1] + s * 0.55 + reach * 0.6)], mix(ORANGE, BG, a), 8)
    # pneumatic puff near right footpad
    if puff > 0:
        px = cx + s * 1.7
        for k in range(8):
            ang = -math.pi / 2 + (k - 3.5) * 0.22
            d = s * 0.5 * puff
            cv.circ((px + d * math.cos(ang) * (1 + k % 2 * 0.3), gy - 10 + d * math.sin(ang)), 4 + 3 * puff, mix(BLUE, BG, a * (1 - puff * 0.6)))

def rover(cv, cx, cy, s, a=1.0, wheels=True, tilt=0.0):
    if a <= 0: return
    body = mix((216, 212, 200), BG, a); dk = mix((110, 114, 124), BG, a)
    cv.rect((cx - s, cy - s * 0.55, cx + s, cy + s * 0.55), body, 6)
    cv.rect((cx - s * 0.9, cy - s * 0.5, cx + s * 0.9, cy - s * 0.25), mix(BLUE, BG, a))
    if wheels:
        for sx in (-0.7, 0.7):
            cv.circ((cx + sx * s, cy + s * 0.65), s * 0.3, dk); cv.circ((cx + sx * s, cy + s * 0.65), s * 0.12, body)

def ground(cv, gy, a=1.0, col=(58, 54, 54)):
    pts = [(0, H)]
    for k in range(0, W + 41, 40):
        pts.append((k, gy + 10 * math.sin(k * 0.013) + 6 * math.sin(k * 0.041 + 1)))
    pts.append((W, H))
    cv.poly(pts, mix(col, BG, a))

# ------------------------------------------------------------------ scenes
def sc_title(cv, t, p):
    sky(cv, t, 1.0)
    if L:
        ground(cv, 980, 0.9, (26, 30, 40)); rocket(cv, 1560, 975, 760, ease(t / 1.4))
        mars_arc(cv, 160, 1540, 480, ease((t - 0.4) / 1.5)); phobos(cv, 300, 905, 58, ease((t - 0.9) / 1.0))
    else:
        ground(cv, 1270, 0.9, (26, 30, 40)); rocket(cv, 840, 1265, 560, ease(t / 1.4))
        mars_arc(cv, 100, 2080, 640, ease((t - 0.4) / 1.5)); phobos(cv, 300, 1160, 56, ease((t - 0.9) / 1.0))
    y0 = 330 if PORT else 250
    mono(cv, HEAD[0], y0, 'HEARTBEAT TV  /  CH 11  /  SPACE NOW  /  EP 01', 26 if PORT else 26, ORANGE, ease(t / 1.0))
    sz = 108 if PORT else 124
    lines = ('MMX: ten grams', 'from Phobos')
    for k, l in enumerate(lines): big(cv, HEAD[0], y0 + 52 + k * sz * 1.02, l, sz, CREAM, ease((t - 0.3 - k * 0.25) / 1.2))
    yy = y0 + 52 + len(lines) * sz * 1.02 + 30
    cv.para(HEAD[0], yy, "Japan's Mars-moon sample return  ·  launch Oct 19-20, 2026", 'sans', 30 if PORT else 34, SAND, 900, 1.2, 'l', ease((t - 1.4) / 1.0))
    ty = yy + 110; x = HEAD[0]
    for i, (lab, col, f) in enumerate((('KNOWN', GREEN, 0.55), ('PUBLISHED PLAN', BLUE, 0.68), ('OPEN', EMBER, 0.80))):
        aa = ap(t, 's1', f, 0.8)
        if PORT: chip(cv, HEAD[0], ty + i * 64, lab, col, aa)
        else: w = chip(cv, x, ty, lab, col, aa); x += (w if w > 0 else 0) + 18

def sc_launch(cv, t, p):
    sky(cv, t, 0.5)
    x0, y0, x1, y1 = CONT
    if L:
        card(cv, (x0, y0, x0 + 860, y1), ease(t / 0.6))
        stat_rows(cv, t, 's2', x0 + 40, y0 + 40, [('04:41:03  ·  Oct 20', 'Japan Standard Time (JAXA launch plan)', 0.05),
                                                   ('3:41 PM  ·  Oct 19', 'US Eastern (the same instant)', 0.22),
                                                   ('Oct 21 - Nov 7', 'reserved backup period, time set per day', 0.42)], 800, 190, 56, 26)
        ground(cv, y1, 0.9, (26, 30, 40)); rocket(cv, 1420, y1 - 4, 590, ap(t, 's2', 0.55, 1.0),
               [(0.5, 'long fairing  ·  MMX inside'), (1.45, '4 solid boosters (SRB-3)'), (1.95, '2 LE-9 engines')], t)
        mono(cv, 1420, y1 + 14, 'H3-24L  ·  flight 10', 24, SAND, ap(t, 's2', 0.62), 'ma')
    else:
        card(cv, (x0, y0, x1, y0 + 470), ease(t / 0.6))
        stat_rows(cv, t, 's2', x0 + 30, y0 + 30, [('04:41:03  ·  Oct 20', 'Japan time (JAXA launch plan)', 0.05),
                                                   ('3:41 PM  ·  Oct 19', 'US Eastern (same instant)', 0.22),
                                                   ('Oct 21 - Nov 7', 'backup period, time set per day', 0.42)], x1 - x0 - 60, 140, 50, 24)
        ground(cv, y1, 0.9, (26, 30, 40)); rocket(cv, x0 + 220, y1 - 4, 330, ap(t, 's2', 0.55, 1.0),
               [(0.5, 'long fairing'), (1.45, '4 boosters'), (1.95, '2 LE-9 engines')], t)
        mono(cv, x0 + 220, y1 + 12, 'H3-24L · flight 10', 22, SAND, ap(t, 's2', 0.62), 'ma')

EVENTS = [(116, 'T+1:56  boosters off', 0.12), (197, 'T+3:17  fairing off', 0.24), (299, 'T+4:59  stage 1 off', 0.36),
          (312, 'T+5:12  stage 2 burn 1', 0.44), (640, 'T+10:40  cutoff, coast', 0.52), (3837, 'T+1:03:57  burn 2', 0.66),
          (4221, 'T+1:10:21  cutoff', 0.74), (4272, 'T+1:11:12  MMX released  ·  592 km  ·  11.2 km/s', 0.82)]
def sc_ascent(cv, t, p):
    sky(cv, t, 0.7)
    x0, y0, x1, y1 = CONT
    # rising arc, event dots along it (time axis is not linear: labelled)
    if L: pts = [(x0 + 900 + k * (x1 - x0 - 940) / 60, y1 - 40 - (y1 - y0 - 120) * (k / 60) ** 0.55) for k in range(61)]
    else: pts = [(x0 + 560 + k * (x1 - x0 - 590) / 60, y1 - 60 - (y1 - y0 - 420) * (k / 60) ** 0.55) for k in range(61)]
    u = ap(t, 's3', 0.0, 1.0) * 0.02 + ap(t, 's3', 0.9, 6.0) * 0.98
    n = max(2, int(len(pts) * ease(u)))
    cv.line(pts[:n], mix(ORANGE, BG, 0.9), 4)
    mono(cv, x0 + (900 if L else 560), y1 - (18 if L else 38), 'LIFTOFF', 20, DIM, 1, 'la')
    for i, (sec, lab, f) in enumerate(EVENTS):
        a = ap(t, 's3', f)
        if a <= 0: continue
        k = int(60 * ((i + 1) / len(EVENTS)) ** 1.0); px, py = pts[min(k, 60)]
        cv.circ((px, py), 9, mix(ORANGE if i < 7 else GREEN, BG, a))
        mono(cv, px, py + 16, str(i + 1), 18, DIM, a, 'ma')
        if L:
            yy = y0 + 20 + i * 62
            mono(cv, x0 + 20, yy, f'{i + 1}  ' + (lab if i < 7 else 'T+1:11:12  MMX released  ·  592 km  ·  11.2 km/s'), 24, SAND if i < 7 else GREEN, a)
        else:
            yy = y0 + 60 + i * 86 if i < 7 else y0 + 60 + 7 * 86
            mono(cv, x0 + 20, yy, f'{i + 1}  ' + (lab if i < 7 else 'T+1:11:12  MMX released'), 24, SAND if i < 7 else GREEN, a)
            if i == 7: mono(cv, x0 + 20, yy + 34, '   592 km up  ·  11.2 km/s', 24, GREEN, a)
    chip(cv, x1, y0 if L else y1 - 50, 'PUBLISHED PLAN  ·  OCT 20 CASE', BLUE, ease((t - 0.5) / 1), 20, 'r')

def sc_craft(cv, t, p):
    sky(cv, t, 0.5)
    x0, y0, x1, y1 = CONT
    # three stacked modules
    if L: cx, top, mw = x0 + 300, y0 + 40, 300
    else: cx, top, mw = W / 2, y0 + 30, 420
    mods = [('RETURN MODULE', 'solar wings · antenna · sample capsule', BLUE, 0.52, 150), ('EXPLORATION MODULE', 'landing legs · 2 samplers · instruments', ORANGE, 0.36, 150), ('PROPULSION MODULE', 'the push to Mars, cast off when done', SAND, 0.20, 210)]
    yy = top
    for (name, sub, col, f, hh) in mods:
        a = ap(t, 's4', f)
        if a > 0:
            cv.rect((cx - mw / 2, yy, cx + mw / 2, yy + hh), mix(mix(col, PANEL, 0.35), BG, a), 10); cv.outline((cx - mw / 2, yy, cx + mw / 2, yy + hh), mix(col, BG, a), 3, 10)
            big(cv, cx + mw / 2 + 30 if L else cx, yy + 20 if L else yy + hh / 2 - 34, name, 40 if L else 34, CREAM, a, 'la' if L else 'ma')
            cv.para(cx + mw / 2 + 30 if L else cx, yy + 72 if L else yy + hh / 2 + 10, sub, 'sans', 26, DIM, 700 if L else mw - 20, 1.2, 'l' if L else 'm', a)
            if name.startswith('RETURN') and PORT:
                cv.rect((cx - mw / 2 - 170, yy + 50, cx - mw / 2 - 10, yy + 90), mix(BLUE, BG, a)); cv.rect((cx + mw / 2 + 10, yy + 50, cx + mw / 2 + 170, yy + 90), mix(BLUE, BG, a))
        yy += hh + 14
    a = ap(t, 's4', 0.03)
    if L:
        card(cv, (x1 - 560, y0 + 20, x1, y0 + 250), a)
        big(cv, x1 - 530, y0 + 40, count(4480, t, F('s4', 0.03)) + ' kg', 92, ORANGE, a); cv.para(x1 - 530, y0 + 160, 'launch mass (JAXA launch plan, Aug 2026)', 'sans', 26, DIM, 520, 1.2, 'l', a)
        a2 = ap(t, 's4', 0.8)
        mono(cv, x1 - 530, y0 + 300, 'PARTNERS', 20, DIM, a2)
        for i, (pn, role) in enumerate((('JAXA', 'lead, spacecraft, H3'), ('NASA', 'MEGANE, pneumatic sampler'), ('CNES', 'MIRS, rover (with DLR)'), ('DLR', 'rover (with CNES)'), ('ESA', 'deep-space radio, ground stations'))):
            aa = ap(t, 's4', 0.8 + i * 0.03)
            big(cv, x1 - 530, y0 + 340 + i * 56, pn, 34, CREAM, aa); mono(cv, x1 - 390, y0 + 350 + i * 56, role, 22, SAND, aa)
    else:
        big(cv, x0 + 10, y1 - 300, count(4480, t, F('s4', 0.03)) + ' kg', 84, ORANGE, a); cv.para(x0 + 10, y1 - 200, 'launch mass (JAXA launch plan, Aug 2026)', 'sans', 26, DIM, 600, 1.2, 'l', a)
        a2 = ap(t, 's4', 0.8)
        cv.para(x0 + 10, y1 - 120, 'JAXA leads · NASA (MEGANE, pneumatic sampler) · CNES + DLR (rover, MIRS) · ESA (radio, ground stations)', 'sans', 26, SAND, x1 - x0 - 20, 1.25, 'l', a2)

def sc_phobos(cv, t, p):
    sky(cv, t, 0.9)
    x0, y0, x1, y1 = CONT
    if L:
        mars_arc(cv, x0 + 120, y1 + 700, 760, ease(t / 1.2)); phobos(cv, x0 + 330, y0 + 170, 92, ease((t - 0.3) / 1.0))
        cv.arc((x0 + 120, y1 + 700), 1120, 212, 262, mix(DIM, BG, 0.6 * ease((t - 0.5) / 1)), 2)
        stat_rows(cv, t, 's5', x0 + 640, y0 + 10, [('~27 x 22 x 18 km', 'a dark lump, albedo like coal (NASA)', 0.08), ('6,000 km up', 'three times closer than most satellites are to Earth', 0.2),
                                                   ('7 h 39 min', 'one lap of Mars - faster than Mars turns', 0.28)], 560, 118, 44, 24)
        bx = x0 + 640; by = y0 + 380
        for i, (lab, body, col, f) in enumerate((('CAPTURED ASTEROID', 'looks like one (dark, red-ish); but capture should leave a tilted, stretched orbit', BLUE, 0.5),
                                                 ('IMPACT DEBRIS', 'explains the circular, equatorial orbit; but heated debris should be dry', EMBER, 0.7))):
            a = ap(t, 's5', f); bb = (bx + i * 560, by, bx + i * 560 + 540, by + 210)
            card(cv, bb, a, col); chip(cv, bb[0] + 20, bb[1] + 18, lab, col, a, 20)
            cv.para(bb[0] + 20, bb[1] + 70, body, 'sans', 25, CREAM, 500, 1.22, 'l', a)
        chip(cv, x0 + 640, y1 - 40, 'NOT SETTLED', EMBER, ap(t, 's5', 0.88), 22)
    else:
        mars_arc(cv, x0 - 200, y1 + 900, 900, ease(t / 1.2)); phobos(cv, x0 + 240, y0 + 150, 86, ease((t - 0.3) / 1.0))
        stat_rows(cv, t, 's5', x0 + 420, y0 + 10, [('~27 km long', 'dark as coal', 0.08), ('6,000 km up', 'close to Mars', 0.2), ('7 h 39 min', 'one lap', 0.28)], 560, 108, 40, 22)
        by = y0 + 360
        for i, (lab, body, col, f) in enumerate((('CAPTURED ASTEROID', 'looks like one; but capture should leave a tilted, stretched orbit', BLUE, 0.5),
                                                 ('IMPACT DEBRIS', 'explains the circular, equatorial orbit; but heated debris should be dry', EMBER, 0.7))):
            a = ap(t, 's5', f); bb = (x0 + 10, by + i * 200, x1 - 10, by + i * 200 + 180)
            card(cv, bb, a, col); chip(cv, bb[0] + 20, bb[1] + 16, lab, col, a, 20)
            cv.para(bb[0] + 20, bb[1] + 66, body, 'sans', 25, CREAM, x1 - x0 - 60, 1.22, 'l', a)
        chip(cv, x0 + 10, y1 - 60, 'NOT SETTLED', EMBER, ap(t, 's5', 0.88), 22)

def sc_lab(cv, t, p):
    sky(cv, t, 0.4)
    x0, y0, x1, y1 = CONT
    a = ease(t / 0.8)
    # the 10 g vial
    vx, vy = (x0 + 150, y0 + 80) if L else (x0 + 120, y0 + 40)
    cv.rect((vx - 60, vy, vx + 60, vy + 260), mix(INK2, BG, a), 18); cv.outline((vx - 60, vy, vx + 60, vy + 260), mix(SAND, BG, a), 3, 18)
    rr = random.Random(5)
    for k in range(70):
        gx, gy = vx + rr.uniform(-48, 48), vy + 150 + rr.uniform(-10, 95)
        cv.circ((gx, gy), rr.uniform(2, 5), mix((110, 96, 88), BG, a))
    big(cv, vx, vy + 290, '10 g', 54, ORANGE, a, 'ma'); mono(cv, vx, vy + 350, 'minimum', 20, DIM, a, 'ma')
    lx = x0 + 320 if L else x0 + 260
    stat_rows(cv, t, 's6', lx, y0 + 10, [('minerals + locked water', 'what it is made of, how wet it was', 0.12), ('isotope ratios (H, O, Cr, Ti)', 'a fingerprint of where it formed', 0.28),
                                        ('radiometric age', 'when it last melted', 0.4)], 700 if L else 760, 118 if L else 112, 40 if L else 36, 24 if L else 22)
    by = y0 + 400 if L else y0 + 400
    cols = [('IF CAPTURED', 'like a body from the outer solar system; could carry water and organic matter from out there', BLUE, 0.56), ('IF IMPACT DEBRIS', 'roughly half Martian material, with the easily vaporised elements baked out', EMBER, 0.72)]
    for i, (lab, body, col, f) in enumerate(cols):
        aa = ap(t, 's6', f)
        bb = (lx + i * 560, by, lx + i * 560 + 540, by + 190) if L else (x0 + 10, by + i * 200, x1 - 10, by + i * 200 + 180)
        card(cv, bb, aa, col); chip(cv, bb[0] + 20, bb[1] + 18, lab, col, aa, 20); cv.para(bb[0] + 20, bb[1] + 70, body, 'sans', 25, CREAM, bb[2] - bb[0] - 40, 1.22, 'l', aa)
    chip(cv, lx, y1 - 40 if L else y1 - 50, 'THE TEST  ·  R. HYODO (JAXA / ISAS), MMX NEWS', GREEN, ap(t, 's6', 0.86), 20)

def sc_grains(cv, t, p):
    sky(cv, t, 0.8)
    x0, y0, x1, y1 = CONT
    a = ease(t / 1.0)
    if L: mcx, mcy, mr, pcx, pcy, angd = x0 + 200, y1 + 260, 520, x0 + 560, y0 + 90, -50
    else: mcx, mcy, mr, pcx, pcy, angd = x0 - 150, y1 + 450, 620, x0 + 150, y0 + 110, -75
    mars_arc(cv, mcx, mcy, mr, a); phobos(cv, pcx, pcy, 90 if L else 80, a, 4)
    mono(cv, pcx, pcy - (120 if L else 110), 'PHOBOS', 18, DIM, a, 'ma'); mono(cv, mcx + (420 if L else 330), mcy - mr + 40, 'MARS', 18, DIM, a, 'ma')
    # ejecta arcs: impact flash on Mars, arcs to Phobos
    aa = ap(t, 's7', 0.1, 1.5)
    if aa > 0:
        ang = math.radians(angd); ix, iy = mcx + mr * math.cos(ang), mcy + mr * math.sin(ang)
        cv.circ((ix, iy), 14 + 10 * aa, mix(ORANGE, BG, aa * 0.9))
        for k in range(6):
            u = clamp01(ap(t, 's7', 0.12 + k * 0.03, 2.2))
            if u <= 0: continue
            n = max(2, int(30 * u)); pts = []
            for j in range(n):
                s = j / 29; px = lerp(ix, pcx, s) - math.sin(s * math.pi) * (30 + k * 18) * (1 if L else -1); py = lerp(iy, pcy, s) - math.sin(s * math.pi) * (60 + k * 20)
                pts.append((px, py))
            cv.line(pts, mix(SAND, BG, 0.7 * aa), 2)
            cv.circ(pts[-1], 4, mix(ORANGE, BG, aa))
    rx = x0 + 900 if L else x0 + 330; ry = y0 + 40 if L else y0 + 10; rw = 880 if L else 640
    stat_rows(cv, t, 's7', rx, ry, [('~340 ppm', 'Martian material in the top layer, statistical estimate; up to ~760 ppm with rare big impacts', 0.3),
                                    ('a few dozen grains', 'of Mars in a 10 g sample, if the model holds (0.3 mm grains)', 0.5)], rw, 150 if L else 150, 52 if L else 44, 24 if L else 23)
    chip(cv, rx, ry + 320, 'MODEL ESTIMATE  ·  Hyodo et al. 2019', BLUE, ap(t, 's7', 0.68), 20)
    cv.para(rx, ry + 390, 'if it holds: Mars material carried home for the first time, inside Phobos dirt', 'head', 30 if L else 28, SAND, rw, 1.2, 'l', ap(t, 's7', 0.84))

def sc_timeline(cv, t, p):
    sky(cv, t, 0.5)
    x0, y0, x1, y1 = CONT
    yr = lerp(2026.8, 2031.0, ease(ap(t, 's8', 0.02, 1.0) * 0.1 + ap(t, 's8', 0.1, 18.0) * 0.9))
    ry = y0 + 330 if L else y0 + 520
    marks = [(2026.8, 'LAUNCH', GREEN, ap(t, 's8', 0.0)), (2027.65, 'ARRIVE · QSO', BLUE, ap(t, 's8', 0.06)), (2029.1, 'ROVER', BLUE, ap(t, 's8', 0.4)),
             (2029.6, 'LAND (DLR)', EMBER, ap(t, 's8', 0.62)), (2030.3, 'LAND (ESA)', EMBER, ap(t, 's8', 0.56)), (2031.5, 'HOME', GREEN, ap(t, 's8', 0.78))]
    rail(cv, x0 + 40, x1 - 40, ry, yr, ease(t / 0.8), True, marks)
    rows = [('late 2027', 'Mars orbit, then a quasi-satellite orbit shadowing Phobos: a first', 0.05), ('months of mapping', 'shape, gravity, dozens of candidate landing spots', 0.25),
            ('2029', 'drop the rover; landing + sampling 2029 (DLR) or 2030 (ESA): the agencies differ by a year', 0.45), ('2031', 'capsule to Australia, samples to JAXA in Sagamihara', 0.78)]
    if L:
        for i, (b, s, f) in enumerate(rows):
            a = ap(t, 's8', f)
            if a <= 0: continue
            bx = x0 + 40 + i * 440; by = ry + 110
            cv.rect((bx, by, bx + 5, by + 150), mix(ORANGE, BG, a)); big(cv, bx + 22, by, b, 40, CREAM, a); cv.para(bx + 22, by + 50, s, 'sans', 24, DIM, 390, 1.2, 'l', a)
    else:
        stat_rows(cv, t, 's8', x0 + 10, y0 + 10, rows, x1 - x0 - 30, 118, 40, 22)
    chip(cv, x1 - 40 if L else x1 - 10, y0 + 10 if L else y1 - 50, 'PUBLISHED PLAN, NOT A PROMISE', BLUE, ap(t, 's8', 0.9), 20, 'r')

def sc_rover(cv, t, p):
    sky(cv, t, 0.7)
    x0, y0, x1, y1 = CONT
    gy = y1 - 30
    ground(cv, gy, 0.95)
    # drop: rover falls from the ship, tumbles, lands, wheels unfold
    u = ap(t, 's9', 0.36, 3.0); v = ap(t, 's9', 0.62, 1.5)
    rx = x0 + 300 if L else x0 + 260
    sy = y0 + 20; ry = lerp(sy, gy - 60, u)
    cv.rect((rx - 90, sy - 30, rx + 90, sy + 20), mix((200, 204, 210), BG, ease(t / 0.8)), 6)
    mono(cv, rx + 110, sy - 20, 'MMX, about 40 m up', 22, SAND, ease(t / 0.8))
    rover(cv, rx, ry, 70, ease((t - 0.2) / 0.8), wheels=v > 0.5)
    if 0 < u < 1: cv.line([(rx, sy + 30), (rx, ry - 50)], mix(DIM2, BG, 0.6), 2)
    big(cv, rx, gy + 10 if L else gy + 8, 'lands, rights itself, 4 wheels', 24, SAND, v, 'ma')
    sx = x0 + 640 if L else x0 + 10; sy2 = y0 + 10 if L else y0 + 150
    stat_rows(cv, t, 's9', sx, sy2, [('IDEFIX', 'CNES (France) + DLR (Germany); drives ~1 mm/s', 0.0), ('25 kg on Earth', 'about 15 g of weight on Phobos (ESA): a few coins', 0.08),
                                    ('~100 days', 'cameras, Raman spectrometer (RAX), radiometer (miniRAD)', 0.78)], 900 if L else 540, 130 if L else 120, 46 if L else 40, 24 if L else 22)
    chip(cv, sx, sy2 + 420 if L else sy2 + 380, 'SCOUT FOR THE LANDER', GREEN, ap(t, 's9', 0.9), 20)

def sc_landing(cv, t, p):
    sky(cv, t, 0.7)
    x0, y0, x1, y1 = CONT
    gy = y1 - 30; ground(cv, gy, 0.95)
    arm = ap(t, 's10', 0.3, 2.0); puff = ap(t, 's10', 0.55, 1.2) * (1 - ap(t, 's10', 0.75, 1.5))
    lcx = x0 + 420 if L else W / 2; s = 110 if L else 90
    lander(cv, lcx, gy, s, ease(t / 0.8), arm, puff)
    if arm > 0.3: mono(cv, lcx - s * 0.9, gy + 12, '> 2 cm core, shape-memory grip', 20, ORANGE, ap(t, 's10', 0.4), 'ma')
    if puff > 0.05: mono(cv, lcx + s * 1.7, gy - s * 1.0, 'nitrogen puff', 20, BLUE, 1, 'ma')
    sx = x0 + 900 if L else x0 + 10; sy = y0 + 10
    stat_rows(cv, t, 's10', sx, sy, [('up to 44 min', 'radio there and back: it lands by itself, on 4 legs', 0.05),
                                     ('C-SMP corer', 'on the arm: pushes past 2 cm, keeps the core (JAXA)', 0.26),
                                     ('P-SMP pneumatic', 'by a footpad: nitrogen blows surface grains in (NASA)', 0.5)], 880 if L else 760, 130 if L else 118, 44 if L else 38, 24 if L else 22)
    chip(cv, sx, sy + 410 if L else y0 + 380, '2 SOFT LANDINGS  ·  2-3 H EACH  ·  JAXA', BLUE, ap(t, 's10', 0.86), 20)

INSTR = [('TENGOO', 'telescope camera', 'JAXA'), ('OROCHI', 'wide colour camera', 'JAXA'), ('LIDAR', 'laser altimeter', 'JAXA'), ('MIRS', 'infrared: minerals, water', 'CNES'),
         ('MEGANE', 'gamma rays + neutrons: elements', 'NASA / APL'), ('MSA', 'ion analyser', 'JAXA'), ('CMDM', 'dust counter', 'JAXA'), ('IREM', 'radiation monitor', 'JAXA'),
         ('SHV', '4K / 8K camera', 'JAXA + NHK')]
def sc_instruments(cv, t, p):
    sky(cv, t, 0.6)
    x0, y0, x1, y1 = CONT
    cols = 3; cw = (x1 - x0 - 20) / cols; ch = 150 if L else 160
    for i, (nm, what, who) in enumerate(INSTR):
        a = ap(t, 's11', 0.04 + i * 0.075)
        if a <= 0: continue
        bx = x0 + (i % cols) * cw + 10; by = y0 + (i // cols) * (ch + 14)
        bb = (bx, by, bx + cw - 20, by + ch)
        card(cv, bb, a, ORANGE if nm == 'MEGANE' else None)
        big(cv, bx + 22, by + 16, nm, 40 if L else 34, CREAM, a); mono(cv, bx + 22, by + 68 if L else by + 62, who, 20, SAND, a)
        cv.para(bx + 22, by + 98 if L else by + 92, what, 'sans', 24 if L else 22, DIM, cw - 60, 1.15, 'l', a)
    a = ap(t, 's11', 0.86)
    if L:
        phobos(cv, x1 - 110, y1 - 60, 34, a, 9, False); mono(cv, x1 - 160, y1 - 72, 'DEIMOS flybys, second half of the mission', 22, SAND, a, 'ra')
    else:
        phobos(cv, x1 - 70, y1 - 90, 34, a, 9, False); mono(cv, x0 + 10, y1 - 100, 'DEIMOS flybys, 2nd half of mission', 22, SAND, a)

def sc_ledger(cv, t, p):
    sky(cv, t, 0.4)
    x0, y0, x1, y1 = CONT
    cols = [('KNOWN', GREEN, ['launch 04:41:03 JST Oct 20 (scheduled)', 'H3-24L, flight 10', '4,480 kg', '10 g minimum', '3 modules + Idefix'], 0.03),
            ('PUBLISHED PLAN', BLUE, ['arrive 2027', 'rover 2029', 'two soft landings, 2-3 h each', 'capsule 2031, Australia'], 0.3),
            ('OPEN', EMBER, ['landing year: 2029 (DLR) or 2030 (ESA)', 'how much of Phobos is Mars', 'where Phobos came from', 'what the ten grams say'], 0.5)]
    for i, (lab, col, items, f) in enumerate(cols):
        a = ap(t, lab and 's12', f)
        if L: bb = (x0 + i * 580, y0, x0 + i * 580 + 560, y1 - 90)
        else: bb = (x0, y0 + i * 262, x1, y0 + i * 262 + 250)
        card(cv, bb, a, col); chip(cv, bb[0] + 24, bb[1] + 22, lab, col, a, 24)
        for k, it in enumerate(items):
            aa = ap(t, 's12', f + 0.04 + k * 0.035)
            if L: cv.para(bb[0] + 24, bb[1] + 100 + k * 64, it, 'sans', 30, CREAM, 510, 1.2, 'l', aa)
            else:
                cx_ = bb[0] + 24 + (k % 2) * 490; cy_ = bb[1] + 80 + (k // 2) * 58
                cv.para(cx_, cy_, it, 'sans', 26, CREAM, 470, 1.15, 'l', aa)
    big(cv, x1 if L else x0 + 24, y1 - 60 if L else y1 - 36, 'the answer is in the dirt', 36, ORANGE, ap(t, 's12', 0.92), 'ra' if L else 'la')

SOURCES = [
    'JAXA press release 2026-08-20 + launch plan (jaxa20260820-1_01.pdf): 04:41:03 JST Oct 20 2026, H3 F10 (H3-24L), backup Oct 21-Nov 7, 4,480 kg, 3 modules, flight sequence, instrument list (P-SMP: NASA)',
    'ESA "Mars moon lander set to launch on 19 October" + ESA MMX factsheet: timeline (Mars Aug 2027, rover early 2029, landing 2030, return 2031), Idefix 25 kg / ~15 g on Phobos, instrument counts, firsts',
    'DLR MMX facts and figures: rover 2029, sampling 2029, return 2031; corer > 2 cm; Idefix 25 kg, ~1 mm/s, 100 days. DLR news 2026: release from ~40 m, rights itself. CNES MMX page: 2 cm, 10 g, 2031 Australia',
    'JAXA MMX site (mmx.jaxa.jp): 1-year cruise, QSO, 44 min round-trip radio, >= 10 g; science page: two soft landings, 2-3 h each, Deimos in the 2nd half, SHV 8K+4K with NHK. MMX News (R. Hyodo): the origin test. NASA/APL: MEGANE',
    'Hyodo et al. 2019 "Transport of impact ejecta from Mars to its moons" (arXiv 1912.12056): ~340 ppm statistical, ~760 ppm stochastic, >= ~34 grains in 10 g. Phobos size/orbit: NASA Science. Diagrams schematic']
def sc_close(cv, t, p):
    sky(cv, t, 0.8)
    x0, y0, x1, y1 = CONT
    end = SEG['s13']['start'] + SEG['s13']['dur'] - BOUND['s13'][0]
    ae = ease((t - end - 0.3) / 1.0)
    if ae < 1:
        a = 1 - ae
        if L:
            ground(cv, y1, 0.9 * a, (26, 30, 40)); rocket(cv, x1 - 240, y1 - 4, 560, a * ease(t / 1.0))
            rows = [('3:41 PM ET  ·  Oct 19', 'scheduled liftoff (04:41:03 JST Oct 20); JAXA streams it in English', 0.03), ('T + 2 min', 'solid boosters drop away', 0.3), ('T + 71 min', 'MMX released toward Mars, on its own', 0.45), ('then cruise', 'roughly a year to Mars; we will follow it here', 0.7)]
            for i, (b, s, f) in enumerate(rows):
                aa = ap(t, 's13', f) * a
                if aa <= 0: continue
                yy = y0 + 20 + i * 140
                cv.rect((x0, yy + 6, x0 + 5, yy + 110), mix(ORANGE, BG, aa)); big(cv, x0 + 22, yy, b, 48, CREAM, aa); cv.para(x0 + 22, yy + 60, s, 'sans', 26, DIM, 900, 1.2, 'l', aa)
        else:
            rows = [('3:41 PM ET · Oct 19', 'scheduled liftoff (04:41:03 JST Oct 20); JAXA streams it in English', 0.03), ('T + 2 min', 'solid boosters drop away', 0.3), ('T + 71 min', 'MMX released toward Mars', 0.45), ('then cruise', 'roughly a year to Mars; we follow it here', 0.7)]
            for i, (b, s, f) in enumerate(rows):
                aa = ap(t, 's13', f) * a
                if aa <= 0: continue
                yy = y0 + 20 + i * 150
                cv.rect((x0, yy + 6, x0 + 5, yy + 120), mix(ORANGE, BG, aa)); big(cv, x0 + 22, yy, b, 44, CREAM, aa); cv.para(x0 + 22, yy + 56, s, 'sans', 26, DIM, x1 - x0 - 40, 1.2, 'l', aa)
            ground(cv, y1, 0.9 * a, (26, 30, 40)); rocket(cv, x1 - 120, y1 - 4, 300, a * ease(t / 1.0))
    if ae > 0:
        y = 90 if PORT else 50
        mono(cv, HEAD[0], y, 'HEARTBEAT TV  /  CH 11', 26, ORANGE, ae)
        big(cv, HEAD[0], y + 36, 'SPACE NOW', 100, CREAM, ae)
        mono(cv, HEAD[0], y + 160, 'heartbeatobservatory.com', 32, ORANGE, ae)
        yy = y + 215
        mono(cv, HEAD[0], yy, 'SOURCES', 22, DIM, ae); yy += 34
        for i, s in enumerate(SOURCES):
            yy = cv.para(HEAD[0], yy, s, 'mono', 21 if PORT else 23, CREAM, (W - 2 * HEAD[0]) * (1 if PORT else 0.96), 1.22, 'l', ease((t - end - 0.5 - i * 0.15) / 0.8)) + 8

# (segment id, headline, source line, draw fn, mission-clock year)
SCENES = [
    ('s1', None, 'Status as of Oct 17, 2026. JAXA / ESA / DLR / CNES / NASA pages, see end card', sc_title, 2026.8),
    ('s2', 'when it flies', 'JAXA press release 2026-08-20 and launch plan jaxa20260820-1_01.pdf', sc_launch, 2026.8),
    ('s3', 'the first 71 minutes', 'JAXA launch plan, flight sequence for the Oct 20 (JST) case; event times shift on backup days', sc_ascent, 2026.8),
    ('s4', 'the ship', 'JAXA launch plan (4,480 kg, 3 modules, instrument list); ESA MMX factsheet; module drawing schematic', sc_craft, 2026.8),
    ('s5', 'why Phobos', 'NASA Science: Phobos; JAXA MMX science; ESA. Origin: both hypotheses under study (JAXA)', sc_phobos, None),
    ('s6', 'what ten grams can say', 'JAXA MMX science page (water, organics, origin); R. Hyodo, JAXA MMX News "Why explore the moons of Mars?" (the test)', sc_lab, None),
    ('s7', 'a bonus: pieces of Mars', 'Hyodo et al. 2019, arXiv 1912.12056 (model); grain count assumes 0.3 mm grains', sc_grains, None),
    ('s8', 'the plan, year by year', 'ESA launch article (Aug 2027, early 2029, 2030, 2031); DLR facts (2027, 2029, 2029, 2031); JAXA mission flow', sc_timeline, None),
    ('s9', 'the rover: Idefix', 'DLR facts and figures; DLR news 2026 (release ~40 m, rights itself, ~3 months); ESA (~15 g on Phobos)', sc_rover, 2029.1),
    ('s10', 'landing and sampling', 'JAXA MMX site (44 min, >= 10 g; science page: two soft landings, 2-3 h); JAXA MMX news (C-SMP, P-SMP); launch plan (P-SMP by NASA)', sc_landing, 2029.8),
    ('s11', 'what it measures', 'JAXA launch plan instrument list; ESA factsheet (SHV 4K/8K); NASA / JHU APL (MEGANE)', sc_instruments, 2028.0),
    ('s12', 'the ledger', 'Status as of Oct 17, 2026', sc_ledger, 2031.0),
    ('s13', 'what to watch', None, sc_close, 2026.8),
]

def _subs(text):
    out = []
    for s in re.split(r'(?<=[.?!])\s+', text.strip()):
        parts = [s]
        while True:
            nxt = []; changed = False
            for q in parts:
                if len(q) > 96:
                    cs = [m.end() for m in re.finditer(r'[,:;] ', q)]
                    if cs:
                        k = min(cs, key=lambda c: abs(c - len(q) / 2)); nxt += [q[:k].strip(), q[k:].strip()]; changed = True; continue
                nxt.append(q)
            parts = nxt
            if not changed: break
        out += parts
    return out
SUBS = {s['id']: _subs(s['text']) for s in TL['segs']}

bounds = []; BOUND = {}
for i, (sid, *_r) in enumerate(SCENES):
    s0 = 0.0 if i == 0 else SEG[sid]['start'] - 0.5
    s1 = TOTAL if i == len(SCENES) - 1 else SEG[SCENES[i + 1][0]]['start'] - 0.5
    bounds.append((s0, s1)); BOUND[sid] = (s0, s1)

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
    for i, (sid, head, src, fn, yr) in enumerate(SCENES):
        s0, s1 = bounds[i]
        if s0 <= tt < s1 or (i == len(SCENES) - 1 and tt >= s0): break
    t = tt - s0; p = clamp01(t / max(0.1, s1 - s0 - 0.6))
    fn(cv, t, p)
    endcard = sid == 's13' and t > SEG['s13']['start'] + SEG['s13']['dur'] - BOUND['s13'][0] + 0.3
    if not endcard:
        # top band: channel mark + mission clock
        mono(cv, HEAD[0], 24 if L else 60, 'SPACE NOW  ·  11.1', 20 if L else 22, ORANGE, 0.9)
        mono(cv, HEAD[0] + (230 if L else 250), 24 if L else 60, f'{i + 1:02d} / {len(SCENES):02d}', 20 if L else 22, DIM2, 0.9)
        if sid != 's8': rail(cv, RAIL[0], RAIL[2], RAIL[1], yr, 0.85)
        else: mono(cv, RAIL[2], RAIL[1] - 8, 'MISSION CLOCK', 18, DIM, 0.8, 'ra')
    if head and not endcard:
        a = ease(t / 0.6)
        f = font('head', SZ['head']); ls = wrap(head, f, HEAD[2] - HEAD[0])
        for k, l in enumerate(ls): cv.text((HEAD[0], HEAD[1] + k * SZ['head'] * 1.1), l, 'head', SZ['head'], CREAM, 'la', a)
        cv.rect((HEAD[0], HEAD[1] - 16, HEAD[0] + 54 * a, HEAD[1] - 12), mix(ORANGE, BG, a))
    sub = subtitle_at(sid, tt)
    if sub:
        f = font('sans', SZ['cap']); ls = wrap(sub, f, CAP[2] - CAP[0] - 40); n = len(ls)
        lh = SZ['cap'] * 1.28; y0 = CAP[1] + (CAP[3] - CAP[1] - n * lh) / 2 if L else CAP[1] + 10
        for k, l in enumerate(ls):
            tw = f.getlength(l) / SS
            cv.rect((W / 2 - tw / 2 - 18, y0 + k * lh + 4, W / 2 + tw / 2 + 18, y0 + (k + 1) * lh + 2), mix(BG, INK, 0.3), 6)
            cv.text((W / 2, y0 + k * lh), l, 'sans', SZ['cap'], CREAM, 'ma')
    if src and not endcard:
        a = ease(t / 1.2)
        f = font('mono', SZ['src']); ls = wrap(src, f, SRC[2] - SRC[0] - 110)[:3]
        cv.rect((SRC[0] - 16, SRC[1] - 10, SRC[2] + 16, SRC[1] + len(ls) * SZ['src'] * 1.25 + 8), mix(BG, INK, 0.5), 8)
        mono(cv, SRC[0], SRC[1], 'SOURCE', 17, ORANGE, a)
        for k, l in enumerate(ls): cv.text((SRC[0] + 100, SRC[1] + k * SZ['src'] * 1.25), l, 'mono', SZ['src'], DIM, 'la', a)
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
    pool = Pool(int(os.environ.get('TVPOOL', 8)))
    try:
        for k, buf in enumerate(pool.imap(work, range(a, b), chunksize=int(os.environ.get('TVCHUNK', 4)))):
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
