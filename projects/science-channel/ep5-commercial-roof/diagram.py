# The non-Blender passages, drawn with Pillow at 24 fps into the same frame numbering as the render:
#   "diag_heat" - one summer day on a metal roof: air vs panel temperature, the 40 ft panel growing and shrinking, the screw hole.
#   "diag_leak" - the flat roof in cutaway: membrane, cover board, two layers of polyiso, steel deck, bar joist; water through a
#                 seam spreads in the insulation, R-value drops, the deck rusts from the top, the ceiling stains.
#   "diag_cool" - why white: solar reflectance numbers (new / aged / dark), roof surface temperatures (DOE), what it buys.
#   "end_card"  - Heartbeat Observatory + the source list.
# Own look (cream paper, earth tones, ink lines), same family as 8.4.   python diagram.py [FRAMES_DIR] [--force]
import math, os, sys, random
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shots import SHOTS, FPS
OUT = next((a for a in sys.argv[1:] if not a.startswith("--")), "C:/Users/lilli/Renders/roof-ep5/frames")
W, H, SS = 1280, 720, 2
CREAM = (243, 237, 224); INK = (46, 40, 34); DIM = (120, 110, 96); RULE = (200, 190, 172); PAPER = (236, 226, 206)
WATER = (62, 120, 190); AMBER = (196, 120, 28); RED = (178, 70, 52); STEEL = (150, 155, 160); RUST = (165, 82, 30)
MEMB = (225, 225, 218); COVER = (190, 180, 160); ISO = (222, 200, 120); DECK = (140, 146, 150); JOIST = (110, 112, 115)
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
    def rect(s, b, fill, outline=None, w=2, r=0):
        bb = [b[0] * SS, b[1] * SS, b[2] * SS, b[3] * SS]
        s.d.rounded_rectangle(bb, radius=r * SS, fill=fill, outline=outline, width=w * SS if outline else 0)
    def circ(s, c, r, fill, outline=None, w=2): s.d.ellipse([(c[0] - r) * SS, (c[1] - r) * SS, (c[0] + r) * SS, (c[1] + r) * SS], fill=fill, outline=outline, width=w * SS if outline else 0)
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
    def tag(s, cx, cy, t, a=1.0, wdt=150):
        s.rect((cx - wdt / 2, cy - 15, cx + wdt / 2, cy + 15), mix(CREAM, (236, 220, 190), a), outline=mix(CREAM, AMBER, a), w=2, r=8)
        s.text((cx, cy - 10), t, "sansb", 16, AMBER, "ma", a)
    def arrow(s, a_, b_, col, w=3, head=9):
        s.line([a_, b_], col, w)
        ang = math.atan2(b_[1] - a_[1], b_[0] - a_[0])
        s.poly([b_, (b_[0] - head * math.cos(ang - .5), b_[1] - head * math.sin(ang - .5)), (b_[0] - head * math.cos(ang + .5), b_[1] - head * math.sin(ang + .5))], col)

# ---------------------------------------------------------------- one summer day on a metal roof
def air_T(h): return 77 + 13 * math.cos((h - 15.5) / 24 * 2 * math.pi)                          # 64 at ~3:30 am, 90 at ~3:30 pm
def panel_T(h):
    sun = max(0.0, math.sin((h - 6) / 14 * math.pi)) if 6 <= h <= 20 else 0.0
    return air_T(h) - 4 + 68 * sun ** 1.3                                                         # ~150 at ~1 pm, below air at night (radiates to the sky)
