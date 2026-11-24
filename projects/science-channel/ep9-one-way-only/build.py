# Heartbeat TV Science 8.9 "Every one-way-only is a story". Pure-script Blender 5.1 scene, no downloaded assets (ep7 pipeline).
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
sc.cycles.max_bounces = 10; sc.cycles.diffuse_bounces = 2; sc.cycles.glossy_bounces = 3; sc.cycles.transmission_bounces = 10
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


# ================================================================ ep9 scene (Science 8.9 "Every one-way-only is a story")
# Generic everyday objects, built from primitives (no downloaded assets); all labelled as illustrations on screen.  1 unit = 1 m.
#   PUMP    a fuel dispenser at night: a gas nozzle (black handle) and a diesel nozzle (green handle), spouts side by side
#   NECK    a car's open fuel door and filler neck; a wider diesel spout stops at the narrow opening
#   DESERT  a dry lakebed at dawn with a long rocket-sled track and a simple sled (not the real 1949 track or sled)
#   SPRINGS a small metal dish with two coil springs and a switch housing on a workbench (Shingo's 1961 example, drawn)
#   SHIFT   a generic automatic shifter in Park on a dark console
#   MICRO   a generic microwave oven; the door opens and the light goes off
#   SIM     a nano SIM card with its cut corner, on a phone's tray (real size, macro)
#   USB     a USB-C plug turning over: the same shape upside down
ORG = {"PUMP": Vector((0, 0, 0)), "NECK": Vector((50, 0, 0)), "SPRINGS": Vector((100, 0, 0)), "SHIFT": Vector((150, 0, 0)),
       "MICRO": Vector((200, 0, 0)), "SIM": Vector((250, 0, 0)), "USB": Vector((300, 0, 0)), "DESERT": Vector((10000, 0, 0))}
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

# ================================================================ PUMP
o = ORG["PUMP"]
give(grid("PumpFloor", 12, 12, 1, 1, lambda X, Y: X * 0, "PUMP", origin=o), floor_mat("Concrete", (.32, .31, .29), (.22, .21, .2), 3.0, .85, .2))
cab = give(prim_box("Cabinet", (1.1, .55, 1.9), "PUMP", loc=o + Vector((0, .4, .95))), painted("CabPaint", (.55, .58, .62))); bevel(cab, .02)
pan = give(prim_box("Panel", (.9, .02, .55), "PUMP", loc=o + Vector((0, .115, 1.35))), plastic("PanelPl", (.08, .09, .1), .3, .5))
scr = give(prim_box("Screen", (.36, .02, .2), "PUMP", loc=o + Vector((-.2, .1, 1.42))), EMITM("ScreenEm", (.35, .55, .7), 1.2))
for k, (x, hm) in enumerate(((-.27, M_BLACK), (.27, M_GREEN))):
    hol = give(prim_box("Holster%d" % k, (.18, .12, .26), "PUMP", loc=o + Vector((x, .07, .95))), M_STEEL); bevel(hol, .01)
NOZ = {}
for k, (x, hm, rr, nm) in enumerate(((-.27, M_BLACK, .0107, "gas"), (.27, M_GREEN, .0119, "diesel"))):
    base = o + Vector((x, -.02, 1.02))
    body = give(prim_box("NozBody%d" % k, (.07, .09, .22), "PUMP", loc=base), hm); bevel(body, .02, 4)
    body.rotation_euler = (math.radians(-12), 0, 0)
    trig = give(prim_box("Trig%d" % k, (.03, .02, .14), "PUMP", loc=base + Vector((0, -.07, -.05))), M_STEEL); bevel(trig, .006)
    guard = give(prim_box("Guard%d" % k, (.04, .12, .015), "PUMP", loc=base + Vector((0, -.05, -.13))), M_STEEL); bevel(guard, .005)
    sp = give(prim_cyl("Spout%d" % k, rr, .2, "PUMP", 40, loc=base + Vector((0, -.02, -.2))), M_ALU)
    sp.rotation_euler = (math.radians(-12), 0, 0)
    hose = curve_obj("Hose%d" % k, [tuple(base + Vector((0, .02, .12))), tuple(base + Vector((0, .0, .45))), tuple(o + Vector((x * 1.4, .15, 1.75))), tuple(o + Vector((x * 1.6, .3, 1.9)))], .016, "PUMP", M_RUBBER)
    NOZ[nm] = body
canopy = give(prim_box("Canopy", (10, 10, .3), "PUMP", loc=o + Vector((0, 0, 4.6))), painted("CanopyW", (.7, .7, .7), .6))
for i, (lx, ly) in enumerate(((-1.5, -1.5), (1.5, -1.5), (0, 1.5))):
    give(prim_box("CLight%d" % i, (.8, .8, .02), "PUMP", loc=o + Vector((lx, ly, 4.44))), EMITM("CLightE", (1, .97, .9), 20))
    add_light("CanA%d" % i, "AREA", "PUMP", o + Vector((lx, ly, 4.4)), 380, (1, .96, .9), .9, rot=(0, 0, 0))
