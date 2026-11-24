"""pipe_encode.py - fallback encoder for the rendered news (11/22/2026).

On 11/22 ffmpeg's own PNG reader failed on the Unreal frames ("inflate returned error -3", then a crash) while every frame
decoded fine in PIL. This reads the frames with PIL and pipes raw RGB into ffmpeg with the SAME x264/aac settings as the
normal encode, so the show still publishes. run_rendered_news.ps1 calls it only when the normal encode fails.
usage: python pipe_encode.py <frames_dir> <episode.wav> <out.mp4> [hold_frames]
"""
import os, subprocess, sys, time
from multiprocessing import Pool
from PIL import Image

FR = sys.argv[1]

def load(name):
    with Image.open(os.path.join(FR, name)) as im:
        return im.convert("RGB").tobytes()

if __name__ == "__main__":
    wav, mp4 = sys.argv[2], sys.argv[3]
    hold = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    names = sorted((n for n in os.listdir(FR) if n.startswith("f_") and n.endswith(".png")), key=lambda n: int(n[2:-4]))
    with Image.open(os.path.join(FR, names[0])) as im:
        w, h = im.size
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h}", "-framerate", "24",
           "-i", "-", "-i", wav, "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", mp4]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    t, last = time.time(), None
    with Pool(10) as pool:
        for k, b in enumerate(pool.imap(load, names, chunksize=8)):
            p.stdin.write(b); last = b
            if k % 4000 == 0: print(f"{k}/{len(names)} {time.time() - t:.0f}s", flush=True)
    for _ in range(hold):
        p.stdin.write(last)
    p.stdin.close()
    rc = p.wait()
    print("pipe encode rc", rc, f"{time.time() - t:.0f}s")
    sys.exit(rc)
