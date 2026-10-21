import json, urllib.request

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.load(r)

for path in ["tennis/atp", "tennis/wta", "tennis/all"]:
    try:
        d = get(f"https://site.api.espn.com/apis/site/v2/sports/{path}/scoreboard")
    except Exception as ex:
        print(path, "ERR", ex)
        continue
    print("===", path, "===")
    for e in d.get("events", []):
        groups = e.get("groupings") or []
        comps = []
        if groups:
            for g in groups:
                comps.extend(g.get("competitions") or [])
        else:
            comps = e.get("competitions") or []
        for c in comps:
            st = (c.get("status") or {}).get("type") or {}
            if st.get("state") not in ("in", "pre"):
                continue
            rows = []
            for x in c.get("competitors") or []:
                ath = x.get("athlete") or {}
                nm = ath.get("displayName") or "?"
                sets = [str(int(l.get("value", 0))) for l in (x.get("linescores") or [])]
                cur = x.get("score", "")
                set_s = "-".join(sets) if sets else "?"
                rows.append("%s sets=%s pts=%s" % (nm, set_s, cur))
            detail = st.get("detail") or st.get("shortDetail")
            print(st.get("state"), detail, "|", " || ".join(rows))
