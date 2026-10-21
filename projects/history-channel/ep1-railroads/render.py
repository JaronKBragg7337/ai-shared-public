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

# ---------------------------------------------------------------- geography
OUT = [(-124.7,48.4),(-123.0,48.3),(-122.8,49.0),(-95.15,49.0),(-94.6,48.7),(-93.0,48.6),(-91.5,48.1),(-89.6,48.0),(-90.8,46.9),(-92.1,46.7),
(-90.4,46.6),(-88.4,47.4),(-87.4,46.5),(-85.0,46.8),(-84.5,46.5),(-84.7,45.9),(-83.4,45.2),(-83.9,43.7),(-82.5,43.0),(-83.1,42.3),(-83.4,41.7),
(-82.7,41.5),(-81.7,41.5),(-80.5,42.0),(-79.0,42.7),(-79.0,43.3),(-76.5,43.5),(-76.3,44.2),(-75.0,44.9),(-74.7,45.0),(-71.5,45.0),(-71.1,45.3),
(-70.3,45.9),(-70.0,46.7),(-69.2,47.45),(-68.3,47.35),(-67.8,47.07),(-67.8,45.7),(-67.4,45.2),(-67.0,44.8),(-68.2,44.3),(-69.8,43.8),(-70.7,43.1),
(-70.8,42.5),(-70.0,42.0),(-70.5,41.8),(-71.4,41.4),(-72.9,41.2),(-73.7,40.9),(-74.0,40.6),(-74.1,39.7),(-74.9,38.9),(-75.1,38.4),(-75.9,37.1),
(-76.0,36.9),(-75.6,35.9),(-75.5,35.2),(-76.5,34.7),(-77.9,33.9),(-79.0,33.3),(-80.0,32.6),(-81.1,31.7),(-81.4,30.7),(-81.3,29.9),(-80.6,28.4),
(-80.1,26.8),(-80.2,25.7),(-80.4,25.2),(-81.1,25.2),(-81.8,26.1),(-82.2,26.9),(-82.7,27.8),(-82.8,28.9),(-83.7,29.9),(-84.3,30.0),(-85.3,29.7),
(-86.5,30.4),(-87.5,30.3),(-88.1,30.3),(-89.2,30.3),(-89.6,30.2),(-89.2,29.0),(-90.2,29.1),(-91.3,29.3),(-92.3,29.5),(-93.8,29.7),(-94.7,29.3),
(-95.4,28.9),(-96.4,28.3),(-97.2,27.7),(-97.4,26.9),(-97.15,25.95),(-98.3,26.1),(-99.1,26.4),(-99.5,27.5),(-100.4,28.2),(-101.0,29.4),(-102.3,29.8),
(-102.7,29.7),(-103.1,29.0),(-104.5,29.6),(-104.9,30.6),(-106.5,31.8),(-108.2,31.8),(-108.2,31.3),(-111.1,31.3),(-114.8,32.5),(-117.1,32.5),
(-117.3,33.0),(-118.4,33.8),(-118.5,34.0),(-119.2,34.1),(-120.5,34.5),(-120.65,35.2),(-121.9,36.6),(-122.5,37.6),(-123.0,38.3),(-123.8,39.4),
(-124.4,40.4),(-124.1,41.8),(-124.5,42.8),(-124.1,44.0),(-124.0,46.2),(-124.1,47.0),(-124.7,48.4)]

def _dens(pts, step=2.0):
    out = []
    for a, b in zip(pts, pts[1:]):
        n = max(1, int(max(abs(b[0] - a[0]), abs(b[1] - a[1])) / step))
        out += [(a[0] + (b[0] - a[0]) * k / n, a[1] + (b[1] - a[1]) * k / n) for k in range(n)]
    return out + [pts[-1]]
OUT = _dens(OUT)

def albers(lon, lat):
    p1, p2, p0, l0 = map(math.radians, (29.5, 45.5, 37.5, -96.0))
    n = (math.sin(p1) + math.sin(p2)) / 2; C = math.cos(p1) ** 2 + 2 * n * math.sin(p1)
    r0 = math.sqrt(C - 2 * n * math.sin(p0)) / n; la = math.radians(lat); lo = math.radians(lon)
    r = math.sqrt(C - 2 * n * math.sin(la)) / n; th = n * (lo - l0)
    return r * math.sin(th), -(r0 - r * math.cos(th))

_pb = [albers(*p) for p in OUT]
BX0, BX1 = min(p[0] for p in _pb), max(p[0] for p in _pb); BY0, BY1 = min(p[1] for p in _pb), max(p[1] for p in _pb)

