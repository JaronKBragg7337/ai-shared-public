import sys; sys.path.insert(0, '..')
from elib import *
import tvlib, random

SCR = json.load(open('script.json'))
SUBS = {s['id']: s['disp'] for s in SCR}
def cq(sid, k): return cue(sid, min(k, len(SUBS[sid]) - 1))
SKY = TEA; RUST = COR; LIFE = (140, 198, 104); ICE = (190, 226, 240); OCH = (232, 178, 70)
def ctr(): return (CONT[0] + CONT[2]) / 2
def P(a, b): return b if PORT else a

# ------------------------------------------------------------------ s1 title
def sc_title(cv, t, p):
    a = ease(t / 1.0); ty = 150
    cv.text((W / 2, ty), 'HEARTBEAT TV  ·  EARTH  ·  EPISODE 1', 'sansb', P(34, 30), DIMC, 'ma', a)
    sz = P(112, 92)
    lines = ('The first great', 'extinction was', 'caused by life itself') if PORT else ('The first great extinction', 'was caused by life itself')
    for k, l in enumerate(lines):
        cv.text((W / 2, ty + 70 + k * sz * 1.12), l, 'serif', sz, CREAM, 'ma', ease((t - 0.2 - k * 0.2) / 1.0), 5)
    y = P(600, 760)
    c = cq('s1', 1)
    for i, (txt, col) in enumerate((('ASTEROID?', DIMC), ('VOLCANO?', DIMC), ('LIFE?', RUST))):
        a2 = ease((t - c - i * 1.2) / 0.7)
        pill(cv, W / 2 if PORT else W * (0.25 + 0.25 * i), y + (i * 110 if PORT else 0), txt, col, a2, 40)
    a3 = ease((t - cq('s1', 3)) / 0.8)
    if PORT:
        cv.text((W / 2, y + 330), 'The Great Oxidation Event', 'serifr', 46, OCH, 'ma', a3)
        cv.text((W / 2, y + 390), 'about 2.4 billion years ago', 'serifr', 46, OCH, 'ma', a3)
    else:
        cv.text((W / 2, y + 120), 'The Great Oxidation Event  ·  about 2.4 billion years ago', 'serifr', 44, OCH, 'ma', a3)

# ------------------------------------------------------------------ s2 air
def sc_air(cv, t, p):
    x0 = P(100, 70); x1 = W - x0; bh = P(120, 110)
    y1 = CONT[1] + P(60, 60); y2 = y1 + P(330, 380)
    a = ease(t / 0.7)
    cv.text((x0, y1 - 46), 'AIR TODAY', 'sansb', 36, DIMC, 'la', a)
    u = ease(t / 1.2); w = x1 - x0
    cv.rect((x0, y1, x0 + w * 0.78 * u, y1 + bh), mix((120, 120, 128), BG, a))
    ox = x0 + w * 0.78
    cv.rect((ox, y1, ox + w * 0.21 * u, y1 + bh), mix(SKY, BG, a))
    cv.text((x0 + 24, y1 + bh / 2 - 26), 'nitrogen 78%', 'sansb', 44, CREAM, 'la', a)
    if u > 0.9: cv.text((ox + w * 0.105, y1 + bh / 2 - 26), 'oxygen 21%', 'sansb', P(40, 30), (20, 30, 40), 'ma', a)
    c = cq('s2', 2); a2 = ease((t - c) / 0.8)
    cv.text((x0, y2 - 46), 'AIR BEFORE ~2.4 BILLION YEARS AGO', 'sansb', 36, DIMC, 'la', a2)
    cv.rect((x0, y2, x1, y2 + bh), mix((96, 90, 84), BG, a2))
    cv.text((x0 + 24, y2 + bh / 2 - 26), 'oxygen: too thin to draw', 'sansb', 44, CREAM, 'la', a2)
    a3 = ease((t - c - 1.0) / 0.8)
    cv.para(W / 2, y2 + bh + P(30, 40), "Oxygen estimated below 0.001% of today's amount (from sulfur isotopes). An estimate, not a measurement of the air.", 'sans', P(36, 34), TEA, W - 2 * x0, 1.2, 'm', a3)

