import json, urllib.request

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.load(r)

print("=== ESPN tennis all deep ===")
try:
    d = get("https://site.web.api.espn.com/apis/site/v2/sports/tennis/all/scoreboard")
    for e in d.get("events", []):
        name = e.get("name") or e.get("shortName")
        st = e.get("status", {}).get("type", {})
        print("EVENT", name, st.get("state"), st.get("description"))
        for comp in e.get("competitions") or []:
            cst = (comp.get("status") or {}).get("type") or {}
            lines = []
            for c in comp.get("competitors") or []:
                ath = (c.get("athlete") or {}).get("displayName") or (c.get("team") or {}).get("displayName") or "?"
                ls = c.get("linescores") or []
                lsv = "-".join(str(x.get("value")) for x in ls)
                lines.append(f"{ath} tot={c.get('score')} sets={lsv}")
            note = (comp.get("notes") or [{}])
            ntxt = note[0].get("text") if note else ""
            print("  COMP", cst.get("state"), cst.get("detail") or cst.get("description"), "|", " / ".join(lines), "|", ntxt)
except Exception as ex:
    print("espn fail", ex)

for sport in ["tennis", "table-tennis"]:
    print(f"=== sofa {sport} live ===")
    try:
        d = get(f"https://api.sofascore.com/api/v1/sport/{sport}/events/live")
        evs = d.get("events") or []
        print("count", len(evs))
        for ev in evs:
            h = (ev.get("homeTeam") or {}).get("name", "")
            a = (ev.get("awayTeam") or {}).get("name", "")
            sc = ev.get("homeScore") or {}
            ac = ev.get("awayScore") or {}
            def periods(s):
                return "-".join(str(s.get(f"period{i}")) for i in range(1, 6))
            print(f"{h} {sc.get('current')}({periods(sc)}) vs {a} {ac.get('current')}({periods(ac)}) | {(ev.get('status') or {}).get('description')} | {(ev.get('tournament') or {}).get('name')}")
    except Exception as ex:
        print("sofa fail", ex)

# also scheduled today tennis search for our names via sofa scheduled
print("=== sofa tennis scheduled today ===")
try:
    d = get("https://api.sofascore.com/api/v1/sport/tennis/scheduled-events/2026-09-25")
    evs = d.get("events") or []
    keys = ["Volynets", "Birrell", "Brooksby", "Sonego", "Mertens", "Chwalinska", "Ye", "Jiang", "Mukhin", "Korniichuk"]
    for ev in evs:
        h = (ev.get("homeTeam") or {}).get("name", "")
        a = (ev.get("awayTeam") or {}).get("name", "")
        blob = h + " " + a
        if any(k.lower() in blob.lower() for k in keys):
            sc = ev.get("homeScore") or {}
            ac = ev.get("awayScore") or {}
            print(f"{h} vs {a} | status={(ev.get('status') or {}).get('description')} | score {sc} / {ac} | tour={(ev.get('tournament') or {}).get('name')}")
except Exception as ex:
    print("sched fail", ex)
