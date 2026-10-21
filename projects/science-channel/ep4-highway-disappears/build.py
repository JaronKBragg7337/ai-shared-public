# Heartbeat TV Science 8.4 "How a highway disappears" - one stretch of a central-Indiana interstate, the same camera
# positions as the seasons and years pass.  Pure-script Blender 5.1 scene (no downloaded assets): procedural asphalt with
# cracks/paint/dirt/moss/water, shape-key potholes and slab heave, geometry-nodes grass + leaf litter + saplings, blob trees
# (framed at distance), a green sign on steel posts, a storm-drain inlet, a concrete overpass that spalls.
# One number STAGE (0 clean .. 1 first summer .. 2 first fall .. 3 first winter .. 4 years 2-5 .. 5 years 5-20 .. 6 years 20-50)
# is keyed per shot; every material / modifier / object reads it through the param table P below.
# Cycles OptiX on the RTX 4060 (one GPU job at a time).
#   blender -b -P build.py -- [--still FRAME out.png] [--stills DIR --frames a,b,c] [--anim OUTDIR [--start F --end F]]
#                             [--samples N] [--cpu] [--save out.blend]
import bpy, bmesh, math, random, sys, os, json
from mathutils import Vector, noise

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from shots import SHOTS, FPS
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def arg(k, d=None): return argv[argv.index(k) + 1] if k in argv else d
random.seed(11)
ZERO = [z for z in arg("--zero", "").split(",") if z]

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
sc.cycles.samples = int(arg("--samples", "40")); sc.cycles.use_adaptive_sampling = True; sc.cycles.adaptive_threshold = 0.06
sc.cycles.use_denoising = True; sc.cycles.denoiser = "OPENIMAGEDENOISE" if "--cpu" in argv else "OPTIX"
sc.cycles.max_bounces = 4; sc.cycles.diffuse_bounces = 2; sc.cycles.glossy_bounces = 2; sc.cycles.transmission_bounces = 2; sc.cycles.volume_bounces = 0
sc.cycles.transparent_max_bounces = int(arg("--tmb", "256"))
sc.cycles.caustics_reflective = False; sc.cycles.caustics_refractive = False
sc.cycles.blur_glossy = 1.0; sc.cycles.sample_clamp_indirect = 6.0
sc.render.resolution_x, sc.render.resolution_y = int(arg("--w", "1280")), int(arg("--h", "720")); sc.render.resolution_percentage = 100
sc.render.use_motion_blur = False
sc.view_settings.view_transform = "AgX"
try: sc.view_settings.look = "AgX - Medium Contrast"
except Exception: pass
sc.view_settings.exposure = float(arg("--exp", "-2.6"))
sc.render.image_settings.file_format = "PNG"; sc.render.image_settings.color_mode = "RGB"

# ---------------------------------------------------------------- the stage parameter table (piecewise-linear in STAGE)
P = {
 "grass_h":  [(0, .10), (.6, .13), (1, .70), (2, .75), (2.7, .6), (3, .3), (3.4, .45), (4, .8), (6, .85)],
 "dead":     [(0, 0), (.7, .05), (1, .35), (2, .6), (3, .85), (3.4, .25), (4, .3), (6, .3)],
 "encroach": [(3, 0), (4, .7), (5, 2.6), (6, 5.5)],
 "weeds":    [(3, 0), (3.6, .04), (4, .35), (5, .9), (6, 1)],
 "leaves":   [(1.4, 0), (2, 1), (2.6, .9), (3, .35), (3.4, .22), (6, .3)],
 "snow":     [(2.7, 0), (3, 1), (3.35, 0)],
 "crack":    [(0, .10), (2, .13), (3, .3), (4, .55), (5, .8), (6, 1)],
 "moss":     [(3, 0), (4, .6), (5, 1), (6, 1)],
 "dirt":     [(2.5, 0), (4, .2), (5, .55), (6, .9)],
 "pothole":  [(3, 0), (3.3, .06), (4, .4), (5, .8), (6, 1)],
 "heave":    [(4, 0), (5, .3), (6, 1)],
 "water":    [(2.5, 0), (3.3, .6), (4, 1), (6, 1)],
 "paint":    [(0, 1), (2, .95), (4, .6), (5, .22), (6, .02)],
 "sapl":     [(4.2, 0), (4.6, .04), (5, .25), (5.5, .55), (6, 1)],
 "sapl_d":   [(4.2, 0), (5, .6), (6, 1)],
 "rust":     [(2, 0), (4, .15), (5, .5), (6, 1)],
 "lean":     [(4.5, 0), (5, 5), (6, 21)],
 "spall":    [(4, 0), (5, .3), (6, 1)],
 "fall":     [(1.5, 0), (2, 1), (2.6, 1), (3, 0)],
 "bare":     [(2.4, 0), (2.8, 1), (3, 1), (3.4, 0)],
 "grow":     [(0, 1), (4, 1.05), (6, 1.3)],
 "sun_el":   [(0, 54), (1, 60), (2, 36), (3, 20), (3.4, 44), (4, 56), (6, 54)],
 "sun_rot":  [(0, 150), (1, 140), (2, 165), (3, 175), (3.4, 150), (6, 150)],
 "sun_str":  [(0, 1), (2, .9), (2.7, .8), (3, .22), (3.4, .9), (6, 1)],
 "overcast": [(2.6, 0), (3, 1), (3.4, 0)],
 "burrow":   [(4.6, 0), (5, 1)],
}
def pl(s, pts):
    if s <= pts[0][0]: return pts[0][1]
    for (a, va), (b, vb) in zip(pts, pts[1:]):
        if s <= b: return va + (vb - va) * (s - a) / (b - a)
    return pts[-1][1]
def pv(name, s): return pl(s, P[name])

SETTERS = []          # (apply(value), fn(stage)) - keyed at every stage key
def reg(fn, apply): SETTERS.append((apply, fn))

def val_node(nt, name, pname, scale=1.0, off=0.0):
    """a Value node in node tree nt driven by stage param pname (keyframed)"""
    v = nt.nodes.new("ShaderNodeValue"); v.name = v.label = name
    def apply(x, v=v): v.outputs[0].default_value = x; v.outputs[0].keyframe_insert("default_value", frame=sc.frame_current)
    reg((lambda s: 0.0) if pname in ZERO else (lambda s: pv(pname, s) * scale + off), apply)
    return v.outputs[0]

# ---------------------------------------------------------------- node helpers
def mat(name):
    m = bpy.data.materials.new(name); nt = m.node_tree; nt.nodes.clear()
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
def M(nt, op, a, b=None, c=None):
    n = nt.nodes.new("ShaderNodeMath"); n.operation = op; n.use_clamp = False
    for i, x in enumerate((a, b, c)):
        if x is None: continue
        if hasattr(x, "is_linked"): L(nt, x, n.inputs[i])
        else: n.inputs[i].default_value = x
    return n.outputs[0]
def MIXC(nt, fac, a, b, blend="MIX"):
    n = nt.nodes.new("ShaderNodeMix"); n.data_type = "RGBA"; n.blend_type = blend; n.clamp_factor = True
    for sock, x in ((n.inputs["Factor"], fac), (n.inputs[6], a), (n.inputs[7], b)):
        if hasattr(x, "is_linked"): L(nt, x, sock)
        else: sock.default_value = x if len(x) == 4 else tuple(x) + (1,)
    return n.outputs[2]
def MIXF(nt, fac, a, b):
    n = nt.nodes.new("ShaderNodeMix"); n.data_type = "FLOAT"; n.clamp_factor = True
    for sock, x in ((n.inputs["Factor"], fac), (n.inputs[2], a), (n.inputs[3], b)):
        if hasattr(x, "is_linked"): L(nt, x, sock)
        else: sock.default_value = x
    return n.outputs[0]
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
def SMOOTH(nt, x, a, b):     # smoothstep via map range
    n = N(nt, "ShaderNodeMapRange"); n.interpolation_type = "SMOOTHSTEP"
    for sock, v in ((n.inputs["From Min"], a), (n.inputs["From Max"], b)):
        if hasattr(v, "is_linked"): L(nt, v, sock)
        else: sock.default_value = v
    L(nt, x, n.inputs["Value"]); return n.outputs[0]
def finish(nt, shader, disp=None):
    L(nt, shader, nt.nodes["OUT"].inputs["Surface"])
    if disp is not None: L(nt, disp, nt.nodes["OUT"].inputs["Displacement"])
def principled(nt, color, rough, spec=.5, normal=None, metallic=0.0, trans=None, sss=None):
    b = N(nt, "ShaderNodeBsdfPrincipled"); b.inputs["Roughness"].default_value = rough if not hasattr(rough, "is_linked") else .5
    if hasattr(rough, "is_linked"): L(nt, rough, b.inputs["Roughness"])
    if hasattr(color, "is_linked"): L(nt, color, b.inputs["Base Color"])
    else: b.inputs["Base Color"].default_value = tuple(color) + (1,)
    b.inputs["Specular IOR Level"].default_value = spec; b.inputs["Metallic"].default_value = metallic
    if normal is not None: L(nt, normal, b.inputs["Normal"])
    return b