# ------------------------------------------------------------------ s3 cyanobacteria
def cell(cv, cx, cy, r, a, col=LIFE):
    cv.circ((cx, cy), r + 6, mix((60, 90, 50), BG, a)); cv.circ((cx, cy), r, mix(col, BG, a))
    cv.circ((cx - r * 0.25, cy - r * 0.25), r * 0.35, mix((176, 224, 140), BG, a * 0.8))
def sc_cyano(cv, t, p):
    a = ease(t / 0.7)
    mx = W / 2; my = CONT[1] + P(200, 220)
    for k in range(5):
        cell(cv, mx + (k - 2) * 70, my + 8 * math.sin(k * 1.3 + t * 0.8), 34, a)
    cv.text((mx, my + 60), 'cyanobacteria (a chain of cells)', 'serifr', 32, DIMC, 'ma', a)
    c1 = cq('s3', 1); a1 = ease((t - c1) / 0.8)
    for i, (lab, col) in enumerate((('sunlight', OCH), ('CO2', DIMC), ('water', SKY))):
        yy = my - 80 + i * 80
        xx = P(240, 170)
        pill(cv, xx, yy, lab, col, a1, 32)
        arrow(cv, (xx + 105, yy), (mx - 190, my), col, 4, 16, a1 * 0.9)
    c2 = cq('s3', 2); a2 = ease((t - c2) / 0.8)
    ox = W - P(300, 200)
    pill(cv, ox, my - 60, 'sugar (food)', LIFE, a2, 32)
    arrow(cv, (mx + 190, my - 15), (ox - 110, my - 56), LIFE, 4, 16, a2)
    pill(cv, ox, my + 60, 'O2 = waste', SKY, a2, 36)
    arrow(cv, (mx + 190, my + 15), (ox - 110, my + 56), SKY, 4, 16, a2)
    for k in range(10):
        bt = (t * 0.45 + k * 0.1) % 1.0
        bx = mx + 130 + (k % 5) * 30; by = my + 30 - bt * 150
        if a2 > 0.2: cv.ring((bx, by), 8 + (k % 3) * 3, mix(SKY, BG, 0.7 * a2 * (1 - bt)), 3)
    by = my + P(130, 150)
    a3 = ease((t - cq('s3', 3)) / 0.8)
    if a3 > 0:
        badge(cv, ctr(), by, 'WHEN THIS STARTED: DEBATED', ROSE, a3, 34, 'm')
        cv.para(ctr(), by + 80, '2.7 billion years ago or earlier (some evidence). Claimed older fossils are contested.', 'sans', P(36, 34), CREAM, CONT[2] - CONT[0] - 160, 1.2, 'm', a3)
    a4 = ease((t - cq('s3', 6)) / 0.8)
    if a4 > 0: cv.para(ctr(), by + P(170, 200), 'Agreed: the oxygen did not pile up in the air right away.', 'serifr', P(44, 40), OCH, CONT[2] - CONT[0] - 120, 1.2, 'm', a4)

