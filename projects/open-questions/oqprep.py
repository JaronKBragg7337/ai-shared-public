# Open Questions audio prep. Run from an episode folder (needs script.json + audio/<id>.wav from Kokoro).
# - synthesizes the 'hmm' sketch (entries with "sfx": "hmm") and the music bed (pentatonic flute-ish plucks over a drone + soft frame drum)
# - trims clips, lays them on a timeline, writes timeline.json, voice.wav, music.wav.   All synthesized sound is CC0.
import json, subprocess, numpy as np, wave, os
GAP, LEAD, TAIL = 0.4, 0.7, 2.8
os.makedirs('audio', exist_ok=True)

def write_wav(path, x, sr, ch=1):
    x = np.clip(x, -1, 1)
    with wave.open(path, 'wb') as w:
        w.setnchannels(ch); w.setsampwidth(2); w.setframerate(sr); w.writeframes((x * 32767).astype('<i2').tobytes())

def synth_hmm(path, sr=24000):
    notes = [(220.0, 261.63, .75), (261.63, 261.63, .5), (293.66, 261.63, .8), (329.63, 329.63, .9), (392.0, 329.63, .9), (293.66, 220.0, 1.5)]
    out = []
    for f0, f1, d in notes:
        n = int(d * sr); tt = np.arange(n) / sr
        f = f0 + (f1 - f0) * np.minimum(1, tt / (d * 0.5)) * (1 + 0.004 * np.sin(2 * np.pi * 5.5 * tt))
        ph = 2 * np.pi * np.cumsum(f) / sr
        w = np.sin(ph) + 0.55 * np.sin(2 * ph) + 0.25 * np.sin(3 * ph) + 0.1 * np.sin(4 * ph)
        env = np.minimum(1, tt / 0.07) * np.minimum(1, (d - tt) / 0.18) * (0.85 + 0.15 * np.sin(2 * np.pi * 5.5 * tt))
        out.append(w * env * 0.3)
    x = np.concatenate(out); tt = np.arange(len(x)) / sr
    rng = np.random.default_rng(3); x += np.convolve(rng.normal(0, 1, len(x)), np.ones(40) / 40, 'same') * 0.02   # a little breath
    t = 0.0
    while t < len(x) / sr - 0.3:   # soft frame-drum pulse
        i = int(t * sr); m = min(int(0.3 * sr), len(x) - i); k = np.arange(m) / sr
        x[i:i + m] += np.sin(2 * np.pi * (95 - 30 * k / 0.3) * k) * np.exp(-k * 14) * 0.35; t += 0.6
    x = x / np.abs(x).max() * 0.55
    write_wav(path, x, sr)

def synth_music(path, total, sr=44100):
    n = int(total * sr); L = np.zeros(n); R = np.zeros(n); rng = np.random.default_rng(11)
    scale = [220.0, 261.63, 293.66, 329.63, 392.0, 440.0]
    bar = 8.0
    for i in range(int(total / bar) + 2):
        t0 = i * bar; a = int(t0 * sr); b = min(n, int((t0 + bar + 2) * sr))
        if a >= n: break
        tt = np.arange(b - a) / sr; env = np.minimum(1, tt / 3) * np.minimum(1, (bar + 2 - tt) / 2)
        for f, g in ((110.0, 0.05), (164.81, 0.035)):   # drone: A2 + E3
            w = np.sin(2 * np.pi * f * tt) * env * g * (1 + 0.2 * np.sin(2 * np.pi * 0.09 * tt)); L[a:b] += w; R[a:b] += w
        for k in range(4):   # plucked flute-ish notes
            ts = t0 + 0.5 + k * 2.0 + rng.uniform(0, 0.8); f = scale[rng.integers(0, len(scale))]; pan = rng.uniform(0.25, 0.75)
            m = int(3.2 * sr); s = int(ts * sr)
            if s >= n: continue
            m = min(m, n - s); q = np.arange(m) / sr
            vib = 1 + 0.004 * np.sin(2 * np.pi * 5 * q) * np.minimum(1, q / 0.5)
            ph = 2 * np.pi * f * np.cumsum(vib) / sr
            w = (np.sin(ph) + 0.3 * np.sin(2 * ph) + 0.08 * np.sin(3 * ph)) * np.minimum(1, q / 0.12) * np.exp(-q * 1.3) * 0.07
            for dl, g in ((0, 1.0), (0.37, 0.35), (0.74, 0.15)):
                o = int(dl * sr)
                if s + o + m > n: continue
                L[s + o:s + o + m] += w * g * (1 - pan); R[s + o:s + o + m] += w * g * pan
        for j in range(4):   # very soft frame drum on 2 and 4
            s = int((t0 + j * 2.0) * sr)
            if s + 8000 > n: continue
            q = np.arange(8000) / sr; d = np.sin(2 * np.pi * (80 - 25 * q / 0.18) * q) * np.exp(-q * 18) * (0.05 if j % 2 == 0 else 0.03)
            L[s:s + 8000] += d; R[s:s + 8000] += d
    x = np.arange(n) / sr; fade = np.minimum(1, x / 2.0) * np.minimum(1, (total - x) / 2.5)
    st = np.stack([L * fade, R * fade], 1); st = st / np.abs(st).max() * 0.9
    write_wav(path, st.reshape(-1), sr, 2)

segs = json.load(open('script.json'))
for s in segs:
    if s.get('sfx') == 'hmm': synth_hmm(f"audio/{s['id']}.wav")
t = LEAD; tl = []
for s in segs:
    out = f"audio/t_{s['id']}.wav"
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', f"audio/{s['id']}.wav", '-af',
        'silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.05,areverse,silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.1,areverse',
        '-ar', '24000', '-ac', '1', out], check=True)
    d = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', out]))
    tl.append(dict(id=s['id'], start=round(t, 3), dur=round(d, 3), text=s['text'])); t += d + GAP
total = t - GAP + TAIL
json.dump(dict(total=round(total, 3), segs=tl), open('timeline.json', 'w'), indent=1)
cmd = ['ffmpeg', '-y', '-v', 'error']
for s in tl: cmd += ['-i', f"audio/t_{s['id']}.wav"]
fc = ''.join(f"[{i}]adelay={int(s['start'] * 1000)}:all=1[a{i}];" for i, s in enumerate(tl))
fc += ''.join(f"[a{i}]" for i in range(len(tl))) + f"amix=inputs={len(tl)}:normalize=0,loudnorm=I=-16:TP=-1.5,apad=whole_dur={total}[v]"
subprocess.run(cmd + ['-filter_complex', fc, '-map', '[v]', '-ar', '44100', '-ac', '2', 'audio/voice.wav'], check=True)
synth_music('audio/music.wav', total)
print('total', total)
