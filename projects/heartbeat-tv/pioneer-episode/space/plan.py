# Shot plan for the space + truck scenes: every moving thing, every frame, every camera -> plan.json (read by build.py in
# Unreal and by overlay.py for labels). Units: Unreal cm, degrees. Pioneer sits at the origin in the space scenes.
import json, math, numpy as np
from geom import *
HERE = __file__.replace("\\", "/").rsplit("/", 1)[0]
TL = json.load(open(HERE + "/../timeline.json", encoding="utf-8"))
SC = {s["id"]: s for s in TL["scenes"]}
FPS = 24
PARK = [0.0, 0.0, -4.0e7]
G = np.array([0.0, 0.0, -3.0e6])          # the parking lot (liftoff) site
H0 = np.array([0.0, 300000.0, 0.0])       # the false-colour heat-view copy of Pioneer
SPIN = 3.0                                 # deg/s about the dish axis (real Pioneer ~4.8 rpm; slowed for the eye)

def nrm(v): v = np.asarray(v, float); return v / max(np.linalg.norm(v), 1e-12)
def smooth(t): t = min(1.0, max(0.0, t)); return t * t * t * (t * (6 * t - 15) + 10)
def ease(t): t = min(1.0, max(0.0, t)); return t * t * (3 - 2 * t)
def lerp(a, b, t): return np.asarray(a, float) + (np.asarray(b, float) - np.asarray(a, float)) * t
def ramp(f, a, b): return smooth((f - a) / max(1e-9, b - a))

def catmull(P, u):
    """centripetal-ish uniform Catmull-Rom through points P, u in [0,1] over the whole path"""
    P = [np.asarray(p, float) for p in P]
    if len(P) == 1: return P[0]
    if len(P) == 2: return lerp(P[0], P[1], u)
    n = len(P) - 1; x = min(n - 1e-9, max(0.0, u * n)); i = int(x); t = x - i
    p0 = P[max(0, i - 1)]; p1 = P[i]; p2 = P[i + 1]; p3 = P[min(n, i + 2)]
    if i == 0: p0 = 2 * p1 - p2
    if i + 1 == n: p3 = 2 * p2 - p1
    return 0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3)

def keyed(keys, f):
    """keys: [(frame, vec)]: smooth (C1) through the keys with ease at the first/last key, times honoured"""
    fr = [k[0] for k in keys]; P = [np.asarray(k[1], float) for k in keys]
    if f <= fr[0]: return P[0]
    if f >= fr[-1]: return P[-1]
    i = max(j for j in range(len(fr) - 1) if fr[j] <= f); t = (f - fr[i]) / (fr[i + 1] - fr[i])
    # Hermite with Catmull-Rom tangents (zero tangent at the ends -> ease in/out)
    def tan(j):
        if j == 0 or j == len(P) - 1: return np.zeros_like(P[j])
        return (P[j + 1] - P[j - 1]) / (fr[j + 1] - fr[j - 1]) * (fr[i + 1] - fr[i])
    m0, m1 = tan(i), tan(i + 1); h = (2 * t ** 3 - 3 * t * t + 1, t ** 3 - 2 * t * t + t, -2 * t ** 3 + 3 * t * t, t ** 3 - t * t)
    return h[0] * P[i] + h[1] * m0 + h[2] * P[i + 1] + h[3] * m1

def rot_from_axes(X, Y, Z):
    pitch = math.degrees(math.asin(max(-1, min(1, X[2])))); yaw = math.degrees(math.atan2(X[1], X[0])); roll = math.degrees(math.atan2(-Y[2], Z[2]))
    return [roll, pitch, yaw]
def axes_from_rot(r):
    roll, pitch, yaw = [math.radians(a) for a in r]; CR, SR, CP, SP, CY, SY = math.cos(roll), math.sin(roll), math.cos(pitch), math.sin(pitch), math.cos(yaw), math.sin(yaw)
    X = np.array([CP * CY, CP * SY, SP]); Y = np.array([SR * SP * CY - CR * SY, SR * SP * SY + CR * CY, -SR * CP]); Z = np.array([-(CR * SP * CY + SR * SY), CY * SR - CR * SP * SY, CR * CP])
    return X, Y, Z
def frame_axes(fwd, up=(0, 0, 1)):
    X = nrm(fwd); Y = nrm(np.cross(np.asarray(up, float), X)); Z = np.cross(X, Y); return X, Y, Z
def look(pos, tgt, up=(0, 0, 1), roll=0.0):
    X, Y, Z = frame_axes(np.asarray(tgt, float) - np.asarray(pos, float), up)
    if roll:
        a = math.radians(roll); Y, Z = Y * math.cos(a) + Z * math.sin(a), -Y * math.sin(a) + Z * math.cos(a)
    return rot_from_axes(X, Y, Z)
def spun(fwd, spin_deg, up=(0, 0, 1)):
    X, Y, Z = frame_axes(fwd, up); a = math.radians(spin_deg)
    return X, Y * math.cos(a) + Z * math.sin(a), -Y * math.sin(a) + Z * math.cos(a)
