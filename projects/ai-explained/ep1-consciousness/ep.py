import sys; sys.path.insert(0, '..')
from ailib import *
import ailib, tvlib, random, math

SCR = json.load(open('script.json'))
SUBS = {s['id']: s['disp'] for s in SCR}
def D(sid): b = tvlib.BOUND[sid]; return b[1] - b[0]

def three(cv, p, items, area=None, gap=70, arrows=True):
    """items: (label, big, small, colour, reveal_fraction)"""
    bxs = boxes(len(items), area, gap)
    for i, (bx, (lab, big, small, col, f)) in enumerate(zip(bxs, items)):
        a = rev(p, f)
        if a <= 0: continue
        card(cv, bx, a, col); w = bx[2] - bx[0]
        cv.text((bx[0] + 28, bx[1] + 24), lab, 'monob', 28, col, 'la', a)
        bs = 50 if PORT else 52
        y = cv.para(bx[0] + 28, bx[1] + 80, big, 'serif', bs, CREAM, w - 56, 1.12, 'l', a)
        if small: cv.para(bx[0] + 28, y + 10, small, 'sans', 34, DIMC, w - 56, 1.2, 'l', a)
        if arrows and i < len(items) - 1 and rev(p, items[i + 1][4]) > 0:
            na = rev(p, items[i + 1][4])
            if PORT: arrow(cv, ((bx[0] + bx[2]) / 2, bx[3] + 10), ((bx[0] + bx[2]) / 2, bx[3] + gap - 10), DIMC, 5, 18, na)
            else: arrow(cv, (bx[2] + 10, (bx[1] + bx[3]) / 2), (bx[2] + gap - 10, (bx[1] + bx[3]) / 2), DIMC, 5, 18, na)

# ------------------------------------------------------------------ a1 title
def sc_title(cv, t, p):
    cx, cy = W / 2, (900 if PORT else 560)
    for k in range(5):
        r = (t * 150 + k * 160) % 800; a = max(0.0, 1 - r / 800) * 0.35 * ease(t / 1.5)
        cv.ring((cx, cy), r, mix(LIME, BG, a), 4)
    a = ease(t / 1.0); ty = 170 if PORT else 120
    cv.text((W / 2, ty), 'HEARTBEAT TV  ·  AI EXPLAINED  ·  EPISODE 1', 'monob', 28 if PORT else 34, LIME, 'ma', a)
    sz = 100 if PORT else 128
    for k, l in enumerate(('Can consciousness', 'be measured?')):
        cv.text((W / 2, ty + 100 + k * sz * 1.18 + (80 if PORT else 0)), l, 'serif', sz, CREAM, 'ma', ease((t - 0.2) / 1.0), 6)
    y = 1100 if PORT else 690
    for k, (lab, col) in enumerate((('PEOPLE', LIME), ('ANIMALS', SKY), ('AI SYSTEMS', LILAC))):
        pill(cv, W * (0.2 + 0.3 * k), y, lab, col, rev(p, 0.45 + k * 0.12, 0.06), 30 if PORT else 36)
    cv.text((W / 2, y + (90 if PORT else 70)), 'what the tests show, and what they cannot', 'serifr', 40, DIMC, 'ma', rev(p, 0.8, 0.08))

# ------------------------------------------------------------------ a2 the problem
def sc_problem(cv, t, p):
    area = (30, 380, W - 30, 1240) if PORT else (60, 250, W - 60, 600)
    three(cv, p, [('YOUR EXPERIENCE', 'Only you can observe it', 'first-person, from the inside', LILAC, 0.06),
                  ('A REPORT', '"I saw it."', 'what a person says', SKY, 0.38),
                  ('A BRAIN SIGNAL', 'Measurable', 'checked against reports', LIME, 0.62)], area, 90)

# ------------------------------------------------------------------ a3 PCI illustration
_rng = random.Random(7)
NODES = []
for i in range(84):
    while True:
        x, y = _rng.uniform(-1, 1), _rng.uniform(-1, 1)
        if x * x + y * y < 0.94: break
    NODES.append((x, y, _rng.uniform(0, 6.28), _rng.uniform(1.5, 4.0), _rng.uniform(0, 1.0)))
STIM = (-0.55, 0.15)

