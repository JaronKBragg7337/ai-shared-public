# Procedural meshes for the Pioneer space scenes -> GLB files (one mesh per material), imported by build.py.
# Geometry is written in Unreal cm (X forward, Y right, Z up) and converted to glTF (metres, Y up): g = (X, Z, Y) / 100.
import json, math, struct, numpy as np
from geom import *
OUT = __file__.replace("\\", "/").rsplit("/", 1)[0] + "/meshes/"
rng = np.random.default_rng(1972)

def nrm(v):
    v = np.asarray(v, float); l = np.linalg.norm(v, axis=-1, keepdims=True); return v / np.maximum(l, 1e-12)

def basis(axis, up_hint=(0, 0, 1)):
    """orthonormal frame with X = axis"""
    x = nrm(axis); u = np.asarray(up_hint, float)
    if abs(np.dot(x, nrm(u))) > 0.95: u = np.array([0, 1.0, 0]) if abs(x[1]) < 0.9 else np.array([1.0, 0, 0])
    y = nrm(np.cross(u, x)); z = np.cross(x, y)
    return np.stack([x, y, z], 1)        # columns = local axes in world

class Bank:
    def __init__(s): s.m = {}
    def add(s, name, V, N, UV, T):
        d = s.m.setdefault(name, [[], [], [], [], 0])
        V = np.asarray(V, float).reshape(-1, 3); N = np.asarray(N, float).reshape(-1, 3); UV = np.asarray(UV, float).reshape(-1, 2)
        T = np.asarray(T, int).reshape(-1, 3)
        d[0].append(V); d[1].append(nrm(N)); d[2].append(UV); d[3].append(T + d[4]); d[4] += len(V)

    # ---------- primitives (world = origin + M @ local)
    def box(s, name, c, size, M=np.eye(3), uvs=100.0):
        c = np.asarray(c, float); h = np.asarray(size, float) / 2
        faces = [((1, 0, 0), (0, 1, 0), (0, 0, 1)), ((-1, 0, 0), (0, -1, 0), (0, 0, 1)), ((0, 1, 0), (-1, 0, 0), (0, 0, 1)),
                 ((0, -1, 0), (1, 0, 0), (0, 0, 1)), ((0, 0, 1), (0, 1, 0), (-1, 0, 0)), ((0, 0, -1), (0, 1, 0), (1, 0, 0))]
        for n, u, v in faces:
            n, u, v = map(np.array, (n, u, v))
            ctr = n * h; us = np.abs(u) @ h; vs = np.abs(v) @ h
            P = [ctr - u * us - v * vs, ctr + u * us - v * vs, ctr + u * us + v * vs, ctr - u * us + v * vs]
            V = [c + M @ p for p in P]; N = [M @ n] * 4
            UV = [(0, 0), (2 * us / uvs, 0), (2 * us / uvs, 2 * vs / uvs), (0, 2 * vs / uvs)]
            s.add(name, V, N, UV, [(0, 1, 2), (0, 2, 3)])

    def revolve(s, name, prof, origin=(0, 0, 0), M=np.eye(3), seg=48, phi0=0.0, phi1=360.0, nrmprof=None, vrange=None):
        """prof: list of (x, r) in the local frame (axis = local X); normals from the profile (outward of the curve's left side)"""
        prof = np.asarray(prof, float); o = np.asarray(origin, float); n = len(prof)
        if nrmprof is None:
            t = np.gradient(prof, axis=0); nrmprof = np.stack([-t[:, 1], t[:, 0]], 1)    # rotate tangent: (dx, dr) -> (-dr, dx)
        nrmprof = nrm(nrmprof)
        L = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(prof, axis=0), axis=1))]); L = L / max(L[-1], 1e-9)
        if vrange is not None: L = vrange[0] + L * (vrange[1] - vrange[0])
        V, N, UV, T = [], [], [], []
        for j in range(seg + 1):
            a = math.radians(phi0 + (phi1 - phi0) * j / seg); ca, sa = math.cos(a), math.sin(a)
            for i in range(n):
                x, r = prof[i]; nx, nr = nrmprof[i]
                V.append(o + M @ np.array([x, r * ca, r * sa])); N.append(M @ np.array([nx, nr * ca, nr * sa])); UV.append((j / seg, L[i]))
        for j in range(seg):
            for i in range(n - 1):
                a0 = j * n + i; b0 = (j + 1) * n + i
                T += [(a0, b0, b0 + 1), (a0, b0 + 1, a0 + 1)]
        s.add(name, V, N, UV, T)

    def cyl(s, name, p0, p1, r0, r1=None, seg=20, caps=True):
        p0 = np.asarray(p0, float); p1 = np.asarray(p1, float); r1 = r0 if r1 is None else r1
        ax = p1 - p0; Lh = np.linalg.norm(ax); M = basis(ax)
        s.revolve(name, [(0, r0), (Lh, r1)], p0, M, seg)
        if caps:
            for x, r, sgn in ((0, r0, -1), (Lh, r1, 1)):
                if r <= 0: continue
                c = p0 + M @ np.array([x, 0, 0]); V = [c]; N = [M @ np.array([sgn, 0, 0])]; UV = [(0.5, 0.5)]; T = []
                for j in range(seg + 1):
                    a = 2 * math.pi * j / seg; V.append(p0 + M @ np.array([x, r * math.cos(a), r * math.sin(a)])); N.append(N[0]); UV.append((0.5 + 0.5 * math.cos(a), 0.5 + 0.5 * math.sin(a)))
                for j in range(seg): T.append((0, j + 1, j + 2))
                s.add(name, V, N, UV, T)

    def torus(s, name, c, axis, R, r, seg=48, seg2=12, arc=360.0, up=(0, 0, 1)):
        M = basis(axis, up); c = np.asarray(c, float); V, N, UV, T = [], [], [], []
        for j in range(seg + 1):
            a = math.radians(arc * j / seg); ra = np.array([0, math.cos(a), math.sin(a)])
            for i in range(seg2 + 1):
                b = 2 * math.pi * i / seg2; nl = ra * math.cos(b) + np.array([1, 0, 0]) * math.sin(b)
                V.append(c + M @ (ra * R + nl * r)); N.append(M @ nl); UV.append((j / seg, i / seg2))
        for j in range(seg):
            for i in range(seg2):
                a0 = j * (seg2 + 1) + i; b0 = (j + 1) * (seg2 + 1) + i
                T += [(a0, b0, b0 + 1), (a0, b0 + 1, a0 + 1)]
        s.add(name, V, N, UV, T)

    def quad(s, name, c, u, v, w, h, uv=((0, 0), (1, 1)), n=None):
        """u = image-right direction, v = image-down direction; normal defaults to v x u (faces the viewer for whom u is right and v is down)"""
        c = np.asarray(c, float); u = nrm(u); v = nrm(v); n = nrm(np.cross(v, u)) if n is None else nrm(n)
        P = [c - u * w / 2 - v * h / 2, c + u * w / 2 - v * h / 2, c + u * w / 2 + v * h / 2, c - u * w / 2 + v * h / 2]
        (u0, v0), (u1, v1) = uv
        s.add(name, P, [n] * 4, [(u0, v0), (u1, v0), (u1, v1), (u0, v1)], [(0, 1, 2), (0, 2, 3)])

    def poly(s, name, pts, n, uvf):
        pts = [np.asarray(p, float) for p in pts]
        s.add(name, pts, [n] * len(pts), [uvf(p) for p in pts], [(0, i, i + 1) for i in range(1, len(pts) - 1)])

    def extrude(s, name, prof, y0, y1, uvs=100.0):
        """convex polygon in (x, z), extruded along Y"""
        prof = [np.asarray(p, float) for p in prof]; k = len(prof)
        for y, sgn in ((y0, -1), (y1, 1)):
            s.poly(name, [(p[0], y, p[1]) for p in prof], (0, sgn, 0), lambda q: (q[0] / uvs, -q[2] / uvs))
        for i in range(k):
            a, b = prof[i], prof[(i + 1) % k]; e = b - a; nn = nrm([e[1], 0, -e[0]])
            ctr = np.mean(prof, 0)
            if np.dot([(a + b)[0] / 2 - ctr[0], 0, (a + b)[1] / 2 - ctr[1]], nn) < 0: nn = -nn
            P = [(a[0], y0, a[1]), (b[0], y0, b[1]), (b[0], y1, b[1]), (a[0], y1, a[1])]
            Ln = np.linalg.norm(e)
            s.add(name, P, [nn] * 4, [(0, 0), (Ln / uvs, 0), (Ln / uvs, (y1 - y0) / uvs), (0, (y1 - y0) / uvs)], [(0, 1, 2), (0, 2, 3)])

    def rod(s, name, a, b, r, seg=8): s.cyl(name, a, b, r, r, seg, caps=False)

    # ---------- GLB
    def write(s, fn):
        bins = b""; views = []; accs = []; meshes = []; nodes = []; mats = []
        def push(arr, target, comp, typ, minmax=False):
            nonlocal bins
            raw = arr.tobytes(); pad = (-len(bins)) % 4; bins += b"\0" * pad
            views.append({"buffer": 0, "byteOffset": len(bins), "byteLength": len(raw), "target": target}); bins += raw
            a = {"bufferView": len(views) - 1, "componentType": comp, "count": int(arr.shape[0]), "type": typ}
            if minmax: a["min"] = arr.min(0).tolist(); a["max"] = arr.max(0).tolist()
            accs.append(a); return len(accs) - 1
        for name, (Vs, Ns, UVs, Ts, _) in s.m.items():
            V = np.concatenate(Vs); N = np.concatenate(Ns); UV = np.concatenate(UVs); T = np.concatenate(Ts)
            G = np.stack([V[:, 0], V[:, 2], V[:, 1]], 1) / 100.0; GN = np.stack([N[:, 0], N[:, 2], N[:, 1]], 1)
            # winding: make every triangle CCW around its vertex normal (glTF is right-handed)
            a, b, c = G[T[:, 0]], G[T[:, 1]], G[T[:, 2]]
            cr = np.cross(b - a, c - a); nn = GN[T[:, 0]] + GN[T[:, 1]] + GN[T[:, 2]]
            flip = np.einsum("ij,ij->i", cr, nn) < 0; T = T.copy(); T[flip] = T[flip][:, [0, 2, 1]]
            ia = push(G.astype(np.float32), 34962, 5126, "VEC3", True); ib = push(GN.astype(np.float32), 34962, 5126, "VEC3")
            ic = push(UV.astype(np.float32), 34962, 5126, "VEC2"); ii = push(T.astype(np.uint32).reshape(-1), 34963, 5125, "SCALAR")
            mats.append({"name": "MAT_" + name, "pbrMetallicRoughness": {"baseColorFactor": [0.8, 0.8, 0.8, 1], "metallicFactor": 0, "roughnessFactor": 0.5}})
            meshes.append({"name": name, "primitives": [{"attributes": {"POSITION": ia, "NORMAL": ib, "TEXCOORD_0": ic}, "indices": ii, "material": len(mats) - 1}]})
            nodes.append({"name": name, "mesh": len(meshes) - 1})
            print("  %-22s %6d verts %6d tris" % (name, len(V), len(T)))
        js = {"asset": {"version": "2.0", "generator": "pioneer meshgen"}, "scene": 0, "scenes": [{"nodes": list(range(len(nodes)))}],
              "nodes": nodes, "meshes": meshes, "materials": mats, "accessors": accs, "bufferViews": views, "buffers": [{"byteLength": len(bins)}]}
        jb = json.dumps(js).encode(); jb += b" " * ((-len(jb)) % 4); bins += b"\0" * ((-len(bins)) % 4)
        with open(OUT + fn, "wb") as f:
            f.write(struct.pack("<III", 0x46546C67, 2, 12 + 8 + len(jb) + 8 + len(bins)))
            f.write(struct.pack("<II", len(jb), 0x4E4F534A)); f.write(jb); f.write(struct.pack("<II", len(bins), 0x004E4942)); f.write(bins)
        print("wrote", fn)