def apply(pos, axes, p):
    X, Y, Z = axes; p = np.asarray(p, float); return np.asarray(pos, float) + X * p[0] + Y * p[1] + Z * p[2]
def wobble(f, seed, freqs=(0.37, 0.83, 1.71)):
    r = np.random.default_rng(seed); ph = r.uniform(0, 2 * math.pi, len(freqs))
    return sum(math.sin(2 * math.pi * fr * f / FPS + p) / (i + 1) for i, (fr, p) in enumerate(zip(freqs, ph))) / 1.83

S_DEF = nrm([1.0, 0.0, 0.12])
E_DEF = nrm(S_DEF + np.array([0.0, 0.042, -0.012]))   # Earth ~2.5 deg from the Sun as seen from ~20+ AU (illustration)

class Scene:
    def __init__(s, sid):
        s.id = sid; sc = SC[sid]; s.f0 = sc["f0"]; s.N = sc["f1"] - sc["f0"]; s.tracks = {}; s.cams = []; s.cuts = []; s.mpc = {}; s.labels = []
        s.lines = [(l["f0"] - s.f0, l["frames"], l["text"]) for l in sc["lines"]]
    def row(s, name, f, pos, rot=(0, 0, 0), scale=(1, 1, 1)):
        s.tracks.setdefault(name, [None] * s.N)[f] = [float(v) for v in (*pos, *rot, *(scale if hasattr(scale, "__len__") else (scale,) * 3))]
    def const(s, name, pos, rot=(0, 0, 0), scale=(1, 1, 1)):
        for f in range(s.N): s.row(name, f, pos, rot, scale)
    def cam(s, name, f0, f1, lens, fn, fstop=16.0, focus=1000.0):
        rows = []
        for f in range(f0, f1):
            pos, rot = fn(f); rows.append([float(v) for v in (*pos, *rot)])
        s.cams.append({"name": name, "f0": f0, "f1": f1, "lens": lens, "fstop": fstop, "focus": focus, "rows": rows})
        if f0 > 0: s.cuts.append(f0)
    def key(s, param, f, v): s.mpc.setdefault(param, []).append([int(f), float(v)])
    def label(s, text, a, b, anchor=None, at=None, offset=(0, 0), kind="tag"):
        """anchor: function f -> world point (leader line), at: fixed screen (x, y) fraction"""
        s.labels.append({"text": text, "a": a, "b": b, "kind": kind, "offset": list(offset), "at": at,
                         "pts": None if anchor is None else [[float(v) for v in anchor(f)] for f in range(s.N)]})
    def sky(s, S=S_DEF, E=E_DEF, center=(0, 0, 0), earth=True, sun_d=4.5e6):
        c = np.asarray(center, float)
        s.const("Sun", c + S * sun_d, rot_from_axes(*frame_axes(S)), (sun_d / 4.5e6 * 300,) * 3)
        if earth: s.const("Earth", c + E * sun_d * 0.98, rot_from_axes(*frame_axes(E)), (sun_d / 4.5e6 * 80,) * 3)
        s.const("SunLight", (0, 0, 1000), rot_from_axes(*frame_axes(-S)))
        fill = nrm(0.55 * S + np.array([0.15, 0.55, -0.75]))
        s.const("FillLight", (0, 0, 1000), rot_from_axes(*frame_axes(fill)))
        s.S, s.E = S, E
    def out(s):
        return {"id": s.id, "f0": s.f0, "frames": s.N, "tracks": s.tracks, "cams": s.cams, "cuts": s.cuts, "mpc": s.mpc, "labels": s.labels, "lines": s.lines}

def pioneer_axes(E, spin): return spun(E, spin)
def pio_world(axes, p, local_pt, pos=(0, 0, 0)): return apply(pos, axes, local_pt)

def put_pioneer(s, name, f, pos, E, spin):
    ax = pioneer_axes(E, spin); s.row(name, f, pos, rot_from_axes(*ax)); return ax

def truck_parts(s, f, pos, axes, E_home, flame=0.0, dish_target=None, seed=0):
    """truck body + roof dish (aimed at E_home, or at a world point) + optional flame"""
    s.row("Truck", f, pos, rot_from_axes(*axes))
    piv = apply(pos, axes, TRK_ROOFDISH_PIVOT)
    aim = nrm(np.asarray(dish_target, float) - piv) if dish_target is not None else E_home
    s.row("RoofDish", f, piv, rot_from_axes(*frame_axes(aim, axes[2])))
    if flame > 0.01:
        noz = apply(pos, axes, TRK_NOZZLE); fl = flame * (1 + 0.10 * wobble(f, 11 + seed, (3.1, 7.3, 11.9))); fw = flame ** 0.5 * (1 + 0.05 * wobble(f, 12 + seed, (5.3, 9.1)))
        rr = rot_from_axes(*axes)
        s.row("Flame", f, noz, rr, (fl, fw, fw)); s.row("FlameCore", f, noz, rr, (fl * 1.05, fw, fw))
        s.row("FlameLight", f, apply(pos, axes, (TRK_NOZZLE[0] - 120, 0, TRK_NOZZLE[2])))
    else:
        for n in ("Flame", "FlameCore", "FlameLight"): s.row(n, f, PARK, (0, 0, 0), (0.001,) * 3)

