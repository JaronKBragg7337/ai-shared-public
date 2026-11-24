import json, sys, re; sys.path.insert(0, '../../tv-lib')
from tvlib import *
import tvlib

def at(sid, f): return SEG[sid]['start'] + f * SEG[sid]['dur'] - tvlib.BOUND[sid][0]

def rails(cv, t, y, a=1.0, n=40):
    for i in range(-1, n):
        xx = i * 44 - (t * 60) % 44
        cv.line([(xx, y + 20), (xx + 20, y + 36)], mix((70, 54, 40), BG, a), 5)
    for dy in (14, 34): cv.line([(0, y + dy), (W, y + dy)], mix((120, 132, 150), BG, a), 4)

def bullet(cv, x, y):
    s = 1.0 if PORT else 1.35; L = 560 * s
    cv.rect((x, y - 44 * s, x + L, y - 6 * s), (232, 236, 242), 10)
    cv.rect((x, y - 26 * s, x + L, y - 18 * s), TEAL, 2)
    for k in range(9): cv.rect((x + 40 * s + k * 52 * s, y - 38 * s, x + 66 * s + k * 52 * s, y - 28 * s), (40, 60, 90), 2)
    cv.poly([(x + L - 4, y - 44 * s), (x + L + 90 * s, y - 14 * s), (x + L + 90 * s, y - 6 * s), (x + L - 4, y - 6 * s)], (232, 236, 242))
    for w in (60, 160, 300, 420, 520): cv.circ((x + w * s, y - 4 * s), 5 * s, (15, 20, 30))

def sc_title(cv, t, p):
    title_block(cv, t, 'HISTORY', '7  ·  SEQUEL TO EPISODE 6', 'What if America had', 'high-speed rail?', '')
    cv.text((W / 2, 540 if PORT else 372), 'A viewer asked: not freight, travel.', 'serifr', 44, DIM, 'ma', ease((t - 1.0) / 1.0))
    a2 = ease((t - at('s1', 0.6)) / 0.8)
    cv.para(W / 2, 700 if PORT else 440, 'Like Europe and Asia. Every trip time here is an estimate.', 'serif', 60 if PORT else 56, AMBER, W - 160, 1.2, 'm', a2)
    ry = 1000 if PORT else 640
    rails(cv, t, ry, ease(t / 1.5))
    bullet(cv, -900 + (min(t, 5.0) / 5.0) * (W + 1300), ry + 14)

def sc_who(cv, t, p):
    stat_cards(cv, t, [
        dict(num='1964', label='Japan opens the Shinkansen', sub='about 2,950 km today; trains up to 320 km/h', at=at('s2', 0.04)),
        dict(num='1981', label='France: the TGV begins', sub='about 2,800 km of high-speed line (2021)', col=BLUE, at=at('s2', 0.26)),
        dict(num='~4,000 km', label='Spain: largest in Europe', sub='about 3,970 km in 2024; 4,090 reported 2025', col=TEAL, at=at('s2', 0.45)),
        dict(num='50,000+ km', label='China: largest in the world', sub='end of 2025, per China Railway', col=RED, at=at('s2', 0.68))])

def sc_bench(cv, t, p):
    cv.text((W / 2, CONT[1] + 10), '320 mi ÷ 2 h 21 min', 'serif', 84 if not PORT else 72, TXT, 'ma', ease(t / 0.8))
    cv.text((W / 2, CONT[1] + (125 if not PORT else 115)), '≈ 136 mph average, stops included', 'serif', 64 if not PORT else 54, AMBER, 'ma', ease((t - at('s3', 0.3)) / 0.8))
    hbars(cv, t, [
        dict(label='Tokyo to Osaka (Nozomi)', val=136, txt='136 mph', at=at('s3', 0.45), col=AMBER),
        dict(label='Brightline Florida (Miami to Orlando)', val=69, txt='69 mph', at=at('s3', 0.78), col=STEEL)],
        150, area=(CONT[0] + 20, CONT[1] + (260 if not PORT else 250), CONT[2] - 20, CONT[1] + (560 if not PORT else 700)), label_w=(520 if not PORT else 330))
    note(cv, t, at('s3', 0.85), '515 km = 320 mi. Averages include station stops. 69 mph is the route average, not top speed.', CONT[3] - (60 if not PORT else 120), DIM, 28)

