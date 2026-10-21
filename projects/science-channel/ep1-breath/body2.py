
# ---------------------------------------------------------------- scenes
def sc_title(cv, t, p):
    a = ease(t / 1.2)
    cv.text((W / 2, 520 if PORT else CONT[1] + 30), 'HEARTBEAT TV  ·  SCIENCE  ·  EPISODE 1', 'sansb', 34 if PORT else 36, AMBER, 'ma', a)
    ty = 640 if PORT else 300
    for k, l in enumerate(('Turning breath', 'back into air')):
        cv.text((W / 2, ty + k * (118 if PORT else 140)), l, 'serif', 96 if PORT else 118, TXT, 'ma', ease((t - 0.2) / 1.2))
    ry = 1060 if PORT else 720; x0 = 120; x1 = W - 120; xc = W / 2
    cv.rect((xc - 70, ry - 70, xc + 70, ry + 70), mix(STEEL, BG, 0.5), 14); cv.outline((xc - 70, ry - 70, xc + 70, ry + 70), STEEL, 3, 14)
    cv.text((xc, ry), 'KO₂', 'sansb', 44, TXT, 'mm')
    al = ease(t / 1.5)
    for j in range(16):
        u = ((t * 0.12 + j / 16.0) % 1.0); yy = ry + math.sin(j * 2.3 + t * 1.3) * 34
        if u < 0.5: mol(cv, 'co2', (x0 + (xc - 80 - x0) * (u / 0.5), yy), 0.4 * math.sin(t + j), 10, al * min(1, u / 0.05))
        else: mol(cv, 'o2', (xc + 80 + (x1 - xc - 80) * ((u - 0.5) / 0.5), yy), 0.4 * math.sin(t + j), 11, al * min(1, (1 - u) / 0.05))

def sc_simA(cv, t, p): sim_scene(cv, t, p, 'none', 's2')
def sc_lioh(cv, t, p): sim_scene(cv, t, p, 'lioh', 's3')
def sc_simC(cv, t, p): sim_scene(cv, t, p, 'ko2', 's7')

def canister(cv, c, kind, s, a=1.0):
    col = mix((196, 208, 224), BG, a); inner = mix((60, 76, 104), BG, a)
    if kind == 'round':
        cv.circ(c, 95 * s, col); cv.circ(c, 80 * s, inner); cv.circ(c, 20 * s, col)
    else:
        cv.rect((c[0] - 95 * s, c[1] - 95 * s, c[0] + 95 * s, c[1] + 95 * s), col, 8); cv.rect((c[0] - 80 * s, c[1] - 80 * s, c[0] + 80 * s, c[1] + 80 * s), inner, 4)
        cv.rect((c[0] - 20 * s, c[1] - 20 * s, c[0] + 20 * s, c[1] + 20 * s), col, 4)

def sc_apollo(cv, t, p):
    x0, x1 = CONT[0] + 30, CONT[2] - 30; w = x1 - x0
    if PORT: cL = (x0 + 190, CONT[1] + 190); cR = (x1 - 190, CONT[1] + 190); s = 1.0
    else: cL = (x0 + 280, CONT[1] + 190); cR = (x1 - 280, CONT[1] + 190); s = 1.15
    a1 = ease(t / 0.8); a2 = ease((t - 2.2) / 0.8)
    canister(cv, cL, 'round', s, a1); canister(cv, cR, 'square', s, a2)
    cv.text((cL[0], cL[1] + 120 * s), 'Lunar Module', 'sansb', 38, TXT, 'ma', a1); cv.text((cL[0], cL[1] + 120 * s + 48), 'round canisters', 'sans', 32, DIM, 'ma', a1)
    cv.text((cR[0], cR[1] + 120 * s), 'Command Module', 'sansb', 38, TXT, 'ma', a2); cv.text((cR[0], cR[1] + 120 * s + 48), 'square canisters', 'sans', 32, DIM, 'ma', a2)
    cv.text((W / 2, cL[1]), '≠', 'sansb', 110, RED, 'mm', ease((t - 3.5) / 0.6))
    by = CONT[1] + (450 if not PORT else 500)
    items = ['plastic bags', 'cardboard', 'suit hoses', 'duct tape']
    cv.text((x0, by), 'The adapter, built from what was aboard:', 'sansb', 38, AMBER, 'la', ease((t - 6.5) / 0.8))
    cx = x0; cy = by + 70
    for i, nm in enumerate(items):
        a = ease((t - 7.5 - i * 0.7) / 0.6); f2 = font('sansb', 40); wd = f2.getlength(nm) / SS + 52
        if cx + wd > x1: cx = x0; cy += 84
        if a > 0:
            cv.rect((cx, cy, cx + wd, cy + 64), mix(STEEL, BG, 0.5 * a), 14); cv.text((cx + wd / 2, cy + 32), nm, 'sansb', 40, TXT, 'mm', a)
        cx += wd + 20
    n = ease((t - 12.0) / 1.0)
    txt = 'Installed in April 1970. CO₂ readings are not shown: not verified here.'
    if PORT: cv.para(x0, CONT[3] - 90, txt, 'sans', 30, DIM, w, 1.2, 'l', n)
    else: cv.text((x0, CONT[3] - 20), txt, 'sans', 30, DIM, 'ls', n)

