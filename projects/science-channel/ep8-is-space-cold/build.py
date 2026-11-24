# Heartbeat TV Science 8.8 "Is space cold?". Pure-script Blender 5.1 scene, no downloaded assets (ep7 pipeline).
# Cycles OptiX on the RTX 4060.
import bpy, bmesh, math, random, sys, os, time
import numpy as np
from mathutils import Vector, Matrix, noise
#   blender -b -P build.py -- [--stills DIR --frames a,b,c] [--anim OUTDIR [--step 2] [--ranges a-b,c-d]] [--samples N]
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


# ================================================================ ep8 scene (Science 8.8 "Is space cold?")
# Sets (1 unit = 1 m):
#   ORBIT  an illustrated Earth (procedural land, ocean, clouds, thin atmosphere rim) seen from ~400 km, stars;
#          a GENERIC station truss with white radiator panels and solar wings (like the ISS idea, not the real station);
#          a GENERIC "data center" satellite concept (bus, long solar wings, a big white radiator array; no company's design)
#   PLATE  a metal plate in a dark vacuum chamber, heated until it glows (blackbody colour), illustration
SUNV = Vector((-.55, .62, .38)).normalized()
R_E = 6371000.0; ALT = 400000.0
EC = Vector((0, 0, -(R_E + ALT)))            # Earth centre, the station sits at the origin
ORG = {"ORBIT": Vector((0, 0, 0)), "PLATE": Vector((0, 0, 0))}
PLATE_O = Vector((0, 2000.0, 300.0))         # the chamber floats far from the station (only shown in its own shots)

# ---------------------------------------------------------------- Earth
def earth_mat():
    m, nt = mat("Earth"); ob, gen = coords(nt)
    nrm = N(nt, "ShaderNodeVectorMath"); nrm.operation = "NORMALIZE"; L(nt, ob, nrm.inputs[0]); p = nrm.outputs[0]
    land = SMOOTH(nt, NOISE(nt, p, 1.6, 9, .58), .52, .545)
    ice = SMOOTH(nt, M(nt, "ABSOLUTE", SEP(nt, p)[2]), .86, .9)
    tint = NOISE(nt, p, 5.0, 6, .6)
    lc = MIXC(nt, SMOOTH(nt, tint, .4, .62), (.035, .07, .025), (.2, .15, .085))
    lc = MIXC(nt, SMOOTH(nt, NOISE(nt, p, 22.0, 4, .6), .45, .7), lc, (.12, .11, .07))
    oc = MIXC(nt, SMOOTH(nt, NOISE(nt, p, 3.0, 4, .5), .3, .7), (.004, .018, .055), (.006, .03, .075))
    col = MIXC(nt, land, oc, lc); col = MIXC(nt, ice, col, (.8, .82, .85))
    rough = M(nt, "ADD", M(nt, "MULTIPLY", land, .55), .35)
    b = principled(nt, col, rough, spec=.18)
    finish(nt, b.outputs[0]); return m
def cloud_mat():
    m, nt = mat("Clouds"); ob, gen = coords(nt)
    nrm = N(nt, "ShaderNodeVectorMath"); nrm.operation = "NORMALIZE"; L(nt, ob, nrm.inputs[0]); p = nrm.outputs[0]
    warp = N(nt, "ShaderNodeVectorMath"); warp.operation = "ADD"; L(nt, p, warp.inputs[0])
    w2 = N(nt, "ShaderNodeCombineXYZ"); L(nt, M(nt, "MULTIPLY", NOISE(nt, p, 3.0, 3), .35), w2.inputs[0])
    L(nt, w2.outputs[0], warp.inputs[1])
    c = SMOOTH(nt, NOISE(nt, warp.outputs[0], 9.0, 10, .62), .53, .68)
    c = M(nt, "MULTIPLY", c, SMOOTH(nt, NOISE(nt, p, 2.0, 3), .4, .6))
    b = principled(nt, (.92, .93, .95), .9, spec=.2)
    tr = N(nt, "ShaderNodeBsdfTransparent"); mx = N(nt, "ShaderNodeMixShader")
    L(nt, c, mx.inputs[0]); L(nt, tr.outputs[0], mx.inputs[1]); L(nt, b.outputs[0], mx.inputs[2])
    finish(nt, mx.outputs[0]); return m
