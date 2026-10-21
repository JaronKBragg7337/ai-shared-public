import urllib.request, json

def get(url):
    with urllib.request.urlopen(url, timeout=25) as r:
        return json.load(r)

for eid, label in [('401858254','FSU-LOU'), ('401868265','COLU-MRST')]:
    data=get('https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event='+eid)
    hdr=data.get('header',{})
    comps=hdr.get('competitions',[{}])[0]
    status=comps.get('status',{}).get('type',{})
    print('===', label, '===')
    print('status:', status.get('detail'), status.get('state'))
    for t in comps.get('competitors', []):
        print(t.get('homeAway'), t.get('team',{}).get('abbreviation'), 'score', t.get('score'), 'prob', t.get('probability',{}).get('winPercentage') if isinstance(t.get('probability'), dict) else t.get('probability'))
    sit=data.get('situation') or {}
    print('situation possession', (sit.get('possession') or ''), 'downDist', sit.get('downDistanceText'), 'lastPlay', (sit.get('lastPlay') or {}).get('text') if isinstance(sit.get('lastPlay'), dict) else sit.get('lastPlay'))
    # win probability from predictor if present
    pred=data.get('predictor') or {}
    if pred:
        print('predictor keys', list(pred.keys())[:20])
        print('predictor', {k:pred.get(k) for k in list(pred.keys())[:12]})
    wp=data.get('winprobability') or []
    if wp:
        last=wp[-1]
        print('winprob last', last)