def snowmix(nt, shader, snow, noise_fac, up):
    """mix a snow BSDF over `shader` on upward faces, patchy by noise, by the snow param"""
    sb = N(nt, "ShaderNodeBsdfPrincipled"); sb.inputs["Base Color"].default_value = (.86, .88, .92, 1); sb.inputs["Roughness"].default_value = .75
    sb.inputs["Subsurface Weight"].default_value = .3; sb.inputs["Subsurface Radius"].default_value = (.05, .05, .06)
    f = M(nt, "MULTIPLY", snow, up); f = M(nt, "MULTIPLY", f, SMOOTH(nt, noise_fac, .25, .5)); f = SMOOTH(nt, M(nt, "MULTIPLY", f, 1.6), .3, .7)
    mx = N(nt, "ShaderNodeMixShader"); L(nt, f, mx.inputs[0]); L(nt, shader, mx.inputs[1]); L(nt, sb.outputs[0], mx.inputs[2])
    return mx.outputs[0]
def upness(nt):
    g = N(nt, "ShaderNodeNewGeometry"); sx = N(nt, "ShaderNodeSeparateXYZ"); L(nt, g.outputs["Normal"], sx.inputs[0])
    return SMOOTH(nt, sx.outputs["Z"], .45, .85)

# ---------------------------------------------------------------- geometry helpers
def mesh_obj(name, verts, faces, m=None, smooth=False):
    me = bpy.data.meshes.new(name); me.from_pydata(verts, [], faces); me.update()
    if smooth:
        for p in me.polygons: p.use_smooth = True
    o = bpy.data.objects.new(name, me); bpy.context.collection.objects.link(o)
    if m: me.materials.append(m)
    return o
def box(name, a, b, m, bevel=0.0):
    x0, y0, z0 = a; x1, y1, z1 = b
    v = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0), (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
    f = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    o = mesh_obj(name, v, f, m)
    if bevel:
        bm = o.modifiers.new("Bevel", "BEVEL"); bm.width = bevel; bm.segments = 2
    return o
def cyl(name, base, r, h, m, verts=16, r_top=None, axis="z"):
    bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=r, radius2=r if r_top is None else r_top, depth=h, location=(base[0], base[1], base[2] + h / 2))
    o = bpy.context.object; o.name = name; o.data.materials.append(m)
    if axis == "y": o.rotation_euler = (math.pi / 2, 0, 0); o.location = (base[0], base[1] + h / 2, base[2])
    if axis == "x": o.rotation_euler = (0, math.pi / 2, 0); o.location = (base[0] + h / 2, base[1], base[2])
    for p in o.data.polygons: p.use_smooth = True
    return o
def grid(name, x0, x1, y0, y1, step, m, zfn=None):
    nx = int(round((x1 - x0) / step)); ny = int(round((y1 - y0) / step))
    verts = []; faces = []
    for j in range(ny + 1):
        for i in range(nx + 1):
            x = x0 + i * step; y = y0 + j * step
            verts.append((x, y, zfn(x, y) if zfn else 0.0))
    for j in range(ny):
        for i in range(nx):
            a = j * (nx + 1) + i; faces.append((a, a + 1, a + nx + 2, a + nx + 1))
    return mesh_obj(name, verts, faces, m, smooth=True)

# ---------------------------------------------------------------- layout (metres; road along +X, camera-side shoulder is +Y)
X0, X1 = -90, 300
PIN, POUT = 4.8, 20.0          # pavement from |y|=4.8 (inner shoulder) to 20.0 (outer shoulder edge); lanes 6..17 (3 x 3.66)
OVX = 112.0                    # overpass centre x
SIGNX, SIGNY = 60.0, 23.2
DRAINX, DRAINY = 20.0, 19.0
POTS = [(40.5, 11.8, 0.95, .17), (38.2, 13.4, .5, .1)] + [(random.uniform(-60, 290), random.choice([1, -1]) * random.uniform(6.5, 18.5), random.uniform(.3, 1.2), random.uniform(.05, .13)) for _ in range(110)]
PUDDLES = [(43.5, 9.8, 4.5, .035), (24, 16.5, 3.5, .03)] + [(random.uniform(-60, 290), random.choice([1, -1]) * random.uniform(7, 17), random.uniform(2.5, 6), random.uniform(.02, .04)) for _ in range(40)]

# ---------------------------------------------------------------- materials
# asphalt (lanes + paved shoulders): paint, cracks (+moss), dirt, pits -> water, snow
asph, nt = mat("Asphalt")
tc = N(nt, "ShaderNodeTexCoord"); pos = tc.outputs["Object"]
sxyz = N(nt, "ShaderNodeSeparateXYZ"); L(nt, pos, sxyz.inputs[0]); X, Y, Z = sxyz.outputs
crack = val_node(nt, "crack", "crack"); moss = val_node(nt, "moss", "moss"); dirt = val_node(nt, "dirt", "dirt")
water = val_node(nt, "water", "water"); paint = val_node(nt, "paint", "paint"); snow = val_node(nt, "snow", "snow")
ay = M(nt, "ABSOLUTE", Y)
# base asphalt: fine aggregate noise + wear band in wheel paths
n1 = NOISE(nt, pos, 40, 4, .6); n2 = NOISE(nt, pos, .35, 2)
base = RAMP(nt, n1, [(0, (.03, .03, .03)), (1, (.085, .085, .08))])
base = MIXC(nt, M(nt, "MULTIPLY", n2, .5), base, (.07, .07, .068))
# cracks: coarse network widening + fine alligator net later
v1 = VORO(nt, pos, .45); v2 = VORO(nt, pos, 2.2)
cw = M(nt, "ADD", .003, M(nt, "MULTIPLY", crack, .014))
c1 = SMOOTH(nt, v1.outputs["Distance"], cw, M(nt, "MULTIPLY", cw, .3))      # 1 inside crack
net = NOISE(nt, pos, .08, 2); c1 = M(nt, "MULTIPLY", c1, SMOOTH(nt, net, M(nt, "SUBTRACT", .95, M(nt, "MULTIPLY", crack, .9)), M(nt, "SUBTRACT", 1.0, M(nt, "MULTIPLY", crack, .75))))
c2 = SMOOTH(nt, v2.outputs["Distance"], .007, .002); c2 = M(nt, "MULTIPLY", c2, SMOOTH(nt, crack, .55, .95)); c2 = M(nt, "MULTIPLY", c2, SMOOTH(nt, NOISE(nt, pos, .12, 2), .45, .7))
ck = M(nt, "MAXIMUM", c1, c2)
mossc = MIXC(nt, moss, (.008, .008, .007), (.012, .03, .008))
col = MIXC(nt, ck, base, mossc)
# lane paint: yellow inner edge |y|=6, white outer edge |y|=17, dashed whites at 9.66 / 13.32 (3 m dash, 9 m gap)
def band(c, w): return M(nt, "MULTIPLY", SMOOTH(nt, ay, c - w - .01, c - w), SMOOTH(nt, ay, c + w + .01, c + w))
dash = SMOOTH(nt, M(nt, "MODULO", M(nt, "ADD", X, 1000.0), 12.0), 3.05, 2.95)
ywhite = M(nt, "ADD", band(17.0, .06), M(nt, "MULTIPLY", dash, M(nt, "ADD", band(9.66, .06), band(13.32, .06))))
yyellow = band(6.0, .06)
wear = M(nt, "MULTIPLY", paint, SMOOTH(nt, NOISE(nt, pos, 3, 3), M(nt, "SUBTRACT", .7, M(nt, "MULTIPLY", paint, .55)), M(nt, "SUBTRACT", .9, M(nt, "MULTIPLY", paint, .55))))
pm = M(nt, "MULTIPLY", M(nt, "SUBTRACT", 1.0, ck), wear)
col = MIXC(nt, M(nt, "MULTIPLY", ywhite, pm), col, (.8, .8, .78)); col = MIXC(nt, M(nt, "MULTIPLY", yyellow, pm), col, (.85, .62, .08))
# dirt / thin soil: noise blotches + heavier at the pavement edges + in the pits
dn = NOISE(nt, pos, .14, 3, .55); edge = SMOOTH(nt, ay, 15.5, 19.9); edge2 = SMOOTH(nt, ay, 7.0, 5.0)
dm = SMOOTH(nt, M(nt, "ADD", dn, M(nt, "MULTIPLY", M(nt, "MAXIMUM", edge, edge2), .25)), M(nt, "SUBTRACT", 1.05, M(nt, "MULTIPLY", dirt, .95)), M(nt, "SUBTRACT", 1.15, M(nt, "MULTIPLY", dirt, .95)))
pit = SMOOTH(nt, Z, -.004, -.03)
dm = M(nt, "MAXIMUM", dm, M(nt, "MULTIPLY", pit, dirt))
soil = RAMP(nt, NOISE(nt, pos, 9, 3), [(0, (.08, .055, .03)), (1, (.16, .12, .07))])
col = MIXC(nt, dm, col, soil)
rough = MIXF(nt, dm, .85, .95); rough = MIXF(nt, ck, rough, .95)
# water in the pits (dark, glossy, shallow): where z dips below the surface
wm = M(nt, "MULTIPLY", SMOOTH(nt, Z, -.012, -.03), water)
wcol = MIXC(nt, wm, col, (.02, .025, .025)); wrough = MIXF(nt, wm, rough, .05)
# bump: aggregate + cracks
bmp = N(nt, "ShaderNodeBump"); bmp.inputs["Strength"].default_value = .12; bmp.inputs["Distance"].default_value = .01
hgt = M(nt, "SUBTRACT", M(nt, "MULTIPLY", n1, .3), M(nt, "MULTIPLY", ck, .6)); L(nt, hgt, bmp.inputs["Height"])
b = principled(nt, wcol, wrough, .2, bmp.outputs[0])
up = upness(nt)
finish(nt, snowmix(nt, b.outputs[0], M(nt, "MULTIPLY", snow, .8), NOISE(nt, pos, .6, 2), up))

