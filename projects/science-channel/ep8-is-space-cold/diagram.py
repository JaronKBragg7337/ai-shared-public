# Pillow boards for Science 8.8 Is space cold? (cream-paper look, same family as ep6).  python diagram.py [FRAMES_DIR] [--force] [--only=name] [--preview]
import math, os, sys, random
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shots import SHOTS, FPS
OUT = next((a for a in sys.argv[1:] if not a.startswith("--")), "C:/Users/lilli/Renders/space-cold-ep8/frames")
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



# ======================================================================== ep8 boards (Science 8.8, Is space cold?)
# Layout rule (same as ep6/ep7): nothing below y = 640; finish.py shrinks each board into the top of the frame and puts the
# captions in a dark band under it.  No em or en dashes anywhere on screen.
HOT = (200, 80, 40); COOL = (62, 110, 170); GREEN = (70, 130, 80); STEEL = (150, 150, 156)
def fade(t, dur, a_in=.6, a_out=1.0): return max(0.0, min(1.0, t / a_in, (dur - t) / a_out))
def ap(t, t0, d=.7): return ease((t - t0) / d)
def src_line(cv, y, text, a): cv.text((W / 2, y), text, "sansl", 13, DIM, "ma", a)
def panel(cv, b, u): cv.rect(b, mix(CREAM, PAPER, u), mix(CREAM, RULE, u), 2, 10)
def pill(cv, cx, cy, t, u, col=RED, wdt=None):
    wdt = wdt or (font("sansb", 15).getlength(t) / SS + 30)
    cv.rect((cx - wdt / 2, cy - 15, cx + wdt / 2, cy + 15), mix(CREAM, (246, 228, 214), u), outline=mix(CREAM, col, u), w=2, r=14)
    cv.text((cx, cy - 10), t, "sansb", 15, col, "ma", u)

def three_frame(t, dur):
    cv = Cv(); a = fade(t, dur)
    cv.header("Three ways heat leaves", "On Earth a hot thing uses all three. In the near vacuum of space, mostly one is left.", a)
    cols = [(1.0, "Touch", "conduction", "Heat flows into whatever cooler thing it touches."),
            (2.5, "Flow", "convection", "Air or water moves past and carries the heat away."),
            (4.0, "Glow", "radiation", "Every warm thing gives off infrared light, even in a vacuum.")]
    for i, (t0, big, word, txt) in enumerate(cols):
        u = ap(t, t0) * a; x0 = 60 + i * 395; cx = x0 + 180
        panel(cv, (x0, 140, x0 + 360, 420), u)
        cv.text((cx, 152), big, "serif", 30, INK, "ma", u); cv.text((cx, 192), word, "sansl", 15, DIM, "ma", u)
        cv.circ((cx, 285), 34, mix(CREAM, HOT, u))
        if i == 0:
            cv.rect((cx + 34, 266, cx + 140, 304), mix(CREAM, STEEL, u)); cv.arrow((cx + 40, 285), (cx + 120, 285), mix(CREAM, HOT, u), 3)
        elif i == 1:
            for k in range(3):
                yy = 245 + k * 40; cv.arrow((cx - 140, yy), (cx + 140, yy - 10), mix(CREAM, COOL, u * .8), 2)
        else:
            for k in range(10):
                ang = k * 2 * math.pi / 10; r0, r1 = 44, 44 + 20 + 8 * (k % 2)
                cv.dashed([(cx + r0 * math.cos(ang), 285 + r0 * math.sin(ang)), (cx + r1 * math.cos(ang), 285 + r1 * math.sin(ang))], mix(CREAM, AMBER, u), 2, 5, 4)
        cv.para(x0 + 20, 345, txt, "sans", 16, INK, 320, 1.25, "l", u)
    u = ap(t, 12.0) * a
    for i in (0, 1):
        x0 = 60 + i * 395; cv.line([(x0 + 110, 225), (x0 + 250, 335)], mix(CREAM, RED, u), 5)
    cv.text((60, 432), "In space: almost nothing to touch, nothing to flow. Across the emptiness, heat travels by the glow.", "sansb", 16, RED, "la", u)
    cv.text((60, 456), "Some systems also carry heat away by releasing material.", "sans", 15, INK, "la", u)
    u = ap(t, 21.0) * a
    panel(cv, (60, 486, 1220, 590), u)
    cv.rect((96, 498, 150, 580), mix(CREAM, STEEL, u), mix(CREAM, INK, u), 2, 8); cv.rect((106, 506, 140, 572), CREAM, mix(CREAM, DIM, u), 1, 6)
    cv.rect((112, 512, 134, 566), mix(CREAM, (110, 70, 40), u), None, 1, 4)
    cv.text((182, 500), "A thermos works the same way", "serif", 22, INK, "la", u)
    cv.para(182, 532, "A layer of vacuum between two walls slows touch and flow, so the coffee stays hot.", "sans", 17, INK, 1000, 1.3, "l", u)
    src_line(cv, 610, "Textbook heat transfer. Space is not perfectly empty, but far too thin to carry much heat by touch or flow.", ap(t, 22) * a)
    return cv.im.reduce(SS)

