# Heartbeat TV Science 8.10 "Antarctica, Part 2: the sky in the ice". Pure-script Blender 5.1 scene, no downloaded assets (ep7 pipeline).
# Cycles OptiX on the RTX 4060.
#   blender -b -P build.py -- [--stills DIR --frames a,b,c] [--anim OUTDIR [--step 2] [--ranges a-b,c-d]] [--samples N]
import bpy, bmesh, math, random, sys, os, time
import numpy as np
from mathutils import Vector, Matrix, noise

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from shots import SHOTS, FPS
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def arg(k, d=None): return argv[argv.index(k) + 1] if k in argv else d
random.seed(7); np.random.seed(7)

DUR = sum(int(round(s["dur"] * FPS)) for s in SHOTS)
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.fps = FPS; sc.frame_start, sc.frame_end = 1, DUR

# ---------------------------------------------------------------- render
sc.render.engine = "CYCLES"
prefs = bpy.context.preferences.addons["cycles"].preferences
prefs.compute_device_type = "OPTIX"; prefs.get_devices()
for d in prefs.devices: d.use = d.type == "OPTIX"
sc.cycles.device = "CPU" if "--cpu" in argv else "GPU"
sc.cycles.samples = int(arg("--samples", "40")); sc.cycles.use_adaptive_sampling = True; sc.cycles.adaptive_threshold = 0.04
sc.cycles.use_denoising = True; sc.cycles.denoiser = "OPENIMAGEDENOISE" if "--cpu" in argv else "OPTIX"
sc.cycles.max_bounces = 40; sc.cycles.diffuse_bounces = 2; sc.cycles.glossy_bounces = 6; sc.cycles.transmission_bounces = 40
sc.cycles.volume_bounces = 0; sc.cycles.transparent_max_bounces = 12
sc.cycles.caustics_reflective = False; sc.cycles.caustics_refractive = False
sc.cycles.blur_glossy = 1.0; sc.cycles.sample_clamp_indirect = 6.0
sc.cycles.volume_step_rate = 4.0
sc.render.resolution_x, sc.render.resolution_y = int(arg("--w", "1280")), int(arg("--h", "720")); sc.render.resolution_percentage = 100
sc.render.use_motion_blur = False
sc.view_settings.view_transform = "AgX"
try: sc.view_settings.look = "AgX - Medium High Contrast"
except Exception: pass
sc.view_settings.exposure = float(arg("--exp", "0.0"))
sc.render.image_settings.file_format = "PNG"; sc.render.image_settings.color_mode = "RGB"

# ---------------------------------------------------------------- node helpers (same family as ep6)
def mat(name):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial"); out.name = "OUT"
    return m, nt
def N(nt, t, **kw):
    n = nt.nodes.new(t)
    for k, v in kw.items(): setattr(n, k, v)
    return n
def L(nt, a, b): nt.links.new(a, b)
def lk(x): return hasattr(x, "is_linked")
def M(nt, op, a, b=None, c=None):
    n = nt.nodes.new("ShaderNodeMath"); n.operation = op; n.use_clamp = False
    for i, x in enumerate((a, b, c)):
        if x is None: continue
        if lk(x): L(nt, x, n.inputs[i])
        else: n.inputs[i].default_value = x
    return n.outputs[0]
def MIXC(nt, fac, a, b, blend="MIX"):
    n = nt.nodes.new("ShaderNodeMix"); n.data_type = "RGBA"; n.blend_type = blend; n.clamp_factor = True
    for sock, x in ((n.inputs["Factor"], fac), (n.inputs[6], a), (n.inputs[7], b)):
        if lk(x): L(nt, x, sock)
        else: sock.default_value = x if (not isinstance(x, (tuple, list)) or len(x) == 4) else tuple(x) + (1,)
    return n.outputs[2]
def NOISE(nt, vec, scale, detail=3, rough=.5):
    n = N(nt, "ShaderNodeTexNoise"); n.inputs["Scale"].default_value = scale; n.inputs["Detail"].default_value = detail; n.inputs["Roughness"].default_value = rough
    L(nt, vec, n.inputs["Vector"]); return n.outputs["Fac"]
def VORO(nt, vec, scale, feat="F1", rnd=1.0):
    n = N(nt, "ShaderNodeTexVoronoi"); n.feature = feat; n.inputs["Scale"].default_value = scale; n.inputs["Randomness"].default_value = rnd
    L(nt, vec, n.inputs["Vector"]); return n
def SMOOTH(nt, x, a, b):
    n = N(nt, "ShaderNodeMapRange"); n.interpolation_type = "SMOOTHSTEP"
    n.inputs["From Min"].default_value = a; n.inputs["From Max"].default_value = b
    L(nt, x, n.inputs["Value"]); return n.outputs[0]
def finish(nt, shader): L(nt, shader, nt.nodes["OUT"].inputs["Surface"])
def principled(nt, color, rough, spec=.5, normal=None, metallic=0.0, trans=0.0, ior=1.45, sss=0.0, sss_r=(1, .5, .3), coat=0.0, alpha=None):
    b = N(nt, "ShaderNodeBsdfPrincipled")
    if lk(rough): L(nt, rough, b.inputs["Roughness"])
    else: b.inputs["Roughness"].default_value = rough
    if lk(color): L(nt, color, b.inputs["Base Color"])
    else: b.inputs["Base Color"].default_value = tuple(color) + (1,)
    b.inputs["Specular IOR Level"].default_value = spec
    if lk(metallic): L(nt, metallic, b.inputs["Metallic"])
    else: b.inputs["Metallic"].default_value = metallic
    b.inputs["Transmission Weight"].default_value = trans; b.inputs["IOR"].default_value = ior
    if sss: b.inputs["Subsurface Weight"].default_value = sss; b.inputs["Subsurface Radius"].default_value = sss_r; b.inputs["Subsurface Scale"].default_value = .05
    if coat: b.inputs["Coat Weight"].default_value = coat
    if alpha is not None: b.inputs["Alpha"].default_value = alpha
    if normal is not None: L(nt, normal, b.inputs["Normal"])
    return b
def BUMP(nt, height, strength, dist=1.0, normal=None):
    b = N(nt, "ShaderNodeBump"); b.inputs["Strength"].default_value = strength; b.inputs["Distance"].default_value = dist
    L(nt, height, b.inputs["Height"])
    if normal is not None: L(nt, normal, b.inputs["Normal"])
    return b.outputs[0]
def coords(nt):
    tc = N(nt, "ShaderNodeTexCoord"); return tc.outputs["Object"], tc.outputs["Generated"]
def SEP(nt, v):
    s = N(nt, "ShaderNodeSeparateXYZ"); L(nt, v, s.inputs[0]); return s.outputs
def VSCALE(nt, v, sx, sy, sz):
    n = N(nt, "ShaderNodeVectorMath"); n.operation = "MULTIPLY"; L(nt, v, n.inputs[0]); n.inputs[1].default_value = (sx, sy, sz); return n.outputs[0]
def EMIT(nt, col, s):
    e = N(nt, "ShaderNodeEmission"); e.inputs["Color"].default_value = tuple(col) + (1,); e.inputs["Strength"].default_value = s; return e

SETS = {}
def link(o, setname):
    sc.collection.objects.link(o); SETS.setdefault(setname, []).append(o); return o
def mesh_obj(name, verts, faces, setname, smooth=True):
    me = bpy.data.meshes.new(name); me.from_pydata(verts, [], faces); me.update()
    if smooth: me.polygons.foreach_set("use_smooth", [True] * len(me.polygons))
    return link(bpy.data.objects.new(name, me), setname)
def grid(name, sx, sy, nx, ny, hfun, setname, origin=(0, 0, 0)):
    xs = np.linspace(-sx / 2, sx / 2, nx + 1); ys = np.linspace(-sy / 2, sy / 2, ny + 1)
    X, Y = np.meshgrid(xs, ys); Z = np.broadcast_to(np.asarray(hfun(X, Y), dtype=float), X.shape)
    V = np.stack([X.ravel(), Y.ravel(), Z.ravel()], 1)
    F = []
    for j in range(ny):
        for i in range(nx):
            a = j * (nx + 1) + i; F.append((a, a + 1, a + nx + 2, a + nx + 1))
    o = mesh_obj(name, [tuple(v) for v in V], F, setname); o.location = origin; return o
