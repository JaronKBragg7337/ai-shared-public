import json, sys, re; sys.path.insert(0, '../../tv-lib')
from tvlib import *
import tvlib

def at(sid, f): return SEG[sid]['start'] + f * SEG[sid]['dur'] - tvlib.BOUND[sid][0]

def rails(cv, t, y, a=1.0, n=40):
    for i in range(-1, n):
        xx = i * 44 - (t * 60) % 44
        cv.line([(xx, y + 20), (xx + 20, y + 36)], mix((70, 54, 40), BG, a), 5)
    for dy in (14, 34): cv.line([(0, y + dy), (W, y + dy)], mix((120, 132, 150), BG, a), 4)

def train(cv, x, y):
    s = 1.0 if PORT else 1.35; cars = 5; cx = x
    for i in range(cars):
        cv.rect((cx, y - 34 * s, cx + 62 * s, y - 6 * s), AMBER if i % 2 == 0 else (205, 140, 40), 2)
        for w in (10, 50): cv.circ((cx + w * s, y - 4 * s), 4.5 * s, (15, 20, 30))
        cx += 66 * s
    cv.rect((cx, y - 40 * s, cx + 70 * s, y - 6 * s), (200, 70, 50), 3)
    cv.rect((cx + 40 * s, y - 56 * s, cx + 70 * s, y - 38 * s), (200, 70, 50), 3)
    for w in (12, 34, 58): cv.circ((cx + w * s, y - 5 * s), 5.5 * s, (15, 20, 30))

def sc_title(cv, t, p):
    title_block(cv, t, 'HISTORY', '6  ·  SEQUEL TO EPISODE 1', 'What if America kept', 'building railroads?', '')
    cv.text((W / 2, 540 if PORT else 372), 'A viewer asked. You are not alone if you wondered too.', 'serifr', 44, DIM, 'ma', ease((t - 1.0) / 1.0))
    a2 = ease((t - at('s1', 0.62)) / 0.8)
    cv.para(W / 2, 700 if PORT else 440, 'America never stopped building railroads.', 'serif', 64 if PORT else 60, AMBER, W - 160, 1.2, 'm', a2)
    ry = 1000 if PORT else 640
    rails(cv, t, ry, ease(t / 1.5))
    train(cv, -520 + (min(t, 6.0) / 6.0) * (W + 700), ry + 14)

def sc_peak(cv, t, p):
    hbars(cv, t, [
        dict(label='1916 peak', val=254, txt='254,000 mi', at=at('s2', 0.12), col=AMBER),
        dict(label='Today (freight network)', val=135, txt='135,000 mi', at=at('s2', 0.38), col=STEEL)],
        254, area=(CONT[0] + 20, CONT[1] + 40, CONT[2] - 20, CONT[1] + (400 if not PORT else 560)), label_w=(480 if not PORT else 330))
    note(cv, t, at('s2', 0.8), "Different definitions: 1916 is route-miles (ICC); today is AAR's network count. Rough comparison.", CONT[3] - (90 if not PORT else 150), DIM, 30)

def sc_why(cv, t, p):
    stat_cards(cv, t, [
        dict(num='1956', label='Interstate system authorized', sub='41,000 miles', at=at('s3', 0.12)),
        dict(num='107k to 49k', label='Intercity passenger route-miles', sub='1958 to 1970; Amtrak took over in 1971', col=RED, at=at('s3', 0.34)),
        ])

def sc_staggers(cv, t, p):
    stat_cards(cv, t, [
        dict(num='1980', label='Staggers Rail Act', sub='price contracts; drop money-losing routes', at=at('s4', 0.1)),
        dict(num='−46%', label='Inflation-adjusted rail rates', sub='2025 vs 1981 (industry figure, AAR)', col=TEAL, at=at('s4', 0.55))])

def sc_freight(cv, t, p):
    x0 = CONT[0] + 30; x1 = CONT[2] - 30; w = x1 - x0
    cv.text((W / 2, CONT[1] + 10), '~40%', 'serif', 150, AMBER, 'ma', ease(t / 1.0))
    cv.text((W / 2, CONT[1] + 190), 'of long-distance freight, in ton-miles', 'sans', 40, TXT, 'ma', ease(t / 1.0))
    by = CONT[1] + (300 if not PORT else 350); bh = 120
    f = ease((t - at('s5', 0.1)) / 1.6)
    cv.rect((x0, by, x1, by + bh), mix(STEEL, BG, 0.55), 10)
    cv.rect((x0, by, x0 + w * 0.40 * f, by + bh), AMBER, 10)
    if f > 0.99:
        cv.text((x0 + w * 0.2, by + bh / 2), 'Freight rail', 'sansb', 38, BG, 'mm')
        cv.text((x0 + w * 0.7, by + bh / 2), 'All other modes', 'sansb', 38, TXT, 'mm')
    a = ease((t - at('s5', 0.6)) / 0.8)
    cv.text((W / 2, by + bh + 50), '≈ $25 billion a year invested in the network', 'sansb', 38, TEAL, 'ma', a)
    cv.text((W / 2, by + bh + 105), '(industry figure, AAR)', 'sans', 30, DIM, 'ma', a)

