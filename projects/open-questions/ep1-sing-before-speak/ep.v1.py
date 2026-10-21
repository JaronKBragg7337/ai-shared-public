import sys; sys.path.insert(0, '..')
from oqlib import *
import tvlib

SCR = json.load(open('script.json'))
SUBS = {s['id']: s['disp'] for s in SCR}

def fcard(cv, x0, y0, x1, y1, a, col):
    card(cv, (x0, y0, x1, y1), a, col)

# ------------------------------------------------------------------ s1 title
def sc_title(cv, t, p):
    a = ease(t / 1.0); ty = 150 if PORT else 70
    cv.text((W / 2, ty), 'HEARTBEAT TV  ·  OPEN QUESTIONS  ·  EPISODE 1', 'sansb', 30 if PORT else 34, DIMC, 'ma', a)
    sz = 104 if PORT else 128
    for k, l in enumerate(('Did we sing', 'before we spoke?')):
        cv.text((W / 2, ty + 90 + k * sz * 1.15), l, 'serif', sz, CREAM, 'ma', ease((t - 0.2) / 1.0), 5)
    y = 640 if PORT else 560
    c2 = cue('s1', 2)
    a2 = ease((t - c2) / 0.8)
    pill(cv, W * 0.27, y, 'SONG FIRST?', COR, a2, 38)
    pill(cv, W * 0.73, y, 'SPEECH FIRST?', TEA, a2, 38)
    cv.text((W / 2, y - 24), 'or', 'serifr', 44, DIMC, 'ma', a2)
    a3 = ease((t - c2 - 1.0) / 0.8)
    cv.text((W * 0.27, y + 80), 'Darwin · Mithen', 'sans', 32, DIMC, 'ma', a3)
    cv.text((W * 0.73, y + 80), 'Pinker', 'sans', 32, DIMC, 'ma', a3)

# ------------------------------------------------------------------ s2 Darwin
def sc_darwin(cv, t, p):
    if PORT: bx = (30, 350, 1050, 760); fx = W / 2; ty = 800; n1 = 950; n2 = 1160
    else: bx = (60, 200, 900, 800); fx = 1410; ty = 250; n1 = 470; n2 = 700
    a = ease(t / 0.7); card(cv, bx, a, COR)
    cx = (bx[0] + bx[2]) / 2
    cv.text((cx, bx[1] + 50), '1871', 'serif', 190, COR, 'ma', a)
    cv.text((cx, bx[1] + 290), 'Charles Darwin', 'sansb', 46, CREAM, 'ma', a)
    cv.text((cx, bx[1] + 350), 'The Descent of Man', 'serifr', 40, DIMC, 'ma', a)
    a1 = ease((t - cue('s2', 1)) / 0.7)
    cv.para(fx, ty, 'Music is in every culture. Its survival use is unclear.', 'sans', 44 if PORT else 40, CREAM, 520 if not PORT else 900, 1.2, 'm', a1)
    a2 = ease((t - cue('s2', 2)) / 0.7)
    if a2 > 0:
        pill(cv, fx, n1, 'musical calls + rhythm', COR, a2, 36)
        arrow(cv, (fx, n1 + 48), (fx, n2 - 52), DIMC, 5, 18, a2)
        cv.text((fx + 28, (n1 + n2) / 2 - 20), "Darwin's guess", 'serifr', 34, DIMC, 'la', a2)
        pill(cv, fx, n2, 'words', TEA, ease((t - cue('s2', 2) - 1.2) / 0.7), 36)

