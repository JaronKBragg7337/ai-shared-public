import urllib.request, json, os, subprocess, sys

def get(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    return json.loads(urllib.request.urlopen(req, timeout=25).read().decode())

print('=== LIVE NFL ===')
sb = get('https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard')
for e in sb.get('events', []):
    st = e.get('status', {}).get('type', {})
    if st.get('completed') or st.get('state') == 'pre':
        continue
    eid = e.get('id')
    comps = e.get('competitions', [{}])[0]
    teams = comps.get('competitors', [])
    home = next(t for t in teams if t.get('homeAway')=='home')
    away = next(t for t in teams if t.get('homeAway')=='away')
    print(f"{e.get('shortName')} id={eid} | {away.get('team',{}).get('abbreviation')} {away.get('score')} @ {home.get('team',{}).get('abbreviation')} {home.get('score')} | {st.get('detail')}")
    try:
        wp = get(f'https://site.api.espn.com/apis/site/v2/sports/football/nfl/summary?event={eid}')
        wps = wp.get('winprobability') or []
        if wps:
            last = wps[-1]
            print(f"  homeWP={last.get('homeWinPercentage')} awayWP={last.get('awayWinPercentage')}")
        else:
            print('  no winprobability list')
            pred = wp.get('predictor') or {}
            if pred:
                print('  predictor', pred)
    except Exception as ex:
        print('  WP err', ex)

print('=== LIVE CFB ===')
try:
    cfb = get('https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?groups=80')
    n=0
    for e in cfb.get('events', []):
        st = e.get('status', {}).get('type', {})
        if st.get('completed') or st.get('state') == 'pre':
            continue
        n+=1
        comps = e.get('competitions', [{}])[0]
        teams = comps.get('competitors', [])
        parts = [f"{t.get('team',{}).get('abbreviation')} {t.get('score')}" for t in sorted(teams, key=lambda x: x.get('homeAway'))]
        print(e.get('shortName'), st.get('detail'), '|', ' - '.join(parts))
    if n==0:
        print('(none)')
except Exception as ex:
    print('CFB err', ex)
