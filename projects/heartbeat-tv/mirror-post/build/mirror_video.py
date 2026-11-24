# "In our own image" post video.  Pillow + numpy frames piped to ffmpeg; audio synthesized here (no downloads).
#   python build/mirror_video.py port|land render [--out file.mp4]
#   python build/mirror_video.py port|land still SECONDS out.png
#   python build/mirror_video.py port audio          (writes build/audio.wav)
#   python build/mirror_video.py port sheet          (contact sheet from the finished vertical file)
# House look from projects/tv-lib/tvlib.py: dark navy, gold numbers, serif.
import sys, os, math, random, subprocess, wave
import numpy as np
from multiprocessing import Pool
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
ORI = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] in ('port', 'land') else 'port'
PORT = ORI == 'port'
W, H = (1080, 1920) if PORT else (1920, 1080)
FPS = 30; SS = 2

BG = (11, 18, 32); AMBER = (242, 177, 52); TXT = (236, 240, 246); DIM = (142, 156, 178)
TEAL = (88, 190, 178); BLUE = (140, 184, 240); STEEL = (96, 124, 158)
FD = 'C:/Windows/Fonts/'
FONTS = {'serif': 'georgiab.ttf', 'serifr': 'georgia.ttf', 'serifi': 'georgiai.ttf', 'sans': 'segoeui.ttf', 'sansb': 'segoeuib.ttf'}
_fc = {}
def font(kind, size):
    k = (kind, int(size * SS))
    if k not in _fc: _fc[k] = ImageFont.truetype(FD + FONTS[kind], k[1])
    return _fc[k]
def mix(c, d, a): return tuple(int(c[i] * a + d[i] * (1 - a)) for i in range(3))
def clamp01(x): return max(0.0, min(1.0, x))
def ease(x): x = clamp01(x); return x * x * (3 - 2 * x)
def lerp(a, b, u): return a + (b - a) * u
def wrap(txt, f, maxw):
    lines = []; cur = ''
    for w in txt.split():
        t = (cur + ' ' + w).strip()
        if f.getlength(t) <= maxw * SS or not cur: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