def RX(phi):  # local frame for a boom at angle phi around X: columns (radial, tangential, axial X)
    d = np.array(ydir(phi)); t = np.cross([1.0, 0, 0], d)
    return d, t

# ======================================================================= Pioneer 10
def pioneer():
    b = Bank()
    # dish: front (concave, faces +X), back, rim
    rs = np.linspace(0, DISH_R, 40)
    front = [(dish_x(r), r) for r in rs]; nf = [(1, -r / (2 * DISH_F)) for r in rs]
    b.revolve("PIO_DishFront", front, seg=96, nrmprof=nf)
    back = [(dish_x(r) - DISH_T, r) for r in rs]; nb = [(-1, r / (2 * DISH_F)) for r in rs]
    b.revolve("PIO_DishBack", back, seg=96, nrmprof=nb)
    b.revolve("PIO_DishBack", [(dish_x(DISH_R) - DISH_T, DISH_R), (dish_x(DISH_R) + 0.5, DISH_R)], seg=96, nrmprof=[(0, 1), (0, 1)])
    b.cyl("PIO_Metal", (dish_x(0) - 1, 0, 0), (dish_x(0) + 7, 0, 0), 20, 16, seg=32)
    # feed: tripod to the focus + horn (medium-gain antenna)
    fx = DISH_X0 + DISH_F
    for phi in (90, 210, 330):
        p = np.array(local(dish_x(112), phi, 112)); b.rod("PIO_Metal", p, (fx - 6, *[v * 9 for v in ydir(phi)[1:]]), 1.6)
    b.cyl("PIO_Metal", (fx - 8, 0, 0), (fx + 18, 0, 0), 9, 9, seg=24)
    b.revolve("PIO_Feed", [(fx - 8, 9), (fx - 20, 15)], seg=24)
    # equipment bus: hexagonal prism (vertices at 30 + 60k deg), MLI on the sides
    vang = [30 + 60 * k for k in range(6)]
    for k in range(6):
        a0, a1 = vang[k], vang[(k + 1) % 6]
        p0 = np.array(local(0, a0, BUS_R)); p1 = np.array(local(0, a1, BUS_R)); mid = (p0 + p1) / 2; n = nrm(mid)
        side = np.linalg.norm(p1 - p0)
        P = [p0 + [BUS_X0, 0, 0], p1 + [BUS_X0, 0, 0], p1 + [BUS_X1, 0, 0], p0 + [BUS_X1, 0, 0]]
        b.add("PIO_MLI", P, [n] * 4, [(0, 0), (side / 60, 0), (side / 60, 36 / 60), (0, 36 / 60)], [(0, 1, 2), (0, 2, 3)])
    for x, sgn, nm in ((BUS_X1, 1, "PIO_Dark"), (BUS_X0, -1, "PIO_Dark")):
        pts = [np.array(local(x, a, BUS_R)) for a in vang]
        b.poly(nm, pts, (sgn, 0, 0), lambda q: (q[1] / 140 + 0.5, q[2] / 140 + 0.5))
    # thermal louvers on the aft face
    for i in range(9):
        z = -40 + i * 10; b.box("PIO_Louver", (BUS_X0 - 1.5, 0, z), (1.5, 60, 7.5), M=np.array([[math.cos(0.5), 0, -math.sin(0.5)], [0, 1, 0], [math.sin(0.5), 0, math.cos(0.5)]]))
    b.box("PIO_Metal", (BUS_X0 - 0.6, 0, 0), (1.0, 66, 94))
    # experiment compartment on the face at 180 deg
    d, t = RX(180); c = np.array([BUS_XM + 2, 0, 0]) + d * (BUS_R * math.cos(math.radians(30)) + 21)
    M = np.stack([np.array([1.0, 0, 0]), t, d], 1)
    b.box("PIO_MLI", c, (30, 62, 42), M=M, uvs=60)
    # low-gain antenna behind the bus
    b.cyl("PIO_Metal", (BUS_X0 - 2, 0, 0), (BUS_X0 - 20, 0, 0), 3.5); b.cyl("PIO_Feed", (BUS_X0 - 20, 0, 0), (BUS_X0 - 30, 0, 0), 4, 9)
    # struts: bus top corners -> dish back
    xd = dish_x(STRUT_R_DISH) - DISH_T
    for a in vang:
        b.rod("PIO_Metal", local(BUS_X1, a, BUS_R), local(xd, a, STRUT_R_DISH), 1.7)
        b.rod("PIO_Metal", local(BUS_X1, a, BUS_R - 8), local(xd, a + 30, STRUT_R_DISH - 6), 1.0)
    # plaque on the struts (faces outward at PLAQUE_PHI); image right = -Z-ish tangential, image down = -X
    d, t = RX(PLAQUE_PHI); pc = np.array(PLAQUE_C)
    b.quad("PIO_Plaque", pc + d * 0.4, -t, np.array([-1.0, 0, 0]), PLAQUE_W, PLAQUE_H, n=d)
    b.box("PIO_Metal", pc - d * 0.5, (PLAQUE_H + 1.0, PLAQUE_W + 1.0, 1.0), M=np.stack([np.array([1.0, 0, 0]), -t, d], 1))
    for sgn in (-1, 1):   # brackets to the two struts at +-30 deg
        e = pc + t * sgn * (PLAQUE_W / 2 + 0.5)
        tgt = np.array(local(PLAQUE_X, PLAQUE_PHI + sgn * 30, strut_r_at(PLAQUE_X)))
        b.rod("PIO_Metal", e - d * 0.5, tgt, 0.8)
    # RTG booms: triangular truss + two finned RTGs each
    for phi in RTG_PHI:
        d, t = RX(phi); ax = np.array([1.0, 0, 0])
        offs = [ax * 6, -ax * 3 + t * 5.5, -ax * 3 - t * 5.5]
        base = np.array([BOOM_X, 0, 0])
        ends = [(base + d * 55 + o * 1.6, base + d * RTG_BOOM_END + o) for o in offs]
        for a_, b_ in ends: b.rod("PIO_Boom", a_, b_, 1.1)
        for k in range(9):    # zig-zag braces
            f0 = 60 + k * 26; f1 = f0 + 26
            for i in range(3):
                b.rod("PIO_Boom", base + d * f0 + offs[i], base + d * f1 + offs[(i + 1) % 3], 0.6, seg=6)
        for rc in RTG_CENTERS:
            c0 = base + d * (rc - RTG_LEN / 2); c1 = base + d * (rc + RTG_LEN / 2)
            b.cyl("PIO_RTGCore", c0, c1, RTG_RC, seg=24)
            b.cyl("PIO_RTGCore", c0 - d * 1.5, c0 + d * 1.5, RTG_RC + 2.5, seg=24); b.cyl("PIO_RTGCore", c1 - d * 1.5, c1 + d * 1.5, RTG_RC + 2.5, seg=24)
            for k in range(6):
                a = math.radians(k * 60 + 30); rdir = ax * math.cos(a) + t * math.sin(a)
                M = np.stack([d, np.cross(rdir, d), rdir], 1)
                b.box("PIO_RTG", base + d * rc + rdir * (RTG_RC + RTG_RF) / 2, (RTG_LEN - 2, 1.3, RTG_RF - RTG_RC), M=M, uvs=30)
        b.cyl("PIO_RTGCore", base + d * (RTG_CENTERS[0] + RTG_LEN / 2), base + d * (RTG_CENTERS[1] - RTG_LEN / 2), 6, seg=16)
    # magnetometer boom (long, thin) + sensor at the tip
    d, t = RX(MAG_PHI); base = np.array([BOOM_X, 0, 0])
    b.rod("PIO_Boom", base + d * 60, base + d * (MAG_END - 12), 1.5, seg=10)
    for k in range(5): b.cyl("PIO_Boom", base + d * (100 + k * 110), base + d * (104 + k * 110), 2.6, seg=10)
    b.cyl("PIO_Metal", base + d * (MAG_END - 14), base + d * (MAG_END + 8), 4.5, seg=16)
    # thruster pods on the dish rim
    for phi in (30, 150, 270):
        dd, tt = RX(phi); M = np.stack([np.array([1.0, 0, 0]), tt, dd], 1)
        b.box("PIO_Metal", np.array([dish_x(DISH_R) - 9, 0, 0]) + dd * (DISH_R + 4), (12, 9, 8), M=M)
    b.write("pioneer.glb")