add_light("PumpFill", "AREA", "PUMP", o + Vector((-1.2, -2.0, 1.4)), 40, (.8, .85, 1.0), 1.0, target=o + Vector((0, 0, 1)))

# ================================================================ NECK: open fuel door + filler neck, a diesel spout too wide
o = ORG["NECK"]
def body_h(X, Y): return -.03 * X ** 2 - .02 * Y ** 2
car = give(grid("CarSide", 1.6, 1.2, 40, 30, body_h, "NECK", origin=o), painted("CarPaint", (.38, .03, .03), .25))
car.rotation_euler = (math.pi / 2, 0, 0)   # the panel stands vertical, facing -Y
recess = give(prim_cyl("Recess", .085, .06, "NECK", 64, loc=o + Vector((0, .02, 0)), rot=(math.pi / 2, 0, 0)), plastic("RecessPl", (.03, .03, .03), .5))
door = give(prim_cyl("FuelDoor", .086, .006, "NECK", 64, loc=o + Vector((.11, -.06, 0)), rot=(math.pi / 2, 0, math.radians(-70))), painted("CarPaint2", (.38, .03, .03), .25))
neck = give(prim_cyl("NeckRim", .032, .03, "NECK", 64, loc=o + Vector((0, -.012, 0)), rot=(math.pi / 2, 0, 0)), M_BLACK)
bm = bmesh.new(); bmesh.ops.create_circle(bm, cap_ends=False, radius=.0122, segments=48)
bmesh.ops.create_circle(bm, cap_ends=False, radius=.024, segments=48)
me = bpy.data.meshes.new("NeckFace"); bm.to_mesh(me); bm.free()
nf = link(bpy.data.objects.new("NeckFace", me), "NECK")
# ring face: build as a thin tube with the narrow opening (the restrictor) visible
ring = give(prim_cyl("Restrictor", .024, .004, "NECK", 64, loc=o + Vector((0, -.028, 0)), rot=(math.pi / 2, 0, 0)), M_STEEL)
bo = prim_cyl("RHole", .0118, .05, "NECK", 48, loc=o + Vector((0, -.028, 0)), rot=(math.pi / 2, 0, 0))
mod = ring.modifiers.new("hole", "BOOLEAN"); mod.object = bo; mod.operation = "DIFFERENCE"; bo.hide_render = True; bo.hide_viewport = True
SETS["NECK"].remove(bo)
hole_dark = give(prim_cyl("HoleDark", .0118, .002, "NECK", 48, loc=o + Vector((0, -.012, 0)), rot=(math.pi / 2, 0, 0)), EMITM("Black", (0, 0, 0), 0))
nf.hide_render = True
dz = give(prim_cyl("DieselSpout", .0119, .22, "NECK", 48, loc=o + Vector((0, -.25, 0)), rot=(math.pi / 2, 0, 0)), M_ALU)
dzb = give(prim_box("DieselBody", (.07, .22, .09), "NECK", loc=o + Vector((0, -.42, .02))), M_GREEN); bevel(dzb, .02, 4)
add_light("NeckKey", "AREA", "NECK", o + Vector((-.6, -.8, .5)), 25, (1, .97, .92), .6, target=o)
add_light("NeckRim", "AREA", "NECK", o + Vector((.7, -.4, .3)), 10, (.8, .88, 1.0), .4, target=o)

# ================================================================ DESERT: dry lakebed at dawn, rocket-sled track
o = ORG["DESERT"]
def lake_h(X, Y): return .03 * fbm2(X, Y, .02, 3, 3.0)
lb = grid("Lakebed", 900, 900, 90, 90, lake_h, "DESERT", origin=o)
def lakebed_mat():
    m, nt = mat("Playa"); ob, gen = coords(nt)
    vo = VORO(nt, ob, 1.4, "DISTANCE_TO_EDGE", .9); crack = SMOOTH(nt, vo.outputs["Distance"], .0, .03)
    h = NOISE(nt, ob, .3, 6, .6)
    col = MIXC(nt, h, (.66, .55, .4), (.54, .43, .31)); col = MIXC(nt, crack, (.3, .25, .2), col)
    b = principled(nt, col, .9, normal=BUMP(nt, crack, .5, .03)); finish(nt, b.outputs[0]); return m
give(lb, lakebed_mat())
def mts_h(X, Y): return np.maximum(0, 60 + 160 * fbm2(X, Y, .004, 5, 9.0)) * np.clip((Y - 1500) / 900, 0, 1)
mts = give(grid("Mountains", 9000, 4000, 120, 60, mts_h, "DESERT", origin=o + Vector((0, 2600, -2))), floor_mat("MtRock", (.35, .27, .22), (.22, .18, .16), .01, .9, .5))
M_RAIL = metal("Rail", (.45, .43, .4), .4); M_TIE = plastic("Tie", (.18, .15, .12), .9)
for side in (-.7, .7):
    give(prim_box("Rail%d" % (side > 0), (.08, 900, .12), "DESERT", loc=o + Vector((side, 0, .14))), M_RAIL)
