import urllib.request, json
url='https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard'
raw=urllib.request.urlopen(url, timeout=20).read()
data=json.loads(raw)
for e in data.get('events', []):
    comp=e['competitions'][0]
    st=comp['status']['type']
    status=st.get('description','')
    state=st.get('state','')
    clock=comp['status'].get('displayClock','')
    period=comp['status'].get('period','')
    print(f"{e['name']} | {status} {clock} Q{period} state={state}")
    sit=comp.get('situation') or {}
    last=sit.get('lastPlay') or {}
    prob=sit.get('probability') or last.get('probability') or {}
    print(f"  sit_prob={prob}")
    for c in comp['competitors']:
        ab=c['team']['abbreviation']
        sc=c['score']
        ha=c['homeAway']
        p=c.get('probability')
        print(f"  {ha} {ab} {sc} probability={p}")
    # summary predictor if present
    pred=(e.get('competitions') or [{}])[0].get('predictor') or e.get('predictor')
    if pred:
        print(f"  predictor={pred}")
