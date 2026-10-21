# Heartbeat TV shared renderer (look = History ep1/ep2 + Science ep1: dark navy cards, gold numbers, serif headline,
# one idea per screen, source line at the bottom, burned-in captions). Pillow, 2x supersampled, frames piped to ffmpeg.
# An episode file does:  from tvlib import *   ... define SUBS, SCENES ...   configure(SUBS, SCENES)   if __name__=='__main__': main()
#   python ep.py land|port [--still SECONDS out.png] [--secs A B] [--out file.mp4]
import json, math, subprocess, sys, random
from multiprocessing import Pool
from PIL import Image, ImageDraw, ImageFont

TL = json.load(open('timeline.json'))
TOTAL = TL['total']; SEG = {s['id']: s for s in TL['segs']}
FPS = 30; SS = 2
ORI = 'port' if 'port' in sys.argv[1:2] else 'land'
PORT = ORI == 'port'
W, H = (1080, 1920) if PORT else (1920, 1080)

BG = (11, 18, 32); BG2 = (17, 28, 48)
AMBER = (242, 177, 52); STEEL = (96, 124, 158); TXT = (236, 240, 246); DIM = (142, 156, 178)
RED = (222, 98, 84); TEAL = (88, 190, 178); BLUE = (96, 160, 230); GREEN = (120, 200, 130)
CARD = (22, 36, 60)

FD = 'C:/Windows/Fonts/'
_fc = {}
def font(kind, size):
    k = (kind, size)
    if k not in _fc:
        f = {'serif': 'georgiab.ttf', 'serifr': 'georgia.ttf', 'sans': 'segoeui.ttf', 'sansb': 'segoeuib.ttf'}[kind]
        _fc[k] = ImageFont.truetype(FD + f, int(size * SS))
    return _fc[k]

SZ = dict(head=64 if PORT else 72, cap=54 if PORT else 46, src=32 if PORT else 30)
if PORT:
    HEAD = (50, 70, W - 50, 330); CONT = (30, 350, W - 30, 1230); CAP = (60, 1290, W - 60, 1740); SRC = (60, 1770, W - 60, 1890)
else:
    HEAD = (70, 36, W - 70, 170); CONT = (60, 190, W - 60, 830); CAP = (110, 850, W - 110, 990); SRC = (110, 1000, W - 110, 1070)

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
    def outline(s, b, col, w=3, r=0):
        bb = [b[0] * SS, b[1] * SS, b[2] * SS, b[3] * SS]
        s.d.rounded_rectangle(bb, radius=r * SS, outline=col, width=int(w * SS))
    def line(s, pts, col, w):
        s.d.line([s.P(p) for p in pts], fill=col, width=int(w * SS), joint='curve')
    def poly(s, pts, fill, edge=None):
        s.d.polygon([s.P(p) for p in pts], fill=fill, outline=edge)
    def circ(s, c, r, fill):
        s.d.ellipse([(c[0] - r) * SS, (c[1] - r) * SS, (c[0] + r) * SS, (c[1] + r) * SS], fill=fill)
    def ring(s, c, r, col, w=3):
        s.d.ellipse([(c[0] - r) * SS, (c[1] - r) * SS, (c[0] + r) * SS, (c[1] + r) * SS], outline=col, width=int(w * SS))
    def text(s, xy, t, kind, size, col, anchor='la', a=1.0, stroke=0):
        s.d.text(s.P(xy), t, font=font(kind, size), fill=mix(col, BG, a), anchor=anchor, stroke_width=int(stroke * SS), stroke_fill=BG)
    def para(s, x, y, t, kind, size, col, maxw, lh=1.25, anchor='l', a=1.0):
        f = font(kind, size); ls = wrap(t, f, maxw)
        for i, l in enumerate(ls):
            s.d.text(s.P((x, y + i * size * lh)), l, font=f, fill=mix(col, BG, a), anchor='ma' if anchor == 'm' else 'la')
        return y + len(ls) * size * lh

# ------------------------------------------------------------------ reusable pieces
def badge(cv, x, y, label, col=RED, a=1.0, size=30, anchor='l'):
    f = font('sansb', size); w = f.getlength(label) / SS + 36; h = size + 20
    x0 = x if anchor == 'l' else x - w / 2
    cv.rect((x0, y, x0 + w, y + h), mix(col, BG, 0.22 * a), 10)
    cv.outline((x0, y, x0 + w, y + h), mix(col, BG, a), 3, 10)
    cv.text((x0 + w / 2, y + 9), label, 'sansb', size, col, 'ma', a)
    return w

