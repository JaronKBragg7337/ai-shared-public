import sys; sys.path.insert(0, '..')
from oqlib import *
import tvlib, random

SCR = json.load(open('script.json'))
SUBS = {s['id']: s['disp'] for s in SCR}
def F(sid, f):
    return tvlib.SEG[sid]['start'] + f * tvlib.SEG[sid]['dur'] - tvlib.BOUND[sid][0]

def sc_title(cv, t, p):
    a = ease(t / 1.0); ty = 150 if PORT else 70
    cv.text((W / 2, ty), 'HEARTBEAT TV  ·  OPEN QUESTIONS  ·  EPISODE 4', 'sansb', 30 if PORT else 34, DIMC, 'ma', a)
    if PORT: lines, sz = ("What if gravity", "isn't the", 'full story?'), 100
    else: lines, sz = ("What if gravity", "isn't the full story?"), 124
    for k, l in enumerate(lines):
        cv.text((W / 2, ty + 90 + k * sz * 1.15), l, 'serif', sz, CREAM, 'ma', ease((t - 0.2) / 1.0), 5)
    c = F('s1', 0.40); a2 = ease((t - c) / 0.8)
    if PORT:
        y = 760
        pill(cv, W / 2, y, 'UNSEEN MASS: DARK MATTER?', COR, a2, 34)
        cv.text((W / 2, y + 62), 'or', 'serifr', 44, DIMC, 'ma', a2)
        pill(cv, W / 2, y + 160, 'GRAVITY ITSELF DIFFERENT?', TEA, a2, 34); y += 160
    else:
        y = 560
        pill(cv, W * 0.27, y, 'UNSEEN MASS: DARK MATTER?', COR, a2, 36)
        pill(cv, W * 0.73, y, 'GRAVITY ITSELF DIFFERENT?', TEA, a2, 36)
        cv.text((W / 2, y - 24), 'or', 'serifr', 44, DIMC, 'ma', a2)
    a3 = ease((t - F('s1', 0.85)) / 0.8)
    if a3 > 0: cv.text((W / 2, y + 90), 'Published papers and preprints. Sources on screen.', 'sans', 32, DIMC, 'ma', a3)

def sc_curve(cv, t, p):
    if PORT: gb = (30, 370, 1050, 860); c1 = (30, 900, 1050, 1060); c2 = (30, 1080, 1050, 1240)
    else: gb = (60, 225, 1000, 780); c1 = (1050, 225, 1860, 480); c2 = (1050, 510, 1860, 780)
    a = ease(t / 0.7); card(cv, gb, a, COR)
    cv.text((gb[0] + 30, gb[1] + 16), 'Orbital speed vs distance from center (schematic)', 'sansb', 26, COR, 'la', a)
    x0, x1, y0, y1 = gb[0] + 90, gb[2] - 40, gb[1] + 80, gb[3] - 80
    cv.rect((x0, y1, x1, y1 + 4), mix(DIMC, BG, a)); cv.rect((x0 - 4, y0, x0, y1), mix(DIMC, BG, a))
    cv.text((x1, y1 + 14), 'distance from galactic center', 'sans', 24, DIMC, 'ra', a)
    cv.text((x0 + 12, y0 - 6), 'speed', 'sans', 24, DIMC, 'la', a)
    def pred(u): return (u * 8) / (1 + (u * 8) ** 2) ** 0.75
    N = 120
    mx = max(pred(k / N) for k in range(N + 1))
    tp = clamp01((t - F('s2', 0.30)) / 3.0); n = int(N * tp) + 1
    pts = [(x0 + (x1 - x0) * k / N, y1 - (y1 - y0 - 30) * (pred(k / N) / mx) * 0.70) for k in range(n)]
    if len(pts) > 1: cv.line(pts, mix(TEA, BG, a), 7)
    ao = ease((t - F('s2', 0.62)) / 0.6)
    if ao > 0:
        to = clamp01((t - F('s2', 0.62)) / 3.0); n2 = int(N * to) + 1
        pts2 = [(x0 + (x1 - x0) * k / N, y1 - (y1 - y0 - 30) * (1 - math.exp(-k / N * 9.0)) * 0.82) for k in range(n2)]
        if len(pts2) > 1: cv.line(pts2, mix(COR, BG, ao), 7)
    cv.text((x1 - 10, y1 - (y1 - y0) * 0.12), 'expected from visible matter', 'sansb', 26, TEA, 'ra', ease((t - F('s2', 0.35)) / 0.6))
    cv.text((x1 - 10, y0 + 6), 'observed: roughly flat', 'sansb', 26, COR, 'ra', ao)
    a1 = ease((t - F('s2', 0.12)) / 0.7)
    if a1 > 0:
        card(cv, c1, a1, LAV); cv.text((c1[0] + 28, c1[1] + 16), 'Zwicky (1933)', 'serif', 44, LAV, 'la', a1)
        cv.para(c1[0] + 28, c1[1] + 74, 'Coma Cluster galaxies move faster than visible mass explains', 'sans', 32, CREAM, c1[2] - c1[0] - 56, 1.15, 'l', a1)
    a2 = ease((t - F('s2', 0.50)) / 0.7)
    if a2 > 0:
        card(cv, c2, a2, COR); cv.text((c2[0] + 28, c2[1] + 16), 'Rubin, Ford, Thonnard', 'serif', 44, COR, 'la', a2)
        cv.para(c2[0] + 28, c2[1] + 74, 'Andromeda, then many spirals: outer speeds often roughly flat', 'sans', 32, CREAM, c2[2] - c2[0] - 56, 1.15, 'l', a2)