# ======================================================================= the live truck
def truck():
    b = Bank()
    X0, X1, Y, Z0, Z1 = -330.0, 95.0, 115.0, 60.0, 300.0
    L = X1 - X0
    b.quad("TRK_LiveryL", ((X0 + X1) / 2, -Y, (Z0 + Z1) / 2), (-1, 0, 0), (0, 0, -1), L, Z1 - Z0, n=(0, -1, 0))
    b.quad("TRK_LiveryR", ((X0 + X1) / 2, Y, (Z0 + Z1) / 2), (1, 0, 0), (0, 0, -1), L, Z1 - Z0, n=(0, 1, 0))
    b.quad("TRK_White", ((X0 + X1) / 2, 0, Z1), (1, 0, 0), (0, 1, 0), L, 2 * Y, n=(0, 0, 1), uv=((0, 0), (4, 2)))
    b.quad("TRK_White", ((X0 + X1) / 2, 0, Z0), (1, 0, 0), (0, -1, 0), L, 2 * Y, n=(0, 0, -1))
    b.quad("TRK_Rear", (X0, 0, (Z0 + Z1) / 2), (0, 1, 0), (0, 0, -1), 2 * Y, Z1 - Z0, n=(-1, 0, 0))
    b.quad("TRK_White", (X1, 0, (245 + Z1) / 2), (0, 1, 0), (0, 0, -1), 2 * Y, Z1 - 245, n=(1, 0, 0))
    for zz in (60, 298): b.box("TRK_Trim", ((X0 + X1) / 2, 0, zz), (L + 2, 2 * Y + 2, 4))
    b.box("TRK_Trim", (X0 - 1, 0, 180), (2, 2, 236)); b.box("TRK_Trim", (X0 - 1, 0, 180), (2, 2 * Y, 2))   # rear door seams
    # cab
    cab = [(95, 55), (302, 55), (302, 135), (288, 150), (236, 158), (160, 245), (95, 245)]
    b.extrude("TRK_White", cab, -110, 110)
    ws_a, ws_b = np.array([236.0, 158.0]), np.array([160.0, 245.0]); e = ws_b - ws_a; nws = nrm([-e[1], 0, e[0]]) * -1
    nws = nrm([e[1], 0, -e[0]]); nws = nws if nws[0] > 0 else -nws
    mid = (ws_a + ws_b) / 2
    b.quad("TRK_Glass", np.array([mid[0], 0, mid[1]]) + nws * 0.6, (0, -1, 0), nrm([e[0], 0, e[1]]) * -1, 196, np.linalg.norm(e) - 8, n=nws)
    for sgn in (-1, 1):
        y = sgn * 110.6; n = (0, sgn, 0)
        b.poly("TRK_Glass", [(118, y, 168), (222, y, 168), (166, y, 232), (118, y, 232)][::sgn], n, lambda q: (q[0] / 100, q[2] / 100))
    # wheels, bumpers, lights
    for x in (-240.0, 215.0):
        for sgn in (-1, 1):
            b.cyl("TRK_Tire", (x, sgn * 85, 42), (x, sgn * 112, 42), 42, seg=32)
            b.cyl("TRK_Metal", (x, sgn * 112, 42), (x, sgn * 113.5, 42), 24, seg=24)
            b.revolve("TRK_Dark", [(0, 50), (0, 47)], origin=(x, sgn * 113, 42), M=basis((0, sgn, 0)), seg=24, phi0=0, phi1=180)
    b.box("TRK_Dark", (306, 0, 70), (12, 226, 30)); b.box("TRK_Dark", (-335, 0, 68), (10, 230, 22))
    b.box("TRK_Dark", (-60, 0, 50), (520, 200, 18))
    b.quad("TRK_Dark", (302.5, 0, 110), (0, 1, 0), (0, 0, -1), 120, 36, n=(1, 0, 0))
    for sgn in (-1, 1):
        b.box("TRK_Lamp", (302, sgn * 85, 112), (3, 34, 18)); b.box("TRK_Tail", (X0 - 1.5, sgn * 100, 115), (3, 14, 40))
        b.box("TRK_Dark", (232, sgn * 120, 170), (8, 14, 18))     # mirrors
    # roof mast (the dish itself is a separate moving part)
    b.cyl("TRK_Metal", (TRK_ROOFDISH_PIVOT[0], 0, Z1), (TRK_ROOFDISH_PIVOT[0], 0, TRK_ROOFDISH_PIVOT[2] - 6), 7)
    b.box("TRK_Metal", (TRK_ROOFDISH_PIVOT[0], 0, Z1 + 3), (40, 40, 6))
    b.box("TRK_Dark", (40, 0, Z1 + 5), (60, 160, 6))     # roof rack
    # the rocket on the back
    cz = TRK_NOZZLE[2]; rx0, rx1, rr = -560.0, -331.0, 42.0
    b.cyl("TRK_RocketBody", (rx0, 0, cz), (rx1, 0, cz), rr, seg=40)
    for x in (-392.0, -528.0): b.cyl("TRK_RocketRed", (x, 0, cz), (x + 14, 0, cz), rr + 0.6, seg=40, caps=False)
    for x in (-410.0, -505.0): b.cyl("TRK_Strap", (x, 0, cz), (x + 7, 0, cz), rr + 1.2, seg=40, caps=False)
    for k in range(4):
        a = math.radians(45 + 90 * k); rd = np.array([0, math.cos(a), math.sin(a)]); M = np.stack([np.array([1.0, 0, 0]), np.cross(rd, [1.0, 0, 0]), rd], 1)
        b.box("TRK_RocketRed", np.array([-540.0, 0, cz]) + rd * (rr + 18), (52, 3, 36), M=M)
    b.revolve("TRK_Nozzle", [(rx0, 26), (rx0 - 12, 21), (TRK_NOZZLE[0], 36)], origin=(0, 0, cz), seg=32)
    b.revolve("TRK_Nozzle", [(TRK_NOZZLE[0] + 1, 33), (rx0 - 10, 19)], origin=(0, 0, cz), seg=32)
    for sgn in (-1, 1):
        for zz in (120, 250):
            b.rod("TRK_Metal", (-420, sgn * 20, cz + (zz - cz) * 0.4), (X0, sgn * 85, zz), 2.2)
    b.write("truck.glb")
    # roof dish (own pivot at the origin, points along +X)
    r = Bank(); R, Dp = 45.0, 12.0; f = R * R / (4 * Dp); x0 = 8.0
    rs = np.linspace(0, R, 20)
    r.revolve("RD_Dish", [(x0 + q * q / (4 * f), q) for q in rs], seg=48, nrmprof=[(1, -q / (2 * f)) for q in rs])
    r.revolve("RD_Dish", [(x0 + q * q / (4 * f) - 1.5, q) for q in rs], seg=48, nrmprof=[(-1, q / (2 * f)) for q in rs])
    for phi in (90, 210, 330):
        p = np.array([x0 + 36 * 36 / (4 * f), *[v * 36 for v in ydir(phi)[1:]]]); r.rod("RD_Metal", p, (x0 + f - 3, 0, 0), 0.8)
    r.cyl("RD_Metal", (x0 + f - 4, 0, 0), (x0 + f + 4, 0, 0), 3)
    r.cyl("RD_Metal", (x0 - 1.5, 0, 0), (-4, 0, 0), 6); r.box("RD_Metal", (0, 0, -4), (10, 14, 10))
    r.write("roofdish.glb")

