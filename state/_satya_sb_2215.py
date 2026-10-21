import json, urllib.request, ssl
ctx = ssl.create_default_context()
H = {"User-Agent": "Mozilla/5.0"}

def get(u):
    req = urllib.request.Request(u, headers=H)
    return json.loads(urllib.request.urlopen(req, timeout=25, context=ctx).read())

url = "https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?groups=80&limit=300"
data = get(url)
print("events", len(data.get("events", [])))
for e in data.get("events", []):
    comp = e["competitions"][0]
    st = comp["status"]["type"]
    if st.get("state") != "in":
        continue
    name = e.get("name", "")
    eid = e.get("id")
    status = st.get("detail") or st.get("description")
    rows = []
    for c in comp["competitors"]:
        t = c["team"].get("abbreviation")
        rows.append(f"{c.get('homeAway')} {t} {c.get('score')}")
    print(eid, "|", name, "|", status, "|", "; ".join(rows))
