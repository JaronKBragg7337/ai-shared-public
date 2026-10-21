import json, urllib.request, re
from html.parser import HTMLParser

def get_json(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.load(r)

def get_text(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=25) as r:
        return r.read().decode('utf-8', 'replace')

# ESPN game summary odds if any for Arsenal
try:
    sb = get_json('https://site.api.espn.com/apis/site/v2/sports/soccer/eng.1/scoreboard')
    for e in sb.get('events', []):
        if 'ARS' in (e.get('shortName') or '') or 'Arsenal' in (e.get('name') or ''):
            print('ARS event id', e.get('id'), e.get('status',{}).get('type',{}).get('detail'))
            comps = e.get('competitions', [{}])[0]
            print(' odds', comps.get('odds'))
            print(' situation', comps.get('situation'))
            for c in comps.get('competitors', []):
                print(' team', c.get('homeAway'), c.get('team',{}).get('abbreviation'), c.get('score'), 'winner', c.get('winner'))
except Exception as ex:
    print('espn ars err', ex)

# Valorant via vlr.gg search
try:
    html = get_text('https://www.vlr.gg/')
    # crude: look near G2 / Vitality
    for m in re.finditer(r'.{0,80}(G2|Vitality).{0,80}', html, re.I):
        s = re.sub(r'\s+', ' ', m.group(0))
        if 'vital' in s.lower() or 'g2' in s.lower():
            print('VLR', s[:160])
except Exception as ex:
    print('vlr err', ex)

# Polymarket gamma event for ars-lee if public
for url in [
    'https://gamma-api.polymarket.com/events?slug=atc-epl-ars-lee-2026-10-10-ars',
    'https://gamma-api.polymarket.com/markets?slug=atc-epl-ars-lee-2026-10-10-ars',
]:
    try:
        print('PM', url, str(get_json(url))[:500])
    except Exception as ex:
        print('PM err', url, ex)
