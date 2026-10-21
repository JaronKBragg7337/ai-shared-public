import urllib.request, json, sys
url = "http://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard"
data = json.loads(urllib.request.urlopen(url, timeout=20).read().decode())
want = {"JMU","GASO","BOIS","FRES","UTAH","KU","ALA","UGA","LSU","UK","USC","PSU","MEM","UAB","CCU","MRSH","PUR","MINN"}
for ev in data.get("events", []):
    comp = ev["competitions"][0]
    st = comp["status"]["type"]
    teams = comp["competitors"]
    abbrs = {t["team"]["abbreviation"] for t in teams}
    # normalize some ESPN abbrs
    if not (abbrs & want) and not any(x in ev.get("shortName","").upper() for x in ["JMU","JAMES","BOISE","FRESNO","UTAH","KANSAS","ALABAMA","GEORGIA","LSU","KENTUCKY"]):
        if st.get("state") != "in":
            continue
    line = []
    for t in sorted(teams, key=lambda x: 0 if x.get("homeAway")=="away" else 1):
        line.append(f"{t['team']['abbreviation']} {t['score']}")
    print(f"{ev.get('shortName')} | {st.get('detail')} | {' - '.join(line)} | id={ev['id']} state={st.get('state')}")
    if st.get("state") in ("in","post"):
        try:
            sd = json.loads(urllib.request.urlopen(f"https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event={ev['id']}", timeout=12).read().decode())
            wpa = sd.get("winprobability") or []
            if wpa:
                last = wpa[-1]
                print("  WP:", {k:last[k] for k in last if "percentage" in k.lower() or "Percentage" in k or k in ("homeWinPercentage","awayWinPercentage","tiePercentage")})
                # also raw
                for k,v in last.items():
                    if isinstance(v,(int,float)) and ("win" in k.lower() or "pct" in k.lower() or "prob" in k.lower()):
                        print(f"   {k}={v}")
            # header
            hdr = (sd.get("header") or {}).get("competitions",[{}])[0]
            for t in hdr.get("competitors",[]):
                if "probability" in t: print("  hdrprob", t["team"]["abbreviation"], t["probability"])
        except Exception as e:
            print("  WP err", e)
