# Pioneer episode: lay every voiced line on one clock -> timeline.json + voices/dialogue.wav (48 kHz mono).
# Gaps like the news plan: 0.45 s between lines, 0.9 s extra between scenes, 1.0 s lead-in. Scene windows are what the
# Unreal shots and boards must fill. Frames at 24 fps.
import json, wave, struct, os
FPS, RATE, GAP, SCENE_GAP, LEAD, TAIL = 24, 48000, 0.45, 0.9, 1.0, 1.5
D = os.path.dirname(os.path.abspath(__file__)); V = os.path.join(D, "voices")
script = json.load(open(os.path.join(D, "script.json"), encoding="utf8"))
man = {}
for m in ("manifest_vex.json", "manifest.json"):
    p = os.path.join(V, m)
    if os.path.exists(p):
        for r in json.load(open(p, encoding="utf8")): man[r["file"]] = r
def read(f):
    w = wave.open(os.path.join(V, f)); sr, n, ch = w.getframerate(), w.getnframes(), w.getnchannels()
    s = struct.unpack("<%dh" % (n * ch), w.readframes(n))[::ch]
    if sr != RATE:   # simple resample
        k = sr / RATE; s = [s[min(len(s) - 1, int(i * k))] for i in range(int(len(s) / k))]
    # trim trailing near-silence (the chain adds a 0.9 s tail)
    e = len(s)
    while e > 0 and abs(s[e - 1]) < 200: e -= 1
    return list(s[:e + int(0.05 * RATE)])
t = LEAD; scenes = []; track = []
for si, sc in enumerate(script):
    st = t; lines = []
    for li, l in enumerate(sc["lines"]):
        f = "%02d_%02d_%s.wav" % (si, li, l["who"]); s = read(f); dur = len(s) / RATE
        lines.append({"who": l["who"], "text": l["text"], "file": f, "start": round(t, 3), "dur": round(dur, 3),
                      "f0": int(round(t * FPS)), "frames": int(round(dur * FPS)) + 1})
        track.append((int(t * RATE), s)); t += dur + GAP
    t += SCENE_GAP - GAP
    scenes.append({"id": sc["id"], "place": sc["place"], "shot": sc["shot"], "board": sc.get("board"),
                   "start": round(st, 3), "end": round(t, 3), "f0": int(round(st * FPS)), "f1": int(round(t * FPS)), "lines": lines})
scenes[0]["start"] = 0.0; scenes[0]["f0"] = 0
END = t + TAIL; scenes[-1]["end"] = round(END, 3); scenes[-1]["f1"] = int(round(END * FPS))
for i in range(len(scenes) - 1): scenes[i]["end"] = scenes[i + 1]["start"]; scenes[i]["f1"] = scenes[i + 1]["f0"]
buf = [0] * int(END * RATE + RATE)
for a, s in track:
    for i, x in enumerate(s): buf[a + i] = max(-32767, min(32767, buf[a + i] + x))
w = wave.open(os.path.join(V, "dialogue.wav"), "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(RATE)
w.writeframes(struct.pack("<%dh" % len(buf), *buf)); w.close()
json.dump({"fps": FPS, "seconds": round(END, 3), "frames": int(round(END * FPS)), "scenes": scenes}, open(os.path.join(D, "timeline.json"), "w", encoding="utf8"), ensure_ascii=False, indent=1)
print("total %.1f s (%d:%02d)" % (END, END // 60, END % 60))
for s in scenes: print("%s %-6s %6.1f-%6.1f (%5.1f s) %d lines" % (s["id"], s["place"], s["start"], s["end"], s["end"] - s["start"], len(s["lines"])))
