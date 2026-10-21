import urllib.request, json
url='https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard'
with urllib.request.urlopen(url, timeout=20) as r:
    data=json.load(r)
for e in data.get('events',[]):
    c=e['competitions'][0]
    st=c['status']['type']
    if st.get('state') not in ('in','halftime'):
        continue
    comps={x['homeAway']:x for x in c['competitors']}
    h,a=comps['home'],comps['away']
    wp=None
    sit=c.get('situation') or {}
    lp=sit.get('lastPlay') or {}
    prob=lp.get('probability') or {}
    if not prob:
        # try winprobability array
        warr=c.get('odds')
    hwp=prob.get('homeWinPercentage')
    awp=prob.get('awayWinPercentage')
    def pct(x):
        return None if x is None else round(100*float(x),1)
    print(f"{e.get('shortName')}: {a['team']['abbreviation']} {a['score']} @ {h['team']['abbreviation']} {h['score']} | {st.get('detail')} | homeWP={pct(hwp)} awayWP={pct(awp)}")
