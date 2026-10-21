import json, urllib.request, re, pathlib
from datetime import datetime, timezone

# Recent desk-trade lines for open Satya positions
trail = pathlib.Path(r'C:\Users\lilli\AI-Shared\state\desk-trade.md').read_text(encoding='utf-8', errors='replace')
lines = [l for l in trail.splitlines() if 'satya' in l.lower() or 'demis' in l.lower() or 'ORST' in l or 'BYU' in l or 'ohio' in l.lower() or '#1057' in l or '#1060' in l or 'txtech' in l or 'wash-usc' in l]
print('=== RECENT DESK HITS ===')
for l in lines[-40:]:
    print(l[:300])

# ESPN scoreboard CFB
url = 'https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard'
with urllib.request.urlopen(url, timeout=20) as r:
    data = json.load(r)
print('\n=== ESPN CFB LIVE ===')
want = ['byu','tcu','oregon state','colorado state','texas tech','colorado','washington','usc','kentucky','south carolina','utah state','boise','miami','clemson']
for ev in data.get('events', []):
    name = ev.get('name','')
    status = ev.get('status',{}).get('type',{}).get('description','')
    comps = ev.get('competitions',[{}])[0]
    competitors = comps.get('competitors',[])
    scores = {c['team']['displayName']: c.get('score') for c in competitors}
    low = name.lower()
    if not any(w in low for w in want):
        continue
    # win probability
    wp = None
    for c in competitors:
        if 'probability' in str(c).lower() or c.get('statistics'):
            pass
    # sitd winprob from situation
    sit = comps.get('situation',{}) or {}
    # try probability endpoint fields
    probs = {}
    for c in competitors:
        home = c.get('homeAway')
        team = c['team']['abbreviation']
        # some boards embed winprobability
        if 'winprobability' in c:
            probs[team] = c['winprobability']
    # detailed: fetch summary
    eid = ev.get('id')
    wp_str = ''
    try:
        su = f'https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event={eid}'
        with urllib.request.urlopen(su, timeout=15) as r2:
            sdata = json.load(r2)
        wpr = sdata.get('winprobability') or []
        if wpr:
            last = wpr[-1]
            home_wp = last.get('homeWinPercentage')
            # identify home
            home_team = next((c['team']['abbreviation'] for c in competitors if c.get('homeAway')=='home'), '?')
            away_team = next((c['team']['abbreviation'] for c in competitors if c.get('homeAway')=='away'), '?')
            wp_str = f' homeWP={home_wp:.3f} ({home_team}) awayWP={1-home_wp:.3f} ({away_team})'
        elif 'predictor' in sdata:
            pred = sdata['predictor']
            wp_str = f" predictor home={pred.get('homeTeam',{}).get('gameProjection')} away={pred.get('awayTeam',{}).get('gameProjection')}"
    except Exception as e:
        wp_str = f' wp_err={e}'
    print(f"{name} | {status} | {scores}{wp_str}")
