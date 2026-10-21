import json,urllib.request,ssl,sys
sys.path.insert(0,r"C:\Users\lilli\AI-Shared\tools")
import executor as X
ctx=ssl.create_default_context(); H={"User-Agent":"Mozilla/5.0"}
def get(u):
    return json.loads(urllib.request.urlopen(urllib.request.Request(u,headers=H),timeout=25,context=ctx).read())
s=get("https://site.api.espn.com/apis/site/v2/sports/soccer/fifa.friendly/scoreboard")
eid=None
for e in s.get("events",[]):
    n=e.get("name","")
    if "Mexico" in n and ("United States" in n or "USA" in n):
        eid=e.get("id"); print("event",eid,n,e["status"]["type"].get("detail"))
        comp=e["competitions"][0]
        for c in comp["competitors"]:
            print(" ",c.get("homeAway"),c["team"].get("abbreviation"),c.get("score"), c.get("form"))
        print(" situation", (comp.get("situation") or {}) )
if eid:
    j=get(f"https://site.api.espn.com/apis/site/v2/sports/soccer/fifa.friendly/summary?event={eid}")
    print("keys", list(j.keys())[:30])
    wps=j.get("winprobability") or []
    print("wp len", len(wps))
    if wps:
        print("last wp", wps[-1])
    # predictor?
    pred=j.get("predictor") or j.get("pickcenter") or {}
    print("predictor", str(pred)[:400])
    h=j.get("header",{}); comps=(h.get("competitions") or [{}])[0]
    print("header status", (comps.get("status") or {}).get("type"))
m=X.Mcp()
for slug in ["atc-intf-usa-mex-2026-10-03-usa","atc-intf-usa-mex-2026-10-03-mex","atc-intf-usa-mex-2026-10-03-draw","tsc-intf-usa-mex-2026-10-03-1pt5","tsc-intf-usa-mex-2026-10-03-2pt5"]:
    b=m.call("polymarket_bbo",{"slug":slug})
    md=b.get("marketData") or {}
    print(slug, "bid/ask", (md.get("bestBid") or {}).get("value"), (md.get("bestAsk") or {}).get("value"), "last", (md.get("lastTradePx") or {}).get("value"))
