import sys; sys.path.insert(0, '../../tv-lib')
from tvlib import *

# simplified periodic-table silhouette (decorative): period -> list of group columns
def table_cells():
    cells = []
    for per in range(1, 8):
        if per == 1: cols = [1, 18]
        elif per in (2, 3): cols = [1, 2] + list(range(13, 19))
        else: cols = list(range(1, 19))
        for c in cols: cells.append((per, c))
    return cells

def sc_title(cv, t, p):
    a = ease(t / 1.2)
    if PORT: x0, y0, cs = 60, 560, 54
    else: x0, y0, cs = 380, 340, 62
    for per, c in table_cells():
        x = x0 + (c - 1) * cs; y = y0 + (per - 1) * cs
        col = (34, 48, 74);
        if (per, c) == (6, 11): col = AMBER
        if (per, c) == (6, 17): col = TEAL
        cv.rect((x + 2, y + 2, x + cs - 2, y + cs - 2), mix(col, BG, a * (0.9 if col != (34, 48, 74) else 0.8)), 4)
    if t > 1.4:
        aa = ease((t - 1.4) / 0.8)
        cv.text((x0 + 10 * cs + cs / 2, y0 + 5 * cs + cs + 10), 'Au gold', 'sansb', 28, AMBER, 'ma', aa)
        cv.text((x0 + 16 * cs + cs / 2, y0 + 5 * cs + cs + 40), 'At astatine', 'sansb', 28, TEAL, 'ma', aa)
    title_block(cv, t, 'SCIENCE', 3, 'The rarest', 'material?', 'Two ways to measure rarity')

def sc_abund(cv, t, p):
    x0, x1 = CONT[0] + 20, CONT[2] - 20
    y = CONT[1] + (60 if not PORT else 40); bh = 110
    segs = [('Hydrogen', 74, BLUE, cue('s2', 1)), ('Helium', 24, TEAL, cue('s2', 1) + 1.5), ('Everything else', 2, AMBER, cue('s2', 2))]
    cv.text((x0, y - 50), 'Ordinary matter, by mass', 'sansb', 36, DIM, 'la', ease(t / 0.6))
    xx = x0
    for nm, v, col, at in segs:
        a = ease((t - at) / 0.7)
        w = (x1 - x0) * v / 100.0
        if a > 0:
            cv.rect((xx, y, xx + w * a, y + bh), col, 6)
            if v > 5:
                cv.text((xx + w / 2, y + 12), f'{nm} ≈ {v}%', 'serif', 44 if not PORT else 36, BG, 'ma', a)
        xx += w
    a2 = ease((t - cue('s2', 2) - 0.3) / 0.7)
    if a2 > 0:
        cv.line([(x1 - 12, y + bh + 6), (x1 - 12, y + bh + 50)], mix(AMBER, BG, a2), 4)
        cv.text((x1, y + bh + 56), 'everything heavier: ≈ 2%', 'serif', 52, AMBER, 'ra', a2)
        cv.text((x1, y + bh + 126), 'carbon, oxygen, iron, gold ...', 'sans', 34, DIM, 'ra', a2)
    stat_cards(cv, t, [dict(num='≈ 5%', label='ordinary matter: share of the universe’s energy', sub='dark matter ≈ 27%, dark energy ≈ 68%', col=BLUE, at=cue('s2', 3))],
               area=(CONT[0] + (0 if PORT else 560), CONT[1] + (290 if not PORT else 330), CONT[2] - (0 if PORT else 560), CONT[3] - (0 if not PORT else 20)))

def sc_origins(cv, t, p):
    stat_cards(cv, t, [
        dict(num='Big Bang', label='hydrogen, helium, a little lithium', at=cue('s3', 1)),
        dict(num='Stars', label='fusion builds elements up to iron', col=TEAL, at=cue('s3', 2)),
        dict(num='Beyond iron', label='slow capture in aging stars; rapid capture in violent events', col=BLUE, at=cue('s3', 3)),
        dict(num='Mergers', label='2017: a merger shows heavy elements being made', sub=None if PORT else 'magnetar flares: up to ~10%? (2025)', col=AMBER, tag='SHARE STILL OPEN', at=cue('s3', 4))], area=(CONT[0], CONT[1], CONT[2], CONT[3] + (60 if PORT else 0)))

