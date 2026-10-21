import re, urllib.request
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"

def fetch(url, extra=None):
    h = {"User-Agent": UA, "Accept": "text/html,application/json,*/*", "Accept-Language": "en-US,en;q=0.9"}
    if extra: h.update(extra)
    req = urllib.request.Request(url, headers=h)
    with urllib.request.urlopen(req, timeout=25) as r:
        return r.read().decode("utf-8", "replace")

urls = [
    "https://www.scoremania.com/tennis-live-centre/match-detail/harold-mayot-vs-murphy-cassone/37127/info",
    "https://www.scoremania.com/tennis-live-centre/match-detail/maria-timofeeva-vs-mia-pohankova/37130/info",
    "https://www.scoremania.com/tennis-live-centre/match-detail/coleman-wong-vs-adolfo-vallejo/37092/info",
]
for url in urls:
    print("====", url)
    try:
        html = fetch(url)
        text = re.sub(r"<script[\s\S]*?</script>", " ", html, flags=re.I)
        text = re.sub(r"<style[\s\S]*?</style>", " ", text, flags=re.I)
        text = re.sub(r"<[^>]+>", " | ", text)
        text = re.sub(r"\s+", " ", text)
        for name in ("Mayot", "Cassone", "Timofeeva", "Pohankova", "Wong", "Vallejo", "set", "Set"):
            i = text.lower().find(name.lower()) if name.lower() in ("set",) else text.find(name)
            if i >= 0:
                print(text[max(0,i-100):i+250])
                print("---")
        # look for numeric sequences near names
        for m in re.finditer(r".{0,40}(Mayot|Cassone|Timofeeva|Pohankova|Wong|Vallejo).{0,80}", text):
            print("CTX", m.group(0))
        print("LEN", len(html))
        # dump interesting attrs
        for pat in [r"data-score=\"[^\"]+\"", r"score-\w+=\"[^\"]+\"", r"\\b\\d+\\s*:\\s*\\d+\\b", r"games?\\s*[:=]\\s*\\d+"]:
            ms = re.findall(pat, html, flags=re.I)
            if ms:
                print(pat, ms[:20])
    except Exception as e:
        print("fail", e)

print("==== FS FEEDS")
for path in [
    "https://global.flashscore.ninja/2/x/feed/df_sui_1_O4aHjdoE",
    "https://global.flashscore.ninja/2/x/feed/dc_1_O4aHjdoE",
    "https://2.flashscore.ninja/api/v1/event/O4aHjdoE",
]:
    print("--", path)
    try:
        body = fetch(path, {"X-Fsign": "SW9D1eZo"})
        print(body[:1000])
    except Exception as e:
        print("fail", e)