def atmo_mat():
    m, nt = mat("Atmo")
    lw = N(nt, "ShaderNodeLayerWeight"); lw.inputs["Blend"].default_value = .25
    geo = N(nt, "ShaderNodeNewGeometry"); dot = N(nt, "ShaderNodeVectorMath"); dot.operation = "DOT_PRODUCT"
    L(nt, geo.outputs["Normal"], dot.inputs[0]); dot.inputs[1].default_value = tuple(SUNV)
    lit = SMOOTH(nt, dot.outputs["Value"], -.25, .35)
    fac = M(nt, "MULTIPLY", M(nt, "POWER", lw.outputs["Facing"], 9.0), lit)
    e = N(nt, "ShaderNodeEmission"); e.inputs["Color"].default_value = (.25, .5, 1.0, 1); L(nt, M(nt, "MULTIPLY", fac, 2.5), e.inputs["Strength"])
    tr = N(nt, "ShaderNodeBsdfTransparent"); ad = N(nt, "ShaderNodeAddShader"); L(nt, tr.outputs[0], ad.inputs[0]); L(nt, e.outputs[0], ad.inputs[1])
    finish(nt, ad.outputs[0]); return m
def sphere(name, r, setname, seg=384, ring=192, loc=(0, 0, 0)):
    bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=ring, radius=r)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); me.polygons.foreach_set("use_smooth", [True] * len(me.polygons))
    o = link(bpy.data.objects.new(name, me), setname); o.location = loc; return o
earth = sphere("Earth", R_E, "ORBIT", loc=EC); earth.data.materials.append(earth_mat()); earth.rotation_euler = (1.35, .2, 1.1)
clouds = sphere("Clouds", R_E + 9000, "ORBIT", loc=EC); clouds.data.materials.append(cloud_mat()); clouds.rotation_euler = (1.5, .5, .3)
atmo = sphere("Atmo", R_E + 70000, "ORBIT", loc=EC); atmo.data.materials.append(atmo_mat())
for o in (earth, clouds, atmo): o.visible_shadow = False
if os.environ.get('DBG') == '1': clouds.scale = (.5, .5, .5); atmo.scale = (.5, .5, .5)


# ---------------------------------------------------------------- shared spacecraft materials
def white_panel_mat(name="Radiator"):
    m, nt = mat(name); ob, gen = coords(nt)
    br = N(nt, "ShaderNodeTexBrick"); br.inputs["Scale"].default_value = 1.0; br.inputs["Mortar Size"].default_value = .012
    br.inputs["Color1"].default_value = (.82, .82, .80, 1); br.inputs["Color2"].default_value = (.76, .77, .76, 1); br.inputs["Mortar"].default_value = (.42, .42, .42, 1)
    br.offset = 0.0; br.inputs["Brick Width"].default_value = 2.0; br.inputs["Row Height"].default_value = .5
    L(nt, VSCALE(nt, ob, .6, .6, .6), br.inputs["Vector"])
    dirt = SMOOTH(nt, NOISE(nt, ob, .4, 6), .3, .8)
    col = MIXC(nt, M(nt, "MULTIPLY", dirt, .25), br.outputs["Color"], (.6, .58, .52))
    b = principled(nt, col, .45, spec=.4, normal=BUMP(nt, br.outputs["Fac"], .15, .02))
    finish(nt, b.outputs[0]); return m
def solar_mat():
    m, nt = mat("Solar"); ob, gen = coords(nt)
    br = N(nt, "ShaderNodeTexBrick"); br.inputs["Scale"].default_value = 1.0; br.inputs["Mortar Size"].default_value = .02
    br.inputs["Color1"].default_value = (.012, .02, .05, 1); br.inputs["Color2"].default_value = (.016, .026, .065, 1); br.inputs["Mortar"].default_value = (.35, .3, .2, 1)
    br.offset = 0.0; br.inputs["Brick Width"].default_value = 1.0; br.inputs["Row Height"].default_value = 1.0
    L(nt, VSCALE(nt, ob, 2.2, 2.2, 2.2), br.inputs["Vector"])
    b = principled(nt, br.outputs["Color"], .18, spec=.7, coat=.3)
    finish(nt, b.outputs[0]); return m
