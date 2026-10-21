import sys; sys.path.insert(0, '../../tv-lib')
from tvlib import *

SAND = (214, 186, 124); SANDD = (150, 126, 80)

def pyramid(cv, box, a=1.0, fill=None, edge=None):
    x0, y0, x1, y1 = box
    top = ((x0 + x1) / 2, y0)
    cv.poly([top, (x1, y1), (x0, y1)], mix(fill or (40, 56, 84), BG, a), mix(edge or STEEL, BG, a))
    return top

def sc_title(cv, t, p):
    a = ease(t / 1.2)
    if PORT: box = (140, 520, 940, 1180)
    else: box = (610, 330, 1310, 930)
    pyramid(cv, box, a * 0.8, (44, 58, 84))
    n = 9
    for k in range(1, n):
        y = box[1] + (box[3] - box[1]) * k / n; half = (box[2] - box[0]) / 2 * k / n; cx = (box[0] + box[2]) / 2
        cv.line([(cx - half, y), (cx + half, y)], mix(SANDD, BG, 0.5 * a), 2)
    title_block(cv, t, 'HISTORY', 4, 'How the pyramids', 'were built', 'What we actually know')

def sc_great(cv, t, p):
    stat_cards(cv, t, [
        dict(num='≈ 2600 BC', label='Built for Pharaoh Khufu, Fourth Dynasty', sub='radiocarbon: 2613–2577 BC; sources differ', at=cue('s2', 0) + 0.6),
        dict(num='146.6 m', label='original height', sub='today 138.5 m, casing stones gone', at=cue('s2', 2)),
        dict(num='≈ 2.3 million', label='blocks', sub='an estimate', at=cue('s2', 2) + 2.0)])

def sc_workers(cv, t, p):
    c3 = cue('s3', 3)
    if t < c3 - 0.2:
        stat_cards(cv, t, [
            dict(num='Later', label='Greek writers said slaves', sub='written centuries afterwards', col=DIM, at=cue('s3', 0) + 1.5),
            dict(num='Town', label='bakeries and grain silos', sub='Heit el-Ghurab, over 7 hectares', at=cue('s3', 2)),
            dict(num='Tombs', label='workers buried near the pyramids', sub='with bread and beer jars', col=TEAL, at=cue('s3', 2) + 3.0)])
    else:
        hbars(cv, t, [
            dict(label='Diodorus (ancient claim)', val=360000, txt='360,000', at=c3 - 0.1, col=DIM),
            dict(label='Herodotus (ancient claim)', val=100000, txt='100,000', at=c3 + 0.2, col=DIM),
            dict(label='Modern estimate: peak', val=40000, txt='≈ 40,000', at=c3 + 3.0, col=AMBER),
            dict(label='Modern estimate: average', val=14000, txt='≈ 14,000', at=c3 + 3.4, col=AMBER)],
            360000, area=(CONT[0], CONT[1] + 10, CONT[2], CONT[3] - 110))
        a = ease((t - cue('s3', 4) - 0.5) / 0.6)
        if a > 0: badge(cv, W / 2, CONT[3] - 85, 'OPEN: how many were paid, how many served as labor tax', AMBER, a, 30 if not PORT else 26, 'm')

def river_map(cv, t):
    x0, y0, x1, y1 = CONT[0], CONT[1], CONT[2], CONT[3] - (0 if not PORT else 100)
    w = x1 - x0; h = y1 - y0
    # Nile band, schematic (runs top to bottom)
    cxn = x0 + w * 0.5
    pts = [(cxn + math.sin(k / 6.0 * 3.14) * w * 0.04 - w * 0.0, y0 + h * k / 12) for k in range(13)]
    for off, wd in ((0, w * 0.10),):
        cv.line(pts, mix(BLUE, BG, 0.35), wd)
    cv.text((cxn, y0 + 6), 'Nile', 'serif', 40, BLUE, 'ma')
    giza = (x0 + w * 0.17, y0 + h * 0.30); tura = (x1 - w * 0.17, y0 + h * 0.70)
    pyramid(cv, (giza[0] - 60, giza[1] - 60, giza[0] + 60, giza[1] + 30), 1.0, (60, 76, 104))
    cv.text((giza[0], giza[1] + 44), 'Giza', 'sansb', 38, TXT, 'ma')
    cv.circ(tura, 22, SAND); cv.text((tura[0], tura[1] + 34), 'Tura quarries', 'sansb', 36, TXT, 'ma')
    cv.text((tura[0], tura[1] + 76), 'white limestone', 'sans', 30, DIM, 'ma')
    return giza, tura, (cxn, y0 + h * 0.5), (x0, y0, x1, y1)

