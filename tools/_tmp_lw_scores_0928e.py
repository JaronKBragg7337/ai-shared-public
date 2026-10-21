import urllib.request, re
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

def get(url):
    req = urllib.request.Request(url, headers=UA)
    return urllib.request.urlopen(req, timeout=25).read().decode("utf-8", "replace")

def strip_tags(s):
    s = re.sub(r"<script[\s\S]*?</script>", " ", s, flags=re.I)
    s = re.sub(r"<style[\s\S]*?</style>", " ", s, flags=re.I)
    s = re.sub(r"<[^>]+>", "\n", s)
    return s

print("=== TENNIS365 MATCHES ===")
for u in [
    "https://livescore.tennis365.com/Italy-ATP-Challenger-Bari-Gadamauri,-Buvaysar-vs-Dalla-Valle,-Enrico-3381267",
    "https://livescore.tennis365.com/Turkey-WTA-Adana-Efremova,Ksenia-vs-Kubka,Martyna-3381309",
]:
    page = get(u)
    text = strip_tags(page)
    lines = [L.strip() for L in text.splitlines() if L.strip()]
    print("URL", u.split("/")[-1][:55])
    # print a window around status words
    for i, L in enumerate(lines):
        if re.search(r"^(Set \d|Inter\.|Final|Retired|NSY)$", L, re.I) or re.search(r"^\d+\s*-\s*\d+$", L):
            lo = max(0, i - 6)
            hi = min(len(lines), i + 8)
            print("-- window --")
            for j in range(lo, hi):
                print(f"  {j}: {lines[j][:80]}")
    # raw numeric attributes
    attrs = re.findall(r"data-[a-zA-Z0-9_-]+=\"[^\"]{0,40}\"", page)
    for a in attrs:
        if re.search(r"score|set|game|point|status|home|away", a, re.I):
            print("ATTR", a)
    print()

print("=== TE LIVE NAME SCAN ===")
page = get("https://www.tennisexplorer.com/live/")
rows = re.findall(r"<tr[^>]*>([\s\S]*?)</tr>", page)
print("rows", len(rows))
pat = re.compile(r"Efremova|Kubka|Gadamauri|Erhard|Mmoh|Matusevich|Heredia|Nesmian|Heerae|Fernandez|Rodriguez|Dalla|Cambronne|Valle|Bruno|Lorenzo|Mathys|Anton|Samuel|Alina|Michael|Buvaysar", re.I)
hits = 0
for r in rows:
    t = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", r)).strip()
    if pat.search(t):
        print(t[:260])
        hits += 1
print("hits", hits)

# also try tournament pages
print("=== TE TOURNAMENT PAGES ===")
for path in ["/adana/", "/bari-challenger/", "/mouilleron-le-captif-challenger/", "/porto-challenger/"]:
    try:
        p = get("https://www.tennisexplorer.com" + path)
        print("OK", path, "bytes", len(p))
        for r in re.findall(r"<tr[^>]*>([\s\S]*?)</tr>", p):
            t = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", r)).strip()
            if pat.search(t) and re.search(r"\d", t):
                print(" ", t[:240])
    except Exception as e:
        print("FAIL", path, e)