def mapper(box):
    bw, bh = box[2] - box[0], box[3] - box[1]
    sc = min(bw / (BX1 - BX0), bh / (BY1 - BY0))
    ox = box[0] + (bw - (BX1 - BX0) * sc) / 2; oy = box[1] + (bh - (BY1 - BY0) * sc) / 2
    def f(lon, lat):
        x, y = albers(lon, lat); return (ox + (x - BX0) * sc, oy + (y - BY0) * sc)
    return f

CITY = dict(NYC=(-74.0,40.7),BOS=(-71.06,42.36),ALB=(-73.75,42.65),BUF=(-78.88,42.89),PHL=(-75.17,39.95),BAL=(-76.6,39.29),WAS=(-77.04,38.9),
PIT=(-80.0,40.44),WHE=(-80.72,40.06),CLE=(-81.69,41.5),CHI=(-87.63,41.88),CIN=(-84.5,39.1),COL=(-83.0,39.96),IND=(-86.16,39.77),STL=(-90.2,38.63),
KC=(-94.58,39.1),OMA=(-95.93,41.26),CHY=(-104.8,41.14),PRO=(-112.55,41.62),SAC=(-121.49,38.58),SF=(-122.42,37.77),SLC=(-111.89,40.76),
DEN=(-104.99,39.74),NOL=(-90.07,29.95),HOU=(-95.37,29.76),SAT=(-98.49,29.42),ELP=(-106.49,31.76),TUC=(-110.97,32.22),LA=(-118.24,34.05),
STP=(-93.09,44.95),FAR=(-96.79,46.88),BIS=(-100.78,46.81),BIL=(-108.5,45.78),MIS=(-114.0,46.87),SPO=(-117.43,47.66),SEA=(-122.33,47.61),
POR=(-122.68,45.52),ATL=(-84.39,33.75),CHA=(-79.93,32.78),SAV=(-81.1,32.08),RIC=(-77.44,37.54),MEM=(-90.05,35.15),NAS=(-86.78,36.16),
LOU=(-85.76,38.25),CAI=(-89.18,37.0),JAX=(-81.66,30.33),TAM=(-82.46,27.95),MIA=(-80.19,25.76),DAL=(-96.8,32.78),DOD=(-100.02,37.75),
ABQ=(-106.65,35.08),TOP=(-95.68,39.05),MOB=(-88.04,30.69),CHT=(-85.31,35.05),CHR=(-80.84,35.23),MINOT=(-101.3,48.23),HAVRE=(-109.68,48.55))

RAILS = [  # (first year, last year, [cities])
 (1830,1853,'BAL WHE'),(1830,1836,'BAL WAS'),(1832,1840,'NYC PHL BAL'),(1831,1851,'NYC ALB'),(1835,1842,'BOS ALB'),(1837,1849,'BOS NYC'),
 (1833,1857,'CHA ATL'),(1842,1853,'ALB BUF'),(1846,1854,'PHL PIT'),(1850,1856,'BUF CLE CHI'),(1850,1857,'PIT COL IND STL'),(1851,1855,'CIN IND CHI'),
 (1851,1872,'CLE COL CIN'),(1852,1858,'CHI STL'),(1851,1873,'CHI CAI NOL'),(1855,1867,'CHI STP'),(1858,1865,'STL KC'),(1845,1855,'ATL CHT NAS'),
 (1859,1865,'NAS LOU CIN'),(1840,1872,'WAS RIC'),(1856,1870,'RIC CHR ATL'),(1860,1881,'CHA SAV JAX'),(1853,1869,'CHI OMA'),(1865,1867,'OMA CHY'),
 (1867,1869,'CHY PRO'),(1863,1869,'SAC PRO'),(1869,1870,'SAC SF'),(1867,1870,'KC DEN'),(1868,1870,'CHY DEN'),(1869,1870,'PRO SLC'),
 (1870,1872,'STP FAR'),(1872,1881,'FAR BIS BIL'),(1881,1883,'BIL MIS SPO SEA'),(1869,1872,'TOP DOD'),(1878,1880,'DOD ABQ'),(1880,1887,'ABQ LA'),
 (1876,1880,'NOL HOU'),(1877,1881,'HOU SAT'),(1881,1883,'SAT ELP TUC LA'),(1870,1881,'KC DAL'),(1872,1874,'DAL HOU'),(1861,1883,'ATL MOB NOL'),
 (1869,1876,'SF LA'),(1870,1887,'SAC POR'),(1883,1884,'POR SEA'),(1881,1883,'DEN SLC'),(1880,1893,'STP MINOT HAVRE SPO SEA'),(1884,1896,'JAX TAM MIA'),
 (1857,1866,'MEM NAS'),(1870,1877,'KC OMA')]
