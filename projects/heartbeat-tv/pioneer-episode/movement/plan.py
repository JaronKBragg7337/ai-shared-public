# Movement test choreography -> motion.json (per-frame transforms + anim sections) for build_test.py in Unreal.
# Joe: MetaHuman locomotion clips (in place). His position is SOLVED from the clips: every 1/120 s the actor moves (and pivots)
#      so the planted foot's ball stays exactly where it is on the floor - also through turns and clip blends (v2, Fable 11/15;
#      v1 used a smoothed speed profile that averaged the swinging foot in -> Joe travelled ~20% too slow and skated).
#      Turns are arcs while walking; the turning is weighted toward late stance (heel up, pivot on the ball) like a real step turn.
# Vex: no legs (the show's bust) -> he hovers on a small base: eased glides, tilt follows acceleration, slow bob, looks at Joe.
# Coordinates: three.js style (x right, z toward camera, metres) -> Unreal X = x*100, Y = z*100. Yaw 0 = facing +z (camera).
import json, math, wave, numpy as np
FPS = 24; SUB = 5; HZ = FPS * SUB        # solve at 120 Hz, key at 24
RATE = 0.82                              # clip play rate: the clip walks 1.9 m/s (brisk); 0.82 -> ~1.55 m/s, calm but not slow-motion
BL = 6 / 24; BLI = 10 / 24                   # blend seconds between walk clips / in and out of the idle (feet differ ~4 cm: read as a weight shift)
FEET = json.load(open('feet.json'))      # ball-of-foot positions per clip, component space (x = his left, y = forward, z = up), 120 Hz
LOCO = "/MetaHumanCharacter/Optional/Animation/UEFNAnimPreset/Locomotion/"
IDLE, START, LOOP, STOP = "AS_MH_Neutral_Stand_Idle_Loop", "AS_MH_Neutral_Walk_Start_F_Rfoot", "AS_MH_Neutral_Walk_Loop_F", "AS_MH_Neutral_Walk_Stop_F_Lfoot"
ARR = {n: (np.array([f['l'] for f in FEET[n]['frames']]), np.array([f['r'] for f in FEET[n]['frames']])) for n in (IDLE, START, LOOP, STOP)}
def feet_at(n, ta):
    ln = FEET[n]['len']; ta = ta % ln if 'Loop' in n else min(ta, ln)
    l, r = ARR[n]; u = ta * 120; i = min(len(l) - 2, int(u)); k = u - i
    return l[i] * (1 - k) + l[i + 1] * k, r[i] * (1 - k) + r[i + 1] * k
def pose(n, t): l, r = feet_at(n, t); return np.array([l[1], 3 * l[2], r[1], 3 * r[2]])
LLEN = FEET[LOOP]['len']; lt = np.arange(0, LLEN, 1 / 120); LP = np.array([pose(LOOP, t) for t in lt])
def match_loop(p): return float(lt[np.linalg.norm(LP - p, axis=1).argmin()])
STOP_PH = [0.925, 1.9, 2.917, 3.917]     # loop phases that match the stop clip's first frame

# ---- Joe's clip list: [clip, seq_start, anim_offset, seq_end, blend_in, blend_out, play_rate]
IRATE = 1.3                              # pass 2: the standing idle plays a bit faster (its sway is only ~2 cm) and from its liveliest stretch
F2 = json.load(open('feet2.json'))[IDLE]['frames']; _hh = np.array([f['head'] + f['hand'] for f in F2]); _mv = np.linalg.norm(np.diff(_hh, axis=0), axis=1)
def live_off(dur):                       # idle offset whose next `dur` seconds move the head + hand the most
    n = int(dur * IRATE * 120); c = np.concatenate([_mv, _mv]); best = max(range(0, 1200, 30), key=lambda i: c[i:i + n].sum()); return best / 120