tie = give(prim_box("Tie0", (2.0, .25, .12), "DESERT", loc=o + Vector((0, -300, .06))), M_TIE)
scatter_instances("Tie", tie, [o + Vector((0, -300 + 1.5 * i, .06)) for i in range(1, 420)], [1.0] * 419, "DESERT")
sled = give(prim_box("Sled", (1.6, 3.2, .5), "DESERT", loc=o + Vector((0, 6, .55))), painted("SledPaint", (.6, .6, .58), .45)); bevel(sled, .05)
seat = give(prim_box("Seat", (.7, .7, .9), "DESERT", loc=o + Vector((0, 6.6, 1.2))), painted("SeatPaint", (.5, .1, .06), .5)); bevel(seat, .08)
for i in range(4):
    give(prim_cyl("Rocket%d" % i, .14, .9, "DESERT", 32, loc=o + Vector((-.45 + .3 * i, 4.2, .62)), rot=(math.pi / 2, 0, 0)), M_STEEL)
for side in (-.7, .7):
    give(prim_box("Shoe%d" % (side > 0), (.22, 2.8, .14), "DESERT", loc=o + Vector((side, 6, .27))), M_RAIL)
bunker = give(prim_box("Blockhouse", (5, 4, 2.6), "DESERT", loc=o + Vector((-14, 40, 1.3))), floor_mat("Block", (.6, .58, .52), (.5, .48, .44), 2.0, .9, .1)); bevel(bunker, .05)

# ================================================================ SPRINGS: workbench, dish, two springs, a switch
o = ORG["SPRINGS"]
give(grid("Bench", 1.2, .8, 1, 1, lambda X, Y: X * 0, "SPRINGS", origin=o), floor_mat("Wood", (.42, .27, .14), (.3, .18, .09), 22.0, .6, .05))
dish = give(prim_cyl("Dish", .035, .008, "SPRINGS", 64, loc=o + Vector((0, 0, .004))), M_STEEL); bevel(dish, .003, 3)
dishin = give(prim_cyl("DishIn", .031, .002, "SPRINGS", 64, loc=o + Vector((0, 0, .0075))), metal("DishIn", (.5, .5, .52), .35))
M_SPRING = metal("Spring", (.7, .7, .72), .2)
sp1 = helix("Spring1", .0035, .0005, 7, .016, "SPRINGS", o + Vector((-.012, .006, .0115)), M_SPRING, "X")
sp2 = helix("Spring2", .0035, .0005, 7, .016, "SPRINGS", o + Vector((.004, -.012, .0115)), M_SPRING, "X")
sp2.rotation_euler = (0, math.pi / 2, .7)
sw = give(prim_box("Switch", (.03, .018, .014), "SPRINGS", loc=o + Vector((.065, .02, .007))), plastic("SwitchPl", (.82, .8, .74), .5)); bevel(sw, .002)
btn = give(prim_box("SwBtn", (.01, .008, .006), "SPRINGS", loc=o + Vector((.065, .02, .016))), M_BLACK); bevel(btn, .001)
for i in range(2):
    give(prim_box("Pin%d" % i, (.002, .002, .008), "SPRINGS", loc=o + Vector((.058 + .014 * i, .03, .004))), M_GOLD)
tw = give(prim_box("Tweezers", (.11, .006, .002), "SPRINGS", loc=o + Vector((-.02, .06, .002))), M_STEEL); tw.rotation_euler = (0, 0, .25)
add_light("SprKey", "AREA", "SPRINGS", o + Vector((-.25, -.3, .35)), 6, (1, .96, .9), .3, target=o)
add_light("SprRim", "AREA", "SPRINGS", o + Vector((.25, .3, .15)), 2, (.85, .9, 1.0), .2, target=o)

# ================================================================ SHIFT: console + lever in Park
o = ORG["SHIFT"]
con = give(prim_box("Console", (.3, .6, .12), "SHIFT", loc=o + Vector((0, 0, -.06))), plastic("ConsolePl", (.025, .025, .028), .5)); bevel(con, .02, 4)
gate = give(prim_box("Gate", (.12, .24, .01), "SHIFT", loc=o + Vector((0, 0, .002))), plastic("GatePl", (.05, .05, .055), .25, .5)); bevel(gate, .006)
slot = give(prim_box("Slot", (.012, .17, .005), "SHIFT", loc=o + Vector((0, 0, .006))), EMITM("Black2", (0, 0, 0), 0))
M_LET = EMITM("Letters", (.95, .95, .95), 2.0); M_LET2 = EMITM("LettersP", (1.0, .55, .15), 4.0)
for i, ch in enumerate("PRND"):
    text_obj("L_" + ch, ch, .022, "SHIFT", o + Vector((.035, .07 - i * .045, .0075)), m=M_LET2 if ch == "P" else M_LET)
