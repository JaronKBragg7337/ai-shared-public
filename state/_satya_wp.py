import json, urllib.request

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.load(r)

for eid, label in [("401858254", "FSU@LOU"), ("401868265", "COLU@MRST")]:
    print("====", label, eid)
    # summary
    for path in [
        f"https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event={eid}",
        f"https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event={eid}&region=us&lang=en",
    ]:
        try:
            d = get(path)
            # winprobability array
            wp = d.get("winprobability") or []
            if wp:
                last = wp[-1]
                print("last WP keys", list(last.keys()))
                print("last WP", last)
            # header competitions
            header = d.get("header") or {}
            comps = (header.get("competitions") or [{}])[0]
            print("status", (comps.get("status") or {}).get("type", {}).get("detail"))
            for t in comps.get("competitors", []):
                print(" team", t.get("team",{}).get("abbreviation"), "score", t.get("score"), "homeAway", t.get("homeAway"), "prob", t.get("probability"))
            # situation
            sit = comps.get("situation") or d.get("situation") or {}
            if sit:
                print("sit", {k:sit.get(k) for k in list(sit)[:12]})
            # predictor
            pred = d.get("predictor") or {}
            if pred:
                print("predictor keys", list(pred.keys())[:20])
                print("predictor snippet", json.dumps(pred)[:500])
            break
        except Exception as ex:
            print("fail", path, ex)

# also pull live board prices from file
print("==== live-board refresh via python scrape of state file timestamp")
