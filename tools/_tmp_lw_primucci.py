import urllib.request, re
ua = {"User-Agent": "Mozilla/5.0", "X-Fsign": "SW9D1eZo"}
url = "https://www.flashscore.com/tennis/itf-men-singles/m25-santa-margherita-di-pula-4/"
raw = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=25).read().decode("utf-8", "ignore")
print("len", len(raw), "primucci_count", raw.lower().count("primucci"), "lenders_count", raw.lower().count("lenders"))
for m in re.finditer(r".{0,120}Primucci.{0,200}", raw, re.I | re.S):
    s = re.sub(r"<[^>]+>", " ", m.group(0))
    s = re.sub(r"\s+", " ", s)
    print("CTX", s[:350])
# try feed detail if we can find event id near Primucci
idx = raw.lower().find("primucci")
print("AROUND", raw[max(0, idx - 200): idx + 400].replace("\n", " ")[:600])
# search live feed for names from encode
feed = urllib.request.urlopen(urllib.request.Request("https://global.flashscore.ninja/2/x/feed/f_2_0_2_en_1", headers=ua), timeout=25).read().decode("utf-8", "ignore")
# also scheduled feed
for fu in [
    "https://global.flashscore.ninja/2/x/feed/f_2_0_2_en_1",
    "https://global.flashscore.ninja/2/x/feed/f_2_1_2_en_1",
    "https://global.flashscore.ninja/2/x/feed/f_2_-1_2_en_1",
]:
    try:
        b = urllib.request.urlopen(urllib.request.Request(fu, headers=ua), timeout=20).read().decode("utf-8", "ignore")
        print(fu, "primucci", "Primucci" in b, "Lenders" in b, "Lokoli" in b)
    except Exception as e:
        print("FAIL", fu, e)
