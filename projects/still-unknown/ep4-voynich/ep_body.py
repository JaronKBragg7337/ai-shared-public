# Still Unknown ep 4 body: "The book nobody can read" (Voynich MS 408). Scenes + sources; framework in su_kit_a/b.
EP = 4
RG = random.Random(408)

def marks(cv, x, y, w, a, col=DIM, size=14, seed=0):
    """a line of invented marks (NOT the real script): short strokes and loops."""
    r = random.Random(seed); xx = x
    while xx < x + w - size:
        k = r.randint(0, 3)
        if k == 0: cv.line([(xx, y + size), (xx, y)], mix(col, BG, a), 2)
        elif k == 1: cv.ring((xx + size * 0.4, y + size * 0.5), size * 0.4, mix(col, BG, a), 2)
        elif k == 2: cv.line([(xx, y + size), (xx + size * 0.5, y), (xx + size, y + size)], mix(col, BG, a), 2)
        else: cv.line([(xx, y + size * 0.5), (xx + size * 0.8, y + size * 0.5), (xx + size * 0.4, y + size)], mix(col, BG, a), 2)
        xx += size * (1.1 + r.random() * 0.8) + (size * 0.8 if r.random() < 0.18 else 0)

def art_pages(cv, t, R, sid):
    x0, y0, x1, y1 = R; a = ease(t / 1.4)
    pw = (x1 - x0 - 30) / 2; ph = min(y1 - y0 - 40, pw * 1.35)
    for k in range(2):
        px = x0 + k * (pw + 30); py = y0 + 10
        rrect(cv, (px, py, px + pw, py + ph), INK, DIM2, a)
        if k == 0:   # a plant drawn simply, and text lines
            cx = px + pw / 2
            cv.line([(cx, py + ph * 0.52), (cx + 6, py + ph * 0.34), (cx - 4, py + ph * 0.16)], mix(MINT, BG, a * 0.8), 3)
            for j, (dx, dy) in enumerate(((-34, 0.44), (30, 0.38), (-30, 0.30), (28, 0.24), (-24, 0.18))):
                cv.line([(cx, py + ph * dy + 14), (cx + dx, py + ph * dy - 10)], mix(MINT, BG, a * 0.8), 3)
            for r in range(6): marks(cv, px + 16, py + ph * 0.62 + r * 24, pw - 32, a * 0.8, DIM, 13, r)
        else:        # a chart of rings and text
            cx, cy = px + pw / 2, py + ph * 0.3
            for rr in (22, 44, 66): cv.ring((cx, cy), rr, mix(VIO, BG, a * 0.8), 2)
            for q in range(8): cv.circ((cx + 66 * math.cos(q * 0.785), cy + 66 * math.sin(q * 0.785)), 4, mix(CYAN, BG, a))
            for r in range(6): marks(cv, px + 16, py + ph * 0.62 + r * 24, pw - 32, a * 0.8, DIM, 13, r + 20)
    mono(cv, x0, y0 + ph + 22, 'ILLUSTRATION: invented marks and simple drawings, not the real pages', 17, DIM, a)

def art_book(cv, t, R, sid):
    x0, y0, x1, y1 = R; a = ease(t / 1.0)
    bw, bh = 300, 400
    bx = (x0 + x1) / 2 - bw / 2 if L else x0 + 40; by = y0 + 30 if L else y0 + 5
    if not L: bw, bh = 200, 270
    rrect(cv, (bx, by, bx + bw, by + bh), INK2, VIO, a, 3)
    cv.rect((bx, by, bx + 18, by + bh), mix(VIO, BG, a * 0.8))
    cv.text((bx + bw / 2 + 8, by + bh * 0.4), 'MS 408', 'monob', 34 if L else 26, TXT, 'mm', a)
    cv.text((bx + bw / 2 + 8, by + bh * 0.4 + 44), 'Beinecke Library', 'mono', 20 if L else 16, DIM, 'mm', a)
    cv.text((bx + bw / 2 + 8, by + bh * 0.4 + 70), 'Yale', 'mono', 20 if L else 16, DIM, 'mm', a)
    mono(cv, bx + (bw + 30 if not L else -20), by + (bh + 20 if L else 60), 'schematic book, not to scale', 17, DIM, a)