def sc_dm(cv, t, p):
    if PORT: gb = (30, 370, 1050, 840); cd = (30, 880, 1050, 1200); py = 1230
    else: gb = (60, 225, 900, 780); cd = (960, 225, 1860, 600); py = 690
    a = ease(t / 0.7); card(cv, gb, a, COR)
    cx, cy = (gb[0] + gb[2]) / 2, (gb[1] + gb[3]) / 2 + 20
    ah = ease((t - F('s3', 0.12)) / 1.2)
    R = min(gb[2] - gb[0], gb[3] - gb[1]) * 0.44
    if ah > 0:
        cv.circ((cx, cy), R * ah, mix(COR, BG, 0.22 * ah))
        cv.text((cx, cy - R * ah + 14), 'invisible halo (dark matter)', 'sansb', 26, COR, 'ma', ah)
    for k in range(40):
        ang = k * 2.4; r = 20 + (k % 20) * 7.5 * (R / 190) * 0.55
        cv.circ((cx + math.cos(ang) * r, cy + math.sin(ang) * r * 0.45), 4, mix(CREAM, BG, a))
    cv.text((gb[0] + 24, gb[1] + 14), 'schematic', 'sans', 24, DIMC, 'la', a)
    a2 = ease((t - F('s3', 0.45)) / 0.7)
    if a2 > 0:
        card(cv, cd, a2, LAV); cv.text((cd[0] + 30, cd[1] + 18), 'Not one observation', 'serif', 44, LAV, 'la', a2)
        cv.para(cd[0] + 30, cd[1] + 84, 'Part of the standard model (Lambda-CDM), which must fit many observations at once', 'sans', 36, CREAM, cd[2] - cd[0] - 60, 1.15, 'l', a2)
    a3 = ease((t - F('s3', 0.78)) / 0.7)
    if a3 > 0: pill(cv, (cd[0] + cd[2]) / 2 if not PORT else W / 2, py, 'No particle confirmed yet', ROSE, a3, 34)

