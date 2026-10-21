# The Keeper's Light ep.3 "The Keeper" - soundtrack, all generated (numpy only): the calm after the storm - sea against the
# base, a light wind, far gulls, the lamp switching off (8.5 s), the door (12 s), the keeper's steps timed to his walk in
# build.py (walk from 12.5 s, x1.33 slower, heel strikes every 12 source frames), and a warm pad. -> soundtrack_ep3.wav
import wave
import numpy as np

SR, DUR, FPS = 48000, 42.0, 24
N = int(SR * DUR)
t = np.arange(N) / SR
rng = np.random.default_rng(7)
CUTS = [0, 11, 22, 32, 42]
W0, W1, SCALE = int(12.5 * FPS), int(17.3 * FPS), 1.33


def band(x, lo, hi, soft=0.15):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    m = np.ones_like(f)
    if lo > 0:
        m *= np.clip((f - lo * (1 - soft)) / max(lo * soft * 2, 1), 0, 1)
    if hi:
        m *= np.clip((hi * (1 + soft) - f) / max(hi * soft * 2, 1), 0, 1)
    return np.fft.irfft(X * m, len(x))


def norm(x):
    return x / (np.max(np.abs(x)) + 1e-9)


def env(points):
    ts, vs = zip(*points)
    return np.interp(t, ts, vs)


def slow(rate, seed):
    r = np.random.default_rng(seed); k = int(DUR * rate) + 3
    return np.interp(t, np.linspace(0, DUR, k), r.random(k))


def shot_env(levels):
    pts = []
    for i, lv in enumerate(levels):
        pts += [(CUTS[i] + (0.3 if i else 0), lv), (CUTS[i + 1] - 0.3, lv)]
    return env(pts)


def burst(start, length, lo, hi, decay, seed):
    # a short filtered-noise event placed at `start` seconds
    r = np.random.default_rng(seed); n = int(length * SR); i0 = int(start * SR)
    x = band(r.standard_normal(n), lo, hi) * np.exp(-np.arange(n) / SR / decay)
    out = np.zeros(N); out[i0:i0 + n] = norm(x)[:max(0, min(n, N - i0))]
    return out


out = np.zeros((2, N))
steps = []
k = 0
while True:
    f = W0 + SCALE * (1 + 12 * k)
    if f > W1 + 4:
        break
    steps.append(f / FPS); k += 1

for ch in (0, 1):
    # sea: a soft roar + slow swells slapping the base
    roar = norm(band(np.cumsum(rng.standard_normal(N)), 40, 500))
    wash = norm(band(rng.standard_normal(N), 200, 4500))
    swell = np.zeros(N); tt = 1.0 + ch * 0.4
    while tt < DUR:
        i0 = int(tt * SR); seg = np.arange(N - i0) / SR; size = rng.uniform(0.5, 0.9)
        swell[i0:] += size * np.where(seg < 0.5, seg / 0.5, np.exp(-(seg - 0.5) / 1.6))
        tt += rng.uniform(5.0, 7.0)
    sea = 0.7 * roar + 0.5 * wash * swell
    sea_lv = shot_env([0.32, 0.22, 0.26, 0.3])
    # wind: light and steady
    wind = norm(band(rng.standard_normal(N), 150, 900)) * (0.6 + 0.4 * slow(0.25, 3 + ch))
    wind_lv = shot_env([0.1, 0.07, 0.1, 0.1])
    # gulls, far off: a falling two-part cry with a quick wobble
    gulls = np.zeros(N)
    for gt, gp, pan in ((4.2, 1.0, 0), (6.1, 0.9, 1), (24.5, 1.05, 1), (27.0, 0.95, 0), (35.0, 1.0, 0), (36.1, 1.1, 1)):
        for part, (dt_, ln) in enumerate(((0.0, 0.32), (0.4, 0.5))):
            i0 = int((gt + dt_) * SR); n = int(ln * SR); tl = np.arange(n) / SR
            f0 = gp * (1750 - 700 * tl / ln) * (1 + 0.02 * np.sin(2 * np.pi * 23 * tl))
            ph = 2 * np.pi * np.cumsum(f0) / SR
            cry = (np.sin(ph) + 0.35 * np.sin(2 * ph) + 0.15 * np.sin(3 * ph)) * np.sin(np.pi * tl / ln) ** 0.6
            gulls[i0:i0 + n] += cry * (0.8 if part else 0.55) * (1.0 if pan == ch else 0.6)
    gulls = band(gulls, 600, 5500) * 0.07
    # the lamp switching off: a low clunk up in the lantern, far away in the wide shot
    clunk = burst(8.52, 0.4, 60, 400, 0.08, 11) * 0.14
    # the door: latch click, then a slow creak (a resonant scrape with a rising pitch)
    latch = burst(11.95, 0.1, 1500, 6000, 0.015, 12) * 0.22
    n = int(0.9 * SR); i0 = int(12.05 * SR); tl = np.arange(n) / SR
    creak_f = 180 + 140 * tl / 0.9 + 25 * np.sin(2 * np.pi * 9 * tl)
    creak = np.zeros(N)
    pulse = (np.sin(2 * np.pi * np.cumsum(creak_f) / SR) > 0.93).astype(float)     # stick-slip clicks
    creak[i0:i0 + n] = band(pulse, 250, 3500)[:n] * np.sin(np.pi * tl / 0.9) ** 0.5
    creak = norm(creak) * 0.12
    # footsteps on wet concrete: a soft heel thud with a little splash
    foot = np.zeros(N)
    for j, st in enumerate(steps):
        foot += burst(st + ch * 0.003, 0.25, 70, 900, 0.035, 100 + j) * 0.28
        foot += burst(st + 0.01, 0.2, 2500, 9000, 0.03, 200 + j) * 0.06
    foot_lv = env([(0, 0), (11.9, 0), (12.0, 1), (21.8, 1), (22.2, 0), (42, 0)])   # heard in the door shot only
    # pad: D major, warm, rising for the end card
    pad = sum(a * np.sin(2 * np.pi * f * t + k_ * 0.7 + ch) for k_, (f, a) in enumerate(
        [(73.42, 1.0), (110.0, 0.6), (146.83, 0.45), (185.0, 0.35), (220.0, 0.2)]))
    pad *= 0.85 + 0.15 * np.sin(2 * np.pi * 0.09 * t + ch)
    pad_lv = env([(0, 0), (5, 0.07), (28, 0.08), (36.5, 0.15), (42, 0.15)])
    out[ch] = (sea * sea_lv + wind * wind_lv + gulls + clunk + latch + creak + foot * foot_lv + norm(pad) * pad_lv)

out *= env([(0, 0), (1.2, 1), (40, 1), (42, 0)])
out = out / np.max(np.abs(out)) * 0.89
pcm = (out.T * 32767).astype(np.int16)
with wave.open(__file__.replace("keeper_audio.py", "soundtrack_ep3.wav"), "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print("wrote soundtrack_ep3.wav; steps at", [round(x, 2) for x in steps])
