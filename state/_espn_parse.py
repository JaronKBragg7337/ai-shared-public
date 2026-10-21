import json, os, urllib.request
path = os.path.join(os.environ['TEMP'], 'espn-cfb.json')
with open(path, encoding='utf-8') as f:
    d = json.load(f)
want = ('TTU','COLO','BYU','TCU','WASH','USC','ARMY','LT','TEM','USF','MIA','CLEM','IU','RUTG','GASO','CCU','UTSA','ARST','UL')
for e in d.get('events', []):
    c = e['competitions'][0]
    st = c['status']['type']
    teams = c['competitors']
    abbrs = [t['team']['abbreviation'] for t in teams]
    if not any(a in want for a in abbrs):
        continue
    parts = []
    for t in teams:
        parts.append(f"{t['team']['abbreviation']} {t.get('score','')} ({t['homeAway']})")
    print(f"{e.get('shortName','?')} | {st.get('detail','')} | {' vs '.join(parts)} | completed={st.get('completed')} id={e.get('id')}")
# also pull win probs via summary for key ids
ids = []
for e in d.get('events', []):
    c = e['competitions'][0]
    abbrs = [t['team']['abbreviation'] for t in c['competitors']]
    if any(a in ('TTU','COLO','ARMY','LT','WASH','USC','BYU','TCU','TEM','USF') for a in abbrs):
        if not c['status']['type'].get('completed'):
            ids.append(e['id'])
print('---WP---')
for gid in ids:
    url = f'https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event={gid}'
    try:
        req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=20) as r:
            s = json.load(r)
        hdr = s.get('header', {})
        comps = hdr.get('competitions', [{}])[0]
        status = comps.get('status', {}).get('type', {}).get('detail', '')
        wps = []
        for t in comps.get('competitors', []):
            wp = None
            if 'probability' in t:
                wp = round(100*float(t['probability'].get('winPercentage', 0)), 1)
            wps.append(f"{t['team']['abbreviation']} {t.get('score','')} WP={wp}")
        # sit win pct alternate
        sit = s.get('situation') or {}
        last = (sit.get('lastPlay') or {})
        print(gid, status, ' | '.join(wps), 'sit', last.get('probability'))
    except Exception as ex:
        print(gid, 'ERR', ex)