def pci_panel(cv, bx, kind, a, tt):
    col = LIME if kind == 'rich' else SKY
    card(cv, bx, a, col)
    w = bx[2] - bx[0]; h = bx[3] - bx[1]
    lab = 'AWAKE  ·  DREAMING' if kind == 'rich' else 'DEEP SLEEP  ·  ANESTHESIA'
    sub = 'rich, varied echo' if kind == 'rich' else 'simple, short echo'
    cv.text((bx[0] + 26, bx[1] + 20), lab, 'monob', 28, col, 'la', a)
    cv.text((bx[0] + 26, bx[1] + 58), sub, 'serifr', 36, CREAM, 'la', a)
    if PORT: cx, cy, R = bx[0] + 190, bx[1] + h * 0.62, 125
    else: cx, cy, R = (bx[0] + bx[2]) / 2, bx[1] + 330, 175
    cv.ring((cx, cy), R + 12, mix(DIMC, BG, 0.5 * a), 3)
    ph = tt % 7.0
    for (x, y, p0, fr, rd) in NODES:
        px, py = cx + x * R, cy + y * R; d = math.hypot(x - STIM[0], y - STIM[1])
        lit = 0.0
        if ph > 0.8:
            e = ph - 0.8
            if kind == 'rich':
                lit = (1.0 if e > d * 0.5 else 0) * max(0.0, math.sin(p0 + e * fr * 2.0)) * (1 if e < 5.2 else max(0, (6.0 - e) / 0.8))
                lit = lit if lit > 0.35 else lit * 0.3
            else:
                wv = e * 1.3
                lit = max(0.0, 1 - abs(d - wv) / 0.35) if e < 1.6 else 0.0
        c = mix(col, BG, 0.16 + 0.84 * min(1, lit))
        r = 7 + 6 * min(1, lit)
        if lit > 0.5: cv.circ((px, py), r + 7, mix(col, BG, 0.25 * lit * a))
        cv.circ((px, py), r, mix(c, BG, a))
    sx, sy = cx + STIM[0] * R, cy + STIM[1] * R
    if 0.2 < ph < 1.4: cv.ring((sx, sy), 12 + (ph - 0.2) * 40, mix(LILAC, BG, a * (1 - (ph - 0.2) / 1.2)), 4)
    cv.circ((sx, sy), 9, mix(LILAC, BG, a)); cv.text((sx - 16, sy - 40), 'pulse', 'mono', 24, LILAC, 'ra', a)
    if PORT: x0, x1, yc, amp = bx[0] + 360, bx[2] - 30, bx[1] + h * 0.62, 55
    else: x0, x1, yc, amp = bx[0] + 40, bx[2] - 40, bx[1] + h - 70, 42
    pts = []
    for k in range(240):
        u = k / 239; tm = u * 3.0
        if kind == 'rich':
            v = (math.sin(tm * 17 + 1) * 0.5 + math.sin(tm * 29) * 0.35 + math.sin(tm * 41 + 2) * 0.25) * math.exp(-tm * 0.35)
        else:
            v = math.sin(tm * 13) * math.exp(-tm * 3.4)
        pts.append((x0 + (x1 - x0) * u, yc - v * amp))
    cv.line(pts, mix(col, BG, 0.9 * a), 3); cv.text((x0, yc + amp + 14), 'EEG echo (schematic)', 'mono', 22, DIMC, 'la', a)

def sc_pci(cv, t, p):
    area = (30, 350, W - 30, 1230) if PORT else (60, 215, W - 60, 830)
    b = boxes(2, area, 26)
    pci_panel(cv, b[0], 'rich', rev(p, 0.18), t); pci_panel(cv, b[1], 'simple', rev(p, 0.36), t)

# ------------------------------------------------------------------ a4 numbers
def sc_numbers(cv, t, p):
    d = D('a4')
    stat_cards(cv, t, [dict(num='150', label='people who could report', sub='the benchmark group', at=0.1 * d, col=LIME),
                       dict(num='81', label='patients who could not communicate', sub='tested with that cutoff', at=0.34 * d, col=SKY),
                       dict(num='95%', label='of minimally conscious patients scored above it', sub='36 of 38', at=0.52 * d, col=LIME),
                       dict(num='9 of 43', label='vegetative-state patients scored above it', sub='suggests hidden consciousness; not proven', at=0.72 * d, col=PEACH)])

