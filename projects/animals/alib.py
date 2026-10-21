# Animals look (Heartbeat TV ch 19), derived from the Open Questions look (ch 9): warm dark, TWO-SIDES split screen (coral = one answer, teal = the other),
# live voice waveform behind the captions, Constantia/Corbel type. Built on tv-lib's Cv + animation helpers, with the
# History/Science navy+gold palette replaced. Import this FIRST in an episode file:  from oqlib import *
import sys, os, math, wave
import numpy as np
sys.path.insert(0, 'C:/Users/lilli/AI-Shared/projects/tv-lib')
import tvlib
from PIL import Image, ImageDraw, ImageChops

BG = (21, 31, 26); BGA = (26, 38, 31); BGB = (18, 27, 22)
COR = (236, 168, 70); TEA = (112, 196, 232); CREAM = (248, 242, 226); DIMC = (176, 190, 162)
ROSE = (228, 96, 124); LAV = (178, 158, 242); SAGE = (166, 204, 120); CARDC = (34, 50, 41); BONE = (226, 210, 176); BONED = (140, 120, 92)
tvlib.BG = BG; tvlib.BG2 = BGA; tvlib.AMBER = COR; tvlib.STEEL = (110, 140, 116); tvlib.TXT = CREAM; tvlib.DIM = DIMC
tvlib.RED = ROSE; tvlib.TEAL = TEA; tvlib.BLUE = LAV; tvlib.GREEN = SAGE; tvlib.CARD = CARDC

_fc = {}
def font(kind, size):
    k = (kind, size)
    if k not in _fc:
        f = {'serif': 'cambriab.ttf', 'serifr': 'cambriai.ttf', 'sans': 'candara.ttf', 'sansb': 'candarab.ttf'}[kind]
        _fc[k] = tvlib.ImageFont.truetype('C:/Windows/Fonts/' + f, int(size * tvlib.SS))
    return _fc[k]
tvlib.font = font
from tvlib import *
if PORT: HEAD = (50, 128, W - 50, 330)

# ------------------------------------------------------------------ live voice waveform
ENV = None; RAW = None
def _load():
    global ENV, RAW
    if RAW is None:
        RAW = np.zeros(44100)
        if os.path.exists('audio/voice.wav'):
            with wave.open('audio/voice.wav') as w:
                ch = w.getnchannels(); RAW = np.frombuffer(w.readframes(w.getnframes()), '<i2').reshape(-1, ch).mean(1) / 32768.0
        n = len(RAW) // 441
        ENV = np.sqrt((RAW[:n * 441].reshape(n, 441) ** 2).mean(1))   # RMS per 10 ms

def voice_wave(cv, tt, yc, amp, alpha=0.3, span=4.0):
    _load(); step = 7 if not PORT else 8
    for x in range(0, W, step):
        off = (x - W / 2) / W * span
        i = int((tt + off) * 100)
        v = ENV[i] if 0 <= i < len(ENV) else 0.0
        h = 3 + min(1.0, v / 0.16) * amp
        col = COR if x < W / 2 else TEA
        near = 1.0 - min(1.0, abs(x - W / 2) / (W / 2)) * 0.5
        cv.rect((x, yc - h, x + step - 3, yc + h), mix(col, BG, alpha * near), 2)

def scope(cv, tt, area, col, w=5):
    """oscilloscope of the actual samples playing now (used for the synthesized sound demo)."""
    _load(); x0, y0, x1, y1 = area; n = 700; sr = 44100
    c = int(tt * sr); seg = RAW[c:c + int(0.045 * sr)]
    if len(seg) < 50: return
    idx = np.linspace(0, len(seg) - 1, n).astype(int); ys = seg[idx]
    peak = max(0.05, np.abs(RAW[max(0, c - 4000):c + 4000]).max())
    pts = [(x0 + (x1 - x0) * k / (n - 1), (y0 + y1) / 2 - ys[k] / peak * (y1 - y0) / 2 * 0.9) for k in range(n)]
    cv.line(pts, mix(col, BG, 0.45), w + 6); cv.line(pts, col, w); cv.line(pts, CREAM, 2)

