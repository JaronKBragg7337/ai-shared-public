import sys; sys.path.insert(0, '../../tv-lib')
from tvlib import *

BONE = (222, 206, 168); BONED = (150, 132, 98)

def flute(cv, x0, yc, L, th, t, a=1.0, holes=5):
    """bone tube; left end = mouthpiece with V notches, right end broken."""
    body = [(x0, yc - th / 2), (x0 + L, yc - th / 2), (x0 + L + 8, yc - th / 6), (x0 + L - 6, yc), (x0 + L + 10, yc + th / 4), (x0 + L, yc + th / 2), (x0, yc + th / 2)]
    cv.poly(body, mix(BONE, BG, a), mix(BONED, BG, a))
    for dy in (-1, 1):
        cv.poly([(x0, yc + dy * th / 2), (x0 + 38, yc + dy * th / 2), (x0 + 14, yc + dy * th * 0.05)], BG)
    pos = [0.36, 0.47, 0.58, 0.70, 0.81][:holes]
    for k, f in enumerate(pos):
        cv.circ((x0 + L * f, yc), th * 0.22, mix((58, 46, 30), BG, a * ease((t - 0.5 - k * 0.15) / 0.3)))
    return [(x0 + L * f, yc) for f in pos]

def sc_title(cv, t, p):
    a = ease(t / 1.2)
    if PORT: flute(cv, 90, 700, 900, 62, t + 2, 0.55 * a)
    else: flute(cv, 240, 520, 1440, 70, t + 2, 0.55 * a)
    title_block(cv, t, 'HISTORY', 3, 'The oldest', 'music', 'Part 1 · Flutes before writing')

def sc_hohle(cv, t, p):
    c1 = cue('s2', 2); c2 = cue('s2', 3); c3 = cue('s2', 4)
    if PORT: x0, yc, L, th = 80, 560, 880, 56
    else: x0, yc, L, th = 200, 310, 1300, 64
    hp = flute(cv, x0, yc, L, th, t)
    a1 = ease((t - c1) / 0.6)
    yy = yc + th / 2 + 50
    col = mix(AMBER, BG, a1)
    cv.line([(x0, yy), (x0 + L, yy)], col, 3); cv.line([(x0, yy - 12), (x0, yy + 12)], col, 3); cv.line([(x0 + L, yy - 12), (x0 + L, yy + 12)], col, 3)
    cv.text((x0 + L / 2, yy + 14), '21.8 cm preserved · about 8 mm wide', 'sansb', 34, AMBER, 'ma', a1)
    a2 = ease((t - c2) / 0.6)
    cv.text((hp[2][0], yc - th / 2 - 62), 'five finger holes', 'sansb', 34, TXT, 'ma', a2)
    arrow(cv, (hp[2][0], yc - th / 2 - 18), (hp[2][0], yc - th * 0.28), AMBER, 3, 12, a2)
    a3 = ease((t - c2 - 1.6) / 0.6)
    cv.text((x0 + 10, yc - th / 2 - (62 if not PORT else 112)), 'two V-shaped notches', 'sansb', 34, TXT, 'la', a3)
    stat_cards(cv, t, [dict(num='Griffon vulture', label='wing bone (radius), Gyps fulvus', at=cue('s2', 2) - 1.5),
                       dict(num='12 pieces', label='found within a 10 × 20 cm patch, summer 2008', at=c3),
                       dict(num='Aurignacian', label='lowest layer: the oldest culture tied to modern humans in Europe', at=c3 + 1.0)],
               area=(CONT[0], yy + 90, CONT[2], CONT[3]))

def ago_timeline(cv, t, items, vmax=60000, area=None):
    x0, y0, x1, y1 = area or CONT
    bx0 = x0 + 40; bx1 = x1 - 40
    X = lambda ya: bx1 - (bx1 - bx0) * ya / vmax
    n = len(items); step = (y1 - y0 - 70) / max(n, 1)
    fs = 34 if not PORT else 32
    for i, it in enumerate(items):
        a = ease((t - it['at']) / 0.6)
        if a <= 0: continue
        y = y0 + i * step; col = it.get('col', AMBER)
        cv.text((bx0, y), it['label'], 'sansb', fs, TXT, 'la', a)
        if it.get('sub'):
            if PORT: cv.text((bx0, y + 38), it['sub'], 'sans', 28, DIM, 'la', a)
            else: cv.text((bx0 + font('sansb', fs).getlength(it['label']) / SS + 20, y + 4), it['sub'], 'sans', 28, DIM, 'la', a)
        a_, b_ = it['rng']
        u = ease((t - it['at'] - 0.2) / 0.9)
        xa, xb = X(b_), X(a_)
        xb = xa + (xb - xa) * u
        yb = y + (78 if PORT else 48)
        cv.rect((xa, yb, max(xa + 14, xb), yb + 24), mix(col, BG, a), 6)
        if it.get('open'): arrow(cv, (xa, yb + 12), (xa - 50, yb + 12), col, 5, 16, a)
        if it.get('tag'): badge(cv, min(xb + 20, bx1 - 190), yb - 10, it['tag'], RED, a, 22)
    ya = y1 - 40
    cv.line([(bx0, ya), (bx1, ya)], mix(STEEL, BG, 0.8), 3)
    for v in (60000, 40000, 20000, 0):
        cv.line([(X(v), ya - 8), (X(v), ya + 8)], mix(STEEL, BG, 0.8), 3)
        cv.text((X(v), ya + 14), 'today' if v == 0 else f'{v:,}', 'sans', 26, DIM, 'ma')
    cv.text((bx0 - 10, ya + 44), 'years ago', 'sans', 24, DIM, 'la')

