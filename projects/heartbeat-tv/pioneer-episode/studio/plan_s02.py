# Pioneer episode s02 (walk-and-talk to the live truck) -> motion_s02.json for build_studio.py.
# Same machinery as movement/plan.py (approved movement test): Joe's position is solved from the clips so the planted foot stays put;
# Vex hovers beside him on a soft spring. Line timings come from timeline.json (the clock) and are not changed here.
import json, math, os, numpy as np
MV = os.path.dirname(os.path.abspath(__file__)) + '/../movement/'
FPS = 24; SUB = 5; HZ = FPS * SUB        # solve at 120 Hz, key at 24
RATE = 0.82                              # clip play rate: the clip walks 1.9 m/s (brisk); 0.82 -> ~1.55 m/s, calm but not slow-motion
BL = 6 / 24; BLI = 10 / 24                   # blend seconds between walk clips / in and out of the idle (feet differ ~4 cm: read as a weight shift)
FEET = json.load(open(MV + 'feet.json'))      # ball-of-foot positions per clip, component space (x = his left, y = forward, z = up), 120 Hz
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


# ---- the clock
TL = json.load(open(MV + '../timeline.json', encoding='utf-8')); SC = next(s for s in TL['scenes'] if s['id'] == 's02')
NF = SC['f1'] - SC['f0']; END = NF / FPS; N = NF * SUB
LINES = [{"who": l["who"], "file": l["file"], "start": l["f0"] - SC["f0"], "frames": l["frames"]} for l in SC["lines"]]

# ---- Joe's clip list: [clip, seq_start, anim_offset, seq_end, blend_in, blend_out, play_rate]
IRATE = 1.3
F2 = json.load(open(MV + 'feet2.json'))[IDLE]['frames']; _hh = np.array([f['head'] + f['hand'] for f in F2]); _mv = np.linalg.norm(np.diff(_hh, axis=0), axis=1)
def live_off(dur):
    n = int(dur * IRATE * 120); c = np.concatenate([_mv, _mv]); best = max(range(0, 1200, 30), key=lambda i: c[i:i + n].sum()); return best / 120
secs = []
q = lambda x: round(x * FPS) / FPS
def walk(t0, walk_secs, ts=1.2):
    s3 = q(t0 + ts / RATE)
    secs.append([START, t0, 0.0, s3 + BL, BLI, BL, RATE])
    l0 = match_loop(pose(START, ts)); want = t0 + walk_secs
    s4 = q(min(s3 + (((ph - l0) % LLEN) + k * LLEN) / RATE for k in range(12) for ph in STOP_PH if s3 + (((ph - l0) % LLEN) + k * LLEN) / RATE >= want))
    secs.append([LOOP, s3, l0, s4 + BL, BL, BL, RATE])
    e = q(s4 + 1.0 / RATE) + BLI
    secs.append([STOP, s4, 0.0, e, BL, BLI, RATE])
    return s4, e
T_A = q(1.0)                              # Vex: "Our ride is in the parking lot." -> Joe sets off
secs.append([IDLE, 0.0, live_off(T_A + BLI), T_A + BLI, 0, BLI, IRATE])
STOP1, e1 = walk(T_A, 4.6)               # toward camera, long easy arc to stage left, stops by the rocket (he is finishing "...send stories home")
T_B = q(10.3)                             # sets off again during Vex's "...that makes it a spacecraft"
secs.append([IDLE, e1 - BLI, live_off(T_B + 2 * BLI - e1), T_B + BLI, BLI, BLI, IRATE])
STOP2, e2 = walk(T_B, 3.4)               # along the van to the cab door ("...the coffee machine was fixed"), stop
secs.append([IDLE, e2 - BLI, live_off(END - e2 + BLI), END, BLI, 0, IRATE])
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
def planted(P):
    vf = np.gradient(P[:, 1]) * HZ
    return sig((2.3 - P[:, 2]) / 0.3) * sig((60 - vf) / 15)