RAILS = [(a, b, [CITY[c] for c in s.split()]) for a, b, s in RAILS]
MILES = [(1830,23),(1840,2818),(1850,9021),(1860,30626),(1870,52922),(1880,93262),(1890,160817),(1900,193346),(1916,254037)]
def miles_at(y):
    for (y0, m0), (y1, m1) in zip(MILES, MILES[1:]):
        if y <= y1: return m0 + (m1 - m0) * clamp01((y - y0) / (y1 - y0))
    return MILES[-1][1]

def draw_us(cv, mp, edge=True):
    pts = [mp(*p) for p in OUT]
    cv.poly(pts, LAND, None); cv.d.line([cv.P(p) for p in pts + [pts[0]]], fill=LANDEDGE, width=int(2.5 * SS), joint='curve')

def partial(pts, f):
    seg = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]; tot = sum(seg); goal = tot * f; out = [pts[0]]; acc = 0
    for i, l in enumerate(seg):
        if acc + l <= goal: out.append(pts[i + 1]); acc += l
        else:
            r = (goal - acc) / l if l else 0
            out.append((pts[i][0] + (pts[i + 1][0] - pts[i][0]) * r, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * r)); break
    return out

# ---------------------------------------------------------------- icons
def train(cv, x, y, s, col=AMBER, cars=5, a=1.0):
    """loco + cars, left to right, baseline y, x = rear of the last car (logical px); s = scale"""
    c = mix(col, BG, a); dark = mix((40, 52, 74), BG, a); wheel = mix((15, 20, 30), BG, a)
    cx = x
    for i in range(cars):
        cv.rect((cx, y - 34 * s, cx + 62 * s, y - 6 * s), c if i % 2 == 0 else mix((205, 140, 40), BG, a), 2)
        cv.rect((cx + 3 * s, y - 31 * s, cx + 59 * s, y - 27 * s), dark)
        for w in (10, 50): cv.circ((cx + w * s, y - 4 * s), 4.5 * s, wheel)
        cx += 66 * s
    cv.rect((cx, y - 40 * s, cx + 70 * s, y - 6 * s), mix((200, 70, 50), BG, a), 3)
    cv.rect((cx + 40 * s, y - 56 * s, cx + 70 * s, y - 38 * s), mix((200, 70, 50), BG, a), 3)
    cv.rect((cx + 46 * s, y - 52 * s, cx + 64 * s, y - 42 * s), dark)
    for w in (12, 34, 58): cv.circ((cx + w * s, y - 5 * s), 5.5 * s, wheel)
    return cx + 70 * s

def truck(cv, x, y, s, col=STEEL):
    cv.rect((x, y - 52 * s, x + 130 * s, y - 12 * s), col, 3)
    cv.rect((x + 136 * s, y - 40 * s, x + 176 * s, y - 12 * s), RED, 3)
    cv.rect((x + 160 * s, y - 56 * s, x + 176 * s, y - 40 * s), RED, 2)
    cv.rect((x + 140 * s, y - 46 * s, x + 158 * s, y - 34 * s), (30, 40, 60))
    for w in (22, 44, 120, 150): cv.circ((x + w * s, y - 8 * s), 9 * s, (15, 20, 30))

# ---------------------------------------------------------------- scenes
def sc_title(cv, t, p):
    a = ease(t / 1.2)
    cv.text((W / 2, CONT[1] + 30 if not PORT else 520), 'HEARTBEAT TV  ·  HISTORY  ·  EPISODE 1', 'sansb', 34 if PORT else 36, AMBER, 'ma', a)
    ty = 640 if PORT else 330
    for k, l in enumerate(('What if the railroads', 'never existed?')):
        cv.text((W / 2, ty + k * (118 if PORT else 140)), l, 'serif', 96 if PORT else 118, TXT, 'ma', ease((t - 0.2) / 1.2))
    # rails across the lower part and a train rolling through
    ry = (1000 if PORT else 770)
    for i in range(-1, 40):
        xx = (i * 44 - (t * 60) % 44)
        cv.line([(xx, ry + 20), (xx + 20, ry + 36)], mix((70, 54, 40), BG, ease(t / 1.5)), 5)
    cv.line([(0, ry + 14), (W, ry + 14)], mix((120, 132, 150), BG, ease(t / 1.5)), 4)
    cv.line([(0, ry + 34), (W, ry + 34)], mix((120, 132, 150), BG, ease(t / 1.5)), 4)
    xe = -520 + (t / 4.0) * (W + 700)
    train(cv, xe, ry + 14, 1.35 if not PORT else 1.0, AMBER, 5)