def metal_mat(name, col, rough=.35):
    m, nt = mat(name); b = principled(nt, col, rough, metallic=1.0); finish(nt, b.outputs[0]); return m
def foil_mat():
    m, nt = mat("Foil"); ob, gen = coords(nt)
    h = NOISE(nt, ob, 3.0, 8, .7)
    b = principled(nt, (.85, .6, .25), M(nt, "ADD", M(nt, "MULTIPLY", h, .3), .12), metallic=1.0, normal=BUMP(nt, h, .5, .05))
    finish(nt, b.outputs[0]); return m
M_RAD = white_panel_mat(); M_SOL = solar_mat(); M_TRUSS = metal_mat("Truss", (.55, .56, .58), .4); M_FOIL = foil_mat()
M_MOD = white_panel_mat("Module")
def give(o, m): o.data.materials.append(m); return o

# ---------------------------------------------------------------- generic station (origin)
st = []
st.append(give(prim_box("TrussMain", (90, 2.6, 2.6), "ORBIT"), M_TRUSS))
for i in range(-14, 15):   # truss bays
    st.append(give(prim_box("Bay%d" % i, (.25, 2.9, 2.9), "ORBIT", loc=(i * 3.1, 0, 0)), M_TRUSS))
for k, x in enumerate((-22, -12, -2, 8)):   # pressurised modules below the truss, along +Y
    pass
mod = give(prim_cyl("ModA", 2.2, 16, "ORBIT", loc=(0, -9, -3.2), rot=(math.pi / 2, 0, 0)), M_MOD); st.append(mod)
mod2 = give(prim_cyl("ModB", 2.2, 14, "ORBIT", loc=(0, 8, -3.2), rot=(math.pi / 2, 0, 0)), M_MOD); st.append(mod2)
mod3 = give(prim_cyl("ModC", 2.0, 10, "ORBIT", loc=(-6, -9, -3.2), rot=(0, math.pi / 2, 0)), M_MOD); st.append(mod3)
for o in (mod, mod2, mod3): bevel(o, .2)
# radiators: on each side of the centre, three white panels hang off the truss (each ~23 m long, 3 m wide), turned edge-on to the Sun
RADS = []
for side in (-1, 1):
    for j in range(3):
        o = give(prim_box("Rad%d%d" % (side, j), (3.0, 23.0, .12), "ORBIT", loc=(side * (14 + j * 3.4), side * 12.8, 0)), M_RAD)
        o.rotation_euler = (0, math.radians(8), 0); st.append(o); RADS.append(o)
    arm = give(prim_box("RadArm%d" % side, (11, .4, .4), "ORBIT", loc=(side * 17.4, side * 1.4, 0)), M_TRUSS); st.append(arm)
# solar wings at both ends: two long blankets per side
for side in (-1, 1):
    for up in (-1, 1):
        o = give(prim_box("Sol%d%d" % (side, up), (11.5, 34, .05), "ORBIT", loc=(side * 42, up * 19.5, 0)), M_SOL); st.append(o)
        o.rotation_euler = (0, math.radians(-20), 0)
        mast = give(prim_box("Mast%d%d" % (side, up), (.3, 34, .3), "ORBIT", loc=(side * 42, up * 19.5, .1)), M_TRUSS); st.append(mast)
        mast.rotation_euler = o.rotation_euler

# ---------------------------------------------------------------- generic data-center satellite concept, 600 m away along -Y
SAT = Vector((0, -600, 20))
sat = []
bus = give(prim_box("Bus", (5, 5, 7), "ORBIT", loc=SAT), M_FOIL); bevel(bus, .15); sat.append(bus)
for side in (-1, 1):
    w = give(prim_box("SatSol%d" % side, (40, 9, .05), "ORBIT", loc=SAT + Vector((side * 24, 0, 1))), M_SOL); sat.append(w)
    y = give(prim_box("SatYoke%d" % side, (4, .3, .3), "ORBIT", loc=SAT + Vector((side * 3.8, 0, 1))), M_TRUSS); sat.append(y)