sL, sR = planted(Lf), planted(Rf); tot = np.maximum(sL + sR, 1e-6); wL, wR = sL / tot, sR / tot
late = np.clip(-(wL * Lf[:, 1] + wR * Rf[:, 1]) / 40, 0, 1)
def ss(u): u = min(1, max(0, u)); return u * u * (3 - 2 * u)
TURNS = [(T_A + 1.1, T_A + 3.9, 0, 90)]  # yaw 0 = toward camera, 90 = toward -x (stage left, where the truck is)
yaw = np.zeros(N + 1)
for a, b, y0, y1 in TURNS:
    m = (TS >= a) & (TS <= b); u = (TS[m] - a) / (b - a)
    rate = 6 * u * (1 - u) * (0.55 + 0.9 * np.convolve(late, np.ones(13) / 13, mode='same')[m])
    c = np.cumsum(rate); c = c / c[-1]
    yaw[m] = y0 + (y1 - y0) * c; yaw[TS > b] = y1
pos = np.zeros((N + 1, 2)); pos[0] = (200.0, 150.0)
def off(P, i):
    a = math.radians(yaw[i]); return np.array([P[i, 0] * math.cos(a) - P[i, 1] * math.sin(a), P[i, 0] * math.sin(a) + P[i, 1] * math.cos(a)])
for i in range(1, N + 1):
    pos[i] = pos[i - 1] + wL[i] * (off(Lf, i - 1) - off(Lf, i)) + wR[i] * (off(Rf, i - 1) - off(Rf, i))
slip = []
for i in range(1, N + 1):
    for P, s in ((Lf, sL), (Rf, sR)):
        if s[i] > 0.9 and s[i - 1] > 0.9: slip.append(np.linalg.norm((pos[i] + off(P, i)) - (pos[i - 1] + off(P, i - 1))) * HZ)
slip = np.array(slip)
joe = [[round(pos[f * SUB, 0], 2), round(pos[f * SUB, 1], 2), round(yaw[f * SUB], 3)] for f in range(NF)]
J = np.array(joe); Jm = J[:, :2] / 100; Jr = np.radians(J[:, 2])
print("s02: %d frames %.2f s ; planted-foot slip mean %.2f p95 %.2f cm/s ; Joe x %.2f..%.2f z %.2f..%.2f" % (NF, END, slip.mean(), np.percentile(slip, 95), Jm[:, 0].min(), Jm[:, 0].max(), Jm[:, 1].min(), Jm[:, 1].max()))
for s in secs: print("  %-34s %6.2f-%6.2f off %.3f" % (s[0], s[1], s[3], s[2]))
for t in [T_A, TURNS[0][1], STOP1, e1, T_B, STOP2, e2, END - 0.05]: print("   t %5.2f  joe %5.2f %5.2f yaw %4.0f" % (t, *Jm[int(t * FPS)], J[int(t * FPS)][2]))

# ---- Vex: on Joe's right (the far side from the camera once they head for the truck), a little ahead while moving
def gauss(a, sigma_s):
    n = int(sigma_s * FPS * 3); k = np.exp(-0.5 * (np.arange(-n, n + 1) / (sigma_s * FPS)) ** 2); k /= k.sum()
    return np.stack([np.convolve(np.pad(a[:, c], n, mode='edge'), k, mode='valid') for c in range(a.shape[1])], axis=1)
jsp = np.linalg.norm(np.gradient(Jm, axis=0), axis=1) * FPS
lead = gauss((0.55 + 0.35 * np.clip(jsp / 1.4, 0, 1))[:, None], 0.45)[:, 0]; SIDE = 0.80
V = np.array([Jm[f] - SIDE * np.array([math.cos(Jr[f]), math.sin(Jr[f])]) + lead[f] * np.array([-math.sin(Jr[f]), math.cos(Jr[f])]) for f in range(NF)])
V = gauss(V, 0.22)
sx = V[0].copy(); sv = np.zeros(2); W0, ZETA = 5.5, 0.6; Vs = np.zeros_like(V)
for f in range(NF):
    for _ in range(SUB): sv += (W0 * W0 * (V[f] - sx) - 2 * ZETA * W0 * sv) / HZ; sx = sx + sv / HZ
    Vs[f] = sx