# ------------------------------------------------------------------ a5 limits of PCI
def sc_limits(cv, t, p):
    three(cv, p, [('IT MEASURES', "How rich the brain's response is", 'a level of consciousness', LIME, 0.12),
                  ('IT DOES NOT SHOW', 'What is being experienced', "not a window into anyone's mind", ROSE, 0.42),
                  ('CALIBRATED ON', 'People who could report', 'how they were doing', PEACH, 0.7)],
          (30, 380, W - 30, 1240) if PORT else (60, 250, W - 60, 570), 40, False)

# ------------------------------------------------------------------ a6 hidden awareness
def sc_hidden(cv, t, p):
    b = boxes(2, (30, 350, W - 30, 1240) if PORT else (60, 215, W - 60, 640), 30)
    a = rev(p, 0.05); card(cv, b[0], a, SKY); bx = b[0]; w = bx[2] - bx[0]
    cv.text((bx[0] + 28, bx[1] + 24), '2006  ·  ONE PATIENT', 'monob', 28, SKY, 'la', a)
    y = cv.para(bx[0] + 28, bx[1] + 80, 'Imagine playing tennis. Imagine walking through your home.', 'serif', 40 if PORT else 44, CREAM, w - 56, 1.15, 'l', a)
    a2 = rev(p, 0.3)
    cv.para(bx[0] + 28, y + 24, 'Her scan lit up the expected regions, as in healthy volunteers. Diagnosis: vegetative state.', 'sans', 34, DIMC, w - 56, 1.2, 'l', a2)
    a3 = rev(p, 0.52); bx = b[1]; card(cv, bx, a3, LIME); w = bx[2] - bx[0]
    cv.text((bx[0] + 28, bx[1] + 24), '2024  ·  353 PATIENTS, 6 CENTERS', 'monob', 26, LIME, 'la', a3)
    cv.text(((bx[0] + bx[2]) / 2, bx[1] + 90), '60 of 241', 'serif', 86 if PORT else 100, LIME, 'ma', a3)
    a4 = rev(p, 0.66)
    cv.para(bx[0] + 28, bx[1] + 90 + 140, 'with no bedside response to commands still did a thinking task on fMRI or EEG: about 1 in 4.', 'sans', 34, CREAM, w - 56, 1.2, 'l', a4)

# ------------------------------------------------------------------ a7 pass is informative
def sc_passmiss(cv, t, p):
    d = D('a7')
    hbars(cv, t, [dict(label='Responded at the bedside (n = 112)', val=38, txt='38%  ·  43 of 112', at=0.1 * d, col=LIME),
                  dict(label='No bedside response (n = 241)', val=25, txt='25%  ·  60 of 241', at=0.3 * d, col=SKY)],
          50, (30, 400, W - 30, 880) if PORT else (60, 250, W - 60, 640), 330 if PORT else 520)
    cv.text((W / 2, 960 if PORT else 700), 'passed a scan or EEG task', 'serifr', 40, DIMC, 'ma', rev(p, 0.25))
    a = rev(p, 0.62)
    if a > 0:
        cv.para(W / 2, 1040 if PORT else 760, 'A pass is informative. A miss does not show that no one is home.', 'serif', 42 if PORT else 46, CREAM, W - 200, 1.15, 'm', a)

# ------------------------------------------------------------------ a8 theories
BRAINC = (52, 92, 90)
def brain(cv, cx, cy, w, h, hi, col, a):
    pts = [(cx + math.cos(k / 60 * 6.283) * w / 2, cy + math.sin(k / 60 * 6.283) * h / 2 * (1 if math.sin(k / 60 * 6.283) < 0 else 0.82)) for k in range(60)]
    cv.poly(pts, mix(BRAINC, BG, a), mix(DIMC, BG, 0.7 * a))
    xe = cx - w * 0.10 if hi == 'front' else cx + w * 0.10
    sel = [q for q in pts if (q[0] < xe if hi == 'front' else q[0] > xe)]
    if sel: cv.poly(sel, mix(col, BG, 0.55 * a))
    r = random.Random(3)
    for k in range(7):
        x0 = cx + r.uniform(-0.38, 0.38) * w; y0 = cy + r.uniform(-0.3, 0.2) * h
        cv.line([(x0 + math.sin(j * 1.3 + k) * 8, y0 + j * 11) for j in range(7)], mix(BG, BRAINC, 0.5 * a + 0.5), 4)
    cv.poly([(cx + w * 0.05, cy + h * 0.33), (cx + w * 0.17, cy + h * 0.33), (cx + w * 0.14, cy + h * 0.62), (cx + w * 0.06, cy + h * 0.62)], mix(BRAINC, BG, a))
    cv.text((cx - w / 2, cy - h / 2 - 30), 'FRONT', 'mono', 22, DIMC, 'la', a); cv.text((cx + w / 2, cy - h / 2 - 30), 'BACK', 'mono', 22, DIMC, 'ra', a)

