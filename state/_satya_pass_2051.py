import json, urllib.request

URLS = [
    'https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?groups=80&limit=300',
    'https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?groups=81&limit=300',
    'https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?limit=300',
]
WANT = ['Toledo','Ball State','Ohio','Kent State','Eastern Michigan','UMass','Massachusetts',
        'Auburn','Tennessee','Florida','Missouri','Kentucky','South Carolina','Ohio State','Iowa',
        'Louisville','NC State','Virginia','Florida State','California','UNLV','Old Dominion',
        'Georgia State','Western Michigan','Buffalo']

seen = set()
for url in URLS:
    try:
        with urllib.request.urlopen(url, timeout=20) as r:
            data = json.load(r)
    except Exception as e:
        print('ERR', url, e)
        continue
    for e in data.get('events', []):
        eid = e.get('id')
        if eid in seen:
            continue
        comp = e['competitions'][0]
        names = ' / '.join(c['team']['displayName'] for c in comp['competitors'])
        if not any(w.lower() in names.lower() for w in WANT):
            continue
        seen.add(eid)
        status = comp['status']['type'].get('detail') or comp['status']['type'].get('description')
        comps = sorted(comp['competitors'], key=lambda c: 0 if c.get('homeAway')=='home' else 1)
        scoreline = ' - '.join(f"{c['team']['abbreviation']} {c.get('score','?')}" for c in comps)
        # prefer homeAway labels
        home = next(c for c in comp['competitors'] if c.get('homeAway')=='home')
        away = next(c for c in comp['competitors'] if c.get('homeAway')=='away')
        score2 = f"{away['team']['abbreviation']} {away.get('score')} @ {home['team']['abbreviation']} {home.get('score')}"
        wp_home = wp_away = None
        sit = comp.get('situation') or {}
        # situation.probability sometimes
        if 'probability' in sit:
            print('sit.probability', sit['probability'])
        # lastPlay probabilities
        lp = sit.get('lastPlay') or {}
        probs = lp.get('probability') if isinstance(lp, dict) else None
        if isinstance(probs, dict):
            wp_home = probs.get('homeWinPercentage')
            wp_away = probs.get('awayWinPercentage')
        # also check competitors for possession
        # winprobability array on competition
        wparr = comp.get('probability') or e.get('probability')
        # fetch summary for wp if missing
        print(f"GAME {e.get('shortName')} | {score2} | {status}")
        print(f"  names={names}")
        if wp_home is not None:
            print(f"  lastPlay WP home={wp_home} away={wp_away}")
        # try summary endpoint
        try:
            surl = f"https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event={eid}"
            with urllib.request.urlopen(surl, timeout=15) as r2:
                summ = json.load(r2)
            wps = summ.get('winprobability') or []
            if wps:
                last = wps[-1]
                # homeWinPercentage typically
                hwp = last.get('homeWinPercentage')
                print(f"  summary last WP homeWinPercentage={hwp} keys={list(last.keys())[:8]}")
            # also predictor
            pred = summ.get('predictor') or {}
            if pred:
                print(f"  predictor home={pred.get('homeTeam',{}).get('gameProjection')} away={pred.get('awayTeam',{}).get('gameProjection')}")
            header = summ.get('header') or {}
            comps2 = ((header.get('competitions') or [{}])[0].get('competitors') or [])
            for c in comps2:
                print(f"  header {c.get('homeAway')} {c.get('team',{}).get('abbreviation')} score={c.get('score')} winner={c.get('winner')}")
        except Exception as ex:
            print('  summary err', ex)
        print()