def law_frame(t, dur):
    cv = Cv(); a = fade(t, dur)
    cv.header("How fast a glow carries heat", "Stefan-Boltzmann law: power = area x σ x T⁴   (T counted from absolute zero, in kelvin)", a)
    X0, X1, Y0, Y1 = 110, 640, 560, 160
    cv.line([(X0, Y0), (X1, Y0)], mix(CREAM, INK, a), 2); cv.line([(X0, Y0), (X0, Y1)], mix(CREAM, INK, a), 2)
    def px(T): return X0 + (X1 - X0) * T / 700.0
    def py(P): return Y0 - (Y0 - Y1) * P / 10000.0
    for T in (0, 100, 200, 300, 400, 500, 600, 700):
        cv.text((px(T), Y0 + 8), "%d K" % T, "sans", 14, DIM, "ma", a)
    for P in (0, 2500, 5000, 7500, 10000):
        cv.text((X0 - 8, py(P) - 9), "{:,} W".format(P), "sans", 14, DIM, "ra", a)
    cv.text((X0 + 10, Y1 - 4), "glow per square metre (perfect dark surface)", "sansl", 13, DIM, "la", a)
    u = ap(t, .8, 3.0) * a
    pts = [(px(T), py(5.670e-8 * T ** 4)) for T in range(0, int(650 * min(1, max(0.0001, u))) + 1, 5) if 5.670e-8 * T ** 4 <= 10000]
    if len(pts) > 1: cv.line(pts, mix(CREAM, HOT, a), 4)
    u2 = ap(t, 1.0) * a
    for T, lab, anc, dx, dy in ((300, "300 K, room temperature: ~460 W", "la", 16, -34), (600, "600 K: 16 times as much, ~7,300 W", "ra", -14, -10)):
        P = 5.670e-8 * T ** 4; cv.circ((px(T), py(P)), 6, mix(CREAM, INK, u2))
        cv.text((px(T) + dx, py(P) + dy), lab, "sansb", 15, INK, anc, u2)
    u3 = ap(t, 4.5) * a
    panel(cv, (700, 160, 1220, 360), u3)
    cv.text((720, 172), "Double T, 16 times the glow", "serif", 24, INK, "la", u3)
    cv.para(720, 210, "2 x 2 x 2 x 2 = 16. Very hot things shed heat fast by glowing.", "sans", 17, INK, 480, 1.3, "l", u3)
    cv.para(720, 268, "At everyday temperatures the numbers are small: about 460 W per square metre at room temperature.", "sans", 16, INK, 480, 1.3, "l", u3)
    u4 = ap(t, 11.5) * a
    panel(cv, (700, 380, 1220, 560), u4)
    cv.text((720, 392), "So: big radiators, shielded from sunlight", "serif", 22, INK, "la", u4)
    cv.para(720, 428, "Spacecraft with a lot of heat often need large radiator surfaces, shielded from sunlight.", "sans", 17, INK, 480, 1.3, "l", u4)
    src_line(cv, 604, "σ = 5.67 x 10⁻⁸ W per m² per K⁴.  460 W/m² = one face, a perfect emitter, at 300 K (our arithmetic).  Real surfaces glow a little less.", ap(t, 11.5) * a)
    return cv.im.reduce(SS)

