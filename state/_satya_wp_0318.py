import urllib.request, json

def fetch(url):
    return json.load(urllib.request.urlopen(url, timeout=20))

def find_and_wp(want):
    url='https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?groups=80&limit=300'
    data=fetch(url)
    for e in data.get('events',[]):
        name=e.get('shortName','')
        up=name.upper()
        if not any(w in up for w in want):
            continue
        comp=e['competitions'][0]
        st=comp['status']['type']
        teams=' '.join(['%s(%s)=%s'%(c['team']['abbreviation'],c['homeAway'],c.get('score')) for c in comp['competitors']])
        print(name, '|', st.get('description'), st.get('detail'), '|', teams)
        eid=e['id']
        s=fetch('http://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event=%s'%eid)
        wpa=s.get('winprobability') or []
        if wpa:
            last=wpa[-1]
            hwp=float(last.get('homeWinPercentage') or 0)
            # identify home
            home=[c for c in comp['competitors'] if c['homeAway']=='home'][0]
            away=[c for c in comp['competitors'] if c['homeAway']=='away'][0]
            print('  home=%s WP=%.1f%%  away=%s WP=%.1f%%' % (home['team']['abbreviation'], 100*hwp, away['team']['abbreviation'], 100*(1-hwp)))
        else:
            print('  no winprob')

find_and_wp(['WYO','SJSU','WSU','USU','BYU','ISU','IOWA','WASH'])
