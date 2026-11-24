# Heartbeat TV Science 8.7 "Antarctica: what's frozen in the ice" (Part 1).  Pure-script Blender 5.1 scene, no downloaded
# assets (same rule and pipeline as ep6 Phobos).  Scene unit = 1 m.  Nine small "sets", each 20 km apart on +X, only the
# set a shot uses is visible in that shot:
#   FIELD   a wind-scoured blue-ice field with low rocky hills (the look of a blue-ice area like the Allan Hills; not a map)
#   CHUNK   a block of old ice full of air bubbles, close up (illustration)
#   CORES   ice-core sections on a lab table, banded (illustration)
#   SEA     dark seafloor, a sediment core pulled up from the mud, marine snow (illustration)
#   DIATOM  glass-shelled diatoms drifting, macro (illustration, not to scale)
#   MICRO   bacteria, clay grains and short DNA fragments; one fragment taken up; cells dividing (illustration)
#   LAKE    a cutaway: ice sheet over a liquid lake over bedrock, heights stretched (illustration)
#   SHELF   an ice-shelf front over the ocean, icebergs, a rocky shore
#   STATION a generic research station at night, aurora (illustration; not any real station)
# Cycles OptiX on the RTX 4060.
#   blender -b -P build.py -- [--stills DIR --frames a,b,c] [--anim OUTDIR [--start F --end F --step 2] [--ranges a-b,c-d]]
#                             [--samples N] [--w 1280 --h 720] [--save out.blend]
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

# ---------------------------------------------------------------- set origins
ORG = {k: Vector((20000.0 * i, 0, 0)) for i, k in enumerate(["FIELD", "CHUNK", "CORES", "SEA", "DIATOM", "MICRO", "LAKE", "SHELF", "STATION"])}
SUN_EL, SUN_AZ = 9.0, 200.0          # low polar sun (deg above horizon, deg azimuth from +Y toward +X)
def sun_vec(el=SUN_EL, az=SUN_AZ):
    e, a = math.radians(el), math.radians(az); return Vector((math.sin(a) * math.cos(e), math.cos(a) * math.cos(e), math.sin(e)))
SUNV = sun_vec()

# ================================================================ shared ice / snow materials
def snow_mat(name="Snow"):
    m, nt = mat(name); pos, gen = coords(nt)
    st = VSCALE(nt, pos, .35, 2.4, 1.0)                                   # sastrugi: stretched along the wind (x)
    h = M(nt, "ADD", M(nt, "MULTIPLY", NOISE(nt, st, 1.2, 5, .6), .7), M(nt, "MULTIPLY", NOISE(nt, pos, 18.0, 3, .5), .3))
    col = MIXC(nt, NOISE(nt, pos, .05, 3, .5), (.86, .90, .97), (.95, .97, 1.0))
    b = principled(nt, col, .62, .45, BUMP(nt, h, .35, .25), sss=.25, sss_r=(.5, .75, 1.0)); finish(nt, b.outputs[0]); return m
def blue_ice_field_mat():
    """wind-scoured blue ice with snow patches: blue glaze, sun-cup scallops, crack lines; snow drifts in the hollows"""
    m, nt = mat("BlueIceField"); pos, gen = coords(nt)
    sx = SEP(nt, pos)
    patches = SMOOTH(nt, M(nt, "ADD", NOISE(nt, VSCALE(nt, pos, .006, .02, 1), 1.0, 5, .62), M(nt, "MULTIPLY", NOISE(nt, pos, .4, 3, .5), .12)), .60, .68)
    scal = VORO(nt, pos, 2.2, "SMOOTH_F1"); cr = VORO(nt, pos, .35, "DISTANCE_TO_EDGE")
    crack = M(nt, "SUBTRACT", 1.0, SMOOTH(nt, cr.outputs["Distance"], 0.0, .012))
    ice_col = MIXC(nt, NOISE(nt, pos, .08, 4, .55), (.12, .30, .52), (.30, .52, .76))
    ice_col = MIXC(nt, M(nt, "MULTIPLY", crack, .5), ice_col, (.82, .90, .97))
    ice_h = M(nt, "ADD", M(nt, "MULTIPLY", scal.outputs["Distance"], .6), M(nt, "MULTIPLY", crack, -.15))
    st = VSCALE(nt, pos, .35, 2.4, 1.0)
    snow_h = M(nt, "ADD", M(nt, "MULTIPLY", NOISE(nt, st, 1.2, 5, .6), .8), .2)
    h = M(nt, "ADD", M(nt, "MULTIPLY", ice_h, M(nt, "SUBTRACT", 1.0, patches)), M(nt, "MULTIPLY", snow_h, patches))
    col = MIXC(nt, patches, ice_col, (.93, .96, 1.0))
    rough = M(nt, "ADD", .06, M(nt, "MULTIPLY", patches, .55))
    b = principled(nt, col, rough, .5, BUMP(nt, h, .28, .3), sss=.2, sss_r=(.4, .7, 1.0), coat=.3)
    finish(nt, b.outputs[0]); return m
def rock_mat(name="Rock", base=(.03, .029, .028), snowcap=True):
    m, nt = mat(name); pos, gen = coords(nt)
    n1 = NOISE(nt, pos, .08, 5, .6); n2 = NOISE(nt, pos, 1.5, 5, .6)
    vo = VORO(nt, pos, .6, "DISTANCE_TO_EDGE")
    col = MIXC(nt, n1, base, (base[0] * 1.9, base[1] * 1.8, base[2] * 1.7))
    col = MIXC(nt, M(nt, "MULTIPLY", SMOOTH(nt, n2, .45, .7), .5), col, (.05, .04, .034))
    h = M(nt, "ADD", M(nt, "MULTIPLY", n2, .8), M(nt, "MULTIPLY", SMOOTH(nt, vo.outputs["Distance"], 0, .08), .15))
    nrm = BUMP(nt, h, .6, .5)
    if snowcap:
        g = N(nt, "ShaderNodeNewGeometry"); nz = SEP(nt, g.outputs["Normal"])[2]
        snow = SMOOTH(nt, M(nt, "ADD", nz, M(nt, "MULTIPLY", M(nt, "SUBTRACT", NOISE(nt, pos, .25, 4, .6), .5), .9)), .86, .95)
        col = MIXC(nt, snow, col, (.9, .93, .98))
    b = principled(nt, col, .85, .3, nrm); finish(nt, b.outputs[0]); return m
SNOW = snow_mat(); ROCK = rock_mat(); BLUEICE = blue_ice_field_mat()

# ================================================================ FIELD
O = ORG["FIELD"]
def field_h(X, Y):
    big = fbm2(X, Y, 1 / 900.0, 3, 1.3) * 9.0
    swell = np.sin(X / 140.0) * .8 + fbm2(X, Y, 1 / 120.0, 2, 4.1) * 1.4
    # the ground rises toward the hills (blue ice areas sit where ice flows against a barrier)
    rise = np.clip((Y - 300) / 1200.0, 0, 1) ** 2 * 25
    return big + swell + rise
fld = grid("FieldIce", 3600, 3600, 300, 300, field_h, "FIELD", O); fld.data.materials.append(BLUEICE)
# far snow plain to the horizon
far = grid("FarSnow", 60000, 60000, 1, 1, lambda X, Y: X * 0 - 3.0, "FIELD", O); far.data.materials.append(SNOW)
# low dark hills / nunataks on the far side (Allan Hills-like: low, a few hundred metres, wind-swept)
hills = []
for i, (x, y, r, h, sd) in enumerate([(-900, 1700, 260, .55, 1), (-350, 1950, 340, .42, 2), (300, 1800, 220, .7, 3), (900, 2100, 420, .38, 4),
                                       (1600, 1650, 250, .5, 5), (-1700, 2300, 380, .33, 6), (2400, 2500, 500, .3, 7), (-2600, 1900, 300, .45, 8)]):
    b = blob("Hill%d" % i, r, sd * 3.3, "FIELD", 6, .42, 2.6, (1.3, 1.0, h * 1.5), flat_bottom=-.15)
    b.location = O + Vector((x, y, 10 + max(0, (y - 300) / 1200.0) ** 2 * 25 - 25)); b.rotation_euler = (0, 0, sd)
    b.data.materials.append(ROCK); hills.append(b)
# a few wind-scoured boulders near the low camera path (moraine rocks sit on blue ice fields)
for i in range(40):
    rx, ry = random.uniform(-60, 60), random.uniform(-40, 160)
    b = blob("Bould%d" % i, random.uniform(.15, .9), i * 1.7, "FIELD", 3, .3, 1.3, (1, 1, .6), flat_bottom=-.25)
    b.location = O + Vector((rx, ry, float(field_h(np.array([[rx]]), np.array([[ry]]))[0, 0]) - .05)); b.data.materials.append(ROCK)
    b.rotation_euler = (0, 0, random.random() * 6)
