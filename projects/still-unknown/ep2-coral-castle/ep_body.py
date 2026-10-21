
import re
L = not PORT

# ------------------------------------------------------------------ helpers
def poly(cv, pts, fill): cv.d.polygon([cv.P(p) for p in pts], fill=fill)
def F(sid, f): return SEG[sid]['start'] + f * SEG[sid]['dur'] - BOUND[sid][0]
def ap(t, sid, f, d=0.8): return ease((t - F(sid, f)) / d)

def night(cv, tt, dim=0.5):
    for (x, y, r, b, ph) in STARS:
        tw = 0.65 + 0.35 * math.sin(tt * 1.1 + ph)
        cv.circ((x * W, y * H), r * 0.9, mix(TXT, BG, b * tw * dim))
    # a faint moon, low contrast, behind content
    mx, my = (W - 150, H - 520) if L else (W - 130, 120)
    for k in range(5, 0, -1): cv.circ((mx, my), 40 + k * 14, mix(VIO, BG, 0.025 * (6 - k) * dim * 2))
    cv.circ((mx, my), 40, mix(TXT, BG, 0.30 * dim * 2))

def stone(cv, x0, y0, x1, y1, a=1.0, col=DIM, label=None, fill=None):
    """a drawn limestone block: dark face, thin edge, faint bedding lines"""
    cv.rect((x0, y0, x1, y1), mix(fill or INK2, BG, a))
    cv.outline((x0, y0, x1, y1), mix(col, BG, a * 0.9), 2)
    n = max(1, int((y1 - y0) / 26))
    for i in range(1, n): cv.line([(x0 + 4, y0 + i * (y1 - y0) / n), (x1 - 4, y0 + i * (y1 - y0) / n)], mix(col, BG, a * 0.18), 1)
    if label: cv.text(((x0 + x1) / 2, (y0 + y1) / 2), label, 'monob', 20, TXT, 'mm', a)

def tripod(cv, cx, by, h, a=1.0, lift=0.0, sway=0.0, blk=True):
    ax, ay = cx + sway * h * 0.03, by - h
    feet = [(cx - 0.42 * h, by), (cx + 0.42 * h, by), (cx + 0.06 * h, by - 0.08 * h)]
    col = mix(DIM, BG, a)
    cv.line([(ax, ay), feet[2]], mix(DIM2, BG, a), 6)
    cv.line([(ax, ay), feet[0]], col, 8); cv.line([(ax, ay), feet[1]], col, 8)
    cv.circ((ax, ay), 8, mix(CYAN, BG, a))
    bw, bh = 0.24 * h, 0.15 * h
    top = by - 0.22 * h - lift * 0.42 * h - bh
    bx = cx + sway * h * 0.03
    cv.line([(ax, ay), (bx, top)], mix(CYAN, BG, a * 0.8), 2)
    if blk: stone(cv, bx - bw / 2, top, bx + bw / 2, top + bh, a, CYAN)
    cv.line([(cx - 0.7 * h, by), (cx + 0.7 * h, by)], mix(DIM2, BG, a), 2)

def card(cv, x, y, w, h, col, a=1.0):
    cv.rect((x, y, x + w, y + h), mix(INK, BG, a * 0.9)); cv.rect((x, y, x + 5, y + h), mix(col, BG, a))

def stack(cv, x, y, rows, a_list, size=26, gap=8, maxw=600, col=TXT, kind='sans'):
    for (txt, a) in zip(rows, a_list):
        y = cv.para(x, y, txt, kind, size, col, maxw, 1.25, 'l', a) + gap
    return y

def hdr(cv, label, a=1.0):
    mono(cv, HEAD[0], (300 if PORT else 250), label, 28 if PORT else 26, CYAN, a)

# ------------------------------------------------------------------ scenes
def sc_title(cv, t, p):
    night(cv, t, 0.9)
    a = ease(t / 2.0)
    y0 = 300 if PORT else 250
    mono(cv, HEAD[0], y0, 'HEARTBEAT TV  /  CH 10  /  STILL UNKNOWN  /  EP 02', 28 if PORT else 26, CYAN, ease(t / 1.0))
    sz = 100 if PORT else 118
    lines = ('coral castle:', 'one man,', '1,100 tons') if PORT else ('coral castle:', 'one man, 1,100 tons')
    for k, l in enumerate(lines): big(cv, HEAD[0], y0 + 60 + k * sz * 1.05, l, sz, TXT, ease((t - 0.3 - k * 0.25) / 1.2))
    yy = y0 + 60 + len(lines) * sz * 1.05 + 40
    mono(cv, HEAD[0], yy, 'the 1,100 is the castle\'s own figure: we check it', 24, DIM, ease((t - 1.5) / 1.0))
    ty = yy + 70
    x = HEAD[0]
    for i, (lab, col, f) in enumerate((('DOCUMENTED', MINT, 0.35), ('CLAIMED', VIO, 0.5), ('NOT ESTABLISHED', ROSE, 0.7), ('UNKNOWN', ROSE, 0.88))):
        aa = ap(t, 's1', f, 0.8)
        if PORT:
            tag(cv, HEAD[0], ty + i * 62, lab, col, aa)
        else:
            w = tag(cv, x, ty, lab, col, aa)
            x += (w if w > 0 else 0) + 20
            x = x if aa > 0 else x
    # lift the stone, slowly, at right
    lift = 0.15 + 0.1 * math.sin(t * 0.5)
    if L: tripod(cv, 1560, 850, 520, a, lift, math.sin(t * 0.7))
    else: tripod(cv, 800, 1330, 380, a, lift, math.sin(t * 0.7))

def timeline(cv, evs, t, sid):
    x0, y0, x1, y1 = CONT
    if L:
        ly = y0 + 250; n = len(evs); step = (x1 - x0 - 200) / (n - 1)
        cv.line([(x0, ly), (x1 - 100, ly)], INK2, 3)
        for i, (yr, txt, col, f) in enumerate(evs):
            a = ap(t, sid, f); px = x0 + 40 + i * step
            if a <= 0: continue
            cv.circ((px, ly), 11, mix(col, BG, a)); big(cv, px - 10, ly - 120, yr, 60, TXT, a)
            cv.para(px - 10, ly + 40, txt, 'sans', 28, TXT, step - 40, 1.25, 'l', a)
    else:
        n = len(evs); ly = x0 + 40
        cv.line([(ly, y0), (ly, y0 + 800)], INK2, 3)
        for i, (yr, txt, col, f) in enumerate(evs):
            a = ap(t, sid, f); py = y0 + 20 + i * 200
            if a <= 0: continue
            cv.circ((ly, py + 30), 11, mix(col, BG, a)); big(cv, ly + 50, py, yr, 62, TXT, a)
            cv.para(ly + 50, py + 80, txt, 'sans', 32, TXT, 820, 1.2, 'l', a)

