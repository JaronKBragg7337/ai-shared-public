import json, urllib.request
UA = {"User-Agent": "Mozilla/5.0"}

def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.load(r)

def dump_comp(comp, indent=0):
    st = (comp.get("status") or {}).get("type") or {}
    parts = []
    for c in comp.get("competitors") or []:
        ath = c.get("athlete") or {}
        nm = ath.get("displayName") or (c.get("team") or {}).get("displayName") or "?"
        ls = c.get("linescores") or []
        sets = "-".join(str(x.get("value", x.get("displayValue", ""))) for x in ls)
        parts.append(f"{nm}:{c.get('score')}/{sets}")
    print(" " * indent, st.get("state"), st.get("detail"), "|", " / ".join(parts), "|", comp.get("notes"))
    for sub in comp.get("details") or []:
        pass

for label, url in [
    ("atp", "https://site.web.api.espn.com/apis/site/v2/sports/tennis/atp/scoreboard"),
    ("all", "https://site.web.api.espn.com/apis/site/v2/sports/tennis/all/scoreboard"),
]:
    print("===", label, "===")
    d = get(url)
    for e in d.get("events", []):
        name = e.get("name") or e.get("shortName") or ""
        print("EVENT", name, "keys", list(e.keys())[:20])
        comps = e.get("competitions") or []
        print(" ncomps", len(comps))
        for comp in comps[:30]:
            dump_comp(comp, 1)
            # sometimes group events nest further
            for k in ("group", "groupings", "notes", "type"):
                if k in comp:
                    print("  ", k, str(comp.get(k))[:200])
        # also check leagues/calendar style
        if not comps:
            print(json.dumps(e, indent=2)[:1500])