def fbm2(X, Y, scale, oct=4, seed=0.0):
    X = np.asarray(X, dtype=float); Y = np.asarray(Y, dtype=float); out = np.zeros_like(X); a = 1.0; f = scale
    pts = np.stack([X.ravel(), Y.ravel()], 1)
    for _ in range(oct):
        out += a * np.array([noise.noise(Vector((x * f + seed, y * f - seed, seed * .37))) for x, y in pts]).reshape(X.shape)
        a *= .5; f *= 2.0
    return out
def blob(name, r, seed, setname, subdiv=4, amp=.35, nscale=1.6, squash=(1, 1, 1), flat_bottom=None):
    bm = bmesh.new(); bmesh.ops.create_icosphere(bm, subdivisions=subdiv, radius=1.0)
    for v in bm.verts:
        d = v.co.normalized()
        s = 1 + amp * noise.noise(d * nscale + Vector((seed, seed * .3, 1.7))) + amp * .35 * noise.noise(d * nscale * 3.1 + Vector((seed * 2, 0, 0)))
        v.co = Vector((d.x * r * squash[0] * s, d.y * r * squash[1] * s, d.z * r * squash[2] * s))
        if flat_bottom is not None and v.co.z < flat_bottom: v.co.z = flat_bottom
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    me.polygons.foreach_set("use_smooth", [True] * len(me.polygons)); me.update()
    return link(bpy.data.objects.new(name, me), setname)
def capsule(name, length, r, setname, segs=24, rings=12):
    bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=segs, v_segments=rings, radius=r)
    for v in bm.verts:
        if v.co.x > 1e-6: v.co.x += length / 2
        elif v.co.x < -1e-6: v.co.x -= length / 2
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    me.polygons.foreach_set("use_smooth", [True] * len(me.polygons)); me.update()
    return link(bpy.data.objects.new(name, me), setname)
def prim_cyl(name, r, depth, setname, verts=48, loc=(0, 0, 0), rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=depth, vertices=verts, location=loc, rotation=rot)
    o = bpy.context.object; o.name = name
    for c in o.users_collection: c.objects.unlink(o)
    return link(o, setname)
def prim_box(name, size, setname, loc=(0, 0, 0), rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot); o = bpy.context.object; o.name = name
    o.data.transform(Matrix.Diagonal(Vector(size)).to_4x4())
    for c in o.users_collection: c.objects.unlink(o)
    return link(o, setname)
def bevel(o, w, seg=3):
    m = o.modifiers.new("bev", "BEVEL"); m.width = w; m.segments = seg; m.limit_method = "ANGLE"; return m
def add_light(name, kind, setname, loc, energy, color=(1, 1, 1), size=1.0, rot=None, target=None, spot=None):
    ld = bpy.data.lights.new(name, kind); ld.energy = energy; ld.color = color
    if kind == "AREA": ld.size = size
    if kind in ("POINT", "SPOT"): ld.shadow_soft_size = size
    if kind == "SPOT" and spot: ld.spot_size = math.radians(spot); ld.spot_blend = .6
    o = bpy.data.objects.new(name, ld); link(o, setname); o.location = loc
    if target is not None: o.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    elif rot is not None: o.rotation_euler = rot
    return o
def scatter_instances(name, src, pts, scales, setname, rots=None):
    """one object per point (as linked duplicates of src's mesh)"""
    out = []
    for i, p in enumerate(pts):
        o = bpy.data.objects.new("%s%04d" % (name, i), src.data); link(o, setname); o.location = p
        s = scales[i]; o.scale = (s, s, s) if not isinstance(s, (tuple, list)) else s
        if rots is not None: o.rotation_euler = rots[i]
        out.append(o)
    return out


def give(o, m): o.data.materials.append(m); return o
def plastic(name, col, rough=.45, coat=0.0):
    m, nt = mat(name); ob, gen = coords(nt); h = NOISE(nt, ob, 400.0, 3)
    b = principled(nt, col, M(nt, "ADD", M(nt, "MULTIPLY", h, .1), rough), coat=coat, normal=BUMP(nt, h, .05, .001)); finish(nt, b.outputs[0]); return m
def metal(name, col, rough=.25):
    m, nt = mat(name); ob, gen = coords(nt); h = NOISE(nt, ob, 900.0, 4)
    b = principled(nt, col, M(nt, "ADD", M(nt, "MULTIPLY", h, .12), rough), metallic=1.0); finish(nt, b.outputs[0]); return m
def painted(name, col, rough=.3):
    m, nt = mat(name); b = principled(nt, col, rough, coat=.6); finish(nt, b.outputs[0]); return m
def floor_mat(name, c1, c2, scale, rough=.8, bump=.3):
    m, nt = mat(name); ob, gen = coords(nt); h = NOISE(nt, ob, scale, 8, .6)
    col = MIXC(nt, h, c1, c2); b = principled(nt, col, rough, normal=BUMP(nt, h, bump, .02)); finish(nt, b.outputs[0]); return m
def EMITM(name, col, s):
    m, nt = mat(name); e = EMIT(nt, col, s); finish(nt, e.outputs[0]); return m
def text_obj(name, body, size, setname, loc, rot=(0, 0, 0), m=None, extrude=0.0):
    cu = bpy.data.curves.new(name, "FONT"); cu.body = body; cu.size = size; cu.align_x = "CENTER"; cu.align_y = "CENTER"; cu.extrude = extrude
    o = bpy.data.objects.new(name, cu); link(o, setname); o.location = loc; o.rotation_euler = rot
    if m: cu.materials.append(m)
    return o
def curve_obj(name, pts, r, setname, m=None, res=12):
    cu = bpy.data.curves.new(name, "CURVE"); cu.dimensions = "3D"; cu.bevel_depth = r; cu.bevel_resolution = 4; cu.resolution_u = res
    sp = cu.splines.new("NURBS"); sp.points.add(len(pts) - 1)
    for i, p in enumerate(pts): sp.points[i].co = (p[0], p[1], p[2], 1)
    sp.use_endpoint_u = True; sp.order_u = min(4, len(pts))
    o = bpy.data.objects.new(name, cu); link(o, setname)
    if m: cu.materials.append(m)
    return o
def helix(name, r, wire, turns, length, setname, loc, m, axis="Z"):
    pts = []
    n = int(turns * 24)
    for i in range(n + 1):
        a_ = 2 * math.pi * i / 24; z = length * i / n
        pts.append((r * math.cos(a_), r * math.sin(a_), z))
    o = curve_obj(name, pts, wire, setname, m, 4); o.location = loc
    if axis == "X": o.rotation_euler = (0, math.pi / 2, 0)
    return o

M_ALU = metal("Alu", (.78, .78, .8), .28); M_STEEL = metal("Steel", (.6, .6, .62), .3); M_CHROME = metal("Chrome", (.9, .9, .92), .08)
M_BLACK = plastic("BlackPl", (.012, .012, .014), .4); M_GREEN = plastic("GreenPl", (.02, .25, .06), .45); M_RUBBER = plastic("Rubber", (.02, .02, .022), .7)
M_GOLD = metal("Gold", (1.0, .76, .36), .18)

# ================================================================ Science 8.10 "Antarctica Part 2: the sky in the ice"
# Generic scenes built from primitives in code (no downloaded assets); every one is labelled ILLUSTRATION on screen.  1 unit = 1 m.
#   FIELD  a flat polar snow plateau under a low sun (generic, not a real site); a few falling ice crystals for "it starts as snow"
#   CORE   a cold-room bench: a clear ice core with air bubbles lying in a foam cradle; hairline cracks grow (brittle ice)
#   LAB    a lab bench: a small ice piece beside three sugar cubes for scale; a laser beam turns the ice to vapor; a gas readout
#   GLASS  a glass of water with a chunk of glacier-style ice; bubbles stream out as it melts (generic, no brand)
#   CAPE   a windy coastal headland with a small white air station, an intake mast and steel cylinders (generic, not Cape Grim)
#   SHELF  an archive store room: rows of air cylinders, one old olive-drab cylinder, and an old scuba tank on a shelf
#   JAR    a jar with a lid and a dated paper tag on an outdoor wooden table
ORG = {"CORE": Vector((0, 0, 0)), "LAB": Vector((50, 0, 0)), "GLASS": Vector((100, 0, 0)), "SHELF": Vector((150, 0, 0)),
       "JAR": Vector((0, 3000, 0)), "CAPE": Vector((0, 20000, 0)), "FIELD": Vector((10000, 0, 0))}
