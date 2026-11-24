# Pillow boards for Science 8.10 Antarctica Part 2: the sky in the ice (cream-paper look, same family as ep6-ep9).  python diagram.py [FRAMES_DIR] [--force] [--only=name] [--preview]
import math, os, sys, random
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shots import SHOTS, FPS
OUT = next((a for a in sys.argv[1:] if not a.startswith("--")), "C:/Users/lilli/Renders/antarctica-p2/frames")
W, H, SS = 1280, 720, 2
CREAM = (243, 237, 224); INK = (46, 40, 34); DIM = (120, 110, 96); RULE = (200, 190, 172); PAPER = (236, 226, 206)
AMBER = (196, 120, 28); RED = (178, 70, 52); BLUE = (62, 110, 170); MARS = (196, 110, 62); MARSD = (150, 78, 44)
MOON = (118, 110, 100); MOOND = (80, 74, 68); CAP = (240, 240, 236)
FD = "C:/Windows/Fonts/"
_f = {}
def font(kind, size):
    k = (kind, size)
    if k not in _f: _f[k] = ImageFont.truetype(FD + {"serif": "georgiab.ttf", "serifr": "georgia.ttf", "sans": "segoeui.ttf", "sansb": "segoeuib.ttf", "sansl": "segoeuil.ttf"}[kind], size * SS)
    return _f[k]
def ease(x): x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)
def mix(a, b, u): return tuple(int(a[i] + (b[i] - a[i]) * u) for i in range(3))

class Cv:
    def __init__(s):
        s.im = Image.new("RGB", (W * SS, H * SS), CREAM); s.d = ImageDraw.Draw(s.im)
    def P(s, p): return (p[0] * SS, p[1] * SS)
    def poly(s, pts, fill, outline=None, w=2): s.d.polygon([s.P(p) for p in pts], fill=fill, outline=outline, width=w * SS if outline else 0)
    def line(s, pts, col, w=2): s.d.line([s.P(p) for p in pts], fill=col, width=w * SS, joint="curve")
    def dashed(s, pts, col, w=2, dash=8, gap=6):
        for a, b in zip(pts, pts[1:]):
            L_ = math.hypot(b[0] - a[0], b[1] - a[1]); n = max(1, int(L_ / (dash + gap)))
            if L_ < 1e-6: continue
            for i in range(n):
                u0 = i * (dash + gap) / L_; u1 = min(1, (i * (dash + gap) + dash) / L_)
                s.line([(a[0] + (b[0] - a[0]) * u0, a[1] + (b[1] - a[1]) * u0), (a[0] + (b[0] - a[0]) * u1, a[1] + (b[1] - a[1]) * u1)], col, w)
    def rect(s, b, fill, outline=None, w=2, r=0):
        bb = [b[0] * SS, b[1] * SS, b[2] * SS, b[3] * SS]
        s.d.rounded_rectangle(bb, radius=r * SS, fill=fill, outline=outline, width=w * SS if outline else 0)
    def circ(s, c, r, fill, outline=None, w=2): s.d.ellipse([(c[0] - r) * SS, (c[1] - r) * SS, (c[0] + r) * SS, (c[1] + r) * SS], fill=fill, outline=outline, width=w * SS if outline else 0)
    def ring(s, c, r, col, w=2): s.circ(c, r, None, col, w)
    def arc(s, c, r, a0, a1, col, w=2): s.d.arc([(c[0] - r) * SS, (c[1] - r) * SS, (c[0] + r) * SS, (c[1] + r) * SS], a0, a1, fill=col, width=w * SS)
    def text(s, xy, t, kind, size, col, anchor="la", a=1.0): s.d.text(s.P(xy), t, font=font(kind, size), fill=mix(CREAM, col, a), anchor=anchor)
    def para(s, x, y, t, kind, size, col, maxw, lh=1.3, anchor="l", a=1.0):
        f = font(kind, size); words = t.split(); lines = []; cur = ""
        for w_ in words:
            tt = (cur + " " + w_).strip()
            if f.getlength(tt) <= maxw * SS or not cur: cur = tt
            else: lines.append(cur); cur = w_
        if cur: lines.append(cur)
        for i, l in enumerate(lines): s.d.text(s.P((x, y + i * size * lh)), l, font=f, fill=mix(CREAM, col, a), anchor="ma" if anchor == "m" else "la")
        return y + len(lines) * size * lh
    def tag(s, cx, cy, t, a=1.0, wdt=150, col=AMBER):
        s.rect((cx - wdt / 2, cy - 15, cx + wdt / 2, cy + 15), mix(CREAM, (236, 220, 190), a), outline=mix(CREAM, col, a), w=2, r=8)
        s.text((cx, cy - 10), t, "sansb", 16, col, "ma", a)
    def arrow(s, a_, b_, col, w=3, head=9):
        s.line([a_, b_], col, w)
        ang = math.atan2(b_[1] - a_[1], b_[0] - a_[0])
        s.poly([b_, (b_[0] - head * math.cos(ang - .5), b_[1] - head * math.sin(ang - .5)), (b_[0] - head * math.cos(ang + .5), b_[1] - head * math.sin(ang + .5))], col)
    def potato(s, c, r, col, outline, rot=0.0, a=1.0, seed=3, w=2):
        rs = random.Random(seed); pts = []
        for i in range(40):
            t = 2 * math.pi * i / 40
            rr = r * (1 + .08 * math.sin(3 * t + seed) + .05 * math.cos(5 * t + 1.3 * seed))
            pts.append((c[0] + rr * 1.18 * math.cos(t + rot), c[1] + rr * .9 * math.sin(t + rot)))
        s.poly(pts, mix(CREAM, col, a), mix(CREAM, outline, a), w)
    def header(s, title, sub, a):
        s.text((W / 2, 30), title, "serif", 40, INK, "ma", a)
        s.text((W / 2, 84), sub, "sans", 19, DIM, "ma", a)
        s.line([(W / 2 - 70, 116), (W / 2 + 70, 116)], mix(CREAM, AMBER, a), 3)




