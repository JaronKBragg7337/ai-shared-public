# ---------------------------------------------------------------- shared
import random
BLUE = (96, 160, 230)

def cue(sid, k):
    subs = SUBS[sid]; tot = sum(len(s) for s in subs); acc = sum(len(s) for s in subs[:k])
    return SEG[sid]['start'] + acc / tot * SEG[sid]['dur'] - BOUND[sid][0]

def pump(cv, c, r=9, a=1.0, t=0.0, ring=True):
    if ring:
        for k in range(2):
            ph = ((t * 0.8 + k * 0.5) % 1.0)
            rr = r + ph * 46
            cv.d.ellipse([(c[0] - rr) * SS, (c[1] - rr) * SS, (c[0] + rr) * SS, (c[1] + rr) * SS],
                         outline=mix(AMBER, BG, (1 - ph) * 0.9 * a), width=int(3 * SS))
    cv.circ(c, r + 4, BG); cv.circ(c, r, mix(AMBER, BG, a))
    cv.circ(c, r * 0.4, BG)

# ---------------------------------------------------------------- schematic Soho map (units 0..100 x 0..62)
HST = [('Oxford St', 5, (0, 100)), ('', 18, (4, 96)), ('Broad St', 31, (6, 94)), ('', 45, (4, 96)), ('', 57, (6, 94))]
VST = [('', 8, (5, 57)), ('Poland St', 28, (5, 57)), ('Cambridge St', 56, (5, 57)), ('', 76, (5, 57)), ('', 92, (5, 57))]
PUMPU = (56, 31)
OTHERP = [(14, 12), (84, 12), (14, 50), (84, 50), (40, 57), (68, 18)]

def soho_map(box):
    bw, bh = box[2] - box[0], box[3] - box[1]
    sc = min(bw / 100.0, bh / 62.0); ox = box[0] + (bw - 100 * sc) / 2; oy = box[1] + (bh - 62 * sc) / 2
    return (lambda x, y: (ox + x * sc, oy + y * sc)), sc

def draw_streets(cv, mp, sc, labels=True, a=1.0):
    col = mix((70, 92, 128), BG, a)
    for nm, y, (x0, x1) in HST:
        cv.line([mp(x0, y), mp(x1, y)], col, max(3, 0.9 * sc))
    for nm, x, (y0, y1) in VST:
        cv.line([mp(x, y0), mp(x, y1)], col, max(3, 0.9 * sc))
    if labels:
        cv.text((mp(58.8, 6.0)[0], mp(58.8, 6.0)[1]), 'Oxford St', 'sans', 24, DIM, 'la', a)
        cv.text((mp(9.5, 31)[0], mp(9.5, 31)[1] - 34), 'Broad St', 'sans', 26, DIM, 'la', a)
        cv.text((mp(28, 5)[0] + 8, mp(28, 5)[1] + 24), 'Poland St', 'sans', 24, DIM, 'la', a)

_rng = random.Random(1854)
def gen_dots(n=210):
    segs = [('h', y, x0, x1) for _, y, (x0, x1) in HST] + [('v', x, y0, y1) for _, x, (y0, y1) in VST]
    out = []
    while len(out) < n:
        s = _rng.choice(segs); u = _rng.random()
        if s[0] == 'h': x, y = s[2] + (s[3] - s[2]) * u, s[1] + _rng.uniform(-0.9, 0.9)
        else: x, y = s[1] + _rng.uniform(-0.9, 0.9), s[2] + (s[3] - s[2]) * u
        d = math.hypot(x - PUMPU[0], (y - PUMPU[1]) * 1.1)
        if _rng.random() < math.exp(-d * d / (2 * 12.0 ** 2)) * 0.95 + 0.012: out.append((x, y))
    _rng.shuffle(out); return out
DOTS = gen_dots()