def fill_park(s, names):
    for n in names:
        if n not in s.tracks: s.const(n, PARK, (0, 0, 0), (0.001,) * 3)
        else:
            tr = s.tracks[n]
            for i in range(s.N):
                if tr[i] is None: tr[i] = PARK + [0, 0, 0, 0.001, 0.001, 0.001]

ALL = ["Pioneer", "PioneerHeat", "Truck", "RoofDish", "Cab", "Ground", "Sky", "Sun", "Earth", "Flame", "FlameCore", "FlameLight",
       "Cup", "Blob", "Paper", "Ball", "BigArrow", "PlaqueLight", "CabLight", "SunLight", "FillLight"] + \
      ["Ring%d" % i for i in range(7)] + ["Arrow%d" % i for i in range(44)] + ["Smoke%d" % i for i in range(10)]
TRUCK_BESIDE = np.array([-80.0, 760.0, -40.0])
yaw_axes = lambda yaw, pitch=0.0, roll=0.0: axes_from_rot([roll, pitch, yaw])

# ======================================================================= s04: the truck glides up beside Pioneer
def s04():
    s = Scene("s04"); s.sky(); N = s.N; spin0 = 20.0
    start, end = np.array([5600.0, 2100.0, 420.0]), TRUCK_BESIDE
    for f in range(N):
        ax = put_pioneer(s, "Pioneer", f, (0, 0, 0), s.E, spin0 + SPIN * f / FPS)
        t = ramp(f, 0, 360); p = lerp(start, end, 1 - (1 - min(1, f / 360)) ** 2.4)    # glide in, decelerating
        yaw = 180 + 12 * (1 - t); roll = 4 * math.sin(f / 40) * (1 - t) + 0.6 * wobble(f, 3)
        truck_parts(s, f, p + np.array([0, 0, 6 * wobble(f, 4)]), yaw_axes(yaw, 0.8 * wobble(f, 5), roll), s.E)
    K = [(0, ((-1450, -700, 120), (400, 150, -170))), (380, ((-1060, -820, 120), (150, 300, -160))),
         (560, ((160, -1180, 130), (-40, 380, -150))), (685, ((620, -1060, 140), (-60, 400, -140)))]
    def cam(f):
        pos = keyed([(k, v[0]) for k, v in K], f); tgt = keyed([(k, v[1]) for k, v in K], f); return pos, look(pos, tgt)
    s.cam("Cam_s04", 0, N, 30, cam)
    return s

# ======================================================================= s05: slow orbit + labels, RTG heat glow, radio ripple
def s05():
    s = Scene("s05"); s.sky(); N = s.N
    truck_at = np.array([-400.0, 2900.0, -260.0])
    C = np.array([-30.0, 0, -40.0])
    def campos(f):
        u = smooth(f / (N - 1)); az = math.radians(-12 - 170 * u)
        R = 1080 + 380 * ramp(f, 800, 1000); el = math.radians(13 - 3 * ramp(f, 820, 1000))
        pos = C + R * np.array([math.cos(el) * math.cos(az), math.cos(el) * math.sin(az), math.sin(el)])
        tgt = C + np.array([0, 0, -95]) + s.S * 3000 * ramp(f, 830, 1010)
        return pos, tgt
    # pick the spin phase so the plaque faces the camera around frame 800
    best = None
    for k in range(0, 360, 2):
        ax = pioneer_axes(s.E, k + SPIN * 800 / FPS); n = ax[1] * math.cos(math.radians(PLAQUE_PHI)) + ax[2] * math.sin(math.radians(PLAQUE_PHI))
        pos, _ = campos(800); sc = np.dot(n, nrm(pos - apply((0, 0, 0), ax, PLAQUE_C)))
        if best is None or sc > best[0]: best = (sc, k)
    spin0 = best[1]; s.spin0 = spin0
    AX = []
    for f in range(N):
        AX.append(put_pioneer(s, "Pioneer", f, (0, 0, 0), s.E, spin0 + SPIN * f / FPS))
        truck_parts(s, f, truck_at + np.array([0, 0, 5 * wobble(f, 8)]), yaw_axes(180, 0, 0.5 * wobble(f, 9)), s.E)
    s.cam("Cam_s05", 0, N, 30, lambda f: (campos(f)[0], look(*campos(f))))
    # RTG glow (false colour) while the RTGs are discussed
    for f, v in ((0, 0), (115, 0), (150, 1), (590, 1), (640, 0)): s.key("RTGGlow", f, v)
    # radio ripple toward the Earth dot
    born = list(range(862, N, 30)); RL = 170
    for i in range(7):
        for f in range(N):
            mine = [b for b in born[i::7] if b <= f < b + RL]
            if mine:
                age = f - mine[0]; ax = AX[f]; start = apply((0, 0, 0), ax, (DISH_X0 + DISH_F * 0.45, 0, 0))
                p = start + s.E * (age * 95.0 + 0.5 * age * age * 0.25); sc = (0.25 + 1.5 * smooth(age / 30)) * (1 + age / 140)
                s.row("Ring%d" % i, f, p, rot_from_axes(*frame_axes(s.E)), (sc, sc, sc))
            else: s.row("Ring%d" % i, f, PARK, (0, 0, 0), (0.001,) * 3)
    A = lambda key: (lambda f: apply((0, 0, 0), AX[f], ANCH[key]))
    s.label("six-sided equipment box", 24, 290, A("bus"), offset=(-0.16, 0.13))
    s.label("RTG power units (4)", 105, 610, A("rtg1"), offset=(0.12, -0.06))
    s.label("RTG glow: false-color heat view (illustration)", 135, 600, at=(0.5, 0.06), kind="banner")
    s.label("magnetometer boom", 655, 846, A("mag"), offset=(0.08, 0.07))
    s.label("gold plaque", 765, 850, A("plaque"), offset=(-0.16, 0.09))
    s.label("radio signal home: 8 watts", 880, N, A("dish"), offset=(-0.16, 0.06))
    s.label("Earth", 925, N, lambda f: s.E * 4.5e6 * 0.98, offset=(0.05, 0.06))
    s.label("Sun", 925, N, lambda f: s.S * 4.5e6, offset=(-0.06, -0.06))
    return s