# ======================================================================== ep10 boards (Science 8.10, Antarctica Part 2: the sky in the ice)
# Layout rule (same as ep6-ep9): nothing below y = 640; finish.py shrinks each board into the top of the frame and puts the
# captions in a dark band under it.  No em or en dashes anywhere on screen.  Reveal times are seconds from the board's start,
# placed on the narration's word timings (audio/words_*.json).
COOL = (62, 110, 170); GREEN = (40, 120, 60); STEEL = (150, 150, 156); ICE = (214, 228, 238); ICED = (150, 178, 200); SNOW = (248, 248, 244)
def fade(t, dur, a_in=.6, a_out=1.0): return max(0.0, min(1.0, t / a_in, (dur - t) / a_out))
def ap(t, t0, d=.7): return ease((t - t0) / d)
def src_line(cv, y, text, a): cv.text((W / 2, y), text, "sansl", 13, DIM, "ma", a)
def panel(cv, b, u): cv.rect(b, mix(CREAM, PAPER, u), mix(CREAM, RULE, u), 2, 10)
def pill(cv, cx, cy, t, u, col=RED, wdt=None):
    wdt = wdt or (font("sansb", 15).getlength(t) / SS + 30)
    cv.rect((cx - wdt / 2, cy - 15, cx + wdt / 2, cy + 15), mix(CREAM, (246, 228, 214), u), outline=mix(CREAM, col, u), w=2, r=14)
    cv.text((cx, cy - 10), t, "sansb", 15, col, "ma", u)
def strike(cv, x0, x1, y, u, col=RED):
    if u > 0: cv.line([(x0, y), (x0 + (x1 - x0) * u, y)], col, 3)

def firn_frame(t, dur):
    cv = Cv(); a = fade(t, dur)
    cv.header("How snow turns into sealed air", "A generic column. Real depths vary from site to site.  Drawn, not to scale.", a)
    X0, X1, Y0, MPX = 120, 470, 150, 3.4          # column: depth 0 m at y 150, 3.4 px per meter
    def yd(m): return Y0 + m * MPX
    seal = 82 + 18 * ap(t, 17.6, 1.5)              # the sealing band slides into place as "50 to 120 m" is said
    u0 = a
    # firn body
    cv.rect((X0, yd(0), X1, yd(seal - 10)), mix(CREAM, (234, 238, 240), u0), mix(CREAM, RULE, u0), 2, 0)
    cv.rect((X0, yd(seal - 10), X1, yd(seal)), mix(CREAM, (214, 224, 232), u0), None)
    cv.rect((X0, yd(seal), X1, yd(130)), mix(CREAM, ICE, u0), mix(CREAM, RULE, u0), 2, 0)
    cv.rect((X0, yd(0), X1, yd(3)), mix(CREAM, SNOW, u0), None)
    # snow grains at the top, open channels below (a fixed random pattern)
    rs = random.Random(4)
    u1 = ap(t, 1.4) * a
    for i in range(70):
        cv.circ((rs.uniform(X0 + 6, X1 - 6), rs.uniform(yd(0) + 2, yd(2.6))), rs.uniform(1.5, 3), mix(CREAM, (200, 210, 220), u0))
    u2 = ap(t, 4.3) * a
    for i in range(14):
        x = X0 + 18 + i * (X1 - X0 - 36) / 13; pts = []
        bottom = seal - 10 + (rs.random() * 8)
        for k in range(24):
            m = 3 + (bottom - 3) * k / 23; pts.append((x + 5 * math.sin(k * 1.3 + i), yd(m)))
        cv.line(pts, mix(CREAM, (176, 194, 210), u2), max(1, int(4 - 3 * 0)))
    # air arrows moving down through the open firn
    u3 = ap(t, 9.4) * a
    if u3 > 0:
        for i in range(6):
            x = X0 + 45 + i * 52; ph = ((t - 9.4) * 14 + i * 37) % ((seal - 14) * MPX)
            yy = yd(4) + ph
            cv.arrow((x, yy), (x, yy + 18), mix(CREAM, COOL, u3), 3, 8)
    # bubbles in the sealed ice
    u4 = ap(t, 20.7) * a
    for i in range(60):
        cv.ring((rs.uniform(X0 + 8, X1 - 8), rs.uniform(yd(seal) + 6, yd(129))), rs.uniform(2, 4.5), mix(CREAM, (120, 150, 175), u4), 2)
    # depth ruler
    for m in (0, 25, 50, 75, 100, 125):
        cv.line([(X0 - 12, yd(m)), (X0, yd(m))], mix(CREAM, INK, a), 2); cv.text((X0 - 18, yd(m) - 9), "%d m" % m, "sans", 14, INK, "ra", a)
    cv.text((X0 + 10, yd(0) + 4), "snow", "sansb", 15, INK, "la", u1)
    cv.text((X0 + 10, yd(14)), "FIRN: porous, open channels", "sansb", 16, INK, "la", u2)
    cv.text((X0 + 10, yd(36)), "open to the sky", "sans", 15, COOL, "la", ap(t, 5.4) * a)
    cv.text((X0 + 10, yd(seal) + 10), "ICE: air locked in bubbles", "sansb", 16, INK, "la", u4)
    # right panel
    u5 = ap(t, 17.9) * a
    panel(cv, (520, 150, 1220, 590), u5)
    cv.text((544, 164), "Where the channels pinch shut", "serif", 24, INK, "la", u5)
    cv.para(544, 204, "Usually somewhere between 50 and 120 meters down.", "sans", 19, INK, 640, 1.3, "l", u5)
    pill(cv, 1110, 178, "NOT ONE LINE", ap(t, 26.0) * a, AMBER, 150)
    rows = [(27.1, "West Antarctica (WAIS Divide)", "a lock-in zone about 10 m thick on the way to the final seal"),
            (34.4, "Summit, Greenland", "about 70 m down"),
            (38.7, "South Pole (colder)", "about 120 m down")]
    for i, (t0, k, v) in enumerate(rows):
        uu = ap(t, t0) * a; yy = 280 + i * 92
        cv.circ((556, yy + 12), 7, mix(CREAM, COOL, uu)); cv.text((574, yy), k, "sansb", 19, INK, "la", uu)
        cv.para(574, yy + 30, v, "sans", 17, INK, 620, 1.25, "l", uu)
    src_line(cv, 606, "Sources: Davies, Ice core basics (AntarcticGlaciers.org); Battle et al. 2011 (WAIS Divide); Schwander et al. 1997 (Summit); icedrill.org (South Pole).", a)
    return cv.im.reduce(SS)

