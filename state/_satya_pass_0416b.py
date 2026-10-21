import urllib.request, json

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    return json.load(urllib.request.urlopen(req, timeout=25))

# FCS / all groups search
print("=== SEARCH MTST ANY STATE ===")
for dates in ["20261002", "20261003", "20261004"]:
    for groups in ["80", "81", "", None]:
        if groups is None:
            url = f"https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?dates={dates}&limit=400"
        elif groups == "":
            url = f"https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?dates={dates}&groups=80,81&limit=400"
        else:
            url = f"https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?dates={dates}&groups={groups}&limit=400"
        try:
            data = get(url)
        except Exception as e:
            print("err", dates, groups, e)
            continue
        for ev in data.get("events") or []:
            name = ev.get("name", "")
            if "Montana State" in name or ("Idaho" in name and "Vandals" in name):
                comp = (ev.get("competitions") or [{}])[0]
                st = (comp.get("status") or {}).get("type", {})
                print(dates, "g", groups, name, "|", st.get("detail"), st.get("state"), "completed", st.get("completed"))
                for c in comp.get("competitors") or []:
                    print(" ", c.get("team", {}).get("abbreviation"), c.get("score"), c.get("homeAway"), "winner", c.get("winner"))

# site search
print("=== SITE SEARCH ===")
try:
    q = urllib.parse.quote if False else __import__("urllib.parse").parse.quote
    url = "https://site.web.api.espn.com/apis/common/v3/search?query=Montana%20State%20Idaho&limit=10&type=player,team,league,event"
    data = get(url)
    for item in (data.get("items") or data.get("results") or [])[:15]:
        print(item.get("displayName") or item.get("name") or item)
except Exception as e:
    print("search err", e)

# try scoreboard with conferences FCS Big Sky
print("=== BIG SKY / FCS ===")
for conf in [20, 40, 48, 18, 17]:
    try:
        data = get(f"https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?dates=20261003&groups={conf}&limit=100")
        for ev in data.get("events") or []:
            name = ev.get("name", "")
            if "Montana" in name or "Idaho" in name:
                comp = (ev.get("competitions") or [{}])[0]
                st = (comp.get("status") or {}).get("type", {})
                print("conf", conf, name, st.get("detail"), st.get("state"))
                for c in comp.get("competitors") or []:
                    print(" ", c.get("team", {}).get("abbreviation"), c.get("score"), c.get("homeAway"))
    except Exception as e:
        print("conf", conf, e)

print("DONE")