def sc_theories(cv, t, p):
    b = boxes(2, (30, 350, W - 30, 1240) if PORT else (60, 215, W - 60, 830), 30)
    defs = [('GLOBAL WORKSPACE THEORY', 'Broadcast widely: "ignition"', 'Often linked to networks in the front of the brain', 'front', LIME, 0.06),
            ('INTEGRATED INFORMATION THEORY', 'Causal structure of the system', 'Predicts a "hot zone" in the back of the cortex', 'back', SKY, 0.4)]
    for bx, (lab, big, small, hi, col, f) in zip(b, defs):
        a = rev(p, f); card(cv, bx, a, col); w = bx[2] - bx[0]
        cv.text((bx[0] + 26, bx[1] + 22), lab, 'monob', 26 if PORT else 28, col, 'la', a)
        if PORT: brain(cv, bx[0] + w * 0.5, bx[1] + 170, 340, 140, hi, col, a); ty = bx[1] + 262
        else: brain(cv, bx[0] + w / 2, bx[1] + 225, 540, 280, hi, col, a); ty = bx[1] + 425
        y = cv.para(bx[0] + 26, ty, big, 'serif', 36 if PORT else 40, CREAM, w - 52, 1.12, 'l', a)
        cv.para(bx[0] + 26, y + 6, small, 'sans', 30 if PORT else 32, DIMC, w - 52, 1.2, 'l', rev(p, f + 0.1))

# ------------------------------------------------------------------ a9 Cogitate
def sc_cogitate(cv, t, p):
    hy = 378 if PORT else 232
    for k, (lab, col) in enumerate((('256 PEOPLE', LIME), ('fMRI · MEG · intracranial EEG', SKY), ('PREREGISTERED', LILAC))):
        cx = [190, 540, 880][k] if PORT else [W * 0.2, W * 0.5, W * 0.8][k]
        pill(cv, cx, hy, lab, col, rev(p, 0.02 + k * 0.03), 22 if PORT else 28, 18 if PORT else 24)
    rows = [('IIT', SKY, 'Sustained synchronization in the back of the cortex', 'LACKING', ROSE, 0.30),
            ('GNWT', LIME, 'Ignition when the image disappears', 'MOSTLY ABSENT', ROSE, 0.44),
            ('GNWT', LIME, 'Prefrontal cortex represents the conscious dimensions', 'LIMITED', ROSE, 0.56),
            ('BOTH', LILAC, 'What was seen: in visual, ventrotemporal and inferior frontal cortex', 'FOUND', LIME, 0.70),
            ('BOTH', LILAC, 'Frontal and early-visual areas synchronize by content', 'FOUND', LIME, 0.82)]
    y = 450 if PORT else 290; step = 158 if PORT else 106
    for i, (tag, tc, txt, res, rc, f) in enumerate(rows):
        a = rev(p, f); yy = y + i * step
        if PORT:
            card(cv, (30, yy, W - 30, yy + step - 12), a, rc if rc == ROSE else None, 14)
            pill(cv, 120, yy + 34, tag, tc, a, 22, 16); pill(cv, W - 200, yy + 34, res, rc, a, 22, 16)
            cv.para(52, yy + 66, txt, 'sans', 30, CREAM, W - 100, 1.15, 'l', a)
        else:
            card(cv, (60, yy, W - 60, yy + step - 14), a, rc if rc == ROSE else None, 14)
            pill(cv, 160, yy + 46, tag, tc, a, 28, 20)
            cv.para(290, yy + 28, txt, 'sans', 36, CREAM, 1180, 1.12, 'l', a)
            pill(cv, W - 250, yy + 46, res, rc, a, 28, 20)

