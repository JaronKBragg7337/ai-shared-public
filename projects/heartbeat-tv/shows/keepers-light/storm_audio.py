# The Keeper's Light ep.2 "Storm Night" - soundtrack, all generated (numpy only): rain, gusting wind, surf on the rocks,
# thunder after each flash in build.py's FLASHES, and a low pad under it. -> soundtrack_ep2.wav (48 kHz stereo, 42 s)
import wave
import numpy as np

SR, DUR = 48000, 42.0
N = int(SR * DUR)
t = np.arange(N) / SR
rng = np.random.default_rng(42)
FLASHES = [(3.1, 1.0, 3.0), (14.6, 0.6, 2.2), (24.2, 0.75, 1.8), (35.4, 1.35, 0.5)]   # (s, size, thunder delay s)
CUTS = [0, 11, 22, 32, 42]                                                           # shots: sea, surf, gallery, window


def band(x, lo, hi, soft=0.15):
    # zero-phase band-pass by FFT mask with soft edges
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    m = np.ones_like(f)
    if lo > 0:
        m *= np.clip((f - lo * (1 - soft)) / max(lo * soft * 2, 1), 0, 1)
    if hi:
        m *= np.clip((hi * (1 + soft) - f) / max(hi * soft * 2, 1), 0, 1)
    return np.fft.irfft(X * m, len(x))


def norm(x):
    return x / (np.max(np.abs(x)) + 1e-9)


def smooth_env(points):
    # piecewise-linear envelope from (time, level) pairs
    ts, vs = zip(*points)
    return np.interp(t, ts, vs)


def slow_noise(rate, seed):
    # a slow random wobble, 0..1
    r = np.random.default_rng(seed)
    k = int(DUR * rate) + 3
    return np.interp(t, np.linspace(0, DUR, k), r.random(k))


def shot_env(levels):
    # a level per shot, eased over 0.6 s at each cut
    pts = []
    for i, lv in enumerate(levels):
        a, b = CUTS[i], CUTS[i + 1]
        pts += [(a + (0.3 if i else 0), lv), (b - 0.3, lv)]
    return smooth_env(pts)


out = np.zeros((2, N))
for ch in (0, 1):
    # rain: bright hiss + a softer body, fluttering a little
    hiss = norm(band(rng.standard_normal(N), 1800, 12000))
    body = norm(band(rng.standard_normal(N), 350, 2500))
    flutter = 0.8 + 0.2 * slow_noise(3, 10 + ch)
    rain = (0.55 * hiss + 0.45 * body) * flutter
    # close rain on metal/glass in the gallery shot: sharp random ticks
    ticks = np.zeros(N); idx = rng.integers(0, N, 5200); ticks[idx] = rng.uniform(0.3, 1, len(idx))
    ticks = norm(band(ticks, 2500, 9000))
    rain_lv = shot_env([0.22, 0.2, 0.3, 0.24])
    tick_lv = shot_env([0.0, 0.0, 0.18, 0.05])

    # wind: three bands whose mix moves with the gusts -> a howl that rises and falls
    gust = np.clip(0.25 + 0.9 * slow_noise(0.35, 20) ** 1.6, 0, 1.2)
    w_lo = norm(band(rng.standard_normal(N), 120, 420)); w_mid = norm(band(rng.standard_normal(N), 380, 900))
    w_hi = norm(band(rng.standard_normal(N), 850, 1700))
    wind = w_lo * (1.1 - gust * 0.5) + w_mid * gust * 0.8 + w_hi * gust ** 2 * 0.45
    wind_lv = shot_env([0.2, 0.16, 0.28, 0.2])

    # sea: a constant deep roar + waves breaking (sharp rise, long hiss-off), harder in the surf shot
    roar = norm(band(np.cumsum(rng.standard_normal(N)), 30, 380))
    crash_src = norm(band(rng.standard_normal(N), 150, 5000))
    crash_env = np.zeros(N)
    tt = 0.8 + ch * 0.35
    while tt < DUR:
        i0 = int(tt * SR); rise = 0.25; dec = rng.uniform(1.8, 3.2); size = rng.uniform(0.6, 1.0)
        seg = np.arange(N - i0) / SR
        crash_env[i0:] += size * np.where(seg < rise, seg / rise, np.exp(-(seg - rise) / dec))
        tt += rng.uniform(4.5, 7.5)
    sea = 0.6 * roar + 0.55 * crash_src * crash_env
    sea_lv = shot_env([0.34, 0.42, 0.16, 0.3])

    # thunder: a crack for the near strike, then rolling rumble; far strikes are softer and duller
    thunder = np.zeros(N)
    for fs, size, delay in FLASHES:
        t0 = fs + delay + ch * 0.012
        i0 = int(t0 * SR); seg = np.arange(N - i0) / SR
        near = delay < 1.0
        rum = band(np.cumsum(rng.standard_normal(N - i0)), 20, 160 if not near else 260)
        rum = rum / (np.sqrt(np.mean(rum[:3 * SR] ** 2)) + 1e-9) * 0.3    # by loudness, not by one stray peak
        rum = np.clip(rum, -1, 1) * (1 - np.exp(-seg / (0.35 if not near else 0.08))) * np.exp(-seg / (3.2 if not near else 3.8))
        rum *= 0.75 + 0.25 * np.interp(seg, np.linspace(0, 8, 40), rng.random(40))     # rolling
        thunder[i0:] += size * rum
        if near:
            crack = norm(band(rng.standard_normal(N - i0), 400, 7000)) * np.exp(-seg / 0.09)
            thunder[i0:] += 0.9 * size * crack
    thunder *= 0.9

    # pad: D minor, very low and quiet, like the ep.1 pad in a darker key; lifts a little for the end card
    ph = rng.uniform(0, 6.28)
    pad = sum(a * np.sin(2 * np.pi * f * t + ph + k) for k, (f, a) in enumerate([(73.42, 1), (110.0, 0.6), (87.31, 0.5), (146.83, 0.25)]))
    pad *= 0.85 + 0.15 * np.sin(2 * np.pi * 0.11 * t + ch)
    pad_lv = smooth_env([(0, 0), (4, 0.05), (30, 0.06), (36.5, 0.1), (42, 0.1)])

    mix = rain * rain_lv + ticks * tick_lv + wind * wind_lv + sea * sea_lv + thunder + norm(pad) * pad_lv
    out[ch] = mix

fade = smooth_env([(0, 0), (1.2, 1), (40, 1), (42, 0)])
out *= fade
out = out / np.max(np.abs(out)) * 0.89
pcm = (out.T * 32767).astype(np.int16)
with wave.open(__file__.replace("storm_audio.py", "soundtrack_ep2.wav"), "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print("wrote soundtrack_ep2.wav", pcm.shape)
