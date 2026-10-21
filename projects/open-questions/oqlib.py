# Open Questions look (Heartbeat TV ch 9): warm dark, TWO-SIDES split screen (coral = one answer, teal = the other),
# live voice waveform behind the captions, Constantia/Corbel type. Built on tv-lib's Cv + animation helpers, with the
# History/Science navy+gold palette replaced. Import this FIRST in an episode file:  from oqlib import *
import sys, os, math, wave
import numpy as np
sys.path.insert(0, 'C:/Users/lilli/AI-Shared/projects/tv-lib')
import tvlib
from PIL import Image, ImageDraw, ImageChops

BG = (35, 26, 28); BGA = (42, 25, 26); BGB = (28, 29, 33)
COR = (238, 118, 86); TEA = (92, 190, 176); CREAM = (248, 238, 220); DIMC = (196, 176, 156)
ROSE = (228, 96, 124); LAV = (178, 158, 242); SAGE = (166, 204, 120); CARDC = (56, 38, 40); BONE = (226, 210, 176); BONED = (140, 120, 92)
tvlib.BG = BG; tvlib.BG2 = BGA; tvlib.AMBER = COR; tvlib.STEEL = (150, 118, 108); tvlib.TXT = CREAM; tvlib.DIM = DIMC
tvlib.RED = ROSE; tvlib.TEAL = TEA; tvlib.BLUE = LAV; tvlib.GREEN = SAGE; tvlib.CARD = CARDC

_fc = {}
def font(kind, size):
    k = (kind, size)
    if k not in _fc:
        f = {'serif': 'constanb.ttf', 'serifr': 'constani.ttf', 'sans': 'corbel.ttf', 'sansb': 'corbelb.ttf'}[kind]
        _fc[k] = tvlib.ImageFont.truetype('C:/Windows/Fonts/' + f, int(size * tvlib.SS))
    return _fc[k]
tvlib.font = font
from tvlib import *

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
def _bg():
    global _bgimg
    if _bgimg is None:
        im = Image.new('RGB', (W, H), BGB); d = ImageDraw.Draw(im); d.rectangle([0, 0, W // 2, H], fill=BGA)
        d.rectangle([W // 2 - 1, 0, W // 2 + 1, H], fill=mix(CREAM, BG, 0.10)); _bgimg = im
    return _bgimg

EPN = os.environ.get('OQ_EP', '9.1')   # episode number shown in the corner chip (set OQ_EP=9.2 for ep 2)
def chip(cv):
    if PORT: cv.text((W / 2, 24), 'OPEN QUESTIONS  ·  ' + EPN, 'sansb', 28, DIMC, 'ma')
    else: cv.text((W - 70, 46), 'OPEN QUESTIONS  ·  ' + EPN, 'sansb', 28, DIMC, 'ra')

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
        a = ease(t / 0.6); hw = HEAD[2] - HEAD[0] - (0 if PORT else 360)
        f = font('serif', SZ['head']); ls = wrap(head, f, hw)
        for k, l in enumerate(ls): cv.text((HEAD[0], HEAD[1] + k * SZ['head'] * 1.15), l, 'serif', SZ['head'], CREAM, 'la', a)
        ry = HEAD[3] - 6 if not PORT else HEAD[1] + len(ls) * SZ['head'] * 1.15 + 14
        cv.rect((HEAD[0], ry, HEAD[0] + 60, ry + 5), mix(COR, BG, a)); cv.rect((HEAD[0] + 60, ry, HEAD[0] + 120, ry + 5), mix(TEA, BG, a))
    chip(cv)
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
