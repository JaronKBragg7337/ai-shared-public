# First Light - the first song on Heartbeat TV's Music channel.
# Written and played by Claude Code (Opus 5.5) on the MSI, 2026-10-24, for Jaron. CC0 - free to use.
#
# Every sound here is made from math: no samples, no AI music service. A heartbeat opens and closes it
# (the company's name), piano and a warm pad carry the chords (D - A - Bm - G, the hopeful one), and a
# soft lead sings the tune. "First light" is what an observatory calls the first image a new telescope sees.
#
#   python compose.py           -> first-light.wav (full song, ~2:15) and first-light-post.wav (68.5 s, cut to Post 1)
import numpy as np, wave, sys, os

SR = 44100
BPM = 120
BEAT = 60 / BPM
BAR = 4 * BEAT                      # 2 s: the Post 1 video's sections land on bar lines
rng = np.random.default_rng(141)    # 141 days since the first tool went on the MSI

def hz(m): return 440.0 * 2 ** ((m - 69) / 12)

CHORDS = {   # piano voicing, pad voicing, bass root
    "D":  ([62, 66, 69, 76], [50, 57, 62, 66], 38),
    "A":  ([61, 64, 69, 71], [45, 57, 61, 64], 33),
    "Bm": ([62, 66, 71, 73], [47, 54, 62, 66], 35),
    "G":  ([62, 67, 71, 74], [43, 55, 62, 67], 31),
}
# The tune, two lines per chord: (beat, length in beats, note).
MELODY = {
    "D":  [[(0, 1.5, 78), (1.5, .5, 76), (2, 1, 74), (3, 1, 69)],
           [(0, 1.5, 78), (1.5, .5, 76), (2, 1, 74), (3, 1, 78)]],
    "A":  [[(0, 1.5, 73), (1.5, .5, 74), (2, 2, 76)],
           [(0, 2, 81), (2, 1, 79), (3, 1, 78)]],
    "Bm": [[(0, 1, 78), (1, 1, 81), (2, 1, 78), (3, 1, 76)],
           [(0, 1, 76), (1, .5, 78), (1.5, .5, 76), (2, 2, 74)]],
    "G":  [[(0, 1.5, 74), (1.5, .5, 71), (2, 1, 74), (3, 1, 76)],
           [(0, 1, 71), (1, 1, 74), (2, 2, 74)]],
}

def env(n, a, r, total=None):
    """attack/release envelope, seconds"""
    e = np.ones(n)
    na, nr = int(a * SR), int(r * SR)
    if na: e[:na] = np.linspace(0, 1, na)
    if nr: e[-nr:] *= np.linspace(1, 0, nr)
    return e

def piano(m, dur, vel=1.0):
    n = int((dur + 1.6) * SR); t = np.arange(n) / SR; f = hz(m); out = np.zeros(n)
    for k in range(1, 9):
        fk = f * k * (1 + 0.0004 * k * k)                       # a little string stiffness
        out += np.sin(2 * np.pi * fk * t + rng.random()) * k ** -1.4 * np.exp(-t * (1.1 + 0.9 * k))
    out *= env(n, 0.004, 0.05)
    hold = np.ones(n); cut = int(dur * SR)
    if cut < n: hold[cut:] = np.exp(-(t[cut:] - dur) * 6)        # key let go: damper
    return out * hold * vel * 0.34

def pad(m, dur):
    n = int((dur + 0.8) * SR); t = np.arange(n) / SR; out = np.zeros(n)
    for det in (-0.12, 0.0, 0.11):                               # three voices, slightly apart = warmth
        f = hz(m + det)
        for k in range(1, 10):
            out += np.sin(2 * np.pi * f * k * t + rng.random() * 6) * k ** -2.2
    return out * env(n, 0.9, 0.8) * 0.055

def bass(m, dur):
    n = int(dur * SR); t = np.arange(n) / SR; f = hz(m)
    x = 0.8 * np.sin(2 * np.pi * f * t) + 0.5 * np.sin(4 * np.pi * f * t) + 0.25 * np.sin(6 * np.pi * f * t)
    return np.tanh(1.6 * x) * env(n, 0.006, min(0.08, dur / 3)) * 0.30

