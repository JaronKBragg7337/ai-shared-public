# Still Unknown music bed: NOT the History/Science Am-F-C-G pad. A low D drone with a slow fifth, a soft filtered-noise
# shimmer, and a sparse high "ping" every ~11 s. Generated here (CC0). Overwrites audio/music.wav after tv-lib/prep.py.
import json, numpy as np, wave
total = json.load(open('timeline.json'))['total']
sr = 44100; n = int(total * sr); t = np.arange(n) / sr
rng = np.random.default_rng(10)
L = np.zeros(n); R = np.zeros(n)
# drone: D1/D2 with slow detune, fifth (A2) fading in and out over 20 s
for f, amp, ph in ((36.71, 0.09, 0.0), (73.42, 0.07, 1.0), (73.42 * 1.004, 0.05, 2.0), (110.0, 0.035, 0.5)):
    sw = 0.5 + 0.5 * np.sin(2 * np.pi * t / 20.0 + ph) if f > 100 else 1.0
    w = np.sin(2 * np.pi * f * t + ph) * amp * sw
    L += w * (0.55 if f < 100 else 0.35); R += w * (0.45 if f < 100 else 0.65)
# shimmer: noise through a crude one-pole low-pass, slowly breathing
noise = rng.standard_normal(n) * 0.02
lp = np.zeros(n); a = 0.02
acc = 0.0
# vectorised IIR via lfilter-free loop would be slow; use scipy if present else chunked numpy approximation
try:
    from scipy.signal import lfilter
    lp = lfilter([a], [1, -(1 - a)], noise)
except Exception:
    lp = np.convolve(noise, np.exp(-np.arange(400) * a) * a, 'same')
breath = 0.4 + 0.6 * (0.5 + 0.5 * np.sin(2 * np.pi * t / 13.0))
L += lp * breath * 2.0; R += np.roll(lp, 900) * breath * 2.0
# sparse pings: high D (1174.7 Hz) with a 3 s decay, every ~11 s, offset
for k in range(int(total / 11) + 1):
    t0 = 4.0 + k * 11.0
    if t0 >= total: break
    i0 = int(t0 * sr); i1 = min(n, i0 + int(3.5 * sr)); tt = np.arange(i1 - i0) / sr
    p = np.sin(2 * np.pi * 1174.66 * tt) * np.exp(-tt / 1.1) * 0.05 + np.sin(2 * np.pi * 1174.66 * 1.5 * tt) * np.exp(-tt / 0.6) * 0.02
    pan = 0.3 + 0.4 * (k % 2)
    L[i0:i1] += p * (1 - pan); R[i0:i1] += p * pan
fade = np.minimum(1, t / 3.0) * np.minimum(1, (total - t) / 3.0)
st = np.stack([L * fade, R * fade], 1); st = st / np.abs(st).max() * 0.9
with wave.open('audio/music.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes((st * 32767).astype('<i2').tobytes())
print('music', total)