LINEAR_ANIM = set(); SMOOTH_ANIM = set()

def lathe(name, prof, setname, segs=64, cap_top=False):
    """revolve a closed (r, z) profile around Z"""
    V = []; F = []; n = len(prof)
    for i in range(segs):
        a_ = 2 * math.pi * i / segs
        for r, z in prof: V.append((r * math.cos(a_), r * math.sin(a_), z))
    for i in range(segs):
        i2 = (i + 1) % segs
        for k in range(n - 1):
            F.append((i * n + k, i2 * n + k, i2 * n + k + 1, i * n + k + 1))
        F.append((i * n + n - 1, i2 * n + n - 1, i2 * n, i * n))
    o = mesh_obj(name, V, F, setname)
    bm = bmesh.new(); bm.from_mesh(o.data); bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-6)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces); bm.to_mesh(o.data); bm.free(); o.data.update()
    return o

def glass_mat(name, ior=1.5, col=(1, 1, 1), rough=0.0):
    m, nt = mat(name); b = principled(nt, col, rough, trans=1.0, ior=ior); finish(nt, b.outputs[0]); return m
def ice_mat(name, rough=.04, frost=0.0):
    m, nt = mat(name); ob, gen = coords(nt); h = NOISE(nt, ob, 60.0, 5, .6)
    r = M(nt, "ADD", M(nt, "MULTIPLY", h, .08 + frost), rough)
    b = principled(nt, (.86, .93, 1.0), r, trans=1.0, ior=1.31, normal=BUMP(nt, h, .04 + frost, .002)); finish(nt, b.outputs[0]); return m
def snow_mat(name, scale=1.0):
    m, nt = mat(name); ob, gen = coords(nt)
    v = VORO(nt, ob, 900.0 * scale); h1 = NOISE(nt, ob, 3.0 * scale, 6, .6); h2 = NOISE(nt, ob, 40.0 * scale, 4, .5)
    hh = M(nt, "ADD", M(nt, "MULTIPLY", v.outputs["Distance"], .4), M(nt, "ADD", h1, M(nt, "MULTIPLY", h2, .5)))
    col = MIXC(nt, h1, (.86, .9, .96), (.97, .975, .985))
    b = principled(nt, col, .5, sss=.25, sss_r=(.4, .6, 1.0), normal=BUMP(nt, hh, .5, .05)); finish(nt, b.outputs[0]); return m
def wood_mat(name, c1, c2, scale=8.0):
    m, nt = mat(name); ob, gen = coords(nt)
    st = VSCALE(nt, ob, 1.0, 30.0, 1.0); h = NOISE(nt, st, scale, 6, .6)
    col = MIXC(nt, h, c1, c2); b = principled(nt, col, .5, normal=BUMP(nt, h, .2, .002)); finish(nt, b.outputs[0]); return m
def foam_mat(name, col):
    m, nt = mat(name); ob, gen = coords(nt); h = NOISE(nt, ob, 500.0, 4)
    b = principled(nt, col, .9, normal=BUMP(nt, h, .2, .001), sss=.1); finish(nt, b.outputs[0]); return m
def paper_mat(name):
    m, nt = mat(name); ob, gen = coords(nt); h = NOISE(nt, ob, 300.0, 5)
    col = MIXC(nt, h, (.86, .82, .72), (.93, .9, .82)); b = principled(nt, col, .85, normal=BUMP(nt, h, .1, .001)); finish(nt, b.outputs[0]); return m
def ink_mat(name, col=(.03, .04, .08)):
    m, nt = mat(name); b = principled(nt, col, .6); finish(nt, b.outputs[0]); return m

M_AIRB = glass_mat("AirBubble", 1.0 / 1.31)
M_WATER = glass_mat("Water", 1.333, (.95, .98, 1.0))
M_GLASS = glass_mat("Glass", 1.5, (.97, .99, .98))

# ================================================================ FIELD: polar plateau
o = ORG["FIELD"]
def plateau_h(X, Y):
    sast = .3 * fbm2(X * 1.0, Y * 4.0, .05, 4, 2.0)          # wind-carved ridges run across Y
    return sast + 1.2 * fbm2(X, Y, .002, 3, 5.0)
give(grid("Plateau", 900, 900, 260, 260, plateau_h, "FIELD", origin=o), snow_mat("Snow", 1.0))
def near_h(X, Y):   # sastrugi: wind-cut ridges, finer near the cameras
    return plateau_h(X, Y - 2.0) + .03 + .22 * np.abs(fbm2(X * .3, Y * 1.2, .6, 3, 8.0)) + .025 * fbm2(X, Y, 3.0, 2, 3.0)
give(grid("SnowNear", 40, 40, 320, 320, near_h, "FIELD", origin=o + Vector((0, -2, 0))), snow_mat("SnowFine", 3.0))
# falling ice crystals near the low camera (FIELD_B); one empty carries them down
flake_src = blob("FlakeSrc", .006, 1.0, "FIELD", 1, .25, 2.0, (1, 1, .3)); give(flake_src, foam_mat("Flake", (.95, .97, 1.0)))
FL = bpy.data.objects.new("Flakes", None); link(FL, "FIELD"); FL.location = o + Vector((0, 0, 0))
z_near = float(plateau_h(np.array([0.0]), np.array([-2.0]))[0]) + .02
rs = random.Random(3); fl_pts = [o + Vector((rs.uniform(-.6, .6), rs.uniform(-3.5, -2.0), z_near + rs.uniform(.05, 1.7))) for _ in range(220)]
fls = scatter_instances("Fl", flake_src, fl_pts, [rs.uniform(.6, 1.4) for _ in fl_pts], "FIELD", [(rs.uniform(0, 3), rs.uniform(0, 3), rs.uniform(0, 3)) for _ in fl_pts])
for f_ in fls: f_.parent = FL; f_.location = f_.location - FL.location
flake_src.hide_render = True
LINEAR_ANIM.add(FL.name)

# ================================================================ CORE: ice core on a foam cradle in a cold room
o = ORG["CORE"]
give(prim_box("CoreTable", (1.6, .7, .04), "CORE", loc=o + Vector((0, 0, .78))), metal("TableSteel", (.55, .56, .58), .35))
give(prim_box("LightTable", (1.5, .5, .004), "CORE", loc=o + Vector((0, 0, .802))), EMITM("LightTableE", (.92, .96, 1.0), 2.5))
give(prim_box("CoreBack", (8, .1, 4), "CORE", loc=o + Vector((0, 1.4, 1.5))), plastic("ColdWall", (.42, .5, .58), .7))
give(grid("CoreFloor", 8, 8, 1, 1, lambda X, Y: X * 0, "CORE", origin=o), plastic("ColdFloor", (.1, .11, .13), .6))
M_FOAM = foam_mat("Foam", (.75, .8, .85))
CZ = .804 + .05
for x_ in (-.36, .36):   # small foam chocks hold the core on the light table
    for s_ in (-1, 1): give(prim_box("Chock%g%d" % (x_, s_), (.05, .03, .025), "CORE", loc=o + Vector((x_, s_ * .055, .804 + .0125))), M_FOAM)
core = give(prim_cyl("Core", .05, .8, "CORE", 96, loc=o + Vector((0, 0, CZ)), rot=(0, math.pi / 2, 0)), ice_mat("CoreIce", .03, .02))
core2 = give(prim_cyl("Core2", .05, .4, "CORE", 96, loc=o + Vector((.68, -.02, CZ)), rot=(0, math.pi / 2, math.radians(4))), ice_mat("CoreIce2", .05, .04))
for x_ in (.52, .84):
    for s_ in (-1, 1): give(prim_box("Chock2%g%d" % (x_, s_), (.05, .03, .025), "CORE", loc=o + Vector((x_, -.02 + s_ * .055, .804 + .0125)), rot=(0, 0, math.radians(4))), M_FOAM)
