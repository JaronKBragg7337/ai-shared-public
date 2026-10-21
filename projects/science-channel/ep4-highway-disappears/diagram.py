# The two non-Blender passages, drawn with Pillow at 24 fps into the same frame numbering as the render:
#   "diag_freeze" - a cutaway of the road layers: water in a crack, freeze (ice grows, crack widens), thaw (water goes deeper),
#                   a cycle counter, then the two mechanisms side by side (9 % expansion vs ice growth fed through channels).
#   "end_card"    - Heartbeat Observatory + the source list.
# Own look (cream paper, earth tones, ink lines) - not the navy card template.   python diagram.py [FRAMES_DIR]
import math, os, sys, random
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shots import SHOTS, FPS
OUT = next((a for a in sys.argv[1:] if not a.startswith("--")), "C:/Users/lilli/Renders/highway-ep4/frames")
W, H, SS = 1280, 720, 2
CREAM = (243, 237, 224); INK = (46, 40, 34); DIM = (120, 110, 96); RULE = (200, 190, 172)
ASPH = (72, 70, 68); ASPH2 = (96, 94, 90); BASE = (150, 138, 118); SUBB = (184, 172, 146); SOIL = (120, 92, 62)
WATER = (62, 120, 190); ICE = (190, 222, 240); ICE2 = (150, 196, 228); AMBER = (196, 120, 28); RED = (178, 70, 52)
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

# ---------------------------------------------------------------- the cutaway
def crack_path(x0, y0, depth, width, jag=7, seed=3):
    """left and right edge of a jagged crack from the surface (y0) down `depth`, opening `width` at the top"""
    rnd = random.Random(seed); L = []; R = []
    n = 9
    for i in range(n + 1):
        u = i / n; y = y0 + depth * u; w = width * (1 - u) ** 1.3 + 1.0
        dx = rnd.uniform(-jag, jag) * (0.3 + u)
        L.append((x0 + dx - w / 2, y)); R.append((x0 + dx + w / 2, y))
    return L, R

