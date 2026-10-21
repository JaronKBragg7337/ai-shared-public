# Heartbeat News - the 9:16 cuts for phones and social (Jaron 10/17: screen-recording cut things off; TikTok/Shorts/X need their own).
#   python make_vertical.py EPISODE.mp4 EP_DIR OUT_DIR
# Makes, from the finished 16:9 episode (no re-render):
#   vertical.mp4   the whole show, 1080x1920, picture letterboxed over a blurred copy (nothing cropped), captions under the picture
#   short.mp4      the open + the top stories (whole stories, up to ~2:55), same look + an end card line - the daily social post
# Captions come from the same script the video was voiced from (script.json + plan.json timing), so they match the words.
import sys, os, json, ast, subprocess

mp4, epdir, out = sys.argv[1], sys.argv[2], sys.argv[3]   # add --short-only to remake just the short
os.makedirs(out, exist_ok=True)
plan = json.load(open(os.path.join(epdir, "plan.json")))
script = json.load(open(os.path.join(epdir, "script.json"), encoding="utf-8"))
fps = plan["fps"]
W, H = 1080, 1920


def seg_lines(g):
    v = g.get("lines")
    if isinstance(v, str):
        try: v = ast.literal_eval(v)
        except Exception: v = []
    return v or []


texts = {}
for si, g in enumerate(script["segments"]):
    for li, l in enumerate(seg_lines(g)):
        texts[(si, li)] = l.get("text", "")


def t(s):
    h, s = divmod(max(s, 0), 3600); m, s = divmod(s, 60)
    return "%d:%02d:%05.2f" % (h, m, s)


def chunks(text, n=6):
    w = text.split()
    return [" ".join(w[i:i + n]) for i in range(0, len(w), n)] or [""]


def ass(lines, offset=0.0, end=None, endcard=None, cut=None):
    head = ("[Script Info]\nScriptType: v4.00+\nPlayResX: %d\nPlayResY: %d\nWrapStyle: 0\n\n[V4+ Styles]\n"
            "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, "
            "ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
            "Style: Cap,Arial,64,&H00FFFFFF,&H00FFFFFF,&H00000000,&H99000000,1,0,0,0,100,100,0,0,1,5,2,8,70,70,1330,1\n"
            "Style: Who,Arial,40,&H0080D8FF,&H00FFFFFF,&H00000000,&H99000000,1,0,0,0,100,100,2,0,1,4,1,8,70,70,1255,1\n"
            "Style: Top,Arial,58,&H00FFFFFF,&H00FFFFFF,&H00000000,&H99000000,1,0,0,0,100,100,3,0,1,4,1,8,60,60,300,1\n"
            "Style: Card,Arial,52,&H00FFFFFF,&H00FFFFFF,&H00000000,&H99000000,1,0,0,0,100,100,0,0,1,4,1,2,60,60,230,1\n\n"
            "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n") % (W, H)
    ev = []
    total = end if end is not None else plan["frames"] / fps
    ev.append("Dialogue: 0,%s,%s,Top,,0,0,0,,HEARTBEAT NEWS\\N{\\fs40\\b0}%s" % (t(0), t(total), script.get("date", plan["date"])))
    for l in lines:
        st = l["start"] / fps - offset; du = l["frames"] / fps
        if st + du <= 0.05: continue   # before the cut point (the short starts mid-show)
        if end is not None and st >= end: continue
        if cut is not None and st >= cut - 0.6: continue
        txt = texts.get((l["seg"], l["line"]), "")
        if not txt: continue
        who = {"vex": "VEX", "joe": "JOE"}.get(l["who"], l["who"].upper())
        parts = chunks(txt)
        tot = sum(len(p) for p in parts) or 1; a = st
        ev.append("Dialogue: 0,%s,%s,Who,,0,0,0,,%s" % (t(st), t(st + du), who))
        for p in parts:
            b = a + du * len(p) / tot
            ev.append("Dialogue: 0,%s,%s,Cap,,0,0,0,,%s" % (t(a), t(b), p.replace("{", "(").replace("}", ")")))
            a = b
    if endcard:
        ev.append("Dialogue: 1,%s,%s,Card,,0,0,0,,%s" % (t(endcard[0]), t(endcard[1]), endcard[2]))
    return head + "\n".join(ev) + "\n"


