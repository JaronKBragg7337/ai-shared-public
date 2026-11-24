# Heartbeat beat kit - sketch beats for Jaron's producer ear. Built by Claude Code, 2026-10-24. CC0.
# Every sound is made from math (no samples). Each beat writes stems (drums, bass, keys, melody) + a full mix,
# so a beat can be tweaked part by part for an artist's flow.
#
#   python beat.py            -> out/<style>/{drums,bass,keys,melody,mix}.wav + <style>.mp3, for every style
#   python beat.py trap       -> just one
import numpy as np, wave, os, sys, subprocess

SR = 44100
rng = np.random.default_rng(7)
def hz(m): return 440.0 * 2 ** ((m - 69) / 12)
def t_(sec): return np.arange(int(sec * SR)) / SR
def fade(x, a=0.003, r=0.02):
    n = len(x); e = np.ones(n); na, nr = min(n, int(a * SR)), min(n, int(r * SR))
    if na: e[:na] = np.linspace(0, 1, na)
    if nr: e[-nr:] *= np.linspace(1, 0, nr)
    return x * e
def smooth(x, k): return np.convolve(x, np.ones(k) / k, mode="same")

# ---------- drums ----------
def kick(punch=1.0, dec=0.22):
    t = t_(0.7); f = 48 + 110 * np.exp(-t * 30)
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = (np.sin(ph) + 0.3 * np.sin(2 * ph)) * np.exp(-t / dec)
    x[:120] += rng.normal(0, 1, 120) * np.exp(-np.arange(120) / 25) * 0.25 * punch
    return np.tanh(x * 1.5) * 0.9
def snare(body=185, dec=0.11, tone=0.35):
    t = t_(0.45); nz = smooth(rng.normal(0, 1, len(t)), 2) - smooth(rng.normal(0, 1, len(t)), 12) * 0.6
    return nz * np.exp(-t / dec) * 0.45 + np.sin(2 * np.pi * body * t) * np.exp(-t / 0.05) * tone
def clap():
    t = t_(0.4); out = np.zeros(len(t))
    for i, d in enumerate((0, 0.011, 0.022)):            # three hands, a hair apart
        j = int(d * SR); nz = smooth(rng.normal(0, 1, len(t) - j), 3)
        out[j:] += nz * np.exp(-t[: len(t) - j] / (0.012 if i < 2 else 0.12)) * 0.5
    return out - smooth(out, 20) * 0.7
def hat(dec=0.025, amp=0.11):
    t = t_(0.2); nz = rng.normal(0, 1, len(t)); nz = nz - smooth(nz, 4)
    return nz * np.exp(-t / dec) * amp
def rim():
    t = t_(0.12); return (np.sin(2 * np.pi * 480 * t) * 0.5 + smooth(rng.normal(0, 1, len(t)), 2) * 0.3) * np.exp(-t / 0.018)
def snap():
    t = t_(0.15); nz = rng.normal(0, 1, len(t)); nz = nz - smooth(nz, 6)
    return nz * np.exp(-t / 0.03) * 0.35
def vinyl(sec):
    x = rng.normal(0, 1, int(sec * SR)) * 0.004
    pops = rng.random(len(x)) < 0.00012; x[pops] += rng.normal(0, 0.25, pops.sum())
    return smooth(x, 3)

# ---------- tonal ----------
def b808(m, dur, slide_from=None):
    t = t_(dur + 0.05); f = np.full(len(t), hz(m))
    if slide_from is not None: f = hz(m) + (hz(slide_from) - hz(m)) * np.exp(-t * 18)
    f = f * (1 + 0.6 * np.exp(-t * 45))                  # click of the hit
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.sin(ph) * np.exp(-t / max(0.35, dur * 0.8))
    return fade(np.tanh(x * 2.2) * 0.55, 0.002, 0.04)     # saturation = heard on phones
def ubass(m, dur):                                        # round upright-ish bass
    t = t_(dur); ph = 2 * np.pi * hz(m) * t
    x = (np.sin(ph) + 0.4 * np.sin(2 * ph) + 0.15 * np.sin(3 * ph)) * np.exp(-t * 2.2)
    return fade(np.tanh(x * 1.3) * 0.5, 0.004, 0.03)
