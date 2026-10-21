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
        out.append((ath, x.get("score"), ls))
    return out

print("==== ESPN ATP Marozsan/Daniel + in-progress ====")
for label,url in [
    ("atp","https://site.web.api.espn.com/apis/site/v2/sports/tennis/atp/scoreboard?dates=20260925"),
    ("all","https://site.web.api.espn.com/apis/site/v2/sports/tennis/all/scoreboard"),
]:
    d=get_json(url)
    for e in d.get("events") or []:
        for g in e.get("groupings") or []:
            for c in g.get("competitions") or []:
                ns=names_of(c)
                blob=" ".join(n[0] for n in ns)
                st=(c.get("status") or {}).get("type") or {}
                if st.get("state")=="in" or any(k in blob for k in ["Marozsan","Daniel","Wang","Prozorova"]):
                    print(label, e.get("name"), "|", st.get("state"), st.get("detail"), "|", ns)

print("==== Flashscore embed parse ====")
html=get_html("https://www.flashscoreusa.com/game/baseball/hanwha-eagles-4tfKodg8/nc-dinos-O6x8hD4U/")
# common FS patterns
for pat in [
    r'event_stage_type_id[\\"\']?:\s*(\d+)',
    r'event_stage[\\"\']?:\s*[\\"\']([^\\"\']+)',
    r'eventStageTypeId":(\d+)',
    r'event_stage_time":"([^"]+)"',
    r'"home_score[^}]{0,80}',
    r'"away_score[^}]{0,80}',
    r'scoreboard[^}]{0,200}',
]:
    ms=re.findall(pat, html, re.I)
    if ms:
        print(pat, ms[:5])
# dump a window around event_stage
m=re.search(r'.{200}event_stage_time.{200}', html)
if m: print('CTX', m.group(0)[:400])
# look for df_s_1 or similar feed chunks
for m in re.finditer(r'df_[a-z0-9_]+\s*=\s*\[[^\]]{0,300}\]', html):
    s=m.group(0)
    if 'score' in s.lower() or 'Dinos' in s or any(c.isdigit() for c in s):
        print('DF', s[:250])
        break

print("==== MyKBO games list search ====")
html=get_html("https://mykbostats.com/")
for m in re.finditer(r'href="(/games/[^"]+)"[^>]*>', html):
    href=m.group(1)
    if '2026-09-25' in href or 'Dinos' in href or 'Hanwha' in href:
        print(href)
# broader
for m in re.finditer(r'.{0,30}Dinos.{0,80}', html):
    print(m.group(0)[:110])