def sc_map(cv, t, p):
    y = 1830 + ease(p / 0.88) * (1916 - 1830); mi = miles_at(y)
    mb = (CONT[0] + 470, CONT[1], CONT[2], CONT[3]) if not PORT else (CONT[0], CONT[1], CONT[2], CONT[3] - 200)
    mp = mapper(mb); draw_us(cv, mp)
    for a, b, cs in RAILS:
        if y <= a: continue
        f = clamp01((y - a) / max(1, b - a)); pts = [mp(*c) for c in cs]; pp = partial(pts, f)
        if len(pp) > 1:
            cv.line(pp, mix(AMBER, BG, 0.28), 8 if not PORT else 7); cv.line(pp, AMBER, 3.6 if not PORT else 3.2)
    for nm, lab in (('NYC', 'New York'), ('CHI', 'Chicago'), ('SF', 'San Francisco'), ('NOL', 'New Orleans')):
        c = mp(*CITY[nm]); cv.circ(c, 6, TXT)
        dx = (-14 if nm == 'NYC' else 14) if PORT else 14
        cv.text((c[0] + dx, c[1] + (44 if (PORT and nm == 'NYC') else 10)), lab, 'sansb', 30, TXT, 'ra' if dx < 0 else 'la', 1.0, 3)
    # counters
    if PORT: cx, cy = CONT[0] + 30, CONT[3] - 190
    else: cx, cy = CONT[0] + 10, CONT[1] + 150
    cv.text((cx, cy), str(int(y)), 'serif', 128 if not PORT else 120, TXT)
    cv.text((cx, cy + 150), (f'about {int(round(mi, -4 if mi >= 100000 else -3 if mi >= 20000 else -2)):,} miles of line' if mi > 500 else f'{int(mi):,} miles of line'), 'sansb', 44, AMBER)
    cv.text((cx, cy + 205), 'in the United States', 'sans', 34, DIM)

def sc_share(cv, t, p):
    a = ease(t / 1.0); bx0, bx1 = CONT[0] + 20, CONT[2] - 20; by0 = CONT[1] + (270 if not PORT else 330); bh = 130 if not PORT else 150
    cv.text((W / 2, CONT[1] + 10), '~40%', 'serif', SZ['big'], AMBER, 'ma', a)
    cv.text((W / 2, CONT[1] + (190 if not PORT else 190)), 'of long-distance freight, in ton-miles', 'sans', 40, TXT, 'ma', a)
    f = ease((t - 0.8) / 1.8); w = bx1 - bx0
    cv.rect((bx0, by0, bx1, by0 + bh), mix(STEEL, BG, 0.55), 10)
    cv.rect((bx0, by0, bx0 + w * 0.40 * f, by0 + bh), AMBER, 10)
    if f > 0.99:
        cv.text((bx0 + w * 0.20, by0 + bh / 2), 'Freight rail', 'sansb', 40, BG, 'mm')
        cv.text((bx0 + w * 0.70, by0 + bh / 2 - 18), 'All other modes', 'sansb', 40, TXT, 'mm')
        cv.text((bx0 + w * 0.70, by0 + bh / 2 + 34), 'trucks · barges · pipelines · air', 'sans', 30, DIM, 'mm')
    cv.text((W / 2, by0 + bh + 40), 'One ton-mile = one ton of freight moved one mile', 'sans', 34, DIM, 'ma', ease((t - 2.5) / 1))
    xe = -500 + ((t * 0.22) % 1.0) * (W + 900)
    train(cv, xe, by0 - 50 if not PORT else by0 - 40, 1.0, AMBER, 6, 0.9)

def sc_eff(cv, t, p):
    x0 = CONT[0] + 30; x1 = CONT[2] - 30; w = x1 - x0
    top = CONT[1] + 30
    cv.text((x0, top), 'Miles one ton of freight goes on one gallon of fuel', 'sansb', 38 if not PORT else 40, TXT)
    rows = [('Train', 500, 500, AMBER), ('Truck', 125, 167, STEEL)]
    y = top + (120 if not PORT else 150)
    for i, (nm, lo, hi, col) in enumerate(rows):
        f = ease((t - 0.6 - i * 1.4) / 1.6)
        if nm == 'Train': train(cv, x0, y + 44, 0.8, AMBER, 2)
        else: truck(cv, x0, y + 50, 0.9, STEEL)
        by = y + 56
        cv.rect((x0, by, x1, by + 80), mix(STEEL, BG, 0.2), 8)
        cv.rect((x0, by, x0 + w * (lo / 500.0) * f, by + 80), col, 8)
        if hi > lo:
            cv.rect((x0 + w * (lo / 500.0) * f, by, x0 + w * (hi / 500.0) * f, by + 80), mix(col, BG, 0.55), 0)
        lab = '≈ 500 miles  (AAR: "nearly 500")' if nm == 'Train' else ''
        if f > 0.99:
            if nm == 'Train': cv.text((x0 + 22, by + 40), lab, 'sansb', 36 if not PORT else 34, BG, 'lm')
            else: cv.text((x0 + w * (hi / 500.0) + 20, by + 40), '≈ 125–165 miles' if not PORT else '125–165', 'sansb', 36, TXT, 'lm')
        y += 215 if not PORT else 290
    for m in (0, 100, 200, 300, 400, 500):
        xx = x0 + w * m / 500.0; cv.text((xx, y - 40), str(m), 'sans', 28, DIM, 'ma' if 0 < m < 500 else ('la' if m == 0 else 'ra'))
    cv.text((x0, y + 10), 'The railroads\' own figures. The truck range is implied by their "3 to 4 times" estimate.', 'sans', 30, DIM) if not PORT else \
        cv.para(x0, y + 10, 'The railroads\' own figures. The truck range is implied by their "3 to 4 times" estimate.', 'sans', 30, DIM, w)

