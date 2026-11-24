import sys, glob, os
from PIL import Image, ImageDraw
d_, out = sys.argv[1], sys.argv[2]
fs = sorted(glob.glob(d_ + '/t_*.png'), key=lambda p: int(p.split('_')[-1][:-4]))
W, H, cols = 640, 360, 3; rows = (len(fs) + cols - 1) // cols
sh = Image.new('RGB', (W * cols, H * rows))
for i, f in enumerate(fs):
    im = Image.open(f).convert('RGB').resize((W, H)); ImageDraw.Draw(im).text((8, 8), os.path.basename(f), fill=(255, 0, 0))
    sh.paste(im, ((i % cols) * W, (i // cols) * H))
sh.save(out, quality=85)