def run(args):
    print(" ".join(args[:6]), "...", flush=True)
    subprocess.run(args, check=True)


def vf(assfile):
    p = assfile.replace("\\", "/").replace(":", "\\:")
    return ("split[a][b];[a]scale=%d:%d:force_original_aspect_ratio=increase,crop=%d:%d,gblur=sigma=30,eq=brightness=-0.18[bg];"
            "[b]scale=%d:-2[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2-120,subtitles='%s',format=yuv420p" % (W, H, W, H, W, p))


# 1) the short (Jaron 10/17): the open alone was a trailer with no news. Now it opens on the H logo like his own videos, goes
# STRAIGHT into the top stories (whole stories, in order, no tease), then a "that was the short version" card, then the cream
# brand card the TV shows end on. Whole thing <= 3:00 (YouTube Shorts max). Stops at the first commercial. At least 1 story.
from PIL import Image, ImageDraw, ImageFont
BRAND = "C:/Users/lilli/AI-Shared/state/brand-options-2026-10-10"
FONT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts", "BarlowCondensed-ExtraBold.ttf")
FONT2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts", "BarlowCondensed-SemiBold.ttf")
CREAM, INK, RUST = (250, 243, 232), (40, 28, 18), (160, 82, 30)


def logo_card(w, h, path):
    im = Image.new("RGB", (w, h), (0, 0, 0)); lg = Image.open(BRAND + "/x-profile-h-heartbeat-800.png").convert("RGB")   # his white H on black
    sz = int(min(w, h) * 0.6); lg = lg.resize((sz, sz)); im.paste(lg, ((w - sz) // 2, (h - sz) // 2)); im.save(path)


def full_show_card(w, h, path, lines):
    im = Image.new("RGB", (w, h), CREAM); d = ImageDraw.Draw(im)
    lg = Image.open(BRAND + "/x-profile-h-heartbeat-800.png").convert("RGB"); sz = int(min(w, h) * 0.24); lg = lg.resize((sz, sz))
    y = int(h * 0.2); im.paste(lg, ((w - sz) // 2, y)); y += sz + int(h * 0.05)
    for txt, size, col, f in lines:
        fn = ImageFont.truetype(f, int(size * min(w, h) / 1080)); bw = d.textlength(txt, font=fn)
        d.text(((w - bw) / 2, y), txt, font=fn, fill=col); y += int(size * min(w, h) / 1080 * 1.35)
    im.save(path)


def still(png, secs, w, h, outp, fade_in=0.3):
    run(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-t", "%.2f" % secs, "-i", png, "-f", "lavfi", "-t", "%.2f" % secs,
         "-i", "anullsrc=r=48000:cl=stereo", "-vf", "scale=%d:%d,fps=24,fade=t=in:d=%.2f,fade=t=out:st=%.2f:d=0.3,format=yuv420p" % (w, h, fade_in, secs - 0.3),
         "-c:v", "libx264", "-crf", "20", "-c:a", "aac", "-ar", "48000", "-ac", "2", "-shortest", outp])


def concat(parts, outp):
    lst = outp + ".txt"; open(lst, "w").write("".join("file '%s'\n" % os.path.abspath(x).replace("\\", "/") for x in parts))
    lst = os.path.abspath(lst)
    run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c:v", "libx264", "-crf", "21", "-preset", "medium",
         "-c:a", "aac", "-ar", "48000", "-ac", "2", "-b:a", "128k", "-movflags", "+faststart", outp])


kinds = {i: g.get("kind") for i, g in enumerate(script["segments"])}
seg_start, seg_end = {}, {}
for l in plan["lines"]:
    seg_start[l["seg"]] = min(seg_start.get(l["seg"], 1e9), l["start"] / fps); seg_end[l["seg"]] = max(seg_end.get(l["seg"], 0), (l["start"] + l["frames"]) / fps)
LOGO_S, CARD_S, END_S = 1.6, 3.5, 4.0
budget = 180 - LOGO_S - CARD_S - END_S - 1
first = next((k for k in sorted(seg_end) if k > 0 and kinds.get(k) not in ("ad", "wire", "close", "open")), 1)
S = max(0, seg_start[first] - 0.4); E = seg_end[first] + 0.6
for k in sorted(seg_end):
    if k <= first: continue
    if kinds.get(k) in ("ad", "wire", "close"): break
    if seg_end[k] + 0.6 - S > budget: break
    E = seg_end[k] + 0.6
E = min(E, S + budget)
tmp = os.path.join(out, "_parts"); os.makedirs(tmp, exist_ok=True)
a2 = os.path.join(out, "short.ass")
open(a2, "w", encoding="utf-8").write(ass(plan["lines"], offset=S, end=E - S, cut=E - S))
body = os.path.join(tmp, "body_v.mp4")
run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "%.2f" % S, "-t", "%.2f" % (E - S), "-i", mp4, "-filter_complex",
     vf(a2) + ",fps=24,fade=t=in:d=0.4,fade=t=out:st=%.2f:d=0.5" % (E - S - 0.5), "-af", "afade=t=in:d=0.3,afade=t=out:st=%.2f:d=0.6,aresample=48000" % (E - S - 0.6),
     "-c:v", "libx264", "-crf", "20", "-c:a", "aac", "-ar", "48000", "-ac", "2", body])