def sc_trips(cv, t, p):
    stat_cards(cv, t, [
        dict(num='≈ 7 h', label='New York to Chicago', sub='959 rail mi ÷ 136 mph. At 69 mph: ~14 h. Amtrak today: about 20 h.', tag='ESTIMATE', at=at('s4', 0.2)),
        dict(num='≈ 2.8 h', label='Los Angeles to San Francisco', sub='380 road mi ÷ 136 mph. At 69 mph: ~5.5 h.', col=TEAL, tag='ESTIMATE', at=at('s4', 0.45)),
        dict(num='≈ 2.3 h', label='Chicago, Fort Wayne, Detroit', sub='158 + 156 = 314 road mi ÷ 136 mph. At 69 mph: ~4.6 h.', col=BLUE, tag='ESTIMATE', at=at('s4', 0.7))],
        area=(CONT[0], CONT[1], CONT[2], CONT[3] - 70))
    note(cv, t, at('s4', 0.85), "California's own legal target for its line: San Francisco to LA in 2 h 40 min, nonstop.", CONT[3] - 40, DIM, 28)

def reasons(cv, t, items):
    x0, y0, x1, y1 = CONT; n = len(items); step = (y1 - y0) / n
    for i, (at_, lab, det, col) in enumerate(items):
        a = ease((t - at_) / 0.6)
        if a <= 0: continue
        y = y0 + i * step
        cv.rect((x0, y + 6, x1, y + step - 6), mix(CARD, BG, a), 16)
        if PORT:
            cv.text((x0 + 28, y + 22), lab, 'serif', 44, col, 'la', a)
            cv.para(x0 + 28, y + 78, det, 'sans', 30, TXT, x1 - x0 - 56, 1.18, 'l', a)
        else:
            cv.text((x0 + 30, y + step / 2 - 6), lab, 'serif', 42, col, 'lm', a)
            cv.para(x0 + 560, y + step / 2 - 38, det, 'sans', 32, TXT, x1 - x0 - 600, 1.18, 'l', a)

def sc_why(cv, t, p):
    reasons(cv, t, [
        (at('s5', 0.08), 'Distance & density', 'Many US city pairs are far apart; the Northeast corridor is the dense exception. (Argued, not measured here.)', AMBER),
        (at('s5', 0.25), 'Highways & airlines', 'Interstate system authorized 1956 (FHWA); air travel grew too.', TEAL),
        (at('s5', 0.42), 'Land & cost', "California's Merced to Bakersfield segment: about $35 to $37 billion estimated.", BLUE),
        (at('s5', 0.6), 'Politics & funding', "Projects outlast election cycles; California's inspector general called its 2026 plan incomplete.", RED),
        (at('s5', 0.78), 'Freight owns the tracks', 'Amtrak owns 623 route miles; over 70% of its travel is on freight-owned track (AAR).', STEEL)])

def sc_now(cv, t, p):
    stat_cards(cv, t, [
        dict(num='Aug 2025', label='Acela: new Avelia Liberty trains', sub='rated 160 mph; track limits actual speed', at=at('s6', 0.06)),
        dict(num='Sept 2023', label='Brightline: Miami to Orlando', sub='235 mi; up to 125 mph on part; avg ~69 mph', col=TEAL, at=at('s6', 0.28)),
        dict(num='Late 2029', label='Brightline West: Las Vegas to Rancho Cucamonga', sub="218 mi; under construction; company's target", col=BLUE, at=at('s6', 0.5)),
        dict(num='2032', label='California HSR: Merced to Bakersfield', sub='target; no date for San Francisco to LA', col=RED, at=at('s6', 0.75))])

