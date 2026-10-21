import urllib.request, json

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.load(r)

def detail(url, matchers):
    data = get(url)
    for ev in data.get("events") or []:
        name = (ev.get("name") or "") + " " + (ev.get("shortName") or "")
        low = name.lower()
        if not any(m in low for m in matchers):
            continue
        comp = (ev.get("competitions") or [{}])[0]
        status = (comp.get("status") or {}).get("type", {})
        print("NAME", name.strip())
        print("STATUS", status.get("state"), status.get("detail"))
        for c in comp.get("competitors") or []:
            t = c.get("team", {})
            p = c.get("probability") or {}
            print(" ", t.get("abbreviation"), t.get("displayName"), "score", c.get("score"),
                  "homeAway", c.get("homeAway"), "prob", p)
        print("raw status", json.dumps(status)[:300])

print("=== PSU/NU ===")
detail("https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?dates=20261002",
       ["penn", "northwestern"])
detail("https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?groups=80",
       ["penn", "northwestern"])

print("=== Montana/Idaho ===")
for u in [
    "https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?dates=20261002",
    "https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?dates=20261003",
    "https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard",
]:
    try:
        detail(u, ["montana", "idaho", "bobcat", "vandals"])
    except Exception as e:
        print("ERR", e)

# FCS scoreboard sometimes separate
print("=== FCS try ===")
for u in [
    "https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?groups=81&dates=20261002",
    "https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?groups=81&dates=20261003",
]:
    try:
        data = get(u)
        print(u, "events", len(data.get("events") or []))
        for ev in data.get("events") or []:
            name = ev.get("name") or ""
            if any(k in name.lower() for k in ["montana", "idaho", "bobcat", "vandal"]):
                print("HIT", name)
                detail(u, ["montana", "idaho", "bobcat", "vandal"])
    except Exception as e:
        print("ERR", e)

print("=== Jamaica ===")
detail("https://site.api.espn.com/apis/site/v2/sports/soccer/concacaf.nations.league/scoreboard",
       ["jamaica", "salvador"])