def fh(x, y): return float(field_h(np.array([[x]]), np.array([[y]]))[0, 0])
# drifting snow over the ice (spindrift): a thin low volume
spd = prim_box("Spindrift", (900, 900, 1.6), "FIELD", loc=O + Vector((0, 200, 0.6)))
vm, nt = mat("Spindrift"); pos, gen = coords(nt)
den = M(nt, "MULTIPLY", SMOOTH(nt, NOISE(nt, VSCALE(nt, pos, .02, .25, 3.0), 4.0, 4, .6), .55, .75), M(nt, "SUBTRACT", 1.0, SEP(nt, gen)[2]))
pv = N(nt, "ShaderNodeVolumePrincipled"); pv.inputs["Color"].default_value = (.95, .97, 1, 1); L(nt, M(nt, "MULTIPLY", den, .35), pv.inputs["Density"])
L(nt, pv.outputs[0], nt.nodes["OUT"].inputs["Volume"]); spd.data.materials.append(vm)

# ================================================================ CHUNK: a block of old blue ice with air bubbles
O = ORG["CHUNK"]
g = grid("ChunkGround", 40, 40, 80, 80, lambda X, Y: fbm2(X, Y, 1 / 8.0, 3, 9.1) * .25, "CHUNK", O); g.data.materials.append(BLUEICE)
farc = grid("ChunkFar", 30000, 30000, 1, 1, lambda X, Y: X * 0 - 1.0, "CHUNK", O); farc.data.materials.append(SNOW)
bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0)
bmesh.ops.subdivide_edges(bm, edges=bm.edges[:], cuts=8, use_grid_fill=True)
for v in bm.verts:
    d = v.co.copy(); v.co = Vector((d.x * .55, d.y * .42, d.z * .46)) * (1 + .06 * noise.noise(d * 2.3 + Vector((3, 1, 2))))
me = bpy.data.meshes.new("IceChunk"); bm.to_mesh(me); bm.free(); me.update()
chunk = link(bpy.data.objects.new("IceChunk", me), "CHUNK"); chunk.location = O + Vector((0, 0, .15)); chunk.rotation_euler = (0, .05, .35)
sub = chunk.modifiers.new("sub", "SUBSURF"); sub.levels = 2; sub.render_levels = 2
cm, nt = mat("OldIce"); pos, gen = coords(nt)
nrm = BUMP(nt, M(nt, "ADD", NOISE(nt, pos, 6.0, 4, .6), M(nt, "MULTIPLY", VORO(nt, pos, 9.0, "SMOOTH_F1").outputs["Distance"], .5)), .12, .02)
b = principled(nt, MIXC(nt, NOISE(nt, pos, 3.0, 2, .5), (.80, .90, .98), (.70, .85, .97)), M(nt, "ADD", .03, M(nt, "MULTIPLY", NOISE(nt, pos, 4.0, 3, .5), .06)), .5, nrm, trans=1.0, ior=1.31)
finish(nt, b.outputs[0]); chunk.data.materials.append(cm)
# bubbles: in bands (each band = one season's air), radius 0.5-4 mm
bub_m, nt = mat("AirBubble"); b = principled(nt, (1, 1, 1), 0.0, .5, trans=1.0, ior=1.0 / 1.31); finish(nt, b.outputs[0])
bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, segments=16, ring_count=8); bsrc = bpy.context.object; bsrc.name = "BubbleSrc"
for c in bsrc.users_collection: c.objects.unlink(c.objects[bsrc.name]) if False else c.objects.unlink(bsrc)
bsrc.data.polygons.foreach_set("use_smooth", [True] * len(bsrc.data.polygons)); bsrc.data.materials.append(bub_m)
pts, scs = [], []
rs = random.Random(5)
inv = chunk.matrix_world.copy()
for i in range(900):
    while True:
        p = Vector((rs.uniform(-.52, .52), rs.uniform(-.36, .36), rs.uniform(-.28, .28)))
        band = math.sin(p.z * 60 + noise.noise(p * 4) * 2)
        if (p.x / .55) ** 2 + (p.y / .39) ** 2 + (p.z / .31) ** 2 < 1 and rs.random() < .35 + .65 * (band > .3): break
    pts.append(chunk.location + Matrix.Rotation(.35, 3, "Z") @ p); scs.append(.0005 + .0035 * rs.random() ** 2.5)
scatter_instances("Bub", bsrc, pts, scs, "CHUNK")
for i in range(6):   # a few loose ice shards around the block
    s = blob("Shard%d" % i, rs.uniform(.04, .12), i * 2.1, "CHUNK", 3, .25, 1.5, (1, .8, .6), flat_bottom=-.4)
    a = rs.random() * 6.28; s.location = O + Vector((math.cos(a) * rs.uniform(.8, 1.6), math.sin(a) * rs.uniform(.8, 1.6), .02)); s.data.materials.append(cm)

# ================================================================ CORES: ice-core sections on a lab table
O = ORG["CORES"]
tbl = prim_box("Table", (3.2, 1.2, .05), "CORES", loc=O + Vector((0, 0, .9))); bevel(tbl, .005)
tm, nt = mat("Steel"); pos, gen = coords(nt)
br = NOISE(nt, VSCALE(nt, pos, 40, 1200, 1), 1.0, 2, .5)
b = principled(nt, (.62, .64, .66), M(nt, "ADD", .22, M(nt, "MULTIPLY", br, .12)), .5, metallic=1.0); finish(nt, b.outputs[0]); tbl.data.materials.append(tm)
room = prim_box("Room", (14, 10, 6), "CORES", loc=O + Vector((0, 0, 3)))
rmm, nt = mat("RoomWall"); b = principled(nt, (.10, .11, .13), .8, .2); finish(nt, b.outputs[0]); room.data.materials.append(rmm)
def core_mat(name, seed, depth_scale):
    """translucent milky ice; bands = annual / seasonal layers, thinner deeper; scattered bubble haze"""
    m, nt = mat(name); pos, gen = coords(nt)
    x = SEP(nt, pos)[2]   # cylinders are made along local Z
    w = N(nt, "ShaderNodeTexWave"); w.wave_type = "BANDS"; w.bands_direction = "Z"; w.inputs["Scale"].default_value = 6.0 * depth_scale
    w.inputs["Distortion"].default_value = 3.0; w.inputs["Detail"].default_value = 3.0; L(nt, pos, w.inputs["Vector"])
    band = SMOOTH(nt, w.outputs["Fac"], .35, .75)
    haze = NOISE(nt, M(nt, "MULTIPLY", x, 1.0) if False else pos, 30.0, 3, .5)
    col = MIXC(nt, band, (.70, .80, .88), (.92, .95, .98))
    col = MIXC(nt, M(nt, "MULTIPLY", haze, .25), col, (.98, .99, 1.0))
    b = principled(nt, col, M(nt, "ADD", .18, M(nt, "MULTIPLY", band, .2)), .5, BUMP(nt, NOISE(nt, pos, 60.0, 3, .5), .05, .005),
                   trans=.35, ior=1.31, sss=1.0, sss_r=(.8, .9, 1.0))
    b.inputs["Subsurface Scale"].default_value = .03
    finish(nt, b.outputs[0]); return m
for i, (y, ds, ln) in enumerate([(-.3, 1.0, 1.0), (0.0, 2.6, 1.0), (.3, 6.0, .8)]):
    c = prim_cyl("Core%d" % i, .049, ln, "CORES", 64, O + Vector((-.15 + i * .12, y, .937 + .049)), (0, math.radians(90), 0)); bevel(c, .004, 2)
    c.data.polygons.foreach_set("use_smooth", [True] * len(c.data.polygons)); c.data.materials.append(core_mat("Core%dM" % i, i, ds))
    tray = prim_box("Tray%d" % i, (ln + .08, .13, .012), "CORES", loc=O + Vector((-.15 + i * .12, y, .931)))
    trm, nt = mat("TrayM%d" % i); bb = principled(nt, (.85, .87, .9), .35, .5); finish(nt, bb.outputs[0]); tray.data.materials.append(trm)
# a small paper tag by each core (blank; no fake writing)
for i, y in enumerate([-.3, 0, .3]):
    t = prim_box("Tag%d" % i, (.07, .045, .002), "CORES", loc=O + Vector((-.62 + i * .12, y + .095, .937)))
    tgm, nt = mat("Tag%d" % i); bb = principled(nt, (.85, .82, .72), .7, .3); finish(nt, bb.outputs[0]); t.data.materials.append(tgm)