# ground: grass-coloured soil with tyre ruts near the shoulder; ditch bottoms hold water; snow
grd, nt = mat("Ground")
tc = N(nt, "ShaderNodeTexCoord"); pos = tc.outputs["Object"]
sxyz = N(nt, "ShaderNodeSeparateXYZ"); L(nt, pos, sxyz.inputs[0]); X, Y, Z = sxyz.outputs
dead = val_node(nt, "dead", "dead"); snow = val_node(nt, "snow", "snow"); water = val_node(nt, "water", "water")
gn = NOISE(nt, pos, .9, 4, .6); gn2 = NOISE(nt, pos, 12, 3)
green = RAMP(nt, gn, [(0, (.05, .12, .02)), (.5, (.09, .18, .035)), (1, (.14, .2, .05))])
straw = RAMP(nt, gn, [(0, (.22, .17, .07)), (1, (.36, .3, .14))])
col = MIXC(nt, M(nt, "MULTIPLY", dead, SMOOTH(nt, gn2, .2, .8)), green, straw)
col = MIXC(nt, M(nt, "MULTIPLY", gn2, .35), col, (.06, .045, .025))
wm = M(nt, "MULTIPLY", SMOOTH(nt, Z, -.42, -.52), water)
col = MIXC(nt, wm, col, (.03, .035, .03)); rough = MIXF(nt, wm, .9, .06)
bmp = N(nt, "ShaderNodeBump"); bmp.inputs["Strength"].default_value = .4; bmp.inputs["Distance"].default_value = .03; L(nt, gn2, bmp.inputs["Height"])
b = principled(nt, col, rough, .3, bmp.outputs[0])
finish(nt, snowmix(nt, b.outputs[0], snow, NOISE(nt, pos, .5, 2), upness(nt)))

# grass blades: per-instance random hue, dead/straw mix by stage, translucent, snow dusting
gra, nt = mat("GrassBlade")
oi = N(nt, "ShaderNodeObjectInfo"); rnd = oi.outputs["Random"]
tc = N(nt, "ShaderNodeTexCoord"); gen = tc.outputs["Generated"]; sg = N(nt, "ShaderNodeSeparateXYZ"); L(nt, gen, sg.inputs[0])
dead = val_node(nt, "dead", "dead"); snow = val_node(nt, "snow", "snow")
green = RAMP(nt, rnd, [(0, (.06, .16, .025)), (.5, (.1, .22, .04)), (1, (.16, .25, .06))])
straw = RAMP(nt, rnd, [(0, (.3, .24, .1)), (1, (.5, .42, .2))])
dfac = SMOOTH(nt, M(nt, "ADD", M(nt, "MULTIPLY", dead, 1.3), M(nt, "MULTIPLY", rnd, .4)), .35, .95)
dfac = M(nt, "MAXIMUM", dfac, M(nt, "MULTIPLY", dead, sg.outputs["Z"]))        # tips go to seed first
col = MIXC(nt, dfac, green, straw)
col = MIXC(nt, M(nt, "MULTIPLY", snow, .7), col, (.85, .87, .9))
b = principled(nt, col, .7, .25); b.inputs["Subsurface Weight"].default_value = 0.0
tr = N(nt, "ShaderNodeBsdfTranslucent"); L(nt, col, tr.inputs["Color"])
mx = N(nt, "ShaderNodeMixShader"); mx.inputs[0].default_value = .35; L(nt, b.outputs[0], mx.inputs[1]); L(nt, tr.outputs[0], mx.inputs[2])
finish(nt, mx.outputs[0])

# leaf litter: per-instance attribute "lv" -> orange/brown/yellow; snow
lef, nt = mat("Leaf")
at = N(nt, "ShaderNodeAttribute"); at.attribute_name = "lv"; at.attribute_type = "GEOMETRY"
snow = val_node(nt, "snow", "snow"); leaves_p = val_node(nt, "leaves", "leaves")
col = RAMP(nt, at.outputs["Fac"], [(0, (.5, .14, .03)), (.3, (.55, .3, .05)), (.6, (.3, .12, .03)), (1, (.18, .09, .03))])
# older litter goes brown-grey (leaves param small = old)
col = MIXC(nt, SMOOTH(nt, leaves_p, .6, .3), col, (.14, .1, .06))
col = MIXC(nt, M(nt, "MULTIPLY", snow, .8), col, (.85, .87, .9))
b = principled(nt, col, .8, .2); tr = N(nt, "ShaderNodeBsdfTranslucent"); L(nt, col, tr.inputs["Color"])
mx = N(nt, "ShaderNodeMixShader"); mx.inputs[0].default_value = .3; L(nt, b.outputs[0], mx.inputs[1]); L(nt, tr.outputs[0], mx.inputs[2])
finish(nt, mx.outputs[0])

# tree canopy: leafy noise colour, fall colour, bare (holes) in winter, snow on top
can, nt = mat("Canopy")
tc = N(nt, "ShaderNodeTexCoord"); pos = tc.outputs["Object"]; oi = N(nt, "ShaderNodeObjectInfo"); rnd = oi.outputs["Random"]
fall = val_node(nt, "fall", "fall"); bare = val_node(nt, "bare", "bare"); snow = val_node(nt, "snow", "snow")
ln = NOISE(nt, pos, 2.5, 4, .6)
green = RAMP(nt, ln, [(0, (.03, .09, .015)), (.5, (.07, .16, .03)), (1, (.15, .24, .05))])
green = MIXC(nt, M(nt, "MULTIPLY", rnd, .5), green, (.1, .14, .03))
fcol = RAMP(nt, M(nt, "ADD", ln, M(nt, "MULTIPLY", rnd, .7)), [(0, (.6, .25, .03)), (.4, (.7, .5, .06)), (.8, (.55, .12, .03)), (1, (.3, .1, .03))])
col = MIXC(nt, SMOOTH(nt, M(nt, "ADD", fall, M(nt, "MULTIPLY", rnd, .5)), .3, .9), green, fcol)
col = MIXC(nt, M(nt, "MULTIPLY", snow, .5), col, (.85, .87, .9))
b = principled(nt, col, .75, .2); tr = N(nt, "ShaderNodeBsdfTranslucent"); L(nt, col, tr.inputs["Color"])
mx = N(nt, "ShaderNodeMixShader"); mx.inputs[0].default_value = .3; L(nt, b.outputs[0], mx.inputs[1]); L(nt, tr.outputs[0], mx.inputs[2])
# holes: fine noise cut away (a little always, most of it when bare)
hn = NOISE(nt, pos, 9, 3, .7); thr = M(nt, "SUBTRACT", .62, M(nt, "MULTIPLY", bare, float(arg("--barek", ".5")))); hole = SMOOTH(nt, hn, M(nt, "SUBTRACT", thr, .02), M(nt, "ADD", thr, .02))
twig = N(nt, "ShaderNodeBsdfPrincipled"); twig.inputs["Base Color"].default_value = (.08, .06, .04, 1); twig.inputs["Roughness"].default_value = .9
m2 = N(nt, "ShaderNodeMixShader"); L(nt, SMOOTH(nt, bare, .4, .9), m2.inputs[0]); L(nt, mx.outputs[0], m2.inputs[1]); L(nt, twig.outputs[0], m2.inputs[2])
tp = N(nt, "ShaderNodeBsdfTransparent"); m3 = N(nt, "ShaderNodeMixShader"); L(nt, hole, m3.inputs[0]); L(nt, m2.outputs[0], m3.inputs[1]); L(nt, tp.outputs[0], m3.inputs[2])
finish(nt, m3.outputs[0])
can.surface_render_method = "DITHERED"

bark, nt = mat("Bark")
tc = N(nt, "ShaderNodeTexCoord"); pos = tc.outputs["Object"]
bn = NOISE(nt, pos, 14, 4, .7); col = RAMP(nt, bn, [(0, (.05, .035, .025)), (1, (.16, .12, .09))])
bmp = N(nt, "ShaderNodeBump"); bmp.inputs["Strength"].default_value = .6; bmp.inputs["Distance"].default_value = .02; L(nt, bn, bmp.inputs["Height"])
finish(nt, principled(nt, col, .9, .2, bmp.outputs[0]).outputs[0])