# ------------------------------------------------------------------ s4 sinks
def sc_sinks(cv, t, p):
    x0 = 90; x1 = W - 90
    rows = [('Dissolved iron in the oceans', RUST), ('Volcanic gases', DIMC), ('Freshly exposed rock', OCH), ('Free oxygen in the air', SKY)]
    step = (CONT[3] - CONT[1] - P(150, 200)) / 4; bh = 56
    y = CONT[1] + 20
    cv.text((x0, y), 'WHERE THE NEW OXYGEN WENT  (schematic)', 'sansb', 30, DIMC, 'la', ease(t / 0.6))
    y += 56
    base = cq('s4', 2)
    for i, (lab, col) in enumerate(rows):
        t0 = base - 0.3 + i * 1.5 + (1.2 if i == 3 else 0)
        a = ease((t - t0) / 0.5); yy = y + i * step
        cv.text((x0, yy), lab, 'sansb', 36, CREAM, 'la', a)
        bx = (x0, yy + 46, x1, yy + 46 + bh)
        cv.rect(bx, mix((70, 56, 46), BG, a), 10)
        u = ease((t - t0 - 0.3) / 1.4)
        if i == 3: u = ease((t - t0 - 0.3) / 3.0) * 0.5
        cv.rect((bx[0], bx[1], bx[0] + (bx[2] - bx[0]) * u, bx[3]), mix(col, BG, a), 10)
    a = ease((t - cq('s4', 4)) / 0.8)
    badge(cv, ctr(), CONT[3] - P(60, 130), 'DELAY ESTIMATES: ~200 TO 400 MILLION YEARS', ROSE, a, 30, 'm')
    cv.text((ctr(), CONT[3] - P(0, 62)) if PORT else (ctr(), CONT[3] + 6), 'depends on when the microbes began: not settled', 'sans', 28, DIMC, 'ma', ease((t - cq('s4', 5)) / 0.8))

# ------------------------------------------------------------------ s5 banded iron formation
IRON = [(172, 70, 44), (200, 96, 58), (150, 58, 40)]; SIL = [(60, 54, 54), (110, 108, 112), (46, 42, 44)]
def sc_bif(cv, t, p):
    bx = (60, CONT[1] + 10, 1020, CONT[1] + 250) if PORT else (70, 210, 800, 740)
    rnd = random.Random(5); layers = []; yy = bx[1]
    while yy < bx[3]:
        h = rnd.choice([14, 20, 28, 40]); layers.append((yy, min(yy + h, bx[3]))); yy += h
    cv.rect((bx[0] - 6, bx[1] - 6, bx[2] + 6, bx[3] + 6), mix(CARDC, BG, ease(t / 0.4)), 8)
    for i, (a_, b_) in enumerate(layers):
        col = IRON[i % 3] if i % 2 == 0 else SIL[i % 3]
        aa = ease((t - 0.4 - i * 0.08) / 0.5)
        cv.rect((bx[0], a_, bx[0] + (bx[2] - bx[0]) * aa, b_), col)
    a = ease((t - 2.0) / 0.8)
    cv.para(bx[0], bx[3] + 14, 'Iron-rich and silica-rich layers. Hamersley Range, W. Australia, ~2.5 billion years old. (Drawing, not a photo.)', 'sans', 28, DIMC, bx[2] - bx[0], 1.2, 'l', a)
    fx = 60 if PORT else 880; fy = bx[3] + 110 if PORT else 215; fw = 960 if PORT else 980
    a2 = ease((t - cq('s5', 5)) / 0.7)
    if a2 > 0:
        pill(cv, fx + 170, fy + 30, 'iron in seawater', DIMC, a2, 30)
        cv.text((fx + 340, fy + 4), '+ O2', 'serif', 46, SKY, 'la', a2)
        arrow(cv, (fx + 470, fy + 30), (fx + 560, fy + 30), CREAM, 4, 16, a2)
        pill(cv, fx + 700, fy + 30, 'rust sinks', RUST, a2, 30)
    a3 = ease((t - cq('s5', 5)) / 0.7)
    if a3 > 0: badge(cv, fx, fy + 90, 'ONE PROMINENT EXPLANATION, NOT SETTLED', OCH, a3, 28)
    a4 = ease((t - cq('s5', 7)) / 0.7)
    if a4 > 0:
        badge(cv, fx, fy + 190, 'CAVEAT', ROSE, a4, 28)
        cv.para(fx, fy + 260, 'Some formed when oxygen was still scarce. Proposed causes: other microbes, or sunlight.', 'sans', P(38, 36), CREAM, fw, 1.2, 'l', a4)
    a5 = ease((t - cq('s5', 9)) / 0.7)
    if a5 > 0:
        cv.para(fx, fy + P(400, 350), 'The bands show iron leaving the ocean. On their own, they do not date the oxygen in the air.', 'serifr', P(40, 38), OCH, fw, 1.2, 'l', a5)

