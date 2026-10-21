import json, urllib.request

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.load(r)

for label, url in [
    ("tennis_all", "https://site.web.api.espn.com/apis/site/v2/sports/tennis/all/scoreboard"),
    ("wta", "https://site.web.api.espn.com/apis/site/v2/sports/tennis/wta/scoreboard"),
    ("atp", "https://site.web.api.espn.com/apis/site/v2/sports/tennis/atp/scoreboard"),
]:
    try:
        d = get(url)
    except Exception as ex:
        print(label, "ERR", ex)
        continue
    print("===", label, "===")
    for e in d.get("events", [])[:40]:
        st = e.get("status", {}).get("type", {})
        if st.get("state") not in ("in", "pre"):
            # still print in-progress only
            if st.get("state") != "in":
                continue
        name = e.get("name") or e.get("shortName") or ""
        comps = (e.get("competitions") or [{}])[0]
        lines = []
        for c in comps.get("competitors", []):
            ath = c.get("athlete", {}) or {}
            t = c.get("team", {}) or {}
            nm = ath.get("displayName") or t.get("displayName") or t.get("abbreviation") or "?"
            lines.append(f"{nm} {c.get('score','')} ({c.get('homeAway')})")
        print(st.get("state"), st.get("detail"), "|", name, "|", " / ".join(lines))
