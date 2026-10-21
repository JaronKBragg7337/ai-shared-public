# The non-Blender passages, drawn with Pillow at 24 fps into the same frame numbering as the render:
#   "diag_orbit"   - Mars, Phobos and Deimos to scale in distance, one Mars day as a time-lapse; the synchronous line; why
#                    Phobos rises in the west.
#   "diag_grooves" - the two groove explanations (tidal stretch marks vs Stickney boulder tracks), labelled not settled.
#   "diag_origin"  - captured asteroid vs giant-impact debris, what fits and what does not, what a sample can tell.
#   "diag_mmx"     - the MMX mission timeline 2026 -> 2031.
#   "end_card"     - Heartbeat Observatory + the source list.
# Own look (cream paper, ink lines, one warm accent), same family as 8.4 / 8.5.   python diagram.py [FRAMES_DIR] [--force] [--only=name]
import math, os, sys, random
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shots import SHOTS, FPS
OUT = next((a for a in sys.argv[1:] if not a.startswith("--")), "C:/Users/lilli/Renders/phobos-ep6/frames")
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

# ---------------------------------------------------------------- one Mars day, to scale in distance
# Layout rule for every Pillow passage: nothing below y = 640. finish.py draws the captions in a dark band at y 644-720,
# so captions never sit on diagram text, source lines or the NOT SETTLED / PUBLISHED PLAN pills.
KM = 0.0100
MARS_DAY = 24.6597; T_PH = 7.6533; T_DE = 30.312
def orbit_frame(t, dur):
    cv = Cv(); a = min(1.0, t / .6, (dur - t) / 1.0)
    cv.header("One day on Mars, with its two moons", "Distances to scale (sizes are not): Mars R 3,390 km  ·  Phobos 9,376 km from the centre  ·  Deimos 23,460 km", a)
    cx, cy = 580, 385
    hours = ease(min(1, (t - 1.0) / (dur - 4.0))) * MARS_DAY * 1.0 if t > 1.0 else 0.0
    hours = min(hours, MARS_DAY)
    # synchronous line
    rs = 20428 * KM
    cv.dashed([(cx + rs * math.cos(2 * math.pi * i / 90), cy + rs * math.sin(2 * math.pi * i / 90)) for i in range(91)], mix(CREAM, AMBER, a), 2, 7, 7)
    cv.text((cx, cy - rs - 6), "synchronous orbit ~20,400 km (a moon here would hang over one spot)", "sansb", 14, AMBER, "md", a)
    # orbits
    rp = 9376 * KM; rd = 23460 * KM
    cv.ring((cx, cy), rp, mix(CREAM, RULE, a), 2); cv.ring((cx, cy), rd, mix(CREAM, RULE, a), 2)
    # Mars with a rotating surface marker
    cv.circ((cx, cy), 3390 * KM, mix(CREAM, MARS, a), mix(CREAM, MARSD, a), 2)
    th_m = -2 * math.pi * hours / MARS_DAY - math.pi / 2
    mx_, my_ = cx + 3390 * KM * math.cos(th_m), cy + 3390 * KM * math.sin(th_m)
    cv.circ((mx_, my_), 5, mix(CREAM, INK, a))
    cv.line([(cx, cy), (mx_, my_)], mix(CREAM, MARSD, a), 2)
    # moons (counter-clockwise = same sense as the spin, seen from above the north pole)
    th_p = -2 * math.pi * hours / T_PH - math.pi / 2; th_d = -2 * math.pi * hours / T_DE - math.pi / 2
    px, py = cx + rp * math.cos(th_p), cy + rp * math.sin(th_p); dx, dy = cx + rd * math.cos(th_d), cy + rd * math.sin(th_d)
    # clock + facts (drawn first; the moons and their labels go on top so nothing clips them)
    cv.rect((40, 150, 300, 330), mix(CREAM, PAPER, a), mix(CREAM, RULE, a), 2, 10)
    cv.text((60, 160), "Mars clock", "sansb", 16, DIM, "la", a)
    cv.text((60, 182), "%2d h %02d min" % (int(hours), int((hours % 1) * 60)), "serif", 40, INK, "la", a)
    cv.text((60, 236), "A Mars day (sol): 24 h 39 min", "sans", 15, INK, "la", a)
    cv.text((60, 258), "Phobos orbit: 7 h 39 min  (laps ~3x a sol)", "sans", 15, INK, "la", a)
    cv.text((60, 280), "Deimos orbit: 30 h 18 min", "sans", 15, INK, "la", a)
    laps = hours / T_PH
    cv.text((60, 304), "Phobos laps so far: %.1f" % laps, "sansb", 16, AMBER, "la", a)
    # inside / outside (left column, under the clock)
    cv.para(40, 420, "Inside the synchronous line, Phobos moves faster than Mars turns: the tidal bulge it raises trails behind it and pulls it back, so it spirals IN (~1.8 cm a year).", "sans", 14, INK, 265, 1.3, "l", a)
    cv.para(40, 535, "Deimos sits outside it, moves slower than Mars turns, and is slowly pushed OUT, like our Moon from Earth.", "sans", 14, INK, 265, 1.3, "l", a)
    # right panel: seen from the ground
    X0, Y0 = 880, 290
    cv.rect((X0, 150, 1240, 540), mix(CREAM, PAPER, a), mix(CREAM, RULE, a), 2, 10)
    cv.text((X0 + 180, 160), "From the ground on Mars", "sansb", 17, INK, "ma", a)
    hz = Y0 + 140
    cv.arc((X0 + 180, hz), 150, 180, 360, mix(CREAM, RULE, a), 2)
    cv.line([(X0 + 20, hz), (X0 + 340, hz)], mix(CREAM, INK, a), 3)
    cv.text((X0 + 22, hz + 8), "W", "sansb", 18, INK, "la", a); cv.text((X0 + 338, hz + 8), "E", "sansb", 18, INK, "ra", a)
    # Phobos crosses W -> E in ~4 h 15; a pass every ~11 h 06 (synodic); show two passes in the sol
    syn = 11.12
    for k in range(3):
        u = (hours - k * syn) / 4.25
        if 0 <= u <= 1:
            ang = math.pi + math.pi * u; qx, qy = X0 + 180 + 150 * math.cos(ang), hz + 150 * math.sin(ang)
            cv.potato((qx, qy), 9, MOON, MOOND, ang, a, 3)
    # the Sun crosses E -> W over the sol (rises ~6 h, sets ~18 h)
    us = (hours - 6.0) / 12.3
    if 0 <= us <= 1:
        ang = 2 * math.pi - math.pi * us; sx_, sy_ = X0 + 180 + 150 * math.cos(ang), hz + 150 * math.sin(ang)
        cv.circ((sx_, sy_), 9, mix(CREAM, AMBER, a))
    cv.text((X0 + 180, hz + 32), "Phobos rises in the WEST and crosses in ~4 h 15 min;", "sans", 14, INK, "ma", a)
    cv.text((X0 + 180, hz + 52), "the Sun and Deimos rise in the east, like at home.", "sans", 14, INK, "ma", a)
    cv.text((X0 + 180, hz + 80), "Source: NASA Science (Phobos), ESA Mars Express;", "sansl", 12, DIM, "ma", a)
    cv.text((X0 + 180, hz + 96), "orbital periods from NASA/JPL.", "sansl", 12, DIM, "ma", a)
    cv.tag(170, 362, "TIME-LAPSE", a, 150)
    cv.text((170, 384), "one sol in %d seconds" % int(dur - 4), "sans", 13, DIM, "ma", a)
    # the moons last, on top of everything (Deimos' label used to be covered by the right panel)
    cv.potato((px, py), 11, MOON, MOOND, th_p, a, 3); cv.potato((dx, dy), 7, MOON, MOOND, th_d, a, 5)
    cv.text((px + 16, py - 9), "Phobos", "sansb", 15, INK, "la", a)
    cv.text((dx + 12, dy - 9) if dx < cx else (dx - 12, dy - 9), "Deimos", "sansb", 15, INK, "la" if dx < cx else "ra", a)
    return cv.im.reduce(SS)