# ------------------------------------------------------------------ a10 dispute
def sc_dispute(cv, t, p):
    area = (30, 350, W - 30, 880) if PORT else (60, 215, W - 60, 520)
    b = boxes(2, area, 30)
    for bx, (lab, big, small, col, f) in zip(b, [
        ('THE LETTER  ·  SEPT 2023', '"Pseudoscience"', "124 researchers said IIT's claims outrun the evidence.", PEACH, 0.1),
        ('THE REPLY', '"Disproportionate"', 'Philosopher David Chalmers, among others, objected to the label.', SKY, 0.4)]):
        a = rev(p, f); card(cv, bx, a, col); w = bx[2] - bx[0]
        cv.text((bx[0] + 28, bx[1] + 22), lab, 'monob', 26, col, 'la', a)
        y = cv.para(bx[0] + 28, bx[1] + 70, big, 'serif', 52 if PORT else 60, CREAM, w - 56, 1.1, 'l', a)
        cv.para(bx[0] + 28, y + 10, small, 'sans', 32 if PORT else 34, DIMC, w - 56, 1.2, 'l', a)
    ty = 1040 if PORT else 640
    a = rev(p, 0.62); cv.line([(100, ty), (W - 100, ty)], mix(DIMC, BG, 0.7 * a), 4)
    for k, (lab, sub, col) in enumerate((('SEP 2023', 'open letter', PEACH), ('APR 2025', 'Cogitate test, Nature', LIME), ('2026', 'protocol: monkeys and mice. Results: none found yet', SKY))):
        cx = [190, 540, 890][k] if PORT else [270, W / 2, W - 300][k]
        aa = rev(p, 0.66 + k * 0.1); cv.circ((cx, ty), 14, mix(col, BG, aa))
        cv.text((cx, ty + 28), lab, 'monob', 28, col, 'ma', aa)
        cv.para(cx, ty + 70, sub, 'sans', 30, CREAM, 300 if PORT else 380, 1.15, 'm', aa)

# ------------------------------------------------------------------ a11 mirror test
def face(cv, cx, cy, r, a, mark=True):
    cv.circ((cx, cy), r, mix((226, 200, 170), BG, a)); cv.circ((cx - r * 0.35, cy - r * 0.15), r * 0.09, mix((40, 30, 30), BG, a)); cv.circ((cx + r * 0.35, cy - r * 0.15), r * 0.09, mix((40, 30, 30), BG, a))
    cv.line([(cx - r * 0.3, cy + r * 0.4), (cx, cy + r * 0.5), (cx + r * 0.3, cy + r * 0.4)], mix((90, 50, 40), BG, a), 4)
    if mark: cv.circ((cx + r * 0.5, cy - r * 0.55), r * 0.13, mix(ROSE, BG, a))

def sc_mirror(cv, t, p):
    items = [('1970', 'Chimpanzees', 'touched the dye mark seen in the mirror', 'PASSED', LIME, 0.12),
             ('1970', 'Monkeys tested', 'showed no such behavior', 'DID NOT', DIMC, 0.3),
             ('2008', 'Magpies', 'reported to pass', 'REPORTED', LIME, 0.5),
             ('2019', 'Cleaner wrasse', 'reported to pass, far more disputed', 'DISPUTED', PEACH, 0.68)]
    if PORT:
        for i, (yr, nm, dt, st, col, f) in enumerate(items):
            a = rev(p, f); y = 360 + i * 190; card(cv, (30, y, W - 30, y + 174), a, col, 16)
            cv.text((60, y + 28), yr, 'serif', 64, col, 'la', a)
            cv.text((260, y + 24), nm, 'serif', 42, CREAM, 'la', a); cv.para(260, y + 80, dt, 'sans', 32, DIMC, 560, 1.15, 'l', a)
            pill(cv, W - 130, y + 87, st, col, a, 22, 12)
        cv.para(W / 2, 1150, 'Narrow test: mirror-guided behavior toward a mark. Not a test of consciousness.', 'serifr', 36, CREAM, W - 120, 1.15, 'm', rev(p, 0.82))
    else:
        cv.line([(100, 520), (W - 100, 520)], mix(DIMC, BG, 0.6), 4)
        for i, (yr, nm, dt, st, col, f) in enumerate(items):
            a = rev(p, f); cx = 270 + i * 460
            cv.circ((cx, 520), 16, mix(col, BG, a)); cv.text((cx, 410), yr, 'serif', 76, col, 'ma', a)
            cv.text((cx, 570), nm, 'serif', 42, CREAM, 'ma', a); cv.para(cx, 630, dt, 'sans', 32, DIMC, 380, 1.15, 'm', a)
            pill(cv, cx, 750, st, col, a, 24, 18)
        face(cv, 150, 300, 56, rev(p, 0.04)); cv.text((250, 262), 'Mark on the face + a mirror:', 'serifr', 38, CREAM, 'la', rev(p, 0.06))
        cv.text((250, 306), 'does the animal touch the mark?', 'serifr', 38, CREAM, 'la', rev(p, 0.06))
        cv.para(W / 2, 810, 'Narrow test: mirror-guided behavior toward a mark. Not a test of consciousness.', 'sans', 32, DIMC, W - 200, 1.15, 'm', rev(p, 0.82))

