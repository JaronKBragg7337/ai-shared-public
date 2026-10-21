import urllib.request, json

def get(url):
    return json.loads(urllib.request.urlopen(url, timeout=15).read())

mlb = get('https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard')
for e in mlb.get('events', []):
    name = e.get('name','')
    if any(x in name for x in ['Padres','Cubs','Yankees','Red Sox']):
        c = e['competitions'][0]
        a, h = c['competitors'][1], c['competitors'][0]
        print('MLB', a['team']['abbreviation'], a['score'], '-', h['team']['abbreviation'], h['score'], '|', e['status']['type']['detail'])

nhl = get('https://site.api.espn.com/apis/site/v2/sports/hockey/nhl/scoreboard')
for e in nhl.get('events', []):
    name = e.get('name','')
    if any(x in name for x in ['Canucks','Oilers','Blackhawks','Golden Knights']):
        c = e['competitions'][0]
        a, h = c['competitors'][1], c['competitors'][0]
        print('NHL', a['team']['abbreviation'], a['score'], '-', h['team']['abbreviation'], h['score'], '|', e['status']['type']['detail'])
        # try win pct
        for x in (a,h):
            print('  WP', x['team']['abbreviation'], x.get('probability',{}).get('winPercentage', 'n/a'))

for path in ['tennis/wta/scoreboard','tennis/atp/scoreboard']:
    try:
        t = get(f'https://site.api.espn.com/apis/site/v2/sports/{path}')
        keys = ['Lehecka','Bergs','Vidmanova','Timofeeva','Vacherot','Blockx','Khachanov','Auger','Ruse','Tagger','Tjen','Kalinina']
        for e in t.get('events', []):
            n = e.get('name','')
            if any(x in n for x in keys):
                print('TENNIS', n, '|', e['status']['type']['detail'])
                for x in e['competitions'][0]['competitors']:
                    nm = x.get('athlete',{}).get('displayName') or x.get('team',{}).get('displayName')
                    print(' ', nm, x.get('score'), 'W' if x.get('winner') else '')
    except Exception as ex:
        print('tennis err', path, ex)
