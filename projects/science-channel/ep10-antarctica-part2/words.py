import json, os, subprocess, sys, numpy as np
H = os.path.dirname(os.path.abspath(__file__))
from faster_whisper import WhisperModel
m = WhisperModel("small.en", device="cpu", compute_type="int8")
for s in json.load(open(os.path.join(H, "script.json"), encoding="utf8")):
    sid = s["id"]; src = os.path.join(H, "audio", sid + ".wav"); wav = os.path.join(H, "audio", "t_%s.wav" % sid)
    cache = os.path.join(H, "audio", "words_%s.json" % sid)
    if os.path.exists(cache) and os.path.getmtime(cache) > os.path.getmtime(src): continue
    subprocess.check_call(["ffmpeg", "-y", "-v", "error", "-i", src, "-af", "silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.05,areverse,silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.1,areverse", "-ar", "24000", "-ac", "1", wav])
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", wav, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"])
    audio = np.frombuffer(raw, dtype="<i2").astype("float32") / 32768.0
    segs, _ = m.transcribe(audio, language="en", beam_size=5, word_timestamps=True, condition_on_previous_text=False)
    ws = [dict(w=w.word.strip(), s=round(w.start, 3), e=round(w.end, 3)) for sg in segs for w in (sg.words or [])]
    json.dump(ws, open(cache, "w"))
    d = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", wav]).decode())
    print("==", sid, round(d, 2), flush=True)
    line = []
    for w in ws:
        line.append("%s@%.1f" % (w["w"], w["s"]))
    print(" ".join(line), flush=True)