def age_frame(t, dur):
    cv = Cv(); a = fade(t, dur)
    cv.header("The air is younger than its ice", "Air keeps moving down through the open firn, so it seals later than the snow around it.", a)
    def row(y, name, sub, gap_txt, gap_px, t0, t1):
        u = ap(t, t0) * a
        panel(cv, (60, y, 1220, y + 170), u)
        cv.text((84, y + 14), name, "serif", 26, INK, "la", u); cv.text((84, y + 52), sub, "sans", 16, DIM, "la", u)
        ub = ap(t, t1) * a
        x0 = 420
        cv.rect((x0, y + 30, x0 + 640, y + 62), mix(CREAM, ICE, u), mix(CREAM, ICED, u), 2, 6); cv.text((x0 + 10, y + 34), "ICE  (when the snow fell)", "sansb", 15, INK, "la", u)
        cv.rect((x0 + gap_px, y + 92, x0 + 640, y + 124), mix(CREAM, (246, 226, 200), ub), mix(CREAM, AMBER, ub), 2, 6)
        cv.text((x0 + gap_px + 10, y + 96), "AIR in its bubbles", "sansb", 15, INK, "la", ub)
        cv.line([(x0, y + 140), (x0 + gap_px, y + 140)], mix(CREAM, RED, ub), 3)
        cv.line([(x0, y + 132), (x0, y + 148)], mix(CREAM, RED, ub), 3); cv.line([(x0 + gap_px, y + 132), (x0 + gap_px, y + 148)], mix(CREAM, RED, ub), 3)
        cv.text((x0 + gap_px + 12, y + 132), gap_txt, "sansb", 17, RED, "la", ub)
    row(140, "Law Dome", "snowy coast of East Antarctica", "gap: about 30 years", 70, 0.0, 4.3)
    row(330, "Dome C", "dry high plateau", "gap: about 2,000 years (bigger in the last ice age)", 300, 7.8, 9.3)
    u = ap(t, 14.1) * a
    pill(cv, W / 2, 530, "WORKED OUT WITH MODELS  ·  DETAILS STILL DEBATED", u, AMBER, 470)
    src_line(cv, 606, "Sources: Etheridge et al. 1996 (Law Dome); Schwander et al. 2001, Loulergue et al. 2007 (Dome C). Bars not to scale.", a)
    return cv.im.reduce(SS)

