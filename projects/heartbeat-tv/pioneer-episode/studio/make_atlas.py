# wall_atlas.png (2x2, 4096 x 2048) for the studio LED wall. Cells: 0 = s02, 1 = s01, 2 = s10, 3 = s15.
# Each cell uses ../walls/<id>.png when it exists (the orchestrator's cards). If one is missing, a stand-in card is drawn here in the
# show's wall style from script.json (clearly a stand-in: re-run when the real card arrives). s02 shows the s01 card (same evening, same wall)
# unless walls/s02.png exists. Power-of-two atlas like the daily show: a 4200 x 1800 atlas hung Unreal in "Processing Asset Data".
import os, json
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); EP = HERE + "/.."; W, H = 2100, 900
S = {s["id"]: s for s in json.load(open(EP + "/script.json", encoding="utf-8"))}
F = lambda n, sz: ImageFont.truetype(n, sz)
def card(tag, t1, t2, bullets, source=None):
    im = Image.new("RGB", (W, H)); d = ImageDraw.Draw(im)
    for y in range(H): d.line([(0, y), (W, y)], fill=(int(10 - 7 * y / H), int(36 - 28 * y / H), int(96 - 70 * y / H)))
    tw = d.textlength(tag, font=F("segoeuib.ttf", 46)); d.rounded_rectangle((75, 62, 75 + tw + 60, 132), 10, fill=(26, 86, 219)); d.text((105, 66), tag, font=F("segoeuib.ttf", 46), fill="white")
    d.text((75, 165), t1, font=F("segoeuib.ttf", 118), fill="white"); d.text((75, 300), t2, font=F("segoeuib.ttf", 118), fill=(64, 156, 255))
    y = 478
    for b in bullets:
        d.ellipse((82, y + 22, 106, y + 46), fill=(240, 40, 60)); d.text((132, y), b, font=F("segoeui.ttf", 50), fill=(232, 236, 245)); y += 78
    if source: d.text((132, y + 6), "Source: " + source, font=F("segoeui.ttf", 32), fill=(150, 165, 195))
    d.rectangle((0, H - 70, W, H), fill=(226, 30, 48)); d.text((30, H - 64), "HEARTBEAT NEWS  ·  SCIENCE", font=F("segoeuib.ttf", 44), fill="white")
    d.rounded_rectangle((W - 420, H - 330, W - 110, H - 100), 34, fill=(12, 30, 80), outline="white", width=8); d.text((W - 345, H - 310), "HBN", font=F("segoeuib.ttf", 96), fill="white")
    pts = [(W - 395, H - 165), (W - 330, H - 165), (W - 305, H - 200), (W - 270, H - 120), (W - 240, H - 195), (W - 220, H - 165), (W - 135, H - 165)]; d.line(pts, fill=(226, 30, 48), width=14, joint="curve")
    return im
def standin(sid):
    b = S[sid].get("board") or {}
    if sid == "s01": return card("PARAPHRASE", "Grok suggests:", "the Pioneer Anomaly", ["Heartbeat asked on X: what episode should we make?", "Grok, in our words: a spacecraft pulled by something unexplained", "Filed under: STILL UNKNOWN"])
    if sid == "s10": return card("LIVE", "LIVE FROM", "DEEP SPACE", b.get("lines", []), b.get("source"))
    return card("CORRECTION", "Correction:", "filed under Science", b.get("lines", []), b.get("source"))
def cell(sid):
    p = EP + "/walls/%s.png" % sid
    if os.path.exists(p): return Image.open(p).convert("RGB"), "walls/%s.png" % sid
    return standin(sid), "stand-in drawn by make_atlas.py"
at = Image.new("RGB", (4096, 2048)); used = {}
for i, sid in enumerate(["s02", "s01", "s10", "s15"]):
    im, src = cell(sid if (sid != "s02" or os.path.exists(EP + "/walls/s02.png")) else "s01"); used[sid] = src
    at.paste(im.resize((2048, 1024), Image.LANCZOS), ((i % 2) * 2048, (i // 2) * 1024))
at.save(HERE + "/wall_atlas.png"); json.dump(used, open(HERE + "/wall_sources.json", "w")); print("atlas ok:", used)