# ======================================================================= s06: close on the plaque (camera rides with the spin)
def s06():
    s = Scene("s06"); s.sky(); N = s.N; spin0 = 140.0
    n = np.array(ydir(PLAQUE_PHI)); t = np.cross([1.0, 0, 0], n); pc = np.array(PLAQUE_C)
    def local_cam(f):
        u = smooth(f / (N - 1)); D = 118 - 52 * u
        pos = pc + n * D + t * (9 * (1 - u) - 2) + np.array([1.0, 0, 0]) * (5 - 4 * u)
        tgt = pc - np.array([1.0, 0, 0]) * (3.0 - 1.2 * u) + t * 0.3
        return pos, tgt
    AX = []
    for f in range(N):
        AX.append(put_pioneer(s, "Pioneer", f, (0, 0, 0), s.E, spin0 + SPIN * f / FPS))
        ax = AX[-1]; lp = apply((0, 0, 0), ax, pc + n * 130 + np.array([60.0, 0, 0]) + t * 40)
        s.row("PlaqueLight", f, lp, rot_from_axes(*frame_axes(apply((0, 0, 0), ax, pc) - lp)))
    def cam(f):
        ax = AX[f]; lp, lt = local_cam(f); pos = apply((0, 0, 0), ax, lp); tgt = apply((0, 0, 0), ax, lt)
        return pos, rot_from_axes(*frame_axes(tgt - pos, ax[0]))     # camera 'up' = the dish axis (plaque upright)
    s.const("Truck", TRUCK_BESIDE, (0, 0, 180)); s.const("RoofDish", apply(TRUCK_BESIDE, yaw_axes(180), TRK_ROOFDISH_PIVOT), rot_from_axes(*frame_axes(s.E)))
    s.cam("Cam_s06", 0, N, 50, cam, fstop=11.0, focus=70.0)
    return s