# concrete (overpass): spalling flakes reveal darker interior + rust streaks; carbonation grime
con, nt = mat("Concrete")
tc = N(nt, "ShaderNodeTexCoord"); pos = tc.outputs["Object"]
spall = val_node(nt, "spall", "spall"); rust = val_node(nt, "rust", "rust")
cn = NOISE(nt, pos, 6, 4, .6); col = RAMP(nt, cn, [(0, (.3, .3, .29)), (1, (.5, .5, .48))])
grime = NOISE(nt, pos, .6, 3); col = MIXC(nt, M(nt, "MULTIPLY", SMOOTH(nt, grime, .4, .8), M(nt, "ADD", .3, M(nt, "MULTIPLY", rust, .7))), col, (.12, .12, .11))
vv = VORO(nt, pos, 1.3, "F1"); cellr = vv.outputs["Distance"]
vn = NOISE(nt, pos, 1.1, 2)
flake = SMOOTH(nt, vn, M(nt, "SUBTRACT", 1.05, M(nt, "MULTIPLY", spall, .75)), M(nt, "SUBTRACT", 1.1, M(nt, "MULTIPLY", spall, .75)))
flake = M(nt, "MULTIPLY", flake, SMOOTH(nt, NOISE(nt, pos, 4.5, 3, .6), .42, .55))
inner = RAMP(nt, NOISE(nt, pos, 20, 3), [(0, (.12, .11, .1)), (1, (.25, .23, .2))])
streak = M(nt, "MULTIPLY", SMOOTH(nt, NOISE(nt, pos, 2.5, 3), .45, .75), spall)
col = MIXC(nt, flake, col, inner); col = MIXC(nt, M(nt, "MULTIPLY", streak, .8), col, (.3, .12, .04))
bmp = N(nt, "ShaderNodeBump"); bmp.inputs["Strength"].default_value = .5; bmp.inputs["Distance"].default_value = .04
L(nt, M(nt, "SUBTRACT", M(nt, "MULTIPLY", cn, .2), flake), bmp.inputs["Height"])
finish(nt, principled(nt, col, .85, .3, bmp.outputs[0]).outputs[0])

rebarm, nt = mat("Rebar")
tc = N(nt, "ShaderNodeTexCoord"); col = RAMP(nt, NOISE(nt, tc.outputs["Object"], 30, 3), [(0, (.18, .06, .02)), (1, (.4, .15, .05))])
finish(nt, principled(nt, col, .9, .3).outputs[0])

# galvanised steel posts -> rust; green sign face with fading
steel, nt = mat("Steel")
tc = N(nt, "ShaderNodeTexCoord"); pos = tc.outputs["Object"]; sxyz = N(nt, "ShaderNodeSeparateXYZ"); L(nt, pos, sxyz.inputs[0])
rust = val_node(nt, "rust", "rust")
rn = NOISE(nt, pos, 8, 4, .65)
# rust climbs from the ground (z small) first
rz = SMOOTH(nt, sxyz.outputs["Z"], M(nt, "MULTIPLY", rust, 6.0), M(nt, "MULTIPLY", rust, 1.5))
rf = SMOOTH(nt, M(nt, "ADD", M(nt, "MULTIPLY", rust, .8), M(nt, "MULTIPLY", rn, .6)), .55, .95); rf = M(nt, "MAXIMUM", M(nt, "MULTIPLY", rf, rust), M(nt, "MULTIPLY", rz, SMOOTH(nt, rn, .3, .5)))
rcol = RAMP(nt, rn, [(0, (.2, .07, .02)), (1, (.45, .2, .06))])
col = MIXC(nt, rf, (.55, .56, .55), rcol); rough = MIXF(nt, rf, .35, .9); met = MIXF(nt, rf, .9, .0)
b = principled(nt, col, rough, .5); L(nt, met, b.inputs["Metallic"])
finish(nt, b.outputs[0])

signm, nt = mat("SignFace")
tc = N(nt, "ShaderNodeTexCoord"); pos = tc.outputs["Object"]
rust = val_node(nt, "rust", "rust")
sn = NOISE(nt, pos, 3, 3)
col = MIXC(nt, M(nt, "MULTIPLY", rust, .7), (.0, .22, .08), (.18, .26, .18))
col = MIXC(nt, M(nt, "MULTIPLY", SMOOTH(nt, sn, .5, .8), rust), col, (.3, .14, .05))
b = principled(nt, col, MIXF(nt, rust, .35, .8), .5); finish(nt, b.outputs[0])
white, nt = mat("SignWhite"); rust = val_node(nt, "rust", "rust")
col = MIXC(nt, M(nt, "MULTIPLY", rust, .6), (.85, .85, .85), (.55, .5, .42)); finish(nt, principled(nt, col, .4, .5).outputs[0])
grate, nt = mat("Grate"); rust = val_node(nt, "rust", "rust")
col = MIXC(nt, M(nt, "MULTIPLY", rust, .8), (.12, .12, .12), (.3, .12, .04)); finish(nt, principled(nt, col, .7, .4, metallic=.3).outputs[0])
pile, nt = mat("LeafPile")
tc = N(nt, "ShaderNodeTexCoord"); pos = tc.outputs["Object"]; snow = val_node(nt, "snow", "snow"); leaves_p = val_node(nt, "leaves", "leaves")
vc = VORO(nt, pos, 35, "F1"); col = RAMP(nt, NOISE(nt, pos, 30, 2), [(0, (.33, .1, .025)), (.5, (.38, .2, .05)), (1, (.14, .06, .02))])
col = MIXC(nt, SMOOTH(nt, leaves_p, .6, .3), col, (.11, .08, .045)); col = MIXC(nt, M(nt, "MULTIPLY", snow, .8), col, (.85, .87, .9))
bmp = N(nt, "ShaderNodeBump"); bmp.inputs["Strength"].default_value = .8; bmp.inputs["Distance"].default_value = .02; L(nt, vc.outputs["Distance"], bmp.inputs["Height"])
finish(nt, principled(nt, col, .85, .2, bmp.outputs[0]).outputs[0])
dirtm, nt = mat("Dirt"); tc = N(nt, "ShaderNodeTexCoord")
finish(nt, principled(nt, RAMP(nt, NOISE(nt, tc.outputs["Object"], 20, 3), [(0, (.07, .05, .03)), (1, (.15, .11, .07))]), .9, .2).outputs[0])
black, nt = mat("Hole"); finish(nt, principled(nt, (.005, .004, .003), 1.0, 0).outputs[0])

# ---------------------------------------------------------------- world: Nishita sky + sun, overcast mix for winter
w = bpy.data.worlds.new("Sky"); sc.world = w; wn = w.node_tree; wn.nodes.clear()
sky = wn.nodes.new("ShaderNodeTexSky"); sky.sky_type = "MULTIPLE_SCATTERING"; sky.altitude = 250; sky.air_density = 1.0; sky.sun_size = math.radians(.6)
bg = wn.nodes.new("ShaderNodeBackground"); bg.inputs["Strength"].default_value = 1.0
ovc = wn.nodes.new("ShaderNodeValue"); ovc.name = "overcast"
grey = wn.nodes.new("ShaderNodeRGB"); grey.outputs[0].default_value = (5.5, 5.8, 6.4, 1)      # overcast: bright flat sky in the sky texture's units
mx = wn.nodes.new("ShaderNodeMix"); mx.data_type = "RGBA"; mx.clamp_factor = True
wn.links.new(ovc.outputs[0], mx.inputs["Factor"]); wn.links.new(sky.outputs[0], mx.inputs[6]); wn.links.new(grey.outputs[0], mx.inputs[7])
wo = wn.nodes.new("ShaderNodeOutputWorld"); wn.links.new(mx.outputs[2], bg.inputs[0]); wn.links.new(bg.outputs[0], wo.inputs["Surface"])
def apply_sky(x):
    el, rot, st, oc = x
    sky.sun_elevation = math.radians(el); sky.sun_rotation = math.radians(rot); sky.sun_intensity = st
    sky.keyframe_insert("sun_elevation", frame=sc.frame_current); sky.keyframe_insert("sun_rotation", frame=sc.frame_current); sky.keyframe_insert("sun_intensity", frame=sc.frame_current)
    ovc.outputs[0].default_value = oc; ovc.outputs[0].keyframe_insert("default_value", frame=sc.frame_current)
reg(lambda s: (pv("sun_el", s), pv("sun_rot", s), pv("sun_str", s), pv("overcast", s)), apply_sky)
# a sun lamp matching the sky (Nishita's own sun lights the scene; the lamp adds crisp shadows and is dimmed when overcast)
bpy.ops.object.light_add(type="SUN"); sun = bpy.context.object; sun.name = "Sun"; sun.data.angle = math.radians(1.0)
def apply_sun(x):
    el, rot, st, oc = x
    d = Vector((math.cos(math.radians(el)) * math.sin(math.radians(rot)), math.cos(math.radians(el)) * -math.cos(math.radians(rot)), math.sin(math.radians(el))))
    sun.rotation_euler = (-d).to_track_quat("-Z", "Y").to_euler(); sun.keyframe_insert("rotation_euler", frame=sc.frame_current)
    sun.data.energy = 1.0 * st * (1 - .85 * oc); sun.data.keyframe_insert("energy", frame=sc.frame_current)
    sun.data.color = (1, .97 - .1 * (1 - el / 60), .92 - .25 * (1 - el / 60)); sun.data.keyframe_insert("color", frame=sc.frame_current)