bub_src = blob("BubSrc", .001, 2.0, "CORE", 2, .08, 2.0, (1, 1, 1.25)); give(bub_src, M_AIRB)
rs = random.Random(11); bp = []; bsc = []
while len(bp) < 900:
    x = rs.uniform(-.39, .39); y = rs.uniform(-.045, .045); z = rs.uniform(-.045, .045)
    if y * y + z * z > .044 ** 2: continue
    bp.append(o + Vector((x, y, CZ + z))); bsc.append(rs.uniform(.35, 1.5) if rs.random() > .1 else rs.uniform(1.5, 2.6))
scatter_instances("Bub", bub_src, bp, bsc, "CORE", [(rs.uniform(0, 3), rs.uniform(0, 3), rs.uniform(0, 3)) for _ in bp])
bub_src.hide_render = True
CRACKS = []
M_CRACK = mat("CrackM"); _b = principled(M_CRACK[1], (.9, .93, .97), .25, trans=0.0); finish(M_CRACK[1], _b.outputs[0]); M_CRACK = M_CRACK[0]
for k, (x, ang, r_) in enumerate(((-.16, 18, .042), (.05, -25, .045), (.21, 32, .04), (-.30, -12, .038))):
    c_ = give(prim_cyl("Crack%d" % k, r_, .00015, "CORE", 48, loc=o + Vector((x, 0, CZ)), rot=(math.radians(ang), math.radians(90 + ang * .6), 0)), M_CRACK)
    CRACKS.append(c_); SMOOTH_ANIM.add(c_.name)
add_light("CoreTop", "AREA", "CORE", o + Vector((0, -.3, 2.0)), 120, (.85, .92, 1.0), 1.2, target=o + Vector((0, 0, CZ)))
add_light("CoreRim", "AREA", "CORE", o + Vector((.2, .9, 1.1)), 90, (.75, .85, 1.0), .6, target=o + Vector((0, 0, CZ)))
add_light("CoreUnder", "AREA", "CORE", o + Vector((-.6, -.4, .95)), 12, (1.0, .9, .8), .3, target=o + Vector((0, 0, CZ)))

# ================================================================ LAB: ice piece, sugar cubes, laser, readout
o = ORG["LAB"]
give(prim_box("LabBench", (1.4, .8, .04), "LAB", loc=o + Vector((0, 0, .88))), floor_mat("Slate", (.08, .085, .09), (.12, .125, .13), 30.0, .55, .05))
give(prim_box("LabBack", (6, .1, 3), "LAB", loc=o + Vector((0, .7, 1.4))), plastic("LabWall", (.5, .52, .54), .8))
BZ = .90
plate = give(prim_cyl("LabPlate", .03, .004, "LAB", 64, loc=o + Vector((0, 0, BZ + .002))), M_STEEL)
icep = give(blob("IcePiece", .0135, 4.0, "LAB", 4, .18, 2.2, (1.05, .95, .8), flat_bottom=-.009), ice_mat("IcePieceM", .05, .06))
icep.location = o + Vector((0, 0, BZ + .004 + .009)); SMOOTH_ANIM.add(icep.name)
M_SUGAR = foam_mat("Sugar", (.93, .92, .9))
for k in range(3):
    sc_ = give(prim_box("Sugar%d" % k, (.016, .016, .016), "LAB", loc=o + Vector((.06 + k * .02, -.012 + (k % 2) * .006, BZ + .008)), rot=(0, 0, math.radians(rs.uniform(-12, 12)))), M_SUGAR)
    bevel(sc_, .0012, 2)
head_ = give(prim_cyl("LaserHead", .012, .06, "LAB", 48, loc=o + Vector((0, 0, BZ + .16))), M_BLACK)
give(prim_cyl("LaserLens", .006, .004, "LAB", 32, loc=o + Vector((0, 0, BZ + .128))), M_CHROME)
give(prim_box("LaserArm", (.012, .2, .012), "LAB", loc=o + Vector((0, .1, BZ + .17))), M_ALU)
give(prim_cyl("LaserPost", .008, .3, "LAB", 24, loc=o + Vector((0, .2, BZ + .03))), M_ALU)
beam = give(prim_cyl("Beam", .0007, .12, "LAB", 16, loc=o + Vector((0, 0, BZ + .067))), EMITM("BeamE", (1.0, .12, .08), 60))
glow = add_light("BeamGlow", "POINT", "LAB", o + Vector((0, 0, BZ + .02)), 0.0, (1.0, .35, .2), .003)
scr_ = give(prim_box("Readout", (.22, .015, .13), "LAB", loc=o + Vector((-.17, .12, BZ + .1)), rot=(math.radians(-8), 0, math.radians(12))), M_BLACK)
M_SCR = EMITM("ReadoutE", (.06, .12, .1), 1.0); M_TXT = EMITM("ReadoutT", (.55, 1.0, .7), 3.0)
give(prim_box("ReadoutGlass", (.2, .002, .11), "LAB", loc=o + Vector((-.17, .112, BZ + .1)), rot=(math.radians(-8), 0, math.radians(12))), M_SCR)
for k, t_ in enumerate(("CO2", "CH4", "N2O")):
    txo = text_obj("RdT%d" % k, t_, .022, "LAB", o + Vector((-.215, .109, BZ + .135 - k * .032)), (math.radians(82), 0, math.radians(12)), M_TXT)
    txo.data.align_x = "LEFT"
    give(prim_box("RdBar%d" % k, (.07 * (1 - .2 * k), .001, .008), "LAB", loc=o + Vector((-.125, .108, BZ + .136 - k * .032)), rot=(math.radians(-8), 0, math.radians(12))), M_TXT)
add_light("LabKey", "AREA", "LAB", o + Vector((-.3, -.5, 1.4)), 40, (1, .97, .92), .8, target=o + Vector((0, 0, BZ)))
add_light("LabRim", "AREA", "LAB", o + Vector((.4, .4, 1.2)), 25, (.8, .88, 1.0), .5, target=o + Vector((0, 0, BZ)))

# ================================================================ GLASS: a glass of water with glacier-style ice, bubbles streaming
o = ORG["GLASS"]
give(prim_box("Bar", (1.6, .7, .04), "GLASS", loc=o + Vector((0, 0, .98))), wood_mat("BarWood", (.12, .06, .03), (.22, .12, .06), 6.0))
give(prim_box("BarBack", (6, .1, 3), "GLASS", loc=o + Vector((0, 1.0, 1.5))), plastic("BarWall", (.3, .22, .15), .8))
GZ = 1.0
tumbler = give(prim_cyl("Tumbler", .041, .11, "GLASS", 96, loc=o + Vector((0, 0, GZ + .055))), M_GLASS)
bm = bmesh.new(); bm.from_mesh(tumbler.data)
bmesh.ops.delete(bm, geom=[f_ for f_ in bm.faces if f_.normal.z > .9], context="FACES"); bm.to_mesh(tumbler.data); bm.free()
so = tumbler.modifiers.new("solid", "SOLIDIFY"); so.thickness = .0026; so.offset = -1.0; so.use_even_offset = True
tumbler.data.polygons.foreach_set("use_smooth", [True] * len(tumbler.data.polygons))
bev_ = tumbler.modifiers.new("bev", "BEVEL"); bev_.width = .0008; bev_.segments = 2; bev_.limit_method = "ANGLE"
water = give(prim_cyl("WaterIn", .0381, .0752, "GLASS", 96, loc=o + Vector((0, 0, GZ + .0028 + .0376))), M_WATER)
gice = give(blob("GlassIce", .021, 7.0, "GLASS", 4, .22, 1.8, (1.1, .9, .95)), ice_mat("GlassIceM", .01, 0.0)); gice.location = o + Vector((.003, 0, GZ + .074))
rs = random.Random(21); gb = []
for k in range(40):   # a few bubbles trapped in the chunk
    p_ = Vector((rs.uniform(-.014, .014), rs.uniform(-.012, .012), rs.uniform(-.012, .012)))
    gb.append(o + Vector((.003, 0, GZ + .074)) + p_)
gbsrc = blob("GBSrc", .0008, 3.0, "GLASS", 2, .05, 2.0); give(gbsrc, M_AIRB)
scatter_instances("GB", gbsrc, gb, [rs.uniform(.5, 1.8) for _ in gb], "GLASS"); gbsrc.hide_render = True
RISERS = []
rsrc = blob("RiseSrc", .0007, 5.0, "GLASS", 2, .03, 2.0); give(rsrc, M_AIRB); rsrc.hide_render = True
for k in range(36):
    b_ = bpy.data.objects.new("Rise%02d" % k, rsrc.data); link(b_, "GLASS")
    b_.scale = (rs.uniform(.6, 1.4),) * 3; RISERS.append((b_, rs.uniform(-.012, .012), rs.uniform(-.01, .01), rs.uniform(0, 1), rs.uniform(1.4, 2.4)))
    LINEAR_ANIM.add(b_.name)
