# Heartbeat TV History ep.1 "What if the railroads never existed?"
# Pure-Python (Pillow) animated maps/charts, 2x supersampled, frames piped to ffmpeg.
#   python render.py land|port [--still SECONDS out.png] [--secs A B]
import json, math, subprocess, sys
from multiprocessing import Pool
from PIL import Image, ImageDraw, ImageFont

TL = json.load(open('timeline.json'))
TOTAL = TL['total']; SEG = {s['id']: s for s in TL['segs']}
FPS = 30; SS = 2
ORI = sys.argv[1] if len(sys.argv) > 1 else 'land'
PORT = ORI == 'port'
W, H = (1080, 1920) if PORT else (1920, 1080)

BG = (11, 18, 32); BG2 = (17, 28, 48)
AMBER = (242, 177, 52); STEEL = (96, 124, 158); TXT = (236, 240, 246); DIM = (142, 156, 178)
RED = (222, 98, 84); LAND = (24, 38, 62); LANDEDGE = (52, 78, 112); TEAL = (88, 190, 178)

FD = 'C:/Windows/Fonts/'
_fc = {}
def font(kind, size):
    k = (kind, size)
    if k not in _fc:
        f = {'serif': 'georgiab.ttf', 'serifr': 'georgia.ttf', 'sans': 'segoeui.ttf', 'sansb': 'segoeuib.ttf'}[kind]
        _fc[k] = ImageFont.truetype(FD + f, int(size * SS))
    return _fc[k]

# font sizes by orientation (logical px)
SZ = dict(head=64 if PORT else 72, cap=54 if PORT else 46, src=32 if PORT else 30, big=150 if PORT else 160,
          lab=42 if PORT else 40, small=34 if PORT else 32)

# layout boxes (logical)
if PORT:
    HEAD = (50, 70, W - 50, 330); CONT = (30, 350, W - 30, 1230); CAP = (60, 1290, W - 60, 1740); SRC = (60, 1770, W - 60, 1890)
else:
    HEAD = (70, 36, W - 70, 170); CONT = (60, 190, W - 60, 830); CAP = (110, 850, W - 110, 990); SRC = (110, 1000, W - 110, 1070)

def mix(c, d, a):
    return tuple(int(c[i] * a + d[i] * (1 - a)) for i in range(3))

def ease(x):
    x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)

def clamp01(x): return max(0.0, min(1.0, x))

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
    def outline(s, b, col, w=3, r=0):
        bb = [b[0] * SS, b[1] * SS, b[2] * SS, b[3] * SS]
        s.d.rounded_rectangle(bb, radius=r * SS, outline=col, width=int(w * SS))
    def line(s, pts, col, w):
        s.d.line([s.P(p) for p in pts], fill=col, width=int(w * SS), joint='curve')
    def poly(s, pts, fill, edge=None):
        s.d.polygon([s.P(p) for p in pts], fill=fill, outline=edge)
    def circ(s, c, r, fill):
        s.d.ellipse([(c[0] - r) * SS, (c[1] - r) * SS, (c[0] + r) * SS, (c[1] + r) * SS], fill=fill)
    def text(s, xy, t, kind, size, col, anchor='la', a=1.0, stroke=0):
        s.d.text(s.P(xy), t, font=font(kind, size), fill=mix(col, BG, a), anchor=anchor, stroke_width=int(stroke * SS), stroke_fill=BG)
    def para(s, x, y, t, kind, size, col, maxw, lh=1.25, anchor='l', a=1.0):
        f = font(kind, size); ls = wrap(t, f, maxw)
        for i, l in enumerate(ls):
            xx = x if anchor == 'l' else (x - 0 if anchor == 'm' else x)
            s.d.text(s.P((xx, y + i * size * lh)), l, font=f, fill=mix(col, BG, a), anchor='ma' if anchor == 'm' else 'la')
        return y + len(ls) * size * lh