def sc_fogel(cv, t, p):
    x0 = CONT[0] + 30; x1 = CONT[2] - 30; w = x1 - x0
    cv.text((x0, CONT[1] + 10), 'U.S. economy, 1890  =  100% of national output', 'sansb', 38, TXT, 'la', ease(t / 0.8))
    by = CONT[1] + 80; bh = 110 if not PORT else 120
    f = ease((t - 0.8) / 1.2)
    cv.rect((x0, by, x0 + w * f, by + bh), mix(STEEL, BG, 0.6), 6)
    sl = w * 0.027 * ease((t - 4.0) / 1.2)
    cv.rect((x0, by, x0 + max(sl, 0), by + bh), AMBER, 0)
    if sl > 5:
        cv.line([(x0 + sl / 2, by + bh), (x0 + sl / 2, by + bh + 50)], AMBER, 3)
        cv.text((x0, by + bh + 58), '≤ 2.7%', 'serif', 96 if not PORT else 90, AMBER)
        cv.para(x0, by + bh + 172, 'most that railroads saved on farm freight (Fogel, 1964)', 'sans', 38, TXT, w)
    # the no-railroad country
    yy = CONT[3] - (220 if not PORT else 290)
    cv.text((x0, yy), 'Fogel\'s country without railroads:', 'sansb', 36, DIM, 'la', ease((t - 2.2) / 0.8))
    cx = x0
    for i, nm in enumerate(('rivers', 'canals', 'wagons')):
        a = ease((t - 2.8 - i * 0.7) / 0.6); f2 = font('sansb', 42)
        wd = f2.getlength(nm) / SS + 56
        cv.rect((cx, yy + 56, cx + wd, yy + 126), mix(STEEL, BG, 0.45 * a + 0.0), 14) if a > 0 else None
        cv.text((cx + wd / 2, yy + 91), nm, 'sansb', 42, TXT, 'mm', a)
        cx += wd + 24
    n = ease((t - 14.0) / 1.0)
    if n > 0.01:
        cv.text((x0, yy + (150 if not PORT else 150)), 'Nobel Memorial Prize in Economics, 1993', 'serifr', 38, AMBER, 'la', n)

def sc_debate(cv, t, p):
    x0 = CONT[0] + 30; x1 = CONT[2] - 30; w = x1 - x0
    cv.text((x0, CONT[1] + 8), 'The critics', 'serif', 54, AMBER, 'la', ease(t / 0.8))
    y = cv.para(x0, CONT[1] + 82, '“Compared to an economy that never existed.” (Fishlow, 1965, and others)' if False else
                'Fogel compared railroads to an economy that never existed.', 'sans', 40, TXT, w, 1.25, 'l', ease((t - 1.0) / 0.8))
    by = CONT[1] + (280 if not PORT else 330)
    cv.text((x0, by), 'Value of American farmland, 1890', 'sansb', 38, TXT, 'la', ease((t - 6.0) / 0.8))
    f = ease((t - 7.0) / 1.4); g = ease((t - 9.0) / 1.6); bh = 80
    cv.rect((x0, by + 70, x0 + w * f, by + 70 + bh), AMBER, 8)
    if f > 0.99: cv.text((x0 + 20, by + 70 + bh / 2), 'With railroads  =  100', 'sansb', 36, BG, 'lm')
    cv.rect((x0, by + 70 + bh + 24, x0 + w * 0.398 * g, by + 70 + bh * 2 + 24), STEEL, 8)
    if g > 0.99: cv.text((x0 + 20, by + 70 + bh * 1.5 + 24), 'Without  ≈ 40', 'sansb', 36, TXT, 'lm')
    if g > 0.5:
        a = ease((g - 0.5) / 0.5)
        cv.text((x0 + w * 0.40 + 24, by + 70 + bh * 1.5 + 24), 'about 60% less', 'serif', 44, RED, 'lm', a) if not PORT else \
            cv.text((x1, by + 70 + bh * 1.5 + 24), '−60%', 'serif', 56, RED, 'rm', a)
    cv.text((x0, by + 70 + bh * 2 + 60), '(Donaldson & Hornbeck, 2016)', 'sans', 32, DIM, 'la', ease((t - 10.0) / 0.8))
    n = ease((t - 14.0) / 1.0)
    cv.rect((x0, CONT[3] - 100, x1, CONT[3] - 20), mix(AMBER, BG, 0.18 * n), 14)
    cv.text((W / 2, CONT[3] - 60), 'Land value, not output. Not the same measure.', 'sansb', 36 if not PORT else 34, TXT, 'mm', n)

