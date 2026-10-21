import json, urllib.request, re
ua = {"User-Agent": "Mozilla/5.0"}

def get_json(url):
    req = urllib.request.Request(url, headers=ua)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

def names(comp):
    out = []
    for x in comp.get("competitors") or []:
        ath = ((x.get("athlete") or {}).get("displayName")) or "?"
        ls = "-".join(str((y or {}).get("value")) for y in (x.get("linescores") or []))
        out.append((ath, ls, x.get("winner")))
    return out

KEYS = ["Marozsan", "Daniel", "Wang", "Prozorova", "Volynets", "Birrell"]
print("==== LIVE TENNIS ====")
for label, url in [
    ("atp", "https://site.web.api.espn.com/apis/site/v2/sports/tennis/atp/scoreboard?dates=20260925"),
    ("wta", "https://site.web.api.espn.com/apis/site/v2/sports/tennis/wta/scoreboard?dates=20260925"),
    ("all", "https://site.web.api.espn.com/apis/site/v2/sports/tennis/all/scoreboard"),
]:
    try:
        d = get_json(url)
    except Exception as e:
        print(label, "ERR", e)
        continue
    for e in d.get("events") or []:
        for g in e.get("groupings") or []:
            for c in g.get("competitions") or []:
                ns = names(c)
                blob = " ".join(n[0] for n in ns)
                st = (c.get("status") or {}).get("type") or {}
                if any(k in blob for k in KEYS) and st.get("state") in ("in", "post"):
                    print(label, e.get("name"), "|", st.get("state"), st.get("detail") or st.get("description"), "|", ns)

print("==== VLR NS/NRG ====")
try:
    req = urllib.request.Request(
        "https://www.vlr.gg/753460/nongshim-redforce-vs-nrg-valorant-champions-2026-opening-d",
        headers=ua,
    )
    html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")
    ms = re.findall(r'class="score"[^>]*>\s*(\d+)\s*<', html)
    print("class score", ms[:30])
    # map titles near scores
    for m in re.finditer(r'(Lotus|Split|Sunset).{0,200}?(\d).{0,40}?(\d)', html, re.I|re.S):
        print("map", m.group(1), m.group(2), m.group(3))
        break
    # spoiler score spans common on vlr
    ms2 = re.findall(r'mod-spawner[^>]*>\s*(\d+)\s*<', html)
    print("mod-spawner", ms2[:20])
    if "LIVE" in html.upper():
        print("has LIVE marker")
except Exception as e:
    print("VLR ERR", e)