# ---------------------------------------------------------------- scenes
def sc_title(cv, t, p):
    a = ease(t / 1.2)
    mb = (CONT[0], 450 if PORT else 330, CONT[2], 1200 if PORT else 960)
    mp, sc = soho_map(mb); draw_streets(cv, mp, sc, False, a * 0.45)
    for i, (x, y) in enumerate(DOTS[:120]):
        k = ease((t - 0.6 - i * 0.015) / 0.4)
        if k > 0: cv.circ(mp(x, y), 4, mix(RED, BG, k * 0.55))
    pump(cv, mp(*PUMPU), 9, a, t)
    cv.text((W / 2, 150 if PORT else 36), 'HEARTBEAT TV  ·  HISTORY  ·  EPISODE 2', 'sansb', 34 if PORT else 36, AMBER, 'ma', a)
    for k, l in enumerate(('The map that', 'beat a theory')):
        cv.text((W / 2, (230 if PORT else 90) + k * (110 if PORT else 128)), l, 'serif', 96 if PORT else 112, TXT, 'ma', ease((t - 0.2) / 1.2), 6)
    cv.text((W / 2, 1330 if PORT else 960), 'London · 1854 · Broad Street', 'serifr', 44, DIM, 'ma', ease((t - 1.0) / 1.0))

def sc_outbreak(cv, t, p):
    if PORT: c = (W / 2, CONT[1] + 200); R = 160; cx, cy = W / 2, CONT[1] + 560
    else: c = (CONT[0] + 330, CONT[1] + 330); R = 250; cx, cy = CONT[0] + 820, CONT[1] + 20
    c2 = cue('s2', 2)
    ca = ease((t - 0.3) / 0.8)
    for rr, al in ((R, 0.9), (R * 0.66, 0.5), (R * 0.33, 0.3)):
        cv.d.ellipse([(c[0] - rr) * SS, (c[1] - rr) * SS, (c[0] + rr) * SS, (c[1] + rr) * SS], outline=mix(STEEL, BG, al * ca), width=int(2 * SS))
    rg = random.Random(7)
    for i in range(220):
        ang = rg.uniform(0, 6.283); d = min(abs(rg.gauss(0, 0.5)), 0.97)
        kk = ease((t - c2 - i * 0.012) / 0.3)
        if kk > 0: cv.circ((c[0] + math.cos(ang) * d * R, c[1] + math.sin(ang) * d * R), 4, mix(RED, BG, 0.85 * kk))
    pump(cv, c, 9, ca, t)
    cv.text((c[0], c[1] + R + 14), '≈ 250 yards', 'sansb', 34, AMBER, 'ma', ease((t - c2) / 1.4))
    m = ease((t - 0.4) / 0.8) * (1 - 0.65 * ease((t - c2) / 0.8))
    if PORT: bx = (60, CONT[3] - 150, W - 60, CONT[3] - 20)
    else: bx = (cx, cy + 520, CONT[2] - 20, cy + 650)
    cv.rect(bx, mix(STEEL, BG, 0.28 * m), 16)
    cv.text(((bx[0] + bx[2]) / 2, bx[1] + 20), 'The accepted theory: “miasma”', 'sansb', 36, TXT, 'ma', m)
    cv.text(((bx[0] + bx[2]) / 2, bx[1] + 70), 'bad air from filth and rot', 'sans', 34, DIM, 'ma', m)
    n = int(500 * ease((t - c2) / 2.4))
    if PORT: tx, ty, an = W / 2, CONT[1] + 420, 'ma'
    else: tx, ty, an = cx, cy + 120, 'la'
    if t > c2 - 0.2:
        cv.text((tx, ty), f'{n}+' if n >= 500 else str(n), 'serif', 170 if not PORT else 150, AMBER, an)
        cv.text((tx, ty + (190 if not PORT else 170)), 'fatal attacks in ten days', 'sansb', 40, TXT, an)
        cv.text((tx, ty + (245 if not PORT else 225)), 'within ~250 yards of the pump', 'sans', 32, DIM, an)