# ------------------------------------------------------------------ s6 sulfur + other clues
def sc_sulfur(cv, t, p):
    gx = (80, CONT[1] + 60, 1000, CONT[1] + 360) if PORT else (110, 260, 840, 690)
    a = ease(t / 0.7)
    cv.rect((gx[0] - 30, gx[1] - 56, gx[2] + 30, gx[3] + 66), mix(CARDC, BG, a), 18)
    cv.text(((gx[0] + gx[2]) / 2, gx[1] - 46), 'Sulfur isotope signal (schematic)', 'sansb', 30, DIMC, 'ma', a)
    midy = (gx[1] + gx[3]) / 2
    cv.line([(gx[0], midy), (gx[2], midy)], mix(DIMC, BG, 0.5 * a), 2)
    rnd = random.Random(2); n = 90; cut = gx[0] + (gx[2] - gx[0]) * 0.45
    for i in range(n):
        xx = gx[0] + 10 + (gx[2] - gx[0] - 20) * i / (n - 1)
        sp = 0.46 if xx < cut else 0.04
        yy = midy + rnd.uniform(-1, 1) * sp * (gx[3] - gx[1])
        cv.circ((xx, yy), 7, mix(OCH if xx < cut else SKY, BG, ease((t - 0.5 - i * 0.03) / 0.4)))
    a2 = ease((t - 3.0) / 0.8)
    cv.text(((gx[0] + cut) / 2, gx[3] + 12), 'older rocks: signal', 'sans', 26, OCH, 'ma', a2)
    cv.text(((cut + gx[2]) / 2, gx[3] + 12), 'younger rocks: gone', 'sans', 26, SKY, 'ma', a2)
    cv.text((cut, gx[1] - 4), 'change falls between ~2.45 and 2.09 billion yrs ago', 'sansb', 22, CREAM, 'ma', a2)
    items = [(cq('s6', 7), 'Grains that rust away (pyrite, uraninite) wash into old river sand, then stop appearing'),
             (cq('s6', 9), 'Red, rusted soil layers show up'),
             (cq('s6', 10), 'None is a switch. They are proxies: rocks tell the story. Nobody measured the air.')]
    x0 = 60 if PORT else 930; y0 = CONT[1] + 440 if PORT else 250; w = 960 if PORT else 920; hh = 150 if PORT else 140
    for i, (tc, txt) in enumerate(items):
        aa = ease((t - tc) / 0.7)
        if aa <= 0: continue
        yy = y0 + i * (hh + 20)
        card(cv, (x0, yy, x0 + w, yy + hh), aa, [OCH, RUST, ROSE][i])
        cv.para(x0 + 26, yy + 26, txt, 'sans', P(38, 36), CREAM, w - 52, 1.2, 'l', aa)

