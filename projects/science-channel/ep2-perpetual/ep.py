import sys; sys.path.insert(0, '../../tv-lib')
from tvlib import *
import numpy as np
import wheel as WH

SIM_A = np.load('simA.npy'); SIM_B = np.load('simB.npy')   # columns: t, theta, omega, KE, PE, heat
ETOT = float(SIM_A[0, 3] + SIM_A[0, 4])
SIM_DT = SIM_A[1, 0] - SIM_A[0, 0]

def sim_at(sim, ts):
    i = min(len(sim) - 1, max(0, int(ts / SIM_DT + 0.5)))
    return sim[i]

def draw_wheel(cv, c, sc, theta, a=1.0, labels=False, t=0.0):
    cx, cy = c
    P = lambda x, y: (cx + x * sc, cy - y * sc)
    cv.ring(c, WH.RIM * sc, mix(STEEL, BG, a), 4)
    ps = []
    for i in range(WH.N):
        al = theta + 2 * math.pi * i / WH.N
        pv = (WH.RIM * math.cos(al), WH.RIM * math.sin(al))
        r = WH.rho(math.cos(al)); wp = (r * math.cos(al), r * math.sin(al))
        cv.line([c, P(*pv)], mix(STEEL, BG, 0.5 * a), 3)
        cv.line([P(*pv), P(*wp)], mix(DIM, BG, a), 6)
        cv.circ(P(*pv), 6, mix(TXT, BG, a))
        ps.append(P(*wp))
    for q in ps: cv.circ(q, 17, mix(AMBER, BG, a))
    cv.circ(c, 11, mix(TXT, BG, a))

def sc_title(cv, t, p):
    a = ease(t / 1.2)
    c = (W / 2, 760 if PORT else 560); sc = 520 if PORT else 640
    draw_wheel(cv, c, sc * 0.9, 0.3 + t * 0.25, 0.45 * a)
    title_block(cv, t, 'SCIENCE', 2, 'Can a machine', 'run forever?', 'Perpetual motion, tested')

def sc_history(cv, t, p):
    stat_cards(cv, t, [
        dict(num='c. 1150', label='A wheel with weights on its rim', sub='often credited to Bhaskara', tag='ATTRIBUTION DISPUTED', at=cue('s2', 1)),
        dict(num='c. 1230', label='Villard de Honnecourt', sub='draws an overbalanced wheel in France', col=TEAL, at=cue('s2', 2)),
        dict(num='c. 1500', label='Leonardo da Vinci', sub='draws several, and doubts them', col=TEAL, at=cue('s2', 3)),
        dict(num='1775', label='Paris Academy of Sciences', sub='stops examining such proposals', col=BLUE, at=cue('s2', 4))])

def sc_wheel(cv, t, p):
    if PORT: c = (W / 2, CONT[1] + 400); sc = 640
    else: c = (CONT[0] + 520, CONT[1] + 330); sc = 640
    a = ease(t / 0.8)
    draw_wheel(cv, c, sc, -0.35, a)
    a2 = ease((t - cue('s3', 1)) / 0.7)
    tx = c[0] + (0.62 * sc if not PORT else 0.55 * sc)
    if not PORT:
        for k, (txt, col) in enumerate((('8 weights, 1 kg each', TXT), ('arms swing OUT on the right', AMBER), ('and fold IN on the left', TEAL))):
            cv.text((tx + 330, c[1] - 150 + k * 70), txt, 'sansb', 40, col, 'la', ease((t - cue('s3', 1) - k * 0.7) / 0.6))
    else:
        for k, (txt, col) in enumerate((('8 weights, 1 kg each', TXT), ('arms swing OUT on the right, fold IN on the left', AMBER))):
            cv.text((W / 2, CONT[3] - 150 + k * 62), txt, 'sansb', 36, col, 'ma', ease((t - cue('s3', 1) - k * 0.7) / 0.6))
    a3 = ease((t - cue('s3', 2)) / 0.8)
    if a3 > 0:
        # clockwise arrow: the direction it "should" turn
        r = 0.52 * sc
        pts = [(c[0] + r * math.cos(math.radians(60 - k * 6)), c[1] - r * math.sin(math.radians(60 - k * 6))) for k in range(0, 14)]
        cv.line(pts, mix(RED, BG, a3), 8)
        e0, e1 = pts[-2], pts[-1]
        arrow(cv, e0, e1, RED, 8, 26, a3)
        cv.text((c[0] + r * 0.82, c[1] - r * 1.08 - 6), 'should turn this way', 'sansb', 32, RED, 'la', a3)