def sc_stone(cv, t, p):
    giza, tura, mid, box = river_map(cv, t)
    a1 = ease((t - cue('s4', 1)) / 0.7)
    bw = 520 if not PORT else 460
    # papyrus card
    bx = (box[0] + 10, box[3] - 150, box[0] + 10 + bw, box[3] - 8)
    if a1 > 0:
        cv.rect(bx, mix(CARD, BG, a1), 16); cv.outline(bx, mix(SAND, BG, 0.6 * a1), 2, 16)
        cv.text((bx[0] + 22, bx[1] + 14), 'Wadi al-Jarf, Red Sea coast', 'sansb', 34, TXT, 'la', a1)
        cv.text((bx[0] + 22, bx[1] + 58), 'papyrus logbooks found 2013', 'sans', 32, SAND, 'la', a1)
        cv.text((bx[0] + 22, bx[1] + 98), 'Diary of Merer, inspector', 'sans', 32, DIM, 'la', a1)
    c2 = cue('s4', 2)
    u = ease((t - c2) / 3.0)
    if u > 0:
        cx, cy = mid[0], mid[1] - 100
        P0, P1, P2 = tura, (mid[0], mid[1] + 40), giza
        def bez(s): return (((1 - s) ** 2) * P0[0] + 2 * (1 - s) * s * P1[0] + s * s * P2[0], ((1 - s) ** 2) * P0[1] + 2 * (1 - s) * s * P1[1] + s * s * P2[1])
        pts = [bez(k / 30 * u) for k in range(31)]
        cv.line(pts, AMBER, 5)
        bp = pts[-1]
        cv.poly([(bp[0] - 36, bp[1] - 6), (bp[0] + 36, bp[1] - 6), (bp[0] + 24, bp[1] + 14), (bp[0] - 24, bp[1] + 14)], AMBER)
        cv.rect((bp[0] - 14, bp[1] - 26, bp[0] + 14, bp[1] - 6), SAND)
    c3 = cue('s4', 3); a3 = ease((t - c3) / 0.8)
    if a3 > 0:
        bx0 = box[0] + (box[2] - box[0]) * 0.42
        for k in range(18):
            xx = box[0] + (box[2] - box[0]) * 0.30 + k * 6
        gx = giza[0] + 150
        dash = [(gx + 30 * math.sin(k / 2.0), box[1] + (box[3] - box[1]) * (0.45 + k * 0.025)) for k in range(14)]
        for k in range(0, 13, 2): cv.line([dash[k], dash[k + 1]], mix(BLUE, BG, a3), 6)
        cv.text((dash[3][0] + 40, dash[3][1] - 10), 'dry Nile branch?', 'sansb', 32, BLUE, 'la', a3)
        badge(cv, dash[6][0] + 40, dash[6][1], 'HYPOTHESIS', RED, a3, 30)

def mini(cv, box, kind, a, label, who, tag, col=AMBER, doubt=False):
    x0, y0, x1, y1 = box
    cv.rect(box, mix(CARD, BG, a), 18); cv.outline(box, mix(STEEL, BG, 0.5 * a), 2, 18)
    px0, px1 = x0 + 40, x1 - 40; py0, py1 = y0 + 30, y1 - 150
    top = pyramid(cv, (px0, py0, px1, py1), a)
    pc = mix(col, BG, a); L = (px0, py1); R = (px1, py1)
    cx = (px0 + px1) / 2
    if kind == 'straight':
        cv.poly([(px0 - 20, py1), (px0 + (px1 - px0) * 0.40, py0 + (py1 - py0) * 0.28), (px0 + (px1 - px0) * 0.50, py0 + (py1 - py0) * 0.28), (px0 + 20, py1)], pc)
    elif kind == 'zigzag':
        pts = []; n = 5
        for k in range(n + 1):
            yy = py1 - (py1 - py0) * 0.9 * k / n; half = (px1 - px0) / 2 * (1 - 0.9 * k / n) * 0.95
            pts.append((cx - half if k % 2 == 0 else cx + half, yy))
        cv.line(pts, pc, 6)
    elif kind == 'spiral':
        pts = []
        for k in range(0, 61):
            s = k / 60.0; ang = s * 3 * 6.283; r = 1 - 0.85 * s
            yy = py1 - (py1 - py0) * 0.85 * s
            half = (px1 - px0) / 2 * (1 - 0.85 * s)
            pts.append((cx + math.sin(ang) * half * 0.95, yy))
        cv.line(pts, pc, 5)
    elif kind == 'internal':
        cv.poly([(px0 - 20, py1), (px0 + (px1 - px0) * 0.38, py0 + (py1 - py0) * 0.62), (px0 + (px1 - px0) * 0.46, py0 + (py1 - py0) * 0.62), (px0 + 20, py1)], pc)
        for k in range(0, 8, 2):
            s0 = k / 8.0; s1 = (k + 1) / 8.0
            cv.line([(cx - 30 + 60 * s0, py0 + (py1 - py0) * (0.62 - 0.5 * s0)), (cx - 30 + 60 * s1, py0 + (py1 - py0) * (0.62 - 0.5 * s1))], mix(RED, BG, a), 5)
    ty = y1 - 140
    cv.text(((x0 + x1) / 2, ty), label, 'sansb', 34, TXT, 'ma', a)
    cv.text(((x0 + x1) / 2, ty + 42), who, 'sans', 28, DIM, 'ma', a)
    badge(cv, (x0 + x1) / 2, ty + 80, tag, RED if doubt else AMBER, a, 22, 'm')