# --- the reaction, atom by atom
def build_atoms():
    A = {}; bondsR = []; bondsP = []
    for i in range(4):
        A[f'K{i}'] = dict(el='K'); A[f'Oa{i}'] = dict(el='O'); A[f'Ob{i}'] = dict(el='O'); bondsR += [(f'K{i}', f'Oa{i}'), (f'Oa{i}', f'Ob{i}')]
    for j in range(2):
        A[f'C{j}'] = dict(el='C'); A[f'Oc{j}'] = dict(el='O'); A[f'Od{j}'] = dict(el='O'); bondsR += [(f'Oc{j}', f'C{j}'), (f'C{j}', f'Od{j}')]
        bondsP += [(f'C{j}', f'Oc{j}'), (f'C{j}', f'Od{j}'), (f'C{j}', f'Ob{2 * j}'), (f'K{2 * j}', f'Oc{j}'), (f'K{2 * j + 1}', f'Od{j}')]
    bondsP += [('Oa0', 'Oa1'), ('Ob1', 'Ob3'), ('Oa2', 'Oa3')]
    for k in ('Oa0', 'Oa1', 'Ob1', 'Ob3', 'Oa2', 'Oa3'): A[k]['gas'] = True
    return A, bondsR, bondsP
ATOMS, BR, BPR = build_atoms()
RAD = dict(K=26, O=17, C=19); ECOL = dict(K=KCOL, O=OCOL, C=CCOL)

