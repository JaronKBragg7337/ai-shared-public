# frames + the two lines (timed from motion.json) -> mp4.   python mux.py <frames dir> <out.mp4> [phone]
# Frames go through PIL into ffmpeg as raw video (this ffmpeg build's PNG reader threw inflate errors / dropped a frame on these files).
# The first SKIP frames are left out: frame 0 of the render shows a ghost of Joe's default pose (motion blur before the first animation tick).
# Pass 2: the take is one camera with no cuts; the low-camera foot checks (<frames dir>_c0, _c1) are appended as labelled replays.
import json, subprocess, sys, os
from PIL import Image, ImageDraw, ImageFont
SKIP = 2
HERE = os.path.dirname(os.path.abspath(__file__)); M = json.load(open(HERE + "/motion.json")); FPS = M["fps"]
frames, out = sys.argv[1], sys.argv[2]; phone = len(sys.argv) > 3
W, H = Image.open(frames + "/f_%04d.png" % SKIP).size
seq = [(frames + "/f_%04d.png" % f, None) for f in range(SKIP, M["frames"])]
for i, c in enumerate(M.get("footchecks", [])):
    d = "%s_c%d" % (frames, i)
    if os.path.isdir(d): seq += [(d + "/f_%04d.png" % f, c["label"]) for f in range(c["f0"], c["f1"]) if os.path.exists(d + "/f_%04d.png" % f)]
dur = len(seq) / FPS
font = ImageFont.truetype("arialbd.ttf", round(H / 24))
cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "%dx%d" % (W, H), "-framerate", str(FPS), "-i", "-"]
for l in M["lines"]: cmd += ["-i", l["file"]]
fl = ";".join("[%d:a]aresample=48000,aformat=channel_layouts=stereo,adelay=%d:all=1[a%d]" % (i + 1, round((l["start"] - SKIP) / FPS * 1000), i) for i, l in enumerate(M["lines"]))
fl += ";" + "".join("[a%d]" % i for i in range(len(M["lines"]))) + "amix=inputs=%d:normalize=0,apad=whole_dur=%.3f[a]" % (len(M["lines"]), dur)   # (an open-ended apad floods the muxer queue while the frames trickle in)
vf = "scale=1280:720:flags=lanczos,format=yuv420p" if phone else "scale=1920:1080:flags=lanczos,format=yuv420p"
cmd += ["-filter_complex", fl + ";[0:v]" + vf + "[v]", "-map", "[v]", "-map", "[a]", "-t", "%.3f" % dur, "-c:v", "libx264", "-preset", "medium", "-crf", "21" if phone else "18",
        "-profile:v", "high", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", out]
p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
for path, label in seq:
    im = Image.open(path).convert("RGB")
    if label:
        dr = ImageDraw.Draw(im); x, y = round(W * 0.03), round(H * 0.045); bb = dr.textbbox((x, y), label, font=font)
        dr.rectangle((bb[0] - 14, bb[1] - 10, bb[2] + 14, bb[3] + 10), fill=(12, 14, 20)); dr.text((x, y), label, fill=(255, 226, 120), font=font)
    p.stdin.write(im.tobytes())
p.stdin.close(); assert p.wait() == 0
print(out, os.path.getsize(out) // 1024, "KB", "%.2f s" % dur, len(seq), "frames")
