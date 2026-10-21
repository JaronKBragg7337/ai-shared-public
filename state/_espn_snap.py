import urllib.request, json
u='https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?dates=20261010&limit=100'
d=json.loads(urllib.request.urlopen(u,timeout=15).read().decode())
for e in d.get('events',[]):
 n=e.get('name','')
 if not any(x in n for x in ['UCLA','Oregon','Houston','Kansas','Texas','Oklahoma','Ole Miss','Vanderbilt','Notre Dame','Stanford','South Carolina','Maryland','Ohio State']):
  continue
 s=e.get('status',{}).get('type',{}).get('detail','')
 comps=e.get('competitions',[{}])[0].get('competitors',[])
 sc=' | '.join(f"{c.get('team',{}).get('abbreviation','?')} {c.get('score','')}" for c in sorted(comps, key=lambda c: c.get('homeAway')!='away'))
 print(f"{n} || {sc} || {s}")
