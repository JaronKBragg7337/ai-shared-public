"""raw_frames.py - fallback frame reader for render.mjs (same idea as news-show/pipeline/pipe_encode.py).
Decodes the JPEG frames with PIL and writes raw RGB to stdout, so ffmpeg's own image decoders are never used.
usage: python raw_frames.py <frames_dir>   (stdout -> ffmpeg -f rawvideo -pix_fmt rgb24 -s WxH -i -)
"""
import os, sys
from PIL import Image
d = sys.argv[1]
out = sys.stdout.buffer
for n in sorted(f for f in os.listdir(d) if f.endswith(".jpg")):
    with Image.open(os.path.join(d, n)) as im:
        out.write(im.convert("RGB").tobytes())
out.flush()
