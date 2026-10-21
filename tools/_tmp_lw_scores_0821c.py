import json, urllib.request, re

ua = {"User-Agent": "Mozilla/5.0"}

def get_json(url):
    req = urllib.request.Request(url, headers=ua)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

def get_html(url):
    req = urllib.request.Request(url, headers=ua)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")

print("==== MyKBO game 13978 ====")
html = get_html("https://mykbostats.com/games/13978-Hanwha-vs-NC-20260925")
print("len", len(html))
# status / score cues
for pat in [
    r'Cancelled|Postponed|Suspended|Final|In Progress|Delayed|Rain|LIVE',
    r'class="[^"]*score[^"]*"[^>]*>[^<]{0,20}',
    r'data-score="[^"]+"',
    r'>\s*(\d{1,2})\s*<',
]:
    ms = re.findall(pat, html, re.I)
    if ms:
        print(pat, ms[:15])
# strip tags near Hanwha/NC
text = re.sub(r'<[^>]+>', ' ', html)
text = re.sub(r'\s+', ' ', text)
for key in ["Hanwha", "Dinos", "Cancelled", "Final", "Inning", "Top", "Bot", "Postponed", "Suspended"]:
    i = text.lower().find(key.lower())
    if i >= 0:
        print("CTX", key, text[max(0,i-60):i+80])

print("==== ESPN Hangzhou Marozsan detail ====")
d = get_json("https://site.web.api.espn.com/apis/site/v2/sports/tennis/atp/scoreboard?dates=20260925")
for e in d.get("events") or []:
    if "Hangzhou" not in (e.get("name") or ""):
        continue
    for g in e.get("groupings") or []:
        for c in g.get("competitions") or []:
            comps = c.get("competitors") or []
            names = [((x.get("athlete") or {}).get("displayName") or "?") for x in comps]
            if not any("Marozsan" in n or "Daniel" in n for n in names):
                continue
            st = (c.get("status") or {}).get("type") or {}
            print("status", st)
            for x in comps:
                print("  ", (x.get("athlete") or {}).get("displayName"), "score", x.get("score"), "lines", x.get("linescores"), "winner", x.get("winner"))
            print("notes", c.get("notes"))
            print("situation", c.get("situation"))

print("==== ESPN Wang detail ====")
d = get_json("https://site.web.api.espn.com/apis/site/v2/sports/tennis/wta/scoreboard?dates=20260925")
for e in d.get("events") or []:
    if "Singapore" not in (e.get("name") or ""):
        continue
    for g in e.get("groupings") or []:
        for c in g.get("competitions") or []:
            comps = c.get("competitors") or []
            names = [((x.get("athlete") or {}).get("displayName") or "?") for x in comps]
            if not any("Wang" in n and "Xinyu" in n for n in names) and not any("Prozorova" in n for n in names):
                continue
            # only the matchup of both
            blob = " ".join(names)
            if "Prozorova" in blob and "Wang" in blob:
                st = (c.get("status") or {}).get("type") or {}
                print("status", st)
                for x in comps:
                    print("  ", (x.get("athlete") or {}).get("displayName"), "score", x.get("score"), "lines", x.get("linescores"))
