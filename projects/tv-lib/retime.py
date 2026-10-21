"""Retime a finished-silent video so every narration cue window is at least as long as its narration.
Used when narration is re-voiced longer than the shots were cut for (no Blender re-render): the section of video
under a too-short cue is slowed (setpts + motion interpolation) and everything after it moves later.
  plan(cues, dur0, lens, gap=1.0)  -> Plan with .cues (new starts), .dur, .m(t) (old time -> new time)
  apply(full_mp4, plan, workdir)   -> path of the retimed mp4
cues = [(start_s, id), ...] on the ORIGINAL timeline; lens = {id: seconds of the trimmed narration clip}."""
import os, subprocess

FPS = 24

class Plan:
    def __init__(self, edges_old, edges_new, cues_old, cues_new):
        self.old, self.new, self.cues0, self.cues = edges_old, edges_new, cues_old, cues_new
        self.dur = edges_new[-1]
    def m(self, t):
        o, n = self.old, self.new
        if t <= o[0]: return t
        for i in range(len(o) - 1):
            if t <= o[i + 1]:
                return n[i] + (t - o[i]) * (n[i + 1] - n[i]) / (o[i + 1] - o[i])
        return n[-1] + (t - o[-1])
    @property
    def stretched(self):
        return any(abs((self.new[i + 1] - self.new[i]) - (self.old[i + 1] - self.old[i])) > 0.01 for i in range(len(self.old) - 1))

def plan(cues, dur0, lens, gap=1.0, end_gap=1.5):
    old = [0.0] + [c for c, _ in cues] + [dur0]
    # rebuild cleanly: edge k = start of interval k (k=0 head, k=1..n cue windows), final edge = end
    new = [0.0, old[1]]
    for i, (c, sid) in enumerate(cues):
        win = old[i + 2] - old[i + 1]
        need = lens[sid] + (end_gap if i == len(cues) - 1 else gap)
        new.append(new[-1] + max(win, need))
    return Plan(old, new, cues, [(new[i + 1], sid) for i, (c, sid) in enumerate(cues)])

def _run(cmd):
    subprocess.check_call(cmd)

def apply(full, p, workdir):
    out = os.path.join(workdir, "full_rt.mp4")
    if not p.stretched: return full
    runs = []   # (old_a, old_b, new_len) merging unstretched neighbours
    for i in range(len(p.old) - 1):
        a, b = p.old[i], p.old[i + 1]; nl = p.new[i + 1] - p.new[i]; st = abs(nl - (b - a)) > 0.01
        if runs and not st and not runs[-1][3]: runs[-1] = (runs[-1][0], b, runs[-1][2] + nl, False)
        else: runs.append((a, b, nl, st))
    parts = []
    for k, (a, b, nl, st) in enumerate(runs):
        o = os.path.join(workdir, "rt%02d.mp4" % k); parts.append(o)
        n = int(round(nl * FPS)); f = nl / (b - a)
        vf = "setpts=%.6f*PTS,minterpolate=fps=%d:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1,format=yuv420p" % (f, FPS) if st else "fps=%d,format=yuv420p" % FPS
        print("retime %.2f-%.2f -> %.2fs (x%.3f)" % (a, b, nl, f), flush=True)
        _run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "%.4f" % a, "-t", "%.4f" % (b - a + 0.05), "-i", full, "-vf", vf,
              "-frames:v", str(n), "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-an", o])
    lst = os.path.join(workdir, "rt_cat.txt")
    open(lst, "w").write("".join("file '%s'\n" % x.replace("\\", "/") for x in parts))
    _run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", out])
    return out
