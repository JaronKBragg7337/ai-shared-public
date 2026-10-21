import urllib.request, json, sys
from collections import Counter

print('====DESK====')
try:
    import subprocess
    r = subprocess.run([sys.executable, r'C:\Users\lilli\AI-Shared\tools\desk.py'], capture_output=True, text=True, timeout=60)
    print(r.stdout[-3000:] if r.stdout else '')
    if r.stderr: print('stderr', r.stderr[-1000:])
except Exception as e:
    print('desk err', e)

print('====SCHED====')
try:
    r = subprocess.run([sys.executable, r'C:\Users\lilli\AI-Shared\tools\desk_schedule.py'], capture_output=True, text=True, timeout=60)
    print(r.stdout[-2500:] if r.stdout else '')
    if r.stderr: print('stderr', r.stderr[-800:])
except Exception as e:
    print('sched err', e)

print('====EPL====')
try:
    u='https://site.api.espn.com/apis/site/v2/sports/soccer/eng.1/scoreboard'
    d=json.load(urllib.request.urlopen(u, timeout=20))
    for e in d.get('events', []):
        s=e['status']['type']; comp=e['competitions'][0]; teams=comp['competitors']
        home=next(t for t in teams if t['homeAway']=='home')
        away=next(t for t in teams if t['homeAway']=='away')
        print(away['team']['abbreviation'], away['score'], '-', home['score'], home['team']['abbreviation'], '|', s.get('detail',''), 'state=', s.get('state'))
        # odds if any
        odds=comp.get('odds') or []
        if odds:
            print('  odds', odds[0])
except Exception as e:
    print('epl err', e)

print('====CFB====')
try:
    u='https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?groups=80&limit=100'
    d=json.load(urllib.request.urlopen(u, timeout=20))
    c=Counter()
    for e in d.get('events', []):
        st=e['status']['type']['state']; c[st]+=1
        if st=='in':
            comp=e['competitions'][0]; teams=comp['competitors']
            home=next(t for t in teams if t['homeAway']=='home')
            away=next(t for t in teams if t['homeAway']=='away')
            print('LIVE', away['team']['abbreviation'], away['score'], home['team']['abbreviation'], home['score'], e['status']['type'].get('detail'))
    print('counts', dict(c))
    pre=[]
    for e in d.get('events', []):
        if e['status']['type']['state']=='pre':
            pre.append((e['date'], e['name'], e['status']['type'].get('shortDetail','')))
    pre.sort()
    print('next pre:')
    for row in pre[:15]:
        print(row)
except Exception as e:
    print('cfb err', e)
