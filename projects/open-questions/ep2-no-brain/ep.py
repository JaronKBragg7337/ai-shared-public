import sys; sys.path.insert(0, '..')
from oqlib import *
import tvlib, random

SCR = json.load(open('script.json'))
SUBS = {s['id']: s['disp'] for s in SCR}
SLIME = (236, 196, 72); SLIMED = (150, 118, 40)

def lab(cv, t, t0, txt, y, col=DIMC, size=32):
    a = ease((t - t0) / 0.7)
    if a > 0: cv.para(W / 2, y, txt, 'sans', size, col, W - 200, 1.2, 'm', a)

# ---------------------------------------------------------------- s1 title
def sc_title(cv, t, p):
    a = ease(t / 1.0); ty = 150 if PORT else 70
    cv.text((W / 2, ty), 'HEARTBEAT TV  ·  OPEN QUESTIONS  ·  EPISODE 2', 'sansb', 30 if PORT else 34, DIMC, 'ma', a)
    sz = 100 if PORT else 124
    for k, l in enumerate(('Can something learn', 'without a brain?')):
        cv.text((W / 2, ty + 90 + k * sz * 1.15), l, 'serif', sz, CREAM, 'ma', ease((t - 0.2) / 1.0), 5)
    y = 640 if PORT else 560; c = cue('s1', 1)
    a2 = ease((t - c) / 0.8)
    if PORT:
        pill(cv, W / 2, y - 60, 'NO BRAIN, NO NERVES', COR, a2, 36); cv.text((W / 2, y + 5), 'yet', 'serifr', 44, DIMC, 'ma', a2)
        pill(cv, W / 2, y + 100, 'BEHAVIOR CHANGES', TEA, a2, 36); y += 100
    else:
        pill(cv, W * 0.27, y, 'NO BRAIN, NO NERVES', COR, a2, 36)
        pill(cv, W * 0.73, y, 'BEHAVIOR CHANGES', TEA, a2, 36)
        cv.text((W / 2, y - 24), 'yet', 'serifr', 44, DIMC, 'ma', a2)
    lab(cv, t, cue('s1', 5), 'Published experiments only. Sources on screen.', y + 90, DIMC, 32)

# ---------------------------------------------------------------- s2 definition
def sc_def(cv, t, p):
    bx = (60, 200, 1860, 400) if not PORT else (30, 350, 1050, 650)
    a = ease((t - cue('s2', 1)) / 0.7); card(cv, bx, a, COR)
    cv.text((bx[0] + 34, bx[1] + 18), 'LEARNING, as researchers define it here', 'sansb', 30, COR, 'la', a)
    cv.para(bx[0] + 34, bx[1] + 70, 'An organism acts differently because of what happened before.', 'serif', 52 if not PORT else 48, CREAM, bx[2] - bx[0] - 68, 1.15, 'l', a)
    y = 450 if not PORT else 700
    w = 880 if not PORT else 1020; xs = (60, 980) if not PORT else (30, 30); ys = (y, y) if not PORT else (y, y + 220)
    for k, (title, txt, tc) in enumerate((('Habituation', 'learning to ignore something repeated and harmless', cue('s2', 4)), ('Association', 'linking one signal with another', cue('s2', 5)))):
        aa = ease((t - tc) / 0.6)
        if aa <= 0: continue
        b2 = (xs[k], ys[k], xs[k] + w, ys[k] + 190); card(cv, b2, aa, TEA)
        cv.text((b2[0] + 30, b2[1] + 18), title, 'serif', 50, TEA, 'la', aa)
        cv.para(b2[0] + 30, b2[1] + 88, txt, 'sans', 36, CREAM, w - 60, 1.15, 'l', aa)
    a6 = ease((t - cue('s2', 6)) / 0.7)
    if a6 > 0:
        yy = 680 if not PORT else 1180
        cv.text((W / 2, yy), 'Not part of this definition:', 'sansb', 32, DIMC, 'ma', a6)
        for k, (w_, dx) in enumerate((('thinking', -300), ('feeling', 0), ('awareness', 300))):
            pill(cv, W / 2 + dx * (1 if not PORT else 0.9), yy + 80, w_, LAV, ease((t - cue('s2', 6) - 0.5 - k * 0.4) / 0.5), 32)

