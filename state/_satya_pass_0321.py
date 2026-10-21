import json, urllib.request, ssl, sys
sys.path.insert(0, r"C:\Users\lilli\AI-Shared\tools")
import executor as X
ctx = ssl.create_default_context()
H = {"User-Agent": "Mozilla/5.0"}

def get(u):
    req = urllib.request.Request(u, headers=H)
    return json.loads(urllib.request.urlopen(req, timeout=25, context=ctx).read())

sb = get("https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?groups=80")
live=[]
for e in sb.get("events", []):
    comp=e["competitions"][0]
    st=comp["status"]["type"]
    if st.get("state")!="in":
        continue
    rows=[(c.get("homeAway"), c["team"].get("abbreviation"), c.get("score")) for c in comp["competitors"]]
    live.append((e.get("id"), e.get("name",""), st.get("detail"), rows))
    print("LIVE", e.get("id"), e.get("name"), "|", st.get("detail"), rows)
print("---WPs---")
for eid,name,status,rows in live:
    try:
        j=get(f"https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event={eid}")
        wps=j.get("winprobability") or []
        wp=wps[-1] if wps else {}
        hwp=float(wp.get("homeWinPercentage") or 0)
        print(name, "|", status, "| homeWP", round(hwp*100,1), "awayWP", round((1-hwp)*100,1), "|", rows)
    except Exception as ex:
        print(name, "WPERR", ex)
print("---BOOKS---")
m=X.Mcp()
slugs=[
 "aec-cfb-bayl-arzst-2026-10-03",
 "aec-cfb-frest-washst-2026-10-03",
 "aec-cfb-txst-sdst-2026-10-03",
 "aec-cfb-cin-arz-2026-10-03",
 "aec-cfb-mia-clmsn-2026-10-03",
 "atc-intf-usa-mex-2026-10-03-usa",
 "atc-intf-usa-mex-2026-10-03-mex",
 "atc-intf-usa-mex-2026-10-03-draw",
]
for slug in slugs:
    try:
        b=m.call("polymarket_get_book", {"market_slug": slug})
        print(slug, str(b)[:260].replace("\n"," "))
    except Exception as e:
        print(slug, "ERR", e)
print("---POSITIONS---")
try:
    pos=m.call("polymarket_positions", {})
    print(str(pos)[:4000])
except Exception as e:
    print("pos ERR", e)
print("---OPEN ORDERS---")
try:
    oo=m.call("polymarket_open_orders", {})
    print(str(oo)[:3000])
except Exception as e:
    print("oo ERR", e)