add_light("LabKey", "AREA", "CORES", O + Vector((.4, -1.0, 2.6)), 60, (1.0, .97, .92), 1.6, target=O + Vector((0, 0, .95)))
add_light("LabFill", "AREA", "CORES", O + Vector((-1.6, 1.2, 2.0)), 15, (.78, .86, 1.0), 2.0, target=O + Vector((0, 0, .95)))
add_light("LabBack", "AREA", "CORES", O + Vector((0, 2.0, 1.4)), 30, (.7, .85, 1.0), 1.0, target=O + Vector((0, 0, .95)))

# ================================================================ SEA: seafloor + sediment core
O = ORG["SEA"]
sf = grid("Seafloor", 60, 60, 160, 160, lambda X, Y: fbm2(X, Y, 1 / 9.0, 4, 2.2) * .6 + fbm2(X, Y, .6, 2, 5.5) * .05, "SEA", O)
sm, nt = mat("Mud"); pos, gen = coords(nt)
h = M(nt, "ADD", M(nt, "MULTIPLY", NOISE(nt, pos, 3.0, 5, .6), .6), M(nt, "MULTIPLY", VORO(nt, pos, 7.0, "SMOOTH_F1").outputs["Distance"], .4))
col = MIXC(nt, NOISE(nt, pos, .4, 4, .55), (.09, .085, .07), (.17, .16, .12))
b = principled(nt, col, .95, .2, BUMP(nt, h, .5, .05)); finish(nt, b.outputs[0]); sf.data.materials.append(sm)
for i in range(30):   # a few dropstones (rocks carried out by icebergs and dropped on the seafloor)
    s = blob("Drop%d" % i, random.uniform(.05, .3), i * 1.3, "SEA", 3, .3, 1.4, (1, 1, .7), flat_bottom=-.3)
    s.location = O + Vector((random.uniform(-8, 8), random.uniform(-3, 12), -.05)); s.data.materials.append(rock_mat("DropM", (.05, .05, .05), False))
pipe = prim_cyl("DrillPipe", .14, 30, "SEA", 48, O + Vector((0, 4, 15.0))); bevel(pipe, .01, 2)
pm, nt = mat("PipeSteel"); pos, gen = coords(nt)
rust = SMOOTH(nt, NOISE(nt, pos, 2.0, 5, .6), .5, .7)
b = principled(nt, MIXC(nt, rust, (.32, .33, .35), (.25, .13, .06)), M(nt, "ADD", .35, M(nt, "MULTIPLY", rust, .4)), .5, metallic=M(nt, "SUBTRACT", 1.0, rust))
finish(nt, b.outputs[0]); pipe.data.materials.append(pm)
core = prim_cyl("SedCore", .11, 2.4, "SEA", 48, O + Vector((0, 4, 0)))
km, nt = mat("SedCoreM"); pos, gen = coords(nt)
w = N(nt, "ShaderNodeTexWave"); w.wave_type = "BANDS"; w.bands_direction = "Z"; w.inputs["Scale"].default_value = 3.5; w.inputs["Distortion"].default_value = 4.0; L(nt, gen, w.inputs["Vector"])
col = MIXC(nt, w.outputs["Fac"], (.16, .15, .11), (.30, .28, .20))
col = MIXC(nt, SMOOTH(nt, NOISE(nt, VSCALE(nt, gen, 1, 1, 12), 3.0, 3, .5), .6, .7), col, (.40, .37, .28))
b = principled(nt, col, .75, .4, BUMP(nt, NOISE(nt, pos, 40.0, 3, .5), .3, .01)); finish(nt, b.outputs[0]); core.data.materials.append(km)
core.parent = pipe; core.location = (0, 0, -15.0 - 1.2 + .05); pipe.location = O + Vector((0, 4, 15.0))
# marine snow
ms_src = blob("SnowSrc", 1.0, 1, "SEA", 1, .3, 1.0); ms_src.hide_render = True
msm, nt = mat("MarineSnow"); b = principled(nt, (.75, .78, .72), .9, .2); finish(nt, b.outputs[0]); ms_src.data.materials.append(msm)
pts = [O + Vector((random.uniform(-6, 6), random.uniform(-2, 12), random.uniform(0, 7))) for _ in range(700)]
snow_objs = scatter_instances("MS", ms_src, pts, [random.uniform(.004, .015) for _ in pts], "SEA")
SETS["SEA"].remove(ms_src)
# deep water: a faint blue volume so the lamp beam shows
wv = prim_box("SeaWater", (40, 40, 16), "SEA", loc=O + Vector((0, 4, 7.9)))
wm_, nt = mat("SeaWater"); pv = N(nt, "ShaderNodeVolumePrincipled"); pv.inputs["Color"].default_value = (.3, .6, .75, 1); pv.inputs["Density"].default_value = .05
pv.inputs["Absorption Color"].default_value = (.05, .3, .5, 1)
L(nt, pv.outputs[0], nt.nodes["OUT"].inputs["Volume"]); wv.data.materials.append(wm_)
add_light("SeaLamp", "SPOT", "SEA", O + Vector((-2.5, -3.0, 5.0)), 5000, (.85, .93, 1.0), .2, target=O + Vector((0, 4, .5)), spot=45)
add_light("SeaLamp2", "SPOT", "SEA", O + Vector((3.0, -2.0, 4.0)), 2000, (.8, .9, 1.0), .2, target=O + Vector((0, 4, 1.0)), spot=40)

# ================================================================ DIATOM: glass-shelled algae, macro (units = 10 micrometres)
O = ORG["DIATOM"]
def diatom_mat(name, kind, tint):
    m, nt = mat(name); pos, gen = coords(nt); s = SEP(nt, pos)
    if kind == "centric":
        ang = M(nt, "ARCTAN2", s[1], s[0]); rad = M(nt, "SQRT", M(nt, "ADD", M(nt, "POWER", s[0], 2.0), M(nt, "POWER", s[1], 2.0)))
        ribs = M(nt, "SINE", M(nt, "MULTIPLY", ang, 56.0)); rings = M(nt, "SINE", M(nt, "MULTIPLY", rad, 46.0))
        pat = M(nt, "MULTIPLY", SMOOTH(nt, ribs, .1, .8), SMOOTH(nt, rings, -.2, .6))
    else:
        stri = M(nt, "SINE", M(nt, "MULTIPLY", s[0], 30.0)); mid = SMOOTH(nt, M(nt, "ABSOLUTE", s[1]), .03, .08)
        pat = M(nt, "MULTIPLY", SMOOTH(nt, stri, .0, .7), mid)
    nrm = BUMP(nt, pat, .45, .02)
    glass = principled(nt, (.92, .95, .9), .08, .5, nrm, trans=.85, ior=1.43)
    # golden-brown chloroplasts seen through the glass
    plast = principled(nt, tint, .5, .3, nrm, sss=1.0, sss_r=(1, .6, .3))
    mx = N(nt, "ShaderNodeMixShader"); L(nt, M(nt, "MULTIPLY", SMOOTH(nt, NOISE(nt, pos, 2.5, 3, .5), .45, .62), .55), mx.inputs[0])
    L(nt, glass.outputs[0], mx.inputs[1]); L(nt, plast.outputs[0], mx.inputs[2]); finish(nt, mx.outputs[0]); return m
cen_m = diatom_mat("Centric", "centric", (.55, .38, .12)); pen_m = diatom_mat("Pennate", "pennate", (.50, .40, .14))
diatoms = []
rs = random.Random(11)
for i in range(26):
    if i % 3 != 2:
        r = rs.uniform(.5, 1.2); d = prim_cyl("Cen%d" % i, r, r * .45, "DIATOM", 64); bevel(d, r * .18, 4); d.data.materials.append(cen_m)
    else:
        d = capsule("Pen%d" % i, rs.uniform(1.6, 3.2), .32, "DIATOM", 32, 16); d.scale = (1, 1, .55); d.data.materials.append(pen_m)
    d.data.polygons.foreach_set("use_smooth", [True] * len(d.data.polygons))
    d.location = O + Vector((rs.uniform(-7, 7), rs.uniform(-1, 16), rs.uniform(-3, 4))); d.rotation_euler = (rs.uniform(0, 6.3), rs.uniform(0, 6.3), rs.uniform(0, 6.3))
    diatoms.append(d)
