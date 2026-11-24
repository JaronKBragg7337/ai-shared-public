# Burn the on-screen labels (projected from the same camera plan Unreal used) and encode renders/<id>.mp4.
# Usage: python overlay.py s05 [--src DIR] [--test f1,f2 -> writes stills to space/stills/]
import json, math, os, sys, subprocess, glob, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
REN = HERE + "/../renders"; MR = "C:/Users/lilli/Projects/necklace-unreal/Saved/MovieRenders"
FFMPEG = "ffmpeg"
W, H = 1920, 1080
FB = "C:/Windows/Fonts/segoeuib.ttf"; FR_ = "C:/Windows/Fonts/segoeui.ttf"
def font(p, s): return ImageFont.truetype(p, s)

def axes_from_rot(r):
    roll, pitch, yaw = [math.radians(a) for a in r]; CR, SR, CP, SP, CY, SY = math.cos(roll), math.sin(roll), math.cos(pitch), math.sin(pitch), math.cos(yaw), math.sin(yaw)
    X = np.array([CP * CY, CP * SY, SP]); Y = np.array([SR * SP * CY - CR * SY, SR * SP * SY + CR * CY, -SR * CP]); Z = np.array([-(CR * SP * CY + SR * SY), CY * SR - CR * SP * SY, CR * CP])
    return X, Y, Z

def project(cam, f, p, w=W, h=H):
    row = cam["rows"][f - cam["f0"]]; pos = np.array(row[:3]); X, Y, Z = axes_from_rot(row[3:6])
    d = np.asarray(p, float) - pos; z = d @ X
    if z <= 1: return None
    k = (w / 2) / (18.0 / cam["lens"])
    return (w / 2 + (d @ Y) / z * k, h / 2 - (d @ Z) / z * k)

def fade(f, a, b, n=9):
    return max(0.0, min(1.0, (f - a) / n, (b - f) / n))

def pill(d, box, alpha, accent=(222, 40, 52)):
    x0, y0, x1, y1 = box
    d.rounded_rectangle(box, radius=10, fill=(8, 12, 22, int(170 * alpha)))
    d.rectangle([x0, y0 + 6, x0 + 5, y1 - 6], fill=(*accent, int(255 * alpha)))