def sc_man(cv, t, p):
    night(cv, t, 0.5)
    tag(cv, CONT[0], CONT[1] - 40, 'REPORTED: AS TOLD IN THE NRHP FORM, 1984', CYAN, ease(t / 0.8))
    evs = [('1887', 'born in Latvia', MINT, 0.18), ('about 1913', 'engaged at about 26; the bride calls off the wedding', MINT, 0.38),
           ('1910s', 'jobs across North America, a lumber camp, poor health', MINT, 0.66), ('early 1920s', 'reaches Florida City', MINT, 0.86)]
    timeline(cv, evs, t, 's2')

def sc_agnes(cv, t, p):
    night(cv, t, 0.4)
    x0, y0, x1, y1 = CONT
    if L: cw = (x1 - x0 - 60) / 2; boxes = [(x0, y0 + 20, cw, 440), (x0 + cw + 60, y0 + 20, cw, 440)]
    else: boxes = [(x0, y0, x1 - x0, 400), (x0, y0 + 440, x1 - x0, 400)]
    (ax, ay, aw, ah), (bx, by, bw, bh) = boxes
    a1 = ease(t / 0.8); card(cv, ax, ay, aw, ah, VIO, a1)
    mono(cv, ax + 30, ay + 24, 'THE STORY AS TOLD', 22, VIO, a1)
    stack(cv, ax + 30, ay + 70, ['engaged at about 26 to Agnes, ten years younger', 'she called off the wedding shortly before it', 'he later called her "Sweet Sixteen"'],
          [ap(t, 's3', 0.0, 0.8), ap(t, 's3', 0.05, 0.8), ap(t, 's3', 0.1, 0.8)], 32 if L else 30, 14, aw - 60)
    tag(cv, ax + 30, ay + ah - 70, 'CLAIMED: TOLD LATER', VIO, a1, 22)
    a2 = ap(t, 's3', 0.18); card(cv, bx, by, bw, bh, ROSE, a2)
    mono(cv, bx + 30, by + 24, 'THE NAME', 22, ROSE, a2)
    stack(cv, bx + 30, by + 70, ['NRHP 1984 form: "Scuff", footnote also gives "Skuvst"', 'one Latvian account: a different name and age'],
          [ap(t, 's3', 0.28, 0.8), ap(t, 's3', 0.45, 0.8)], 32 if L else 30, 14, bw - 60)
    tag(cv, bx + 30, by + bh - 70, 'NOT SETTLED', ROSE, ap(t, 's3', 0.6), 22)

def sc_site(cv, t, p):
    night(cv, t, 0.5)
    x0, y0, x1, y1 = CONT
    tag(cv, x0, y0 - 40, 'DOCUMENTED: NRHP FORM, 1984', MINT, ease(t / 0.8))
    # schematic plan (not to scale)
    if L: px, py, pw, ph = x0 + 40, y0 + 60, 640, 420
    else: px, py, pw, ph = x0 + 20, y0 + 20, 700, 420
    a = ease(t / 1.2)
    cv.outline((px, py, px + pw, py + ph), mix(CYAN, BG, a), 3)
    mono(cv, px, py - 28, 'ED\'S PLACE, FLORIDA CITY: schematic, not to scale', 18, DIM, a)
    tw = ap(t, 's4', 0.45)
    cv.rect((px + 40, py + 40, px + 200, py + 190), mix(INK2, BG, tw)); cv.outline((px + 40, py + 40, px + 200, py + 190), mix(VIO, BG, tw), 2)
    cv.text((px + 120, py + 115), 'two-story tower', 'mono', 18, TXT, 'mm', tw)
    fu = ap(t, 's4', 0.75)
    for (fx, fy, fw, fh, lab) in ((300, 60, 90, 60, 'table'), (420, 60, 70, 70, 'chair'), (300, 160, 120, 50, 'bench'), (470, 190, 90, 70, 'chair'), (330, 270, 120, 90, 'sundial?')):
        cv.rect((px + fx, py + fy, px + fx + fw, py + fy + fh), mix(INK2, BG, fu)); cv.outline((px + fx, py + fy, px + fx + fw, py + fy + fh), mix(DIM, BG, fu), 1)
    cv.text((px + 330, py + 380), 'furniture, astronomy pieces', 'mono', 18, DIM, 'lm', fu)
    pit = ap(t, 's4', 0.85)
    for k in range(3): cv.ring((px + 60 + k * 100, py + ph + 70), 36, mix(DIM2, BG, pit), 2)
    cv.text((px + 330, py + ph + 70), 'quarry pits outside the wall', 'mono', 18, DIM, 'lm', pit)
    # facts
    fx0 = x0 + 760 if L else x0 + 20; fy0 = y0 + 40 if L else y0 + 530
    ga = ap(t, 's4', 0.1); big(cv, fx0, fy0, '1923', 110 if L else 100, TXT, ga)
    stack(cv, fx0, fy0 + (130 if L else 120), ['one acre, $12 (Dade County Deed Book 1546, p. 8)', 'ground: oolitic limestone, "coral rock"'],
          [ap(t, 's4', 0.15), ap(t, 's4', 0.3)], 28, 12, 900 if L else 900, DIM, 'mono')