def hydrate_frame(t, dur):
    cv = Cv(); a = fade(t, dur)
    cv.header("Deeper still: no bubbles at all", "The air moves into the ice crystals themselves.  Drawn, not to scale.", a)
    panel(cv, (60, 140, 420, 590), a)
    cv.text((240, 154), "A bubble shrinks", "serif", 22, INK, "ma", a)
    r = 70 * (1 - .9 * ap(t, 1.4, 4.5)); c = (240, 330)
    cv.rect((90, 200, 390, 470), mix(CREAM, ICE, a), mix(CREAM, ICED, a), 2, 8)
    if r > 4: cv.circ(c, r, mix(CREAM, (246, 250, 252), a), mix(CREAM, (120, 150, 175), a), 3)
    rs = random.Random(9); u_in = ap(t, 2.9, 3.0) * a
    for i in range(26):   # gas molecules leaving the bubble into the crystal
        ang = rs.uniform(0, 2 * math.pi); d0 = rs.uniform(5, 50); d1 = rs.uniform(80, 140)
        d = d0 + (d1 - d0) * u_in
        cv.circ((c[0] + d * math.cos(ang), c[1] + d * .85 * math.sin(ang)), 4, mix(CREAM, COOL, a))
    cv.text((240, 486), "the air goes into the crystals", "sans", 16, INK, "ma", ap(t, 2.9) * a)
    # the cage
    u = ap(t, 6.0) * a
    panel(cv, (440, 140, 820, 590), u)
    cv.text((630, 154), "A cage of water molecules", "serif", 22, INK, "ma", u)
    cx, cy = 630, 340
    pts = [(cx + 110 * math.cos(2 * math.pi * k / 12 + .2), cy + 110 * math.sin(2 * math.pi * k / 12 + .2)) for k in range(12)]
    for i in range(12):
        uu = ap(t, 6.0 + i * .12) * a
        cv.line([pts[i], pts[(i + 1) % 12]], mix(CREAM, ICED, uu), 3)
        cv.circ(pts[i], 13, mix(CREAM, RED, uu)); cv.circ((pts[i][0] + 10, pts[i][1] - 8), 6, mix(CREAM, (240, 240, 240), uu), mix(CREAM, DIM, uu), 1)
    cv.circ((cx - 14, cy), 22, mix(CREAM, COOL, u)); cv.circ((cx + 14, cy), 22, mix(CREAM, COOL, u))
    cv.text((cx, cy + 34), "gas molecule", "sans", 15, INK, "ma", u)
    cv.text((630, 470), "water molecules", "sans", 15, RED, "ma", u)
    cv.text((630, 510), "AIR HYDRATE", "sansb", 22, AMBER, "ma", ap(t, 10.9) * a)
    # Dome Fuji ruler
    u = ap(t, 13.1) * a
    panel(cv, (840, 140, 1220, 590), u)
    cv.text((1030, 154), "Dome Fuji, Antarctica", "serif", 22, INK, "ma", u)
    def yd(m): return 200 + m * .25
    cv.rect((900, yd(0), 960, yd(1250)), mix(CREAM, ICE, u), mix(CREAM, ICED, u), 2, 4)
    rs = random.Random(2)
    for i in range(70):
        m = rs.uniform(80, 1240); keep = 1.0 if m < 600 else max(0.0, 1 - (m - 600) / 500)
        if rs.random() < keep: cv.ring((rs.uniform(908, 952), yd(m)), 3, mix(CREAM, (120, 150, 175), u), 2)
    for m, lab, t0 in ((0, "surface", 13.1), (600, "about 600 m: first hydrates", 16.2), (1100, "below about 1,100 m:", 18.5)):
        uu = ap(t, t0) * a
        cv.line([(960, yd(m)), (990, yd(m))], mix(CREAM, INK, uu), 2); cv.text((998, yd(m) - 10), lab, "sansb" if m else "sans", 16, INK, "la", uu)
    cv.text((998, yd(1100) + 12), "no bubbles at all", "sansb", 16, RED, "la", ap(t, 20.6) * a)
    cv.para(870, 534, "The air is still there. You just can't see it.", "serif", 17, INK, 340, 1.25, "l", ap(t, 22.5) * a)
    src_line(cv, 606, "Sources: Uchida et al. (Dome Fuji air hydrates); Davies, Ice core basics. The molecule drawing is a sketch, not the real geometry.", a)
    return cv.im.reduce(SS)

def bar_scale(cv, x0, x1, y, lo, hi, ticks, unit, u):
    cv.line([(x0, y), (x1, y)], mix(CREAM, INK, u), 2)
    for v in ticks:
        x = x0 + (x1 - x0) * (v - lo) / (hi - lo)
        cv.line([(x, y), (x, y + 8)], mix(CREAM, INK, u), 2); cv.text((x, y + 12), "{:,}".format(v), "sans", 14, INK, "ma", u)
    cv.text((x1, y + 34), unit, "sans", 14, DIM, "ra", u)

def air_frame(t, dur):
    cv = Cv(); a = fade(t, dur)
    cv.header("What ancient air is made of", "Mostly the same as yours. The big difference is carbon dioxide.", a)
    panel(cv, (60, 140, 470, 400), a)
    cv.text((84, 154), "Mostly", "serif", 24, INK, "la", a)
    cv.rect((84, 200, 446, 236), mix(CREAM, (196, 210, 226), a), None, 0, 6); cv.rect((84, 200, 84 + 362 * .78, 236), mix(CREAM, (120, 150, 190), a), None, 0, 6)
    cv.text((92, 207), "nitrogen ~78%", "sansb", 15, CREAM, "la", a); cv.text((446, 242), "oxygen ~21%", "sansb", 15, INK, "ra", a)
    u = ap(t, 2.2) * a
    cv.para(84, 276, "Oxygen over 800,000 years: down only about 0.7% of what it was.", "sans", 18, INK, 360, 1.3, "l", u)
    cv.text((84, 360), "(a relative drop, not 0.7 points)", "sansl", 14, DIM, "la", u)
    u = ap(t, 7.0) * a
    panel(cv, (490, 140, 1220, 590), u)
    cv.text((514, 154), "Carbon dioxide", "serif", 26, INK, "la", u)
    x0, x1, lo, hi = 530, 1180, 150, 450
    def X(v): return x0 + (x1 - x0) * (v - lo) / (hi - lo)
    bar_scale(cv, x0, x1, 470, lo, hi, (150, 200, 250, 300, 350, 400, 450), "parts per million (ppm)", u)
    ub = ap(t, 10.2) * a
    cv.rect((X(172), 240, X(172) + (X(300) - X(172)) * ap(t, 15.7, 2.0), 290), mix(CREAM, ICED, ub), mix(CREAM, COOL, ub), 2, 6)
    cv.text((X(172), 212), "Before the industrial era, 800,000 years of ice cores", "sansb", 15, COOL, "la", ub)
    cv.text((X(172) + 6, 254), "172", "sansb", 16, INK, "la", ap(t, 15.7) * a); cv.text((X(300) - 6, 254), "300", "sansb", 16, INK, "ra", ap(t, 17.6) * a)
    um = ap(t, 19.1) * a
    cv.text((514, 318), "2026, Mauna Loa, Hawaii: monthly averages", "sansb", 15, RED, "la", um)
    for v, lab, t0, yy in ((431, "June ~431", 24.8, 350), (426, "Sept ~426", 26.9, 400)):
        uu = ap(t, t0) * a
        cv.line([(X(v), yy), (X(v), 460)], mix(CREAM, RED, uu), 3); cv.circ((X(v), yy), 7, mix(CREAM, RED, uu))
        cv.text((X(v) - 12, yy - 10), lab, "sansb", 16, RED, "ra", uu)
    pill(cv, 760, 545, "ROUGHLY 1.5 TIMES THE OLD HIGH", ap(t, 30.3) * a, RED, 330)
    src_line(cv, 606, "Sources: EPICA Dome C CO2 (Luthi et al. 2008); NOAA GML Mauna Loa monthly means (2026); oxygen: Stolper et al. 2016.", a)
    return cv.im.reduce(SS)