def art_dating(cv, t, R, sid):
    x0, y0, x1, y1 = R; a = ease(t / 1.0)
    ax0, ax1 = x0 + 30, x1 - 30; ay = y0 + (230 if L else 200)
    def X(yr): return ax0 + (yr - 1380) / (1460 - 1380) * (ax1 - ax0)
    cv.line([(ax0, ay), (ax1, ay)], mix(DIM2, BG, a), 3)
    for yr in range(1380, 1461, 20):
        cv.line([(X(yr), ay - 8), (X(yr), ay + 8)], mix(DIM, BG, a), 2); cv.text((X(yr), ay + 14), str(yr), 'mono', 20, DIM, 'ma', a)
    u = ap(t, sid, 0.12, 1.2)
    cv.rect((X(1404), ay - 46, X(1404) + (X(1438) - X(1404)) * u, ay - 4), mix(MINT, BG, 0.9 * a))
    cv.text(((X(1404) + X(1438)) / 2, ay - 80), 'vellum: 1404 to 1438', 'monob', 24, MINT, 'mm', u)
    mono(cv, ax0, y0 + 10, 'RADIOCARBON, UNIVERSITY OF ARIZONA, 2009', 20, CYAN, a)

def art_zipf(cv, t, R, sid):
    x0, y0, x1, y1 = R; a = ease(t / 1.0)
    px0, py0, px1, py1 = x0 + 60, y0 + 40, x1 - 20, y1 - 70
    cv.line([(px0, py0), (px0, py1), (px1, py1)], mix(DIM, BG, a), 2)
    pts = []
    for i in range(1, 60):
        xr = i / 59.0; fx = px0 + (px1 - px0) * math.log(1 + 40 * xr) / math.log(41)
        fy = py1 - (py1 - py0) * (1 - math.log(1 + 40 * xr) / math.log(41)) ** 1.6
        pts.append((fx, py0 + (py1 - py0) * (1 - (1 - xr) ** 0.55) * 0 + (py1 - py0) * (1 - 1 / (1 + 6 * xr)) * 0.0 + (py1 - fy) * 0 + (py1 - py0) * 0))
    # simple schematic: steep fall then long tail
    curve = [(px0 + (px1 - px0) * s, py0 + (py1 - py0) * (1 - 1 / (1 + 12 * s)) * 0.92) for s in [i / 60 for i in range(61)]]
    n = int(len(curve) * ease(t / 2.0))
    if n > 1: cv.line(curve[:n], mix(CYAN, BG, a), 4)
    cv.text((px0 - 12, py0), 'common', 'mono', 18, DIM, 'rm', a); cv.text((px0 - 12, py1), 'rare', 'mono', 18, DIM, 'rm', a)
    cv.text((px1, py1 + 14), 'words, ranked', 'mono', 18, DIM, 'ra', a)
    mono(cv, px0, py1 + 40, 'SCHEMATIC of a Zipf-like curve, not the real data', 17, DIM, a)

def art_entropy(cv, t, R, sid):
    x0, y0, x1, y1 = R; a = ease(t / 1.0)
    bx = x0 + (330 if L else 270); full = (x1 - bx - 40)
    mono(cv, x0, y0, 'CONDITIONAL ENTROPY (letters), bits', 20, CYAN, a)
    rows = [('Voynich text (B and L 2021)', 2.0, ROSE, 1.0), ('natural-language samples', 2.0, MINT, 0.0)]
    for i, (nm, v, col, solid) in enumerate(rows):
        yy = y0 + 50 + i * (90 if L else 80); u = ap(t, sid, 0.25 + 0.2 * i, 1.0)
        cv.text((x0, yy + 22), nm, 'sans', 22 if L else 20, TXT, 'lm', a)
        w = full * 0.45 * u
        cv.rect((bx, yy, bx + w, yy + 44), mix(col, BG, a * 0.85))
        if solid == 0.0:
            for k in range(6): cv.rect((bx + w + k * 26, yy, bx + w + k * 26 + 14, yy + 44), mix(col, BG, a * 0.85 * (1 - k / 6.5) * u))
            cv.text((bx + w + 170, yy + 22), 'higher', 'monob', 22, MINT, 'lm', u * a)
        else:
            cv.text((bx + w + 14, yy + 22), 'about 2', 'monob', 24, TXT, 'lm', u * a)
    mono(cv, x0, y0 + 50 + 2 * (90 if L else 80) + 10, 'not to scale: the language bar only shows "higher"', 17, DIM, a)