# ======================================================================= s09: inside the truck, Pioneer through the windshield
def s09():
    s = Scene("s09"); s.sky(); N = s.N; spin0 = 60.0
    cab_pos = np.array([-200.0, 1250.0, -215.0]); cab_ax = yaw_axes(math.degrees(math.atan2(-1250, 200)) + 3, -1.0, 0.0)
    for f in range(N): put_pioneer(s, "Pioneer", f, (0, 0, 0), s.E, spin0 + SPIN * f / FPS)
    s.const("Cab", cab_pos, rot_from_axes(*cab_ax))
    s.const("CabLight", apply(cab_pos, cab_ax, (40, 0, 238)))
    W = lambda p: apply(cab_pos, cab_ax, p)
    def cam(f):
        u = smooth(f / (N - 1)); lp = lerp((86, 8, 183), (122, -2, 180), u); lt = lerp((300, 6, 180), (300, -6, 182), u)
        lp = lp + np.array([0, 0.6 * wobble(f, 21), 0.5 * wobble(f, 22)])
        return W(lp), rot_from_axes(*frame_axes(W(lt) - W(lp), cab_ax[2]))
    s.cam("Cam_s09", 0, N, 24, cam)
    # the floating coffee cup drifts by the dash (still floating since liftoff)
    for f in range(N):
        p = lerp((190, 70, 196), (175, 30, 205), f / N) + np.array([0, 2 * wobble(f, 31), 2 * wobble(f, 32)])
        cax = axes_from_rot([20 + f * 0.25, 10 + f * 0.11, f * 0.18])
        X = cab_ax[0] * cax[0][0] + cab_ax[1] * cax[0][1] + cab_ax[2] * cax[0][2]
        Y = cab_ax[0] * cax[1][0] + cab_ax[1] * cax[1][1] + cab_ax[2] * cax[1][2]
        Z = cab_ax[0] * cax[2][0] + cab_ax[1] * cax[2][1] + cab_ax[2] * cax[2][2]
        s.row("Cup", f, W(p), rot_from_axes(X, Y, Z))
    # the printed headline floats up into view at 375, hangs, then drifts away after "put the headline down"
    for f in range(N):
        if f < 350: s.row("Paper", f, PARK, (0, 0, 0), (0.001,) * 3); continue
        a = ramp(f, 350, 395); b = ramp(f, 468, 560)
        lp = lerp((215, -40, 105), (215, -4, 177), a) + lerp((0, 0, 0), (30, 70, -110), b) + np.array([0, 1.2 * wobble(f, 41), 1.2 * wobble(f, 42)])
        yaw = 8 * wobble(f, 43) + 50 * b; roll = 6 * wobble(f, 44) + 30 * b; pitch = 10 + 4 * wobble(f, 45) - 40 * b
        pax = axes_from_rot([roll, pitch, yaw])
        X = sum(cab_ax[i] * pax[0][i] for i in range(3)); Y = sum(cab_ax[i] * pax[1][i] for i in range(3)); Z = sum(cab_ax[i] * pax[2][i] for i in range(3))
        s.row("Paper", f, W(lp), rot_from_axes(X, Y, Z), (1, 1, 1))
    s.bubbles = [("dark matter?", 128, 330, (0.30, 0.30)), ("bent gravity?", 178, 336, (0.52, 0.22)), ("a new law of nature?", 238, 342, (0.72, 0.33))]
    for txt, a, b, at in s.bubbles: s.label(txt, a, b, at=at, kind="bubble")
    return s