def suit_frame(t, dur):
    cv = Cv(); a = fade(t, dur)
    cv.header("A spacesuit has the same problem", "Your body is a heater. The suit traps much of the heat, so astronauts need a cooling system.", a)
    stats = [(.8, "~70 W", "body heat, resting"), (2.5, "700+ W", "working hard")]
    for i, (t0, big, lab) in enumerate(stats):
        u = ap(t, t0) * a; x0 = 60 + i * 300
        panel(cv, (x0, 140, x0 + 280, 260), u)
        cv.text((x0 + 140, 152), big, "serif", 40, HOT, "ma", u); cv.text((x0 + 140, 214), lab, "sans", 17, INK, "ma", u)
    u = ap(t, 8.0) * a
    panel(cv, (60, 280, 1220, 590), u)
    gx, gy = 150, 310
    cv.rect((gx, gy, gx + 180, gy + 210), mix(CREAM, (230, 232, 236), u), mix(CREAM, INK, u), 2, 30)
    for k in range(8):
        yy = gy + 22 + k * 22
        cv.line([(gx + 20, yy), (gx + 160, yy)], mix(CREAM, COOL, u), 3)
    cv.text((gx + 90, gy + 218), "cooling underwear", "sansb", 15, INK, "ma", u)
    cv.text((gx + 90, gy + 238), "(thin tubes of cool water)", "sansl", 13, DIM, "ma", u)
    u2 = ap(t, 14.0) * a
    bx = 560
    cv.rect((bx, gy + 20, bx + 220, gy + 190), mix(CREAM, (220, 214, 200), u2), mix(CREAM, INK, u2), 2, 12)
    cv.text((bx + 110, gy + 34), "backpack", "sansb", 16, INK, "ma", u2)
    cv.rect((bx + 30, gy + 72, bx + 190, gy + 170), mix(CREAM, (238, 244, 250), u2), mix(CREAM, COOL, u2), 2, 8)
    cv.text((bx + 110, gy + 82), "sublimator", "sansb", 16, COOL, "ma", u2)
    cv.para(bx + 110, gy + 108, "water freezes, then turns straight into vapour", "sans", 13, INK, 150, 1.2, "m", u2)
    cv.arrow((gx + 182, gy + 80), (bx - 6, gy + 80), mix(CREAM, HOT, u2), 3); cv.text(((gx + bx) / 2 + 90, gy + 54), "warm water", "sans", 14, HOT, "ma", u2)
    cv.arrow((bx - 6, gy + 150), (gx + 182, gy + 150), mix(CREAM, COOL, u2), 3); cv.text(((gx + bx) / 2 + 90, gy + 156), "cooled water", "sans", 14, COOL, "ma", u2)
    u3 = ap(t, 19.0) * a
    for k in range(6):
        yy = gy + 70 + k * 16; cv.dashed([(bx + 224, yy), (bx + 300 + 10 * (k % 2), yy - 20)], mix(CREAM, DIM, u3), 2, 5, 5)
    cv.text((bx + 310, gy + 60), "vapour leaves", "sansb", 15, DIM, "la", u3); cv.text((bx + 310, gy + 80), "into space,", "sans", 15, DIM, "la", u3); cv.text((bx + 310, gy + 100), "taking the heat", "sans", 15, DIM, "la", u3)
    u4 = ap(t, 24.5) * a
    cv.rect((1000, gy + 10, 1200, gy + 200), mix(CREAM, (236, 220, 190), u4), mix(CREAM, AMBER, u4), 2, 10)
    cv.text((1100, gy + 30), "~3.5 kg", "serif", 36, AMBER, "ma", u4)
    cv.para(1100, gy + 86, "of water used on one spacewalk", "sans", 16, INK, 170, 1.25, "m", u4)
    cv.text((640, 560), "Schematic, not a real suit diagram.", "sansl", 13, DIM, "ma", u)
    src_line(cv, 610, "Source: NASA (suit heat loads about 70 to 730 W; liquid cooling and ventilation garment; sublimator; about 3.6 kg of water per spacewalk).", u4)
    return cv.im.reduce(SS)

