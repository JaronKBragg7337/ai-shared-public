# Heartbeat Observatory promo clips (Jaron 10/19: "We need to show other stuff. Not just shows and channels. Maybe the same
# commercials we use for the news ... as quick videos to show what else is here").
#   python ad_clips.py EPISODE.mp4 EP_DIR OUT_DIR [--queue]
# Cuts every house commercial out of the finished daily show (Vex + Joe at the desk, the page on the LED wall), makes each one
# 9:16 with captions, and wraps it: H logo -> the commercial -> "free at heartbeatobservatory.com/<page>" card -> cream end card.
# --queue adds new ones to state/social-queue.json "promos" (one posts a day at 12:15 PM, task "HB Socials Promo"). An ad that
# already has a clip in the queue is skipped, so each commercial goes out once until its words change.
import sys, os, json, ast, subprocess, shutil, re
from PIL import Image, ImageDraw, ImageFont

mp4, epdir, out = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(out, exist_ok=True)
plan = json.load(open(os.path.join(epdir, "plan.json")))
script = json.load(open(os.path.join(epdir, "script.json"), encoding="utf-8"))
fps = plan["fps"]; W, H = 1080, 1920
HERE = os.path.dirname(os.path.abspath(__file__))
BRAND = "C:/Users/lilli/AI-Shared/state/brand-options-2026-10-10"
FONT = os.path.join(HERE, "fonts", "BarlowCondensed-ExtraBold.ttf"); FONT2 = os.path.join(HERE, "fonts", "BarlowCondensed-SemiBold.ttf")
CREAM, INK, RUST = (250, 243, 232), (40, 28, 18), (160, 82, 30)
QUEUE = "C:/Users/lilli/AI-Shared/state/social-queue.json"
ADS = json.load(open("C:/Users/lilli/Projects/heartbeat-observatory/news/ads/ads.json", encoding="utf-8"))
CATALOG = {a["id"]: a for a in ADS["ads"] + ADS["break"]["spots"]}
SKIP = {"ad-trades", "ad-city"}   # retired 10/19 (old Trade Desk page; World 2 being remade)


def seg_lines(g):
    v = g.get("lines")
    if isinstance(v, str):
        try: v = ast.literal_eval(v)
        except Exception: v = []
    return v or []


texts = {(si, li): l.get("text", "") for si, g in enumerate(script["segments"]) for li, l in enumerate(seg_lines(g))}


def t(s):
    h, s = divmod(max(s, 0), 3600); m, s = divmod(s, 60)
    return "%d:%02d:%05.2f" % (h, m, s)


def ass(lines, offset, dur, top):
    head = ("[Script Info]\nScriptType: v4.00+\nPlayResX: %d\nPlayResY: %d\nWrapStyle: 0\n\n[V4+ Styles]\n"
            "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, "
            "ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
            "Style: Cap,Arial,64,&H00FFFFFF,&H00FFFFFF,&H00000000,&H99000000,1,0,0,0,100,100,0,0,1,5,2,8,70,70,1530,1\n"
            "Style: Who,Arial,40,&H0080D8FF,&H00FFFFFF,&H00000000,&H99000000,1,0,0,0,100,100,2,0,1,4,1,8,70,70,1460,1\n"
            "Style: Top,Arial,58,&H00FFFFFF,&H00FFFFFF,&H00000000,&H99000000,1,0,0,0,100,100,3,0,1,4,1,8,60,60,140,1\n\n"
            "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n") % (W, H)
    ev = ["Dialogue: 0,%s,%s,Top,,0,0,0,,HEARTBEAT OBSERVATORY\\N{\\fs40\\b0}%s" % (t(0), t(dur), top)]
    for l in lines:
        st = l["start"] / fps - offset; du = l["frames"] / fps
        if st + du <= 0.05 or st >= dur: continue
        txt = texts.get((l["seg"], l["line"]), "")
        if not txt: continue
        w = txt.split(); parts = [" ".join(w[i:i + 6]) for i in range(0, len(w), 6)]
        tot = sum(len(p) for p in parts) or 1; a = st
        ev.append("Dialogue: 0,%s,%s,Who,,0,0,0,,%s" % (t(st), t(st + du), {"vex": "VEX", "joe": "JOE"}.get(l["who"], l["who"].upper())))
        for p in parts:
            b = a + du * len(p) / tot; ev.append("Dialogue: 0,%s,%s,Cap,,0,0,0,,%s" % (t(a), t(b), p.replace("{", "(").replace("}", ")"))); a = b
    return head + "\n".join(ev) + "\n"