# ------------------------------------------------------------------ s3 Mithen
def sc_mithen(cv, t, p):
    rows = [('H', 'Holistic'), ('M', 'Manipulative'), ('M', 'Multi-modal'), ('M', 'Musical'), ('M', 'Mimetic')]
    x0 = 130 if not PORT else 110; y0 = 215 if not PORT else 385; st = 112 if not PORT else 100
    c1 = cue('s3', 1)
    for k, (l, w) in enumerate(rows):
        a = ease((t - c1 - 0.3 - k * 0.9) / 0.5)
        cv.text((x0, y0 + k * st), l, 'serif', 100 if not PORT else 84, COR, 'la', a)
        cv.text((x0 + 100, y0 + k * st + (22 if not PORT else 16)), w, 'serif', 56 if not PORT else 48, CREAM, 'la', a)
    c2 = cue('s3', 2); a2 = ease((t - c2) / 0.7)
    fx = 1400 if not PORT else W / 2
    cv.para(fx, 230 if not PORT else 880, 'Whole phrases carried meaning and feeling, with no separate words.', 'sans', 40 if not PORT else 38, CREAM, 640 if not PORT else 900, 1.2, 'm', a2)
    c3 = cue('s3', 3); a3 = ease((t - c3) / 0.7)
    if a3 > 0:
        ny = 420 if not PORT else 1000; py = 690 if not PORT else 1160; dx = 190 if not PORT else 230
        pill(cv, fx, ny, 'Hmmmmm', LAV, a3, 40)
        arrow(cv, (fx - 40, ny + 48), (fx - dx + 20, py - 48), DIMC, 5, 18, a3)
        arrow(cv, (fx + 40, ny + 48), (fx + dx - 20, py - 48), DIMC, 5, 18, a3)
        a4 = ease((t - c3 - 1.0) / 0.7)
        pill(cv, fx - dx, py, 'speech', TEA, a4, 36); pill(cv, fx + dx, py, 'music', COR, a4, 36)

# ------------------------------------------------------------------ s3b synthesized demo
def sc_demo(cv, t, p):
    a = ease(t / 0.6); tt = t + tvlib.BOUND['s3b'][0]
    area = (140, 260, 1780, 640) if not PORT else (50, 460, 1030, 860)
    card(cv, (area[0] - 30, area[1] - 50, area[2] + 30, area[3] + 50), a, LAV)
    scope(cv, tt, area, COR if (tt * 1.7) % 2 < 1 else TEA)
    badge(cv, area[0] - 30, area[1] - 50 - 74 if not PORT else area[1] - 124, 'SYNTHESIZED SOUND', LAV, a, 28)
    cv.para(W / 2, area[3] + 90, 'Made for this video: pitch and rhythm, no words. An illustration, not a reconstruction.', 'sans', 36, DIMC, W - 300, 1.2, 'm', ease((t - 0.8) / 0.8))

# ------------------------------------------------------------------ s4 Pinker
def sc_pinker(cv, t, p):
    a0 = ease((t - cue('s4', 0)) / 0.7)
    cv.text((W / 2, 220 if not PORT else 385), 'Steven Pinker', 'serif', 64, TEA, 'ma', a0)
    cv.text((W / 2, 300 if not PORT else 470), 'How the Mind Works, 1997', 'serifr', 38, DIMC, 'ma', a0)
    c1 = cue('s4', 1); c2 = cue('s4', 2)
    ccx, ccy, cr = (1330, 470, 165) if not PORT else (790, 730, 150)
    a1 = ease((t - c1) / 0.8)
    if a1 > 0:
        cv.circ((ccx, ccy), cr, mix(COR, BG, 0.25 * a1)); cv.ring((ccx, ccy), cr, mix(COR, BG, a1), 5)
        cv.text((ccx, ccy - 38), 'MUSIC', 'serif', 64, CREAM, 'ma', a1)
        cv.text((ccx, ccy + cr + 22), '"auditory cheesecake"', 'serifr', 38, COR, 'ma', a1)
        cv.text((ccx, ccy + cr + 70), 'a pleasure, not the starting point', 'sans', 30, DIMC, 'ma', a1)
    px = 440 if not PORT else 245
    for k, w in enumerate(('language', 'hearing', 'emotion')):
        ay = ease((t - (c2 - 3.2 + k * 0.9)) / 0.6)
        yy = (ccy - 130 + k * 130)
        if ay > 0:
            pill(cv, px, yy, w, TEA, ay, 36)
            arrow(cv, (px + 130 if not PORT else px + 115, yy), (ccx - cr - 12, ccy + (k - 1) * 60), DIMC, 4, 14, ay)
    a3 = ease((t - cue('s4', 3)) / 0.8)
    if a3 > 0: pill(cv, W / 2, 800 if not PORT else 1130, 'language first', TEA, a3, 44)