def orbitdc_frame(t, dur):
    cv = Cv(); a = fade(t, dur)
    cv.header("Data centers in orbit: who says what", "AI chips turn nearly all their power into heat. These are the companies' own claims and filings.", a)
    rows = [(.3, "Google  ·  research project Suncatcher", "Says solar panels in the right orbit can be up to 8 times more productive.", "GOOGLE'S CLAIM"),
            (3.5, "Starcloud, a startup  ·  2025", "Flew one Nvidia chip and says it trained a small AI model in orbit.", "COMPANY-REPORTED"),
            (11.5, "SpaceX  ·  2026", "Asked permission for up to one million data center satellites.", "A REQUEST, NOT BUILT"),
            (17.0, "Blue Origin  ·  2026", "Filed for more than fifty thousand.", "A REQUEST, NOT BUILT")]
    for i, (t0, title, txt, tag) in enumerate(rows):
        u = ap(t, t0) * a; y = 140 + i * 112
        panel(cv, (60, y, 1220, y + 100), u)
        cv.text((84, y + 12), title, "serif", 22, INK, "la", u)
        cv.para(84, y + 52, txt, "sans", 17, INK, 820, 1.25, "l", u)
        pill(cv, 1080, y + 30, tag, u, RED if "NOT" in tag else AMBER, 250)
    src_line(cv, 604, "Sources: Google Research (Suncatcher, Nov 2025); Starcloud and Nvidia (2025); FCC filings reported Jan and Mar 2026.", ap(t, 17.5) * a)
    return cv.im.reduce(SS)

def radiator_frame(t, dur):
    cv = Cv(); a = fade(t, dur)
    cv.header("The catch is the heat", "Two published estimates. Different assumptions, so they are not one number.", a)
    u = ap(t, 1.0) * a
    panel(cv, (60, 140, 630, 470), u)
    cv.text((84, 152), "~1,600 m²", "serif", 44, AMBER, "la", u)
    cv.para(84, 214, "of radiator for every megawatt of computing, for a radiator around 20 °C.", "sans", 18, INK, 520, 1.3, "l", u)
    s = 150; cv.rect((84, 290, 84 + s, 290 + s), mix(CREAM, (238, 238, 236), u), mix(CREAM, INK, u), 2)
    cv.text((84 + s + 14, 300), "40 m x 40 m", "sansb", 16, INK, "la", u); cv.para(84 + s + 14, 326, "a square this size, per megawatt", "sans", 15, DIM, 300, 1.2, "l", u)
    cv.text((84, 446), "One World Economic Forum analysis, 2026", "sansl", 13, DIM, "la", u)
    u2 = ap(t, 12.5) * a
    panel(cv, (650, 140, 1220, 470), u2)
    cv.text((674, 152), "~1.4 m²", "serif", 44, AMBER, "la", u2)
    cv.para(674, 214, "for one 700-watt AI chip, at 60 °C.", "sans", 18, INK, 520, 1.3, "l", u2)
    cv.rect((674, 290, 674 + 118, 290 + 118), mix(CREAM, (238, 238, 236), u2), mix(CREAM, INK, u2), 2)
    cv.text((806, 300), "1.2 m x 1.2 m", "sansb", 16, INK, "la", u2)
    cv.text((674, 446), "IEEE Spectrum estimate", "sansl", 13, DIM, "la", u2)
    u3 = ap(t, 18.5) * a
    panel(cv, (60, 488, 1220, 590), u3)
    cv.para(84, 500, "Radiators are heavy, and must survive sunlight and tiny debris for years with no repair crew. One startup's chief executive admitted the economics of launch don't quite work yet.", "sans", 17, INK, 1110, 1.3, "l", u3)
    src_line(cv, 610, "Sources: World Economic Forum (2026); IEEE Spectrum; The Register (April 2026).", u3)
    return cv.im.reduce(SS)

