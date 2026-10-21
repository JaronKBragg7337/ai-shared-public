import urllib.request, re
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

def get(url):
    req = urllib.request.Request(url, headers=UA)
    return urllib.request.urlopen(req, timeout=25).read().decode("utf-8", "replace")

def dump_window(url, label):
    page = get(url)
    text = re.sub(r"<script[\s\S]*?</script>", " ", page, flags=re.I)
    text = re.sub(r"<style[\s\S]*?</style>", " ", text, flags=re.I)
    text = re.sub(r"<[^>]+>", "\n", text)
    lines = [L.strip() for L in text.splitlines() if L.strip()]
    print("====", label, "lines", len(lines))
    # find player name indices
    for i, L in enumerate(lines):
        if re.search(r"Gadamauri|Dalla Valle|Efremova|Kubka|Mmoh|Djere|Erhard", L, re.I):
            if i < 200:  # header area
                lo, hi = max(0, i-2), min(len(lines), i+20)
                print(f"-- around {i} --")
                for j in range(lo, hi):
                    print(f"{j}: {lines[j][:100]}")
                break
    # print lines 100-160 always (score block on tennis365)
    print("-- block 100-170 --")
    for j in range(100, min(170, len(lines))):
        print(f"{j}: {lines[j][:100]}")

dump_window(
    "https://livescore.tennis365.com/Italy-ATP-Challenger-Bari-Gadamauri,-Buvaysar-vs-Dalla-Valle,-Enrico-3381267",
    "Gadamauri",
)
dump_window(
    "https://livescore.tennis365.com/Turkey-WTA-Adana-Efremova,Ksenia-vs-Kubka,Martyna-3381309",
    "Efremova",
)

# Porto Mmoh page discovery via TE
print("==== PORTO / MMH ====")
p = get("https://www.tennisexplorer.com/porto-challenger/")
for r in re.findall(r"<tr[^>]*>([\s\S]*?)</tr>", p):
    t = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", r)).strip()
    if re.search(r"Mmoh|Djere|Erhard|Cam", t, re.I):
        print(t[:300])
# mouilleron full name scan
print("==== MOUILLERON ====")
p = get("https://www.tennisexplorer.com/mouilleron-le-captif-challenger/")
for r in re.findall(r"<tr[^>]*>([\s\S]*?)</tr>", p):
    t = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", r)).strip()
    if re.search(r"Erhard|Cam|Theate|Alb", t, re.I):
        print(t[:300])
# bari results section
print("==== BARI FULL MATCHING ROWS ====")
p = get("https://www.tennisexplorer.com/bari-challenger/")
for r in re.findall(r"<tr[^>]*>([\s\S]*?)</tr>", p):
    t = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", r)).strip()
    if re.search(r"Gadamauri|Dalla", t, re.I):
        print(t[:300])
