import sys; sys.path.insert(0, '..')
from oqlib import *
import tvlib

SCR = json.load(open('script.json'))
SUBS = {s['id']: s['disp'] for s in SCR}
def F(sid, f):
    """time (scene-relative) at fraction f of the narration of segment sid"""
    return tvlib.SEG[sid]['start'] + f * tvlib.SEG[sid]['dur'] - tvlib.BOUND[sid][0]

# ---------------------------------------------------------------- s1 title
def sc_title(cv, t, p):
    a = ease(t / 1.0); ty = 150 if PORT else 70
    cv.text((W / 2, ty), 'HEARTBEAT TV  ·  OPEN QUESTIONS  ·  EPISODE 3', 'sansb', 30 if PORT else 34, DIMC, 'ma', a)
    if PORT: lines, sz = ("Did humanity's", 'birthplace have', 'something special?'), 96
    else: lines, sz = ("Did humanity's birthplace", 'have something special?'), 124
    for k, l in enumerate(lines):
        cv.text((W / 2, ty + 90 + k * sz * 1.15), l, 'serif', sz, CREAM, 'ma', ease((t - 0.2) / 1.0), 5)
    c = F('s1', 0.55); a2 = ease((t - c) / 0.8)
    if PORT:
        y = 760
        pill(cv, W / 2, y, 'SOMETHING SPECIAL ABOUT AFRICA?', COR, a2, 34)
        cv.text((W / 2, y + 62), 'or', 'serifr', 44, DIMC, 'ma', a2)
        pill(cv, W / 2, y + 160, 'WHERE THE BONES SURVIVED?', TEA, a2, 34); y += 160
    else:
        y = 560
        pill(cv, W * 0.27, y, 'SOMETHING SPECIAL ABOUT AFRICA?', COR, a2, 36)
        pill(cv, W * 0.73, y, 'WHERE THE BONES SURVIVED?', TEA, a2, 36)
        cv.text((W / 2, y - 24), 'or', 'serifr', 44, DIMC, 'ma', a2)
    a3 = ease((t - F('s1', 0.85)) / 0.8)
    if a3 > 0: cv.text((W / 2, y + 90), 'Published studies only. Sources on screen.', 'sans', 32, DIMC, 'ma', a3)

# ---------------------------------------------------------------- s2 fossils rail
def sc_fossils(cv, t, p):
    items = [dict(year='3.7M', who='Laetoli, Tanzania', what='Footprints in volcanic ash', at=F('s2', 0.10), col=COR),
             dict(year='1.8M', who='Olduvai Gorge, Tanzania', what='Skull found 1959; layer dated by ash', at=F('s2', 0.40), col=COR),
             dict(year='~300K', who='Jebel Irhoud, Morocco', what='Early stage of our species', at=F('s2', 0.62), col=TEA),
             dict(year='230K+', who='Omo Kibish, Ethiopia', what='Early Homo sapiens', at=F('s2', 0.82), col=TEA)]
    rail(cv, t, items, area=(60, 215, 1860, 830) if not PORT else (30, 360, 1050, 1170))
    cv.text((W / 2, 790 if not PORT else 1196), 'years ago, approximate  ·  M = million, K = thousand', 'sans', 26, DIMC, 'ma', ease((t - 1) / 1))

