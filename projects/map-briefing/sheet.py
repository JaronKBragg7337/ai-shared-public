# contact sheets of the stills, for a quick look: python sheet.py <date> [vertical|wide]
import sys, glob, os
from PIL import Image
date = sys.argv[1]; kind = sys.argv[2] if len(sys.argv) > 2 else "vertical"
here = os.path.dirname(os.path.abspath(__file__))
fs = sorted(glob.glob(os.path.join(here, "out", f"{date}-{kind}-still-*.jpg")))
per = 4 if kind == "vertical" else 4
for n in range(0, len(fs), per):
    ims = [Image.open(f) for f in fs[n:n + per]]
    w, h = ims[0].size; sc = 500 / w if kind == "vertical" else 900 / w
    tw, th = int(w * sc), int(h * sc); cols = per if kind == "vertical" else 2
    rows = (len(ims) + cols - 1) // cols
    sheet = Image.new("RGB", (tw * cols, th * rows), (0, 0, 0))
    for i, im in enumerate(ims): sheet.paste(im.resize((tw, th), Image.LANCZOS), ((i % cols) * tw, (i // cols) * th))
    out = os.path.join(here, "out", f"{date}-{kind}-sheet-{n // per + 1}.jpg"); sheet.save(out, quality=88); print(out)
