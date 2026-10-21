# Heartbeat News (rendered show) - the full running order the video is made from: the day's stories PLUS the house
# commercials and the wires, laid out exactly the way the live page does it (news/show.js withAds + wireLines), so the video
# and the page's rundown / subtitles / banners match line for line (Jaron 9/27: "the old one had the commercial banners").
# Takes (the joke variants) are picked by the date, not dice, so a re-render of the same day gives the same show.
#   python episode_script.py 2026-09-27 OUTDIR   -> OUTDIR/script.json  {date, segments:[...]}
# Everything downstream (voices, plan, Unreal, the page in rendered mode) reads script.json instead of the episode JSON.
import sys, os, json, zlib, urllib.request, datetime
DATE, OUT = sys.argv[1], sys.argv[2]; os.makedirs(OUT, exist_ok=True)
SITE = "https://www.heartbeatobservatory.com"
get = lambda u: json.load(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "hb-news-render"}), timeout=30))
ep = get(f"{SITE}/news/episodes/{DATE}.json")
try: cat = get(f"{SITE}/news/ads/ads.json")
except Exception: cat = {"ads": []}
try: wire = [x for x in get(f"{SITE}/api/news").get("items", []) if x and x.get("title")][:6]
except Exception: wire = []
ADS_EVERY = 3
pick = lambda arr, key: arr[zlib.crc32((DATE + key).encode()) % len(arr)] if arr else None
clean = lambda t: " ".join(str(t).split()).rstrip(". ").strip()

def ad_seg(ad, prefix="ad-"):
    lines = pick(ad.get("takes") or [], ad["id"]) or ad.get("lines") or []
    g = {"kicker": ad.get("kicker") or "COMMERCIAL", "title": ad.get("title"), "image": ad.get("image") or "", "images": ad.get("images"), "url": ad.get("url") or ""}
    return {"id": prefix + ad["id"], "kind": "ad", "strap": ad.get("strap") or (ad.get("title") or "").upper(), "headline": ad.get("title"),
            "category": "COMMERCIAL", "status": "", "graphic": g, "sources": [{"name": ad["title"] + " (tap to visit)", "url": ad["url"]}] if ad.get("url") else [], "lines": lines}

def wire_lines(w):
    w = w[:4]
    if not w: return []
    out = [{"who": "joe", "text": "Now a quick look at more headlines from the wires."}]
    for i, x in enumerate(w): out.append({"who": "joe" if i % 2 else "vex", "text": clean(x["title"]) + ". That's from " + (x.get("source") or "the wires") + "."})
    return out

segs, stories = [], 0
k = int(datetime.datetime.fromisoformat(DATE).timestamp() // 86400)
ads = cat.get("ads") or []
for s in ep.get("segments", []):
    s = dict(s)
    if s.get("kind") == "wire":
        s["lines"] = wire_lines(wire)
        s["sources"] = [{"name": x.get("source") or "wire", "url": x.get("url") or ""} for x in wire[:4]]
        s["graphic"] = {**(s.get("graphic") or {}), "bullets": [clean(x["title"]) for x in wire[:4]]}
    if s.get("lines"): segs.append(s)
    if s.get("kind") in ("open", "close", "wire", "ad") or not ads: continue
    stories += 1
    if stories % ADS_EVERY == 0: segs.append(ad_seg(ads[k % len(ads)])); k += 1
br = cat.get("break") or {}
if br.get("spots"):
    card = lambda id_, lines, title: {"id": id_, "kind": "ad", "strap": "HEARTBEAT NEWS · COMMERCIAL BREAK", "headline": title, "category": "COMMERCIAL",
                                      "status": "", "graphic": {"kicker": "COMMERCIAL BREAK", "title": title}, "sources": [], "lines": lines}
    segs.append(card("break-in", pick(br.get("intro") or [[{"who": "joe", "text": "We'll be right back."}]], "intro"), "More from Heartbeat"))
    segs += [ad_seg(sp, "break-") for sp in br["spots"]]
    segs.append(card("break-out", pick(br.get("outro") or [[{"who": "joe", "text": "From the top."}]], "outro"), "Back to the news"))
json.dump({"date": DATE, "segments": segs}, open(os.path.join(OUT, "script.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("script: %d segments, %d lines (%d commercials)" % (len(segs), sum(len(s["lines"]) for s in segs), sum(s["kind"] == "ad" for s in segs)))