# ---------------------------------------------------------------- s3 maze
NODES = {(i, j): (i, j) for i in range(6) for j in range(3)}
WALL_REMOVED = {((1, 0), (2, 0)), ((2, 1), (3, 1)), ((3, 0), (3, 1)), ((4, 1), (4, 2)), ((0, 1), (1, 1)), ((1, 2), (2, 2)), ((3, 2), (4, 2))}
def maze_edges():
    E = []
    for (i, j) in NODES:
        for d in ((1, 0), (0, 1)):
            n = (i + d[0], j + d[1])
            if n in NODES and ((i, j), n) not in WALL_REMOVED: E.append(((i, j), n))
    return E
def bfs_path(E, a, b):
    adj = {}
    for u, v in E: adj.setdefault(u, []).append(v); adj.setdefault(v, []).append(u)
    prev = {a: None}; q = [a]; dist = {a: 0}
    while q:
        u = q.pop(0)
        for v in adj.get(u, []):
            if v not in prev: prev[v] = u; dist[v] = dist[u] + 1; q.append(v)
    path = []; u = b
    while u is not None: path.append(u); u = prev.get(u)
    return path[::-1], dist
MEDGES = maze_edges(); MSTART, MEND = (0, 0), (5, 2)
MPATH, MDIST = bfs_path(MEDGES, MSTART, MEND)
MPSET = {frozenset(e) for e in zip(MPATH, MPATH[1:])}

def sc_maze(cv, t, p):
    area = (200, 215, 1720, 690) if not PORT else (80, 400, 1000, 880)
    card(cv, (area[0] - 50, area[1] - 40, area[2] + 50, area[3] + 40), ease(t / 0.6), DIMC)
    sx = (area[2] - area[0]) / 5; sy = (area[3] - area[1]) / 2
    pos = lambda n: (area[0] + n[0] * sx, area[1] + n[1] * sy)
    ts = cue('s3', 4); tr = cue('s3', 5); maxd = max(MDIST.values())
    for u, v in MEDGES:
        cv.line([pos(u), pos(v)], mix(DIMC, BG, 0.22), 34)
    for u, v in MEDGES:
        d = min(MDIST.get(u, 0), MDIST.get(v, 0))
        grow = clamp01((t - ts - d * 0.55) / 0.8)
        onp = frozenset((u, v)) in MPSET
        shrink = 0 if onp else clamp01((t - tr - 0.2 * (maxd - d)) / 1.2)
        g = grow * (1 - shrink)
        if g > 0:
            cv.line([pos(u), pos(v)], mix(SLIMED, BG, g), 30); cv.line([pos(u), pos(v)], mix(SLIME, BG, g), 22)
    af = ease((t - cue('s3', 3)) / 0.6)
    for n in (MSTART, MEND):
        c = pos(n); cv.circ(c, 40, mix(SAGE, BG, af)); cv.text((c[0], c[1] - 16), 'food', 'sansb', 24, BG, 'ma', af)
    a = ease((t - tr - 2) / 0.8)
    if a > 0: badge(cv, area[0] - 50, area[3] + 62, 'WHAT REMAINS: THE SHORTEST ROUTE', SAGE, a, 26)
    cv.text((area[2] + 50, area[3] + 66), 'schematic maze', 'sans', 26, DIMC, 'ra', 1.0)

# ---------------------------------------------------------------- s4 Tokyo network
CITY = [(0.5, 0.5), (0.35, 0.35), (0.65, 0.3), (0.2, 0.55), (0.8, 0.55), (0.4, 0.75), (0.62, 0.78), (0.12, 0.25), (0.88, 0.25), (0.3, 0.12), (0.72, 0.1), (0.9, 0.8), (0.1, 0.85)]
def mst_edges(extra):
    n = len(CITY); inT = {0}; E = []
    d = lambda a, b: math.dist(CITY[a], CITY[b])
    while len(inT) < n:
        u, v = min(((u, v) for u in inT for v in range(n) if v not in inT), key=lambda e: d(*e)); E.append((u, v)); inT.add(v)
    allp = sorted(((d(a, b), a, b) for a in range(n) for b in range(a + 1, n) if (a, b) not in E and (b, a) not in E))
    for k in range(extra): E.append(allp[k][1:])
    return E