# ------------------------------------------------------------------ s5 In between
def sc_between(cv, t, p):
    x0, x1 = (160, 1760) if not PORT else (90, 990); by = 300 if not PORT else 410
    a = ease(t / 0.7)
    N = 60
    for i in range(N):
        u = i / (N - 1); col = tuple(int(COR[c] * (1 - u) + TEA[c] * u) for c in range(3))
        cv.rect((x0 + (x1 - x0) * i / N, by, x0 + (x1 - x0) * (i + 1) / N + 1, by + 14), mix(col, BG, a))
    specs = [(0.0, 'Music first', COR, ['Darwin (1871)', 'Mithen (2005)'], 0.4),
             (0.5, 'Shared ancestor', CREAM, ['Brown (2000): "musilanguage"', 'Fitch (2010): prosodic protolanguage'], cue('s5', 1)),
             (1.0, 'Language first', TEA, ['Pinker (1997)'], 1.0)]
    for u, title, col, lines, tc in specs:
        aa = ease((t - tc) / 0.7)
        if aa <= 0: continue
        mx = x0 + (x1 - x0) * u
        cv.circ((mx, by + 7), 15, mix(col, BG, aa))
        if PORT:
            k = int(round(u * 2)); bx = (30, 500 + k * 250, 1050, 500 + k * 250 + 225)
        else:
            w = 540; cx = x0 + (x1 - x0) * u; cx = min(max(cx, x0 + w / 2 - 100), x1 - w / 2 + 100); bx = (cx - w / 2, 380, cx + w / 2, 690)
        card(cv, bx, aa, col)
        cv.text((bx[0] + 30, bx[1] + 20), title, 'serif', 50, col, 'la', aa)
        yy = bx[1] + 95
        for l in lines: yy = cv.para(bx[0] + 30, yy, l, 'sans', 36, CREAM, bx[2] - bx[0] - 60, 1.2, 'l', aa) + 8

# ------------------------------------------------------------------ s6 hyoid
def sc_hyoid(cv, t, p):
    if PORT: bc = (540, 480); R = 165; ly = 660; c1b = (30, 705, 1050, 865); c2b = (30, 885, 1050, 1045); by = 1068; sy = 1130
    else: bc = (440, 470); R = 205; ly = 700; c1b = (900, 200, 1860, 400); c2b = (900, 420, 1860, 620); by = 650; sy = 730
    a = ease(t / 0.8); hyoid(cv, bc[0], bc[1], R, a)
    cv.text((bc[0], ly), 'hyoid bone (schematic drawing)', 'sans', 30, DIMC, 'ma', a)
    for bx, tc, num, lab, sub in ((c1b, cue('s6', 1), '60,000', 'years old, about', 'Kebara 2, Mount Carmel, Israel'),
                                  (c2b, cue('s6', 2), '2013', 'inner structure like modern humans', "D'Anastasio et al., PLOS ONE")):
        aa = ease((t - tc) / 0.6)
        if aa <= 0: continue
        card(cv, bx, aa, LAV)
        cv.text((bx[0] + 30, (bx[1] + bx[3]) / 2 - 58), num, 'serif', 96 if not PORT else 84, LAV, 'la', aa)
        nx = bx[0] + (400 if not PORT else 300)
        cv.para(nx, bx[1] + 30, lab, 'sansb', 38 if not PORT else 34, CREAM, bx[2] - nx - 20, 1.1, 'l', aa)
        cv.text((nx, bx[3] - 56), sub, 'sans', 32 if not PORT else 29, DIMC, 'la', aa)
    a3 = ease((t - cue('s6', 3)) / 0.6)
    if a3 > 0: badge(cv, 900 if not PORT else 30, by, 'SHAPE IS NOT USE', ROSE, a3, 28)
    a4 = ease((t - cue('s6', 4)) / 0.8)
    if a4 > 0: cv.para((1380 if not PORT else W / 2), sy, 'Spoken or sung? The bone cannot say.', 'serif', 50 if not PORT else 46, CREAM, 960, 1.15, 'm', a4)