secs = []
q = lambda x: round(x * FPS) / FPS      # every clip boundary sits on a whole frame, so this math and Sequencer agree exactly
def walk(t0, walk_secs, ts=1.2):
    """start at t0, walk ~walk_secs, stop at the next matched foot phase. returns (time the stop clip starts, time it ends)"""
    s3 = q(t0 + ts / RATE)
    secs.append([START, t0, 0.0, s3 + BL, BLI, BL, RATE])
    l0 = match_loop(pose(START, ts)); want = t0 + walk_secs
    s4 = q(min(s3 + (((ph - l0) % LLEN) + k * LLEN) / RATE for k in range(8) for ph in STOP_PH if s3 + (((ph - l0) % LLEN) + k * LLEN) / RATE >= want))
    secs.append([LOOP, s3, l0, s4 + BL, BL, BL, RATE])
    e = q(s4 + 1.0 / RATE) + BLI          # pass 2: the stop clip's feet are settled 1.0 s in; the idle fades in from there (v2 waited for the clip's still tail = a statue)
    secs.append([STOP, s4, 0.0, e, BL, BLI, RATE])
    return s4, e
T_A = 1.5
secs.append([IDLE, 0.0, live_off(T_A + BLI), T_A + BLI, 0, BLI, IRATE])
STOP1, e1 = walk(T_A, 5.9)               # toward camera, arc left, across, arc left, away, stop
T_B = q(e1 + 1.3)
secs.append([IDLE, e1 - BLI, live_off(T_B + 2 * BLI - e1), T_B + BLI, BLI, BLI, IRATE])
STOP2, e2 = walk(T_B, 5.9)               # start away, arc right, across with Vex (walk-and-talk), curve to camera, stop
END = q(e2 + 3.6)
secs.append([IDLE, e2 - BLI, live_off(END - e2 + BLI), END, BLI, 0, IRATE])
NF = int(round(END * FPS)); N = NF * SUB
def weight(s, t):
    a, b = s[1], s[3]
    if t < a or (t > b and s[5] > 0): return 0.0
    w = 1.0
    if s[4] > 0: w = min(w, (t - a) / s[4])
    if s[5] > 0: w = min(w, (b - t) / s[5])
    return max(0.0, min(1.0, w))
def feet_blend(t):
    tot = 0; l = np.zeros(3); r = np.zeros(3)
    for s in secs:
        w = weight(s, t)
        if w > 0:
            a, b = feet_at(s[0], s[2] + s[6] * (t - s[1])); l += w * a; r += w * b; tot += w
    return l / tot, r / tot
TS = np.arange(N + 1) / HZ
Lf = np.zeros((N + 1, 3)); Rf = np.zeros((N + 1, 3))
for i, t in enumerate(TS): Lf[i], Rf[i] = feet_blend(t)
sig = lambda x: 1 / (1 + np.exp(-np.clip(x, -30, 30)))
def planted(P):    # 0..1: ball on the floor and not swinging forward (the swinging ball passes only ~3 cm above the floor, so height alone is not enough)
    vf = np.gradient(P[:, 1]) * HZ
    return sig((2.3 - P[:, 2]) / 0.3) * sig((60 - vf) / 15)
sL, sR = planted(Lf), planted(Rf); tot = np.maximum(sL + sR, 1e-6); wL, wR = sL / tot, sR / tot
# how far behind him the planted ball is (0..1) = heel is up = the moment a real walker pivots
late = np.clip(-(wL * Lf[:, 1] + wR * Rf[:, 1]) / 40, 0, 1)
def ss(u): u = min(1, max(0, u)); return u * u * (3 - 2 * u)
# heading schedule (t0, t1, yaw0, yaw1); yaw 0 = toward camera, 90 = toward -x, 180 = away
TURNS = [(T_A + 1.8, T_A + 3.5, 0, 90), (T_A + 3.9, T_A + 5.6, 90, 180), (T_B + 0.5, T_B + 2.3, 180, 270), (STOP2 - 3.5, STOP2 - 0.3, 270, 360)]   # pass 2: the last turn is one long easy arc toward camera
yaw = np.zeros(N + 1)
for a, b, y0, y1 in TURNS:
    m = (TS >= a) & (TS <= b); u = (TS[m] - a) / (b - a)
    rate = 6 * u * (1 - u) * (0.55 + 0.9 * np.convolve(late, np.ones(13) / 13, mode='same')[m])   # smooth bell x step-pivot weighting
    c = np.cumsum(rate); c = c / c[-1]
    yaw[m] = y0 + (y1 - y0) * c; yaw[TS > b] = y1
