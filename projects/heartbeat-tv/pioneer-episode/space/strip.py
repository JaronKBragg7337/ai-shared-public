# 12-frame contact sheet of a finished renders/<id>.mp4 -> argv[2]
import subprocess, sys, json
sid, out = sys.argv[1], sys.argv[2]
n = json.load(open(__file__.rsplit("\\",1)[0].rsplit("/",1)[0] + "/../timeline.json", encoding="utf-8"))
N = next(s["f1"] - s["f0"] for s in n["scenes"] if s["id"] == sid); step = max(1, N // 12)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "../renders/%s.mp4" % sid, "-vf", "select='not(mod(n\,%d))',scale=480:270,tile=3x4" % step, "-frames:v", "1", out], check=True)
r = subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries", "stream=nb_read_frames,width,height,r_frame_rate", "-of", "csv=p=0", "../renders/%s.mp4" % sid], capture_output=True, text=True)
print(sid, "expected", N, "got", r.stdout.strip())