reg(lambda s: (pv("sun_el", s), pv("sun_rot", s), pv("sun_str", s), pv("overcast", s)), apply_sun)

# ---------------------------------------------------------------- ground (flat corridor, ditches, rolling land beyond)
def gz(x, y):
    a = abs(y)
    z = 0.0
    if a < PIN: z = -.5 * (1 - (a / PIN) ** 2)                       # median swale
    elif a < POUT: z = -.35 * min(1.0, (a - PIN) / .4, (POUT - a) / .4)   # under the pavement: well below the road slab
    elif a < 28: z = -.75 * math.sin(math.pi * (a - POUT) / 8)       # ditch, bottom at |y| = 24
    else: z = 0.0
    far = min(1, max(0, (a - 27) / 25))
    z += far * (0.9 * noise.noise(Vector((x * .013, y * .013, 0))) + 0.25 * noise.noise(Vector((x * .07, y * .07, 1))))
    if a < 28 and a > 20: z += .04 * noise.noise(Vector((x * .5, y * .5, 2)))
    return z
ground = grid("Ground", X0 - 300, X1 + 300, -280, 280, 2.5, grd, gz)
# a finer strip for the shoulders/ditches/median that the cameras see up close
for o in [ground]: o.data.materials[0] = grd
near = grid("GroundNear", X0, X1, -35, 35, .5, grd, gz); near.location.z = .01
sc.frame_set(1)

# ---------------------------------------------------------------- the road: two carriageways with shape keys (potholes, heave)
def road_half(sign):
    y0, y1 = (PIN, POUT) if sign > 0 else (-POUT, -PIN)
    o = grid("Road%s" % ("N" if sign > 0 else "S"), X0, X1, y0, y1, .5, asph, lambda x, y: .02)
    o.shape_key_add(name="Basis")
    kp = o.shape_key_add(name="pot"); kh = o.shape_key_add(name="heave"); kw = o.shape_key_add(name="puddle")
    for i, v in enumerate(o.data.vertices):
        x, y = v.co.x, v.co.y; dz = 0.0; dw = 0.0
        for (px, py, r, dep) in POTS:
            d = math.hypot(x - px, y - py)
            if d < r: dz -= dep * (1 - (d / r) ** 2) ** .6
        for (px, py, r, dep) in PUDDLES:
            d = math.hypot(x - px, y - py)
            if d < r: dw -= dep * (1 - (d / r) ** 2)
        kp.data[i].co.z = v.co.z + dz
        kw.data[i].co.z = v.co.z + dw
        # heave: slabs tilt + large waves; roots along the edges lift them
        hv = .16 * noise.noise(Vector((x * .04, y * .08, 3))) + .06 * noise.noise(Vector((x * .25, y * .25, 4)))
        ed = max(0, (abs(y) - 16.5) / 3.5) ** 2
        hv += .25 * ed * (.5 + .5 * noise.noise(Vector((x * .3, 0, 5))))
        kh.data[i].co.z = v.co.z + hv
    for nm, pn in (("pot", "pothole"), ("heave", "heave"), ("puddle", "water")):
        k = o.data.shape_keys.key_blocks[nm]
        def apply(x, k=k): k.value = x; k.keyframe_insert("value", frame=sc.frame_current)
        reg(lambda s, pn=pn: min(1.0, pv(pn, s)), apply)
    return o
roadN = road_half(1); roadS = road_half(-1)

# ---------------------------------------------------------------- grass / leaves / saplings with geometry nodes
def blade_clump():
    verts = []; faces = []
    for k in range(9):
        a = random.uniform(0, 2 * math.pi); r0 = random.uniform(0, .07); lean = random.uniform(.15, .55); h = random.uniform(.6, 1.0); w = .012
        cx, cy = r0 * math.cos(a), r0 * math.sin(a); dx, dy = math.cos(a) * lean, math.sin(a) * lean
        base = len(verts)
        for j in range(4):
            u = j / 3; ww = w * (1 - u * .85)
            px, py, pz = cx + dx * u * u * h, cy + dy * u * u * h, u * h
            verts += [(px - ww * math.sin(a), py + ww * math.cos(a), pz), (px + ww * math.sin(a), py - ww * math.cos(a), pz)]
        for j in range(3):
            b_ = base + j * 2; faces.append((b_, b_ + 1, b_ + 3, b_ + 2))
    return mesh_obj("Clump", verts, faces, gra)
clump = blade_clump(); clump.hide_render = True; clump.hide_viewport = True
leaf = mesh_obj("LeafQuad", [(-.03, -.025, 0), (.03, -.025, 0), (.038, .025, .006), (-.038, .025, .006), (0, .045, .012)], [(0, 1, 2, 4, 3)], lef)
leaf.hide_render = True; leaf.hide_viewport = True

def tree(name, h, spread, trunk_r, n_can):
    """a blob tree: tapered trunk, a few branches, displaced spheres for the canopy; height h in metres (unit tree = 1 m tall)"""
    parts = []
    t = cyl(name + "_trunk", (0, 0, 0), trunk_r, h * .55, bark, 10, trunk_r * .45); parts.append(t)
    for k in range(3):
        a = k * 2.1 + random.uniform(-.4, .4); bl = h * random.uniform(.25, .4)
        br = cyl(name + "_br%d" % k, (0, 0, 0), trunk_r * .4, bl, bark, 8, trunk_r * .12)
        br.rotation_euler = (math.radians(random.uniform(35, 55)), 0, a); br.location = (0, 0, h * random.uniform(.35, .5))
        parts.append(br)
    for k in range(n_can):
        a = k * 2 * math.pi / n_can + random.uniform(-.5, .5); rr = spread * random.uniform(.25, .55) if k else 0
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=3, radius=spread * random.uniform(.4, .55) * (1.2 if k == 0 else 1), location=(rr * math.cos(a), rr * math.sin(a), h * random.uniform(.58, .88) if k else h * .72))
        c = bpy.context.object; c.name = name + "_c%d" % k; c.data.materials.append(can); c.scale.z = random.uniform(.7, .95)
        tx = bpy.data.textures.new(name + "_t%d" % k, "CLOUDS"); tx.noise_scale = spread * .35; tx.noise_depth = 3
        dm = c.modifiers.new("D", "DISPLACE"); dm.texture = tx; dm.strength = spread * .5; dm.mid_level = .5
        bpy.ops.object.shade_smooth(); parts.append(c)
    for p in parts[1:]: p.parent = parts[0]
    return parts[0]
trees_col = bpy.data.collections.new("TreeKinds")   # not linked to the scene: only instanced; one child collection per kind
KINDS = []; KCOL = []
for i, (h, sp, tr, n) in enumerate([(1.0, .6, .035, 6), (1.0, .48, .03, 5), (1.0, .75, .045, 7)]):
    t = tree("Kind%d" % i, h, sp, tr, n); KINDS.append(t)
    c = bpy.data.collections.new("Kind%dCol" % i); trees_col.children.link(c); KCOL.append(c)
    for o in [t] + list(t.children_recursive):
        for cc in list(o.users_collection): cc.objects.unlink(o)
        c.objects.link(o)

