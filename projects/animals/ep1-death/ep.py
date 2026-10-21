import sys; sys.path.insert(0, '..')
from alib import *
import tvlib, random

SCR = json.load(open('script.json'))
SUBS = {s['id']: s['disp'] for s in SCR}
def cq(sid, k): return cue(sid, min(k, len(SUBS[sid]) - 1))
OBS = SAGE; INT = LAV; DIS = ROSE; AMB = COR
CHAR = (116, 122, 140); JAY = (104, 150, 214); ELE = (150, 148, 140); CHIMP = (96, 78, 66); ORC = (92, 108, 132)
def ctr(): return (CONT[0] + CONT[2]) / 2
def P(a, b): return b if PORT else a
def A(t, t0, d=0.6): return ease((t - t0) / d)

def box(cv, bx, a, col, title=None, tsize=46):
    card(cv, bx, a, col)
    if title: cv.text((bx[0] + 30, bx[1] + 16), title, 'serif', tsize, col, 'la', a)

# ---------------------------------------------------------------- s1 title
def sc_title(cv, t, p):
    a = A(t, 0, 1.0); ty = P(120, 150)
    cv.text((W / 2, ty), 'HEARTBEAT TV  ·  ANIMALS  ·  EPISODE 1', 'sansb', P(34, 30), DIMC, 'ma', a)
    sz = P(116, 100)
    lines = ('Do animals understand death?',) if not PORT else ('Do animals', 'understand', 'death?')
    for k, l in enumerate(lines):
        cv.text((W / 2, ty + 66 + k * sz * 1.12), l, 'serif', sz, CREAM, 'ma', A(t, 0.2 + k * 0.2, 1.0), 5)
    y0 = P(430, 690); items = [(elephant, 'ELEPHANTS', ELE), (primate, 'APES & MONKEYS', CHIMP), (crow, 'CROWS & JAYS', CHAR), (orca, 'DOLPHINS & ORCAS', ORC)]
    cw = P(400, 460); ch = P(300, 230); gap = P(36, 30)
    for i, (fn, lab, col) in enumerate(items):
        a2 = A(t, [cq('s1', 0), cq('s1', 0) + 1.0, cq('s1', 1), cq('s1', 1) + 1.0][i])
        if PORT: bx = (50 + (i % 2) * (cw + gap), y0 + (i // 2) * (ch + gap), 50 + (i % 2) * (cw + gap) + cw, y0 + (i // 2) * (ch + gap) + ch)
        else: bx = (120 + i * (cw + gap), y0, 120 + i * (cw + gap) + cw, y0 + ch)
        card(cv, bx, a2, DIMC); cx = (bx[0] + bx[2]) / 2; cy = bx[1] + ch * 0.42
        if fn is elephant: elephant(cv, cx - 20, cy + 5, ch * 0.30, col, a2)
        elif fn is primate: primate(cv, cx, cy - 8, ch * 0.30, col, a2)
        elif fn is crow: crow(cv, cx - 5, cy + 5, ch * 0.34, col, a2)
        else: orca(cv, cx + 6, cy + 5, ch * 0.30, col, a2)
        cv.text((cx, bx[3] - P(52, 44)), lab, 'sansb', P(32, 30), CREAM, 'ma', a2)
    a3 = A(t, cq('s1', 3))
    ly = y0 + P(ch + 36, 2 * ch + gap + 12)
    tag(cv, W / 2 - P(330, 300), ly, 'obs', a3, 30); tag(cv, W / 2 + P(40, 10), ly, 'int', a3, 30)

# ---------------------------------------------------------------- s2 what would it mean
def glyph(cv, kind, cx, cy, s, col, a):
    c = mix(col, BG, a)
    if kind == 'perm':
        cv.line([(cx - s, cy), (cx + s * 0.8, cy)], c, 8); cv.poly([(cx + s, cy), (cx + s * 0.55, cy - s * 0.4), (cx + s * 0.55, cy + s * 0.4)], c)
        cv.line([(cx + s * 0.1, cy - s * 0.55), (cx + s * 0.1, cy + s * 0.55)], c, 8)
    elif kind == 'stop':
        pts = [(cx - s, cy), (cx - s * 0.5, cy), (cx - s * 0.35, cy - s * 0.7), (cx - s * 0.1, cy + s * 0.6), (cx + s * 0.1, cy), (cx + s, cy)]
        cv.line(pts, c, 7)
    elif kind == 'all':
        for r in range(2):
            for k in range(5): cv.circ((cx - s * 0.8 + k * s * 0.4, cy - s * 0.2 + r * s * 0.45), s * 0.12, c)
    else:
        cv.circ((cx - s * 0.28, cy - s * 0.15), s * 0.32, c); cv.circ((cx + s * 0.28, cy - s * 0.15), s * 0.32, c)
        cv.poly([(cx - s * 0.58, cy), (cx + s * 0.58, cy), (cx, cy + s * 0.7)], c)
def sc_parts(cv, t, p):
    x0, y0, x1, y1 = CONT; items = [('perm', 'It is permanent', OBS), ('stop', 'The body stops working', OBS), ('all', 'It happens to everything alive', OBS)]
    t0s = [cq('s2', 1), cq('s2', 2) - 0.3, cq('s2', 2) + 0.6]
    if PORT:
        h = 190; gap = 16; y = y0 + 4
        for i, (g, lab, col) in enumerate(items):
            a = A(t, t0s[i]); bx = (x0 + 10, y + i * (h + gap), x1 - 10, y + i * (h + gap) + h); card(cv, bx, a, col)
            glyph(cv, g, bx[0] + 110, (bx[1] + bx[3]) / 2, 60, col, a); cv.para(bx[0] + 240, bx[1] + 55, lab, 'serif', 44, CREAM, bx[2] - bx[0] - 270, 1.15, 'l', a)
        a = A(t, cq('s2', 3)); bx = (x0 + 10, y + 3 * (h + gap) + 10, x1 - 10, y + 3 * (h + gap) + 10 + 200); card(cv, bx, a, INT)
        glyph(cv, 'feel', bx[0] + 110, (bx[1] + bx[3]) / 2, 60, INT, a); cv.para(bx[0] + 240, bx[1] + 30, 'Separate question: do animals grieve?', 'serif', 44, CREAM, bx[2] - bx[0] - 270, 1.15, 'l', a)
        tag(cv, bx[0] + 240, bx[3] - 62, 'int', a, 24)
        cv.para(ctr(), y1 - 36, 'Behavior shows what an animal does, not what it knows or feels.', 'serifr', 34, AMB, x1 - x0 - 60, 1.2, 'm', A(t, cq('s2', 4)))
    else:
        w = 450; gap = 30; h = 360; ty = y0 + 20
        cv.text((x0 + 10, ty - 8), 'Parts researchers use when studying how children learn about death', 'sans', 28, DIMC, 'la', A(t, cq('s2', 1) - 0.4))
        for i, (g, lab, col) in enumerate(items):
            a = A(t, t0s[i]); bx = (x0 + i * (w + gap), ty + 40, x0 + i * (w + gap) + w - 20, ty + 40 + h - 40); card(cv, bx, a, col)
            glyph(cv, g, (bx[0] + bx[2]) / 2, bx[1] + 90, 70, col, a); cv.para((bx[0] + bx[2]) / 2, bx[1] + 190, lab, 'serif', 44, CREAM, bx[2] - bx[0] - 50, 1.15, 'm', a)
        a = A(t, cq('s2', 3)); bx = (x0 + 3 * (w + gap), ty + 40, x1, ty + 40 + h - 40); card(cv, bx, a, INT)
        glyph(cv, 'feel', (bx[0] + bx[2]) / 2, bx[1] + 90, 70, INT, a); cv.para((bx[0] + bx[2]) / 2, bx[1] + 165, 'Separate: do animals grieve?', 'serif', 38, CREAM, bx[2] - bx[0] - 50, 1.15, 'm', a)
        tag(cv, (bx[0] + bx[2]) / 2, bx[3] - 70, 'int', a, 24, 'm')
        cv.para(ctr(), y1 - 100, 'Behavior shows what an animal does, not what it knows or feels.', 'serifr', 46, AMB, x1 - x0 - 100, 1.2, 'm', A(t, cq('s2', 4)))

# ---------------------------------------------------------------- s3 elephants observed
def sc_ele(cv, t, p):
    x0, y0, x1, y1 = CONT
    if PORT: L = (x0, y0, x1, y0 + 440); R = (x0, y0 + 460, x1, y1)
    else: L = (x0, y0, x0 + 880, y1); R = (x0 + 920, y0, x1, y1)
    a = A(t, 0); box(cv, L, a, OBS, 'Samburu, Kenya (2006)', P(44, 42)); tag(cv, L[0] + 30, L[1] + 82, 'obs', a, 24)
    steps = [(cq('s3', 1), 'Eleanor, an old matriarch, collapses'), (cq('s3', 2), 'Grace comes, touches her with trunk and foot, then lifts her with her tusks'), (cq('s3', 4), 'Eleanor dies the next day'), (cq('s3', 5), 'Elephants from other families approach the body (some seen, others inferred from GPS)')]
    sy = L[1] + P(150, 140); lh = P(105, 68)
    for i, (tc, txt) in enumerate(steps):
        aa = A(t, tc); yy = sy + i * lh
        cv.circ((L[0] + 46, yy + 20), 14, mix(OBS, BG, aa))
        if i < 3: cv.line([(L[0] + 46, yy + 34), (L[0] + 46, yy + lh + 6)], mix(OBS, BG, 0.45 * aa), 4)
        cv.para(L[0] + 80, yy, txt, 'sans', P(36, 30), CREAM, L[2] - L[0] - 110, 1.12, 'l', aa)
    if not PORT:
        elephant(cv, L[0] + 250, L[3] - 70, 62, ELE, A(t, cq('s3', 2))); elephant(cv, L[0] + 560, L[3] - 70, 62, mix(ELE, BG, 0.8), A(t, cq('s3', 2)), flip=-1)
    a = A(t, cq('s3', 7) - 0.5); box(cv, R, a, OBS, 'Amboseli National Park (2006)', P(44, 40)); tag(cv, R[0] + 30, R[1] + 82, 'obs', a, 24)
    tiles = [('elephant skulls', 1.0), ('ivory', 0.92), ("other animals' skulls", 0.35), ('a log', 0.18)]
    gp = P(20, 14); tw = (R[2] - R[0] - 60 - 3 * gp) / 4
    base = R[3] - P(110, 100); mh = P(240, 140)
    for i, (lab, v) in enumerate(tiles):
        tc = cq('s3', 7) + 0.3 * i if i < 2 else cq('s3', 8) + 0.3 * (i - 2)
        aa = A(t, tc); bx = R[0] + 30 + i * (tw + gp); u = ease((t - cq('s3', 9)) / 1.2)
        hh = max(10, mh * v * u)
        col = OBS if v > 0.5 else DIMC
        cv.rect((bx, base - hh, bx + tw, base), mix(col, BG, aa), 8)
        cv.para(bx + tw / 2, base + 10, lab, 'sansb', P(26, 22), CREAM, tw + 10, 1.1, 'm', aa)
    cv.text((R[0] + 30, base - mh - P(44, 40)), 'time spent investigating (schematic)', 'sans', P(26, 24), DIMC, 'la', A(t, cq('s3', 9)))

# ---------------------------------------------------------------- s4 elephants interpretation
def sc_eleint(cv, t, p):
    x0, y0, x1, y1 = CONT; area = (x0, y0, x1, y1 - P(150, 200))
    left = ('Reading 1: grief', AMB, ['They recognize a lost individual', 'And they grieve'], ('INTERPRETATION', INT))
    right = ('Reading 2: interest', TEA, ["Simply interested in their own species' remains", 'That is not the same as knowing a death happened'], ('INTERPRETATION', INT))
    side_cards(cv, t, left, right, cq('s4', 1) - 0.3, cq('s4', 2) - 0.3, area, P(38, 33))
    a = A(t, cq('s4', 4)); cv.para(ctr(), y1 - P(140, 190), "Amboseli shows interest in their own kind's remains. It does not show that elephants grasp what death is.", 'serifr', P(38, 34), CREAM, x1 - x0 - 60, 1.2, 'm', a)
    a = A(t, cq('s4', 7)); badge(cv, ctr(), y1 - P(50, 60), 'IT CANNOT SETTLE WHICH READING IS RIGHT', DIS, a, P(26, 24), 'm')

# ---------------------------------------------------------------- s5 primates observed
def sc_prim(cv, t, p):
    x0, y0, x1, y1 = CONT
    cards = [('2010', 'Pansy, a safari park in Scotland', 'Her group groomed her as she was dying and inspected her body. Her daughter stayed near it overnight. For days afterward the group avoided the place where she died.', cq('s5', 1)),
             ('2010', 'Bossou, Guinea (wild chimpanzees)', 'Mothers carried their dead infants for weeks.', cq('s5', 5)),
             ('2006', 'Chacma baboons, Botswana', 'Females who lost a close relative to a predator had higher stress hormones, then groomed a wider circle of partners.', cq('s5', 6))]
    gap = 26
    for i, (yr, who, txt, tc) in enumerate(cards):
        a = A(t, tc - 0.2)
        if PORT: h = (y1 - y0 - gap * 2) / 3; bx = (x0, y0 + i * (h + gap), x1, y0 + i * (h + gap) + h)
        else: w = (x1 - x0 - gap * 2) / 3; bx = (x0 + i * (w + gap), y0, x0 + i * (w + gap) + w, y1)
        card(cv, bx, a, OBS)
        cv.text((bx[0] + 28, bx[1] + 14), yr, 'serif', P(96, 80), OBS, 'la', a)
        tx = bx[0] + 28; ty = bx[1] + P(125, 100)
        if PORT: tx = bx[0] + 250; ty = bx[1] + 16
        yy = cv.para(tx, ty, who, 'sansb', P(38, 32), CREAM, bx[2] - tx - 24, 1.12, 'l', a)
        cv.para(tx, yy + 6, txt, 'sans', P(34, 28), CREAM, bx[2] - tx - 24, 1.15, 'l', A(t, tc + 0.5))
        if PORT: tag(cv, bx[0] + 28, bx[1] + 108, 'obs', a, 22)
        else: tag(cv, bx[0] + 28, bx[3] - 58, 'obs', a, 22)
        if i < 2 and not PORT: primate(cv, bx[2] - 70, bx[1] + 64, 36, CHIMP, a)

# ---------------------------------------------------------------- s6 primate debate (venn)
def sc_primint(cv, t, p):
    x0, y0, x1, y1 = CONT
    r = P(225, 245); d = P(105, 150); cy = P(y0 + 345, y0 + 330); cx = W / 2
    a = A(t, cq('s6', 1) - 0.5)
    venn(cv, cx, cy, r, d, a)
    if A(t, cq('s6', 5)) > 0.02: cv.para(cx, cy - 55, 'Starting point: behavior changes after a death', 'sansb', P(26, 25), CREAM, 2 * (r - d) - 20, 1.15, 'm', A(t, cq('s6', 5)))
    rev = 'Gonçalves & Carvalho (2019): mostly single events; recognizing a body as dead is not the same as grasping permanence. Their conclusion: primates show an implicit awareness of death.'
    if PORT:
        lx = x0 + 10; rx = x0 + (x1 - x0) / 2 + 10; ww = (x1 - x0) / 2 - 30; by = y0 + 600
        for xx, ttl, body, col, tc, tc2 in ((lx, 'Critical review', rev, AMB, cq('s6', 1), cq('s6', 2)), (rx, 'Grief is a reasonable reading', 'Anthropologist Barbara King argues for it.', TEA, cq('s6', 6), cq('s6', 6))):
            aa = A(t, tc); yy = cv.para(xx, by, ttl, 'serif', 36, col, ww, 1.12, 'l', aa); cv.para(xx, yy + 8, body, 'sans', 27, CREAM, ww, 1.15, 'l', A(t, tc2))
        cv.para(ctr(), y1 - 60, 'A mother carrying an infant for weeks: deeply attached, or not reading the body as dead?', 'serifr', 30, INT, x1 - x0 - 80, 1.2, 'm', A(t, cq('s6', 5)))
    else:
        ww = cx - r - d - x0 - 40
        xx = x0 + 10
        yy = cv.para(xx, y0 + 20, 'Critical review', 'serif', 50, AMB, ww, 1.12, 'l', A(t, cq('s6', 1)))
        cv.para(xx, yy + 10, rev, 'sans', 29, CREAM, ww, 1.18, 'l', A(t, cq('s6', 2)))
        xx = cx + r + d + 40
        yy = cv.para(xx, y0 + 20, 'Grief is a reasonable reading', 'serif', 50, TEA, x1 - xx, 1.12, 'l', A(t, cq('s6', 6)))
        cv.para(xx, yy + 10, 'Anthropologist Barbara King argues for it.', 'sans', 32, CREAM, x1 - xx, 1.2, 'l', A(t, cq('s6', 6) + 0.4))
        cv.para(cx, y1 - 55, 'A mother carrying an infant for weeks: deeply attached, or not reading the body as dead?', 'serifr', 34, INT, 1300, 1.2, 'm', A(t, cq('s6', 5)))

# ---------------------------------------------------------------- s7 birds
def gather(cv, t, box_, t0, col, n=7, seed=3):
    r = random.Random(seed); cx = (box_[0] + box_[2]) / 2; cy = (box_[1] + box_[3]) / 2 + 20; s = min(box_[2] - box_[0], box_[3] - box_[1]) * 0.24
    crow(cv, cx, cy + s * 0.2, s * 1.0, mix(DIMC, BG, 0.7), 1.0, 1, True)
    for k in range(n):
        ang = k / n * 2 * math.pi + 0.4; R0 = s * 3.4; R1 = s * (1.5 + 0.2 * (k % 2))
        u = ease((t - t0 - k * 0.22) / 1.6); rr = R0 + (R1 - R0) * u
        bx = cx + rr * math.cos(ang) * 1.3; by = cy + rr * math.sin(ang) * 0.55 - s * 0.2
        bx = max(box_[0] + s, min(box_[2] - s, bx)); by = max(box_[1] + s * 0.8, min(box_[3] - s * 0.8, by))
        if u > 0.01: crow(cv, bx, by, s * 0.7, col, 1.0, 1 if bx < cx else -1)
def sc_birds(cv, t, p):
    x0, y0, x1, y1 = CONT; sh = P(450, 320)
    if PORT: B = [(x0, y0, x1, y0 + sh), (x0, y0 + sh + 14, x1, y0 + 2 * sh + 14)]
    else: B = [(x0, y0, x0 + 880, y0 + sh), (x0 + 920, y0, x1, y0 + sh)]
    spec = [('Scrub-jays, California (2012)', JAY, cq('s7', 1), 'Experiment: dead jays shown at feeders. The jays gathered, called loudly, and foraged less for about a day.', 11),
            ('American crows, Washington (2015)', CHAR, cq('s7', 5), 'Experiment: staged tests. Crows scolded, avoided feeding nearby, and learned to scold people seen near the dead crow.', 5)]
    for bx, (ttl, col, tc, txt, sd) in zip(B, spec):
        a = A(t, tc - 0.3); card(cv, bx, a, OBS); cv.text((bx[0] + 24, bx[1] + 12), ttl, 'sansb', P(32, 28), CREAM, 'la', a)
        tag(cv, bx[2] - 200 if PORT else bx[2] - 210, bx[1] + 14 if not PORT else bx[1] + 52, 'obs', a, 20)
        gather(cv, t, (bx[0] + 10, bx[1] + 70, bx[2] - 10, bx[1] + sh * 0.56), tc, col, 7, sd)
        cv.para(bx[0] + 24, bx[1] + sh * 0.62, txt, 'sans', P(30, 26), CREAM, bx[2] - bx[0] - 48, 1.15, 'l', A(t, tc + 1.2))
    iy = y0 + P(sh + 24, 2 * sh + 34)
    a = A(t, cq('s7', 3)); bx = (x0, iy, x1, y1 - 2)
    card(cv, bx, a, INT)
    tag(cv, bx[0] + 24, bx[1] + 14, 'int', a, 22)
    cv.para(bx[0] + 24, bx[1] + 62, 'The jay study used the word "funeral", but its results support another explanation: a dead bird is a warning of danger.', 'sans', P(32, 27), CREAM, bx[2] - bx[0] - 48, 1.15, 'l', A(t, cq('s7', 4)))
    badge(cv, bx[0] + 24, bx[3] - P(66, 56), 'MOURNING ON TOP OF THAT: UNKNOWN', DIS, A(t, cq('s7', 8)), P(26, 21))

# ---------------------------------------------------------------- s8 orca
def sc_orca(cv, t, p):
    x0, y0, x1, y1 = CONT
    lw = P(900, 1020)
    a = A(t, 0); sz = P(95, 62)
    orca(cv, x0 + P(250, 360), y0 + P(110, 62), sz, ORC, a)
    cv.text((x0 + P(250, 360), y0 + P(205, 126)), 'illustration', 'sans', 22, DIMC, 'ma', a * 0.8)
    cv.para(x0 + 10, y0 + P(240, 150), 'Reggente et al. 2016: cases of dolphins and whales supporting or carrying dead companions, often calves.', 'sans', P(30, 27), DIMC, lw - 20, 1.2, 'l', A(t, cq('s8', 1)))
    u2 = ease((t - cq('s8', 4)) / 1.8)
    ny = y0 + P(360, 240)
    cv.text((x0 + 20, ny), f'{int(round(17 * u2))}', 'serif', P(150, 110), AMB, 'la', A(t, cq('s8', 3)))
    cv.text((x0 + P(190, 140), ny + P(86, 62)), 'days, 2018', 'serifr', P(48, 40), CREAM, 'la', A(t, cq('s8', 3)))
    cv.text((x0 + 20, ny + P(150, 115)), f'~{int(round(1000 * u2)):,}', 'serif', P(110, 88), TEA, 'la', A(t, cq('s8', 4)))
    cv.text((x0 + P(440, 340), ny + P(186, 145)), 'miles', 'serifr', P(48, 40), CREAM, 'la', A(t, cq('s8', 4)))
    cv.text((x0 + 20, ny + P(300, 215)), 'Tahlequah, Southern Resident orca', 'sans', P(28, 26), DIMC, 'la', A(t, cq('s8', 3)))
    if PORT: rb = [(x0, y0 + 500, x1, y0 + 590), (x0, y0 + 604, x1, y1)]
    else: rb = [(x0 + 960, y0, x1, y0 + 250), (x0 + 960, y0 + 280, x1, y0 + 580)]
    a = A(t, cq('s8', 6)); card(cv, rb[0], a, OBS)
    if not PORT: tag(cv, rb[0][0] + 24, rb[0][1] + 14, 'obs', a, 24)
    else: tag(cv, x1 - 200, rb[0][1] + 28, 'obs', a, 22)
    cv.para(rb[0][0] + 24, rb[0][1] + P(76, 24), 'She carried the calf for 17 days.', 'serif', P(46, 36), CREAM, rb[0][2] - rb[0][0] - P(48, 250), 1.15, 'l', a)
    a = A(t, cq('s8', 7)); card(cv, rb[1], a, INT); tag(cv, rb[1][0] + 24, rb[1][1] + 14, 'int', a, 24)
    cv.para(rb[1][0] + 24, rb[1][1] + P(76, 66), 'Grief, or an instinct to keep a calf at the surface, or both.', 'serif', P(42, 38), CREAM, rb[1][2] - rb[1][0] - 48, 1.15, 'l', a)
    badge(cv, rb[1][0] + 24, rb[1][3] - P(66, 70), 'THE OBSERVATIONS DO NOT SAY WHICH', DIS, A(t, cq('s8', 8)), P(26, 24))

# ---------------------------------------------------------------- s9 ladder
def sc_ladder(cv, t, p):
    x0, y0, x1, y1 = CONT
    rows = [('Many studied species notice and react to dead companions', 'WELL SUPPORTED', OBS, cq('s9', 1)), ('They touch, guard, carry or avoid them', 'WELL SUPPORTED', OBS, cq('s9', 2)),
            ('Stress changes after a loss', 'SOME SPECIES', AMB, cq('s9', 3)), ('They know that death is permanent', 'NOT ESTABLISHED', DIS, cq('s9', 4)),
            ('They know that it comes to everyone', 'NOT ESTABLISHED', DIS, cq('s9', 5)), ('What they feel is grief as people know it', 'NOT ESTABLISHED', DIS, cq('s9', 5) + 1.2)]
    rh = P(78, 106); yy = y0 + P(0, 6); g = P(8, 8)
    for i, (lab, st, col, tc) in enumerate(rows):
        a = A(t, tc); y = yy + i * (rh + g)
        card(cv, (x0, y, x1, y + rh), a, col, 14)
        if PORT:
            cv.para(x0 + 20, y + 10, lab, 'sans', 32, CREAM, x1 - x0 - 40, 1.08, 'l', a); badge(cv, x0 + 20, y + rh - 44, st, col, a, 20)
        else:
            cv.text((x0 + 30, y + rh / 2 - 22), lab, 'sansb', 36, CREAM, 'la', a); badge(cv, x1 - 360, y + rh / 2 - 26, st, col, a, 26)
    ya = yy + 6 * (rh + g) + P(34, 44)
    cv.text((W / 2, ya), 'The behavior is real. The meaning is open.', 'serif', P(64, 48), CREAM, 'ma', A(t, cq('s9', 6)))

# ---------------------------------------------------------------- s10 traps
def sc_traps(cv, t, p):
    x0, y0, x1, y1 = CONT
    by = y0 + P(330, 330); bx0 = x0 + 40; bx1 = x1 - 40; bw = bx1 - bx0
    a = A(t, 0.3)
    cv.rect((bx0, by - 10, bx1, by + 10), mix(DIMC, BG, 0.55 * a), 10)
    cv.rect((bx0 + bw * 0.38, by - 22, bx0 + bw * 0.62, by + 22), mix(OBS, BG, 0.9 * A(t, cq('s10', 6))), 12)
    cv.circ((bx0, by), 16, mix(AMB, BG, A(t, cq('s10', 1)))); cv.circ((bx1, by), 16, mix(TEA, BG, A(t, cq('s10', 4))))
    cv.text((W / 2, by + 36), 'careful science', 'sansb', P(32, 30), OBS, 'ma', A(t, cq('s10', 6)))
    if t > cq('s10', 1):
        ph = 0.5 + 0.5 * math.sin((t - cq('s10', 1)) * 0.7)
        if A(t, cq('s10', 6)) < 0.5: cv.ring((bx0 + bw * ph, by), 12, mix(CREAM, BG, 0.8), 4)
    ww = P(820, 960); lx = bx0 - 10
    a = A(t, cq('s10', 1))
    yy = cv.para(lx, y0 + 10, 'Trap 1: anthropomorphism', 'serif', P(48, 44), AMB, ww, 1.1, 'l', a)
    cv.para(lx, yy + 6, 'Reading human feelings into every report.', 'sans', P(34, 31), CREAM, ww, 1.18, 'l', a)
    cv.para(lx, by + P(100, 100), 'A caution, not a measured result: striking cases get shared, while animals that ignore a body rarely make the news.', 'sans', P(32, 29), DIMC, ww, 1.2, 'l', A(t, cq('s10', 2)))
    a = A(t, cq('s10', 4))
    if PORT:
        ry = by + 330
        yy = cv.para(lx, ry, 'Trap 2: anthropodenial', 'serif', 44, TEA, ww, 1.1, 'l', a)
        cv.para(lx, yy + 6, "Frans de Waal's word for refusing to see anything in animals that people also have.", 'sans', 31, CREAM, ww, 1.18, 'l', A(t, cq('s10', 5)))
    else:
        rx = x1 - 40 - ww
        yy = cv.para(rx, y0 + 10, 'Trap 2: anthropodenial', 'serif', 48, TEA, ww, 1.1, 'l', a)
        cv.para(rx, yy + 6, "Frans de Waal's word for refusing to see anything in animals that people also have.", 'sans', 34, CREAM, ww, 1.18, 'l', A(t, cq('s10', 5)))

# ---------------------------------------------------------------- s11 what would settle it
def sc_settle(cv, t, p):
    x0, y0, x1, y1 = CONT
    items = [('Compare responses to the dead, the dying, the sleeping and the sedated, recorded the same way each time', cq('s11', 1)),
             ('Long-term field records that include the times nothing happens', cq('s11', 3)),
             ('Hormone measures across many deaths', cq('s11', 4)),
             ('Tests that separate smell and curiosity from attachment', cq('s11', 5))]
    y = y0 + P(10, 20); sz = P(40, 36)
    for i, (txt, tc) in enumerate(items):
        a = A(t, tc); checkbox(cv, x0 + 20, y + 4, 46, a)
        yy = cv.para(x0 + 100, y, txt, 'sans', sz, CREAM, x1 - x0 - 130, 1.18, 'l', a)
        y = max(yy, y + 62) + P(34, 44)
    cv.para(ctr(), y1 - P(120, 190), 'Researchers have proposed approaches like these. They are hard, and no animal should be harmed to find out.', 'serifr', P(40, 36), AMB, x1 - x0 - 80, 1.2, 'm', A(t, cq('s11', 6)))

# ---------------------------------------------------------------- s12 close
def sc_close(cv, t, p):
    x0, y0, x1, y1 = CONT
    badge(cv, W / 2, y0 + P(40, 50), 'NOT ESTABLISHED', DIS, A(t, cq('s12', 0)), P(54, 50), 'm')
    lines = [(cq('s12', 1), 'Some species clearly react to death.', CREAM, 'serif'), (cq('s12', 2), 'Whether they understand it the way a person does is still open.', AMB, 'serifr')]
    statements(cv, t, lines, y0 + P(190, 220))
    a = A(t, cq('s12', 3)); cs = P(300, 230); yy = y1 - P(110, 160)
    for i, fn in enumerate((elephant, primate, crow, orca)):
        cx = W / 2 + (i - 1.5) * cs; col = (ELE, CHIMP, CHAR, ORC)[i]
        if fn is elephant: elephant(cv, cx, yy, 50, col, a * 0.9)
        elif fn is primate: primate(cv, cx, yy - 10, 48, col, a * 0.9)
        elif fn is crow: crow(cv, cx, yy, 54, col, a * 0.9)
        else: orca(cv, cx, yy, 52, col, a * 0.9)

SOURCES = ['Elephants: Douglas-Hamilton et al., Applied Animal Behaviour Science (2006) · McComb, Baker & Moss, Biology Letters (2006)',
 'Primates: Anderson, Gillies & Lock, Current Biology (2010) · Biro et al., Current Biology (2010) · Engh et al., Proc. R. Soc. B (2006)',
 'Gonçalves & Carvalho, Biological Reviews (2019) · King, How Animals Grieve (2013) · de Waal, Philosophical Topics (1999)',
 'Birds: Iglesias, McElreath & Patricelli, Animal Behaviour (2012) · Swift & Marzluff, Animal Behaviour (2015)',
 'Dolphins and whales: Reggente et al., Journal of Mammalogy (2016) · Center for Whale Research, Tahlequah (2018)']
def sc_end(cv, t, p):
    a = A(t, 0, 1.0); cy = P(90, 190)
    cv.text((W / 2, cy), 'Heartbeat Observatory', 'serif', P(100, 84), CREAM, 'ma', a)
    cv.text((W / 2, cy + P(135, 130)), 'heartbeatobservatory.com', 'sansb', 52, AMB, 'ma', a)
    cv.text((W / 2, cy + 215), 'Animals · Episode 1 · sources checked October 2026', 'sans', P(34, 30), DIMC, 'ma', a)
    y = cy + 290; cv.text((W / 2, y), 'Sources', 'sansb', 32, DIMC, 'ma', A(t, 0.6, 1))
    yy = y + 50
    for i, s in enumerate(SOURCES):
        yy = cv.para(W / 2, yy, s, 'sans', P(28, 27), CREAM, P(1700, 980), 1.2, 'm', A(t, 0.8 + i * 0.2, 0.8)) + 8
    cv.text((W / 2, yy + 20), 'Made with AI by Heartbeat Observatory', 'sans', 30, DIMC, 'ma', A(t, 2.5, 0.8))

SCENES = [
 ('s1', '', '', sc_title),
 ('s2', 'What would it mean?', 'Parts used in studies of how children learn about death (Speece & Brent, 1984). Field: comparative thanatology.', sc_parts),
 ('s3', 'Elephants: what was seen', 'Sources: Douglas-Hamilton et al., Appl. Anim. Behav. Sci. (2006); McComb, Baker & Moss, Biology Letters (2006).', sc_ele),
 ('s4', 'Elephants: two readings', 'Source: McComb, Baker & Moss, Biology Letters (2006). The readings are interpretations, not findings.', sc_eleint),
 ('s5', 'Primates: what was seen', 'Sources: Anderson, Gillies & Lock (2010); Biro et al. (2010), Current Biology; Engh et al., Proc. R. Soc. B (2006).', sc_prim),
 ('s6', 'Primates: where scientists disagree', 'Sources: Gonçalves & Carvalho, Biological Reviews (2019); King, How Animals Grieve (2013).', sc_primint),
 ('s7', 'Crows and jays', 'Sources: Iglesias, McElreath & Patricelli, Animal Behaviour (2012); Swift & Marzluff, Animal Behaviour (2015). Birds drawn schematically.', sc_birds),
 ('s8', 'Dolphins and orcas', 'Sources: Reggente et al., Journal of Mammalogy (2016); Center for Whale Research reports on Tahlequah (J35), 2018.', sc_orca),
 ('s9', 'What is and is not established', 'Summary of the studies above.', sc_ladder),
 ('s10', 'Two traps', 'Source: de Waal, "Anthropomorphism and anthropodenial", Philosophical Topics (1999).', sc_traps),
 ('s11', 'What would settle it', 'Research directions proposed in the comparative thanatology literature.', sc_settle),
 ('s12', '', '', sc_close),
 ('s13', '', '', sc_end),
]
configure(SUBS, SCENES)
if __name__ == '__main__': main()