# ======================================================================= s12: false-colour heat view
def s12():
    s = Scene("s12"); s.sky(earth=False); N = s.N; rng = np.random.default_rng(12)
    ax = spun(np.array([1.0, 0, 0]), 30.0); s.const("PioneerHeat", H0, rot_from_axes(*ax))
    W = lambda p: apply(H0, ax, p)
    def cam(f):
        u = smooth(f / (N - 1)); pos = H0 + lerp((-150, -1700, 40), (-120, -1450, 30), u); tgt = H0 + lerp((-70, 0, -110), (-60, 0, -100), u)
        return pos, look(pos, tgt)
    s.cam("Cam_s12", 0, N, 30, cam)
    rtg = [np.array(local(BOOM_X, phi + 0.0, rc)) for phi in RTG_PHI for rc in RTG_CENTERS]
    phis = list(RTG_PHI)
    def path_for(kind):
        if kind == "bounce":
            i = rng.integers(0, 4); phi = phis[i // 2]; p0 = rtg[i] + np.array([rng.uniform(5, 15), 0, 0])
            hr = rng.uniform(70, 128); hphi = phi + rng.uniform(-28, 28)
            p1 = np.array(local(dish_x(hr) - DISH_T - 2, hphi, hr))
            refl = nrm(np.array([-1.0, 0, 0]) + np.array(ydir(hphi)) * rng.uniform(0.1, 0.45))
            return [p0, p1, p1 + refl * 600]
        if kind == "back":
            if rng.random() < 0.55:
                i = rng.integers(0, 4); p0 = rtg[i]; phi = phis[i // 2]
                d = nrm(np.array([-1.0, 0, 0]) * rng.uniform(0.6, 1.0) + np.array(ydir(phi + rng.uniform(-50, 50))) * rng.uniform(0.2, 0.9))
                p0 = p0 + d * 25
            else:
                p0 = np.array([BUS_X0 - 4, *(rng.uniform(-45, 45, 2))]); d = nrm(np.array([-1.0, *rng.uniform(-0.35, 0.35, 2)]))
            return [p0, p0 + d * 650]
        i = rng.integers(0, 4); p0 = rtg[i]; phi = phis[i // 2]
        d = nrm(np.array([1.0, 0, 0]) * rng.uniform(0.3, 0.8) + np.array(ydir(phi + rng.uniform(-30, 30))) * rng.uniform(0.6, 1.0)); p0 = p0 + d * 25
        return [p0, p0 + d * 650]
    SPEED = 5.2; LA = 66.0 * 0.62
    for k in range(44):
        rows = [None] * N; f = -int(rng.integers(0, 160)) + 10
        while f < N:
            kind = rng.choice(["bounce", "back", "front"], p=[0.42, 0.36, 0.22]); P = path_for(kind)
            segs = [np.linalg.norm(P[j + 1] - P[j]) for j in range(len(P) - 1)]; total = sum(segs); life = int(total / SPEED)
            for a in range(life):
                g = f + a
                if g < 0 or g >= N: continue
                dist = a * SPEED; j = 0
                while j < len(segs) - 1 and dist > segs[j]: dist -= segs[j]; j += 1
                d = nrm(P[j + 1] - P[j]); tip = P[j] + d * dist
                if j > 0 and dist < LA:     # just bounced: swing the arrow over as it leaves the dish
                    d0 = nrm(P[j] - P[j - 1]); w = smooth(dist / LA); d = nrm(d0 * (1 - w) + d * w)
                sc = 0.62 * min(1.0, a / 8.0, (life - a) / 10.0)
                if g < 22: sc *= g / 22.0
                wd = ax[0] * d[0] + ax[1] * d[1] + ax[2] * d[2]
                rows[g] = [*W(tip - d * LA), *rot_from_axes(*frame_axes(wd)), sc, sc * 1.1, sc * 1.1]
            f += life + int(rng.integers(4, 30))
        s.tracks["Arrow%d" % k] = [r if r is not None else PARK + [0, 0, 0, 0.001, 0.001, 0.001] for r in rows]
    # the net push: a small arrow on the craft, pointing sunward (+X here = toward the Sun)
    for f in range(N):
        g = ramp(f, 628, 650) * (1 + 0.04 * math.sin(f / 6.0))
        if g < 0.01: s.row("BigArrow", f, PARK, (0, 0, 0), (0.001,) * 3)
        else: s.row("BigArrow", f, W((-150 + 0, -105, -10)), rot_from_axes(*frame_axes(ax[0])), (2.3 * g, 2.6 * g, 2.6 * g))
    s.label("false-color heat view (illustration)", 0, N, at=(0.5, 0.055), kind="banner")
    s.label("toward the Sun", 0, N, at=(0.085, 0.16), kind="arrowleft")
    s.label("RTGs: hot", 30, 627, lambda f: W(local(BOOM_X, RTG_PHI[0], 285)), offset=(0.13, 0.03))
    s.label("electronics box: warm", 60, 627, lambda f: W((BUS_XM, 0, -40)), offset=(0.13, 0.12))
    s.label("heat bounces off the back of the dish", 330, 700, lambda f: W((dish_x(110) - 6, *[v * 110 for v in ydir(RTG_PHI[0] - 12)[1:]])), offset=(-0.17, -0.08))
    s.label("net push: toward the Sun", 650, N, lambda f: W((-40, -105, -10)), offset=(-0.10, 0.12))
    s.label("about 63 W beamed one way, of ~2,000 W", 720, 935, at=(0.24, 0.27), kind="note")
    return s

# ======================================================================= s14: wide pull-back, Pioneer shrinking from the cab, the truck turns for home
def s14():
    s = Scene("s14"); s.sky(); N = s.N; spin0 = 200.0; A1, B1 = 399, 697
    cab_pos = np.array([1150.0, 60.0, -260.0]); cab_ax = yaw_axes(180.0, -1.5, 0.0)
    for f in range(N):
        if f < A1:
            put_pioneer(s, "Pioneer", f, (-2.0 * f, 0, 0), s.E, spin0 + SPIN * f / FPS)
            truck_parts(s, f, TRUCK_BESIDE + np.array([-2.0 * f, 0, 4 * wobble(f, 51)]), yaw_axes(180, 0, 0.5 * wobble(f, 52)), s.E)
            s.row("Cab", f, PARK, (0, 0, 0), (0.001,) * 3); s.row("CabLight", f, PARK)
        elif f < B1:
            u = (f - A1) / (B1 - A1); put_pioneer(s, "Pioneer", f, (-300 - 2600 * u ** 1.3, 0, -30 + 0 * u), s.E, spin0 + SPIN * f / FPS)
            for n_ in ("Truck", "RoofDish"): s.row(n_, f, PARK, (0, 0, 0), (0.001,) * 3)
            for n_ in ("Flame", "FlameCore", "FlameLight"): s.row(n_, f, PARK, (0, 0, 0), (0.001,) * 3)
            s.row("Cab", f, cab_pos, rot_from_axes(*cab_ax)); s.row("CabLight", f, apply(cab_pos, cab_ax, (40, 0, 238)))
        else:
            g = f - B1; u = smooth(g / 88.0); yaw = 180 - 180 * u
            put_pioneer(s, "Pioneer", f, (-5200 - 3 * g, 700, 0), s.E, spin0 + SPIN * f / FPS)
            T = np.array([300.0 + 60 * ramp(g, 70, 96) * (g - 70) / 26, 0, 0]); bank = -10 * math.sin(math.pi * u)
            truck_parts(s, f, T + np.array([0, 0, 3 * wobble(f, 53)]), yaw_axes(yaw, 0, bank), s.E, flame=0.75 * ramp(g, 72, 84))
            s.row("Cab", f, PARK, (0, 0, 0), (0.001,) * 3); s.row("CabLight", f, PARK)
    # crumpled headline floating in the cab during B
    for f in range(N):
        if A1 <= f < B1:
            u = (f - A1) / (B1 - A1); lp = lerp((215, 70, 160), (215, -35, 176), u) + np.array([0, 2 * wobble(f, 61), 2 * wobble(f, 62)])
            s.row("Ball", f, apply(cab_pos, cab_ax, lp), (f * 0.7, f * 0.4, f * 0.9), (0.6, 0.6, 0.6))
        else: s.row("Ball", f, PARK, (0, 0, 0), (0.001,) * 3)
    def camA(f):
        u = smooth(f / (A1 - 1)); pos = lerp((-2300, -760, 330), (-4600, -1500, 640), u) + np.array([-2.0 * f, 0, 0]); tgt = lerp((0, 300, -60), (300, 260, 60), u) + np.array([-2.0 * f, 0, 0])
        return pos, look(pos, tgt)
    def camB(f):
        u = smooth((f - A1) / (B1 - A1)); lp = lerp((92, 4, 183), (120, 0, 181), u); lt = (300, -2, 170)
        W = lambda p: apply(cab_pos, cab_ax, p); return W(lp), rot_from_axes(*frame_axes(W(lt) - W(lp), cab_ax[2]))
    def camC(f):
        g = f - B1; u = smooth(g / 95.0); pos = np.array([420.0 - 120 * u, -1500.0, 170.0]); tgt = np.array([260.0 - 40 * u, 0.0, -70.0])
        return pos, look(pos, tgt)
    s.cam("Cam_s14a", 0, A1, 28, camA); s.cam("Cam_s14b", A1, B1, 24, camB); s.cam("Cam_s14c", B1, N, 24, camC)
    s.label("Sun", 40, A1, lambda f: s.S * 4.5e6, offset=(-0.05, -0.06)); s.label("Earth", 60, A1, lambda f: s.E * 4.5e6 * 0.98, offset=(0.05, 0.06))
    return s

# ======================================================================= s03: liftoff from the parking lot
def s03():
    s = Scene("s03"); N = s.N; A1, B1, C1 = 100, 205, 262
    S = nrm([-0.45, -0.62, 0.64]); s.sky(S=S, earth=False, center=G, sun_d=1.0e6)
    s.const("Ground", G); s.const("Sky", G, (0, 0, 0), (15000, 15000, 15000))
    station = G + np.array([-2700.0, 3000.0, 1160.0])
    for f, v in ((0, 1), (130, 1), (205, 0.35), (262, 0.12), (300, 0)): s.key("SkyAmount", f, v)
    # truck flight: ignition 100, lift 112, nose up, accelerate; 330+: the TV shortcut
    pos = G.copy(); vel = np.zeros(3); traj = []
    for f in range(N):
        pitch = 72 * smooth((f - 112) / 70.0) if f >= 112 else 0.0
        ax = yaw_axes(0.0, pitch, 0.0)
        if f >= 112:
            acc = 0.5 + 2.4 * smooth((f - 112) / 40.0) + (4.0 * ramp(f, 200, 260)) + (60 * ramp(f, 338, 370)) ; vel = vel + ax[0] * acc * 0.6 + np.array([0, 0, acc * 0.4]) * (1 if f < 190 else 0.3)
        pos = pos + vel; traj.append((pos.copy(), ax))
    for f in range(N):
        p, ax = traj[f]
        if f < A1:
            s.row("Truck", f, PARK, (0, 0, 0), (0.001,) * 3); s.row("RoofDish", f, PARK, (0, 0, 0), (0.001,) * 3)
            for n_ in ("Flame", "FlameCore", "FlameLight"): s.row(n_, f, PARK, (0, 0, 0), (0.001,) * 3)
        elif B1 <= f < C1:
            s.row("Truck", f, PARK, (0, 0, 0), (0.001,) * 3); s.row("RoofDish", f, PARK, (0, 0, 0), (0.001,) * 3)
            for n_ in ("Flame", "FlameCore", "FlameLight"): s.row(n_, f, PARK, (0, 0, 0), (0.001,) * 3)
        else:
            shake = np.array([0, 1.5 * wobble(f, 71, (6.1, 9.7)), 1.5 * wobble(f, 72, (5.3, 8.9))]) if f < 140 else 0
            truck_parts(s, f, p + shake, ax, None, flame=(1.25 if f < 330 else 1.6) * ramp(f, A1, A1 + 8), dish_target=station, seed=3)
    # the cab (interior): on the ground for A, pitched up in the sky for C
    cabA = (G, yaw_axes(0, 0, 0)); cabC = (G + np.array([0, 0, 60000.0]), yaw_axes(0, 62, 0))
    for f in range(N):
        cp, cax = cabA if f < A1 + 20 else cabC
        s.row("Cab", f, cp, rot_from_axes(*cax)); s.row("CabLight", f, apply(cp, cax, (40, 0, 238)))
    # coffee cup + droplet float in C
    for f in range(N):
        if B1 - 10 <= f < C1:
            g = f - B1; cp, cax = cabC; lp = np.array([118.0, 10.0, 178.0]) + np.array([0, -0.15 * g, 0.12 * g])
            W = lambda q: apply(cp, cax, q)
            def wr(r):
                a_ = axes_from_rot(r); return rot_from_axes(*[sum(cax[i] * a_[k][i] for i in range(3)) for k in range(3)])
            s.row("Cup", f, W(lp), wr([25 + 0.8 * g, 12 + 0.35 * g, 30 + 0.5 * g])); s.row("Blob", f, W(lp + np.array([4, 12 - 0.1 * g, 9 + 0.05 * g])), (0, 0, 0), (0.016 * (1 + 0.1 * math.sin(g / 3)), 0.016 * (1 - 0.08 * math.sin(g / 3)), 0.016))
        else:
            s.row("Cup", f, PARK, (0, 0, 0), (0.001,) * 3); s.row("Blob", f, PARK, (0, 0, 0), (0.001,) * 3)
    # smoke puffs from the nozzle during B
    rng = np.random.default_rng(3)
    for i in range(10):
        b = A1 + 2 + i * 9; jitter = rng.normal(0, 1, 3)
        for f in range(N):
            if b <= f < C1 + 200 and f < B1:
                p0, ax0 = traj[b]; noz = apply(p0, ax0, TRK_NOZZLE) - np.array([0, 0, 60])
                age = f - b; sc = 0.6 + 5.5 * (1 - math.exp(-age / 25.0)); drift = jitter * np.array([60, 60, 20]) * (age / 25.0) + np.array([0, 0, -20 * age / 25.0])
                s.row("Smoke%d" % i, f, noz + drift, (age * 0.7, i * 30, age * 0.4), (sc, sc, sc * 0.85))
            else: s.row("Smoke%d" % i, f, PARK, (0, 0, 0), (0.001,) * 3)
    WA = lambda q: apply(cabA[0], cabA[1], q)
    def camA(f):
        k = ramp(f, 20, 95); sh = np.array([0, (0.3 + 1.6 * k) * wobble(f, 81, (4.7, 7.9, 12.3)), (0.3 + 1.6 * k) * wobble(f, 82, (5.9, 9.3, 13.1))])
        lp = np.array([92.0, 6, 183]) + sh; lt = np.array([300.0, -10, 168])
        return WA(lp), rot_from_axes(*frame_axes(WA(lt) - WA(lp), (0.012 * k * wobble(f, 83, (6.7, 10.1)), 0, 1)))
    def camB(f):
        p, _ = traj[f]; pos = G + np.array([-1500.0, -3400.0, 170.0]); tgt = p + np.array([0, 0, 120])
        tgt = lerp(G + np.array([0, 0, 260]), tgt, ramp(f, 108, 140))
        return pos, look(pos, tgt)
    WC = lambda q: apply(cabC[0], cabC[1], q)
    def camC(f):
        g = f - B1; lp = np.array([62.0, -14, 186]) + np.array([0, 0.4 * wobble(f, 91), 0.4 * wobble(f, 92)]); lt = np.array([118.0, 6 - 0.15 * g, 178 + 0.12 * g])
        return WC(lp), rot_from_axes(*frame_axes(WC(lt) - WC(lp), cabC[1][2]))
    def camD(f):
        hold = traj[332][0]; p = traj[min(f, 332)][0]
        base = p + np.array([-700.0, -1300.0, -260.0]); pos = base
        tgt = traj[f][0] + np.array([-100, 0, 80]) * (1 - ramp(f, 332, 350))
        return pos, look(pos, tgt)
    s.cam("Cam_s03a", 0, A1, 24, camA); s.cam("Cam_s03b", A1, B1, 32, camB); s.cam("Cam_s03c", B1, C1, 30, camC, fstop=8, focus=80); s.cam("Cam_s03d", C1, N, 28, camD)
    s.traj_end = traj[-1][0].tolist()
    return s

if __name__ == "__main__":
    import sys
    want = sys.argv[1:] or ["s03", "s04", "s05", "s06", "s09", "s12", "s14"]
    out = {"park": PARK, "G": G.tolist(), "H0": H0.tolist(), "actors": ALL, "scenes": {}}
    for sid in want:
        s = globals()[sid](); fill_park(s, ALL)
        for n_, tr in s.tracks.items():     # unwrap angles so sub-frame samples never spin the long way round
            for ch in (3, 4, 5):
                for i in range(1, len(tr)):
                    d = tr[i][ch] - tr[i - 1][ch]
                    if d > 180: tr[i][ch] -= 360 * round(d / 360)
                    elif d < -180: tr[i][ch] += 360 * round(-d / 360)
        for c in s.cams:
            for ch in (3, 4, 5):
                for i in range(1, len(c["rows"])):
                    d = c["rows"][i][ch] - c["rows"][i - 1][ch]
                    if abs(d) > 180: c["rows"][i][ch] -= 360 * round(d / 360)
        out["scenes"][sid] = s.out(); print(sid, s.N, "frames,", len(s.cams), "cams,", len(s.labels), "labels")
    json.dump(out, open(HERE + "/plan.json", "w"))
