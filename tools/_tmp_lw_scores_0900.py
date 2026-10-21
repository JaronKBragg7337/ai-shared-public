import json, urllib.request

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.load(r)

keys = ("medvedev", "rublev", "giustino", "sperle", "komano", "ciocan", "pennaforti", "bouzige", "hoole", "meerschen")

for label, url in [
    ("live", "https://api.sofascore.com/api/v1/sport/tennis/events/live"),
    ("day", "https://api.sofascore.com/api/v1/sport/tennis/scheduled-events/2026-09-29"),
]:
    try:
        d = get(url)
        evs = d.get("events") or []
        print(label, "count", len(evs))
        for ev in evs:
            h = (ev.get("homeTeam") or {}).get("name", "")
            a = (ev.get("awayTeam") or {}).get("name", "")
            blob = (h + " " + a).lower()
            if not any(k in blob for k in keys):
                continue
            sc = ev.get("homeScore") or {}
            ac = ev.get("awayScore") or {}
            st = (ev.get("status") or {}).get("description")
            tn = (ev.get("tournament") or {}).get("name")
            print(h, sc, "vs", a, ac, "|", st, "|", tn)
    except Exception as e:
        print(label, "fail", type(e).__name__, e)
