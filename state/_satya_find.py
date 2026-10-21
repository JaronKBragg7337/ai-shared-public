import json, urllib.request

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.load(r)

# Try scoreboard with all groups / FCS
for url in [
    "https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?groups=80",
    "https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?groups=81",
    "https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?limit=300",
]:
    try:
        data = get(url)
        hits = []
        for e in data.get("events", []):
            name = e.get("name", "")
            if any(x in name for x in ("Florida State", "Louisville", "Columbia", "Marist")):
                comps = e.get("competitions", [{}])[0]
                st = e.get("status", {}).get("type", {})
                sc = []
                for t in comps.get("competitors", []):
                    sc.append(f"{t.get('team',{}).get('abbreviation')}={t.get('score')} homeAway={t.get('homeAway')}")
                # try summary for WP
                eid = e.get("id")
                hits.append((name, " | ".join(sc), st.get("detail"), eid))
        print("URL", url, "events", len(data.get("events", [])), "hits", len(hits))
        for h in hits:
            print(" ", h)
    except Exception as ex:
        print("fail", url, ex)

# search endpoints
for q in ["Florida State", "Louisville", "Columbia Lions", "Marist"]:
    try:
        data = get(f"https://site.api.espn.com/apis/common/v3/search?query={urllib.parse.quote(q)}&limit=5&type=team")
        print("search", q, json.dumps(data)[:300])
    except Exception as ex:
        print("search fail", q, ex)