pos = np.zeros((N + 1, 2)); pos[0] = (120.0, 260.0)
def off(P, i):     # world offset of a foot from the actor origin (Unreal yaw: x' = x cos - y sin, y' = x sin + y cos)
    a = math.radians(yaw[i]); return np.array([P[i, 0] * math.cos(a) - P[i, 1] * math.sin(a), P[i, 0] * math.sin(a) + P[i, 1] * math.cos(a)])
for i in range(1, N + 1):
    pos[i] = pos[i - 1] + wL[i] * (off(Lf, i - 1) - off(Lf, i)) + wR[i] * (off(Rf, i - 1) - off(Rf, i))
# report: how much does a planted foot still move on the floor?
slip = []
for i in range(1, N + 1):
    for P, s in ((Lf, sL), (Rf, sR)):
        if s[i] > 0.9 and s[i - 1] > 0.9: slip.append((np.linalg.norm((pos[i] + off(P, i)) - (pos[i - 1] + off(P, i - 1))) * HZ, TS[i]))
slip = np.array(slip); spd = np.linalg.norm(np.gradient(pos, axis=0), axis=1) * HZ
print("planted-foot slip cm/s: mean %.2f  p95 %.2f  max %.1f at t=%.2f ; walk speed %.0f cm/s" % (slip[:, 0].mean(), np.percentile(slip[:, 0], 95), slip[:, 0].max(), slip[slip[:, 0].argmax(), 1], np.percentile(spd, 90)))
joe = [[round(pos[f * SUB, 0], 2), round(pos[f * SUB, 1], 2), round(yaw[f * SUB], 3)] for f in range(NF)]
J = np.array(joe)
print("Joe frames", NF, "secs %.1f" % END, "x %.2f..%.2f z %.2f..%.2f" % (J[:, 0].min() / 100, J[:, 0].max() / 100, J[:, 1].min() / 100, J[:, 1].max() / 100))
for s in secs: print("  %-34s %6.2f-%6.2f off %.3f" % (s[0], s[1], s[3], s[2]))
for t in [T_A, TURNS[0][0], TURNS[0][1], TURNS[1][0], TURNS[1][1], STOP1, e1, T_B, TURNS[2][1], TURNS[3][0], STOP2, e2]: print("   t %5.2f  joe %5.2f %5.2f yaw %4.0f" % (t, *(J[int(t * FPS)][:2] / 100), J[int(t * FPS)][2]))
WT0 = TURNS[2][1] - 0.9; WT1 = STOP2 + 0.6     # walk-and-talk window

# ---- Vex
def gauss(a, sigma_s):
    n = int(sigma_s * FPS * 3); k = np.exp(-0.5 * (np.arange(-n, n + 1) / (sigma_s * FPS)) ** 2); k /= k.sum()
    return np.stack([np.convolve(np.pad(a[:, c], n, mode='edge'), k, mode='valid') for c in range(a.shape[1])], axis=1)