lever = give(prim_cyl("Lever", .007, .1, "SHIFT", 32, loc=o + Vector((0, .07, .05))), M_CHROME)
knob = give(blob("Knob", .028, 2.0, "SHIFT", 4, .05, 1.0, (1.0, 1.25, .9)), plastic("Leather", (.03, .028, .026), .6))
knob.location = o + Vector((0, .07, .115))
kbtn = give(prim_box("KnobBtn", (.012, .016, .008), "SHIFT", loc=o + Vector((-.024, .07, .12))), M_CHROME); bevel(kbtn, .003)
add_light("ShKey", "AREA", "SHIFT", o + Vector((-.4, -.45, .5)), 14, (1, .96, .9), .4, target=o)
add_light("ShRim", "AREA", "SHIFT", o + Vector((.35, .4, .25)), 6, (.8, .88, 1.0), .3, target=o)

# ================================================================ MICRO: microwave on a counter
o = ORG["MICRO"]
give(grid("Counter", 2.0, 1.0, 1, 1, lambda X, Y: X * 0, "MICRO", origin=o), floor_mat("Stone", (.5, .48, .45), (.36, .34, .32), 40.0, .35, .02))
give(prim_box("Backsplash", (2.0, .02, 1.0), "MICRO", loc=o + Vector((0, .45, .5))), floor_mat("Tile", (.75, .73, .68), (.7, .68, .64), 10.0, .3, .02))
mw = give(prim_box("MWBody", (.5, .38, .29), "MICRO", loc=o + Vector((0, .18, .145))), painted("MWPaint", (.06, .06, .065), .35)); bevel(mw, .008)
cav = give(prim_box("Cavity", (.31, .3, .21), "MICRO", loc=o + Vector((-.06, .15, .15))), painted("CavPaint", (.75, .74, .7), .5))
cav_l = add_light("CavLight", "POINT", "MICRO", o + Vector((-.06, .16, .22)), 3.0, (1, .85, .6), .03)
plate = give(prim_cyl("Turntable", .12, .006, "MICRO", 64, loc=o + Vector((-.06, .15, .05))), plastic("Glass", (.8, .85, .85), .05))
bowl = give(prim_cyl("Bowl", .06, .05, "MICRO", 48, loc=o + Vector((-.06, .15, .08))), plastic("Bowl", (.85, .82, .75), .3))
hinge = bpy.data.objects.new("Hinge", None); link(hinge, "MICRO"); hinge.location = o + Vector((-.25, -.012, .145))
door_ = give(prim_box("MWDoor", (.37, .02, .27), "MICRO", loc=(.185, 0, 0)), painted("DoorPaint", (.05, .05, .055), .3)); bevel(door_, .006)
door_.parent = hinge
def mesh_glass():
    m, nt = mat("DoorGlass"); ob, gen = coords(nt)
    br = N(nt, "ShaderNodeTexBrick"); br.inputs["Scale"].default_value = 1.0; br.inputs["Mortar Size"].default_value = .25; br.offset = .5
    br.inputs["Brick Width"].default_value = .004; br.inputs["Row Height"].default_value = .004
    br.inputs["Color1"].default_value = (1, 1, 1, 1); br.inputs["Color2"].default_value = (1, 1, 1, 1); br.inputs["Mortar"].default_value = (0, 0, 0, 1)
    L(nt, ob, br.inputs["Vector"])
    tr = N(nt, "ShaderNodeBsdfTransparent"); dk = principled(nt, (.01, .01, .01), .2)
    mx = N(nt, "ShaderNodeMixShader"); L(nt, M(nt, "MULTIPLY", br.outputs["Fac"], .75), mx.inputs[0]); L(nt, dk.outputs[0], mx.inputs[1]); L(nt, tr.outputs[0], mx.inputs[2])
    finish(nt, mx.outputs[0]); return m
win = give(prim_box("MWWindow", (.25, .022, .17), "MICRO", loc=(.16, 0, 0)), mesh_glass()); win.parent = hinge
door_.location = (.185, 0, 0); win.location = (.16, -.0005, 0)
pad = give(prim_box("Keypad", (.1, .01, .25), "MICRO", loc=o + Vector((.18, -.006, .145))), plastic("PadPl", (.08, .08, .085), .3, .4))
disp = give(prim_box("MWDisp", (.07, .012, .025), "MICRO", loc=o + Vector((.18, -.008, .24))), EMITM("Disp", (.3, .9, .5), 3.0))
add_light("MWKey", "AREA", "MICRO", o + Vector((-.6, -.8, .8)), 40, (1, .96, .9), .8, target=o + Vector((0, .15, .15)))
add_light("MWFill", "AREA", "MICRO", o + Vector((.8, -.5, .4)), 10, (.85, .9, 1.0), .6, target=o + Vector((0, .15, .15)))