def sc_move(cv, t, p):
    night(cv, t, 0.7)
    x0, y0, x1, y1 = CONT
    tag(cv, x0, y0 - 40, 'REPORTED', CYAN, ease(t / 0.8)); tag(cv, x0 + 190, y0 - 40, 'DATES CONFLICT', ROSE, ap(t, 's5', 0.3))
    lx0, lx1 = x0 + 60, x1 - 60
    ly = y0 + (200 if L else 160)
    a = ease(t / 1.0)
    cv.line([(lx0, ly), (lx1, ly)], mix(DIM2, BG, a), 3)
    for xx, nm in ((lx0, 'Florida City'), (lx1, 'Homestead')):
        cv.circ((xx, ly), 12, mix(CYAN, BG, a)); cv.text((xx, ly + 40), nm, 'mono', 26, TXT, 'ma', a)
    cv.text(((lx0 + lx1) / 2, ly - 50), 'about 10 miles', 'mono', 24, DIM, 'mm', a)
    # truck shuttling with a block, loaded one way
    ph = (t * 0.22) % 2.0; u = ph if ph < 1 else 2 - ph
    tx = lx0 + (lx1 - lx0) * ease(u)
    loaded = ph < 1
    cv.rect((tx - 50, ly - 56, tx + 10, ly - 12), mix(VIO, BG, a)); cv.rect((tx + 10, ly - 40, tx + 80, ly - 12), mix(INK2, BG, a))
    cv.outline((tx - 50, ly - 56, tx + 80, ly - 12), mix(DIM, BG, a), 2)
    cv.circ((tx - 30, ly - 8), 10, mix(TXT, BG, a)); cv.circ((tx + 50, ly - 8), 10, mix(TXT, BG, a))
    if loaded: stone(cv, tx + 14, ly - 82, tx + 76, ly - 40, a, CYAN)
    # date table
    ty = ly + (130 if L else 130)
    rows = [('by 1936', 'buys 10 acres at Homestead (castle chronology)', 0.2), ('1937', 'the 1984 NRHP form: "moved date 1937"', 0.35), ('1939', 'obelisk: "Moved in 1939"; land clearing from May 1939', 0.5),
            ('hauling', 'Bob Biggers, a farmer, hauls the stones (form: his truck; castle: a trailer)', 0.7), ('loading', 'Ed loads and unloads alone, at night (form and later accounts)', 0.88)]
    for i, (k, v, f) in enumerate(rows):
        aa = ap(t, 's5', f); yy = ty + i * (62 if L else 100)
        if aa <= 0: continue
        mono(cv, x0 + 20, yy, k, 28, CYAN, aa)
        if L: cv.text((x0 + 250, yy), v, 'sans', 32, TXT, 'la', aa)
        else: cv.para(x0 + 20, yy + 36, v, 'sans', 30, TXT, 900, 1.2, 'l', aa)

def sc_weights(cv, t, p):
    night(cv, t, 0.4)
    x0, y0, x1, y1 = CONT
    tag(cv, x0, y0 - 40, 'REPORTED: WEIGHTS PRINTED IN THE NRHP FORM, 1984', CYAN, ease(t / 0.8), 20)
    items = [('Polaris sighting slab', 20, 0.12), ('each quarter moon', 18, 0.28), ('full moon fountain', 23, 0.4), ('obelisk', 28.5, 0.55), ('north-wall sculpture', 30, 0.78)]
    lw = 430 if L else 0
    bx0 = x0 + (lw + 30 if L else 0); bmax = (x1 - bx0 - 240) if L else (x1 - x0 - 380)
    rh = 96 if L else 140
    for i, (nm, v, f) in enumerate(items):
        aa = ap(t, 's6', f); yy = y0 + 30 + i * rh
        if aa <= 0: continue
        if L: cv.text((x0, yy + 28), nm, 'sans', 30, TXT, 'la', aa); by = yy + 14
        else: cv.text((x0, yy), nm, 'sans', 32, TXT, 'la', aa); by = yy + 50
        wlen = bmax * v / 30 * ease((t - F('s6', f)) / 1.2)
        cv.rect((bx0, by, bx0 + wlen, by + (46 if L else 50)), mix(CYAN, BG, aa * 0.85))
        cv.text((bx0 + wlen + 16, by + (23 if L else 25)), f'{v:g} short tons', 'monob', 26, TXT, 'lm', aa)
    yy = y0 + 30 + len(items) * rh + 10
    mono(cv, x0, yy, '1 short ton = 2,000 lb.  The form\'s published estimates, not weighings.', 20, DIM, ap(t, 's6', 0.5))
    mono(cv, x0, yy + 30, 'Castle site: heaviest piece "over 21 tons". Wall blocks: 8 x 4 x 3 ft, "several tons".', 20, DIM, ap(t, 's6', 0.85))

def sc_total(cv, t, p):
    night(cv, t, 0.4)
    x0, y0, x1, y1 = CONT
    a = ease(t / 1.2)
    big(cv, x0, y0 + 10, '1,100', 220 if L else 200, TXT, a)
    mono(cv, x0 + (640 if L else 20), y0 + (150 if L else 270), 'short tons: the castle\'s own total', 30, VIO, a)
    tag(cv, x0 + (640 if L else 20), y0 + (210 if L else 330), 'CLAIMED', VIO, ap(t, 's7', 0.3)); tag(cv, x0 + (800 if L else 200), y0 + (210 if L else 330), 'SOURCE UNTRACED', ROSE, ap(t, 's7', 0.55))
    ty = y0 + (330 if L else 460)
    rows = [('coralcastle.com', 'states "1,100 tons"; no estimator named', 0.15), ('Wikipedia', '1,100 short tons; figure not attributed', 0.3), ('NRHP form, 1984', 'lists pieces "up to 30 tons"; no total', 0.45), ('C. A. Lake, 1950s', 'adds walls and tower: "over 1000 tons"', 0.62), ('first use of "1,100"', 'not found', 0.8)]
    for i, (k, v, f) in enumerate(rows):
        aa = ap(t, 's7', f); yy = ty + i * (62 if L else 100)
        hline(cv, x0, x1, yy - 10, INK2, aa, 1)
        mono(cv, x0 + 10, yy + 4, k, 26, CYAN if i < 4 else ROSE, aa)
        if L: cv.text((x0 + 380, yy), v, 'sans', 32, TXT if i < 4 else ROSE, 'la', aa)
        else: cv.text((x0 + 10, yy + 40), v, 'sans', 32, TXT if i < 4 else ROSE, 'la', aa)

