# frames -> renders/<id>.mp4 (1920x1080, 24 fps, H.264 crf 16, no audio, exactly f1-f0 frames; the PRE pre-roll frames are dropped)
# python encode.py s01 [tag] ; frames go through PIL (this ffmpeg build's PNG reader dropped frames on Unreal PNGs)
import json, subprocess, sys, os
from PIL import Image
EP = os.path.dirname(os.path.abspath(__file__)) + "/.."; PRE = 8
sid = sys.argv[1]; tag = sys.argv[2] if len(sys.argv) > 2 else ""
sc = next(s for s in json.load(open(EP + "/timeline.json", encoding="utf-8"))["scenes"] if s["id"] == sid); N = sc["f1"] - sc["f0"]
D = "C:/Users/lilli/Projects/necklace-unreal/Saved/MovieRenders/Pioneer_" + sid + tag
files = ["%s/f_%04d.png" % (D, PRE + f) for f in range(N)]; miss = [f for f in files if not os.path.exists(f)]
assert not miss, "missing %d frames, first %s" % (len(miss), miss[0])
out = sys.argv[3] if len(sys.argv) > 3 else EP + "/renders/%s.mp4" % sid; os.makedirs(os.path.dirname(out), exist_ok=True)
W, H = Image.open(files[0]).size
cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "%dx%d" % (W, H), "-framerate", "24", "-i", "-", "-an",
       "-vf", "scale=1920:1080:flags=lanczos,format=yuv420p", "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-profile:v", "high", "-movflags", "+faststart", out]
p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
for f in files: p.stdin.write(Image.open(f).convert("RGB").tobytes())
p.stdin.close(); assert p.wait() == 0
n = subprocess.check_output(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v", "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", out]).decode().strip()
print(sid, out, "frames", n, "expected", N, "OK" if int(n) == N else "MISMATCH")
