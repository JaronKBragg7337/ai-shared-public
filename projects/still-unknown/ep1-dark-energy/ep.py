# Heartbeat TV - Still Unknown ep.1 "The energy we can't explain yet"
# Own look (NOT the navy/gold/serif History-Science cards): near-black violet void, thin Segoe Light headlines in lowercase,
# Consolas data/sources, full-bleed expanding-universe simulation behind every scene, left-aligned lower-third captions,
# status tags MEASURED / INFERRED / NOT SETTLED / UNKNOWN, one real NASA image (HUDF 2014, public domain) with credit.
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
def hudf():
    global HUDF
    if HUDF is None:
        im = Image.open('assets-untrusted/hudf2014.jpg').convert('RGB')
        sw, sh = W * SS, H * SS; k = max(sw / im.width, sh / im.height)
        im = im.resize((int(im.width * k) + 1, int(im.height * k) + 1), Image.LANCZOS)
        x = (im.width - sw) // 2; y = (im.height - sh) // 2
        HUDF = im.crop((x, y, x + sw, y + sh))
    return HUDF

def paste_hudf(cv, a):
    if a <= 0: return
    im = hudf()
    dark = Image.blend(Image.new('RGB', im.size, BG), im, max(0.0, min(1.0, a)))
    cv.im.paste(dark); cv.d = ImageDraw.Draw(cv.im)

# ------------------------------------------------------------------ real-number helpers
C_KM = 299792.458
def dL(z, om, ol, h0=70.0):
    """luminosity distance in Mpc (flat or open), numeric integral"""
    ok = 1 - om - ol; zz = np.linspace(0, z, 200); E = np.sqrt(om * (1 + zz) ** 3 + ok * (1 + zz) ** 2 + ol)
    dc = C_KM / h0 * np.trapezoid(1 / E, zz)
    if abs(ok) < 1e-6: dm = dc
    elif ok > 0: dm = C_KM / h0 / math.sqrt(ok) * math.sinh(math.sqrt(ok) * dc * h0 / C_KM)
    else: dm = C_KM / h0 / math.sqrt(-ok) * math.sin(math.sqrt(-ok) * dc * h0 / C_KM)
    return (1 + z) * dm
def mu(z, om, ol): return 5 * math.log10(dL(z, om, ol) * 1e6 / 10)
ZS = np.linspace(0.01, 1.0, 60)
MODELS = {k: [mu(z, *v) for z in ZS] for k, v in dict(matter=(1.0, 0.0), empty=(0.0, 0.0), lcdm=(0.3, 0.7)).items()}
# illustrative points: scattered around the LCDM curve (NOT the published data points; screen says so)
RP = random.Random(3)
PTS = [(z, mu(z, 0.3, 0.7) + RP.gauss(0, 0.18)) for z in [RP.uniform(0.3, 0.97) for _ in range(22)] + [RP.uniform(0.02, 0.12) for _ in range(18)]]

def ia_lightcurve(d):
    """shape of a type Ia light curve (days from explosion), relative flux - illustrative template"""
    if d < 0: return 0.0
    return (1 - math.exp(-d / 6.0)) * (0.6 * math.exp(-max(0, d - 18) / 12.0) + 0.4 * math.exp(-max(0, d - 18) / 50.0))