# ------------------------------------------------------------------ frame
_bgimg = None
def tracks(d, x0, H):
    """walking footprints down the left edge (two-toed pairs, alternating)"""
    y = 40; k = 0
    while y < H:
        cx = x0 + (9 if k % 2 == 0 else 24)
        d.ellipse([(cx - 6) * SS, (y - 9) * SS, (cx + 6) * SS, (y + 9) * SS], fill=(54, 78, 62))
        d.ellipse([(cx - 4) * SS, (y - 17) * SS, (cx + 4) * SS, (y - 11) * SS], fill=(54, 78, 62))
        y += 52; k += 1
def _bg():
    global _bgimg
    if _bgimg is None:
        im = Image.new('RGB', (W * SS, H * SS), BGB); d = ImageDraw.Draw(im)
        tracks(d, 4 if PORT else 10, H * SS // SS)
        _bgimg = im.reduce(SS)
    return _bgimg

GA = {}
def ruler(cv, ga, a=1.0): return

def chip(cv):
    if PORT: cv.text((W / 2, 22), 'ANIMALS  ·  19.1', 'sansb', 28, DIMC, 'ma')
    else: cv.text((W - 70, 40), 'ANIMALS  ·  19.1', 'sansb', 28, DIMC, 'ra')

def oq_frame(tt):
    cv = Cv(); cv.im.paste(_bg().resize((W * SS, H * SS)))
    sc = tvlib.SCENES; bounds = tvlib.bounds
    for i, (sid, head, src, fn) in enumerate(sc):
        s0, s1 = bounds[i]
        if s0 <= tt < s1 or (i == len(sc) - 1 and tt >= s0): break
    t = tt - s0; p = clamp01(t / max(0.1, s1 - s0 - 0.6))
    if PORT: voice_wave(cv, tt, 1262, 22, 0.6)
    else: voice_wave(cv, tt, 920, 46, 0.2)
    if head:
        a = ease(t / 0.6); hw = HEAD[2] - HEAD[0] - (0 if PORT else 500)
        f = font('serif', SZ['head']); ls = wrap(head, f, hw)
        for k, l in enumerate(ls): cv.text((HEAD[0], HEAD[1] + k * SZ['head'] * 1.15), l, 'serif', SZ['head'], CREAM, 'la', a)
        ry = HEAD[3] - 6 if not PORT else HEAD[1] + len(ls) * SZ['head'] * 1.15 + 14
        cv.rect((HEAD[0], ry, HEAD[0] + 60, ry + 5), mix(SAGE, BG, a)); cv.rect((HEAD[0] + 60, ry, HEAD[0] + 120, ry + 5), mix(LAV, BG, a))
    chip(cv); ruler(cv, GA.get(sid), ease(t / 0.8))
    fn(cv, t, p)
    sub = tvlib.subtitle_at(sid, tt)
    if sub:
        f = font('sans', SZ['cap']); ls = wrap(sub, f, CAP[2] - CAP[0]); n = len(ls)
        y0 = CAP[1] + (CAP[3] - CAP[1] - n * SZ['cap'] * 1.28) / 2 if not PORT else CAP[1] + 20
        for k, l in enumerate(ls): cv.text((W / 2, y0 + k * SZ['cap'] * 1.28), l, 'sans', SZ['cap'], CREAM, 'ma', 1.0, 1.5)
    if src: cv.para(SRC[0], SRC[1], src, 'sans', SZ['src'], DIMC, SRC[2] - SRC[0], 1.25, 'l', ease(t / 1.2))
    im = cv.im.reduce(SS)
    fa = min(1.0, t / 0.35, (s1 - tt) / 0.35 if i < len(sc) - 1 else (TOTAL - tt) / 1.2)
    if fa < 1.0: im = Image.blend(_bg(), im, max(0.0, fa))
    return im
tvlib.frame = oq_frame

def configure(subs, scenes):
    tvlib.configure(subs, scenes); tvlib.SCENES = scenes

def cue(sid, k): return tvlib.cue(sid, k)
main = tvlib.main

# ------------------------------------------------------------------ pieces
def flute(cv, x0, yc, L, th, t, a=1.0, holes=5, bgc=CARDC):
    body = [(x0, yc - th / 2), (x0 + L, yc - th / 2), (x0 + L + 8, yc - th / 6), (x0 + L - 6, yc), (x0 + L + 10, yc + th / 4), (x0 + L, yc + th / 2), (x0, yc + th / 2)]
    cv.poly(body, mix(BONE, bgc, a), mix(BONED, bgc, a))
    for dy in (-1, 1): cv.poly([(x0, yc + dy * th / 2), (x0 + th * 0.6, yc + dy * th / 2), (x0 + th * 0.2, yc + dy * th * 0.05)], bgc)
    pos = [0.36, 0.47, 0.58, 0.70, 0.81][:holes]
    for k, f in enumerate(pos): cv.circ((x0 + L * f, yc), th * 0.22, mix((58, 46, 30), bgc, a * ease((t - 0.3 - k * 0.12) / 0.3)))

def card(cv, bx, a, edge=DIMC, r=20, fill=CARDC):
    cv.rect(bx, mix(fill, BG, a), r); cv.outline(bx, mix(edge, BG, 0.55 * a), 3, r)

def pill(cv, cx, cy, txt, col, a=1.0, size=36, pad=26):
    if a <= 0.02: return (cx, cy, cx, cy)
    f = font('sansb', size); w = f.getlength(txt) / SS + pad * 2; h = size + 26
    bx = (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)
    cv.rect(bx, mix(col, BG, 0.2 * a), h / 2); cv.outline(bx, mix(col, BG, a), 3, h / 2)
    cv.text((cx, cy - size * 0.62), txt, 'sansb', size, col, 'ma', a)
    return bx

def side_cards(cv, t, left, right, ta, tb, area=None, size=None):
    """left/right = (title, colour, [bullets], optional (tag, tagcolour)). Side by side (land) or stacked (port)."""
    x0, y0, x1, y1 = area or CONT; gap = 30
    if PORT:
        h = (y1 - y0 - gap) / 2; boxes = [(x0, y0, x1, y0 + h), (x0, y0 + h + gap, x1, y1)]
    else:
        w = (x1 - x0 - gap) / 2; boxes = [(x0, y0, x0 + w, y1), (x0 + w + gap, y0, x1, y1)]
    for bx, spec, t0 in zip(boxes, (left, right), (ta, tb)):
        title, col, lines = spec[:3]; tag = spec[3] if len(spec) > 3 else None
        a = ease((t - t0) / 0.6)
        if a <= 0: continue
        card(cv, bx, a, col)
        cv.text((bx[0] + 34, bx[1] + 22), title, 'serif', 54 if PORT else 52, col, 'la', a)
        y = bx[1] + (88 if PORT else 100)
        if tag:
            badge(cv, bx[0] + 34, y, tag[0], tag[1], a, 26); y += 62
        for k, l in enumerate(lines):
            aa = ease((t - t0 - 0.5 - k * 0.5) / 0.6)
            y = cv.para(bx[0] + 34, y, '• ' + l, 'sans', (42 if PORT else 40) if size is None else size, CREAM, bx[2] - bx[0] - 68, 1.2, 'l', aa) + 12
    return boxes

def hyoid(cv, cx, cy, R, a, col=BONE, edge=BONED):
    pts = [(cx + R * math.cos(math.radians(th)), cy + R * 0.82 * math.sin(math.radians(th))) for th in range(-18, 199, 4)]
    cv.line(pts, mix(edge, BG, a), R * 0.30 + 8); cv.line(pts, mix(col, BG, a), R * 0.30)
    for th in (-18, 198):
        c = (cx + R * math.cos(math.radians(th)), cy + R * 0.82 * math.sin(math.radians(th)))
        cv.circ(c, R * 0.17, mix(edge, BG, a)); cv.circ(c, R * 0.14, mix(col, BG, a))

def venn(cv, cx, cy, r, d, a):
    cL = (cx - d, cy); cR = (cx + d, cy)
    cv.circ(cL, r, mix(COR, BG, 0.28 * a)); cv.circ(cR, r, mix(TEA, BG, 0.28 * a))
    m1 = Image.new('L', cv.im.size, 0); m2 = Image.new('L', cv.im.size, 0)
    for m, c in ((m1, cL), (m2, cR)):
        ImageDraw.Draw(m).ellipse([(c[0] - r) * SS, (c[1] - r) * SS, (c[0] + r) * SS, (c[1] + r) * SS], fill=255)
    cv.im.paste(mix(CREAM, BG, 0.30 * a), mask=ImageChops.multiply(m1, m2))
    cv.ring(cL, r, mix(COR, BG, a), 4); cv.ring(cR, r, mix(TEA, BG, a), 4)
    return cL, cR

def checkbox(cv, x, y, s, a):
    cv.outline((x, y, x + s, y + s), mix(LAV, BG, a), 4, 8)

def rail(cv, t, items, area=None):
    """dated items on a timeline rail. items: dict(year, who, what, at, col). Horizontal (land) / vertical (port)."""
    x0, y0, x1, y1 = area or CONT; n = len(items)
    if PORT:
        cv.rect((x0 + 70, y0 + 20, x0 + 76, y1 - 20), mix(DIMC, BG, 0.5)); step = (y1 - y0) / n
        for i, it in enumerate(items):
            a = ease((t - it['at']) / 0.6)
            if a <= 0: continue
            cy = y0 + i * step + step / 2; col = it.get('col', COR)
            cv.circ((x0 + 73, cy), 17, mix(col, BG, a))
            cv.text((x0 + 130, cy - step * 0.40), it['year'], 'serif', 84, col, 'la', a)
            cv.text((x0 + 130, cy + 10), it['who'], 'sansb', 36, CREAM, 'la', a)
            cv.para(x0 + 130, cy + 54, it['what'], 'sans', 36, DIMC, x1 - x0 - 150, 1.2, 'l', a)
    else:
        ly = y0 + 120; cv.rect((x0 + 20, ly - 3, x1 - 20, ly + 3), mix(DIMC, BG, 0.5)); w = (x1 - x0) / n
        for i, it in enumerate(items):
            a = ease((t - it['at']) / 0.6)
            if a <= 0: continue
            cx = x0 + i * w + 40; col = it.get('col', COR)
            cv.circ((cx + 6, ly), 17, mix(col, BG, a))
            cv.text((cx, ly - 125), it['year'], 'serif', 120, col, 'la', a)
            cv.text((cx, ly + 50), it['who'], 'sansb', 40, CREAM, 'la', a)
            cv.para(cx, ly + 108, it['what'], 'sans', 42, DIMC, w - 70, 1.2, 'l', a)

# ------------------------------------------------------------------ flat animal icons (illustrations, labeled as such in the episode)
def _e(cv, cx, cy, rx, ry, col):
    cv.d.ellipse([(cx - rx) * SS, (cy - ry) * SS, (cx + rx) * SS, (cy + ry) * SS], fill=col)

def elephant(cv, cx, cy, s, col, a=1.0, dark=None, flip=1):
    c = mix(col, BG, a); dk = mix(dark or (col[0] * 0.7, col[1] * 0.7, col[2] * 0.7), BG, a)
    X = lambda dx: cx + dx * s * flip
    for dx in (-0.55, -0.25, 0.28, 0.58):
        cv.rect((X(dx) - 0.07 * s * (1 if flip > 0 else -1) if False else min(X(dx) - 0.07 * s, X(dx) + 0.07 * s), cy + 0.2 * s, max(X(dx) - 0.07 * s, X(dx) + 0.07 * s), cy + 0.62 * s), dk, 6)
    _e(cv, X(0.0), cy, 0.72 * s, 0.42 * s, c)
    _e(cv, X(0.6), cy - 0.12 * s, 0.34 * s, 0.33 * s, c)
    tr = [(X(0.84), cy - 0.02 * s), (X(0.98), cy + 0.2 * s), (X(1.0), cy + 0.44 * s), (X(0.92), cy + 0.62 * s)]
    cv.line(tr, c, 0.15 * s); cv.line([(X(0.84), cy - 0.02 * s), (X(0.95), cy + 0.18 * s)], c, 0.2 * s)
    _e(cv, X(0.46), cy - 0.04 * s, 0.17 * s, 0.26 * s, dk)
    cv.poly([(X(0.8), cy + 0.05 * s), (X(0.98), cy + 0.2 * s), (X(0.82), cy + 0.12 * s)], mix(BONE, BG, a))
    _e(cv, X(0.68), cy - 0.2 * s, 0.025 * s, 0.025 * s, mix(CREAM, BG, a))

def crow(cv, cx, cy, s, col, a=1.0, flip=1, down=False):
    c = mix(col, BG, a); X = lambda dx: cx + dx * s * flip
    if down:   # lying on its side: simple flat shape, no detail
        _e(cv, cx, cy, 0.62 * s, 0.22 * s, c); _e(cv, X(0.5), cy - 0.05 * s, 0.16 * s, 0.14 * s, c)
        cv.poly([(X(0.64), cy - 0.05 * s), (X(0.84), cy), (X(0.64), cy + 0.03 * s)], mix(DIMC, BG, a)); cv.poly([(X(-0.55), cy), (X(-0.98), cy - 0.12 * s), (X(-0.95), cy + 0.12 * s)], c); return
    cv.line([(X(-0.1), cy + 0.3 * s), (X(-0.1), cy + 0.55 * s)], c, 0.05 * s); cv.line([(X(0.15), cy + 0.3 * s), (X(0.15), cy + 0.55 * s)], c, 0.05 * s)
    _e(cv, cx, cy, 0.45 * s, 0.3 * s, c); _e(cv, X(0.4), cy - 0.25 * s, 0.17 * s, 0.16 * s, c)
    cv.poly([(X(0.53), cy - 0.3 * s), (X(0.82), cy - 0.2 * s), (X(0.54), cy - 0.16 * s)], mix(DIMC, BG, a))
    cv.poly([(X(-0.35), cy - 0.05 * s), (X(-0.95), cy + 0.12 * s), (X(-0.9), cy + 0.28 * s), (X(-0.3), cy + 0.15 * s)], c)
    _e(cv, X(0.46), cy - 0.28 * s, 0.025 * s, 0.025 * s, mix(CREAM, BG, a))

def primate(cv, cx, cy, s, col, a=1.0):
    c = mix(col, BG, a); face = mix((214, 176, 142), BG, a)
    _e(cv, cx, cy + 0.62 * s, 0.7 * s, 0.4 * s, c)
    for dx in (-1, 1): _e(cv, cx + dx * 0.5 * s, cy - 0.05 * s, 0.15 * s, 0.18 * s, c)
    _e(cv, cx, cy, 0.46 * s, 0.5 * s, c); _e(cv, cx, cy + 0.07 * s, 0.32 * s, 0.34 * s, face)
    for dx in (-1, 1): _e(cv, cx + dx * 0.14 * s, cy - 0.04 * s, 0.035 * s, 0.035 * s, mix((30, 24, 20), BG, a))
    _e(cv, cx, cy + 0.2 * s, 0.14 * s, 0.07 * s, mix((170, 130, 104), BG, a))

def orca(cv, cx, cy, s, col, a=1.0, flip=1):
    c = mix(col, BG, a); X = lambda dx: cx + dx * s * flip
    top = [(-1.0, 0.0), (-0.7, -0.22), (-0.2, -0.32), (0.3, -0.26), (0.75, -0.08), (1.0, 0.04)]
    bot = [(1.0, 0.04), (0.7, 0.1), (0.2, 0.3), (-0.3, 0.25), (-0.8, 0.12), (-1.0, 0.0)]
    cv.poly([(X(x), cy + y * s) for x, y in top + bot], c)
    cv.poly([(X(-0.3), cy - 0.3 * s), (X(-0.12), cy - 0.72 * s), (X(0.02), cy - 0.3 * s)], c)
    cv.poly([(X(-0.95), cy), (X(-1.25), cy - 0.2 * s), (X(-1.2), cy), (X(-1.25), cy + 0.2 * s)], c)
    cv.poly([(X(0.1), cy + 0.2 * s), (X(0.3), cy + 0.45 * s), (X(0.4), cy + 0.2 * s)], c)
    _e(cv, X(0.62), cy - 0.13 * s, 0.1 * s, 0.045 * s, mix(CREAM, BG, a))
    _e(cv, X(0.1), cy + 0.2 * s, 0.38 * s, 0.07 * s, mix(CREAM, BG, 0.75 * a)) if False else None

def tag(cv, x, y, kind, a=1.0, size=28, anchor='l'):
    """kind: 'obs' | 'int' | 'dis' | 'est'"""
    lab, col = {'obs': ('OBSERVED', SAGE), 'int': ('INTERPRETATION', LAV), 'dis': ('DISPUTED', ROSE), 'est': ('NOT ESTABLISHED', ROSE)}[kind]
    return badge(cv, x, y, lab, col, a, size, anchor)