def sc_gate(cv, t, p):
    night(cv, t, 0.4)
    x0, y0, x1, y1 = CONT
    tag(cv, x0, y0 - 40, 'DIMENSIONS: NRHP FORM', MINT, ease(t / 0.8)); tag(cv, x0 + 330, y0 - 40, 'REPAIR: REPORTED', CYAN, ap(t, 's8', 0.5))
    sc = 3.6 if L else 3.3
    gw, gh = 81 * sc, 92 * sc
    ex, ey = (x0 + 120, y0 + 60) if L else (x0 + 20, y0 + 20)
    a = ease(t / 1.0)
    stone(cv, ex, ey + 20, ex + 130, ey + 20 + gh + 30, a, DIM)
    stone(cv, ex + 130 + gw, ey + 20, ex + 260 + gw, ey + 20 + gh + 30, a, DIM)
    stone(cv, ex, ey - 20, ex + 260 + gw, ey + 20, a, DIM)      # lintel
    ga = ap(t, 's8', 0.12)
    stone(cv, ex + 130, ey + 22, ex + 130 + gw, ey + 20 + gh + 30, ga, CYAN)
    cx = ex + 130 + gw / 2
    sa = ap(t, 's8', 0.35)
    cv.line([(cx, ey - 20), (cx, ey + 20 + gh + 30)], mix(VIO, BG, sa), 5)
    cv.text((cx + 14, ey + 60), 'central shaft', 'mono', 18, VIO, 'la', sa); cv.text((cx + 14, ey + 84), '(auto axle, per form)', 'mono', 18, VIO, 'la', sa)
    cv.text((cx, ey + 20 + gh + 66), '81 in wide x 92 in tall x 21 in thick', 'monob', 20, TXT, 'ma', ga)
    # top view with swing
    tvx, tvy = (ex + 260 + gw + 190, ey + 150) if L else (ex + 260 + gw + 90, ey + 190)
    ang = math.radians(75 * (0.5 - 0.5 * math.cos(t * 0.9)))
    cv.line([(tvx - 150, tvy), (tvx - 100, tvy)], mix(DIM, BG, a), 8); cv.line([(tvx + 100, tvy), (tvx + 150, tvy)], mix(DIM, BG, a), 8)
    r = 100
    cv.line([(tvx - r * math.cos(ang), tvy - r * math.sin(ang)), (tvx + r * math.cos(ang), tvy + r * math.sin(ang))], mix(CYAN, BG, ga), 12)
    cv.circ((tvx, tvy), 9, mix(VIO, BG, sa)); cv.text((tvx, tvy + 130), 'top view: swings on its center', 'mono', 18, DIM, 'ma', ga)
    # 1986 facts
    fy = ey + 20 + gh + 130
    rows = [('"nine ton" (form): see the next check', 0.35, MINT), ('reported to turn with one finger (form, 1984)', 0.45, MINT), ('mid-1980s: stopped turning, 1984 or 1986 (sources differ)', 0.62, CYAN), ('six men and a crane lifted it out (50-ton in one account); rusted truck bearing replaced', 0.8, CYAN)]
    fx = x0 + (1130 if L else 20); yy = (ey + 20) if L else fy
    for i, (txt, f, col) in enumerate(rows):
        aa = ap(t, 's8', f)
        if aa <= 0: continue
        cv.rect((fx, yy + 6, fx + 5, yy + 36), mix(col, BG, aa))
        yy = cv.para(fx + 20, yy, txt, 'sans', 32 if L else 30, TXT, (x1 - fx - 30) if L else 900, 1.2, 'l', aa) + (24 if L else 12)

def sc_check(cv, t, p):
    night(cv, t, 0.4)
    x0, y0, x1, y1 = CONT
    tag(cv, x0, y0 - 40, 'OUR ARITHMETIC', CYAN, ease(t / 0.8)); tag(cv, x0 + 270, y0 - 40, 'NOT SETTLED: GATE WEIGHT', ROSE, ap(t, 's9', 0.6))
    vol_in3 = 81 * 92 * 21; vft = vol_in3 / 1728.0
    rows = [('calcite, solid (2.71 g/cm3)', 2.71, 0.0), ('aragonite, solid (2.93 g/cm3)', 2.93, 0.0), ('aragonite, 30% pore space', 2.93 * 0.7, 0.0), ('calcite, 30% pore space', 2.71 * 0.7, 0.0)]
    a0 = ap(t, 's9', 0.05)
    mono(cv, x0, y0 + 10, f'81 x 92 x 21 in = {vol_in3:,} cubic in = {vft:.1f} cubic ft', 30 if L else 26, TXT, a0)
    mono(cv, x0, y0 + 56, '(1 g/cm3 = 62.43 lb/ft3; weight = volume x density)', 20, DIM, a0)
    order = [1, 0, 2, 3]; fr = [0.3, 0.38, 0.55, 0.62]
    scale_max = 10.0; bx0 = x0 + (500 if L else 0); bw = (x1 - bx0 - 150) if L else (x1 - x0 - 200)
    for i, k in enumerate(order):
        nm, d, _ = rows[k]; aa = ap(t, 's9', fr[i]); tons = vft * d * 62.428 / 2000.0
        yy = y0 + 120 + i * (84 if L else 120)
        if aa <= 0: continue
        if L: cv.text((x0, yy + 10), nm, 'sans', 28, TXT, 'la', aa); by = yy
        else: cv.text((x0, yy), nm, 'sans', 28, TXT, 'la', aa); by = yy + 40
        wl = bw * tons / scale_max * ease((t - F('s9', fr[i])) / 1.0)
        col = ROSE if i < 2 else MINT
        cv.rect((bx0, by, bx0 + wl, by + 44), mix(col, BG, aa * 0.8)); cv.text((bx0 + wl + 14, by + 22), f'{tons:.1f} short tons', 'monob', 24, TXT, 'lm', aa)
    ua = ap(t, 's9', 0.45)
    ux = bx0 + bw * 0.9
    ytop = y0 + 100; ybot = y0 + 120 + 4 * (84 if L else 120)
    cv.line([(ux, ytop), (ux, ybot)], mix(VIO, BG, ua), 3); cv.text((ux, ytop - 8), 'form: "nine ton"', 'monob', 22, VIO, 'ms', ua)
    mono(cv, x0, ybot + 20, 'densities: standard mineral values. 30% porosity is our assumption.', 20, DIM, ap(t, 's9', 0.7))
    mono(cv, x0, ybot + 50, 'full rectangle assumed, dry rock; a 1950s engineer\'s book gives other dimensions (about 7 x 5 x 3 ft)', 20, DIM, ap(t, 's9', 0.82))