# ------------------------------------------------------------------ the quotes (all from quotes.md, confirmed rows only)
# big = the number as shown; words = the person's exact words (shown in quote marks); about = plain label of what it measures
# kind: doom = odds it goes badly (gold), low = doubters and good odds (teal), when = how soon (blue)
SLOW = [
    dict(name='Geoffrey Hinton', role='AI pioneer, University of Toronto', big='10% to 20%', kind='doom',
         about='that AI wipes out humanity within about 30 years', words='',
         src='BBC Radio 4 Today, 27 Dec 2024, as printed by The Guardian'),
    dict(name='Dario Amodei', role='CEO, Anthropic', big='25%', kind='doom',
         about='', words='I think there\u2019s a 25% chance that things go really, really badly.',
         src='Axios AI+ DC Summit, 17 Sep 2025, as printed by TechRadar'),
    dict(name='Elon Musk', role='Tesla, SpaceX, xAI', big='10 to 20%', kind='doom',
         about='', words='some chance, which could be, 10 to 20 per cent, that it goes bad',
         src='Future Investment Initiative, Riyadh, 29 Oct 2024, as printed by The National'),
    dict(name='Yoshua Bengio', role='Mila, Universit\u00e9 de Montr\u00e9al', big='20%', kind='doom',
         about='', words='around, like, 20 per cent probability that it turns out catastrophic',
         src='ABC News Australia, 15 Jul 2023'),
]
FAST = [
    dict(name='Emad Mostaque', big='50%', kind='doom', about='\u201cMy P(doom) is 50%.\u201d', src='X post, 4 Dec 2024'),
    dict(name='Paul Christiano', big='46%', kind='doom', about='humanity \u201cirreversibly messed up our future\u201d', src='LessWrong, 27 Apr 2023'),
    dict(name='Survey of 2,778 AI researchers', big='5%', kind='low', about='median odds of extinction or similar', src='Grace et al., arXiv 2401.02843, Jan 2024'),
    dict(name='Dan Hendrycks', big='over 80%', kind='doom', about='\u201cmy p(doom) > 80%\u201d', src='X post, 2 Apr 2023'),
    dict(name='Yann LeCun', big='essentially zero', kind='low', about='\u201cthe existential risk is essentially zero\u201d', src='X post, 13 Apr 2026'),
    dict(name='Vitalik Buterin', big='10%', kind='doom', about='\u201cMy p(doom) is around 0.1.\u201d', src='X post, 27 Nov 2023'),
    dict(name='Sam Altman', big='a few thousand days', kind='when', about='until superintelligence, he says is possible', src='The Intelligence Age, 23 Sep 2024'),
    dict(name='Roman Yampolskiy', big='99.999999%', kind='doom', about='\u201cI am at 99.999999%\u201d', src='X post, 12 Mar 2024'),
    dict(name='Elon Musk', big='80%', kind='low', about='\u201cThe probability of a good outcome is like 80%.\u201d', src='Joe Rogan Experience, Feb 2025, via Business Insider'),
    dict(name='Demis Hassabis', big='50% in 5 to 10 years', kind='when', about='chance of AGI as DeepMind defines it', src='WIRED, 3 Jun 2025'),
    dict(name='Geoffrey Hinton', big='10%', kind='doom', about='extinction in 30 years, if AI is not strongly regulated', src='X post, 31 Oct 2023'),
    dict(name='Eliezer Yudkowsky', big='\u201cYes\u201d', kind='doom', about='ruin, if superintelligence is built like current systems', src='X post, 20 Sep 2026'),
    dict(name='Dario Amodei', big='as early as 2026', kind='when', about='powerful AI \u201ccould come as early as 2026\u201d', src='Machines of Loving Grace, Oct 2024'),
    dict(name='Paul Christiano', big='22%', kind='doom', about='\u201cProbability of an AI takeover: 22%.\u201d', src='LessWrong, 27 Apr 2023'),
    dict(name='Yann LeCun', big='\u201cP(doom) is BS.\u201d', kind='low', about='his words', src='X post, 7 Feb 2024'),
    dict(name='Masayoshi Son', big='2035', kind='when', about='superintelligence: \u201cthat\u2019s coming in 2035\u201d', src='FII Riyadh, 29 Oct 2024, via The National'),
    dict(name='Geoffrey Hinton', big='next 20 years', kind='when', about='AIs \u201csmarter than people\u201d, most experts think', src='BBC Radio 4, 27 Dec 2024, via The Guardian'),
    dict(name='Paul Christiano', big='20%', kind='doom', about='most humans die within 10 years of powerful AI', src='LessWrong, 27 Apr 2023'),
    dict(name='Survey of 2,778 AI researchers', big='50% by 2047', kind='when', about='machines outperform humans at every task', src='Grace et al., arXiv 2401.02843, Jan 2024'),
]
KCOL = {'doom': AMBER, 'low': TEAL, 'when': BLUE}
OPENER = 'People say we might only have so many years before AI turns on us.'
LABEL = 'IN THEIR OWN WORDS'
FOOT = 'Every number is that person\u2019s own. They are not all answering the same question.'
LEGEND = 'Gold: odds it goes badly.  Teal: doubters and good odds.  Blue: how soon.'
LINE = [  # (lines for vertical, lines for wide, colour)
    (['When you try to create', 'a technology'], ['When you try to create a technology'], TXT),
    (['in your own image'], ['in your own image'], AMBER),
    (['and end up creating', 'something you\u2019re scared of,'], ['and end up creating something you\u2019re scared of,'], TXT),
    (['it may be because', 'you\u2019re scared of yourself.'], ['it may be because you\u2019re scared of yourself.'], TXT),
]
CLOSE = ['Become what you want', 'your AI to become.']
CLOSE_WIDE = ['Become what', 'you want your AI', 'to become.']
BRAND = 'Heartbeat Observatory'
def _all_text():
    out = [OPENER, LABEL, FOOT, LEGEND, BRAND] + CLOSE + CLOSE_WIDE
    for q in SLOW + FAST: out += [q.get(k, '') for k in ('name', 'role', 'big', 'about', 'words', 'src')]
    for a, b, _ in LINE: out += a + b
    return out
for s in _all_text():
    assert not any(ch in s for ch in '-\u2010\u2011\u2012\u2013\u2014\u2212'), 'dash in on-screen text: ' + s

# ------------------------------------------------------------------ timeline (seconds); everything hangs off the heartbeat
T_CARDS0 = 3.3; BEATS_PER_CARD = 3; PILE_LEN = 8.6; BLACK_LEN = 1.0; LINE_LEN = 8.4; MIRROR_LEN = 15.2
def _build():
    beats = []; t = 0.5
    # slow part: steady, tightening a little
    while len(beats) < 4 or True:
        beats.append(t)
        p = 0.95 if t < T_CARDS0 else lerp(0.95, 0.80, clamp01((t - T_CARDS0) / 10.5))
        t += p
        i0 = next((i for i, b in enumerate(beats) if b >= T_CARDS0), None)
        if i0 is not None and len(beats) > i0 + BEATS_PER_CARD * len(SLOW): break
    i0 = next(i for i, b in enumerate(beats) if b >= T_CARDS0)
    card_t = [beats[i0 + BEATS_PER_CARD * k] for k in range(len(SLOW))]
    pile0 = beats[i0 + BEATS_PER_CARD * len(SLOW)]
    beats = beats[:i0 + BEATS_PER_CARD * len(SLOW)]
    t = pile0; black0 = pile0 + PILE_LEN; arr = []
    while t < black0 - 0.12:
        x = (t - pile0) / PILE_LEN
        p = 0.80 * (0.29 / 0.80) ** (x ** 1.25)
        beats.append(t); arr.append(t)
        if x > 0.80: arr += [t + p / 3, t + 2 * p / 3]
        elif x > 0.45: arr.append(t + p / 2)
        t += p
    arr = [a for a in arr if a < black0 - 0.05]
    line0 = black0 + BLACK_LEN; mirror0 = line0 + LINE_LEN; end = mirror0 + MIRROR_LEN
    t = line0 + 0.25
    while t < end - 1.0: beats.append(t); t += 1.08
    return beats, card_t, pile0, arr, black0, line0, mirror0, end
