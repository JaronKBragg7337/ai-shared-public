# Pillow boards for Science 8.9 Every one-way-only is a story (cream-paper look, same family as ep6).  python diagram.py [FRAMES_DIR] [--force] [--only=name] [--preview]
import math, os, sys, random
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shots import SHOTS, FPS
OUT = next((a for a in sys.argv[1:] if not a.startswith("--")), "C:/Users/lilli/Renders/one-way-ep9/frames")
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



# ======================================================================== ep9 boards (Science 8.9, Every one-way-only is a story)
# Layout rule (same as ep6/ep7/ep8): nothing below y = 640; finish.py shrinks each board into the top of the frame and puts the
# captions in a dark band under it.  No em or en dashes anywhere on screen.
COOL = (62, 110, 170); GREEN = (40, 120, 60); STEEL = (150, 150, 156)
def fade(t, dur, a_in=.6, a_out=1.0): return max(0.0, min(1.0, t / a_in, (dur - t) / a_out))
def ap(t, t0, d=.7): return ease((t - t0) / d)
def src_line(cv, y, text, a): cv.text((W / 2, y), text, "sansl", 13, DIM, "ma", a)
def panel(cv, b, u): cv.rect(b, mix(CREAM, PAPER, u), mix(CREAM, RULE, u), 2, 10)
def pill(cv, cx, cy, t, u, col=RED, wdt=None):
    wdt = wdt or (font("sansb", 15).getlength(t) / SS + 30)
    cv.rect((cx - wdt / 2, cy - 15, cx + wdt / 2, cy + 15), mix(CREAM, (246, 228, 214), u), outline=mix(CREAM, col, u), w=2, r=14)
    cv.text((cx, cy - 10), t, "sansb", 15, col, "ma", u)

def murphy_frame(t, dur):
    cv = Cv(); a = fade(t, dur)
    cv.header("Murphy's Law: a story with disputed details", "\"If anything can go wrong, it will.\"  The exact original wording is not established.", a)
    u = ap(t, 8.0) * a
    panel(cv, (60, 140, 630, 420), u)
    cv.text((84, 152), "Tellings disagree on", "serif", 24, INK, "la", u)
    items = [("how many sensors there were", ""), ("who wired them", ""), ("even who was riding", "")]
    for i, (k, v) in enumerate(items):
        uu = ap(t, 9.0 + i * 1.2) * a; yy = 200 + i * 70
        cv.circ((96, yy + 12), 6, mix(CREAM, RED, uu)); cv.text((114, yy), k, "sans", 20, INK, "la", uu)
    pill(cv, 520, 166, "DISPUTED", u, RED, 140)
    u2 = ap(t, 14.0) * a
    panel(cv, (650, 140, 1220, 420), u2)
    cv.text((674, 152), "Who named it?", "serif", 24, INK, "la", u2)
    cv.para(674, 194, "George Nichols, on the project team: the team named it, partly to tease Murphy.", "sans", 17, INK, 520, 1.3, "l", u2)
    u3 = ap(t, 20.5) * a
    cv.para(674, 268, "Murphy's son: it came from his father.", "sans", 17, INK, 520, 1.3, "l", u3)
    u4 = ap(t, 23.0) * a
    cv.para(674, 316, "And similar sayings were around before 1949.", "sans", 17, INK, 520, 1.3, "l", u4)
    pill(cv, 1110, 166, "NOT SETTLED", u2, RED, 160)
    u5 = ap(t, 27.0) * a
    panel(cv, (60, 440, 1220, 580), u5)
    cv.text((84, 452), "What every telling shares", "serif", 22, AMBER, "la", u5)
    cv.para(84, 490, "The lesson Stapp made famous: assume it will go wrong, and plan for it.", "serif", 26, INK, 1110, 1.3, "l", u5)
    src_line(cv, 604, "Sources: Air and Space Forces Magazine; Improbable Research (Nick T. Spark); wordorigins.org; American Dialect Society list.", u5)
    return cv.im.reduce(SS)