def heat_frame(t, dur):
    cv = Cv(); a = min(1.0, t / .5, (dur - t) / .5)
    cv.text((90, 44), "One summer day on an exposed-fastener metal roof", "serif", 38, INK, "la", a)
    cv.text((90, 92), "Typical curves, not a measurement. Peak from DOE Energy Saver (conventional roofs 150 F or more); the panel movement is the standard expansion formula.", "sans", 17, DIM, "la", a)
    # graph box
    gx0, gy0, gx1, gy1 = 90, 150, 760, 470
    cv.rect((gx0, gy0, gx1, gy1), mix(CREAM, (238, 232, 218), a), outline=mix(CREAM, RULE, a), w=2, r=6)
    def X(h): return gx0 + 30 + (gx1 - gx0 - 60) * h / 24.0
    def Y(T): return gy1 - 20 - (gy1 - gy0 - 50) * (T - 40) / 130.0
    for T in (40, 70, 100, 130, 170):
        cv.line([(gx0 + 30, Y(T)), (gx1 - 30, Y(T))], mix(CREAM, RULE, a * .8), 1); cv.text((gx0 + 24, Y(T) - 9), "%d F" % T, "sans", 15, DIM, "ra", a)
    for h, lab in ((0, "midnight"), (6, "6 am"), (12, "noon"), (18, "6 pm"), (24, "midnight")):
        cv.text((X(h), gy1 - 16), lab, "sans", 15, DIM, "ma", a)
    cv.line([(X(0), Y(32)), (X(24), Y(32))], mix(CREAM, (150, 170, 200), a), 1)
    # curves draw in: air 0.5-4 s, panel 4-9 s
    ua = ease((t - .5) / 3.5); up = ease((t - 4) / 5.0)
    pts = [(X(h), Y(air_T(h))) for h in [i * 24 / 120 for i in range(int(120 * ua) + 1)]]
    if len(pts) > 1: cv.line(pts, mix(CREAM, WATER, a), 3)
    if ua > .8: cv.text((X(19.5), Y(air_T(19.5)) + 8), "air", "sansb", 17, WATER, "la", a)
    pts = [(X(h), Y(panel_T(h))) for h in [i * 24 / 120 for i in range(int(120 * up) + 1)]]
    if len(pts) > 1: cv.line(pts, mix(CREAM, RED, a), 3)
    if up > .45: cv.text((X(8.2) - 8, Y(panel_T(8.2)) - 6), "steel panel surface", "sansb", 17, RED, "ra", a)
    if up >= 1: cv.text((X(13) + 6, Y(150) - 26), "~150 F (DOE: 150 F or more on a sunny afternoon)", "sans", 15, RED, "la", a)
    # after 9 s: a time marker sweeps the day twice, the panel bar follows
    hh = None
    if t >= 9:
        hh = ((t - 9) * 24 / 4.5) % 24
        cv.line([(X(hh), gy0 + 10), (X(hh), gy1 - 30)], mix(CREAM, INK, a * .7), 2)
        cv.circ((X(hh), Y(panel_T(hh))), 6, mix(CREAM, RED, a))
    # the panel: 40 ft, drawn as a bar whose length change is magnified x40 and shown
    bx0, by = 90, 540
    T = panel_T(hh) if hh is not None else 70.0
    dL = 6.5e-6 * 480 * (T - 70.0)        # inches, from a 70 F install
    cv.text((bx0, 500), "One 40 ft steel panel, screwed down at a 70 F install:", "sansb", 19, INK, "la", a)
    L = 560 + dL * 40 * 4
    cv.rect((bx0, by, bx0 + L, by + 28), mix(CREAM, STEEL, a), outline=mix(CREAM, INK, a), w=2, r=3)
    for i in range(1, 7): cv.line([(bx0 + i * 80, by + 2), (bx0 + i * 80, by + 26)], mix(CREAM, (120, 125, 130), a), 1)
    cv.circ((bx0 + 26, by + 14), 5, mix(CREAM, INK, a)); cv.text((bx0 + 26, by + 34), "fixed screw", "sans", 14, DIM, "ma", a)
    cv.line([(bx0 + 560, by - 8), (bx0 + 560, by + 36)], mix(CREAM, DIM, a), 1)
    col = RED if dL > 0 else WATER
    cv.text((bx0 + 585, by + 2), "%+.2f in" % dL, "serif", 24, col, "la", a)
    cv.text((bx0 + 585, by + 30), "length change (exaggerated)", "sans", 14, DIM, "la", a)
    # the screw hole, magnified: the panel slides under a fixed screw and the hole wears oval
    sx, sy = 960, 300
    cv.text((sx, 150), "At every screw, magnified", "sansb", 19, INK, "ma", a)
    cv.rect((sx - 130, 180, sx + 130, 420), mix(CREAM, STEEL, a), outline=mix(CREAM, INK, a), w=2, r=4)
    wear = ease((t - 9) / 9.0) if t >= 9 else 0.0
    shift = dL * 40 * 4 * .6
    cv.circ((sx + shift, sy), 22 + 10 * wear, mix(CREAM, (60, 56, 52), a))              # the hole, going oval with wear
    cv.rect((sx + shift - 34 - 10 * wear, sy - 22, sx + shift + 34 + 10 * wear, sy + 22), mix(CREAM, (60, 56, 52), a), r=22)
    cv.circ((sx, sy), 30, mix(CREAM, (90, 90, 95), a), outline=mix(CREAM, INK, a), w=2)   # washer
    cv.circ((sx, sy), 16, mix(CREAM, (170, 172, 175), a), outline=mix(CREAM, INK, a), w=2)  # head
    if t >= 9:
        cv.arrow((sx - 90, sy + 70), (sx - 90 + 40 * (1 if dL > 0 else -1), sy + 70), mix(CREAM, col, a))
        cv.text((sx, sy + 95), "panel slides, screw stays", "sans", 15, DIM, "ma", a)
        cv.text((sx, sy + 118), "the hole wears oval, the washer cracks", "sans", 15, DIM, "ma", a * wear)
    if t >= 13:
        u = ease((t - 13) / 4.0); n = int(5500 * u)
        cv.text((sx, 440), "%s" % format(n, ","), "serif", 48, INK, "ma", a)
        cv.text((sx, 500), "day-night cycles in 15 years (365 a year)", "sans", 16, DIM, "ma", a)
        cv.tag(sx, 540, "ARITHMETIC, NOT A TEST", a, 230)
    cv.text((90, 652), "ΔL = 6.5 x 10^-6 per F  x  480 in  x  ΔT.  A 150 F panel from a 70 F install: about +1/4 in; the winter low to the summer high, about 1/2 in.", "sans", 16, DIM, "la", a)
    cv.text((90, 676), "Standing-seam roofs let that movement happen on sliding clips; most exposed-fastener roofs make the screw holes take it.", "sans", 16, DIM, "la", a)
    cv.tag(1140, 664, "ESTIMATE", a, 130)
    return cv.im.reduce(SS)