add_light("BarKey", "AREA", "GLASS", o + Vector((-.4, -.3, 1.5)), 30, (1.0, .9, .78), .5, target=o + Vector((0, 0, GZ + .06)))
add_light("BarBackL", "AREA", "GLASS", o + Vector((.1, .45, 1.15)), 25, (1.0, .85, .65), .3, target=o + Vector((0, 0, GZ + .06)))
give(prim_box("BarGlow", (1.4, .02, .5), "GLASS", loc=o + Vector((.05, .93, 1.2))), EMITM("BarGlowE", (1.0, .75, .5), 3.0))

# ================================================================ CAPE: coastal headland, small station, mast, cylinders
o = ORG["CAPE"]
def cape_h(X, Y):
    land = np.clip((60 - Y) / 25.0, 0, 1)                       # cliff edge near y = 60 .. 85 drops to the sea
    land = land * land * (3 - 2 * land)
    return -2 + land * (32 + 2.5 * fbm2(X, Y, .008, 3, 1.0)) + .5 * fbm2(X, Y, .1, 3, 4.0) * land
grid("Headland", 700, 500, 220, 180, cape_h, "CAPE", origin=o + Vector((0, -150, 0)))
hl = bpy.data.objects["Headland"]
m_, nt_ = mat("Grass"); ob_, gen_ = coords(nt_); h_ = NOISE(nt_, ob_, .4, 6, .6); h2_ = NOISE(nt_, ob_, 6.0, 4, .6)
col_ = MIXC(nt_, h_, (.16, .2, .07), (.34, .32, .16)); col_ = MIXC(nt_, SMOOTH(nt_, h2_, .62, .7), col_, (.3, .28, .25))
b_ = principled(nt_, col_, .9, normal=BUMP(nt_, M(nt_, "ADD", h2_, h_), .6, .3)); finish(nt_, b_.outputs[0]); hl.data.materials.append(m_)
sea = grid("Sea", 6000, 6000, 1, 1, lambda X, Y: X * 0, "CAPE", origin=o + Vector((0, 2800, 0)))
m_, nt_ = mat("SeaM"); ob_, gen_ = coords(nt_)
nz = N(nt_, "ShaderNodeTexNoise"); nz.noise_dimensions = "4D"; nz.inputs["Scale"].default_value = .25; nz.inputs["Detail"].default_value = 8
L(nt_, ob_, nz.inputs["Vector"]); SEA_W = nz.inputs["W"]
b_ = principled(nt_, (.01, .03, .05), .06, normal=BUMP(nt_, nz.outputs["Fac"], .5, .4)); finish(nt_, b_.outputs[0]); sea.data.materials.append(m_)
SEA_NT = nt_
def cape_z(x, y): return float(cape_h(np.array([x]), np.array([y + 150]))[0])
hx, hy = 0.0, -130.0; hz = cape_z(hx, hy)
M_WHITE = painted("StationWhite", (.8, .8, .78), .4)
hut = give(prim_box("Hut", (8, 5, 3), "CAPE", loc=o + Vector((hx, hy, hz + 1.3))), M_WHITE); bevel(hut, .05)
give(prim_box("HutRoof", (8.6, 5.6, .25), "CAPE", loc=o + Vector((hx, hy, hz + 2.9))), painted("Roof", (.25, .27, .3), .5))
give(prim_box("HutDoor", (1.0, .05, 2.0), "CAPE", loc=o + Vector((hx - 2, hy - 2.52, hz + .9))), painted("Door", (.2, .3, .4), .4))
for k in range(3): give(prim_box("HutWin%d" % k, (1.1, .05, .7), "CAPE", loc=o + Vector((hx + .3 + k * 1.5, hy - 2.52, hz + 1.8))), glass_mat("Win", 1.5, (.3, .35, .4), .1))
mast = give(prim_cyl("Mast", .12, 14, "CAPE", 24, loc=o + Vector((hx + 6, hy + 1, hz + 7))), M_STEEL)
give(prim_cyl("Intake", .25, .5, "CAPE", 24, loc=o + Vector((hx + 6, hy + 1, hz + 14.1))), M_STEEL)
curve_obj("IntakeLine", [tuple(o + Vector((hx + 6, hy + 1, hz + 13.8))), tuple(o + Vector((hx + 5.2, hy + .5, hz + 6))), tuple(o + Vector((hx + 4.1, hy, hz + 2.2)))], .04, "CAPE", M_BLACK)
for k in range(5):
    give(prim_cyl("CapeCyl%d" % k, .12, 1.3, "CAPE", 32, loc=o + Vector((hx - 5.5 + k * .3, hy - 3.2, hz + .65))), M_ALU)
    give(prim_cyl("CapeVal%d" % k, .03, .12, "CAPE", 16, loc=o + Vector((hx - 5.5 + k * .3, hy - 3.2, hz + 1.36))), M_CHROME)
give(prim_box("CylBase", (1.8, .5, .06), "CAPE", loc=o + Vector((hx - 4.9, hy - 3.2, hz - .02))), metal("RackSteel", (.3, .32, .35), .5))

# ================================================================ SHELF: archive store
o = ORG["SHELF"]
give(grid("StoreFloor", 14, 14, 1, 1, lambda X, Y: X * 0, "SHELF", origin=o), floor_mat("StoreConc", (.36, .35, .33), (.26, .25, .24), 3.0, .8, .15))
give(prim_box("StoreWall", (14, .1, 4), "SHELF", loc=o + Vector((0, 2.6, 2))), plastic("StoreWallM", (.55, .56, .55), .8))
M_RACK = painted("RackBlue", (.08, .16, .32), .45); M_ALU2 = metal("AluMatte", (.62, .63, .65), .5)
rs = random.Random(5)
for row in range(2):
    y0 = .8 + row * 1.2
    for x in (-3.6, 3.6):
        give(prim_box("Upr%d_%g" % (row, x), (.06, .5, 2.0), "SHELF", loc=o + Vector((x, y0, 1.0))), M_RACK)
    for lv in range(2):
        give(prim_box("Deck%d%d" % (row, lv), (7.3, .5, .04), "SHELF", loc=o + Vector((0, y0, .1 + lv * 1.05))), metal("Deck", (.5, .5, .52), .5))
        for k in range(16):
            x = -3.3 + k * .44
            h_c = .85
            give(prim_cyl("SC%d%d%02d" % (row, lv, k), .1, h_c, "SHELF", 32, loc=o + Vector((x, y0, .12 + lv * 1.05 + h_c / 2))), M_ALU2)
            give(prim_cyl("SV%d%d%02d" % (row, lv, k), .025, .08, "SHELF", 16, loc=o + Vector((x, y0, .12 + lv * 1.05 + h_c + .04))), M_CHROME)
            tg = give(prim_box("ST%d%d%02d" % (row, lv, k), (.07, .002, .04), "SHELF", loc=o + Vector((x, y0 - .101, .12 + lv * 1.05 + .55))), paper_mat("Tag%d" % (k % 3)))
