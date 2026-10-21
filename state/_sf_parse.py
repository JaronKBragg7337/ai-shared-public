import json, os, urllib.request
url = 'https://www.sofascore.com/api/v1/sport/tennis/events/live'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=20) as r:
        d = json.loads(r.read().decode('utf-8'))
except Exception as e:
    print('SOFA_ERR', e)
    path = os.path.join(os.environ.get('TEMP','.'), 'sf-tennis.json')
    if os.path.exists(path):
        d = json.load(open(path, encoding='utf-8'))
    else:
        raise
evs = d.get('events', [])
print('live_tennis', len(evs))
keys = ('faria','atmane','sweeny','daniel','yeon','ku','ruse','gibson','morvay','svitolina','minton','shimabukuro','gaston','bin','bar')
for e in evs:
    h = e.get('homeTeam',{}).get('name','')
    a = e.get('awayTeam',{}).get('name','')
    blob = (h + ' ' + a).lower()
    if not any(k in blob for k in keys):
        continue
    s = e.get('homeScore', {})
    t = e.get('awayScore', {})
    st = e.get('status', {}).get('description', '')
    print(f'{h} vs {a} | sets {s.get("current")}-{t.get("current")} | {st}')
    print('  home', s)
    print('  away', t)
    print('  lastPeriod', e.get('lastPeriod'), 'time', e.get('time'))
# also print first 15 live for discovery
print('---ALL LIVE (15)---')
for e in evs[:15]:
    h = e.get('homeTeam',{}).get('name','')
    a = e.get('awayTeam',{}).get('name','')
    s = e.get('homeScore', {})
    t = e.get('awayScore', {})
    st = e.get('status', {}).get('description', '')
    print(f'{h} vs {a} | {s.get("current")}-{t.get("current")} | {st}')