# ---------------------------------------------------------------- the flat roof in cutaway
def leak_frame(t, dur):
    cv = Cv(); a = min(1.0, t / .5, (dur - t) / .5)
    cv.text((90, 44), "Where the water goes", "serif", 40, INK, "la", a)
    cv.text((90, 92), "Cutaway of the flat roof, not to scale. A common assembly: 60-mil membrane, cover board, two layers of polyiso, steel deck, bar joists.", "sans", 17, DIM, "la", a)
    X0, X1, Y = 90, 820, 150
    layers = [(Y, Y + 22, MEMB, "Single-ply membrane (TPO/PVC ~60 mil, drawn thick)"),
              (Y + 22, Y + 50, COVER, "Cover board (e.g. 1/2 in gypsum)"),
              (Y + 50, Y + 120, ISO, "Polyiso insulation, layer 1"),
              (Y + 120, Y + 190, ISO, "Polyiso insulation, layer 2 (joints staggered)"),
              (Y + 190, Y + 232, DECK, "Steel deck (1.5 in ribs)"),
              (Y + 232, Y + 330, None, "Bar joists, then the room below")]
    for i, (ya, yb, c, lab) in enumerate(layers):
        aa = ease((t - .3 - i * .5) / .6) * a
        if c is not None:
            if i == 4:   # deck: a ribbed profile
                cv.rect((X0, ya, X1, ya + 8), mix(CREAM, c, aa))
                k = X0
                while k < X1 - 1:
                    cv.poly([(k, ya + 8), (k + 14, ya + 8), (k + 20, yb), (k + 34, yb), (k + 40, ya + 8), (k + 48, ya + 8)], mix(CREAM, c, aa))
                    cv.poly([(k + 14, ya + 8), (k + 20, yb), (k + 34, yb), (k + 40, ya + 8)], None, outline=mix(CREAM, (90, 95, 100), aa), w=1)
                    k += 48
            else:
                cv.rect((X0, ya, X1, yb), mix(CREAM, c, aa))
                if i in (2, 3):   # board joints
                    off = 0 if i == 2 else 120
                    for k in range(X0 + off, X1, 240): cv.line([(k, ya), (k, yb)], mix(CREAM, (180, 160, 90), aa), 2)
                    rnd = random.Random(i)
                    for _ in range(300):
                        cv.circ((rnd.uniform(X0 + 3, X1 - 3), rnd.uniform(ya + 3, yb - 3)), rnd.uniform(.8, 1.8), mix(CREAM, (200, 175, 95), aa))
        else:
            for k in range(X0 + 60, X1, 220):   # joists
                cv.rect((k - 3, ya, k + 3, ya + 6), mix(CREAM, JOIST, aa)); cv.rect((k - 3, yb - 10, k + 3, yb - 4), mix(CREAM, JOIST, aa))
                for j in range(6):
                    cv.line([(k - 40 + j * 16, ya + 6), (k - 32 + j * 16, yb - 10)], mix(CREAM, JOIST, aa), 2)
            cv.rect((X0, yb - 4, X1, yb), mix(CREAM, (120, 120, 118), aa))   # ceiling line / top of the room
        cv.text((X1 + 22, (ya + yb) / 2 - 10), lab, "sans", 18, INK, "la", aa)
        cv.line([(X1 + 4, (ya + yb) / 2), (X1 + 16, (ya + yb) / 2)], mix(CREAM, DIM, aa), 2)
    # the seam with a fishmouth at x=300
    sx = 300
    cv.line([(sx - 60, Y + 3), (sx + 60, Y + 3)], mix(CREAM, (170, 170, 160), a), 2)
    fm = ease((t - 6) / 1.5) * a
    cv.poly([(sx - 10, Y), (sx + 22, Y - 10 * fm - 1), (sx + 40, Y - 2), (sx + 40, Y + 4), (sx - 10, Y + 4)], mix(CREAM, (205, 205, 198), a))
    if fm > 0: cv.text((sx + 50, Y + 1), "open seam (fishmouth)", "sansb", 15, RED, "la", fm)
    # rain + water path: 7-13 s water enters, drops through the cover board, spreads sideways in the insulation
    if t >= 7:
        u = ease((t - 7) / 6.0)
        rnd = random.Random(1)
        for i in range(30):
            rx = rnd.uniform(X0, X1); ph = ((t * 1.4) + rnd.random()) % 1.0
            cv.line([(rx, 128 + 16 * ph), (rx - 1, 136 + 16 * ph)], mix(CREAM, WATER, a * .7), 2)
        # down through the open seam and the cover board
        cv.poly([(sx + 8, Y + 2), (sx + 20, Y + 2), (sx + 24, Y + 50 * min(1, u * 3)), (sx + 4, Y + 50 * min(1, u * 3))], mix(CREAM, WATER, a))
        # the spread in the insulation (an elongated blob, growing sideways much more than down)
        sp = max(0.0, (u - .3) / .7)
        if sp > 0:
            wdt = 40 + 330 * sp; dep = 20 + 120 * min(1, sp * 1.3)
            cy = Y + 50
            cv.poly([(sx + 14 - wdt * .55, cy), (sx + 14 + wdt, cy), (sx + 14 + wdt * .85, cy + dep * .6), (sx + 14 + wdt * .5, cy + dep), (sx + 14 - wdt * .3, cy + dep), (sx + 14 - wdt * .5, cy + dep * .5)], mix(CREAM, (120, 150, 190), a * .85))
            if sp > .5: cv.text((110, 515), "Water can spread sideways in the insulation, well beyond the hole.", "sansb", 20, WATER, "la", ease((sp - .5) / .3) * a)
    # 14-22 s: R-value meter and the "cannot dry" note
    if t >= 14:
        u = ease((t - 14) / 5.0)
        mx, my = 1060, 560
        cv.text((mx, my - 40), "Insulating value of the wet boards", "sansb", 17, INK, "ma", ease((t - 14) / .6) * a)
        cv.rect((mx - 120, my, mx + 120, my + 26), mix(CREAM, (230, 224, 210), a), outline=mix(CREAM, DIM, a), w=2, r=6)
        cv.rect((mx - 118, my + 2, mx - 118 + 236 * (1 - .6 * u), my + 24), mix(CREAM, mix(ISO, RED, u), a), r=5)
        cv.text((mx, my + 32), "falls as the foam fills with water; how far depends on how wet", "sans", 13, DIM, "ma", a)
        cv.tag(mx, my + 66, "ESTIMATE", a, 120)
        if t >= 18:
            aa = ease((t - 18) / .8) * a
            cv.text((110, 545), "The membrane that let the water in now keeps it from drying out.", "sansb", 20, INK, "la", aa)
    # 22-30 s: deck rusts from the top, drips, stain
    if t >= 22:
        u = ease((t - 22) / 5.0)
        ya = Y + 190
        rnd = random.Random(3)
        for i in range(int(60 * u)):
            rx = rnd.uniform(sx - 120, sx + 300); cv.circ((rx, ya + rnd.uniform(0, 6)), rnd.uniform(2, 5), mix(CREAM, RUST, a * .9))
        if u > .4:
            aa = ease((u - .4) / .4) * a
            cv.text((110, 575), "The steel deck rusts from the top, where no one can see it.", "sansb", 20, RUST, "la", aa)
            # drips off the deck bottom into the room, a stain on the ceiling line
            for k in range(3):
                ph = ((t * 1.1) + k * .33) % 1.0; dx = sx + 60 + k * 90
                cv.line([(dx, Y + 232 + 90 * ph), (dx, Y + 232 + 90 * ph + 10)], mix(CREAM, WATER, aa), 3)
            cv.poly([(sx + 20, Y + 326), (sx + 300, Y + 326), (sx + 300, Y + 330), (sx + 20, Y + 330)], mix(CREAM, RUST, aa * .8))
            cv.text((sx + 160, Y + 332), "the ceiling stain, often far from the hole", "sans", 14, RUST, "ma", aa)
    if t >= 29:
        aa = ease((t - 29) / .8) * a
        cv.rect((90, 652, 1190, 698), mix(CREAM, PAPER, aa), outline=mix(CREAM, RULE, aa), w=2, r=8)
        cv.text((640, 662), "By the time the ceiling stains, the insulation may have been wet for a long time. Found with an infrared scan after sunset, confirmed with core cuts.", "sansb", 16, INK, "ma", aa)
    cv.text((90, 120), "Sources: NRCA Roofing Manual (membrane assemblies); ERDC roof moisture surveys (flashing and penetration defects as the main source of wet insulation); PIMA / manufacturer polyiso data.", "sansl", 14, DIM, "la", a)
    return cv.im.reduce(SS)