BEATS, CARD_T, T_PILE0, ARRIVALS, T_BLACK0, T_LINE0, T_MIRROR0, TOTAL = _build()
NB = np.array(BEATS)
# mirror-shot local times
M_FADEIN = 1.6; M_TR0 = 2.3; M_TR1 = 9.3; M_TEXT = 9.9; M_BRAND = 11.9; M_FADEOUT = 14.1

def beat_pulse(t, tau=0.13):
    b = NB[NB <= t]
    return float(math.exp(-(t - b[-1]) / tau)) if len(b) else 0.0

# ------------------------------------------------------------------ canvas
class Cv:
    def __init__(s, bg=BG):
        s.im = Image.new('RGB', (W * SS, H * SS), bg); s.d = ImageDraw.Draw(s.im); s.bg = bg
    def text(s, xy, t, kind, size, col, anchor='ma', a=1.0, bg=None):
        if a <= 0.003: return
        s.d.text((xy[0] * SS, xy[1] * SS), t, font=font(kind, size), fill=mix(col, bg or s.bg, clamp01(a)), anchor=anchor)
    def lines(s, x, y, ls, kind, size, col, a=1.0, lh=1.3, anchor='ma'):
        for i, l in enumerate(ls): s.text((x, y + i * size * lh), l, kind, size, col, anchor, a)
        return y + len(ls) * size * lh
    def para(s, x, y, t, kind, size, col, maxw, a=1.0, lh=1.3, anchor='ma'):
        return s.lines(x, y, wrap(t, font(kind, size), maxw), kind, size, col, a, lh, anchor)
    def rect(s, b, fill): s.d.rectangle([v * SS for v in b], fill=fill)
    def out(s): return s.im.reduce(SS)

def fit(txt, kind, size, maxw, lo=40):
    while size > lo and font(kind, size).getlength(txt) / SS > maxw: size -= 4
    return size

# ------------------------------------------------------------------ the heartbeat trace along the bottom
ECG_Y = 1668 if PORT else 950; ECG_AMP = 62 if PORT else 46; ECG_WIN = 3.4 if PORT else 5.0
def ecg(cv, t, a=1.0, col=AMBER):
    if a <= 0.01: return
    head = 0.84 * W
    xs = np.arange(0, head + 1, 2.0)
    ts = t - (head - xs) / W * ECG_WIN
    near = NB[(NB > t - ECG_WIN - 0.5) & (NB < t + 0.5)]
    y = np.zeros_like(xs)
    for b in near:
        d = ts - b
        y += (1.0 * np.exp(-(d / 0.013) ** 2) - 0.22 * np.exp(-((d + 0.035) / 0.012) ** 2) - 0.34 * np.exp(-((d - 0.035) / 0.014) ** 2)
              + 0.20 * np.exp(-((d - 0.21) / 0.05) ** 2) + 0.09 * np.exp(-((d + 0.13) / 0.03) ** 2))
    pts = [(float(x) * SS, (ECG_Y - float(v) * ECG_AMP) * SS) for x, v in zip(xs, y)]
    n = len(pts); seg = 6
    for k in range(0, n - 1, seg):
        f = (k / n) ** 1.6
        cv.d.line(pts[k:k + seg + 1], fill=mix(col, cv.bg, a * (0.08 + 0.62 * f)), width=int(3 * SS), joint='curve')
    hx, hy = pts[-1]; r = (5 + 3 * beat_pulse(t)) * SS
    cv.d.ellipse([hx - r, hy - r, hx + r, hy + r], fill=mix(col, cv.bg, a))

def chrome(cv, t, a, legend=0.0):
    """label at the top, honesty line at the bottom (cards and pile)"""
    y = 118 if PORT else 52
    cv.text((W / 2, y), LABEL, 'sansb', 30 if PORT else 28, AMBER, 'ma', 0.9 * a)
    tw = font('sansb', 30 if PORT else 28).getlength(LABEL) / SS
    cv.rect((W / 2 - tw / 2, y + 50, W / 2 + tw / 2, y + 52), mix(AMBER, cv.bg, 0.5 * a))
    fy = 1766 if PORT else 1012
    if PORT:
        ls = wrap(FOOT, font('sans', 27), W - 150)
        cv.lines(W / 2, fy, ls, 'sans', 27, DIM, 0.85 * a * (1 - legend), 1.3)
        ls = wrap(LEGEND, font('sans', 27), W - 150)
        cv.lines(W / 2, fy, ls, 'sans', 27, DIM, 0.95 * a * legend, 1.3)
    else:
        cv.text((W / 2, fy), FOOT, 'sans', 26, DIM, 'ma', 0.85 * a * (1 - legend))
        cv.text((W / 2, fy), LEGEND, 'sans', 26, DIM, 'ma', 0.95 * a * legend)