# ------------------------------------------------------------------ s7 flutes
def sc_flutes(cv, t, p):
    if PORT: boxes = [(30, 350, 1050, 700), (30, 720, 1050, 1070)]; foot = 1090
    else: boxes = [(60, 190, 940, 730), (980, 190, 1860, 730)]; foot = 745
    specs = [
        ('Divje Babe, Slovenia', ROSE, ('DISPUTED', ROSE), cue('s7', 1),
         [(cue('s7', 1), 'Cave bear thighbone, found 1995'), (cue('s7', 1) + 2.2, 'Estimated 50,000 to 60,000 years old'),
          (cue('s7', 2), 'Finders: Neanderthals made the holes'), (cue('s7', 3), 'Others: hyenas chewed them')]),
        ('Geissenklösterle, Germany', SAGE, ('WIDELY ACCEPTED', SAGE), cue('s7', 4),
         [(cue('s7', 4), 'Bird bone and mammoth ivory flutes'), (cue('s7', 4) + 2.5, 'Layers dated to about 42,000 years ago'),
          (cue('s7', 4) + 5.0, 'Attributed to modern humans')])]
    for bx, (title, col, tag, tc, lines) in zip(boxes, specs):
        a = ease((t - tc) / 0.6)
        if a <= 0: continue
        card(cv, bx, a, col)
        cv.text((bx[0] + 34, bx[1] + 20), title, 'serif', 44 if PORT else 50, col, 'la', a)
        badge(cv, bx[0] + 34, bx[1] + (84 if PORT else 96), tag[0], tag[1], a, 26)
        if PORT: flute(cv, bx[2] - 340, bx[1] + 130, 280, 34, t - tc, a, 5 if col == SAGE else 3); y = bx[1] + 160
        else: flute(cv, bx[0] + 140, bx[1] + 220, 560, 54, t - tc, a, 5 if col == SAGE else 3); y = bx[1] + 290
        if PORT: y = bx[1] + 150
        for lt, txt in lines:
            la = ease((t - lt) / 0.6)
            y = cv.para(bx[0] + 34, y, '• ' + txt, 'sans', 35 if PORT else 38, CREAM, bx[2] - bx[0] - 68, 1.15, 'l', la) + 8
    a5 = ease((t - cue('s7', 5)) / 0.7)
    if a5 > 0: cv.text((W / 2, foot), 'Oldest music we can agree on: about 42,000 years', 'serif', 44 if PORT else 52, CREAM, 'ma', a5)
    a6 = ease((t - cue('s7', 6)) / 0.7)
    if a6 > 0: cv.text((W / 2, foot + (62 if PORT else 66)), 'If the Slovenian bone is a flute: older', 'serifr', 38 if PORT else 42, ROSE, 'ma', a6)

# ------------------------------------------------------------------ s8 babies
def sc_babies(cv, t, p):
    c4 = cue('s8', 4)
    if t < c4 - 0.3:
        a1 = ease((t - cue('s8', 1)) / 0.7)
        py = 250 if not PORT else 400
        for k, (w, dx) in enumerate((('higher', -330), ('slower', 0), ('more melodic', 360))):
            pill(cv, W / 2 + dx * (1 if not PORT else 0.72), py, w, LAV, ease((t - cue('s8', 1) - 0.6 - k * 0.5) / 0.5), 34)
        if PORT: boxes = [(30, 500, 1050, 840), (30, 860, 1050, 1200)]
        else: boxes = [(60, 360, 940, 800), (980, 360, 1860, 800)]
        for bx, tc, num, lab, sub in ((boxes[0], cue('s8', 2), '315', 'societies studied (2019)', 'song found in every one; lullabies recognized across cultures'),
                                      (boxes[1], cue('s8', 3), '144', 'American infants (2021)', 'relaxed to unfamiliar foreign lullabies')):
            aa = ease((t - tc) / 0.7)
            if aa <= 0: continue
            card(cv, bx, aa, LAV)
            cv.text(((bx[0] + bx[2]) / 2 if not PORT else bx[0] + 40, bx[1] + 28), num, 'serif', 140, LAV, 'ma' if not PORT else 'la', aa)
            tx = (bx[0] + bx[2]) / 2 if not PORT else bx[0] + 360
            if PORT:
                cv.text((tx, bx[1] + 50), lab, 'sansb', 38, CREAM, 'la', aa); cv.para(tx, bx[1] + 105, sub, 'sans', 32, DIMC, bx[2] - tx - 30, 1.2, 'l', aa)
            else:
                cv.text((tx, bx[1] + 200), lab, 'sansb', 40, CREAM, 'ma', aa); cv.para(tx, bx[1] + 260, sub, 'sans', 34, DIMC, 780, 1.2, 'm', aa)
    else:
        side_cards(cv, t, ('Music-first read', COR, ['An old, deep root for song', 'Infants respond to lullabies from other cultures']),
                   ('Skeptic read', TEA, ['Babies like calm, repeating sounds', 'That says little about dates', '"Universal" depends on how a lullaby is defined']),
                   c4 - 0.2, cue('s8', 5), area=((60, 270, 1860, 690) if not PORT else None))

