# Heartbeat TV Science 8.6 "Phobos: the moon that's falling".  Pure-script Blender 5.1 scene (no downloaded assets).
# Scene unit = 1 km.  Phobos (a displaced icosphere: ellipsoid 26 x 22.6 x 18.4 km, ~200 craters incl. Stickney ~9 km,
# three families of parallel grooves ~0.2 km wide / tens of metres deep, boulders near the surface cameras) sits at the
# origin, long axis toward Mars; Mars (R 3389.5 km, procedural ochre/dark regions/polar caps + thin atmosphere rim) is 9,376 km
# away on +Y; Deimos (15 x 12 x 11 km) sits at its own distance 23,460 km from Mars.  The spiral-in / ring shots use an
# enlarged Phobos marker (x25, labelled on screen), an orbit line, and a rubble point cloud instanced with geometry nodes.
# Cycles OptiX on the RTX 4060 (one GPU job at a time).
#   blender -b -P build.py -- [--still FRAME out.png] [--stills DIR --frames a,b,c] [--anim OUTDIR [--start F --end F --step 2]]
#                             [--samples N] [--cpu] [--save out.blend] [--w 1280 --h 720]
import bpy, bmesh, math, random, sys, os, time
import numpy as np
from mathutils import Vector, Matrix, noise

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from shots import SHOTS, FPS
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def arg(k, d=None): return argv[argv.index(k) + 1] if k in argv else d
random.seed(11); np.random.seed(11)

DUR = sum(int(round(s["dur"] * FPS)) for s in SHOTS)
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.fps = FPS; sc.frame_start, sc.frame_end = 1, DUR
sc.unit_settings.scale_length = 1000.0

# ---------------------------------------------------------------- render
sc.render.engine = "CYCLES"
prefs = bpy.context.preferences.addons["cycles"].preferences
prefs.compute_device_type = "OPTIX"; prefs.get_devices()
for d in prefs.devices: d.use = d.type == "OPTIX"
sc.cycles.device = "CPU" if "--cpu" in argv else "GPU"
sc.cycles.samples = int(arg("--samples", "48")); sc.cycles.use_adaptive_sampling = True; sc.cycles.adaptive_threshold = 0.05
sc.cycles.use_denoising = True; sc.cycles.denoiser = "OPENIMAGEDENOISE" if "--cpu" in argv else "OPTIX"
sc.cycles.max_bounces = 3; sc.cycles.diffuse_bounces = 2; sc.cycles.glossy_bounces = 2; sc.cycles.transmission_bounces = 2; sc.cycles.volume_bounces = 0
sc.cycles.transparent_max_bounces = 12
sc.cycles.caustics_reflective = False; sc.cycles.caustics_refractive = False
sc.cycles.blur_glossy = 1.0; sc.cycles.sample_clamp_indirect = 4.0
sc.render.resolution_x, sc.render.resolution_y = int(arg("--w", "1280")), int(arg("--h", "720")); sc.render.resolution_percentage = 100
sc.render.use_motion_blur = False
sc.view_settings.view_transform = arg("--view", "Standard")
try: sc.view_settings.look = "AgX - Medium High Contrast" if sc.view_settings.view_transform == "AgX" else "None"
except Exception: pass
sc.view_settings.exposure = float(arg("--exp", "0.0"))
sc.render.image_settings.file_format = "PNG"; sc.render.image_settings.color_mode = "RGB"
sc.render.film_transparent = False

# ---------------------------------------------------------------- node helpers (same family as 8.4 / 8.5)
def mat(name):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial"); out.name = "OUT"
    return m, nt
def N(nt, t, **kw):
    n = nt.nodes.new(t)
    for k, v in kw.items():
        if k == "inputs":
            for ik, iv in v.items(): n.inputs[ik].default_value = iv
        else: setattr(n, k, v)
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
        else: sock.default_value = x if len(x) == 4 else tuple(x) + (1,)
    return n.outputs[2]
def NOISE(nt, vec, scale, detail=3, rough=.5):
    n = N(nt, "ShaderNodeTexNoise"); n.inputs["Scale"].default_value = scale; n.inputs["Detail"].default_value = detail; n.inputs["Roughness"].default_value = rough
    L(nt, vec, n.inputs["Vector"]); return n.outputs["Fac"]
def VORO(nt, vec, scale, feat="DISTANCE_TO_EDGE", rnd=1.0):
    n = N(nt, "ShaderNodeTexVoronoi"); n.feature = feat; n.inputs["Scale"].default_value = scale; n.inputs["Randomness"].default_value = rnd
    L(nt, vec, n.inputs["Vector"]); return n
def RAMP(nt, fac, stops):
    n = N(nt, "ShaderNodeValToRGB"); cr = n.color_ramp
    while len(cr.elements) < len(stops): cr.elements.new(0.5)
    for e, (p, c) in zip(cr.elements, stops): e.position = p; e.color = tuple(c) + (1,) if len(c) == 3 else c
    L(nt, fac, n.inputs[0]); return n.outputs[0]
def SMOOTH(nt, x, a, b):
    n = N(nt, "ShaderNodeMapRange"); n.interpolation_type = "SMOOTHSTEP"
    for sock, v in ((n.inputs["From Min"], a), (n.inputs["From Max"], b)):
        if lk(v): L(nt, v, sock)
        else: sock.default_value = v
    L(nt, x, n.inputs["Value"]); return n.outputs[0]
def finish(nt, shader): L(nt, shader, nt.nodes["OUT"].inputs["Surface"])
def principled(nt, color, rough, spec=.5, normal=None, metallic=0.0):
    b = N(nt, "ShaderNodeBsdfPrincipled"); b.inputs["Roughness"].default_value = rough if not lk(rough) else .5
    if lk(rough): L(nt, rough, b.inputs["Roughness"])
    if lk(color): L(nt, color, b.inputs["Base Color"])
    else: b.inputs["Base Color"].default_value = tuple(color) + (1,)
    b.inputs["Specular IOR Level"].default_value = spec; b.inputs["Metallic"].default_value = metallic
    if normal is not None: L(nt, normal, b.inputs["Normal"])
    return b
