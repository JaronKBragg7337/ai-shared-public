import urllib.request, json

def summary_wp(eid, label):
    try:
        u = f'https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event={eid}'
        d = json.load(urllib.request.urlopen(u, timeout=20))
        # winprobability array
        wp = d.get('winprobability') or []
        last = wp[-1] if wp else {}
        # header score
        h = d.get('header') or {}
        comps = (h.get('competitions') or [{}])[0]
        teams = []
        for c in comps.get('competitors', []):
            teams.append(f"{c['team']['abbreviation']} {c.get('score','?')} ({c['homeAway']})")
        st = (comps.get('status') or {}).get('type', {})
        print(f"{label} eid={eid} | {' vs '.join(teams)} | {st.get('detail')} | homeWinPct={last.get('homeWinPercentage')} tiePct={last.get('tiePercentage')} playId={last.get('playId')}")
    except Exception as e:
        print(label, 'ERR', e)

# find event ids from scoreboard
data = json.load(urllib.request.urlopen('https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?dates=20260919&limit=200', timeout=25))
want = ['SELA','ULM','OHIO','USA','FIU','FAU','ECU','ODU','FLA','AUB','NEV','MTST','MRSH','MSRST','WMU','RICE','CONN','TROY','MIZ','AUSP','UWF','PRE','CHSO','NICH','SHSU']
for e in data.get('events', []):
    name = e.get('name','')
    short = e.get('shortName','')
    abbs = []
    for c in e['competitions'][0]['competitors']:
        abbs.append(c['team']['abbreviation'])
    if any(a in want for a in abbs) or any(w in name.upper() for w in ['SOUTHEASTERN','MONROE','FLORIDA','AUBURN','OHIO','SOUTH ALA','FIU','ATLANTIC','EAST CAROLINA','DOMINION','NEVADA','MONTANA','MARSHALL','WESTERN MICH','RICE','CONNECTICUT','TROY','MISSOURI','PRESBYTERIAN','NICHOLLS']):
        st = e['competitions'][0]['status']['type']
        if st.get('completed'):
            continue
        if st.get('name') == 'STATUS_SCHEDULED':
            continue
        print('FOUND', e['id'], short, abbs, st.get('detail'))
        summary_wp(e['id'], short)