def art_sing(cv, t, R, sid):
    x0, y0, x1, y1 = R; a = ease(t / 1.0)
    sz = 70 if L else 56
    for row, (lab, order) in enumerate((('MADE AS', (1, 2, 3, 4)), ('BOUND AS', (3, 1, 4, 2)))):
        yy = y0 + 20 + row * (sz + 90)
        aa = a if row == 0 else ap(t, sid, 0.55, 1.0)
        mono(cv, x0, yy - 4, lab, 20, CYAN if row == 0 else ROSE, aa)
        for k, n in enumerate(order):
            bx = x0 + 180 + k * (sz + 16)
            rrect(cv, (bx, yy, bx + sz * 0.8, yy + sz), INK2, DIM, aa)
            cv.text((bx + sz * 0.4, yy + sz / 2), str(n), 'monob', 28, TXT, 'mm', aa)
    mono(cv, x0, y0 + 20 + 2 * (sz + 90), 'SCHEMATIC of the idea only: not the real order', 17, DIM, a)

def sc_pass(cv, t, p): pass

SC = {}
SC['s1'] = S_title('s1', 4, ('the book nobody', 'can read'), ('the book', 'nobody', 'can read'), 'Beinecke MS 408, Yale: what is established, claimed, open',
                   (('DOCUMENTED', MINT, 0.3), ('CLAIMED', VIO, 0.45), ('DISPUTED', ROSE, 0.62), ('UNKNOWN', ROSE, 0.85)), art_pages)
SC['s2'] = S_rows('s2', [('DOCUMENTED', MINT, None)], [
    ('DOCUMENTED', MINT, 'Beinecke MS 408, Yale. About 240 pages survive; about 272 is a reconstruction from gaps.', 0.12),
    ('DOCUMENTED', MINT, 'Handwritten on vellum, in a script Yale describes as unidentified. Plants, star charts, small bathing figures.', 0.45),
    ('DOCUMENTED', MINT, 'Named for Wilfrid Voynich, the dealer who bought it in 1912.', 0.78)], art_book)
SC['s3'] = S_rows('s3', [('DOCUMENTED', MINT, None), ('NOT ESTABLISHED: WHO, WHY', ROSE, 0.8)], [
    ('DOCUMENTED', MINT, 'Radiocarbon, University of Arizona, 2009: the sampled vellum dates to 1404 to 1438.', 0.1),
    ('DOCUMENTED', MINT, 'That dates the animal skin, not the writing on it.', 0.4),
    ('REPORTED', CYAN, 'Ink and paint analyses: materials consistent with the period. A modern forgery is difficult to argue.', 0.62)], art_dating)
SC['s4'] = S_table('s4', [('DOCUMENTED: 1639, 1912, 1969', MINT, None), ('CLAIMED: RUDOLF, BACON', VIO, 0.3)], [
    ('1639', 'Georg Baresch, Prague, writes to Athanasius Kircher: the earliest known mention', MINT, 0.12, 'DOCUMENTED', MINT),
    ('1665/66', 'Jan Marci relays a story told to him: Emperor Rudolf II paid 600 ducats; Roger Bacon wrote it', VIO, 0.32, 'CLAIMED', VIO),
    ('now', 'No independent record confirms the story. The Bacon idea is largely discredited', ROSE, 0.5, 'DISPUTED', ROSE),
    ('1912', 'Wilfrid Voynich buys the book', MINT, 0.68, 'DOCUMENTED', MINT),
    ('1969', 'The dealer H. P. Kraus donates it to Yale', MINT, 0.84, 'DOCUMENTED', MINT)])
SC['s5'] = S_rows('s5', [('MEASURED', MINT, None), ('COUNTS VARY', CYAN, 0.2)], [
    ('MEASURED', MINT, 'About 170,000 characters; about 38,000 transcribed words; about 8,000 different forms. A word = a string between spaces.', 0.08),
    ('MEASURED', MINT, 'Word frequencies are roughly Zipf-like, as in natural languages. Related words cluster in related places.', 0.4),
    ('NOT PROOF', ROSE, 'Patterns like these do not by themselves prove a language.', 0.78)], art_zipf)