def BUMP(nt, height, strength, dist=1.0, normal=None):
    b = N(nt, "ShaderNodeBump"); b.inputs["Strength"].default_value = strength; b.inputs["Distance"].default_value = dist
    L(nt, height, b.inputs["Height"])
    if normal is not None: L(nt, normal, b.inputs["Normal"])
    return b.outputs[0]
def objcoord(nt):
    tc = N(nt, "ShaderNodeTexCoord"); return tc.outputs["Object"], tc.outputs["Generated"]
def ATTR(nt, name):
    a = N(nt, "ShaderNodeAttribute"); a.attribute_name = name; return a.outputs["Fac"]

def link(o):
    sc.collection.objects.link(o); return o

# ---------------------------------------------------------------- layout
MC = Vector((0.0, 9376.0, 0.0))          # Mars centre (Phobos semi-major axis 9,376 km)
RM = 3389.5                              # Mars mean radius
PH = (11.3, 13.0, 9.2)                   # Phobos semi-axes (x along orbit, y toward Mars, z pole)
DM = (7.5, 6.1, 5.5)                     # Deimos semi-axes
DEIMOS_POS = MC + Vector((-8000.0, -22050.0, 0.0))   # 23,460 km from Mars centre
SUN_DIR = Vector((-0.55, -0.38, 0.74)).normalized()  # direction toward the Sun (Phobos lit from the camera side, Mars gibbous)
C2_SITE = (-0.93, 0.21, 0.30)                        # the sample-shot site: ~78 deg from the sub-Mars point (Mars low, on the horizon)

# ---------------------------------------------------------------- the small bodies: displaced icospheres
def fbm(v, oct=5, lac=2.0, gain=0.5, base=1.0):
    a, f, s = 1.0, base, 0.0
    for _ in range(oct):
        s += a * noise.noise(v * f); a *= gain; f *= lac
    return s

def body_mesh(name, semi, craters, grooves, subdiv, lump_amp, lump_scale, seed, fine=0.0):
    bm = bmesh.new(); bmesh.ops.create_icosphere(bm, subdivisions=subdiv, radius=1.0)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    n = len(me.vertices); d = np.empty(n * 3); me.vertices.foreach_get("co", d); d = d.reshape(n, 3)
    d /= np.linalg.norm(d, axis=1)[:, None]
    a, b, c = semi
    r0 = 1.0 / np.sqrt((d[:, 0] / a) ** 2 + (d[:, 1] / b) ** 2 + (d[:, 2] / c) ** 2)
    rmean = (a + b + c) / 3.0
    off = Vector((seed * 7.1, seed * 3.3, seed * 1.7))
    lump = np.array([fbm(Vector(x) * lump_scale + off, 4) for x in d]) * lump_amp
    if fine > 0:
        lump += np.array([fbm(Vector(x) * lump_scale * 9 + off * 2, 3) for x in d]) * fine
    h = np.zeros(n); stk = np.zeros(n); grv = np.zeros(n)
    for (cd, R, dep, big) in craters:
        cosang = np.clip(d @ np.array(cd), -1, 1); s = np.arccos(cosang) * rmean
        m = s < R * 1.7
        x = s[m] / R
        bowl = np.where(x < 1, -dep * (1 - x * x) ** 1.1, 0.0)
        rim = dep * (.22 if big else .3) * np.exp(-((x - 1.0) / (.16 if big else .2)) ** 2)
        ej = -dep * .04 * np.exp(-((x - 1.35) / .3) ** 2)
        h[m] += bowl + rim + ej
        if big: stk[m] = np.maximum(stk[m], np.clip(1.15 - x, 0, 1))
    p = d * (r0 + lump + h)[:, None]
    for (nrm, sp, w, dep, center, spread, gseed) in grooves:
        nrm = np.array(nrm) / np.linalg.norm(nrm); cen = np.array(center) / np.linalg.norm(center)
        t = (p @ nrm) % sp; dist = np.abs(t - sp / 2)
        prof = np.clip(1 - (dist / (w / 2)) ** 2, 0, 1)
        mask = np.exp(-(np.arccos(np.clip(d @ cen, -1, 1)) / spread) ** 2)
        # broken into segments / pit chains along their length
        u1 = np.cross(nrm, [0.3, 0.5, 0.8]); u1 /= np.linalg.norm(u1)
        along = p @ u1; lane = np.floor((p @ nrm) / sp)
        segv = np.array([noise.noise(Vector((al * .35, ln * 3.1 + gseed, gseed * .7))) for al, ln in zip(along, lane)])
        seg = np.clip((segv + .22) * 2.2, 0, 1)
        pits = .75 + .25 * np.cos(along * 2 * math.pi / .5)
        g = prof * mask * seg * pits
        h -= dep * g; grv = np.maximum(grv, g)
    r = r0 + lump + h
    v = d * r[:, None]
    print(name, "grv>0.3:", int((grv > .3).sum()), "stk>0.3:", int((stk > .3).sum()), flush=True)
    me.vertices.foreach_set("co", v.ravel())
    me.polygons.foreach_set("use_smooth", [True] * len(me.polygons))
    for nm, arr in (("stk", stk), ("grv", grv)):
        at = me.attributes.new(nm, "FLOAT", "POINT"); at.data.foreach_set("value", arr)
    me.update()
    # true mesh normals of the displaced surface (lumps, crater walls, slopes), accumulated from the triangles
    nf = len(me.polygons); pv = np.empty(nf * 3, dtype=np.int32); me.polygons.foreach_get("vertices", pv); pv = pv.reshape(nf, 3)
    fn = np.cross(v[pv[:, 1]] - v[pv[:, 0]], v[pv[:, 2]] - v[pv[:, 0]])
    vn = np.zeros((n, 3)); np.add.at(vn, pv.ravel(), np.repeat(fn, 3, axis=0)); vn /= np.linalg.norm(vn, axis=1)[:, None] + 1e-12
    if (vn * d).sum(1).mean() < 0: vn = -vn
    o = bpy.data.objects.new(name, me); link(o)
    # a radius function for placing cameras / boulders on the real surface: radius, point, mesh normal there
    # (smooth = average the normal over a cap of that angular radius, for cameras that should sit on the general slope)
    def surf(dirv, smooth=0.0):
        dv = np.array(dirv, dtype=float); dv /= np.linalg.norm(dv)
        dots = d @ dv; i = int(np.argmax(dots))
        if smooth > 0:
            m = dots > math.cos(smooth); nn = vn[m].mean(0); nn /= np.linalg.norm(nn)
        else: nn = vn[i]
        return float(r[i]), Vector(v[i]), Vector(nn).normalized()
    return o, surf, (d, r)