def shingo_frame(t, dur):
    cv = Cv(); a = fade(t, dur)
    cv.header("Poka-yoke: mistake-proofing", "Shigeo Shingo, a Japanese engineer who trained and advised factories, including Toyota.", a)
    u = ap(t, 8.0) * a
    panel(cv, (60, 140, 630, 590), u)
    cv.text((84, 152), "An early case, 1961", "serif", 24, INK, "la", u)
    cv.para(84, 194, "A switch needed two small springs. Workers sometimes forgot one.", "sans", 18, INK, 520, 1.3, "l", u)
    # switch sketch with one spring missing
    cv.rect((120, 290, 330, 400), mix(CREAM, (226, 222, 210), u), mix(CREAM, INK, u), 2, 8)
    def coil(cx, cy, col, uu):
        for k in range(7): cv.ring((cx + k * 9, cy), 10, mix(CREAM, col, uu), 2)
    coil(150, 330, STEEL, u)
    cv.rect((228, 318, 300, 342), None, mix(CREAM, RED, u), 2, 6); cv.text((264, 350), "missing", "sansb", 14, RED, "ma", u)
    cv.text((225, 412), "drawn, not to scale", "sansl", 13, DIM, "ma", u)
    u2 = ap(t, 11.0) * a
    panel(cv, (650, 140, 1220, 590), u2)
    cv.text((674, 152), "The fix", "serif", 24, INK, "la", u2)
    steps = ["Count two springs into a little dish first.", "Build the switch.", "A spring still in the dish? You missed it."]
    for i, st_ in enumerate(steps):
        uu = ap(t, 11.3 + i * .6) * a; yy = 200 + i * 62
        cv.circ((694, yy + 12), 15, mix(CREAM, AMBER, uu)); cv.text((694, yy + 1), str(i + 1), "sansb", 16, CREAM, "ma", uu)
        cv.para(722, yy, st_, "sans", 18, INK, 470, 1.25, "l", uu)
    u3 = ap(t, 12.5) * a
    cv.line([(674, 410), (1196, 410)], mix(CREAM, RULE, u3), 2)
    cv.para(674, 428, "Don't blame the worker. Change the job so the mistake can't slip through.", "serif", 22, INK, 520, 1.3, "l", u3)
    src_line(cv, 610, "Sources: Shingo's book Zero Quality Control, via mistakeproofing.com and Michel Baudin; Lean Blog (2024). An early case, not proven the first.", u2)
    return cv.im.reduce(SS)

def nozzles_frame(t, dur):
    cv = Cv(); a = fade(t, dur)
    cv.header("Why the gas nozzle got thinner", "United States, 1970s: catalytic converters that leaded gas would ruin.", a)
    # three spout tips drawn to the same scale (1 inch = 220 px)
    S = 190.0
    tips = [(7.0, "unleaded", "no wider than 0.840 in (21.3 mm)", .840, (40, 40, 44), "EPA rule"),
            (12.0, "leaded (gone from cars)", "about 0.93 in or wider: blocked", .930, (120, 110, 100), "EPA rule"),
            (15.5, "diesel", "usually 15/16 in (23.8 mm)", .9375, GREEN, "SAE J285")]
    for i, (t0, name, txt, d_in, col, src) in enumerate(tips):
        u = ap(t, t0) * a; cx = 210 + i * 420; cy = 312
        panel(cv, (cx - 190, 176, cx + 190, 470), u)
        cv.circ((cx, cy), d_in * S / 2, mix(CREAM, (205, 205, 210), u), mix(CREAM, col, u), 4)
        cv.circ((cx, cy), d_in * S / 2 - 10, mix(CREAM, (60, 60, 64), u))
        cv.text((cx, 400), name, "sansb", 19, INK, "ma", u)
        cv.para(cx, 426, txt, "sans", 15, INK, 340, 1.2, "m", u)
        cv.text((cx + 176, 450), src, "sansl", 13, DIM, "ra", u)
    u = ap(t, 9.0) * a
    for i in range(3):
        cx = 210 + i * 420; r_ = 0.885 * S / 2
        pts = [(cx + r_ * math.cos(2 * math.pi * k / 72), 312 + r_ * math.sin(2 * math.pi * k / 72)) for k in range(73)]
        cv.dashed(pts, mix(CREAM, AMBER, u), 3, 5, 4)
        uu = min(u, ap(t, tips[i][0] + .8) * a)
        pill(cv, cx, 200, ("FITS", "WON'T FIT", "OFTEN WON'T FIT")[i], uu, GREEN if i == 0 else RED, (90, 130, 190)[i])
    cv.text((W / 2, 150), "Dashed circle: a gas car's narrow filler opening (drawn to show the idea)", "sansb", 15, AMBER, "ma", u)
    u2 = ap(t, 1.0) * a
    cv.text((W / 2, 484), "Spout tips drawn to the same scale.", "sansl", 13, DIM, "ma", u2)
    u3 = ap(t, 2.0) * a
    src_line(cv, 606, "Sources: EPA rules (first published 1973; 40 CFR 80.22 and 80.24); SAE J285 nozzle spouts; AAA on misfueling.", u3)
    return cv.im.reduce(SS)

