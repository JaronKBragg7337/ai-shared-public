"""verify_frames.py - is the finished mp4 really the frames we rendered?
Decodes the mp4 (ffmpeg, raw RGB out) and compares every frame with its source JPEG decoded by PIL.
A damaged frame (blocky smear) differs hugely from its source; a healthy x264 frame differs by a couple of levels.
usage: python verify_frames.py <frames_dir> <video.mp4>   -> prints "VERIFY ok ..." or "VERIFY BAD ...", exit 0 / 5
"""
import os, subprocess, sys
from PIL import Image, ImageChops, ImageStat
d, mp4 = sys.argv[1], sys.argv[2]
names = sorted(f for f in os.listdir(d) if f.endswith(".jpg"))
with Image.open(os.path.join(d, names[0])) as im: w, h = im.size
p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", mp4, "-an", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
bad, worst, n = [], 0.0, 0
for k, name in enumerate(names):
    buf = p.stdout.read(w * h * 3)
    if len(buf) < w * h * 3: bad.append((k, "missing")); break
    n += 1
    if k % 3: continue                      # every third frame is plenty: damage lasts until the next keyframe
    a = Image.frombytes("RGB", (w, h), buf).resize((w // 4, h // 4))
    with Image.open(os.path.join(d, name)) as src: b = src.convert("RGB").resize((w // 4, h // 4))
    diff = sum(ImageStat.Stat(ImageChops.difference(a, b)).mean) / 3
    worst = max(worst, diff)
    if diff > 6: bad.append((k, round(diff, 1)))
p.stdout.close(); p.wait()
if bad: print(f"VERIFY BAD {len(bad)} frames, first {bad[:6]}, worst diff {worst:.1f}"); sys.exit(5)
print(f"VERIFY ok {n} frames, worst diff {worst:.2f}")
