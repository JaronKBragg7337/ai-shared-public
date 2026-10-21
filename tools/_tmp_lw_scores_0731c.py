import json, urllib.request
UA = {"User-Agent": "Mozilla/5.0"}
KEYS = ("halys", "safiull", "cina", "muller", "damm", "hurkacz", "bondar", "birrell")

def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.load(r)

def walk(d):
    for e in d.get("events", []):
        for g in e.get("groupings") or []:
            for comp in g.get("competitions") or []:
                notes = " ".join(n.get("text", "") for n in (comp.get("notes") or []))
                parts = []
                names = []
                for c in comp.get("competitors") or []:
                    ath = c.get("athlete") or {}
                    nm = ath.get("displayName") or (c.get("team") or {}).get("displayName") or "?"
                    names.append(nm)
                    ls = c.get("linescores") or []
                    sets = "-".join(str(x.get("value", x.get("displayValue", ""))) for x in ls)
                    parts.append(f"{nm} sc={c.get('score')} sets={sets} winner={c.get('winner')}")
                blob = (" ".join(names) + " " + notes).lower()
                st = (comp.get("status") or {}).get("type") or {}
                if any(k in blob for k in KEYS) or st.get("state") == "in":
                    print(e.get("shortName"), "|", st.get("state"), st.get("detail"), "|", " / ".join(parts), "|", notes)

for url in [
    "https://site.web.api.espn.com/apis/site/v2/sports/tennis/atp/scoreboard",
    "https://site.web.api.espn.com/apis/site/v2/sports/tennis/wta/scoreboard",
]:
    print("URL", url)
    walk(get(url))
