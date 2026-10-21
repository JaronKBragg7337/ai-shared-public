import json, urllib.request

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.load(r)

urls = [
    "https://site.api.espn.com/apis/site/v2/sports/tennis/atp/scoreboard",
    "https://site.api.espn.com/apis/site/v2/sports/tennis/atp/scoreboard?dates=20260927",
    "https://site.api.espn.com/apis/site/v2/sports/tennis/all/scoreboard?dates=20260927",
]
for u in urls:
    try:
        d = get(u)
        evs = d.get("events") or []
        print("URL", u.split("sports/")[-1], "events", len(evs))
        for e in evs:
            name = e.get("name") or e.get("shortName") or ""
            keys = ("Gaston", "Rublev", "Muller", "Fokina", "Davidovich", "Digvijay", "Nordquist", "Wang", "Kubareva")
            if not any(k in name for k in keys):
                # print all in-progress briefly
                st = (e.get("status") or {}).get("type") or {}
                if st.get("state") == "in":
                    print(" IN", st.get("detail"), "|", name)
                continue
            st = (e.get("status") or {}).get("type") or {}
            comps = (e.get("competitions") or [{}])[0]
            lines = []
            for c in comps.get("competitors", []):
                ath = c.get("athlete") or {}
                nm = ath.get("displayName") or ((c.get("team") or {}).get("displayName")) or "?"
                ls = c.get("linescores") or []
                sets = "-".join(str(x.get("value")) for x in ls) if ls else c.get("score")
                lines.append(f"{nm}:{sets}")
            print("HIT", st.get("state"), st.get("detail"), "|", name, "|", " / ".join(lines))
    except Exception as ex:
        print("ERR", u, ex)
