import urllib.request, json, sys

def get(url):
    with urllib.request.urlopen(url, timeout=25) as r:
        return json.load(r)

want = ("Georgia", "Alabama", "LSU", "Kentucky", "USC", "Penn State", "Minnesota", "Purdue", "UAB", "Memphis", "Utah", "Kansas", "Coastal", "Marshall", "Syracuse", "Virginia", "Nevada", "UTEP", "Air Force", "Northern Illinois", "James Madison", "Georgia Southern", "Louisiana", "UNLV", "North Dakota")

data = get("https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?limit=300")
for e in data.get("events", []):
    name = e.get("name") or ""
    if not any(w.lower() in name.lower() for w in want):
        continue
    eid = e.get("id")
    st = (e.get("status") or {}).get("type") or {}
    comps = (e.get("competitions") or [{}])[0]
    teams = comps.get("competitors") or []
    bits = []
    for t in teams:
        ab = (t.get("team") or {}).get("abbreviation")
        sc = t.get("score")
        bits.append(f"{ab} {sc}")
    print(f"SCOREBOARD {name} | {st.get('detail')} | {' - '.join(bits)} | id={eid}")
    if st.get("state") not in ("in", "post"):
        continue
    try:
        s = get("https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event=" + str(eid))
    except Exception as ex:
        print("  summary err", ex)
        continue
    hdr = s.get("header") or {}
    c0 = (hdr.get("competitions") or [{}])[0]
    for t in c0.get("competitors") or []:
        prob = t.get("probability")
        if isinstance(prob, dict):
            wp = prob.get("winPercentage")
        else:
            wp = prob
        print(f"  {t.get('homeAway')} {(t.get('team') or {}).get('abbreviation')} score={t.get('score')} wp={wp}")
    wp = s.get("winprobability") or []
    if wp:
        last = wp[-1]
        print("  winprob_last", last)
