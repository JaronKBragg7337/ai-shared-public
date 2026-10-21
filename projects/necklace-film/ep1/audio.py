# The Necklace ep.1 part 1 - the sound bed, all generated (numpy only): insects and waves on the pilings (loud outside, muffled
# inside), the bar murmur with a burst of laughter where the book puts it, a glass set down, Mateo's steps, and a slow warm
# minor pad. Voices are mixed on top by finish.sh.  -> bed.wav (48 kHz stereo, 116 s)
import wave, math
import numpy as np

SR, DUR, FPS = 48000, 116.0, 24
N = int(SR * DUR); t = np.arange(N) / SR
rng = np.random.default_rng(11)
SH = {"s1": (0, 11), "s2": (11, 27), "s3": (27, 37), "s4": (37, 46), "s5": (46, 68.5), "s6": (68.5, 74.5), "s7": (74.5, 87.5),
      "s8a": (87.5, 92.3), "s8b": (92.3, 96.5), "s8c": (96.5, 109.5), "s9": (109.5, 116)}
OUTSIDE = [SH["s1"], SH["s4"]]


def band(x, lo, hi, soft=0.15):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); m = np.ones_like(f)
    if lo > 0: m *= np.clip((f - lo * (1 - soft)) / max(lo * soft * 2, 1), 0, 1)
    if hi: m *= np.clip((hi * (1 + soft) - f) / max(hi * soft * 2, 1), 0, 1)
    return np.fft.irfft(X * m, len(x))


def norm(x): return x / (np.max(np.abs(x)) + 1e-9)
def env(points):
    ts, vs = zip(*points); return np.interp(t, ts, vs)


def inside_env(out_lv, in_lv, ramp=0.25):
    """level that is out_lv during the exterior shots and in_lv inside, with a short crossfade at each cut"""
    pts = [(0, out_lv)]
    for a, b in sorted(SH.values()):
        lv = out_lv if (a, b) in OUTSIDE else in_lv
        pts += [(a + (ramp if a else 0), lv), (b - ramp, lv)]
    pts.append((DUR, pts[-1][1]))
    return env(pts)


def burst(start, length, lo, hi, decay, seed, amp=1.0):
    r = np.random.default_rng(seed); n = int(length * SR); i0 = int(start * SR)
    x = band(r.standard_normal(n), lo, hi) * np.exp(-np.arange(n) / SR / decay)
    out = np.zeros(N); n = min(n, N - i0); out[i0:i0 + n] = norm(x)[:n] * amp
    return out


