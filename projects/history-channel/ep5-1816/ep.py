import sys, re; sys.path.insert(0, '../../tv-lib')
from tvlib import *
import tvlib

SOOT = (60, 52, 64); HAZE = (200, 150, 90)

def at(sid, f):
    """time inside scene sid at fraction f of its narration"""
    return SEG[sid]['start'] + f * SEG[sid]['dur'] - tvlib.BOUND[sid][0]

def sun(cv, c, r, a=1.0, haze=0.0):
    for k in range(6, 0, -1):
        cv.circ(c, r + k * 22, mix(AMBER, BG, 0.05 * a * (1 - haze * 0.4)))
    cv.circ(c, r, mix(AMBER, BG, a))
    if haze > 0:
        cv.circ(c, r, mix(HAZE, BG, 0.30 * haze * a))

def sc_title(cv, t, p):
    a = ease(t / 1.4)
    cx = W / 2; cy = 700 if not PORT else 900
    r = 150 if not PORT else 190
    sun(cv, (cx, cy), r, a, haze=min(1, t / 6))
    for k in range(5):
        y = cy - 40 + k * 46
        cv.rect((60, y, W - 60, y + 14), mix(SOOT, BG, 0.30 * ease((t - 1.5 - k * 0.5) / 1.5)))
    a2 = ease(t / 1.2)
    cv.text((W / 2, 150 if PORT else 36), 'HEARTBEAT TV  ·  HISTORY  ·  EPISODE 5', 'sansb', 34 if PORT else 36, AMBER, 'ma', a2)
    for k, l in enumerate(('The year summer', 'never came')):
        cv.text((W / 2, (230 if PORT else 90) + k * (110 if PORT else 128)), l, 'serif', 96 if PORT else 112, TXT, 'ma', ease((t - 0.2) / 1.2), 6)
    cv.text((W / 2, 1180 if PORT else 960), '1816, and the volcano behind it', 'serifr', 44, DIM, 'ma', ease((t - 1.0) / 1.0))

def sc_eruption(cv, t, p):
    stat_cards(cv, t, [
        dict(num='Apr 1815', label='Tambora erupts, Sumbawa (Indonesia)', sub='main blast about April 10', at=at('s2', 0.1)),
        dict(num='VEI 7', label='among the largest in recorded history', sub='heard about 2,000 km away', col=RED, at=at('s2', 0.35)),
        dict(num='≈ 71,000', label='deaths nearby: one estimate (Oppenheimer)', sub='mostly hunger and disease', col=TEAL, tag='ESTIMATES VARY', at=at('s2', 0.7))])

def sc_aerosol(cv, t, p):
    x0, y0, x1, y1 = CONT
    if PORT: y1 -= 40
    h = y1 - y0
    sx = x0 + (x1 - x0) * 0.18; sy = y0 + 110
    cv.circ((sx, sy), 46, AMBER); cv.circ((sx, sy), 66, mix(AMBER, BG, 0.15))
    lay_y = y0 + h * 0.42; ground = y1 - 60
    cv.rect((x0, ground, x1, y1), (46, 84, 70))
    cv.text((x0 + 16, ground + 8), 'Earth surface', 'sansb', 30, TXT, 'la')
    a_v = ease((t - at('s3', 0.30)) / 1.5)
    if a_v > 0:
        for k in range(3):
            cv.rect((x0, lay_y + k * 14, x1, lay_y + k * 14 + 8), mix(HAZE, BG, 0.55 * a_v))
        cv.text((x1 - 10, lay_y - 44), 'Sulfate droplet veil, stratosphere', 'sansb', 32 if not PORT else 28, HAZE, 'ra', a_v, stroke=5)
    a_r = ease((t - at('s3', 0.2)) / 1.2)
    nrays = 6 if not PORT else 4
    for k in range(nrays):
        xs = sx + 60 + k * ((x1 - sx - 120) / nrays)
        cv.line([(sx + 30, sy + 30), (xs, lay_y)], mix(AMBER, BG, 0.8 * a_r), 4)
        if a_v > 0.2 and k % 2 == 0:
            cv.line([(xs, lay_y), (xs + 90, y0 + 20)], mix(AMBER, BG, 0.5 * a_v), 3)
        else:
            cv.line([(xs, lay_y), (xs + (20 if a_v < 0.2 else 6), ground)], mix(AMBER, BG, 0.8 * a_r * (1 - 0.5 * a_v)), 4)
    if a_v > 0.5:
        cv.text(((x0 + x1) / 2, lay_y + 80), 'some sunlight reflected back to space', 'sans', 32, DIM, 'ma', a_v)
    a2 = ease((t - at('s3', 0.78)) / 0.8)
    if a2 > 0:
        badge(cv, W / 2, ground - 62, 'DEBATED: ~1809 eruption + weak sun also in play', RED, a2, 28 if not PORT else 24, 'm')

