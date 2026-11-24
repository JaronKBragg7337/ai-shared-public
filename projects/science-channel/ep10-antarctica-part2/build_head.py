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
