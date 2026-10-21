import json, urllib.request, re

# load live board prices
board = open(r'C:\Users\lilli\AI-Shared\state\live-board.md', encoding='utf-8', errors='replace').read()
prices = {}
for line in board.splitlines():
    m = re.search(r'`(aec-cfb-[^`]+)`\s*\|\s*[^0-9]*([0-9.]+)/([0-9.]+)', line)
    if m:
        prices[m.group(1)] = (float(m.group(2)), float(m.group(3)))

# map slug tokens to espn abbrevs roughly via dry-run books instead
# pull fresh books via polymarket is hard; use scoreboard + known slugs
SLUGS = {
    'aec-cfb-aubrn-tenn-2026-10-03': ('AUB', 'TENN'),
    'aec-cfb-cah-unlv-2026-10-03': ('CAL', 'UNLV'),
    'aec-cfb-emich-umass-2026-10-03': ('EMU', 'MASS'),
    'aec-cfb-fl-missr-2026-10-03': ('FLA', 'MIZ'),
    'aec-cfb-lou-ncst-2026-10-03': ('LOU', 'NCSU'),
    'aec-cfb-ohio-kentst-2026-10-03': ('OHIO', 'KENT'),
    'aec-cfb-ohiost-iowa-2026-10-03': ('OSU', 'IOWA'),
    'aec-cfb-old-gast-2026-10-03': ('ODU', 'GAST'),
    'aec-cfb-toledo-ballst-2026-10-03': ('TOL', 'BALL'),
    'aec-cfb-uk-sc-2026-10-03': ('UK', 'SC'),
    'aec-cfb-vir-flst-2026-10-03': ('UVA', 'FSU'),
}

url = 'https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?limit=300'
data = json.load(urllib.request.urlopen(url, timeout=20))
games = {}
for e in data['events']:
    comp = e['competitions'][0]
    away = next(c for c in comp['competitors'] if c['homeAway']=='away')
    home = next(c for c in comp['competitors'] if c['homeAway']=='home')
    a = away['team']['abbreviation']
    h = home['team']['abbreviation']
    # normalize MASS
    if a == 'MA': a = 'MASS'
    if h == 'MA': h = 'MASS'
    eid = e['id']
    st = comp['status']['type'].get('detail') or ''
    if 'Final' in st or 'Scheduled' in st or 'EDT' in st or 'PM' in st and 'Quarter' not in st and 'Half' not in st:
        # keep finals out unless needed
        if 'Quarter' not in st and 'Half' not in st and 'End' not in st and 'Final' not in st:
            continue
    try:
        summ = json.load(urllib.request.urlopen(
            f'https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event={eid}', timeout=15))
        wps = summ.get('winprobability') or []
        hwp = wps[-1]['homeWinPercentage'] if wps else None
    except Exception:
        hwp = None
    games[(a,h)] = {
        'score': f"{a} {away.get('score')} @ {h} {home.get('score')}",
        'st': st,
        'awayWP': (1-hwp) if hwp is not None else None,
        'homeWP': hwp,
        'short': e.get('shortName'),
    }

print('EDGE SCAN')
for slug, (a,h) in SLUGS.items():
    g = games.get((a,h)) or games.get((h,a))
    # try alt abbrevs
    if not g:
        for (aa,hh), gg in games.items():
            if {aa,hh} == {a,h} or a in (aa,hh) and h in (aa,hh):
                g = gg
                break
    bidask = prices.get(slug)
    if not g:
        print(f'{slug}: no espn match board={bidask}')
        continue
    yes_ask = bidask[1] if bidask else None
    # YES is first side in board = typically the slug's first team token side
    # From desk-trade: aubrn-tenn YES=Tigers(Auburn), cah-unlv YES=Golden Bears(CAL),
    # emich YES=Eagles(EMU), fl YES=Gators(FLA), lou YES=Cardinals(LOU),
    # ohio YES=Bobcats(OHIO), ohiost YES=Buckeyes(OSU), old YES=Monarchs(ODU),
    # toledo YES=Rockets(TOL), uk YES=Wildcats(UK), vir YES=Cavaliers(UVA)
    first = {
        'aec-cfb-aubrn-tenn-2026-10-03': 'AUB',
        'aec-cfb-cah-unlv-2026-10-03': 'CAL',
        'aec-cfb-emich-umass-2026-10-03': 'EMU',
        'aec-cfb-fl-missr-2026-10-03': 'FLA',
        'aec-cfb-lou-ncst-2026-10-03': 'LOU',
        'aec-cfb-ohio-kentst-2026-10-03': 'OHIO',
        'aec-cfb-ohiost-iowa-2026-10-03': 'OSU',
        'aec-cfb-old-gast-2026-10-03': 'ODU',
        'aec-cfb-toledo-ballst-2026-10-03': 'TOL',
        'aec-cfb-uk-sc-2026-10-03': 'UK',
        'aec-cfb-vir-flst-2026-10-03': 'UVA',
    }[slug]
    if g['awayWP'] is None:
        print(f"{slug}: {g['score']} {g['st']} no WP book={yes_ask}")
        continue
    # map first team to WP
    # need which of a/h is first
    # use score string
    awp, hwp = g['awayWP'], g['homeWP']
    # determine away/home abbrev from score
    parts = g['score'].split()
    away_ab, home_ab = parts[0], parts[3]
    if first == away_ab:
        ywp = awp
    elif first == home_ab:
        ywp = hwp
    else:
        # fuzzy
        ywp = awp if first in away_ab or away_ab in first else hwp
    gap = (ywp - yes_ask) if yes_ask is not None else None
    print(f"{slug}: {g['score']} | {g['st']} | YES({first}) WP={ywp:.3f} ask={yes_ask} gap={gap:+.3f}" if gap is not None else f"{slug}: {g['score']} WP={ywp}")