def range_bar(cv, area, rows, vmax, tt, ticks):
    x0, y0, x1, y1 = area
    lw = 460 if not PORT else 300
    ax0 = x0 + lw; ax1 = x1 - 120
    n = len(rows); step = (y1 - y0 - 70) / n
    for v in ticks:
        xx = ax0 + (ax1 - ax0) * v / vmax
        cv.line([(xx, y0), (xx, y1 - 60)], mix(STEEL, BG, 0.35), 2)
        cv.text((xx, y1 - 50), f'{v:g} °C', 'sans', 30, DIM, 'ma')
    for i, r in enumerate(rows):
        a = ease((tt - r['at']) / 0.6)
        if a <= 0: continue
        yy = y0 + i * step + step / 2
        for k, l in enumerate(wrap(r['label'], font('sansb', 32 if not PORT else 28), lw - 20)):
            cv.text((ax0 - 14, yy - 22 + k * 36), l, 'sansb', 32 if not PORT else 28, TXT, 'ra', a)
        u = ease((tt - r['at'] - 0.2) / 1.0)
        xa = ax0 + (ax1 - ax0) * r['lo'] / vmax; xb = ax0 + (ax1 - ax0) * (r['lo'] + (r['hi'] - r['lo']) * u) / vmax
        cv.rect((xa, yy - 24, max(xa + 8, xb), yy + 24), mix(r.get('col', AMBER), BG, a), 8)
        if u > 0.9: cv.text((xb + 12, yy - 22), r['txt'], 'serif', 38 if not PORT else 32, r.get('col', AMBER), 'la', a)

def sc_cooling(cv, t, p):
    range_bar(cv, (CONT[0], CONT[1] + 10, CONT[2], CONT[3] - 90), [
        dict(label='Annual, tropics + N. extratropics, vs prior 30 yrs', lo=0.4, hi=0.8, txt='≈ 0.4 to 0.8', col=AMBER, at=at('s4', 0.25)),
        dict(label='Some regional summers, Europe and North America', lo=0.8, hi=2.0, txt='often more', col=RED, at=at('s4', 0.55)),
    ], 3.2, t, [0, 1, 2, 3])
    a = ease((t - at('s4', 0.5)) / 0.6)
    if a > 0: badge(cv, W / 2, CONT[3] - 70, 'A RANGE, NOT ONE NUMBER: differs by study', AMBER, a, 30 if not PORT else 25, 'm')

def flake(cv, c, r, col, a=1.0):
    for k in range(6):
        ang = k * math.pi / 3
        cv.line([c, (c[0] + r * math.cos(ang), c[1] + r * math.sin(ang))], mix(col, BG, a), 4)