def methane_frame(t, dur):
    cv = Cv(); a = fade(t, dur)
    cv.header("Methane tells the same story, louder", "Ice-core methane before the industrial era, and the global average now.", a)
    panel(cv, (60, 150, 1220, 560), a)
    x0, x1, lo, hi = 110, 1170, 0, 2100
    def X(v): return x0 + (x1 - x0) * (v - lo) / (hi - lo)
    bar_scale(cv, x0, x1, 440, lo, hi, (0, 500, 1000, 1500, 2000), "parts per billion (ppb)", a)
    u = ap(t, 7.0) * a
    cv.text((X(350), 196), "650,000 years before the industrial era (ice cores)", "sansb", 16, COOL, "la", u)
    w_ = ap(t, 12.0, 1.5)
    cv.rect((X(350), 230, X(350) + (X(800) - X(350)) * w_, 290), mix(CREAM, ICED, u), mix(CREAM, COOL, u), 2, 6)
    cv.text((X(350), 300), "~350  ice ages", "sansb", 16, INK, "la", ap(t, 8.2) * a)
    cv.text((X(800), 326), "~800  warm times", "sansb", 16, INK, "ra", ap(t, 12.0) * a)
    uu = ap(t, 18.4) * a
    cv.text((X(1935), 196), "June 2026, global average", "sansb", 16, RED, "ra", ap(t, 15.0) * a)
    cv.line([(X(1935), 230), (X(1935), 432)], mix(CREAM, RED, uu), 4); cv.circ((X(1935), 260), 9, mix(CREAM, RED, uu))
    cv.text((X(1935) - 16, 270), "~1,935", "sansb", 22, RED, "ra", uu)
    pill(cv, 640, 510, "ABOUT 2.4 TIMES THE OLD HIGH", ap(t, 21.2) * a, RED, 320)
    src_line(cv, 606, "Sources: EPICA Dome C methane (Loulergue et al. 2008); NOAA GML global monthly methane (June 2026, 1,934.6 ppb).", a)
    return cv.im.reduce(SS)

def extract_frame(t, dur):
    cv = Cv(); a = fade(t, dur)
    cv.header("How do you get the air out?", "Three ways scientists free the old air from the ice.", a)
    items = [(2.0, "CRUSH", "in a cold vacuum (dry)"), (4.3, "MELT", "and collect the gas (wet)"), (5.2, "VAPOR", "turn ice straight to gas")]
    for i, (t0, k, v) in enumerate(items):
        u = ap(t, t0) * a; x = 80 + i * 390
        panel(cv, (x, 150, x + 360, 430), u)
        cx, cy = x + 180, 260
        if k == "CRUSH":
            for j in range(5): cv.poly([(cx - 70 + j * 30, cy - 30), (cx - 55 + j * 30, cy + 20), (cx - 40 + j * 30, cy - 30)], mix(CREAM, STEEL, u))
            rs = random.Random(1)
            for j in range(16):
                xx = cx - 70 + rs.uniform(0, 140); yy = cy + 32 + rs.uniform(0, 26); cv.rect((xx, yy, xx + rs.uniform(4, 10), yy + rs.uniform(4, 9)), mix(CREAM, ICED, u))
        elif k == "MELT":
            cv.poly([(cx, cy - 50), (cx - 36, cy + 10), (cx, cy + 50), (cx + 36, cy + 10)], mix(CREAM, (150, 190, 225), u))
            cv.circ((cx, cy + 14), 36, mix(CREAM, (150, 190, 225), u))
        else:
            cv.rect((cx - 40, cy + 10, cx + 40, cy + 50), mix(CREAM, ICE, u), mix(CREAM, ICED, u), 2, 6)
            for j in range(3): cv.arc((cx - 30 + j * 30, cy - 10), 18, 200, 340, mix(CREAM, DIM, u), 3); cv.arc((cx - 30 + j * 30, cy - 40), 18, 20, 160, mix(CREAM, DIM, u), 3)
        cv.text((cx, 340), k, "sansb", 24, INK, "ma", u); cv.text((cx, 380), v, "sans", 17, INK, "ma", u)
    u = ap(t, 7.1) * a
    panel(cv, (80, 450, 1200, 580), u)
    cv.para(104, 468, "Melting can make extra carbon dioxide, so melting is used for gases such as methane instead.", "serif", 22, INK, 1070, 1.3, "l", u)
    src_line(cv, 606, "Sources: Schmitt et al. 2011, AMT (dry, wet, sublimation extraction); Krauss et al., EGU26-13891 (laser method, 2026).", a)
    return cv.im.reduce(SS)