# ======================================================================= cab interior (truck-local coordinates)
def cab():
    b = Bank()
    b.box("CAB_Floor", (75, 0, 61), (450, 224, 12))
    b.box("CAB_Liner", (10, 0, 250), (320, 224, 10)); b.box("CAB_Liner", (160, 0, 244), (22, 224, 12))
    b.box("CAB_Panel", (-150, 0, 155), (10, 224, 190))
    for sgn in (-1, 1):
        y = sgn * 110
        b.box("CAB_Panel", (75, y, 118), (450, 6, 100))
        b.box("CAB_Panel", (10, y, 240), (320, 6, 12)); b.box("CAB_Panel", (-15, y, 200), (270, 6, 70))
        # A-pillar along the windshield edge
        a, c = np.array([236.0, 158.0]), np.array([160.0, 245.0]); e = c - a; ex = nrm([e[0], 0, e[1]])
        M = np.stack([ex, np.array([0, 1.0, 0]), np.cross(ex, [0, 1.0, 0])], 1)
        b.box("CAB_Panel", (198, sgn * 104, 202), (np.linalg.norm(e) + 10, 14, 9), M=M)
        b.poly("CAB_Panel", [(222, y * 0.99, 168), (240, y * 0.99, 160), (236, y * 0.99, 168)][::sgn], (0, -sgn, 0), lambda q: (0, 0))
        # seats
        sy = sgn * 52
        b.box("CAB_Seat", (78, sy, 92), (62, 52, 26)); b.box("CAB_Seat", (78, sy, 74), (40, 30, 14))
        tilt = math.radians(14); M = np.array([[math.cos(tilt), 0, math.sin(tilt)], [0, 1, 0], [-math.sin(tilt), 0, math.cos(tilt)]])
        b.box("CAB_Seat", (40, sy, 150), (14, 52, 92), M=M); b.box("CAB_Seat", (30, sy, 205), (12, 30, 22), M=M)
        b.rod("CAB_Metal", (32, sy - 8, 193), (34, sy - 8, 200), 0.8); b.rod("CAB_Metal", (32, sy + 8, 193), (34, sy + 8, 200), 0.8)
    # dashboard
    b.extrude("CAB_Dash", [(196, 112), (300, 112), (300, 156), (238, 162), (205, 158), (192, 136)], -106, 106)
    b.box("CAB_Dash", (265, 0, 90), (70, 212, 44))
    b.box("CAB_Dash", (180, 0, 98), (60, 40, 70))   # centre console
    # steering wheel (left seat)
    ax = nrm([-1.0, 0, 0.55])
    b.torus("CAB_Dark", (200, -52, 150), ax, 18, 2.2, seg=40, seg2=10)
    b.rod("CAB_Dark", (200, -52, 150), (232, -52, 133), 3.5); b.rod("CAB_Dark", (200, -52, 150), (200, -52 + 17, 150 + 0), 1.2); b.rod("CAB_Dark", (200, -52, 150), (200, -52 - 17, 150), 1.2)
    # monitors: dash centre, header left, right wall
    def monitor(name, c, w, h, face, up=(0, 0, 1)):
        face = nrm(face); upv = np.asarray(up, float); vdir = -face
        ir = nrm(np.cross(upv, vdir))                       # image right for a viewer looking along vdir (Unreal: right = up x forward)
        down = -nrm(upv - face * np.dot(upv, face))
        b.quad(name, np.asarray(c, float) + face * 1.6, ir, down, w, h, n=face)
        M = np.stack([face, ir, -down], 1)
        b.box("CAB_Dark", c, (3, w + 3, h + 3), M=M)
    monitor("CAB_Mon1", (222, 62, 172), 30, 19, nrm([-1, -0.3, 0.35]))
    monitor("CAB_Mon2", (150, -72, 226), 30, 19, nrm([-1, 0.5, -0.3]))
    monitor("CAB_Mon3", (120, 100, 200), 32, 20, nrm([-0.6, -1, 0]))
    b.rod("CAB_Dark", (150, -72, 236), (150, -72, 245), 1.2)
    # cables
    for (p0, p1, sag) in (((222, 62, 160), (150, 80, 244), 14), ((150, -72, 216), (60, -100, 245), 12), ((120, 100, 190), (40, 108, 150), 10)):
        p0 = np.array(p0, float); p1 = np.array(p1, float); pts = [p0 + (p1 - p0) * t - np.array([0, 0, sag * math.sin(math.pi * t)]) for t in np.linspace(0, 1, 9)]
        for a_, c_ in zip(pts[:-1], pts[1:]): b.rod("CAB_Cable", a_, c_, 0.9, seg=6)
    # gear rack behind the seats (seen in the coffee shot)
    b.box("CAB_Dark", (-120, 0, 150), (40, 160, 170))
    for k in range(5): b.box("CAB_Metal", (-99, 0, 85 + k * 32), (1, 150, 24))
    b.write("cab.glb")