# the old olive-drab cylinder on a low pallet in front
give(prim_box("Pallet", (.8, .6, .1), "SHELF", loc=o + Vector((-1.8, -.4, .05))), wood_mat("PalletW", (.35, .26, .16), (.5, .38, .24), 4.0))
od = give(capsule("OldCyl", .55, .14, "SHELF"), plastic("OliveDrab", (.045, .055, .02), .55, .2)); od.location = o + Vector((-1.8, -.4, .1 + .14))
give(prim_cyl("OldVal", .03, .1, "SHELF", 16, loc=o + Vector((-1.8 + .45, -.4, .1 + .14)), rot=(0, math.pi / 2, 0)), metal("Brass", (.75, .55, .25), .3))
# an old scuba tank on its own shelf to the right
give(prim_box("ScubaShelf", (.9, .45, .04), "SHELF", loc=o + Vector((4.6, 1.5, .9))), metal("Deck2", (.5, .5, .52), .5))
give(prim_box("ScubaLeg", (.05, .4, .9), "SHELF", loc=o + Vector((4.2, 1.5, .45))), M_RACK)
give(prim_box("ScubaLeg2", (.05, .4, .9), "SHELF", loc=o + Vector((5.0, 1.5, .45))), M_RACK)
sct = give(capsule("Scuba", .45, .09, "SHELF"), painted("ScubaYellow", (.55, .38, .04), .45)); sct.rotation_euler = (0, math.pi / 2, 0); sct.location = o + Vector((4.6, 1.5, 1.255))
give(prim_cyl("ScubaVal", .025, .09, "SHELF", 16, loc=o + Vector((4.6, 1.5, 1.61))), M_CHROME)
give(prim_cyl("ScubaKnob", .03, .02, "SHELF", 16, loc=o + Vector((4.6, 1.5, 1.66))), M_BLACK)
give(prim_box("ScubaTag", (.08, .002, .05), "SHELF", loc=o + Vector((4.6, 1.5 - .091, 1.25))), paper_mat("TagS"))
for k, x in enumerate((-3, 0, 3)):
    give(prim_box("StoreLamp%d" % k, (1.2, .15, .03), "SHELF", loc=o + Vector((x, .8, 3.3))), EMITM("LampE", (1, .98, .95), 12))
    add_light("StoreA%d" % k, "AREA", "SHELF", o + Vector((x, .3, 3.2)), 260, (.95, .97, 1.0), 1.0, rot=(0, 0, 0))
add_light("StoreFill", "AREA", "SHELF", o + Vector((0, -4, 1.6)), 120, (1, .95, .9), 3.0, target=o + Vector((0, 1, 1)))

# ================================================================ JAR: a jar with a dated tag on an outdoor table
o = ORG["JAR"]
JZ = .76
for k in range(6):
    give(prim_box("Plank%d" % k, (1.6, .145, .035), "JAR", loc=o + Vector((0, -.375 + k * .15, JZ - .018))), wood_mat("Plank%d" % (k % 2), (.33, .22, .13), (.45, .31, .19), 5.0 + k))
grid("Lawn", 200, 200, 80, 80, lambda X, Y: .2 * fbm2(X, Y, .05, 3, 6.0), "JAR", origin=o)
m_, nt_ = mat("LawnM"); ob_, gen_ = coords(nt_); h_ = NOISE(nt_, ob_, 2.0, 6, .6)
b_ = principled(nt_, MIXC(nt_, h_, (.08, .16, .04), (.2, .26, .08)), .85, normal=BUMP(nt_, h_, .5, .1)); finish(nt_, b_.outputs[0]); bpy.data.objects["Lawn"].data.materials.append(m_)
M_LEAF = plastic("Leaf", (.05, .13, .03), .8)
rs = random.Random(8)
for k in range(14):
    a_ = rs.uniform(-.9, .9) + math.pi / 2; d_ = rs.uniform(12, 30)
    bb = give(blob("Bush%d" % k, rs.uniform(1.5, 4), rs.uniform(0, 9), "JAR", 3, .3, 1.2, (1, 1, .8)), M_LEAF)
    bb.location = o + Vector((d_ * math.cos(a_), d_ * math.sin(a_), 1.0))
jar = lathe("Jar", [(0, 0), (.042, 0), (.045, .006), (.045, .1), (.036, .118), (.035, .13), (.032, .13), (.033, .118), (.042, .1), (.042, .006), (0, .004)], "JAR")
give(jar, M_GLASS); jar.location = o + Vector((0, 0, JZ))
lid = give(prim_cyl("JarLid", .038, .016, "JAR", 64, loc=o + Vector((0, 0, JZ + .134))), metal("LidMetal", (.7, .62, .45), .3)); bevel(lid, .002)
tag = give(prim_box("JarTag", (.09, .06, .0008), "JAR", loc=o + Vector((.1, -.07, JZ + .0005)), rot=(0, 0, math.radians(-14))), paper_mat("TagPaper"))
TR = Matrix.Rotation(math.radians(-14), 3, "Z")
for k, t_ in enumerate(("Air of ____", "Town: ______", "CO2 ___ ppm")):
    tt = text_obj("JarTxt%d" % k, t_, .0095, "JAR", o, (0, 0, math.radians(-14)), ink_mat("Ink"))
    tt.location = o + Vector((.1, -.07, JZ + .0011)) + TR @ Vector((0, .016 - k * .016, 0))
pencil = give(prim_cyl("Pencil", .0035, .15, "JAR", 6, loc=o + Vector((.17, .02, JZ + .0035)), rot=(0, math.pi / 2, math.radians(30))), painted("PencilY", (.8, .55, .05), .4))

# ================================================================ world: one low-sun sky for the outdoor sets, a dim grey for the rooms
w = bpy.data.worlds.new("World"); sc.world = w; w.use_nodes = True; wn = w.node_tree; wn.nodes.clear()
sky = wn.nodes.new("ShaderNodeTexSky"); sky.sky_type = "MULTIPLE_SCATTERING"
SUN_EL, SUN_ROT = 9.0, 100.0
try: sky.sun_elevation = math.radians(SUN_EL); sky.sun_rotation = math.radians(SUN_ROT); sky.altitude = 300.0; sky.sun_disc = False
except Exception as e: print("sky props", e)
vday = wn.nodes.new("ShaderNodeValue"); vgrey = wn.nodes.new("ShaderNodeValue")
def wmul(a, b):
    n = wn.nodes.new("ShaderNodeMath"); n.operation = "MULTIPLY"; wn.links.new(a, n.inputs[0]); n.inputs[1].default_value = b; return n.outputs[0]
bg_d = wn.nodes.new("ShaderNodeBackground"); wn.links.new(sky.outputs[0], bg_d.inputs["Color"]); wn.links.new(wmul(vday.outputs[0], .5), bg_d.inputs["Strength"])
bg_g = wn.nodes.new("ShaderNodeBackground"); bg_g.inputs["Color"].default_value = (.5, .52, .56, 1); wn.links.new(vgrey.outputs[0], bg_g.inputs["Strength"])
ad = wn.nodes.new("ShaderNodeAddShader"); wn.links.new(bg_d.outputs[0], ad.inputs[0]); wn.links.new(bg_g.outputs[0], ad.inputs[1])
wo_ = wn.nodes.new("ShaderNodeOutputWorld"); wn.links.new(ad.outputs[0], wo_.inputs["Surface"])
SUNV = Vector((math.sin(math.radians(SUN_ROT)) * math.cos(math.radians(SUN_EL)), math.cos(math.radians(SUN_ROT)) * math.cos(math.radians(SUN_EL)), math.sin(math.radians(SUN_EL))))
sun_d = bpy.data.lights.new("Sun", "SUN"); sun_d.angle = math.radians(.53); sun_d.color = (1.0, .86, .7)
sun = bpy.data.objects.new("Sun", sun_d); sc.collection.objects.link(sun); sun.rotation_euler = SUNV.to_track_quat("Z", "Y").to_euler()
SET_WORLD = {"FIELD": (1.0, 0.0, 4.5), "CAPE": (1.0, 0.0, 4.0), "JAR": (1.0, 0.0, 4.0),
             "CORE": (0, .25, 0), "LAB": (0, .03, 0), "GLASS": (0, .004, 0), "SHELF": (0, .05, 0)}
SET_EXP = {"FIELD": -.15, "CAPE": -.3, "JAR": -.3, "SHELF": -.6}

# ---------------------------------------------------------------- camera
cd = bpy.data.cameras.new("Cam"); cam = bpy.data.objects.new("Cam", cd); sc.collection.objects.link(cam); sc.camera = cam
cd.clip_start = .002; cd.clip_end = 20000.0; cd.sensor_width = 36.0; cd.dof.use_dof = True
cam.rotation_mode = "QUATERNION"
def lookat(p, t, up=Vector((0, 0, 1))):
    f = (Vector(t) - Vector(p)).normalized(); r = f.cross(Vector(up)).normalized(); u = r.cross(f)
    return Matrix((r, u, -f)).transposed().to_quaternion()