# ================================================================ SIM: nano SIM (12.3 x 8.8 x 0.67 mm) on a tray
o = ORG["SIM"]
give(grid("SimDesk", .2, .2, 1, 1, lambda X, Y: X * 0, "SIM", origin=o), floor_mat("Desk", (.2, .19, .18), (.16, .15, .14), 300.0, .5, .02))
def sim_mesh(w, h, t, cut):
    pts = [(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2 - cut), (w / 2 - cut, h / 2), (-w / 2, h / 2)]
    bm = bmesh.new(); vs = [bm.verts.new((x, y, 0)) for x, y in pts]; f_ = bm.faces.new(vs)
    ex = bmesh.ops.extrude_face_region(bm, geom=[f_]); bmesh.ops.translate(bm, verts=[v for v in ex["geom"] if isinstance(v, bmesh.types.BMVert)], vec=(0, 0, t))
    me = bpy.data.meshes.new("SimM"); bm.to_mesh(me); bm.free(); return me
simo = link(bpy.data.objects.new("Sim", sim_mesh(.0123, .0088, .00067, .0017)), "SIM"); give(simo, plastic("SimPl", (.85, .84, .8), .4))
simo.location = o + Vector((0, 0, .0006)); bevel(simo, .0002, 2)
pads = []
for i in range(2):
    for j in range(3):
        p_ = give(prim_box("Pad%d%d" % (i, j), (.0026, .0017, .00005), "SIM", loc=o + Vector((-.0021 + .0042 * i, -.0021 + .0021 * j, .00128))), M_GOLD)
tray = give(prim_box("Tray", (.016, .0115, .0006), "SIM", loc=o + Vector((0, 0, .0003))), metal("TrayM", (.25, .25, .27), .3)); bevel(tray, .0006, 3)
add_light("SimKey", "AREA", "SIM", o + Vector((-.06, -.08, .1)), .6, (1, .96, .9), .05, target=o)
add_light("SimRim", "AREA", "SIM", o + Vector((.06, .07, .04)), .2, (.85, .9, 1.0), .03, target=o)

# ================================================================ USB: a USB-C plug (shell 8.25 x 2.4 mm) turning over, a port opposite
o = ORG["USB"]
give(grid("UsbDesk", .3, .3, 1, 1, lambda X, Y: X * 0, "USB", origin=o + Vector((0, 0, -.006))), floor_mat("Desk2", (.18, .17, .16), (.14, .13, .12), 300.0, .5, .02))
plug = bpy.data.objects.new("PlugRoot", None); link(plug, "USB"); plug.location = o + Vector((-.02, 0, .006))
shell = give(prim_box("Shell", (.0066, .00825, .0024), "USB", loc=(.0033, 0, 0)), M_CHROME); bevel(shell, .00115, 6); shell.parent = plug
tongue_hole = give(prim_box("ShellIn", (.0005, .0075, .0016), "USB", loc=(.0064, 0, 0)), EMITM("Black3", (0, 0, 0), 0)); bevel(tongue_hole, .0007, 4); tongue_hole.parent = plug
hous = give(prim_box("Overmold", (.016, .012, .0062), "USB", loc=(-.008, 0, 0)), plastic("Overmold", (.02, .02, .022), .5)); bevel(hous, .0025, 5); hous.parent = plug
cab_ = curve_obj("Cable", [(-.016, 0, 0), (-.04, 0, 0), (-.08, .01, -.002), (-.14, .03, -.006)], .0018, "USB", M_RUBBER); cab_.parent = plug
dev = give(prim_box("Device", (.03, .06, .009), "USB", loc=o + Vector((.03, 0, .0045 + .0015))), painted("DevPaint", (.12, .13, .15), .4)); bevel(dev, .002, 3)
port = give(prim_box("Port", (.002, .0087, .0028), "USB", loc=o + Vector((.0151, 0, .006))), EMITM("Black4", (0, 0, 0), 0)); bevel(port, .0012, 5)
add_light("UsbKey", "AREA", "USB", o + Vector((-.08, -.12, .12)), 1.2, (1, .96, .9), .08, target=o)
add_light("UsbRim", "AREA", "USB", o + Vector((.06, .1, .05)), .5, (.85, .9, 1.0), .05, target=o)

# ================================================================ world: dawn sky for the desert, a dim studio grey elsewhere
w = bpy.data.worlds.new("World"); sc.world = w; w.use_nodes = True; wn = w.node_tree; wn.nodes.clear()
sky = wn.nodes.new("ShaderNodeTexSky"); sky.sky_type = "MULTIPLE_SCATTERING"
try: sky.sun_elevation = math.radians(4.0); sky.sun_rotation = math.radians(100); sky.altitude = 700.0; sky.sun_disc = False
except Exception as e: print("sky props", e)
vday = wn.nodes.new("ShaderNodeValue"); vgrey = wn.nodes.new("ShaderNodeValue")
def wmul(a, b):
    n = wn.nodes.new("ShaderNodeMath"); n.operation = "MULTIPLY"; wn.links.new(a, n.inputs[0]); n.inputs[1].default_value = b; return n.outputs[0]