def rnd_dir():
    while True:
        x = np.random.normal(size=3)
        if np.linalg.norm(x) > 1e-6: return list(x / np.linalg.norm(x))

# Phobos craters: Stickney (~9 km across) on the leading / sub-Mars quarter, Hall (~5 km) on the far side, then a power-law field
STICK = Vector((-0.72, 0.5, 0.48)).normalized()
craters = [(list(STICK), 4.6, 1.15, True), ([0.6, -0.55, -0.55], 2.7, .55, True), ([0.2, -0.95, 0.25], 2.0, .4, False), ([-0.9, 0.3, 0.3], 1.6, .32, False)]
for i in range(210):
    R = .18 + 2.0 * (np.random.random() ** 2.6)
    craters.append((rnd_dir(), R, R * (.18 + .08 * np.random.random()), False))
# groove families: (plane normal, spacing km, width km, depth km, region centre, region spread rad, seed)
GROOVES = [([0.15, 0.1, 1.0], .8, .28, .09, [0.1, -1.0, 0.4], 1.1, 1.0),
           ([1.0, 0.25, 0.3], 1.05, .26, .06, [0.95, 0.1, 0.1], .7, 2.0),
           ([0.3, -1.0, 0.25], .9, .24, .055, [-0.5, -0.1, -0.85], .7, 3.0)]
t0 = time.time()
phobos, psurf, _ = body_mesh("Phobos", PH, craters, GROOVES, 8, .9, 1.4, 1, fine=.012)
print("phobos mesh", len(phobos.data.vertices), "verts %.1fs" % (time.time() - t0), flush=True)
dcr = [([0.5, 0.6, 0.6], 1.5, .25, False), ([-0.7, 0.2, -0.6], 1.1, .18, False)]
for i in range(60):
    R = .15 + 1.0 * (np.random.random() ** 2.5); dcr.append((rnd_dir(), R, R * .12, False))
deimos, dsurf, _ = body_mesh("Deimos", DM, dcr, [], 6, .5, 1.6, 2, fine=.02)
deimos.location = DEIMOS_POS; deimos.rotation_euler = (0.3, 0.1, 0.9)

# regolith materials
def regolith(name, base, light, stk_tint=None):
    m, nt = mat(name); pos, gen = objcoord(nt)
    n1 = NOISE(nt, pos, .6, 4, .55); n2 = NOISE(nt, pos, 6.0, 5, .6); n3 = NOISE(nt, pos, 60.0, 3, .6)
    col = MIXC(nt, M(nt, "MULTIPLY", n1, 1.0), base, light)
    col = MIXC(nt, M(nt, "MULTIPLY", M(nt, "SUBTRACT", n2, .5), .8), col, (base[0] * .6, base[1] * .6, base[2] * .6))
    if stk_tint is not None:
        col = MIXC(nt, M(nt, "MULTIPLY", ATTR(nt, "stk"), .55), col, stk_tint)
    col = MIXC(nt, M(nt, "MULTIPLY", ATTR(nt, "grv"), 1.0), col, (base[0] * .45, base[1] * .44, base[2] * .42))
    # bump: fine regolith + boulder-ish voronoi + micro craters
    vo = VORO(nt, pos, 25.0, "DISTANCE_TO_EDGE")
    bh = M(nt, "ADD", M(nt, "MULTIPLY", n3, .5), M(nt, "MULTIPLY", SMOOTH(nt, vo.outputs["Distance"], 0.0, .05), .35))
    bh = M(nt, "ADD", bh, M(nt, "MULTIPLY", NOISE(nt, pos, 400.0, 2, .5), .25))
    nrm = BUMP(nt, bh, .45, .02)
    b = principled(nt, col, .95, .25, nrm); finish(nt, b.outputs[0]); return m
phobos_m = regolith("PhobosRegolith", (.08, .07, .062), (.12, .11, .098), stk_tint=(.085, .088, .098))
phobos.data.materials.append(phobos_m)
deimos.data.materials.append(regolith("DeimosRegolith", (.07, .063, .056), (.10, .092, .084)))

# boulders near the surface cameras (metres-scale rocks: real Phobos has boulder fields around Stickney)
rock_m = regolith("RockM", (.07, .064, .058), (.11, .10, .092))
SHINE = bpy.data.collections.new("Shine")      # objects that receive the fill / Mars-shine lights (small bodies + rocks; not Mars)
def rock_obj(name, r, seed, flat=.72):
    """a lumpy rock, random tumble baked in, squashed along its local Z (resting rocks are wider than tall);
    returns the object and the lowest point along local Z so it can be sunk into the ground."""
    bm = bmesh.new(); bmesh.ops.create_icosphere(bm, subdivisions=3, radius=r)
    rs = random.Random(seed)
    rot = Matrix.Rotation(rs.random() * 6.3, 3, "X") @ Matrix.Rotation(rs.random() * 6.3, 3, "Y") @ Matrix.Rotation(rs.random() * 6.3, 3, "Z")
    for v in bm.verts:
        v.co *= 1 + .35 * noise.noise(v.co * (3.0 / r) + Vector((seed, seed * .3, 0))) + .12 * (rs.random() - .5)
        v.co = rot @ v.co; v.co.z *= flat
    zmin = min(v.co.z for v in bm.verts)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    me.polygons.foreach_set("use_smooth", [True] * len(me.polygons)); me.update()
    o = bpy.data.objects.new(name, me); link(o); SHINE.objects.link(o); o.data.materials.append(rock_m); return o, zmin