def rhodes(m, dur, vel=1.0):
    t = t_(dur + 1.2); f = hz(m)
    idx = 1.6 * vel * np.exp(-t * 3.5)                   # the bark of a Rhodes tine, fading
    x = np.sin(2 * np.pi * f * t + idx * np.sin(2 * np.pi * f * t))
    x += 0.25 * np.sin(2 * np.pi * f * 4 * t) * np.exp(-t * 9)
    x *= np.exp(-t * 0.9) * (1 + 0.12 * np.sin(2 * np.pi * 4.5 * t))   # tremolo
    hold = np.ones(len(t)); c = int(dur * SR); hold[c:] = np.exp(-(t[c:] - dur) * 7)
    return fade(x * hold, 0.003, 0.05) * vel * 0.16
def bell(m, dur, vel=1.0):
    t = t_(dur + 1.5); f = hz(m)
    x = np.sin(2 * np.pi * f * t + 2.2 * np.exp(-t * 2.5) * np.sin(2 * np.pi * f * 3.5 * t))
    return fade(x * np.exp(-t * 1.8), 0.002, 0.1) * vel * 0.14
def pad(m, dur):
    t = t_(dur + 0.6); x = np.zeros(len(t))
    for det in (-0.1, 0, 0.09):
        for k in range(1, 8): x += np.sin(2 * np.pi * hz(m + det) * k * t + rng.random() * 6) * k ** -2.3
    e = np.minimum(1, t / 0.5) * np.minimum(1, np.maximum(0, (dur + 0.6 - t) / 0.6))
    return x * e * 0.035

# ---------- arranging ----------
class Beat:
    def __init__(self, bpm, bars, swing=0.5):
        self.bpm, self.bars, self.swing = bpm, bars, swing
        self.beat = 60 / bpm; self.sec = bars * 4 * self.beat + 2.5
        self.stems = {k: np.zeros((int(self.sec * SR), 2)) for k in ("drums", "bass", "keys", "melody")}
        self.sends = {k: 0.0 for k in self.stems}
    def at(self, bar, step16):                           # time of a 16th step, with swing on the off-16ths
        base = (bar * 16 + step16) * self.beat / 4
        return base + ((self.swing - 0.5) * self.beat / 2 if step16 % 2 else 0)
    def put(self, stem, x, sec, pan=0.0, vel=1.0):
        i = int(sec * SR); buf = self.stems[stem]
        if i >= len(buf): return
        x = x[: len(buf) - i] * vel * (0.92 + 0.08 * rng.random())   # small human wobble
        l, r = np.cos((pan + 1) * np.pi / 4) * 1.414, np.sin((pan + 1) * np.pi / 4) * 1.414
        buf[i:i + len(x), 0] += x * l; buf[i:i + len(x), 1] += x * r
    def render(self, name, sends, gains=None, extra=None):
        gains = gains or {}
        here = os.path.dirname(os.path.abspath(__file__)); d = os.path.join(here, "out", name); os.makedirs(d, exist_ok=True)
        n = len(self.stems["drums"]); ir_n = int(2.2 * SR); t = np.arange(ir_n) / SR
        ir = smooth(rng.normal(0, 1, ir_n), 6) * np.exp(-t / 0.55); ir[: int(0.015 * SR)] = 0; ir /= np.sqrt((ir ** 2).sum())
        L = n + ir_n; IR = np.fft.rfft(ir, L); mix = np.zeros((n, 2)); outs = {}
        for k, s in self.stems.items():
            s = s * gains.get(k, 1.0)
            if sends.get(k):
                for ch in range(2): s[:, ch] += np.fft.irfft(np.fft.rfft(s[:, ch], L) * IR, L)[:n] * sends[k] * 0.35
            outs[k] = s; mix += s
        if extra is not None: mix[: len(extra)] += extra[:n, None]
        peak = np.abs(mix).max() + 1e-9
        mix = np.tanh(mix / peak * 1.2) * 0.89 / np.tanh(1.2)
        for k, s in outs.items(): save(os.path.join(d, k + ".wav"), s / peak * 0.89)
        save(os.path.join(d, "mix.wav"), mix)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", os.path.join(d, "mix.wav"), "-b:a", "256k", os.path.join(here, "out", name + ".mp3")], check=True)
        print(name, f"{self.bpm} BPM, {self.bars} bars, {n / SR:.1f} s")

