# Pillow boards for Science 8.7 Antarctica Part 1 (cream-paper look, same family as ep6).  python diagram.py [FRAMES_DIR] [--force] [--only=name] [--preview]
import math, os, sys, random
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shots import SHOTS, FPS
OUT = next((a for a in sys.argv[1:] if not a.startswith("--")), "C:/Users/lilli/Renders/antarctica-ep7/frames")
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


# ======================================================================== ep7 boards (Science 8.7, Antarctica Part 1)
# Layout rule (same as ep6): nothing below y = 640; finish.py shrinks each board into the top of the frame and puts the captions
# in a dark band under it.  No em or en dashes anywhere on screen.
ICE = (120, 170, 214); ICED = (70, 120, 170); SNOWC = (250, 250, 248); FIRN = (222, 232, 240); ROCKC = (96, 86, 76); SEA_ = (88, 140, 180)
GREEN = (70, 130, 80)
def fade(t, dur, a_in=.6, a_out=1.0): return max(0.0, min(1.0, t / a_in, (dur - t) / a_out))
def ap(t, t0, d=.7): return ease((t - t0) / d)
def src_line(cv, y, text, a): cv.text((W / 2, y), text, "sansl", 13, DIM, "ma", a)

def layers_frame(t, dur):
    cv = Cv(); a = fade(t, dur)
    cv.header("How ice gets that old", "Snow piles up year after year; its weight squeezes the old snow into ice and seals in air.", a)
    x0, x1, y0, y1 = 90, 330, 150, 590
    u = a
    for i in range(60):
        f0 = (i / 60) ** 1.6; f1 = ((i + 1) / 60) ** 1.6
        ya, yb = y0 + (y1 - y0) * f0, y0 + (y1 - y0) * f1
        d = (ya - y0) / (y1 - y0)
        base = mix(SNOWC, FIRN, min(1, d * 3)) if d < .33 else mix(FIRN, ICE, min(1, (d - .33) * 1.6))
        if i % 2: base = mix(base, (255, 255, 255), .25)
        cv.rect((x0, ya, x1, yb + 1), mix(CREAM, base, u))
    cv.rect((x0, y0, x1, y1), None, mix(CREAM, INK, u), 2)
    rs = random.Random(3)
    for k in range(140):
        yy = y0 + (y1 - y0) * (.36 + .62 * rs.random()); xx = rs.uniform(x0 + 8, x1 - 8)
        cv.circ((xx, yy), 1.3 + 1.6 * rs.random(), mix(CREAM, (250, 252, 255), u), mix(CREAM, ICED, u), 1)
    for (yy, lab) in ((y0 + 30, "new snow"), (y0 + 150, "firn: packed old snow"), (y0 + 300, "ice: air trapped in bubbles"), (y1 - 40, "deeper = older, thinner layers")):
        cv.line([(x1 + 6, yy), (x1 + 28, yy)], mix(CREAM, DIM, u), 2); cv.text((x1 + 34, yy - 10), lab, "sans", 16, INK, "la", u)
    cv.text(((x0 + x1) / 2 + 60, y1 + 8), "Layer on layer, like tree rings (drawn, not to scale)", "sansl", 13, DIM, "ma", u)
    bx = 640
    u1 = ap(t, 1.5) * a
    cv.rect((bx, 150, 1230, 360), mix(CREAM, PAPER, u1), mix(CREAM, RULE, u1), 2, 10)
    cv.text((bx + 22, 162), "One unbroken record", "serif", 24, INK, "la", u1)
    cv.text((bx + 22, 196), "Beyond EPICA  ·  Little Dome C, East Antarctica  ·  January 2025", "sansb", 15, AMBER, "la", u1)
    cv.para(bx + 22, 226, "Drilled about 2.8 km down to bedrock. The core holds one continuous record at least 1.2 million years long.", "sans", 17, INK, 540, 1.3, "l", u1)
    for i in range(10):
        cv.rect((bx + 22 + i * 54, 296, bx + 22 + (i + 1) * 54 - 4, 316), mix(CREAM, mix(FIRN, ICED, i / 9), u1))
    cv.text((bx + 22, 322), "surface", "sansl", 13, DIM, "la", u1); cv.text((bx + 558, 322), "bedrock, ~2.8 km", "sansl", 13, DIM, "ra", u1)
    u2 = ap(t, 6.0) * a
    cv.rect((bx, 380, 1230, 590), mix(CREAM, PAPER, u2), mix(CREAM, RULE, u2), 2, 10)
    cv.text((bx + 22, 392), "Scattered very old chunks", "serif", 24, INK, "la", u2)
    cv.text((bx + 22, 426), "Allan Hills blue-ice area  ·  announced October 2025", "sansb", 15, AMBER, "la", u2)
    cv.para(bx + 22, 456, "Ice up to about 6 million years old, dated directly from argon gas in its air bubbles. Not one timeline: old pieces pushed up near the surface, where wind strips the snow away.", "sans", 17, INK, 545, 1.3, "l", u2)
    src_line(cv, 614, "Sources: CNR / Stockholm University (Beyond EPICA, Jan 2025); WHOI and PNAS, 28 Oct 2025 (Allan Hills, COLDEX).", ap(t, 7) * a)
    return cv.im.reduce(SS)

