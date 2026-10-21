import urllib.request, json
u = 'https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard'
d = json.load(urllib.request.urlopen(u))
for e in d.get('events', []):
    s = e.get('status', {}).get('type', {})
    name = e.get('name', '')
    if 'Indianapolis' in name or 'Washington' in name or 'Colts' in name or 'Commanders' in name:
        comps = e.get('competitions', [{}])[0]
        teams = comps.get('competitors', [])
        print('EVENT', name)
        print('STATUS', s.get('description'), s.get('detail'), 'state=', s.get('state'), 'completed=', s.get('completed'))
        for t in teams:
            prob = (t.get('probability') or {})
            print(' ', t.get('homeAway'), t.get('team', {}).get('abbreviation'), 'score', t.get('score'), 'WP', prob.get('winPercentage'))
        # also try summary endpoint for WP
        eid = e.get('id')
        try:
            su = f'https://site.api.espn.com/apis/site/v2/sports/football/nfl/summary?event={eid}'
            sd = json.load(urllib.request.urlopen(su))
            pred = (sd.get('predictor') or {})
            print('PREDICTOR', {k: pred.get(k) for k in pred if 'win' in k.lower() or 'home' in k.lower() or 'away' in k.lower()})
            wp = sd.get('winprobability') or []
            if wp:
                print('LAST_WP', wp[-1])
            sit = (comps.get('situation') or {})
            print('SIT', sit.get('downDistanceText'), 'clock', sit.get('clock'), 'possession', (sit.get('possession') or ''))
        except Exception as ex:
            print('summary err', ex)
# soccer Kosovo Austria
print('====SOCCER====')
for sport_path in [
    'https://site.api.espn.com/apis/site/v2/sports/soccer/uefa.nations/scoreboard',
    'https://site.api.espn.com/apis/site/v2/sports/soccer/fifa.worldq.uefa/scoreboard',
    'https://site.api.espn.com/apis/site/v2/sports/soccer/all/scoreboard',
]:
    try:
        sd = json.load(urllib.request.urlopen(sport_path))
        for e in sd.get('events', []):
            name = e.get('name', '')
            if 'Kosovo' in name or 'Austria' in name:
                s = e.get('status', {}).get('type', {})
                comps = e.get('competitions', [{}])[0]
                teams = comps.get('competitors', [])
                print(sport_path.split('/')[-2], name, s.get('detail'))
                for t in teams:
                    print(' ', t.get('team', {}).get('displayName'), t.get('score'))
    except Exception as ex:
        print('fail', sport_path, ex)