def fit_serif(txt, ns, maxw):
    while ns > 30 and font('serif', ns).getlength(txt) / SS > maxw: ns -= 4
    return ns

def count(v, t, t0, dur=1.2, fmt='{:,.0f}'):
    return fmt.format(v * ease((t - t0) / dur))

def stat_cards(cv, t, items, area=None):
    """items: dict(num, label, sub, at, col, tag).  Cards side by side (land) or stacked (port)."""
    n = len(items); x0, y0, x1, y1 = area or CONT
    gap = 28
    for i, it in enumerate(items):
        a = ease((t - it.get('at', 0)) / 0.6)
        if a <= 0: continue
        col = it.get('col', AMBER)
        if PORT:
            h = (y1 - y0 - gap * (n - 1)) / n; bx = (x0, y0 + i * (h + gap), x1, y0 + i * (h + gap) + h)
            cv.rect(bx, mix(CARD, BG, a), 18); cv.outline(bx, mix(STEEL, BG, 0.5 * a), 2, 18)
            numw = 380
            ns = fit_serif(it['num'], 92, numw - 20)
            cv.text((bx[0] + 30, (bx[1] + bx[3]) / 2 - ns * 0.62), it['num'], 'serif', ns, col, 'la', a)
            ty = bx[1] + 26
            ty = cv.para(bx[0] + 30 + numw, ty, it['label'], 'sansb', 36, TXT, bx[2] - bx[0] - numw - 60, 1.15, 'l', a)
            if it.get('sub'): cv.para(bx[0] + 30 + numw, ty + 6, it['sub'], 'sans', 30, DIM, bx[2] - bx[0] - numw - 60, 1.2, 'l', a)
            if it.get('tag'): badge(cv, bx[0] + 30 + numw, bx[3] - 62, it['tag'], RED, a, 26)
        else:
            hh = min(y1 - y0, 470 if n < 4 else 580); yy0 = y0 + (y1 - y0 - hh) / 2
            w = (x1 - x0 - gap * (n - 1)) / n; bx = (x0 + i * (w + gap), yy0, x0 + i * (w + gap) + w, yy0 + hh)
            cv.rect(bx, mix(CARD, BG, a), 20); cv.outline(bx, mix(STEEL, BG, 0.5 * a), 2, 20)
            ns = fit_serif(it['num'], 120 if n <= 3 else 100, w - 50)
            cv.text(((bx[0] + bx[2]) / 2, bx[1] + 30), it['num'], 'serif', ns, col, 'ma', a)
            ty = bx[1] + 30 + ns * 1.35
            ty = cv.para((bx[0] + bx[2]) / 2, ty, it['label'], 'sansb', 40, TXT, w - 50, 1.15, 'm', a)
            if it.get('sub'): cv.para((bx[0] + bx[2]) / 2, ty + 10, it['sub'], 'sans', 32, DIM, w - 50, 1.2, 'm', a)
            if it.get('tag'): badge(cv, (bx[0] + bx[2]) / 2, bx[3] - 70, it['tag'], RED, a, 28, 'm')

def hbars(cv, t, rows, vmax, area=None, label_w=None, fmt='{:,.0f}', unit=''):
    """rows: dict(label,val,txt,at,col,tag).  Horizontal bars."""
    x0, y0, x1, y1 = area or CONT
    n = len(rows); step = (y1 - y0) / n; bh = min(70, step * 0.55)
    lw = label_w or (440 if not PORT else 330)
    for i, r in enumerate(rows):
        a = ease((t - r.get('at', 0)) / 0.5)
        if a <= 0: continue
        y = y0 + i * step + (step - bh) / 2
        col = r.get('col', AMBER)
        ls = wrap(r['label'], font('sansb', 32 if not PORT else 30), lw - 20)
        for k, l in enumerate(ls): cv.text((x0 + lw - 16, y + bh / 2 - len(ls) * 19 + k * 38), l, 'sansb', 32 if not PORT else 30, TXT, 'ra', a)
        full = x1 - x0 - lw - (250 if not PORT else 200)
        u = ease((t - r.get('at', 0) - 0.2) / 1.1)
        bw = max(6, full * r['val'] / vmax * u)
        cv.rect((x0 + lw, y, x0 + lw + bw, y + bh), mix(col, BG, a), 8)
        cv.text((x0 + lw + bw + 14, y + bh / 2 - 22), r.get('txt', fmt.format(r['val'] * u) + unit), 'serif', 40 if not PORT else 36, col, 'la', a)
        if r.get('tag'): badge(cv, x0 + lw + 10, y + bh + 4, r['tag'], RED, a, 22)