def fz(x, y): return float(plateau_h(np.array([x]), np.array([y]))[0])
def cam_keys(name):
    """(fraction, pos, target, lens, fstop, focus distance or None)"""
    if name == "FIELD_A":    # low over the plateau, tilting up from the snow to the sky
        o = ORG["FIELD"]; z = fz(0, -6)
        return [(0, o + Vector((0, -6, z + 1.4)), o + Vector((26, 32, z + 2.0)), 28, 16, None), (1, o + Vector((0, -6.3, z + 1.5)), o + Vector((26, 32, z + 20)), 28, 16, None)]
    if name == "FIELD_B":    # close to the surface, ice crystals falling
        o = ORG["FIELD"]; z = fz(0, -2)
        return [(0, o + Vector((-.5, -3.9, z + .5)), o + Vector((.3, -1.0, z + .05)), 40, 5.6, 1.6), (1, o + Vector((-.4, -3.6, z + .42)), o + Vector((.3, -1.0, z + .02)), 40, 5.6, 1.5)]
    if name == "FIELD_C":    # skimming the open snow
        o = ORG["FIELD"]; z = fz(2, -8)
        return [(0, o + Vector((2, -8, z + .5)), o + Vector((0, 12, z - .2)), 30, 11, None), (1, o + Vector((1.6, -5.2, z + .38)), o + Vector((0, 14, z - .2)), 30, 11, None)]
    if name == "FIELD_D":    # toward the low sun, today's snow
        o = ORG["FIELD"]; z = fz(-6, 0)
        return [(0, o + Vector((-6, -1, z + .7)), o + Vector((20, 4, z + .2)), 30, 11, None), (1, o + Vector((-4.4, -.8, z + .6)), o + Vector((20, 4, z + .25)), 30, 11, None)]
    if name == "FIELD_Z":    # end: rise off the snow and tilt up into the sky
        o = ORG["FIELD"]; z = fz(0, -10)
        return [(0, o + Vector((0, -10, z + 1.5)), o + Vector((24, 30, z + .5)), 28, 16, None), (1, o + Vector((0, -22, z + 14)), o + Vector((30, 40, z + 22)), 28, 16, None)]
    if name == "CORE_A":     # macro push into the bubbles
        o = ORG["CORE"]
        return [(0, o + Vector((.07, -.2, CZ + .06)), o + Vector((.03, 0, CZ)), 85, 16, None), (1, o + Vector((.045, -.13, CZ + .035)), o + Vector((.025, 0, CZ)), 85, 16, None)]
    if name == "CORE_A2":
        o = ORG["CORE"]
        return [(0, o + Vector((-.24, -.2, CZ + .07)), o + Vector((-.2, 0, CZ)), 85, 16, None), (1, o + Vector((-.2, -.15, CZ + .05)), o + Vector((-.2, 0, CZ)), 85, 16, None)]
    if name == "CORE_B":     # the core on its cradle; cracks appear
        o = ORG["CORE"]
        return [(0, o + Vector((-.75, -.95, CZ + .45)), o + Vector((0, 0, CZ)), 50, 5.6, None), (1, o + Vector((-.45, -.7, CZ + .3)), o + Vector((0, 0, CZ)), 50, 5.6, None)]
    if name == "CORE_C":     # macro along a crack, then over to the second piece resting
        o = ORG["CORE"]
        return [(0, o + Vector((.3, -.36, CZ + .13)), o + Vector((.15, 0, CZ)), 60, 11, None), (.5, o + Vector((.33, -.33, CZ + .12)), o + Vector((.19, 0, CZ)), 60, 11, None),
                (1, o + Vector((.5, -.38, CZ + .16)), o + Vector((.66, -.02, CZ)), 60, 8, None)]
    if name == "CORE_D":     # a short core section by itself (a generic core, not the Allan Hills core)
        o = ORG["CORE"]
        return [(0, o + Vector((1.25, -.75, CZ + .38)), o + Vector((.68, -.02, CZ)), 60, 5.6, None), (1, o + Vector((1.12, -.62, CZ + .3)), o + Vector((.68, -.02, CZ)), 60, 5.6, None)]
    if name == "LAB_A":
        o = ORG["LAB"]
        return [(0, o + Vector((-.1, -.26, BZ + .12)), o + Vector((0, 0, BZ + .025)), 50, 9, None), (.45, o + Vector((-.07, -.2, BZ + .09)), o + Vector((0, 0, BZ + .025)), 50, 9, None),
                (1, o + Vector((.07, -.4, BZ + .19)), o + Vector((-.1, .07, BZ + .07)), 30, 9, None)]
    if name == "GLASS_A":
        o = ORG["GLASS"]
        return [(0, o + Vector((-.13, -.33, GZ + .1)), o + Vector((0, 0, GZ + .065)), 70, 6, None), (1, o + Vector((-.08, -.23, GZ + .085)), o + Vector((0, 0, GZ + .068)), 70, 6, None)]
    if name == "CAPE_A":     # behind the station looking out to sea, then down to the cylinders
        o = ORG["CAPE"]
        return [(0, o + Vector((-18, -158, cape_z(-18, -158) + 5)), o + Vector((0, -40, hz)), 35, 11, None),
                (.6, o + Vector((-13, -150, cape_z(-13, -150) + 3.6)), o + Vector((0, -40, hz)), 35, 11, None),
                (1, o + Vector((-8.2, -139.5, cape_z(-8.2, -139.5) + 1.7)), o + Vector((hx - 4.9, hy - 3.2, hz + .8)), 35, 8, None)]
    if name == "SHELF_A":    # the old olive cylinder, then the rows
        o = ORG["SHELF"]
        return [(0, o + Vector((-2.7, -1.7, 1.0)), o + Vector((-1.8, -.4, .6)), 45, 4, None), (.45, o + Vector((-2.55, -1.6, .95)), o + Vector((-1.8, -.4, .6)), 45, 4, None),
                (1, o + Vector((1.6, -2.7, 1.6)), o + Vector((0, 1.2, .9)), 32, 8, None)]
    if name == "SHELF_B":
        o = ORG["SHELF"]
        return [(0, o + Vector((3.85, .55, 1.55)), o + Vector((4.6, 1.5, 1.3)), 50, 4, None), (1, o + Vector((4.05, .8, 1.48)), o + Vector((4.6, 1.5, 1.3)), 50, 4, None)]
    if name == "JAR_A":
        o = ORG["JAR"]
        return [(0, o + Vector((-.36, -.46, JZ + .26)), o + Vector((.03, -.02, JZ + .05)), 50, 4, None), (1, o + Vector((-.22, -.3, JZ + .16)), o + Vector((.04, -.03, JZ + .045)), 50, 4, None)]
    raise KeyError(name)

def key_vis(o_, frame, hidden):
    o_.hide_render = hidden; o_.keyframe_insert("hide_render", frame=frame)
SRC_HIDE = {"FlakeSrc", "BubSrc", "GBSrc", "RiseSrc"}
allsets = list(SETS.keys())
for c_ in CRACKS:   # cracks start tiny
    c_.scale = (.01, .01, 1); c_.keyframe_insert("scale", frame=1)