def oldest_frame(t, dur):
    cv = Cv(); a = fade(t, dur)
    cv.header("What the oldest air did, and didn't, say", "Allan Hills, Antarctica: the six-million-year-old air from Part One.", a)
    panel(cv, (60, 140, 620, 590), a)
    cv.text((84, 154), "6 million years old", "serif", 24, INK, "la", a)
    rows = [("AGE", "from its argon", GREEN), ("TEMPERATURE", "Antarctica about 12 C cooler since then", GREEN)]
    for i, (k, v, col) in enumerate(rows):
        yy = 210 + i * 80; cv.text((84, yy), k, "sansb", 18, col, "la", a); cv.para(84, yy + 28, v, "sans", 18, INK, 510, 1.25, "l", a)
    u = ap(t, .4) * a
    cv.text((84, 380), "CARBON DIOXIDE", "sansb", 18, RED, "la", u)
    cv.para(84, 408, "No number from that air published, as of our research.", "sans", 18, INK, 510, 1.25, "l", u)
    pill(cv, 500, 168, "AS OF OUR RESEARCH", u, AMBER, 200)
    u = ap(t, 5.0) * a
    panel(cv, (640, 140, 1220, 590), u)
    cv.text((664, 154), "An earlier Allan Hills study (2019)", "serif", 22, INK, "la", u)
    cv.para(664, 200, "Air from about 1 to 2 million years ago:", "sans", 18, INK, 530, 1.25, "l", u)
    cv.text((664, 240), "about 204 to 289 ppm", "sansb", 26, COOL, "la", ap(t, 10.1) * a)
    u2 = ap(t, 14.5) * a
    cv.text((664, 320), "Oldest samples: over 1,600 ppm", "sansb", 22, INK, "la", u2)
    strike(cv, 660, 1010, 336, ap(t, 16.9, 1.0) * a)
    cv.para(664, 372, "Microbes near the bedrock had probably added carbon dioxide.", "sans", 18, INK, 530, 1.25, "l", ap(t, 17.6) * a)
    pill(cv, 850, 470, "NOT THE ANCIENT SKY", ap(t, 22.8) * a, RED, 230)
    src_line(cv, 606, "Sources: Shackleton et al. 2025 (6-million-year Allan Hills ice); Yan et al. 2019, Nature (1 to 2 million years; microbial CO2).", a)
    return cv.im.reduce(SS)

def claims_frame(t, dur):
    cv = Cv(); a = fade(t, dur)
    cv.header("Ancient ice in a drink?", "One company sells Greenland iceberg ice to bars. Its claims, labelled.", a)
    rows = [(0.1, "Sold as", "Greenland iceberg ice", None),
            (3.8, "Age", "over 100,000 years old", "THE SELLER'S CLAIM"),
            (8.2, "Bubbles", "none, a co-founder said", "IF SO, NO FIZZ")]
    for i, (t0, k, v, tg) in enumerate(rows):
        u = ap(t, t0) * a; yy = 150 + i * 140
        panel(cv, (100, yy, 1180, yy + 120), u)
        cv.text((130, yy + 20), k, "sansb", 20, DIM, "la", u); cv.text((330, yy + 34), v, "serif", 30, INK, "la", u)
        if tg: pill(cv, 1020, yy + 60, tg, ap(t, t0 + 2.0) * a, RED, 220)
    src_line(cv, 606, "Company not named. Its age claim and the co-founder's no-bubbles remark are as reported; not tested by us.", a)
    return cv.im.reduce(SS)

def modern_frame(t, dur):
    cv = Cv(); a = fade(t, dur)
    cv.header("Old air, modern air", "No medical claims here: what is known, and what is not.", a)
    panel(cv, (60, 140, 620, 420), a)
    cv.text((84, 154), "Air in old ice", "serif", 24, INK, "la", a)
    cv.para(84, 196, "Sealed before modern traffic and factory pollution.", "sans", 19, INK, 510, 1.3, "l", a)
    u = ap(t, 4.0) * a
    cv.para(84, 262, "But nature always had some:", "sans", 19, INK, 510, 1.3, "l", u)
    for i, w_ in enumerate(("smoke", "dust", "pollen", "ozone")):
        uu = ap(t, 4.2 + i * .9) * a; cv.tag(150 + i * 125, 330, w_, uu, 110, COOL)
    u = ap(t, 8.4) * a
    panel(cv, (640, 140, 1220, 420), u)
    cv.text((664, 154), "US EPA: main outdoor asthma triggers", "serif", 22, INK, "la", u)
    cv.tag(790, 236, "ground-level ozone", ap(t, 12.6) * a, 230, AMBER); cv.text((790, 260), "(a part of smog)", "sans", 15, DIM, "ma", ap(t, 14.4) * a)
    cv.tag(1070, 236, "particle pollution", ap(t, 15.9) * a, 220, AMBER)
    pill(cv, 930, 350, "HEALTH BENEFIT OF ANCIENT AIR: NOT ESTABLISHED", ap(t, 19.9) * a, RED, 470)
    u = ap(t, 23.9) * a
    panel(cv, (60, 440, 1220, 580), u)
    cv.text((84, 454), "And the ice isn't pure", "serif", 22, INK, "la", u)
    cv.para(84, 494, "It holds dust, ash and sea salt from its own time, which is exactly what scientists read.", "sans", 20, INK, 1100, 1.3, "l", ap(t, 26.2) * a)
    src_line(cv, 606, "Sources: US EPA, asthma triggers (outdoor air pollution); ice-core impurity records.", a)
    return cv.im.reduce(SS)