# ------------------------------------------------------------------ scenes
def scene_open(cv, t):
    a = ease((t - 0.25) / 0.9) * (1 - ease((t - (T_CARDS0 - 0.55)) / 0.5))
    size = 66 if PORT else 70
    ls = wrap(OPENER, font('serifr', size), W - (170 if PORT else 520))
    y = (H * 0.40 if PORT else H * 0.36) - len(ls) * size * 0.66
    cv.lines(W / 2, y, ls, 'serifr', size, TXT, a, 1.36)
    ecg(cv, t, ease(t / 0.8))

def draw_card(cv, q, a, pulse):
    col = KCOL[q['kind']]
    if PORT:
        cv.text((W / 2, 400), q['name'], 'serif', 72, TXT, 'ma', a)
        cv.text((W / 2, 496), q['role'], 'sans', 36, DIM, 'ma', a)
        ns = fit(q['big'], 'serif', 330, W - 110); ns2 = ns * (1 + 0.035 * pulse)
        cv.text((W / 2, 800), q['big'], 'serif', ns2, col, 'mm', a)
        y = 800 + ns * 0.62 + 50
        if q['words']: y = cv.para(W / 2, y, '\u201c' + q['words'] + '\u201d', 'serifi', 50, TXT, W - 170, a, 1.34)
        if q['about']: y = cv.para(W / 2, y, q['about'], 'serifr', 50, TXT, W - 170, a, 1.34)
        cv.para(W / 2, 1440, q['src'], 'sans', 30, DIM, W - 200, a, 1.3)
    else:
        cv.text((W / 2, 150), q['name'], 'serif', 66, TXT, 'ma', a)
        cv.text((W / 2, 236), q['role'], 'sans', 32, DIM, 'ma', a)
        ns = fit(q['big'], 'serif', 300, W - 500); ns2 = ns * (1 + 0.035 * pulse)
        cv.text((W / 2, 470), q['big'], 'serif', ns2, col, 'mm', a)
        y = 470 + ns * 0.60 + 26
        if q['words']: y = cv.para(W / 2, y, '\u201c' + q['words'] + '\u201d', 'serifi', 44, TXT, W - 520, a, 1.32)
        if q['about']: y = cv.para(W / 2, y, q['about'], 'serifr', 44, TXT, W - 520, a, 1.32)
        cv.text((W / 2, 838), q['src'], 'sans', 28, DIM, 'ma', a)

def scene_cards(cv, t):
    k = max(i for i, c in enumerate(CARD_T) if t >= c)
    t0 = CARD_T[k]; t1 = CARD_T[k + 1] if k + 1 < len(CARD_T) else T_PILE0
    a = ease((t - t0) / 0.22) * (1 - ease((t - (t1 - 0.16)) / 0.16))
    draw_card(cv, SLOW[k], a, beat_pulse(t))
    chrome(cv, t, ease((t - CARD_T[0]) / 0.6)); ecg(cv, t)

def _pile_layout():
    """where every flying number lands; fixed seed so both versions and every frame agree"""
    rnd = random.Random(11); items = []
    order = list(range(len(FAST)))
    seq = order + [rnd.randrange(len(FAST)) for _ in range(len(ARRIVALS))]
    x0, x1 = (90, W - 90) if PORT else (150, W - 150)
    y0, y1 = (250, 1540) if PORT else (150, 850)
    cols = 2 if PORT else 3; rows = 5 if PORT else 3
    cells = [(c, r) for r in range(rows) for c in range(cols)]; rnd.shuffle(cells); ci = 0
    for i, ta in enumerate(ARRIVALS):
        q = FAST[seq[i]]; x = (ta - T_PILE0) / PILE_LEN
        echo = i >= len(FAST)
        size = rnd.uniform(118, 215) if not echo else rnd.uniform(90, 300)
        if not PORT: size *= 0.86
        maxw = (W - 120) if PORT else (W * 0.50)
        size = fit(q['big'], 'serif', size, maxw, 44)
        c, r = cells[ci % len(cells)]; ci += 1
        if ci % len(cells) == 0: rnd.shuffle(cells)
        cx = x0 + (x1 - x0) * ((c + 0.5) / cols) + rnd.uniform(-70, 70)
        cy = y0 + (y1 - y0) * ((r + 0.5) / rows) + rnd.uniform(-60, 60)
        early = [(540, 430), (540, 1180), (540, 800), (540, 1440), (540, 620)] if PORT else [(500, 300), (1420, 300), (960, 560), (430, 690), (1500, 690)]
        if i < len(early):          # the first few land clear of each other so each one can be read; then they start to collide
            cx, cy = early[i]; size = fit(q['big'], 'serif', (200 - 12 * i) * (1.0 if PORT else 0.8), maxw, 44)
        hw = font('serif', size).getlength(q['big']) / SS / 2
        cx = min(max(cx, 40 + hw), W - 40 - hw)
        items.append(dict(q=q, t=ta, size=size, x=cx, y=cy, echo=echo))
    return items
PILE = _pile_layout()

