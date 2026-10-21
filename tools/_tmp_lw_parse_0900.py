import re, urllib.request

ua = {"User-Agent": "Mozilla/5.0"}

url = "https://www.sportschau.de/live-und-ergebnisse/tennis/co14747/hangzhou-open/ma11761789/daniil-medvedev_andrey-rublev/spiel-spiele-und-ergebnisse"
html = urllib.request.urlopen(urllib.request.Request(url, headers=ua), timeout=20).read().decode("utf-8", "replace")
print("=== SPORTSCHAU Medvedev ===")
# pull numeric clusters near player names
idx = html.find("Daniil Medvedev")
if idx < 0:
    idx = html.find("D. Medvedev")
chunk = html[max(0, idx - 200): idx + 2500]
text = re.sub(r"<[^>]+>", " ", chunk)
text = re.sub(r"\s+", " ", text)
print(text[:800])

url2 = "https://www.tennisexplorer.com/matches/?type=all&year=2026&month=09&day=29"
html2 = urllib.request.urlopen(urllib.request.Request(url2, headers=ua), timeout=25).read().decode("utf-8", "replace")
print("\n=== TENNISEXPLORER rows ===")
keys = ["Medvedev", "Giustino", "Komano", "Pennaforti", "Bouzige"]
for k in keys:
    i = html2.find(k)
    if i < 0:
        print("miss", k)
        continue
    # find enclosing tr roughly
    start = html2.rfind("<tr", 0, i)
    end = html2.find("</tr>", i)
    row = html2[start:end+5] if start >= 0 and end > start else html2[i-300:i+400]
    text = re.sub(r"<[^>]+>", "|", row)
    text = re.sub(r"\|+", "|", text)
    text = re.sub(r"\s+", " ", text)
    print(k, text[:300])
