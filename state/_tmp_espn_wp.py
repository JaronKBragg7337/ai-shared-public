import urllib.request, json
url='https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?dates=20261010&limit=300'
data=json.loads(urllib.request.urlopen(url, timeout=20).read().decode())
for ev in data.get('events', []):
    comp=ev['competitions'][0]
    st=comp.get('status',{}).get('type',{})
    if st.get('state')!='in':
        continue
    sit=comp.get('situation') or {}
    lp=sit.get('lastPlay') or {}
    prob=lp.get('probability') or {}
    comps=comp.get('competitors',[])
    home=next(c for c in comps if c.get('homeAway')=='home')
    away=next(c for c in comps if c.get('homeAway')=='away')
    h=home['team']['abbreviation']; a=away['team']['abbreviation']
    print('%s %s-%s %s | %s | homeWP=%s awayWP=%s | %s' % (
        a, away.get('score'), h, home.get('score'), st.get('shortDetail'),
        prob.get('homeWinPercentage'), prob.get('awayWinPercentage'), ev.get('shortName')))