def run(args): subprocess.run(args, check=True)


def vf(assfile, img=None):
    """Page screenshot big on top (the thing being advertised), the anchors at the desk under it, captions below."""
    p = assfile.replace("\\", "/").replace(":", "\:")
    bg = "[0:v]split[a][b];[a]scale=%d:%d:force_original_aspect_ratio=increase,crop=%d:%d,gblur=sigma=30,eq=brightness=-0.25[bg];[b]scale=%d:-2[fg];" % (W, H, W, H, W)
    if img:
        return bg + "[1:v]scale=1000:-2,format=rgba[im];[bg][im]overlay=(W-w)/2:300:shortest=1[t1];[t1][fg]overlay=0:810,subtitles='%s',format=yuv420p" % p
    return bg + "[bg][fg]overlay=(W-w)/2:(H-h)/2-120,subtitles='%s',format=yuv420p" % p


def still(png, secs, outp, fade_in=0.3):
    run(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-t", "%.2f" % secs, "-i", png, "-f", "lavfi", "-t", "%.2f" % secs,
         "-i", "anullsrc=r=48000:cl=stereo", "-vf", "scale=%d:%d,fps=24,fade=t=in:d=%.2f,fade=t=out:st=%.2f:d=0.3,format=yuv420p" % (W, H, fade_in, secs - 0.3),
         "-c:v", "libx264", "-crf", "20", "-c:a", "aac", "-ar", "48000", "-ac", "2", "-shortest", outp])


def card(path, lines):
    im = Image.new("RGB", (W, H), CREAM); d = ImageDraw.Draw(im)
    lg = Image.open(BRAND + "/x-profile-h-heartbeat-800.png").convert("RGB").resize((260, 260)); y = int(H * 0.2); im.paste(lg, ((W - 260) // 2, y)); y += 260 + 90
    for txt, size, col, f in lines:
        fn = ImageFont.truetype(f, size)
        while d.textlength(txt, font=fn) > W - 100 and size > 30: size -= 4; fn = ImageFont.truetype(f, size)
        d.text(((W - d.textlength(txt, font=fn)) / 2, y), txt, font=fn, fill=col); y += int(size * 1.35)
    im.save(path)


def concat(parts, outp):
    lst = os.path.abspath(outp + ".txt"); open(lst, "w").write("".join("file '%s'\n" % os.path.abspath(x).replace("\\", "/") for x in parts))
    run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c:v", "libx264", "-crf", "21", "-preset", "medium",
         "-c:a", "aac", "-ar", "48000", "-ac", "2", "-b:a", "128k", "-movflags", "+faststart", outp]); os.remove(lst)