def sc_ramps(cv, t, p):
    c4 = cue('s5', 4)
    if t < c4 - 0.2:
        items = [('straight', 'Straight ramp', 'widely doubted', 'DOUBTED', cue('s5', 1), True),
                 ('zigzag', 'Zigzag ramp', 'proposed by Hölscher', 'THEORY', cue('s5', 2), False),
                 ('spiral', 'Spiral ramp', 'proposed by Lehner', 'THEORY', cue('s5', 2) + 1.0, False),
                 ('internal', 'Internal ramp', 'proposed by Houdin', 'THEORY', cue('s5', 2) + 2.0, False)]
        if PORT:
            w = (CONT[2] - CONT[0] - 24) / 2; h = (CONT[3] - CONT[1] - 74) / 2
            boxes = [(CONT[0] + (i % 2) * (w + 24), CONT[1] + (i // 2) * (h + 24), CONT[0] + (i % 2) * (w + 24) + w, CONT[1] + (i // 2) * (h + 24) + h) for i in range(4)]
        else:
            w = (CONT[2] - CONT[0] - 3 * 24) / 4
            boxes = [(CONT[0] + i * (w + 24), CONT[1], CONT[0] + i * (w + 24) + w, CONT[3] - 40) for i in range(4)]
        for bx, (k, lab, who, tag, at, d) in zip(boxes, items):
            a = ease((t - at) / 0.6)
            if a > 0: mini(cv, bx, k, a, lab, who, tag, AMBER, d)
        note(cv, t, cue('s5', 3), 'None confirmed. Only small ramps have been found.', y=CONT[3] - 30 if not PORT else CONT[3] + 5, col=AMBER, size=32)
    else:
        stat_cards(cv, t, [
            dict(num='≥ 20%', label='slope of the Hatnub quarry ramp', sub='post holes beside the steps for ropes', at=c4),
            dict(num='≥ Khufu', label='dated to at least his reign', sub='inscriptions; announced 2018', col=TEAL, at=c4 + 1.5),
            dict(num='Giza?', label='used on the Great Pyramid?', sub='not known; critics dispute the link', col=RED, tag='NOT ESTABLISHED', at=cue('s5', 5))],
            area=(CONT[0], CONT[1], CONT[2], CONT[3] - 20))

def sc_tools(cv, t, p):
    c = cue('s6', 1)
    stat_cards(cv, t, [
        dict(num='Copper', label='chisels and saws cut limestone', sub='arsenical copper tools found at Giza (Khufu–Khafre reigns)', at=c),
        dict(num='Dolerite', label='pounded granite from Aswan', sub='900+ km south; cut with sand', col=TEAL, at=cue('s6', 2)),
        dict(num='≈ 6×', label='faster cutting with wetted stone', sub='one experiment at a Khufu-era quarry', col=BLUE, at=cue('s6', 3))])

def sc_open(cv, t, p):
    c = cue('s7', 1)
    stat_cards(cv, t, [
        dict(num='Ramps', label='which design, if any, raised the blocks', tag='OPEN', at=c),
        dict(num='25–80 t', label='heaviest granite beams: how were they lifted?', tag='OPEN', at=cue('s7', 2)),
        dict(num='? workers', label='how many, and how they were paid', tag='OPEN', at=cue('s7', 3))],
        area=(CONT[0], CONT[1], CONT[2], CONT[3] - 10))

def sc_lesson(cv, t, p):
    statements(cv, t, [(cue('s8', 0), 'We know the town, the tools, the boats.', TEAL, 'serifr'), (cue('s8', 1), 'The ramps are still a question.', AMBER, 'serif')])

def sc_end(cv, t, p):
    end_block(cv, t, 'History', 4, ['Ramsey et al. (2010), radiocarbon · Lehner & colleagues, workforce study (1999) · AERA, Heit el-Ghurab',
        'P. Tallet, Les papyrus de la Mer Rouge I (2017) · Ghoneim et al., Communications Earth & Environment (2024)',
        'IFAO / Univ. of Liverpool, Hatnub (2018) · M. Odler (2021), Giza copper tools · Hölscher, Arnold, Houdin on ramps'])

SUBS = {
 's1': ['How were the pyramids built? What do we actually know?'],
 's2': ['The Great Pyramid of Giza was built for Pharaoh Khufu, about 4,600 years ago. Sources differ by a few decades.', 'It stood about 147 meters tall,', 'with an estimated 2.3 million blocks.'],
 's3': ['Who built it? Greek writers, centuries later, said slaves.', 'The evidence points elsewhere.', 'Beside the pyramids are a town with bakeries and grain silos, and cemeteries where workers were buried with bread and beer jars.', 'Herodotus claimed 100,000 workers.', 'A modern estimate is about 14,000 on average, 40,000 at peak. Estimates still disagree.'],
 's4': ['How did the stone arrive?', 'In 2013, archaeologists found papyrus logbooks at Wadi al-Jarf, on the Red Sea.', 'They are the diary of an inspector named Merer and his crew, moving white limestone by boat from the Tura quarries to Giza, in Khufu’s last years.', 'A dry Nile branch near the site may have helped. That is a hypothesis.'],
 's5': ['How were the blocks raised? Theories, not answers.', 'A straight ramp is widely doubted.', 'Zigzag, spiral and internal ramps have been proposed.', 'None is confirmed, and only small ramps have been found.', 'At the Hatnub quarry, a team announced a ramp climbing at 20 percent or more, with post holes, dated to at least Khufu’s reign.', 'Whether Giza used the same method is not known.'],
 's6': ['The tools were simple.', 'Copper chisels and saws cut limestone.', 'Granite came from Aswan, over 900 kilometers away, and was pounded with harder dolerite and cut with sand.', 'Wetting stone made cutting about six times faster in one experiment.'],
 's7': ['Still open:', 'the ramp design.', 'How the heaviest granite beams, up to 80 tonnes, were lifted.', 'How many workers there were, and how they were paid.'],
 's8': ['We know the town, the tools and the boats.', 'The ramps are still a question.'],
 's9': [],
}
SCENES = [
 ('s1', '', '', sc_title),
 ('s2', 'The Great Pyramid', 'Sources: Ramsey et al. (2010) radiocarbon dating; standard references. Block count is an estimate; dates vary by source.', sc_great),
 ('s3', 'Who built it?', 'Sources: AERA (Heit el-Ghurab); Lehner et al. workforce study (1999); Hawass (2010) tomb finds; Herodotus; Diodorus. Estimates differ.', sc_workers),
 ('s4', 'How the stone arrived', 'Sources: P. Tallet, Les papyrus de la Mer Rouge I (2017); Ghoneim et al. (2024). Map is schematic, not to scale.', sc_stone),
 ('s5', 'How were blocks raised?', 'Sources: Hölscher; Arnold; Lehner; Houdin (2007). Hatnub: IFAO / Univ. of Liverpool (2018); critics dispute the link to Giza.', sc_ramps),
 ('s6', 'Copper, dolerite, sand', 'Sources: M. Odler (2021); F. Burgos, quarry experiment. One experiment is not proof of the method.', sc_tools),
 ('s7', 'What is still open', 'Open in the scholarly literature (Lehner, Arnold, Tallet). Workforce: Lehner et al. estimate about 14,000 on average, 40,000 at peak.', sc_open),
 ('s8', '', '', sc_lesson),
 ('s9', '', '', sc_end),
]
configure(SUBS, SCENES)
if __name__ == '__main__': main()