def dna_frame(t, dur):
    cv = Cv(); a = fade(t, dur)
    cv.header("The oldest DNA ever read", "Found in mud, not in bone or ice. Ages are approximate.", a)
    X0, X1 = 330, 1180
    def X(myr): return X0 + (X1 - X0) * myr / 7.0
    y = 310
    cv.line([(X0, y), (X1, y)], mix(CREAM, INK, a), 3)
    for m in range(8):
        cv.line([(X(m), y - 6), (X(m), y + 6)], mix(CREAM, INK, a), 2); cv.text((X(m), y + 12), "%d" % m, "sans", 15, DIM, "ma", a)
    cv.text((X1, y + 34), "million years ago", "sansl", 14, DIM, "ra", a)
    rows = [(2.0, "Northern Greenland, 2022", "~2 million years: a lost forest with mastodons, reindeer, hares, geese", GREEN, 1.0),
            (1.0, "Scotia Sea floor, 2022", "~1 million years: oldest confirmed DNA from the sea (drilled 2019, up to 178 m under the seafloor)", BLUE, 3.0),
            (0.54, "diatom DNA in that mud", "~540,000 years: glass-shelled algae", SEA_, 5.0)]
    for i, (myr, title, det, col, t0) in enumerate(rows):
        u = ap(t, t0) * a
        yy = 150 + i * 50
        cv.rect((X0, yy, X(myr), yy + 24), mix(CREAM, col, u))
        cv.text((X0 - 14, yy + 1), title, "sansb", 15, INK, "ra", u)
        cv.para(X(myr) + 10, yy + 2, det, "sans", 14, INK, X1 + 80 - X(myr), 1.15, "l", u)
    u = ap(t, 8.0) * a
    cv.dashed([(X(6.8), 140), (X(6.8), y - 8)], mix(CREAM, RED, u), 2)
    cv.text((X(6.8) - 6, 280), "bone model", "sansb", 13, RED, "ra", u)
    cv.rect((60, 380, 1220, 476), mix(CREAM, PAPER, u), mix(CREAM, RULE, u), 2, 10)
    cv.text((80, 390), "A model, not a find", "sansb", 16, RED, "la", u)
    cv.para(80, 414, "One study (Allentoft et al. 2012, moa bones) estimated that DNA in bone kept at minus 5 °C would be broken apart completely after roughly 6.8 million years (dashed line). Most ancient DNA survives only as short, broken pieces.", "sans", 16, INK, 1110, 1.3, "l", u)
    u = ap(t, 10.0) * a
    cv.rect((60, 494, 1220, 574), mix(CREAM, PAPER, u), mix(CREAM, RULE, u), 2, 10)
    cv.para(80, 506, "DNA lasts longer stuck to grains of clay and other minerals.  And DNA by itself is not alive: it is a molecule, not a cell.", "sans", 17, INK, 1110, 1.3, "l", u)
    src_line(cv, 604, "Sources: Kjær et al., Nature 2022 (Kap København); Armbrecht et al., Nature Communications, 5 Oct 2022; Allentoft et al. 2012.", ap(t, 10.5) * a)
    return cv.im.reduce(SS)