bg_d = wn.nodes.new("ShaderNodeBackground"); wn.links.new(sky.outputs[0], bg_d.inputs["Color"]); wn.links.new(wmul(vday.outputs[0], .5), bg_d.inputs["Strength"])
bg_g = wn.nodes.new("ShaderNodeBackground"); bg_g.inputs["Color"].default_value = (.5, .5, .52, 1); wn.links.new(vgrey.outputs[0], bg_g.inputs["Strength"])
ad = wn.nodes.new("ShaderNodeAddShader"); wn.links.new(bg_d.outputs[0], ad.inputs[0]); wn.links.new(bg_g.outputs[0], ad.inputs[1])
wo_ = wn.nodes.new("ShaderNodeOutputWorld"); wn.links.new(ad.outputs[0], wo_.inputs["Surface"])
SUNV = Vector((math.sin(math.radians(100)) * math.cos(math.radians(4)), math.cos(math.radians(100)) * math.cos(math.radians(4)), math.sin(math.radians(4))))
sun_d = bpy.data.lights.new("Sun", "SUN"); sun_d.angle = math.radians(.53); sun_d.color = (1.0, .78, .55)
sun = bpy.data.objects.new("Sun", sun_d); sc.collection.objects.link(sun); sun.rotation_euler = SUNV.to_track_quat("Z", "Y").to_euler()
SET_WORLD = {"DESERT": (1.0, 0.0, 6.0), "PUMP": (0, .004, 0), "NECK": (0, .02, 0), "SPRINGS": (0, .03, 0), "SHIFT": (0, .01, 0),
             "MICRO": (0, .05, 0), "SIM": (0, .03, 0), "USB": (0, .03, 0)}
SET_EXP = {"DESERT": -.3, "PUMP": -.2}

# ---------------------------------------------------------------- camera
cd = bpy.data.cameras.new("Cam"); cam = bpy.data.objects.new("Cam", cd); sc.collection.objects.link(cam); sc.camera = cam
cd.clip_start = .0005; cd.clip_end = 20000.0; cd.sensor_width = 36.0; cd.dof.use_dof = True
cam.rotation_mode = "QUATERNION"
def lookat(p, t, up=Vector((0, 0, 1))):
    f = (Vector(t) - Vector(p)).normalized(); r = f.cross(Vector(up)).normalized(); u = r.cross(f)
    return Matrix((r, u, -f)).transposed().to_quaternion()