out = np.zeros((2, N))
for ch in (0, 1):
    # --- waves on the pilings: a soft roar + slow swells that slap and hiss
    roar = norm(band(np.cumsum(rng.standard_normal(N)), 30, 400))
    hiss = norm(band(rng.standard_normal(N), 300, 5000))
    swell = np.zeros(N); tt = 0.6 + ch * 0.9
    while tt < DUR:
        i0 = int(tt * SR); seg = np.arange(N - i0) / SR; size = rng.uniform(0.5, 1.0)
        swell[i0:] += size * np.where(seg < 0.35, seg / 0.35, np.exp(-(seg - 0.35) / 1.3))
        tt += rng.uniform(3.2, 5.5)
    waves = 0.55 * roar + 0.6 * hiss * np.clip(swell, 0, 1.4)
    waves_in = band(waves, 0, 900)            # through the walls: only the low thump
    # --- insects: many crickets (pulsed tones ~4.2 kHz) + a cicada drone
    insects = np.zeros(N)
    for k in range(7):
        f0 = rng.uniform(3600, 4700); rate = rng.uniform(13, 24); ph = rng.random()
        pulse = (np.sin(2 * np.pi * rate * t + ph * 6.28) > 0.3).astype(float)
        on = (np.sin(2 * np.pi * rng.uniform(0.07, 0.2) * t + rng.random() * 6) > -0.4).astype(float)   # they stop and start
        insects += np.sin(2 * np.pi * f0 * t) * pulse * on * (0.6 if (k % 2) == ch else 0.35)
    cic = np.sin(2 * np.pi * 5900 * t) * (0.5 + 0.5 * np.sin(2 * np.pi * 110 * t)) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.05 * t + ch))
    insects = norm(insects + 0.25 * cic) * 0.5
    insects_in = band(insects, 0, 3200) * 0.6     # dulled by the room
    # --- the bar murmur: band-limited noise shaped by syllable-rate modulation, several "voices", plus the room's hum
    murmur = np.zeros(N)
    for k in range(6):
        syl = np.clip(np.sin(2 * np.pi * rng.uniform(3, 5) * t + rng.random() * 6) * 0.5 + 0.5 + 0.3 * np.sin(2 * np.pi * rng.uniform(0.3, 0.9) * t), 0, 1)
        on = (np.sin(2 * np.pi * rng.uniform(0.05, 0.15) * t + rng.random() * 6) > -0.2).astype(float)
        lo, hi = (120, 900) if k % 2 else (180, 1800)
        murmur += norm(band(rng.standard_normal(N), lo, hi)) * syl * on * (0.7 if k % 2 == ch else 0.45)
    murmur = norm(murmur)
    # the burst of laughter the book mentions (during "punctuated by the occasional burst of laughter", ~52 s), far table
    laugh = np.zeros(N)
    for j, (lt, lf) in enumerate(((52.4, 420), (52.62, 400), (52.84, 385), (53.05, 370), (53.3, 350), (53.6, 330))):
        i0 = int(lt * SR); n = int(0.17 * SR); tl = np.arange(n) / SR
        v = np.sin(2 * np.pi * lf * tl) * (1 + 0.4 * np.sin(2 * np.pi * 2 * lf * tl)) + 0.5 * band(rng.standard_normal(n), 400, 3000)
        laugh[i0:i0 + n] += v * np.sin(np.pi * tl / 0.17) ** 0.7 * (0.9 - 0.1 * j)
    laugh = band(laugh, 250, 3500); laugh = norm(laugh) * (0.11 if ch == 0 else 0.07)
    fan = norm(band(rng.standard_normal(N), 60, 160)) * 0.5 + 0.5 * np.sin(2 * np.pi * 0.9 * t)   # the ceiling fan's slow beat
    # --- foley: the glass set down on the bar (s3 end), Mateo's steps (s6), the stool creak as he sits (cut), a second glass
    glass = burst(36.2, 0.25, 900, 6000, 0.03, 21, 0.18) + burst(36.21, 0.5, 120, 700, 0.09, 22, 0.14)
    steps = np.zeros(N)
    st = 69.0
    while st < 74.2:
        steps += burst(st + ch * 0.002, 0.22, 90, 900, 0.03, 100 + int(st * 10), 0.22) + burst(st + 0.01, 0.15, 2000, 7000, 0.02, 200 + int(st * 10), 0.04)
        st += 0.62
    stool = burst(74.6, 0.4, 150, 1500, 0.12, 31, 0.1)
    glass2 = burst(96.0, 0.25, 900, 6000, 0.03, 41, 0.12) + burst(96.01, 0.5, 120, 700, 0.09, 42, 0.1)
    # --- pad: D minor, slow, warm; swells under the title and again at the warning / the doorway
    chords = [(0, [73.42, 110.0, 146.83, 174.61]), (27, [65.41, 98.0, 130.81, 164.81]), (46, [73.42, 110.0, 146.83, 174.61]),
              (68.5, [58.27, 87.31, 116.54, 146.83]), (87.5, [73.42, 110.0, 146.83, 174.61]), (96.5, [55.0, 82.41, 110.0, 130.81]), (116, [55.0, 82.41, 110.0, 130.81])]
    pad = np.zeros(N)
    for i in range(len(chords) - 1):
        a, fa = chords[i]; b, fb = chords[i + 1]
        ia, ib = int(a * SR), int(b * SR); seg = np.arange(ib - ia) / SR
        xf = np.clip(seg / 2.5, 0, 1)                      # 2.5 s crossfade into each chord
        for f_ in fa: pad[ia:ib] += (1 - xf) * np.sin(2 * np.pi * f_ * t[ia:ib] + ch * 0.7) * (0.9 if f_ < 100 else 0.5)
        for f_ in fb: pad[ia:ib] += xf * np.sin(2 * np.pi * f_ * t[ia:ib] + ch * 0.7) * (0.9 if f_ < 100 else 0.5)
    pad = norm(pad) * (0.85 + 0.15 * np.sin(2 * np.pi * 0.08 * t + ch))
    pad_lv = env([(0, 0), (2, 0.16), (10, 0.16), (13, 0.06), (36, 0.06), (37, 0.09), (46, 0.09), (47, 0.05), (68, 0.05),
                  (69, 0.08), (87, 0.07), (96, 0.07), (97, 0.1), (109, 0.12), (110, 0.17), (114, 0.17), (116, 0)])
    # --- mix with the inside / outside levels
    mix = (waves * inside_env(0.42, 0.0) + waves_in * inside_env(0.0, 0.16)
           + insects * inside_env(0.5, 0.0) + insects_in * inside_env(0.0, 0.14)
           + murmur * inside_env(0.03, 0.17) + laugh + fan * inside_env(0.0, 0.05)
           + glass + steps + stool + glass2 + pad * pad_lv)
    out[ch] = mix

out *= env([(0, 0), (1.0, 1), (113.5, 1), (116, 0)])
out = out / np.max(np.abs(out)) * 0.85
pcm = (out.T * 32767).astype(np.int16)
with wave.open(__file__.replace("audio.py", "bed.wav"), "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print("wrote bed.wav")