def sc_mond(cv, t, p):
    area = (60, 215, 1860, 690) if not PORT else (30, 350, 1050, 1100)
    side_cards(cv, t, ('Newtonian gravity', DIMC, ['Pull weakens with distance', 'Visible mass alone leaves outer speeds too high'], ('STANDARD', DIMC)),
               ('MOND (Milgrom, 1983)', TEA, ['Below a tiny acceleration, effective gravity is stronger', 'One constant, visible matter only'], ('MODIFIED DYNAMICS / GRAVITY', TEA)),
               F('s4', 0.12), F('s4', 0.30), area=area, size=36 if PORT else 38)
    a = ease((t - F('s4', 0.62)) / 0.7)
    if a > 0: pill(cv, W / 2, 770 if not PORT else 1160, 'McGaugh et al. 2016: tight acceleration relation', LAV, a, 32)
    a = ease((t - F('s4', 0.85)) / 0.7)
    if a > 0: pill(cv, W / 2, 850 if not PORT else 1250, 'Both sides explain it: which does better is debated', ROSE, a, 30)

def sc_succ(cv, t, p):
    items = [dict(year='1983', who='MOND', what='Milgrom: a rule for weak accelerations', at=F('s5', 0.10), col=TEA),
             dict(year='2004', who='Bekenstein', what='A relativistic version of MOND', at=F('s5', 0.38), col=TEA),
             dict(year='2021', who='Skordis & Zlosnik', what='A newer relativistic theory', at=F('s5', 0.55), col=TEA)]
    rail(cv, t, items, area=(60, 215, 1860, 830) if not PORT else (30, 360, 1050, 1150))
    a = ease((t - F('s5', 0.80)) / 0.7)
    if a > 0: badge(cv, W / 2 - 400, 740 if not PORT else 1170, 'CLUSTER DISCREPANCY REMAINS', ROSE, a, 30)

def sc_bullet(cv, t, p):
    if PORT: dg = (30, 370, 1050, 800); c1 = (30, 840, 1050, 1060); c2 = (30, 1080, 1050, 1250)
    else: dg = (60, 225, 1000, 780); c1 = (1050, 225, 1860, 500); c2 = (1050, 530, 1860, 780)
    a = ease(t / 0.7); card(cv, dg, a, ROSE)
    cv.text((dg[0] + 30, dg[1] + 16), 'Two clusters after colliding (schematic)', 'sansb', 26, ROSE, 'la', a)
    cy = (dg[1] + dg[3]) / 2 + 30; cx = (dg[0] + dg[2]) / 2; d = (dg[2] - dg[0]) * 0.30
    tg = ease((t - F('s6', 0.15)) / 1.0)
    if tg > 0:
        for s in (-1, 1): cv.circ((cx + s * d * 0.35, cy), 70, mix(ROSE, BG, 0.45 * tg))
        cv.text((cx, cy + 100), 'hot gas (X-rays), slowed in the collision', 'sans', 26, ROSE, 'ma', tg)
    tm = ease((t - F('s6', 0.50)) / 1.0)
    if tm > 0:
        for s in (-1, 1):
            cv.circ((cx + s * d, cy), 78, mix(LAV, BG, 0.28 * tm))
            cv.ring((cx + s * d, cy), 78, mix(LAV, BG, tm), 4)
            for k in range(6): cv.circ((cx + s * d + math.cos(k * 1.1) * 38, cy + math.sin(k * 1.9) * 30), 5, mix(CREAM, BG, tm))
        cv.text((cx, cy - 120), 'most of the mass (lensing) is near the galaxies', 'sansb', 26, LAV, 'ma', tm)
    a1 = ease((t - F('s6', 0.58)) / 0.7)
    if a1 > 0:
        card(cv, c1, a1, LAV); cv.text((c1[0] + 28, c1[1] + 16), 'Clowe et al. (2006)', 'serif', 44, LAV, 'la', a1)
        cv.para(c1[0] + 28, c1[1] + 74, 'Lensing mass sits apart from the gas: evidence for mass that does not follow the gas', 'sans', 32, CREAM, c1[2] - c1[0] - 56, 1.15, 'l', a1)
    a2 = ease((t - F('s6', 0.84)) / 0.7)
    if a2 > 0:
        card(cv, c2, a2, TEA); cv.text((c2[0] + 28, c2[1] + 16), 'MOND side', 'serif', 44, TEA, 'la', a2)
        cv.para(c2[0] + 28, c2[1] + 74, 'MOND models add some unseen matter in clusters: what that implies is debated', 'sans', 32, CREAM, c2[2] - c2[0] - 56, 1.15, 'l', a2)