# ======================================================================= props, effects, sky, ground
def props():
    b = Bank()
    # coffee cup (axis +Z, origin at its centre)
    b.revolve("PROP_Cup", [(-5.5, 0), (-5.5, 4.2), (5.5, 4.4), (5.5, 4.0), (-4.5, 3.8), (-4.5, 0)], M=np.stack([[0, 0, 1.0], [1.0, 0, 0], [0, 1.0, 0]], 1), seg=40)
    b.revolve("PROP_CupRed", [(1.0, 4.35), (3.0, 4.42)], M=np.stack([[0, 0, 1.0], [1.0, 0, 0], [0, 1.0, 0]], 1), seg=40)
    b.torus("PROP_Cup", (0, 4.6, 0.5), (1, 0, 0), 2.7, 0.65, seg=20, seg2=8, arc=180, up=(0, 1, 0))
    b.revolve("PROP_Coffee", [(2.2, 0), (2.2, 3.85)], M=np.stack([[0, 0, 1.0], [1.0, 0, 0], [0, 1.0, 0]], 1), seg=40, nrmprof=[(1, 0), (1, 0)])
    # coffee blob (floating droplet)
    b.revolve("PROP_Coffee", [(-1.6 * math.cos(a), 1.6 * math.sin(a)) for a in np.linspace(0, math.pi, 12)], origin=(0, 0, 0), seg=16)
    # newspaper (faces -X; image right = +Y, image down = -Z), gently curled
    W, H = 38.0, 52.0; nu, nv = 16, 20; V, N, UV, T = [], [], [], []
    for j in range(nv + 1):
        for i in range(nu + 1):
            u, v = i / nu, j / nv; y = (u - 0.5) * W; z = (0.5 - v) * H; x = 3.0 * math.sin(math.pi * u) + 1.5 * (v - 0.5) ** 2 * 4
            V.append((x, y, z)); UV.append((u, v)); N.append((-1, -3.0 * math.pi / W * math.cos(math.pi * u) * 0, 0))
    for j in range(nv):
        for i in range(nu):
            a = j * (nu + 1) + i; T += [(a, a + 1, a + nu + 2), (a, a + nu + 2, a + nu + 1)]
    b.add("PROP_Paper", V, N, UV, T)
    # crumpled paper ball
    V, N, UV, T = [], [], [], []; nl, na = 20, 32
    noise = rng.normal(0, 1, (nl + 1, na + 1))
    for j in range(nl + 1):
        for i in range(na + 1):
            th = math.pi * j / nl; ph = 2 * math.pi * i / na; r = 9 * (1 + 0.07 * noise[j, i % na if i == na else i])
            p = np.array([math.sin(th) * math.cos(ph), math.sin(th) * math.sin(ph), math.cos(th)]); V.append(p * r); N.append(p); UV.append((i / na, j / nl))
    for j in range(nl):
        for i in range(na):
            a = j * (na + 1) + i; T += [(a, a + 1, a + na + 2), (a, a + na + 2, a + na + 1)]
    b.add("PROP_Ball", V, N, UV, T)
    # flame (origin at the nozzle exit, pointing -X); v runs 0 (nozzle) -> 1 (tip)
    ts = np.linspace(0, 1, 24)
    b.revolve("FX_Flame", [(-420 * t, 34 * (1 - t) ** 0.8 * (1 + 0.35 * math.sin(math.pi * t))) for t in ts], seg=32)
    b.revolve("FX_FlameCore", [(-200 * t, 22 * (1 - t) ** 0.9) for t in ts], seg=24)
    # radio ring (around X) and arrow (along +X)
    b.torus("FX_Ring", (0, 0, 0), (1, 0, 0), 100, 2.0, seg=72, seg2=8)
    b.cyl("FX_Arrow", (0, 0, 0), (46, 0, 0), 2.4, seg=12); b.cyl("FX_Arrow", (46, 0, 0), (66, 0, 0), 7, 0.0, seg=16)
    # smoke puff: lumpy sphere
    V, N, UV, T = [], [], [], []; nl, na = 12, 18; noise = rng.normal(0, 1, (nl + 1, na))
    for j in range(nl + 1):
        for i in range(na + 1):
            th = math.pi * j / nl; ph = 2 * math.pi * i / na; r = 100 * (1 + 0.12 * noise[j, i % na])
            p = np.array([math.sin(th) * math.cos(ph), math.sin(th) * math.sin(ph), math.cos(th)]); V.append(p * r); N.append(p); UV.append((i / na, j / nl))
    for j in range(nl):
        for i in range(na):
            a = j * (na + 1) + i; T += [(a, a + 1, a + na + 2), (a, a + na + 2, a + na + 1)]
    b.add("FX_Smoke", V, N, UV, T)
    b.write("props.glb")

