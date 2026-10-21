import json,urllib.request,ssl,sys
sys.path.insert(0,r"C:\Users\lilli\AI-Shared\tools")
import executor as X
ctx=ssl.create_default_context(); H={"User-Agent":"Mozilla/5.0"}
def get(u):
    return json.loads(urllib.request.urlopen(urllib.request.Request(u,headers=H),timeout=25,context=ctx).read())
m=X.Mcp()
oo=m.call("polymarket_open_orders",{})
orders=(oo or {}).get("orders") or []
print("OPEN ORDERS",len(orders))
for o in orders:
    print(o.get("id"), o.get("marketSlug"), o.get("intent"), o.get("price"), "cum",o.get("cumQuantity"),"leaves",o.get("leavesQuantity"), o.get("state"))
# CIN summary
j=get("https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event=401856820")
wps=j.get("winprobability") or []; wp=wps[-1] if wps else {}
hwp=float(wp.get("homeWinPercentage") or 0)
h=j.get("header",{}); comps=(h.get("competitions") or [{}])[0]
status=(comps.get("status") or {}).get("type",{}).get("detail")
rows=[(c.get("homeAway"),c.get("team",{}).get("abbreviation"),c.get("score")) for c in comps.get("competitors",[])]
print("CIN",rows,status,"homeWP",round(hwp*100,1),"awayWP",round((1-hwp)*100,1))
b=m.call("polymarket_bbo",{"slug":"aec-cfb-cin-arz-2026-10-03"})
md=b.get("marketData") or b
ask=float((md.get("bestAsk") or {}).get("value") or 0); bid=float((md.get("bestBid") or {}).get("value") or 0)
cin_wp=round((1-hwp)*100,1)
print("CIN book",bid,ask,"gap_c",round(cin_wp-ask*100,1))
# BAY
j2=get("https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event=401856817")
wps2=j2.get("winprobability") or []; wp2=wps2[-1] if wps2 else {}
hwp2=float(wp2.get("homeWinPercentage") or 0)
h2=j2.get("header",{}); comps2=(h2.get("competitions") or [{}])[0]
status2=(comps2.get("status") or {}).get("type",{}).get("detail")
rows2=[(c.get("homeAway"),c.get("team",{}).get("abbreviation"),c.get("score")) for c in comps2.get("competitors",[])]
print("BAY",rows2,status2,"homeWP",round(hwp2*100,1),"awayWP",round((1-hwp2)*100,1))
b2=m.call("polymarket_bbo",{"slug":"aec-cfb-bayl-arzst-2026-10-03"}); md2=b2.get("marketData") or b2
ask2=float((md2.get("bestAsk") or {}).get("value") or 0)
bay_wp=round((1-hwp2)*100,1)
print("BAY book ask",ask2,"gap_c",round(bay_wp-ask2*100,1))
# soccer USA MEX try
for u in [
 "https://site.api.espn.com/apis/site/v2/sports/soccer/usa.1/scoreboard",
 "https://site.api.espn.com/apis/site/v2/sports/soccer/fifa.worldq.concacaf/scoreboard",
 "https://site.api.espn.com/apis/site/v2/sports/soccer/fifa.friendly/scoreboard",
]:
    try:
        s=get(u)
        for e in s.get("events",[]):
            n=e.get("name","")
            if "Mexico" in n or "United States" in n or "USA" in n:
                st=e["status"]["type"]
                comp=e["competitions"][0]
                rows=[(c.get("homeAway"),c["team"].get("abbreviation"),c.get("score")) for c in comp["competitors"]]
                print("SOCCER",u.split("/")[-2], n, st.get("detail"), rows)
    except Exception as ex:
        print("SOCCER ERR",u,ex)