def scene_pile(cv, t):
    x = (t - T_PILE0) / PILE_LEN
    surge = ease((x - 0.80) / 0.2)                       # last stretch: everything flares back up
    pulse = beat_pulse(t, 0.10)
    sh = surge * 7 * pulse
    ox = math.sin(t * 61.0) * sh; oy = math.cos(t * 47.0) * sh
    live = [it for it in PILE if it['t'] <= t]
    for it in live:
        age = t - it['t']; q = it['q']; col = KCOL[q['kind']]
        a = min(1.0, age / 0.09) * (0.17 + 0.83 * math.exp(-age / (1.25 - 0.7 * x)))
        a = max(a, surge * (0.55 + 0.35 * pulse)) if age > 0.09 else a
        s = it['size'] * (1.0 + 0.10 * math.exp(-age / 0.10) + 0.03 * age / 3)
        cx, cy = it['x'] + ox, it['y'] + oy
        cv.text((cx, cy), q['big'], 'serif', s, col, 'mm', a)
        if not it['echo'] or it['size'] > 150:
            ns = max(24, min(38, it['size'] * 0.2)); yy = cy + s * 0.60
            a2 = a * (1.0 if age < 1.2 else 0.6)
            cv.text((cx, yy), q['name'], 'sansb', ns, TXT, 'ma', a2)
            cv.text((cx, yy + ns * 1.34), q['about'], 'sans', max(20, ns * 0.72), TXT, 'ma', a2 * 0.85)
            cv.text((cx, yy + ns * 1.34 + max(20, ns * 0.72) * 1.36), q['src'], 'sans', max(18, ns * 0.62), DIM, 'ma', a2 * 0.9)
    chrome(cv, t, 1.0, legend=ease((t - T_PILE0 - 0.3) / 0.6)); ecg(cv, t)

def scene_line(cv, t):
    lt = t - T_LINE0
    out = 1 - ease((lt - (LINE_LEN - 0.75)) / 0.7)
    size = 68 if PORT else 66; lh = 1.38
    groups = [(g[0] if PORT else g[1], g[2]) for g in LINE]
    nlines = sum(len(g[0]) for g in groups); gap = 20
    y = H * (0.44 if PORT else 0.46) - (nlines * size * lh + gap * (len(groups) - 1)) / 2
    cues = [0.35, 2.0, 3.6, 5.6]
    for (ls, col), c in zip(groups, cues):
        a = ease((lt - c) / 1.1) * out
        y = cv.lines(W / 2, y, ls, 'serifr', size, col, a, lh) + gap

# ------------------------------------------------------------------ the mirror shot (blend of the Blender passes)
_P = {}
def passes():
    if not _P:
        d = os.path.join(HERE, 'passes')
        Hm = np.load(os.path.join(d, f'{ORI}_H.npy')).astype(np.float32)
        A = np.load(os.path.join(d, f'{ORI}_A.npy')).astype(np.float32)
        E = np.load(os.path.join(d, f'{ORI}_E.npy')).astype(np.float32)
        M = np.load(os.path.join(d, f'{ORI}_M.npy')).astype(np.float32)
        cov = np.clip(M[..., 1], 0, 1); tm = np.where(cov > 0.02, M[..., 0] / np.maximum(M[..., 1], 1e-4), 1.0)
        A = A * (1 - (1 - AI_DARK) * cov[..., None])            # keep the metal dark so the gold lines read as gold
        _P.update(H=Hm, D=A - Hm, E=np.clip(E, 0, 60) * E_GAIN, cov=cov[..., None], tm=np.clip(tm, 0, 1)[..., None])
        hh, ww = Hm.shape[:2]
        yy, xx = np.mgrid[0:hh, 0:ww].astype(np.float32)
        fx, fy = (0.56, 0.42) if PORT else (0.61, 0.42)
        r = np.sqrt(((xx / ww - fx) * (ww / hh if not PORT else 1.0)) ** 2 + ((yy / hh - fy) * (1.0 if not PORT else hh / ww)) ** 2)
        _P['vig'] = (1.0 - 0.55 * np.clip((r - 0.25) / 0.75, 0, 1) ** 1.5)[..., None].astype(np.float32)
    return _P
def sstep(x, a, b):
    u = np.clip((x - a) / (b - a), 0, 1); return u * u * (3 - 2 * u)
EXPO = float(os.environ.get('EXPO', 1.1)); AI_DARK = float(os.environ.get('AI_DARK', 0.5)); E_GAIN = float(os.environ.get('E_GAIN', 0.4))
def tonemap(x):
    x = np.maximum(x * EXPO, 0)
    y = (x * (2.51 * x + 0.03)) / (x * (2.43 * x + 0.59) + 0.14)
    return np.clip(y, 0, 1) ** (1 / 2.2)
GOLD_L = np.array([1.0, 0.58, 0.15], np.float32)