add_light("DiaBack", "AREA", "DIATOM", O + Vector((0, 24, 2)), 9000, (.75, .92, 1.0), 14, target=O + Vector((0, 4, 0)))
add_light("DiaKey", "AREA", "DIATOM", O + Vector((-6, -6, 8)), 1400, (1.0, .96, .88), 6, target=O + Vector((0, 4, 0)))
dw = prim_box("DiaWater", (40, 50, 30), "DIATOM", loc=O + Vector((0, 8, 0)))
dwm, nt = mat("DiaWater"); pv = N(nt, "ShaderNodeVolumePrincipled"); pv.inputs["Color"].default_value = (.5, .8, .8, 1); pv.inputs["Density"].default_value = .012
L(nt, pv.outputs[0], nt.nodes["OUT"].inputs["Volume"]); dw.data.materials.append(dwm)

# ================================================================ MICRO: bacteria, clay, DNA fragments (units = 1 micrometre)
O = ORG["MICRO"]
def cell_mat(name, col, glow=0.0):
    m, nt = mat(name); pos, gen = coords(nt)
    nrm = BUMP(nt, NOISE(nt, pos, 6.0, 4, .6), .15, .05)
    b = principled(nt, MIXC(nt, NOISE(nt, pos, 2.0, 3, .5), col, tuple(min(1, c * 1.3) for c in col)), .35, .5, nrm, sss=1.0, sss_r=(.9, .8, .6), coat=.5)
    b.inputs["Subsurface Scale"].default_value = .25
    if glow: b.inputs["Emission Color"].default_value = tuple(col) + (1,); b.inputs["Emission Strength"].default_value = glow
    finish(nt, b.outputs[0]); return m
CELL = cell_mat("Cell", (.42, .58, .50)); CELL_W = cell_mat("CellWin", (.70, .62, .38), .08)
clay_m, nt = mat("Clay"); pos, gen = coords(nt)
b = principled(nt, MIXC(nt, NOISE(nt, pos, 3.0, 4, .5), (.30, .22, .15), (.45, .35, .24)), .8, .3, BUMP(nt, NOISE(nt, pos, 9.0, 4, .6), .4, .03)); finish(nt, b.outputs[0])
dna_m, nt = mat("DNA"); b = principled(nt, (.95, .62, .20), .3, .5, coat=.6); b.inputs["Emission Color"].default_value = (1, .6, .2, 1); b.inputs["Emission Strength"].default_value = .6; finish(nt, b.outputs[0])
def dna_frag(name, turns, setname, rad=.11, pitch=.5):
    """a short double helix: two strands (curves with a round bevel) + rungs"""
    cu = bpy.data.curves.new(name, "CURVE"); cu.dimensions = "3D"; cu.bevel_depth = rad * .22; cu.bevel_resolution = 3
    n = int(turns * 20)
    for ph in (0.0, math.pi * .8):
        sp = cu.splines.new("POLY"); sp.points.add(n - 1)
        for i in range(n):
            t = i / 20 * 2 * math.pi; sp.points[i].co = (rad * math.cos(t + ph), rad * math.sin(t + ph), pitch * i / 20, 1)
    for i in range(0, n, 2):
        t = i / 20 * 2 * math.pi; sp = cu.splines.new("POLY"); sp.points.add(1)
        sp.points[0].co = (rad * math.cos(t), rad * math.sin(t), pitch * i / 20, 1); sp.points[1].co = (rad * math.cos(t + math.pi * .8), rad * math.sin(t + math.pi * .8), pitch * i / 20, 1)
    o = bpy.data.objects.new(name, cu); link(o, setname); cu.materials.append(dna_m); return o
# clay grains: thin, irregular hexagonal plates in a loose pile
clays = []
for i in range(28):
    c = prim_cyl("Clay%d" % i, random.uniform(.4, 1.1), .06, "MICRO", 6); bevel(c, .015, 2); c.data.materials.append(clay_m)
    c.location = O + Vector((random.uniform(-2.5, 2.5), random.uniform(-1.5, 1.5), random.uniform(-.6, .4)))
    c.rotation_euler = (random.uniform(-.9, .9), random.uniform(-.9, .9), random.uniform(0, 6.3)); clays.append(c)
frags = []
for i in range(14):   # short fragments stuck on the grains
    f = dna_frag("Frag%d" % i, random.uniform(1.0, 2.5), "MICRO"); c = clays[i]
    f.location = c.location + Vector((random.uniform(-.3, .3), random.uniform(-.3, .3), .08)); f.rotation_euler = (random.uniform(1.2, 1.9), 0, random.uniform(0, 6.3)); frags.append(f)
# bacteria around the pile, plus the "taker" cell and the fragment it takes up
bacts = []
for i in range(9):
    b_ = capsule("Bac%d" % i, random.uniform(.9, 1.6), .32, "MICRO"); b_.data.materials.append(CELL)
    a = i / 9 * 6.28; b_.location = O + Vector((math.cos(a) * random.uniform(3.2, 5.5), math.sin(a) * random.uniform(2.5, 4.5) + 1.0, random.uniform(-.8, 1.2)))
    b_.rotation_euler = (random.uniform(0, .6), random.uniform(-.4, .4), random.uniform(0, 6.3)); bacts.append(b_)
taker = capsule("Taker", 1.5, .36, "MICRO"); taker.data.materials.append(CELL); taker.location = O + Vector((1.4, -2.6, .9)); taker.rotation_euler = (0, .15, .4)
loose = dna_frag("LooseFrag", 1.6, "MICRO"); loose.location = O + Vector((-.2, -1.0, .6)); loose.rotation_euler = (1.4, 0, .9)
add_light("MicKey", "AREA", "MICRO", O + Vector((-4, -6, 6)), 900, (1, .95, .88), 4, target=O)
add_light("MicRim", "AREA", "MICRO", O + Vector((3, 7, 2)), 1500, (.6, .8, 1.0), 4, target=O)
mw = prim_box("MicWater", (40, 40, 20), "MICRO", loc=O)
mwm, nt = mat("MicWater"); pv = N(nt, "ShaderNodeVolumePrincipled"); pv.inputs["Color"].default_value = (.6, .8, .85, 1); pv.inputs["Density"].default_value = .015
L(nt, pv.outputs[0], nt.nodes["OUT"].inputs["Volume"]); mw.data.materials.append(mwm)
# the dividing population (shot M3), off to one side of the clay pile so the camera can look at it alone
POP = O + Vector((0, 22, 0))
pop = []   # (object, birth frame offset fraction, parent position, direction)
rsd = random.Random(21)
base_cells = []
for i in range(16):
    p = POP + Vector((rsd.uniform(-6, 6), rsd.uniform(-3, 3), rsd.uniform(-2, 2)))
    o = capsule("Pop%d" % i, rsd.uniform(1.0, 1.4), .32, "MICRO"); o.location = p; o.rotation_euler = (rsd.uniform(0, .5), rsd.uniform(-.3, .3), rsd.uniform(0, 6.3))
    win = i in (2, 7, 11); o.data.materials.append(CELL_W if win else CELL); base_cells.append((o, win))
add_light("PopKey", "AREA", "MICRO", POP + Vector((-5, -8, 7)), 1200, (1, .95, .88), 5, target=POP)
add_light("PopRim", "AREA", "MICRO", POP + Vector((4, 9, 3)), 1800, (.6, .8, 1.0), 5, target=POP)

# ================================================================ LAKE: cutaway, ice sheet over a lake over bedrock (heights x5, labelled)
O = ORG["LAKE"]
VX = 5.0                     # vertical exaggeration (said on screen)
ICE_T = 80.0                 # drawn ice thickness at the start (800 m / 10 m per unit * ... see SCALE below)
# horizontal: 1 unit = 10 m; vertical: 1 unit = 10 m / VX.  Lake: ~12 m deep (Whillans is shallow, ~2 m; this is drawn deeper so it reads)
W_, D_ = 300.0, 120.0
def lake_floor(x):   # bed under the lake (a lens)
    return -12.0 * max(0.0, 1 - (x / 95.0) ** 2) ** 1.2
bed_v, bed_f = [], []
nx = 160
for i in range(nx + 1):
    x = -W_ / 2 + W_ * i / nx; z = lake_floor(x)
    for y in (-D_ / 2, D_ / 2): bed_v.append((x, y, z))
    bed_v.append((x, -D_ / 2, -60.0)); bed_v.append((x, D_ / 2, -60.0))
for i in range(nx):
    a = 4 * i; b2 = 4 * (i + 1)
    bed_f += [(a, a + 1, b2 + 1, b2), (a + 2, b2 + 2, b2, a), (a + 1, a + 3, b2 + 3, b2 + 1), (a + 2, a + 3, b2 + 3, b2 + 2)]