NET_SLIME = mst_edges(5); NET_RAIL = mst_edges(3)
def netpanel(cv, bx, edges, col, a, t0, t):
    card(cv, bx, a, col)
    w = bx[2] - bx[0] - 120; h = bx[3] - bx[1] - 190
    P = lambda c: (bx[0] + 60 + c[0] * w, bx[1] + 120 + c[1] * h)
    for k, (u, v) in enumerate(edges):
        g = clamp01((t - t0 - 0.4 - k * 0.12) / 0.5)
        if g > 0: cv.line([P(CITY[u]), P(CITY[v])], mix(col, BG, g), 8)
    for c in CITY: cv.circ(P(c), 13, mix(CREAM, BG, a))
def sc_tokyo(cv, t, p):
    if PORT: b1 = (30, 360, 1050, 740); b2 = (30, 760, 1050, 1140)
    else: b1 = (60, 200, 940, 700); b2 = (980, 200, 1860, 700)
    a1 = ease((t - cue('s4', 1)) / 0.6); a2 = ease((t - cue('s4', 3)) / 0.6)
    netpanel(cv, b1, NET_SLIME, SLIME, a1, cue('s4', 1), t); netpanel(cv, b2, NET_RAIL, TEA, a2, cue('s4', 3), t)
    cv.text((b1[0] + 30, b1[1] + 18), 'Slime mold network', 'serif', 46, SLIME, 'la', a1); cv.text((b2[0] + 30, b2[1] + 18), 'Tokyo-area rail system', 'serif', 46, TEA, 'la', a2)
    a4 = ease((t - cue('s4', 4)) / 0.7)
    if a4 > 0: pill(cv, W / 2, 745 if not PORT else 1170, 'cost · efficiency · resilience: comparable', SAGE, a4, 34)
    cv.text((W / 2, 790 if not PORT else 1212), 'schematic: city positions are not to scale', 'sans', 24, DIMC, 'ma', ease((t - 1) / 1))

# ---------------------------------------------------------------- s5 habituation
def sc_habit(cv, t, p):
    ax0, ay0, ax1, ay1 = (140, 290, 1000, 680) if not PORT else (110, 470, 990, 800)
    a = ease((t - cue('s5', 1)) / 0.7)
    cv.rect((ax0, ay1, ax1, ay1 + 4), mix(DIMC, BG, a)); cv.rect((ax0, ay0, ax0 + 4, ay1), mix(DIMC, BG, a))
    cv.text((ax0, ay0 - 50), 'hesitation', 'sans', 28, DIMC, 'la', a); cv.text((ax1, ay1 + 14), 'days of crossing', 'sans', 28, DIMC, 'ra', a)
    vals = [1.0, 0.82, 0.62, 0.45, 0.32, 0.22]
    c5 = cue('s5', 5)
    bw = (ax1 - ax0) / 9
    for k, v in enumerate(vals):
        aa = ease((t - c5 + 1.2 - k * 0.5) / 0.5)
        x = ax0 + 40 + k * bw * 1.15; h = (ay1 - ay0) * v * aa
        if aa > 0: cv.rect((x, ay1 - h, x + bw, ay1), mix(COR, BG, aa), 6)
    a6 = ease((t - cue('s5', 6)) / 0.7)
    x = ax0 + 40 + 6 * bw * 1.15; h = (ay1 - ay0) * 0.6 * a6
    if a6 > 0:
        cv.rect((x, ay1 - h, x + bw, ay1), mix(LAV, BG, a6), 6); cv.text((x + bw / 2, ay1 + 50), 'after rest', 'sans', 24, LAV, 'ma', a6)
    a2 = ease((t - cue('s5', 2)) / 0.7)
    rx = 1080 if not PORT else 60; ry = 250 if not PORT else 880; rw = 780 if not PORT else 960
    if a2 > 0:
        bx = (rx, ry, rx + rw, ry + (210 if not PORT else 170)); card(cv, bx, a2, SLIME)
        cv.para(bx[0] + 26, bx[1] + 18, 'Slime mold must cross a bridge coated with a bitter but harmless substance (quinine or caffeine) to reach food.', 'sans', 32, CREAM, rw - 52, 1.15, 'l', a2)
    a7 = ease((t - cue('s5', 7)) / 0.7)
    if a7 > 0:
        y0 = ry + (250 if not PORT else 200)
        bx = (rx, y0, rx + rw, y0 + (150 if not PORT else 130)); card(cv, bx, a7, TEA)
        cv.para(bx[0] + 26, bx[1] + 18, 'Used to one substance, still hesitated at a different one.', 'sans', 32, CREAM, rw - 52, 1.15, 'l', a7)
    badge(cv, 140 if not PORT else 110, 750 if not PORT else 1020, 'SCHEMATIC SHAPE OF THE FINDING, NOT DATA', LAV, ease((t - 1) / 1), 24)