def interlock_frame(t, dur):
    cv = Cv(); a = fade(t, dur)
    cv.header("Brake to shift out of Park", "Brake transmission shift interlock, required in the United States.", a)
    rows = [(.3, "Since September 2010", "Cars and light trucks with an automatic transmission and a Park position must have it.", "FMVSS 114"),
            (1.0, "How it works", "The shifter can't leave Park unless your foot is on the brake.", ""),
            (5.0, "Why", "A law passed in 2008, aimed at keeping children safe around cars, made it required.", "Kids Transportation Safety Act"),
            (10.5, "And", "Automakers had already agreed to do it.", "voluntary agreement")]
    for i, (t0, k, v, src) in enumerate(rows):
        u = ap(t, t0) * a; y = 140 + i * 112
        panel(cv, (60, y, 1220, y + 100), u)
        cv.text((84, y + 12), k, "serif", 22, AMBER, "la", u)
        cv.para(84, y + 50, v, "sans", 18, INK, 860, 1.25, "l", u)
        if src: cv.text((1196, y + 16), src, "sansl", 14, DIM, "ra", u)
    src_line(cv, 604, "Sources: NHTSA, FMVSS 114 final rule, Federal Register, 30 Mar 2010 (S5.3, vehicles under 10,000 lb).", ap(t, 10) * a)
    return cv.im.reduce(SS)

def end_frame(t, dur):
    cv = Cv(); a = fade(t, dur, .8, 1.2)
    cv.text((W / 2, 22), "Heartbeat Observatory", "serif", 46, INK, "ma", a)
    cv.text((W / 2, 82), "heartbeatobservatory.com", "sansb", 24, AMBER, "ma", a)
    cv.text((W / 2, 116), "Science  ·  Episode 8.9  ·  Every one-way-only is a story", "sans", 18, DIM, "ma", a)
    cv.line([(W / 2 - 60, 146), (W / 2 + 60, 146)], mix(CREAM, AMBER, a), 3)
    cv.text((W / 2, 154), "The 3D scenes are illustrations built in Blender: generic objects, not real products, places or footage.", "sans", 15, DIM, "ma", a)
    src = [
        "Murphy's Law: Air and Space Forces Magazine; Improbable Research (Nick T. Spark); wordorigins.org; American Dialect Society list",
        "Poka-yoke: Shingo, Zero Quality Control (via mistakeproofing.com, Michel Baudin); Lean Blog (2024)",
        "Nozzles: EPA, 40 CFR 80.22 and 80.24; SAE J285; AAA  ·  Shift interlock: FMVSS 114, Federal Register 30 Mar 2010",
        "Microwave doors: 21 CFR 1030.10 (FDA)  ·  SIM formats: ETSI nano-SIM (2012)  ·  USB-C: USB 3.0 Promoter Group, Aug 2014",
    ]
    y = 182
    for i, s_ in enumerate(src):
        y = cv.para(W / 2, y, s_, "sans", 15, INK, 1200, 1.22, "m", ease((t - .5 - i * .2) / .6) * a) + 5
    u = ease((t - 2.0) / .6) * a
    panel(cv, (70, 340, 1210, 500), u)
    cv.text((W / 2, 352), "Still open (labelled in the episode)", "sansb", 17, RED, "ma", u)
    opens = [("DISPUTED", "the details of the 1949 sensor story and who named Murphy's Law"),
             ("NOT ESTABLISHED", "the exact original wording of Murphy's Law"),
             ("NOT PROVEN FIRST", "the 1961 spring dish as Shingo's first mistake-proofing case")]
    for i, (tg, txt) in enumerate(opens):
        yy = 392 + i * 30
        cv.text((420, yy), tg, "sansb", 14, RED, "ra", u); cv.text((436, yy), txt, "sans", 15, INK, "la", u)
    cv.text((W / 2, 530), "Two fixes: make the wrong way impossible, or make every way right.", "serif", 22, INK, "ma", u)
    cv.text((W / 2, 600), "Made by Claude Code on the MSI: Blender 5.1 (Cycles), Kokoro voice, Pillow, ffmpeg.  CC0.  Fact-checked by Codex with web search.", "sans", 14, INK, "ma", a)
    return cv.im.reduce(SS)

BOARDS_FN = {"diag_murphy": murphy_frame, "diag_shingo": shingo_frame, "diag_nozzles": nozzles_frame,
             "diag_interlock": interlock_frame, "end_card": end_frame}

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