def y2014_frame(t, dur):
    cv = Cv(); a = fade(t, dur)
    cv.header("Why keep old air?", "Because the future asks new questions.", a)
    u = ap(t, 3.6) * a
    panel(cv, (60, 140, 1220, 330), u)
    cv.text((84, 154), "2014", "serif", 34, AMBER, "la", u)
    cv.para(200, 160, "Scientists tested Cape Grim's archived bottles, with air pumped out of Greenland snow (firn).", "sans", 20, INK, 980, 1.3, "l", u)
    u2 = ap(t, 10.1) * a
    cv.text((200, 240), "Found: 4 ozone-destroying gases nobody had known were in the air", "sansb", 20, RED, "la", u2)
    for i, g in enumerate(("CFC-112", "CFC-112a", "CFC-113a", "HCFC-133a")):
        cv.tag(270 + i * 170, 292, g, ap(t, 10.6 + i * .4) * a, 150, COOL)
    u3 = ap(t, 15.3) * a
    panel(cv, (60, 350, 1220, 580), u3)
    cv.text((84, 364), "Using the old bottles, they traced one back to 1978", "serif", 24, INK, "la", u3)
    x0, x1 = 120, 1160
    cv.line([(x0, 470), (x1, 470)], mix(CREAM, INK, u3), 3)
    for yr in (1978, 1990, 2000, 2010, 2014):
        x = x0 + (x1 - x0) * (yr - 1978) / (2014 - 1978)
        cv.line([(x, 462), (x, 478)], mix(CREAM, INK, u3), 2); cv.text((x, 486), str(yr), "sansb" if yr in (1978, 2014) else "sans", 16, INK, "ma", u3)
    w_ = ap(t, 15.6, 2.5)
    cv.line([(x1, 440), (x1 - (x1 - x0) * w_, 440)], mix(CREAM, RED, u3), 5)
    cv.text((x1, 410), "HCFC-133a, read back from the archive", "sansb", 16, RED, "ra", u3)
    src_line(cv, 606, "Sources: Laube et al. 2014, Nature Geoscience; CSIRO Cape Grim Air Archive.", a)
    return cv.im.reduce(SS)

def today_frame(t, dur):
    cv = Cv(); a = fade(t, dur)
    cv.header("Today's air seals later than you'd think", "Law Dome, East Antarctica, where snow piles up fast.", a)
    panel(cv, (60, 140, 1220, 300), a)
    cv.text((84, 154), "Air at the sealing depth averages", "sans", 20, INK, "la", a)
    cv.text((84, 188), "about 9 years old", "serif", 34, AMBER, "la", ap(t, 2.2) * a)
    cv.text((640, 196), "(a mean: it is mixed air from many years)", "sans", 16, DIM, "la", ap(t, 2.2) * a)
    u = ap(t, 4.6) * a
    panel(cv, (60, 320, 1220, 590), u)
    pill(cv, 1100, 340, "OUR ESTIMATE", u, AMBER, 160)
    cv.text((84, 334), "Our own arithmetic, if conditions stay similar", "serif", 22, INK, "la", u)
    x0, x1 = 120, 1100
    def X(yr): return x0 + (x1 - x0) * (yr - 2024) / (2040 - 2024)
    cv.line([(x0, 460), (x1, 460)], mix(CREAM, INK, u), 3)
    for yr in range(2024, 2041, 2):
        cv.line([(X(yr), 452), (X(yr), 468)], mix(CREAM, INK, u), 2); cv.text((X(yr), 476), str(yr), "sans", 15, INK, "ma", u)
    u2 = ap(t, 8.0) * a
    cv.circ((X(2026), 430), 10, mix(CREAM, COOL, u2)); cv.text((X(2026), 392), "2026 air", "sansb", 16, COOL, "ma", u2)
    w_ = ap(t, 8.4, 3.0)
    if w_ > 0: cv.arrow((X(2026) + 14, 430), (X(2026) + 14 + (X(2034.5) - X(2026) - 14) * w_, 430), mix(CREAM, COOL, u2), 3, 10)
    u3 = ap(t, 11.0) * a
    cv.rect((X(2033), 400, X(2037), 446), mix(CREAM, (246, 226, 200), u3), mix(CREAM, AMBER, u3), 2, 8)
    cv.text((X(2035), 410), "some of it sealed, mid-2030s", "sansb", 15, INK, "ma", u3)
    cv.para(84, 510, "Mixed with air from other years, in ice from snow that fell decades earlier.", "sans", 18, INK, 1100, 1.3, "l", ap(t, 12.7) * a)
    cv.para(84, 546, "This year's snow will trap some future year's air.", "sansb", 18, INK, 1100, 1.3, "l", ap(t, 18.2) * a)
    src_line(cv, 606, "Source: Etheridge et al. 1996 and Levchenko 1996 (Law Dome). The mid-2030s date is our estimate from the ~9-year mean, not a measurement.", a)
    return cv.im.reduce(SS)