SC['s6'] = S_rows('s6', [('MEASURED', MINT, None), ('ARGUED', VIO, 0.7)], [
    ('MEASURED', MINT, 'Bowern and Lindemann 2021: conditional entropy about 2 bits, lower than their language samples.', 0.08),
    ('MEASURED', MINT, 'Some characters appear almost only at the start or end of words.', 0.34),
    ('MEASURED', MINT, 'Two varieties, A and B, with different profiles (Currier).', 0.52),
    ('ARGUED', VIO, 'Five scribes, from the handwriting (Fagin Davis 2020).', 0.74)], art_entropy)
SC['s7'] = S_rows('s7', [('INTERPRETATION', VIO, None)], [
    ('MEASURED', MINT, 'Language-like in some ways: word frequencies, clustering.', 0.15),
    ('MEASURED', MINT, 'Unlike the languages it has been tested against in others: very predictable letters.', 0.42),
    ('NOT ESTABLISHED', ROSE, 'No proposed reading has been broadly accepted. This describes the data. It is not an explanation.', 0.7)])
SC['s8'] = S_table('s8', [('CLAIMED', VIO, None), ('DISCREDITED', ROSE, 0.45)], [
    ('1921', 'William Newbold, University of Pennsylvania: a hidden second script of microscopic shorthand', VIO, 0.12, 'CLAIMED', VIO),
    ('1931', 'John Manly, University of Chicago, in Speculum: a critique that dismantled the readings', MINT, 0.45, 'DOCUMENTED', MINT),
    ('result', 'Newbold\'s readings were not accepted. The pattern: a confident claim, then specialist critique.', ROSE, 0.75, 'DISCREDITED', ROSE)])
SC['s9'] = S_table('s9', [('CLAIMED', VIO, None), ('NONE BROADLY ACCEPTED', ROSE, 0.5)], [
    ('2013', 'Tucker and Talbert: Nahuatl, the Aztec language', VIO, 0.1, 'CLAIMED', VIO),
    ('2017', 'Nicholas Gibbs, Times Literary Supplement: abbreviated Latin on women\'s health', VIO, 0.28, 'CLAIMED', VIO),
    ('2017', 'Kondrak and Hauer: Hebrew with scrambled letters, by computer', VIO, 0.46, 'CLAIMED', VIO),
    ('2018', 'Ahmet Ardic: an old Turkic language', VIO, 0.64, 'CLAIMED', VIO),
    ('2019', 'Gerard Cheshire: a proto-Romance language', VIO, 0.82, 'CLAIMED', VIO)])
SC['s10'] = S_rows('s10', [('DISPUTED', ROSE, None)], [
    ('DISPUTED', ROSE, 'Lisa Fagin Davis on Gibbs: the method does not produce Latin that makes sense. On Cheshire: a circular method.', 0.1),
    ('DISPUTED', ROSE, 'M. Pharao Hansen on Tucker and Talbert: the readings are pure speculation.', 0.4),
    ('THE TEST', MINT, 'A credible decipherment: others get the same readable text, and it predicts pages nobody has read. None of these has met that.', 0.62)])
SC['s11'] = S_rows('s11', [('HOAX?', CYAN, None), ('NOT SETTLED', ROSE, 0.6)], [
    ('2003, RUGG', CYAN, 'A table of word parts and a card with holes (a Cardan grille) can generate text with some similar features. Shows a method is possible; not that it was used.', 0.1),
    ('2013, MONTEMURRO AND ZANETTE', VIO, 'Word patterns they argue are unlikely in a hoax. How much this proves is debated.', 0.6)])
SC['s12'] = S_rows('s12', [('CIPHER?', CYAN, None), ('ARGUED', VIO, 0.55)], [
    ('2025, GRESHKO, CRYPTOLOGIA', CYAN, 'The Naibbe cipher turns Latin or Italian into text reproducing some measured properties of the Voynich. A proof of concept, not a solution.', 0.12),
    ('2026, LAYFIELD AND DAVIS', VIO, 'Pages made as four-page units, bound out of order in the 15th century. Their argument, not a settled fact. "We do not know if it is a code."', 0.58)], art_sing)
