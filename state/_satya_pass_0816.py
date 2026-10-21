import json, urllib.request, datetime
from pathlib import Path

print('TIME', datetime.datetime.now().isoformat())

def get(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.load(r)

# CFB
data = get('https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?groups=80&limit=100')
events = data.get('events', [])
live, soon = [], []
for e in events:
    st = e.get('status', {}).get('type', {})
    name = e.get('shortName') or e.get('name')
    detail = st.get('detail', '')
    comps = e.get('competitions', [{}])[0]
    competitors = comps.get('competitors', [])
    score = '-'.join(f"{c.get('team',{}).get('abbreviation','?')}{c.get('score','')}" for c in competitors)
    if st.get('state') == 'in':
        live.append(f'{name} | {detail} | {score}')
    elif st.get('state') == 'pre':
        soon.append(f'{name} | {detail}')
print('CFB live', len(live))
for x in live[:20]:
    print(' ', x)
print('CFB pre first15')
for x in soon[:15]:
    print(' ', x)

# EPL
data = get('https://site.api.espn.com/apis/site/v2/sports/soccer/eng.1/scoreboard')
for e in data.get('events', []):
    name = e.get('shortName') or e.get('name')
    st = e.get('status', {}).get('type', {})
    comps = e.get('competitions', [{}])[0]
    competitors = comps.get('competitors', [])
    score = ' '.join(f"{c.get('team',{}).get('abbreviation','?')} {c.get('score','')}" for c in competitors)
    print('EPL', name, '|', st.get('detail'), '|', score, '|', st.get('state'))

# NFL
data = get('https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard')
nfl_live = [e for e in data.get('events', []) if e.get('status',{}).get('type',{}).get('state')=='in']
print('NFL live', len(nfl_live))
for e in data.get('events', [])[:8]:
    st = e.get('status', {}).get('type', {})
    print(' NFL', e.get('shortName'), '|', st.get('detail'), '|', st.get('state'))

# desk account helpers if present
for p in [
    Path(r'C:\Users\lilli\AI-Shared\state\_desk-acct-tmp.txt'),
    Path(r'C:\Users\lilli\AI-Shared\state\_account-snap.txt'),
    Path(r'C:\Users\lilli\AI-Shared\state\_tmp_account.txt'),
]:
    if p.exists():
        print('ACCTFILE', p, p.read_text(encoding='utf-8', errors='replace')[:500])
