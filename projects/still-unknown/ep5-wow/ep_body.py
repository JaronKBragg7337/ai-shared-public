# Still Unknown ep 5 body: "72 seconds from somewhere" (the 1977 Wow! signal). Scenes + sources; framework in su_kit_a/b.
EP = 5

def art_transit(cv, t, R, sid):
    x0, y0, x1, y1 = R; a = ease(t / 1.0)
    cx = (x0 + x1) / 2; sy = y0 + 110 if L else y0 + 50
    # sky strip drifting past a fixed beam
    hh = 70 if L else 40
    cv.rect((x0, sy - hh, x1, sy + hh), mix(INK, BG, a * 0.9))
    rr = random.Random(5)
    ph = (t * 0.09) % 1.0
    for i in range(40):
        sx = x0 + ((rr.random() - ph * 1.0) % 1.0) * (x1 - x0); syy = sy - 60 + rr.random() * 120
        cv.circ((sx, syy), 1.8, mix(TXT, BG, a * 0.6))
    src = x0 + (1.0 - ((t * 0.09) % 1.0)) * (x1 - x0) * 0.0 + (x1 - x0) * (1.0 - ph)
    cv.circ((src, sy), 8, mix(ROSE, BG, a)); cv.ring((src, sy), 14, mix(ROSE, BG, a * 0.5), 2)
    bw = 120 if L else 100
    cv.outline((cx - bw / 2, sy - hh, cx + bw / 2, sy + hh), mix(CYAN, BG, a), 3)
    cv.text((cx, sy - hh - 12), 'fixed beam', 'mono', 18, CYAN, 'ms', a)
    cv.text((x0 + 8, sy + hh + 8), 'the Earth turns; the sky drifts through the beam', 'mono', 18, DIM, 'la', a)
    # intensity as the source crosses
    cy0 = y0 + (360 if L else 215); ch = 150 if L else 65
    cv.line([(x0, cy0), (x1, cy0)], mix(DIM2, BG, a), 2)
    pts = []
    for i in range(101):
        u = i / 100.0; px = x0 + u * (x1 - x0); pts.append((px, cy0 - ch * math.exp(-((u - 0.5) / 0.17) ** 2)))
    cu = (cx + (x1 - x0) / 2 - src) / (x1 - x0) if False else 0
    prog = clamp01(((x1 - src) / (x1 - x0)))
    n = max(2, int(101 * prog))
    cv.line(pts[:n], mix(MINT, BG, a), 4)
    mono(cv, x0, cy0 + 14, '0 s', 18, DIM, a); mono(cv, x1, cy0 + 14, '72 s', 18, DIM, a, 'ra'); mono(cv, cx, cy0 + 14, 'time in view', 18, DIM, a, 'ma')
    mono(cv, x0, cy0 + 44, 'SCHEMATIC, not the real data', 17, DIM, a)

def art_printout(cv, t, R, sid):
    x0, y0, x1, y1 = R; a = ease(t / 1.0)
    chars = [('6', 6), ('E', 14), ('Q', 26), ('U', 30), ('J', 19), ('5', 5)]
    cw = (x1 - x0) / 6.0; base = y0 + (330 if L else 270); hmax = 230 if L else 170
    mono(cv, x0, y0 - 4, 'EHMAN\'S PRINTOUT CODE', 20, CYAN, a)
    for i, (c, v) in enumerate(chars):
        u = ap(t, sid, 0.1 + 0.07 * i, 0.9)
        cx = x0 + cw * (i + 0.5)
        cv.text((cx, y0 + (40 if L else 26)), c, 'monob', 70 if L else 44, TXT if c != 'U' else ROSE, 'ma', u)
        hh = hmax * v / 30.0 * u
        cv.rect((cx - cw * 0.3, base - hh, cx + cw * 0.3, base), mix(ROSE if c == 'U' else CYAN, BG, a * 0.85))
        cv.text((cx, base + 10), str(v), 'mono', 22, DIM, 'ma', u)
    mono(cv, x0, base + 44, 'scale: multiples of the background noise (E = 14, Q = 26, U = 30)', 18, DIM, a)