# ---------------------------------------------------------------- why white
def cool_frame(t, dur):
    cv = Cv(); a = min(1.0, t / .5, (dur - t) / .5)
    cv.text((90, 44), "Why the coating is white", "serif", 40, INK, "la", a)
    cv.text((90, 92), "Solar reflectance = the share of sunlight a surface bounces back. Rating labs (CRRC) test it new and after three years outdoors.", "sans", 17, DIM, "la", a)
    # bars: dark roof, white new, white aged 3 yr
    bars = [("dark roof", .05, .20, (60, 58, 55), "about 5-20 %"), ("white, new", .78, .85, (225, 225, 218), "about 80 %"), ("white, 3 years of dirt", .55, .65, (205, 200, 185), "typically 55-65 %")]
    bx0, by0, bh = 120, 170, 300
    for i, (lab, lo, hi, col, txt) in enumerate(bars):
        u = ease((t - 1 - i * 1.2) / 1.2) * a
        x = bx0 + i * 210
        cv.rect((x, by0, x + 140, by0 + bh), mix(CREAM, (236, 230, 216), u), outline=mix(CREAM, RULE, u), w=2, r=6)
        for k in (0, .25, .5, .75, 1): cv.line([(x + 2, by0 + bh - bh * k), (x + 138, by0 + bh - bh * k)], mix(CREAM, RULE, u * .8), 1)
        mid = (lo + hi) / 2 * ease((t - 1.2 - i * 1.2) / 1.2)
        cv.rect((x + 20, by0 + bh - bh * mid, x + 120, by0 + bh), mix(CREAM, col, u), outline=mix(CREAM, INK, u), w=2, r=4)
        cv.line([(x + 125, by0 + bh - bh * hi), (x + 125, by0 + bh - bh * lo)], mix(CREAM, AMBER, u), 3)   # the range
        cv.text((x + 70, by0 + bh + 10), lab, "sansb", 16, INK, "ma", u)
        cv.text((x + 70, by0 + bh + 34), txt, "sans", 15, DIM, "ma", u)
    cv.text((bx0 - 8, by0 - 6), "100 %", "sans", 13, DIM, "ra", a); cv.text((bx0 - 8, by0 + bh - 14), "0 %", "sans", 13, DIM, "ra", a)
    cv.text((bx0, by0 + bh + 64), "Ranges (amber) from LBNL / CRRC rated-product data; the old ENERGY STAR roof mark (ended 2022) asked for 0.65 new and 0.50 aged on low-slope roofs.", "sansl", 14, DIM, "la", a)
    # thermometers: conventional vs cool roof (DOE)
    if t >= 6:
        u = ease((t - 6) / 1.0) * a
        tx = 880
        cv.text((tx + 110, 160), "Sunny summer afternoon (DOE Energy Saver)", "sansb", 18, INK, "ma", u)
        for k, (lab, T, col) in enumerate((("conventional dark roof", 150, RED), ("cool roof", 100, WATER))):
            x = tx + k * 190
            cv.rect((x, 200, x + 26, 440), mix(CREAM, (230, 224, 210), u), outline=mix(CREAM, DIM, u), w=2, r=13)
            uu = ease((t - 6.5 - k * 1.2) / 2.0); hgt = 226 * (T - 40) / 140.0 * uu
            cv.rect((x + 7, 440 - 7 - hgt, x + 19, 440 - 7), mix(CREAM, col, u), r=6); cv.circ((x + 13, 452), 18, mix(CREAM, col, u))
            cv.text((x + 13, 480), "%d F" % int(round(40 + 140 * hgt / 226)) if uu > 0 else "", "serif", 30, INK, "ma", u)
            cv.text((x + 13, 518), lab, "sans", 15, DIM, "ma", u)
        if t >= 10:
            uu = ease((t - 10) / .8) * a
            cv.text((tx + 110, 556), "about 50 F cooler", "sansb", 20, WATER, "ma", uu)
            cv.text((tx + 110, 582), "\"150 F or more\" vs \"more than 50 F cooler\" - energy.gov", "sansl", 13, DIM, "ma", uu)
    # what it buys / what it costs
    if t >= 13:
        rows = [("Less heat into the panel = less daily movement at every screw and seam", 13),
                ("Cooling energy: DOE puts the saving at up to about 15 % for a single-storey building in a warm climate", 15.5),
                ("Cold winters give part of it back (the roof also reflects wanted winter sun); the net depends on the climate", 18),
                ("The numbers are for the coating as rated; dirt, ponding and algae pull a roof toward the aged value", 20.5)]
        for i, (txt, t0) in enumerate(rows):
            u = ease((t - t0) / .7) * a
            y = 626 + i * 0 if False else 0
        y = 612
        for i, (txt, t0) in enumerate(rows):
            u = ease((t - t0) / .7) * a
            cv.circ((100, y + 9 + i * 24), 4, mix(CREAM, AMBER, u)); cv.text((114, y + i * 24), txt, "sans", 16, INK, "la", u)
    cv.tag(1150, 640, "TYPICAL VALUES", a, 170)
    return cv.im.reduce(SS)

