import urllib.request, json
base='https://site.api.espn.com/apis/site/v2/sports/football/college-football'
eid='401856821'
s=json.loads(urllib.request.urlopen(base+f'/summary?event={eid}', timeout=15).read().decode())
comp=s['header']['competitions'][0]
st=comp['status']['type'].get('detail')
scores=', '.join(f"{c['team']['abbreviation']} {c.get('score')}" for c in comp['competitors'])
wp=(s.get('winprobability') or [None])[-1]
hwp=wp.get('homeWinPercentage') if wp else None
print(scores, '|', st, '| COLO_WPh', hwp, 'TTU_WP', None if hwp is None else round(1-hwp,4))