def lead(m, dur, vel=1.0):
    n = int((dur + 0.35) * SR); t = np.arange(n) / SR
    vib = 1 + 0.004 * np.sin(2 * np.pi * 5.2 * t) * np.clip((t - 0.18) * 4, 0, 1)
    ph = 2 * np.pi * np.cumsum(hz(m) * vib) / SR
    x = sum(((-1) ** (k // 2)) * np.sin(k * ph) / k ** 2 for k in (1, 3, 5, 7))   # soft triangle
    x += 0.25 * np.sin(2 * ph)                                                      # a little body
    e = env(n, 0.025, 0.3); e *= np.exp(-t * 0.6)
    return x * e * vel * 0.24

def thump(f0, f1, dec, amp):
    n = int(0.6 * SR); t = np.arange(n) / SR
    f = f1 + (f0 - f1) * np.exp(-t * 28)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return (0.75 * np.sin(ph) + 0.35 * np.sin(2 * ph) + 0.15 * np.sin(3 * ph)) * np.exp(-t / dec) * amp   # upper partials: heard on phone speakers too

def kick():  return thump(140, 46, 0.18, 0.9) + np.r_[rng.normal(0, 1, 90) * np.exp(-np.arange(90) / 20) * 0.15, np.zeros(int(0.6 * SR) - 90)]
def lub():   return thump(85, 42, 0.12, 0.75)
def dub():   return thump(95, 48, 0.09, 0.5)

def snare():
    n = int(0.35 * SR); t = np.arange(n) / SR
    nz = np.convolve(rng.normal(0, 1, n), np.ones(4) / 4, mode="same")   # body, not hiss
    return (nz * np.exp(-t / 0.07) * 0.30 + np.sin(2 * np.pi * 185 * t) * np.exp(-t / 0.05) * 0.25)

def hat(open_=False):
    n = int((0.3 if open_ else 0.08) * SR); t = np.arange(n) / SR
    nz = np.diff(rng.normal(0, 1, n + 1))
    nz = nz - np.convolve(nz, np.ones(3) / 3, mode="same") * 0.5     # bright but not glassy
    return nz * np.exp(-t / (0.09 if open_ else 0.022)) * 0.032

def riser(dur):
    n = int(dur * SR); t = np.arange(n) / SR
    nz = np.convolve(rng.normal(0, 1, n), np.ones(6) / 6, mode="same")
    return nz * (t / dur) ** 2.2 * 0.05

class Track:
    def __init__(self, seconds):
        self.n = int(seconds * SR); self.dry = np.zeros((self.n, 2)); self.wet = np.zeros((self.n, 2))
        self.duck = np.ones(self.n)   # pad + bass breathe with the kick
        self.ducked = np.zeros((self.n, 2))
    def add(self, x, at, pan=0.0, send=0.2, ducked=False):
        i = int(at * SR)
        if i >= self.n: return
        x = x[: self.n - i]
        l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
        tgt = self.ducked if ducked else self.dry
        tgt[i:i + len(x), 0] += x * l * 1.414 * (1 - send * 0.5)
        tgt[i:i + len(x), 1] += x * r * 1.414 * (1 - send * 0.5)
        self.wet[i:i + len(x), 0] += x * l * send
        self.wet[i:i + len(x), 1] += x * r * send
    def pump(self, at, depth=0.45):
        i = int(at * SR); n = min(int(0.42 * SR), self.n - i)
        if n > 0: self.duck[i:i + n] = np.minimum(self.duck[i:i + n], 1 - depth * np.exp(-np.arange(n) / (0.12 * SR)))
    def mix(self):
        # Reverb: one long room made of fading noise, convolved in one pass.
        ir_n = int(2.8 * SR); t = np.arange(ir_n) / SR
        wet = np.zeros_like(self.wet)
        for ch in range(2):
            ir = rng.normal(0, 1, ir_n) * np.exp(-t / 0.75)
            ir = np.convolve(ir, np.ones(8) / 8, mode="same")       # darker tail
            ir[: int(0.02 * SR)] = 0
            L = self.n + ir_n
            wet[:, ch] = np.fft.irfft(np.fft.rfft(self.wet[:, ch], L) * np.fft.rfft(ir, L), L)[: self.n]
        wet *= 0.9 / (np.abs(wet).max() + 1e-9) * np.abs(self.wet).max()
        out = self.dry + self.ducked * self.duck[:, None] + wet
        out = np.tanh(out * 1.1) / np.tanh(1.1)
        return out / (np.abs(out).max() + 1e-9) * 0.89                # -1 dB

def play(plan, seconds, fade_out=3.0):
    """plan: list of (section, chord), one per 2-second bar."""
    tr = Track(seconds); var = {}
    for b, (sec, ch) in enumerate(plan):
        t0 = b * BAR; pv, padv, root = CHORDS[ch]
        full = sec in ("chorus", "final")
        # heartbeat: lub-dub once a second in the intro, break and outro (resting heart, 60 bpm)
        if sec in ("intro", "verse", "break", "outro", "lift"):
            for bt in range(0, 4, 2) if sec != "outro" or b < len(plan) - 1 else [0]:
                tr.add(lub(), t0 + bt * BEAT, send=0.15); tr.add(dub(), t0 + bt * BEAT + 0.19, send=0.15)
        # piano
        if sec in ("intro", "lift", "outro"):
            for j, m in enumerate(pv): tr.add(piano(m, BAR * (2 if sec == "outro" else 1), 0.8), t0 + j * 0.03, pan=-0.2 + 0.13 * j, send=0.4)
        elif sec in ("verse", "break", "chorus", "final"):
            arp = [pv[0], pv[1], pv[2], pv[3], pv[2], pv[1], pv[2], pv[3]]
            for j, m in enumerate(arp):
                tr.add(piano(m, BEAT * 0.5, 0.55 if sec == "break" else 0.7), t0 + j * BEAT / 2, pan=-0.35 + 0.1 * j, send=0.35)
        # pad
        if sec != "intro":
            for m in padv: tr.add(pad(m + (12 if sec == "final" else 0), BAR), t0, pan=0, send=0.5, ducked=full)
        # bass
        if sec in ("verse", "chorus", "final"):
            for q in range(4): tr.add(bass(root, BEAT * 0.9), t0 + q * BEAT, ducked=full)
        if sec == "outro" and b == len(plan) - 3: tr.add(bass(root, BAR * 2), t0)
        # drums: half-time - kick on 1, snare on 3, hats on 8ths
        if full:
            for q in (0, 2.5): tr.add(kick(), t0 + q * BEAT, send=0.05); tr.pump(t0 + q * BEAT)
            tr.add(snare(), t0 + 2 * BEAT, send=0.35)
            for e in range(8): tr.add(hat(e == 7), t0 + e * BEAT / 2, pan=0.3, send=0.1)
        elif sec == "verse":
            for e in range(1, 8, 2): tr.add(hat(), t0 + e * BEAT / 2, pan=0.3, send=0.1)
        if sec == "lift": tr.add(riser(BAR), t0, send=0.6)
        # the tune
        if sec in ("chorus", "final", "break"):
            k = var.get(ch, 0); var[ch] = k + 1
            for bt, d, m in MELODY[ch][k % 2]:
                if sec == "break":
                    if d >= 1: tr.add(piano(m, d * BEAT, 0.9), t0 + bt * BEAT, pan=0.1, send=0.55)
                    continue
                tr.add(lead(m, d * BEAT), t0 + bt * BEAT, pan=0.15, send=0.35)
                if sec == "final": tr.add(lead(m + 12, d * BEAT, 0.35), t0 + bt * BEAT, pan=-0.25, send=0.6)
    out = tr.mix()
    fn = int(fade_out * SR); out[-fn:] *= np.linspace(1, 0, fn)[:, None] ** 1.5
    return out

def save(path, x):
    with wave.open(path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype("<i2").tobytes())
    print(path, f"{len(x) / SR:.1f} s")

def bars(sec, chords): return [(sec, c) for c in chords]
P = ["D", "A", "Bm", "G"]

# Post 1 cut: every section change lands on the video (site appears at 6 s, "school laptop" 20 s, TV 22 s,
# phone 44 s, closing words 52 s, end card 64 s).
POST = (bars("intro", ["D", "A", "Bm"]) + bars("verse", ["G", "D", "A", "Bm", "G", "D", "A"]) + bars("lift", ["A"]) +
        bars("chorus", P * 2 + ["D", "A", "Bm"]) + bars("break", ["G", "D", "A", "Bm"]) +
        bars("final", ["G", "D", "A", "Bm", "G", "A"]) + bars("outro", ["D", "D", "D"]))
FULL = (bars("intro", P) + bars("verse", P * 2) + bars("lift", ["A"]) + bars("chorus", P * 4) + bars("break", P * 2) +
        bars("lift", ["A"]) + bars("final", P * 4) + bars("outro", ["D", "D", "D", "D"]))

if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    save(os.path.join(here, "first-light-post.wav"), play(POST, 68.5, fade_out=3.5))
    if "--post-only" not in sys.argv:
        save(os.path.join(here, "first-light.wav"), play(FULL, len(FULL) * BAR + 2, fade_out=5))