# ---------------------------------------------------------------- the grooves: two explanations
def grooves_frame(t, dur):
    cv = Cv(); a = min(1.0, t / .6, (dur - t) / 1.0)
    cv.header("What cut the grooves?", "Two published explanations. Each fits many of the grooves; neither is accepted as the whole answer.", a)
    for k, (x0, title, who) in enumerate(((60, "1. Stretch marks from Mars' pull", "Hurford et al. 2016, J. Geophys. Res. Planets"), (660, "2. Boulder tracks from the Stickney impact", "Ramsley & Head 2018, Planetary and Space Science"))):
        u = ease((t - .4 - k * .5) / .8) * a
        cv.rect((x0, 140, x0 + 560, 528), mix(CREAM, PAPER, u), mix(CREAM, RULE, u), 2, 12)
        cv.text((x0 + 280, 152), title, "sansb", 20, INK, "ma", u)
        cv.text((x0 + 280, 180), who, "sansl", 14, DIM, "ma", u)
        cx, cy = x0 + 280, 305
        if k == 0:
            # Phobos stretched along the Mars direction; grooves follow the stress lines
            s_ = ease((t - 2.0) / 3.0)
            cv.potato((cx, cy), 80 + 10 * s_, MOON, MOOND, 0, u, 3, 3)
            for i in range(-3, 4):
                yy = cy + i * 22
                cv.line([(cx - 85 + abs(i) * 6, yy), (cx + 85 - abs(i) * 6, yy)], mix(CREAM, MOOND, u * (.4 + .6 * s_)), 2)
            cv.arrow((cx - 150, cy), (cx - 110, cy), mix(CREAM, RED, u), 3); cv.arrow((cx + 150, cy), (cx + 110, cy), mix(CREAM, RED, u), 3)
            cv.text((cx - 180, cy - 10), "Mars", "sansb", 15, RED, "ra", u); cv.text((cx + 180, cy - 10), "away", "sansb", 15, RED, "la", u)
            cv.para(x0 + 30, 410, "Mars pulls harder on the near side than the far side. The model: a weak, rubbly inside under a stiffer skin; most grooves line up with the computed stress, so they would be the first cracks of a moon starting to come apart.", "sans", 15, INK, 500, 1.3, "l", u)
        else:
            # Stickney with boulder tracks radiating and wrapping
            cv.potato((cx, cy), 85, MOON, MOOND, 0, u, 3, 3)
            cv.circ((cx - 55, cy - 10), 26, mix(CREAM, MOOND, u), mix(CREAM, INK, u), 2)
            cv.text((cx - 55, cy - 60), "Stickney", "sansb", 14, INK, "ma", u)
            s_ = ease((t - 2.0) / 4.0)
            for i, ang in enumerate((-.5, -.2, .1, .4, .7, -.85)):
                L_ = (60 + 25 * i) * s_
                pts = [(cx - 55 + 28 * math.cos(ang) + L_ * uu * math.cos(ang + .3 * uu), cy - 10 + 28 * math.sin(ang) + L_ * uu * math.sin(ang + .3 * uu) * .8) for uu in [j / 12 for j in range(13)]]
                cv.dashed(pts, mix(CREAM, MOOND, u), 2, 5, 4)
                if s_ > 0: cv.circ(pts[-1], 4, mix(CREAM, INK, u))
            cv.para(x0 + 30, 410, "The impact that dug Stickney (about 9 km across) threw out boulders. In gravity this weak they rolled for kilometres, some all the way round the moon, crossing their own tracks. The model reproduces most of the groove families and the groove-free zone.", "sans", 15, INK, 500, 1.3, "l", u)
    u2 = ease((t - 3.5) / .8) * a
    cv.para(W / 2, 544, "Nayak & Asphaug 2016 (Nature Communications) found young grooves that cut across the tidal pattern and proposed a third source: debris knocked off Phobos that briefly orbits Mars and falls back as chains of pits. Grooves measure about 100-200 m wide, under ~30 m deep, up to ~20 km long (NASA, ESA Mars Express). In the 3D scenes they are drawn deeper than real, so they read on screen.", "sans", 14, INK, 1120, 1.3, "m", u2)
    cv.tag(W / 2, 618, "NOT SETTLED", u2, 160, RED)
    return cv.im.reduce(SS)