def cam_keys(name):
    """(fraction, pos, target, lens, fstop, focus distance or None)"""
    if name == "PUMP_A":     # the two nozzles side by side, slow push
        o = ORG["PUMP"]; t = o + Vector((0, -.04, .86))
        return [(0, o + Vector((-.45, -1.7, 1.15)), t + Vector((0, 0, .08)), 50, 5.6, None), (1, o + Vector((-.2, -1.15, 1.02)), t + Vector((0, 0, .06)), 50, 5.6, None)]
    if name == "PUMP_W":     # wide, for the montage
        o = ORG["PUMP"]
        return [(0, o + Vector((-2.4, -3.2, 1.5)), o + Vector((0, .2, 1.0)), 35, 8.0, None), (1, o + Vector((-2.0, -3.4, 1.6)), o + Vector((0, .2, 1.0)), 35, 8.0, None)]
    if name == "DESERT_A":   # low along the track at dawn toward the sled
        o = ORG["DESERT"]
        return [(0, o + Vector((3.2, -40, 1.1)), o + Vector((0, 6, .9)), 35, 16, None), (.55, o + Vector((2.6, -18, 1.4)), o + Vector((0, 6, .9)), 35, 16, None),
                (1, o + Vector((5.5, -2, 2.4)), o + Vector((-1, 30, 1.0)), 30, 16, None)]
    if name == "SPRINGS_A":
        o = ORG["SPRINGS"]; t = o + Vector((0, 0, .008))
        return [(0, o + Vector((-.1, -.17, .13)), t + Vector((.02, 0, 0)), 70, 11, None), (1, o + Vector((-.035, -.075, .06)), t, 70, 11, None)]
    if name == "NECK_A":     # the diesel spout comes in and stops at the narrow opening
        o = ORG["NECK"]; t = o + Vector((0, -.05, 0))
        return [(0, o + Vector((-.35, -.5, .12)), t, 50, 5.6, None), (1, o + Vector((-.22, -.36, .08)), t, 50, 5.6, None)]
    if name == "SHIFT_A":
        o = ORG["SHIFT"]; t = o + Vector((0, .03, .04))
        return [(0, o + Vector((-.25, -.35, .3)), t, 50, 4.0, None), (1, o + Vector((-.15, -.28, .22)), t, 50, 4.0, None)]
    if name == "SHIFT_W":
        o = ORG["SHIFT"]; t = o + Vector((0, .03, .04))
        return [(0, o + Vector((.2, -.32, .26)), t, 45, 4.0, None), (1, o + Vector((.16, -.3, .24)), t, 45, 4.0, None)]
    if name in ("MICRO_A", "MICRO_W"):
        o = ORG["MICRO"]; t = o + Vector((0, .12, .15))
        if name == "MICRO_W": return [(0, o + Vector((-.5, -1.0, .45)), t, 40, 5.6, None), (1, o + Vector((-.45, -1.0, .43)), t, 40, 5.6, None)]
        return [(0, o + Vector((-.55, -1.1, .5)), t, 40, 5.6, None), (1, o + Vector((-.35, -.85, .38)), t, 40, 5.6, None)]
    if name in ("SIM_A", "SIM_W"):
        o = ORG["SIM"]; t = o + Vector((0, 0, .0007))
        if name == "SIM_W": return [(0, o + Vector((.03, -.05, .045)), t, 60, 22, None), (1, o + Vector((.028, -.05, .043)), t, 60, 22, None)]
        return [(0, o + Vector((-.04, -.06, .06)), t, 60, 22, None), (1, o + Vector((-.015, -.04, .035)), t, 60, 22, None)]
    if name in ("USB_A", "USB_W"):
        o = ORG["USB"]; t = o + Vector((-.006, 0, .006))
        if name == "USB_W": return [(0, o + Vector((-.03, -.07, .04)), t, 60, 18, None), (1, o + Vector((-.028, -.07, .038)), t, 60, 18, None)]
        return [(0, o + Vector((.03, -.06, .03)), t, 60, 18, None), (1, o + Vector((.04, -.045, .02)), t, 60, 18, None)]
    if name == "DESERT_Z":   # end: high and wide over the track at dawn
        o = ORG["DESERT"]
        return [(0, o + Vector((-26, -50, 7)), o + Vector((0, 30, 0)), 30, 16, None), (1, o + Vector((-30, -58, 11)), o + Vector((0, 40, 0)), 30, 16, None)]
    raise KeyError(name)

def key_vis(o_, frame, hidden):
    o_.hide_render = hidden; o_.keyframe_insert("hide_render", frame=frame)
allsets = list(SETS.keys())
f = 1; cut = set()
for sh in SHOTS:
    n = int(round(sh["dur"] * FPS)); fa, fb = f, f + n - 1
    if sh["cam"] is None: f = fb + 1; continue
    cut.add(fb)
    setname = sh["cam"].split("_")[0]
    for s_ in allsets:
        for o_ in SETS[s_]:
            if o_.name in ("RHole",): continue
            key_vis(o_, fa, s_ != setname)
    dy, gr, se = SET_WORLD[setname]
    vday.outputs[0].default_value = dy; vday.outputs[0].keyframe_insert("default_value", frame=fa)
    vgrey.outputs[0].default_value = gr; vgrey.outputs[0].keyframe_insert("default_value", frame=fa)
    sun_d.energy = se; sun_d.keyframe_insert("energy", frame=fa)
    sc.view_settings.exposure = SET_EXP.get(setname, 0.0); sc.view_settings.keyframe_insert("exposure", frame=fa)
    for u, p, t, lens, fs_, fd in cam_keys(sh["cam"]):
        ff = int(round(fa + (fb - fa) * u))
        cam.location = p; cam.rotation_quaternion = lookat(p, t)
        cam.keyframe_insert("location", frame=ff); cam.keyframe_insert("rotation_quaternion", frame=ff)
        cd.lens = lens; cd.keyframe_insert("lens", frame=ff)
        cd.dof.aperture_fstop = fs_; cd.dof.keyframe_insert("aperture_fstop", frame=ff)
        cd.dof.focus_distance = fd if fd else (Vector(t) - Vector(p)).length; cd.dof.keyframe_insert("focus_distance", frame=ff)
    if sh["cam"] == "NECK_A":    # spout slides in, stops against the rim (it is wider than the opening)
        o = ORG["NECK"]
        for u, yy in ((0, -.36), (.25, -.15), (.33, -.142), (1, -.142)):
            ff = int(round(fa + (fb - fa) * u))
            dz.location = o + Vector((0, yy, 0)); dzb.location = o + Vector((0, yy - .17, .02))
            dz.keyframe_insert("location", frame=ff); dzb.keyframe_insert("location", frame=ff)
    if sh["cam"] == "MICRO_A":   # door opens partway through; the light goes off at once
        t_open = int(fa + (fb - fa) * .35)
        hinge.rotation_euler = (0, 0, 0); hinge.keyframe_insert("rotation_euler", frame=fa); hinge.keyframe_insert("rotation_euler", frame=t_open)
        hinge.rotation_euler = (0, 0, math.radians(-95)); hinge.keyframe_insert("rotation_euler", frame=t_open + 30)
        cav_l.data.energy = 3.0; cav_l.data.keyframe_insert("energy", frame=fa); cav_l.data.keyframe_insert("energy", frame=t_open)
        cav_l.data.energy = 0.0; cav_l.data.keyframe_insert("energy", frame=t_open + 1)
        plate.rotation_euler = (0, 0, 0); plate.keyframe_insert("rotation_euler", frame=fa)
        plate.rotation_euler = (0, 0, .5 * (t_open - fa) / FPS); plate.keyframe_insert("rotation_euler", frame=t_open)
        bowl.rotation_euler = plate.rotation_euler.copy(); bowl.keyframe_insert("rotation_euler", frame=t_open)
    if sh["cam"] == "MICRO_W":   # montage: door closed, light on
        hinge.rotation_euler = (0, 0, 0); hinge.keyframe_insert("rotation_euler", frame=fa)
        cav_l.data.energy = 3.0; cav_l.data.keyframe_insert("energy", frame=fa)
    if sh["cam"] in ("USB_A", "USB_W"):   # turn the plug over about its long axis; it looks the same
        plug.rotation_euler = (0, 0, 0); plug.keyframe_insert("rotation_euler", frame=fa)
        if sh["cam"] == "USB_A":
            t1 = int(fa + (fb - fa) * .3); t2 = int(fa + (fb - fa) * .65)
            plug.keyframe_insert("rotation_euler", frame=t1); plug.rotation_euler = (math.pi, 0, 0); plug.keyframe_insert("rotation_euler", frame=t2)
            plug.location = ORG["USB"] + Vector((-.02, 0, .006)); plug.keyframe_insert("location", frame=t2)
            plug.location = ORG["USB"] + Vector((-.0055, 0, .006)); plug.keyframe_insert("location", frame=fb)
        else:
            plug.location = ORG["USB"] + Vector((-.02, 0, .006)); plug.keyframe_insert("location", frame=fa)
    f = fb + 1