# ---------------------------------------------------------------- s6 fusion
def blob(cv, c, r, col, a, mark=None):
    cv.circ(c, r + 8, mix(SLIMED, BG, a)); cv.circ(c, r, mix(col, BG, a))
    if mark: cv.text((c[0], c[1] - 20), mark, 'sansb', 30, BG, 'ma', a)
def sc_fuse(cv, t, p):
    cy = 400 if not PORT else 640; cx = W / 2; sep = 360 if not PORT else 250
    f = clamp01((t - cue('s6', 2) - 0.5) / 2.2); d = sep * (1 - f)
    a = ease(t / 0.7)
    if f < 1.0:
        blob(cv, (cx - d, cy), 115, SLIME, a, 'used to it'); blob(cv, (cx + d, cy), 115, mix(SLIME, CREAM, 0.35), a, 'new')
    else:
        blob(cv, (cx, cy), 150, SLIME, 1.0, 'fused')
    a2 = ease((t - cue('s6', 3)) / 0.7)
    if a2 > 0: pill(cv, cx, cy + (215 if not PORT else 250), 'salt bridge: crossed more readily than a naive one', SAGE, a2, 34)
    a3 = ease((t - cue('s6', 4)) / 0.7)
    if a3 > 0: cv.para(W / 2, cy + (275 if not PORT else 330), "Researchers' conclusion: the learned response transferred through fusion.", 'serif', 44, CREAM, W - 250, 1.15, 'm', a3)
    a4 = ease((t - cue('s6', 5)) / 0.7)
    if a4 > 0: badge(cv, W / 2, cy + (370 if not PORT else 480), 'HOW IT IS STORED: STILL BEING STUDIED', LAV, a4, 26, 'm')