bed_f += [(0, 1, 3, 2), (4 * nx, 4 * nx + 1, 4 * nx + 3, 4 * nx + 2)]
bed = mesh_obj("Bedrock", [(v[0], v[1], v[2]) for v in bed_v], bed_f, "LAKE", False); bed.location = O
bed.data.materials.append(rock_mat("BedRock", (.05, .045, .04), False))

# water lens
wv_, wf_ = [], []
xs = [x for x in np.linspace(-95, 95, 120)]
for x in xs:
    for y in (-D_ / 2 + .2, D_ / 2 - .2): wv_ += [(x, y, lake_floor(x) + .05), (x, y, 0.0)]
for i in range(len(xs) - 1):
    a = 4 * i; b2 = 4 * (i + 1)
    wf_ += [(a, b2, b2 + 1, a + 1), (a + 2, a + 3, b2 + 3, b2 + 2), (a + 1, b2 + 1, b2 + 3, a + 3), (a, a + 2, b2 + 2, b2)]
water = mesh_obj("LakeWater", wv_, wf_, "LAKE", False); water.location = O
lw_m, nt = mat("LakeWater"); pos, gen = coords(nt)
cells = VORO(nt, pos, 2.2, "F1")
spark = M(nt, "MULTIPLY", M(nt, "LESS_THAN", cells.outputs["Distance"], .05), 3.0)
b = principled(nt, (.02, .06, .10), .05, .5, trans=.0); em = EMIT(nt, (.55, .95, .85), 1.0); L(nt, spark, em.inputs["Strength"])
ad = N(nt, "ShaderNodeAddShader"); L(nt, b.outputs[0], ad.inputs[0]); L(nt, em.outputs[0], ad.inputs[1]); finish(nt, ad.outputs[0]); water.data.materials.append(lw_m)
# ice sheet: a slab on top; its thickness is animated between the two lake shots (Whillans ~800 m, Mercer ~1,100 m)
ice = prim_box("IceSheet", (W_, D_, 1.0), "LAKE", loc=O + Vector((0, 0, .5)))
im_, nt = mat("IceSheetCut"); pos, gen = coords(nt)
gz = SEP(nt, gen)[2]
w = N(nt, "ShaderNodeTexWave"); w.wave_type = "BANDS"; w.bands_direction = "Z"; w.inputs["Scale"].default_value = 40.0; w.inputs["Distortion"].default_value = 2.0
L(nt, gen, w.inputs["Vector"])
rp = N(nt, "ShaderNodeValToRGB"); cr = rp.color_ramp; cr.elements.new(.5)
for e, (p_, c_) in zip(cr.elements, [(0.0, (.06, .17, .36)), (.45, (.30, .50, .74)), (1.0, (.82, .89, .96))]): e.position = p_; e.color = c_ + (1,)
L(nt, gz, rp.inputs[0])
col = MIXC(nt, M(nt, "MULTIPLY", w.outputs["Fac"], .3), rp.outputs[0], (.90, .94, 1.0))
b = principled(nt, col, .75, .12, BUMP(nt, NOISE(nt, pos, .3, 4, .5), .2, .3)); finish(nt, b.outputs[0]); ice.data.materials.append(im_)
icetop = grid("IceTop", W_, D_, 120, 50, lambda X, Y: fbm2(X, Y, 1 / 30.0, 3, 3.3) * .4, "LAKE", O); icetop.data.materials.append(SNOW)
farl = grid("LakeFar", 30000, 30000, 1, 1, lambda X, Y: X * 0 - 64.0, "LAKE", O); farl.data.materials.append(SNOW)
# the clean borehole + a small drill shelter on top (Whillans 2013 used hot-water drilling)
hole = prim_cyl("Borehole", .9, 1.0, "LAKE", 24, O + Vector((-20, -D_ / 2 + 6, .5)))
hm_, nt = mat("Hole"); b = principled(nt, (.02, .05, .09), .1, .5); finish(nt, b.outputs[0]); hole.data.materials.append(hm_)
hut = prim_box("DrillHut", (8, 6, 5), "LAKE", loc=O + Vector((-20, -D_ / 2 + 9, 0))); bevel(hut, .3)
hutm, nt = mat("HutRed"); b = principled(nt, (.55, .08, .05), .5, .4); finish(nt, b.outputs[0]); hut.data.materials.append(hutm)

# ================================================================ SHELF: ice-shelf front, ocean, icebergs, rocky shore
O = ORG["SHELF"]
ocean = grid("Ocean", 1, 1, 1, 1, lambda X, Y: X * 0, "SHELF", O)
oc = ocean.modifiers.new("ocean", "OCEAN"); oc.geometry_mode = "GENERATE"; oc.size = 1.0; oc.repeat_x = oc.repeat_y = 12; oc.spatial_size = 160
oc.resolution = 12; oc.wave_scale = 1.1; oc.choppiness = 1.2; oc.wind_velocity = 9.0; oc.depth = 200
ocean.location = O + Vector((-900, -400, 0))
om_, nt = mat("Sea"); pos, gen = coords(nt)
b = principled(nt, (.008, .03, .045), .04, .6, trans=0.0, ior=1.33); finish(nt, b.outputs[0]); ocean.data.materials.append(om_)
fars = grid("SeaFar", 80000, 80000, 1, 1, lambda X, Y: X * 0 - .3, "SHELF", O); fars.data.materials.append(om_)
# the shelf front: a 40 m cliff, cut by vertical runnels, ~1.6 km long, receding to +Y
sv, sf_ = [], []
nxs, nzs = 260, 30
for i in range(nxs + 1):
    x = -800 + 1600 * i / nxs
    yb = 600 + 40 * noise.noise(Vector((x * .004, 0, 2))) + 10 * noise.noise(Vector((x * .03, 0, 5)))
    for k in range(nzs + 1):
        z = -20 + 62 * k / nzs; z = min(z, 40 + 3 * noise.noise(Vector((x * .02, 1, 1))))
        run_ = 1.6 * noise.noise(Vector((x * .35, z * .01, 3))) + .6 * noise.noise(Vector((x * 1.4, z * .08, 7)))
        sv.append((x, yb + run_ - (z > 36) * (z - 36) * .6, z))
for i in range(nxs):
    for k in range(nzs):
        a = i * (nzs + 1) + k; sf_.append((a, a + nzs + 1, a + nzs + 2, a + 1))
front = mesh_obj("ShelfFront", sv, sf_, "SHELF"); front.location = O
top = grid("ShelfTop", 1600, 3000, 160, 60, lambda X, Y: 40 + fbm2(X, Y, 1 / 200.0, 3, 1.9) * 1.5, "SHELF", O + Vector((0, 2140, 0))); top.data.materials.append(SNOW)
cliff_m, nt = mat("ShelfIce"); pos, gen = coords(nt); z = SEP(nt, pos)[2]
str_ = NOISE(nt, VSCALE(nt, pos, 1.2, 1.2, .04), 1.0, 5, .6)
lay = N(nt, "ShaderNodeTexWave"); lay.wave_type = "BANDS"; lay.bands_direction = "Z"; lay.inputs["Scale"].default_value = 2.0; lay.inputs["Distortion"].default_value = 1.5; L(nt, VSCALE(nt, pos, .01, .01, .01), lay.inputs["Vector"])
low = SMOOTH(nt, z, 2.0, 14.0)
col = MIXC(nt, low, (.30, .55, .72), (.80, .88, .96))
col = MIXC(nt, M(nt, "MULTIPLY", lay.outputs["Fac"], .25), col, (.95, .97, 1.0))
b = principled(nt, col, .35, .5, BUMP(nt, M(nt, "ADD", str_, M(nt, "MULTIPLY", NOISE(nt, pos, .6, 4, .6), .4)), .5, 1.0), sss=.5, sss_r=(.35, .65, 1.0))
finish(nt, b.outputs[0]); front.data.materials.append(cliff_m)
bergs = []
for i, (x, y, r, sq, tab) in enumerate([(-260, 260, 34, (1.6, 1.0, .45), True), (180, 330, 22, (1.0, 1.2, .9), False), (520, 180, 46, (2.2, 1.4, .38), True),
                                         (-620, 120, 16, (1.0, 1.0, .9), False), (60, 120, 9, (1.2, 1.0, .8), False), (-120, 60, 5, (1, 1.3, .7), False),
                                         (380, 40, 6, (1.4, 1, .6), False), (900, 400, 60, (2.4, 1.3, .3), True), (-1100, 500, 45, (2.0, 1.4, .35), True)]):
    bb = blob("Berg%d" % i, r, i * 4.7 + 1, "SHELF", 5, .18 if tab else .32, 1.2, sq)
    if tab:
        for v in bb.data.vertices:
            if v.co.z > r * sq[2] * .55: v.co.z = r * sq[2] * .55 + .02 * r * noise.noise(v.co * .2)
    bb.location = O + Vector((x, y, r * sq[2] * .05 - 1.0)); bb.rotation_euler = (0, 0, i * .9); bb.data.materials.append(cliff_m); bergs.append(bb)