SC['s13'] = S_rows('s13', [('OPEN', ROSE, None)], [
    ('NO PROOF', ROSE, 'A natural language in an invented script?   A cipher of a known language?', 0.12),
    ('NO PROOF', ROSE, 'A constructed language?   Meaningless text, a hoax?', 0.4),
    ('UNKNOWN', ROSE, 'Who made it, where, and why. Many plants are not confidently matched to real species. What the baths and charts were for.', 0.62)])
SC['s14'] = S_rows('s14', [('THE LEDGER', CYAN, None)], [
    ('DOCUMENTED', MINT, 'Vellum dated 1404 to 1438. In Prague by 1639. Held by Yale.', 0.12),
    ('MEASURED', MINT, 'Language-like word statistics, low letter entropy, two text varieties, several hands.', 0.3),
    ('CLAIMED', VIO, 'Every decipherment so far.', 0.5),
    ('COMPETING', CYAN, 'Hoax, cipher, language: unequal support.', 0.62),
    ('UNKNOWN', ROSE, 'What it says, if anything. Who made it.', 0.78)])
SC['s15'] = S_close('s15', 'not established.', 'not ruled out.', 'NOT ESTABLISHED', 'NOT RULED OUT', 'a credible solution would give coherent text that others can reproduce. the scans are free online at yale.')
SC['s16'] = sc_end

SOURCES = [
    'Beinecke Rare Book and Manuscript Library, Yale: MS 408 catalogue record and digital scans (beinecke.library.yale.edu). Yale News, 31 Oct 2016 (facsimile; materials analysis)',
    'Hodgins et al., University of Arizona radiocarbon dating of the vellum, 2009 (1404-1438). Wikipedia "Voynich manuscript" (provenance and claims summary; read 2026-10-20)',
    'Reddy and Knight 2011, ACL workshop; Bowern and Lindemann 2021, Annual Review of Linguistics 7; Montemurro and Zanette 2013, PLoS ONE; L. Fagin Davis 2020 (scribes)',
    'Manly 1931, Speculum (Newbold); G. Rugg 2003-04; Tucker and Talbert 2013; Gibbs, TLS, 5 Sep 2017; Hauer and Kondrak (TACL); Ardic 2018; Cheshire 2019, Romance Studies',
    'M. Greshko, "The Naibbe cipher", Cryptologia 2025; C. Layfield and L. Fagin Davis, "Singulion structure and the Voynich Manuscript", Digital Medievalist 19 (2026)',
    'Every picture here is drawn for this episode: invented marks stand in for the script. No photographs.']

SCENES = [
    ('s1', None, 'MS 408, Beinecke Library, Yale. Radiocarbon: vellum 1404 to 1438', SC['s1']),
    ('s2', 'the object', 'Beinecke Library, Yale: MS 408 record', SC['s2']),
    ('s3', 'its age', 'University of Arizona radiocarbon study, 2009; ink and paint analyses', SC['s3']),
    ('s4', 'its history', 'Beinecke record; Wikipedia "Voynich manuscript" (provenance)', SC['s4']),
    ('s5', 'the text', 'Reddy and Knight 2011; Montemurro and Zanette 2013. Counts vary by transcription', SC['s5']),
    ('s6', 'a strange text', 'Bowern and Lindemann 2021, Annual Review of Linguistics; Fagin Davis 2020', SC['s6']),
    ('s7', 'the problem', 'Our summary of the studies above', SC['s7']),
    ('s8', 'the solutions, part 1', 'Manly 1931, Speculum; Wikipedia "Voynich manuscript"', SC['s8']),
    ('s9', 'the solutions, part 2', 'Press and journal accounts as summarized on Wikipedia, read 2026-10-20', SC['s9']),
    ('s10', 'why specialists objected', 'L. Fagin Davis on Gibbs and Cheshire (Ars Technica, 2019); M. Pharao Hansen on Tucker and Talbert', SC['s10']),
    ('s11', 'a hoax?', 'G. Rugg 2003-04; Montemurro and Zanette 2013, PLoS ONE', SC['s11']),
    ('s12', 'a cipher? a binding error?', 'Greshko 2025, Cryptologia; Layfield and Davis 2026, Digital Medievalist', SC['s12']),
    ('s13', 'what is open', 'Status as of October 2026', SC['s13']),
    ('s14', None, 'Status as of October 2026', SC['s14']),
    ('s15', None, None, SC['s15']),
    ('s16', None, None, SC['s16']),
]