# ------------------------------------------------------------------ a12 declaration
def sc_decl(cv, t, p):
    x0, y0, x1, y1 = (30, 360, W - 30, 1000) if PORT else (60, 215, W - 60, 700)
    ins = 90 if PORT else 85
    lv = [('MANY INVERTEBRATES: octopuses, crabs, insects', 'realistic possibility', LILAC, 0.55),
          ('ALL VERTEBRATES', 'realistic possibility', SKY, 0.32),
          ('MAMMALS AND BIRDS', 'strong scientific support', LIME, 0.08)]
    for k, (lab, st, col, f) in enumerate(lv):
        a = rev(p, f, 0.05)
        bx = (x0 + k * ins * (0.8 if PORT else 1.3), y0 + k * ins, x1 - k * ins * (0.8 if PORT else 1.3), y1 - k * ins * 0.55)
        cv.rect(bx, mix(col, BG, 0.10 * a), 26); cv.outline(bx, mix(col, BG, a), 4, 26)
        cv.text((bx[0] + 30, bx[1] + 18), lab, 'monob', 24 if PORT else 30, col, 'la', a)
        cv.text((bx[2] - 30, bx[1] + (54 if PORT else 18)), st.upper(), 'mono', 22 if PORT else 28, CREAM, 'ra', a)
    cv.para(W / 2, 1060 if PORT else 740, 'New York Declaration, April 2024: a judgment about evidence and probability, not a measurement.', 'sans', 30, DIMC, W - 180, 1.15, 'm', rev(p, 0.8))

# ------------------------------------------------------------------ a13 same words / indicators
def bubble(cv, x0, y0, x1, y1, txt, col, a):
    cv.rect((x0, y0, x1, y1), mix(col, BG, 0.16 * a), 28); cv.outline((x0, y0, x1, y1), mix(col, BG, a), 3, 28)
    cv.text(((x0 + x1) / 2, (y0 + y1) / 2 - 24), txt, 'serifr', 40 if PORT else 44, CREAM, 'ma', a)

def sc_words(cv, t, p):
    area = (30, 350, W - 30, 800) if PORT else (60, 215, W - 60, 530)
    b = boxes(2, area, 40)
    for bx, (lab, col, f) in zip(b, [('A PERSON', LIME, 0.06), ('A CHATBOT TRAINED ON HUMAN TEXT', LILAC, 0.2)]):
        a = rev(p, f); card(cv, bx, a, col); h = bx[3] - bx[1]
        cv.text((bx[0] + 26, bx[1] + 20), lab, 'monob', 24 if PORT else 28, col, 'la', a)
        bubble(cv, bx[0] + 40, bx[1] + h * 0.42, bx[2] - 40, bx[1] + h * 0.85, '"I feel something."', col, rev(p, f + 0.08))
    cv.text((W / 2, 815 if PORT else 548), 'Same words. Different causes.', 'serif', 40, PEACH, 'ma', rev(p, 0.34))
    ty = 900 if PORT else 640
    cv.text((W / 2, ty - 12 if not PORT else ty - 20), '2023: Butlin, Long and colleagues', 'monob', 26, DIMC, 'ma', rev(p, 0.55))
    steps = [('Leading theories', 0.58), ('Indicator properties', 0.7), ('Check AI systems', 0.82)]
    if PORT:
        for i, (lab, f) in enumerate(steps):
            a = rev(p, f); y = ty + 40 + i * 100; cv.rect((140, y, W - 140, y + 76), mix(SKY, BG, 0.15 * a), 14); cv.outline((140, y, W - 140, y + 76), mix(SKY, BG, a), 3, 14)
            cv.text((W / 2, y + 14), lab, 'serif', 38, CREAM, 'ma', a)
            if i < 2: arrow(cv, (W / 2, y + 78), (W / 2, y + 98), DIMC, 4, 12, rev(p, steps[i + 1][1]))
    else:
        for i, (lab, f) in enumerate(steps):
            a = rev(p, f); x = 120 + i * 600; cv.rect((x, ty + 40, x + 520, ty + 140), mix(SKY, BG, 0.15 * a), 16); cv.outline((x, ty + 40, x + 520, ty + 140), mix(SKY, BG, a), 3, 16)
            cv.text((x + 260, ty + 66), lab, 'serif', 46, CREAM, 'ma', a)
            if i < 2: arrow(cv, (x + 530, ty + 90), (x + 590, ty + 90), DIMC, 5, 16, rev(p, steps[i + 1][1]))