def revive_frame(t, dur):
    cv = Cv(); a = fade(t, dur)
    cv.header("Has anything really come back to life?", "A few things have. Here is how sure each one is.", a)
    rows = [("Bacteria from seafloor mud", "more than 100 million years (101.5)", "Woke up and multiplied in a lab. From mud under the deep seafloor, not from ice.", "Morono et al., Nature Communications 2020", "REVIVED IN LAB", GREEN),
            ("A tiny worm (nematode), Siberia", "about 46,000 years in permafrost", "Revived; more than 100 generations since. Some scientists suspect modern contamination.", "Shatilovich et al., PLOS Genetics 2023", "SOME DOUBT", AMBER),
            ("Bacteria from Antarctic ice, 2007 claim", "about 8 million years", "Only weak growth and damaged DNA. The age of the ice is still questioned.", "Bidle et al., PNAS 2007", "DOUBTED", RED)]
    for i, (what, age, det, src, tagt, col) in enumerate(rows):
        u = ap(t, 1.0 + i * 6.0) * a
        y0 = 140 + i * 158
        cv.rect((60, y0, 1220, y0 + 142), mix(CREAM, PAPER, u), mix(CREAM, RULE, u), 2, 10)
        cv.text((84, y0 + 14), what, "serif", 25, INK, "la", u)
        cv.text((84, y0 + 52), age, "sansb", 17, col, "la", u)
        cv.para(84, y0 + 80, det, "sans", 16, INK, 880, 1.3, "l", u)
        cv.text((84, y0 + 120), src, "sansl", 12, DIM, "la", u)
        cv.tag(1105, y0 + 30, tagt, u, 200, col)
    return cv.im.reduce(SS)

def amoeba(cv, c, r, u, seed=4):
    rs = random.Random(seed); pts = []
    for i in range(60):
        th = 2 * math.pi * i / 60
        rr = r * (1 + .28 * max(0, math.sin(3 * th + 1)) ** 3 + .08 * math.sin(7 * th + seed) + .3 * max(0, math.sin(2 * th - 2)) ** 6)
        pts.append((c[0] + rr * math.cos(th), c[1] + rr * .8 * math.sin(th)))
    cv.poly(pts, mix(CREAM, (214, 226, 200), u), mix(CREAM, GREEN, u), 2)
    cv.circ((c[0] - r * .15, c[1]), r * .22, mix(CREAM, (170, 190, 150), u), mix(CREAM, GREEN, u), 2)
    for k in range(12):
        cv.circ((c[0] + rs.uniform(-.5, .5) * r, c[1] + rs.uniform(-.4, .4) * r), 2.5, mix(CREAM, (150, 170, 130), u))