# ---------------------------------------------------------------- s3 genetics
def sc_genes(cv, t, p):
    if PORT: bx = (30, 370, 1050, 760); cb = (30, 800, 1050, 1070); py = (1130, 1200)
    else: bx = (60, 225, 930, 760); cb = (990, 225, 1860, 560); py = (630, 710)
    a = ease((t - F('s3', 0.10)) / 0.7); card(cv, bx, a, COR)
    cv.text((bx[0] + 30, bx[1] + 18), 'Genetic variation (schematic)', 'sansb', 30, COR, 'la', a)
    iw = bx[2] - bx[0] - 60; ih = bx[3] - bx[1] - 190
    r1 = (bx[0] + 30, bx[1] + 80, bx[0] + 30 + iw, bx[1] + 80 + ih)
    cv.rect(r1, mix(COR, BG, 0.35 * a), 14)
    cv.text((r1[0] + 20, r1[1] + 14), 'Variation among people in Africa', 'sansb', 34, CREAM, 'la', a)
    a2 = ease((t - F('s3', 0.20)) / 0.7)
    r2 = (r1[0] + iw * 0.12, r1[1] + ih * 0.42, r1[0] + iw * 0.12 + iw * 0.42, r1[3] - 20)
    if a2 > 0:
        cv.rect(r2, mix(TEA, BG, 0.75 * a2), 12)
        cv.para((r2[0] + r2[2]) / 2, r2[1] + 12, 'Elsewhere: largely a subset', 'sansb', 30, BG, r2[2] - r2[0] - 30, 1.15, 'm', a2)
    a3 = ease((t - F('s3', 0.45)) / 0.7)
    if a3 > 0:
        card(cv, cb, a3, LAV)
        cv.text((cb[0] + 30, cb[1] + 18), 'Schlebusch et al., Science (2017)', 'sansb', 30, LAV, 'la', a3)
        cv.para(cb[0] + 30, cb[1] + 66, 'Deepest split among living human populations: roughly 350,000 to 260,000 years ago', 'serif', 42, CREAM, cb[2] - cb[0] - 60, 1.15, 'l', a3)
    a4 = ease((t - F('s3', 0.72)) / 0.6)
    if a4 > 0: pill(cv, (cb[0] + cb[2]) / 2, py[0], 'African origin: well supported', SAGE, a4, 34)
    a5 = ease((t - F('s3', 0.88)) / 0.6)
    if a5 > 0: pill(cv, (cb[0] + cb[2]) / 2, py[1], 'Why there, and where: open', LAV, a5, 34)

# ---------------------------------------------------------------- s4 two explanations
def sc_two(cv, t, p):
    area = (60, 215, 1860, 690) if not PORT else (30, 350, 1050, 1100)
    side_cards(cv, t, ('The place mattered', COR, ['Rift Valley region: varied habitats, shifting climate', 'Conditions pushed our ancestors to adapt'], ('EXPLANATION 1', COR)),
               ('The record is skewed', TEA, ['Fossils survive and get found in the Rift', 'The true map may be wider'], ('EXPLANATION 2', TEA)),
               F('s4', 0.20), F('s4', 0.50), area=area, size=36 if PORT else 38)
    a = ease((t - F('s4', 0.90)) / 0.7)
    if a > 0: pill(cv, W / 2, 770 if not PORT else 1180, 'Not exclusive: researchers weigh them differently', LAV, a, 34)

