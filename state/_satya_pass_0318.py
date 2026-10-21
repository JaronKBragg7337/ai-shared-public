import urllib.request, json, sys

def fetch(url):
    return json.load(urllib.request.urlopen(url, timeout=20))

def show_scoreboard(name, url, want_abbrs=None):
    print('====', name, '====')
    data = fetch(url)
    for e in data.get('events', []):
        comp = e['competitions'][0]
        st = comp['status']['type']
        status = st.get('description', '')
        detail = st.get('detail', '')
        state = st.get('state', '')
        teams = []
        abbrs = []
        for c in comp['competitors']:
            abbr = c['team']['abbreviation']
            abbrs.append(abbr)
            teams.append('%s(%s)=%s' % (abbr, c['homeAway'], c.get('score', '?')))
        if want_abbrs:
            up = set(a.upper() for a in abbrs)
            if not (up & set(a.upper() for a in want_abbrs)):
                if state != 'in':
                    continue
        # win probability endpoint
        eid = e.get('id')
        print('%s | %s | %s | %s' % (e.get('shortName'), status, detail, ' '.join(teams)))
        try:
            wpurl = 'https://site.api.espn.com/apis/site/v2/sports/%s/summary?event=%s' % (
                'football/college-football' if 'football' in url else 'basketball/wnba', eid)
            # better: predictor from summary
            sumurl = url.replace('/scoreboard', '/summary') + ('?event=%s' % eid)
            # use dedicated winprobability
            sport_path = 'football/college-football' if 'college-football' in url else 'basketball/wnba'
            wpu = 'http://site.api.espn.com/apis/site/v2/sports/%s/summary?event=%s' % (sport_path, eid)
            s = fetch(wpu)
            # predictor
            pred = s.get('predictor') or {}
            ha = pred.get('homeTeam') or {}
            aw = pred.get('awayTeam') or {}
            if ha or aw:
                print('  predictor awayGP=%s homeGP=%s' % (aw.get('gameProjection'), ha.get('gameProjection')))
            # winprobability array last
            wpa = s.get('winprobability') or []
            if wpa:
                last = wpa[-1]
                print('  winprob last homeWinPercentage=%s tiePercentage=%s' % (
                    last.get('homeWinPercentage'), last.get('tiePercentage')))
            # situation
            sit = (s.get('header') or {}).get('competitions', [{}])[0].get('situation') if False else None
        except Exception as ex:
            print('  wp err', type(ex).__name__, ex)

want = ['IOWA','WASH','BYU','ISU','WSU','USU','WYO','SJSU','COLU','MRST','FSU','LOU','GS','LV']
show_scoreboard('cfb', 'https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard', want)
show_scoreboard('wnba', 'https://site.api.espn.com/apis/site/v2/sports/basketball/wnba/scoreboard', ['GS','LV','GSV'])
