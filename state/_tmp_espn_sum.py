import json, urllib.request
ids = ['401858256','401856824','401856716','401858481']
for eid in ids:
    url = f'http://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event={eid}'
    try:
        d = json.load(urllib.request.urlopen(url, timeout=20))
    except Exception as e:
        print(eid, 'ERR', e); continue
    header = d.get('header', {})
    comps = header.get('competitions', [{}])[0]
    print('===', header.get('competitions',[{}])[0].get('competitors',[{},{}])[0].get('team',{}).get('abbreviation'), 'vs', '===')
    print('detail:', comps.get('status',{}).get('type',{}).get('detail'))
    for c in comps.get('competitors', []):
        print(c.get('homeAway'), c.get('team',{}).get('abbreviation'), c.get('score'), 'WP=', (c.get('probability') or {}).get('winPercentage'))
    # also check predictor
    pred = d.get('predictor') or {}
    if pred: print('predictor keys', list(pred.keys())[:8])
    sit = comps.get('situation') or d.get('situation') or {}
    if isinstance(sit, dict):
        print('sit', sit.get('downDistanceText'), sit.get('possessionText'), str((sit.get('lastPlay') or {}).get('text',''))[:100])
