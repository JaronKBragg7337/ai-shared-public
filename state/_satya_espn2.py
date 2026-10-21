import urllib.request, json

def get(url):
    return json.loads(urllib.request.urlopen(url, timeout=20).read())

# CFB scoreboard with all events including final
data = get("https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard")
want = ("IOWA", "WASH", "WYO", "SJSU", "COLU", "MRST", "FSU", "LOU", "WSU", "USU", "ISU", "BYU")
for e in data.get("events", []):
    name = e.get("shortName") or ""
    abbs = []
    comp = e["competitions"][0]
    for c in comp["competitors"]:
        abbs.append(c["team"].get("abbreviation",""))
    if not any(a in want for a in abbs):
        # also check name
        up = name.upper()
        if not any(w in up for w in ("IOWA","WASH","WYO","SAN JOSE","COLUMBIA","MARIST","FLORIDA ST","LOUISVILLE","WASHINGTON ST","UTAH ST","BYU")):
            continue
    st = comp["status"]["type"]
    detail = st.get("detail") or st.get("description")
    state = st.get("state")
    bits = []
    for c in comp["competitors"]:
        ab = c["team"].get("abbreviation")
        sc = c.get("score")
        ha = c.get("homeAway")
        bits.append(f"{ab}({ha})={sc}")
    # try summary for WP
    eid = e.get("id")
    wp = None
    try:
        s = get(f"https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event={eid}")
        # winprobability last
        wparr = s.get("winprobability") or []
        if wparr:
            last = wparr[-1]
            wp = last
        # also header competitions probability
        hdr = s.get("header") or {}
        for c2 in (hdr.get("competitions") or [{}])[0].get("competitors") or []:
            if isinstance(c2.get("probability"), dict):
                print("prob", c2["team"].get("abbreviation"), c2["probability"])
    except Exception as ex:
        wp = f"summary_err:{ex}"
    print(name, "|", state, detail, "|", " ".join(bits), "| wp_last=", wp)