def scatter_rocks(prefix, dirv, count, spread_km, rmin, rmax, seed):
    rs = random.Random(seed); cen = Vector(dirv).normalized()
    u = cen.cross(Vector((0, 0, 1)) if abs(cen.z) < .9 else Vector((1, 0, 0))).normalized(); w = cen.cross(u)
    for i in range(count):
        a = rs.random() * 2 * math.pi; dist = max(0.12, spread_km * (rs.random() ** .6))   # a clear zone where the camera stands
        dd = (cen * 1.0 + (u * math.cos(a) + w * math.sin(a)) * (dist / 11.5)).normalized()
        rr, pt, nrm = psurf(dd); r = rmin + (rmax - rmin) * (rs.random() ** 2.2)
        o, zmin = rock_obj("%s%03d" % (prefix, i), r, seed * 100 + i)
        # stand the rock on the local mesh normal with its lowest point sunk 35% of its radius into the regolith
        o.rotation_mode = "QUATERNION"; o.rotation_quaternion = nrm.to_track_quat("Z", "Y")
        o.location = pt + nrm * (-zmin - r * .35)

# ---------------------------------------------------------------- Mars
bpy.ops.mesh.primitive_uv_sphere_add(radius=RM, location=MC, segments=160, ring_count=80); mars = bpy.context.object; mars.name = "Mars"
bpy.ops.object.shade_smooth()
mars.rotation_euler = (0, 0, 0.6)
mm, nt = mat("MarsSurface"); pos, gen = objcoord(nt)
n_big = NOISE(nt, gen, 3.2, 6, .55); n_mid = NOISE(nt, gen, 11.0, 6, .6); n_fine = NOISE(nt, gen, 40.0, 4, .6)
ochre = (.40, .15, .045); dust = (.62, .31, .12); dark = (.11, .045, .025); rusty = (.34, .13, .05)
col = MIXC(nt, n_big, ochre, dust)
darkm = SMOOTH(nt, M(nt, "ADD", M(nt, "MULTIPLY", n_big, .7), M(nt, "MULTIPLY", n_mid, .3)), .56, .66)
col = MIXC(nt, darkm, col, dark)
col = MIXC(nt, M(nt, "MULTIPLY", M(nt, "SUBTRACT", n_fine, .5), .9), col, rusty)
# polar caps from the generated z (0..1 across the sphere)
sg = N(nt, "ShaderNodeSeparateXYZ"); L(nt, gen, sg.inputs[0])
capz = M(nt, "ABSOLUTE", M(nt, "SUBTRACT", sg.outputs["Z"], .5))
cap = SMOOTH(nt, M(nt, "ADD", capz, M(nt, "MULTIPLY", M(nt, "SUBTRACT", n_mid, .5), .03)), .478, .492)
col = MIXC(nt, cap, col, (.92, .93, .96))
bumph = M(nt, "ADD", M(nt, "MULTIPLY", n_mid, .6), M(nt, "MULTIPLY", n_fine, .4))
b = principled(nt, col, .9, .2, BUMP(nt, bumph, .3, .01)); finish(nt, b.outputs[0])
mars.data.materials.append(mm)
# thin atmosphere rim (a slightly larger sphere, transparent except near the limb)
bpy.ops.mesh.primitive_uv_sphere_add(radius=RM * 1.014, location=MC, segments=96, ring_count=48); atmo = bpy.context.object; atmo.name = "MarsAtmo"
bpy.ops.object.shade_smooth()
am, nt = mat("MarsAtmo"); am.surface_render_method = "BLENDED"; am.use_backface_culling = True
lw = N(nt, "ShaderNodeLayerWeight"); lw.inputs["Blend"].default_value = .5
f = M(nt, "POWER", lw.outputs["Facing"], 4.5)
em = N(nt, "ShaderNodeEmission"); em.inputs["Color"].default_value = (.55, .66, .95, 1); em.inputs["Strength"].default_value = 1.4
tr = N(nt, "ShaderNodeBsdfTransparent")
mx = N(nt, "ShaderNodeMixShader"); L(nt, M(nt, "MULTIPLY", f, .85), mx.inputs[0]); L(nt, tr.outputs[0], mx.inputs[1]); L(nt, em.outputs[0], mx.inputs[2])
finish(nt, mx.outputs[0]); atmo.data.materials.append(am)
atmo.visible_shadow = False; atmo.visible_diffuse = False; atmo.visible_glossy = False

# ---------------------------------------------------------------- world: black with stars; sun
w = bpy.data.worlds.new("Space"); sc.world = w; wn = w.node_tree; wn.nodes.clear()
tc = wn.nodes.new("ShaderNodeTexCoord"); vo = wn.nodes.new("ShaderNodeTexVoronoi"); vo.feature = "F1"; vo.inputs["Scale"].default_value = 160.0; vo.inputs["Randomness"].default_value = 1.0
wn.links.new(tc.outputs["Generated"], vo.inputs["Vector"])
def wm(op, a, b=None):
    n = wn.nodes.new("ShaderNodeMath"); n.operation = op
    for i, x in enumerate((a, b)):
        if x is None: continue
        if lk(x): wn.links.new(x, n.inputs[i])
        else: n.inputs[i].default_value = x
    return n.outputs[0]