Jm = J[:, :2] / 100; Jr = np.radians(J[:, 2])
HOME = np.array([-0.9, 2.2]); WATCH = np.array([1.7, 2.9])
G0, G1 = T_A + 1.2, T_A + 4.6            # glide from his start spot to a place where he can watch Joe walk
E0, E1 = T_B - 0.8, T_B + 3.0            # joins Joe: far side of him from the camera and half a step ahead (so both stay in view)
V = np.zeros((NF, 2))
for f in range(NF):
    t = f / FPS; p = HOME + (WATCH - HOME) * ss((t - G0) / (G1 - G0))
    lead = 0.8 - 0.8 * ss((t - TURNS[3][0] - 0.9) / 2.6); side = 0.78     # (the spring below trails ~0.35 m at walking speed) drops back level on the last turn
    esc = Jm[f] + side * np.array([math.cos(Jr[f]), math.sin(Jr[f])]) + lead * np.array([-math.sin(Jr[f]), math.cos(Jr[f])])
    k = ss((t - E0) / (E1 - E0)); V[f] = p + (esc - p) * k
V = gauss(V, 0.22)
# pass 2: he follows that path on a soft spring, so he eases off, drifts a touch past his stopping point and settles instead of stopping dead
sx = V[0].copy(); sv = np.zeros(2); W0, ZETA = 5.5, 0.6; Vs = np.zeros_like(V)
for f in range(NF):
    for _ in range(SUB): sv += (W0 * W0 * (V[f] - sx) - 2 * ZETA * W0 * sv) / HZ; sx = sx + sv / HZ
    Vs[f] = sx
V = Vs
vel = np.gradient(V, axis=0) * FPS; acc = gauss(np.gradient(vel, axis=0) * FPS, 0.12); sp = np.linalg.norm(vel, axis=1)
vy = 0.0; vyaw = np.zeros(NF); yr = 0.0
for f in range(NF):
    t = f / FPS; to_joe = math.degrees(math.atan2(-(Jm[f, 0] - V[f, 0]), Jm[f, 1] - V[f, 1]))
    if sp[f] > 0.35:
        want = math.degrees(math.atan2(-vel[f, 0], vel[f, 1]))
        if t > E0 + 0.8: want += 0.45 * ((to_joe - want + 180) % 360 - 180)      # walk-and-talk: turned part-way to Joe
    elif t < G0: want = 0.0
    elif t > STOP2: want = 0.5 * ((to_joe + 180) % 360 - 180)                    # at the end: half to Joe, half to camera
    else: want = to_joe                                                         # hovering: watches Joe
    d = (want - vy + 180) % 360 - 180
    yr += (max(-110, min(110, d * 3.0)) - yr) * 0.2; vy += yr / FPS; vyaw[f] = vy     # eased, max 110 deg/s
tilt = gauss(np.clip(3.0 * acc + 1.6 * vel, -8, 8), 0.15)                       # degrees, world x/z: leans the way he accelerates (+ a little into his speed)
vex = []
for f in range(NF):
    t = f / FPS; a = math.radians(vyaw[f])
    roll = tilt[f, 0] * -math.sin(a) + tilt[f, 1] * math.cos(a)                 # Unreal roll > 0 tips his top toward his forward (+Y local)
    pitch = -(tilt[f, 0] * math.cos(a) + tilt[f, 1] * math.sin(a))              # Unreal pitch > 0 tips his top toward local -X
    bob = 2.6 * math.sin(2 * math.pi * 0.42 * t) + 0.6 * math.sin(2 * math.pi * 0.95 * t + 1)
    vex.append([round(V[f, 0] * 100, 2), round(V[f, 1] * 100, 2), round(27 + bob, 2), round(roll, 3), round(pitch, 3), round(vyaw[f], 3)])
dmin = np.linalg.norm(Jm - V, axis=1); print("Vex x %.2f..%.2f z %.2f..%.2f ; closest to Joe %.2f m at %.1fs ; top speed %.2f m/s at %.1fs, max tilt %.1f deg" % (V[:, 0].min(), V[:, 0].max(), V[:, 1].min(), V[:, 1].max(), dmin.min(), dmin.argmin() / FPS, sp.max(), sp.argmax() / FPS, np.abs(tilt).max()))