tmp = os.path.join(out, "_parts"); os.makedirs(tmp, exist_ok=True)
card(os.path.join(tmp, "logo.png"), [])
im = Image.new("RGB", (W, H), (0, 0, 0)); lg = Image.open(BRAND + "/x-profile-h-heartbeat-800.png").convert("RGB").resize((648, 648)); im.paste(lg, ((W - 648) // 2, (H - 648) // 2)); im.save(os.path.join(tmp, "logo.png"))
still(os.path.join(tmp, "logo.png"), 1.4, os.path.join(tmp, "logo.mp4"), 0.4)
endv = os.path.join(tmp, "end.mp4")
run(["ffmpeg", "-y", "-loglevel", "error", "-i", BRAND + "/vertical/endcard-vertical-cream.mp4", "-vf", "scale=%d:%d,fps=24,format=yuv420p" % (W, H),
     "-af", "aresample=48000", "-c:v", "libx264", "-crf", "20", "-c:a", "aac", "-ar", "48000", "-ac", "2", endv])

segs = plan["segments"]; made = []
for i, s in enumerate(segs):
    sid = s["id"]; key = sid.replace("break-", "")
    if not (sid.startswith("ad-") or sid.startswith("break-ad-") or sid == "break-reel-games"): continue
    key = key if key in CATALOG else key.replace("ad-", "", 1)
    if key in SKIP or ("ad-" + key) in SKIP or key not in CATALOG: continue
    ad = CATALOG[key]
    st = s["start"] / fps; en = (segs[i + 1]["start"] if i + 1 < len(segs) else plan["frames"]) / fps
    lines = [l for l in plan["lines"] if l["seg"] == i]
    if lines: st = min(st, lines[0]["start"] / fps); en = max(l["start"] + l["frames"] for l in lines) / fps + 0.8
    dur = en - st
    a = os.path.join(tmp, key + ".ass"); open(a, "w", encoding="utf-8").write(ass(plan["lines"], st, dur, ad.get("title", "")))
    body = os.path.join(tmp, key + "_body.mp4")
    img = ad.get("image") or (ad.get("images") or [None])[0]
    img = os.path.join("C:/Users/lilli/Projects/heartbeat-observatory", img.lstrip("/")) if img else None
    img = img if img and os.path.exists(img) else None
    run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "%.2f" % st, "-t", "%.2f" % dur, "-i", mp4] + (["-loop", "1", "-i", img] if img else []) + ["-filter_complex",
         vf(a, img) + ",fps=24,fade=t=in:d=0.3,fade=t=out:st=%.2f:d=0.4" % (dur - 0.4), "-af", "afade=t=in:d=0.2,afade=t=out:st=%.2f:d=0.5,aresample=48000" % (dur - 0.5),
         "-c:v", "libx264", "-crf", "20", "-c:a", "aac", "-ar", "48000", "-ac", "2", body])
    page = re.sub(r"^https?://(www\.)?", "", ad.get("url", "heartbeatobservatory.com")).rstrip("/")
    page = page if "heartbeatobservatory.com" in page else "heartbeatobservatory.com"
    card(os.path.join(tmp, key + "_card.png"), [(ad.get("title", ""), 104, INK, FONT), ("", 24, INK, FONT2), ("Free, right now:", 70, INK, FONT2),
         (page, 72, RUST, FONT), ("", 24, INK, FONT2), ("One site, many worlds", 62, INK, FONT2)])
    still(os.path.join(tmp, key + "_card.png"), 3.2, os.path.join(tmp, key + "_card.mp4"))
    outp = os.path.join(out, key + ".mp4")
    concat([os.path.join(tmp, "logo.mp4"), body, os.path.join(tmp, key + "_card.mp4"), endv], outp)
    made.append((key, ad, outp, page)); print("made", key, "%.0fs" % (dur + 1.4 + 3.2 + 4))
shutil.rmtree(tmp, ignore_errors=True)

if "--queue" in sys.argv and made:
    q = json.load(open(QUEUE, encoding="utf-8")); promos = q.setdefault("promos", [])
    have = {p["ad"] for p in promos}
    keep = os.path.join("C:/Users/lilli/AI-Shared/state/promo-clips"); os.makedirs(keep, exist_ok=True)
    for key, ad, f, page in made:
        if key in have: continue
        dst = os.path.join(keep, key + ".mp4"); shutil.copy(f, dst)
        first = next((x["text"] for take in ad.get("takes", [])[:1] for x in take), ad.get("title", ""))
        promos.append({"id": "promo-" + key, "ad": key, "title": ad.get("title", ""), "file": dst.replace("\\", "/"),
                       "link": "https://" + page,
                       "caption": f"{first}\n\n{ad.get('title', '')}, free at {page}\nMade with AI by Heartbeat Observatory · AI Robot Vex and Alien Joe are characters\n#AI #heartbeatobservatory"})
        print("queued", key)
    json.dump(q, open(QUEUE, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
