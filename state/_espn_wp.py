import json, urllib.request

def get(url):
    req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0','Accept':'application/json'})
    with urllib.request.urlopen(req, timeout=40) as r:
        return json.load(r)

# find event ids
board = get('https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?groups=80&dates=20261003')
want = {
 'Western Michigan':'WMU','Buffalo':'BUF','West Virginia':'WVU','Iowa State':'ISU',
 'Syracuse':'SYR','Connecticut':'CONN','Toledo':'TOL','Ball State':'BALL'
}
for e in board.get('events',[]):
    n=e.get('name','')
    if not any(k in n for k in want):
        continue
    eid=e['id']
    c=e['competitions'][0]
    s=c['status']['type']
    comps=c['competitors']
    a=next(x for x in comps if x['homeAway']=='away')
    h=next(x for x in comps if x['homeAway']=='home')
    print('EVENT', eid, n, '|', a['team']['abbreviation'], a['score'], '-', h['score'], h['team']['abbreviation'], '|', s.get('detail'))
    # summary for winprob
    try:
        summ=get(f'https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event={eid}')
        wp=summ.get('winprobability') or []
        if wp:
            last=wp[-1]
            print(' WP_LAST', last)
        # header
        hdr=summ.get('header') or {}
        comps2=((hdr.get('competitions') or [{}])[0].get('competitors') or [])
        for x in comps2:
            print(' HDR', x.get('homeAway'), x.get('team',{}).get('abbreviation'), 'score', x.get('score'), 'prob', x.get('probability'))
        # predictor
        pred=summ.get('predictor') or {}
        if pred:
            print(' PREDICTOR', {k:pred.get(k) for k in list(pred)[:8]})
        sit=summ.get('situation') or (c.get('situation') or {})
        if sit:
            print(' DOWN', sit.get('downDistanceText'), 'clock', sit.get('clock'), 'poss', (sit.get('possession') or ''))
    except Exception as ex:
        print(' summary err', ex)
    print()