def wav_len(p): w = wave.open(p); return w.getnframes() / w.getframerate()
A = 'C:/Users/lilli/AI-Shared/projects/heartbeat-tv/pioneer-episode/movement/audio/'
vex_t = E0 + 0.1; vl = wav_len(A + '00_00_vex.wav'); joe_t = vex_t + vl - 0.35;   # pass 2: Vex speaks as he comes over and they set off; Joe answers while still walking
jl = wav_len(A + '00_01_joe.wav')
lines = [{"who": "vex", "file": A + "00_00_vex.wav", "start": int(round(vex_t * FPS))}, {"who": "joe", "file": A + "00_01_joe.wav", "start": int(round(joe_t * FPS))}]
print("walk-and-talk %.1f-%.1f, vex line %.1f (%.1fs), joe line %.1f-%.1f, end %.1f" % (WT0, WT1, vex_t, vl, joe_t, joe_t + jl, END))
# ONE camera, one take (pass 2: the v2 cuts jumped distance and hid Vex's move): locked wide for the first walk, then it travels in to
# follow the pair as the second walk starts, and moves closer for Joe's line so his mouth can be read.
mid = gauss((Jm * 0.6 + V * 0.4) * 100, 0.45); cam = []
for f in range(NF):
    t = f / FPS; k1 = ss((t - (T_B - 0.3)) / 3.2); k2 = ss((t - (joe_t - 1.4)) / 2.8); m = mid[f]
    tp = np.array([m[0] + 150 - 60 * k2, m[1] + 455 - 175 * k2, 138 + 12 * k2]); ta = np.array([m[0], m[1], 98 + 27 * k2])
    p = np.array([10.0, 1120.0, 175.0]) * (1 - k1) + tp * k1; a = np.array([10.0, 380.0, 95.0]) * (1 - k1) + ta * k1
    cam.append([round(float(v), 2) for v in list(p) + list(a)])
# foot checks: the same take seen from low static cameras (rendered separately, appended to the video as labelled replays)
ax0, ax1 = TURNS[0][1] - 0.8, TURNS[1][0] + 0.9; am = (Jm[int(ax0 * FPS)] + Jm[int(ax1 * FPS)]) / 2 * 100; je = Jm[min(NF - 1, int(e2 * FPS))] * 100
checks = [{"label": "FOOT CHECK - same take, low camera (walking + turns)", "pos": [am[0], am[1] + 345, 42], "aim": [am[0], am[1], 70], "t0": ax0, "t1": ax1},
          {"label": "FOOT CHECK - same take, low camera (the last stop)", "pos": [je[0] - 245, je[1] + 45, 40], "aim": [je[0] - 5, je[1] - 55, 55], "t0": STOP2 - 1.1, "t1": e2 + 0.7}]
for c in checks: c["f0"] = int(c["t0"] * FPS); c["f1"] = int(c["t1"] * FPS); c["pos"] = [round(float(v), 1) for v in c["pos"]]; c["aim"] = [round(float(v), 1) for v in c["aim"]]
json.dump({"fps": FPS, "frames": NF, "rate": RATE, "loco": LOCO,
           "joe_sections": [{"anim": s[0], "start": s[1], "end": s[3], "offset": s[2], "blend_in": s[4], "blend_out": s[5], "rate": s[6]} for s in secs],
           "joe": joe, "vex": vex, "cam": cam, "lines": lines, "walktalk": [WT0, WT1], "footchecks": checks,
           "turns": TURNS, "stops": [STOP1, e1, STOP2, e2], "starts": [T_A, T_B]}, open('motion.json', 'w'))
if __name__ == '__main__' and __import__('os').environ.get('SLIPDBG'):
    cur = None
    for v, t in slip:
        if v > 4:
            if cur and t - cur[1] < 0.1: cur[1] = t; cur[2] = max(cur[2], v); cur[3] += v / HZ
            else:
                if cur: print("  slip %.2f-%.2f max %.0f cm/s total %.1f cm" % tuple(cur))
                cur = [t, t, v, v / HZ]
    if cur: print("  slip %.2f-%.2f max %.0f cm/s total %.1f cm" % tuple(cur))