ZONES = [('Eastern', -75.0, -82.5), ('Central', -90.0, -97.5), ('Mountain', -105.0, -112.5), ('Pacific', -120.0, -180.0)]
ZCITY = [('New York', -74.0, 40.7, 0), ('Pittsburgh', -80.0, 40.44, 0), ('Chicago', -87.63, 41.88, 1), ('St. Louis', -90.2, 38.63, 1),
         ('Denver', -105.0, 39.74, 2), ('Salt Lake', -111.89, 40.76, 2), ('San Francisco', -122.42, 37.77, 3)]
def sc_time(cv, t, p):
    mb = (CONT[0], CONT[1] + 70, CONT[2], CONT[3]) if PORT else (CONT[0] + 40, CONT[1] + 10, CONT[2] - 40, CONT[3])
    mp = mapper(mb); draw_us(cv, mp)
    snap = ease((t - 7.4) / 1.4)
    cols = [(60, 100, 170), (50, 150, 140), (140, 110, 190), (190, 140, 70)]
    layer = Image.new('RGB', cv.im.size, LAND); ld = ImageDraw.Draw(layer)
    mask = Image.new('L', cv.im.size, 0)
    ImageDraw.Draw(mask).polygon([cv.P(mp(*q)) for q in OUT], fill=255)
    top = mp(-96, 49.0)[1] - 40; bot = mp(-96, 25.0)[1] + 10
    for i, (nm, mer, edge) in enumerate(ZONES):
        lo = mp(-67 if i == 0 else ZONES[i - 1][2], 40)[0]; hi = mp(edge if i < 3 else -130, 40)[0]
        xa, xb = (lo, hi) if lo < hi else (hi, lo)
        k = ease((t - 6.8 - i * 0.35) / 0.8)
        if k > 0.01:
            ld.rectangle([(xa + 2) * SS, top * SS, (xb - 2) * SS, (top + (bot - top) * k) * SS], fill=mix(cols[i], LAND, 0.55))
            cv.text(((xa + xb) / 2, bot - 50), nm, 'sansb', 30, TXT, 'ma', k, 3)
    cv.im.paste(layer, (0, 0), mask)
    cv.d.line([cv.P(q) for q in [mp(*q) for q in OUT] + [mp(*OUT[0])]], fill=LANDEDGE, width=int(2.5 * SS))
    for nm, lon, lat, z in ZCITY:
        c = mp(lon, lat)
        off = (lon - ZONES[z][1]) * 4.0
        sun = 12 * 60 + off; sunt = f'{int(sun // 60)}:{int(round(sun % 60)):02d}'
        shown = sunt if snap < 0.5 else '12:00'
        col = AMBER if snap < 0.5 else TEAL
        if not PORT or nm in ('New York', 'Chicago', 'Denver', 'San Francisco'):
            dy = -54 if z % 2 == 0 else 16
            cv.text((c[0], c[1] + dy), shown, 'sansb', 34, col, 'ma', ease(t / 1.5), 4)
        cv.circ(c, 7, TXT)
    lab = 'Before: each town on its own sun time' if snap < 0.5 else 'After: four railroad time zones'
    cv.para(CONT[0] + 10, CONT[1] + 6, lab, 'sansb', 38, AMBER if snap < 0.5 else TEAL, 380 if not PORT else 900, 1.2, 'l', ease(t / 1.2))