def cutaway(cv, t, a, state):
    """state: dict(water 0..1 fill height, ice 0..1, width px, depth px, fallen 0..1, temp F)"""
    X0, X1 = 90, 760; Y = 150
    # layers (surface course 5 cm = 40 px here, exaggerated on purpose and labelled)
    layers = [(Y, Y + 70, ASPH, "Asphalt, surface + binder (10-15 cm)"), (Y + 70, Y + 150, BASE, "Aggregate base, crushed stone"),
              (Y + 150, Y + 220, SUBB, "Subbase / drainage layer"), (Y + 220, Y + 380, SOIL, "Subgrade, Indiana clay")]
    for i, (ya, yb, c, lab) in enumerate(layers):
        aa = ease((t - .3 - i * .25) / .6) * a
        cv.rect((X0, ya, X1, yb), mix(CREAM, c, aa))
        if i == 1:   # stones
            rnd = random.Random(9)
            for _ in range(140):
                x = rnd.uniform(X0 + 6, X1 - 6); y = rnd.uniform(ya + 6, yb - 6); r = rnd.uniform(3, 7)
                cv.circ((x, y), r, mix(CREAM, mix(c, (110, 100, 86), .5), aa))
        if i == 3:
            rnd = random.Random(4)
            for _ in range(60):
                x = rnd.uniform(X0 + 6, X1 - 6); y = rnd.uniform(ya + 10, yb - 10)
                cv.line([(x, y), (x + rnd.uniform(8, 20), y + rnd.uniform(-2, 2))], mix(CREAM, (100, 74, 48), aa), 2)
        cv.text((X1 + 22, (ya + yb) / 2 - 11), lab, "sans", 21, INK, "la", aa)
        cv.line([(X1 + 4, (ya + yb) / 2), (X1 + 16, (ya + yb) / 2)], mix(CREAM, DIM, aa), 2)
    # aggregate texture in the surface
    rnd = random.Random(5)
    for _ in range(500):
        x = rnd.uniform(X0 + 3, X1 - 3); y = rnd.uniform(Y + 3, Y + 67)
        cv.circ((x, y), rnd.uniform(1, 2.6), mix(CREAM, ASPH2, ease((t - .3) / .6) * a))
    # the crack
    cx = 420; depth = state["depth"]; width = state["width"]
    L, R = crack_path(cx, Y, depth, width)
    cv.poly(L + R[::-1], mix(CREAM, (30, 26, 24), a))
    # water in it (from the bottom up to `water` share of depth)
    wf = state["water"]
    if wf > 0:
        k = max(1, int(round(len(L) * (1 - wf))))
        pts = L[k - 1:] + R[k - 1:][::-1]
        if len(pts) > 3: cv.poly(pts, mix(CREAM, WATER, a * .95))
    # ice (top part of the water column), lighter, pushing the walls: drawn wider by the ice share
    icf = state["ice"]
    if icf > 0:
        k0 = max(1, int(round(len(L) * (1 - wf)))); k1 = max(k0, int(round(len(L) * (1 - wf) + len(L) * wf * icf)))
        Li = [(x - icf * width * .18 * (1 - i / len(L)), y) for i, (x, y) in enumerate(L)]; Ri = [(x + icf * width * .18 * (1 - i / len(R)), y) for i, (x, y) in enumerate(R)]
        pts = Li[:k1 + 1] + Ri[:k1 + 1][::-1]
        if len(pts) > 3: cv.poly(pts, mix(CREAM, ICE, a)); cv.poly(pts, None, outline=mix(CREAM, ICE2, a), w=2)
        # push arrows
        for sgn in (-1, 1):
            x = cx + sgn * (width * .5 + 10); y = Y + 22
            cv.line([(x, y), (x + sgn * 26 * icf, y)], mix(CREAM, RED, a * icf), 4)
            cv.poly([(x + sgn * 26 * icf, y - 7), (x + sgn * 26 * icf, y + 7), (x + sgn * (26 * icf + 10), y)], mix(CREAM, RED, a * icf))
    # a broken-off piece of surface once the crack is wide (the start of a pothole)
    fl = state["fallen"]
    if fl > 0:      # the edges break off: a bowl opens at the surface (the start of a pothole)
        hw = width / 2 + 70 * fl; dp = 34 * fl
        cv.poly([(cx - hw, Y - 1), (cx + hw, Y - 1), (cx + hw * .7, Y + dp * .8), (cx + hw * .3, Y + dp), (cx - hw * .35, Y + dp), (cx - hw * .75, Y + dp * .7)], mix(CREAM, (30, 26, 24), a))
        cv.poly([(cx - hw, Y - 2), (cx + hw, Y - 2), (cx + hw, Y), (cx - hw, Y)], mix(CREAM, CREAM, a))
    # thermometer
    tx, ty = 1180, 150
    cv.rect((tx, ty, tx + 26, ty + 300), mix(CREAM, (230, 224, 210), a), outline=mix(CREAM, DIM, a), w=2, r=13)
    T = state["temp"]; u = (T - 0) / 70.0; u = max(0.02, min(.98, u))
    col = WATER if T > 32 else ICE2
    cv.rect((tx + 7, ty + 300 - 7 - 286 * u, tx + 19, ty + 300 - 7), mix(CREAM, RED if T > 32 else (90, 140, 200), a), r=6)
    cv.circ((tx + 13, ty + 312), 18, mix(CREAM, RED if T > 32 else (90, 140, 200), a))
    fy = ty + 300 - 7 - 286 * (32 / 70.0)
    cv.line([(tx - 14, fy), (tx + 40, fy)], mix(CREAM, INK, a), 2)
    cv.text((tx - 22, fy - 12), "32 F / 0 C", "sansb", 20, INK, "ra", a)
    cv.text((tx + 13, ty + 345), "%d F" % int(round(T)), "serif", 34, INK, "ma", a)
    cv.text((tx + 13, ty - 44), "Air temp.", "sans", 20, DIM, "ma", a)
    return cx, Y

