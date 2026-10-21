import urllib.request, json
UA={'User-Agent':'Mozilla/5.0','Accept':'application/json'}

def get(url):
    req=urllib.request.Request(url,headers=UA)
    with urllib.request.urlopen(req,timeout=25) as r:
        return json.load(r)

# Find ESPN game ids for live MLB
data=get('https://site.web.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard?dates=20260919')
for ev in data.get('events',[]):
    comp=ev['competitions'][0]
    st=comp['status']['type']
    if st.get('state')!='in':
        continue
    gid=ev['id']
    teams=comp['competitors']
    home=next(t for t in teams if t['homeAway']=='home')
    away=next(t for t in teams if t['homeAway']=='away')
    d=get('https://site.web.api.espn.com/apis/site/v2/sports/baseball/mlb/summary?event='+gid)
    wp=d.get('winprobability') or []
    last=wp[-1] if wp else {}
    print('{} {} @ {} {} | {} | homeWP={} awayWP~{}'.format(
        away['team']['abbreviation'], away.get('score'),
        home['team']['abbreviation'], home.get('score'),
        st.get('detail'), last.get('homeWinPercentage'),
        (1-last['homeWinPercentage']) if last.get('homeWinPercentage') is not None else None))