# ------------------------------------------------------------------ a14 AI assessment + theory dependence
def sc_ai(cv, t, p):
    top = (30, 350, W - 30, 700) if PORT else (60, 215, W - 60, 420)
    b = boxes(2, top, 30)
    for bx, (txt, f) in zip(b, [('Using theory-derived indicators, the analysis suggested no current AI system is conscious.', 0.06),
                                 ('It also found no obvious technical barrier to building systems that meet them.', 0.22)]):
        a = rev(p, f); card(cv, bx, a, SKY); cv.para(bx[0] + 26, bx[1] + 22, txt, 'serif', 32 if PORT else 34, CREAM, bx[2] - bx[0] - 52, 1.15, 'l', a)
    bot = (30, 730, W - 30, 1240) if PORT else (60, 450, W - 60, 830)
    b = boxes(2, bot, 30)
    for bx, (lab, big, small, col, f) in zip(b, [
        ('WORKSPACE-STYLE VIEWS', 'Consciousness as a kind of information processing', 'so a machine with the right design could count', LIME, 0.46),
        ('INTEGRATED INFORMATION THEORY', 'Physical causal structure matters', 'so software behavior alone would not settle it', PEACH, 0.7)]):
        a = rev(p, f); card(cv, bx, a, col); w = bx[2] - bx[0]
        cv.text((bx[0] + 26, bx[1] + 20), lab, 'monob', 24 if PORT else 28, col, 'la', a)
        y = cv.para(bx[0] + 26, bx[1] + 70, big, 'serif', 34 if PORT else 40, CREAM, w - 52, 1.12, 'l', a)
        cv.para(bx[0] + 26, y + 8, small, 'sans', 30 if PORT else 32, DIMC, w - 52, 1.2, 'l', a)

# ------------------------------------------------------------------ a15 ledger
def sc_ledger(cv, t, p):
    cols = [('ESTABLISHED', LIME, ['Brain measures track levels of consciousness in people who can report', 'Some unresponsive patients show hidden awareness'], 0.12),
            ('DISPUTED', PEACH, ['Which theory is right', 'How testable the theories are'], 0.4),
            ('OPEN', SKY, ['Whether any test can settle it for a fish, an octopus or a machine'], 0.7)]
    b = boxes(3, (30, 350, W - 30, 1240) if PORT else (60, 215, W - 60, 640), 26)
    for bx, (lab, col, items, f) in zip(b, cols):
        a = rev(p, f); card(cv, bx, a, col); w = bx[2] - bx[0]
        cv.text((bx[0] + 26, bx[1] + 22), lab, 'monob', 36, col, 'la', a)
        cv.rect((bx[0] + 26, bx[1] + 70, bx[0] + 146, bx[1] + 75), mix(col, BG, a))
        y = bx[1] + 100
        for k, it in enumerate(items):
            y = cv.para(bx[0] + 26, y, it, 'sans', 34 if PORT else 40, CREAM, w - 52, 1.18, 'l', rev(p, f + 0.05 + k * 0.08)) + 20

# ------------------------------------------------------------------ a16 end
SOURCES = ['Casali et al. 2013, Sci Transl Med 5:198ra105 (PCI)',
           'Casarotto et al. 2016, Ann Neurol 80:718 (PCI cutoff, patients)',
           'Owen et al. 2006, Science · Bodien et al. 2024, NEJM 391:598',
           'Cogitate Consortium 2025, Nature 642:133 (IIT vs GNWT)',
           'Fleming et al. 2023, PsyArXiv (IIT letter) · Gibbons et al. 2026, PLOS ONE (protocol)',
           'Gallup 1970, Science · Prior et al. 2008 · Kohda et al. 2019, PLoS Biology',
           'New York Declaration on Animal Consciousness, April 2024',
           'Butlin et al. 2023, arXiv:2308.08708 · Dehaene, Lau, Kouider 2017, Science']