def sc_crust(cv, t, p):
    stat_cards(cv, t, [
        dict(num='≈ 4 ppb', label='gold in Earth’s crust', sub='estimates range 1–6 ppb (by mass)', at=cue('s4', 0) + 0.6),
        dict(num='≈ 5 ppb', label='platinum in Earth’s crust', col=TEAL, at=cue('s4', 0) + 2.5),
        dict(num='< 1 g to 28 g', label='astatine in the whole crust', sub='longest-lived form: half-life 8.1 hours', col=AMBER, tag='ESTIMATES DIFFER', at=cue('s4', 1))])

def sc_life(cv, t, p):
    stat_cards(cv, t, [
        dict(num='Wood', label='cellulose and lignin, made by land plants', at=cue('s5', 2)),
        dict(num='Limestone', label='much of it built from shells of living things', col=TEAL, at=cue('s5', 3)),
        dict(num='Coal', label='fossil plants', col=BLUE, at=cue('s5', 4)),
        dict(num='Only Earth', label='as far as we know', col=AMBER, tag='SO FAR', at=cue('s5', 5))])

def sc_wood(cv, t, p):
    x0, x1 = CONT[0] + 40, CONT[2] - 40
    y = CONT[1] + (150 if not PORT else 120); bh = 90
    a = ease(t / 0.7)
    split = x0 + (x1 - x0) * (1 - 386 / 4540.0)
    cv.rect((x0, y, split, y + bh), mix(STEEL, BG, 0.7 * a), 6)
    u = ease((t - cue('s6', 1)) / 1.0)
    cv.rect((split, y, split + (x1 - split) * u, y + bh), mix(AMBER, BG, 1.0), 6)
    cv.text((x0, y - 84), 'Earth forms', 'sansb', 36, TXT, 'la', a)
    cv.text((x0, y - 44), '4.54 billion years ago', 'sans', 30, DIM, 'la', a)
    cv.text((x1, y - 84), 'today', 'sansb', 36, TXT, 'ra', a)
    a2 = ease((t - cue('s6', 1)) / 0.8)
    if a2 > 0:
        cv.line([(split, y + bh), (split, y + bh + 70)], mix(AMBER, BG, a2), 4)
        cv.text((split - 20, y + bh + 80), 'oldest known forest', 'sansb', 38, AMBER, 'ra', a2)
        cv.text((split - 20, y + bh + 128), '≈ 386 million years ago (Cairo, New York)', 'sans', 32, DIM, 'ra', a2)
    a3 = ease((t - cue('s6', 2)) / 0.8)
    if a3 > 0:
        cv.text((W / 2, y + bh + (230 if not PORT else 300)), 'Wood has existed for about 8% of Earth’s history.', 'serif', 52 if not PORT else 44, TXT, 'ma', a3)
        cv.text((W / 2, y + bh + (310 if not PORT else 440)), 'Before land plants grew tall: none.', 'serifr', 44 if not PORT else 40, DIM, 'ma', a3)

def sc_explored(cv, t, p):
    stat_cards(cv, t, [
        dict(num='One', label='planet we know in detail: Earth', sub='a few other worlds sampled by spacecraft', at=cue('s7', 1)),
        dict(num='6,000+', label='confirmed planets around other stars', sub='NASA, Sept 2025; surface chemistry mostly unknown', col=TEAL, at=cue('s7', 2)),
        dict(num='Not found', label='wood, or anything like it, elsewhere', sub='so far; a fact about our sample, not a law', col=AMBER, tag='NOT ESTABLISHED', at=cue('s7', 4))])

def sc_lesson(cv, t, p):
    statements(cv, t, [(cue('s8', 1), 'Rare by abundance: astatine, in Earth’s crust.', AMBER, 'serifr'),
                       (cue('s8', 2), 'Rare by place: materials that need life, so far.', TEAL, 'serifr'),
                       (cue('s8', 3), 'Rarity depends on how you ask.', TXT, 'serif')])