def sc_cmb(cv, t, p):
    if PORT: eb = (30, 380, 1050, 820); cd = (30, 860, 1050, 1200)
    else: eb = (60, 225, 900, 760); cd = (960, 225, 1860, 700)
    a = ease(t / 0.7); card(cv, eb, a, TEA)
    cx, cy = (eb[0] + eb[2]) / 2, (eb[1] + eb[3]) / 2 + 10
    rx, ry = (eb[2] - eb[0]) * 0.42, (eb[3] - eb[1]) * 0.40
    rnd = random.Random(7); tn = ease((t - F('s7', 0.10)) / 1.5)
    for k in range(260):
        ang = rnd.random() * 6.283; rr = (rnd.random() ** 0.5) * min(rx, ry) * 0.95
        col = rnd.choice([COR, TEA, LAV, CREAM, ROSE])
        cv.circ((cx + math.cos(ang) * rr * 1.3, cy + math.sin(ang) * rr), 8 + rnd.random() * 14, mix(col, BG, 0.5 * tn))
    cv.text((eb[0] + 24, eb[1] + 14), 'cosmic microwave background (schematic)', 'sans', 24, DIMC, 'la', a)
    a2 = ease((t - F('s7', 0.30)) / 0.7)
    if a2 > 0:
        card(cv, cd, a2, SAGE); cv.text((cd[0] + 30, cd[1] + 18), 'Planck team (2018)', 'serif', 46, SAGE, 'la', a2)
        cv.para(cd[0] + 30, cd[1] + 84, 'Standard cosmology with dark matter fits the pattern very precisely: about 5x more dark matter than ordinary matter', 'sans', 34, CREAM, cd[2] - cd[0] - 60, 1.15, 'l', a2)
    by = cd[3] - 130 if not PORT else cd[3] - 110
    a3 = ease((t - F('s7', 0.62)) / 0.7)
    if a3 > 0: badge(cv, cd[0] + 30, by, 'GRAVITY-ONLY IDEAS: HARDER TO MATCH (OPEN)', ROSE, a3, 26)
    a4 = ease((t - F('s7', 0.86)) / 0.7)
    if a4 > 0: badge(cv, cd[0] + 30, by + 60, 'DARK ENERGY: SEPARATE, NOT COVERED', DIMC, a4, 26)

def sc_wide(cv, t, p):
    if PORT: dg = (30, 370, 1050, 840); cd = (30, 880, 1050, 1200)
    else: dg = (60, 225, 1000, 780); cd = (1050, 225, 1860, 600)
    a = ease(t / 0.7); card(cv, dg, a, LAV)
    cx, cy = (dg[0] + dg[2]) / 2, (dg[1] + dg[3]) / 2 + 20
    sep = (dg[2] - dg[0]) * 0.34; ang = t * 0.5
    for k in range(80):
        th = k / 80 * 6.283
        cv.circ((cx + math.cos(th) * sep / 2, cy + math.sin(th) * sep / 2 * 0.6), 2, mix(DIMC, BG, 0.5 * a))
    for s, col, r in ((-1, COR, 22), (1, TEA, 16)):
        cv.circ((cx + s * sep / 2 * math.cos(ang), cy + s * sep / 2 * math.sin(ang) * 0.6), r, mix(col, BG, a))
    cv.text((cx, dg[3] - 50), 'pair thousands of times farther apart than Earth and Sun', 'sans', 26, DIMC, 'ma', ease((t - F('s8', 0.3)) / 0.7))
    cv.text((dg[0] + 24, dg[1] + 14), 'schematic', 'sans', 24, DIMC, 'la', a)
    a2 = ease((t - F('s8', 0.45)) / 0.7)
    if a2 > 0:
        card(cv, cd, a2, LAV); cv.text((cd[0] + 30, cd[1] + 18), 'The prediction', 'serif', 46, LAV, 'la', a2)
        cv.para(cd[0] + 30, cd[1] + 84, 'Weak pull: at the widest separations MOND predicts faster orbits than Newtonian gravity, by a model-dependent amount. Data: Gaia telescope.', 'sans', 34, CREAM, cd[2] - cd[0] - 60, 1.15, 'l', a2)

