# Procedural textures for the space/truck scenes (Pillow + numpy). All original artwork.
import math, random, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
OUT = __file__.replace("\\", "/").rsplit("/", 1)[0] + "/tex/"
F = "C:/Windows/Fonts/"
def font(name, size): return ImageFont.truetype(F + name, size)

def save(img, name): img.convert("RGB").save(OUT + name + ".png"); print("tex", name, img.size)

def blur_noise(h, w, sigma, seed):
    r = np.random.default_rng(seed).random((h, w)).astype(np.float32)
    im = Image.fromarray((r * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(sigma))
    a = np.asarray(im).astype(np.float32) / 255.0
    return (a - a.min()) / (a.max() - a.min() + 1e-6)

def up(a, W, H):
    return np.asarray(Image.fromarray((a * 255).astype(np.uint8)).resize((W, H), Image.BILINEAR)).astype(np.float32) / 255

# ---------------- plaque engraving (ORIGINAL simplified design: line figures, starburst, planet row, probe path)
def plaque():
    W, H = 4096, 2672; S = 2
    im = Image.new("L", (W * S, H * S), 255); d = ImageDraw.Draw(im)
    def P(x, y): return (x * W * S, y * H * S)
    lw = int(16 * S)
    def line(a, b, w=lw): d.line([P(*a), P(*b)], fill=40, width=w)
    def circ(c, r, w=lw, fill=None):
        x, y = P(*c); rr = r * W * S
        d.ellipse([x - rr, y - rr, x + rr, y + rr], outline=40, width=w, fill=fill)
    m = 0.025
    d.rectangle([P(m, m * 1.53), P(1 - m, 1 - m * 1.53)], outline=70, width=int(4 * S))
    for c in ((0.05, 0.08), (0.95, 0.08), (0.05, 0.92), (0.95, 0.92)): circ(c, 0.008, w=int(12 * S))
    # starburst (our own: 11 rays of different lengths, a dot at each tip) + a reference line
    cx, cy = 0.31, 0.43
    rays = [(12, 0.20), (40, 0.12), (73, 0.17), (105, 0.09), (140, 0.15), (166, 0.22), (200, 0.11), (228, 0.16), (262, 0.13), (300, 0.19), (330, 0.10)]
    for ang, L in rays:
        a = math.radians(ang); b = (cx + L * math.cos(a), cy - L * math.sin(a) * 1.533)
        line((cx, cy), b, w=int(12 * S)); circ(b, 0.0035, w=int(10 * S), fill=40)
    line((cx, cy), (0.62, cy), w=int(10 * S))
    circ((cx, cy), 0.012, w=int(14 * S))
    # spacecraft outline (simplified, behind the figures): dish bowl + hex body + booms
    sx, sy = 0.79, 0.40
    d.arc([P(sx - 0.13, sy - 0.30), P(sx + 0.13, sy - 0.02)], 200, 340, fill=60, width=int(6 * S))
    line((sx - 0.12, sy - 0.21), (sx + 0.12, sy - 0.21), w=int(12 * S))
    hx = [(sx + 0.05 * math.cos(math.radians(a)), sy - 0.13 + 0.05 * 1.533 * math.sin(math.radians(a))) for a in range(0, 360, 60)]
    d.polygon([P(*p) for p in hx], outline=60, width=int(5 * S))
    line((sx - 0.05, sy - 0.13), (sx - 0.16, sy - 0.05), w=int(10 * S)); line((sx + 0.05, sy - 0.13), (sx + 0.17, sy - 0.07), w=int(10 * S))
    # two simple line figures in front of the craft (outline style, original proportions)
    def figure(x0, h, wave):
        hy = 0.86 - h; hr = h * 0.075
        circ((x0, hy + hr * 1.533), hr)
        neck = hy + 2 * hr * 1.533
        sh = neck + h * 0.06; hip = neck + h * 0.42; foot = 0.86
        line((x0, neck), (x0, hip))
        line((x0 - h * 0.11, sh), (x0 + h * 0.11, sh))
        line((x0 - h * 0.11, sh), (x0 - h * 0.15, sh + h * 0.30))
        if wave:
            line((x0 + h * 0.11, sh), (x0 + h * 0.20, sh - h * 0.18)); line((x0 + h * 0.20, sh - h * 0.18), (x0 + h * 0.18, sh - h * 0.30))
        else: line((x0 + h * 0.11, sh), (x0 + h * 0.15, sh + h * 0.30))
        line((x0, hip), (x0 - h * 0.08, foot)); line((x0, hip), (x0 + h * 0.08, foot))
    figure(0.72, 0.44, True); figure(0.84, 0.40, False)
    # planet row along the bottom: Sun (bigger) + 9 dots; a tiny probe path leaving the third planet
    py = 0.93; xs = [0.115 + i * 0.056 for i in range(10)]; rs = [0.016, 0.004, 0.006, 0.006, 0.005, 0.012, 0.011, 0.008, 0.008, 0.004]
    for x, r in zip(xs, rs): circ((x, py), r, w=int(12 * S))
    pts = [(xs[3] + (xs[-1] + 0.05 - xs[3]) * t, py - 0.012 - 0.11 * math.sin(t * math.pi * 0.62)) for t in np.linspace(0, 1, 40)]
    d.line([P(*p) for p in pts], fill=70, width=int(4 * S))
    tip = pts[-1]; d.polygon([P(tip[0] + 0.012, tip[1] - 0.004), P(tip[0] - 0.004, tip[1] - 0.012), P(tip[0] - 0.002, tip[1] + 0.006)], fill=40)
    im = im.resize((W, H), Image.LANCZOS)
    a = np.asarray(im).astype(np.float32) / 255.0
    g = up(blur_noise(H // 8, W // 8, 1.2, 3), W, H)
    a = np.clip(a * (0.93 + 0.07 * g), 0, 1)
    save(Image.fromarray((a * 255).astype(np.uint8)), "T_Plaque")

# ---------------- truck livery (box sides): white, red + blue sweep, HBN LIVE
def livery():
    W, H = 2048, 1024; im = Image.new("RGB", (W, H), (236, 238, 240)); d = ImageDraw.Draw(im)
    red, blue = (205, 22, 38), (20, 60, 170)
    def band(y0, y1, col, rise):
        d.polygon([(0, y0 - rise), (W, y0), (W, y1), (0, y1 - rise)], fill=col)
    band(620, 700, blue, 80); band(705, 790, red, 80)
    f1 = font("arialbd.ttf", 330); f2 = font("arialbd.ttf", 96); f3 = font("arialbd.ttf", 64)
    d.text((140, 180), "HBN", font=f1, fill=blue)
    d.text((880, 260), "HEARTBEAT", font=f2, fill=(30, 34, 44)); d.text((880, 370), "NEWS", font=f2, fill=red)
    d.rounded_rectangle([1520, 120, 1900, 230], 24, fill=red); d.text((1585, 125), "LIVE", font=f2, fill=(255, 255, 255))
    d.text((150, 840), "heartbeatobservatory.com", font=f3, fill=(70, 74, 84))
    save(im, "T_Livery")

def lot():
    W = 4096
    n = up(blur_noise(W // 4, W // 4, 1.0, 11), W, W); n2 = up(blur_noise(W // 32, W // 32, 2.0, 12), W, W)
    base = 0.20 + 0.06 * n + 0.05 * n2
    img = np.stack([base * 0.98, base, base * 1.03], -1)
    im = Image.fromarray((np.clip(img, 0, 1) * 255).astype(np.uint8)); d = ImageDraw.Draw(im)
    ppm = W / 120.0
    for row_y in (30, 58, 86):
        y0 = int(row_y * ppm)
        for i in range(0, 34):
            x = int((10 + i * 2.7) * ppm); d.line([(x, y0), (x, y0 + int(5.5 * ppm))], fill=(225, 225, 215), width=5)
        d.line([(int(10 * ppm), y0 + int(5.5 * ppm)), (int(101.8 * ppm), y0 + int(5.5 * ppm))], fill=(225, 225, 215), width=4)
    d.text((int(52 * ppm), int(44 * ppm)), "HBN", font=font("arialbd.ttf", 200), fill=(200, 200, 190))
    save(im, "T_Lot")

def sky():
    H = 512; a = np.zeros((H, 16, 3), np.float32)
    hor = np.array([0.62, 0.78, 0.95]); zen = np.array([0.10, 0.30, 0.78])
    for y in range(H):
        v = y / (H - 1)
        t = min(1.0, max(0.0, (0.5 - v) / 0.5)) ** 0.55
        a[y, :] = hor * (1 - t) + zen * t if v <= 0.5 else hor * 0.9
    save(Image.fromarray((a * 255).astype(np.uint8)), "T_Sky")

def dish():
    W, H = 2048, 512; a = np.ones((H, W), np.float32) * 0.92
    a -= 0.04 * blur_noise(H, W, 6, 21)
    for k in range(24):
        x = int(k * W / 24); a[:, max(0, x - 2):x + 2] = 0.72
    for v in (0.13, 0.42, 0.72, 0.985):
        y = int(v * H); a[max(0, y - 2):y + 2, :] = 0.76
    save(Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8)), "T_Dish")

def mli():
    W = 1024; h = blur_noise(W, W, 3, 31) * 0.6 + blur_noise(W, W, 9, 32) * 0.4
    ridge = 1 - np.abs(blur_noise(W, W, 4, 33) * 2 - 1)
    h = 0.5 * h + 0.5 * ridge ** 3
    gy, gx = np.gradient(h * 8.0)
    nz = np.ones_like(h); l = np.sqrt(gx * gx + gy * gy + nz * nz)
    nrm = np.stack([-gx / l, -gy / l, nz / l], -1)
    save(Image.fromarray(((nrm * 0.5 + 0.5) * 255).astype(np.uint8)), "T_MLI_N")
    c = 0.75 + 0.25 * blur_noise(W, W, 5, 34)
    save(Image.fromarray((np.clip(c, 0, 1) * 255).astype(np.uint8)), "T_MLI")

def monitors():
    f = font("consolab.ttf", 64); fs = font("consolab.ttf", 40)
    im = Image.new("RGB", (1024, 640), (6, 14, 32)); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 1024, 90], fill=(180, 20, 36)); d.text((30, 10), "HBN LIVE   SIGNAL", font=f, fill=(255, 255, 255))
    for i in range(5): d.rectangle([80 + i * 110, 470 - i * 70, 160 + i * 110, 560], fill=(60, 220, 120))
    d.text((640, 300), "LINK: GOOD", font=fs, fill=(120, 255, 170)); d.text((640, 360), "DISH: HOME", font=fs, fill=(120, 200, 255))
    save(im, "T_Mon1")
    im = Image.new("RGB", (1024, 640), (4, 10, 22)); d = ImageDraw.Draw(im)
    for x in range(0, 1024, 64): d.line([(x, 0), (x, 640)], fill=(20, 40, 70), width=2)
    for y in range(0, 640, 64): d.line([(0, y), (1024, y)], fill=(20, 40, 70), width=2)
    d.ellipse([90, 290, 150, 350], fill=(255, 220, 90))
    for i in range(40):
        t = i / 39; x = 150 + t * 780; y = 320 - 180 * math.sin(t * 1.3)
        d.ellipse([x - 5, y - 5, x + 5, y + 5], fill=(110, 200, 255))
    d.text((30, 20), "TRACK  P-10", font=fs, fill=(140, 210, 255)); d.text((30, 570), "DOPPLER  OK", font=fs, fill=(140, 255, 180))
    save(im, "T_Mon2")
    im = Image.new("RGB", (1024, 640), (8, 10, 20)); d = ImageDraw.Draw(im)
    pts = [(x, 320 + 150 * math.sin(x / 37.0) * math.sin(x / 210.0)) for x in range(0, 1024, 4)]
    d.line(pts, fill=(255, 190, 70), width=6); d.text((30, 20), "AUDIO  -12 dB", font=fs, fill=(255, 200, 120))
    save(im, "T_Mon3")

def paper():
    W, H = 1400, 1900; base = 0.86 + 0.06 * blur_noise(H, W, 3, 41)
    im = Image.fromarray((np.stack([base, base * 0.985, base * 0.95], -1) * 255).astype(np.uint8)); d = ImageDraw.Draw(im)
    ink = (28, 28, 30)
    d.text((70, 40), "HEARTBEAT NEWS", font=font("georgiab.ttf", 120), fill=ink)
    d.line([(60, 190), (W - 60, 190)], fill=ink, width=6); d.text((70, 200), "SPACE EDITION  -  LIVE FROM THE TRUCK", font=font("georgia.ttf", 42), fill=ink)
    d.line([(60, 260), (W - 60, 260)], fill=ink, width=3)
    d.text((60, 300), "GRAVITY:", font=font("impact.ttf", 300), fill=ink)
    d.text((60, 640), "BROKEN?", font=font("impact.ttf", 300), fill=(170, 18, 30))
    d.text((70, 1000), "Old spacecraft slows down a tiny bit too much", font=font("georgiai.ttf", 46), fill=ink)
    r = random.Random(5)
    for col in range(3):
        x0 = 70 + col * 430
        for i in range(24):
            y = 1090 + i * 32; L = r.randint(300, 390) if i % 7 != 6 else r.randint(120, 260)
            d.rectangle([x0, y, x0 + L, y + 12], fill=(95, 95, 98))
    save(im, "T_Paper")

def sign():
    im = Image.new("RGB", (2048, 256), (12, 16, 30)); d = ImageDraw.Draw(im)
    d.text((40, 30), "HEARTBEAT NEWS", font=font("arialbd.ttf", 180), fill=(240, 244, 255))
    d.rectangle([1760, 50, 2010, 210], fill=(205, 22, 38)); d.text((1785, 70), "HBN", font=font("arialbd.ttf", 110), fill=(255, 255, 255))
    save(im, "T_Sign")

def fx():
    n = 256; y, x = np.mgrid[0:n, 0:n] / (n - 1.0) - 0.5; r = np.sqrt(x * x + y * y) * 2
    core = np.clip(1 - r, 0, 1) ** 2.2; halo = np.exp(-(r * 3.2) ** 2) * 0.35
    a = np.clip(core + halo * (r < 1), 0, 1); a[r >= 1] = 0
    save(Image.fromarray((a * 255).astype(np.uint8)), "T_Radial")
    h = 256; g = np.zeros((h, 16, 3), np.float32)
    for i in range(h):
        v = i / (h - 1.0)
        c = np.array([1.0, 0.95, 0.8]) * (1 - v) ** 0.5 if v < 0.12 else None
        stops = [(0.0, (1.0, 0.97, 0.85)), (0.15, (1.0, 0.75, 0.30)), (0.45, (1.0, 0.40, 0.08)), (0.8, (0.6, 0.12, 0.02)), (1.0, (0.0, 0.0, 0.0))]
        for (v0, c0), (v1, c1) in zip(stops[:-1], stops[1:]):
            if v0 <= v <= v1:
                t = (v - v0) / (v1 - v0); g[i, :] = np.array(c0) * (1 - t) + np.array(c1) * t
    save(Image.fromarray((g * 255).astype(np.uint8)), "T_Flame")
    save(Image.new("RGB", (8, 8), (255, 255, 255)), "T_White")

if __name__ == "__main__":
    for fn in (plaque, livery, lot, sky, dish, mli, monitors, paper, sign, fx): fn()