# ------------------------------------------------------------------ s7 timing
def sc_timing(cv, t, p):
    x0 = 120 if not PORT else 70; x1 = W - 90 if not PORT else W - 70
    lo, hi = 2.6, 2.1
    def X(v): return x0 + (lo - v) / (lo - hi) * (x1 - x0)
    y0 = CONT[1] + 20; a = ease(t / 0.6)
    cv.text((x0, y0), 'PUBLISHED ESTIMATES: when oxygen began to rise', 'sansb', 30, DIMC, 'la', a)
    rows = [('Gumsley et al. 2017', 2.460, 2.426, cq('s7', 2)), ('Warke et al. 2020', 2.501, 2.434, cq('s7', 3)), ('Poulton et al. 2021: early rise to permanent', 2.434, 2.222, cq('s7', 3) + 1.5)]
    rs = P(100, 110); ay = y0 + 50 + 3 * rs + 10
    cv.line([(x0, ay), (x1, ay)], mix(DIMC, BG, 0.6 * a), 3)
    for v in (2.6, 2.5, 2.4, 2.3, 2.2, 2.1):
        cv.line([(X(v), ay - 8), (X(v), ay + 8)], mix(DIMC, BG, 0.6 * a), 3)
        cv.text((X(v), ay + 12), f'{v}', 'sans', 26, DIMC, 'ma', a)
    for i, (nm, v0, v1, tc) in enumerate(rows):
        aa = ease((t - tc) / 0.7); yy = y0 + 50 + i * rs
        if aa <= 0: continue
        cv.text((x0, yy), nm, 'sansb', 32, CREAM, 'la', aa)
        u = ease((t - tc - 0.2) / 0.9)
        cv.rect((X(v0), yy + 42, X(v0) + (X(v1) - X(v0)) * u, yy + 78), mix(OCH if i < 2 else ROSE, BG, aa), 10)
    a3 = ease((t - cq('s7', 4)) / 0.8)
    cy0 = ay + P(70, 90); ch = P(150, 220)
    if a3 > 0:
        cv.text((x0, cy0), 'More like pulses than a switch (schematic)', 'sansb', 30, DIMC, 'la', a3)
        pts = []
        for k in range(121):
            u = k / 120; yv = 0.15 + 0.7 * u + 0.12 * math.sin(u * 17) * (1 - u * 0.4)
            pts.append((x0 + (x1 - x0) * u, cy0 + 50 + ch * (1 - min(0.95, yv))))
        m = int(len(pts) * ease((t - cq('s7', 4)) / 3.0))
        if m > 1: cv.line(pts[:m], mix(SKY, BG, a3), 6)
        cv.text((x0, cy0 + 56 + ch), 'oxygen  vs.  time', 'sans', 24, DIMC, 'la', a3)

# ------------------------------------------------------------------ s8 poison and payoff
def sc_poison(cv, t, p):
    bxs = [(60, CONT[1] + 10, 1020, CONT[1] + 300), (60, CONT[1] + 330, 1020, CONT[1] + 890)] if PORT else [(70, 210, 900, 830), (940, 210, 1850, 830)]
    a = ease(t / 0.6); card(cv, bxs[0], a, ROSE)
    cv.text((bxs[0][0] + 34, bxs[0][1] + 20), 'The danger', 'serif', 54, ROSE, 'la', a)
    y = bxs[0][1] + 100
    for k, l in enumerate(['Oxygen forms reactive molecules', 'They can damage proteins, DNA, cell membranes', 'Cells without defenses suffer']):
        y = cv.para(bxs[0][0] + 34, y, '• ' + l, 'sans', P(40, 36), CREAM, bxs[0][2] - bxs[0][0] - 68, 1.2, 'l', ease((t - 0.8 - k * 0.9) / 0.6)) + 14
    c2 = cq('s8', 2); a2 = ease((t - c2) / 0.7); card(cv, bxs[1], a2, SAGE)
    cv.text((bxs[1][0] + 34, bxs[1][1] + 20), 'The payoff', 'serif', 54, SAGE, 'la', a2)
    rows = [dict(label='Fermenting', val=2, txt='about 2', at=c2 + 0.5, col=DIMC), dict(label='Breathing oxygen', val=32, txt='about 30', at=c2 + 1.4, col=SKY)]
    ar = (bxs[1][0] + 20, bxs[1][1] + 100, bxs[1][2] - 20, bxs[1][1] + P(300, 250))
    hbars(cv, t, rows, 34, ar, P(280, 290))
    cv.text((bxs[1][0] + 34, ar[3] + 6), 'ATP (cell energy) per sugar molecule, textbook values', 'sans', 26, DIMC, 'la', ease((t - c2 - 1.4) / 0.8))
    a3 = ease((t - cq('s8', 4)) / 0.8)
    cv.para(bxs[1][0] + 34, ar[3] + 56, 'Strict anaerobes still live where oxygen does not reach: mud, deep sediment, animal guts. For some, the story was retreat, not only death.', 'sans', P(38, 36), CREAM, bxs[1][2] - bxs[1][0] - 68, 1.2, 'l', a3)