def sc_dispute(cv, t, p):
    area = (60, 215, 1860, 690) if not PORT else (30, 350, 1050, 1060)
    side_cards(cv, t, ('Chae (2023)', COR, ['Apparent speed excess in Gaia pairs', 'Consistent with MOND'], ('ApJ', COR)),
               ('Banik et al. (2024)', TEA, ['Also Gaia pairs: no such effect', 'Favors Newtonian gravity'], ('MNRAS', TEA)),
               F('s9', 0.12), F('s9', 0.30), area=area, size=38 if not PORT else 36)
    a = ease((t - F('s9', 0.55)) / 0.7)
    if a > 0: cv.para(W / 2, 730 if not PORT else 1090, 'Differences: pair selection  ·  hidden third stars  ·  orbit modeling', 'sansb', 34, CREAM, 1500 if not PORT else 960, 1.15, 'm', a)
    a = ease((t - F('s9', 0.88)) / 0.7)
    if a > 0: badge(cv, W / 2 - 260, 830 if not PORT else 1200, 'CONTESTED · NOT ESTABLISHED', ROSE, a, 32)

def sc_settle(cv, t, p):
    rows = [(F('s10', 0.08), 'Detect a dark matter particle (or keep narrowing the options)'), (F('s10', 0.42), 'Gaia data release 4, planned December 2026: cleaner wide-binary samples'),
            (F('s10', 0.65), 'Radial-velocity checks on individual pairs for hidden companions'), (F('s10', 0.85), 'More cluster collisions like the Bullet Cluster')]
    y = 250 if not PORT else 420; step = 135 if not PORT else 190
    for i, (tc, txt) in enumerate(rows):
        a = ease((t - tc) / 0.7)
        if a <= 0: continue
        x = 140 if not PORT else 60
        checkbox(cv, x, y + i * step, 56, a)
        cv.para(x + 100, y + i * step - 6, txt, 'serif', 46 if not PORT else 42, CREAM, W - x - 220, 1.15, 'l', a)

def sc_shows(cv, t, p):
    side_cards(cv, t, ('Established', SAGE, ['Visible matter alone cannot explain these motions under standard gravity', 'The dark matter model fits many observations, including the CMB and cluster collisions', 'A MOND-style rule matches many galaxy rotation curves'], ('PUBLISHED EVIDENCE', SAGE)),
               ('Not established', LAV, ['What is dark matter?', 'Can any modified gravity fit galaxies, clusters and the CMB together?', 'Do wide binaries depart from Newtonian gravity?'], ('OPEN', LAV)),
               F('s11', 0.12), F('s11', 0.50), area=(60, 215, 1860, 800) if not PORT else (30, 350, 1050, 1240), size=32 if PORT else 36)

def sc_close(cv, t, p):
    statements(cv, t, [(F('s12', 0.0), 'This does not settle what gravity does, or what the universe contains.', CREAM, 'serif'), (F('s12', 0.30), 'The mismatch is real. The answer could be new matter, new gravity, or something not yet proposed.', LAV, 'serif'),
                       (F('s12', 0.70), 'Scientists still disagree.', DIMC, 'serifr')], 230 if not PORT else 290)
    a = ease((t - F('s12', 0.30)) / 0.8); x0 = W / 2 - 120; y = 900 if not PORT else 1180
    cv.rect((x0, y, x0 + 120, y + 6), mix(COR, BG, a)); cv.rect((x0 + 120, y, x0 + 240, y + 6), mix(TEA, BG, a))