def sc_end(cv, t, p):
    a = ease(t / 1.0); cy = 250 if PORT else 215
    cv.text((W / 2, cy - 20), 'Can consciousness be measured?', 'serif', 54 if PORT else 56, CREAM, 'ma', a)
    cv.para(W / 2, cy + 70, 'Some brain signatures of consciousness, in people: yes. Animals and machines: evidence informs judgments, but no current measure settles it conclusively.', 'serifr', 36 if PORT else 40, LIME, W - 160, 1.15, 'm', ease((t - 0.6) / 1.0))
    y = cy + (280 if PORT else 200)
    cv.text((W / 2, y), 'SOURCES', 'monob', 26, DIMC, 'ma', ease((t - 1.0) / 1.0))
    yy = y + 44
    for i, s in enumerate(SOURCES):
        yy = cv.para(W / 2, yy, s, 'mono', 26 if PORT else 24, CREAM, W - 80, 1.2, 'm', ease((t - 1.2 - i * 0.18) / 0.7)) + 8
    cv.text((W / 2, H - 130), 'Heartbeat Observatory  ·  heartbeatobservatory.com', 'sansb', 38 if PORT else 44, LIME, 'ma', ease((t - 2.5) / 1.0))

SCENES = [('a1', None, None, sc_title),
          ('a2', 'No one can observe it directly', None, sc_problem),
          ('a3', 'Tool 1: the echo of a pulse', 'Casali et al., Sci Transl Med 2013  ·  schematic of the idea, not real data', sc_pci),
          ('a4', 'Tested on people who could report', 'Casarotto et al., Annals of Neurology 2016', sc_numbers),
          ('a5', 'What that number means', 'Casarotto et al., Annals of Neurology 2016', sc_limits),
          ('a6', 'Tool 2: imagine it', 'Owen et al., Science 2006  ·  Bodien et al., NEJM 2024', sc_hidden),
          ('a7', 'The limit of the scan task', 'Bodien et al., NEJM 2024: 353 adults with disorders of consciousness', sc_passmiss),
          ('a8', 'Two rival theories', 'Schematic, not anatomically exact  ·  Cogitate Consortium 2025', sc_theories),
          ('a9', 'The test: both theories, head to head', 'Cogitate Consortium, Nature 642:133-142 (2025)', sc_cogitate),
          ('a10', 'Not everyone agrees', 'Fleming et al., PsyArXiv 2023  ·  Gibbons et al., PLOS ONE 2026', sc_dispute),
          ('a11', 'Animals: the mirror test', 'Gallup, Science 1970  ·  Prior et al., PLoS Biol 2008  ·  Kohda et al., PLoS Biol 2019', sc_mirror),
          ('a12', 'Animals: weighing the evidence', 'New York Declaration on Animal Consciousness, April 2024', sc_decl),
          ('a13', 'And AI systems?', 'Butlin et al., arXiv 2308.08708 (2023)', sc_words),
          ('a14', 'What the assessment depends on', 'Butlin et al. 2023  ·  Dehaene, Lau, Kouider, Science 2017', sc_ai),
          ('a15', 'Where things stand', None, sc_ledger),
          ('a16', None, None, sc_end)]
ailib.STATUS.update({'a2': ('THE PROBLEM', SKY), 'a3': ('ILLUSTRATION', LILAC), 'a4': ('PUBLISHED RESULT', LIME), 'a5': ('LIMITS', PEACH),
                     'a6': ('PUBLISHED RESULT', LIME), 'a7': ('LIMITS', PEACH), 'a8': ('COMPETING THEORIES', PEACH), 'a9': ('PUBLISHED RESULT', LIME),
                     'a10': ('DISPUTED', PEACH), 'a11': ('REPORTED, DEBATED', PEACH), 'a12': ('EXPERT STATEMENT', SKY), 'a13': ('ILLUSTRATION', LILAC),
                     'a14': ('THEORY-DEPENDENT', PEACH), 'a15': ('SUMMARY', LIME)})
configure(SUBS, SCENES)
if __name__ == '__main__': main()
