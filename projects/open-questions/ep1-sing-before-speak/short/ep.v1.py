import sys; sys.path.insert(0, '../..')
from oqlib import *
import tvlib
SCR = json.load(open('script.json')); SUBS = {s['id']: s['disp'] for s in SCR}

def sc_title(cv, t, p):
    a = ease(t / 0.8); sz = 110
    cv.text((W / 2, 150), 'HEARTBEAT TV  ·  OPEN QUESTIONS', 'sansb', 30, DIMC, 'ma', a)
    for k, l in enumerate(('Did we sing', 'before we spoke?')):
        cv.text((W / 2, 250 + k * sz * 1.15), l, 'serif', sz, CREAM, 'ma', ease((t - 0.2) / 0.8), 5)
    a2 = ease((t - cue('q1', 2)) / 0.7)
    pill(cv, W * 0.27, 700, 'SONG FIRST?', COR, a2, 38); pill(cv, W * 0.73, 700, 'SPEECH FIRST?', TEA, a2, 38)
    cv.text((W / 2, 676), 'or', 'serifr', 44, DIMC, 'ma', a2)

def sc_sides(cv, t, p):
    c0, c2 = cue('q2', 0), cue('q2', 2)
    side_cards(cv, t, ('Song first', COR, ['Darwin, 1871: musical calls before words', 'Mithen, 2005: a humming, singing "Hmmmmm"']),
               ('Language first', TEA, ['Pinker, 1997: music is "auditory cheesecake"', 'A pleasant by-product of other brain systems']), c0, c2, size=44)

def sc_demo(cv, t, p):
    a = ease(t / 0.6); tt = t + tvlib.BOUND['qd'][0]
    area = (60, 480, 1020, 880)
    card(cv, (30, 430, 1050, 930), a, LAV)
    scope(cv, tt, area, COR if (tt * 1.7) % 2 < 1 else TEA)
    badge(cv, 30, 350, 'SYNTHESIZED SOUND', LAV, a, 28)
    cv.para(W / 2, 960, 'Made for this video: pitch and rhythm, no words. An illustration.', 'sans', 38, DIMC, 960, 1.2, 'm', ease((t - 0.8) / 0.8))

def sc_evidence(cv, t, p):
    side_cards(cv, t, ('Neanderthal hyoid', LAV, ['About 60,000 years old, like ours', 'Speech sounds possible', 'Spoken or sung? It cannot say']),
               ('Bone flutes', SAGE, ['Germany: about 42,000 years, accepted', 'Slovenia: maybe older, disputed']), cue('q4', 1), cue('q4', 2), size=44)

def sc_new(cv, t, p):
    items = [dict(year='2024', who='Science Advances', what='Songs are slower and higher than speech (55 languages)', at=cue('q5', 1), col=COR),
             dict(year='2025', who='Current Biology', what='Wild chimpanzees drum in steady rhythm', at=cue('q5', 2), col=LAV),
             dict(year='2026', who='Current Biology (March)', what='Musicality is rooted in biology', at=cue('q5', 3), col=TEA)]
    rail(cv, t, items, (30, 350, 1050, 1120))
    a = ease((t - cue('q5', 4)) / 0.7)
    cv.text((W / 2, 1150), 'None of it dates the first song.', 'serif', 46, CREAM, 'ma', a)

def sc_settle(cv, t, p):
    rows = ['Undisputed instruments older than 50,000 years', 'Evidence of ancient voices and hearing', 'Tests across species']
    for k, txt in enumerate(rows):
        a = ease((t - cue('q6', 1) - k * 1.8) / 0.6)
        if a <= 0: continue
        bx = (30, 360 + k * 150, 1050, 360 + k * 150 + 128); card(cv, bx, a, LAV); checkbox(cv, 64, bx[1] + 40, 48, a)
        cv.para(150, bx[1] + 30, txt, 'sans', 40, CREAM, 860, 1.15, 'l', a)
    a3 = ease((t - cue('q6', 3)) / 0.8)
    cv.text((W / 2, 880), 'Not established.', 'serif', 92, LAV, 'ma', a3)
    a4 = ease((t - cue('q6', 4)) / 0.8)
    cv.text((W / 2, 1030), 'heartbeatobservatory.com', 'sansb', 50, COR, 'ma', a4)
    two = W / 2 - 100; cv.rect((two, 1110, two + 100, 1116), mix(COR, BG, a4)); cv.rect((two + 100, 1110, two + 200, 1116), mix(TEA, BG, a4))

SCENES = [('q1', '', '', sc_title), ('q2', 'Two sides', 'Sources: Darwin (1871); Mithen, The Singing Neanderthals (2005); Pinker, How the Mind Works (1997).', sc_sides),
          ('qd', 'A sketch of a "Hmmmmm"', '', sc_demo),
          ('q4', 'What the evidence says', "Sources: D'Anastasio et al., PLOS ONE (2013); Higham et al., J. Human Evolution (2012); Tuniz et al. (2012); Diedrich (2015).", sc_evidence),
          ('q5', 'What is new', 'Sources: Ozaki et al., Science Advances (2024); Eleuteri et al., Current Biology (2025); Honing, Current Biology (March 2026).', sc_new),
          ('q6', 'What would settle it', 'Full sources: heartbeatobservatory.com, Heartbeat TV, Open Questions 9.1.', sc_settle)]
configure(SUBS, SCENES)
if __name__ == '__main__': main()