def gn_tree(name):
    ng = bpy.data.node_groups.new(name, "GeometryNodeTree")
    ng.interface.new_socket("Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
    ng.interface.new_socket("Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    gi = ng.nodes.new("NodeGroupInput"); go = ng.nodes.new("NodeGroupOutput")
    return ng, gi, go
def gn_in(ng, name, default, mn=0.0, mx=100.0):
    s = ng.interface.new_socket(name, in_out="INPUT", socket_type="NodeSocketFloat"); s.default_value = default; s.min_value = mn; s.max_value = mx
    return s.identifier
def gmath(ng, op, a, b=None, c=None):
    n = ng.nodes.new("ShaderNodeMath"); n.operation = op
    for i, x in enumerate((a, b, c)):
        if x is None: continue
        if hasattr(x, "is_linked"): ng.links.new(x, n.inputs[i])
        else: n.inputs[i].default_value = x
    return n.outputs[0]
def gsmooth(ng, x, a, b):
    n = ng.nodes.new("ShaderNodeMapRange"); n.interpolation_type = "SMOOTHSTEP"
    for sock, v in ((n.inputs["From Min"], a), (n.inputs["From Max"], b)):
        if hasattr(v, "is_linked"): ng.links.new(v, sock)
        else: sock.default_value = v
    ng.links.new(x, n.inputs["Value"]); return n.outputs[0]
def gnoise(ng, scale, detail=2):
    n = ng.nodes.new("ShaderNodeTexNoise"); n.inputs["Scale"].default_value = scale; n.inputs["Detail"].default_value = detail; return n.outputs["Fac"]
def grandom(ng, lo, hi, seed=0):
    r = ng.nodes.new("FunctionNodeRandomValue"); r.data_type = "FLOAT"; r.inputs[2].default_value = lo; r.inputs[3].default_value = hi; r.inputs[8].default_value = seed
    return r.outputs[1]

def scatter(obj, name, inst_obj=None, inst_col=None, density_fn=None, scale_lo=.7, scale_hi=1.3, seed=1, dist_min=0.0, align=True, attr=None, scale_id="Scale", dens_id="Density"):
    ng, gi, go = gn_tree(name)
    s_dens = gn_in(ng, "Density", 1.0); s_scale = gn_in(ng, "Scale", 1.0)
    extra = {}
    pos = ng.nodes.new("GeometryNodeInputPosition"); sx = ng.nodes.new("ShaderNodeSeparateXYZ"); ng.links.new(pos.outputs[0], sx.inputs[0])
    ay = gmath(ng, "ABSOLUTE", sx.outputs["Y"])
    mask = density_fn(ng, gi, sx.outputs["X"], ay, extra) if density_fn else 1.0
    dist = ng.nodes.new("GeometryNodeDistributePointsOnFaces"); dist.distribute_method = "RANDOM"; dist.inputs["Seed"].default_value = seed
    ng.links.new(gi.outputs["Geometry"], dist.inputs["Mesh"])
    ng.links.new(gmath(ng, "MULTIPLY", gi.outputs[s_dens], mask), dist.inputs["Density"])
    iop = ng.nodes.new("GeometryNodeInstanceOnPoints"); ng.links.new(dist.outputs["Points"], iop.inputs["Points"])
    if inst_obj:
        oi = ng.nodes.new("GeometryNodeObjectInfo"); oi.inputs["Object"].default_value = inst_obj; oi.transform_space = "RELATIVE"
        ng.links.new(oi.outputs["Geometry"], iop.inputs["Instance"])
    else:
        ci = ng.nodes.new("GeometryNodeCollectionInfo"); ci.inputs["Collection"].default_value = inst_col; ci.inputs["Separate Children"].default_value = True; ci.inputs["Reset Children"].default_value = True
        ng.links.new(ci.outputs[0], iop.inputs["Instance"]); iop.inputs["Pick Instance"].default_value = True
        ri = ng.nodes.new("FunctionNodeRandomValue"); ri.data_type = "INT"; ri.inputs[4].default_value = 0; ri.inputs[5].default_value = 2; ri.inputs[8].default_value = seed + 3
        ng.links.new(ri.outputs[2], iop.inputs["Instance Index"])
    rot = ng.nodes.new("FunctionNodeRandomValue"); rot.data_type = "FLOAT_VECTOR"; rot.inputs[0].default_value = (0, 0, 0); rot.inputs[1].default_value = (0, 0, 6.283); rot.inputs[8].default_value = seed + 1
    ng.links.new(rot.outputs[0], iop.inputs["Rotation"])
    sv = grandom(ng, scale_lo, scale_hi, seed + 2)
    scl = gmath(ng, "MULTIPLY", sv, gi.outputs[s_scale])
    if "scale_mask" in extra: scl = gmath(ng, "MULTIPLY", scl, extra["scale_mask"])
    ng.links.new(scl, iop.inputs["Scale"])
    last = iop.outputs[0]
    if attr:
        st = ng.nodes.new("GeometryNodeStoreNamedAttribute"); st.data_type = "FLOAT"; st.domain = "INSTANCE"; st.inputs["Name"].default_value = attr
        ng.links.new(last, st.inputs["Geometry"]); ng.links.new(grandom(ng, 0, 1, seed + 7), st.inputs["Value"]); last = st.outputs[0]
    jn = ng.nodes.new("GeometryNodeJoinGeometry"); ng.links.new(gi.outputs["Geometry"], jn.inputs[0]); ng.links.new(last, jn.inputs[0])
    ng.links.new(jn.outputs[0], go.inputs["Geometry"])
    md = obj.modifiers.new(name, "NODES"); md.node_group = ng
    return md, s_dens, s_scale

def key_mod(md, ident, pname, scale=1.0, fn=None):
    def apply(x, md=md, ident=ident): md[ident] = float(x); md.keyframe_insert('["%s"]' % ident, frame=sc.frame_current)
    reg((lambda s: fn(s)) if fn else (lambda s: pv(pname, s) * scale), apply)

# shoulder / median grass on the near ground: everywhere off the pavement, thinning out past |y|=40
def grass_mask(ng, gi, x, ay, extra):
    off = gmath(ng, "ADD", gsmooth(ng, ay, PIN + .1, PIN - .3), gsmooth(ng, ay, POUT - .1, POUT + .3))
    far = gsmooth(ng, ay, 42, 34)
    return gmath(ng, "MULTIPLY", gmath(ng, "MULTIPLY", off, far), gmath(ng, "ADD", .6, gmath(ng, "MULTIPLY", gnoise(ng, .3), .8)))
md, d_id, s_id = scatter(near, "GrassNear", inst_obj=clump, density_fn=grass_mask, seed=1)
md[d_id] = 13.0; key_mod(md, s_id, "grass_h")
# the same on the far ground, sparse, so the field edge does not read as a line
def far_mask(ng, gi, x, ay, extra): return gmath(ng, "MULTIPLY", gsmooth(ng, ay, 33, 36), gsmooth(ng, ay, 110, 70))
md, d_id, s_id = scatter(ground, "GrassFar", inst_obj=clump, density_fn=far_mask, seed=5, scale_lo=1.2, scale_hi=2.0)
md[d_id] = 2.0; key_mod(md, s_id, "grass_h")
# grass creeping onto the pavement from both edges + weeds in the cracks (noise-patchy)
def road_grass(ng, gi, x, ay, extra):
    enc = gn_in(ng, "Encroach", 0.0); weed = gn_in(ng, "Weeds", 0.0)
    e = gi.outputs[enc]
    edge = gmath(ng, "ADD", gsmooth(ng, gmath(ng, "SUBTRACT", POUT, ay), gmath(ng, "ADD", e, .3), gmath(ng, "SUBTRACT", e, .6)),
                             gsmooth(ng, gmath(ng, "SUBTRACT", ay, PIN), gmath(ng, "ADD", e, .3), gmath(ng, "SUBTRACT", e, .6)))
    wn_ = gnoise(ng, .25, 2); wn2 = gnoise(ng, 3, 2)
    w = gmath(ng, "MULTIPLY", gi.outputs[weed], gsmooth(ng, gmath(ng, "ADD", wn_, gmath(ng, "MULTIPLY", wn2, .35)), gmath(ng, "SUBTRACT", 1.0, gmath(ng, "MULTIPLY", gi.outputs[weed], .55)), gmath(ng, "SUBTRACT", 1.15, gmath(ng, "MULTIPLY", gi.outputs[weed], .55))))
    extra["enc"] = enc; extra["weed"] = weed
    return gmath(ng, "MINIMUM", 1.0, gmath(ng, "ADD", edge, w))
for rd in (roadN, roadS):
    md, d_id, s_id = scatter(rd, "RoadGrass", inst_obj=clump, density_fn=road_grass, seed=11 if rd is roadN else 12)
    md[d_id] = 8.0; key_mod(md, s_id, "grass_h"); key_mod(md, md.node_group.interface.items_tree["Encroach"].identifier, "encroach"); key_mod(md, md.node_group.interface.items_tree["Weeds"].identifier, "weeds")
# leaf litter on the pavement: wind-piled toward the outer edge and the median swale; thick around the drain
def leaf_mask(ng, gi, x, ay, extra):
    pileedge = gmath(ng, "ADD", .25, gmath(ng, "MULTIPLY", gsmooth(ng, ay, 14, 19.5), 1.0))
    inner = gmath(ng, "MULTIPLY", gsmooth(ng, ay, 8, 5.2), .8)
    wind = gmath(ng, "ADD", .3, gmath(ng, "MULTIPLY", gnoise(ng, .15, 2), 1.2))
    dx = gmath(ng, "SUBTRACT", x, DRAINX); dr = gmath(ng, "SQRT", gmath(ng, "ADD", gmath(ng, "MULTIPLY", dx, dx), gmath(ng, "POWER", gmath(ng, "SUBTRACT", ay, abs(DRAINY)), 2)))
    drain = gmath(ng, "MULTIPLY", gsmooth(ng, dr, 3.0, .4), 5.0)
    return gmath(ng, "ADD", gmath(ng, "MULTIPLY", gmath(ng, "ADD", pileedge, inner), wind), drain)
for rd in (roadN, roadS):
    md, d_id, s_id = scatter(rd, "Leaves", inst_obj=leaf, density_fn=leaf_mask, seed=21 if rd is roadN else 22, scale_lo=.8, scale_hi=1.4, attr="lv")
    key_mod(md, d_id, "leaves", 22.0); md[s_id] = 1.0
md, d_id, s_id = scatter(near, "LeavesGround", inst_obj=leaf, density_fn=lambda ng, gi, x, ay, e: gmath(ng, "MULTIPLY", gsmooth(ng, ay, 36, 20), gmath(ng, "ADD", .2, gnoise(ng, .2))), seed=23, attr="lv")
key_mod(md, d_id, "leaves", 8.0); md[s_id] = 1.0
# saplings -> young forest on the pavement and the shoulders; density and height both grow with the stage
def sapl_mask(ng, gi, x, ay, extra):
    n_ = gnoise(ng, .06, 2); extra["scale_mask"] = gmath(ng, "ADD", .55, gmath(ng, "MULTIPLY", gnoise(ng, .09), .9))
    keep = gmath(ng, "MULTIPLY", gsmooth(ng, gmath(ng, "ABSOLUTE", gmath(ng, "SUBTRACT", x, 40.5)), 1.5, 4.0), 1.0)   # keep the hero pothole clear
    keep = gmath(ng, "MULTIPLY", keep, gsmooth(ng, gmath(ng, "ABSOLUTE", gmath(ng, "SUBTRACT", x, OVX - 9)), 5.0, 9.0))  # and the ground in front of the overpass camera
    return gmath(ng, "MULTIPLY", gmath(ng, "MULTIPLY", gsmooth(ng, n_, .35, .7), keep), gsmooth(ng, ay, 42, 36))
for ob, dens, sd in ((roadN, .012, 31), (roadS, .012, 32), (near, .02, 33)):
    md, d_id, s_id = scatter(ob, "Saplings", inst_col=trees_col, density_fn=sapl_mask, seed=sd, scale_lo=.6, scale_hi=1.4, dist_min=2.0)
    key_mod(md, d_id, "sapl_d", dens); key_mod(md, s_id, "sapl", fn=lambda s: .4 + 11.5 * pv("sapl", s) ** 1.3)

# ---------------------------------------------------------------- the tree lines (right of way edge), two ragged rows each side
def plant(name, x, y, h, kind):
    o = bpy.data.objects.new(name, None); o.instance_type = "COLLECTION"; o.instance_collection = KCOL[kind]
    o.location = (x, y, gz(x, y) - .05); o.rotation_euler = (math.radians(random.uniform(-4, 4)), math.radians(random.uniform(-4, 4)), random.uniform(0, 6.28)); bpy.context.collection.objects.link(o)
    def apply(v, o=o, h=h): o.scale = (h * v, h * v, h * v); o.keyframe_insert("scale", frame=sc.frame_current)
    reg(lambda s: pv("grow", s), apply)
    return o
k = 0
for side in (1, -1):
    for row, (yb, gap) in enumerate(((36.0, 7.0), (44.0, 9.0))):
        x = X0 - 40 + random.uniform(0, 6)
        while x < X1 + 60:
            if not (OVX - 7 < x < OVX + 7 and row == 0):
                plant("T%d" % k, x, side * (yb + random.uniform(-2.5, 2.5)), random.uniform(6, 16) * (1.0 if row else .8), random.randrange(3)); k += 1
            x += gap * random.uniform(.6, 1.5)
# a far wood behind, big trees, sparse
for _ in range(140):
    x = random.uniform(X0 - 150, X1 + 150); y = random.choice([1, -1]) * random.uniform(55, 160)
    plant("W%d" % k, x, y, random.uniform(12, 20), random.randrange(3)); k += 1
print("trees", k)

# ---------------------------------------------------------------- the sign (ground-mounted, two posts, exit panel) - leans with stage
signE = bpy.data.objects.new("SignRoot", None); bpy.context.collection.objects.link(signE); signE.location = (SIGNX, SIGNY, gz(SIGNX, SIGNY))
for yy in (-1.6, 1.6):
    p = box("Post%g" % yy, (-.08, yy - .08, 0), (.08, yy + .08, 4.6), steel); p.parent = signE
face = box("SignFace", (-.03, -2.4, 2.2), (.03, 2.4, 4.6), signm, .01); face.parent = signE
rim = box("SignRim", (-.035, -2.42, 2.18), (-.031, 2.42, 4.62), white); rim.parent = signE
face2 = box("SignFaceIn", (-.038, -2.3, 2.3), (-.036, 2.3, 4.5), signm); face2.parent = signE
def text(name, s, loc, size, m, rot=(math.pi / 2, 0, -math.pi / 2)):
    bpy.ops.object.text_add(location=loc); t = bpy.context.object; t.name = name; t.data.body = s; t.data.size = size; t.data.extrude = .004
    t.data.align_x = "CENTER"; t.rotation_euler = rot; t.data.materials.append(m)
    try: t.data.font = bpy.data.fonts.load("C:/Windows/Fonts/arialbd.ttf")
    except Exception: pass
    return t
for i, (s, z, sz) in enumerate((("EXIT 27", 4.05, .42), ("Pike Road", 3.4, .5), ("1 MILE", 2.65, .42))):
    t = text("SignText%d" % i, s, (-.042, 0, z), sz, white); t.parent = signE
def apply_lean(v): signE.rotation_euler = (0, -math.radians(v), 0); signE.keyframe_insert("rotation_euler", frame=sc.frame_current)
reg(lambda s: pv("lean", s), apply_lean)

# ---------------------------------------------------------------- the storm-drain inlet at the shoulder edge + leaf pile + burrow
box("DrainBox", (DRAINX - .55, DRAINY - .4, -.3), (DRAINX + .55, DRAINY + .4, .03), con)
box("DrainWell", (DRAINX - .45, DRAINY - .3, -.6), (DRAINX + .45, DRAINY + .3, -.02), black)
for i in range(9):
    box("Bar%d" % i, (DRAINX - .47 + i * .115, DRAINY - .3, 0.0), (DRAINX - .47 + i * .115 + .03, DRAINY + .3, .04), grate)
for yy in (-.3, 0, .3): box("Bar_y%g" % yy, (DRAINX - .47, DRAINY + yy - .015, 0.0), (DRAINX + .47, DRAINY + yy + .015, .04), grate)
bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(DRAINX + .1, DRAINY - .1, 0), segments=24, ring_count=12); pileo = bpy.context.object; pileo.name = "LeafPile"
pileo.data.materials.append(pile); tx = bpy.data.textures.new("pile_t", "CLOUDS"); tx.noise_scale = .25
dm = pileo.modifiers.new("D", "DISPLACE"); dm.texture = tx; dm.strength = .25; bpy.ops.object.shade_smooth()
def apply_pile(v): pileo.scale = (1.0 * v + .001, .8 * v + .001, .2 * v + .001); pileo.keyframe_insert("scale", frame=sc.frame_current)
reg(lambda s: min(1.0, pv("leaves", s) * 1.1), apply_pile)
# groundhog burrow undercutting the shoulder edge: a dirt fan and a dark hole
bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(DRAINX + 6.5, POUT + .9, -.05), segments=20, ring_count=10); mound = bpy.context.object; mound.name = "BurrowMound"
mound.data.materials.append(dirtm); bpy.ops.object.shade_smooth()
hole = cyl("BurrowHole", (DRAINX + 6.5, POUT + .35, -.6), .16, .62, black, 14)
hole.rotation_euler = (math.radians(-35), 0, 0)
def apply_burrow(v):
    for o, s_ in ((mound, (1.1, .8, .18)), (hole, (1, 1, 1))):
        o.scale = tuple(x * v + .001 for x in s_); o.keyframe_insert("scale", frame=sc.frame_current)