def siberia_frame(t, dur):
    cv = Cv(); a = fade(t, dur)
    cv.header("The zombie viruses: Siberia, not Antarctica", "Real, but from frozen ground at the other end of the planet.", a)
    u = a
    cv.rect((60, 150, 580, 360), mix(CREAM, PAPER, u), mix(CREAM, RULE, u), 2, 10)
    cv.text((84, 164), "Where they came from", "sansb", 16, GREEN, "la", u)
    cv.text((84, 192), "Siberia", "serif", 44, INK, "la", u)
    cv.para(84, 256, "Permafrost: ground in the far north (the Arctic) that has stayed frozen for thousands of years.", "sans", 17, INK, 470, 1.3, "l", u)
    u2 = ap(t, 2.5) * a
    cv.rect((60, 380, 580, 520), mix(CREAM, PAPER, u2), mix(CREAM, RULE, u2), 2, 10)
    cv.text((84, 394), "Not from", "sansb", 16, RED, "la", u2)
    cv.text((84, 420), "Antarctic ice", "serif", 40, DIM, "la", u2)
    cv.line([(80, 448), (80 + font("serif", 40).getlength("Antarctic ice") / SS + 10, 448)], mix(CREAM, RED, u2), 3)
    cv.text((84, 482), "The other end of the planet.", "sans", 16, INK, "la", u2)
    u3 = ap(t, 4.0) * a
    cv.rect((620, 150, 1220, 400), mix(CREAM, PAPER, u3), mix(CREAM, RULE, u3), 2, 10)
    cv.text((644, 164), "What was revived", "serif", 24, INK, "la", u3)
    cv.para(644, 202, "Giant viruses from Siberian permafrost, up to about 48,500 years old (Alempic et al. 2023), after the first one, Pithovirus, in 2014.", "sans", 17, INK, 550, 1.3, "l", u3)
    cv.para(644, 296, "The scientists chose viruses that infect only amoebae: tiny single-celled creatures. Not people.", "sans", 17, INK, 550, 1.3, "l", u3)
    u4 = ap(t, 8.0) * a
    amoeba(cv, (760, 505), 66, u4)
    cv.text((760, 586), "an amoeba (drawn)", "sansl", 13, DIM, "ma", u4)
    cv.tag(1040, 480, "AMOEBAE ONLY", u4, 200, GREEN)
    cv.tag(1040, 530, "NOT PEOPLE", u4, 200, GREEN)
    src_line(cv, 614, "Sources: Alempic et al., Viruses 15(2):564, Feb 2023; Legendre et al., PNAS 2014 (Pithovirus sibericum).", u4)
    return cv.im.reduce(SS)

# ---- Antarctica outline (simplified, hand-placed from published maps; lon, lat), ice shelves included
COAST = [(-57, -63.3), (-60, -64.0), (-62.5, -64.8), (-64.5, -65.8), (-66.5, -67.2), (-67.5, -68.6), (-68.5, -70.2), (-71, -71.3), (-74, -72.3), (-78, -72.9),
         (-85, -73.2), (-92, -72.9), (-98, -73.4), (-103, -74.6), (-108, -74.9), (-113, -74.1), (-120, -73.9), (-127, -74.3), (-134, -74.6), (-140, -75.4),
         (-146, -76.2), (-152, -77.6), (-158, -78.1), (-165, -78.4), (-172, -78.4), (-180, -78.1), (175, -77.8), (169, -77.6), (166, -77.4), (163.5, -76.0),
         (162.5, -74.8), (164.5, -73.6), (167, -72.6), (170, -71.4), (166, -70.6), (160, -69.8), (154, -68.9), (147, -67.9), (142, -66.9), (136, -66.2),
         (130, -66.2), (124, -66.4), (118, -66.8), (112, -66.3), (106, -65.9), (100, -65.6), (96, -66.2), (90, -66.6), (85, -66.9), (80, -67.6), (77, -68.8),
         (74, -69.7), (71, -69.6), (69, -68.2), (66, -67.6), (62, -67.4), (56, -66.6), (50, -66.6), (45, -67.6), (40, -68.9), (35, -69.4), (30, -69.9),
         (24, -70.2), (17, -70.0), (10, -70.2), (3, -70.4), (-3, -70.8), (-9, -71.3), (-14, -72.6), (-19, -74.0), (-24, -75.6), (-29, -76.5), (-34, -77.6),
         (-40, -78.0), (-47, -77.9), (-54, -76.6), (-59, -75.4), (-61.5, -74.0), (-61.5, -72.2), (-61, -70.4), (-61, -68.6), (-60, -66.8), (-59, -65.4), (-58, -64.3)]
