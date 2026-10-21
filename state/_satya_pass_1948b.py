import json, urllib.request

# Find Oregon State / any remaining CFB with WP
url = "https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?groups=80&limit=200"
with urllib.request.urlopen(url, timeout=20) as r:
    data = json.load(r)
print("=== ALL LIVE/RECENT CFB (filtered) ===")
for ev in data.get("events", []):
    name = ev.get("name","")
    st = ev.get("status",{}).get("type",{})
    desc = st.get("description",""); detail = st.get("detail",""); state = st.get("state","")
    comps = ev.get("competitions",[{}])[0]
    competitors = comps.get("competitors",[])
    scores = {c["team"]["abbreviation"]: c.get("score") for c in competitors}
    low = name.lower()
    if state == "pre":
        continue
    if any(x in low for x in ["oregon state","colorado state","byu","tcu","texas tech","colorado","washington","usc","ohio","kent","miami","clemson","arkansas","texas a&m","georgia southern","coastal"]):
        eid = ev["id"]
        wp_str = ""
        try:
            su = f"https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event={eid}"
            with urllib.request.urlopen(su, timeout=15) as r2:
                sdata = json.load(r2)
            wpr = sdata.get("winprobability") or []
            if wpr:
                last = wpr[-1]
                home_wp = last.get("homeWinPercentage")
                home = next(c["team"]["abbreviation"] for c in competitors if c.get("homeAway")=="home")
                away = next(c["team"]["abbreviation"] for c in competitors if c.get("homeAway")=="away")
                wp_str = f" {away}={1-home_wp:.1%} {home}={home_wp:.1%}"
        except Exception as e:
            wp_str = f" err={e}"
        print(f"{name} | {desc} {detail} | {scores}{wp_str}")
