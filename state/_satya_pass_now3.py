import urllib.request, json, sys

def get(url):
    with urllib.request.urlopen(url, timeout=20) as r:
        return json.load(r)

def dump(name, url, keys):
    print('===', name, '===')
    try:
        data = get(url)
    except Exception as e:
        print('ERR', e)
        return
    for ev in data.get('events', []):
        comp = (ev.get('competitions') or [{}])[0]
        status = (comp.get('status') or {}).get('type', {})
        detail = status.get('detail') or status.get('description') or ''
        state = status.get('state')
        comps = comp.get('competitors') or []
        parts = []
        for c in comps:
            t = c.get('team', {})
            ab = t.get('abbreviation') or t.get('shortDisplayName') or '?'
            score = c.get('score')
            ha = c.get('homeAway')
            p = (c.get('probability') or {}).get('winPercentage')
            s = f"{ab}({ha})={score}"
            if p is not None:
                s += f" WP={p}"
            parts.append(s)
        line = ' | '.join(parts) + f" | {state} {detail}"
        blob = (line + ' ' + (ev.get('name') or '')).lower()
        if any(k in blob for k in keys) or state == 'in':
            tag = 'MATCH' if any(k in blob for k in keys) else 'LIVE'
            print(tag + ':', line)

dump('cfb', 'https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard',
     ['pitt','virginia tech','hokies','penn state','northwestern','liberty','delaware'])
dump('cnl', 'https://site.api.espn.com/apis/site/v2/sports/soccer/concacaf.nations.league/scoreboard',
     ['martinique','honduras','mtq','hon'])
dump('friendly', 'https://site.api.espn.com/apis/site/v2/sports/soccer/fifa.friendly/scoreboard',
     ['colombia','paraguay','col','par'])
# also broad soccer scoreboards sometimes used
for slug in ['concacaf.nations.league','fifa.friendly','uefa.nations','eng.1']:
    pass
