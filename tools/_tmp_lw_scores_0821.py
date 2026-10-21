import json, urllib.request, re

ua = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

def get_json(url):
    req = urllib.request.Request(url, headers=ua)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

def get_html(url):
    req = urllib.request.Request(url, headers=ua)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")

def names_of(comp):
    out = []
    for x in comp.get("competitors") or []:
        ath = ((x.get("athlete") or {}).get("displayName")) or ((x.get("team") or {}).get("displayName")) or "?"
        ls = "-".join(str((y or {}).get("value")) for y in (x.get("linescores") or []))
        out.append((ath, x.get("score"), ls, x.get("winner"), x.get("homeAway")))
    return out

KEYS = ["Volynets", "Birrell", "Wang", "Prozorova", "Pawlikowska", "Adeshina"]
print("==== ESPN WTA/ATP/ALL ====")
for label, url in [
    ("wta", "https://site.web.api.espn.com/apis/site/v2/sports/tennis/wta/scoreboard?dates=20260925"),
    ("atp", "https://site.web.api.espn.com/apis/site/v2/sports/tennis/atp/scoreboard?dates=20260925"),
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
                ns = names_of(c)
                blob = " ".join(n[0] for n in ns)
                st = (c.get("status") or {}).get("type") or {}
                if any(k.lower() in blob.lower() for k in KEYS) and st.get("state") in ("in", "post"):
                    if "Volynets" in blob or "Birrell" in blob or "Wang" in blob or "Prozorova" in blob or "Pawlikowska" in blob or "Adeshina" in blob:
                        print(label, e.get("name"), "|", st.get("state"), st.get("detail") or st.get("description"), "|", ns)

print("==== GSA KBO ====")
try:
    html = get_html("https://globalsportsarchive.com/match/baseball/2026-09-25/nc-dinos-vs-hanwha-eagles/4114949/")
    # crude extract scoreboard numbers near team names
    for pat in [r"Hanwha Eagles.{0,200}?(\d+)", r"NC Dinos.{0,200}?(\d+)", r"(\d+)\s*:\s*(\d+)", r"Inning|LIVE|Final|Status"]:
        ms = re.findall(pat, html, re.I|re.S)
        if ms:
            print(pat, ms[:8])
    # look for score table cells
    cells = re.findall(r">(\d{1,2})<", html)
    print("numeric cells sample", cells[:40])
except Exception as e:
    print("GSA ERR", e)

print("==== Flashscore KBO ====")
try:
    html = get_html("https://www.flashscoreusa.com/game/baseball/hanwha-eagles-4tfKodg8/nc-dinos-O6x8hD4U/")
    print("len", len(html))
    for pat in [r"event_stage[^<]{0,40}", r"smsc[^>]*>[^<]+", r"\"score\"[^,]{0,40}", r"Dinos|Hanwha|LIVE|Finished|After"]:
        ms = re.findall(pat, html, re.I)
        if ms:
            print(pat, ms[:10])
except Exception as e:
    print("FS ERR", e)

print("==== MyKBO today ====")
for url in [
    "https://mykbostats.com/",
    "https://www.mykbostats.com/games",
]:
    try:
        html = get_html(url)
        print(url, "len", len(html))
        if re.search(r"Dinos|Hanwha|NC", html, re.I):
            for m in re.finditer(r".{0,40}(?:Dinos|Hanwha).{0,60}", html, re.I):
                print(m.group(0)[:100])
                break
    except Exception as e:
        print(url, "ERR", e)