def sc_tools(cv, t, p):
    night(cv, t, 0.5)
    x0, y0, x1, y1 = CONT
    lift = 0.35 + 0.3 * math.sin(t * 0.4)
    if L: tripod(cv, x0 + 330, y0 + 570, 520, ease(t / 1.0), lift, math.sin(t * 0.6))
    else: tripod(cv, x1 - 200, y0 + 330, 300, ease(t / 1.0), lift, math.sin(t * 0.6))
    tx = x0 + (720 if L else 0); ty = y0 + (0 if L else 360)
    rows = [('DOCUMENTED', MINT, 'tools on display (NRHP 1984): block and tackle ("metal fall"), rollers, jacks, wedges, slings, cables, sledges, chisels; some made from old car parts', 0.15),
            ('DOCUMENTED', MINT, 'old photographs show tall wooden tripods with chains, and a chain hoist', 0.5),
            ('UNKNOWN', ROSE, 'exact rig set-up and procedures: "no detailed records" (Rock Gate Park, an independent archive site)', 0.78)]
    yy = ty
    for lab, col, txt, f in rows:
        aa = ap(t, 's10', f)
        if aa > 0:
            tag(cv, tx, yy, lab, col, aa, 20)
            yy = cv.para(tx, yy + 56, txt, 'sans', 30 if L else 28, TXT, (x1 - tx - 20), 1.22, 'l', aa) + 22
    mono(cv, x0, y1 - (10 if L else 0), 'diagram: ILLUSTRATION of a pole tripod, not a drawing of his rig', 18, DIM, ease((t - 2) / 1.0))

def pulley(cv, cx, cy, w, a, col):
    cv.rect((cx - w / 2, cy - 22, cx + w / 2, cy + 22), mix(INK2, BG, a)); cv.outline((cx - w / 2, cy - 22, cx + w / 2, cy + 22), mix(col, BG, a), 2)
    for k in range(3): cv.ring((cx - w / 3 + k * w / 3, cy), 12, mix(col, BG, a), 2)

def sc_tackle(cv, t, p):
    night(cv, t, 0.3)
    x0, y0, x1, y1 = CONT
    tag(cv, x0, y0 - 40, 'ILLUSTRATION: IDEAL, NO FRICTION', CYAN, ease(t / 0.8), 20)
    a = ease(t / 1.0)
    dx, dy = (x0 + 220, y0 + 90) if L else (x0 + 220, y0 + 70)
    u = 0.5 - 0.5 * math.cos(t * 0.5)
    topy = dy; boty = dy + 330 - 150 * u
    w = 280
    pulley(cv, dx, topy, w, a, DIM)
    pulley(cv, dx, boty, w, a, CYAN)
    for k in range(6):
        xx = dx - w / 2 + 14 + k * (w - 28) / 5
        cv.line([(xx, topy + 22), (xx, boty - 22)], mix(TXT, BG, a * 0.7), 2)
    cv.line([(dx + w / 2, topy), (dx + w / 2 + 70, topy), (dx + w / 2 + 70, topy + 380 + 30 * u)], mix(VIO, BG, a), 3)
    mono(cv, dx + w / 2 + 84, topy + 330, 'pull', 22, VIO, a)
    cv.line([(dx, boty + 22), (dx, boty + 70)], mix(TXT, BG, a * 0.7), 2)
    stone(cv, dx - 70, boty + 70, dx + 70, boty + 150, a, CYAN, '10 tons')
    cv.line([(dx, dy - 40), (dx, topy - 22)], mix(DIM, BG, a), 4)
    sx = x0 + (560 if L else 0); sy = y0 + (20 if L else 600)
    rows = [('load: 10 short tons = 20,000 lb', 0.0, TXT), ('6 rope segments:  20,000 / 6 = 3,333 lb pull', 0.18, TXT), ('two sets, 6 x 6 = 36:  20,000 / 36 = 556 lb', 0.4, TXT),
            ('+ 5:1 winch, 36 x 5 = 180:  20,000 / 180 = 111 lb', 0.58, MINT), ('cost: 36 ft of tackle rope per 1 ft of lift; ~180 ft of winch-handle travel', 0.78, ROSE)]
    for i, (txt, f, col) in enumerate(rows):
        aa = ap(t, 's11', f)
        if aa <= 0: continue
        yy = sy + i * (84 if L else 56)
        cv.rect((sx, yy + 4, sx + 5, yy + 44), mix(col, BG, aa)); cv.text((sx + 20, yy), txt, 'sans', 32 if L else 26, col, 'la', aa)
    mono(cv, sx, sy + 5 * (84 if L else 56) + 10, 'possible on paper; real rigs lose force to friction', 20, DIM, ap(t, 's11', 0.9))

def sc_lever(cv, t, p):
    night(cv, t, 0.3)
    x0, y0, x1, y1 = CONT
    tag(cv, x0, y0 - 40, 'ILLUSTRATION', CYAN, ease(t / 0.8))
    a = ease(t / 1.0)
    px, py = (x0 + 220, y0 + 330) if L else (x0 + 140, y0 + 330)
    ang = math.radians(-8 + 14 * (0.5 - 0.5 * math.cos(t * 0.8)))
    unit = 56
    lx, ly = px - unit * math.cos(ang), py + unit * math.sin(ang) * -1
    rx, ry = px + 9 * unit * math.cos(ang), py - 9 * unit * math.sin(ang) * -1
    poly(cv, [(px, py), (px - 30, py + 70), (px + 30, py + 70)], mix(DIM, BG, a))
    cv.line([(lx, ly), (rx, ry)], mix(TXT, BG, a), 10)
    stone(cv, lx - 60, ly - 70, lx + 10, ly - 4, a, CYAN)
    cv.line([(rx, ry - 70), (rx, ry - 8)], mix(VIO, BG, a), 4); poly(cv, [(rx - 10, ry - 20), (rx + 10, ry - 20), (rx, ry - 4)], mix(VIO, BG, a))
    cv.text((rx, ry - 84), 'push', 'mono', 20, VIO, 'ms', a); cv.text((px, py + 100), '1 : 9', 'monob', 26, TXT, 'ma', a)
    sx = x0 + (780 if L else 0); sy = y0 + (30 if L else 520)
    ap1 = ap(t, 's12', 0.25); ap2 = ap(t, 's12', 0.6)
    cv.text((sx, sy), 'force x arm = force x arm', 'monob', 32, TXT, 'la', ap1)
    cv.text((sx, sy + 60), '100 lb x 9 ft  =  900 lb x 1 ft', 'monob', 32, MINT, 'la', ap1)
    # cribbing: raise an inch, add a timber, repeat
    cy0 = sy + 170 if L else sy + 140
    for k in range(4):
        aa = ap(t, 's12', 0.55 + k * 0.1, 0.6)
        if aa <= 0: continue
        bx = sx + k * 170
        for j in range(k + 1): cv.rect((bx, cy0 + 120 - (j + 1) * 16, bx + 120, cy0 + 120 - j * 16 - 2), mix(DIM, BG, aa))
        stone(cv, bx + 10, cy0 + 120 - (k + 1) * 16 - 70, bx + 110, cy0 + 120 - (k + 1) * 16, aa, CYAN)
    cv.text((sx, cy0 + 150), 'raise an inch, slide a timber under, repeat', 'mono', 24, DIM, 'la', ap2); cv.text((sx, cy0 + 190), 'a principle, not a plan for a ten-ton block', 'mono', 20, DIM, 'la', ap2)