def end_frame(t, dur):
    cv = Cv(); a = min(1.0, t / .8, (dur - t) / 1.2)
    cv.text((W / 2, 36), "Heartbeat Observatory", "serif", 54, INK, "ma", a)
    cv.text((W / 2, 106), "heartbeatobservatory.com", "sansb", 27, AMBER, "ma", a)
    cv.text((W / 2, 144), "Science  ·  Episode 8.5  ·  How a commercial roof dies", "sans", 20, DIM, "ma", a)
    cv.line([(W / 2 - 60, 178), (W / 2 + 60, 178)], mix(CREAM, AMBER, a), 3)
    cv.text((W / 2, 190), "A simulation. Lifespans and timings are typical ranges, drawn from these sources:", "sans", 18, DIM, "ma", a)
    src = [
        "DOE Energy Saver, Cool Roofs (energy.gov): conventional roofs 150 F+ on a sunny afternoon, cool roofs more than 50 F cooler, up to ~15 % cooling saving",
        "LBNL Heat Island Group / Cool Roof Rating Council: rated solar reflectance new and 3-year aged (ASTM D7897); EPA ENERGY STAR roof criteria (0.65 / 0.50, sunset June 2022)",
        "NRCA Roofing Manual: ponding = water remaining 48 h after rain; positive drainage, 1/4 in per ft (also IBC 1507); IBC 2018 s.1511.3.1 / 2021 s.1512.2.1: coatings over metal and single-ply without tear-off",
        "Manufacturer / contractor service-life ranges (they vary widely): TPO and PVC ~20-30 yr, EPDM ~15-30 yr, metal ~30-50+ yr (GAF, CentiMark, Nations Roof, J.S. Held, NRCA)",
        "Coating specs: silicone / acrylic dry film ~20-40 mils for 10-20 yr warranties; power wash, fastener repair, rust-inhibiting primer, fabric-reinforced details, adhesion test (GAF, Progressive Materials guides)",
        "Thermal movement: ΔL = α L ΔT with steel α ≈ 6.5-6.7 x 10^-6 per F (Construction Canada, Professional Roofing); fastener back-out, washer failure, long-life fasteners (roofing trade sources, MBCI)",
        "Wet insulation and moisture surveys: ERDC / US Army roof surveys; infrared + core cuts; IIBEC single-ply aging studies; PIMA polyiso data",
    ]
    y = 228
    for i, s_ in enumerate(src):
        y = cv.para(W / 2, y, s_, "sans", 16, INK, 1140, 1.22, "m", ease((t - .6 - i * .18) / .6) * a) + 6
    cv.text((W / 2, 668), "Made by Claude Code on the MSI: Blender 5.1 (Cycles), Kokoro voice, Pillow, ffmpeg.  CC0.  Generic product types only; no brand is recommended.", "sansl", 16, DIM, "ma", a)
    return cv.im.reduce(SS)

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    f = 1
    for sh in SHOTS:
        n = int(round(sh["dur"] * FPS))
        if sh["cam"] is None:
            fn = {"diag_heat": heat_frame, "diag_leak": leak_frame, "diag_cool": cool_frame}.get(sh["name"], end_frame)
            only = [a for a in sys.argv[1:] if a.startswith("--only=")]
            if only and sh["name"] not in only[0]: f += n; continue
            for i in range(n):
                p = os.path.join(OUT, "f_%04d.png" % (f + i))
                if os.path.exists(p) and os.path.getsize(p) > 1000 and "--force" not in sys.argv: continue
                fn(i / FPS, sh["dur"]).save(p)
            print(sh["name"], f, f + n - 1, flush=True)
        f += n
