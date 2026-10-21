import urllib.request, re
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")

def dump(url, label):
    print("====", label, url)
    page = get(url)
    text = re.sub(r"<script[\s\S]*?</script>", " ", page, flags=re.I)
    text = re.sub(r"<style[\s\S]*?</style>", " ", text, flags=re.I)
    text = re.sub(r"<[^>]+>", "\n", text)
    lines = [re.sub(r"\s+", " ", L).strip() for L in text.splitlines()]
    lines = [L for L in lines if L and L not in ("&nbsp;", ">", "|")]
    print("lines", len(lines))
    shown = 0
    for L in lines:
        if len(L) < 2:
            continue
        if re.search(r"cookie|privacy|subscribe|javascript|function ", L, re.I):
            continue
        print(L[:180])
        shown += 1
        if shown >= 90:
            break
    for i, L in enumerate(lines):
        if re.search(r"Silva|Olivieri|Pareja|Frodin|Cazacu|Vrba|Fenty|Marcondes", L, re.I):
            print("-- around", i, "--")
            for j in range(max(0, i-2), min(len(lines), i+20)):
                print(f"{j}: {lines[j][:160]}")

dump("https://livescore.tennis365.com/Brazil-Challenger-Curitiba-Andrade-Da-Silva,-Lucas-vs-Olivieri,Genaro-Alberto-3381257", "DaSilva")
dump("https://livescore.tennis365.com/Tennis/USA/W100-Templeton/79085", "Templeton")
