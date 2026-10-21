# Space Now music bed (CC0, generated here): NOT the History pad, NOT Still Unknown's drone. A warm, steady "mission clock":
# a soft low pulse every 2 s (like a slow heartbeat / telemetry tick), a sustained warm fifth (G2 + D3) with slow swell,
# and a gentle rising three-note motif every ~16 s. Overwrites audio/music.wav after tv-lib/prep.py.
import json, numpy as np, wave
total = json.load(open('timeline.json'))['total']
sr = 44100; n = int(total * sr); t = np.arange(n) / sr
L = np.zeros(n); R = np.zeros(n)
# warm sustained fifth with slow swell
for f, amp, ph, pan in ((98.0, 0.07, 0.0, 0.45), (98.0 * 1.003, 0.05, 1.2, 0.55), (146.83, 0.045, 0.6, 0.6), (196.0, 0.02, 2.0, 0.4)):
    sw = 0.6 + 0.4 * np.sin(2 * np.pi * t / 17.0 + ph)
    w = np.sin(2 * np.pi * f * t + ph) * amp * sw
    L += w * (1 - pan); R += w * pan
# soft pulse every 2 s: filtered thump (low sine burst with fast decay)
for k in range(int(total / 2.0) + 1):
    t0 = k * 2.0; i0 = int(t0 * sr); i1 = min(n, i0 + int(0.5 * sr))
    if i0 >= n: break
    tt = np.arange(i1 - i0) / sr
    p = np.sin(2 * np.pi * 55.0 * tt) * np.exp(-tt / 0.09) * 0.12
    L[i0:i1] += p * 0.5; R[i0:i1] += p * 0.5
# rising motif every 16 s: G4 - A4 - D5, soft triangle-ish, 0.9 s each
motif = [(392.0, 0.0), (440.0, 0.9), (587.33, 1.8)]
for k in range(int(total / 16) + 1):
    base = 6.0 + k * 16.0
    for f, off in motif:
        t0 = base + off; i0 = int(t0 * sr); i1 = min(n, i0 + int(2.2 * sr))
        if i0 >= n: break
        tt = np.arange(i1 - i0) / sr
        env = np.minimum(1, tt / 0.05) * np.exp(-tt / 0.9)
        s = (np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(2 * np.pi * 2 * f * tt)) * env * 0.035
        pan = 0.35 + 0.3 * (off / 1.8)
        L[i0:i1] += s * (1 - pan); R[i0:i1] += s * pan
fade = np.minimum(1, t / 2.5) * np.minimum(1, (total - t) / 3.0)
st = np.stack([L * fade, R * fade], 1); st = st / np.abs(st).max() * 0.9
with wave.open('audio/music.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes((st * 32767).astype('<i2').tobytes())
print('music', total)