def sc_age(cv, t, p):
    ago_timeline(cv, t, [
        dict(at=cue('s3', 1), label='Hohle Fels flute', sub='older than 35,000 calendar years (Nature, 2009)', rng=(35000, 41000), open=True),
        dict(at=cue('s3', 2), label='Geissenklösterle layers', sub='flutes of swan bone and mammoth ivory', rng=(42000, 43000), col=TEAL),
    ], area=(CONT[0], CONT[1] + 20, CONT[2], CONT[3] - 130 if not PORT else CONT[1] + 520))
    note(cv, t, cue('s3', 3), 'Dated: animal bones in the same layers. Not dated directly: the flutes.', y=CONT[3] - 75 if not PORT else CONT[1] + 640, col=AMBER, size=34)

def sc_ivory(cv, t, p):
    c = cue('s4', 1)
    stat_cards(cv, t, [
        dict(num='1', label='Shape a curved piece of tusk', at=c),
        dict(num='2', label='Split it in two, along the layers', at=c + 1.5),
        dict(num='3', label='Hollow both halves, carve the holes', at=c + 3.0),
        dict(num='4', label='Join the halves, sealed airtight', at=c + 4.5)])

def sc_divje(cv, t, p):
    stat_cards(cv, t, [
        dict(num='1995', label='Cave bear thighbone with holes, Divje Babe, Slovenia', sub='about 11 cm; estimated 50,000–60,000 years old', at=cue('s5', 1)),
        dict(num='Flute?', label='Neanderthals made the holes', sub='Turk and colleagues; Slovenian National Museum', col=TEAL, at=cue('s5', 2)),
        dict(num='Chewed?', label='Animals made the holes', sub="d'Errico; Chase & Nowell; Diedrich", col=RED, at=cue('s5', 3))],
        area=(CONT[0], CONT[1], CONT[2], CONT[3] - 110))
    a = ease((t - cue('s5', 3) - 0.8) / 0.6)
    if a > 0: badge(cv, W / 2, CONT[3] - 90, 'DISPUTED: not settled', RED, a, 40, 'm')

def two_cols(cv, t, left, right, ta, tb):
    gap = 30
    if PORT: boxes = [(CONT[0], CONT[1], CONT[2], CONT[1] + 420), (CONT[0], CONT[1] + 450, CONT[2], CONT[1] + 900)]
    else:
        w = (CONT[2] - CONT[0] - gap) / 2
        boxes = [(CONT[0], CONT[1], CONT[0] + w, CONT[3] - 70), (CONT[0] + w + gap, CONT[1], CONT[2], CONT[3] - 70)]
    for bx, (title, col, lines), t0 in zip(boxes, (left, right), (ta, tb)):
        a = ease((t - t0) / 0.6)
        if a <= 0: continue
        cv.rect(bx, mix(CARD, BG, a), 20); cv.outline(bx, mix(col, BG, 0.5 * a), 3, 20)
        cv.text((bx[0] + 36, bx[1] + 26), title, 'serif', 52, col, 'la', a)
        y = bx[1] + 110
        for k, l in enumerate(lines):
            aa = ease((t - t0 - 0.5 - k * 0.5) / 0.6)
            y = cv.para(bx[0] + 36, y, '• ' + l, 'sans', 40 if not PORT else 36, TXT, bx[2] - bx[0] - 72, 1.2, 'l', aa) + 14

def sc_sound(cv, t, p):
    two_cols(cv, t, ('We can know', TEAL, ['How many holes, and where they are', 'That replicas play several different notes', 'That the maker planned the tool']),
             ('We cannot know', RED, ['What scale, if any, was used', 'Any tune or rhythm', 'Whether it joined voices, dance or ritual', 'Whether singing came first']),
             cue('s6', 1), cue('s6', 3))
    note(cv, t, cue('s6', 5), 'Complete, testable flutes: Jiahu, China, crane bone, 5–8 holes, c. 7000–5700 BC', y=CONT[3] - 50 if not PORT else CONT[1] + 950, size=30)