# ------------------------------------------------------------------ s9 brain
def sc_brain(cv, t, p):
    if PORT: cx, cy, r, d = 540, 690, 250, 140
    else: cx, cy, r, d = 960, 465, 215, 140
    a = ease(t / 0.8); cL, cR = venn(cv, cx, cy, r, d, a)
    cv.text((cL[0] - r * 0.42, cy - 18), 'music', 'serif', 54, COR, 'ma', a); cv.text((cR[0] + r * 0.38, cy - 18), 'language', 'serif', 50, TEA, 'ma', a)
    a1 = ease((t - cue('s9', 1)) / 0.7)
    if a1 > 0:
        ty = cy - r - 62 if not PORT else cy - r - 55
        cv.text((cx, ty), 'shared processing', 'sansb', 36, CREAM, 'ma', a1)
        cv.line([(cx, ty + 46), (cx, cy - 20)], mix(CREAM, BG, a1), 3)
    a3 = ease((t - cue('s9', 3)) / 0.7)
    cv.text((W / 2, cy + r + 18), 'Patients can lose music and keep language, or the reverse', 'sans', 36 if not PORT else 36, DIMC, 'ma', a3)
    a4 = ease((t - cue('s9', 4)) / 0.7)
    if a4 > 0: cv.text((W / 2, cy + r + 66), 'Overlap shows kinship, not order.', 'serif', 52 if not PORT else 46, LAV, 'ma', a4)

# ------------------------------------------------------------------ s10 new
def sc_new(cv, t, p):
    items = [dict(year='2024', who='Ozaki et al., Science Advances', what='Songs are slower, higher and steadier in pitch than speech (55 languages, 75 researchers)', at=cue('s10', 1), col=COR),
             dict(year='2025', who='Eleuteri et al., Current Biology', what='Wild chimpanzees drum with steady, regular timing', at=cue('s10', 3), col=LAV),
             dict(year='2026', who='Honing, Current Biology (9 March)', what='Musicality is rooted in biology, not only culture', at=cue('s10', 4), col=TEA)]
    rail(cv, t, items, (60, 190, 1860, 700) if not PORT else (30, 350, 1050, 1120))
    a = ease((t - cue('s10', 5)) / 0.7)
    cv.text((W / 2, 745 if not PORT else 1150), 'None of these dates the first song.', 'serif', 54 if not PORT else 46, CREAM, 'ma', a)

# ------------------------------------------------------------------ s11 settle
def sc_settle(cv, t, p):
    rows = ['Undisputed instruments older than 50,000 years, or a firm answer on Divje Babe',
            'Better evidence of ancient voices and hearing: fossils, ancient DNA',
            'Comparisons across species: which musical abilities came before ours?',
            'Brain tests that pull shared and separate machinery apart']
    y0, y1 = (190, 740) if not PORT else (350, 1120); n = 4; gap = 18; h = (y1 - y0 - gap * 3) / 4
    for k, txt in enumerate(rows):
        a = ease((t - cue('s11', k + 1)) / 0.6)
        if a <= 0: continue
        bx = (60 if not PORT else 30, y0 + k * (h + gap), W - (60 if not PORT else 30), y0 + k * (h + gap) + h)
        card(cv, bx, a, LAV)
        checkbox(cv, bx[0] + 34, (bx[1] + bx[3]) / 2 - 24, 48, a)
        cv.text((bx[0] + 112, (bx[1] + bx[3]) / 2 - 36), str(k + 1), 'serif', 72, LAV, 'la', a)
        cv.para(bx[0] + 190, bx[1] + 22 if PORT else (bx[1] + bx[3]) / 2 - 26, txt, 'sans', 40 if not PORT else 36, CREAM, bx[2] - bx[0] - 230, 1.15, 'l', a)
    a5 = ease((t - cue('s11', 5)) / 0.7)
    cv.text((W / 2, 765 if not PORT else 1150), 'Voices leave no bones.', 'serif', 52 if not PORT else 46, LAV, 'ma', a5)

# ------------------------------------------------------------------ s12 close, s13 end
def sc_close(cv, t, p):
    statements(cv, t, [(cue('s12', 0), 'Did we sing before we spoke?', CREAM, 'serif'), (cue('s12', 1), 'Not established.', LAV, 'serif'),
                       (cue('s12', 2), 'The question stays open.', DIMC, 'serifr')], 250 if not PORT else 420)
    a = ease((t - cue('s12', 1)) / 0.8); x0 = W / 2 - 120
    cv.rect((x0, 700 if not PORT else 1000, x0 + 120, 706 if not PORT else 1006), mix(COR, BG, a)); cv.rect((x0 + 120, 700 if not PORT else 1000, x0 + 240, 706 if not PORT else 1006), mix(TEA, BG, a))