# ---------------------------------------------------------------- s5 place mattered
def sc_place(cv, t, p):
    if PORT: dg = (30, 370, 1050, 700); c1 = (30, 740, 1050, 940); c2 = (30, 960, 1050, 1230)
    else: dg = (60, 225, 960, 740); c1 = (1010, 225, 1860, 440); c2 = (1010, 470, 1860, 740)
    a = ease((t - 0.2) / 0.7); card(cv, dg, a, COR)
    cv.text((dg[0] + 30, dg[1] + 18), 'Shifting climate and landscape (schematic)', 'sansb', 28, COR, 'la', a)
    x0, x1, y0, y1 = dg[0] + 40, dg[2] - 40, dg[1] + 90, dg[3] - 60
    tt = clamp01((t - F('s5', 0.18)) / max(0.5, F('s5', 0.50) - F('s5', 0.18)))
    n = int(300 * tt) + 1
    pts = [(x0 + (x1 - x0) * k / 300, (y0 + y1) / 2 + math.sin(k / 300 * 9.0) * (y1 - y0) * 0.26 + math.sin(k / 300 * 23.0) * (y1 - y0) * 0.10) for k in range(n)]
    if len(pts) > 1: cv.line(pts, mix(COR, BG, a), 7)
    cv.text((x1, y1 + 12), 'time', 'sans', 24, DIMC, 'ra', a)
    a1 = ease((t - F('s5', 0.28)) / 0.7)
    if a1 > 0:
        card(cv, c1, a1, COR); cv.text((c1[0] + 28, c1[1] + 16), 'Variability selection', 'serif', 44, COR, 'la', a1)
        cv.para(c1[0] + 28, c1[1] + 74 if not PORT else c1[1] + 72, 'Potts (1998): unstable environments favor species that can adapt', 'sans', 32, CREAM, c1[2] - c1[0] - 56, 1.15, 'l', a1)
    a2 = ease((t - F('s5', 0.55)) / 0.7)
    if a2 > 0:
        card(cv, c2, a2, LAV); cv.text((c2[0] + 28, c2[1] + 16), 'Olorgesailie, Kenya', 'serif', 44, LAV, 'la', a2)
        cv.para(c2[0] + 28, c2[1] + 74, 'Potts et al., Science (2018): disruption coincided with animal turnover and a new toolkit', 'sans', 32, CREAM, c2[2] - c2[0] - 56, 1.15, 'l', a2)
    a3 = ease((t - F('s5', 0.80)) / 0.7)
    if a3 > 0: badge(cv, c2[0] + 28, c2[3] - 62, 'CORRELATION AT ONE SITE · HYPOTHESIS', ROSE, a3, 24)

# ---------------------------------------------------------------- s6 skewed record
def sc_skew(cv, t, p):
    if PORT: dg = (30, 370, 1050, 860); fc = (30, 900, 1050, 1150)
    else: dg = (60, 225, 1100, 780); fc = (1150, 225, 1860, 560)
    a = ease(t / 0.7); card(cv, dg, a, TEA)
    cv.text((dg[0] + 30, dg[1] + 16), 'Cross-section of a Rift basin (schematic)', 'sansb', 28, TEA, 'la', a)
    bx0, bx1, by0, by1 = dg[0] + 50, dg[2] - 330 if not PORT else dg[2] - 50, dg[1] + 100, dg[3] - 40
    h = by1 - by0
    bands = [(0.00, 0.20, (96, 72, 58)), (0.20, 0.31, (150, 120, 88)), (0.31, 0.35, CREAM), (0.35, 0.55, (126, 98, 74)), (0.55, 0.59, CREAM), (0.59, 1.0, (100, 78, 62))]
    tb = F('s6', 0.18)
    for k, (f0, f1, col) in enumerate(reversed(bands)):
        g = ease((t - tb - k * 0.45) / 0.6)
        if g > 0: cv.rect((bx0, by0 + h * f0, bx1, by0 + h * f1), mix(col, BG, g))
    tg = ease((t - F('s6', 0.62)) / 1.0)
    if tg > 0:
        cx = (bx0 + bx1) / 2; top = 0.30 * (bx1 - bx0); bot = 0.07 * (bx1 - bx0); depth = h * 0.42 * tg
        cv.poly([(cx - top / 2, by0), (cx + top / 2, by0), (cx + bot / 2, by0 + depth), (cx - bot / 2, by0 + depth)], mix(CARDC, BG, tg))
        cv.line([(cx - bot / 2, by0 + depth - 4), (cx + bot / 2, by0 + depth - 4)], mix(TEA, BG, tg), 8)
    def lbl(x, y, txt, tc, col=CREAM):
        aa = ease((t - tc) / 0.6)
        if aa > 0: cv.para(x, y, txt, 'sansb', 28, col, 300, 1.12, 'l', aa)
    if not PORT:
        lbl(bx1 + 24, by0 + h * 0.38, 'Ash layers can be dated', F('s6', 0.40), CREAM)
        lbl(bx1 + 24, by0 + h * 0.74, 'Fast burial in sediment', F('s6', 0.20), BONE)
        lbl(bx1 + 24, by0 + h * 0.10, 'River and faulting expose old layers', F('s6', 0.66), TEA)
    else:
        lbl(bx1 - 340, by0 + h * 0.62, 'Ash layers can be dated', F('s6', 0.40), BG)
        lbl(bx1 - 340, by0 + h * 0.80, 'Fast burial in sediment', F('s6', 0.20), CREAM)
        lbl(bx0 + 14, by0 + h * 0.06, 'River and faulting expose old layers', F('s6', 0.66), CREAM)
    a2 = ease((t - F('s6', 0.80)) / 0.7)
    if a2 > 0:
        card(cv, fc, a2, ROSE); cv.text((fc[0] + 28, fc[1] + 16), 'Humid forest', 'serif', 46, ROSE, 'la', a2)
        cv.para(fc[0] + 28, fc[1] + 80, 'Acidic soil and scavengers destroy bones fast: few fossils', 'sans', 34, CREAM, fc[2] - fc[0] - 56, 1.15, 'l', a2)