# ------------------------------------------------------------------ scenes
def sc_title(cv, t, p):
    a = ease(t / 2.0)
    paste_hudf(cv, 0.55 * a * (1 - 0.35 * ease((t - 6) / 4)))
    y0 = 300 if PORT else 250
    mono(cv, HEAD[0], y0, 'HEARTBEAT TV  /  CH 10  /  STILL UNKNOWN  /  EP 01', 28 if PORT else 26, CYAN, ease(t / 1.0))
    sz = 92 if PORT else 118
    for k, l in enumerate(('the energy', "we can't", 'explain yet') if PORT else ('the energy', "we can't explain yet")):
        big(cv, HEAD[0], y0 + 60 + k * sz * 1.05, l, sz, TXT, ease((t - 0.3 - k * 0.25) / 1.2))
    # the 5% grid: 100 dots, five lit
    g0 = (HEAD[0], y0 + 60 + (3 if PORT else 2) * sz * 1.05 + 60); cell = 26 if PORT else 22; cols = 25 if not PORT else 20
    ua = ease((t - cue('s1', 2)) / 1.0)
    for i in range(100):
        cx = g0[0] + (i % cols) * cell + cell / 2; cy = g0[1] + (i // cols) * cell + cell / 2
        lit = i < 5
        if ua <= 0: break
        cv.circ((cx, cy), 5 if lit else 3.5, mix(CYAN if lit else DIM2, BG, ua * (1.0 if lit else 0.7)))
    gy = g0[1] + (100 // cols) * cell + 20
    mono(cv, HEAD[0], gy, 'everything we can see: about 5 of every 100', 24, CYAN, ua)
    mono(cv, HEAD[0], gy + 34, 'the other 95: dark matter + dark energy (inferred)', 24, DIM, ease((t - cue('s1', 3)) / 1.0))
    ub = ease((t - cue('s1', 5)) / 1.0)
    tag(cv, HEAD[0], gy + 90, 'MEASURED: THE SPEED-UP', MINT, ub)
    tag(cv, HEAD[0] + (0 if PORT else 290), gy + (140 if PORT else 90), 'NAMED: DARK ENERGY', VIO, ease((t - cue('s1', 6)) / 1.0))
    tag(cv, HEAD[0] + (0 if PORT else 520), gy + (190 if PORT else 90), 'WHAT IS IT: UNKNOWN', ROSE, ease((t - cue('s1', 7)) / 1.0))

def sc_hubble(cv, t, p):
    universe(cv, t, scale=0.9, dim=0.35)
    x0, y0, x1, y1 = CONT
    # left: observer with galaxies and arrows whose length grows with distance
    cx, cy = (W / 2, y0 + 250) if PORT else (x0 + 420, (y0 + y1) / 2 + 20)
    u = ease((t - cue('s2', 1)) / 1.5)
    cv.circ((cx, cy), 7, mix(TXT, BG, u)); mono(cv, cx, cy + 16, 'us', 22, DIM, u, 'ma')
    rr = random.Random(11)
    for i in range(14):
        ang = rr.uniform(0, 6.28); d = rr.uniform(70, 330 if not PORT else 210)
        px, py = cx + d * math.cos(ang), cy + d * math.sin(ang)
        v = d / 330 * 70 * ease((t - cue('s2', 2)) / 1.4)
        cv.circ((px, py), 5, mix(VIO, BG, u))
        if v > 1: cv.line([(px, py), (px + v * math.cos(ang), py + v * math.sin(ang))], mix(CYAN, BG, u), 3)
    cv.ring((cx, cy), 345 if not PORT else 225, mix(INK2, BG, u), 1)
    # right: v vs d line (Hubble's law) - schematic axes
    gx0, gy0, gx1, gy1 = (x0 + 60, y0 + 520, x1 - 60, y0 + 800) if PORT else (x0 + 900, y0 + 60, x1, y1 - 60)
    ug = ease((t - cue('s2', 2)) / 1.2)
    cv.line([(gx0, gy1), (gx1, gy1)], mix(DIM2, BG, ug), 2); cv.line([(gx0, gy1), (gx0, gy0)], mix(DIM2, BG, ug), 2)
    mono(cv, gx1, gy1 + 12, 'distance', 22, DIM, ug, 'ra'); mono(cv, gx0 - 8, gy0, 'speed away', 22, DIM, ug, 'ra' if not PORT else 'la')
    uu = ease((t - cue('s2', 2) - 0.3) / 1.6)
    cv.line([(gx0, gy1), (gx0 + (gx1 - gx0) * uu, gy1 - (gy1 - gy0) * 0.85 * uu)], mix(CYAN, BG, ug), 3)
    oy = 36 if PORT else 0
    mono(cv, gx0 + 20, gy0 + 10 + oy, 'v = H0 x d   (Hubble, 1929)', 24, CYAN, uu)
    mono(cv, gx0 + 20, gy0 + 44 + oy, 'farther away = moving away faster', 22, DIM, uu)
    uc = ease((t - cue('s2', 3)) / 1.0)
    mono(cv, gx0 + 20, gy0 + 78 + (36 if PORT else 0), 'distances from Cepheids (pulsing stars)', 22, DIM, uc)
    uq = ease((t - cue('s2', 4)) / 1.0)
    big(cv, gx0 + 20 if PORT else x0, (gy1 + 40) if PORT else y1 - 90, '1990s question: how fast is gravity slowing it?', 36 if PORT else 40, TXT, uq)
    tag(cv, x0 if not PORT else gx0 + 20, (gy1 + 100) if PORT else y1 - 30, 'MEASURED SINCE 1929', MINT, uq)

def sc_sn(cv, t, p):
    universe(cv, t, scale=1.0, dim=0.4)
    x0, y0, x1, y1 = CONT
    # a galaxy with a supernova flashing; light curve to the right
    gx, gy = (W / 2, y0 + 300) if PORT else (x0 + 380, (y0 + y1) / 2)
    u = ease((t - 0.3) / 1.2)
    rr = random.Random(5)
    for i in range(160):   # a spiral-ish blob of stars
        r = rr.uniform(0, 1) ** 0.5 * 170; th = rr.uniform(0, 6.283) + r * 0.012
        cv.circ((gx + r * math.cos(th) * 1.4, gy + r * math.sin(th) * 0.55), rr.uniform(1, 2.6), mix(TXT, BG, u * rr.uniform(0.2, 0.7)))
    d = (t - cue('s3', 1) + 0.4) * 12.0   # days since explosion, ~12 d/s
    f = ia_lightcurve(d)
    sx, sy = gx + 120, gy - 45
    if f > 0.02:
        for k in (3, 2, 1): cv.circ((sx, sy), 6 + 26 * f * k / 1.0, mix(TXT, BG, 0.18 * f))
        cv.circ((sx, sy), 5 + 7 * f, mix(TXT, BG, min(1, f * 1.2)))
    mono(cv, gx, gy + 130, 'a galaxy  /  one supernova  (simulated)', 22, DIM, u, 'ma')
    # light curve chart
    cx0, cy0, cx1, cy1 = (x0 + 60, y0 + 480, x1 - 60, y0 + 800) if PORT else (x0 + 820, y0 + 80, x1 - 20, y1 - 110)
    ug = ease((t - cue('s3', 1)) / 1.0)
    cv.line([(cx0, cy1), (cx1, cy1)], mix(DIM2, BG, ug), 2); cv.line([(cx0, cy1), (cx0, cy0)], mix(DIM2, BG, ug), 2)
    mono(cv, cx1, cy1 + 12, 'days', 22, DIM, ug, 'ra'); mono(cv, cx0 - 8 if not PORT else cx0 + 8, cy0, 'brightness', 22, DIM, ug, 'ra' if not PORT else 'la')
    pts = []
    for i in range(0, 120):
        dd = i;
        if dd > d: break
        pts.append((cx0 + dd / 120 * (cx1 - cx0), cy1 - ia_lightcurve(dd) * (cy1 - cy0) * 0.9))
    if len(pts) > 1: cv.line(pts, mix(CYAN, BG, ug), 3)
    hline(cv, cx0, cx1, cy1 - 0.9 * (cy1 - cy0), VIO, ug * 0.8, 1)
    mono(cv, cx0 + (170 if PORT else 14), cy1 - 0.9 * (cy1 - cy0) - 30, 'peak: nearly the same, after a fade-rate + color correction', 22, VIO, ease((t - cue('s3', 2)) / 1.0))
    uu = ease((t - cue('s3', 3)) / 1.0)
    big(cv, x0 if not PORT else cx0, (cy1 + 40) if PORT else y1 - 90, 'how faint it looks  =  how far away it is', 36 if PORT else 40, TXT, uu)
    tag(cv, x0 if not PORT else cx0, (cy1 + 100) if PORT else y1 - 30, 'STANDARDIZABLE CANDLE', MINT, uu)

def sc_diagram(cv, t, p):
    universe(cv, t, scale=1.1, accel=0.0006, dim=0.3)
    x0, y0, x1, y1 = CONT
    gx0, gy0, gx1, gy1 = (x0 + 70, y0 + 40, x1 - 40, y0 + 700) if PORT else (x0 + 90, y0 + 30, x0 + 1150, y1 - 50)
    ug = ease(t / 1.0)
    cv.line([(gx0, gy1), (gx1, gy1)], mix(DIM2, BG, ug), 2); cv.line([(gx0, gy1), (gx0, gy0)], mix(DIM2, BG, ug), 2)
    mono(cv, gx1, gy1 + 12, 'redshift z (how far back in time)', 22, DIM, ug, 'ra'); mono(cv, gx0 + 8, gy0 - 30, 'how faint (distance modulus)', 22, DIM, ug)
    mu_lo, mu_hi = 32.5, 45.0
    def P(z, m): return (gx0 + (z - 0.0) / 1.0 * (gx1 - gx0), gy1 - (m - mu_lo) / (mu_hi - mu_lo) * (gy1 - gy0))
    curves = [('matter', 'gravity only, slowing down (matter = 100%)', DIM, cue('s4', 0)), ('empty', 'coasting (empty universe)', DIM2, cue('s4', 0)),
              ('lcdm', 'speeding up (matter 30% + dark energy 70%)', CYAN, cue('s4', 3))]
    for key, lab, col, t0 in curves:
        uc = ease((t - t0) / 1.4)
        if uc <= 0: continue
        n = max(2, int(len(ZS) * uc)); pts = [P(z, m) for z, m in zip(ZS[:n], MODELS[key][:n])]
        cv.line(pts, mix(col, BG, 0.9), 3 if key == 'lcdm' else 2)
        ly = gy0 + 20 + ['matter', 'empty', 'lcdm'].index(key) * 30
        cv.line([(gx0 + 30, ly + 10), (gx0 + 70, ly + 10)], mix(col, BG, uc), 3); mono(cv, gx0 + 84, ly, lab, 20, col, uc)
    up = ease((t - cue('s4', 1)) / 1.5)
    for i, (z, m) in enumerate(PTS):
        a = ease((t - cue('s4', 1) - i * 0.05) / 0.5)
        if a > 0: cv.circ(P(z, m), 5, mix(TXT, BG, a)); cv.ring(P(z, m), 9, mix(TXT, BG, a * 0.3), 1)
    mono(cv, gx0 + 10, gy1 - 30, 'points: illustration of the pattern, not the published data', 20, DIM, up)
    ua = ease((t - cue('s4', 2)) / 1.0)
    big(cv, gx1 + 40 if not PORT else gx0, gy0 + 60 if not PORT else gy1 + 50, 'fainter', 60 if not PORT else 52, ROSE, ua)
    big(cv, gx1 + 40 if not PORT else gx0 + 220, gy0 + 130 if not PORT else gy1 + 50, '= farther', 60 if not PORT else 52, TXT, ua)
    ub = ease((t - cue('s4', 4)) / 1.0)
    big(cv, gx1 + 40 if not PORT else gx0, gy0 + 260 if not PORT else gy1 + 120, 'not slowing.', 48, DIM, ub)
    big(cv, gx1 + 40 if not PORT else gx0 + 330, gy0 + 320 if not PORT else gy1 + 120, 'speeding up.', 48, CYAN, ease((t - cue('s4', 5)) / 1.0))
    tag(cv, gx1 + 40 if not PORT else gx0, gy0 + 410 if not PORT else gy1 + 190, 'MEASURED 1998', MINT, ease((t - cue('s4', 5)) / 1.0))

def sc_teams(cv, t, p):
    universe(cv, t, scale=1.2, accel=0.0006, dim=0.3)
    x0, y0, x1, y1 = CONT
    rows = [('1998', 'High-z Supernova Search Team', 'Schmidt (team lead), Riess (1998 analysis) and colleagues  /  16 distant supernovae', cue('s5', 0)),
            ('1999', 'Supernova Cosmology Project', 'Perlmutter and colleagues  /  42 distant supernovae', cue('s5', 1)),
            ('2011', 'Nobel Prize in Physics', 'Perlmutter, Schmidt, Riess: "the accelerating expansion of the Universe"', cue('s5', 2))]
    ty = y0 + 40; step = (y1 - y0 - 40) / 3
    for i, (yr, a1, a2, t0) in enumerate(rows):
        u = ease((t - t0) / 0.9)
        if u <= 0: continue
        yy = ty + i * step
        hline(cv, x0, x1, yy, INK2, u, 1)
        mono(cv, x0, yy + 18, yr, 54 if PORT else 64, CYAN, u)
        big(cv, x0 + (190 if PORT else 240), yy + 14, a1, 44 if PORT else 52, TXT, u)
        cv.para(x0 + (190 if PORT else 240), yy + (70 if PORT else 84), a2, 'mono', 22 if PORT else 24, DIM, x1 - x0 - (190 if PORT else 240), 1.3, 'l', u)
    tag(cv, x0, y1 - 10, 'MEASURED  /  INDEPENDENTLY, TWICE', MINT, ease((t - cue('s5', 2)) / 1.0))

def sc_lambda(cv, t, p):
    accel = 0.0 if t < cue('s6', 4) else 0.0025 * ease((t - cue('s6', 4)) / 2)
    universe(cv, t, scale=1.0, accel=accel, dim=0.45)
    x0, y0, x1, y1 = CONT
    u = ease(t / 1.0)
    big(cv, x0, y0 + 20, 'dark energy', 72 if PORT else 84, TXT, u)
    mono(cv, x0, y0 + (110 if PORT else 125), 'a name for whatever pushes. not an explanation.', 24, DIM, u)
    u2 = ease((t - cue('s6', 1)) / 1.0)
    ey = y0 + (300 if PORT else 250)
    f = font('light', 64 if PORT else 76)
    parts = [('G', TXT), ('\u03bc\u03bd', DIM), ('  +  ', DIM), ('\u039b', CYAN), (' g', TXT), ('\u03bc\u03bd', DIM), ('  =  ', DIM), ('8\u03c0G/c\u2074 \u00b7 T', TXT), ('\u03bc\u03bd', DIM)]
    xx = x0
    for s, c in parts:
        cv.text((xx, ey), s, 'light', 64 if PORT else 76, c, 'la', u2); xx += f.getlength(s) / SS
    mono(cv, x0, ey + (90 if PORT else 100), 'Einstein 1917: \u039b (lambda), the cosmological constant', 24, DIM, u2)
    u3 = ease((t - cue('s6', 3)) / 1.0)
    yy = ey + (190 if PORT else 160)
    for k, l in enumerate(('an energy of empty space itself', 'the same everywhere', 'the same at all times')):
        big(cv, x0, yy + k * (54 if PORT else 56), l, 40 if PORT else 46, TXT, ease((t - cue('s6', 3) - k * 0.3) / 0.9))
    u4 = ease((t - cue('s6', 4)) / 1.0)
    tag(cv, x0, y1 - 10, 'SIMPLEST MODEL  /  FITS THE SUPERNOVAE', MINT, u4)
    tag(cv, x0 + (0 if PORT else 560), y1 - (60 if PORT else 10), 'WHAT \u039b IS: UNKNOWN', ROSE, ease((t - cue('s6', 4) - 0.6) / 1.0))

def sc_shares(cv, t, p):
    universe(cv, t, scale=1.3, accel=0.0006, dim=0.25)
    x0, y0, x1, y1 = CONT
    cols = 10; cell = (58 if PORT else 52)
    g0 = (x0 + (40 if PORT else 0), y0 + (40 if PORT else 30))
    shares = [(68, VIO, 'dark energy', '68%', cue('s7', 1)), (27, DIM, 'dark matter', '27%', cue('s7', 2)), (5, CYAN, 'ordinary matter', '5%', cue('s7', 3))]
    i = 0
    for n, col, lab, pct, t0 in shares:
        for k in range(n):
            a = ease((t - t0 - k * 0.012) / 0.4)
            cx = g0[0] + (i % cols) * cell + cell / 2; cy = g0[1] + (i // cols) * cell + cell / 2
            cv.circ((cx, cy), cell * 0.3, mix(col, BG, a * (0.5 if col is DIM else 0.95)))
            i += 1
    lx = x0 + (660 if PORT else cols * cell + 120); ly = y0 + (60 if PORT else 60)
    for k, (n, col, lab, pct, t0) in enumerate(shares):
        u = ease((t - t0) / 0.8)
        yy = ly + k * (190 if PORT else 120)
        mono(cv, lx, yy, pct, 64 if PORT else 80, col, u)
        big(cv, lx + (0 if PORT else 240), yy + (80 if PORT else 22), lab, 36 if PORT else 50, TXT, u)
    uu = ease((t - cue('s7', 4)) / 1.0)
    mono(cv, x0 + 40 if PORT else lx, ly + (620 if PORT else 380), 'Planck 2018: \u03a9\u039b 0.685, \u03a9m 0.315, baryons 0.049  (flat \u039bCDM fit)', 22, DIM, uu)
    tag(cv, x0 + 40 if PORT else lx, ly + (665 if PORT else 425), 'INFERRED THROUGH A MODEL', VIO, uu)

H0 = [('Planck 2018  (oldest light, CMB)', 67.4, 0.5, 0.5, VIO, 'early'),
      ('DESI DR2 + BBN  (galaxy map, 2025)', 68.5, 0.6, 0.6, VIO, 'early'),
      ('CCHP 2025  (HST+JWST, red giant stars)', 70.4, 1.9, 1.9, DIM, 'late'),
      ('SH0ES 2022  (Cepheids + supernovae)', 73.0, 1.0, 1.0, CYAN, 'late'),
      ('H0DN 2026, A&A  (local distance network)', 73.5, 0.8, 0.8, CYAN, 'late')]
def sc_tension(cv, t, p):
    universe(cv, t, scale=1.4, accel=0.0006, dim=0.25)
    x0, y0, x1, y1 = CONT
    u = ease(t / 1.0)
    big(cv, x0, y0 + 10, 'H0  the expansion rate today', 56 if PORT else 64, TXT, u)
    mono(cv, x0, y0 + (80 if PORT else 100), 'km/s per megaparsec  /  each bar = one team, with its error bar', 22, DIM, u)
    ax0, ax1 = (x0 + 30, x1 - 30) if PORT else (x0 + 560, x1 - 40)
    ay = y0 + (260 if PORT else 170); lo, hi = 64.0, 77.0
    X = lambda v: ax0 + (v - lo) / (hi - lo) * (ax1 - ax0)
    ug = ease((t - cue('s8', 1)) / 1.0)
    for v in range(65, 78):
        cv.line([(X(v), ay), (X(v), ay + 8)], mix(DIM2, BG, ug), 2); mono(cv, X(v), ay - 30, str(v), 20, DIM, ug, 'ma')
    hline(cv, ax0, ax1, ay, DIM2, ug, 2)
    step = (90 if PORT else 100)
    for i, (lab, v, em, ep_, col, kind) in enumerate(H0):
        t0 = cue('s8', 2 if kind == 'early' else 3) + (i % 2) * 0.35
        a = ease((t - t0) / 0.8)
        if a <= 0: continue
        yy = ay + 60 + i * step
        if PORT:
            mono(cv, ax0, yy - 34, lab, 21, TXT, a)
        else:
            mono(cv, x0, yy - 6, lab, 23, TXT, a, 'la')
        cv.line([(X(v - em), yy + 10), (X(v + ep_), yy + 10)], mix(col, BG, a * 0.8), 6)
        cv.circ((X(v), yy + 10), 11, mix(col, BG, a)); mono(cv, X(v), yy + 28, f'{v:.1f}', 22, col, a, 'ma')
    uq = ease((t - cue('s8', 4)) / 1.0)
    if PORT:
        ly = ay + 60 + len(H0) * step + 10
        big(cv, x0, ly, 'the error bars do not overlap', 44, ROSE, uq)
        tag(cv, x0, ly + 70, 'THE HUBBLE TENSION  /  NOT RESOLVED (OCT 2026)', ROSE, ease((t - cue('s8', 5)) / 1.0))
    else:   # land: the five rows fill the height, so the verdict sits top-right beside the H0 heading
        big(cv, x0 + 940, y0 + 22, 'the error bars do not overlap', 44, ROSE, uq)
        tag(cv, x0 + 940, y0 + 86, 'THE HUBBLE TENSION  /  NOT RESOLVED (OCT 2026)', ROSE, ease((t - cue('s8', 5)) / 1.0))

def sc_matters(cv, t, p):
    universe(cv, t, scale=1.45, accel=0.0008, dim=0.3)
    x0, y0, x1, y1 = CONT
    gx0, gy0, gx1, gy1 = (x0 + 70, y0 + 60, x1 - 40, y0 + 640) if PORT else (x0 + 80, y0 + 40, x0 + 1100, y1 - 70)
    ug = ease(t / 1.0)
    cv.line([(gx0, gy1), (gx1, gy1)], mix(DIM2, BG, ug), 2); cv.line([(gx0, gy1), (gx0, gy0)], mix(DIM2, BG, ug), 2)
    mono(cv, gx1, gy1 + 12, 'time  (now = the dot)', 22, DIM, ug, 'ra'); mono(cv, gx0 + 8, gy0 - 30, 'size of the universe (scale factor)', 22, DIM, ug)
    nowx = gx0 + (gx1 - gx0) * 0.42
    def curve(kind, col, t0, lab):
        u = ease((t - t0) / 1.6)
        if u <= 0: return
        pts = []
        for i in range(0, int(120 * u) + 1):
            s = i / 120.0; x = gx0 + s * (gx1 - gx0)
            # schematic: past = decelerating power law, future = exponential (constant) or softened (weakening)
            tau = (s - 0.42) / 0.58
            if s <= 0.42: a = 0.15 + 0.85 * (s / 0.42) ** 0.75
            else: a = 1.0 + (math.exp(2.2 * tau) - 1) * (1.0 if kind == 'const' else 0.55) * (1 if kind == 'const' else 1 - 0.25 * tau)
            pts.append((x, gy1 - min(0.98, a / 9.5) * (gy1 - gy0)))
        cv.line(pts, mix(col, BG, 0.9), 3)
        if u >= 1: mono(cv, pts[-1][0] - 10, pts[-1][1] - 30, lab, 22, col, 1, 'ra')
    curve('const', VIO, cue('s8b', 1), 'constant: speeds up forever')
    curve('weak', CYAN, cue('s8b', 3), 'weakening: a different future')
    cv.circ((nowx, gy1 - 1.0 / 9.5 * (gy1 - gy0)), 9, mix(TXT, BG, ug)); mono(cv, nowx, gy1 - 1.0 / 9.5 * (gy1 - gy0) + 20, 'now', 22, TXT, ug, 'ma')
    u2 = ease((t - cue('s8b', 2)) / 1.0)
    big(cv, gx1 + 40 if not PORT else gx0, gy0 + 40 if not PORT else gy1 + 70, 'galaxies slip', 48, TXT, u2)
    big(cv, gx1 + 40 if not PORT else gx0, gy0 + 100 if not PORT else gy1 + 130, 'out of sight', 48, TXT, u2)
    u3 = ease((t - cue('s8b', 4)) / 1.0)
    mono(cv, gx1 + 40 if not PORT else gx0, gy0 + 220 if not PORT else gy1 + 200, 'invisible in a lifetime', 24, DIM, u3)
    mono(cv, gx1 + 40 if not PORT else gx0, gy0 + 254 if not PORT else gy1 + 234, 'visible when millions of galaxies are combined', 24, CYAN, ease((t - cue('s8b', 5)) / 1.0))
    tag(cv, gx1 + 40 if not PORT else gx0, gy0 + 320 if not PORT else gy1 + 290, 'WHICH FUTURE: NOT SETTLED', ROSE, ease((t - cue('s8b', 5)) / 1.0))

def sc_desi(cv, t, p):
    universe(cv, t, scale=1.5, accel=0.0006, dim=0.2)
    x0, y0, x1, y1 = CONT
    # a wedge of the 3D map: points in a fan, depth = distance
    u = ease(t / 1.5)
    ax, ay = (W / 2, y0 + 560) if PORT else (x0 + 520, y1 - 20)
    rr = random.Random(21); n = int(1400 * u)
    for i in range(n):
        rad = rr.uniform(0.05, 1.0) ** 0.6 * (520 if PORT else 560); th = rr.uniform(-0.62, 0.62) - math.pi / 2
        clump = 1 + 0.6 * math.sin(rad * 0.06 + th * 9)
        px, py = ax + rad * math.cos(th), ay + rad * math.sin(th)
        cv.circ((px, py), rr.uniform(1, 2.4) * clump, mix(CYAN if rr.random() < 0.15 else TXT, BG, rr.uniform(0.25, 0.8) * u))
    mono(cv, ax, ay + 14, 'DESI  /  one slice of a 3D map  (simulated look, not the catalogue)', 20, DIM, u, 'ma')
    lx = x0 + (20 if PORT else 1080); ly = y0 + (610 if PORT else 20)
    u1 = ease((t - cue('s9', 1)) / 1.0)
    mono(cv, lx, ly, '> 14 million', 56 if PORT else 64, CYAN, u1)
    big(cv, lx, ly + (66 if PORT else 76), 'galaxies and quasars, in 3D', 36 if PORT else 40, TXT, u1)
    u2 = ease((t - cue('s9', 2)) / 1.0)
    big(cv, lx, ly + (150 if PORT else 170), 'March 2025: a hint that dark', 36 if PORT else 40, TXT, u2)
    big(cv, lx, ly + (196 if PORT else 220), 'energy weakens over time', 36 if PORT else 40, TXT, u2)
    u3 = ease((t - cue('s9', 3)) / 1.0)
    mono(cv, lx, ly + (270 if PORT else 300), '2.8 to 4.2 sigma  (depends on the data combined)', 24, VIO, u3)
    tag(cv, lx, ly + (320 if PORT else 350), 'HINT  /  NOT A DISCOVERY', VIO, u3)

def sc_sigma(cv, t, p):
    universe(cv, t, scale=1.6, accel=0.0006, dim=0.2)
    x0, y0, x1, y1 = CONT
    u = ease(t / 1.0)
    big(cv, x0, y0 + 10, 'how sure is sure?', 56 if PORT else 64, TXT, u)
    ax0, ax1 = x0 + 20, x1 - 40; ay = y0 + (200 if PORT else 160)
    X = lambda s: ax0 + s / 6.0 * (ax1 - ax0)
    hline(cv, ax0, ax1, ay, DIM2, u, 2)
    for s in range(0, 7):
        cv.line([(X(s), ay), (X(s), ay + 10)], mix(DIM2, BG, u), 2); mono(cv, X(s), ay + 20, f'{s}\u03c3', 22, DIM, u, 'ma')
    cv.line([(X(5), ay - 70), (X(5), ay + 10)], mix(MINT, BG, u), 3); mono(cv, X(5) + 10, ay - 70, 'discovery: 5\u03c3', 24, MINT, u)
    u1 = ease((t - cue('s10', 0) + 0.5) / 1.0)
    cv.rect((X(2.8), ay - 34, X(4.2), ay - 6), mix(VIO, BG, u1 * 0.9))
    mono(cv, X(3.5), ay - 64, 'DESI DR2, Mar 2025', 22, VIO, u1, 'ma')
    u2 = ease((t - cue('s10', 2)) / 1.2)
    ax2 = ay + (150 if PORT else 110)
    cv.circ((X(1.0), ax2), 10, mix(CYAN, BG, u2)); cv.line([(X(3.5), ax2), (X(1.0) + 14, ax2)], mix(CYAN, BG, u2 * 0.7), 2)
    mono(cv, X(1.0), ax2 + 22, 'DESI Ly\u03b1, Jul 2026: shifts back toward \u039b (constant)', 22, CYAN, u2, 'la')
    mono(cv, X(1.0), ax2 + 50, 'position illustrative: the paper gives no sigma', 20, DIM, u2, 'la')
    u3 = ease((t - cue('s10', 4)) / 1.0)
    ty = ax2 + (160 if PORT else 130)
    for k, (yr, txt) in enumerate((('2021-2026', 'planned five-year survey, finished April 2026'), ('2027', 'full-dataset results expected'))):
        a = ease((t - cue('s10', 4) - k * 0.5) / 1.0)
        mono(cv, x0, ty + k * 70, yr, 36, CYAN, a); big(cv, x0 + (240 if PORT else 300), ty + k * 70 - 2, txt, 34 if PORT else 38, TXT, a)
    tag(cv, x0, y1 - 10, 'CONSTANT OR CHANGING: NOT SETTLED', ROSE, u3)

LEDGER = [('MEASURED', MINT, 'the expansion is speeding up', 1), ('MEASURED / MODEL', MINT, 'the shares: 68 / 27 / 5', 2),
          ('NOT SETTLED', ROSE, 'constant, or changing over time', 3), ('NOT SETTLED', ROSE, 'why the two expansion rates disagree', 4),
          ('UNKNOWN', ROSE, 'what dark energy actually is', 5)]
def sc_ledger(cv, t, p):
    universe(cv, t, scale=1.7, accel=0.0006, dim=0.2)
    x0, y0, x1, y1 = CONT
    big(cv, x0, y0 + 10, 'the ledger', 56 if PORT else 64, TXT, ease(t / 1.0))
    step = (150 if PORT else 112)
    for i, (st, col, txt, k) in enumerate(LEDGER):
        a = ease((t - cue('s11', k)) / 0.8)
        if a <= 0: continue
        yy = y0 + (110 if PORT else 110) + i * step
        hline(cv, x0, x1, yy, INK2, a, 1)
        tag(cv, x0, yy + 16, st, col, a, 22)
        big(cv, x0 + (0 if PORT else 360), yy + (70 if PORT else 10), txt, 40 if PORT else 46, TXT, a)

def sc_candidates(cv, t, p):
    universe(cv, t, scale=1.8, accel=0.0008, dim=0.3)
    x0, y0, x1, y1 = CONT
    cands = [('\u039b', 'the energy of empty space', 'a constant', 1), ('\u03c6', 'a slowly changing field', '"quintessence"', 2), ('G?', 'gravity that behaves differently', 'at the largest scales', 3)]
    n = 3
    for i, (sym, a1, a2, k) in enumerate(cands):
        a = ease((t - cue('s12', k) + 0.6) / 0.9)
        if a <= 0: continue
        if PORT:
            yy = y0 + i * 230; mono(cv, x0, yy, sym, 90, VIO, a); big(cv, x0 + 160, yy + 10, a1, 40, TXT, a); mono(cv, x0 + 160, yy + 66, a2, 24, DIM, a)
            hline(cv, x0, x1, yy + 190, INK2, a, 1)
        else:
            cw = (x1 - x0) / n; cx = x0 + i * cw
            cv.line([(cx, y0 + 20), (cx, y0 + 330)], mix(INK2, BG, a), 1)
            mono(cv, cx + 30, y0 + 30, sym, 110, VIO, a); big(cv, cx + 30, y0 + 190, a1, 36, TXT, a); mono(cv, cx + 30, y0 + 245, a2, 24, DIM, a)
    u0 = ease((t - cue('s12', 4)) / 1.0)
    yy = y0 + (720 if PORT else 400)
    mono(cv, x0, yy - 40, 'each predicts a different expansion history: that is what the surveys measure', 22, DIM, u0)
    u = ease((t - cue('s12', 6)) / 1.0)
    big(cv, x0, yy, 'none has passed the test yet', 44 if PORT else 52, TXT, u)
    u2 = ease((t - cue('s12', 7)) / 1.0)
    tag(cv, x0, yy + (80 if PORT else 90), 'NOT ESTABLISHED', ROSE, u2); tag(cv, x0 + (280 if PORT else 290), yy + (80 if PORT else 90), 'NOT RULED OUT', MINT, ease((t - cue('s12', 8)) / 1.0))
    u3 = ease((t - cue('s12', 9)) / 1.2)
    big(cv, x0, yy + (170 if PORT else 180), 'someone watching this might be the one who finds out.', 36 if PORT else 42, CYAN, u3)

SOURCES = ['Hubble 1929, PNAS 15, 168', 'Riess et al. 1998, AJ 116, 1009  /  Perlmutter et al. 1999, ApJ 517, 565', 'Nobel Prize in Physics 2011, nobelprize.org',
           'Einstein 1917, Sitzungsberichte (cosmological constant)', 'Planck 2018 results VI, A&A 641, A6 (2020)',
           'Riess et al. 2022, ApJL 934, L7 (SH0ES 73.04 +/- 1.04)  /  Freedman et al. 2025, ApJ, doi:10.3847/1538-4357/adce78 (CCHP 70.39 +/- 1.94)', 'H0DN 2026, A&A (arXiv:2510.23823): 73.50 +/- 0.81  /  DESI DR2 Results II Table V: 68.51 +/- 0.58  /  Cai & Wang 2026, arXiv:2606.20434 (review)',
           'DESI DR2 Results II, arXiv:2503.14738; LBL news 19 Mar 2025 (2.8-4.2 sigma)', 'DESI Ly-alpha full-shape key paper, arXiv:2607.27410; desi.lbl.gov 30 Jul 2026',
           'Ohio State / ScienceDaily 28 Apr 2026 (survey complete; results 2027)', 'Image: Hubble Ultra Deep Field 2014. Credit: NASA, ESA, H. Teplitz and M. Rafelski (IPAC/Caltech), A. Koekemoer (STScI), R. Windhorst (ASU), Z. Levay (STScI)']
def sc_end(cv, t, p):
    paste_hudf(cv, 0.35 * ease(t / 2.0))
    a = ease(t / 1.0)
    y = 200 if PORT else 90
    mono(cv, HEAD[0], y, 'HEARTBEAT TV  /  CH 10', 26, CYAN, a)
    big(cv, HEAD[0], y + 40, 'still unknown', 110 if PORT else 128, TXT, a)
    mono(cv, HEAD[0], y + (180 if PORT else 200), 'heartbeatobservatory.com', 34, CYAN, a)
    yy = y + (260 if PORT else 280)
    mono(cv, HEAD[0], yy, 'SOURCES', 22, DIM, ease((t - 0.6) / 1)); yy += 40
    for i, s in enumerate(SOURCES):
        yy = cv.para(HEAD[0], yy, s, 'mono', 21 if PORT else 22, TXT, W - 2 * HEAD[0], 1.25, 'l', ease((t - 0.8 - i * 0.15) / 0.8)) + 10

# (segment id, headline, source line, draw fn)
SCENES = [
    ('s1', None, 'Image: NASA, ESA, H. Teplitz, M. Rafelski, A. Koekemoer, R. Windhorst, Z. Levay (HUDF 2014). 5% = Planck 2018: ordinary matter ~4.9%', sc_title),
    ('s2', 'the universe is expanding', 'Hubble 1929, PNAS 15, 168 (velocity-distance relation)', sc_hubble),
    ('s3', 'a candle with a known brightness', 'Type Ia supernovae: Riess et al. 1998; Perlmutter et al. 1999', sc_sn),
    ('s4', 'what the two teams saw', 'Riess et al. 1998, AJ 116, 1009 / Perlmutter et al. 1999, ApJ 517, 565. Curves computed from flat/open FRW models', sc_diagram),
    ('s5', 'who measured it', 'Riess+ 1998 (16 SNe); Perlmutter+ 1999 (42 SNe); nobelprize.org 2011', sc_teams),
    ('s6', 'the simplest answer: a constant', 'Einstein 1917; NASA science.nasa.gov/dark-energy', sc_lambda),
    ('s7', 'what the universe is made of', 'Planck 2018 results VI, A&A 641, A6 (2020): flat LCDM fit', sc_shares),
    ('s8', 'the first crack', 'Planck 2018 (67.4+/-0.5); DESI DR2 Table V (68.51+/-0.58); Freedman+ 2025 ApJ (70.39+/-1.94); Riess+ 2022 (73.04+/-1.04); H0DN 2026 A&A (73.50+/-0.81)', sc_tension),
    ('s8b', 'why it matters', 'Illustration: scale factor a(t) for a constant vs a weakening dark energy; shapes schematic, not a forecast', sc_matters),
    ('s9', 'a 3D map of 14 million galaxies', 'DESI DR2 Results II, arXiv:2503.14738; LBL news 19 Mar 2025', sc_desi),
    ('s10', 'a hint, then a wobble', 'DESI Ly-alpha key paper, desi.lbl.gov 30 Jul 2026 (arXiv:2607.27410); Ohio State 28 Apr 2026', sc_sigma),
    ('s11', 'known vs unknown', 'Status as of October 2026', sc_ledger),
    ('s12', 'what it could be', 'Candidate models: see Planck 2018 VI sec. 7; Cai & Wang 2026. None confirmed.', sc_candidates),
    ('s13', None, None, sc_end),
]
SUBS = {
 's1': ['Everything we can see. Every star, every galaxy, every atom of you.', 'It all adds up to about five percent of the universe.', 'The rest is dark.', 'And the largest share of that dark is something that pushes.', 'We measured the push.', 'We named its cause: dark energy.', 'We still do not know what it is.'],
 's2': ['Start with what was measured.', "We have known since 1929, from Edwin Hubble's work, that the universe is expanding:", 'the farther away a galaxy is, the faster it moves away from us.', 'Hubble measured those distances with Cepheids, pulsing stars whose rhythm reveals their true brightness.', 'The big question in the 1990s was how fast gravity was slowing that expansion down.'],
 's8b': ['Why does any of this matter?', 'If dark energy is a true constant, the expansion keeps speeding up forever,', 'and distant galaxies slip out of sight one by one.', 'If it weakens, that future changes.', 'The difference is far too small to notice in a human lifetime.', 'It only shows up when you combine measurements of millions of galaxies across a whole survey.'],
 's3': ['In 1998, two teams of astronomers were watching a special kind of exploding star, a type Ia supernova.', 'Once you correct for how fast each one fades, and its color, these explosions reach nearly the same peak brightness.', 'So how faint one looks tells you how far away it is.'],
 's4': ['Both teams expected the far-off supernovae to look a little brighter than a plain expanding universe would predict,', 'because gravity should have been slowing things down.', 'They looked fainter. Farther away than they should be.', 'The expansion of the universe is not slowing down.', 'It is speeding up.'],
 's5': ['The High-z team, led by Brian Schmidt, with Adam Riess leading the 1998 analysis, published sixteen distant supernovae that year.', "Saul Perlmutter's Supernova Cosmology Project published forty-two in 1999.", 'The 2011 Nobel Prize in Physics went to all three, for the discovery of the accelerating expansion of the universe.'],
 's6': ['Whatever drives it got a name: dark energy.', 'The simplest version is a number Einstein wrote into his equations in 1917 and later regretted.', 'The cosmological constant.', 'An energy of empty space itself, the same everywhere, the same at all times.', 'Put it back into the equations, and the supernova measurements fit.'],
 's7': ["Measured by the Planck satellite's map of the oldest light,", 'dark energy makes up about 68 percent of the energy in the universe today.', 'Dark matter, about 27 percent.', 'Ordinary matter, about five.', 'Those shares are inferred through a model, not weighed on a scale.'],
 's8': ['Here is the first crack. The expansion rate today is called the Hubble constant.', 'Measure it from the oldest light, and you get about 67 kilometers per second per megaparsec.', 'Measure it from nearby exploding stars and pulsing stars, and you get about 73.', 'The error bars do not overlap.', 'This is the Hubble tension,', 'and as of October 2026, it is not resolved.'],
 's9': ['Then came DESI, an instrument on a telescope in Arizona', 'that mapped nearly fifteen million galaxies and quasars in three dimensions.', 'In March 2025, combined with other data, it found a preference for dark energy that changes over time, weakening as the universe ages.', 'The strength of that hint: between 2.8 and 4.2 sigma, depending on which data you combine.'],
 's10': ['Physics calls a result a discovery at five sigma. This is not there yet.', 'And in July 2026, a new DESI analysis of the hydrogen gas between galaxies', 'shifted back toward the constant, the simple Einstein version.', 'Both results come from the same project.', 'DESI finished its planned five-year survey in April 2026.', 'Results from the full dataset are expected in 2027.'],
 's11': ['So here is the ledger.', 'Measured: the expansion is speeding up.', 'Measured, through a model: the shares of dark energy, dark matter, and ordinary matter.', 'Not settled: whether dark energy is constant or changing.', 'Not settled: why the two expansion rates disagree.', 'Unknown: what dark energy actually is.'],
 's12': ['The candidates on the table:', 'the energy of empty space,', 'a slowly changing field,', 'or gravity that behaves differently at the largest scales.', 'Each one predicts a slightly different history of the expansion.', 'That is exactly what DESI and the next surveys are built to measure.', 'None has passed the test yet.', 'Could it ever be understood, or used? Not established.', 'Not ruled out.', 'Someone watching this might be the one who finds out.'],
 's13': ['Still Unknown, from Heartbeat Observatory.'],
}

# ------------------------------------------------------------------ framework
bounds = []
for i, (sid, *_r) in enumerate(SCENES):
    s0 = 0.0 if i == 0 else SEG[sid]['start'] - 0.5
    s1 = TOTAL if i == len(SCENES) - 1 else SEG[SCENES[i + 1][0]]['start'] - 0.5
    bounds.append((s0, s1))
BOUND = {sid: b for (sid, *_r), b in zip(SCENES, bounds)}

def cue(sid, k):
    subs = SUBS[sid]; tot = sum(len(s) for s in subs); acc = sum(len(s) for s in subs[:k])
    return SEG[sid]['start'] + acc / tot * SEG[sid]['dur'] - BOUND[sid][0]

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
    # left rail: channel mark + chapter counter (vertical, mono)
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
    pool = Pool(10)
    try:
        for k, buf in enumerate(pool.imap(work, range(a, b), chunksize=4)):
            ff.stdin.write(buf)
            if k % 600 == 0: print(k, '/', b - a, flush=True)
        pool.close(); pool.join()
    except Exception as e:
        print('pool error (frames written so far are kept):', repr(e), flush=True)
    finally:
        # always finish the mp4 (moov atom) even if the pool teardown throws on Windows
        try: ff.stdin.close()
        except Exception: pass
        ff.wait(); print('ffmpeg exit', ff.returncode, flush=True)

if __name__ == '__main__': main()