def diag_frame(t, dur):
    cv = Cv()
    a = min(1.0, t / .5, (dur - t) / .5)
    # headline
    cv.text((90, 48), "What one winter does to a crack", "serif", 40, INK, "la", a)
    cv.text((90, 96), "Cutaway, not to scale. Layers labelled; depths are typical, not this road's.", "sans", 20, DIM, "la", a)
    cv.text((90, 124), "Sources: Gerber, Wilen, Dufresne & Style 2023, Phys. Rev. Lett. 131, 208201 (APS Physics 16, 194); Powers 1945 via FHWA. Cycle count = rough estimate (definitions vary).", "sansl", 15, DIM, "la", a)
    # phases: 0-6 build + rain fills crack; 6-11 freeze; 11-14 thaw; 14-24 cycles counter ramps 2..30 widening; 24-34 mechanisms panel
    if t < 24:
        if t < 6:
            water = ease((t - 2.5) / 3.0) * .55; ice = 0; width = 6; depth = 110; fallen = 0; temp = 41 - 6 * ease((t - 4) / 2)
        elif t < 11:
            u = ease((t - 6) / 4.0); water = .55; ice = u; width = 6 + 6 * u; depth = 110; fallen = 0; temp = 35 - 17 * u
        elif t < 14:
            u = ease((t - 11) / 2.5); water = .55 + .3 * u; ice = 1 - u; width = 12; depth = 110 + 50 * u; fallen = 0; temp = 18 + 24 * u
        else:
            n = (t - 14) / 10.0; cyc = ease(n)
            ph = ((t - 14) * 1.6) % 1.0
            ice = max(0.0, math.sin(ph * math.pi)) * (1 - .2 * cyc); water = .85
            width = 12 + 58 * cyc; depth = 160 + 150 * cyc; fallen = ease((cyc - .55) / .4)
            temp = 32 + 14 * math.cos(ph * 2 * math.pi) * (1 if True else 1)
        cx, Y = cutaway(cv, t, a, dict(water=water, ice=ice, width=width, depth=depth, fallen=fallen, temp=temp))
        # captions on the drawing
        PAPER = (236, 226, 206)
        if 2.5 < t < 6: cv.text((110, Y + 330), "Rain and melt water sit in the crack. The drain is blocked.", "sansb", 22, PAPER, "la", ease((t - 2.8) / .6) * a)
        if 6 <= t < 11 and temp < 32: cv.text((110, Y + 330), "Below 32 F: ice grows in the crack and pushes the sides apart.", "sansb", 22, PAPER, "la", ease((t - 6.3) / .6) * a)
        if 11 <= t < 14 and temp >= 32: cv.text((110, Y + 330), "Thaw: the water drops deeper into the wider crack.", "sansb", 22, PAPER, "la", ease((t - 11.3) / .6) * a)
        if t >= 14: cv.text((110, Y + 330), "Each swing that catches water works the crack a little wider.", "sansb", 22, PAPER, "la", ease((t - 14.3) / .6) * a)
        if t >= 14:
            n = int(1 + 29 * ease((t - 14) / 10.0))
            cv.text((90, 652), "Freeze-thaw cycle", "sans", 24, DIM, "la", a)
            cv.text((300, 630), "%d" % n, "serif", 60, INK, "la", a)
            cv.text((400, 652), "of roughly 25-40 a winter around Indianapolis", "sans", 24, INK, "la", a)
            cv.rect((930, 649, 1090, 681), mix(CREAM, (236, 220, 190), a), outline=mix(CREAM, AMBER, a), w=2, r=8)
            cv.text((1010, 654), "ROUGH ESTIMATE", "sansb", 17, AMBER, "ma", a)
    else:
        u = ease((t - 24) / .8)
        cv.text((90, 152), "Two explanations for the force", "serif", 30, INK, "la", u * a)
        # left: 9 % expansion
        bx = 90; by = 198
        cv.rect((bx, by, bx + 520, by + 362), mix(CREAM, (236, 230, 216), u * a), outline=mix(CREAM, RULE, u * a), w=2, r=14)
        cv.text((bx + 24, by + 20), "The classic one: water expands ~9 % when it freezes", "sansb", 22, INK, "la", u * a)
        # beaker: water vs ice volume
        wa = ease((t - 25) / 1.5) * a
        cv.rect((bx + 60, by + 66, bx + 180, by + 246), None, outline=mix(CREAM, INK, wa), w=3, r=4)
        cv.rect((bx + 63, by + 146, bx + 177, by + 243), mix(CREAM, WATER, wa), r=3)
        cv.text((bx + 120, by + 256), "water", "sans", 20, INK, "ma", wa)
        ia = ease((t - 26.5) / 1.5) * a
        cv.rect((bx + 260, by + 66, bx + 380, by + 246), None, outline=mix(CREAM, INK, ia), w=3, r=4)
        cv.rect((bx + 263, by + 146 - 8.7, bx + 377, by + 243), mix(CREAM, ICE, ia), outline=mix(CREAM, ICE2, ia), w=2, r=3)
        cv.text((bx + 320, by + 256), "ice: same water, +9 % volume", "sans", 20, INK, "ma", ia)
        cv.line([(bx + 395, by + 146), (bx + 395, by + 146 - 8.7)], mix(CREAM, RED, ia), 4)
        cv.text((bx + 404, by + 124), "+9 %", "sansb", 20, RED, "la", ia)
        cv.para(bx + 24, by + 288, "True, and it matters in sealed pores. But a crack is open at the top: expanding ice can push up and out.", "sans", 18, DIM, 470, 1.25, "l", ia)
        # right: ice growth fed through channels
        bx = 660
        ra = ease((t - 28) / .8) * a
        cv.rect((bx, by, bx + 530, by + 362), mix(CREAM, (236, 230, 216), ra), outline=mix(CREAM, RULE, ra), w=2, r=14)
        cv.text((bx + 24, by + 20), "The 2023 finding: ice keeps growing by pulling in water", "sansb", 22, INK, "la", ra)
        # ice lens with channels feeding it
        ga = ease((t - 29) / 1.5) * a
        cx, cy = bx + 170, by + 150
        cv.rect((bx + 40, by + 66, bx + 300, by + 250), mix(CREAM, SUBB, ga), r=6)
        cv.poly([(cx - 90, cy - 20), (cx + 90, cy - 20), (cx + 96, cy + 4), (cx - 96, cy + 4)], mix(CREAM, ICE, ga), outline=mix(CREAM, ICE2, ga), w=2)
        rnd = random.Random(2)
        for i in range(7):
            x = cx - 80 + i * 27; y0_ = cy + 4; y1_ = by + 242
            cv.line([(x, y1_), (x + rnd.uniform(-8, 8), (y0_ + y1_) / 2), (x, y0_)], mix(CREAM, WATER, ga), 3)
            ph = ((t * 1.2) + i * .13) % 1.0
            cv.circ((x + rnd.uniform(-3, 3), y1_ - (y1_ - y0_) * ph), 3.5, mix(CREAM, WATER, ga))
        for sgn in (-1, 1):
            cv.line([(cx, cy - 8), (cx, cy - 8 - 40 * (1 if sgn < 0 else 0))], mix(CREAM, RED, ga), 4) if sgn < 0 else None
        cv.poly([(cx - 8, cy - 48), (cx + 8, cy - 48), (cx, cy - 60)], mix(CREAM, RED, ga))
        cv.text((cx + 110, cy - 30), "ice lens grows", "sans", 19, INK, "la", ga)
        cv.text((cx + 110, cy + 40), "thin liquid channels keep feeding it", "sans", 19, WATER, "la", ga)
        cv.para(bx + 24, by + 268, "Same thing that heaves soil in frost. Fluids that shrink on freezing did the same damage in the experiments, so the volume change is not the main force.", "sans", 18, DIM, 480, 1.25, "l", ga)
    # source line
    return cv.im.reduce(SS)