def sc_today(cv, t, p):
    x0 = CONT[0] + 30; x1 = CONT[2] - 30; w = x1 - x0
    cv.text((x0, CONT[1] + 10), 'Long-distance freight, by ton-miles', 'sansb', 40, TXT, 'la', ease(t / 0.8))
    by = CONT[1] + 90; bh = 100
    cv.rect((x0, by, x1, by + bh), mix(STEEL, BG, 0.5), 10)
    mv = ease((t - 3.5) / 1.2)
    cv.rect((x0, by, x0 + w * 0.40, by + bh), mix(AMBER, RED, mv), 10)
    cv.text((x0 + w * 0.20, by + bh / 2), '40%  rail' if mv < 0.5 else '40%  stops', 'sansb', 36, BG, 'mm')
    cv.text((x0 + w * 0.70, by + bh / 2), 'other modes', 'sansb', 36, TXT, 'mm')
    if mv > 0.3:
        cv.text((x0 + w * 0.20, by + bh + 14), '→ trucks & others', 'sansb', 32, RED, 'ma', ease((mv - 0.3) / 0.7))
    fy = by + 230 if not PORT else by + 260
    cv.text((x0, fy - 62), "Fuel for each ton moved (railroads' estimate)", 'sansb', 38, TXT, 'la', ease((t - 7.0) / 0.8))
    unit = 120 if not PORT else 100
    a1 = ease((t - 8.0) / 0.8)
    cv.rect((x0, fy + 20, x0 + unit * a1, fy + 20 + 80), AMBER, 8)
    cv.text((x0 + unit + 20, fy + 60), 'Rail  1×', 'sansb', 40, TXT, 'lm', a1)
    a2 = ease((t - 9.0) / 1.5)
    cv.rect((x0, fy + 140, x0 + unit * 3.5 * a2, fy + 140 + 80), RED, 8)
    cv.text((x0 + unit * 3.5 + 20, fy + 180), 'Truck  3–4×', 'sansb', 40, TXT, 'lm', ease((t - 10.0) / 0.8))
    cv.text((x0, CONT[3] - 20), "Our reasoning from the railroads' figures, not a forecast.", 'sans', 30, DIM, 'ls', ease((t - 10.5) / 0.8))

def sc_end(cv, t, p):
    a = ease(t / 1.0)
    cy = 560 if PORT else 200
    cv.text((W / 2, cy), 'Heartbeat Observatory', 'serif', 84 if PORT else 100, TXT, 'ma', a)
    cv.text((W / 2, cy + (130 if PORT else 140)), 'heartbeatobservatory.com', 'sansb', 52 if PORT else 56, AMBER, 'ma', a)
    cv.text((W / 2, cy + 260), 'History · Episode 1', 'sans', 38, DIM, 'ma', a)
    src = ['AAR, Freight Rail Facts & Figures', 'R. Fogel, Railroads and American Economic Growth (1964)', 'Donaldson & Hornbeck, Quarterly Journal of Economics (2016)',
           'Library of Congress (time zones) · U.S. Census, Historical Statistics']
    y = cy + 360
    cv.text((W / 2, y), 'Sources', 'sansb', 32, DIM, 'ma', ease((t - 0.6) / 1))
    for i, s in enumerate(src):
        yy = cv.para(W / 2, y + 48 + i * (84 if PORT else 46), s, 'sans', 30 if PORT else 30, TXT, W - 120 if PORT else 1500, 1.2, 'm', ease((t - 0.8 - i * 0.2) / 0.8))

# ---------------------------------------------------------------- scene table
SUBS = {
 's1': ['What if America had never built its railroads?'],
 's2': ['In 1830, the United States had 23 miles of railroad.', 'By 1890, about 160,000.', 'By 1916, the peak: about a quarter of a million miles.'],
 's3': ['Today, freight railroads still carry about 40% of America\'s long-distance freight, in ton-miles.', 'More than any other way of moving goods.'],
 's4': ['And a train is efficient.', 'The railroads report one ton of freight goes nearly 500 miles on a gallon of fuel.', 'They estimate that is 3 to 4 times better than a truck.'],
 's5': ['Without railroads, would the country have stalled?', 'In 1964, economist Robert Fogel argued: not by much.', 'He compared 1890 with a country of rivers, canals and wagons.',
        'For farm freight, he put the savings at no more than 2.7% of national output.', 'He shared the 1993 Nobel Prize in economics.'],
 's6': ['The debate did not end there.', 'Critics said Fogel compared railroads to an economy that never existed.',
        'In 2016, Donaldson and Hornbeck estimated 1890 farmland would be worth about 60% less without railroads.', 'That is land value, not output, so the numbers do not directly compare.', 'Economists still argue.'],
 's7': ['Railroads also changed the clock.', 'Before November 18, 1883, every town kept its own sun time.', 'That day, the railroads switched to standard time zones.',
        'People called it the Day of Two Noons.', 'Congress made it law in 1918.'],
 's8': ['So what if trains stopped today?', 'About 40% of long-distance freight would move to other modes, mostly trucks,', 'which use roughly 3 to 4 times the fuel per ton.', 'The railroads are quiet. But a lot rides on them.'],
 's9': [],
}
SCENES = [  # id, headline, source line, fn
 ('s1', '', '', sc_title),
 ('s2', 'Rails across a continent', "Sources: U.S. Census Bureau, Historical Statistics; 1890: Poor's Manual of Railroads (160,817 mi). Figures vary by definition.", sc_map),
 ('s3', 'Rail today', 'Source: Association of American Railroads (AAR), Freight Rail Facts & Figures', sc_share),
 ('s4', 'One ton. One gallon.', 'Source: AAR (industry figures: ~500 ton-miles per gallon; 3–4× trucks)', sc_eff),
 ('s5', 'The case: “not by much”', 'Source: R. Fogel, Railroads and American Economic Growth (1964); Nobel 1993, shared with D. North', sc_fogel),
 ('s6', 'A debate, not a verdict', 'Sources: critiques of Fogel’s counterfactual (e.g. Fishlow, 1965); Donaldson & Hornbeck, QJE 2016', sc_debate),
 ('s7', 'The Day of Two Noons', 'Source: Library of Congress; Standard Time Act, 1918. Zone edges approximate.', sc_time),
 ('s8', 'If trains stopped today', 'Based on AAR figures (≈40% of ton-miles; 3–4× fuel per ton). Our reasoning.', sc_today),
 ('s9', '', '', sc_end),
]
bounds = []
for i, (sid, *_r) in enumerate(SCENES):
    s0 = 0.0 if i == 0 else SEG[sid]['start'] - 0.5
    s1 = TOTAL if i == len(SCENES) - 1 else SEG[SCENES[i + 1][0]]['start'] - 0.5
    bounds.append((s0, s1))