def record_frame(t, dur):
    cv = Cv(); a = fade(t, dur, .4, .8)
    cv.header("What lasts is what you write down", "The jar is the symbol. The record is the real time capsule.", a)
    # an index card
    cv.d.rounded_rectangle([200 * SS, 150 * SS, 1080 * SS, 580 * SS], radius=8 * SS, fill=mix(CREAM, (252, 250, 242), a), outline=mix(CREAM, RULE, a), width=2 * SS)
    for k in range(6): cv.line([(230, 250 + k * 56), (1050, 250 + k * 56)], mix(CREAM, (190, 205, 225), a), 1)
    cv.line([(290, 160), (290, 570)], mix(CREAM, (220, 150, 140), a), 2)
    cv.text((310, 182), "Air of  ________ (date),  ________ (place)", "serifr", 26, INK, "la", a)
    rows = [(2.3, "Carbon dioxide, outside:  ____ ppm", "a real infrared (NDIR) sensor"),
            (5.4, "That day's air quality (AQI):  ____", "local air-quality report"),
            (7.4, "Latest monthly Mauna Loa CO2:  ____ ppm", "NOAA, gml.noaa.gov")]
    for i, (t0, k, v) in enumerate(rows):
        uu = ap(t, t0, .5) * a; yy = 252 + i * 100
        cv.text((310, yy), k, "serifr", 25, INK, "la", uu); cv.text((330, yy + 40), v, "sans", 16, DIM, "la", uu)
    return cv.im.reduce(SS)

def end_frame(t, dur):
    cv = Cv(); a = fade(t, dur, .8, 1.5)
    cv.text((W / 2, 40), "Antarctica, Part 2: the sky in the ice", "serif", 34, INK, "ma", a)
    cv.text((W / 2, 92), "heartbeatobservatory.com", "sansb", 22, AMBER, "ma", a)
    cv.text((W / 2, 124), "Science  ·  Episode 8.10  ·  follows 8.7, Antarctica: what's frozen in the ice", "sans", 17, DIM, "ma", a)
    cv.line([(W / 2 - 60, 152), (W / 2 + 60, 152)], mix(CREAM, AMBER, a), 3)
    cv.text((W / 2, 160), "The 3D scenes are illustrations built in Blender: generic objects and places, not real footage, labs, products or sites.", "sans", 14, DIM, "ma", a)
    src = [
        "CO2: EPICA Dome C (Luthi et al. 2008); NOAA GML Mauna Loa monthly means  ·  Methane: Loulergue et al. 2008; NOAA GML global methane",
        "Oxygen: Stolper et al. 2016  ·  Firn and sealing: Battle et al. 2011; Schwander et al. 1997, 2001; Etheridge et al. 1996  ·  Air hydrates: Uchida et al. (Dome Fuji)",
        "Oldest air: Shackleton et al. 2025, PNAS; Yan et al. 2019, Nature  ·  Extraction: Schmitt et al. 2011; Krauss et al., EGU 2026",
        "Cape Grim Air Archive: CSIRO; Laube et al. 2014, Nature Geoscience  ·  Asthma triggers: US EPA  ·  Flask drift: NOAA GML",
    ]
    y = 186
    for i, s_ in enumerate(src):
        y = cv.para(W / 2, y, s_, "sans", 14, INK, 1200, 1.22, "m", ease((t - .5 - i * .2) / .6) * a) + 5
    u = ease((t - 2.0) / .6) * a
    panel(cv, (70, 330, 1210, 500), u)
    cv.text((W / 2, 342), "Labelled in the episode", "sansb", 17, RED, "ma", u)
    opens = [("AS OF OUR RESEARCH", "no CO2 number yet from the six-million-year air"),
             ("NOT ESTABLISHED", "any health benefit from breathing ancient air"),
             ("OUR ESTIMATE", "some 2026 air sealing at Law Dome around the mid-2030s"),
             ("REPORTED / CLAIMED", "'bergy seltzer'; a seller's 100,000-year ice")]
    for i, (tg, txt) in enumerate(opens):
        yy = 378 + i * 28
        cv.text((470, yy), tg, "sansb", 14, RED, "ra", u); cv.text((486, yy), txt, "sans", 15, INK, "la", u)
    cv.text((W / 2, 528), "Someday, someone will read the sky of your day.", "serif", 22, INK, "ma", u)
    cv.text((W / 2, 600), "Made by Claude Code on the MSI: Blender 5.1 (Cycles), Kokoro voice, Pillow, ffmpeg.  CC0.  Script fact-checked twice by Codex with web search.", "sans", 13, INK, "ma", a)
    return cv.im.reduce(SS)

BOARDS_FN = {"diag_firn": firn_frame, "diag_age": age_frame, "diag_hydrate": hydrate_frame, "diag_air": air_frame, "diag_methane": methane_frame,
             "diag_extract": extract_frame, "diag_oldest": oldest_frame, "diag_claims": claims_frame, "diag_modern": modern_frame,
             "diag_2014": y2014_frame, "diag_today": today_frame, "diag_record": record_frame, "end_card": end_frame}

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    only = [a for a in sys.argv[1:] if a.startswith("--only=")]
    if "--preview" in sys.argv:   # one still per board at 92% of its length (all elements in)
        os.makedirs("pv", exist_ok=True)
        for sh in SHOTS:
            if sh["cam"] is None and (not only or sh["name"] in only[0]):
                BOARDS_FN[sh["name"]](sh["dur"] * .92, sh["dur"]).save("pv/%s.png" % sh["name"])
        sys.exit(0)
    f = 1
    for sh in SHOTS:
        n = int(round(sh["dur"] * FPS))
        if sh["cam"] is None:
            fn = BOARDS_FN[sh["name"]]
            if only and sh["name"] not in only[0]: f += n; continue
            for i in range(n):
                p = os.path.join(OUT, "f_%04d.png" % (f + i))
                if os.path.exists(p) and os.path.getsize(p) > 1000 and "--force" not in sys.argv: continue
                fn(i / FPS, sh["dur"]).save(p)
            print(sh["name"], f, f + n - 1, flush=True)
        f += n