def sc_building(cv, t, p):
    stat_cards(cv, t, [
        dict(num='$25B / yr', label='Freight railroads invest in their networks', sub='AAR industry figure', at=at('s6', 0.08)),
        dict(num='Sept 2023', label='Brightline opens Miami to Orlando', sub='Florida, about 235 miles', col=TEAL, at=at('s6', 0.27)),
        dict(num='Late 2029', label='Brightline West, Las Vegas to S. California', sub="under construction; company's target", col=BLUE, at=at('s6', 0.5)),
        dict(num='66', label='California high-speed rail structures finished', sub='first 119 miles, Central Valley; no service date', col=RED, at=at('s6', 0.75))])

def sc_elsewhere(cv, t, p):
    stat_cards(cv, t, [
        dict(num='1964', label='Japan opens the Shinkansen', sub='ministry: no passenger deaths from train accidents', at=at('s7', 0.1)),
        dict(num='50,000+ km', label='China high-speed rail, end of 2025', sub='per China Railway', col=RED, at=at('s7', 0.55))],
        area=(CONT[0], CONT[1], CONT[2], CONT[3] - 70))
    note(cv, t, at('s6', 0.75), 'Shinkansen lines total roughly 2,900 km; counts vary by definition.', CONT[3] - 40, DIM, 28)

def sc_unknown(cv, t, p):
    x0 = CONT[0] + 30; w = CONT[2] - CONT[0] - 60
    cv.text((x0, CONT[1] + 10), 'Known', 'serif', 52, TEAL, 'la', ease(t / 0.6))
    y = cv.para(x0, CONT[1] + 80, 'America never stopped building rail. Peak near 254,000 miles in 1916; roads, air and rules shrank the network. Freight carries about 40% of long-distance ton-miles. New lines are under construction.', 'sans', 36, TXT, w, 1.2, 'l', ease((t - 0.4) / 0.8))
    cv.text((x0, y + 30), 'Not known', 'serif', 52, RED, 'la', ease((t - at('s8', 0.25)) / 0.6))
    cv.para(x0, y + 100, "Would more track have paid off, or sat empty beside highways? Would Japan's or China's results carry over to America?", 'sans', 36, TXT, w, 1.2, 'l', ease((t - at('s8', 0.3)) / 0.8))
    badge(cv, x0, CONT[3] - 70, 'The question: what kind of rail, not whether', AMBER, ease((t - at('s8', 0.8)) / 0.6), 30)

def sc_end(cv, t, p):
    end_block(cv, t, 'History', 6, ['AAR, Freight Rail Facts & Figures; Staggers Rail Act of 1980 (AAR)',
        'ICC / U.S. Census, Historical Statistics (1916 route-miles) · FHWA, Federal-Aid Highway Act of 1956',
        'Amtrak history, Rail Passenger Service Act 1970 · Brightline, Brightline West · California High-Speed Rail Authority',
        'Japan MLIT (Shinkansen safety) · China Railway via Global Times (2025)'])

def _norm(s):
    for a, b in (('nineteen sixteen', '1916'), ('two hundred fifty four thousand', '254,000'), ('one hundred thirty five thousand', '135,000'),
                 ('nineteen fifty six', '1956'), ('forty one thousand', '41,000'), ('one hundred seven thousand', '107,000'), ('nineteen fifty eight', '1958'),
                 ('forty nine thousand', '49,000'), ('nineteen seventy one', '1971'), ('nineteen seventy eight', '1978'), ('nineteen seventy', '1970'),
                 ('nineteen eighty one', '1981'), ('nineteen eighty', '1980'), ('twenty twenty five', '2025'), ('nineteen sixty four', '1964'),
                 ('fifty thousand', '50,000'), ('twenty twenty three', '2023'), ('twenty twenty nine', '2029'), ('sixty six', '66'), ('one hundred nineteen', '119'), ('twenty five billion', '25 billion'), ('forty six percent', '46%'), ('forty percent', '40%')):
        s = s.replace(a, b)
    return s

def _subs():
    out = {}
    for d in json.load(open('script.json', encoding='utf-8')):
        t = _norm(d['text'])
        out[d['id']] = [] if d['id'] == 's9' else [x.strip() for x in re.findall(r'[^.!?]+[.!?]+', t)]
    return out

SUBS = _subs()
SCENES = [
 ('s1', '', '', sc_title),
 ('s2', 'The peak, and today', 'Sources: ICC / Census Historical Statistics (254,037 route-miles, 1916); AAR (network "nearly 135,000 miles"). Definitions differ.', sc_peak),
 ('s3', 'Why lines went quiet', 'Sources: FHWA (Federal-Aid Highway Act, 1956); Amtrak history; Rail Passenger Service Act (1970).', sc_why),
 ('s4', 'The Staggers Act', "Source: AAR, Staggers Rail Act of 1980. Rate figure is the industry's own.", sc_staggers),
 ('s5', 'What survived: freight', 'Source: AAR, Freight Rail Facts & Figures (about 40% of long-distance ton-miles; $25B/yr).', sc_freight),
 ('s6', 'Still being built', 'Sources: AAR ($25B/yr); Brightline (service began Sept 22, 2023); Brightline West (company: late 2029; reported Jan 2026); California High-Speed Rail Authority (Oct 2026).', sc_building),
 ('s7', 'Building elsewhere', 'Sources: Japan MLIT (Shinkansen); China Railway, reported by Global Times (Dec 2025). Different countries, different costs.', sc_elsewhere),
 ('s8', "What we don't know", 'A counterfactual: what we know is the record above; the rest is open.', sc_unknown),
 ('s9', '', '', sc_end),
]
configure(SUBS, SCENES)
if __name__ == '__main__': main()