def polar(lon, lat, cx, cy, R):
    r = R * (90 + lat) / 30.0; th = math.radians(lon)
    return (cx + r * math.sin(th), cy - r * math.cos(th))     # Greenwich (0 deg) at the top, 90 E to the right
def map_frame(t, dur):
    cv = Cv(); a = fade(t, dur)
    cv.header("Where the ice is being lost", "NASA satellites: an average of about 135 billion tonnes a year, 2002 to 2025.", a)
    cx, cy, R = 360, 372, 196
    cv.circ((cx, cy), R * 1.08, mix(CREAM, (214, 228, 238), a))
    pts = [polar(lo, la, cx, cy, R) for lo, la in COAST]
    cv.poly(pts, mix(CREAM, (250, 251, 252), a), mix(CREAM, ICED, a), 2)
    u = ap(t, 1.5) * a
    for lo, la, rr in ((-110, -76.0, 40), (-100, -75.0, 28), (-125, -76.5, 28), (-64, -68.0, 20)):
        p = polar(lo, la, cx, cy, R); cv.circ(p, rr, mix(CREAM, (238, 196, 186), u))
    cv.poly(pts, None, mix(CREAM, ICED, a), 2)
    u2 = ap(t, 4.0) * a
    for lo, la0, la1 in ((-108, -66.5, -73.4), (-95, -66.8, -72.6), (-122, -67.5, -73.4), (-72, -62.5, -66.8)):
        cv.arrow(polar(lo, la0, cx, cy, R), polar(lo, la1, cx, cy, R), mix(CREAM, RED, u2), 3, 10)
    p = polar(-100, -64.0, cx, cy, R); cv.text((p[0] - 6, p[1] - 22), "warm ocean water melts", "sansb", 14, RED, "ra", u2)
    cv.text((p[0] - 6, p[1] - 4), "floating ice from below", "sansb", 14, RED, "ra", u2)
    u3 = ap(t, 7.0) * a
    for lo, la, name, dx, anch in ((159.7, -76.7, "Allan Hills", 10, "la"), (122.5, -75.3, "Beyond EPICA", 10, "la"),
                                    (-151.5, -84.4, "Lakes Whillans and Mercer", 10, "la")):
        p = polar(lo, la, cx, cy, R); cv.circ(p, 5, mix(CREAM, INK, u3)); cv.text((p[0] + dx, p[1] - 9), name, "sansb", 13, INK, anch, u3)
    cv.text(polar(80, -78, cx, cy, R), "EAST", "serif", 20, DIM, "ma", a); cv.text(polar(-75, -80, cx, cy, R), "WEST", "serif", 20, DIM, "ma", a)
    cv.text((cx, 588), "Outline simplified. South Pole at the centre.", "sansl", 12, DIM, "ma", a)
    x = 720
    u4 = ap(t, 2.5) * a
    cv.rect((x, 150, 1230, 300), mix(CREAM, PAPER, u4), mix(CREAM, RULE, u4), 2, 10)
    cv.text((x + 20, 162), "~135 billion tonnes a year", "serif", 26, INK, "la", u4)
    cv.para(x + 20, 202, "Average loss 2002 to 2025 from the GRACE and GRACE-FO satellites (NASA). Mostly in the west and at the edges. An independent reanalysis gets about 101, give or take 89.", "sans", 15, INK, 470, 1.3, "l", u4)
    u5 = ap(t, 9.0) * a
    cv.rect((x, 316, 1230, 440), mix(CREAM, PAPER, u5), mix(CREAM, RULE, u5), 2, 10)
    cv.para(x + 20, 330, "Some of the very old ice lies deep inland; at Allan Hills some is pushed up near the surface. Ice flows outward, so much of what is lost at the edges is younger.", "sans", 15, INK, 470, 1.3, "l", u5)
    u6 = ap(t, 14.0) * a
    cv.rect((x, 456, 1230, 570), mix(CREAM, (236, 220, 190), u6), mix(CREAM, AMBER, u6), 2, 10)
    cv.para(x + 20, 470, "How much ancient DNA reaches the sea from today's melt is still unknown.", "sans", 16, INK, 300, 1.3, "l", u6)
    cv.tag(x + 410, 512, "OPEN QUESTION", u6, 150, RED)
    src_line(cv, 614, "Sources: NASA Earth Indicators and SVS (GRACE/GRACE-FO 2002-2025); Otosaka et al. 2023 (IMBIE); Rignot et al., Science 2013.", u6)
    return cv.im.reduce(SS)