def draw_labels(img, sc, f):
    cams = sc["cams"]; cam = next(c for c in cams if c["f0"] <= f < c["f1"])
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    for lb in sc["labels"]:
        if not (lb["a"] <= f < lb["b"]): continue
        al = fade(f, lb["a"], lb["b"]); kind = lb["kind"]
        if kind in ("banner", "note"):
            fn = font(FB, 40 if kind == "banner" else 34); tw = d.textlength(lb["text"], font=fn)
            cx, cy = lb["at"][0] * W, lb["at"][1] * H
            box = (cx - tw / 2 - 26, cy - 30, cx + tw / 2 + 22, cy + 30); pill(d, box, al, (255, 150, 40) if kind == "banner" else (90, 200, 255))
            d.text((cx - tw / 2 + 2, cy - 27), lb["text"], font=fn, fill=(255, 255, 255, int(255 * al)))
        elif kind == "arrowleft":
            fn = font(FB, 34); cx, cy = lb["at"][0] * W, lb["at"][1] * H; tw = d.textlength(lb["text"], font=fn)
            d.polygon([(cx - 70, cy), (cx - 40, cy - 18), (cx - 40, cy + 18)], fill=(255, 255, 255, int(230 * al)))
            d.rectangle([cx - 42, cy - 5, cx - 6, cy + 5], fill=(255, 255, 255, int(230 * al)))
            d.text((cx + 4, cy - 24), lb["text"], font=fn, fill=(255, 255, 255, int(240 * al)))
        elif kind == "bubble":
            t = (f - lb["a"]) / max(1, lb["b"] - lb["a"]); pop = min(1.0, (f - lb["a"]) / 10.0); pop = 1 - (1 - pop) ** 3
            fn = font(FB, 40); tw = d.textlength(lb["text"], font=fn); r = (tw / 2 + 46) * (0.6 + 0.4 * pop)
            cx = lb["at"][0] * W + 30 * math.sin(t * 5 + lb["a"]); cy = lb["at"][1] * H - 120 * t + 60
            d.ellipse([cx - r, cy - r * 0.62, cx + r, cy + r * 0.62], fill=(200, 230, 255, int(60 * al)), outline=(230, 245, 255, int(200 * al)), width=4)
            d.ellipse([cx - r * 0.6, cy - r * 0.5, cx - r * 0.2, cy - r * 0.3], fill=(255, 255, 255, int(70 * al)))
            for k, (dx, dy, rr) in enumerate(((-r * 0.55, r * 0.75, 14), (-r * 0.75, r * 1.0, 8))):
                d.ellipse([cx + dx - rr, cy + dy - rr, cx + dx + rr, cy + dy + rr], outline=(230, 245, 255, int(170 * al)), width=3)
            if pop > 0.2: d.text((cx - tw / 2, cy - 28), lb["text"], font=fn, fill=(255, 255, 255, int(255 * al)))
        else:   # tag with a leader line to a 3D anchor
            p = project(cam, f, lb["pts"][f])
            if p is None: continue
            fn = font(FB, 34); tw = d.textlength(lb["text"], font=fn)
            bx, by = p[0] + lb["offset"][0] * W, p[1] + lb["offset"][1] * H
            bx = min(max(bx, tw / 2 + 40), W - tw / 2 - 40); by = min(max(by, 0.135 * H), 0.74 * H)
            box = (bx - tw / 2 - 22, by - 26, bx + tw / 2 + 18, by + 26)
            ex = min(max(p[0], box[0]), box[2]); ey = box[1] if p[1] < box[1] else (box[3] if p[1] > box[3] else by)
            if p[1] > H * 0.78 or p[0] < 0 or p[0] > W or p[1] < 0: pass
            else:
                d.line([(ex, ey), p], fill=(255, 255, 255, int(220 * al)), width=3)
                d.ellipse([p[0] - 6, p[1] - 6, p[0] + 6, p[1] + 6], outline=(255, 255, 255, int(240 * al)), width=3)
            pill(d, box, al); d.text((bx - tw / 2 + 2, by - 24), lb["text"], font=fn, fill=(255, 255, 255, int(255 * al)))
    if any(lb["a"] <= f < lb["b"] for lb in sc["labels"]):
        sh = ov.split()[3].filter(ImageFilter.GaussianBlur(3)); shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0)); shadow.putalpha(sh.point(lambda v: v // 2))
        img = Image.alpha_composite(img, shadow)
    return Image.alpha_composite(img, ov)

def frame_path(src, f):
    for pat in ("f_%04d.png", "f_%d.png", "f_%05d.png"):
        p = src + "/" + pat % f
        if os.path.exists(p): return p
    return None

if __name__ == "__main__":
    sid = sys.argv[1]; plan = json.load(open(HERE + "/plan.json")); sc = plan["scenes"][sid]; N = sc["frames"]
    src = MR + "/Pio_" + sid
    if "--src" in sys.argv: src = sys.argv[sys.argv.index("--src") + 1]
    if "--test" in sys.argv:
        os.makedirs(HERE + "/stills", exist_ok=True)
        for f in [int(x) for x in sys.argv[sys.argv.index("--test") + 1].split(",")]:
            p = frame_path(src, f)
            if not p: print("missing", f); continue
            im = draw_labels(Image.open(p).convert("RGBA").resize((W, H)), sc, f).convert("RGB")
            im.save(HERE + "/stills/%s_%04d.jpg" % (sid, f), quality=90); print("still", f)
        sys.exit(0)
    missing = [f for f in range(N) if not frame_path(src, f)]
    if missing: print("MISSING %d frames, first %s" % (len(missing), missing[:10])); sys.exit(1)
    os.makedirs(REN, exist_ok=True); out = REN + "/%s.mp4" % sid
    ff = subprocess.Popen([FFMPEG, "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "%dx%d" % (W, H), "-r", "24", "-i", "-",
                           "-an", "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    for f in range(N):
        im = Image.open(frame_path(src, f)).convert("RGBA")
        if im.size != (W, H): im = im.resize((W, H))
        if sc["labels"]: im = draw_labels(im, sc, f)
        ff.stdin.write(im.convert("RGB").tobytes())
        if f % 200 == 0: print(sid, f, "/", N, flush=True)
    ff.stdin.close(); ff.wait(); print("wrote", out)
