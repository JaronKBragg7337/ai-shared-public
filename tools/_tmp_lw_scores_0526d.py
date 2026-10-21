import json, urllib.request

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

KEYS = ["Volynets", "Birrell", "Brooksby", "Sonego", "Mertens", "Chwalinska", "Ye", "Jiang"]

def names_of(comp):
    out=[]
    for x in comp.get("competitors") or []:
        ath=((x.get("athlete") or {}).get("displayName")) or ((x.get("team") or {}).get("displayName")) or "?"
        ls="-".join(str((y or {}).get("value")) for y in (x.get("linescores") or []))
        out.append((ath, x.get("score"), ls, x.get("winner"), x.get("homeAway")))
    return out

for label,url in [
    ("wta","https://site.web.api.espn.com/apis/site/v2/sports/tennis/wta/scoreboard?dates=20260925"),
    ("atp","https://site.web.api.espn.com/apis/site/v2/sports/tennis/atp/scoreboard?dates=20260925"),
    ("all","https://site.web.api.espn.com/apis/site/v2/sports/tennis/all/scoreboard"),
]:
    print("====", label)
    d=get(url)
    hits=0
    for e in d.get("events") or []:
        for g in e.get("groupings") or []:
            for c in g.get("competitions") or []:
                ns=names_of(c)
                blob=" ".join(n[0] for n in ns)
                if any(k.lower() in blob.lower() for k in KEYS):
                    st=(c.get("status") or {}).get("type") or {}
                    print(e.get("name"), "|", st.get("state"), st.get("detail") or st.get("description"), "|", ns)
                    hits += 1
    print("hits", hits)

# also dump any competition with state==in anywhere
print("==== ANY IN-PROGRESS ====")
for label,url in [
    ("wta","https://site.web.api.espn.com/apis/site/v2/sports/tennis/wta/scoreboard?dates=20260925"),
    ("atp","https://site.web.api.espn.com/apis/site/v2/sports/tennis/atp/scoreboard?dates=20260925"),
    ("all","https://site.web.api.espn.com/apis/site/v2/sports/tennis/all/scoreboard"),
]:
    d=get(url)
    for e in d.get("events") or []:
        for g in e.get("groupings") or []:
            for c in g.get("competitions") or []:
                st=(c.get("status") or {}).get("type") or {}
                if st.get("state")=="in":
                    print(label, e.get("name"), st.get("detail"), names_of(c))