star = wm("LESS_THAN", vo.outputs["Distance"], .022)
nz = wn.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 90.0; wn.links.new(tc.outputs["Generated"], nz.inputs["Vector"])
bright = wm("POWER", nz.outputs["Fac"], 6.0)
strength = wm("ADD", wm("MULTIPLY", star, wm("MULTIPLY", bright, 40.0)), 0.0008)
bg = wn.nodes.new("ShaderNodeBackground"); bg.inputs["Color"].default_value = (.85, .88, 1.0, 1)
wn.links.new(strength, bg.inputs["Strength"])
wo = wn.nodes.new("ShaderNodeOutputWorld"); wn.links.new(bg.outputs[0], wo.inputs["Surface"])
sun_d = bpy.data.lights.new("Sun", "SUN"); sun_d.energy = float(arg("--sun", "4.5")); sun_d.angle = math.radians(.35)
sun = bpy.data.objects.new("Sun", sun_d); link(sun)
sun.rotation_euler = SUN_DIR.to_track_quat("Z", "Y").to_euler()
# two weak fills so the night side and crater shadows are dim, not holes to space: Mars-shine (ochre, from Mars) and a faint
# sky fill from the anti-sun side.  Light-linked to the small bodies + rocks only, so Mars' own night side stays dark.
for nm, dirv, col, e, ang in (("MarsShine", Vector((0, 1, 0)), (1.0, .62, .42), float(arg("--shine", "0.55")), 25.0),
                              ("Fill", -SUN_DIR, (.78, .82, .92), float(arg("--fill", "0.4")), 30.0)):
    ld = bpy.data.lights.new(nm, "SUN"); ld.energy = e; ld.color = col; ld.angle = math.radians(ang)
    lo = bpy.data.objects.new(nm, ld); link(lo); lo.rotation_euler = dirv.to_track_quat("Z", "Y").to_euler()
    lo.light_linking.receiver_collection = SHINE
for o in (phobos, deimos): SHINE.objects.link(o)

# ---------------------------------------------------------------- the time-lapse props (shots F, G): marker, orbit line, rubble, ring sheet
marker = bpy.data.objects.new("PhobosMarker", phobos.data); link(marker); marker.scale = (40, 40, 40); SHINE.objects.link(marker)
MARK = 40.0
# orbit line: a bevelled circle around Mars in the XY plane
cu = bpy.data.curves.new("OrbitLine", "CURVE"); cu.dimensions = "3D"; cu.bevel_depth = 32.0 / 9376.0; cu.bevel_resolution = 2; cu.resolution_u = 6
sp = cu.splines.new("NURBS"); sp.points.add(63); sp.use_cyclic_u = True; sp.order_u = 4
for i, pt in enumerate(sp.points):
    a = 2 * math.pi * i / 64; pt.co = (math.sin(a), -math.cos(a), 0, 1)
orbit = bpy.data.objects.new("OrbitLine", cu); link(orbit); orbit.location = MC
om, nt = mat("OrbitLine"); em = N(nt, "ShaderNodeEmission"); em.inputs["Color"].default_value = (.5, .7, 1.0, 1); em.inputs["Strength"].default_value = 2.5; finish(nt, em.outputs[0])
cu.materials.append(om); orbit.visible_shadow = False
# ring sheet: a flat annulus that fades in as the rubble settles into a ring
def annulus(name, r_in, r_out, segs=128):
    vs, fs = [], []
    for i in range(segs):
        a = 2 * math.pi * i / segs; vs += [(r_in * math.cos(a), r_in * math.sin(a), 0), (r_out * math.cos(a), r_out * math.sin(a), 0)]
    for i in range(segs):
        j = (i + 1) % segs; fs.append((2 * i, 2 * i + 1, 2 * j + 1, 2 * j))
    me = bpy.data.meshes.new(name); me.from_pydata(vs, [], fs); me.update(); o = bpy.data.objects.new(name, me); link(o); return o
