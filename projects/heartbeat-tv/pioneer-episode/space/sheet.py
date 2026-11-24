# contact sheets of space/stills/*.jpg -> scratch folder given as argv[1]
import glob, os, sys
from PIL import Image, ImageDraw
fs = sorted(glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), "stills", "*.jpg")))
pat = sys.argv[2] if len(sys.argv) > 2 else ""
fs = [f for f in fs if pat in os.path.basename(f)]
for k in range(0, len(fs), 6):
    sheet = Image.new("RGB", (1280, 1080))
    for i, f in enumerate(fs[k:k + 6]):
        im = Image.open(f).resize((640, 360)); ImageDraw.Draw(im).text((8, 8), os.path.basename(f), fill=(255, 255, 0))
        sheet.paste(im, ((i % 2) * 640, (i // 2) * 360))
    sheet.save(os.path.join(sys.argv[1], "sheet%d.jpg" % (k // 6)))
print(len(fs))