def subtitle_at(sid, tt):
    seg = SEG[sid]; subs = SUBS[sid]; rel = tt - seg['start']
    if not subs: return None
    if rel < -0.1 or rel > seg['dur'] + 0.8: return None
    tot = sum(len(s) for s in subs); acc = 0
    for s in subs:
        a = acc / tot * seg['dur']; acc += len(s); b = acc / tot * seg['dur']
        if rel <= b + (0.8 if s is subs[-1] else 0): return s
    return subs[-1]

def frame(tt):
    cv = Cv()
    for i, (sid, head, src, fn) in enumerate(SCENES):
        s0, s1 = bounds[i]
        if s0 <= tt < s1 or (i == len(SCENES) - 1 and tt >= s0): break
    t = tt - s0; p = clamp01(t / max(0.1, s1 - s0 - 0.6))
    if head:
        a = ease(t / 0.6)
        f = font('serif', SZ['head']); ls = wrap(head, f, HEAD[2] - HEAD[0])
        for k, l in enumerate(ls): cv.text((HEAD[0], HEAD[1] + k * SZ['head'] * 1.15), l, 'serif', SZ['head'], TXT, 'la', a)
        ry = HEAD[3] - 6 if not PORT else HEAD[1] + len(ls) * SZ['head'] * 1.15 + 14
        cv.rect((HEAD[0], ry, HEAD[0] + 120, ry + 4), AMBER)
    fn(cv, t, p)
    sub = subtitle_at(sid, tt)
    if sub:
        f = font('sans', SZ['cap']); ls = wrap(sub, f, CAP[2] - CAP[0]); n = len(ls)
        y0 = CAP[1] + (CAP[3] - CAP[1] - n * SZ['cap'] * 1.28) / 2 if not PORT else CAP[1] + 20
        for k, l in enumerate(ls):
            cv.text((W / 2, y0 + k * SZ['cap'] * 1.28), l, 'sans', SZ['cap'], TXT, 'ma')
    if src:
        cv.para(SRC[0], SRC[1] if not PORT else SRC[1], src, 'sans', SZ['src'], DIM, SRC[2] - SRC[0], 1.25, 'l', ease(t / 1.2))
    im = cv.im.reduce(SS)
    # dip-to-dark at scene edges and the very start/end
    fa = min(1.0, t / 0.35, (s1 - tt) / 0.35 if i < len(SCENES) - 1 else (TOTAL - tt) / 1.2)
    if fa < 1.0: im = Image.blend(Image.new('RGB', im.size, BG), im, max(0.0, fa))
    return im

def work(n):
    return frame(n / FPS).tobytes()

if __name__ == '__main__':
    if '--still' in sys.argv:
        i = sys.argv.index('--still'); frame(float(sys.argv[i + 1])).save(sys.argv[i + 2]); sys.exit()
    out = sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else f'video_{ORI}.mp4'
    a, b = 0, int(TOTAL * FPS)
    if '--secs' in sys.argv:
        i = sys.argv.index('--secs'); a, b = int(float(sys.argv[i + 1]) * FPS), int(float(sys.argv[i + 2]) * FPS)
    ff = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                           '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
    with Pool(14) as pool:
        for k, buf in enumerate(pool.imap(work, range(a, b), chunksize=4)):
            ff.stdin.write(buf)
            if k % 300 == 0: print(k, '/', b - a, flush=True)
    ff.stdin.close(); ff.wait()
