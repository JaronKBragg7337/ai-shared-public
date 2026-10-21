import json, urllib.request

def get(url, headers=None):
    h = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36", "Accept": "application/json,text/plain,*/*", "Referer": "https://www.espn.com/"}
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, headers=h)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

urls = [
    "https://site.web.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?groups=80&limit=300",
    "https://cdn.espn.com/core/college-football/scoreboard?xhr=1&limit=300",
]
for url in urls:
    try:
        data = get(url)
        print("OK", url[:60], "keys", list(data.keys())[:8])
        # try extract events
        events = data.get("events") or (data.get("content") or {}).get("sbData", {}).get("events") or []
        print(" events", len(events))
        keys = ["FRES", "SJSU", "PUR", "UCLA", "JMU", "SDSU", "NDSU", "SDAK", "BOIS", "FRESNO", "PURDUE", "JAMES MADISON", "BOISE", "SOUTH DAKOTA", "SAN JOSE"]
        for e in events:
            c = e["competitions"][0]
            st = c["status"]; typ = st["type"]
            teams = [(t["homeAway"], t["team"].get("abbreviation",""), t.get("score"), t["team"].get("displayName","")) for t in c["competitors"]]
            blob = " ".join(x[1]+" "+x[3] for x in teams).upper()
            if not any(k in blob for k in keys):
                continue
            print("CFB", typ.get("state"), e.get("shortName"), typ.get("detail"), "clock", st.get("displayClock"), "p", st.get("period"), "id", e.get("id"))
            for row in teams:
                print(" ", *row)
        break
    except Exception as ex:
        print("FAIL", url[:50], type(ex).__name__, ex)

# Yahoo sports scoreboard scrape-ish API
yahoo_urls = [
    "https://api-secure.sports.yahoo.com/v1/editorial/s/scoreboard?leagues=ncaaf&format=json",
    "https://sports.yahoo.com/college-football/scoreboard/",
]
for url in yahoo_urls:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=25) as r:
            body = r.read()[:5000]
            print("YAHOO", url[:50], "len", len(body), body[:200])
    except Exception as ex:
        print("YAHOO FAIL", type(ex).__name__, ex)

# tennis
for league in ["wta", "atp"]:
    for base in [
        f"https://site.web.api.espn.com/apis/site/v2/sports/tennis/{league}/scoreboard",
        f"https://site.api.espn.com/apis/site/v2/sports/tennis/{league}/scoreboard",
    ]:
        try:
            data = get(base)
            n=0
            for e in data.get("events", []):
                c=e["competitions"][0]; typ=c["status"]["type"]
                if typ.get("state")!="in":
                    continue
                n+=1
                print("TENNIS", league, e.get("name"), typ.get("detail"))
                for t in c["competitors"]:
                    who=(t.get("athlete") or {}).get("displayName") or (t.get("team") or {}).get("displayName")
                    print(" ", t.get("homeAway"), who, t.get("score"), t.get("linescores"))
            print("TENNIS", league, "live", n, "via", base[:40])
            break
        except Exception as ex:
            print("TENNIS FAIL", league, base[:40], type(ex).__name__, ex)