def end_frame(t, dur):
    cv = Cv(); a = min(1.0, t / .8, (dur - t) / 1.2)
    cv.text((W / 2, 40), "Heartbeat Observatory", "serif", 56, INK, "ma", a)
    cv.text((W / 2, 112), "heartbeatobservatory.com", "sansb", 28, AMBER, "ma", a)
    cv.text((W / 2, 152), "Science  ·  Episode 8.4  ·  How a highway disappears", "sans", 21, DIM, "ma", a)
    cv.line([(W / 2 - 60, 188), (W / 2 + 60, 188)], mix(CREAM, AMBER, a), 3)
    cv.text((W / 2, 202), "A simulation. Every timing is an estimate drawn from these sources:", "sans", 19, DIM, "ma", a)
    src = [
        "Lacan, McBride & De Witt 2015 - Urban forest condition and succession in the abandoned city of Pripyat (Urban Forestry & Urban Greening)",
        "Heyne 2000 - Soil and vegetation recovery on abandoned paved roads in a humid tropical forest, Puerto Rico (UNLV thesis)",
        "Lutz 2022 - Vegetation on abandoned Highway 16 segments, 16-57 years, British Columbia (UNBC thesis)",
        "Gerber, Wilen, Dufresne & Style 2023 - Phys. Rev. Lett. 131, 208201: ice growth fed by liquid channels, not expansion, drives most freeze damage",
        "FHWA pavement preservation guidance; Asphalt Institute - asphalt design life about 20 years with maintenance",
        "AASHTO LRFD - 75-year bridge design life; rust volume 2-6x: Zhao et al. 2011 Corrosion Science; FHWA RD-98-088",
        "Proc. Indiana Academy of Science old-field succession papers; USFS FEIS / Silvics on sumac and cottonwood fire response; Weisman 2007 (general picture)",
    ]
    y = 240
    for i, s_ in enumerate(src):
        y = cv.para(W / 2, y, s_, "sans", 17, INK, 1120, 1.22, "m", ease((t - .6 - i * .18) / .6) * a) + 6
    cv.text((W / 2, 572), "Made by Claude Code on the MSI: Blender 5.1 (Cycles), Kokoro voice, Pillow, ffmpeg.  CC0.", "sansl", 17, DIM, "ma", a)
    return cv.im.reduce(SS)

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    f = 1
    for sh in SHOTS:
        n = int(round(sh["dur"] * FPS))
        if sh["cam"] is None:
            fn = diag_frame if sh["name"].startswith("diag") else end_frame
            for i in range(n):
                p = os.path.join(OUT, "f_%04d.png" % (f + i))
                if os.path.exists(p) and os.path.getsize(p) > 1000 and "--force" not in sys.argv: continue
                fn(i / FPS, sh["dur"]).save(p)
            print(sh["name"], f, f + n - 1, flush=True)
        f += n