# ---------------------------------------------------------------- s7 gaps and delays
def sc_gaps(cv, t, p):
    items = [dict(year='1925', who='Taung Child, South Africa', what='Described by Dart; widely doubted for years', at=F('s7', 0.12), col=LAV),
             dict(year='2005', who='First fossil chimpanzee reported', what='Teeth, Kenya Rift Valley, about half a million years', at=F('s7', 0.45), col=COR),
             dict(year='2010', who='Denisovans', what='First identified from DNA in a finger bone', at=F('s7', 0.80), col=TEA)]
    rail(cv, t, items, area=(60, 215, 1860, 830) if not PORT else (30, 360, 1050, 1180))
    a = ease((t - F('s7', 0.88)) / 0.7)
    if a > 0: badge(cv, W / 2 - 330, 740 if not PORT else 1190, 'GAPS AND DELAYS IN THE RECORD', LAV, a, 30)

# ---------------------------------------------------------------- s8 whole continent
AFRICA = [(-5.9, 35.8), (3, 36.8), (10.2, 37.2), (11, 33.5), (20, 32), (25, 31.6), (29.9, 31.2), (32.3, 31.3), (32.6, 29.9), (34, 27), (37, 21), (38.5, 18), (39.5, 15.5), (43.1, 12.7), (51.2, 11.8),
          (51, 10.4), (48, 5), (42, -0.5), (40, -3), (39.3, -6.8), (40.5, -10.5), (40.5, -15), (35, -20), (35.5, -24), (32.5, -26), (32.8, -28.5), (30, -31.5), (27, -33.8), (22, -34), (18.4, -34.2),
          (17.5, -30), (15, -26.5), (14.5, -22), (11.8, -17), (13.5, -12), (12.3, -6), (9, -1), (9.5, 3.5), (7, 4.3), (4.5, 6.3), (1, 6), (-3, 5), (-7.5, 4.4), (-12.5, 7.3), (-17.5, 14.7), (-16.5, 20),
          (-13, 27.5), (-9.8, 31), (-9.5, 33), (-6.8, 34)]
