# AI Explained look (Heartbeat TV channel 13): "lab notebook on a dark green bench" - deep green-slate with a faint dot grid,
# lime = established / what was measured, peach = disputed, sky = open, lilac = illustration/model, rose = failed prediction.
# Cambria headlines, Candara text, Consolas labels, a status lamp (top right) on every scene, a live "evidence strip" at the bottom.
# Built on tv-lib's Cv + animation helpers.  Import FIRST in an episode file:  from ailib import *
import sys, os, math, random
sys.path.insert(0, 'C:/Users/lilli/AI-Shared/projects/tv-lib')
import tvlib
from PIL import Image, ImageDraw

BG = (15, 31, 32); BGA = (19, 39, 40); CARDC = (27, 55, 55)
LIME = (200, 235, 115); SKY = (126, 206, 232); PEACH = (246, 172, 116); ROSE = (240, 112, 124); LILAC = (182, 162, 242)
CREAM = (246, 240, 224); DIMC = (158, 184, 176)
tvlib.BG = BG; tvlib.BG2 = BGA; tvlib.AMBER = LIME; tvlib.STEEL = (92, 140, 136); tvlib.TXT = CREAM; tvlib.DIM = DIMC
tvlib.RED = ROSE; tvlib.TEAL = SKY; tvlib.BLUE = LILAC; tvlib.GREEN = LIME; tvlib.CARD = CARDC

_fc = {}
def font(kind, size):
    k = (kind, size)
    if k not in _fc:
        f = {'serif': 'cambriab.ttf', 'serifr': 'cambriai.ttf', 'sans': 'candara.ttf', 'sansb': 'candarab.ttf',
             'mono': 'consola.ttf', 'monob': 'consolab.ttf'}[kind]
        _fc[k] = tvlib.ImageFont.truetype('C:/Windows/Fonts/' + f, int(size * tvlib.SS))
    return _fc[k]
tvlib.font = font
from tvlib import *

STATUS = {}           # scene id -> (label, colour) shown as the status lamp
EP = '13.1'

_bgimg = None
def _bg():
    global _bgimg
    if _bgimg is None:
        im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im)
        for y in range(36, H, 48):
            for x in range(36, W, 48): d.ellipse([x - 1, y - 1, x + 1, y + 1], fill=mix(CREAM, BG, 0.10))
        d.rectangle([0, 0, 10, H], fill=mix(LIME, BG, 0.55))     # left spine of the notebook
        _bgimg = im
    return _bgimg

def card(cv, bx, a, edge=None, r=18, fill=CARDC):
    cv.rect(bx, mix(fill, BG, a), r); cv.outline(bx, mix(edge or (92, 140, 136), BG, 0.6 * a), 3, r)

def pill(cv, cx, cy, txt, col, a=1.0, size=34, pad=24, kind='monob'):
    if a <= 0.02: return
    f = font(kind, size); w = f.getlength(txt) / SS + pad * 2; h = size + 24
    cv.rect((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), mix(col, BG, 0.2 * a), h / 2)
    cv.outline((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), mix(col, BG, a), 3, h / 2)
    cv.text((cx, cy - size * 0.62), txt, kind, size, col, 'ma', a)

def rev(p, f, w=0.04): return ease((p - f) / w)

def boxes(n, area=None, gap=26, ratio=None):
    x0, y0, x1, y1 = area or CONT
    out = []
    for i in range(n):
        if PORT:
            h = (y1 - y0 - gap * (n - 1)) / n; out.append((x0, y0 + i * (h + gap), x1, y0 + i * (h + gap) + h))
        else:
            w = (x1 - x0 - gap * (n - 1)) / n; out.append((x0 + i * (w + gap), y0, x0 + i * (w + gap) + w, y1))
    return out

def lamp(cv, sid, t):
    if sid not in STATUS: return
    lab, col = STATUS[sid]; a = ease((t - 0.4) / 0.6)
    if PORT:
        f = font('monob', 24); w = f.getlength(lab) / SS + 40
        pill(cv, W - 50 - w / 2, 40, lab, col, a, 24, 20)
    else:
        f = font('monob', 28); w = f.getlength(lab) / SS + 48
        pill(cv, W - 70 - w / 2, 100, lab, col, a, 28)

def chip(cv):
    if PORT: cv.text((50, 24), 'AI EXPLAINED  ·  ' + EP, 'monob', 26, DIMC, 'la')
    else: cv.text((W - 70, 40), 'AI EXPLAINED  ·  ' + EP, 'monob', 28, DIMC, 'ra')

def strip(cv, tt):
    """thin progress/evidence strip at the very bottom: ticks for every scene, filled to the current time."""
    y = H - 14; x0, x1 = 60, W - 60
    cv.rect((x0, y, x1, y + 6), mix(CREAM, BG, 0.12), 3)
    cv.rect((x0, y, x0 + (x1 - x0) * min(1, tt / TOTAL), y + 6), mix(LIME, BG, 0.8), 3)

def ai_frame(tt):
    cv = Cv(); cv.im.paste(_bg().resize((W * SS, H * SS)))
    sc = tvlib.SCENES; bounds = tvlib.bounds
    for i, (sid, head, src, fn) in enumerate(sc):
        s0, s1 = bounds[i]
        if s0 <= tt < s1 or (i == len(sc) - 1 and tt >= s0): break
    t = tt - s0; p = clamp01(t / max(0.1, s1 - s0 - 0.6))
    if head:
        a = ease(t / 0.6); hw = HEAD[2] - HEAD[0] - (0 if PORT else 380)
        f = font('serif', SZ['head']); ls = wrap(head, f, hw)
        for k, l in enumerate(ls): cv.text((HEAD[0], HEAD[1] + k * SZ['head'] * 1.15), l, 'serif', SZ['head'], CREAM, 'la', a)
        ry = HEAD[3] - 6 if not PORT else HEAD[1] + len(ls) * SZ['head'] * 1.15 + 14
        cv.rect((HEAD[0], ry, HEAD[0] + 120, ry + 5), mix(LIME, BG, a))
    chip(cv); lamp(cv, sid, t)
    fn(cv, t, p)
    sub = tvlib.subtitle_at(sid, tt)
    if sub:
        f = font('sans', SZ['cap']); ls = wrap(sub, f, CAP[2] - CAP[0]); n = len(ls)
        y0 = CAP[1] + (CAP[3] - CAP[1] - n * SZ['cap'] * 1.28) / 2 if not PORT else CAP[1] + 20
        for k, l in enumerate(ls): cv.text((W / 2, y0 + k * SZ['cap'] * 1.28), l, 'sans', SZ['cap'], CREAM, 'ma', 1.0, 1.5)
    if src: cv.para(SRC[0], SRC[1], src, 'mono', SZ['src'] - 5, DIMC, SRC[2] - SRC[0], 1.25, 'l', ease(t / 1.2))
    strip(cv, tt)
    im = cv.im.reduce(SS)
    fa = min(1.0, t / 0.35, (s1 - tt) / 0.35 if i < len(sc) - 1 else (TOTAL - tt) / 1.2)
    if fa < 1.0: im = Image.blend(_bg(), im, max(0.0, fa))
    return im
tvlib.frame = ai_frame

def configure(subs, scenes):
    tvlib.configure(subs, scenes); tvlib.SCENES = scenes
def cue(sid, k): return tvlib.cue(sid, k)
main = tvlib.main
