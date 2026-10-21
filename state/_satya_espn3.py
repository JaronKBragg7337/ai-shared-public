import urllib.request, json

def get(url):
    return json.loads(urllib.request.urlopen(url, timeout=20).read())

# broader search
for groups in [80, 81, 82, 83, 84, 85, 90]:
    try:
        data = get(f"https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?groups={groups}&limit=100")
    except Exception as ex:
        print("group", groups, ex)
        continue
    for e in data.get("events", []):
        name = (e.get("shortName") or "") + " " + (e.get("name") or "")
        up = name.upper()
        if any(x in up for x in ("WYOMING", "SAN JOSE", "COLUMBIA", "MARIST", "WASHINGTON ST", "UTAH ST", "UTAH STATE", "WASH ST")):
            comp = e["competitions"][0]
            st = comp["status"]["type"]
            bits = []
            for c in comp["competitors"]:
                bits.append(f"{c['team'].get('abbreviation')}={c.get('score')}")
            print(groups, e.get("shortName"), "|", st.get("state"), st.get("detail"), "|", " ".join(bits))
            eid = e.get("id")
            try:
                s = get(f"https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event={eid}")
                wparr = s.get("winprobability") or []
                if wparr:
                    print("  wp", wparr[-1])
            except Exception as ex:
                print("  wp_err", ex)
