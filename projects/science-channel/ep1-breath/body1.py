
# ================================================================ SCIENCE EP1 : breath back into air
import random
from model import run as model_run, HOURS, N0
MODEL = {m: model_run(m) for m in ('none', 'lioh', 'ko2')}
KCOL = (150, 120, 210); CCOL = (150, 165, 185); OCOL = RED; WATER = (90, 150, 230)

def sim_at(mode, h):
    a = MODEL[mode]; i = min(len(a) - 1, h / HOURS * (len(a) - 1)); i0 = int(i); i1 = min(len(a) - 1, i0 + 1); f = i - i0
    return tuple(a[i0][k] * (1 - f) + a[i1][k] * f for k in range(4))   # hours, co2%, o2%, used g

def rich(cv, x, y, parts, kind, size, anchor='m', a=1.0):
    f = font(kind, size); tot = sum(f.getlength(t) for t, c in parts) / SS
    xx = x - tot / 2 if anchor == 'm' else (x - tot if anchor == 'r' else x)
    for t, c in parts:
        cv.text((xx, y), t, kind, size, c, 'la', a); xx += f.getlength(t) / SS
    return tot

def mol(cv, kind, c, ang, r, a=1.0):
    """tiny gas molecule icon: 'co2' | 'o2' | 'h2o'"""
    ca, sa = math.cos(ang), math.sin(ang)
    if kind == 'co2':
        for s in (-1, 1): cv.circ((c[0] + s * 1.5 * r * ca, c[1] + s * 1.5 * r * sa), r * 0.95, mix(OCOL, BG2, a))
        cv.circ(c, r, mix(CCOL, BG2, a))
    elif kind == 'o2':
        for s in (-1, 1): cv.circ((c[0] + s * 0.9 * r * ca, c[1] + s * 0.9 * r * sa), r * 0.95, mix(TEAL, BG2, a))
    else:
        cv.circ(c, r * 1.05, mix(WATER, BG2, a))

class P:  # a wandering gas particle, deterministic in time
    def __init__(s, seed):
        r = random.Random(seed); s.f = [r.uniform(0.15, 0.55) for _ in range(4)]; s.p = [r.uniform(0, 6.28) for _ in range(4)]; s.ang = r.uniform(0, 6.28); s.sp = r.uniform(-0.8, 0.8)
    def at(s, t, box):
        u = 0.5 + 0.5 * math.sin(s.f[0] * t + s.p[0]) * math.cos(s.f[2] * t * 0.7 + s.p[2]); v = 0.5 + 0.5 * math.sin(s.f[1] * t + s.p[1]) * math.cos(s.f[3] * t * 0.6 + s.p[3])
        return (box[0] + u * (box[2] - box[0]), box[1] + v * (box[3] - box[1])), s.ang + s.sp * t
CO2P = [P(100 + i) for i in range(80)]; O2P = [P(500 + i) for i in range(80)]

def geo():
    if PORT:
        return dict(pod=(50, 350, 780, 700), can=(800, 360, 1030, 690), gauge=(50, 725, 1030, 1245), ytop=410, ybot=640, bed=(450, 600))
    return dict(pod=(80, 215, 830, 805), can=(850, 255, 1030, 765), gauge=(1080, 205, 1850, 825), ytop=290, ybot=730, bed=(330, 690))

def person(cv, pod, t):
    x = pod[0] + 150; y = pod[3] - 30; k = 1 + 0.025 * math.sin(t * 2 * math.pi / 4.0)
    cv.rect((x - 60, y - 130 * k, x + 60, y), mix(STEEL, BG2, 0.7), 28)
    cv.rect((x - 78, y - 50, x + 78, y - 8), mix(STEEL, BG2, 0.55), 12)
    cv.circ((x, y - 168 * k), 36, mix(STEEL, BG2, 0.85))
    cv.circ((x + 12, y - 172 * k), 4, BG2)

