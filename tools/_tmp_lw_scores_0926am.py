import urllib.request, json

UA={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

def get(url):
    req=urllib.request.Request(url, headers=UA)
    return urllib.request.urlopen(req, timeout=20).read().decode('utf-8','ignore')

for league in ['wta','atp','wta-125','challenger']:
    print('===', league, '===')
    for base in [
        f'https://site.api.espn.com/apis/site/v2/sports/tennis/{league}/scoreboard',
        f'https://site.api.espn.com/apis/site/v2/sports/tennis/{league}/scoreboard?dates=20260926',
    ]:
        try:
            data=json.loads(get(base))
            evs=data.get('events',[])
            print(base, 'events', len(evs))
            for ev in evs:
                name=ev.get('name','')
                keys=['Timofeeva','Pohankova','Kostovic','Iatcenko','Medvedev','Royer','Moeller','Gurri','Fernandez','Chwalinska']
                if not any(k.lower() in name.lower() for k in keys):
                    continue
                comp=ev.get('competitions',[{}])[0]
                status=comp.get('status',{}).get('type',{}).get('description')
                detail=comp.get('status',{}).get('type',{}).get('detail')
                comps=comp.get('competitors',[])
                print(name, '|', status, detail)
                for c in comps:
                    ath=c.get('athlete') or {}
                    dn=ath.get('displayName') or c.get('displayName') or '?'
                    ls=[x.get('value') for x in c.get('linescores',[])]
                    print(' ', dn, 'score', c.get('score'), 'lines', ls, 'winner', c.get('winner'))
        except Exception as e:
            print('err', base, e)
