import json, urllib.request

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
headers = {"User-Agent": UA, "Accept": "application/json"}
needles = ("mayot", "cassone", "wong", "vallejo", "timofeeva", "pohankova", "forti", "sharma", "cobolli")

def get(url):
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.load(r)

# SofaScore live tennis
try:
    d = get("https://api.sofascore.com/api/v1/sport/tennis/events/live")
    evs = d.get("events") or []
    print("sofa live", len(evs))
    for ev in evs:
        h = (ev.get("homeTeam") or {}).get("name", "")
        a = (ev.get("awayTeam") or {}).get("name", "")
        blob = (h + " " + a).lower()
        if any(n in blob for n in needles) or True:
            sc = ev.get("homeScore") or {}
            ac = ev.get("awayScore") or {}
            st = (ev.get("status") or {}).get("description")
            tour = (ev.get("tournament") or {}).get("name")
            if any(n in blob for n in needles):
                print(f"HIT {h} {sc.get('current')}({sc.get('period1')}-{sc.get('period2')}-{sc.get('period3')}) vs {a} {ac.get('current')}({ac.get('period1')}-{ac.get('period2')}-{ac.get('period3')}) | {st} | {tour}")
except Exception as e:
    print("sofa fail", e)

# ESPN scoreboards
for league in ("atp", "wta", "atpchallenger", "challenger", "itf"):
    url = f"https://site.api.espn.com/apis/site/v2/sports/tennis/{league}/scoreboard"
    try:
        d = get(url)
        evs = d.get("events") or []
        print(league, "events", len(evs))
        for e in evs:
            name = e.get("name") or ""
            if not any(n in name.lower() for n in needles):
                continue
            comps = e.get("competitions") or [{}]
            c = comps[0] if comps else {}
            status = ((c.get("status") or {}).get("type") or {}).get("detail") or ((e.get("status") or {}).get("type") or {}).get("detail")
            bits = []
            for a in c.get("competitors") or []:
                nm = ((a.get("athlete") or {}).get("displayName") or (a.get("team") or {}).get("displayName"))
                bits.append(f"{nm} score={a.get('score')} lines={a.get('linescores')}")
            print(" ", name, "|", status, "|", " // ".join(bits))
    except Exception as e:
        print(league, "fail", e)

# also try full tennis core API search
try:
    d = get("https://site.api.espn.com/apis/site/v2/sports/tennis/scoreboard?limit=200")
    evs = d.get("events") or []
    print("tennis generic events", len(evs))
    for e in evs:
        name = e.get("name") or ""
        if any(n in name.lower() for n in needles):
            print("GEN", name, e.get("id"))
            comps = e.get("competitions") or [{}]
            c = comps[0] if comps else {}
            for a in c.get("competitors") or []:
                nm = ((a.get("athlete") or {}).get("displayName") or (a.get("team") or {}).get("displayName"))
                print("   ", nm, a.get("score"), a.get("linescores"))
except Exception as e:
    print("generic fail", e)