def sc_map(cv, t, p):
    if PORT: mb = (CONT[0], CONT[1] - 10, CONT[2], CONT[1] + 470)
    else: mb = (CONT[0], CONT[1], CONT[0] + 1130, CONT[3])
    mp, sc = soho_map(mb); draw_streets(cv, mp, sc)
    for (x, y) in OTHERP:
        c = mp(x, y)
        cv.d.ellipse([(c[0] - 8) * SS, (c[1] - 8) * SS, (c[0] + 8) * SS, (c[1] + 8) * SS], outline=BLUE, width=int(3 * SS))
    cv.text(mp(0, 60.5), '○ other pumps', 'sans', 26, BLUE, 'la', 1.0)
    t0, t1 = 0.8, cue('s3', 2) - 0.3
    for i, (x, y) in enumerate(DOTS):
        k = ease((t - t0 - (t1 - t0) * i / len(DOTS)) / 0.3)
        if k > 0: cv.circ(mp(x, y), 6 if not PORT else 5, mix(RED, BG, k))
    pa = ease((t - cue('s3', 1)) / 0.6)
    pump(cv, mp(*PUMPU), 10, 1.0, t, ring=t > cue('s3', 1))
    cv.text((mp(*PUMPU)[0] + 24, mp(*PUMPU)[1] + 20), 'Broad St pump', 'sansb', 30, AMBER, 'la', pa, 4)
    cv.text(mp(100, 60.5), '● one mark per death (schematic)', 'sans', 26, DIM, 'ra', 1.0)
    if PORT: x0, y0, pw = 60, CONT[1] + 520, 400
    else: x0, y0, pw = CONT[0] + 1180, CONT[1] + 40, CONT[2] - CONT[0] - 1180
    rows = [(cue('s3', 2), '83', 'deaths Snow checked', TXT), (cue('s3', 2) + 1.0, '10', 'lived nearer a different pump', AMBER),
            (cue('s3', 3), '5', 'of those families sent to Broad St for water', AMBER), (cue('s3', 4), '3', 'were children at a school beside it', AMBER)]
    rh = 150 if not PORT else 150
    for i, (tc, num, lab, col) in enumerate(rows):
        a = ease((t - tc) / 0.6)
        if a <= 0: continue
        if PORT: xx, y = x0 + (i % 2) * 510, y0 + (i // 2) * 175
        else: xx, y = x0, y0 + i * rh
        cv.text((xx, y), num, 'serif', 100 if not PORT else 90, col, 'la', a)
        cv.para(xx + (170 if not PORT else 130), y + (14 if not PORT else 8), lab, 'sansb', 36 if not PORT else 30, TXT, (pw - 180) if not PORT else 340, 1.12, 'l', a)

def sc_outliers(cv, t, p):
    cards = [
        (cue('s4', 1), 'Poland Street workhouse', '5 of 535', 'inmates died of cholera', 'Had its own well. (Some accounts say 530 inmates.)', 'work'),
        (cue('s4', 2), 'Broad Street brewery', '0 severe', 'among 70+ workers', 'Drank the malt liquor they were given, not water.', 'brew'),
        (cue('s4', 3), 'Hampstead widow, age 59', '1 death', 'far from Soho', 'Pump water brought by cart. Died Sept 2.', 'wid')]
    if PORT:
        boxes = [(40, CONT[1] + 0 + i * 297, W - 40, CONT[1] + 287 + i * 297) for i in range(3)]
    else:
        gw = (CONT[2] - CONT[0] - 80) / 3
        boxes = [(CONT[0] + i * (gw + 40), CONT[1] + 10, CONT[0] + i * (gw + 40) + gw, CONT[3] - 10) for i in range(3)]
    if t < cue('s4', 1) + 0.6:
        cv.text((W / 2, CONT[1] + (300 if not PORT else 330)), 'Who should have died, and did not?', 'serif', 66 if not PORT else 58, TXT, 'ma', ease((t - 0.2) / 0.8) * (1 - ease((t - cue('s4', 1)) / 0.6)))
    for (tc, ttl, big, l1, l2, kind), b in zip(cards, boxes):
        a = ease((t - tc) / 0.7)
        if a <= 0: continue
        cv.rect(b, mix(BG2, BG, a), 18); cv.outline(b, mix(STEEL, BG, 0.5 * a), 2, 18)
        pad = 28
        cv.text((b[0] + pad, b[1] + 20), ttl, 'sansb', 34, AMBER, 'la', a)
        if PORT:
            cv.text((b[0] + pad, b[1] + 72), big, 'serif', 84, TXT, 'la', a)
            cv.text((b[0] + pad, b[1] + 170), l1, 'sans', 32, TXT, 'la', a)
            cv.para(b[0] + pad, b[1] + 212, l2, 'sans', 26, DIM, 540, 1.15, 'l', a)
            gx0, gy0 = b[0] + 590, b[1] + 80; gw_, gh_ = b[2] - b[0] - 620, 150
        else:
            cv.text((b[0] + pad, b[1] + 78), big, 'serif', 76, TXT, 'la', a)
            cv.text((b[0] + pad, b[1] + 172), l1, 'sans', 34, TXT, 'la', a)
            cv.para(b[0] + pad, b[1] + 222, l2, 'sans', 30, DIM, b[2] - b[0] - 2 * pad, 1.15, 'l', a)
            gx0, gy0 = b[0] + pad, b[1] + 390; gw_, gh_ = b[2] - b[0] - 2 * pad, 220
        if kind == 'work':
            n = 535; cols = 40 if not PORT else 36; cell = gw_ / cols; r = max(1.8, cell * 0.33)
            rg = random.Random(3); red = set(rg.sample(range(n), 5))
            for i in range(n):
                cx_ = gx0 + (i % cols + 0.5) * cell; cy_ = gy0 + (i // cols + 0.5) * cell * 0.85
                cv.circ((cx_, cy_), r * (1.5 if i in red else 1), mix(RED if i in red else STEEL, BG, a * (1 if i in red else 0.8)))
        elif kind == 'brew':
            n = 70; cols = 14 if not PORT else 18; cell = gw_ / cols
            for i in range(n):
                cv.circ((gx0 + (i % cols + 0.5) * cell, gy0 + (i // cols + 0.5) * cell * 0.9), max(3, min(cell * 0.3, 11)), mix(TEAL, BG, 0.85 * a))
        else:
            y = gy0 + gh_ * 0.4
            a0, a1 = (gx0 + 30, y), (gx0 + gw_ - 50, y)
            k = ease((t - tc - 0.8) / 1.2)
            cv.line([a0, (a0[0] + (a1[0] - a0[0]) * k, y)], mix(AMBER, BG, a * 0.8), 4)
            cv.circ(a0, 10, mix(AMBER, BG, a)); cv.text((a0[0], y + 22), 'Soho', 'sans', 26, DIM, 'ma', a)
            cv.circ(a1, 10, mix(RED, BG, a * ease((k - 0.9) / 0.1))); cv.text((a1[0], y + 22), 'Hampstead', 'sans', 26, DIM, 'ma', a)

def sc_handle(cv, t, p):
    x0 = CONT[0] + 30; x1 = CONT[2] - 30; w = x1 - x0
    ca = ease((t - 0.3) / 0.6); cb = ease((t - cue('s5', 1)) / 0.6)
    ch = 90; gap = 24
    if PORT:
        bs = [(x0, CONT[1] + 6, x1, CONT[1] + 6 + ch), (x0, CONT[1] + 6 + ch + gap, x1, CONT[1] + 6 + 2 * ch + gap)]; top = CONT[1] + 2 * ch + 2 * gap + 30
    else:
        hw = (w - gap) / 2
        bs = [(x0, CONT[1] + 6, x0 + hw, CONT[1] + 6 + ch), (x0 + hw + gap, CONT[1] + 6, x1, CONT[1] + 6 + ch)]; top = CONT[1] + ch + 40
    for (b, a, d, txt, col) in ((bs[0], ca, 'Sept 7', 'Snow to parish Board of Guardians', STEEL), (bs[1], cb, 'Sept 8', 'Pump handle removed', RED)):
        if a <= 0: continue
        cv.rect(b, mix(col, BG, 0.42 * a), 14)
        cv.text((b[0] + 24, (b[1] + b[3]) / 2), d, 'serif', 44, TXT, 'lm', a)
        cv.text((b[0] + 200, (b[1] + b[3]) / 2), txt, 'sansb', 33 if not PORT else 32, TXT, 'lm', a)
    cs = cue('s5', 2)
    ha = ease((t - cs) / 0.7)
    if ha <= 0: return
    cb_ = CONT[3] - 70
    cv.text((x0, top + 6), 'Cholera attacks per day, Sept 1854', 'sansb', 34, TXT, 'la', ha)
    slot = w / 12.0
    vals = {1: 143, 2: 116, 3: 54, 8: 12, 9: 11, 10: 5, 11: 5, 12: 1}
    chart_top = top + (220 if not PORT else 230)
    sc_ = (cb_ - chart_top - 40) / 143.0
    cv.line([(x0, cb_), (x1, cb_)], mix(DIM, BG, ha), 2)
    for d in range(1, 13):
        xc = x0 + (d - 0.5) * slot
        cv.text((xc, cb_ + 8), str(d), 'sans', 26, DIM, 'ma', ha)
        if d in vals:
            tc = cue('s5', 3) + (0.0 if d <= 3 else (1.0 if d == 8 else 1.2 + 0.2 * (d - 9)))
            k = ease((t - tc) / 0.6)
            if k > 0:
                hgt = max(3, vals[d] * sc_) * k
                cv.rect((xc - slot * 0.34, cb_ - hgt, xc + slot * 0.34, cb_), RED if d == 8 else AMBER, 4)
                if k > 0.9: cv.text((xc, cb_ - hgt - 40), str(vals[d]), 'sansb', 32, TXT, 'ma')
    if t > cue('s5', 3) + 1.0:
        cv.text((x0 + 5.5 * slot, cb_ - 70), '4–7: not shown', 'sans', 26, DIM, 'ma', 0.9)
    cv.text((x1, cb_ + 44), 'September', 'sans', 26, DIM, 'ra', ha)
    da = ease((t - cue('s5', 4)) / 0.6)
    if da > 0:
        bb = (x0, top + 56, x1, top + 200) if PORT else (x0 + w * 0.42, top + 40, x1, top + 190)
        cv.rect(bb, mix(AMBER, BG, 0.16 * da), 14); cv.outline(bb, mix(AMBER, BG, 0.9 * da), 3, 14)
        cv.text((bb[0] + 24, bb[1] + 16), 'DISPUTED', 'sansb', 30, AMBER, 'la', da)
        cv.para(bb[0] + 24, bb[1] + 56, 'Cases were already falling and many had fled. How much did the handle matter?', 'sans', 30, TXT, bb[2] - bb[0] - 48, 1.15, 'l', da)

def sc_water(cv, t, p):
    x0 = CONT[0] + 30; x1 = CONT[2] - 30; w = x1 - x0
    ry = CONT[1] + (70 if not PORT else 110)
    ra = ease(t / 0.8)
    cv.rect((x0, ry - 28, x1, ry + 28), mix((30, 70, 120), BG, 0.7 * ra), 28)
    cv.text((x0 + 24, ry), 'Thames  →', 'sansb', 28, TXT, 'lm', ra)
    sx = x0 + w * 0.5
    ia = ease((t - cue('s6', 1)) / 0.7)
    if ia > 0:
        cv.circ((sx, ry), 12, mix((150, 110, 70), BG, ia)); cv.text((sx, ry + 40), 'sewage out', 'sans', 26, DIM, 'ma', ia)
        lx = x0 + w * 0.22; vx = x0 + w * 0.8
        cv.circ((lx, ry), 12, mix(TEAL, BG, ia)); cv.text((lx, ry - 70), 'Lambeth intake', 'sansb', 28, TEAL, 'ma', ia)
        cv.circ((vx, ry), 12, mix(RED, BG, ia)); cv.text((vx, ry - 70), 'S&V intake', 'sansb', 28, RED, 'ma', ia)
    cv.text((x0, ry + 90), 'Each company served rich and poor, large houses and small.', 'sans', 30, DIM, 'la', ease((t - cue('s6', 2)) / 0.7))
    top = ry + (215 if not PORT else 230); bh = 100; stp = 112 if not PORT else 160
    cv.text((x0, top - 60), 'Cholera deaths per 10,000 houses, 1854', 'sansb', 36, TXT, 'la', ease((t - cue('s6', 3) + 0.3) / 0.7))
    rows = [('Southwark & Vauxhall', 315, RED, '1,263 deaths · 40,046 houses', cue('s6', 3)), ('Lambeth', 37, TEAL, '98 deaths · 26,107 houses', cue('s6', 4)),
            ('Rest of London', 59, STEEL, '1,422 deaths · 256,423 houses', cue('s6', 4) + 1.5)]
    for i, (nm, v, col, sub, tc) in enumerate(rows):
        a = ease((t - tc) / 0.5); k = ease((t - tc - 0.2) / 1.2)
        if a <= 0: continue
        y = top + i * stp + 20
        cv.text((x0, y - 4), nm, 'sansb', 34, TXT, 'la', a)
        cv.text((x1, y - 2), sub, 'sans', 28, DIM, 'ra', a)
        by = y + 46; bw_ = max(6, (w - 150) * v / 315.0 * k)
        cv.rect((x0, by, x1, by + 50), mix(STEEL, BG, 0.15 * a), 8)
        cv.rect((x0, by, x0 + bw_, by + 50), col, 8)
        cv.text((x0 + bw_ + 16, by + 25), str(int(v * k)), 'serif', 50, TXT, 'lm', a)
    if t > cue('s6', 4) + 1.0:
        cv.text((x1, (top - 62) if not PORT else (top + 3 * stp + 10)), '315 ÷ 37 ≈ 8.5×', 'sansb', 42, AMBER, 'ra', ease((t - cue('s6', 4) - 1.0) / 0.6))

def sc_after(cv, t, p):
    ev = [(cue('s7', 1), '1855', 'A government committee rejects Snow’s water idea', 'General Board of Health', RED),
          (cue('s7', 2), '1854', 'Filippo Pacini sees the cholera bacterium in Florence', 'Almost no one notices', BLUE),
          (cue('s7', 3), '1866', 'William Farr gives up miasma for cholera', 'after the East London outbreak', AMBER),
          (cue('s7', 4), '1883', 'Robert Koch identifies the bacterium', 'Vibrio cholerae', TEAL)]
    order = {'1854': 0, '1855': 1, '1866': 2, '1883': 3}
    x0 = CONT[0] + 40; x1 = CONT[2] - 40
    if PORT:
        y0 = CONT[1] + 30; step = 205
        cv.line([(x0 + 100, y0 + 20), (x0 + 100, y0 + 3 * step + 40)], mix(STEEL, BG, 0.7), 4)
    else:
        ay = CONT[1] + 300
        cv.line([(x0, ay), (x1, ay)], mix(STEEL, BG, 0.7), 4)
    for (tc, yr, txt, sub, col) in ev:
        a = ease((t - tc) / 0.7)
        if a <= 0: continue
        i = order[yr]
        if PORT:
            y = y0 + i * step
            cv.circ((x0 + 100, y + 20), 14, mix(col, BG, a))
            cv.text((x0 + 130, y - 20), yr, 'serif', 70, col, 'la', a)
            cv.para(x0 + 380, y - 8, txt, 'sansb', 36, TXT, x1 - x0 - 400, 1.15, 'l', a)
            cv.text((x0 + 380, y + 118), sub, 'sans', 30, DIM, 'la', a)
        else:
            xc = x0 + 230 + i * ((x1 - x0 - 460) / 3.0)
            cv.circ((xc, ay), 15, mix(col, BG, a))
            lines = wrap(txt, font('sansb', 32), 380)
            if i % 2 == 0:
                cv.text((xc, ay - 120), yr, 'serif', 70, col, 'ma', a)
                cv.text((xc, ay + 36), sub, 'sans', 28, DIM, 'ma', a)
                for k, l in enumerate(lines): cv.text((xc, ay - 120 - (len(lines) - k) * 40 - 10), l, 'sansb', 32, TXT, 'ma', a)
            else:
                cv.text((xc, ay + 34), yr, 'serif', 70, col, 'ma', a)
                for k, l in enumerate(lines): cv.text((xc, ay + 130 + k * 40), l, 'sansb', 32, TXT, 'ma', a)
                cv.text((xc, ay + 130 + len(lines) * 40 + 8), sub, 'sans', 28, DIM, 'ma', a)
    cv.text((W / 2, CONT[3] - 40), 'Miasma faded slowly. Dates vary slightly by source.', 'sans', 30, DIM, 'ma', ease((t - cue('s7', 4) - 1.0) / 0.8))

def sc_lesson(cv, t, p):
    lines = [(cue('s8', 0) + 0.0, 'Snow never saw the germ.', TXT, 'serifr'), (cue('s8', 0) + 1.8, 'He counted.', AMBER, 'serif'),
             (cue('s8', 1), 'Go where it happens.', TXT, 'serif'), (cue('s8', 1) + 1.9, 'Count.', AMBER, 'serif'), (cue('s8', 1) + 3.3, 'Let the numbers change your mind.', TXT, 'serif')]
    y = CONT[1] + (100 if not PORT else 120)
    for i, (tc, txt, col, kind) in enumerate(lines):
        a = ease((t - tc) / 0.7)
        sz = (66 if kind == 'serifr' else 84) if not PORT else (60 if kind == 'serifr' else 80)
        ls = wrap(txt, font(kind, sz), W - 140)
        for k, l in enumerate(ls): cv.text((W / 2, y + k * sz * 1.15), l, kind, sz, col, 'ma', a)
        y += len(ls) * sz * 1.15 + (36 if i == 1 else 20)

def sc_end(cv, t, p):
    a = ease(t / 1.0)
    cy = 460 if PORT else 150
    cv.text((W / 2, cy), 'Heartbeat Observatory', 'serif', 84 if PORT else 100, TXT, 'ma', a)
    cv.text((W / 2, cy + (130 if PORT else 140)), 'heartbeatobservatory.com', 'sansb', 52 if PORT else 56, AMBER, 'ma', a)
    cv.text((W / 2, cy + 260), 'History · Episode 2', 'sans', 38, DIM, 'ma', a)
    src = ['J. Snow, On the Mode of Communication of Cholera, 2nd ed. (1855)', 'UCLA Dept. of Epidemiology, John Snow site · MSU Matrix, John Snow Archive',
           'General Board of Health (1855) · F. Pacini (1854) · W. Farr · R. Koch (1883–84)']
    y = cy + 360
    cv.text((W / 2, y), 'Sources', 'sansb', 32, DIM, 'ma', ease((t - 0.6) / 1))
    for i, s in enumerate(src):
        cv.para(W / 2, y + 48 + i * (100 if PORT else 52), s, 'sans', 30, TXT, W - 120 if PORT else 1600, 1.2, 'm', ease((t - 0.8 - i * 0.2) / 0.8))

# ---------------------------------------------------------------- scene table
SUBS = {
 's1': ['How did one map beat a theory?'],
 's2': ['London, 1854. Most doctors believed cholera spread by miasma: bad air from filth and rot.', 'Then cholera struck Soho.', 'Physician John Snow counted upwards of 500 fatal attacks in ten days,', 'nearly all within about 250 yards of Broad Street.'],
 's3': ['Snow marked each death on a street map, one mark per house.', 'The marks bunched around the Broad Street pump.', 'Of the first 83 deaths he checked, ten lived nearer another pump.', 'Five of those families sent to Broad Street for water.', 'Three were children at a school beside it.'],
 's4': ['Then came the people who should have died, and did not.', 'The Poland Street workhouse, surrounded by cases, had 535 inmates and 5 deaths. It had its own well.', 'At the Broad Street brewery, over 70 workers had no severe cholera. They drank their malt liquor, not water.', 'And a widow in Hampstead, miles away, had Broad Street water delivered by cart.', 'She drank it, and died on September 2.'],
 's5': ['On September 7, Snow took his evidence to the parish Board of Guardians.', 'The next day, the pump handle was removed.', 'Now the honest part.', 'Attacks peaked at 143 on September 1. By the day the handle came off: 12.', 'Many people had already fled.', 'Snow himself could not say how much the handle mattered.'],
 's6': ['His strongest test was two water companies.', "Lambeth drew its water upriver of London's sewage. Southwark and Vauxhall drew it below.", 'Each served rich and poor alike.', 'In the epidemic, Southwark and Vauxhall homes lost 315 per 10,000.', 'Lambeth homes, 37. About eight times as many.'],
 's7': ['The officials were not convinced.', "In 1855, a government committee rejected Snow's water idea.", 'Back in 1854, Filippo Pacini had seen the cholera bacterium in Florence. Almost no one noticed.', 'William Farr gave up miasma for cholera in 1866.', 'Robert Koch identified the bacterium in 1883.'],
 's8': ['Snow never saw the germ. He counted.', 'Go where it happens, count what you can, and let the numbers change your mind.'],
 's9': [],
}
SCENES = [
 ('s1', '', '', sc_title),
 ('s2', 'London, August 1854', 'Source: John Snow, On the Mode of Communication of Cholera, 2nd ed. (1855)', sc_outbreak),
 ('s3', 'Snow’s map', 'Source: Snow (1855). Street layout and mark positions are schematic, not Snow’s data; the counts are his.', sc_map),
 ('s4', 'The exceptions', 'Source: Snow (1855). Workhouse: 535 inmates (some accounts say 530). Brewery owner: Mr. Huggins.', sc_outliers),
 ('s5', 'The handle, and the honest part', 'Source: Snow (1855), daily attacks as he reports them. Days 4–7 not in the text we checked.', sc_handle),
 ('s6', 'The Grand Experiment', 'Source: Snow (1855), deaths by water company in the 1854 epidemic. Rate = deaths per 10,000 houses.', sc_water),
 ('s7', 'The slow turn', 'Sources: General Board of Health (1855); Pacini (1854); W. Farr (1866); R. Koch (1883–84). Dates vary by source.', sc_after),
 ('s8', '', '', sc_lesson),
 ('s9', '', '', sc_end),
]