def sky():
    b = Bank(); R = 5.0e6
    def star(name, d, size):
        d = nrm(d); M = basis(d); u = M[:, 1]; v = -M[:, 2]
        b.quad(name, d * R, u, v, size, size, n=-d)
    allp = []
    for k in range(5200):
        d = rng.normal(0, 1, 3)
        if k > 3400:           # a faint band (our sky's 'Milky Way'), tilted
            th = rng.uniform(0, 2 * math.pi); d = np.array([math.cos(th), math.sin(th), rng.normal(0, 0.09)])
            M = np.array([[1, 0, 0], [0, math.cos(1.0), -math.sin(1.0)], [0, math.sin(1.0), math.cos(1.0)]]); d = M @ d
        m = rng.random()
        grp = "B" if m > 0.985 else ("M" if m > 0.86 else "D")
        tint = "b" if rng.random() < 0.45 else "w"
        size = {"D": 7000, "M": 9500, "B": 14000}[grp] * rng.uniform(0.8, 1.2)
        star("SKY_S%s%s" % (grp, tint), d, size)
    b.quad("SKY_Quad", (0, 0, 0), (0, 1, 0), (0, 0, -1), 100, 100, n=(-1, 0, 0))
    # dome (normals inward), v = 0 at the zenith
    V, N, UV, T = [], [], [], []; nl, na = 48, 64
    for j in range(nl + 1):
        for i in range(na + 1):
            th = math.pi * j / nl; ph = 2 * math.pi * i / na
            p = np.array([math.sin(th) * math.cos(ph), math.sin(th) * math.sin(ph), math.cos(th)]); V.append(p * 100); N.append(-p); UV.append((i / na, j / nl))
    for j in range(nl):
        for i in range(na):
            a = j * (na + 1) + i; T += [(a, a + 1, a + na + 2), (a, a + na + 2, a + na + 1)]
    b.add("SKY_Dome", V, N, UV, T)
    b.write("sky.glb")