f = 1; cut = set()
def F(fa, fb, u): return int(round(fa + (fb - fa) * u))
for sh in SHOTS:
    n = int(round(sh["dur"] * FPS)); fa, fb = f, f + n - 1
    if sh["cam"] is None: f = fb + 1; continue
    cut.add(fb)
    setname = sh["cam"].split("_")[0]
    for s_ in allsets:
        for o_ in SETS[s_]:
            if o_.name in SRC_HIDE: continue
            key_vis(o_, fa, s_ != setname)
    dy, gr, se = SET_WORLD[setname]
    vday.outputs[0].default_value = dy; vday.outputs[0].keyframe_insert("default_value", frame=fa)
    vgrey.outputs[0].default_value = gr; vgrey.outputs[0].keyframe_insert("default_value", frame=fa)
    sun_d.energy = se; sun_d.keyframe_insert("energy", frame=fa)
    sc.view_settings.exposure = SET_EXP.get(setname, 0.0); sc.view_settings.keyframe_insert("exposure", frame=fa)
    for u, p, t, lens, fs_, fd in cam_keys(sh["cam"]):
        ff = F(fa, fb, u)
        cam.location = p; cam.rotation_quaternion = lookat(p, t)
        cam.keyframe_insert("location", frame=ff); cam.keyframe_insert("rotation_quaternion", frame=ff)
        cd.lens = lens; cd.keyframe_insert("lens", frame=ff)
        cd.dof.aperture_fstop = fs_; cd.dof.keyframe_insert("aperture_fstop", frame=ff)
        cd.dof.focus_distance = fd if fd else (Vector(t) - Vector(p)).length; cd.dof.keyframe_insert("focus_distance", frame=ff)
    c = sh["cam"]
    if c == "FIELD_B":       # crystals drift down
        FL.location = ORG["FIELD"] + Vector((.15, 0, .2)); FL.keyframe_insert("location", frame=fa)
        FL.location = ORG["FIELD"] + Vector((-.1, 0, -1.4)); FL.keyframe_insert("location", frame=fb)
    elif c == "FIELD_A" or c.startswith("FIELD"):
        if c != "FIELD_B":
            for fl_ in fls: key_vis(fl_, fa, True)
    if c == "CORE_B":        # "a small knock can make them burst and the ice crack" (~9.5 s in), the core rings
        for k, (t0, t1) in ((0, (9.3, 10.6)), (1, (9.8, 11.4)), (3, (10.2, 12.0))):
            cr = CRACKS[k]; cr.scale = (.01, .01, 1); cr.keyframe_insert("scale", frame=fa + int(t0 * FPS))
            cr.scale = (1, 1, 1); cr.keyframe_insert("scale", frame=fa + int(t1 * FPS))
    if c == "CORE_C":        # "bubbles or tiny cracks can appear again" (~4 s in)
        cr = CRACKS[2]; cr.scale = (.01, .01, 1); cr.keyframe_insert("scale", frame=fa + int(3.4 * FPS))
        cr.scale = (1, 1, 1); cr.keyframe_insert("scale", frame=fa + int(5.6 * FPS))
    if c == "LAB_A":         # laser on ~2.8 s in; the ice shrinks as it turns to vapor
        t_on = fa + int(2.8 * FPS)
        key_vis(beam, fa, True); key_vis(beam, t_on, False)
        glow.data.energy = 0.0; glow.data.keyframe_insert("energy", frame=fa); glow.data.keyframe_insert("energy", frame=t_on - 1)
        glow.data.energy = .6; glow.data.keyframe_insert("energy", frame=t_on)
        icep.scale = (1, 1, 1); icep.keyframe_insert("scale", frame=t_on)
        icep.scale = (.55, .55, .5); icep.keyframe_insert("scale", frame=fb)
        icep.location = ORG["LAB"] + Vector((0, 0, BZ + .004 + .009)); icep.keyframe_insert("location", frame=t_on)
        icep.location = ORG["LAB"] + Vector((0, 0, BZ + .004 + .0045)); icep.keyframe_insert("location", frame=fb)
    if c == "GLASS_A":       # bubbles leave the melting ice and rise to the surface, again and again
        o = ORG["GLASS"]
        for b_, bx, by, ph, per in RISERS:
            rr = math.hypot(bx, by) or 1e-3; ex = bx / rr * .019; ey = by / rr * .017
            z0, z1 = GZ + .056, GZ + .0775; t = fa - ph * per * FPS
            while t < fb + 1:
                a0 = int(t); a1 = int(t + per * FPS) - 1
                if a1 <= fa + 1: t += per * FPS; continue
                b_.location = o + Vector((.003 + ex, ey, z0)); b_.keyframe_insert("location", frame=max(fa, a0))
                b_.location = o + Vector((.003 + ex * 1.15, ey * 1.15, z1)); b_.keyframe_insert("location", frame=max(fa, a1))
                t += per * FPS
    if c == "CAPE_A":        # the sea moves
        SEA_W.default_value = 0.0; SEA_W.keyframe_insert("default_value", frame=fa)
        SEA_W.default_value = sh["dur"] * .08; SEA_W.keyframe_insert("default_value", frame=fb)
        LINEAR_ANIM.add("__sea__")
    f = fb + 1
def all_curves(idb):
    ad_ = idb.animation_data
    if not ad_ or not ad_.action: return []
    cs = getattr(ad_.action, "fcurves", None)
    if cs is not None: return list(cs)
    try: return [fc for layer in ad_.action.layers for strip in layer.strips for bag in strip.channelbags for fc in bag.fcurves]
    except Exception: return []
SMOOTH_ANIM |= {icep.name}
for idb in list(bpy.data.objects) + list(bpy.data.lights) + [w.node_tree, sc, SEA_NT]:
    nm = getattr(idb, "name", "")
    for fc in all_curves(idb):
        lin = (nm in LINEAR_ANIM or idb is SEA_NT or nm.startswith("Rise")) and fc.data_path != "hide_render"
        for k in fc.keyframe_points:
            if lin: k.interpolation = "LINEAR"
            elif nm in SMOOTH_ANIM and fc.data_path != "hide_render": k.interpolation = "BEZIER"
            else: k.interpolation = "CONSTANT"
for b_, *_ in RISERS:   # rising bubbles jump back to the start between cycles
    for fc in all_curves(b_):
        if fc.data_path != "location": continue
        kp = fc.keyframe_points
        for i in range(len(kp)):
            kp[i].interpolation = "LINEAR" if i % 2 == 0 else "CONSTANT"
for idb in (cam, cd):
    for fc in all_curves(idb):
        for k in fc.keyframe_points:
            k.interpolation = "CONSTANT" if int(k.co[0]) in cut else "BEZIER"; k.easing = "EASE_IN_OUT"
print("frames", DUR, flush=True)
# ---------------------------------------------------------------- outputs
if arg("--save"): bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(arg("--save")))
def shot_frame(name, u):
    ff = 1
    for sh in SHOTS:
        n_ = int(round(sh["dur"] * FPS))
        if sh["name"] == name or sh["cam"] == name: return ff + int(u * (n_ - 1))
        ff += n_
    raise KeyError(name)
if arg("--hide"):
    for nm_ in arg("--hide").split(","): bpy.data.objects[nm_].hide_render = True; bpy.data.objects[nm_].animation_data_clear()
if arg("--stills"):
    outd = os.path.abspath(arg("--stills")); os.makedirs(outd, exist_ok=True)
    frs = []
    for x in arg("--frames", "1").split(","):
        if ":" in x: nm_, u_ = x.split(":"); frs.append((nm_ + "_" + u_, shot_frame(nm_, float(u_))))
        else: frs.append(("f", int(x)))
    for tag_, fr in frs:
        t0 = time.time(); sc.frame_set(fr); sc.render.filepath = os.path.join(outd, "t_%s_%04d.png" % (tag_, fr)); bpy.ops.render.render(write_still=True); print("STILL", tag_, fr, "%.1fs" % (time.time() - t0), flush=True)
if arg("--anim"):
    outd = os.path.abspath(arg("--anim")); os.makedirs(outd, exist_ok=True)
    f0, f1 = int(arg("--start", sc.frame_start)), int(arg("--end", sc.frame_end))
    skip = set(); ff_ = 1
    for sh in SHOTS:
        n_ = int(round(sh["dur"] * FPS))
        if sh["cam"] is None: skip.update(range(ff_, ff_ + n_))
        ff_ += n_
    step = int(arg("--step", "1"))
    todo = list(range(f0, f1 + 1, step))
    if arg("--ranges"):
        todo = [fr for ab in arg("--ranges").split(",") for fr in range(int(ab.split("-")[0]), int(ab.split("-")[1]) + 1, step)]
    if arg("--shots"):
        names = arg("--shots").split(","); todo = []; ff_ = 1
        for sh in SHOTS:
            n_ = int(round(sh["dur"] * FPS))
            if sh["name"] in names: todo += list(range(ff_ if ff_ % 2 == 1 else ff_ + 1, ff_ + n_, 2))
            ff_ += n_
    deadline = arg("--deadline")   # "HH:MM" local; stop cleanly before it
    for fr in todo:
        if deadline:
            lt = time.localtime(); hh, mm = map(int, deadline.split(":"))
            if (lt.tm_hour, lt.tm_min) >= (hh, mm) and lt.tm_hour < 12: print("DEADLINE STOP", fr, flush=True); break
        p = os.path.join(outd, "f_%04d.png" % fr)
        if fr in skip or (os.path.exists(p) and os.path.getsize(p) > 1000): continue
        t0 = time.time(); sc.frame_set(fr); sc.render.filepath = p; bpy.ops.render.render(write_still=True)
        print("FRAME %d %.1fs" % (fr, time.time() - t0), flush=True)
