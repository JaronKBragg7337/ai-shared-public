import urllib.request, json

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.load(r)

def show(label, url):
    print('===', label, '===')
    try:
        data = get(url)
    except Exception as e:
        print('ERR', e)
        return
    evs = data.get('events') or []
    print('events', len(evs))
    for ev in evs:
        name = ev.get('name') or ev.get('shortName') or ''
        comp = (ev.get('competitions') or [{}])[0]
        status = (comp.get('status') or {}).get('type', {})
        detail = status.get('detail') or status.get('description') or ''
        state = status.get('state')
        comps = comp.get('competitors') or []
        bits = []
        for c in comps:
            t = c.get('team', {})
            ab = t.get('abbreviation') or t.get('shortDisplayName') or '?'
            p = (c.get('probability') or {}).get('winPercentage')
            s = f"{ab}={c.get('score')}"
            if p is not None:
                s += f" WP={round(float(p)*100,1) if float(p)<=1 else p}%" if False else f" WP={p}"
            bits.append(s)
        line = ' '.join(bits) + f" | {state} {detail} | {name}"
        low = line.lower()
        if any(k in low for k in ['pitt','virginia','hokie','penn','northwestern','liberty','delaware','nittany']):
            print('HIT:', line)
        elif state == 'in':
            print('LIVE:', line)

base = 'https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard'
for u in [
    base,
    base + '?groups=80',
    base + '?dates=20261002',
    base + '?dates=20261003',
    base + '?dates=20261002-20261003',
    base + '?groups=80&dates=20261002',
]:
    show(u.replace(base, 'cfb'), u)

# summary for soccer too
print('=== soccer refresh ===')
for label, url in [
    ('cnl', 'https://site.api.espn.com/apis/site/v2/sports/soccer/concacaf.nations.league/scoreboard'),
    ('friendly', 'https://site.api.espn.com/apis/site/v2/sports/soccer/fifa.friendly/scoreboard'),
]:
    show(label, url)
