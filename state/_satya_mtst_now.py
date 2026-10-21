import urllib.request, json
url = 'https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?groups=80&limit=300'
req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'})
data = json.load(urllib.request.urlopen(req, timeout=25))
for ev in data.get('events') or []:
    name = ev.get('name','')
    if 'Montana State' not in name and 'Idaho' not in name: continue
    if 'Idaho State' in name or 'Northern' in name: continue
    comp = (ev.get('competitions') or [{}])[0]
    st = (comp.get('status') or {}).get('type',{})
    print(name, '|', st.get('detail'), '|', st.get('state'))
    for c in comp.get('competitors') or []:
        t=c.get('team',{})
        print(' ', t.get('abbreviation'), 'score', c.get('score'), 'homeAway', c.get('homeAway'))
    sit = comp.get('situation') or {}
    lp = sit.get('lastPlay') or {}
    print(' lastPlay', (lp.get('text') or '')[:120])
    print(' prob', lp.get('probability'))
    # also summary winprobability last
    summ = ev.get('competitions',[{}])[0]
    # try odds
    print(' odds', comp.get('odds'))
# also dates=20261003
url2 = 'https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?dates=20261003&limit=300'
data2 = json.load(urllib.request.urlopen(urllib.request.Request(url2, headers={'User-Agent':'Mozilla/5.0'}), timeout=25))
for ev in data2.get('events') or []:
    name = ev.get('name','')
    if 'Montana State' in name or ( 'Idaho' in name and 'Idaho State' not in name and 'Northern' not in name):
        comp = (ev.get('competitions') or [{}])[0]
        st = (comp.get('status') or {}).get('type',{})
        if st.get('state') != 'in' and 'Montana State' not in name: continue
        print('D03', name, '|', st.get('detail'))
        sit = comp.get('situation') or {}
        lp = sit.get('lastPlay') or {}
        print('  prob', lp.get('probability'))
        for c in comp.get('competitors') or []:
            t=c.get('team',{})
            print(' ', t.get('abbreviation'), c.get('score'), c.get('homeAway'))
