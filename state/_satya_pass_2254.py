import urllib.request, json
headers={'User-Agent':'Mozilla/5.0'}
urls=[
 ('CFB','https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard'),
 ('NFL','https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard'),
 ('MLS','https://site.api.espn.com/apis/site/v2/sports/soccer/usa.1/scoreboard'),
 ('LALIGA','https://site.api.espn.com/apis/site/v2/sports/soccer/esp.1/scoreboard'),
 ('EPL','https://site.api.espn.com/apis/site/v2/sports/soccer/eng.1/scoreboard'),
 ('BUNDES','https://site.api.espn.com/apis/site/v2/sports/soccer/ger.1/scoreboard'),
 ('LIGUE1','https://site.api.espn.com/apis/site/v2/sports/soccer/fra.1/scoreboard'),
 ('SERIEA','https://site.api.espn.com/apis/site/v2/sports/soccer/ita.1/scoreboard'),
 ('UCL','https://site.api.espn.com/apis/site/v2/sports/soccer/uefa.champions/scoreboard'),
 ('NBA','https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard'),
 ('NHL','https://site.api.espn.com/apis/site/v2/sports/hockey/nhl/scoreboard'),
 ('MLB','https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard'),
]
for label,url in urls:
  try:
    req=urllib.request.Request(url, headers=headers)
    data=json.loads(urllib.request.urlopen(req, timeout=15).read())
    evs=data.get('events',[])
    live=[e for e in evs if e.get('competitions',[{}])[0].get('status',{}).get('type',{}).get('state')=='in']
    pre=[e for e in evs if e.get('competitions',[{}])[0].get('status',{}).get('type',{}).get('state')=='pre']
    print('==',label,'total',len(evs),'live',len(live),'pre',len(pre))
    for e in live+pre[:8]:
      comp=e.get('competitions',[{}])[0]
      st=comp.get('status',{}).get('type',{})
      teams=comp.get('competitors',[])
      bits=[]
      for t in sorted(teams, key=lambda x: x.get('homeAway')!='away'):
        bits.append('%s %s'%(t.get('team',{}).get('abbreviation','?'), t.get('score','')))
      print(' ', ' @ '.join(bits), '|', st.get('state'), st.get('shortDetail') or st.get('detail'))
  except Exception as ex:
    print(label,'ERR',ex)