def sc_newengland(cv, t, p):
    x0, y0, x1, y1 = CONT
    days = list(range(1, 11)) if not PORT else list(range(3, 11))
    n = len(days); gap = 14
    w = (x1 - x0 - gap * (n - 1)) / n; hh = 200 if not PORT else 170
    cv.text(((x0 + x1) / 2, y0 + 4), 'JUNE 1816', 'sansb', 36, AMBER, 'ma', ease(t / 0.8))
    for i, dn in enumerate(days):
        bx = (x0 + i * (w + gap), y0 + 60, x0 + i * (w + gap) + w, y0 + 60 + hh)
        a = ease((t - 0.3 - i * 0.12) / 0.5)
        hit = dn in (6, 7)
        cv.rect(bx, mix(CARD, BG, a), 12); cv.outline(bx, mix(TEAL if hit else STEEL, BG, (0.9 if hit else 0.5) * a), 3 if hit else 2, 12)
        cv.text(((bx[0] + bx[2]) / 2, bx[1] + 12), str(dn), 'serif', 52, TXT, 'ma', a)
        if hit:
            ah = ease((t - at('s5', 0.28)) / 0.7)
            if ah > 0: flake(cv, ((bx[0] + bx[2]) / 2, bx[1] + 130 if not PORT else bx[1] + 115), 34, TEAL, ah)
    stat_cards(cv, t, [
        dict(num='Snow', label='parts of New England, New York, Quebec', sub='June 6-7', col=TEAL, at=at('s5', 0.32)),
        dict(num='Frost', label='returned in July and August', col=BLUE, at=at('s5', 0.5)),
        dict(num='Corn', label='failed in many places', sub='the staple crop', col=AMBER, at=at('s5', 0.62))],
        area=(CONT[0], CONT[1] + 60 + hh + 30, CONT[2], CONT[3]))

def sc_europe(cv, t, p):
    stat_cards(cv, t, [
        dict(num='Rain', label='cold, sodden summer, late and poor harvest', sub='France, Switzerland, Germany, British Isles', col=BLUE, at=at('s6', 0.1)),
        dict(num='Prices', label='grain prices climbed sharply, in places by double', sub='bread riots, people left home to beg', col=AMBER, at=at('s6', 0.32)),
        dict(num='Deaths?', label='no reliable total exists', sub='published figures differ widely', col=RED, tag='DISPUTED', at=at('s6', 0.78))])

def sc_migration(cv, t, p):
    x0, y0, x1, y1 = CONT
    y1 -= 20 if not PORT else 60
    w = x1 - x0; h = y1 - y0
    if not PORT:
        east = (x0 + w * 0.80, y0 + h * 0.32)
        dest = [(x0 + w * 0.43, y0 + h * 0.58, 'Ohio'), (x0 + w * 0.28, y0 + h * 0.58, 'Indiana'), (x0 + w * 0.14, y0 + h * 0.58, 'Illinois')]
    else:
        east = (x0 + w * 0.72, y0 + h * 0.20)
        dest = [(x0 + w * 0.60, y0 + h * 0.55, 'Ohio'), (x0 + w * 0.34, y0 + h * 0.55, 'Indiana'), (x0 + w * 0.12, y0 + h * 0.55, 'Illinois')]
    a = ease(t / 0.8)
    cv.circ(east, 26, mix(AMBER, BG, a)); cv.text((east[0], east[1] + 38), 'New England', 'sansb', 38, TXT, 'ma', a)
    a2 = ease((t - at('s7', 0.35)) / 0.8)
    for (px, py, nm) in dest:
        cv.circ((px, py), 22, mix(TEAL, BG, a2)); cv.text((px, py + 32), nm, 'sansb', 36, TXT, 'ma', a2)
    u = ease((t - at('s7', 0.2)) / 2.5)
    if u > 0:
        west = (dest[1][0], dest[1][1])
        mid = ((east[0] + west[0]) / 2, min(east[1], west[1]) - 80)
        pp = [(((1 - s) ** 2) * east[0] + 2 * (1 - s) * s * mid[0] + s * s * west[0], ((1 - s) ** 2) * east[1] + 2 * (1 - s) * s * mid[1] + s * s * west[1]) for s in [k / 30 * u for k in range(31)]]
        cv.line(pp, AMBER, 6)
    cv.text(((x0 + x1) / 2, y0 + 4), 'Schematic, not a map', 'sans', 30, DIM, 'ma', a)
    ab = ease((t - at('s7', 0.5)) / 0.7)
    if ab > 0: badge(cv, W / 2, y1 - 20 if not PORT else y1 + 10, 'NOT KNOWN: how many left because of the weather', RED, ab, 30 if not PORT else 25, 'm')
    ac = ease((t - at('s7', 0.82)) / 0.7)
    if ac > 0: cv.text(((x0 + x1) / 2, y0 + 70), 'Indiana statehood: Dec 1816', 'serif', 46, TEAL, 'ma', ac)