def art_freq(cv, t, R, sid):
    x0, y0, x1, y1 = R; a = ease(t / 1.0)
    f0, f1 = 1420.30, 1420.80
    ax0, ax1 = x0 + 30, x1 - 30; ay = y0 + (150 if L else 150)
    def X(f): return ax0 + (f - f0) / (f1 - f0) * (ax1 - ax0)
    cv.line([(ax0, ay), (ax1, ay)], mix(DIM2, BG, a), 3)
    for f in (1420.3, 1420.4, 1420.5, 1420.6, 1420.7, 1420.8):
        cv.line([(X(f), ay - 7), (X(f), ay + 7)], mix(DIM, BG, a), 2); cv.text((X(f), ay + 12), f'{f:.1f}', 'mono', 18, DIM, 'ma', a)
    cv.text((ax1, ay + 40), 'MHz', 'mono', 18, DIM, 'ra', a)
    items = [(1420.4058, 'hydrogen line', MINT, 0.05, -30), (1420.4556, '1977 estimate', CYAN, 0.3, -66)]
    if sid == 's11': items.append((1420.726, '2025 preprint', VIO, 0.35, -30))
    for f, nm, col, fr, dy in items:
        u = ap(t, sid, fr, 0.9)
        cv.line([(X(f), ay), (X(f), ay + dy)], mix(col, BG, u), 4); cv.circ((X(f), ay), 7, mix(col, BG, u))
        right = f > 1420.42 and f < 1420.6
        cv.text((X(f) + (10 if right else -10), ay + dy - 28), nm, 'monob', 20, col, 'la' if right else 'ra', u)
    mono(cv, ax0, ay + 70, 'one channel = 10 kHz wide (0.010 MHz)', 18, DIM, a)

def art_horns(cv, t, R, sid):
    x0, y0, x1, y1 = R; a = ease(t / 1.0)
    lx = x0 + 150; lw = x1 - lx - 20
    for k, (nm, yy) in enumerate((('horn A', y0 + 40), ('horn B', y0 + 150))):
        mono(cv, x0, yy + 30, nm, 22, TXT, a)
        cv.line([(lx, yy + 90), (lx + lw, yy + 90)], mix(DIM2, BG, a), 2)
    # observed bump in one horn, expected bump (dashed) in the other
    pts = [(lx + lw * (0.15 + 0.3 * i / 60), y0 + 130 - 80 * math.exp(-((i / 60 - 0.5) / 0.17) ** 2)) for i in range(61)]
    n = max(2, int(61 * ap(t, sid, 0.3, 1.5)))
    cv.line(pts[:n], mix(MINT, BG, a), 4)
    ex = [(lx + lw * (0.55 + 0.3 * i / 60), y0 + 240 - 80 * math.exp(-((i / 60 - 0.5) / 0.17) ** 2)) for i in range(61)]
    ua = ap(t, sid, 0.65, 1.2)
    for i in range(0, 60, 4): cv.line(ex[i:i + 2], mix(ROSE, BG, ua * 0.9), 3)
    cv.text((lx + lw * 0.2, y0 + 70), 'seen', 'monob', 22, MINT, 'la', ap(t, sid, 0.4))
    cv.text((lx + lw * 0.6, y0 + 175), 'expected, not seen', 'monob', 22, ROSE, 'la', ua)
    mono(cv, x0, y0 + 280, 'SCHEMATIC: a steady source should cross both horns', 17, DIM, a)

SC = {}
SC['s1'] = S_title('s1', 5, ('72 seconds', 'from somewhere'), ('72 seconds', 'from', 'somewhere'), 'The 1977 Wow! signal, Big Ear radio telescope, Ohio State',
                   (('DOCUMENTED', MINT, 0.3), ('PROPOSED', VIO, 0.5), ('DISPUTED', ROSE, 0.7), ('UNKNOWN', ROSE, 0.88)), art_transit)
SC['s2'] = S_rows('s2', [('DOCUMENTED', MINT, None)], [
    ('DOCUMENTED', MINT, 'Big Ear, Ohio State University, Delaware, Ohio. A fixed design: tilts in altitude, cannot follow a star.', 0.12),
    ('DOCUMENTED', MINT, 'The Earth\'s rotation carries the sky through the view. Any point takes 72 seconds to cross.', 0.45),
    ('NOTE', CYAN, '72 s is the time a steady source stays in view, not a measured lifetime of a transmitter.', 0.75)], art_transit)
SC['s3'] = S_rows('s3', [('DOCUMENTED', MINT, None), ('NOT A MESSAGE', ROSE, 0.55)], [
    ('DOCUMENTED', MINT, 'Printout numbers = signal strength in multiples of the background noise: 1 to 9, then letters.', 0.1),
    ('DOCUMENTED', MINT, 'The code read 6 E Q U J 5: rose to a peak at U (about 30 on that scale), then fell.', 0.38),
    ('REPORTED', CYAN, 'A smooth rise and fall, as a steady source drifting through the beam would give.', 0.7)], art_printout)
SC['s4'] = S_rows('s4', [('DOCUMENTED', MINT, None), ('FIRST ESTIMATE', CYAN, 0.7)], [
    ('MEASURED', MINT, 'Narrow: inside one 10 kHz channel.', 0.1),
    ('MEASURED', MINT, 'Very near 1420 MHz, the radio frequency of neutral hydrogen. Radio rules reserve this band for astronomy; interference cannot be ruled out entirely.', 0.3),
    ('REPORTED', CYAN, 'First published estimate: 1420.4556 MHz. It is revised in 2025.', 0.72)], art_freq)