# ---------------------------------------------------------------- s7 anticipation
def sc_antic(cv, t, p):
    x0, x1 = (140, 1780) if not PORT else (80, 1000); y0, y1 = (280, 620) if not PORT else (480, 900)
    a = ease(t / 0.7); cv.rect((x0, y1, x1, y1 + 4), mix(DIMC, BG, a)); cv.text((x1, y1 + 14), 'time', 'sans', 26, DIMC, 'ra', a)
    cv.text((x0, y0 - 60), 'speed of the slime mold', 'sans', 26, DIMC, 'la', a)
    ps = [0.15, 0.35, 0.55]; pe = 0.75; sp = (x1 - x0)
    c2 = cue('s7', 2); c5 = cue('s7', 5); span = max(0.5, cue('s7', 4) - c2)
    tt = clamp01((t - c2) / span)
    def sp_at(u):
        v = 0.8
        for q in ps + [pe]: v -= 0.55 * math.exp(-((u - q) / 0.03) ** 2)
        return v
    for q in ps:
        qa = ease((t - c2 - (q - 0.05) / 0.6 * span) / 0.5)
        if qa > 0: cv.rect((x0 + sp * q - 18, y0, x0 + sp * q + 18, y1), mix(TEA, BG, 0.30 * qa))
    n = int(300 * 0.62 * tt) + 1
    pts = [(x0 + sp * k / 300, y1 - sp_at(k / 300) * (y1 - y0) * (1 if k / 300 <= 0.62 else 1)) for k in range(n)]
    cv.line(pts, mix(SLIME, BG, a), 7)
    c4 = cue('s7', 4); a4 = ease((t - c4) / 0.8)
    if a4 > 0:
        k0 = int(300 * 0.62); k1 = k0 + int((300 * 0.38) * clamp01((t - c4) / 2.5)) + 1
        pts2 = [(x0 + sp * k / 300, y1 - sp_at(k / 300) * (y1 - y0)) for k in range(k0, min(k1, 301))]
        if len(pts2) > 1: cv.line(pts2, mix(SLIME, BG, a4), 7)
        qx = x0 + sp * pe; cv.rect((qx - 18, y0, qx + 18, y1), mix(ROSE, BG, 0.15 * a4))
        cv.text((qx, y0 - 50), 'no pulse here', 'sansb', 28, ROSE, 'ma', a4)
    cv.text((x0 + sp * 0.35, y0 - 50), 'dry pulses', 'sansb', 28, TEA, 'ma', ease((t - c2) / 0.7))
    a5 = ease((t - c5) / 0.7)
    if a5 > 0: badge(cv, W / 2, y1 + 90, "AUTHORS' INTERPRETATION: ANTICIPATION", LAV, a5, 28, 'm')
    cv.text((W / 2, y1 + 170), 'schematic plot', 'sans', 24, DIMC, 'ma', ease((t - 1) / 1))

# ---------------------------------------------------------------- s8 mimosa
def leaf(cv, cx, cy, openness, col, a):
    cv.line([(cx, cy + 150), (cx, cy - 120)], mix(col, BG, a), 8)
    for k in range(6):
        y = cy - 100 + k * 40
        for s in (-1, 1):
            ang = openness * 1.15
            ex = cx + s * 80 * math.sin(ang); ey = y - 80 * math.cos(ang) * 0.2 + (1 - openness) * 40
            cv.line([(cx, y), (ex, ey)], mix(col, BG, a), 12)
def sc_mimosa(cv, t, p):
    cy = 450 if not PORT else 640
    xs = [W * 0.17, W * 0.38, W * 0.59] if not PORT else [W * 0.2, W * 0.5, W * 0.8]
    labs = ['first drops: leaves fold', 'after repeated drops: close less', 'about a month later: still reduced']
    ops = [0.0, 0.85, 0.85]
    for k in range(3):
        aa = ease((t - cue('s8', 1) - 1.0 - k * 1.4) / 0.7)
        if aa > 0:
            leaf(cv, xs[k], cy, ops[k], SAGE, aa)
            cv.para(xs[k], cy + 190, labs[k], 'sans', 28 if not PORT else 24, CREAM, 300 if not PORT else 280, 1.15, 'm', aa)
    a4 = ease((t - cue('s8', 4)) / 0.7)
    if a4 > 0: badge(cv, W * 0.84 if not PORT else W / 2, cy - 40 if not PORT else cy + 330, 'DEBATED', ROSE, a4, 44, 'm')
    a5 = ease((t - cue('s8', 5)) / 0.7)
    if a5 > 0: cv.para(W / 2, 745 if not PORT else 1090, 'Open: could fatigue explain it, and is it learning?', 'serif', 42 if not PORT else 38, CREAM, W - 300, 1.15, 'm', a5)