# radiator array: a stack of thin white fins below the bus, edge-on to the Sun
for k in range(10):
    f_ = give(prim_box("Fin%d" % k, (.08, 16, 9), "ORBIT", loc=SAT + Vector((-4.5 + k * 1.0, 0, -9))), M_RAD); sat.append(f_)
boom = give(prim_box("FinBoom", (10, .5, .5), "ORBIT", loc=SAT + Vector((0, 0, -4.4))), M_TRUSS); sat.append(boom)
dish = give(prim_cyl("Dish", 1.2, .25, "ORBIT", loc=SAT + Vector((0, 2.8, 3.2)), rot=(math.radians(70), 0, 0)), M_TRUSS); sat.append(dish)

sun_d = bpy.data.lights.new("Sun", "SUN"); sun_d.angle = math.radians(.53); sun_d.energy = 5.0; sun_d.color = (1.0, .98, .95)
sun = bpy.data.objects.new("Sun", sun_d); sc.collection.objects.link(sun); sun.rotation_euler = SUNV.to_track_quat("Z", "Y").to_euler()

# ---------------------------------------------------------------- PLATE: dark vacuum chamber with a heated plate
P = PLATE_O
def chamber_mat():
    m, nt = mat("Chamber"); ob, gen = coords(nt)
    h = NOISE(nt, ob, 6.0, 5); b = principled(nt, (.05, .05, .055), M(nt, "ADD", M(nt, "MULTIPLY", h, .2), .35), metallic=.8, normal=BUMP(nt, h, .1, .02))
    finish(nt, b.outputs[0]); return m
ch = prim_cyl("Chamber", 2.6, 4.0, "PLATE", verts=64, loc=P + Vector((0, 0, 1.0)))
ch.data.flip_normals(); give(ch, chamber_mat())
stand = give(prim_cyl("Stand", .05, 1.0, "PLATE", loc=P + Vector((0, 0, -.45))), M_TRUSS)
def hot_mat():
    m, nt = mat("Hot"); ob, gen = coords(nt)
    h = NOISE(nt, ob, 18.0, 6)
    b = principled(nt, (.32, .3, .29), M(nt, "ADD", M(nt, "MULTIPLY", h, .25), .3), metallic=1.0, normal=BUMP(nt, h, .2, .005))
    bb = N(nt, "ShaderNodeBlackbody"); tv = N(nt, "ShaderNodeValue"); tv.name = "temp"; tv.outputs[0].default_value = 300.0
    L(nt, tv.outputs[0], bb.inputs["Temperature"])
    sv = N(nt, "ShaderNodeValue"); sv.name = "glow"; sv.outputs[0].default_value = 0.0
    e = N(nt, "ShaderNodeEmission"); L(nt, bb.outputs[0], e.inputs["Color"])
    L(nt, M(nt, "MULTIPLY", sv.outputs[0], M(nt, "ADD", .85, M(nt, "MULTIPLY", h, .3))), e.inputs["Strength"])
    ad = N(nt, "ShaderNodeAddShader"); L(nt, b.outputs[0], ad.inputs[0]); L(nt, e.outputs[0], ad.inputs[1])
    finish(nt, ad.outputs[0]); return m, tv, sv
M_HOT, T_NODE, G_NODE = hot_mat()
plate = give(prim_box("Plate", (.8, .8, .03), "PLATE", loc=P + Vector((0, 0, .5))), M_HOT); bevel(plate, .006, 2)
plate.rotation_euler = (math.radians(70), 0, 0)
holder = give(prim_box("Holder", (.9, .06, .06), "PLATE", loc=P + Vector((0, .1, -.32))), M_TRUSS)
add_light("ChamberKey", "AREA", "PLATE", P + Vector((-1.6, -1.8, 1.6)), 60, (.7, .8, 1.0), 1.2, target=P)
add_light("ChamberRim", "AREA", "PLATE", P + Vector((1.5, 1.8, .8)), 25, (1, .95, .9), .8, target=P)
port = give(prim_cyl("Port", .45, .1, "PLATE", loc=P + Vector((2.45, .4, .6)), rot=(0, math.pi / 2, 0)), metal_mat("PortRing", (.4, .4, .42)))