SOURCES = ['Darwin, The Descent of Man (1871) · Mithen, The Singing Neanderthals (2005) · Pinker, How the Mind Works (1997)',
           'Brown, "The musilanguage model of music evolution" (2000) · Fitch, The Evolution of Language (2010)',
           "D'Anastasio et al., PLOS ONE (2013) · Arensburg et al., Nature (1989): Kebara 2 hyoid",
           'Tuniz et al. (2012) and Diedrich (2015) on Divje Babe · Higham et al., J. Human Evolution (2012), Geissenklösterle',
           'Mehr et al., Science 366 (2019) · Bainbridge et al., Nature Human Behaviour (2021) · "Lullabies and Universality," Cross-Cultural Research (2024)',
           'Patel, Nature Neuroscience (2003) · Peretz et al., amusia studies · Fernald (1989), infant-directed speech',
           'Ozaki et al., Science Advances (May 2024) · Eleuteri et al., Current Biology (2025) · Honing, Current Biology (9 March 2026)']

def sc_end(cv, t, p):
    a = ease(t / 1.0); cy = 80 if not PORT else 230
    cv.text((W / 2, cy), 'Heartbeat Observatory', 'serif', 96 if not PORT else 88, CREAM, 'ma', a)
    cv.rect((W / 2 - 100, cy + 125, W / 2, cy + 131), mix(COR, BG, a)); cv.rect((W / 2, cy + 125, W / 2 + 100, cy + 131), mix(TEA, BG, a))
    cv.text((W / 2, cy + 150), 'heartbeatobservatory.com', 'sansb', 52, COR, 'ma', a)
    cv.text((W / 2, cy + 225), 'Open Questions · Episode 1 · sources checked October 2026', 'sans', 34 if not PORT else 30, DIMC, 'ma', a)
    y = cy + 300; cv.text((W / 2, y), 'Sources', 'sansb', 32, DIMC, 'ma', ease((t - 0.6) / 1))
    yy = y + 50
    for i, s in enumerate(SOURCES):
        yy = cv.para(W / 2, yy, s, 'sans', 28 if not PORT else 27, CREAM, 1700 if not PORT else 980, 1.2, 'm', ease((t - 0.8 - i * 0.2) / 0.8)) + 8

SCENES = [
 ('s1', '', '', sc_title),
 ('s2', 'Darwin, 1871', 'Source: Charles Darwin, The Descent of Man (1871).', sc_darwin),
 ('s3', 'Music first: Mithen', 'Source: Steven Mithen, The Singing Neanderthals (2005).', sc_mithen),
 ('s3b', 'A sketch of a Hmmmmm phrase', '', sc_demo),
 ('s4', 'Language first: Pinker', 'Source: Steven Pinker, How the Mind Works (1997).', sc_pinker),
 ('s5', 'In between', 'Sources: Brown, "The musilanguage model of music evolution" (2000); Fitch, The Evolution of Language (2010).', sc_between),
 ('s6', 'Clue 1: the throat', "Sources: D'Anastasio et al., PLOS ONE (2013); Arensburg et al., Nature (1989). Drawing is schematic.", sc_hyoid),
 ('s7', 'Clue 2: flutes', 'Sources: Tuniz et al. (2012); Diedrich (2015); Higham et al., J. Human Evolution (2012). Ages are estimates; Higham dated animal bones in the flute layers.', sc_flutes),
 ('s8', 'Clue 3: babies', 'Sources: Mehr et al., Science (2019); Bainbridge et al., Nature Human Behaviour (2021); "Lullabies and Universality," Cross-Cultural Research (2024).', sc_babies),
 ('s9', 'Clue 4: the brain', 'Sources: Patel, Nature Neuroscience (2003); Peretz et al. on amusia.', sc_brain),
 ('s10', 'What is new', 'Sources: Ozaki et al., Science Advances (2024); Eleuteri et al., Current Biology (2025); Honing, Current Biology (March 2026), as reported by the University of Amsterdam.', sc_new),
 ('s11', 'What would settle it', '', sc_settle),
 ('s12', '', '', sc_close),
 ('s13', '', '', sc_end),
]
configure(SUBS, SCENES)
if __name__ == '__main__': main()