# ---------------------------------------------------------------- s9 pea
def sc_pea(cv, t, p):
    side_cards(cv, t, ('2016 report', LAV, ['Pea seedlings: fan paired with light', 'Reported: grew toward the fan', 'Gagliano et al., Scientific Reports'], ('REPORTED', LAV)),
               ('2020 repeat', ROSE, ['Markel tried to repeat it', 'Did not find the effect', 'Original authors disputed his setup; Markel disputed that'], ('DID NOT REPLICATE', ROSE)),
               cue('s9', 1), cue('s9', 3), area=((60, 215, 1860, 720) if not PORT else (30, 350, 1050, 1130)))
    a = ease((t - cue('s9', 5)) / 0.7)
    cv.text((W / 2, 765 if not PORT else 1190), 'Pea association: not established.', 'serif', 52 if not PORT else 44, ROSE, 'ma', a)

# ---------------------------------------------------------------- s10 stentor
def sc_stentor(cv, t, p):
    steps = ['bend away', 'reverse cilia', 'contract', 'detach']
    c2 = cue('s10', 2)
    for k, s in enumerate(steps):
        aa = ease((t - c2 - 0.6 - k * 1.3) / 0.6)
        if aa <= 0: continue
        if PORT: pill(cv, 380, 440 + k * 120, f'{k + 1}  {s}', COR, aa, 38)
        else:
            pill(cv, 300 + k * 440, 300, f'{k + 1}  {s}', COR, aa, 38)
            if k < 3: arrow(cv, (300 + k * 440 + 190, 300), (300 + (k + 1) * 440 - 190, 300), DIMC, 4, 16, aa)
    if not PORT:
        specs = (((60, 410, 940, 600), cue('s10', 1), '1902', 'Jennings described the sequence'), ((980, 410, 1860, 600), cue('s10', 4), '2019', 'Dexter et al., Current Biology: confirmed the hierarchy of avoidance responses'))
        for bx, tc, num, txt in specs:
            aa = ease((t - tc) / 0.6)
            if aa > 0: card(cv, bx, aa, LAV); cv.text((bx[0] + 30, bx[1] + 40), num, 'serif', 90, LAV, 'la', aa); cv.para(bx[0] + 260, bx[1] + 50, txt, 'sans', 34, CREAM, bx[2] - bx[0] - 290, 1.15, 'l', aa)
    else:
        specs = (((30, 960, 1050, 1110), cue('s10', 1), '1902', 'Jennings described the sequence'), ((30, 1130, 1050, 1280), cue('s10', 4), '2019', 'Dexter et al.: confirmed the hierarchy'))
        for bx, tc, num, txt in specs:
            aa = ease((t - tc) / 0.6)
            if aa > 0: card(cv, bx, aa, LAV); cv.text((bx[0] + 30, bx[1] + 28), num, 'serif', 80, LAV, 'la', aa); cv.para(bx[0] + 250, bx[1] + 40, txt, 'sans', 32, CREAM, bx[2] - bx[0] - 280, 1.15, 'l', aa)
    a6 = ease((t - cue('s10', 7)) / 0.7)
    if a6 > 0: badge(cv, W / 2, 680 if not PORT else 1310, 'NOT CLEARLY LEARNING', ROSE, a6, 34, 'm')

# ---------------------------------------------------------------- s11 what it shows
def sc_shows(cv, t, p):
    side_cards(cv, t, ('Reported', SAGE, ['Slime mold habituation: behavior changed after earlier experience', 'Fits the behavioral definition of learning', 'Mimosa debated · pea did not replicate'], ('BEHAVIOR, PUBLISHED', SAGE)),
               ('Open', LAV, ['Do they think? Do they feel? Are they aware?', 'Scientists disagree', 'These experiments did not test it'], ('NOT ESTABLISHED', LAV)),
               cue('s11', 1), cue('s11', 6), area=((60, 215, 1860, 760) if not PORT else None))

# ---------------------------------------------------------------- s12 close, s13 end
def sc_close(cv, t, p):
    statements(cv, t, [(cue('s12', 0), 'This does not settle what a brain is.', CREAM, 'serif'), (cue('s12', 1), 'A simple kind of learning may not need one.', LAV, 'serif'),
                       (cue('s12', 3), 'Scientists still argue about what that means.', DIMC, 'serifr')], 250 if not PORT else 420)
    a = ease((t - cue('s12', 1)) / 0.8); x0 = W / 2 - 120; y = 800 if not PORT else 1150
    cv.rect((x0, y, x0 + 120, y + 6), mix(COR, BG, a)); cv.rect((x0 + 120, y, x0 + 240, y + 6), mix(TEA, BG, a))

