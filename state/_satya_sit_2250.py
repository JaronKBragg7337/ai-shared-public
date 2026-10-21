import json, urllib.request
def get(u):
    r = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
    return json.load(urllib.request.urlopen(r, timeout=25))
for eid in ['401872975','401872974']:
    d = get(f'https://site.web.api.espn.com/apis/site/v2/sports/football/nfl/summary?event={eid}')
    comp = d['header']['competitions'][0]
    print('EVENT', eid, [(c['team']['abbreviation'], c.get('score'), c['homeAway'], c['team'].get('id')) for c in comp['competitors']], comp.get('status',{}).get('type',{}).get('detail'))
    sit = d.get('situation') or comp.get('situation') or {}
    print(' SIT', {k: sit.get(k) for k in ['downDistanceText','possession','possessionText','isRedZone','shortDownDistanceText']})
    wp = d.get('winprobability', [])
    for w in wp[-3:]:
        print(' WP', w.get('homeWinPercentage'), w.get('playId'))
    drives = (d.get('drives') or {})
    cur = drives.get('current') or {}
    print(' DRIVE', cur.get('description'), (cur.get('team') or {}).get('abbreviation'))
    plays = cur.get('plays') or []
    for p in plays[-3:]:
        print('  PLAY', (p.get('text') or '')[:160])