ring = annulus("RingSheet", 6300.0, 7900.0); ring.location = MC
rm_, nt = mat("RingSheet"); rm_.surface_render_method = "BLENDED"
pos, gen = objcoord(nt)
rn = NOISE(nt, pos, .0025, 4, .6)
sx = N(nt, "ShaderNodeSeparateXYZ"); L(nt, pos, sx.inputs[0])
rad = M(nt, "SQRT", M(nt, "ADD", M(nt, "POWER", sx.outputs[0], 2.0), M(nt, "POWER", sx.outputs[1], 2.0)))
edge = M(nt, "MULTIPLY", SMOOTH(nt, rad, 6300.0, 6700.0), M(nt, "SUBTRACT", 1.0, SMOOTH(nt, rad, 7500.0, 7900.0)))
ringv = N(nt, "ShaderNodeValue"); ringv.name = "ringfac"; ringv.outputs[0].default_value = 0.0
alpha = M(nt, "MULTIPLY", M(nt, "MULTIPLY", edge, M(nt, "ADD", .35, M(nt, "MULTIPLY", rn, .65))), ringv.outputs[0])
dif = N(nt, "ShaderNodeBsdfDiffuse"); dif.inputs["Color"].default_value = (.45, .40, .36, 1)
tr = N(nt, "ShaderNodeBsdfTransparent"); mx = N(nt, "ShaderNodeMixShader"); L(nt, M(nt, "MULTIPLY", alpha, .7), mx.inputs[0]); L(nt, tr.outputs[0], mx.inputs[1]); L(nt, dif.outputs[0], mx.inputs[2])
finish(nt, mx.outputs[0]); ring.data.materials.append(rm_); ring.visible_shadow = False
# rubble: a point cloud with one shape key per snapshot, instanced with geometry nodes
rock_big, _ = rock_obj("RubbleRock", 1.0, 77, flat=1.0); rock_big.hide_render = True; rock_big.hide_viewport = True
NDEB = 1400
deb_me = bpy.data.meshes.new("Rubble"); deb_me.from_pydata([(0, 0, 0)] * NDEB, [], []); deb_me.update()
rubble = bpy.data.objects.new("Rubble", deb_me); link(rubble); rubble.location = MC; SHINE.objects.link(rubble)
ng = bpy.data.node_groups.new("RubbleGN", "GeometryNodeTree")
ng.interface.new_socket("Geometry", in_out="INPUT", socket_type="NodeSocketGeometry"); ng.interface.new_socket("Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
gi = ng.nodes.new("NodeGroupInput"); go = ng.nodes.new("NodeGroupOutput")
m2p = ng.nodes.new("GeometryNodeMeshToPoints"); ng.links.new(gi.outputs[0], m2p.inputs[0])
iop = ng.nodes.new("GeometryNodeInstanceOnPoints"); ng.links.new(m2p.outputs[0], iop.inputs["Points"])
oi = ng.nodes.new("GeometryNodeObjectInfo"); oi.inputs["Object"].default_value = rock_big; oi.transform_space = "ORIGINAL"; ng.links.new(oi.outputs["Geometry"], iop.inputs["Instance"])
rs_ = ng.nodes.new("FunctionNodeRandomValue"); rs_.data_type = "FLOAT"; rs_.inputs[2].default_value = 40.0; rs_.inputs[3].default_value = 170.0; rs_.inputs[8].default_value = 4
ng.links.new(rs_.outputs[1], iop.inputs["Scale"])
rr = ng.nodes.new("FunctionNodeRandomValue"); rr.data_type = "FLOAT_VECTOR"; rr.inputs[0].default_value = (0, 0, 0); rr.inputs[1].default_value = (6.28, 6.28, 6.28); rr.inputs[8].default_value = 5
ng.links.new(rr.outputs[0], iop.inputs["Rotation"]); ng.links.new(iop.outputs[0], go.inputs[0])
md = rubble.modifiers.new("RubbleGN", "NODES"); md.node_group = ng
rubble.visible_shadow = False

# ---------------------------------------------------------------- camera
cd = bpy.data.cameras.new("Cam"); cam = bpy.data.objects.new("Cam", cd); link(cam); sc.camera = cam
cd.clip_start = 0.005; cd.clip_end = 400000.0; cd.sensor_width = 36.0; cd.dof.use_dof = False
cam.rotation_mode = "QUATERNION"
def lookat(p, t, up=Vector((0, 0, 1))):
    f = (Vector(t) - Vector(p)).normalized(); r = f.cross(Vector(up)).normalized(); u = r.cross(f)
    m = Matrix((r, u, -f)).transposed(); return m.to_quaternion()

def surf_point(dirv, h, mesh_normal=False):
    rr_, pt, nrm = psurf(dirv, smooth=0.08)     # the general slope within ~0.9 km, not one vertex's tilt
    if not mesh_normal: nrm = Vector((pt.x / PH[0] ** 2, pt.y / PH[1] ** 2, pt.z / PH[2] ** 2)).normalized()
    return pt + nrm * h, nrm
def surface_cam(dirv, h, elev_deg, az_off=0.0, roll=0.0, mesh_normal=False):
    """camera standing on Phobos at `dirv`, `h` km up, aimed at Mars' azimuth, `elev_deg` above the local horizon."""
    p, n = surf_point(dirv, h, mesh_normal)
    m = (MC - p).normalized(); hz = (m - n * m.dot(n)).normalized()
    if az_off: hz = (hz * math.cos(az_off) + n.cross(hz) * math.sin(az_off)).normalized()
    f = hz * math.cos(math.radians(elev_deg)) + n * math.sin(math.radians(elev_deg))
    return p, p + f * 10.0, n

# per-shot camera keys: list of (frame_offset_fraction, pos, target, up, lens)
def cam_keys(name):
    if name == "A":    # hero: Phobos foreground, Mars behind
        return [(0, (46, -58, 22), (1, 2, 0), None, 35), (1, (40, -56, 26), (0, 3, 0), None, 35)]
    if name == "A2":   # tide shot: closer, Mars limb across the top
        return [(0, (-30, -40, 14), (0, 4, 1), None, 40), (1, (-24, -42, 12), (0, 6, 1), None, 40)]
    if name == "A3":   # close: slow pull back from Phobos with Mars
        return [(0, (26, -34, 10), (0, 0, 0), None, 32), (1, (44, -60, 20), (0, 2, 0), None, 32)]
    if name == "B":    # flyover across the groove field on the far side
        return [(0, (-10, -21, 7), (2, -9, 0), None, 40), (1, (6, -22, 8), (3, -9, 1), None, 40)]
    if name == "B2":   # over the lit groove field (family 1, sun ~50 deg up there): grazing stripes, no terminator in frame
        g = Vector((0.1, -1.0, 0.4)).normalized() * 11.0
        p0 = Vector((0.38, -0.82, 0.62)).normalized() * 30.0; p1 = Vector((0.30, -0.86, 0.58)).normalized() * 27.0
        return [(0, tuple(p0), tuple(g + Vector((1, 0, 0))), None, 48), (1, tuple(p1), tuple(g + Vector((0, 0, .8))), None, 48)]
    if name == "C":    # standing on Phobos: Mars fills the sky
        p0, t0_, n0 = surface_cam((-0.2, 0.45, 0.87), .03, 22.0, 0.0); p1, t1_, n1 = surface_cam((-0.2, 0.45, 0.87), .03, 23.0, .12)
        return [(0, tuple(p0), tuple(t0_), tuple(n0), 18), (1, tuple(p1), tuple(t1_), tuple(n1), 18)]
    if name == "C2":   # the sample shot: a site ~78 deg from the sub-Mars point, so Mars (21 deg radius) sits ON the horizon,
        # its lower limb cut by the ground; camera 20 m up, 8 deg above the horizon, Mars left of centre, boulders right
        p0, t0_, n0 = surface_cam(C2_SITE, .02, 8.0, -.30, mesh_normal=True); p1, t1_, n1 = surface_cam(C2_SITE, .02, 7.0, -.18, mesh_normal=True)
        return [(0, tuple(p0), tuple(t0_), tuple(n0), 18), (1, tuple(p1), tuple(t1_), tuple(n1), 18)]
    if name == "D":    # Stickney
        rr_, ps, _n = psurf(STICK); c = Vector(STICK)
        p0 = ps + (c + Vector((-.3, -.4, .5))).normalized() * 25; p1 = ps + (c + Vector((-.2, -.5, .4))).normalized() * 21
        return [(0, tuple(p0), tuple(ps), None, 45), (1, tuple(p1), tuple(ps + Vector((0, 0, .3))), None, 45)]
    if name == "E":    # Deimos with Mars small behind
        mdir = (MC - DEIMOS_POS).normalized()
        p0 = DEIMOS_POS - mdir * 34 + Vector((9, 0, 7)); p1 = DEIMOS_POS - mdir * 31 + Vector((7, 0, 8))
        return [(0, tuple(p0), tuple(DEIMOS_POS + mdir * 2), None, 35), (1, tuple(p1), tuple(DEIMOS_POS + mdir * 2), None, 35)]
    if name in ("F", "G"):   # far from Mars, ~15 deg above the orbit plane: the far arc of the orbit passes BEHIND Mars
        p0 = MC + Vector((-15500, -11000, 5200)); p1 = MC + Vector((-14000, -12500, 4700))
        return [(0, tuple(p0), tuple(MC), None, 26), (1, tuple(p1), tuple(MC), None, 26)]
    raise KeyError(name)

# the sample-shot site: search near C2_SITE for ground whose general slope puts Mars' centre 8-12 deg above the local
# horizon (Mars is 21 deg in radius, so its lower limb is cut by the ground) with the Sun at least ~25 deg up
def find_site(base, hide_lo=6.0, hide_hi=18.0, sun_min=0.42, h=0.02):
    """Mars' centre elevation vs the real terrain horizon toward Mars (ray-marched along the surface): keep sites where the
    ground hides between `hide_lo` and `hide_hi` degrees of Mars' lower part (Mars is ~22.5 deg in radius from the surface)."""
    base = Vector(base).normalized(); best = None; rs = random.Random(7)
    for i in range(900):
        dv = (base + Vector((rs.gauss(0, .16), rs.gauss(0, .16), rs.gauss(0, .16)))).normalized()
        _, pt, nn = psurf(dv, smooth=0.08)
        if nn.dot(SUN_DIR) < sun_min: continue
        p = pt + nn * h; m = (MC - p).normalized(); mars_el = math.degrees(math.asin(max(-1, min(1, m.dot(nn)))))
        hz = (m - nn * m.dot(nn)).normalized(); hor = -90.0
        for s in [k * .012 for k in range(1, 60)]:
            dvs = (dv * math.cos(s) + hz * math.sin(s)).normalized(); _, ps, _n = psurf(dvs)
            hor = max(hor, math.degrees(math.asin(max(-1, min(1, (ps - p).normalized().dot(nn))))))
        hidden = hor - (mars_el - 22.5)
        if hide_lo <= hidden <= hide_hi:
            dist = (dv - base).length
            if best is None or dist < best[0]: best = (dist, tuple(dv), round(mars_el, 1), round(hor, 1), round(hidden, 1))
    print("C2 site:", best, flush=True); return best[1]
C2_SITE = find_site(C2_SITE)
# scatter boulders where the surface cameras stand
scatter_rocks("RkC", (-0.2, 0.45, 0.87), 90, 1.2, .004, .035, 3)
scatter_rocks("RkC2", C2_SITE, 110, 1.4, .004, .04, 4)
scatter_rocks("RkD", list(STICK), 60, 5.5, .03, .09, 5)
# (no rocks under the groove camera: at 27 km they only read as dark specks)

# ---------------------------------------------------------------- keyframes
def key_vis(o, frame, hidden):
    o.hide_render = hidden; o.keyframe_insert("hide_render", frame=frame)
def key_ring(frame, v):
    ringv.outputs[0].default_value = v; ringv.outputs[0].keyframe_insert("default_value", frame=frame)
for o in (marker, orbit, ring, rubble): key_vis(o, 1, True)
key_ring(1, 0.0)
f = 1; cut = set()
for sh in SHOTS:
    n = int(round(sh["dur"] * FPS)); fa, fb = f, f + n - 1
    if sh["cam"] is None:
        f = fb + 1; continue
    cut.add(fb)
    for u, p, t, up, lens in cam_keys(sh["cam"]):
        ff = int(round(fa + (fb - fa) * u))
        sc.frame_set(ff); cam.location = p; cam.rotation_quaternion = lookat(p, t, Vector(up) if up else Vector((0, 0, 1)))
        cam.keyframe_insert("location", frame=ff); cam.keyframe_insert("rotation_quaternion", frame=ff)
        cd.lens = lens; cd.keyframe_insert("lens", frame=ff)
    timelapse = sh["cam"] in ("F", "G")
    # real Phobos / Deimos only in the near shots; time-lapse props only in F/G
    key_vis(phobos, fa, timelapse); key_vis(phobos, fb + 1, True)
    key_vis(deimos, fa, timelapse); key_vis(deimos, fb + 1, True)
    for o in (orbit,): key_vis(o, fa, not timelapse); key_vis(o, fb + 1, True)
    key_vis(marker, fa, sh["cam"] != "F"); key_vis(marker, fb + 1, True)
    key_vis(rubble, fa, sh["cam"] != "G"); key_vis(rubble, fb + 1, True)
    key_vis(ring, fa, sh["cam"] != "G"); key_vis(ring, fb + 1, True)
    if sh["cam"] == "F":
        # orbit radius 9,376 -> ~7,900 km, accelerating; 5 laps across the shot; Mars turns a little
        for i in range(n):
            u = i / (n - 1); r = 9376.0 - (9376.0 - 7900.0) * (u ** 2.2); th = 2 * math.pi * 5.0 * u
            sc.frame_set(fa + i)
            marker.location = MC + Vector((r * math.sin(th), -r * math.cos(th), 0)); marker.keyframe_insert("location", frame=fa + i)
            marker.rotation_euler = (0, 0, th); marker.keyframe_insert("rotation_euler", frame=fa + i)
            orbit.scale = (r, r, r); orbit.keyframe_insert("scale", frame=fa + i)
            mars.rotation_euler = (0, 0, 0.6 + u * .5); mars.keyframe_insert("rotation_euler", frame=fa + i)
    if sh["cam"] == "G":
        # the break-up: 1,400 rubble pieces stream out along the orbit (r ~7,900 -> a band 6,500-7,800), 2.5 laps, then a ring sheet
        r_b = 7900.0; rs = np.random.RandomState(5)
        dl = (rs.random_sample(NDEB) ** 1.4) * (2 * math.pi * 1.35) * np.where(rs.random_sample(NDEB) < .5, 1, -1)
        rad_i = r_b - (rs.random_sample(NDEB) ** 1.3) * 1300.0 * np.clip(rs.random_sample(NDEB) * 1.4, 0, 1)
        z_i = rs.normal(size=NDEB) * 45.0
        clump = rs.normal(size=(NDEB, 3)) * np.array([160.0, 160.0, 90.0])
        step = 8; snaps = list(range(0, n, step)) + [n - 1]
        rubble.shape_key_add(name="Basis", from_mix=False)
        for k, i in enumerate(snaps):
            u = i / (n - 1); s = u * u * (3 - 2 * u); spread = s ** .8; th0 = 2 * math.pi * 2.5 * u
            r_now = r_b - (r_b - rad_i) * np.clip(s * 1.3, 0, 1)
            th = th0 + dl * spread
            x = r_now * np.sin(th) + clump[:, 0] * (1 - .85 * spread); y = -r_now * np.cos(th) + clump[:, 1] * (1 - .85 * spread); z = z_i * spread + clump[:, 2] * (1 - .85 * spread)
            co = np.stack([x, y, z], 1).ravel()
            kb = rubble.data.shape_keys.key_blocks[0] if k == 0 else rubble.shape_key_add(name="s%02d" % k, from_mix=False)
            kb.data.foreach_set("co", co)
            if k > 0:
                for fr, v in ((snaps[k - 1], 0.0), (i, 1.0), (snaps[k + 1] if k + 1 < len(snaps) else i + 1, 0.0)):
                    kb.value = v; kb.keyframe_insert("value", frame=fa + fr)
            key_ring(fa + i, max(0.0, (u - .55) / .45) ** 1.5 * .9)
            sc.frame_set(fa + i); orbit.scale = (r_b, r_b, r_b); orbit.keyframe_insert("scale", frame=fa + i)
            mars.rotation_euler = (0, 0, 1.1 + u * .5); mars.keyframe_insert("rotation_euler", frame=fa + i)
    f = fb + 1

def all_curves(idb):
    ad = idb.animation_data
    if not ad or not ad.action: return []
    cs = getattr(ad.action, "fcurves", None)
    if cs is not None: return list(cs)
    try: return [fc for layer in ad.action.layers for strip in layer.strips for bag in strip.channelbags for fc in bag.fcurves]
    except Exception: return []
for idb in [o for o in bpy.data.objects] + list(bpy.data.materials) + [rubble.data.shape_keys] if rubble.data.shape_keys else [o for o in bpy.data.objects] + list(bpy.data.materials):
    for fc in all_curves(idb):
        for k in fc.keyframe_points:
            k.interpolation = "LINEAR"
for idb in (cam, cd):
    for fc in all_curves(idb):
        for k in fc.keyframe_points:
            k.interpolation = "CONSTANT" if int(k.co[0]) in cut else "BEZIER"; k.easing = "EASE_IN_OUT"
print("frames", DUR, flush=True)
if "--debug" in argv:
    dg = bpy.context.evaluated_depsgraph_get()
    for fr in (3313, 3500, 3700, 4000):
        sc.frame_set(fr); ev = rubble.evaluated_get(dg)
        vs = [v.co for v in ev.data.vertices]; inst = sum(1 for i in dg.object_instances if i.is_instance and i.parent and i.parent.name == "Rubble")
        print("DEBUG", fr, "verts", len(vs), "instances", inst, "x range", (min(v.x for v in vs), max(v.x for v in vs)) if vs else None, "hide", rubble.hide_render, [ (k.name, round(k.value, 2)) for k in rubble.data.shape_keys.key_blocks if k.value > 0][:4], flush=True)

# ---------------------------------------------------------------- outputs
if arg("--save"): bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(arg("--save")))
if arg("--still"):
    i = argv.index("--still"); fr = int(argv[i + 1]); outp = argv[i + 2]
    sc.frame_set(fr); sc.render.filepath = os.path.abspath(outp); bpy.ops.render.render(write_still=True); print("STILL", outp)
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
    if arg("--ranges"):   # several a-b ranges in one run (one scene build): --ranges 673-1248,1969-2400
        todo = [fr for ab in arg("--ranges").split(",") for fr in range(int(ab.split("-")[0]), int(ab.split("-")[1]) + 1, int(arg("--step", "1")))]
    for fr in todo:
        p = os.path.join(outd, "f_%04d.png" % fr)
        if fr in skip or (os.path.exists(p) and os.path.getsize(p) > 1000): continue
        t0 = time.time(); sc.frame_set(fr); sc.render.filepath = p; bpy.ops.render.render(write_still=True)
        print("FRAME %d %.1fs" % (fr, time.time() - t0), flush=True)