def save(p, x):
    with wave.open(p, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(x, -1, 1) * 32767).astype("<i2").tobytes())

# ---------- the three sketches ----------
def boombap(bpm=90, bars=16, name=None):
    """90s-style head-nod: 90 BPM, swung, dusty Rhodes on a minor jazz loop, upright bass, vinyl crackle. A minor."""
    b = Beat(bpm, bars, swing=0.58)
    prog = [([57, 60, 64, 67], 45), ([62, 65, 69, 72], 50), ([64, 67, 71, 74], 52), ([62, 65, 69, 72], 50)]   # Am7 Dm7 Em7 Dm7 (voicings)
    for bar in range(bars):
        ch, root = prog[bar % 4]; intro = bar < 2
        for s, v in ((0, 1), (6, 0.55), (11, 0.8)) if bar % 2 == 0 else ((0, 1), (10, 0.85)):
            if not intro: b.put("drums", kick(), b.at(bar, s), vel=v)
        if not intro:
            for s in (4, 12): b.put("drums", snare(body=200, dec=0.13), b.at(bar, s), pan=0.05)
            for s in range(0, 16, 2): b.put("drums", hat(0.03, 0.08), b.at(bar, s), pan=0.3, vel=1 if s % 4 == 0 else 0.6)
            b.put("bass", ubass(root, b.beat * 1.5), b.at(bar, 0)); b.put("bass", ubass(root + 7, b.beat * 0.9), b.at(bar, 10))
        for s, vel in ((0, 0.9), (7, 0.6)):
            for j, m in enumerate(ch): b.put("keys", rhodes(m, b.beat * (1.6 if s == 0 else 1.2), vel), b.at(bar, s) + j * 0.012, pan=-0.2 + 0.12 * j)
        if bar >= 8 and (bar // 8) % 2 == 1:                # a small answering line every other 8 bars
            for s, m in ((2, 76), (3, 74), (8, 72), (14, 69)): b.put("melody", rhodes(m, b.beat * 0.6, 0.7), b.at(bar, s), pan=0.25)
    b.render(name or f"boombap-{bpm}", sends={"keys": 0.5, "drums": 0.12, "melody": 0.6}, gains={"keys": 1.6, "melody": 2.0}, extra=vinyl(b.sec))

def trap(bpm=140, bars=24, name=None):
    """Dark trap: 140 BPM (half-time feel), sliding 808s, rolling hats, clap on 3, a cold bell melody. F# minor."""
    b = Beat(bpm, bars)
    roots = [42, 42, 38, 40]                              # F#, F#, D, E (808 notes)
    chords = [[66, 69, 73], [66, 69, 73], [62, 66, 69], [64, 68, 71]]
    tune = [(0, 78), (3, 76), (6, 73), (8, 76), (11, 73), (14, 69)]
    for bar in range(bars):
        sec = "intro" if bar < 4 else ("drop" if bar < bars - 4 else "out")
        r = roots[bar % 4]; prev = roots[(bar - 1) % 4]
        for j, m in enumerate(chords[bar % 4]): b.put("keys", pad(m, b.beat * 4), b.at(bar, 0), pan=-0.3 + 0.3 * j)
        for s, m in tune if bar % 2 == 0 else tune[:3] + [(10, 81), (12, 78)]:
            b.put("melody", bell(m, b.beat * 0.75, 0.9 if sec == "drop" else 0.6), b.at(bar, s), pan=0.2)
        if sec == "intro": continue
        for s, ln, sl in ((0, 6, prev if prev != r else None), (7, 3, None), (10, 6, r + 12 if bar % 4 == 3 else None)):
            b.put("bass", b808(r, b.beat * ln / 4, slide_from=sl), b.at(bar, s))
        for s in (0, 7, 10): b.put("drums", kick(0.7, 0.12), b.at(bar, s), vel=0.8)
        b.put("drums", clap(), b.at(bar, 8), vel=1.0); b.put("drums", snare(dec=0.08, tone=0.15), b.at(bar, 8), vel=0.5)
        s = 0
        while s < 16:                                      # hats: steady 8ths with 32nd/triplet rolls at bar ends
            if bar % 2 == 1 and s >= 12:
                for k in range(8): b.put("drums", hat(0.015, 0.09), b.at(bar, 12) + k * b.beat / 8, pan=0.35, vel=0.5 + k * 0.06)
                break
            b.put("drums", hat(0.018, 0.1), b.at(bar, s), pan=0.35, vel=1 if s % 4 == 0 else 0.7); s += 2
    b.render(name or f"trap-{bpm}", sends={"melody": 0.7, "keys": 0.6, "drums": 0.08}, gains={"bass": 0.9, "melody": 2.0, "keys": 1.8})

def rnb(bpm=75, bars=12, name=None):
    """Late-night R&B: 75 BPM, lush maj7/min9 chords, soft kick, rimshot + snaps, a sung-style lead to write over. Db major."""
    b = Beat(bpm, bars, swing=0.55)
    prog = [([61, 65, 68, 72], 37), ([60, 63, 67, 70], 36), ([58, 61, 65, 68], 34), ([63, 66, 68, 73], 39)]  # Dbmaj7 Cm7 Bbm7 Ebsus
    for bar in range(bars):
        ch, root = prog[bar % 4]; intro = bar < 2
        for j, m in enumerate(ch): b.put("keys", pad(m, b.beat * 4), b.at(bar, 0), pan=-0.35 + 0.23 * j)
        for s in (0, 6, 10):
            for j, m in enumerate(ch): b.put("keys", rhodes(m, b.beat * 0.9, 0.6), b.at(bar, s) + j * 0.02, pan=0.2)
        if intro: continue
        for s in (0, 10): b.put("drums", kick(0.4, 0.2), b.at(bar, s), vel=0.8)
        b.put("drums", rim(), b.at(bar, 4), pan=-0.1); b.put("drums", snap(), b.at(bar, 12), pan=0.2)
        for s in range(0, 16, 2): b.put("drums", hat(0.02, 0.05), b.at(bar, s), pan=0.4, vel=0.7)
        b.put("bass", b808(root, b.beat * 2.5, slide_from=root - 2 if bar % 4 == 3 else None), b.at(bar, 0), vel=0.7)
        b.put("bass", b808(root + 7, b.beat * 1), b.at(bar, 12), vel=0.5)
        if bar >= 4 and (bar // 8) % 2 == 1:
            line = [(2, 77), (4, 75), (6, 72), (12, 73)] if bar % 2 == 0 else [(0, 72), (3, 70), (8, 68)]
            for s, m in line: b.put("melody", bell(m, b.beat * 1.2, 0.55), b.at(bar, s), pan=-0.15)
    b.render(name or f"rnb-{bpm}", sends={"keys": 0.6, "melody": 0.7, "drums": 0.15}, gains={"melody": 2.6, "bass": 0.8})

STYLES = {"boombap": boombap, "trap": trap, "rnb": rnb}
# Full-length versions for the studio page (~2.5-3 min), each at three tempos so the BPM choice is a real re-render, not a pitch shift.
STUDIO = {"boombap": ([82, 90, 98], 64), "trap": ([130, 140, 150], 96), "rnb": ([68, 75, 82], 48)}
if __name__ == "__main__":
    if sys.argv[1:2] == ["--studio"]:
        for k, (bpms, bars) in STUDIO.items():
            for bpm in bpms: STYLES[k](bpm=bpm, bars=bars, name=f"studio-{k}-{bpm}")
    else:
        for k in (sys.argv[1:] or STYLES): STYLES[k]()
