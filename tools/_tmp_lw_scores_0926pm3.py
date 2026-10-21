import urllib.request, re
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
FSIGN = "SW9D1eZo"

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "X-Fsign": FSIGN, "Referer": "https://www.flashscore.com/"})
    with urllib.request.urlopen(req, timeout=25) as r:
        return r.read().decode("utf-8", "replace", errors="replace")

# event id from URL path mayot-harold-jPfM16Z1 / cassone O4aHjdoE - full event often combination
candidates = [
    "O4aHjdoE",
    "jPfM16Z1",
    "O4aHjdoEjPfM16Z1",
]
feeds = ["dc_1_", "df_sui_1_", "df_sur_1_", "df_sui_1_", "df_hh_1_", "df_st_1_"]
for eid in candidates:
    for f in feeds:
        url = f"https://global.flashscore.ninja/2/x/feed/{f}{eid}"
        try:
            body = get(url)
        except Exception as e:
            print(f"fail {f}{eid}", e)
            continue
        if not body or len(body) < 5:
            continue
        # split on common flashscore separators
        parts = re.split(r"[\xac\x01¬~]", body)
        interesting = [p for p in parts if p and (p.isdigit() or len(p)<40)]
        print(f"==== {f}{eid} len={len(body)}")
        print(body[:1500].replace("\x01","|").replace("¬","|"))
        print("parts sample", interesting[:40])

# also sportytrader search
for url in [
    "https://www.sportytrader.com/en/results-live/harold-mayot-murphy-cassone/",
    "https://www.sofascore.com/api/v1/search/Harold%20Mayot",
    "https://www.sofascore.com/api/v1/sport/tennis/scheduled-events/2026-09-26",
]:
    print("====", url)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json,text/html"})
        with urllib.request.urlopen(req, timeout=25) as r:
            body = r.read().decode("utf-8", "replace")
        print(body[:600])
    except Exception as e:
        print("fail", e)