# ---------------------------------------------------------------- the origin question
def origin_frame(t, dur):
    cv = Cv(); a = min(1.0, t / .6, (dur - t) / 1.0)
    cv.header("Where did Phobos come from?", "Two leading ideas; the orbits argue with the colour. A sample is the planned tie-breaker.", a)
    for k, (x0, title) in enumerate(((60, "Captured asteroid"), (660, "Debris from a giant impact on Mars"))):
        u = ease((t - .4 - k * .5) / .8) * a
        cv.rect((x0, 140, x0 + 560, 498), mix(CREAM, PAPER, u), mix(CREAM, RULE, u), 2, 12)
        cv.text((x0 + 280, 152), title, "sansb", 21, INK, "ma", u)
        cx, cy = x0 + 280, 272
        s_ = ease((t - 1.5) / 4.0)
        if k == 0:
            cv.circ((cx - 120, cy), 42, mix(CREAM, MARS, u), mix(CREAM, MARSD, u), 2)
            # an asteroid arriving on a stretched, tilted path
            pts = [(cx + 230 - 300 * uu, cy + 90 - 170 * uu + 120 * uu * uu) for uu in [j / 20 for j in range(21)]]
            cv.dashed(pts, mix(CREAM, MOOND, u), 2, 6, 5)
            idx = int(20 * s_); cv.potato(pts[idx], 12, MOON, MOOND, 0.5, u, 3)
            cv.text((cx + 120, cy - 95), "tilted, stretched path", "sans", 13, DIM, "ma", u)
            cv.para(x0 + 30, 340, "Fits: Phobos is dark and reddish, with a spectrum like D-type asteroids from the outer asteroid belt.", "sans", 15, INK, 500, 1.3, "l", u)
            cv.para(x0 + 30, 398, "Problem: a captured body should keep a tilted, stretched orbit. Phobos and Deimos ride near-circular orbits right over Mars' equator, and no capture model has reproduced that well.", "sans", 15, RED, 500, 1.3, "l", u)
        else:
            cv.circ((cx - 60, cy), 42, mix(CREAM, MARS, u), mix(CREAM, MARSD, u), 2)
            # a splash and a flat debris disk in the equator plane, with two small moons condensing
            for i in range(8):
                ang = -.6 + .15 * i; L_ = (30 + 50 * s_)
                cv.line([(cx - 60 + 42 * math.cos(ang), cy + 42 * math.sin(ang)), (cx - 60 + (42 + L_) * math.cos(ang), cy + (42 + L_) * math.sin(ang))], mix(CREAM, AMBER, u * (1 - s_ * .7)), 2)
            if s_ > .3:
                v = ease((s_ - .3) / .7)
                cv.d.ellipse([(cx - 60 - 150 * v) * SS, (cy - 9) * SS, (cx - 60 + 150 * v) * SS, (cy + 9) * SS], outline=mix(CREAM, MOOND, u * v), width=2 * SS)
                cv.potato((cx - 60 + 95 * v, cy - 4), 10 * v, MOON, MOOND, 0, u * v, 3); cv.potato((cx - 60 - 140 * v, cy + 2), 7 * v, MOON, MOOND, 0, u * v, 5)
            cv.text((cx + 70, cy - 95), "a flat disk in the equator plane", "sans", 13, DIM, "ma", u)
            cv.para(x0 + 30, 340, "Fits: circular, equatorial orbits for both moons; low density and a porous, loosely packed interior; a 2025 review (Paetzold et al., Space Science Reviews) leans toward accretion from a debris disk, whatever fed the disk.", "sans", 15, INK, 500, 1.3, "l", u)
            cv.para(x0 + 30, 420, "Problem: impact debris is heated, so it should be poor in water and other volatiles, yet Phobos looks like a volatile-rich asteroid type.", "sans", 15, RED, 500, 1.3, "l", u)
    u2 = ease((t - 3.5) / .8) * a
    cv.rect((60, 510, 1220, 592), mix(CREAM, (236, 220, 190), u2), mix(CREAM, AMBER, u2), 2, 10)
    cv.text((80, 518), "What ten grams can tell", "sansb", 16, AMBER, "la", u2)
    cv.para(80, 541, "Water and volatiles (captured material should keep more; impact debris was heated and should hold less) · isotope ratios (oxygen, chromium, titanium and more: asteroid-like or Mars-like) · ages of the grains (when they formed and were altered).", "sans", 14, INK, 1120, 1.3, "l", u2)
    cv.tag(W / 2 - 300, 618, "NOT SETTLED", u2, 160, RED)
    cv.text((W / 2 + 60, 611), "Sources: JAXA MMX science goals; Paetzold et al. 2025; Canup & Salmon 2018 (Science Advances); Hyodo et al. 2017.", "sansl", 12, DIM, "ma", u2)
    return cv.im.reduce(SS)