V = Vs
vel = np.gradient(V, axis=0) * FPS; acc = gauss(np.gradient(vel, axis=0) * FPS, 0.12); sp = np.linalg.norm(vel, axis=1)
vy = 20.0; vyaw = np.zeros(NF); yr = 0.0
for f in range(NF):
    to_joe = math.degrees(math.atan2(-(Jm[f, 0] - V[f, 0]), Jm[f, 1] - V[f, 1]))
    base = math.degrees(math.atan2(-vel[f, 0], vel[f, 1])) if sp[f] > 0.35 else J[f, 2]
    want = base + 0.45 * ((to_joe - base + 180) % 360 - 180)      # turned part-way to Joe, always
    d = (want - vy + 180) % 360 - 180
    yr += (max(-110, min(110, d * 3.0)) - yr) * 0.2; vy += yr / FPS; vyaw[f] = vy
tilt = gauss(np.clip(3.0 * acc + 1.6 * vel, -8, 8), 0.15)
vex = []
for f in range(NF):
    t = f / FPS; a = math.radians(vyaw[f])
    roll = tilt[f, 0] * -math.sin(a) + tilt[f, 1] * math.cos(a); pitch = -(tilt[f, 0] * math.cos(a) + tilt[f, 1] * math.sin(a))
    bob = 2.6 * math.sin(2 * math.pi * 0.42 * t) + 0.6 * math.sin(2 * math.pi * 0.95 * t + 1)
    vex.append([round(V[f, 0] * 100, 2), round(V[f, 1] * 100, 2), round(27 + bob, 2), round(roll, 3), round(pitch, 3), round(vyaw[f], 3)])
dmin = np.linalg.norm(Jm - V, axis=1)
print("Vex x %.2f..%.2f z %.2f..%.2f ; closest to Joe %.2f m ; top speed %.2f m/s ; max tilt %.1f deg" % (V[:, 0].min(), V[:, 0].max(), V[:, 1].min(), V[:, 1].max(), dmin.min(), sp.max(), np.abs(tilt).max()))

# ---- the truck: parked along the far side of their path, rear (with the rocket) toward the desk; they end at the cab door
jend = Jm[-1]; vmin_z = V[int(TURNS[0][1] * FPS):, 1].min()
VAN = {"door_x": float(jend[0]) - 0.35, "near_z": float(vmin_z) - 0.62}   # near_z = the truck's camera-side face
VAN["rear_x"] = VAN["door_x"] + 3.55; VAN["len"] = 5.0; VAN["width"] = 2.05
print("van: rear x %.2f, nose x %.2f, near face z %.2f ; Joe stop 1 at x %.2f" % (VAN["rear_x"], VAN["rear_x"] - VAN["len"], VAN["near_z"], Jm[int(e1 * FPS)][0]))

# ---- one camera, one take: two-shot in front of the desk, follows them across, eases wider at the truck
mid = gauss((Jm * 0.6 + V * 0.4) * 100, 0.45); cam = []
for f in range(NF):
    t = f / FPS; k1 = ss((t - TURNS[0][0]) / 3.5); k2 = ss((t - (T_B + 0.6)) / 4.0); m = mid[f]
    p = [m[0] - 110 * k1 + 170 * k2, m[1] + 430 + 70 * k1 + 20 * k2, 150]; a = [m[0] - 60 * k1 + 150 * k2, m[1], 118 + 12 * k2]
    cam.append([round(float(v), 2) for v in p + a])
json.dump({"fps": FPS, "frames": NF, "rate": RATE, "loco": LOCO,
           "joe_sections": [{"anim": s[0], "start": s[1], "end": s[3], "offset": s[2], "blend_in": s[4], "blend_out": s[5], "rate": s[6]} for s in secs],
           "joe": joe, "vex": vex, "cam": cam, "lines": LINES, "van": VAN}, open(os.path.dirname(os.path.abspath(__file__)) + '/motion_s02.json', 'w'))