def mirror_frame(lt, seed):
    P = passes()
    u = clamp01((lt - M_TR0) / (M_TR1 - M_TR0)); u = u * u * (3 - 2 * u) * 0.55 + u * 0.45
    f_line = -0.18 + u * 1.70; f_surf = -0.50 + u * 1.72
    tm = P['tm']; cov = P['cov']
    m = cov * sstep(f_surf - tm, 0.0, 0.10) + (1 - cov) * float(ease((u - 0.3) / 0.6))
    el = cov * sstep(f_line - tm, 0.0, 0.10) + (1 - cov) * float(ease((u - 0.12) / 0.7))
    pulse = beat_pulse(T_MIRROR0 + lt, 0.30)
    glow = 0.80 + 0.45 * pulse * u
    lead = 1.0 + 1.6 * np.exp(-((tm - f_line) / 0.07) ** 2) * cov * (1.0 - u * 0.6)
    lin = P['H'] + m * P['D'] + P['E'] * (el * lead * glow)
    band = np.exp(-((tm - f_surf) / 0.03) ** 2) * cov * (1.0 if 0.02 < u < 0.99 else 0.0)
    lin = lin + band * GOLD_L * 0.55
    img = tonemap(lin * P['vig'])
    # soft bloom from the glow
    gl = np.clip(P['E'] * (el * glow) * 0.5, 0, 1)
    g8 = Image.fromarray((gl * 255).astype(np.uint8)).resize((img.shape[1] // 4, img.shape[0] // 4), Image.BILINEAR).filter(ImageFilter.GaussianBlur(9))
    bloom = np.asarray(g8.resize((img.shape[1], img.shape[0]), Image.BILINEAR), np.float32) / 255
    img = 1 - (1 - img) * (1 - 0.55 * bloom)
    im = Image.fromarray((np.clip(img, 0, 1) * 255 + 0.5).astype(np.uint8))
    # slow push in toward the reflection
    z = lerp(1.0, 1.115, ease(lt / MIRROR_LEN) * 0.6 + 0.4 * lt / MIRROR_LEN)
    sw, sh = im.size; cw, ch = sw / z, sh / z
    fx, fy = (0.56, 0.44) if PORT else (0.60, 0.46)
    cx = lerp(sw / 2, sw * fx, (z - 1) / 0.115 * 0.9); cy = lerp(sh / 2, sh * fy, (z - 1) / 0.115 * 0.9)
    x0 = min(max(cx - cw / 2, 0), sw - cw); y0 = min(max(cy - ch / 2, 0), sh - ch)
    im = im.resize((W, H), Image.LANCZOS, box=(x0, y0, x0 + cw, y0 + ch))
    a = np.asarray(im, np.float32)
    rs = np.random.RandomState(seed)
    a += rs.normal(0, 2.6, (H, W, 1)).astype(np.float32) + rs.normal(0, 0.8, (H, W, 3)).astype(np.float32)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))

