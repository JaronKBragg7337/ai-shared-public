import urllib.request, json
# NHL web API
urls = [
 'https://api-web.nhle.com/v1/scoreboard/now',
 'https://api-web.nhle.com/v1/gamecenter/2026020004/landing',
 'https://api-web.nhle.com/v1/gamecenter/2026020004/boxscore',
]
for u in urls:
    try:
        req=urllib.request.Request(u, headers={'User-Agent':'Mozilla/5.0'})
        d=json.loads(urllib.request.urlopen(req,timeout=15).read())
        print('URL', u)
        if 'gamesByDate' in d or 'games' in d:
            games=d.get('gamesByDate') or [{'games': d.get('games',[])}]
            for day in (games if isinstance(games,list) else []):
                for g in day.get('games',[]):
                    aw=g.get('awayTeam',{}); hm=g.get('homeTeam',{})
                    if aw.get('abbrev') in ('VAN','EDM') or hm.get('abbrev') in ('VAN','EDM'):
                        print(aw.get('abbrev'), aw.get('score'), '-', hm.get('abbrev'), hm.get('score'), g.get('clock'), g.get('periodDescriptor'), g.get('gameState'))
        else:
            aw=d.get('awayTeam',{}); hm=d.get('homeTeam',{})
            print(aw.get('abbrev'), aw.get('score'), '-', hm.get('abbrev'), hm.get('score'))
            print('clock', d.get('clock'), 'period', d.get('periodDescriptor'), 'state', d.get('gameState'))
            print('keys', list(d.keys())[:20])
    except Exception as ex:
        print('err', u, ex)