RIFT = [(40.5, 12), (38, 8), (36.2, 4.5), (36.6, 0), (36.3, -2), (35.8, -4), (34.8, -8), (34.5, -12), (35, -16)]
def sc_continent(cv, t, p):
    if PORT: mx, my, ms = 40, 400, 540; c1 = (610, 400, 1050, 700); c2 = (610, 730, 1050, 990)
    else: mx, my, ms = 150, 205, 610; c1 = (880, 240, 1860, 480); c2 = (880, 520, 1860, 740)
    pr = lambda ll: (mx + (ll[0] + 18) / 70 * ms, my + (37 - ll[1]) / 72 * ms)
    a = ease(t / 0.8)
    cv.poly([pr(q) for q in AFRICA], mix((74, 56, 52), BG, a), mix(DIMC, BG, 0.6 * a))
    cv.line([pr(q) for q in RIFT], mix(TEA, BG, 0.55 * a), 14)
    cv.text((pr((34, -10))[0] - 10, pr((34, -10))[1]), 'East African Rift', 'sans', 24, TEA, 'ra', a)
    a1 = ease((t - F('s8', 0.25)) / 0.6); a2 = ease((t - F('s8', 0.32)) / 0.6)
    pi, po = pr((-8.9, 31.9)), pr((35.9, 5.4))
    if a1 > 0: cv.circ(pi, 13, mix(COR, BG, a1)); cv.text((pi[0] + 20, pi[1] - 16), 'Jebel Irhoud', 'sansb', 26, COR, 'la', a1)
    if a2 > 0:
        cv.circ(po, 13, mix(COR, BG, a2)); cv.text((po[0] - 20, po[1] - 46), 'Omo Kibish', 'sansb', 26, COR, 'ra', a2)
        cv.line([pi, po], mix(COR, BG, 0.5 * a2), 4)
        cv.text(((pi[0] + po[0]) / 2, (pi[1] + po[1]) / 2 - 38), 'thousands of km', 'sans', 24, DIMC, 'ma', a2)
    a3 = ease((t - F('s8', 0.45)) / 0.7)
    if a3 > 0:
        card(cv, c1, a3, LAV); cv.text((c1[0] + 28, c1[1] + 16), 'Multiregional view', 'serif', 44, LAV, 'la', a3)
        cv.para(c1[0] + 28, c1[1] + 76, 'Scerri et al., Trends in Ecology & Evolution (2018): many partly connected populations across Africa, not one cradle', 'sans', 32, CREAM, c1[2] - c1[0] - 56, 1.15, 'l', a3)
    a4 = ease((t - F('s8', 0.85)) / 0.7)
    if a4 > 0:
        card(cv, c2, a4, ROSE); cv.text((c2[0] + 28, c2[1] + 16), 'Interpretation', 'serif', 44, ROSE, 'la', a4)
        cv.para(c2[0] + 28, c2[1] + 76, 'Not a settled result. "Which valley?" may have no single answer.', 'sans', 32, CREAM, c2[2] - c2[0] - 56, 1.15, 'l', a4)
    cv.text((mx + ms / 2, my + ms + 24), 'schematic map', 'sans', 24, DIMC, 'ma', a)

# ---------------------------------------------------------------- s9 Toba
def sc_toba(cv, t, p):
    if PORT: vg = (30, 380, 1050, 830); cd = (30, 870, 1050, 1180)
    else: vg = (60, 225, 900, 780); cd = (960, 225, 1860, 640)
    a = ease(t / 0.7); card(cv, vg, a, DIMC)
    bx = (vg[0] + vg[2]) / 2; by = vg[3] - 60; pk = vg[1] + 260
    cv.poly([(bx - 300, by), (bx - 40, pk), (bx + 40, pk), (bx + 300, by)], mix((92, 70, 60), BG, a))
    ta = F('s9', 0.20)
    for k in range(6):
        g = ease((t - ta - k * 0.5) / 1.2)
        if g > 0:
            r = 18 + k * 7 + g * 8
            cv.circ((bx + math.sin(k * 1.7) * 30, pk - 20 - k * 28 * g), r, mix(DIMC, BG, 0.45 * g))
    cv.text((bx, by + 12), 'Toba, Sumatra  ·  about 74,000 years ago', 'sansb', 28, CREAM, 'ma', a)
    cv.text((vg[0] + 24, vg[1] + 14), 'schematic', 'sans', 24, DIMC, 'la', a)
    a2 = ease((t - F('s9', 0.50)) / 0.7)
    if a2 > 0:
        card(cv, cd, a2, LAV); cv.text((cd[0] + 30, cd[1] + 18), 'Toba catastrophe hypothesis', 'serif', 46, LAV, 'la', a2)
        cv.para(cd[0] + 30, cd[1] + 84, 'Ambrose (1998): a volcanic winter cut human numbers to a small group of survivors', 'sans', 36, CREAM, cd[2] - cd[0] - 60, 1.15, 'l', a2)
    a3 = ease((t - F('s9', 0.85)) / 0.7)
    if a3 > 0: badge(cv, cd[0] + 30, cd[3] - 70, 'HYPOTHESIS', LAV, a3, 30)