def scene_mirror(t, n):
    lt = t - T_MIRROR0
    im = mirror_frame(lt, n)
    ta = ease((lt - M_TEXT) / 1.3); ba = ease((lt - M_BRAND) / 1.2)
    if ta > 0 or ba > 0:
        ov = Image.new('RGBA', (W * SS, H * SS), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
        if PORT:
            size = 74; cx = W / 2; y = 1395; anchor = 'ma'
            # darken under the words
            sh = Image.new('L', (W, H), 0); ImageDraw.Draw(sh).rectangle([0, 1250, W, H], fill=int(175 * max(ta, ba)))
            sh = sh.filter(ImageFilter.GaussianBlur(110))
            im = Image.composite(Image.new('RGB', (W, H), (5, 8, 14)), im, sh)
        else:
            size = 58; cx = 84; y = 385; anchor = 'la'
        close = CLOSE if PORT else CLOSE_WIDE
        for i, l in enumerate(close):
            d.text((cx * SS, (y + i * size * 1.3) * SS), l, font=font('serif', size), fill=TXT + (int(255 * ta),), anchor=anchor)
        yb = y + len(close) * size * 1.3 + (44 if PORT else 40)
        if ba > 0:
            if PORT: d.rectangle([(W / 2 - 46) * SS, (yb - 6) * SS, (W / 2 + 46) * SS, (yb - 4) * SS], fill=AMBER + (int(200 * ba),))
            else: d.rectangle([cx * SS, (yb - 6) * SS, (cx + 92) * SS, (yb - 4) * SS], fill=AMBER + (int(200 * ba),))
            d.text((cx * SS, (yb + 22) * SS), BRAND, font=font('sansb', 36), fill=AMBER + (int(235 * ba),), anchor=anchor)
        im = Image.alpha_composite(im.convert('RGBA'), ov.reduce(SS)).convert('RGB')
    fa = min(ease(lt / M_FADEIN), 1 - ease((lt - M_FADEOUT) / (MIRROR_LEN - M_FADEOUT - 0.15)))
    if fa < 0.999: im = Image.blend(Image.new('RGB', (W, H), (0, 0, 0)), im, max(0.0, fa))
    return im

def frame(n):
    t = n / FPS
    if t >= T_MIRROR0: return scene_mirror(t, n)
    if t >= T_BLACK0:
        cv = Cv((0, 0, 0))
        if t >= T_LINE0: scene_line(cv, t)
        return cv.out()
    cv = Cv()
    if t < CARD_T[0]: scene_open(cv, t)
    elif t < T_PILE0: scene_cards(cv, t)
    else: scene_pile(cv, t)
    im = cv.out()
    if t >= T_PILE0:      # pressure: the frame warms and tightens as the numbers pile up
        x = (t - T_PILE0) / PILE_LEN
        k = ease((x - 0.55) / 0.45) * (0.5 + 0.5 * beat_pulse(t, 0.10))
        if k > 0.01: im = Image.blend(im, Image.new('RGB', im.size, (60, 34, 10)), 0.16 * k)
    return im
def work(n): return frame(n).tobytes()

# ------------------------------------------------------------------ audio (all synthesized)
SR = 48000
def synth_audio(path):
    N = int((TOTAL + 0.3) * SR); L = np.zeros(N); R = np.zeros(N); rs = np.random.RandomState(7)
    def add(buf_l, buf_r, t0, sig, pan=0.0):
        i = int(t0 * SR); n = min(len(sig), N - i)
        if n <= 0 or i < 0: return
        buf_l[i:i + n] += sig[:n] * (1 - max(0, pan)); buf_r[i:i + n] += sig[:n] * (1 + min(0, pan))
    def thump(f0, f1, dur, amp):
        t = np.arange(int(dur * SR)) / SR
        f = f1 + (f0 - f1) * np.exp(-t / (dur * 0.22)); ph = 2 * np.pi * np.cumsum(f) / SR
        env = np.exp(-t / (dur * 0.26)) * np.minimum(1, t / 0.004)
        body = np.tanh(2.6 * np.sin(ph)) * 0.8 + 0.45 * np.sin(2 * ph) + 0.26 * np.sin(3 * ph) + 0.16 * np.sin(4.02 * ph) + 0.12 * np.sin(5 * ph) + 0.08 * np.sin(6.03 * ph)
        nz = rs.normal(0, 1, len(t)); k = int(SR / 900); nz = np.convolve(nz, np.ones(k) / k, 'same') * np.exp(-t / 0.012) * 0.9
        fk = 230 + 190 * np.exp(-t / 0.02) * (f0 / 74)          # a mid knock so the beat survives phone speakers
        knock = np.sin(2 * np.pi * np.cumsum(fk) / SR) * np.exp(-t / 0.035) * 1.5
        n2 = rs.normal(0, 1, len(t)); k2 = int(SR / 2600); n2 = np.convolve(n2, np.ones(k2) / k2, 'same') * np.exp(-t / 0.02) * 1.6
        return (body + nz) * env * amp + (knock + n2) * np.minimum(1, t / 0.003) * amp
    for b in BEATS:
        if b < T_BLACK0:
            x = clamp01((b - T_PILE0) / PILE_LEN); g = 0.50 + 0.50 * x if b >= T_PILE0 else 0.42 + 0.08 * clamp01(b / T_PILE0)
            per = 0.80 * (0.29 / 0.80) ** (x ** 1.25) if b >= T_PILE0 else 0.9
            pitch = 1.0 + 0.22 * x
        else:
            lt = b - T_LINE0; g = 0.34 + 0.10 * clamp01((b - T_MIRROR0) / 6.0); per = 1.08; pitch = 0.94
            g *= 1 - 0.7 * clamp01((b - (TOTAL - 3.0)) / 3.0)
        s1 = thump(74 * pitch, 44 * pitch, 0.26, g); s2 = thump(92 * pitch, 56 * pitch, 0.20, g * 0.62)
        add(L, R, b, s1); add(L, R, b + min(0.30, per * 0.36), s2)
    # ticks: one per arriving number
    for i, a in enumerate(ARRIVALS):
        t = np.arange(int(0.03 * SR)) / SR; x = (a - T_PILE0) / PILE_LEN
        nz = rs.normal(0, 1, len(t)); nz = nz - np.convolve(nz, np.ones(12) / 12, 'same')
        tick = (nz * 0.5 + np.sin(2 * np.pi * (1500 + 900 * rs.rand()) * t)) * np.exp(-t / 0.006) * (0.035 + 0.05 * x)
        add(L, R, a, tick, pan=rs.uniform(-0.6, 0.6))
    t = np.arange(N) / SR
    # riser under the pile: low cluster + breath of noise, cut dead at the blackout
    x = np.clip((t - T_PILE0) / PILE_LEN, 0, 1); on = (t >= T_PILE0) & (t < T_BLACK0)
    f = 55 * 2 ** (x * 1.0); ph = 2 * np.pi * np.cumsum(f) / SR
    ris = (np.sin(ph) + 0.6 * np.sin(1.498 * ph + 0.3) + 0.35 * np.sin(2.01 * ph) + 0.2 * np.tanh(3 * np.sin(3.0 * ph))) * (x ** 2.2) * 0.20
    nz = rs.normal(0, 1, N); k = 40; nz = np.convolve(nz, np.ones(k) / k, 'same') * 6
    ris += nz * (x ** 3) * 0.05
    cut = np.clip((T_BLACK0 - t) / 0.03, 0, 1)
    ris = ris * on * cut
    L += ris; R += ris
    # pad: enters under the line, opens up in the mirror shot, resolves on the closing words
    def pad(freqs, t0, t1, att, rel, amp):
        seg = np.zeros(N); env = np.clip((t - t0) / att, 0, 1) * np.clip((t1 - t) / rel, 0, 1); env = env * env * (3 - 2 * env)
        outl = np.zeros(N); outr = np.zeros(N)
        for j, fq in enumerate(freqs):
            for det, pan in ((-0.0035, -0.5), (0.0031, 0.5), (0.0, 0.0)):
                ph = 2 * np.pi * fq * (1 + det) * t + j * 1.3 + pan
                v = (np.sin(ph) + 0.28 * np.sin(2 * ph) + 0.10 * np.sin(3 * ph)) * (0.8 + 0.2 * np.sin(2 * np.pi * (0.11 + 0.03 * j) * t + j))
                outl += v * (1 - max(0, pan)); outr += v * (1 + min(0, pan))
        k = amp / (len(freqs) * 3)
        return outl * env * k, outr * env * k
    A2, C3, E3, G3, A3, B3, C4, E4, G4, C5 = 110.0, 130.81, 164.81, 196.0, 220.0, 246.94, 261.63, 329.63, 392.0, 523.25
    tx = T_MIRROR0 + M_TEXT
    for fr, t0, t1, att, rel, amp in (([A2, E3], T_LINE0 + 1.0, T_MIRROR0 + 3.0, 5.0, 4.0, 0.30),
                                      ([A2, E3, A3, B3, C4, E4], T_MIRROR0 + 1.0, tx + 0.8, 5.5, 2.4, 0.62),
                                      ([C3, G3, C4, E4, G4, C5], tx - 0.9, TOTAL + 0.2, 2.6, 3.4, 0.66)):
        pl, pr = pad(fr, t0, t1, att, rel, amp); L += pl; R += pr
    # faint glints while the reflection changes
    for i in range(46):
        tt = T_MIRROR0 + M_TR0 + 0.4 + rs.rand() ** 0.8 * (M_TR1 - M_TR0 - 0.4)
        n = int(0.9 * SR); tl = np.arange(n) / SR; fq = rs.choice([1318.5, 1568.0, 1760.0, 1975.5, 2093.0, 2637.0])
        g = np.sin(2 * np.pi * fq * tl) * np.exp(-tl / 0.22) * np.minimum(1, tl / 0.01) * 0.012
        add(L, R, tt, g, pan=rs.uniform(-0.8, 0.8))
    room = rs.normal(0, 1, N); room = np.convolve(room, np.ones(60) / 60, 'same') * 0.004
    L += room; R += room
    st = np.stack([L, R], 1); st = np.tanh(st * 1.15) ; st *= 0.84 / np.abs(st).max()
    fade = np.clip((TOTAL + 0.25 - t) / 1.2, 0, 1)[:, None]; st *= fade
    with wave.open(path, 'wb') as wf:
        wf.setnchannels(2); wf.setsampwidth(2); wf.setframerate(SR); wf.writeframes((st * 32767).astype('<i2').tobytes())
    print('audio', path, round(TOTAL, 2), 's')

# ------------------------------------------------------------------ main
def main():
    cmd = sys.argv[2] if len(sys.argv) > 2 else 'info'
    if cmd == 'info':
        print('TOTAL', round(TOTAL, 2), 'cards', [round(c, 2) for c in CARD_T], 'pile', round(T_PILE0, 2), 'arrivals', len(ARRIVALS),
              'black', round(T_BLACK0, 2), 'line', round(T_LINE0, 2), 'mirror', round(T_MIRROR0, 2)); return
    if cmd == 'audio': synth_audio(os.path.join(HERE, 'audio.wav')); return
    if cmd == 'still':
        frame(int(float(sys.argv[3]) * FPS)).save(sys.argv[4]); return
    if cmd == 'sheet':
        times = [float(x) for x in sys.argv[3].split(',')]
        ims = [frame(int(t * FPS)).resize((540, 960), Image.LANCZOS) for t in times]
        sheet = Image.new('RGB', (540 * 3 + 40, 960 * 2 + 30), (5, 8, 14))
        for i, im in enumerate(ims): sheet.paste(im, (10 + (i % 3) * 550, 10 + (i // 3) * 970))
        sheet.save(sys.argv[4]); return
    if cmd == 'render':
        out = sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else os.path.join(ROOT, f'mirror-post-{"vertical" if PORT else "wide"}.mp4')
        wav = os.path.join(HERE, 'audio.wav')
        a, b = 0, int(TOTAL * FPS)
        if '--secs' in sys.argv:
            i = sys.argv.index('--secs'); a, b = int(float(sys.argv[i + 1]) * FPS), int(float(sys.argv[i + 2]) * FPS)
        cmdl = ['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-']
        if '--secs' not in sys.argv: cmdl += ['-i', wav, '-c:a', 'aac', '-b:a', '192k', '-shortest']
        cmdl += ['-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out]
        ff = subprocess.Popen(cmdl, stdin=subprocess.PIPE)
        with Pool(int(os.environ.get('NPROC', 10))) as pool:
            for k, buf in enumerate(pool.imap(work, range(a, b), chunksize=2)):
                ff.stdin.write(buf)
                if k % 150 == 0: print(k, '/', b - a, flush=True)
        ff.stdin.close(); ff.wait(); print('wrote', out)

if __name__ == '__main__': main()