def sc_unknown(cv, t, p):
    x0 = CONT[0] + 30; w = CONT[2] - CONT[0] - 60
    cv.text((x0, CONT[1] + 10), 'Known', 'serif', 52, TEAL, 'la', ease(t / 0.6))
    y = cv.para(x0, CONT[1] + 80, "Japan, France, Spain and China run fast passenger lines. At Japan's pace, big US trips would be several hours shorter. America's newest big project has no riders yet.", 'sans', 36, TXT, w, 1.2, 'l', ease((t - 0.4) / 0.8))
    cv.text((x0, y + 30), 'Not known', 'serif', 52, RED, 'la', ease((t - at('s7', 0.4)) / 0.6))
    cv.para(x0, y + 100, 'Would American demand fill fast trains? What would routes really cost? Would these estimates hold with real stops and real track?', 'sans', 36, TXT, w, 1.2, 'l', ease((t - at('s7', 0.45)) / 0.8))
    badge(cv, x0, CONT[3] - 70, 'Estimates are math, not forecasts', AMBER, ease((t - at('s7', 0.85)) / 0.6), 30)

def sc_end(cv, t, p):
    end_block(cv, t, 'History', 7, ['Wikipedia: Shinkansen, High-speed rail in France/China/Spain, Brightline, California HSR, Avelia Liberty · JR Central (Nozomi)',
        'Adif / Majorca Daily Bulletin (Spain) · China Railway via Global Times · AAR, Integrated Rail Network · FHWA, Act of 1956',
        'California High-Speed Rail Authority; Legislative inspector general review of 2026 plan · Brightline West (company)',
        'Trip times are our estimates: distance ÷ speed'])

def _norm(s):
    for a, b in (('nineteen sixty four', '1964'), ('nineteen eighty one', '1981'), ('twenty nine hundred fifty', '2,950'), ('twenty eight hundred', '2,800'),
                 ('four thousand', '4,000'), ('over fifty thousand', 'over 50,000'), ('twenty twenty five', '2025'), ('three hundred twenty', '320'),
                 ('two hours twenty one minutes', '2 hours 21 minutes'), ('one hundred thirty six', '136'), ('sixty nine', '69'),
                 ('nine hundred fifty nine', '959'), ('three hundred eighty', '380'), ('three hundred fourteen', '314'), ('two point eight', '2.8'), ('two point three', '2.3'),
                 ('nineteen fifty six', '1956'), ('thirty five to thirty seven billion', '35 to 37 billion'), ('six hundred twenty three', '623'), ('over seventy percent', 'over 70%'),
                 ('twenty twenty three', '2023'), ('one hundred sixty', '160'), ('two hundred eighteen', '218'), ('twenty twenty nine', '2029'), ('twenty thirty two', '2032'),
                 ('one hundred miles', '100 miles')):
        s = s.replace(a, b)
    return s

def _subs():
    out = {}
    for d in json.load(open('script.json', encoding='utf-8')):
        t = _norm(d['text'])
        out[d['id']] = [] if d['id'] == 's8' else [x.strip() for x in re.findall(r'.+?(?:[.!?:](?=\s|$))', t)]
    return out

SUBS = _subs()
SCENES = [
 ('s1', '', '', sc_title),
 ('s2', 'Who already has it', 'Sources: Wikipedia (Shinkansen 2,951 km; France ~2,800 km, 2021); Adif via reports (Spain); China Railway via Global Times (50,000 km, end 2025).', sc_who),
 ('s3', 'The benchmark', 'Sources: JR Central / Wikipedia Nozomi (515 km, 2 h 21 min); Wikipedia Brightline (235 mi, avg 69 mph). Our math: 320 ÷ 2.35 h.', sc_bench),
 ('s4', 'Rough trips at that pace', 'Estimates, not forecasts: distance ÷ speed. Distances: Amtrak Lake Shore Ltd 959 mi; road miles for the rest; Prop 1A (CA).', sc_trips),
 ('s5', 'Why not here?', 'Sources: FHWA (1956); AAR; California High-Speed Rail Authority and legislative inspector general (2026). Reasons are argued, not settled.', sc_why),
 ('s6', 'What exists or is coming', 'Sources: Wikipedia (Avelia Liberty, Brightline); Brightline West (company, Jan 2026); California High-Speed Rail Authority (2032 target).', sc_now),
 ('s7', "What we know, and don't", 'Known: the record above. Not known: whether it would work here.', sc_unknown),
 ('s8', '', '', sc_end),
]
configure(SUBS, SCENES)
if __name__ == '__main__': main()