logo_card(W, H, os.path.join(tmp, "logo_v.png")); still(os.path.join(tmp, "logo_v.png"), LOGO_S, W, H, os.path.join(tmp, "logo_v.mp4"), 0.5)
full_show_card(W, H, os.path.join(tmp, "full_v.png"), [("That was the short version.", 94, INK, FONT), ("", 30, INK, FONT2),
    ("The full show + every source, free:", 76, INK, FONT2), ("heartbeatobservatory.com/news", 78, RUST, FONT), ("", 30, INK, FONT2),
    ("New show every day by 7 AM Eastern", 64, INK, FONT2)])
still(os.path.join(tmp, "full_v.png"), CARD_S, W, H, os.path.join(tmp, "full_v.mp4"))
endv = os.path.join(tmp, "end_v.mp4")
run(["ffmpeg", "-y", "-loglevel", "error", "-i", BRAND + "/vertical/endcard-vertical-cream.mp4", "-vf", "scale=%d:%d,fps=24,format=yuv420p" % (W, H),
     "-af", "aresample=48000", "-c:v", "libx264", "-crf", "20", "-c:a", "aac", "-ar", "48000", "-ac", "2", endv])
concat([os.path.join(tmp, "logo_v.mp4"), body, os.path.join(tmp, "full_v.mp4"), endv], os.path.join(out, "short.mp4"))
if "--short-only" in sys.argv: sys.exit(0)
# 2) the whole show, vertical
a1 = os.path.join(out, "vertical.ass"); open(a1, "w", encoding="utf-8").write(ass(plan["lines"]))
run(["ffmpeg", "-y", "-loglevel", "error", "-i", mp4, "-filter_complex", vf(a1), "-c:v", "libx264", "-preset", "medium", "-crf", "23",
     "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", os.path.join(out, "vertical.mp4")])

# 3) the whole show for YouTube as a regular video (Jaron 10/17): 16:9, H logo in front, the cream card at the end
logo_card(1920, 1080, os.path.join(tmp, "logo_h.png")); still(os.path.join(tmp, "logo_h.png"), LOGO_S, 1920, 1080, os.path.join(tmp, "logo_h.mp4"), 0.5)
ec = Image.open(BRAND + "/vertical/endcard-vertical-cream.png").convert("RGB").resize((608, 1080)); bg = Image.new("RGB", (1920, 1080), CREAM)
bg.paste(ec, (656, 0)); bg.save(os.path.join(tmp, "end_h.png")); still(os.path.join(tmp, "end_h.png"), END_S, 1920, 1080, os.path.join(tmp, "end_h.mp4"))
mainh = os.path.join(tmp, "main_h.mp4")
run(["ffmpeg", "-y", "-loglevel", "error", "-i", mp4, "-vf", "scale=1920:1080,fps=24,format=yuv420p", "-af", "aresample=48000",
     "-c:v", "libx264", "-crf", "21", "-preset", "medium", "-c:a", "aac", "-ar", "48000", "-ac", "2", mainh])
concat([os.path.join(tmp, "logo_h.mp4"), mainh, os.path.join(tmp, "end_h.mp4")], os.path.join(out, "youtube.mp4"))
import shutil; shutil.rmtree(tmp, ignore_errors=True)
print("vertical cuts done", out)