def energy_panel(cv, t, st, x0, y0, x1, y1, phase):
    ke, pe, ht = max(0, st[3]), max(0, st[4]), st[5]
    # energy conservation: put any tiny numerical drift into PE
    tot = ke + pe + ht
    rows = [('Motion (kinetic)', ke, AMBER), ('Height (potential)', pe, TEAL), ('Heat (friction)', ht, RED)]
    n = len(rows); step = (y1 - y0 - 150) / n
    cv.text((x0, y0), 'Energy accounting', 'serif', 46, TXT, 'la')
    lw = 430 if not PORT else 330
    for i, (lab, v, col) in enumerate(rows):
        y = y0 + 80 + i * step
        cv.text((x0, y + 10), lab, 'sansb', 36 if not PORT else 32, TXT, 'la')
        bx0 = x0 + lw; bw = (x1 - bx0 - 190) * min(1.0, v / ETOT)
        cv.rect((bx0, y + 6, x1 - 190, y + 56), mix(CARD, BG, 1), 8)
        if bw > 0: cv.rect((bx0, y + 6, bx0 + bw, y + 56), col, 8)
        cv.text((x1 - 10, y + 6), f'{v:4.2f} J', 'serif', 44 if not PORT else 40, col, 'ra')
    yt = y0 + 80 + n * step + 8
    cv.line([(x0, yt), (x1, yt)], mix(STEEL, BG, 0.7), 3)
    cv.text((x0, yt + 14), 'Total', 'sansb', 38, TXT, 'la')
    cv.text((x1 - 10, yt + 6), f'{tot:4.2f} J', 'serif', 52, GREEN, 'ra')

def sc_sim(cv, t, p):
    c0 = cue('s4', 0); c3 = cue('s4', 3)
    if PORT: c = (W / 2, CONT[1] + 235); sc = 480; px0, py0, px1, py1 = CONT[0] + 20, CONT[1] + 570, CONT[2] - 20, CONT[3] + 50
    else: c = (CONT[0] + 330, CONT[1] + 300); sc = 600; px0, py0, px1, py1 = CONT[0] + 740, CONT[1] + 20, CONT[2] - 20, CONT[3] - 20
    if t < c3 - 0.1:
        ts = max(0.0, t - c0 - 0.8); st = sim_at(SIM_A, ts); phase = 'NO FRICTION'; pc = TEAL
    else:
        ts = (t - c3) * 1.3; st = sim_at(SIM_B, ts); phase = 'WITH FRICTION (time x1.3)'; pc = RED
    draw_wheel(cv, c, sc, st[1])
    badge(cv, c[0] if PORT else c[0], c[1] + (WH.R_OUT * sc + 60 if not PORT else WH.R_OUT * sc + 70) - (0 if not PORT else 20), phase.split('  ')[0] if PORT else phase, pc, 1.0, 28, 'm')
    if t >= c0 + 0.3: energy_panel(cv, t, st, px0, py0, px1, py1, phase)
    a = ease((t - c0) / 0.6) * (1 - ease((t - c0 - 2.2) / 0.6))
    if a > 0: cv.text((c[0], c[1] - WH.R_OUT * sc - 40), 'one push: 3.34 J in', 'sansb', 38, AMBER, 'ma', a)

def sc_laws(cv, t, p):
    stat_cards(cv, t, [
        dict(num='1st law', label='Energy is conserved', sub='a machine cannot give out more than it takes in', at=cue('s5', 1)),
        dict(num='2nd law', label='Heat flows from hot to cold', sub='no machine turns one heat source fully into work', col=TEAL, at=cue('s5', 2)),
        dict(num='Tested', label='our best current understanding', sub='no claimed perpetual motion machine has passed an independent test', col=BLUE, at=cue('s5', 3))])

def sc_works(cv, t, p):
    stat_cards(cv, t, [
        dict(num='≈ 1,000 W', label='sunlight per square meter, clear noon', sub='panels turn about 20–25% into power', at=cue('s6', 1)),
        dict(num='≈ 3 J', label='per footstep on a floor tile', sub='the maker’s figure; no independent test found', col=TEAL, at=cue('s6', 2)),
        dict(num='0.2 nW–1 µW', label='ambient radio waves per cm²', sub='range across published measurements', col=BLUE, at=cue('s6', 3))])

def sc_little(cv, t, p):
    c = cue('s7', 0)
    stat_cards(cv, t, [
        dict(num='≈ 18,000', label='footsteps to fill one phone battery', sub='15 Wh = 54,000 J at 3 J a step, no losses', at=c + 0.3),
        dict(num='≈ 175 years', label='from radio waves at 10 µW', sub='a generous figure; no losses', col=TEAL, at=cue('s7', 1)),
        dict(num='≈ 5 min', label='one square meter of panel, noon, clear sky', sub='about 200 W; our arithmetic', col=AMBER, at=cue('s7', 2))])

def sc_edge(cv, t, p):
    stat_cards(cv, t, [
        dict(num='1998', label='the expansion is found to be speeding up', sub='supernova surveys; Nobel Prize in Physics 2011', at=cue('s8', 1)),
        dict(num='≈ 68%', label='of the universe’s energy content: dark energy', sub='inferred in the standard model; cause unexplained', col=TEAL, at=cue('s8', 3)),
        dict(num='Hints', label='that it may change over time', sub='DESI 2025: about 2.8–4.2 sigma, short of the 5 sigma bar', col=BLUE, tag='NOT SETTLED', at=cue('s8', 4)),
        dict(num='Tapped?', label='whether anything like it could be used', sub='no known way', col=AMBER, tag='NOT ESTABLISHED', at=cue('s8', 5))])

