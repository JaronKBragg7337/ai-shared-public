import json, urllib.request

def get(u):
    r = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
    return json.load(urllib.request.urlopen(r, timeout=25))

sb = get('https://site.web.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard')
for e in sb.get('events', []):
    comp = e['competitions'][0]
    st = comp['status']['type']
    if st.get('completed') or st.get('state') == 'pre':
        continue
    eid = e['id']
    teams = sorted(comp['competitors'], key=lambda t: 0 if t['homeAway']=='home' else 1)
    line = []
    for t in comp['competitors']:
        line.append(f"{t['team']['abbreviation']}{t.get('score','?')}({t['homeAway']})")
    print(f"EVENT {eid} {e['name']} | {' '.join(line)} | {st.get('detail')}")
    try:
        d = get(f'https://site.web.api.espn.com/apis/site/v2/sports/football/nfl/summary?event={eid}')
        wp = d.get('winprobability', [])
        if wp:
            hwp = float(wp[-1]['homeWinPercentage'])
            print(f"  HOME_WP {hwp:.3f} AWAY_WP {1.0-hwp:.3f}")
            for t in d['header']['competitions'][0]['competitors']:
                abbr = t['team']['abbreviation']
                ha = t['homeAway']
                sc = t.get('score')
                p = hwp if ha=='home' else (1.0-hwp)
                print(f"  {abbr} {ha} score={sc} wp={p:.3f}")
        else:
            print('  no winprobability')
    except Exception as ex:
        print('  ERR', ex)