def risk_frame(t, dur):
    cv = Cv(); a = fade(t, dur)
    cv.header("Disease: how worried should we be?", "What the evidence says so far.", a)
    cx, cy, R = 330, 420, 200
    segs = [(180, 216, (150, 190, 140)), (216, 252, (200, 210, 140)), (252, 288, (230, 200, 120)), (288, 324, (230, 160, 110)), (324, 360, (210, 110, 90))]
    for a0, a1, col in segs:
        for k in range(0, 28, 2):
            cv.arc((cx, cy), R - k, a0, a1, mix(CREAM, col, a), 3)
    u = ap(t, 1.0, 1.2) * a
    ang = math.radians(180 + 36 * (.3 + .7 * u))
    cv.line([(cx, cy), (cx + (R - 40) * math.cos(ang), cy + (R - 40) * math.sin(ang))], mix(CREAM, INK, a), 5); cv.circ((cx, cy), 10, mix(CREAM, INK, a))
    cv.text((cx - R, cy + 14), "low", "sans", 15, DIM, "ma", a); cv.text((cx + R, cy + 14), "high", "sans", 15, DIM, "ma", a)
    cv.text((cx, cy + 40), "Low, but not zero, and watched", "serif", 26, INK, "ma", u)
    cv.text((cx, cy + 80), "(how some scientists see it; not a measured number)", "sansl", 13, DIM, "ma", u)
    x = 640
    items = [(2.5, "A 2025 review found viruses from thawing permafrost no riskier than viruses in ordinary soil and water.", "Mackelprang et al., mSystems 2025", INK),
             (6.0, "No disease-causing germ released from Antarctic ice has been documented.", "No documented case found in the research for this episode", INK),
             (10.0, "The real danger there today came from outside: H5N1 bird flu, found on the mainland in 2024, in skuas and then in Adélie penguins.", "Reports, February and March 2024", RED)]
    y = 150
    for t0, txt, src, col in items:
        u = ap(t, t0) * a
        cv.rect((x, y, 1230, y + 128), mix(CREAM, PAPER, u), mix(CREAM, RULE, u), 2, 10)
        cv.para(x + 20, y + 14, txt, "sans", 17, col, 540, 1.3, "l", u)
        cv.text((x + 20, y + 104), src, "sansl", 12, DIM, "la", u)
        y += 144
    src_line(cv, 614, "Sources: Mackelprang et al., mSystems 2025; National Academies workshop 2020; Popular Science and ScienceAlert (H5N1, 2024).", ap(t, 10) * a)
    return cv.im.reduce(SS)