SOURCES = ['Nakagaki, Yamada & Toth, Nature 407 (2000): maze · Tero et al., Science 327 (2010): Tokyo-area rail network',
           'Boisseau, Vogel & Dussutour, Proc. R. Soc. B (2016): habituation · Vogel & Dussutour, Proc. R. Soc. B (2016): transfer by fusion',
           "Saigusa et al., Physical Review Letters (2008): anticipation of periodic events (the authors' interpretation)",
           'Gagliano et al., Oecologia (2014): Mimosa (debated) · Gagliano et al., Scientific Reports (2016): pea · Markel, eLife (2020): failed replication',
           'Jennings, Behavior of the Lower Organisms (1902) · Dexter, Prabakaran & Gunawardena, Current Biology (2019): Stentor']

def sc_end(cv, t, p):
    a = ease(t / 1.0); cy = 80 if not PORT else 230
    cv.text((W / 2, cy), 'Heartbeat Observatory', 'serif', 96 if not PORT else 88, CREAM, 'ma', a)
    cv.rect((W / 2 - 100, cy + 125, W / 2, cy + 131), mix(COR, BG, a)); cv.rect((W / 2, cy + 125, W / 2 + 100, cy + 131), mix(TEA, BG, a))
    cv.text((W / 2, cy + 150), 'heartbeatobservatory.com', 'sansb', 52, COR, 'ma', a)
    cv.text((W / 2, cy + 225), 'Open Questions · Episode 2 · sources checked October 2026', 'sans', 34 if not PORT else 30, DIMC, 'ma', a)
    y = cy + 300; cv.text((W / 2, y), 'Sources', 'sansb', 32, DIMC, 'ma', ease((t - 0.6) / 1))
    yy = y + 50
    for i, s in enumerate(SOURCES):
        yy = cv.para(W / 2, yy, s, 'sans', 28 if not PORT else 27, CREAM, 1700 if not PORT else 980, 1.2, 'm', ease((t - 0.8 - i * 0.2) / 0.8)) + 8

SCENES = [
 ('s1', '', '', sc_title),
 ('s2', 'What "learning" means here', 'Definition used by the researchers whose work follows: learning by behavior only.', sc_def),
 ('s3', 'A maze, 2000', 'Source: Nakagaki, Yamada & Toth, Nature 407 (2000). Maze drawing is schematic.', sc_maze),
 ('s4', 'A rail map, 2010', 'Source: Tero et al., Science 327 (2010). Drawing is schematic, not the real map.', sc_tokyo),
 ('s5', 'Getting used to a bitter bridge', 'Source: Boisseau, Vogel & Dussutour, Proc. R. Soc. B (2016). Chart shape is schematic.', sc_habit),
 ('s6', 'Learning shared by fusing', 'Source: Vogel & Dussutour, Proc. R. Soc. B (2016). Drawing is schematic.', sc_fuse),
 ('s7', 'Anticipating, or just a rhythm?', 'Source: Saigusa et al., Physical Review Letters (2008). Plot is schematic.', sc_antic),
 ('s8', 'Plants: the sensitive plant', 'Source: Gagliano et al., Oecologia (2014). Result is debated. Drawing is schematic.', sc_mimosa),
 ('s9', 'Plants: the pea', 'Sources: Gagliano et al., Scientific Reports (2016); Markel, eLife (2020).', sc_pea),
 ('s10', 'A single cell: Stentor', 'Sources: Jennings (1902); Dexter, Prabakaran & Gunawardena, Current Biology (2019).', sc_stentor),
 ('s11', 'What this shows, and what it does not', '', sc_shows),
 ('s12', '', '', sc_close),
 ('s13', '', '', sc_end),
]
configure(SUBS, SCENES)
if __name__ == '__main__': main()