SC['s5'] = S_rows('s5', [('DOCUMENTED', MINT, None), ('NOT SETTLED', ROSE, 0.6)], [
    ('DOCUMENTED', MINT, 'Sagittarius, a few degrees from Chi Sagittarii. Two feed horns feeding one switched receiver.', 0.1),
    ('DOCUMENTED', MINT, 'It appeared in one horn, not the other. The records did not preserve which: two possible positions.', 0.4),
    ('PUZZLE', ROSE, 'A source that kept shining at the same strength should have shown up in both.', 0.72)], art_horns)
SC['s6'] = S_table('s6', [('DOCUMENTED', MINT, None), ('NO REPEAT FOUND', ROSE, 0.2)], [
    ('1977-78', 'Ehman and the Big Ear team, following months', MINT, 0.08, 'NOTHING', ROSE),
    ('1987, 1989', 'Robert Gray, META array', MINT, 0.22, 'NOTHING', ROSE),
    ('mid 1990s', 'Gray, Very Large Array: more sensitive than Big Ear', MINT, 0.38, 'NOTHING', ROSE),
    ('1998-99', 'Gray and Ellingsen: six long sessions on another dish', MINT, 0.55, 'NOTHING SIMILAR', ROSE),
    ('2022', 'Breakthrough Listen: that region searched', MINT, 0.76, 'NO CANDIDATES', ROSE)])
SC['s7'] = S_rows('s7', [('PROPOSED', VIO, None)], [
    ('NEAR EARTH', CYAN, 'Ehman suggested space debris in 1994; he later judged that much less likely. No specific terrestrial source has been shown.', 0.12),
    ('NATURAL, DISTANT', VIO, 'A natural source far away. Several versions proposed (next scenes).', 0.45),
    ('A TRANSMISSION', ROSE, 'Some have proposed another civilization. The evidence for it is the signal itself, and nothing else.', 0.68)])
SC['s8'] = S_rows('s8', [('PROPOSED', VIO, None), ('PAPERS: 2017', CYAN, 0.5)], [
    ('PARIS, 2017', VIO, 'Hydrogen cloud around a comet. Antonio Paris, then at St. Petersburg College, Florida.', 0.1),
    ('PARIS, 2017', VIO, 'Comets 266P/Christensen and 335P/Gibbs, which he said were in that part of the sky in 1977.', 0.4),
    ('REPORTED', CYAN, 'He reported a signal near the hydrogen frequency while observing 266P in 2017.', 0.72)])
SC['s9'] = S_rows('s9', [('DISPUTED', ROSE, None)], [
    ('OBJECTION', ROSE, 'Critics, including people from the original Big Ear team: the comets were not in the beam at the right time.', 0.1),
    ('OBJECTION', ROSE, 'Comet hydrogen is not known to give a signal that narrow and that strong.', 0.4),
    ('OBJECTION', ROSE, 'It does not explain why only one horn saw it.', 0.62),
    ('STATUS', CYAN, 'A proposal, not a finding.', 0.82)])
SC['s10'] = S_rows('s10', [('NEWER WORK', CYAN, None)], [
    ('CALEBALLERO 2022'.replace('CALEBALLERO', 'CABALLERO'), CYAN, 'Three Sun-like stars inside the possible patch, the best known about 1,800 light years away: places worth a look. A candidate star is not evidence of a transmitter.', 0.1),
    ('MENDEZ ET AL., 2024', VIO, 'Hypothesis: a natural flare, such as a magnetar, lights a cold hydrogen cloud into a narrow beam: a natural maser. Using Arecibo. No flare tied to 1977.', 0.55)])
SC['s11'] = S_rows('s11', [('PREPRINT 2025', VIO, None), ('NOT PEER REVIEWED, OCT 2026', ROSE, 0.3)], [
    ('ARCHIVE', CYAN, '75,000+ pages of old records digitized. Found a clock offset and an inverted channel order in the 1977 analysis.', 0.08),
    ('REVISED', VIO, 'Frequency 1420.726 MHz (was 1420.4556). Peak more than 250 Jy, higher than earlier estimates.', 0.4),
    ('THEIR CONCLUSION', CYAN, 'A natural hydrogen source most likely. Their results do not show an extraterrestrial signal.', 0.7)], art_freq)