def sc_before(cv, t, p):
    c3 = cue('s7', 3)
    if t < c3 - 0.2:
        ago_timeline(cv, t, [
            dict(at=cue('s7', 0), label='Writing (Uruk)', sub='about 5,300 years ago', rng=(0, 5300), col=BLUE),
            dict(at=cue('s7', 1), label='Hohle Fels flute', sub='older than 35,000', rng=(35000, 41000), open=True),
            dict(at=cue('s7', 1) + 0.8, label='Geissenklösterle layers', sub='42,000–43,000', rng=(42000, 43000), col=TEAL),
            dict(at=cue('s7', 1) + 1.6, label='Divje Babe bone', sub='est. 50,000–60,000', rng=(50000, 60000), col=RED, tag='DISPUTED'),
        ])
    else:
        stat_cards(cv, t, [dict(num='315', label='societies studied (Mehr et al., 2019)', sub='song found in every one', at=c3),
                           dict(num='4', label='common settings: lullabies, dance, healing, love', sub='shows what music does now, not why it began', col=TEAL, at=c3 + 1.5)],
                   area=(CONT[0], CONT[1], CONT[2], CONT[3] - (0 if not PORT else 300)))

def sc_lesson(cv, t, p):
    statements(cv, t, [(cue('s8', 0), 'The oldest music we can prove:', DIM, 'serifr'), (cue('s8', 0) + 1.3, 'a vulture-bone flute.', AMBER, 'serif'),
                       (cue('s8', 1), 'The oldest music is unknown.', TXT, 'serif')])

def sc_end(cv, t, p):
    end_block(cv, t, 'History', 3, ['Univ. Tübingen press release, 24 June 2009 · Conard, Malina & Münzel, Nature 460 (2009)',
        'Higham et al., J. Human Evolution 62 (2012) · Turk et al.; d’Errico et al. (1998); Chase & Nowell (1998) on Divje Babe',
        'Zhang et al., Nature 401 (1999), Jiahu · Mehr et al., Science 366 (2019) · Met Museum on early writing'])

SUBS = {
 's1': ['What is the oldest music we can prove?'],
 's2': ['In caves of the Swabian Jura, in southern Germany, archaeologists found flutes.', 'The best preserved came from Hohle Fels, in summer 2008.', 'It was made from the wing bone of a griffon vulture.', '21.8 centimeters survive, with five finger holes and two V-shaped notches at one end.', 'It was found in twelve pieces.'],
 's3': ['How old is it?', 'The Nature paper said older than 35,000 calendar years.', 'Nearby, at Geissenklösterle cave, there are flutes of swan bone and mammoth ivory. Animal bones in the same layers date to about 42,000 to 43,000 years ago.', 'Note that: the layers were dated, not the flutes themselves.'],
 's4': ['An ivory flute is hard to make.', 'The maker split a curved piece of tusk in two, hollowed both halves, carved the holes, and joined the halves airtight.', 'So these were made with skill, and with a plan.'],
 's5': ['Now the disputed one.', 'In Slovenia, in 1995, a cave bear thighbone with holes was found at Divje Babe. It is estimated at 50 to 60 thousand years old, from Neanderthal times.', 'Its discoverers say Neanderthals made it.', 'Other scientists say hyenas or other animals chewed those holes. This is not settled.'],
 's6': ['What did it sound like? We do not know.', 'The Hohle Fels flute has a broken end, so some length is missing.', 'Modern replicas can play several notes.', 'But that shows what the tube can do, not what anyone played.', 'No tune survives, and no rhythm.', 'Complete flutes that we can test are younger: bird bone flutes from Jiahu in China, with five to eight holes, from about 7000 BC.'],
 's7': ['Writing appears about 5,300 years ago.', 'These flutes are at least 30,000 years older.', 'Why did people make music first? That is open.', 'A 2019 study of 315 societies found song in every one, tied to lullabies, dance, healing and love.', 'That shows what music does today. It does not show why it began.', 'And voices leave no bones. Singing may be far older.'],
 's8': ['So the oldest music we can prove is a vulture bone flute.', 'The oldest music is unknown.'],
 's9': [],
}
SRC2 = 'Sources: Univ. Tübingen press release (24 June 2009); Conard, Malina & Münzel, Nature 460 (2009). Hole spacing is drawn schematically.'
SCENES = [
 ('s1', '', '', sc_title),
 ('s2', 'Hohle Fels, Germany', SRC2, sc_hohle),
 ('s3', 'How old?', 'Sources: Conard et al. (2009); Higham et al., J. Human Evolution 62 (2012). Calendar years; Higham dated animal bones in the flute layers.', sc_age),
 ('s4', 'Ivory takes planning', 'Source: Univ. Tübingen press release (2009), describing how ivory flutes were made.', sc_ivory),
 ('s5', 'The disputed one', 'Sources: Turk et al.; d’Errico et al. (1998); Chase & Nowell (1998); Diedrich (2015). Age: ESR estimate; first radiocarbon date was revised.', sc_divje),
 ('s6', 'What it sounded like', 'Sources: Tübingen 2009 (broken end); Zhang et al., Nature 401 (1999), Jiahu. Replicas are reconstructions.', sc_sound),
 ('s7', 'Before writing', 'Sources: Mehr et al., Science 366 (2019); Met Museum (writing c. 3300 BC); Conard 2009; Higham 2012.', sc_before),
 ('s8', '', '', sc_lesson),
 ('s9', '', '', sc_end),
]
configure(SUBS, SCENES)
if __name__ == '__main__': main()
