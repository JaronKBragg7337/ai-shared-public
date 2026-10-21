# Night harbour backdrop for the Rusty Anchor windows: sky, far hills with town lights, moored boats with mast lights, water glints.
from PIL import Image, ImageDraw, ImageFilter
import random, math
random.seed(3); Wd, Hd = 4096, 1024
im = Image.new("RGB", (Wd, Hd)); px = im.load()
for y in range(Hd):
    t = y / Hd
    for x in range(0, Wd):
        if t < 0.62:   # sky: deep blue to a faint warm glow at the horizon
            k = t / 0.62; c = (int(4 + 22 * k ** 3), int(8 + 20 * k ** 2.5), int(22 + 30 * k ** 1.5))
        else:          # water: darker, reflecting the sky
            k = (t - 0.62) / 0.38; c = (int(8 - 6 * k), int(12 - 8 * k), int(24 - 14 * k))
        px[x, y] = c
d = ImageDraw.Draw(im)
for _ in range(900):   # stars
    x, y = random.randrange(Wd), random.randrange(int(Hd * 0.5)); b = random.randint(60, 200); d.point((x, y), (b, b, b))
d.ellipse((3100, 110, 3175, 185), fill=(235, 232, 215))   # moon
hill = [(0, int(Hd * 0.60))]
for x in range(0, Wd + 64, 64): hill.append((x, int(Hd * (0.52 + 0.05 * math.sin(x / 520) + 0.02 * math.sin(x / 150)))))
hill += [(Wd, int(Hd * 0.62)), (0, int(Hd * 0.62))]
d.polygon(hill, fill=(6, 9, 12))
for _ in range(420):   # town lights on the far shore
    x = random.randrange(Wd); y = int(Hd * random.uniform(0.54, 0.615)); c = random.choice([(255, 190, 110), (255, 220, 160), (200, 220, 255)])
    d.rectangle((x, y, x + 2, y + 2), fill=c)
for _ in range(14):    # moored sailboats: hull + mast + masthead light, sized as ~9-12 m boats at a few hundred metres
    x = random.randrange(100, Wd - 100); y = int(Hd * random.uniform(0.66, 0.74)); s = random.uniform(0.7, 1.3)
    d.polygon([(x - 34 * s, y), (x + 34 * s, y), (x + 26 * s, y + 9 * s), (x - 26 * s, y + 9 * s)], fill=(10, 11, 14))
    d.line((x, y, x, y - 95 * s), fill=(16, 16, 20), width=2); d.ellipse((x - 3, y - 98 * s, x + 3, y - 92 * s), fill=(255, 245, 225))
glow = im.filter(ImageFilter.GaussianBlur(6))
im = Image.blend(im, glow, 0.35)
d = ImageDraw.Draw(im)
for _ in range(1600):  # light glints on the water
    x = random.randrange(Wd); y = int(Hd * random.uniform(0.63, 1.0)); w = random.randint(3, 16)
    b = random.randint(40, 120); d.line((x, y, x + w, y), fill=(b, int(b * 0.85), int(b * 0.6)))
im.save("harbour_night.png"); print("harbour ok")