reg(lambda s: pv("burrow", s), apply_burrow)

# ---------------------------------------------------------------- the overpass: deck, parapets, three bents, abutment slopes, rebar that shows when it spalls
DW = 8.0
deck = box("Deck", (OVX - DW / 2, -46, 5.3), (OVX + DW / 2, 46, 6.5), con, .05)
for sgn in (1, -1):
    box("Parapet%d" % sgn, (OVX + sgn * DW / 2 - (.35 if sgn > 0 else 0), -46, 6.5), (OVX + sgn * DW / 2 + (0 if sgn > 0 else .35), 46, 7.4), con, .03)
    box("Fascia%d" % sgn, (OVX + sgn * DW / 2 - (.12 if sgn > 0 else 0), -46, 4.9), (OVX + sgn * DW / 2 + (0 if sgn > 0 else .12), 46, 5.3), con)
for yc in (0.0, 23.5, -23.5):
    cap = box("Cap%g" % yc, (OVX - DW / 2 - .3, yc - 7.0, 4.6), (OVX + DW / 2 + .3, yc + 7.0, 5.3), con, .04)
    for yy in (-4.5, 4.5):
        cyl("Col%g_%g" % (yc, yy), (OVX, yc + yy, gz(OVX, yc + yy) - .3), .55, 4.9 - gz(OVX, yc + yy) + .3, con, 20)
for sgn in (1, -1):     # abutment: earth slope from the deck end down to the ground
    v = [(OVX - 12, sgn * 46, 0), (OVX + 12, sgn * 46, 0), (OVX + 12, sgn * 60, 5.2), (OVX - 12, sgn * 60, 5.2),
         (OVX - 12, sgn * 90, 5.2), (OVX + 12, sgn * 90, 5.2), (OVX + 30, sgn * 46, 0), (OVX - 30, sgn * 46, 0)]
    mesh_obj("Abut%d" % sgn, v, [(0, 1, 2, 3), (3, 2, 5, 4), (1, 6, 2), (0, 3, 7)], grd)
    box("AbutWall%d" % sgn, (OVX - DW / 2 - .3, sgn * 46 - (0 if sgn > 0 else 1.0), 0), (OVX + DW / 2 + .3, sgn * 46 + (1.0 if sgn > 0 else 0), 5.3), con)
    box("Approach%d" % sgn, (OVX - DW / 2, sgn * 46, 5.2), (OVX + DW / 2, sgn * 95, 5.3), asph)