# a rocky shore with snow patches (no animals drawn: the bird-flu line is about real birds, which we do not recreate)
shore = []
for i in range(14):
    s = blob("Shore%d" % i, random.uniform(3, 14), i * 2.9, "SHELF", 4, .35, 1.3, (1.4, 1.0, .55), flat_bottom=-.6)
    s.location = O + Vector((-420 + random.uniform(-40, 40), -120 + i * 9 + random.uniform(-6, 6), -1.0)); s.rotation_euler = (0, 0, random.random() * 6)
    s.data.materials.append(ROCK); shore.append(s)
for i in range(60):
    s = blob("Peb%d" % i, random.uniform(.2, 1.2), i * 1.1 + 40, "SHELF", 3, .3, 1.3, (1, 1, .6), flat_bottom=-.3)
    s.location = O + Vector((-405 + random.uniform(-30, 30), -130 + random.uniform(0, 120), random.uniform(-.2, 1.5))); s.data.materials.append(ROCK)

# ================================================================ STATION: a generic research station at night (not any real station)
O = ORG["STATION"]
st_g = grid("StationSnow", 3000, 3000, 200, 200, lambda X, Y: fbm2(X, Y, 1 / 300.0, 3, 6.6) * 3.0, "STATION", O); st_g.data.materials.append(SNOW)
farst = grid("StationFar", 60000, 60000, 1, 1, lambda X, Y: X * 0 - 4.0, "STATION", O); farst.data.materials.append(SNOW)
hull_m, nt = mat("Hull"); pos, gen = coords(nt)
b = principled(nt, MIXC(nt, NOISE(nt, pos, .5, 3, .5), (.62, .64, .66), (.70, .71, .72)), .45, .5, BUMP(nt, M(nt, "SINE", M(nt, "MULTIPLY", SEP(nt, pos)[0], 3.0)), .05, .05))
finish(nt, b.outputs[0])
win_m, nt = mat("Window"); pos, gen = coords(nt); e = EMIT(nt, (1.0, .72, .42), 9.0); finish(nt, e.outputs[0])
leg_m, nt = mat("Leg"); b = principled(nt, (.25, .25, .27), .5, .5, metallic=.8); finish(nt, b.outputs[0])
mods = []
for i, (x, y, l, rz) in enumerate([(0, 0, 36, 0), (40, 6, 28, .05), (-38, 10, 24, -.04), (8, 34, 30, 1.57)]):
    gz = 0.0
    md_ = prim_box("Module%d" % i, (l, 10, 5), "STATION", loc=O + Vector((x, y, 4.2 + 2.5)), rot=(0, 0, rz)); bevel(md_, .6, 3); md_.data.materials.append(hull_m)
    for k in range(int(l // 3.2) - 1):   # a row of lit windows on each long side
        for sgn in (-1, 1):
            if random.random() < .25: continue
            wx = -l / 2 + 2.4 + k * 3.2
            wpos = Matrix.Rotation(rz, 4, "Z") @ Vector((wx, sgn * 5.03, 0))
            wo = prim_box("Win%d_%d_%d" % (i, k, sgn), (1.4, .05, 1.0), "STATION", loc=O + Vector((x, y, 6.9)) + wpos.to_3d(), rot=(0, 0, rz)); wo.data.materials.append(win_m)
    for lx in (-l / 2 + 2, l / 2 - 2):
        for sgn in (-1, 1):
            lp = Matrix.Rotation(rz, 4, "Z") @ Vector((lx, sgn * 3.5, 0))
            lg = prim_cyl("Leg%d" % len(mods), .35, 4.6, "STATION", 12, O + Vector((x, y, 2.1)) + lp.to_3d()); lg.data.materials.append(leg_m); mods.append(lg)
for i, (x, y) in enumerate([(-70, -40), (60, -50), (-20, -70), (100, 30)]):   # light poles
    pole = prim_cyl("Pole%d" % i, .12, 9, "STATION", 8, O + Vector((x, y, 4.5))); pole.data.materials.append(leg_m)
    add_light("PoleL%d" % i, "POINT", "STATION", O + Vector((x, y, 9.2)), 6000, (1.0, .78, .5), .4)
# aurora australis: a few emissive curtains (soft, high in the sky)
au_m, nt = mat("Aurora"); au_m.surface_render_method = "BLENDED"; pos, gen = coords(nt); g_ = SEP(nt, gen)
fold = NOISE(nt, VSCALE(nt, gen, 6.0, 1.0, .2), 2.0, 4, .6)
vert = M(nt, "MULTIPLY", SMOOTH(nt, g_[2], 0.0, .25), M(nt, "SUBTRACT", 1.0, SMOOTH(nt, g_[2], .35, 1.0)))
rays = SMOOTH(nt, NOISE(nt, VSCALE(nt, gen, 60.0, 1.0, .5), 1.0, 2, .5), .4, .8)
strength = M(nt, "MULTIPLY", M(nt, "MULTIPLY", vert, M(nt, "ADD", .35, M(nt, "MULTIPLY", rays, .9))), M(nt, "MULTIPLY", SMOOTH(nt, fold, .35, .65), .8))
col = MIXC(nt, g_[2], (.15, 1.0, .45), (.55, .35, .9))
em = N(nt, "ShaderNodeEmission"); L(nt, col, em.inputs["Color"]); L(nt, strength, em.inputs["Strength"])
tr = N(nt, "ShaderNodeBsdfTransparent"); ad = N(nt, "ShaderNodeAddShader"); L(nt, tr.outputs[0], ad.inputs[0]); L(nt, em.outputs[0], ad.inputs[1]); finish(nt, ad.outputs[0])
for i, (y, x0, ang) in enumerate([(9000, -4000, .25), (12000, 1500, -.15), (15000, -1000, .05)]):
    vs, fs = [], []
    for k in range(80):
        u = k / 79; x = x0 + (u - .5) * 16000; yy = y + 2500 * math.sin(u * 4 + i)
        vs += [(x, yy, 1800), (x, yy, 6500)]
    for k in range(79): fs.append((2 * k, 2 * k + 2, 2 * k + 3, 2 * k + 1))
    cur = mesh_obj("Aurora%d" % i, vs, fs, "STATION", False); cur.location = O; cur.data.materials.append(au_m)
    cur.visible_shadow = False; cur.visible_diffuse = False; cur.visible_glossy = False

# ================================================================ world: day sky + night stars + dark, strengths keyed per shot
w = bpy.data.worlds.new("World"); sc.world = w; w.use_nodes = True; wn = w.node_tree; wn.nodes.clear()
sky = wn.nodes.new("ShaderNodeTexSky"); sky.sky_type = "MULTIPLE_SCATTERING"
try: sky.sun_elevation = math.radians(SUN_EL); sky.sun_rotation = math.radians(SUN_AZ); sky.altitude = 2000.0; sky.sun_disc = False
except Exception as e: print("sky props", e)
tc = wn.nodes.new("ShaderNodeTexCoord"); vo = wn.nodes.new("ShaderNodeTexVoronoi"); vo.feature = "F1"; vo.inputs["Scale"].default_value = 260.0
wn.links.new(tc.outputs["Generated"], vo.inputs["Vector"])
def wmath(op, a, b=None):
    n = wn.nodes.new("ShaderNodeMath"); n.operation = op
    for i, x in enumerate((a, b)):
        if x is None: continue
        if lk(x): wn.links.new(x, n.inputs[i])
        else: n.inputs[i].default_value = x
    return n.outputs[0]
nz = wn.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 140.0; wn.links.new(tc.outputs["Generated"], nz.inputs["Vector"])
star = wmath("MULTIPLY", wmath("LESS_THAN", vo.outputs["Distance"], .02), wmath("MULTIPLY", wmath("POWER", nz.outputs["Fac"], 5.0), 30.0))
sep = wn.nodes.new("ShaderNodeSeparateXYZ"); wn.links.new(tc.outputs["Generated"], sep.inputs[0])
# generated z on the world: use the view direction's z instead (stars above the horizon only)
gz = wn.nodes.new("ShaderNodeNewGeometry") if False else None
vday = wn.nodes.new("ShaderNodeValue"); vday.name = "day"; vnight = wn.nodes.new("ShaderNodeValue"); vnight.name = "night"
vdark = wn.nodes.new("ShaderNodeValue"); vdark.name = "dark"
bg_day = wn.nodes.new("ShaderNodeBackground"); wn.links.new(sky.outputs[0], bg_day.inputs["Color"]); wn.links.new(wmath("MULTIPLY", vday.outputs[0], .4), bg_day.inputs["Strength"])
bg_n = wn.nodes.new("ShaderNodeBackground"); bg_n.inputs["Color"].default_value = (.75, .82, 1.0, 1)
wn.links.new(wmath("MULTIPLY", vnight.outputs[0], wmath("ADD", star, .0035)), bg_n.inputs["Strength"])
bg_k = wn.nodes.new("ShaderNodeBackground"); bg_k.inputs["Color"].default_value = (.008, .014, .024, 1); wn.links.new(vdark.outputs[0], bg_k.inputs["Strength"])
a1 = wn.nodes.new("ShaderNodeAddShader"); a2 = wn.nodes.new("ShaderNodeAddShader")
wn.links.new(bg_day.outputs[0], a1.inputs[0]); wn.links.new(bg_n.outputs[0], a1.inputs[1]); wn.links.new(a1.outputs[0], a2.inputs[0]); wn.links.new(bg_k.outputs[0], a2.inputs[1])
wo_ = wn.nodes.new("ShaderNodeOutputWorld"); wn.links.new(a2.outputs[0], wo_.inputs["Surface"])
sun_d = bpy.data.lights.new("Sun", "SUN"); sun_d.angle = math.radians(.53); sun_d.color = (1.0, .96, .91)
sun = bpy.data.objects.new("Sun", sun_d); sc.collection.objects.link(sun); sun.rotation_euler = SUNV.to_track_quat("Z", "Y").to_euler()
moon_d = bpy.data.lights.new("Moon", "SUN"); moon_d.angle = math.radians(1.0); moon_d.color = (.62, .72, 1.0)
moon = bpy.data.objects.new("Moon", moon_d); sc.collection.objects.link(moon); moon.rotation_euler = sun_vec(22, 140).to_track_quat("Z", "Y").to_euler()
SET_EXP = {"FIELD": -.2, "CHUNK": -.2, "SHELF": -.2, "LAKE": -.7, "CORES": -.8}
SET_WORLD = {"FIELD": (1, 0, 0, 3.6, 0), "CHUNK": (1, 0, 0, 3.6, 0), "SHELF": (1, 0, 0, 3.6, 0), "LAKE": (1, 0, 0, 1.1, 0),
             "CORES": (0, 0, .05, 0, 0), "SEA": (0, 0, .15, 0, 0), "DIATOM": (0, 0, .25, 0, 0), "MICRO": (0, 0, .2, 0, 0),
             "STATION": (0, 1, 0, 0, .06)}

# ---------------------------------------------------------------- camera
cd = bpy.data.cameras.new("Cam"); cam = bpy.data.objects.new("Cam", cd); sc.collection.objects.link(cam); sc.camera = cam
cd.clip_start = .01; cd.clip_end = 120000.0; cd.sensor_width = 36.0; cd.dof.use_dof = True; cd.dof.aperture_fstop = 22.0
cam.rotation_mode = "QUATERNION"
def lookat(p, t, up=Vector((0, 0, 1))):
    f = (Vector(t) - Vector(p)).normalized(); r = f.cross(Vector(up)).normalized(); u = r.cross(f)
    return Matrix((r, u, -f)).transposed().to_quaternion()

def cam_keys(name):
    """list of (fraction, pos, target, lens, fstop, focus_dist or None) in world space"""
    if name == "FIELD_A":    # low pass over the blue ice toward the hills, sun low ahead-left
        o = ORG["FIELD"]
        p0 = o + Vector((-6, -40, fh(-6, -40) + 2.2)); p1 = o + Vector((4, 10, fh(4, 10) + 2.8))
        return [(0, p0, o + Vector((60, 1800, 40)), 24, 16, None), (1, p1, o + Vector((80, 1800, 50)), 24, 16, None)]
    if name == "CHUNK_A":    # push in on the bubbly block
        o = ORG["CHUNK"]; c = chunk.location
        return [(0, c + Vector((-1.1, -1.6, .55)), c + Vector((0, 0, .05)), 50, 5.6, 2.0), (1, c + Vector((-.35, -.62, .2)), c + Vector((.02, 0, .04)), 50, 4.0, .72)]
    if name == "CORES_A":    # slow dolly along the cores
        o = ORG["CORES"]
        return [(0, o + Vector((-.9, -.75, 1.25)), o + Vector((-.4, 0, .95)), 45, 2.8, 1.0), (1, o + Vector((.35, -.7, 1.18)), o + Vector((.25, 0, .95)), 45, 2.8, .82)]
    if name == "SEA_A":
        o = ORG["SEA"]
        return [(0, o + Vector((-3.4, -.6, .8)), o + Vector((0, 4, .9)), 30, 8.0, 5.8), (1, o + Vector((-2.6, .2, 1.0)), o + Vector((0, 4, 1.7)), 30, 8.0, 4.9)]
    if name == "DIATOM_A":
        o = ORG["DIATOM"]
        return [(0, o + Vector((-2.5, -9, 1.5)), o + Vector((0, 4, 0)), 40, 4.0, 12.0), (1, o + Vector((-.5, -4.5, .8)), o + Vector((.5, 4, 0)), 40, 4.0, 8.0)]
    if name == "MICRO_A":    # DNA fragments on clay grains, slow orbit
        o = ORG["MICRO"]
        return [(0, o + Vector((-5.5, -6.5, 4.0)), o, 40, 5.6, 9.0), (1, o + Vector((-1.5, -8.0, 3.0)), o + Vector((.2, 0, 0)), 40, 5.6, 8.4)]
    if name == "MICRO_B":    # the taker cell and the loose fragment
        o = ORG["MICRO"]; c = taker.location
        return [(0, c + Vector((-3.0, -4.5, 1.6)), c + Vector((-.9, .9, -.1)), 45, 4.0, 5.4), (1, c + Vector((-1.6, -3.6, 1.2)), c + Vector((-.2, .3, 0)), 45, 4.0, 4.0)]
    if name == "MICRO_C":    # the population
        return [(0, POP + Vector((-4, -15, 6)), POP, 32, 8, 16.0), (1, POP + Vector((2, -13, 4.5)), POP + Vector((.5, 0, 0)), 32, 8, 14.0)]
    if name == "LAKE_A":     # cutaway, Whillans (800 m of ice drawn)
        o = ORG["LAKE"]
        return [(0, o + Vector((-170, -260, 70)), o + Vector((-10, 0, 20)), 30, 22, None), (1, o + Vector((-110, -230, 52)), o + Vector((-5, 0, 18)), 30, 22, None)]
    if name == "LAKE_B":     # deeper: Mercer, more than 1 km of ice
        o = ORG["LAKE"]
        return [(0, o + Vector((150, -250, 30)), o + Vector((0, 0, 10)), 32, 22, None), (1, o + Vector((70, -170, 8)), o + Vector((-10, 0, 2)), 32, 22, None)]
    if name == "SHELF_A":    # along the shelf front at sea level
        o = ORG["SHELF"]
        return [(0, o + Vector((-500, 380, 9)), o + Vector((0, 640, 25)), 28, 22, None), (1, o + Vector((-380, 410, 8)), o + Vector((120, 650, 24)), 28, 22, None)]
    if name == "SHELF_B":    # rocky shore, bergs beyond
        o = ORG["SHELF"]
        return [(0, o + Vector((-390, -150, 4.0)), o + Vector((-250, 260, 6)), 30, 22, None), (1, o + Vector((-396, -138, 3.4)), o + Vector((-220, 260, 6)), 30, 22, None)]
    if name == "SHELF_C":    # wide seascape of icebergs
        o = ORG["SHELF"]
        return [(0, o + Vector((-200, -420, 14)), o + Vector((200, 300, 10)), 35, 22, None), (1, o + Vector((-140, -400, 13)), o + Vector((260, 300, 10)), 35, 22, None)]
    if name == "STATION_A":
        o = ORG["STATION"]
        return [(0, o + Vector((-40, -48, 2.2)), o + Vector((5, 12, 13)), 24, 22, None), (1, o + Vector((-30, -38, 2.0)), o + Vector((5, 12, 14)), 24, 22, None)]
    if name == "FIELD_Z":    # end: rise from the ice and tilt up to the sky
        o = ORG["FIELD"]
        return [(0, o + Vector((0, -20, fh(0, -20) + 2.5)), o + Vector((60, 1800, 40)), 22, 16, None),
                (.55, o + Vector((0, -220, 160)), o + Vector((80, 1800, 120)), 22, 16, None),
                (1, o + Vector((0, -260, 340)), o + Vector((100, 1600, 1500)), 22, 16, None)]
    raise KeyError(name)

# ---------------------------------------------------------------- keyframes
def key_vis(o, frame, hidden):
    o.hide_render = hidden; o.keyframe_insert("hide_render", frame=frame)
def key_val(node, frame, v):
    node.outputs[0].default_value = v; node.outputs[0].keyframe_insert("default_value", frame=frame)
allsets = list(SETS.keys())
f = 1; cut = set()
for sh in SHOTS:
    n = int(round(sh["dur"] * FPS)); fa, fb = f, f + n - 1
    if sh["cam"] is None: f = fb + 1; continue
    cut.add(fb)
    setname = sh["cam"].split("_")[0]
    for s_ in allsets:
        for o in SETS[s_]:
            if o.name in ("BubbleSrc",): continue
            key_vis(o, fa, s_ != setname)
    dy, ni, dk, se, me_ = SET_WORLD[setname]
    key_val(vday, fa, dy); key_val(vnight, fa, ni); key_val(vdark, fa, dk)
    sc.view_settings.exposure = SET_EXP.get(setname, 0.0); sc.view_settings.keyframe_insert("exposure", frame=fa)
    sun_d.energy = se; sun_d.keyframe_insert("energy", frame=fa); moon_d.energy = me_; moon_d.keyframe_insert("energy", frame=fa)
    for u, p, t, lens, fs_, fd in cam_keys(sh["cam"]):
        ff = int(round(fa + (fb - fa) * u))
        cam.location = p; cam.rotation_quaternion = lookat(p, t)
        cam.keyframe_insert("location", frame=ff); cam.keyframe_insert("rotation_quaternion", frame=ff)
        cd.lens = lens; cd.keyframe_insert("lens", frame=ff)
        cd.dof.aperture_fstop = fs_; cd.dof.keyframe_insert("aperture_fstop", frame=ff)
        cd.dof.focus_distance = fd if fd else 1000.0; cd.dof.keyframe_insert("focus_distance", frame=ff)
    # per-shot animation
    if sh["cam"] == "SEA_A":     # the drill string lifts the core out of the mud
        pipe.location = ORG["SEA"] + Vector((0, 4, 15.0)); pipe.keyframe_insert("location", frame=fa)
        pipe.location = ORG["SEA"] + Vector((0, 4, 15.0 + 3.0)); pipe.keyframe_insert("location", frame=fb)
        for o in snow_objs[::3]:
            l0 = o.location.copy(); o.keyframe_insert("location", frame=fa); o.location = l0 + Vector((.3, 0, -.35)); o.keyframe_insert("location", frame=fb)
    if sh["cam"] == "DIATOM_A":
        for i, d in enumerate(diatoms):
            r0 = d.rotation_euler.copy(); l0 = d.location.copy()
            d.keyframe_insert("rotation_euler", frame=fa); d.keyframe_insert("location", frame=fa)
            d.rotation_euler = (r0.x + .4 * math.sin(i), r0.y + .3, r0.z + .5 * math.cos(i)); d.location = l0 + Vector((.3 * math.sin(i * 2), .2, -.25))
            d.keyframe_insert("rotation_euler", frame=fb); d.keyframe_insert("location", frame=fb)
    if sh["cam"] == "MICRO_B":   # the loose fragment drifts to the cell and is drawn in; a soft glow marks it inside
        c = taker.location
        pts_ = [(0.0, loose.location.copy(), 1.0), (.45, c + Vector((-.95, -.1, .15)), 1.0), (.62, c + Vector((-.55, 0, .05)), .9), (.85, c + Vector((-.15, .02, 0)), .75), (1.0, c + Vector((.1, .02, 0)), .7)]
        for u, p, s in pts_:
            ff = int(round(fa + (fb - fa) * u)); loose.location = p; loose.scale = (s, s, s)
            loose.keyframe_insert("location", frame=ff); loose.keyframe_insert("scale", frame=ff)
        r0 = loose.rotation_euler.copy(); loose.keyframe_insert("rotation_euler", frame=fa)
        loose.rotation_euler = (r0.x + .6, r0.y, r0.z + 1.6); loose.keyframe_insert("rotation_euler", frame=fb)
        taker.rotation_euler = (0, .15, .4); taker.keyframe_insert("rotation_euler", frame=fa); taker.rotation_euler = (0, .1, .55); taker.keyframe_insert("rotation_euler", frame=fb)
    if sh["cam"] == "MICRO_C":   # cells divide; three "lucky" warm-coloured lines divide fastest (selection, schematic)
        for i, (o, win) in enumerate(base_cells):
            divs = 3 if win else (1 if i % 3 else 0)
            parent = o
            for k in range(divs):
                t0 = .12 + (k / max(1, divs)) * .7 + .05 * (i % 4); t1 = t0 + .14
                fa_, fb_ = int(fa + (fb - fa) * t0), int(fa + (fb - fa) * min(1, t1))
                ch = bpy.data.objects.new("%s_d%d" % (o.name, k), o.data); link(ch, "MICRO")
                ang = parent.rotation_euler.z + (k * 1.1); dirv = Vector((math.cos(ang), math.sin(ang), .2 * math.sin(i + k))).normalized()
                ch.rotation_euler = parent.rotation_euler; ch.location = parent.location
                key_vis(ch, 1, True); key_vis(ch, fa_, False); key_vis(ch, fb + 1, True)
                ch.scale = (.6, .9, .9); ch.keyframe_insert("scale", frame=fa_); ch.keyframe_insert("location", frame=fa_)
                ch.location = parent.location + dirv * 1.5 * (1 + .4 * k); ch.scale = (1, 1, 1)
                ch.keyframe_insert("location", frame=fb_); ch.keyframe_insert("scale", frame=fb_)
                ch.rotation_euler = (parent.rotation_euler.x, parent.rotation_euler.y, ang + .3); ch.keyframe_insert("rotation_euler", frame=fb_)
                parent = ch
    if sh["cam"] in ("LAKE_A", "LAKE_B"):
        th = 80.0 if sh["cam"] == "LAKE_A" else 110.0      # 1 unit = 10 m (drawn x1 vertically at 800 m -> 80, Mercer ~1,100 m -> 110)
        ice.scale = (1, 1, th); ice.location = ORG["LAKE"] + Vector((0, 0, th / 2)); icetop.location = ORG["LAKE"] + Vector((0, 0, th))
        hole.scale = (1, 1, th if sh["cam"] == "LAKE_A" else .001); hole.location = ORG["LAKE"] + Vector((-20, -D_ / 2 + 6, th / 2))
        hut.location = ORG["LAKE"] + Vector((-20, -D_ / 2 + 9, th + 2.5))
        for o_ in (ice, icetop, hole, hut):
            o_.keyframe_insert("location", frame=fa); o_.keyframe_insert("scale", frame=fa)
        key_vis(hole, fa, sh["cam"] != "LAKE_A"); key_vis(hut, fa, sh["cam"] != "LAKE_A")
    if sh["cam"].startswith("SHELF"):
        oc.time = fa / FPS; oc.keyframe_insert("time", frame=fa); oc.time = fb / FPS; oc.keyframe_insert("time", frame=fb)
    f = fb + 1
# the Micro population children are linked after the visibility pass: hide them everywhere but their own shot (done above)
def all_curves(idb):
    ad = idb.animation_data
    if not ad or not ad.action: return []
    cs = getattr(ad.action, "fcurves", None)
    if cs is not None: return list(cs)
    try: return [fc for layer in ad.action.layers for strip in layer.strips for bag in strip.channelbags for fc in bag.fcurves]
    except Exception: return []
SMOOTH_ANIM = {pipe.name, loose.name, taker.name, ocean.name} | {d.name for d in diatoms} | {o.name for o in snow_objs} | {o.name for o in bpy.data.objects if o.name.startswith("Pop")}
for idb in list(bpy.data.objects) + list(bpy.data.materials) + list(bpy.data.lights) + [w.node_tree, sc]:
    for fc in all_curves(idb):
        for k in fc.keyframe_points: k.interpolation = "LINEAR" if getattr(idb, "name", "") in SMOOTH_ANIM else "CONSTANT"
for o in bpy.data.objects:
    for m_ in o.modifiers:
        pass
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