# ------------------------------------------------------------------ s9 Huronian
def sc_huron(cv, t, p):
    bx = (70, CONT[1] + 10, 470, CONT[1] + 560) if PORT else (90, 210, 540, 730)
    a = ease(t / 0.6)
    cv.rect((bx[0] - 6, bx[1] - 6, bx[2] + 6, bx[3] + 6), mix(CARDC, BG, a), 10)
    h = (bx[3] - bx[1]) / 5
    for i in range(5):
        gl = i in (0, 2, 4); aa = ease((t - 0.5 - i * 0.35) / 0.5)
        cv.rect((bx[0], bx[1] + i * h, bx[2], bx[1] + (i + 1) * h - 3), mix(ICE if gl else (110, 84, 62), BG, aa))
        if gl: cv.text(((bx[0] + bx[2]) / 2, bx[1] + i * h + h / 2 - 16), 'glacial deposits', 'sansb', 24, (30, 40, 50), 'ma', aa)
    a0 = ease((t - 2.5) / 0.8)
    cv.para((bx[0] + bx[2]) / 2, bx[3] + 12, 'North of Lake Huron, Canada. Three glacial horizons, ~2.45 to ~2.22 billion years ago (schematic).', 'sans', 24, DIMC, bx[2] - bx[0] + 80, 1.2, 'm', a0)
    fx = 520 if PORT else 650; fw = 520 if PORT else 1180
    c2 = cq('s9', 3); a2 = ease((t - c2) / 0.7); y = CONT[1] + P(20, 10)
    if a2 > 0:
        cv.text((fx, y), 'The methane idea', 'serif', 50, OCH, 'la', a2)
        cv.para(fx, y + 72, 'Methane warmed the early air. Oxygen destroyed it: CH4 + O2 gives CO2 + water, a weaker greenhouse gas. The planet cooled.', 'sans', P(40, 34), CREAM, fw, 1.2, 'l', a2)
    a3 = ease((t - cq('s9', 5)) / 0.7); yb = y + P(270, 330)
    if a3 > 0:
        badge(cv, fx, yb, 'HYPOTHESIS', ROSE, a3, 26)
        badge(cv, fx + (230 if PORT else 260), yb + (62 if PORT else 0), 'DATING DISPUTED', ROSE, a3, 26) if False else badge(cv, fx, yb + 60, 'DATING DISPUTED', ROSE, a3, 26) if PORT else badge(cv, fx + 260, yb, 'DATING DISPUTED', ROSE, a3, 28)
        cv.para(fx, yb + P(80, 130), 'Makganyene glaciation (South Africa) may have reached the tropics: a possible snowball Earth.', 'sans', P(38, 34), CREAM, fw, 1.2, 'l', a3)
    a4 = ease((t - cq('s9', 7)) / 0.7)
    if a4 > 0: cv.para(fx, yb + P(220, 330), 'Warke et al. 2020 argued oxygen rose before that snowball. That fits, but the link is still a hypothesis.', 'serifr', P(40, 34), OCH, fw, 1.2, 'l', a4)

