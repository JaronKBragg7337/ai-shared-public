import json, urllib.request
UA = {"User-Agent": "Mozilla/5.0"}
KEYS = ("cina", "muller", "halys", "safiull", "damm", "hurkacz", "bondar", "birrell", "chengdu", "hangzhou", "adana")

def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.load(r)

for url in [
    "https://site.web.api.espn.com/apis/site/v2/sports/tennis/atp/scoreboard",
    "https://site.web.api.espn.com/apis/site/v2/sports/tennis/wta/scoreboard",
    "https://site.web.api.espn.com/apis/site/v2/sports/tennis/all/scoreboard",
]:
    print("URL", url)
    try:
        d = get(url)
    except Exception as e:
        print("ERR", e)
        continue
    for e in d.get("events", []):
        name = (e.get("name") or e.get("shortName") or "")
        st = e.get("status", {}).get("type", {})
        low = name.lower()
        if not any(k in low for k in KEYS) and st.get("state") != "in":
            continue
        if not any(k in low for k in KEYS) and st.get("state") == "in":
            # print all in-progress briefly
            pass
        comps = (e.get("competitions") or [{}])[0]
        parts = []
        for c in comps.get("competitors", []):
            ath = c.get("athlete") or {}
            nm = ath.get("displayName") or (c.get("team") or {}).get("displayName") or "?"
            ls = c.get("linescores") or []
            sets = "-".join(str(x.get("value", x.get("displayValue", ""))) for x in ls)
            parts.append(f"{nm} score={c.get('score')} sets={sets}")
        print(st.get("state"), st.get("detail"), "|", name, "|", " / ".join(parts))