def ground():
    b = Bank()
    b.quad("GND_Lot", (0, 0, 0), (1, 0, 0), (0, 1, 0), 12000, 12000, n=(0, 0, 1))
    b.quad("GND_Grass", (0, 0, -3), (1, 0, 0), (0, 1, 0), 600000, 600000, n=(0, 0, 1), uv=((0, 0), (300, 300)))
    # station building
    bx, by, bw, bd, bh = -3500.0, 3300.0, 3200.0, 2000.0, 900.0
    b.box("GND_Wall", (bx, by, bh / 2), (bw, bd, bh), uvs=400)
    b.box("GND_Dark", (bx, by, bh + 15), (bw + 40, bd + 40, 30))
    b.quad("GND_Glass", (bx, by - bd / 2 - 1, 330), (-1, 0, 0), (0, 0, -1), bw - 300, 320, n=(0, -1, 0), uv=((0, 0), (8, 1)))
    b.quad("GND_Sign", (bx, by - bd / 2 - 2, 680), (-1, 0, 0), (0, 0, -1), 2400, 300, n=(0, -1, 0))
    b.box("GND_Dark", (bx + 900, by - bd / 2 - 20, 150), (300, 40, 300))
    # station roof dish aimed at the truck
    sd = np.array([bx + 800, by - 300, bh + 260.0]); aim = nrm(np.array([0, 0, 330.0]) - sd); M = basis(aim)
    R, Dp = 220.0, 50.0; f = R * R / (4 * Dp); rs = np.linspace(0, R, 24)
    b.revolve("GND_Dish", [(q * q / (4 * f), q) for q in rs], origin=sd, M=M, seg=64, nrmprof=[(1, -q / (2 * f)) for q in rs])
    b.revolve("GND_Dish", [(q * q / (4 * f) - 3, q) for q in rs], origin=sd, M=M, seg=64, nrmprof=[(-1, q / (2 * f)) for q in rs])
    b.cyl("GND_Metal", sd - M[:, 0] * 10, (sd[0], sd[1], bh + 30), 18)
    # light poles + parked cars + trees
    for x in (-3000, 0, 3000):
        for y in (-2500, 1200):
            b.cyl("GND_Metal", (x, y, 0), (x, y, 900), 9, 7); b.box("GND_Metal", (x + 60, y, 900), (140, 40, 20)); b.box("GND_Lamp", (x + 90, y, 889), (70, 26, 3))
    cars = [(-2600, -2000, "GND_Car1"), (-1900, -2000, "GND_Car2"), (1800, -2000, "GND_Car3"), (2500, -2000, "GND_Car1"), (-800, 1700, "GND_Car4"), (900, 1700, "GND_Car2"), (2200, 1700, "GND_Car3")]
    for x, y, m in cars:
        b.box(m, (x, y, 80), (180, 440, 90)); b.box(m, (x, y + 20, 150), (165, 230, 60)); b.box("GND_Dark", (x, y + 20, 150), (167, 200, 50))
        for dy in (-140, 140):
            for dx in (-80, 80): b.cyl("GND_Dark", (x + dx - 8, y + dy, 33), (x + dx + 8, y + dy, 33), 33, seg=16)
    for k in range(160):
        a = rng.uniform(0, 2 * math.pi); r = rng.uniform(9000, 16000); x, y = r * math.cos(a), r * math.sin(a); h = rng.uniform(700, 1400)
        b.cyl("GND_Tree", (x, y, h * 0.15), (x, y, h), h * 0.32, 0.0, seg=10); b.cyl("GND_Dark", (x, y, 0), (x, y, h * 0.2), 25, seg=6, caps=False)
    b.write("ground.glb")

if __name__ == "__main__":
    for fn in (pioneer, truck, cab, props, sky, ground): fn()
