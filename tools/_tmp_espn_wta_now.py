import json, urllib.request
req = urllib.request.Request(
    "https://site.api.espn.com/apis/site/v2/sports/tennis/wta/scoreboard",
    headers={"User-Agent": "Mozilla/5.0"},
)
d = json.load(urllib.request.urlopen(req, timeout=25))
keys = ["lazaro", "fruhvirtova", "kalieva", "shi", "sasnovich", "lepchenko", "bassols", "xiaodi"]
for e in d.get("events", []):
    groups = e.get("groupings") or []
    comps = []
    if groups:
        for g in groups:
            comps.extend(g.get("competitions") or [])
    else:
        comps = e.get("competitions") or []
    for c in comps:
        names = " ".join(
            ((x.get("athlete") or {}).get("displayName") or "")
            for x in c.get("competitors") or []
        ).lower()
        if not any(k in names for k in keys):
            continue
        st = (c.get("status") or {}).get("type") or {}
        rows = []
        for x in c.get("competitors") or []:
            nm = (x.get("athlete") or {}).get("displayName") or "?"
            sets = "-".join(str(int(l.get("value", 0))) for l in (x.get("linescores") or []))
            rows.append("%s %s pts=%s" % (nm, sets, x.get("score")))
        print(st.get("state"), st.get("detail"), "|", " || ".join(rows))