# ---------------------------------------------------------------- MMX timeline
def mmx_frame(t, dur):
    cv = Cv(); a = min(1.0, t / .6, (dur - t) / 1.0)
    cv.header("MMX: the Martian Moons eXploration mission", "JAXA, with NASA, CNES (France), DLR (Germany) and ESA. Dates are the published plan and can slip.", a)
    y = 312; x0, x1 = 90, 1190
    cv.line([(x0, y), (x1, y)], mix(CREAM, RULE, a), 4)
    steps = [
        (2026.8, "Oct 20, 2026", "Launch", "H3 rocket, flight 10, Tanegashima, 04:41 JST (Oct 19, 19:41 UTC). Launch window reserved to Nov 7."),
        (2027.7, "2027", "Arrive at Mars", "About a year's cruise, then into orbit around Mars."),
        (2028.3, "2027-2030", "Around Phobos", "Three years in a quasi-satellite orbit of Phobos: mapping, gravity, flybys of Deimos."),
        (2029.3, "2029", "Idefix rover", "A ~25 kg CNES/DLR rover dropped from ~40 m; about 100 days on the surface."),
        (2029.9, "2030", "Land and sample", "The spacecraft itself touches down and collects at least 10 g (CNES lists two sampling sites; JAXA's current flow shows one)."),
        (2031.5, "2031", "Back on Earth", "The capsule lands in the Australian desert (plan: July 2031)."),
    ]
    def X(yr): return x0 + (x1 - x0) * (yr - 2026.5) / (2032.0 - 2026.5)
    for i, (yr, when, what, detail) in enumerate(steps):
        u = ease((t - 1.0 - i * .9) / .7) * a
        xx = X(yr); up = i % 2 == 0
        cv.circ((xx, y), 9, mix(CREAM, AMBER, u), mix(CREAM, CREAM, u), 0)
        yy = y - 152 if up else y + 36
        cv.line([(xx, y - 12 if up else y + 12), (xx, yy + 110 if up else yy)], mix(CREAM, RULE, u), 2)
        cv.text((xx, yy), when, "sansb", 15, AMBER, "ma", u)
        cv.text((xx, yy + 20), what, "serif", 22, INK, "ma", u)
        cv.para(xx, yy + 50, detail, "sans", 13, DIM, 180, 1.25, "m", u)
    # little icons: rocket, Mars, Phobos, rover, capsule
    u = a
    cv.text((W / 2, 520), "The sample would be the first material returned from the Martian system, and the first from a moon of another planet.", "sans", 16, INK, "ma", ease((t - 6.5) / .8) * a)
    cv.text((W / 2, 553), "Launch time and plan: JAXA press release Aug 20, 2026; ESA (Oct 2026); DLR (Sep 1, 2026); CNES MMX project page. Checked Oct 14, 2026.", "sansl", 13, DIM, "ma", ease((t - 7.0) / .8) * a)
    cv.tag(W / 2, 608, "PUBLISHED PLAN", ease((t - 7.0) / .8) * a, 170)
    return cv.im.reduce(SS)