SOURCES = ['Zwicky, Helvetica Physica Acta (1933): Coma Cluster · Ford & Rubin, ApJ (1970); Rubin, Ford & Thonnard, ApJ (1980): rotation curves',
           'Milgrom, ApJ (1983): MOND · McGaugh, Lelli & Schombert, PRL (2016): radial acceleration relation',
           'Bekenstein, PRD (2004): relativistic MOND · Skordis & Zlosnik, PRL (2021): relativistic MOND theory',
           'Clowe et al., ApJ Letters (2006): Bullet Cluster · Planck Collaboration, A&A (2020): 2018 cosmological parameters',
           'LUX-ZEPLIN Collaboration, PRL: dark matter search results · Gaia Collaboration, data release 3',
           'Chae, ApJ (2023) · Banik et al., MNRAS (2024) · Saad & Ting, OJAp (2026); Chae & Yoon, arXiv:2607.14450 (2026): wide binaries']

def sc_end(cv, t, p):
    a = ease(t / 1.0); cy = 80 if not PORT else 230
    cv.text((W / 2, cy), 'Heartbeat Observatory', 'serif', 96 if not PORT else 88, CREAM, 'ma', a)
    cv.rect((W / 2 - 100, cy + 125, W / 2, cy + 131), mix(COR, BG, a)); cv.rect((W / 2, cy + 125, W / 2 + 100, cy + 131), mix(TEA, BG, a))
    cv.text((W / 2, cy + 150), 'heartbeatobservatory.com', 'sansb', 52, COR, 'ma', a)
    cv.text((W / 2, cy + 225), 'Open Questions · Episode 4 · sources checked October 2026', 'sans', 34 if not PORT else 30, DIMC, 'ma', a)
    y = cy + 300; cv.text((W / 2, y), 'Sources', 'sansb', 32, DIMC, 'ma', ease((t - 0.6) / 1))
    yy = y + 50
    for i, s in enumerate(SOURCES):
        yy = cv.para(W / 2, yy, s, 'sans', 28 if not PORT else 27, CREAM, 1700 if not PORT else 980, 1.2, 'm', ease((t - 0.8 - i * 0.2) / 0.8)) + 8

SCENES = [
 ('s1', '', '', sc_title),
 ('s2', 'The mismatch', 'Sources: Zwicky (1933); Ford & Rubin, ApJ (1970); Rubin, Ford & Thonnard, ApJ (1980). Curves are schematic.', sc_curve),
 ('s3', 'Explanation 1: dark matter', 'Drawing is schematic. Dark matter has not been directly detected.', sc_dm),
 ('s4', 'Explanation 2: modified gravity', 'Sources: Milgrom, ApJ (1983); McGaugh, Lelli & Schombert, PRL (2016).', sc_mond),
 ('s5', 'MOND and its successors', 'Sources: Milgrom (1983); Bekenstein (2004); Skordis & Zlosnik, PRL (2021).', sc_succ),
 ('s6', 'The Bullet Cluster', 'Source: Clowe et al., ApJ Letters (2006). Drawing is schematic.', sc_bullet),
 ('s7', 'The cosmic microwave background', 'Source: Planck Collaboration (2018 results). Drawing is schematic.', sc_cmb),
 ('s8', 'A newer test: wide binaries', 'Drawing is schematic. Data: Gaia space telescope.', sc_wide),
 ('s9', 'A live dispute', 'Sources: Chae, ApJ (2023); Banik et al., MNRAS (2024); Saad & Ting, OJAp (2026); Chae & Yoon, arXiv (2026).', sc_dispute),
 ('s10', 'What would settle it', '', sc_settle),
 ('s11', 'What this shows, and what it does not', '', sc_shows),
 ('s12', '', '', sc_close),
 ('s13', '', '', sc_end),
]
configure(SUBS, SCENES)
if __name__ == '__main__': main()
