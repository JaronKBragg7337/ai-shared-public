import urllib.request, json

def fetch(url):
    return json.load(urllib.request.urlopen(url, timeout=20))

def dump(label, url):
    print('====', label, '====')
    data = fetch(url)
    sport_path = 'football/college-football' if 'college-football' in url else 'basketball/wnba'
    for e in data.get('events', []):
        comp = e['competitions'][0]
        st = comp['status']['type']
        state = st.get('state', '')
        if state not in ('in', 'post'):
            continue
        teams = []
        for c in comp['competitors']:
            teams.append('%s(%s)=%s' % (c['team']['abbreviation'], c['homeAway'], c.get('score','?')))
        line = '%s | %s | %s | %s' % (e.get('shortName'), st.get('description'), st.get('detail'), ' '.join(teams))
        print(line)
        if state != 'in':
            continue
        eid = e.get('id')
        try:
            s = fetch('http://site.api.espn.com/apis/site/v2/sports/%s/summary?event=%s' % (sport_path, eid))
            wpa = s.get('winprobability') or []
            if wpa:
                last = wpa[-1]
                print('  homeWP=%.1f%%' % (100*float(last.get('homeWinPercentage') or 0)))
        except Exception as ex:
            print('  wp err', ex)

dump('cfb', 'https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard')
dump('wnba', 'https://site.api.espn.com/apis/site/v2/sports/basketball/wnba/scoreboard')