# ------------------------------------------------------------------ s10 extinction?
def sc_ext(cv, t, p):
    a = ease(t / 0.8); y = CONT[1] + 0
    cv.text((W / 2, y), 'A mass extinction?', 'serif', P(84, 76), CREAM, 'ma', a)
    badge(cv, W / 2, y + P(110, 110), 'NOT ESTABLISHED', ROSE, ease((t - 0.8) / 0.6), 46, 'm')
    bxs = [(60, y + 230, 1020, y + 530), (60, y + 560, 1020, y + 880)] if PORT else [(70, y + 210, 920, y + 620), (960, y + 210, 1850, y + 620)]
    c1 = cq('s10', 3); a1 = ease((t - c1) / 0.7)
    card(cv, bxs[0], a1, DIMC); cv.text((bxs[0][0] + 30, bxs[0][1] + 18), 'What we cannot count', 'serif', 44, DIMC, 'la', a1)
    yy = bxs[0][1] + 84
    for k, l in enumerate(['Microbes leave few fossils', 'Rocks that old are rare and changed by heat and pressure', 'No species counts before and after']):
        yy = cv.para(bxs[0][0] + 30, yy, '• ' + l, 'sans', P(36, 34), CREAM, bxs[0][2] - bxs[0][0] - 60, 1.2, 'l', ease((t - c1 - 0.5 - k * 0.8) / 0.6)) + 8
    c2 = cq('s10', 7); a2 = ease((t - c2) / 0.7)
    card(cv, bxs[1], a2, OCH); cv.text((bxs[1][0] + 30, bxs[1][1] + 18), 'The 2019 sulfate study', 'serif', 44, OCH, 'la', a2)
    cv.para(bxs[1][0] + 30, bxs[1][1] + 80, 'Productivity inferred to fall by more than 80%, ~2.0 billion years ago, shortly after the oxygen rise. An oxygen overshoot as the cause is debated. It measures what the biosphere produced, not species lost.', 'sans', P(34, 32), CREAM, bxs[1][2] - bxs[1][0] - 60, 1.2, 'l', ease((t - c2 - 0.5) / 0.7))
    badge(cv, bxs[1][0] + 30, bxs[1][3] - 62, 'A DIFFERENT MOMENT', ROSE, ease((t - c2 - 1.5) / 0.6), 26)

# ------------------------------------------------------------------ s11 scoreboard
def sc_board(cv, t, p):
    bxs = [(40, CONT[1], 1040, CONT[1] + 330), (40, CONT[1] + 350, 1040, CONT[1] + 690)] if PORT else [(70, 210, 920, 700), (960, 210, 1850, 700)]
    a = ease(t / 0.6); card(cv, bxs[0], a, SAGE)
    cv.text((bxs[0][0] + 30, bxs[0][1] + 18), 'Well supported', 'serif', 52, SAGE, 'la', a)
    yy = bxs[0][1] + 96
    for k, l in enumerate(['Oxygen in the air rose sharply around 2.4 billion years ago', 'The sulfur record changed', 'Living things were the source']):
        yy = cv.para(bxs[0][0] + 30, yy, '• ' + l, 'sans', P(40, 36), CREAM, bxs[0][2] - bxs[0][0] - 60, 1.2, 'l', ease((t - 0.8 - k * 1.0) / 0.6)) + 10
    c = cq('s11', 3); a2 = ease((t - c) / 0.6); card(cv, bxs[1], a2, ROSE)
    cv.text((bxs[1][0] + 30, bxs[1][1] + 18), 'Debated', 'serif', 52, ROSE, 'la', a2)
    yy = bxs[1][1] + 96
    for k, l in enumerate(['Exactly when, and how fast', 'When cyanobacteria began', 'Whether it caused the ice ages', 'How much life died']):
        yy = cv.para(bxs[1][0] + 30, yy, '• ' + l, 'sans', P(40, 36), CREAM, bxs[1][2] - bxs[1][0] - 60, 1.2, 'l', ease((t - c - 0.6 - k * 0.8) / 0.6)) + 10
    a3 = ease((t - cq('s11', 5)) / 0.8)
    cv.para(ctr(), P(CONT[3] - 100, CONT[1] + 720), 'What would help: better-dated rocks, better chemical fingerprints of ancient microbes, models that tie them together.', 'serifr', P(38, 34), OCH, CONT[2] - CONT[0] - 80, 1.2, 'm', a3)

# ------------------------------------------------------------------ s12 close
def sc_close(cv, t, p):
    lines = [(0.4, 'Life did not just live on Earth.', CREAM, 'serif'), (cq('s12', 1), 'It changed the air, the oceans, the rocks, the climate.', OCH, 'serif'), (cq('s12', 2), 'Everything after had to live in the world life made.', CREAM, 'serifr')]
    statements(cv, t, lines, CONT[1] + P(60, 40))
    a = ease((t - cq('s12', 3)) / 0.9)
    if a > 0: cv.para(W / 2, P(CONT[3] - 90, CONT[3] - 150), "Every breath of oxygen began as somebody's waste.", 'serifr', P(54, 46), SKY, W - 160, 1.2, 'm', a)