SC['s12'] = S_rows('s12', [('DISPUTED', ROSE, None)], [
    ('CAUTION', ROSE, 'Gerry Harp, who worked on the Allen Telescope Array: the signal failed even simple tests used to exclude interference.', 0.12),
    ('CAUTION', ROSE, 'Others: failing to repeat shows the event was rare, not what caused it.', 0.45),
    ('STATUS', CYAN, 'One event, no repeat: every explanation is a hypothesis.', 0.72)])
SC['s13'] = S_rows('s13', [('WHAT WOULD SETTLE IT', MINT, None)], [
    ('1', MINT, 'A repeat from the same patch of sky.', 0.12),
    ('2', MINT, 'Independent checks of the 1977 numbers by teams other than the one that reanalyzed them.', 0.35),
    ('3', MINT, 'Searching the Ohio archive (40,000+ narrowband events logged) for other one-off signals like it. Most of it is unexplored.', 0.6)])
SC['s14'] = S_rows('s14', [('THE LEDGER', CYAN, None)], [
    ('DOCUMENTED', MINT, 'A narrow signal near the hydrogen frequency, over the 72 s a source takes to cross the view, peak about 30 on the printout scale.', 0.1),
    ('DOCUMENTED', MINT, 'Repeated searches found no repeat.', 0.3),
    ('DISPUTED', ROSE, 'The comet idea. The meaning of the reanalysis.', 0.42),
    ('PROPOSED', VIO, 'A natural flare from a hydrogen cloud.', 0.56),
    ('CLAIMED', VIO, 'A message from another civilization: no evidence beyond the signal itself.', 0.68),
    ('UNKNOWN', ROSE, 'What it was.', 0.85)], size=(32 if L else 28))
SC['s15'] = S_close('s15', 'not established.', 'not ruled out.', 'NOT ESTABLISHED', 'NOT RULED OUT', 'one signal, seen once. a natural source fits best to one group; others are not convinced. an artificial origin is neither shown nor excluded.')
SC['s16'] = sc_end

SOURCES = [
    'Wikipedia "Wow! signal" (read 2026-10-20). Ohio State Big Ear archive (bigear.org): J. Ehman on the 6EQUJ5 printout; R. Gray and S. Ellingsen, search paper (1998-99 sessions)',
    'A. Paris, arXiv:1706.03259 (observations of 266P) and arXiv:1706.04642 (comet proposal), 2017',
    'A. Caballero, International Journal of Astrobiology, 2022 (candidate stars). Breakthrough Listen 2022 search, as summarized in Wikipedia',
    'A. Mendez et al., arXiv:2408.08513 (2024, maser-flare hypothesis); "Arecibo Wow! II", arXiv:2508.10657 (2025 preprint, not peer reviewed when checked)',
    'A. Mendez, R. Dixon, R. Childers, "The Ohio SETI Program: the last decades", arXiv:2606.11102 (2026); G. Harp comment, centauri-dreams.org, 15 Apr 2025',
    'All pictures are schematic drawings made for this episode, not data plots. No photographs.']

SCENES = [
    ('s1', None, 'Wow! signal, 15 Aug 1977, Big Ear, Ohio State University', SC['s1']),
    ('s2', 'the telescope', 'Wikipedia "Wow! signal"; Ohio State Big Ear archive', SC['s2']),
    ('s3', 'six, e, q, u, j, five', 'J. Ehman\'s explanation of the printout, bigear.org', SC['s3']),
    ('s4', 'what was measured', 'Wikipedia "Wow! signal"; Ohio State Big Ear archive', SC['s4']),
    ('s5', 'where, and the puzzle', 'Gray and Ellingsen; Wikipedia "Wow! signal"', SC['s5']),
    ('s6', 'looking again', 'Gray and Ellingsen; Wikipedia "Wow! signal" (searches 1977 to 2022)', SC['s6']),
    ('s7', 'what could it be?', 'Ehman, as summarized in Wikipedia "Wow! signal"', SC['s7']),
    ('s8', 'the comet idea', 'A. Paris 2017, arXiv:1706.03259 and 1706.04642', SC['s8']),
    ('s9', 'why it was disputed', 'Wikipedia "Wow! signal" (critics, incl. Big Ear team members)', SC['s9']),
    ('s10', 'newer work', 'Caballero 2022; Mendez et al. 2024 (arXiv:2408.08513)', SC['s10']),
    ('s11', 'the 2025 reanalysis', 'Mendez et al., arXiv:2508.10657 (preprint)', SC['s11']),
    ('s12', 'caution', 'G. Harp via centauri-dreams.org, 2025', SC['s12']),
    ('s13', 'what would settle it', 'Mendez, Dixon, Childers, arXiv:2606.11102 (40,000+ events)', SC['s13']),
    ('s14', None, 'Status as of October 2026', SC['s14']),
    ('s15', None, None, SC['s15']),
    ('s16', None, None, SC['s16']),
]