def all_curves(idb):
    ad_ = idb.animation_data
    if not ad_ or not ad_.action: return []
    cs = getattr(ad_.action, "fcurves", None)
    if cs is not None: return list(cs)
    try: return [fc for layer in ad_.action.layers for strip in layer.strips for bag in strip.channelbags for fc in bag.fcurves]
    except Exception: return []
SMOOTH_ANIM = {dz.name, dzb.name, hinge.name, plate.name, bowl.name, plug.name}
for idb in list(bpy.data.objects) + list(bpy.data.lights) + [w.node_tree, sc]:
    for fc in all_curves(idb):
        for k in fc.keyframe_points:
            k.interpolation = "BEZIER" if getattr(idb, "name", "") in SMOOTH_ANIM else "CONSTANT"
for idb in (cam, cd):
    for fc in all_curves(idb):
        for k in fc.keyframe_points:
            k.interpolation = "CONSTANT" if int(k.co[0]) in cut else "BEZIER"; k.easing = "EASE_IN_OUT"
print("frames", DUR, flush=True)
# ---------------------------------------------------------------- outputs
if arg("--save"): bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(arg("--save")))
if arg("--stills"):
    outd = os.path.abspath(arg("--stills")); os.makedirs(outd, exist_ok=True)
    for fr in [int(x) for x in arg("--frames", "1").split(",")]:
        t0 = time.time(); sc.frame_set(fr); sc.render.filepath = os.path.join(outd, "t_%04d.png" % fr); bpy.ops.render.render(write_still=True); print("STILL", fr, "%.1fs" % (time.time() - t0), flush=True)
if arg("--anim"):
    outd = os.path.abspath(arg("--anim")); os.makedirs(outd, exist_ok=True)
    f0, f1 = int(arg("--start", sc.frame_start)), int(arg("--end", sc.frame_end))
    skip = set(); ff_ = 1
    for sh in SHOTS:
        n_ = int(round(sh["dur"] * FPS))
        if sh["cam"] is None: skip.update(range(ff_, ff_ + n_))
        ff_ += n_
    todo = list(range(f0, f1 + 1, int(arg("--step", "1"))))
    if arg("--ranges"):
        todo = [fr for ab in arg("--ranges").split(",") for fr in range(int(ab.split("-")[0]), int(ab.split("-")[1]) + 1, int(arg("--step", "1")))]
    for fr in todo:
        p = os.path.join(outd, "f_%04d.png" % fr)
        if fr in skip or (os.path.exists(p) and os.path.getsize(p) > 1000): continue
        t0 = time.time(); sc.frame_set(fr); sc.render.filepath = p; bpy.ops.render.render(write_still=True)
        print("FRAME %d %.1fs" % (fr, time.time() - t0), flush=True)
