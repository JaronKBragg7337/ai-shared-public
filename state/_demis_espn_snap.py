import json, urllib.request

def board(path, label):
    url = f'https://site.api.espn.com/apis/site/v2/sports/{path}'
    with urllib.request.urlopen(url, timeout=20) as r:
        data = json.load(r)
    print('===', label, '===')
    for ev in data.get('events', []):
        comp = ev['competitions'][0]
        st = comp['status']['type']
        detail = st.get('detail') or st.get('description')
        parts = []
        for c in comp['competitors']:
            parts.append(f"{c['team']['abbreviation']} {c.get('score','?')} ({c['homeAway']})")
        print(' | '.join(parts), '|', detail)
        sit = comp.get('situation') or {}
        if sit:
            print('  sit:', {k: sit.get(k) for k in ('possession','downDistanceText','lastPlay') if k in sit or True})
        odds = comp.get('odds') or []
        if odds:
            o = odds[0]
            print('  odds keys', list(o.keys())[:12])
            for k in ('homeWinPercentage','awayWinPercentage','tiePercentage','overUnder','spread'):
                if k in o:
                    print(f'  {k}={o[k]}')

board('hockey/nhl/scoreboard', 'NHL')
board('basketball/wnba/scoreboard', 'WNBA')
board('baseball/mlb/scoreboard', 'MLB')
board('basketball/nba/scoreboard', 'NBA')
