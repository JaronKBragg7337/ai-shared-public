import json, urllib.request

def get(url, headers=None):
    h = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36", "Accept": "application/json,text/html,*/*"}
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, headers=h)
    with urllib.request.urlopen(req, timeout=30) as r:
        raw = r.read()
        ctype = r.headers.get("Content-Type", "")
        return raw, ctype

urls = [
    "https://site.web.api.espn.com/apis/site/v2/sports/tennis/wta/scoreboard?dates=20260925",
    "https://site.web.api.espn.com/apis/site/v2/sports/tennis/atp/scoreboard?dates=20260925",
    "https://site.api.espn.com/apis/site/v2/sports/tennis/wta/scoreboard?dates=20260925",
    "https://www.espn.com/tennis/scoreboard/_/league/wta/date/20260925",
    "https://www.espn.com/tennis/scoreboard/_/league/atp/date/20260925",
    "https://api.sofascore.com/api/v1/sport/tennis/events/live",
    "https://www.sofascore.com/api/v1/sport/tennis/events/live",
    "https://www.flashscore.com/tennis/",
]
for url in urls:
    print("URL", url)
    try:
        raw, ctype = get(url)
        print("  ok", len(raw), ctype[:60])
        text = raw.decode("utf-8", "replace")
        if "application/json" in ctype or text.lstrip().startswith("{"):
            d = json.loads(text)
            evs = d.get("events") or []
            print("  events", len(evs), "topkeys", list(d.keys())[:12])
            for e in evs[:15]:
                st = (e.get("status") or {}).get("type") or e.get("status") or {}
                if isinstance(st, dict):
                    state = st.get("state") or st.get("description") or st.get("type")
                else:
                    state = st
                name = e.get("name") or e.get("shortName") or ""
                if not name:
                    h = (e.get("homeTeam") or {}).get("name", "")
                    a = (e.get("awayTeam") or {}).get("name", "")
                    name = f"{h} vs {a}"
                print("   ", state, "|", name)
                for c in ((e.get("competitions") or [{}])[0].get("competitors") or []):
                    ath = ((c.get("athlete") or {}).get("displayName")) or ((c.get("team") or {}).get("displayName"))
                    print("      ", ath, c.get("score"), c.get("linescores"))
        else:
            for key in ["Volynets", "Birrell", "Brooksby", "Sonego", "Mertens", "Chwalinska", "Mukhin", "Korniichuk", "Shiyu", "Jiang"]:
                if key in text:
                    print("  html hit", key)
            # espn scoreboard embeds?
            if "__espnfitt__" in text or "scoreboard" in text.lower():
                print("  html has scoreboard chrome")
    except Exception as ex:
        print("  FAIL", ex)

# dump raw korea event competitions length via all scoreboard with leagues
print("=== leagues dump ===")
raw, _ = get("https://site.web.api.espn.com/apis/site/v2/sports/tennis/all/scoreboard")
d = json.loads(raw)
for lg in d.get("leagues") or []:
    print("league", lg.get("name"), "events?", "events" in lg, list(lg.keys())[:10])
for e in d.get("events") or []:
    print(e.get("name"), "comps", len(e.get("competitions") or []), "keys", list(e.keys()))
    # print truncated json of first competition if any
    comps = e.get("competitions") or []
    if comps:
        print(json.dumps(comps[0], indent=0)[:500])