def sc_geneva(cv, t, p):
    people = [('Lord Byron', 'ghost-story contest; "Darkness" (1816)'), ('Percy Shelley', 'poet'), ('Mary Shelley', 'began Frankenstein'),
              ('Claire Clairmont', "Mary's stepsister"), ('John Polidori', "Byron's doctor; later wrote The Vampyre")]
    x0, y0, x1, y1 = CONT; y1 -= 130 if not PORT else 110
    n = len(people); gap = 18
    for i, (nm, sub) in enumerate(people):
        a = ease((t - at('s8', 0.15) - i * 0.5) / 0.6)
        if a <= 0: continue
        if not PORT:
            w = (x1 - x0 - gap * (n - 1)) / n; bx = (x0 + i * (w + gap), y0 + 10, x0 + i * (w + gap) + w, y0 + 300)
            cv.rect(bx, mix(CARD, BG, a), 16); cv.outline(bx, mix(STEEL, BG, 0.5 * a), 2, 16)
            cv.circ(((bx[0] + bx[2]) / 2, bx[1] + 60), 30, mix(STEEL, BG, a))
            cv.para((bx[0] + bx[2]) / 2, bx[1] + 110, nm, 'serif', 36, TXT, w - 30, 1.1, 'm', a)
            cv.para((bx[0] + bx[2]) / 2, bx[1] + 200, sub, 'sans', 28, DIM, w - 30, 1.15, 'm', a)
        else:
            hh = (y1 - y0 - gap * (n - 1)) / n; bx = (x0, y0 + i * (hh + gap), x1, y0 + i * (hh + gap) + hh)
            cv.rect(bx, mix(CARD, BG, a), 14); cv.outline(bx, mix(STEEL, BG, 0.5 * a), 2, 14)
            cv.text((bx[0] + 24, bx[1] + 14), nm, 'serif', 38, TXT, 'la', a)
            cv.para(bx[0] + 24, bx[1] + 62, sub, 'sans', 28, DIM, bx[2] - bx[0] - 48, 1.15, 'l', a)
    a1 = ease((t - at('s8', 0.7)) / 0.6); a2 = ease((t - at('s8', 0.86)) / 0.6)
    yb = CONT[3] - 100 if not PORT else CONT[3] - 90
    if a1 > 0: badge(cv, W / 2, yb - 4, 'DOCUMENTED: a wet, cold summer at Lake Geneva, 1816', TEAL, a1, 30 if not PORT else 24, 'm')
    if a2 > 0: badge(cv, W / 2, yb + 62 if not PORT else yb + 52, 'INTERPRETATION: volcano "caused" the books', RED, a2, 30 if not PORT else 24, 'm')