# ================================================================ world: black space + stars
w = bpy.data.worlds.new("World"); sc.world = w; w.use_nodes = True; wn = w.node_tree; wn.nodes.clear()
tc = wn.nodes.new("ShaderNodeTexCoord"); vo = wn.nodes.new("ShaderNodeTexVoronoi"); vo.feature = "F1"; vo.inputs["Scale"].default_value = 420.0
wn.links.new(tc.outputs["Generated"], vo.inputs["Vector"])
def wmath(op, a, b=None):
    n = wn.nodes.new("ShaderNodeMath"); n.operation = op
    for i, x in enumerate((a, b)):
        if x is None: continue
        if lk(x): wn.links.new(x, n.inputs[i])
        else: n.inputs[i].default_value = x
    return n.outputs[0]
nz = wn.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 160.0; wn.links.new(tc.outputs["Generated"], nz.inputs["Vector"])
star = wmath("MULTIPLY", wmath("LESS_THAN", vo.outputs["Distance"], .035), wmath("MULTIPLY", wmath("POWER", nz.outputs["Fac"], 4.0), 6.0))
bg = wn.nodes.new("ShaderNodeBackground"); bg.inputs["Color"].default_value = (.85, .9, 1.0, 1); wn.links.new(wmath("ADD", star, .0004), bg.inputs["Strength"])
lp = wn.nodes.new("ShaderNodeLightPath"); bgk = wn.nodes.new("ShaderNodeBackground"); bgk.inputs["Color"].default_value = (0, 0, 0, 1)
mxw = wn.nodes.new("ShaderNodeMixShader"); wn.links.new(lp.outputs["Is Camera Ray"], mxw.inputs[0]); wn.links.new(bgk.outputs[0], mxw.inputs[1]); wn.links.new(bg.outputs[0], mxw.inputs[2])
wo_ = wn.nodes.new("ShaderNodeOutputWorld"); wn.links.new(mxw.outputs[0], wo_.inputs["Surface"])
SET_EXP = {"ORBIT": -.45, "PLATE": .2}

# ---------------------------------------------------------------- camera
cd = bpy.data.cameras.new("Cam"); cam = bpy.data.objects.new("Cam", cd); sc.collection.objects.link(cam); sc.camera = cam
cd.clip_start = .05; cd.clip_end = 9.0e6; cd.sensor_width = 36.0; cd.dof.use_dof = False
cam.rotation_mode = "QUATERNION"
def lookat(p, t, up=Vector((0, 0, 1))):
    f = (Vector(t) - Vector(p)).normalized(); r = f.cross(Vector(up)).normalized(); u = r.cross(f)
    return Matrix((r, u, -f)).transposed().to_quaternion()
HZ = Vector((0, 2.2e6, -3.9e5))   # a point near the horizon ahead (+Y)
def cam_keys(name):
    if name == "EARTH_A":    # open: drift above the Earth toward the horizon, the station far below frame
        return [(0, Vector((0, -60, 160)), Vector((0, 2.2e6, -1.1e6)), 24), (1, Vector((0, 40, 175)), Vector((2.0e5, 2.2e6, -1.0e6)), 24)]
    if name == "STATION_A":  # station with its white radiators, Earth below
        return [(0, Vector((-70, -95, 42)), Vector((0, 0, -2)), 30), (1, Vector((-40, -110, 30)), Vector((4, 0, -3)), 30)]
    if name == "STATION_B":  # along one radiator wing
        return [(0, Vector((-2, -36, 9)), Vector((-17, -10, 0)), 28), (1, Vector((-4, -30, 6)), Vector((-18, -12, 0)), 28)]
    if name == "SAT_A":      # data-center satellite concept
        s = SAT; return [(0, s + Vector((-60, -75, 30)), s + Vector((0, 0, -3)), 35), (1, s + Vector((-30, -80, 18)), s + Vector((0, 0, -4)), 35)]
    if name == "SAT_B":      # close on the radiator fins
        s = SAT; return [(0, s + Vector((-30, -34, 4)), s + Vector((2, 0, -6)), 35), (1, s + Vector((-24, -36, 3)), s + Vector((2, 0, -8)), 35)]
    if name == "PLATE_A":    # the plate heats up in the chamber
        p = PLATE_O; return [(0, p + Vector((-.9, -1.9, .55)), p + Vector((0, 0, .45)), 40), (1, p + Vector((-.45, -1.45, .4)), p + Vector((0, 0, .45)), 40)]
    if name == "EARTH_Z":    # end: pull back from the station until it is a speck over the Earth
        return [(0, Vector((-50, -80, 25)), Vector((0, 0, -2)), 30), (.6, Vector((-180, -420, 140)), Vector((0, 0, -8)), 30),
                (1, Vector((-300, -900, 420)), Vector((0, 2.2e6, -6.0e5)), 30)]
    raise KeyError(name)

