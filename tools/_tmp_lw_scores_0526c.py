import json, urllib.request

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

def walk(obj, path=""):
    if isinstance(obj, dict):
        # print athlete names when seen
        if "athlete" in obj and isinstance(obj["athlete"], dict):
            nm = obj["athlete"].get("displayName")
            if nm:
                print("ATH", path, nm, "score", obj.get("score"), "lines", obj.get("linescores"))
        for k,v in obj.items():
            if k in ("groupings","competitions","competitors","events","items","entries","athletes"):
                walk(v, path+"/"+k)
            elif k in ("name","shortName","description","detail","state") and isinstance(v,str) and any(x in v for x in ["Volynets","Birrell","Brooksby","Sonego","Mertens","Chwalinska","Ye","Jiang","Mukhin"]):
                print("HIT", path, k, v)
    elif isinstance(obj, list):
        for i,v in enumerate(obj[:200]):
            walk(v, path+f"[{i}]")

for label,url in [
    ("wta","https://site.web.api.espn.com/apis/site/v2/sports/tennis/wta/scoreboard?dates=20260925"),
    ("atp","https://site.web.api.espn.com/apis/site/v2/sports/tennis/atp/scoreboard?dates=20260925"),
    ("all","https://site.web.api.espn.com/apis/site/v2/sports/tennis/all/scoreboard"),
]:
    print("====", label)
    d=get(url)
    for e in d.get("events") or []:
        print("EVENT", e.get("name"), "groupings", len(e.get("groupings") or []))
        for g in e.get("groupings") or []:
            print("  GROUP", g.get("grouping") or g.get("name") or g.get("slug") or list(g.keys())[:8])
            # competitions inside?
            comps=g.get("competitions") or g.get("events") or []
            print("   comps/events", len(comps), "keys", list(g.keys())[:15])
            for c in comps[:30]:
                st=(c.get("status") or {}).get("type") or {}
                names=[]
                for x in c.get("competitors") or []:
                    ath=((x.get("athlete") or {}).get("displayName")) or ((x.get("team") or {}).get("displayName"))
                    ls="-".join(str((y or {}).get("value")) for y in (x.get("linescores") or []))
                    names.append(f"{ath} {x.get('score')} [{ls}]")
                if names:
                    print("   ", st.get("state"), st.get("detail") or st.get("description"), "|", " vs ".join(names))
    # also brute search names in json text
    raw=json.dumps(d)
    for key in ["Volynets","Birrell","Brooksby","Sonego","Mertens","Chwalinska","Shiyu","Jiang","Mukhin","Korniichuk"]:
        print(key, "present" if key in raw else "absent")