def sc_score(cv, t, p):
    x0, y0, x1, y1 = CONT
    est = ['Tambora erupted in 1815', 'Summer 1816 was unusually cold in the Northern Hemisphere', 'Harvests failed in parts of Europe and North America']
    deb = ['How big the cooling was', 'How much is due to Tambora', 'How many people died', 'How much it changed history']
    if not PORT:
        cw = (x1 - x0 - 30) / 2; cols = [(x0, x0 + cw), (x0 + cw + 30, x1)]; ytop = [y0, y0]; hcol = [y1 - y0 - 80] * 2
    else:
        hcol = [(y1 - y0 - 20) * 0.42, (y1 - y0 - 20) * 0.58 - 20]
        cols = [(x0, x1), (x0, x1)]; ytop = [y0, y0 + hcol[0] + 20]
    for ci, (title, items, col, c0) in enumerate((('ESTABLISHED', est, TEAL, at('s9', 0.28)), ('DEBATED', deb, AMBER, at('s9', 0.62)))):
        a = ease((t - c0) / 0.6)
        if a <= 0: continue
        bx = (cols[ci][0], ytop[ci], cols[ci][1], ytop[ci] + hcol[ci])
        cv.rect(bx, mix(CARD, BG, a), 18); cv.outline(bx, mix(col, BG, 0.8 * a), 3, 18)
        cv.text(((bx[0] + bx[2]) / 2, bx[1] + 18), title, 'serif', 52, col, 'ma', a)
        yy = bx[1] + 100
        for k, it in enumerate(items):
            ai = ease((t - c0 - 0.5 - k * 0.5) / 0.5)
            yy = cv.para(bx[0] + 30, yy, it, 'sansb', 34 if not PORT else 32, TXT, bx[2] - bx[0] - 60, 1.15, 'l', ai) + 14
    a3 = ease((t - at('s9', 0.05)) / 0.6)
    if a3 > 0 and t < at('s9', 0.28): badge(cv, W / 2, CONT[1] + 200, 'UNPROVEN: bicycle invented because horses starved', RED, a3, 32 if not PORT else 26, 'm')

def sc_end(cv, t, p):
    end_block(cv, t, 'History', 5, ['Oppenheimer (2003), Tambora, Prog. Phys. Geography · Raible et al. (2016), WIREs Climate Change · ice-core sulfate records',
        'John D. Post, The Last Great Subsistence Crisis in the Western World (1977) · Mary Shelley, Introduction to Frankenstein (1831)',
        'G. D. Wood, Tambora (2014) · Byron, Darkness (1816) · historical New England weather diaries'])

def _norm(s):
    for a, b in (('eighteen sixteen', '1816'), ('eighteen fifteen', '1815'), ('eighteen oh nine', '1809'), ('eighteen seventeen', '1817'),
                 ('seventy one thousand', '71,000'), ('four tenths to eight tenths', '0.4 to 0.8'), ('two thousand', '2,000'), ('Eighteen Hundred', '1800')):
        s = s.replace(a, b)
    return s

def _subs():
    sc = json.load(open('script.json', encoding='utf-8')); out = {}
    for d in sc:
        t = _norm(d['text']).replace('heartbeatobservatory.com', 'heartbeatobservatory~com')
        ss = [x.strip().replace('~', '.') for x in re.findall(r'[^.!?]+[.!?]+', t)]
        out[d['id']] = [] if d['id'] == 's10' else ss
    return out

SUBS = _subs()
SCENES = [
 ('s1', '', '', sc_title),
 ('s2', 'Mount Tambora, April 1815', 'Sources: Oppenheimer (2003); Stothers (1984); Self et al. 71,000 is one estimate (Oppenheimer); others differ.', sc_eruption),
 ('s3', 'How a volcano cools the world', 'Sources: ice-core sulfate records (Greenland, Antarctica); Raible et al. (2016). Diagram is schematic.', sc_aerosol),
 ('s4', 'How much colder?', 'Sources: Raible et al. (2016), WIREs Climate Change; tree-ring and instrumental reconstructions. Ranges differ by study; regional bar is approximate.', sc_cooling),
 ('s5', 'New England, 1816', 'Sources: newspapers and diaries of the time; Post (1977); Wood (2014). Snow June 6-7 is documented in parts, not everywhere.', sc_newengland),
 ('s6', 'Europe: rain and hunger', 'Sources: Post (1977); regional grain-price and harvest records. No reliable death total exists.', sc_europe),
 ('s7', 'People moved west', 'Sources: Post (1977); historians of westward migration. Role of the weather vs earlier trends is debated.', sc_migration),
 ('s8', 'Lake Geneva, June 1816', 'Sources: Mary Shelley, Introduction to Frankenstein (1831); Byron, Darkness; Polidori. Weather role in the books is interpretation.', sc_geneva),
 ('s9', 'Established vs debated', 'Sources as listed at the end. The bicycle story (Drais, 1817) is repeated by some historians but not firmly proven.', sc_score),
 ('s10', '', '', sc_end),
]
configure(SUBS, SCENES)
if __name__ == '__main__': main()