def statements(cv, t, lines, y0=None):
    """lines: (at, text, col, kind) big centred serif lines."""
    y = y0 if y0 is not None else CONT[1] + (110 if not PORT else 120)
    for i, (tc, txt, col, kind) in enumerate(lines):
        a = ease((t - tc) / 0.7)
        sz = (66 if kind == 'serifr' else 84) if not PORT else (60 if kind == 'serifr' else 80)
        ls = wrap(txt, font(kind, sz), W - 140)
        for k, l in enumerate(ls): cv.text((W / 2, y + k * sz * 1.15), l, kind, sz, col, 'ma', a)
        y += len(ls) * sz * 1.15 + 26

def note(cv, t, t0, txt, y=None, col=DIM, size=30):
    a = ease((t - t0) / 0.8)
    if a > 0: cv.para(W / 2, y if y is not None else CONT[3] - 70, txt, 'sans', size, col, W - 160, 1.2, 'm', a)

def arrow(cv, p0, p1, col, w=4, head=16, a=1.0):
    c = mix(col, BG, a); cv.line([p0, p1], c, w)
    ang = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
    cv.poly([p1, (p1[0] - head * math.cos(ang - 0.45), p1[1] - head * math.sin(ang - 0.45)),
             (p1[0] - head * math.cos(ang + 0.45), p1[1] - head * math.sin(ang + 0.45))], c)

def title_block(cv, t, series, ep, l1, l2, tag):
    a = ease(t / 1.2)
    cv.text((W / 2, 150 if PORT else 36), f'HEARTBEAT TV  ·  {series}  ·  EPISODE {ep}', 'sansb', 34 if PORT else 36, AMBER, 'ma', a)
    for k, l in enumerate((l1, l2)):
        cv.text((W / 2, (230 if PORT else 90) + k * (110 if PORT else 128)), l, 'serif', 96 if PORT else 112, TXT, 'ma', ease((t - 0.2) / 1.2), 6)
    cv.text((W / 2, 1330 if PORT else 960), tag, 'serifr', 44, DIM, 'ma', ease((t - 1.0) / 1.0))

def end_block(cv, t, series, ep, sources):
    a = ease(t / 1.0)
    cy = 330 if PORT else 110
    cv.text((W / 2, cy), 'Heartbeat Observatory', 'serif', 84 if PORT else 100, TXT, 'ma', a)
    cv.text((W / 2, cy + (130 if PORT else 140)), 'heartbeatobservatory.com', 'sansb', 52 if PORT else 56, AMBER, 'ma', a)
    cv.text((W / 2, cy + 250), f'{series} · Episode {ep}', 'sans', 38, DIM, 'ma', a)
    y = cy + 330
    cv.text((W / 2, y), 'Sources', 'sansb', 32, DIM, 'ma', ease((t - 0.6) / 1))
    yy = y + 50
    for i, s in enumerate(sources):
        yy = cv.para(W / 2, yy, s, 'sans', 30, TXT, W - 120 if PORT else 1600, 1.2, 'm', ease((t - 0.8 - i * 0.2) / 0.8)) + 12

# ------------------------------------------------------------------ framework
SUBS = {}; SCENES = []; bounds = []; BOUND = {}

def configure(subs, scenes):
    global SUBS, SCENES, bounds, BOUND
    SUBS, SCENES = subs, scenes; bounds = []
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
    if not subs: return None
    if rel < -0.1 or rel > seg['dur'] + 0.8: return None
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
        for k, l in enumerate(ls): cv.text((W / 2, y0 + k * SZ['cap'] * 1.28), l, 'sans', SZ['cap'], TXT, 'ma')
    if src:
        cv.para(SRC[0], SRC[1], src, 'sans', SZ['src'], DIM, SRC[2] - SRC[0], 1.25, 'l', ease(t / 1.2))
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
    with Pool(24) as pool:
        for k, buf in enumerate(pool.imap(work, range(a, b), chunksize=int(__import__('os').environ.get('TVCHUNK', 4)))):
            ff.stdin.write(buf)
            if k % 600 == 0: print(k, '/', b - a, flush=True)
    ff.stdin.close(); ff.wait()