SOURCES = ['Farquhar, Bao & Thiemens, Science 289 (2000): mass-independent sulfur isotopes',
 'Gumsley et al., PNAS 114 (2017) · Warke et al., PNAS 117 (2020) · Poulton et al., Nature 592 (2021)',
 'Hodgskiss et al., PNAS 116 (2019): productivity collapse after the Great Oxidation Event',
 'Lyons, Reinhard & Planavsky, Nature 506 (2014): the rise of oxygen · Kopp et al., PNAS 102 (2005): Huronian glaciation and methane',
 'Cloud, Science 160 (1968): banded iron formations and oxygen · Fournier et al., Proc. R. Soc. B (2021): cyanobacteria timing']
def sc_end(cv, t, p):
    a = ease(t / 1.0); cy = P(90, 190)
    cv.text((W / 2, cy), 'Heartbeat Observatory', 'serif', P(100, 84), CREAM, 'ma', a)
    cv.text((W / 2, cy + P(135, 130)), 'heartbeatobservatory.com', 'sansb', 52, COR, 'ma', a)
    cv.text((W / 2, cy + 215), 'Earth · Episode 1 · sources checked October 2026', 'sans', P(34, 30), DIMC, 'ma', a)
    y = cy + 290; cv.text((W / 2, y), 'Sources', 'sansb', 32, DIMC, 'ma', ease((t - 0.6) / 1))
    yy = y + 50
    for i, s in enumerate(SOURCES):
        yy = cv.para(W / 2, yy, s, 'sans', P(28, 27), CREAM, P(1700, 980), 1.2, 'm', ease((t - 0.8 - i * 0.2) / 0.8)) + 8
    cv.text((W / 2, yy + 20), 'Made with AI by Heartbeat Observatory', 'sans', 30, DIMC, 'ma', ease((t - 2.5) / 0.8))

SCENES = [
 ('s1', '', '', sc_title),
 ('s2', 'Air before and after', 'Sources: Lyons, Reinhard & Planavsky, Nature (2014); Farquhar et al., Science (2000). Pre-event oxygen is an estimate.', sc_air),
 ('s3', 'Who made the oxygen', 'Sources: Lyons et al., Nature (2014); Fournier et al., Proc. R. Soc. B (2021).', sc_cyano),
 ('s4', 'Where the oxygen went first', 'Sources: Lyons et al., Nature (2014); Poulton et al., Nature (2021). Bars are a schematic.', sc_sinks),
 ('s5', 'Clue 1: banded iron formations', 'Sources: Cloud, Science (1968); Trendall (2002); Hamersley Basin geology.', sc_bif),
 ('s6', 'Clue 2: sulfur and rusting', 'Sources: Farquhar, Bao & Thiemens, Science (2000); Johnson et al., GSA Bulletin (2014).', sc_sulfur),
 ('s7', 'When did it happen?', 'Sources: Gumsley et al., PNAS (2017); Warke et al., PNAS (2020); Poulton et al., Nature (2021).', sc_timing),
 ('s8', 'Poison and payoff', 'Sources: standard biochemistry (ATP yield per glucose); Lyons et al., Nature (2014).', sc_poison),
 ('s9', 'The cold chapter', 'Sources: Kopp et al., PNAS (2005); Warke et al., PNAS (2020); Huronian Supergroup, Ontario.', sc_huron),
 ('s10', 'Was it a mass extinction?', 'Source: Hodgskiss et al., PNAS (2019). Microbial die-offs are inferred, not counted.', sc_ext),
 ('s11', 'Where things stand', '', sc_board),
 ('s12', '', '', sc_close),
 ('s13', '', '', sc_end),
]
GA.update({'s2': 3.2, 's3': 2.7, 's4': 2.5, 's5': 2.5, 's6': 2.4, 's7': 2.4, 's8': 2.4, 's9': 2.3, 's10': 2.0})
configure(SUBS, SCENES)
if __name__ == '__main__': main()