# ---------------------------------------------------------------- s10 Toba pushback
def sc_pushback(cv, t, p):
    items = [dict(year='2007', who='Petraglia et al., Science', what='India: tools above and below the ash, no clear break', at=F('s10', 0.12), col=SAGE),
             dict(year='2013', who='Lane et al., PNAS', what='Lake Malawi: ash, but no volcanic winter signal', at=F('s10', 0.38), col=SAGE),
             dict(year='2018', who='Smith et al., Nature', what='South Africa coast: people lived on through it', at=F('s10', 0.64), col=SAGE)]
    rail(cv, t, items, area=(60, 215, 1860, 830) if not PORT else (30, 360, 1050, 1150))
    a = ease((t - F('s10', 0.85)) / 0.7)
    if a > 0: badge(cv, W / 2 - 250, 740 if not PORT else 1170, 'CONTESTED · NOT ESTABLISHED', ROSE, a, 32)

# ---------------------------------------------------------------- s11 what would settle it
def sc_settle(cv, t, p):
    rows = [(F('s11', 0.10), 'Search places that preserve poorly or are little explored'), (F('s11', 0.42), 'Date more sites precisely'),
            (F('s11', 0.55), 'Recover ancient proteins: they can outlast DNA in warm climates'), (F('s11', 0.85), 'Compare more genomes, ancient and living')]
    y = 250 if not PORT else 420; step = 135 if not PORT else 190
    for i, (tc, txt) in enumerate(rows):
        a = ease((t - tc) / 0.7)
        if a <= 0: continue
        x = 140 if not PORT else 60
        checkbox(cv, x, y + i * step, 56, a)
        cv.para(x + 100, y + i * step - 6, txt, 'serif', 48 if not PORT else 44, CREAM, W - x - 220, 1.15, 'l', a)

# ---------------------------------------------------------------- s12 what this shows
def sc_shows(cv, t, p):
    side_cards(cv, t, ('Established', SAGE, ['Oldest known fossils of our species are in Africa', 'Genetics agrees our species began there', 'Volcanic ash at Rift sites lets many fossil layers be dated'], ('PUBLISHED EVIDENCE', SAGE)),
               ('Not established', LAV, ["Did Africa's conditions cause our origin, or only reveal it?", 'One region, or a network of populations?', 'Did Toba nearly end us?'], ('OPEN', LAV)),
               F('s12', 0.12), F('s12', 0.50), area=(60, 215, 1860, 780) if not PORT else (30, 350, 1050, 1230), size=34 if PORT else 38)

# ---------------------------------------------------------------- s13 close, s14 end
def sc_close(cv, t, p):
    statements(cv, t, [(F('s13', 0.0), 'This does not settle whether Africa was special.', CREAM, 'serif'), (F('s13', 0.25), 'A map of fossils is partly a map of preservation and of searching.', LAV, 'serif'),
                       (F('s13', 0.60), 'Scientists still argue about how much is real, and how much is the record.', DIMC, 'serifr')], 230 if not PORT else 290)
    a = ease((t - F('s13', 0.25)) / 0.8); x0 = W / 2 - 120; y = 880 if not PORT else 1160
    cv.rect((x0, y, x0 + 120, y + 6), mix(COR, BG, a)); cv.rect((x0 + 120, y, x0 + 240, y + 6), mix(TEA, BG, a))