def sc_affidavit(cv, t, p):
    night(cv, t, 0.4)
    x0, y0, x1, y1 = CONT
    tag(cv, x0, y0 - 40, 'DOCUMENTED: 250+ AFFIDAVITS, 1955', MINT, ease(t / 0.8), 20)
    cols = 25 if L else 20; cell = 38 if L else 34
    for i in range(250):
        cx = x0 + 20 + (i % cols) * cell; cy = y0 + 40 + (i // cols) * cell
        lit = ease((t - 0.8 - i * 0.012) / 0.4)
        cv.circ((cx, cy), 7, mix(MINT, BG, 0.15 + 0.85 * lit))
    gy = y0 + 40 + (250 // cols + 1) * cell + 10
    qa = ap(t, 's13', 0.2)
    q = '"...without the aid of any individual or individuals... with simple hand tools..."'
    yy = cv.para(x0, gy, q, 'light', 36 if L else 34, TXT, (x1 - x0) * (0.55 if L else 1.0), 1.25, 'l', qa)
    mono(cv, x0, yy + 4, 'what the affiants signed, as quoted in the NRHP form (collected by the then-owner)', 18, DIM, qa)
    ub = ap(t, 's13', 0.62)
    tag(cv, x0, yy + 50, 'UNKNOWN', ROSE, ub, 22)
    cv.text((x0 + 170, yy + 54), 'who saw the largest blocks go up: the form quotes no one', 'sans', 28 if L else 26, TXT, 'la', ub)

def sc_words(cv, t, p):
    night(cv, t, 0.4)
    x0, y0, x1, y1 = CONT
    a = ease(t / 1.0)
    tag(cv, x0, y0 - 40, 'CLAIMED', VIO, a)
    qa = ap(t, 's14', 0.1)
    cv.rect((x0, y0 + 10, x0 + 5, y0 + (330 if L else 420)), mix(VIO, BG, qa))
    yy = cv.para(x0 + 30, y0 + 10, '"the methods used by the pyramid builders, the practical knowledge of the laws of leverage and weight"', 'light', 54 if L else 50, TXT, (x1 - x0 - 60) * (0.8 if L else 1), 1.2, 'l', qa)
    mono(cv, x0 + 30, yy + 10, 'Ed\'s reply to how he did it, as paraphrased in the NRHP form, 1984', 20, DIM, qa)
    py0 = y0 + (400 if L else 520)
    mono(cv, x0, py0, 'PAMPHLETS (he sold these)', 22, CYAN, ap(t, 's14', 0.55))
    ps = [('1936', 'A Book in Every Home', 0.62), ('Aug 1945', 'Magnetic Current', 0.76), ('Oct 1945', 'Mineral, Vegetable and Animal Life', 0.88)]
    for i, (yr, nm, f) in enumerate(ps):
        aa = ap(t, 's14', f); yy2 = py0 + 46 + i * 56
        mono(cv, x0, yy2, yr, 28, MINT, aa); cv.text((x0 + 200, yy2 - 2), nm, 'sans', 34, TXT, 'la', aa)
    mono(cv, x0, py0 + 46 + 3 * 56 + 6, 'we found none that describes how he lifted the blocks', 22, ROSE, ap(t, 's14', 0.95))

def sc_theories(cv, t, p):
    night(cv, t, 0.4)
    x0, y0, x1, y1 = CONT
    items = [('sound', 'sound levitates the stone', 0.12), ('magnetism', 'the pamphlets do not say this', 0.3), ('beyond Earth', 'help, or mastered gravity: in the 1984 form', 0.48)]
    for i, (a1, a2, f) in enumerate(items):
        aa = ap(t, 's15', f)
        if aa <= 0: continue
        if L:
            cw = (x1 - x0 - 80) / 3; cx = x0 + i * (cw + 40); cy = y0 + 10; ch = 330
        else:
            cw = x1 - x0; cx = x0; cy = y0 + i * 235; ch = 215
        card(cv, cx, cy, cw, ch, ROSE, aa)
        big(cv, cx + 28, cy + 24, a1, 48 if L else 46, TXT, aa)
        cv.para(cx + 28, cy + 96, a2, 'sans', 28, DIM, cw - 56, 1.2, 'l', aa)
        if L:
            tag(cv, cx + 28, cy + ch - 120, 'NOT ESTABLISHED', ROSE, aa, 20); mono(cv, cx + 28, cy + ch - 62, 'evidence found: none', 22, TXT, aa)
        else:
            tag(cv, cx + 28, cy + ch - 70, 'NOT ESTABLISHED', ROSE, aa, 20); mono(cv, cx + 330, cy + ch - 62, 'evidence found: none', 22, TXT, aa)
    ub = ap(t, 's15', 0.72); yb = y0 + (390 if L else 740)
    big(cv, x0, yb, 'absence of evidence is not proof of absence.', 44 if L else 38, TXT, ub)
    mono(cv, x0, yb + 70, 'floating-stone stories: secondhand. not established is not the same as impossible.', 22, DIM, ap(t, 's15', 0.85))

LEDGER = [('DOCUMENTED', MINT, 'land purchase, the form\'s printed weights, the tool list, photographs of hoisting gear', 0.2),
          ('REPORTED', CYAN, 'conflicting details: the move dates, the gate repair', 0.4),
          ('CLAIMED', VIO, 'worked alone  /  pyramid builders\' methods  /  1,100 tons', 0.58),
          ('NOT SETTLED', ROSE, 'the gate\'s true weight', 0.72),
          ('UNKNOWN', ROSE, 'exactly how the largest blocks were raised and set (working alone is claimed)', 0.85)]
def sc_ledger(cv, t, p):
    night(cv, t, 0.3)
    x0, y0, x1, y1 = CONT
    big(cv, x0, y0 + 10, 'the ledger', 56 if PORT else 64, TXT, ease(t / 1.0))
    step = 150 if PORT else 100
    for i, (st, col, txt, f) in enumerate(LEDGER):
        a = ap(t, 's16', f)
        if a <= 0: continue
        yy = y0 + 110 + i * step
        hline(cv, x0, x1, yy, INK2, a, 1)
        tag(cv, x0, yy + 16, st, col, a, 22)
        if L: big(cv, x0 + 360, yy + 10, txt, 38, TXT, a)
        else: cv.para(x0, yy + 76, txt, 'light', 38, TXT, x1 - x0, 1.15, 'l', a)

def sc_close(cv, t, p):
    night(cv, t, 0.8)
    x0, y0, x1, y1 = CONT
    a = ease(t / 1.0)
    sz = 120 if L else 100
    big(cv, x0, y0 + 20, 'not established.', sz, TXT, ap(t, 's17', 0.45))
    big(cv, x0, y0 + 20 + sz * 1.2, 'not ruled out.', sz, TXT, ap(t, 's17', 0.62))
    tag(cv, x0, y0 + 20 + sz * 2.6, 'NOT ESTABLISHED', ROSE, ap(t, 's17', 0.5), 24); tag(cv, x0 + 330, y0 + 20 + sz * 2.6, 'NOT RULED OUT', MINT, ap(t, 's17', 0.68), 24)
    big(cv, x0, y0 + 20 + sz * 3.4, 'someone watching this might be the one who works it out.', 36 if L else 34, CYAN, ap(t, 's17', 0.82, 1.2))
    if L: tripod(cv, 1560, 830, 380, 0.5 * a, 0.2 + 0.1 * math.sin(t * 0.5), math.sin(t * 0.6))

SOURCES = [
    'NPS: National Register of Historic Places Inventory-Nomination Form, "Rock Gate (Ed\'s Place)" / Coral Castle. Florida Division of Archives, 2 Apr 1984; listed 10 May 1984; renamed Coral Castle 2011 (npgallery.nps.gov, asset 1ed2ccd0-b692-42dc-b28d-1227c1a23407)',
    'coralcastle.com: "The Secrets of Coral Castle" (1,100 tons) and "About Edward Leedskalnin" (chronology, Bob Biggers, heaviest piece over 21 tons, gate stopped 1984)',
    'C. A. Lake, Leedskalnin biography (1950s, engineer): "over 1000 tons". Wikipedia "Coral Castle" / "Edward Leedskalnin" (1,100 short tons, unattributed; repair accounts; read 2026-10-13)',
    'rockgatepark.com/the-tools (independent archive, not affiliated with the castle): hoisting-gear photographs; "no detailed records". Also Florida Memory item 328424. No photographs are used here: every picture is drawn.',
    'Further reading: P. A. Hancock, "The making of a modern myth: Edward Leedskalnin and the Coral Castle", Skeptic 18(1), 2013',
    'Our arithmetic (gate volume, density, block and tackle, lever): standard formulas; calcite 2.71, aragonite 2.93 g/cm3; 30% porosity assumed. Details: SOURCES.md']
def sc_end(cv, t, p):
    night(cv, t, 0.7)
    a = ease(t / 1.0)
    if L: tripod(cv, 1620, 700, 300, 0.35 * a, 0.2, 0.0)
    y = 160 if PORT else 70
    mono(cv, HEAD[0], y, 'HEARTBEAT TV  /  CH 10', 26, CYAN, a)
    big(cv, HEAD[0], y + 40, 'still unknown', 110 if PORT else 110, TXT, a)
    mono(cv, HEAD[0], y + (170 if PORT else 170), 'heartbeatobservatory.com', 34, CYAN, a)
    yy = y + (240 if PORT else 240)
    mono(cv, HEAD[0], yy, 'SOURCES', 22, DIM, ease((t - 0.6) / 1)); yy += 40
    for i, s in enumerate(SOURCES):
        yy = cv.para(HEAD[0], yy, s, 'mono', 21 if PORT else 22, TXT, (W - 2 * HEAD[0]) * (1 if PORT else 0.95), 1.25, 'l', ease((t - 0.8 - i * 0.15) / 0.8)) + 10

# (segment id, headline, source line, draw fn)
SCENES = [
    ('s1', None, 'Edward Leedskalnin, 1887-1951. 1,100 tons: castle figure, source untraced', sc_title),
    ('s2', 'a man from latvia', 'NRHP nomination form, Florida Division of Archives, 1984', sc_man),
    ('s3', 'a love story, and its gaps', 'NRHP form 1984 (name spellings, footnote 2); Wikipedia "Edward Leedskalnin"', sc_agnes),
    ('s4', 'ed\'s place, 1923', 'NRHP form 1984; Dade County Deed Book 1546, p. 8', sc_site),
    ('s5', 'the move to homestead', 'NRHP form 1984 (sec. 7, 8); obelisk inscription; coralcastle.com chronology', sc_move),
    ('s6', 'what the form weighs', 'NRHP form 1984: weights in pounds, converted here', sc_weights),
    ('s7', 'the 1,100-ton total', 'coralcastle.com; Wikipedia; NRHP form 1984; C. A. Lake (1950s)', sc_total),
    ('s8', 'the gate', 'NRHP form 1984; coralcastle.com; Wikipedia "Coral Castle" (repair accounts conflict)', sc_gate),
    ('s9', 'a check anyone can do', 'Volume x density. Our arithmetic, assumptions on screen', sc_check),
    ('s10', 'the tools', 'NRHP form 1984 (tool list); rockgatepark.com (independent archive)', sc_tools),
    ('s11', 'block and tackle', 'Ideal mechanical advantage = rope segments. Worked example, not his rig', sc_tackle),
    ('s12', 'the lever', 'Law of the lever. Worked example, not his method', sc_lever),
    ('s13', 'what no one has documented', 'NRHP form 1984 quoting the 1955 affidavits', sc_affidavit),
    ('s14', 'what he said', 'NRHP form 1984 (paraphrase of his reply; pamphlet list)', sc_words),
    ('s15', 'popular theories', 'NRHP form 1984 (extraterrestrial, gravity); thisunexplaineduniverse.com; the pamphlets', sc_theories),
    ('s16', None, 'Status as of October 2026', sc_ledger),
    ('s17', None, None, sc_close),
    ('s18', None, None, sc_end),
]

def _subs(text):
    out = []
    for s in re.split(r'(?<=[.?!])\s+', text.strip()):
        parts = [s]
        while True:
            nxt = []; changed = False
            for q in parts:
                if len(q) > 96:
                    cs = [m.end() for m in re.finditer(r'[,:] ', q)]
                    if cs:
                        k = min(cs, key=lambda c: abs(c - len(q) / 2)); nxt += [q[:k].strip(), q[k:].strip()]; changed = True; continue
                nxt.append(q)
            parts = nxt
            if not changed: break
        out += parts
    return out
SUBS = {s['id']: _subs(s['text']) for s in TL['segs']}

# ------------------------------------------------------------------ framework
bounds = []
for i, (sid, *_r) in enumerate(SCENES):
    s0 = 0.0 if i == 0 else SEG[sid]['start'] - 0.5
    s1 = TOTAL if i == len(SCENES) - 1 else SEG[SCENES[i + 1][0]]['start'] - 0.5
    bounds.append((s0, s1))
BOUND = {sid: b for (sid, *_r), b in zip(SCENES, bounds)}

def subtitle_at(sid, tt):
    seg = SEG[sid]; subs = SUBS[sid]; rel = tt - seg['start']
    if not subs or rel < -0.1 or rel > seg['dur'] + 0.8: return None
    tot = sum(len(s) for s in subs); acc = 0
    for s in subs:
        acc += len(s); b = acc / tot * seg['dur']
        if rel <= b + (0.8 if s is subs[-1] else 0): return s
    return subs[-1]

def frame(tt):
    cv = Cv()
    for i, (sid, head, src, fn) in enumerate(SCENES):
        s0, s1 = bounds[i]
        if s0 <= tt < s1 or (i == len(SCENES) - 1 and tt >= s0): break
    t = tt - s0; p = clamp01(t / max(0.1, s1 - s0 - 0.6))
    fn(cv, t, p)
    cv.rect((0, 0, 6, H), INK2)
    cv.vtext((14, H - (300 if PORT else 260)), 'STILL UNKNOWN', 'mono', 20, DIM, 0.8)
    mono(cv, 16, 30, f'{i + 1:02d}/{len(SCENES):02d}', 20, DIM, 0.8)
    if head:
        a = ease(t / 0.6)
        f = font('light', SZ['head']); ls = wrap(head, f, HEAD[2] - HEAD[0])
        for k, l in enumerate(ls): cv.text((HEAD[0], HEAD[1] + k * SZ['head'] * 1.1), l, 'light', SZ['head'], TXT, 'la', a)
        cv.rect((HEAD[0], HEAD[1] - 14, HEAD[0] + 44 * a, HEAD[1] - 11), mix(CYAN, BG, a))
    sub = subtitle_at(sid, tt)
    if sub:
        f = font('sans', SZ['cap']); ls = wrap(sub, f, CAP[2] - CAP[0] - 30); n = len(ls)
        lh = SZ['cap'] * 1.28; y0 = CAP[3] - n * lh - 10 if not PORT else CAP[1] + 10
        cv.rect((CAP[0] - 30, y0 - 10, CAP[0] - 30 + 5, y0 + n * lh + 4), CYAN)
        for k, l in enumerate(ls):
            tw = f.getlength(l) / SS
            cv.rect((CAP[0] - 12, y0 + k * lh + 4, CAP[0] + tw + 14, y0 + (k + 1) * lh + 2), mix(BG, INK, 0.72))
            cv.text((CAP[0], y0 + k * lh), l, 'sans', SZ['cap'], TXT, 'la')
    if src:
        a = ease(t / 1.2)
        mono(cv, SRC[0] if PORT else SRC[2], SRC[1], 'SOURCE', 18, CYAN, a, 'la' if PORT else 'ra')
        f = font('mono', SZ['src']); ls = wrap(src, f, SRC[2] - SRC[0])[:3]
        for k, l in enumerate(ls): cv.text((SRC[0] if PORT else SRC[2], SRC[1] + 26 + k * SZ['src'] * 1.25), l, 'mono', SZ['src'], DIM, 'la' if PORT else 'ra', a)
    im = cv.im.reduce(SS)
    fa = min(1.0, t / 0.35, (s1 - tt) / 0.35 if i < len(SCENES) - 1 else (TOTAL - tt) / 1.2)
    if fa < 1.0: im = Image.blend(Image.new('RGB', im.size, BG), im, max(0.0, fa))
    return im

def work(n): return frame(n / FPS).tobytes()

def main():
    if '--still' in sys.argv:
        i = sys.argv.index('--still'); frame(float(sys.argv[i + 1])).save(sys.argv[i + 2]); return
    out = sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else f'video_{ORI}.mp4'
    a, b = 0, int(TOTAL * FPS)
    if '--secs' in sys.argv:
        i = sys.argv.index('--secs'); a, b = int(float(sys.argv[i + 1]) * FPS), int(float(sys.argv[i + 2]) * FPS)
    ff = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                           '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
    pool = Pool(8)
    try:
        for k, buf in enumerate(pool.imap(work, range(a, b), chunksize=4)):
            ff.stdin.write(buf)
            if k % 600 == 0: print(k, '/', b - a, flush=True)
        pool.close(); pool.join()
    except Exception as e:
        print('pool error:', repr(e), flush=True)
    finally:
        try: ff.stdin.close()
        except Exception: pass
        ff.wait(); print('ffmpeg exit', ff.returncode, flush=True)

if __name__ == '__main__': main()
