import urllib.request, json
headers={'User-Agent':'Mozilla/5.0'}
url='https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard'
data=json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=15).read())
for e in data.get('events',[]):
  comp=e.get('competitions',[{}])[0]
  st=comp.get('status',{}).get('type',{})
  teams=comp.get('competitors',[])
  names=' @ '.join('%s %s'%(t.get('team',{}).get('abbreviation','?'), t.get('score','')) for t in sorted(teams, key=lambda x: x.get('homeAway')!='away'))
  print(names, '|', st.get('state'), st.get('shortDetail') or st.get('detail'), '|', e.get('name',''))