def sc_end(cv, t, p):
    end_block(cv, t, 'Science', 3, ['Milky Way / universe composition: Wikipedia, Abundance of the chemical elements · NASA / Planck (5%, 27%, 68%)',
        'Crust: CRC-based tables, USGS (gold 1–6 ppb) · Astatine: standard references (<1 g to ~28 g) · Pian et al., Nature (2017)',
        'Patel et al., ApJL 984 (2025) magnetar flare · Stein et al., Nature (2007) and Current Biology (2019) · NASA Exoplanet Archive (2025)'])

SUBS = {
 's1': ['What is the rarest material in the universe?'],
 's2': ['It depends how you measure rarity. First, by abundance.', 'About three quarters of ordinary matter is hydrogen, and about a quarter is helium.', 'Everything heavier adds up to roughly 2 percent.', 'And ordinary matter itself is only about 5 percent of the universe’s energy content.'],
 's3': ['Where do the heavy elements come from?', 'The Big Bang made hydrogen and helium.', 'Stars fuse elements up to iron.', 'Beyond iron, some form slowly in aging stars, and others in violent events.', 'In 2017, astronomers watched two neutron stars merge, and saw signs of heavy elements being made.', 'How much of our gold came from mergers is still being worked out. A 2025 study says giant magnetar flares may add up to a tenth.'],
 's4': ['In Earth’s crust, gold is about 4 parts per billion, and platinum about 5.', 'The rarest natural element there is astatine.', 'Estimates run from under one gram to about 28 grams in the whole crust, because even its longest-lived form lasts only about 8 hours.'],
 's5': ['Now measure a different way: by where a material occurs.', 'Some materials need life.', 'Wood is cellulose and lignin, made by land plants.', 'Much limestone is made from the shells of living things.', 'Coal is fossil plants.', 'As far as we know, all of these exist on one planet only: Earth.'],
 's6': ['Take wood.', 'The oldest known forests are about 386 million years old, found in New York.', 'Before land plants grew tall, there was no wood.'],
 's7': ['But we have looked at very little.', 'Spacecraft have visited a handful of worlds.', 'NASA has confirmed more than 6,000 planets around other stars, and we know almost nothing about their surfaces.', 'So wood is rare in the only place we have looked closely.', 'That tells us about our sample. It is not a law of nature.'],
 's8': ['So what is rarest?', 'By abundance, astatine in Earth’s crust.', 'By place, materials that need life, so far.', 'Rarity depends on how you ask.'],
 's9': [],
}
SCENES = [
 ('s1', '', '', sc_title),
 ('s2', 'Rarity by abundance', 'Sources: Wikipedia, Abundance of the chemical elements (H 74%, He 24%, rest about 2%); NASA / Planck (4.9%, 26.8%, 68.3%). Model-dependent.', sc_abund),
 ('s3', 'Where heavy elements come from', 'Sources: Pian et al., Nature (2017), GW170817; Patel et al., ApJL (2025). How much gold each source makes is open.', sc_origins),
 ('s4', 'Rarity in Earth’s crust', 'Sources: CRC-based tables; USGS circulars (gold 1–6 ppb); astatine estimates from standard references, which differ.', sc_crust),
 ('s5', 'Rarity by where it occurs', 'Sources: standard geology and botany references. “Only Earth” means none found elsewhere so far.', sc_life),
 ('s6', 'The oldest known forests', 'Sources: Stein et al., Nature (2007), Gilboa; Current Biology (2019), Cairo, New York; Earth age 4.54 billion years. Our arithmetic: 386 / 4,540 ≈ 8%.', sc_wood),
 ('s7', 'How little we have explored', 'Sources: NASA Exoplanet Archive (6,000th confirmed planet, Sept 2025). Absence so far is not proof of absence.', sc_explored),
 ('s8', '', '', sc_lesson),
 ('s9', '', '', sc_end),
]
configure(SUBS, SCENES)
if __name__ == '__main__': main()
