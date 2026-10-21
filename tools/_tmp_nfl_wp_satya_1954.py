import json, urllib.request

def get(url):
    return json.loads(urllib.request.urlopen(url, timeout=25).read())

data = get('https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard')
for ev in data.get('events', []):
    comp = ev['competitions'][0]
    st = comp['status']['type']
    if st.get('state') != 'in':
        continue
    detail = st.get('detail', '')
    teams = {}
    for t in comp['competitors']:
        abbr = t['team']['abbreviation']
        teams[abbr] = {
            'score': t['score'],
            'homeAway': t['homeAway'],
            'winner': t.get('winner'),
        }
    # summary endpoint often has win probability
    eid = ev['id']
    wp = {}
    try:
        summ = get(f'https://site.api.espn.com/apis/site/v2/sports/football/nfl/summary?event={eid}')
        # look in predictor / winprobability
        pred = summ.get('predictor') or {}
        if pred:
            ha = pred.get('homeTeam', {})
            aa = pred.get('awayTeam', {})
            wp['home_pred'] = ha.get('gameProjection') or ha.get('teamChanceLoss')
            wp['away_pred'] = aa.get('gameProjection') or aa.get('teamChanceLoss')
        wparr = summ.get('winprobability') or []
        if wparr:
            last = wparr[-1]
            wp['homeWinPercentage'] = last.get('homeWinPercentage')
            wp['tiePercentage'] = last.get('tiePercentage')
            wp['playId'] = last.get('playId')
        # also situation
        sit = summ.get('situation') or comp.get('situation') or {}
        if sit:
            wp['lastPlay'] = (sit.get('lastPlay') or {}).get('text')
            wp['possession'] = (sit.get('possession') or '')
    except Exception as e:
        wp['err'] = str(e)
    away = next(a for a,v in teams.items() if v['homeAway']=='away')
    home = next(a for a,v in teams.items() if v['homeAway']=='home')
    print(f"{away} {teams[away]['score']} @ {home} {teams[home]['score']} | {detail}")
    print('  wp:', json.dumps(wp))