def atom_pos():
    R = {}; Q = {}; cell = 130
    for i in range(4):
        cx = (i % 2) * 240; cy = (i // 2) * cell
        R[f'K{i}'] = (cx, cy); R[f'Oa{i}'] = (cx + 52, cy); R[f'Ob{i}'] = (cx + 88, cy)
    for j in range(2):
        cx = j * 240; cy = 2 * cell
        R[f'Oc{j}'] = (cx, cy); R[f'C{j}'] = (cx + 40, cy); R[f'Od{j}'] = (cx + 80, cy)
    for j in range(2):
        cx = 120 + j * 330; cy = 10
        Q[f'C{j}'] = (cx, cy + 60); Q[f'Oc{j}'] = (cx - 48, cy + 92); Q[f'Od{j}'] = (cx + 48, cy + 92); Q[f'Ob{2 * j}'] = (cx, cy + 6)
        Q[f'K{2 * j}'] = (cx - 100, cy + 150); Q[f'K{2 * j + 1}'] = (cx + 100, cy + 150)
    pairs = [('Oa0', 'Oa1'), ('Ob1', 'Ob3'), ('Oa2', 'Oa3')]
    for n, (a, b) in enumerate(pairs):
        cx = n * 175 + 20; cy = 2 * cell
        Q[a] = (cx, cy); Q[b] = (cx + 36, cy)
    return R, Q
RPOS, QPOS = atom_pos()

def sc_react(cv, t, p):
    x0, x1 = CONT[0] + 30, CONT[2] - 30
    oR = (CONT[0] + 90, CONT[1] + 70); oQ = (CONT[0] + 960, CONT[1] + 70) if not PORT else (CONT[0] + 90, CONT[1] + 70)
    sc = 1.0 if not PORT else 0.9
    m = ease((t - 4.5) / 4.0)
    for k, a in ATOMS.items():
        r0 = RPOS[k]; q0 = QPOS[k]
        if PORT:
            ax = oR[0] + r0[0] * sc; ay = oR[1] + r0[1] * sc; bx = oQ[0] + q0[0] * sc + 120; by_ = oQ[1] + q0[1] * sc
            if k in ('Oa0','Oa1','Ob1','Ob3','Oa2','Oa3'): bx += 0
        else:
            ax = oR[0] + r0[0]; ay = oR[1] + r0[1]; bx = oQ[0] + q0[0]; by_ = oQ[1] + q0[1]
        a['pos'] = (ax + (bx - ax) * m, ay + (by_ - ay) * m)
    if not PORT:
        cv.text((oR[0] - 40, CONT[1] - 6), 'before', 'sans', 28, DIM, 'la'); cv.text((oQ[0] - 80, CONT[1] - 6), 'after', 'sans', 28, DIM, 'la')
        cv.text((oR[0] + 490, CONT[1] + 190), '→', 'sansb', 120, AMBER, 'mm', ease(t / 1.0))
    for (a, b) in BR:
        al = 1.0 if ((a, b) in BPR or (b, a) in BPR) else 1 - ease(m / 0.5)
        if al > 0.02: cv.line([ATOMS[a]['pos'], ATOMS[b]['pos']], mix(TXT, BG, al * 0.8), 5)
    for (a, b) in BPR:
        if (a, b) in BR or (b, a) in BR: continue
        al = ease((m - 0.5) / 0.5)
        if al > 0.02: cv.line([ATOMS[a]['pos'], ATOMS[b]['pos']], mix(TXT, BG, al * 0.8), 5)
    for k, a in ATOMS.items():
        col = ECOL[a['el']]
        if a.get('gas'): col = mix(TEAL, col, ease((m - 0.4) / 0.5))
        cv.circ(a['pos'], RAD[a['el']] * sc, col)
    ey = CONT[1] + (350 if not PORT else 520)
    al = ease((t - 1.0) / 1.0)
    rich(cv, W / 2, ey, [('4 KO₂', KCOL), (' + ', TXT), ('2 CO₂', CCOL), ('  →  ', AMBER), ('2 K₂CO₃', KCOL), (' + ', TXT), ('3 O₂', TEAL)], 'sansb', 62 if not PORT else 54, 'm', al)
    cv.text((W / 2, ey + 82), 'Atoms in = atoms out:  K 4  ·  C 2  ·  O 12', 'sans', 34, DIM, 'ma', ease((t - 9.0) / 1.0))
    n = ease((t - 12.5) / 1.0)
    cv.rect((x0, CONT[3] - 150, x1, CONT[3] - 20), mix(AMBER, BG, 0.15 * n), 14)
    cv.text((W / 2, CONT[3] - 138), 'Per 1 kg of KO₂, by this equation (theory):', 'sans', 32, TXT, 'ma', n)
    rich(cv, W / 2, CONT[3] - 90, [('absorbs up to 0.31 kg CO₂', CCOL), ('   ·   ', DIM), ('releases 0.34 kg O₂', TEAL)], 'sansb', 38 if not PORT else 32, 'm', n)

def sc_water(cv, t, p):
    x0, x1 = CONT[0] + 30, CONT[2] - 30; w = x1 - x0
    cv.text((x0, CONT[1] + 6), 'Exhaled breath also carries water vapor', 'sansb', 40, TXT, 'la', ease(t / 0.8))
    ry = CONT[1] + 130; xs = x0 + 40; xe = x0 + 700 if not PORT else x1 - 520
    cv.rect((xe, ry - 70, xe + 190, ry + 70), mix(STEEL, BG, 0.5), 14); cv.outline((xe, ry - 70, xe + 190, ry + 70), STEEL, 3, 14); cv.text((xe + 95, ry), 'KO₂', 'sansb', 44, TXT, 'mm')
    for j in range(14):
        u = (t * 0.14 + j / 14.0) % 1.0; yy = ry + math.sin(j * 1.9 + t * 1.1) * 40
        mol(cv, 'co2' if j % 2 == 0 else 'h2o', (xs + (xe - 20 - xs) * u, yy), 0.3 * math.sin(j + t), 11, min(1, u / 0.05, (1 - u) / 0.1) * ease((t - 0.8) / 0.8))
    ox = xe + 220
    for j in range(8):
        u = (t * 0.14 + j / 8.0) % 1.0
        mol(cv, 'o2', (ox + (x1 - ox - 20) * u, ry + math.sin(j * 2.1 + t) * 40), 0.3, 12, min(1, u / 0.05, (1 - u) / 0.05) * ease((t - 4.0) / 1.0))
    ey = ry + 95
    lines = [([('4 KO₂', KCOL), (' + ', TXT), ('2 H₂O', WATER), ('  →  ', AMBER), ('4 KOH', KCOL), (' + ', TXT), ('3 O₂', TEAL)], 3.0, 'KO₂ + water: oxygen, and potassium hydroxide'),
             ([('KOH', KCOL), (' + ', TXT), ('CO₂', CCOL), ('  →  ', AMBER), ('carbonate / bicarbonate', TXT)], 6.0, 'the hydroxide captures carbon dioxide')]
    for i, (parts, t0, cap) in enumerate(lines):
        a = ease((t - t0) / 0.9); yy = ey + i * 110
        rich(cv, W / 2, yy, parts, 'sansb', 54 if not PORT else 46, 'm', a); cv.text((W / 2, yy + 66), cap, 'sans', 32, DIM, 'ma', a)
    by = ey + 225
    n = ease((t - 9.0) / 0.8)
    cv.text((x0, by), 'Illustration: more breathing, more oxygen released', 'sansb', 34, AMBER, 'la', n)
    for i, (nm, f) in enumerate((('light breathing', 0.38), ('hard breathing', 0.9))):
        yy = by + 50 + i * 56; k = ease((t - 9.8 - i * 0.8) / 1.2)
        cv.text((x0, yy + 22), nm, 'sans', 30, TXT, 'lm', n); cv.rect((x0 + 290, yy, x0 + 290 + (w - 290) * f * k, yy + 44), TEAL, 8)

def sc_compare(cv, t, p):
    x0, x1 = CONT[0] + 20, CONT[2] - 20; w = x1 - x0
    cols = [('No scrubber', 'none', DIM), ('Lithium hydroxide', 'lioh', TXT), ('Potassium superoxide', 'ko2', AMBER)]
    cw = (w - 40) / 3 if not PORT else w; ch = 540 if not PORT else 260
    for i, (nm, mode, hc) in enumerate(cols):
        h, co2, o2, used = sim_at(mode, HOURS)
        a = ease((t - 0.5 - i * 1.6) / 0.9); k = ease((t - 1.0 - i * 1.6) / 1.4)
        bx = (x0 + i * (cw + 20), CONT[1] + 10, x0 + i * (cw + 20) + cw, CONT[1] + 10 + ch) if not PORT else (x0, CONT[1] + 10 + i * (ch + 20), x1, CONT[1] + 10 + i * (ch + 20) + ch)
        cv.rect(bx, mix(BG2, BG, a), 16); cv.outline(bx, mix(STEEL, BG, 0.7 * a), 3, 16)
        cv.text(((bx[0] + bx[2]) / 2, bx[1] + 22), nm, 'serif', 40 if not PORT else 44, hc, 'ma', a)
        ccol = TEAL if co2 < 0.5 else (AMBER if co2 < 4.0 else RED); ocol = TEAL if o2 >= 19.5 else AMBER
        cs = f'{co2 * k:.2f}%'; osr = f'{(20.95 - (20.95 - o2) * k):.1f}%'
        if not PORT:
            cx = (bx[0] + bx[2]) / 2
            cv.text((cx, bx[1] + 120), 'CO₂ at 6 h', 'sans', 30, DIM, 'ma', a); cv.text((cx, bx[1] + 156), cs, 'serif', 84, ccol, 'ma', a)
            cv.text((cx, bx[1] + 310), 'O₂ at 6 h', 'sans', 30, DIM, 'ma', a); cv.text((cx, bx[1] + 346), osr, 'serif', 84, ocol, 'ma', a)
        else:
            cv.text((bx[0] + 60, bx[1] + 120), 'CO₂ at 6 h', 'sans', 32, DIM, 'la', a); cv.text((bx[0] + 60, bx[1] + 156), cs, 'serif', 80, ccol, 'la', a)
            cv.text((bx[0] + 540, bx[1] + 120), 'O₂ at 6 h', 'sans', 32, DIM, 'la', a); cv.text((bx[0] + 540, bx[1] + 156), osr, 'serif', 80, ocol, 'la', a)
    n = ease((t - 8.0) / 1.0)
    cv.text((W / 2, CONT[3] - 10), 'Same pod, same person, same 6 hours. Model values, not measurements.', 'sans', 30, DIM, 'ms', n)

def sc_use(cv, t, p):
    x0, x1 = CONT[0] + 20, CONT[2] - 20; w = x1 - x0
    cw = (w - 30) / 2 if not PORT else w; ch = 540 if not PORT else 400
    cards = [('Mine self-rescuers', ['Some 60-minute units (e.g. Dräger OXY-SR 60B, MSA 60-min) use KO₂', 'Breath moisture + KO₂ makes oxygen; the hydroxide takes CO₂', 'A chlorate candle gives the first burst of oxygen'], 'CDC / NIOSH / MSHA reports'),
             ('Soviet / Russian spacecraft', ['Vostok, Voskhod, Soyuz, Salyut: oxygen supply stored chemically', 'KO₂ cartridges used for gas recovery (NASA history)', 'Per-craft details differ by source. Mir: not verified.'], 'NASA, A History of Spacecraft ECLS')]
    for i, (hd, ls, sr) in enumerate(cards):
        a = ease((t - 0.5 - i * 5.0) / 0.9)
        bx = (x0 + i * (cw + 30), CONT[1] + 10, x0 + i * (cw + 30) + cw, CONT[1] + 10 + ch) if not PORT else (x0, CONT[1] + 10 + i * (ch + 20), x1, CONT[1] + 10 + i * (ch + 20) + ch)
        cv.rect(bx, mix(BG2, BG, a), 16); cv.outline(bx, mix(STEEL, BG, 0.7 * a), 3, 16)
        cv.text((bx[0] + 30, bx[1] + 26), hd, 'serif', 46 if not PORT else 48, AMBER, 'la', a)
        yy = bx[1] + 110
        for j, l in enumerate(ls):
            yy = cv.para(bx[0] + 30, yy, ('•  ' + l) if j < 2 else l, 'sans', 32, TXT if j < 2 else DIM, bx[2] - bx[0] - 60, 1.25, 'l', a) + 14
        cv.text((bx[0] + 30, bx[3] - 52), sr, 'sans', 28, DIM, 'la', a)

def sc_safe(cv, t, p):
    cx = W / 2; a = ease(t / 1.0)
    cy = CONT[1] + (200 if not PORT else 240)
    cv.rect((cx - 90, cy - 110, cx + 90, cy + 110), mix(STEEL, BG, 0.4 * a), 18); cv.outline((cx - 90, cy - 110, cx + 90, cy + 110), mix(STEEL, BG, a), 4, 18)
    cv.text((cx, cy), 'KO₂', 'sansb', 52, TXT, 'mm', a)
    d = ease((t - 2.5) / 1.5)
    if d > 0:
        wx = cx + 330 - 250 * d; wc = mix(WATER, BG, d)
        cv.poly([(wx, cy - 54), (wx - 24, cy - 6), (wx + 24, cy - 6)], wc); cv.circ((wx, cy + 4), 25, wc)
    cv.text((cx, cy + 150), 'Reacts violently with water.', 'serif', 56 if not PORT else 60, RED, 'ma', ease((t - 3.5) / 1.0))
    cv.text((cx, cy + 230), 'Sealed in canisters, handled by trained people.', 'sans', 40 if not PORT else 36, TXT, 'ma', ease((t - 4.5) / 1.0))

def sc_end(cv, t, p):
    a = ease(t / 1.0)
    cy = 400 if PORT else 100
    cv.text((W / 2, cy), 'Heartbeat Observatory', 'serif', 84 if PORT else 100, TXT, 'ma', a)
    cv.text((W / 2, cy + (130 if PORT else 140)), 'heartbeatobservatory.com', 'sansb', 52 if PORT else 56, AMBER, 'ma', a)
    cv.text((W / 2, cy + 240), 'Science · Episode 1', 'sans', 38, DIM, 'ma', a)
    src = ['NASA (Perry et al., AIAA): 0.84 kg O₂ and 1 kg CO₂ per person-day', 'NASA, A History of Spacecraft ECLS (Daues): Vostok, Voskhod, Soyuz, Salyut',
           'NASA Apollo Lunar Surface Journal; PBS NOVA (Apollo 13 adapter)', 'CDC / NIOSH: CO₂ limits, mine self-rescuer reports · OSHA 29 CFR 1910.146 (19.5% O₂)',
           'Wikipedia, Potassium superoxide (reactions; kg figures checked by molar mass)']
    y = cy + 320; step = 100 if PORT else 46
    cv.text((W / 2, y), 'Sources', 'sansb', 32, DIM, 'ma', ease((t - 0.6) / 1))
    for i, s in enumerate(src):
        cv.para(W / 2, y + 48 + i * step, s, 'sans', 30, TXT, W - 120 if PORT else 1700, 1.2, 'm', ease((t - 0.8 - i * 0.2) / 0.8))
    cv.text((W / 2, y + 48 + 5 * step + 24), 'Simulation: simple model, assumptions shown. Not a measurement.', 'sans', 28, DIM, 'ma', ease((t - 2.2) / 1))

SUBS = {
 's1': ['How do you keep breathing inside a sealed capsule, when the only air is the air you already have?'],
 's2': ["NASA's design numbers: one person uses about 0.84 kg of oxygen a day and breathes out about 1 kg of carbon dioxide.", 'Seal one person in a 3 cubic meter pod, and watch.',
        'In our simulation, carbon dioxide passes the half percent workplace limit in about forty minutes, and keeps climbing.', 'Oxygen slowly falls.'],
 's3': ["Apollo's answer was lithium hydroxide.", 'It captures carbon dioxide, and leaves lithium carbonate and water.', 'Carbon dioxide stays low.', 'But lithium hydroxide makes no oxygen. That has to come from tanks.'],
 's4': ['On Apollo 13, three men had to live in a lunar module built for two.', "Its round canisters could not keep up, and the command module's square ones did not fit.",
        'So the crew and the ground built an adapter from plastic bags, hoses, cardboard, and duct tape.'],
 's5': ['Potassium superoxide does both jobs.', 'Four units of it plus two of carbon dioxide make two of potassium carbonate, and three of oxygen.', 'Carbon dioxide goes in. Oxygen comes out.',
        'One kilogram absorbs up to a third of a kilogram of carbon dioxide, and releases a third of a kilogram of oxygen.'],
 's6': ['Breath also carries water vapor.', 'Potassium superoxide reacts with that too, releasing more oxygen and forming potassium hydroxide,', 'which captures more carbon dioxide.',
        'Breathing drives the chemistry: harder breathing, more oxygen.'],
 's7': ['Now run the same pod with a potassium superoxide canister.', 'Carbon dioxide holds near a quarter of a percent.', 'Oxygen stays near 20 percent, because the canister gives oxygen back.',
        'It used about half a kilogram of the chemical in six hours.'],
 's8': ['Six hours, side by side.', 'With no scrubber, carbon dioxide reaches 4.6 percent, and oxygen drops to 15.8.', 'With lithium hydroxide, carbon dioxide is held, but oxygen falls to 16 and a half.',
        'With potassium superoxide, both stay in range.'],
 's9': ['That is why it turns up where tanks are awkward.', 'Some 60 minute mine self rescuers use it, started by a small chlorate candle.',
        "And NASA's history says Soviet Vostok, Voskhod, and Soyuz craft stored their oxygen chemically,", 'with potassium superoxide cartridges.'],
 's10': ['One honest warning: potassium superoxide reacts violently with water,', 'so it lives sealed inside canisters, handled by trained people.', 'Your breath, turned back into air.'],
 's11': [],
}
SRCSIM = 'Sim inputs: NASA (Perry et al., AIAA) 0.84 kg O₂ + 1 kg CO₂ per person-day. Limits: NIOSH / OSHA. Scrubber flow assumed.'
SCENES = [
 ('s1', '', '', sc_title),
 ('s2', 'Sealed in, breathing', SRCSIM, sc_simA),
 ('s3', 'Lithium hydroxide: CO₂ out, no O₂ in', 'Source: NASA (LiOH scrubbers, Apollo era); same sim inputs. Scrubber flow assumed.', sc_lioh),
 ('s4', 'Apollo 13: a square peg, a round hole', 'Source: NASA Apollo Lunar Surface Journal; PBS NOVA, Apollo 13', sc_apollo),
 ('s5', 'Potassium superoxide: CO₂ in, O₂ out', 'Source: Wikipedia, Potassium superoxide (equation); the kg figures we checked by molar mass', sc_react),
 ('s6', 'And it uses the water in your breath', 'Source: Wikipedia, Potassium superoxide; CDC/NIOSH self-rescuer reports. Bars are an illustration.', sc_water),
 ('s7', 'Same pod, KO₂ canister', 'Sim: carbonate and water routes blended (assumed 0.9 O₂ per CO₂ absorbed). Humidity and heat not modeled.', sc_simC),
 ('s8', 'Six hours, three ways', 'Model values from the same simulation. Limits: NIOSH (CO₂), OSHA 29 CFR 1910.146 (O₂ below 19.5%).', sc_compare),
 ('s9', 'Where it is used', 'Sources: CDC/NIOSH self-rescuer reports; NASA, A History of Spacecraft ECLS (Daues)', sc_use),
 ('s10', 'One honest line', 'Source: Wikipedia, Potassium superoxide (hazards)', sc_safe),
 ('s11', '', '', sc_end),
]