# exposed rebar along the deck fascia + the cap beam above the lanes (hidden until the spalling is well along)
REBAR = []
for yy in [y_ for y_ in range(-18, 19, 1)]:
    for zz in (5.0, 5.15):
        r = cyl("Rebar%d_%g" % (yy, zz), (OVX - DW / 2 - .02, yy, zz), .012, .9, rebarm, 6, axis="x"); r.rotation_euler = (0, math.pi / 2, 0); r.location = (OVX - DW / 2 + .4, yy + .45, zz); REBAR.append(r)
for xx in range(int(OVX - DW / 2) + 1, int(OVX + DW / 2), 1):
    r = cyl("RebarT%d" % xx, (xx, -7.2, 4.62), .012, 14.4, rebarm, 6, axis="y"); REBAR.append(r)
def apply_rebar(v):
    for r in REBAR:
        r.hide_render = v < .5; r.keyframe_insert("hide_render", frame=sc.frame_current)
reg(lambda s: 1.0 if pv("spall", s) > .62 else 0.0, apply_rebar)
# a railing on the parapets
for sgn in (1, -1):
    for yy in range(-45, 46, 3):
        box("RailP%d_%d" % (sgn, yy), (OVX + sgn * DW / 2 - .1, yy - .04, 7.4), (OVX + sgn * DW / 2 + .1, yy + .04, 8.4), steel)
    box("Rail%d" % sgn, (OVX + sgn * DW / 2 - .04, -46, 8.3), (OVX + sgn * DW / 2 + .04, 46, 8.4), steel)
# mile marker + guardrail along the outer shoulder for scale
for xx in range(int(X0), int(X1), 4):
    box("GPost%d" % xx, (xx - .08, POUT + .9, -.3), (xx + .08, POUT + 1.06, .55), steel)
box("GRail", (X0, POUT + .98, .35), (X1, POUT + 1.06, .72), steel, .02)

# ---------------------------------------------------------------- cameras and the stage keys per shot
bpy.ops.object.camera_add(); cam = bpy.context.object; cam.name = "Cam"; sc.camera = cam; cam.rotation_mode = "QUATERNION"
cd = cam.data; cd.sensor_width = 36; cd.dof.use_dof = True; cd.dof.aperture_fstop = 5.6; cd.clip_end = 2000
def aim(p, t): return (Vector(t) - Vector(p)).to_track_quat("-Z", "Y")
CAMS = {   # name: (pos0, tgt0, pos1, tgt1, lens, fstop)
 "A": ((-12, 21.8, 2.3), (70, 9, 1.0), (-8, 21.2, 2.25), (70, 9, 1.0), 32, 8),
 "D": ((OVX, 11.5, 8.3), (30, 10, 0.0), (OVX, 11.0, 8.2), (28, 10.5, 0.0), 38, 8),
 "B": ((16.2, 16.6, 1.15), (DRAINX + .3, DRAINY + .1, .05), (16.8, 16.9, 1.1), (DRAINX + .3, DRAINY + .1, .05), 35, 4),
 "C": ((44, 17.2, 1.7), (SIGNX, SIGNY, 3.2), (46, 17.6, 1.7), (SIGNX, SIGNY, 3.2), 40, 5.6),
 "E": ((36.2, 14.6, .62), (41.0, 11.6, -.04), (36.6, 14.4, .6), (41.0, 11.6, -.04), 35, 2.8),
 "F": ((OVX - 14, 4.0, 1.5), (OVX - 3.5, -2.5, 5.3), (OVX - 13, 3.5, 1.5), (OVX - 3.5, -2.5, 5.3), 35, 5.6),
 "G": ((-12, 21.8, 2.3), (70, 9, 1.0), (4, 19.6, 2.1), (76, 9, 1.0), 32, 8),
}
STAGE_KEYS = []
f = 1
for sh in SHOTS:
    n = int(round(sh["dur"] * FPS)); fa, fb = f, f + n - 1
    if sh["cam"] is None:
        f = fb + 1; continue
    p0, t0, p1, t1, lens, fst = CAMS[sh["cam"]]
    for ff, p, t in ((fa, p0, t0), (fb, p1, t1)):
        sc.frame_set(ff); cam.location = p; cam.rotation_quaternion = aim(p, t)
        cam.keyframe_insert("location", frame=ff); cam.keyframe_insert("rotation_quaternion", frame=ff)
        cd.lens = lens; cd.keyframe_insert("lens", frame=ff); cd.dof.aperture_fstop = fst; cd.dof.keyframe_insert("aperture_fstop", frame=ff)
        cd.dof.focus_distance = (Vector(t) - Vector(p)).length; cd.dof.keyframe_insert("focus_distance", frame=ff)
    s0, s1 = sh["s0"], sh["s1"]
    steps = max(1, int(math.ceil(abs(s1 - s0) / 0.08)))
    for i in range(steps + 1):
        u = i / steps
        # ease the time-lapse a little so stages linger at both ends
        ue = u * u * (3 - 2 * u) if s0 != s1 else 0
        STAGE_KEYS.append((int(round(fa + (fb - fa) * u)), s0 + (s1 - s0) * ue))
    f = fb + 1
print("frames", DUR, "keys", len(STAGE_KEYS))
for fr, s in STAGE_KEYS:
    sc.frame_set(fr)
    for apply, fn in SETTERS: apply(fn(s))
# linear interpolation on every stage key, bezier eased camera within a shot, hard cuts between shots
cut = set()
f = 1
for sh in SHOTS:
    n = int(round(sh["dur"] * FPS)); cut.add(f + n - 1); f += n
def all_curves(idb):
    ad = idb.animation_data
    if not ad or not ad.action: return []
    cs = getattr(ad.action, "fcurves", None)
    if cs is not None: return list(cs)
    try: return [fc for layer in ad.action.layers for strip in layer.strips for bag in strip.channelbags for fc in bag.fcurves]
    except Exception: return []
ids = [o for o in bpy.data.objects] + list(bpy.data.materials) + list(bpy.data.node_groups) + [w, sun.data, cd] + [o.data.shape_keys for o in (roadN, roadS)] + list(bpy.data.worlds)
for idb in ids:
    for fc in all_curves(idb):
        for k in fc.keyframe_points:
            k.interpolation = "LINEAR"
for idb in (cam, cd):
    for fc in all_curves(idb):
        for k in fc.keyframe_points:
            k.interpolation = "CONSTANT" if int(k.co[0]) in cut else "BEZIER"; k.easing = "EASE_IN_OUT"

if "--debug" in argv:
    dg = bpy.context.evaluated_depsgraph_get()
    for fr in (1, 1740, 3300, 5700):
        sc.frame_set(fr); dg.update()
        kb = roadN.data.shape_keys.key_blocks
        ev = roadN.evaluated_get(dg); me = ev.to_mesh() if hasattr(ev, "to_mesh") else None
        zs = [v.co.z for v in me.vertices] if me else []
        print("DBG", fr, {k.name: round(k.value, 3) for k in kb}, "minz", round(min(zs), 3) if zs else None, "maxz", round(max(zs), 3) if zs else None, "nverts", len(zs))
        print("DBG mats", {m.name: {n.name: round(n.outputs[0].default_value, 3) for n in m.node_tree.nodes if n.type == "VALUE"} for m in (asph,)})
# ---------------------------------------------------------------- outputs
if arg("--save"): bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(arg("--save")))
if arg("--still"):
    i = argv.index("--still"); fr = int(argv[i + 1]); outp = argv[i + 2]
    sc.frame_set(fr); sc.render.filepath = os.path.abspath(outp); bpy.ops.render.render(write_still=True); print("STILL", outp)
if arg("--stills"):
    outd = os.path.abspath(arg("--stills")); os.makedirs(outd, exist_ok=True)
    import time
    for fr in [int(x) for x in arg("--frames", "1").split(",")]:
        t0 = time.time(); sc.frame_set(fr); sc.render.filepath = os.path.join(outd, "t_%04d.png" % fr); bpy.ops.render.render(write_still=True); print("STILL", fr, "%.1fs" % (time.time() - t0), flush=True)
if arg("--anim"):
    outd = os.path.abspath(arg("--anim")); os.makedirs(outd, exist_ok=True)
    f0, f1 = int(arg("--start", sc.frame_start)), int(arg("--end", sc.frame_end))
    import time
    skip = set(); ff_ = 1
    for sh in SHOTS:
        n_ = int(round(sh["dur"] * FPS))
        if sh["cam"] is None: skip.update(range(ff_, ff_ + n_))
        ff_ += n_
    for fr in range(f0, f1 + 1, int(arg("--step", "1"))):
        p = os.path.join(outd, "f_%04d.png" % fr)
        if fr in skip or (os.path.exists(p) and os.path.getsize(p) > 1000): continue
        t0 = time.time(); sc.frame_set(fr); sc.render.filepath = p; bpy.ops.render.render(write_still=True)
        print("FRAME %d %.1fs" % (fr, time.time() - t0), flush=True)