def bar(cv, x, y, w, label, val, col, v, lo, hi, ticks, marks):
    cv.text((x, y), label, 'sansb', 34, TXT); cv.text((x + w, y - 14), val, 'serif', 70 if not PORT else 62, col, 'ra')
    by = y + (84 if not PORT else 66); bh = 40 if not PORT else 34
    cv.rect((x, by, x + w, by + bh), mix(STEEL, BG, 0.3), 8)
    fw = w * clamp01((v - lo) / (hi - lo)); cv.rect((x, by, x + max(fw, 4), by + bh), col, 8)
    for tk in ticks:
        xx = x + w * (tk - lo) / (hi - lo); cv.text((xx, by + bh + 4), str(tk), 'sans', 24, DIM, 'ma' if lo < tk < hi else ('la' if tk == lo else 'ra'))
    for mv, lab, mc, side in marks:
        xx = x + w * (mv - lo) / (hi - lo); cv.line([(xx, by - 8), (xx, by + bh + 8)], mc, 4)
        cv.text((xx + (8 if side == 'l' else -8), by + bh + (34 if not PORT else 30)), lab, 'sans', 25, mc, 'la' if side == 'l' else 'ra')

def sim_scene(cv, t, p, mode, sid):
    g = geo(); pod = g['pod']; can = g['can']; seg = SEG[sid]
    hrs = HOURS * clamp01((t - 0.9) / max(1.0, seg['dur'] - 2.2)); h, co2, o2, used = sim_at(mode, hrs)
    cv.rect(pod, BG2, 26); cv.outline(pod, STEEL, 4, 26)
    cv.text((pod[0] + 24, pod[1] + 14), 'SEALED POD  ·  3 m³  ·  1 PERSON', 'sansb', 26, DIM)
    cv.rect((pod[2] - 214, pod[1] + 12, pod[2] - 18, pod[1] + 54), mix(AMBER, BG2, 0.22), 20)
    cv.text(((pod[2] - 214 + pod[2] - 18) / 2, pod[1] + 33), 'SIMULATION', 'sansb', 26, AMBER, 'mm')
    person(cv, pod, t)
    inner = (pod[0] + 26, pod[1] + 70, pod[2] - 26, pod[3] - 70)
    nco = co2 / 100 * N0 / 0.1; no = o2 / 100 * N0 / 0.5
    for k, pa in enumerate(O2P):
        a = clamp01(no - k)
        if a > 0:
            c, ang = pa.at(t, inner); mol(cv, 'o2', c, ang, 8, a)
    for k, pa in enumerate(CO2P):
        a = clamp01(nco - k)
        if a > 0:
            c, ang = pa.at(t, inner); mol(cv, 'co2', c, ang, 7, a)
    # legend
    ly = pod[3] - 30; lx = pod[2] - 330
    cv.rect((lx - 12, ly - 22, pod[2] - 14, ly + 20), BG2)
    mol(cv, 'co2', (lx + 22, ly), 0, 7); cv.text((lx + 56, ly), 'CO₂', 'sansb', 26, TXT, 'lm'); mol(cv, 'o2', (lx + 150, ly), 0, 8); cv.text((lx + 178, ly), 'O₂', 'sansb', 26, TXT, 'lm')
    cv.text((lx + 236, ly), '(not to scale)', 'sans', 20, DIM, 'lm') if False else None
    # scrubber
    cxm = (can[0] + can[2]) / 2; ytop, ybot = g['ytop'], g['ybot']; b0, b1 = g['bed']
    if mode == 'none':
        cv.outline(can, mix(STEEL, BG, 0.5), 3, 16)
        cv.text((cxm, (can[1] + can[3]) / 2 - 20), 'no', 'sansb', 36, DIM, 'mm'); cv.text((cxm, (can[1] + can[3]) / 2 + 22), 'scrubber', 'sansb', 36, DIM, 'mm')
    else:
        name = 'LiOH' if mode == 'lioh' else 'KO₂'; cap = 400.0 if mode == 'lioh' else 600.0
        fresh = (200, 212, 228) if mode == 'lioh' else (232, 176, 60); spent = (122, 138, 160) if mode == 'lioh' else (232, 236, 244)
        pipe = mix(STEEL, BG, 0.6)
        cv.line([(pod[2] - 40, ytop), (cxm, ytop)], pipe, 12); cv.line([(cxm, ybot), (pod[2] - 40, ybot)], pipe, 12)
        cv.rect(can, mix(STEEL, BG, 0.25), 16); cv.outline(can, STEEL, 3, 16)
        bx = (can[0] + 24, b0, can[2] - 24, b1); cv.rect(bx, mix(fresh, BG, 0.9), 8)
        fr = clamp01(used / cap); yy = b0 + (b1 - b0) * fr
        if fr > 0.005: cv.rect((bx[0], b0, bx[2], yy), spent, 8)
        cv.outline(bx, TXT, 2, 8)
        cv.text((cxm, can[3] + 22), f'{name} canister', 'sansb', 30, TXT, 'ma')
        pts = [(pod[2] - 40, ytop), (cxm, ytop), (cxm, b0), (cxm, b1), (cxm, ybot), (pod[2] - 40, ybot)]
        seglen = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]; tot = sum(seglen); ub = (seglen[0] + seglen[1] + (b1 - b0) / 2) / tot
        def pos(u):
            d = u * tot
            for i, l in enumerate(seglen):
                if d <= l: return (pts[i][0] + (pts[i + 1][0] - pts[i][0]) * d / l, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * d / l)
                d -= l
            return pts[-1]
        pc = max(0.2, min(0.85, co2 / 0.5)); CYC = 5.5; N = 12
        for j in range(N):
            tt = t + j * CYC / N; cyc = int(tt // CYC); u = (tt % CYC) / CYC
            hsh = random.Random(j * 977 + cyc * 31).random(); isco = hsh < pc
            al = min(1.0, u / 0.06, (1 - u) / 0.06)
            kind = 'co2' if isco else 'o2'
            if u > ub and isco: kind = 'o2' if mode == 'ko2' else 'h2o'
            if isco and abs(u - ub) < 0.02:
                cv.circ(pos(ub), 14 * (1 - abs(u - ub) / 0.02) + 4, mix(AMBER if mode == 'ko2' else WATER, BG2, 0.5))
            mol(cv, kind, pos(u), 0.5, 7.5, al)
    # gauges
    gx0, gy0, gx1, gy1 = g['gauge']; w = gx1 - gx0
    hh = int(hrs); mm = int((hrs - hh) * 60)
    cv.text((gx0, gy0), 'Elapsed', 'sansb', 30, DIM); cv.text((gx0 + 150, gy0 - 16), f'{hh}:{mm:02d}', 'serif', 66, TXT); cv.text((gx0 + 150 + 170, gy0 + 6), 'hours : minutes', 'sans', 28, DIM)
    cv.rect((gx0, gy0 + 66, gx1, gy0 + 72), mix(STEEL, BG, 0.4)); cv.rect((gx0, gy0 + 66, gx0 + w * hrs / HOURS, gy0 + 72), AMBER)
    gy = gy0 + (100 if not PORT else 84); GAP = 205 if not PORT else 160
    ccol = TEAL if co2 < 0.5 else (AMBER if co2 < 4.0 else RED)
    bar(cv, gx0, gy, w, 'Carbon dioxide', f'{co2:.2f}%', ccol, co2, 0, 5, [0, 1, 2, 3, 4, 5], [(0.5, '0.5% work limit', AMBER, 'l'), (4.0, '4% dangerous to life', RED, 'r')])
    ocol = TEAL if o2 >= 19.5 else AMBER
    bar(cv, gx0, gy + GAP, w, 'Oxygen', f'{o2:.1f}%', ocol, o2, 14, 22, [14, 16, 18, 20, 22], [(19.5, 'below 19.5% = oxygen-deficient', AMBER, 'r')])
    ey = gy + GAP * 2 - (0 if not PORT else 4) - (0 if not PORT else 0)
    if mode == 'lioh': rich(cv, gx0 + w / 2, ey, [('2 LiOH + CO₂ → Li₂CO₃ + H₂O', TXT)], 'sansb', 36 if not PORT else 40, 'm')
    if mode == 'ko2': rich(cv, gx0 + w / 2, ey, [('4 KO₂ + 2 CO₂ → 2 K₂CO₃ + 3 O₂', TXT)], 'sansb', 36 if not PORT else 40, 'm')
    if mode == 'ko2': cv.text((gx0 + w / 2, ey + 52), f'KO₂ used so far: {used / 1000:.2f} kg', 'sans', 28, DIM, 'ma')
    if mode == 'lioh': cv.text((gx0 + w / 2, ey + 52), f'LiOH used so far: {used / 1000:.2f} kg   ·   no oxygen made', 'sans', 28, DIM, 'ma')