SOURCES = ['Leakey & Hay, Nature (1979): Laetoli · Leakey, Evernden & Curtis, Nature (1961): Olduvai dating',
           'Hublin et al., Nature (2017): Jebel Irhoud · Vidal et al., Nature (2022): Omo Kibish · Schlebusch et al., Science (2017): population split',
           'Potts, Yearbook of Physical Anthropology (1998): variability selection · Potts et al., Science (2018): Olorgesailie',
           'Dart, Nature (1925): Taung Child · McBrearty & Jablonski, Nature (2005): fossil chimpanzee · Krause et al., Nature (2010): Denisovans',
           'Scerri et al., Trends in Ecology & Evolution (2018): African multiregional model',
           'Ambrose, Journal of Human Evolution (1998): Toba · Petraglia et al., Science (2007) · Lane et al., PNAS (2013) · Smith et al., Nature (2018)']

def sc_end(cv, t, p):
    a = ease(t / 1.0); cy = 80 if not PORT else 230
    cv.text((W / 2, cy), 'Heartbeat Observatory', 'serif', 96 if not PORT else 88, CREAM, 'ma', a)
    cv.rect((W / 2 - 100, cy + 125, W / 2, cy + 131), mix(COR, BG, a)); cv.rect((W / 2, cy + 125, W / 2 + 100, cy + 131), mix(TEA, BG, a))
    cv.text((W / 2, cy + 150), 'heartbeatobservatory.com', 'sansb', 52, COR, 'ma', a)
    cv.text((W / 2, cy + 225), 'Open Questions · Episode 3 · sources checked October 2026', 'sans', 34 if not PORT else 30, DIMC, 'ma', a)
    y = cy + 300; cv.text((W / 2, y), 'Sources', 'sansb', 32, DIMC, 'ma', ease((t - 0.6) / 1))
    yy = y + 50
    for i, s in enumerate(SOURCES):
        yy = cv.para(W / 2, yy, s, 'sans', 28 if not PORT else 27, CREAM, 1700 if not PORT else 980, 1.2, 'm', ease((t - 0.8 - i * 0.2) / 0.8)) + 8

SCENES = [
 ('s1', '', '', sc_title),
 ('s2', 'What the fossils show', 'Sources: Leakey & Hay, Nature (1979); Leakey, Evernden & Curtis, Nature (1961); Hublin et al. (2017); Vidal et al. (2022). Ages approximate.', sc_fossils),
 ('s3', 'What genetics adds', 'Source: Schlebusch et al., Science (2017). Diagram is schematic, not data.', sc_genes),
 ('s4', 'Two kinds of explanation', 'Researchers weigh these in different amounts; they are not exclusive.', sc_two),
 ('s5', 'Explanation 1: the place mattered', 'Sources: Potts (1998); Potts et al., Science (2018). Curve is schematic.', sc_place),
 ('s6', 'Explanation 2: a skewed record', 'Drawing is schematic. Dating by potassium-argon and argon-argon methods.', sc_skew),
 ('s7', 'Gaps and delays in the record', 'Sources: Dart, Nature (1925); McBrearty & Jablonski, Nature (2005); Krause et al., Nature (2010).', sc_gaps),
 ('s8', 'A third view: a whole continent', 'Source: Scerri et al., Trends in Ecology & Evolution (2018). Map is schematic.', sc_continent),
 ('s9', 'A different question: survival', 'Source: Ambrose, Journal of Human Evolution (1998). Drawing is schematic.', sc_toba),
 ('s10', 'Studies that pushed back', 'Sources: Petraglia et al., Science (2007); Lane et al., PNAS (2013); Smith et al., Nature (2018).', sc_pushback),
 ('s11', 'What would narrow it down', '', sc_settle),
 ('s12', 'What this shows, and what it does not', '', sc_shows),
 ('s13', '', '', sc_close),
 ('s14', '', '', sc_end),
]
configure(SUBS, SCENES)
if __name__ == '__main__': main()