def sc_lesson(cv, t, p):
    statements(cv, t, [(cue('s9', 0), 'Every machine we have built stops.', TXT, 'serifr'), (cue('s9', 1), 'What we have not understood yet is still out there.', AMBER, 'serif')])

def sc_end(cv, t, p):
    end_block(cv, t, 'Science', 2, ['Museo Galileo, perpetual motion in the Middle Ages · Wikipedia, History of perpetual motion machines (1775 Academy)',
        'Simulation: our own model (8 × 1 kg weights, 0.3 m rim), energy conserved to <0.1% · Pavegen FAQ (3 J/step)',
        'Ambient RF reviews (0.2 nW–1 µW/cm²) · NREL / reviews on solar efficiency · Planck (NASA) 68.3% · Nobel Prize 2011 · DESI DR2 (2025)'])

SUBS = {
 's1': ['Can a machine run forever?'],
 's2': ['People have tried for centuries.', 'A 12th century wheel with weights on its rim is often credited to Bhaskara, though that is disputed.', 'Villard de Honnecourt drew one in France in the early 1200s.', 'Leonardo da Vinci drew several, and doubted them.', 'In 1775, the Paris Academy of Sciences stopped examining such proposals.'],
 's3': ['Let’s test it in a simulation.', 'Eight weights on arms: swung out on the right, folded in on the left.', 'The right side looks heavier, so the wheel should keep turning.'],
 's4': ['One push.', 'With no friction, it never gains speed.', 'Energy only trades between motion and height.', 'Now add a little friction.', 'The energy leaks away as heat, and the wheel settles.', 'The push is now warmth in the bearing and the air.', 'Add it all up, and the books always balance.'],
 's5': ['Two rules explain this.', 'First law: energy is neither created nor destroyed, so a machine cannot give out more than it takes in.', 'Second law: heat flows from hot to cold, so no machine can turn heat from one source completely into work.', 'These are our best current understanding, and the most tested rules in physics.', 'No claimed perpetual motion machine has passed an independent test.'],
 's6': ['What works is collecting energy that already flows.', 'Sunlight is about 1,000 watts per square meter, and panels turn 20 to 25 percent of it into power.', 'A footstep on a floor tile gives around 3 joules, by one maker’s figure.', 'Radio waves in the air carry nanowatts to one microwatt per square centimeter.'],
 's7': ['Fill one phone battery from footsteps: about 18,000 steps.', 'From radio waves at 10 microwatts: about 175 years.', 'Useful for tiny sensors, not for a phone.'],
 's8': ['Now the open edge.', 'In 1998, astronomers found that the expansion of the universe is speeding up. The Nobel Prize followed in 2011.', 'We call the cause dark energy.', 'In the standard model it is about 68 percent of the universe’s energy content, and we cannot yet explain it.', 'Recent surveys hint that it may change over time. That is not settled.', 'Whether anything like it could ever be tapped is not established.'],
 's9': ['Every machine we have built stops.', 'What we have not understood yet is still out there.'],
 's10': [],
}
SCENES = [
 ('s1', '', '', sc_title),
 ('s2', 'Wheels meant to run forever', 'Sources: Museo Galileo (Villard, Leonardo); Wikipedia, History of perpetual motion machines. The Bhaskara attribution and the 1775 date rest on secondary sources.', sc_history),
 ('s3', 'The overbalanced wheel', 'Simulation, our own model: 8 weights of 1 kg on a 0.3 m rim; arms out on the right, in on the left. Illustrative design.', sc_wheel),
 ('s4', 'Where does the energy go?', 'Simulation: same wheel, one clockwise push. Friction: a bearing and air drag we chose. Energy conserved to better than 0.1%.', sc_sim),
 ('s5', 'Two rules that explain it', 'Sources: first and second laws of thermodynamics. Stated here as our best current understanding, not a final verdict.', sc_laws),
 ('s6', 'What does work', 'Sources: standard solar test conditions, 1000 W/m²; reviews of module efficiency; Pavegen FAQ; reviews of ambient RF measurements.', sc_works),
 ('s7', 'How little some of it gives', 'Our arithmetic: phone battery 15 Wh = 54,000 J; 3 J per step; 10 µW; 200 W panel. No conversion losses counted.', sc_little),
 ('s8', 'The open edge', 'Sources: Nobel Prize in Physics 2011 (Perlmutter, Schmidt, Riess); NASA / Planck 68.3%; DESI DR2 (2025). Inferred values; model-dependent.', sc_edge),
 ('s9', '', '', sc_lesson),
 ('s10', '', '', sc_end),
]
configure(SUBS, SCENES)
if __name__ == '__main__': main()