def treaty_frame(t, dur):
    cv = Cv(); a = fade(t, dur)
    cv.header("Why you can't just go", "Rules that keep Antarctica for peace and science.", a)
    cards = [(.8, "1959", "The Antarctic Treaty", "Several countries claim parts of Antarctica. The treaty sets those claims aside and keeps the continent for peace and science. 58 countries have joined (April 2026)."),
             (5.0, "1991", "The Madrid Protocol", "Bans mining. Activities there need an environmental assessment first, tourism included."),
             (9.5, "100", "people ashore at once", "The limit tour operators follow at a landing site (IAATO; Measure 15, 2009)."),
             (13.0, "Clean", "boots and clothes", "Operators normally scrub and disinfect boots at landings and vacuum clothes for seeds.")]
    for i, (t0, big, title, det) in enumerate(cards):
        u = ap(t, t0) * a
        x0 = 60 + (i % 2) * 590; y0 = 150 + (i // 2) * 222
        cv.rect((x0, y0, x0 + 570, y0 + 206), mix(CREAM, PAPER, u), mix(CREAM, RULE, u), 2, 10)
        cv.text((x0 + 24, y0 + 14), big, "serif", 44, AMBER, "la", u)
        cv.text((x0 + 24 + font("serif", 44).getlength(big) / SS + 16, y0 + 34), title, "sansb", 19, INK, "la", u)
        cv.para(x0 + 24, y0 + 82, det, "sans", 17, INK, 520, 1.3, "l", u)
    src_line(cv, 614, "Sources: Antarctic Treaty Secretariat; Japan MOFA (58 parties, Apr 2026); Protocol on Environmental Protection (1991); IAATO.", ap(t, 13) * a)
    return cv.im.reduce(SS)

def jobs_frame(t, dur):
    cv = Cv(); a = fade(t, dur)
    cv.header("How people actually go", "Most visitors arrive by ship. Some go to work.", a)
    stats = [(.6, "~118,000", "visitors in the 2024-25 season", "IAATO: 118,491, most by ship"),
             (3.5, "$6,000 to $50,000", "an expedition cruise, per person", "typical published prices")]
    for i, (t0, big, lab, src) in enumerate(stats):
        u = ap(t, t0) * a; x0 = 60 + i * 590
        cv.rect((x0, 150, x0 + 570, 300), mix(CREAM, PAPER, u), mix(CREAM, RULE, u), 2, 10)
        cv.text((x0 + 285, 164), big, "serif", 42, AMBER, "ma", u)
        cv.text((x0 + 285, 222), lab, "sans", 19, INK, "ma", u)
        cv.text((x0 + 285, 262), src, "sansl", 13, DIM, "ma", u)
    u = ap(t, 7.0) * a
    cv.rect((60, 320, 1220, 530), mix(CREAM, PAPER, u), mix(CREAM, RULE, u), 2, 10)
    cv.text((84, 334), "Or get a job: the United States Antarctic Program", "serif", 24, INK, "la", u)
    jobs = ["cooks", "cleaners", "carpenters", "mechanics", "drivers"]
    for i, j in enumerate(jobs):
        uu = ap(t, 8.0 + i * .5) * a; xx = 84 + i * 222
        cv.rect((xx, 384, xx + 206, 430), mix(CREAM, (236, 220, 190), uu), mix(CREAM, AMBER, uu), 2, 22)
        cv.text((xx + 103, 392), j, "sansb", 19, INK, "ma", uu)
    u2 = ap(t, 11.0) * a
    cv.para(84, 456, "Hiring is mostly March to August for the next season, after physical and dental exams. Jobs go through the program's support contractor.", "sans", 18, INK, 1100, 1.3, "l", u2)
    src_line(cv, 614, "Sources: IAATO vessel-tourism overview (ATCM 46); Poseidon Expeditions and Aurora Expeditions price guides; usap.gov Jobs and Opportunities.", u2)
    return cv.im.reduce(SS)

def end_frame(t, dur):
    cv = Cv(); a = fade(t, dur, .8, 1.2)
    cv.text((W / 2, 22), "Heartbeat Observatory", "serif", 46, INK, "ma", a)
    cv.text((W / 2, 82), "heartbeatobservatory.com", "sansb", 24, AMBER, "ma", a)
    cv.text((W / 2, 116), "Science  ·  Episode 8.7  ·  Antarctica, Part 1: what's frozen in the ice", "sans", 18, DIM, "ma", a)
    cv.line([(W / 2 - 60, 146), (W / 2 + 60, 146)], mix(CREAM, AMBER, a), 3)
    cv.text((W / 2, 154), "The 3D scenes are illustrations built in Blender, not footage of real places or events. Sources:", "sans", 15, DIM, "ma", a)
    src = [
        "Ice: WHOI + PNAS 28 Oct 2025 (Allan Hills, 6 Myr, argon dating)  ·  CNR, Stockholm Univ. (Beyond EPICA, 1.2 Myr, Jan 2025)",
        "DNA: Armbrecht et al., Nat. Commun. 2022 (Scotia Sea)  ·  Kjær et al., Nature 2022 (Greenland)  ·  Allentoft et al. 2012 (bone model)",
        "Transformation: Verma et al., Front. Microbiol. 2024  ·  Revivals: Morono et al. 2020; Shatilovich et al. 2023; Bidle et al. 2007",
        "Viruses: Alempic et al., Viruses 2023; Legendre et al., PNAS 2014  ·  Risk: Mackelprang et al., mSystems 2025  ·  H5N1 reports 2024",
        "Lakes: Christner et al., Nature 2014 (Whillans)  ·  Kim et al., Nat. Commun. 18 Aug 2025 (Mercer)",
        "Ice loss: NASA GRACE/GRACE-FO 2002-2025; IMBIE 2023; Rignot et al. 2013  ·  Rules: Antarctic Treaty Secretariat; Madrid Protocol; IAATO; usap.gov",
    ]
    y = 182
    for i, s_ in enumerate(src):
        y = cv.para(W / 2, y, s_, "sans", 15, INK, 1200, 1.22, "m", ease((t - .5 - i * .2) / .6) * a) + 5
    u = ease((t - 2.0) / .6) * a
    cv.rect((70, 376, 1210, 544), mix(CREAM, PAPER, u), mix(CREAM, RULE, u), 2, 10)
    cv.text((W / 2, 386), "Still open (labelled in the episode)", "sansb", 17, RED, "ma", u)
    opens = [("IDEA, NOT SEEN IN THE WILD", "ancient DNA giving genes to today's bacteria"),
             ("NOT PROVEN", "Lake Mercer microbes sealed in since glaciers spread ~30 million years ago"),
             ("DOUBTED", "the 2007 claim of 8-million-year-old bacteria from Antarctic ice"),
             ("OPEN QUESTION", "how much ancient DNA reaches the sea from today's melt")]
    for i, (tg, txt) in enumerate(opens):
        yy = 418 + i * 30
        cv.text((372, yy), tg, "sansb", 14, RED, "ra", u); cv.text((388, yy), txt, "sans", 15, INK, "la", u)
    cv.text((W / 2, 558), "Part 2: what the ice remembers about the sky.", "serif", 20, INK, "ma", u)
    cv.text((W / 2, 600), "Made by Claude Code on the MSI: Blender 5.1 (Cycles), Kokoro voice, Pillow, ffmpeg.  CC0.  Fact-checked twice by Codex with web search.", "sans", 14, INK, "ma", a)
    return cv.im.reduce(SS)

BOARDS_FN = {"diag_layers": layers_frame, "diag_dna": dna_frame, "diag_revive": revive_frame, "diag_siberia": siberia_frame,
             "diag_map": map_frame, "diag_risk": risk_frame, "diag_treaty": treaty_frame, "diag_jobs": jobs_frame, "end_card": end_frame}

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    only = [a for a in sys.argv[1:] if a.startswith("--only=")]
    if "--preview" in sys.argv:   # one still per board at 70% of its length
        os.makedirs("pv", exist_ok=True)
        for sh in SHOTS:
            if sh["cam"] is None and (not only or sh["name"] in only[0]):
                BOARDS_FN[sh["name"]](sh["dur"] * .7, sh["dur"]).save("pv/%s.png" % sh["name"])
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