def debate_frame(t, dur):
    cv = Cv(); a = fade(t, dur)
    cv.header("The other side of the debate", "Supporters answer that this is engineering, not a wall.", a)
    u = ap(t, 1.0) * a
    panel(cv, (60, 140, 630, 440), u)
    cv.text((84, 152), "In one independent model", "serif", 22, INK, "la", u)
    cv.rect((84, 210, 604, 254), mix(CREAM, (214, 206, 190), u), mix(CREAM, INK, u), 2)
    cv.rect((84, 210, 84 + 520 * .14, 254), mix(CREAM, COOL, u))
    cv.text((84 + 520 * .14 + 10, 220), "radiators ~14% of the weight", "sansb", 16, INK, "la", u)
    cv.para(84, 280, "The same study said launch cost matters far more.", "sans", 18, INK, 520, 1.3, "l", u)
    cv.text((84, 410), "Forethought cost model", "sansl", 13, DIM, "la", u)
    u2 = ap(t, 12.5) * a
    panel(cv, (650, 140, 1220, 440), u2)
    cv.text((674, 152), "Google's tests", "serif", 22, INK, "la", u2)
    cv.text((674, 196), "Oct 2026", "serif", 44, AMBER, "la", u2)
    cv.para(674, 252, "Google and Planet launched one test satellite.", "sans", 18, INK, 520, 1.3, "l", u2)
    cv.text((674, 312), "2027", "serif", 44, AMBER, "la", u2)
    cv.para(674, 368, "Two more planned. A plan, not yet a launch.", "sans", 18, INK, 520, 1.3, "l", u2)
    u3 = ap(t, 20.5) * a
    panel(cv, (60, 460, 1220, 580), u3)
    pill(cv, 200, 520, "NOT ESTABLISHED", u3, RED, 220)
    cv.para(330, 500, "Whether computing in space will ever beat computing on the ground.", "serif", 22, INK, 870, 1.3, "l", u3)
    src_line(cv, 604, "Sources: Forethought (space data center cost model); Google Research and Planet (Suncatcher); NPR/GPB and TechCrunch, Oct 2026.", u3)
    return cv.im.reduce(SS)

def end_frame(t, dur):
    cv = Cv(); a = fade(t, dur, .8, 1.2)
    cv.text((W / 2, 22), "Heartbeat Observatory", "serif", 46, INK, "ma", a)
    cv.text((W / 2, 82), "heartbeatobservatory.com", "sansb", 24, AMBER, "ma", a)
    cv.text((W / 2, 116), "Science  ·  Episode 8.8  ·  Is space cold?", "sans", 18, DIM, "ma", a)
    cv.line([(W / 2 - 60, 146), (W / 2 + 60, 146)], mix(CREAM, AMBER, a), 3)
    cv.text((W / 2, 154), "The 3D scenes are illustrations built in Blender: a generic station and a generic satellite, not real spacecraft or footage.", "sans", 15, DIM, "ma", a)
    src = [
        "Cosmic background ~2.7 K: NASA  ·  Heat transfer and the Stefan-Boltzmann law: standard physics",
        "ISS radiators (six, ~23 m, ammonia, ~70 kW design): NASA; Boeing and Lockheed Martin (2002); NASA NTRS 20000032541; SAE 981731",
        "Spacesuit heat and water: NASA (liquid cooling garment, sublimator, ~3.6 kg of water per spacewalk)",
        "Orbit data centers: Google Research and Planet (Suncatcher, Nov 2025; test satellite Oct 2026)  ·  Starcloud and Nvidia (2025)  ·  FCC filings (2026)",
        "Radiator sizes: World Economic Forum (2026); IEEE Spectrum  ·  Launch economics: The Register (Apr 2026)  ·  Forethought",
    ]
    y = 182
    for i, s_ in enumerate(src):
        y = cv.para(W / 2, y, s_, "sans", 15, INK, 1200, 1.22, "m", ease((t - .5 - i * .2) / .6) * a) + 5
    u = ease((t - 2.0) / .6) * a
    panel(cv, (70, 370, 1210, 520), u)
    cv.text((W / 2, 382), "Still open (labelled in the episode)", "sansb", 17, RED, "ma", u)
    opens = [("NOT ESTABLISHED", "whether computing in space will ever beat computing on the ground"),
             ("COMPANY-REPORTED", "Starcloud's small AI model trained in orbit"),
             ("REQUESTS, NOT BUILT", "SpaceX's one million and Blue Origin's fifty thousand satellites")]
    for i, (tg, txt) in enumerate(opens):
        yy = 420 + i * 30
        cv.text((420, yy), tg, "sansb", 14, RED, "ra", u); cv.text((436, yy), txt, "sans", 15, INK, "la", u)
    cv.text((W / 2, 550), "Cold is not the same as cooling.", "serif", 22, INK, "ma", u)
    cv.text((W / 2, 600), "Made by Claude Code on the MSI: Blender 5.1 (Cycles), Kokoro voice, Pillow, ffmpeg.  CC0.  Fact-checked by Codex with web search.", "sans", 14, INK, "ma", a)
    return cv.im.reduce(SS)

BOARDS_FN = {"diag_three": three_frame, "diag_law": law_frame, "diag_suit": suit_frame, "diag_orbitdc": orbitdc_frame,
             "diag_radiator": radiator_frame, "diag_debate": debate_frame, "end_card": end_frame}

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