def end_frame(t, dur):
    cv = Cv(); a = min(1.0, t / .8, (dur - t) / 1.2)
    cv.text((W / 2, 30), "Heartbeat Observatory", "serif", 50, INK, "ma", a)
    cv.text((W / 2, 96), "heartbeatobservatory.com", "sansb", 26, AMBER, "ma", a)
    cv.text((W / 2, 132), "Science  ·  Episode 8.6  ·  Phobos: the moon that's falling", "sans", 19, DIM, "ma", a)
    cv.line([(W / 2 - 60, 164), (W / 2 + 60, 164)], mix(CREAM, AMBER, a), 3)
    cv.text((W / 2, 174), "The 3D scenes are a simulation built from published numbers; the spiral-in and ring are a model. Sources:", "sans", 17, DIM, "ma", a)
    # one line per source, large enough to read at 720p without pausing (the long citations live in SOURCES.md)
    src = [
        "NASA Science, Phobos and Deimos pages: size, 6,000 km / 7 h 39 min orbit, rises in the west, 1.8 m closer per century, ring or impact in ~50 Myr",
        "ESA Mars Express, Phobos: grooves 100-200 m wide, under 30 m deep",
        "Black & Mittal 2015, Nature Geoscience: break-up into a ring in ~20-40 Myr  ·  Hesselbrock & Minton 2017, Nature Geoscience: ring-moon cycle, ~70 Myr",
        "Grooves: Hurford et al. 2016, J. Geophys. Res. Planets  ·  Ramsley & Head 2018, Planetary and Space Science  ·  Nayak & Asphaug 2016, Nature Communications",
        "Origin: Paetzold et al. 2025, Space Science Reviews  ·  Canup & Salmon 2018, Science Advances  ·  Hyodo et al. 2017  ·  JAXA MMX science goals",
        "MMX plan: JAXA press release Aug 20, 2026 (launch Oct 20, 2026 JST, H3 F10)  ·  ESA, DLR (Idefix), CNES (return 2031)  ·  checked Oct 14, 2026",
    ]
    y = 208
    for i, s_ in enumerate(src):
        y = cv.para(W / 2, y, s_, "sans", 17, INK, 1180, 1.25, "m", ease((t - .6 - i * .2) / .6) * a) + 7
    u = ease((t - 2.2) / .6) * a
    cv.rect((W / 2 - 440, 498, W / 2 + 440, 566), mix(CREAM, PAPER, u), mix(CREAM, RULE, u), 2, 10)
    cv.text((W / 2, 508), "A Phobos you can walk on is in The Cosmos, the free browser game on the site: real terrain, low gravity, Mars in the sky.", "sans", 16, INK, "ma", u)
    cv.text((W / 2, 534), "heartbeatobservatory.com  ·  Games  ·  The Cosmos", "sansb", 16, AMBER, "ma", u)
    cv.text((W / 2, 598), "Made by Claude Code on the MSI: Blender 5.1 (Cycles), Kokoro voice, Pillow, ffmpeg.  CC0.  Fact-checked by Codex with web search.", "sans", 15, INK, "ma", a)
    return cv.im.reduce(SS)

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    f = 1
    for sh in SHOTS:
        n = int(round(sh["dur"] * FPS))
        if sh["cam"] is None:
            fn = {"diag_orbit": orbit_frame, "diag_grooves": grooves_frame, "diag_origin": origin_frame, "diag_mmx": mmx_frame}.get(sh["name"], end_frame)
            only = [a for a in sys.argv[1:] if a.startswith("--only=")]
            if only and sh["name"] not in only[0]: f += n; continue
            for i in range(n):
                p = os.path.join(OUT, "f_%04d.png" % (f + i))
                if os.path.exists(p) and os.path.getsize(p) > 1000 and "--force" not in sys.argv: continue
                fn(i / FPS, sh["dur"]).save(p)
            print(sh["name"], f, f + n - 1, flush=True)
        f += n