def key_vis(o, frame, hidden):
    o.hide_render = hidden; o.keyframe_insert("hide_render", frame=frame)
allsets = list(SETS.keys())
f = 1; cut = set(); SHOT_SET = {"EARTH": "ORBIT", "STATION": "ORBIT", "SAT": "ORBIT", "PLATE": "PLATE"}
for sh in SHOTS:
    n = int(round(sh["dur"] * FPS)); fa, fb = f, f + n - 1
    if sh["cam"] is None: f = fb + 1; continue
    cut.add(fb)
    setname = SHOT_SET[sh["cam"].split("_")[0]]
    for s_ in allsets:
        for o in SETS[s_]: key_vis(o, fa, s_ != setname)
    sun_d.energy = 5.0 if setname == "ORBIT" else 0.0; sun_d.keyframe_insert("energy", frame=fa)
    sc.view_settings.exposure = SET_EXP[setname]; sc.view_settings.keyframe_insert("exposure", frame=fa)
    for u, p, t, lens in cam_keys(sh["cam"]):
        ff = int(round(fa + (fb - fa) * u))
        cam.location = p; cam.rotation_quaternion = lookat(p, t)
        cam.keyframe_insert("location", frame=ff); cam.keyframe_insert("rotation_quaternion", frame=ff)
        cd.lens = lens; cd.keyframe_insert("lens", frame=ff)
    if sh["cam"] == "PLATE_A":   # 300 K (dark) -> ~1,100 K (orange glow); visible glow starts near 800 K
        for u, T, g in ((0, 300, 0), (.15, 300, 0), (.45, 750, 0.0), (.7, 950, .012), (1, 1100, .07)):
            ff = int(round(fa + (fb - fa) * u))
            T_NODE.outputs[0].default_value = T; T_NODE.outputs[0].keyframe_insert("default_value", frame=ff)
            G_NODE.outputs[0].default_value = g; G_NODE.outputs[0].keyframe_insert("default_value", frame=ff)
    if sh["cam"].startswith("EARTH") or sh["cam"].startswith("STATION") or sh["cam"].startswith("SAT"):
        clouds.rotation_euler = (1.5, .5, .3); clouds.keyframe_insert("rotation_euler", frame=fa)
        clouds.rotation_euler = (1.5, .5, .3 + .0008 * (fb - fa) / FPS); clouds.keyframe_insert("rotation_euler", frame=fb)
    f = fb + 1
def all_curves(idb):
    ad = idb.animation_data
    if not ad or not ad.action: return []
    cs = getattr(ad.action, "fcurves", None)
    if cs is not None: return list(cs)
    try: return [fc for layer in ad.action.layers for strip in layer.strips for bag in strip.channelbags for fc in bag.fcurves]
    except Exception: return []
SMOOTH_ANIM = {clouds.name}
for idb in list(bpy.data.objects) + list(bpy.data.materials) + list(bpy.data.lights) + [w.node_tree, sc]:
    for fc in all_curves(idb):
        for k in fc.keyframe_points: k.interpolation = "LINEAR" if getattr(idb, "name", "") in SMOOTH_ANIM or idb == M_HOT else "CONSTANT"
for fc in all_curves(M_HOT.node_tree):
    for k in fc.keyframe_points: k.interpolation = "LINEAR"
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
