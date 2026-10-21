# Heartbeat TV Science 8.5 "How a commercial roof dies" - one Indiana warehouse, two roofs side by side, the same camera
# positions as the years pass.  Pure-script Blender 5.1 scene (no downloaded assets).
#   Section A (x<0): an older pre-engineered metal building, gable 1:12, exposed-fastener steel panels (real rib geometry),
#                    ~2,700 screws instanced with geometry nodes (they back out, rust, get replaced + encapsulated, get coated).
#   Section B (x>0): a flat addition, white single-ply membrane (seams, dirt, chalking, algae in the ponds), rooftop units on
#                    curbs, two drains with dome strainers, pipe boots, a gas line on sleepers, walkway pads, a hatch, parapet,
#                    scuppers, the wall flashing where it meets the metal gable end.
#   Plus a small warehouse interior under the deck for the leak shot.
# One number STAGE (0 new .. 1 years 1-5 .. 2 years 5-15 .. 3 the leak .. 3.3-4.6 restoration steps .. 5 coated) is keyed
# per shot; every material / modifier / object reads it through the param table P.
# Cycles OptiX on the RTX 4060 (one GPU job at a time).
#   blender -b -P build.py -- [--still FRAME out.png] [--stills DIR --frames a,b,c] [--anim OUTDIR [--start F --end F]]
#                             [--samples N] [--cpu] [--save out.blend]
import bpy, bmesh, math, random, sys, os
from mathutils import Vector, noise

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from shots import SHOTS, FPS
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def arg(k, d=None): return argv[argv.index(k) + 1] if k in argv else d
random.seed(7)

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
sc.cycles.max_bounces = 4; sc.cycles.diffuse_bounces = 2; sc.cycles.glossy_bounces = 3; sc.cycles.transmission_bounces = 2; sc.cycles.volume_bounces = 0
sc.cycles.transparent_max_bounces = 16
sc.cycles.caustics_reflective = False; sc.cycles.caustics_refractive = False
sc.cycles.blur_glossy = 1.0; sc.cycles.sample_clamp_indirect = 6.0
sc.render.resolution_x, sc.render.resolution_y = int(arg("--w", "1280")), int(arg("--h", "720")); sc.render.resolution_percentage = 100
sc.render.use_motion_blur = False
sc.view_settings.view_transform = "AgX"
try: sc.view_settings.look = "AgX - Medium Contrast"
except Exception: pass
sc.view_settings.exposure = float(arg("--exp", "-3.9"))
sc.render.image_settings.file_format = "PNG"; sc.render.image_settings.color_mode = "RGB"

# ---------------------------------------------------------------- the stage parameter table (piecewise-linear in STAGE)
P = {
 "dirt":     [(0, 0), (1, .3), (2, .8), (3, .9), (3.3, .9), (3.9, 0), (5, 0)],          # dirt / soot; power wash at 3.3-3.9
 "chalk":    [(0, 0), (1, .35), (2, .85), (3, 1), (4.6, 1), (5, 0)],                    # membrane UV chalking (rougher, duller)
 "rust":     [(0, 0), (.5, 0), (1, .15), (2, .65), (3, 1), (5, 1)],                     # rust on screws / laps (stays under primer)
 "prime":    [(3.8, 0), (4.3, 1)],                                                      # rust-inhibiting primer over the rust
 "backout":  [(0, 0), (1, .15), (2, .75), (3, 1), (3.9, 1), (4.25, 0)],                 # screws stand proud, tilt; replaced at 3.9-4.25
 "encap":    [(4.3, 0), (4.6, 1)],                                                      # sealant blobs over every screw head
 "seamfab":  [(4.15, 0), (4.6, 1)],                                                     # fabric + sealant on laps / seams / curb
 "coat":     [(4.6, 0), (5, 1)],                                                        # the white fluid-applied coating
 "settle":   [(0, 0), (1, .35), (2, 1)],                                                # low spots deepen (deck deflection)
 "pond":     [(1.3, 0), (2, 1), (3, 1), (3.25, 0)],                                     # standing water in the low spots
 "clog":     [(1.4, 0), (2, 1), (3, 1), (3.5, 0)],                                      # debris on the drain strainer
 "algae":    [(1.6, 0), (2, .6), (3, 1), (3.6, 0)],                                     # dark growth in the pond footprints
 "fish":     [(1.9, 0), (2.4, 1), (3, 1), (3.6, 0)],                                    # seam fishmouths
 "punct":    [(2.0, 0), (2.3, 1), (3, 1), (3.6, 0)],                                    # punctures near the RTU
 "crack":    [(2.1, 0), (2.6, 1), (3, 1), (4.2, 0)],                                    # curb flashing cracks
 "stain":    [(2.4, 0), (3, 1)],                                                        # interior deck stain
 "wetpatch": [(2.5, 0), (3, 1), (3.25, 1), (3.5, 0)],                                   # damp-looking area over the wet insulation
 "patch":    [(3.35, 0), (3.6, 1)],                                                     # the cut-out + replaced section
 "wet":      [(2.4, 0), (2.7, 1), (3.05, 1), (3.3, 0)],                                 # surfaces wet after rain
 "overcast": [(2.4, 0), (2.7, 1), (3.05, 1), (3.3, 0)],
 "sun_el":   [(0, 38), (1, 44), (2, 36), (3, 30), (3.3, 42), (5, 40)],
 "sun_rot":  [(0, 300), (2, 290), (3, 285), (3.3, 300), (5, 305)],
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
    v = nt.nodes.new("ShaderNodeValue"); v.name = v.label = name
    def apply(x, v=v): v.outputs[0].default_value = x; v.outputs[0].keyframe_insert("default_value", frame=sc.frame_current)
    reg(lambda s: pv(pname, s) * scale + off, apply)
    return v.outputs[0]

# ---------------------------------------------------------------- node helpers (same as ep4)
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
def MIXF(nt, fac, a, b):
    n = nt.nodes.new("ShaderNodeMix"); n.data_type = "FLOAT"; n.clamp_factor = True
    for sock, x in ((n.inputs["Factor"], fac), (n.inputs[2], a), (n.inputs[3], b)):
        if lk(x): L(nt, x, sock)
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
def SMOOTH(nt, x, a, b):
    n = N(nt, "ShaderNodeMapRange"); n.interpolation_type = "SMOOTHSTEP"
    for sock, v in ((n.inputs["From Min"], a), (n.inputs["From Max"], b)):
        if lk(v): L(nt, v, sock)
        else: sock.default_value = v
    L(nt, x, n.inputs["Value"]); return n.outputs[0]
def finish(nt, shader):
    L(nt, shader, nt.nodes["OUT"].inputs["Surface"])
def principled(nt, color, rough, spec=.5, normal=None, metallic=0.0):
    b = N(nt, "ShaderNodeBsdfPrincipled"); b.inputs["Roughness"].default_value = rough if not lk(rough) else .5
    if lk(rough): L(nt, rough, b.inputs["Roughness"])
    if lk(color): L(nt, color, b.inputs["Base Color"])
    else: b.inputs["Base Color"].default_value = tuple(color) + (1,)
    b.inputs["Specular IOR Level"].default_value = spec
    if lk(metallic): L(nt, metallic, b.inputs["Metallic"])
    else: b.inputs["Metallic"].default_value = metallic
    if normal is not None: L(nt, normal, b.inputs["Normal"])
    return b
def coords(nt):
    tc = N(nt, "ShaderNodeTexCoord"); pos = tc.outputs["Object"]
    sx = N(nt, "ShaderNodeSeparateXYZ"); L(nt, pos, sx.inputs[0])
    return pos, sx.outputs["X"], sx.outputs["Y"], sx.outputs["Z"]
def BAND(nt, v, c, w, soft=.01):
    """1 within |v-c|<w, soft edge"""
    d = M(nt, "ABSOLUTE", M(nt, "SUBTRACT", v, c)); return SMOOTH(nt, d, M(nt, "ADD", w, soft) if lk(w) else w + soft, w)
def GRIDDIST(nt, X, Y, x0, y0, px, py):
    """distance to the nearest point of the grid (x0 + i*px, y0 + j*py)"""
    fx = M(nt, "SUBTRACT", M(nt, "MODULO", M(nt, "ADD", M(nt, "SUBTRACT", X, x0 - px / 2), 1000 * px), px), px / 2)
    fy = M(nt, "SUBTRACT", M(nt, "MODULO", M(nt, "ADD", M(nt, "SUBTRACT", Y, y0 - py / 2), 1000 * py), py), py / 2)
    return M(nt, "SQRT", M(nt, "ADD", M(nt, "MULTIPLY", fx, fx), M(nt, "MULTIPLY", fy, fy)))

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
def sphere(name, loc, r, m, seg=24, ring=12):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc, segments=seg, ring_count=ring); o = bpy.context.object; o.name = name
    o.data.materials.append(m); bpy.ops.object.shade_smooth(); return o

# ---------------------------------------------------------------- layout (metres)
MX0, MX1 = -42.0, 0.0        # metal building
FX0, FX1 = 0.0, 48.0         # flat addition
HW = 15.0                    # half width (y)
ZF = 6.0                     # top of the membrane
ZE = 7.0                     # metal eave; ridge at y=0
def zmetal(y): return ZE + (HW - abs(y)) / 12.0
ZR = zmetal(0)
PAR = .9                     # parapet height above the membrane
RIB = .3048                  # 12 in rib spacing; screws every 1.5 m (purlins) in the flat at x0 + .095
SX0, SY0, SPX, SPY = MX0 + .095, -14.25, RIB, 1.5
DRAINS = [(14.0, -4.0), (34.0, 5.0)]     # roof drains (sumps)
BIRD = (30.0, -7.0, 5.5, .05)            # the dead low spot: x, y, r, depth (birdbath, not at a drain)
RTUS = [((10.0, 6.0), (3.2, 2.0, 1.4)), ((36.0, -8.0), (2.4, 1.5, 1.2))]   # centre, (lx, ly, lz)
HATCH = (44.0, -11.0)
PIPES = [(20.0, 8.5), (20.6, 8.5), (21.4, 8.4)]
SEAMY0 = -HW + .4            # first seam; rolls 10 ft (3.048 m) wide, run along x; end lap at x=24.4 (an 80 ft roll)
ROLL = 3.048

# ---------------------------------------------------------------- materials
# metal roof panel: Galvalume (spangled mill finish), dulls; rust haloes at the screw grid + end laps + eave; primer; fabric; coating
met, nt = mat("MetalPanel")
pos, X, Y, Z = coords(nt)
rust = val_node(nt, "rust", "rust"); prime = val_node(nt, "prime", "prime"); dirt = val_node(nt, "dirt", "dirt")
seamfab = val_node(nt, "seamfab", "seamfab"); coat = val_node(nt, "coat", "coat"); wet = val_node(nt, "wet", "wet")
spang = VORO(nt, pos, 90, "F1", .9).outputs["Distance"]
base = RAMP(nt, spang, [(0, (.46, .47, .47)), (.5, (.55, .56, .56)), (1, (.42, .43, .43))])
ribx = M(nt, "MODULO", M(nt, "ADD", M(nt, "SUBTRACT", X, MX0), 1000 * RIB), RIB); ribm = M(nt, "MULTIPLY", SMOOTH(nt, ribx, .18, .215), SMOOTH(nt, ribx, .3, .265))
base = MIXC(nt, M(nt, "MULTIPLY", ribm, .35), base, (.3, .31, .32))
base = MIXC(nt, M(nt, "MULTIPLY", NOISE(nt, pos, .4, 3), M(nt, "MULTIPLY", dirt, .7)), base, (.3, .29, .27))
rn = NOISE(nt, pos, 6, 4, .65); rn2 = NOISE(nt, pos, 1.2, 2)
# per-screw variation: a noise sampled at the grid cell
gd = GRIDDIST(nt, X, Y, SX0, SY0, SPX, SPY)
halo = SMOOTH(nt, gd, M(nt, "ADD", .006, M(nt, "MULTIPLY", rust, .075)), M(nt, "ADD", .004, M(nt, "MULTIPLY", rust, .012)))
halo = M(nt, "MULTIPLY", halo, SMOOTH(nt, M(nt, "ADD", NOISE(nt, pos, 2.1, 1), M(nt, "MULTIPLY", rust, .35)), .45, .75))
lap = M(nt, "MULTIPLY", BAND(nt, M(nt, "ABSOLUTE", Y), 7.5, M(nt, "ADD", .02, M(nt, "MULTIPLY", rust, .22)), .05), SMOOTH(nt, M(nt, "ADD", rn2, M(nt, "MULTIPLY", rust, .5)), .55, .9))
eave = M(nt, "MULTIPLY", SMOOTH(nt, M(nt, "ABSOLUTE", Y), 14.55, 14.98), SMOOTH(nt, M(nt, "ADD", rn2, M(nt, "MULTIPLY", rust, .6)), .5, .9))
streak = M(nt, "MULTIPLY", SMOOTH(nt, NOISE(nt, pos, 3, 3, .7), .62, .8), M(nt, "MULTIPLY", SMOOTH(nt, rust, .5, 1), .5))
rf = M(nt, "MINIMUM", 1.0, M(nt, "ADD", M(nt, "ADD", halo, lap), M(nt, "ADD", eave, streak)))
rf = M(nt, "MULTIPLY", rf, SMOOTH(nt, rust, 0, .15))
rcol = RAMP(nt, rn, [(0, (.22, .07, .02)), (.6, (.4, .16, .05)), (1, (.55, .28, .1))])
col = MIXC(nt, rf, base, rcol); rough = MIXF(nt, rf, M(nt, "ADD", .3, M(nt, "MULTIPLY", dirt, .3)), .9); metal = MIXF(nt, rf, .85, 0.0)
# primer (grey) goes over the rusty spots
pcol = (.48, .5, .52); pf = M(nt, "MULTIPLY", SMOOTH(nt, rf, .15, .5), prime)
col = MIXC(nt, pf, col, pcol); rough = MIXF(nt, pf, rough, .6); metal = MIXF(nt, pf, metal, 0.0)
# fabric + sealant on the end laps and the eave (a whitish band with weave)
fb = M(nt, "MULTIPLY", seamfab, M(nt, "MAXIMUM", BAND(nt, M(nt, "ABSOLUTE", Y), 7.5, .09, .01), SMOOTH(nt, M(nt, "ABSOLUTE", Y), 14.8, 14.88)))
weave = NOISE(nt, pos, 120, 2); fcol = RAMP(nt, weave, [(0, (.78, .78, .76)), (1, (.86, .86, .84))])
col = MIXC(nt, fb, col, fcol); rough = MIXF(nt, fb, rough, .85); metal = MIXF(nt, fb, metal, 0.0)
# the coating: white silicone, slight sheen, a hint of roller texture
ccol = RAMP(nt, NOISE(nt, pos, 30, 2), [(0, (.84, .85, .83)), (1, (.9, .9, .88))]); ccol = MIXC(nt, M(nt, "MULTIPLY", ribm, .25), ccol, (.7, .7, .7))
col = MIXC(nt, coat, col, ccol); rough = MIXF(nt, coat, rough, .45); metal = MIXF(nt, coat, metal, 0.0)
rough = MIXF(nt, wet, rough, .12)
bmp = N(nt, "ShaderNodeBump"); bmp.inputs["Strength"].default_value = .25; bmp.inputs["Distance"].default_value = .004
L(nt, M(nt, "ADD", M(nt, "MULTIPLY", rf, -.6), M(nt, "MULTIPLY", fb, .4)), bmp.inputs["Height"])
finish(nt, principled(nt, col, rough, .5, bmp.outputs[0], metal).outputs[0])

# membrane: white, seams every 10 ft, dirt + chalk + algae + ponding rings + wet patch + punctures; patch; fabric; coating
mem, nt = mat("Membrane")
pos, X, Y, Z = coords(nt)
dirt = val_node(nt, "dirt", "dirt"); chalk = val_node(nt, "chalk", "chalk"); algae = val_node(nt, "algae", "algae")
pond = val_node(nt, "pond", "pond"); wetp = val_node(nt, "wetpatch", "wetpatch"); patch = val_node(nt, "patch", "patch")
seamfab = val_node(nt, "seamfab", "seamfab"); coat = val_node(nt, "coat", "coat"); wet = val_node(nt, "wet", "wet"); punct = val_node(nt, "punct", "punct")
fine = NOISE(nt, pos, 60, 2)
white = RAMP(nt, fine, [(0, (.78, .79, .77)), (1, (.86, .87, .85))])
# seams: a 38 mm weld band, slightly darker edge + tiny ridge; end lap at x = 24.4
sy = M(nt, "MODULO", M(nt, "ADD", M(nt, "SUBTRACT", Y, SEAMY0), 100 * ROLL), ROLL)
seam = SMOOTH(nt, sy, .048, .04); seam = M(nt, "MAXIMUM", seam, BAND(nt, X, 24.4, .045, .01))
seamedge = M(nt, "SUBTRACT", seam, SMOOTH(nt, sy, .04, .035))
col = MIXC(nt, M(nt, "MULTIPLY", seamedge, .85), white, (.5, .5, .48)); col = MIXC(nt, M(nt, "MULTIPLY", seam, .25), col, (.62, .62, .6))
# dirt: wind-streaked, heavier downwind (-x side) of the RTUs and at the parapet; chalk dulls everything
dn = NOISE(nt, pos, .35, 3, .6); dstreak = NOISE(nt, N(nt, "ShaderNodeMapping", inputs={"Scale": (1, 6, 1)}).outputs[0] if False else pos, 2.5, 2)
dm = SMOOTH(nt, M(nt, "ADD", dn, M(nt, "MULTIPLY", dstreak, .3)), M(nt, "SUBTRACT", 1.1, M(nt, "MULTIPLY", dirt, .9)), M(nt, "SUBTRACT", 1.35, M(nt, "MULTIPLY", dirt, .9)))
for (cx, cy), (lx, ly, lz) in RTUS:    # soot fans downwind of each unit
    dx = M(nt, "SUBTRACT", cx - lx / 2, X); dy = M(nt, "ABSOLUTE", M(nt, "SUBTRACT", Y, cy))
    fan = M(nt, "MULTIPLY", SMOOTH(nt, dx, -.5, 2.0), M(nt, "MULTIPLY", SMOOTH(nt, dx, 9, 3), SMOOTH(nt, dy, M(nt, "ADD", ly * .6, M(nt, "MULTIPLY", dx, .25)), ly * .3)))
    dm = M(nt, "MAXIMUM", dm, M(nt, "MULTIPLY", fan, M(nt, "MULTIPLY", dirt, .7)))
dcol = RAMP(nt, NOISE(nt, pos, 8, 3), [(0, (.3, .28, .25)), (1, (.5, .47, .42))])
col = MIXC(nt, dm, col, dcol)
col = MIXC(nt, M(nt, "MULTIPLY", chalk, .35), col, (.66, .66, .63))
# the ponds: algae where the surface dips (z below the membrane plane), a tide ring of dirt just above the water line
dip = M(nt, "SUBTRACT", ZF, Z)
inpond = SMOOTH(nt, dip, .006, .02)
acol = RAMP(nt, NOISE(nt, pos, 5, 3), [(0, (.12, .14, .08)), (1, (.28, .3, .16))])
col = MIXC(nt, M(nt, "MULTIPLY", inpond, algae), col, acol)
ring = M(nt, "MULTIPLY", SMOOTH(nt, dip, .0, .006), SMOOTH(nt, dip, .014, .008)); col = MIXC(nt, M(nt, "MULTIPLY", ring, M(nt, "MAXIMUM", dirt, algae)), col, (.36, .33, .26))
# the wet-insulation area near drain 1 (a dull damp blotch) and later the patch (new bright membrane, a visible square)
d1 = DRAINS[0]; wd = M(nt, "SQRT", M(nt, "ADD", M(nt, "POWER", M(nt, "SUBTRACT", X, d1[0] + 4.5), 2), M(nt, "POWER", M(nt, "SUBTRACT", Y, d1[1] + 1.0), 2)))
wblob = M(nt, "MULTIPLY", SMOOTH(nt, M(nt, "ADD", wd, M(nt, "MULTIPLY", NOISE(nt, pos, .6, 2), 2.0)), 5.0, 2.5), wetp)
col = MIXC(nt, M(nt, "MULTIPLY", wblob, .6), col, (.5, .48, .44))
px0, px1, py0, py1 = d1[0] + .5, d1[0] + 9.0, d1[1] - 2.2, d1[1] + 4.2
inpatch = M(nt, "MULTIPLY", M(nt, "MULTIPLY", SMOOTH(nt, X, px0 - .02, px0), SMOOTH(nt, X, px1 + .02, px1)), M(nt, "MULTIPLY", SMOOTH(nt, Y, py0 - .02, py0), SMOOTH(nt, Y, py1 + .02, py1)))
inpatch = M(nt, "MULTIPLY", inpatch, patch)
pwhite = RAMP(nt, fine, [(0, (.84, .85, .83)), (1, (.9, .91, .89))])
pseam = M(nt, "MAXIMUM", M(nt, "MAXIMUM", BAND(nt, X, px0, .04), BAND(nt, X, px1, .04)), M(nt, "MAXIMUM", BAND(nt, Y, py0, .04), BAND(nt, Y, py1, .04)))
col = MIXC(nt, inpatch, col, MIXC(nt, pseam, pwhite, (.7, .7, .68)))
# punctures: small dark spots near RTU 1's service side (scattered points on a coarse voronoi)
vpt = VORO(nt, pos, 1.6, "F1", 1.0); (rc, rl) = RTUS[0]
near = M(nt, "MULTIPLY", SMOOTH(nt, M(nt, "ABSOLUTE", M(nt, "SUBTRACT", X, rc[0] + 3.4)), 2.6, 1.0), SMOOTH(nt, M(nt, "ABSOLUTE", M(nt, "SUBTRACT", Y, rc[1] - .4)), 2.2, .8))
pdot = M(nt, "MULTIPLY", SMOOTH(nt, vpt.outputs["Distance"], .035, .02), M(nt, "MULTIPLY", near, punct)); pdot = M(nt, "MULTIPLY", pdot, SMOOTH(nt, NOISE(nt, pos, 1.6, 1), .5, .6))
col = MIXC(nt, pdot, col, (.05, .045, .04))
# fabric on the seams (restoration), then the coating
fb = M(nt, "MULTIPLY", seamfab, M(nt, "MAXIMUM", SMOOTH(nt, sy, .11, .09), BAND(nt, X, 24.4, .1, .01)))
fcol = RAMP(nt, NOISE(nt, pos, 120, 2), [(0, (.8, .8, .78)), (1, (.88, .88, .86))]); col = MIXC(nt, fb, col, fcol)
ccol = RAMP(nt, NOISE(nt, pos, 30, 2), [(0, (.86, .87, .85)), (1, (.92, .92, .9))]); col = MIXC(nt, coat, col, ccol)
rough = M(nt, "ADD", .55, M(nt, "MULTIPLY", chalk, .3)); rough = MIXF(nt, dm, rough, .9); rough = MIXF(nt, M(nt, "MULTIPLY", inpond, algae), rough, .7)
rough = MIXF(nt, coat, rough, .4); rough = MIXF(nt, wet, rough, .1)
bmp = N(nt, "ShaderNodeBump"); bmp.inputs["Strength"].default_value = .3; bmp.inputs["Distance"].default_value = .003
L(nt, M(nt, "ADD", M(nt, "MULTIPLY", seam, 1.2), M(nt, "ADD", M(nt, "MULTIPLY", fb, .6), M(nt, "MULTIPLY", pdot, -1))), bmp.inputs["Height"])
finish(nt, principled(nt, col, rough, .4, bmp.outputs[0]).outputs[0])

# membrane on vertical faces (curbs, wall base, parapet inside): same whites, dirt, crack lines on the curbs, coating
flash, nt = mat("Flashing")
pos, X, Y, Z = coords(nt)
dirt = val_node(nt, "dirt", "dirt"); chalk = val_node(nt, "chalk", "chalk"); crack = val_node(nt, "crack", "crack"); seamfab = val_node(nt, "seamfab", "seamfab"); coat = val_node(nt, "coat", "coat")
fine = NOISE(nt, pos, 60, 2); white = RAMP(nt, fine, [(0, (.76, .77, .75)), (1, (.84, .85, .83))])
col = MIXC(nt, M(nt, "MULTIPLY", SMOOTH(nt, NOISE(nt, pos, 2, 3), .4, .8), M(nt, "MULTIPLY", dirt, .6)), white, (.42, .4, .36))
col = MIXC(nt, M(nt, "MULTIPLY", chalk, .3), col, (.66, .66, .63))
# cracks: thin dark voronoi edges, mostly near the top edge of the flashing (z high) - gated by crack
ve = VORO(nt, pos, 3.0).outputs["Distance"]; cl = M(nt, "MULTIPLY", SMOOTH(nt, ve, .012, .003), SMOOTH(nt, NOISE(nt, pos, 1.5, 2), .45, .6))
cl = M(nt, "MULTIPLY", cl, M(nt, "MULTIPLY", crack, SMOOTH(nt, Z, ZF + .08, ZF + .3))); col = MIXC(nt, cl, col, (.08, .07, .06))
fb = M(nt, "MULTIPLY", seamfab, SMOOTH(nt, NOISE(nt, pos, 100, 2), .2, .9)); col = MIXC(nt, M(nt, "MULTIPLY", fb, .9), col, (.84, .84, .82))
col = MIXC(nt, coat, col, RAMP(nt, NOISE(nt, pos, 30, 2), [(0, (.86, .87, .85)), (1, (.92, .92, .9))]))
bmp = N(nt, "ShaderNodeBump"); bmp.inputs["Strength"].default_value = .3; bmp.inputs["Distance"].default_value = .003; L(nt, M(nt, "MULTIPLY", cl, -1), bmp.inputs["Height"])
finish(nt, principled(nt, col, M(nt, "ADD", .55, M(nt, "MULTIPLY", chalk, .3)), .4, bmp.outputs[0]).outputs[0])

# painted / galvanised sheet metal (RTU cabinets, coping, counterflashing, gutters, wall panels): dirt + a little rust at edges
def sheet(name, color, metallic=.6, rough=.35, rustamt=.5):
    m, nt = mat(name); pos, X, Y, Z = coords(nt)
    dirt = val_node(nt, "dirt", "dirt"); rust = val_node(nt, "rust", "rust"); coat_ = val_node(nt, "coat", "coat") if name == "Curb" else None
    rn = NOISE(nt, pos, 4, 3, .6)
    col = MIXC(nt, M(nt, "MULTIPLY", SMOOTH(nt, NOISE(nt, pos, 1.5, 3), .35, .85), M(nt, "MULTIPLY", dirt, .5)), color, tuple(c * .45 for c in color))
    rf = M(nt, "MULTIPLY", SMOOTH(nt, M(nt, "ADD", NOISE(nt, pos, 1.2, 3, .6), M(nt, "MULTIPLY", rust, .3 * rustamt)), .82, .95), M(nt, "MULTIPLY", rust, rustamt))
    col = MIXC(nt, rf, col, (.35, .14, .05)); met = MIXF(nt, rf, metallic, 0.0); ro = MIXF(nt, rf, rough, .9)
    if coat_ is not None: col = MIXC(nt, coat_, col, (.88, .88, .86)); met = MIXF(nt, coat_, met, 0.0); ro = MIXF(nt, coat_, ro, .45)
    finish(nt, principled(nt, col, ro, .5, None, met).outputs[0]); return m
rtu_m = sheet("RTU", (.5, .48, .43), .3, .45, .25)
fan_m = sheet("Fan", (.12, .12, .12), .2, .6, .15)
coping = sheet("Coping", (.42, .43, .43), .8, .3, .2)
wallp = sheet("WallPanel", (.56, .58, .58), .5, .4, .12)
curb_m = sheet("Curb", (.62, .62, .6), .4, .5, .5)
galv = sheet("Galv", (.55, .56, .55), .8, .35, .8)
# screws: zinc-plated hex head + washer; the plating rusts first; coating covers them at the end
scr, nt = mat("Screw")
oi = N(nt, "ShaderNodeObjectInfo"); rnd = oi.outputs["Random"]; pos, X, Y, Z = coords(nt)
rust = val_node(nt, "rust", "rust"); coat = val_node(nt, "coat", "coat"); encap = val_node(nt, "encap", "encap")
rf = SMOOTH(nt, M(nt, "ADD", M(nt, "MULTIPLY", rust, 1.3), M(nt, "MULTIPLY", rnd, .5)), .45, 1.0)
rf = M(nt, "MULTIPLY", rf, M(nt, "SUBTRACT", 1.0, SMOOTH(nt, encap, .0, .3)))     # replaced screws are new again (encap == replaced + sealed)
rcol = RAMP(nt, NOISE(nt, pos, 300, 2), [(0, (.25, .09, .03)), (1, (.5, .22, .07))])
col = MIXC(nt, rf, (.62, .63, .62), rcol); col = MIXC(nt, coat, col, (.87, .87, .85))
finish(nt, principled(nt, col, MIXF(nt, coat, MIXF(nt, rf, .3, .9), .45), .5, None, MIXF(nt, coat, MIXF(nt, rf, .9, 0.0), 0.0)).outputs[0])
wash_m, nt = mat("Washer"); rust = val_node(nt, "rust", "rust"); coat = val_node(nt, "coat", "coat")
col = MIXC(nt, M(nt, "MULTIPLY", rust, .8), (.12, .12, .11), (.25, .14, .08)); col = MIXC(nt, coat, col, (.87, .87, .85))
finish(nt, principled(nt, col, .8, .3).outputs[0])
seal_m, nt = mat("Sealant"); coat = val_node(nt, "coat", "coat")
finish(nt, principled(nt, MIXC(nt, coat, (.82, .82, .8), (.88, .88, .86)), .5, .4).outputs[0])
# standing water: dark, glossy, a little see-through
wat, nt = mat("Water")
b = N(nt, "ShaderNodeBsdfPrincipled"); b.inputs["Base Color"].default_value = (.04, .06, .05, 1); b.inputs["Roughness"].default_value = .02
b.inputs["Alpha"].default_value = .78; b.inputs["Specular IOR Level"].default_value = .6; finish(nt, b.outputs[0]); wat.surface_render_method = "DITHERED"
# cast iron strainer, debris, concrete, dark hole, walkway pad, pipe insulation
iron, nt = mat("Iron"); pos, X, Y, Z = coords(nt); rust = val_node(nt, "rust", "rust")
col = MIXC(nt, M(nt, "MULTIPLY", rust, .7), (.1, .1, .1), (.3, .13, .05)); finish(nt, principled(nt, col, .75, .4, None, .2).outputs[0])
debris, nt = mat("Debris"); pos, X, Y, Z = coords(nt)
col = RAMP(nt, NOISE(nt, pos, 25, 3), [(0, (.2, .12, .05)), (.5, (.32, .2, .07)), (1, (.1, .07, .04))])
bmp = N(nt, "ShaderNodeBump"); bmp.inputs["Strength"].default_value = .8; bmp.inputs["Distance"].default_value = .02; L(nt, VORO(nt, pos, 40, "F1").outputs["Distance"], bmp.inputs["Height"])
finish(nt, principled(nt, col, .9, .2, bmp.outputs[0]).outputs[0])
bagm, nt = mat("Bag"); finish(nt, principled(nt, (.75, .75, .78), .5, .5).outputs[0])
conc, nt = mat("Concrete"); pos, X, Y, Z = coords(nt)
finish(nt, principled(nt, RAMP(nt, NOISE(nt, pos, 3, 3), [(0, (.38, .38, .36)), (1, (.5, .5, .48))]), .9, .3).outputs[0])
black, nt = mat("Hole"); finish(nt, principled(nt, (.005, .004, .003), 1.0, 0).outputs[0])
padm, nt = mat("WalkPad"); pos, X, Y, Z = coords(nt); dirt = val_node(nt, "dirt", "dirt"); coat = val_node(nt, "coat", "coat")
col = MIXC(nt, M(nt, "MULTIPLY", dirt, .5), (.38, .38, .35), (.25, .24, .22)); col = MIXC(nt, coat, col, (.5, .5, .48))
bmp = N(nt, "ShaderNodeBump"); bmp.inputs["Strength"].default_value = .4; bmp.inputs["Distance"].default_value = .004; L(nt, VORO(nt, pos, 60, "F1").outputs["Distance"], bmp.inputs["Height"])
finish(nt, principled(nt, col, .9, .2, bmp.outputs[0]).outputs[0])
pipe_m, nt = mat("Pipe"); dirt = val_node(nt, "dirt", "dirt"); rust = val_node(nt, "rust", "rust")
col = MIXC(nt, M(nt, "MULTIPLY", rust, .5), (.75, .72, .2), (.4, .3, .1)); finish(nt, principled(nt, col, .5, .4).outputs[0])
boot_m, nt = mat("Boot"); dirt = val_node(nt, "dirt", "dirt"); coat = val_node(nt, "coat", "coat")
col = MIXC(nt, M(nt, "MULTIPLY", dirt, .4), (.7, .7, .68), (.45, .44, .4)); col = MIXC(nt, coat, col, (.87, .87, .85)); finish(nt, principled(nt, col, .7, .3).outputs[0])
grass, nt = mat("Grass"); pos, X, Y, Z = coords(nt)
finish(nt, principled(nt, RAMP(nt, NOISE(nt, pos, .6, 4), [(0, (.07, .13, .03)), (1, (.16, .2, .06))]), .9, .2).outputs[0])
asph, nt = mat("Asphalt"); pos, X, Y, Z = coords(nt)
finish(nt, principled(nt, RAMP(nt, NOISE(nt, pos, 20, 3), [(0, (.05, .05, .05)), (1, (.1, .1, .1))]), .85, .3).outputs[0])
canopy, nt = mat("Canopy"); pos, X, Y, Z = coords(nt); oi = N(nt, "ShaderNodeObjectInfo")
col = RAMP(nt, M(nt, "ADD", NOISE(nt, pos, 2, 4), M(nt, "MULTIPLY", oi.outputs["Random"], .4)), [(0, (.03, .09, .015)), (.6, (.08, .17, .03)), (1, (.16, .24, .05))])
finish(nt, principled(nt, col, .8, .2).outputs[0])
bark, nt = mat("Bark"); finish(nt, principled(nt, (.1, .07, .05), .9, .2).outputs[0])
# interior: steel deck underside (grey primer paint) with the stain; joists; lights; floor
deckm, nt = mat("DeckUnder"); pos, X, Y, Z = coords(nt); stain = val_node(nt, "stain", "stain")
base = RAMP(nt, NOISE(nt, pos, 12, 3), [(0, (.5, .52, .5)), (1, (.6, .62, .6))])
sd = M(nt, "SQRT", M(nt, "ADD", M(nt, "POWER", M(nt, "SUBTRACT", X, 106.0), 2), M(nt, "POWER", M(nt, "MULTIPLY", M(nt, "SUBTRACT", Y, -3.0), .35), 2)))
sn = NOISE(nt, pos, 1.2, 3, .6)
sf = M(nt, "MULTIPLY", SMOOTH(nt, M(nt, "ADD", sd, M(nt, "MULTIPLY", sn, 1.5)), M(nt, "ADD", 1.2, M(nt, "MULTIPLY", stain, 2.6)), M(nt, "MULTIPLY", stain, 1.0)), stain)
scol = RAMP(nt, NOISE(nt, pos, 6, 3), [(0, (.25, .13, .05)), (.5, (.4, .25, .09)), (1, (.15, .07, .03))])
ringf = M(nt, "MULTIPLY", SMOOTH(nt, sf, .1, .25), SMOOTH(nt, sf, .45, .3))      # a darker tide ring at the edge
col = MIXC(nt, M(nt, "MULTIPLY", sf, .9), base, scol); col = MIXC(nt, M(nt, "MULTIPLY", ringf, .6), col, (.22, .11, .04))
finish(nt, principled(nt, col, .7, .3).outputs[0])
joist_m, nt = mat("Joist"); finish(nt, principled(nt, (.5, .52, .52), .6, .4, None, .3).outputs[0])
light_m, nt = mat("Light"); e = N(nt, "ShaderNodeEmission"); e.inputs["Color"].default_value = (1, .97, .9, 1); e.inputs["Strength"].default_value = 160; finish(nt, e.outputs[0])
floor_m, nt = mat("Floor"); pos, X, Y, Z = coords(nt); drip = val_node(nt, "drip", "drip")
base = RAMP(nt, NOISE(nt, pos, 2, 3), [(0, (.3, .3, .29)), (1, (.42, .42, .4))])
pd = M(nt, "SQRT", M(nt, "ADD", M(nt, "POWER", M(nt, "SUBTRACT", X, 106.0), 2), M(nt, "POWER", M(nt, "SUBTRACT", Y, -3.0), 2)))
wetf = M(nt, "MULTIPLY", SMOOTH(nt, M(nt, "ADD", pd, M(nt, "MULTIPLY", NOISE(nt, pos, 2, 2), .5)), 1.1, .6), drip)
finish(nt, principled(nt, MIXC(nt, wetf, base, (.12, .12, .12)), MIXF(nt, wetf, .85, .1), .4).outputs[0])
P["drip"] = P["drip"] if "drip" in P else [(2.5, 0), (3, 1)]
rack_m, nt = mat("Rack"); finish(nt, principled(nt, (.75, .35, .1), .5, .4).outputs[0])
cardb, nt = mat("Box"); pos, X, Y, Z = coords(nt); finish(nt, principled(nt, RAMP(nt, NOISE(nt, pos, 5, 2), [(0, (.45, .32, .18)), (1, (.6, .45, .28))]), .9, .2).outputs[0])

# ---------------------------------------------------------------- world: Nishita sky + sun (overcast while it rains)
w = bpy.data.worlds.new("Sky"); sc.world = w; wn = w.node_tree; wn.nodes.clear()
sky = wn.nodes.new("ShaderNodeTexSky"); sky.sky_type = "MULTIPLE_SCATTERING"; sky.altitude = 250; sky.air_density = 1.0; sky.sun_size = math.radians(.6)
bg = wn.nodes.new("ShaderNodeBackground"); bg.inputs["Strength"].default_value = 1.0
ovc = wn.nodes.new("ShaderNodeValue"); ovc.name = "overcast"
grey = wn.nodes.new("ShaderNodeRGB"); grey.outputs[0].default_value = (4.5, 4.8, 5.4, 1)
mx = wn.nodes.new("ShaderNodeMix"); mx.data_type = "RGBA"; mx.clamp_factor = True
wn.links.new(ovc.outputs[0], mx.inputs["Factor"]); wn.links.new(sky.outputs[0], mx.inputs[6]); wn.links.new(grey.outputs[0], mx.inputs[7])
wo = wn.nodes.new("ShaderNodeOutputWorld"); wn.links.new(mx.outputs[2], bg.inputs[0]); wn.links.new(bg.outputs[0], wo.inputs["Surface"])
bpy.ops.object.light_add(type="SUN"); sun = bpy.context.object; sun.name = "Sun"; sun.data.angle = math.radians(1.0)
def apply_sky(x):
    el, rot, oc = x
    sky.sun_elevation = math.radians(el); sky.sun_rotation = math.radians(rot); sky.sun_intensity = 1.0 - .75 * oc
    for k in ("sun_elevation", "sun_rotation", "sun_intensity"): sky.keyframe_insert(k, frame=sc.frame_current)
    ovc.outputs[0].default_value = oc; ovc.outputs[0].keyframe_insert("default_value", frame=sc.frame_current)
    d = Vector((math.cos(math.radians(el)) * math.sin(math.radians(rot)), math.cos(math.radians(el)) * -math.cos(math.radians(rot)), math.sin(math.radians(el))))
    sun.rotation_euler = (-d).to_track_quat("-Z", "Y").to_euler(); sun.keyframe_insert("rotation_euler", frame=sc.frame_current)
    sun.data.energy = 1.0 * (1 - .85 * oc); sun.data.keyframe_insert("energy", frame=sc.frame_current)
reg(lambda s: (pv("sun_el", s), pv("sun_rot", s), pv("overcast", s)), apply_sky)

# ---------------------------------------------------------------- ground, far surroundings (cheap)
grid("Ground", -600, 600, -600, 600, 50, grass)
box("Lot", (MX0 - 30, -HW - 40, .005), (FX1 + 40, -HW - 2, .02), asph)
box("Lot2", (FX1 + 2, -HW - 40, .005), (FX1 + 40, HW + 30, .02), asph)
for i in range(16):      # far warehouses and tree blobs on the horizon
    x = random.uniform(-400, 400); y = random.choice([1, -1]) * random.uniform(120, 350)
    box("FarBox%d" % i, (x, y, 0), (x + random.uniform(40, 120), y + random.uniform(25, 60), random.uniform(6, 11)), wallp)
for i in range(120):
    x = random.uniform(-450, 450); y = random.choice([1, -1]) * random.uniform(60, 420); h = random.uniform(8, 16)
    if -70 < x < 90 and abs(y) < 75: continue
    t = cyl("Tr%d" % i, (x, y, 0), .3, h * .5, bark, 6)
    c = sphere("Tc%d" % i, (x, y, h * .7), h * .4, canopy, 10, 6); c.scale.z = .8
    tx = bpy.data.textures.new("tt%d" % i, "CLOUDS"); tx.noise_scale = h * .15
    dm = c.modifiers.new("D", "DISPLACE"); dm.texture = tx; dm.strength = h * .2
for i in range(7):       # a row of trees along the lot edge (the near-ish ones the hero camera sees past the metal roof)
    x = MX0 - 20 - i * 9 + random.uniform(-2, 2); y = random.uniform(-10, 10); h = random.uniform(9, 14)
    cyl("Tn%d" % i, (x, y, 0), .25, h * .5, bark, 8); c = sphere("Tnc%d" % i, (x, y, h * .7), h * .38, canopy, 14, 8); c.scale.z = .85
    tx = bpy.data.textures.new("tn%d" % i, "CLOUDS"); tx.noise_scale = h * .12; dm = c.modifiers.new("D", "DISPLACE"); dm.texture = tx; dm.strength = h * .22

# ---------------------------------------------------------------- the metal building: walls, gable roof with real ribs, gutters, screws
box("MWallS", (MX0, -HW - .05, 0), (MX1, -HW, ZE), wallp); box("MWallN", (MX0, HW, 0), (MX1, HW + .05, ZE), wallp)
box("MWallW", (MX0 - .05, -HW, 0), (MX0, HW, ZE), wallp)
# gable end wall at x=0 (rises above the flat roof) as a profile: rectangle to the eave + triangle to the ridge
mesh_obj("MGable", [(MX1 - .05, -HW, 0), (MX1 + .05, -HW, 0), (MX1 + .05, HW, 0), (MX1 - .05, HW, 0),
                    (MX1 - .05, -HW, ZE), (MX1 + .05, -HW, ZE), (MX1 + .05, HW, ZE), (MX1 - .05, HW, ZE), (MX1 - .05, 0, ZR), (MX1 + .05, 0, ZR)],
         [(0, 3, 2, 1), (0, 1, 5, 4), (2, 3, 7, 6), (1, 2, 6, 5), (3, 0, 4, 7), (5, 9, 8, 4), (6, 7, 8, 9), (4, 8, 7), (5, 6, 9)], wallp)
def metal_roof(sign):
    """one slope: rib profile along x, extruded along y from eave to ridge (real geometry so the close-ups hold)"""
    prof = [(0, 0), (.19, 0), (.22, .032), (.26, .032), (.29, 0), (RIB, 0)]
    xs = []; zs = []
    k = 0; x = MX0
    while x < MX1 - 1e-6:
        for (dx, dz) in prof[:-1]: xs.append(x + dx); zs.append(dz)
        x += RIB
    xs.append(MX1); zs.append(0)
    ys = [sign * HW, sign * 7.5, 0.0] if sign > 0 else [-HW, -7.5, 0.0]
    ys = sorted(ys)
    verts = []; faces = []
    for y in ys:
        for xx, dz in zip(xs, zs): verts.append((xx, y, zmetal(y) + dz + .02))
    n = len(xs)
    for j in range(len(ys) - 1):
        for i in range(n - 1):
            a = j * n + i; faces.append((a, a + 1, a + n + 1, a + n))
    o = mesh_obj("MRoof%s" % ("N" if sign > 0 else "S"), verts, faces, met)
    for p in o.data.polygons: p.use_smooth = False
    return o
roofN = metal_roof(1); roofS = metal_roof(-1)
box("Ridge", (MX0, -.25, ZR - .02), (MX1 + .1, .25, ZR + .08), galv)        # ridge cap
for sgn in (1, -1):      # box gutter at each eave + a downspout at the corner
    box("Gutter%d" % sgn, (MX0, sgn * HW + (0 if sgn > 0 else -.22), ZE - .18), (MX1, sgn * HW + (.22 if sgn > 0 else 0), ZE + .05), galv)
    cyl("DS%d" % sgn, (MX0 + 1.0, sgn * (HW + .22), 0), .06, ZE - .2, galv, 10)
box("RakeTrimW", (MX0 - .06, -HW - .05, ZE - .08), (MX0 + .02, HW + .05, ZE + .12), galv)
# screws: a grid in the flats at the purlin lines, geometry-nodes instance of a hex head + washer; Backout lifts/tilts them
def screw_obj():
    bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=.0045, depth=.005, location=(0, 0, .0045)); h = bpy.context.object; h.name = "ScrewHead"; h.data.materials.append(scr)
    bpy.ops.mesh.primitive_cylinder_add(vertices=14, radius=.0075, depth=.002, location=(0, 0, .001)); wsh = bpy.context.object; wsh.name = "ScrewWasher"
    for p in wsh.data.polygons: p.use_smooth = True
    bpy.ops.object.select_all(action="DESELECT"); h.select_set(True); wsh.select_set(True); bpy.context.view_layer.objects.active = h
    h.data.materials.append(wash_m)
    for p in wsh.data.polygons: p.material_index = 1
    bpy.ops.object.join()
    return h
screw = screw_obj(); screw.hide_render = True; screw.hide_viewport = True
blob = sphere("Blob", (0, 0, .002), .014, seal_m, 12, 6); blob.scale = (1, 1, .45); blob.hide_render = True; blob.hide_viewport = True
scol = screw

def screw_field(name, sign, inst, s_backout=True):
    ng = bpy.data.node_groups.new(name, "GeometryNodeTree")
    ng.interface.new_socket("Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
    ng.interface.new_socket("Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    sb = ng.interface.new_socket("Backout", in_out="INPUT", socket_type="NodeSocketFloat"); sb.default_value = 0.0
    ss = ng.interface.new_socket("Scale", in_out="INPUT", socket_type="NodeSocketFloat"); ss.default_value = 1.0
    gi = ng.nodes.new("NodeGroupInput"); go = ng.nodes.new("NodeGroupOutput")
    nx = int(round((MX1 - MX0) / RIB)); ny = 10      # 10 purlin rows per slope: y = sign*(0.75 .. 14.25)
    g = ng.nodes.new("GeometryNodeMeshGrid"); g.inputs["Size X"].default_value = (nx - 1) * RIB; g.inputs["Size Y"].default_value = (ny - 1) * SPY
    g.inputs["Vertices X"].default_value = nx; g.inputs["Vertices Y"].default_value = ny
    tr = ng.nodes.new("GeometryNodeTransform"); tr.inputs["Translation"].default_value = (MX0 + .095 + (nx - 1) * RIB / 2, sign * (0.75 + (ny - 1) * SPY / 2), 0)
    ng.links.new(g.outputs[0], tr.inputs[0])
    m2p = ng.nodes.new("GeometryNodeMeshToPoints"); ng.links.new(tr.outputs[0], m2p.inputs[0])
    # z from the gable formula + a backed-out lift (random^3 * 12 mm)
    pos = ng.nodes.new("GeometryNodeInputPosition"); sx = ng.nodes.new("ShaderNodeSeparateXYZ"); ng.links.new(pos.outputs[0], sx.inputs[0])
    def gm(op, a, b=None):
        n = ng.nodes.new("ShaderNodeMath"); n.operation = op
        for i, x in enumerate((a, b)):
            if x is None: continue
            if lk(x): ng.links.new(x, n.inputs[i])
            else: n.inputs[i].default_value = x
        return n.outputs[0]
    z = gm("ADD", ZE + .022 + .0005, gm("DIVIDE", gm("SUBTRACT", HW, gm("ABSOLUTE", sx.outputs["Y"])), 12.0))
    r = ng.nodes.new("FunctionNodeRandomValue"); r.data_type = "FLOAT"; r.inputs[2].default_value = 0; r.inputs[3].default_value = 1; r.inputs[8].default_value = 3
    lift = gm("MULTIPLY", gm("POWER", r.outputs[1], 3.0), gm("MULTIPLY", gi.outputs["Backout"], .012))
    z = gm("ADD", z, lift)
    cxyz = ng.nodes.new("ShaderNodeCombineXYZ"); ng.links.new(sx.outputs["X"], cxyz.inputs[0]); ng.links.new(sx.outputs["Y"], cxyz.inputs[1]); ng.links.new(z, cxyz.inputs[2])
    sp = ng.nodes.new("GeometryNodeSetPosition"); ng.links.new(m2p.outputs[0], sp.inputs["Geometry"]); ng.links.new(cxyz.outputs[0], sp.inputs["Position"])
    iop = ng.nodes.new("GeometryNodeInstanceOnPoints"); ng.links.new(sp.outputs[0], iop.inputs["Points"])
    if isinstance(inst, bpy.types.Collection):
        ci = ng.nodes.new("GeometryNodeCollectionInfo"); ci.inputs["Collection"].default_value = inst; ci.transform_space = "RELATIVE"; ng.links.new(ci.outputs[0], iop.inputs["Instance"])
    else:
        oi = ng.nodes.new("GeometryNodeObjectInfo"); oi.inputs["Object"].default_value = inst; oi.transform_space = "RELATIVE"; ng.links.new(oi.outputs["Geometry"], iop.inputs["Instance"])
    # tilt: slope tilt about x (atan(1/12) toward the ridge) + random wobble by backout
    rr = ng.nodes.new("FunctionNodeRandomValue"); rr.data_type = "FLOAT_VECTOR"; rr.inputs[0].default_value = (-.35, -.35, 0); rr.inputs[1].default_value = (.35, .35, 6.28); rr.inputs[8].default_value = 5
    sv = ng.nodes.new("ShaderNodeVectorMath"); sv.operation = "SCALE"; ng.links.new(rr.outputs[0], sv.inputs[0])
    ng.links.new(gm("MULTIPLY", gi.outputs["Backout"], gm("POWER", r.outputs[1], 2.0)), sv.inputs["Scale"])
    base_rot = ng.nodes.new("FunctionNodeInputVector"); base_rot.vector = (sign * math.atan(1 / 12.0), 0, 0)
    ad = ng.nodes.new("ShaderNodeVectorMath"); ad.operation = "ADD"; ng.links.new(base_rot.outputs[0], ad.inputs[0]); ng.links.new(sv.outputs[0], ad.inputs[1])
    ng.links.new(ad.outputs[0], iop.inputs["Rotation"])
    ng.links.new(gi.outputs["Scale"], iop.inputs["Scale"])
    ng.links.new(iop.outputs[0], go.inputs["Geometry"])
    holder = mesh_obj(name + "Holder", [(0, 0, 0)], [], None)
    md = holder.modifiers.new(name, "NODES"); md.node_group = ng
    return md, sb.identifier, ss.identifier
for sign in (1, -1):
    md, bid, sid = screw_field("Screws%d" % sign, sign, scol)
    def apply_b(x, md=md, bid=bid): md[bid] = float(x); md.keyframe_insert('["%s"]' % bid, frame=sc.frame_current)
    reg(lambda s: pv("backout", s), apply_b)
    md2, bid2, sid2 = screw_field("Blobs%d" % sign, sign, blob)
    def apply_s(x, md=md2, sid=sid2): md[sid] = float(x); md.keyframe_insert('["%s"]' % sid, frame=sc.frame_current)
    reg(lambda s: max(.001, pv("encap", s)), apply_s)

# ---------------------------------------------------------------- the flat addition: walls, membrane roof (sumps + settling), parapet, wall flashing
box("FWallS", (FX0, -HW - .3, 0), (FX1, -HW, ZF - .25), wallp); box("FWallN", (FX0, HW, 0), (FX1, HW + .3, ZF - .25), wallp); box("FWallE", (FX1, -HW - .3, 0), (FX1 + .3, HW + .3, ZF - .25), wallp)
def zflat(x, y): return ZF
roof = grid("FRoof", FX0, FX1, -HW, HW, .25, mem, zflat)
roof.shape_key_add(name="Basis"); ks = roof.shape_key_add(name="sump"); kt = roof.shape_key_add(name="settle")
for i, v in enumerate(roof.data.vertices):
    x, y = v.co.x, v.co.y; dz = 0.0; dt = 0.0
    for (dx_, dy_) in DRAINS:
        d = math.hypot(x - dx_, y - dy_)
        if d < 3.0: dz -= .07 * (1 - d / 3.0)                       # tapered sump to each drain
    bx, by, br, bd = BIRD; d = math.hypot(x - bx, (y - by) * 1.3) * (1 + .35 * noise.noise(Vector((x * .25, y * .25, 7))))
    if d < br: dt -= bd * (1 - (d / br) ** 2) ** 1.2
    dt -= .012 * (.5 + .5 * noise.noise(Vector((x * .12, y * .12, 1))))   # general deck deflection between joists
    ks.data[i].co.z = v.co.z + dz; kt.data[i].co.z = v.co.z + dt
roof.data.shape_keys.key_blocks["sump"].value = 1.0
def apply_settle(x): kb = roof.data.shape_keys.key_blocks["settle"]; kb.value = x; kb.keyframe_insert("value", frame=sc.frame_current)
reg(lambda s: pv("settle", s), apply_settle)
# the ponds: a water plane in the birdbath and a ring around the clogged drain; level keyed
bx, by, br, bd = BIRD
pond1 = grid("Pond1", bx - br, bx + br, by - br / 1.3, by + br / 1.3, .5, wat, lambda x, y: 0.0)
def apply_pond1(v): pond1.location.z = ZF - bd * .999 + bd * .72 * v - (.001 if v < .01 else 0); pond1.hide_render = v < .02; pond1.keyframe_insert("location", frame=sc.frame_current); pond1.keyframe_insert("hide_render", frame=sc.frame_current)
reg(lambda s: pv("pond", s) * pv("settle", s), apply_pond1)
d1 = DRAINS[0]
pond2 = grid("Pond2", d1[0] - 3, d1[0] + 3, d1[1] - 3, d1[1] + 3, .5, wat, lambda x, y: 0.0)
def apply_pond2(v): pond2.location.z = ZF - .07 + .05 * v; pond2.hide_render = v < .05; pond2.keyframe_insert("location", frame=sc.frame_current); pond2.keyframe_insert("hide_render", frame=sc.frame_current)
reg(lambda s: pv("pond", s) * pv("clog", s), apply_pond2)
# parapet on three sides (the 4th side is the metal gable wall): wall + membrane base flashing inside + metal coping
for (a, b) in (((FX0, -HW - .3, ZF - .3), (FX1 + .3, -HW, ZF + PAR)), ((FX0, HW, ZF - .3), (FX1 + .3, HW + .3, ZF + PAR)), ((FX1, -HW - .3, ZF - .3), (FX1 + .3, HW + .3, ZF + PAR))):
    box("Parapet", a, b, flash)
for (a, b) in (((FX0, -HW - .35, ZF + PAR), (FX1 + .35, -HW + .05, ZF + PAR + .05)), ((FX0, HW - .05, ZF + PAR), (FX1 + .35, HW + .35, ZF + PAR + .05)), ((FX1 - .05, -HW - .35, ZF + PAR), (FX1 + .35, HW + .35, ZF + PAR + .05))):
    box("Coping", a, b, coping, .01)
# wall flashing at the gable: membrane up the wall 0.25 m, termination bar, metal counterflashing above it
box("WallBase", (FX0 - .01, -HW, ZF - .01), (FX0 + .06, HW, ZF + .25), flash)
box("TermBar", (FX0 + .06, -HW, ZF + .22), (FX0 + .075, HW, ZF + .25), galv)
box("Counter", (FX0 + .05, -HW, ZF + .2), (FX0 + .09, HW, ZF + .34), galv)
# scuppers through the east parapet (an overflow scupper box + a conductor head and downspout outside)
for yy in (-10.0, 10.0):
    box("Scup%g" % yy, (FX1 - .08, yy - .18, ZF + .05), (FX1 + .4, yy + .18, ZF + .17), galv)
    box("ScupHole%g" % yy, (FX1 - .07, yy - .16, ZF + .06), (FX1 + .39, yy + .16, ZF + .16), black)
    box("CHead%g" % yy, (FX1 + .3, yy - .3, ZF - .55), (FX1 + .7, yy + .3, ZF + .1), galv)
    cyl("CDS%g" % yy, (FX1 + .5, yy, 0), .07, ZF - .55, galv, 10)
# roof drains: cast-iron clamping ring + dome strainer; debris + a plastic bag when clogged
for i, (dx_, dy_) in enumerate(DRAINS):
    zb = ZF - .07
    cyl("DrainRing%d" % i, (dx_, dy_, zb - .01), .28, .03, iron, 24)
    cyl("DrainBowl%d" % i, (dx_, dy_, zb - .25), .17, .25, black, 16)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=.2, location=(dx_, dy_, zb + .02), segments=16, ring_count=8); dome = bpy.context.object; dome.name = "Dome%d" % i
    dome.scale.z = .75; dome.data.materials.append(iron)
    bm = bmesh.new(); bm.from_mesh(dome.data); bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.z < -.02], context="VERTS"); bm.to_mesh(dome.data); bm.free()
    wf = dome.modifiers.new("W", "WIREFRAME"); wf.thickness = .022; wf.use_even_offset = True
    deb = sphere("Debris%d" % i, (dx_ + .05, dy_ - .05, zb), .34, debris, 16, 8)
    tx = bpy.data.textures.new("deb%d" % i, "CLOUDS"); tx.noise_scale = .12; dm = deb.modifiers.new("D", "DISPLACE"); dm.texture = tx; dm.strength = .14
    bag = sphere("Bag%d" % i, (dx_ - .18, dy_ + .12, zb + .08), .16, bagm, 12, 6); bag.scale = (1.4, .9, .5); bag.rotation_euler = (0, 0, .7)
    def apply_clog(v, deb=deb, bag=bag, i=i):
        k = v if i == 0 else v * .45
        deb.scale = (1.1 * k + .001, 1.0 * k + .001, .55 * k + .001); deb.keyframe_insert("scale", frame=sc.frame_current)
        bag.hide_render = (v < .5) or i == 1; bag.keyframe_insert("hide_render", frame=sc.frame_current)
    reg(lambda s: pv("clog", s), apply_clog)
# rooftop units on curbs + condensate line + the wet-flashing crack lines are in the material
for i, ((cx, cy), (lx, ly, lz)) in enumerate(RTUS):
    box("Curb%d" % i, (cx - lx / 2 + .05, cy - ly / 2 + .05, ZF - .01), (cx + lx / 2 - .05, cy + ly / 2 - .05, ZF + .36), flash)
    box("CurbCant%d" % i, (cx - lx / 2 - .04, cy - ly / 2 - .04, ZF - .01), (cx + lx / 2 + .04, cy + ly / 2 + .04, ZF + .04), flash)
    u = box("RTU%d" % i, (cx - lx / 2, cy - ly / 2, ZF + .36), (cx + lx / 2, cy + ly / 2, ZF + .36 + lz), rtu_m, .02)
    box("RTUHood%d" % i, (cx - lx / 2 - .2, cy - ly / 2, ZF + .36 + lz * .45), (cx - lx / 2 + .02, cy + ly / 2, ZF + .36 + lz * .95), rtu_m, .01)   # condenser hood faces -x
    for j in range(2):   # fan grilles on top
        cyl("Fan%d_%d" % (i, j), (cx - lx / 4 + j * lx / 2, cy, ZF + .36 + lz), lx * .17, .03, fan_m, 20)
    box("Panel%d" % i, (cx + lx / 2 - .003, cy - ly / 2 + .25, ZF + .5), (cx + lx / 2 + .003, cy + ly / 2 - .25, ZF + .36 + lz - .2), coping)
    cyl("Cond%d" % i, (cx + lx / 2 + .04, cy - ly / 4, ZF + .06), .012, 2.5, boot_m, 8, axis="x")    # condensate line to a splash block
    box("Splash%d" % i, (cx + lx / 2 + 2.4, cy - ly / 4 - .2, ZF), (cx + lx / 2 + 2.9, cy - ly / 4 + .2, ZF + .04), conc)
# pipe penetrations with boots; gas line on sleepers; walkway pads; hatch
for i, (px_, py_) in enumerate(PIPES):
    cyl("Pipe%d" % i, (px_, py_, ZF), .04, .6, galv, 12)
    cyl("Boot%d" % i, (px_, py_, ZF), .16, .2, boot_m, 14, .06)
    cyl("Clamp%d" % i, (px_, py_, ZF + .19), .065, .015, galv, 12)
for i, x in enumerate(range(5, 41, 3)):
    box("Sleeper%d" % i, (x - .15, 11.8, ZF), (x + .15, 12.4, ZF + .12), padm)
    box("SleepBlock%d" % i, (x - .08, 12.0, ZF + .12), (x + .08, 12.2, ZF + .22), galv)
cyl("GasLine", (4.0, 12.1, ZF + .25), .025, 38.0, pipe_m, 10, axis="x")
hx, hy = HATCH
box("HatchCurb", (hx - .5, hy - .42, ZF - .01), (hx + .5, hy + .42, ZF + .3), flash)
box("HatchLid", (hx - .55, hy - .47, ZF + .3), (hx + .55, hy + .47, ZF + .4), coping, .01)
box("HatchCap", (hx - .55, hy - .47, ZF + .3), (hx + .55, hy + .47, ZF + .33), galv)
def walkway(name, a, b):
    o = box(name, (min(a[0], b[0]) - .38, min(a[1], b[1]) - .38, ZF + .002), (max(a[0], b[0]) + .38, max(a[1], b[1]) + .38, ZF + .008), padm)
for i, ((cx, cy), (lx, ly, lz)) in enumerate(RTUS):
    walkway("Walk%da" % i, (hx, hy), (hx, cy)); walkway("Walk%db" % i, (hx, cy), (cx + lx / 2 + .4, cy))
# seam fishmouths: small lifted tongues at seam lines (scale keyed), near the pond and the drain
FISH = [(d1[0] + 1.2, SEAMY0 + 4 * ROLL), (bx - 1.8, SEAMY0 + 3 * ROLL), (bx + 3.0, SEAMY0 + 2 * ROLL), (d1[0] - 2.0, SEAMY0 + 3 * ROLL)]
for i, (fx_, fy_) in enumerate(FISH):
    root = bpy.data.objects.new("FishRoot%d" % i, None); bpy.context.collection.objects.link(root); root.location = (fx_, fy_ + .06, ZF + .002)
    t_ = box("Fish%d" % i, (-.2, -.075, 0), (.2, 0, .0025), flash); t_.parent = root
    g_ = box("FishGap%d" % i, (-.19, -.07, -.004), (.19, -.005, .0), black); g_.parent = root
    def apply_fish(v, root=root, g_=g_): root.rotation_euler = (math.radians(55 * v), 0, 0); root.keyframe_insert("rotation_euler", frame=sc.frame_current); g_.hide_render = v < .1; g_.keyframe_insert("hide_render", frame=sc.frame_current)
    reg(lambda s: pv("fish", s), apply_fish)

# ---------------------------------------------------------------- the interior (far away at x=100): deck underside, bar joists, lights, floor, racks, bucket, drip
IX, IY = 100.0, 0.0
box("IFloor", (IX - 12, IY - 10, -.05), (IX + 12, IY + 10, 0), floor_m)
for a, b in (((IX - 12, IY - 10.3, 0), (IX + 12, IY - 10, ZF)), ((IX - 12, IY + 10, 0), (IX + 12, IY + 10.3, ZF)), ((IX - 12.3, IY - 10, 0), (IX - 12, IY + 10, ZF)), ((IX + 12, IY - 10, 0), (IX + 12.3, IY + 10, ZF))):
    box("IWall", a, b, conc)
# steel deck: B-deck profile (6 in pitch, 1.5 in deep) extruded along y
def deck():
    prof = [(0, 0), (.045, 0), (.06, -.038), (.09, -.038), (.105, 0), (.1524, 0)]
    xs = []; zs = []; x = IX - 12
    while x < IX + 12 - 1e-6:
        for (dx, dz) in prof[:-1]: xs.append(x + dx); zs.append(dz)
        x += .1524
    xs.append(IX + 12); zs.append(0)
    verts = []; faces = []; ys = (IY - 10, IY + 10)
    for y in ys:
        for xx, dz in zip(xs, zs): verts.append((xx, y, ZF - .13 + dz))
    n = len(xs)
    for i in range(n - 1): faces.append((i, i + 1, i + n + 1, i + n))
    return mesh_obj("Deck", verts, faces, deckm)
deck()
for i, y in enumerate(range(-9, 10, 2)):      # bar joists (top chord, bottom chord, web zigzag as thin boxes)
    y = IY + y
    box("JoistT%d" % i, (IX - 12, y - .05, ZF - .2), (IX + 12, y + .05, ZF - .17), joist_m)
    box("JoistB%d" % i, (IX - 12, y - .04, ZF - .75), (IX + 12, y + .04, ZF - .72), joist_m)
    for k in range(-11, 12):
        w_ = box("Web%d_%d" % (i, k), (-.012, -.012, 0), (.012, .012, .66), joist_m); w_.location = (IX + k * 1.0, y, ZF - .74); w_.rotation_euler = (0, math.radians(38 * (1 if k % 2 else -1)), 0)
for i in range(6):     # high-bay fixtures
    x = IX - 8 + (i % 3) * 8; y = IY - 5 + (i // 3) * 10
    box("Fix%d" % i, (x - .3, y - .6, ZF - 1.3), (x + .3, y + .6, ZF - 1.2), light_m)
for i in range(3):     # pallet racks with boxes, along the far wall
    x = IX - 9 + i * 7
    for z0 in (0, 1.8, 3.6):
        box("Beam%d_%g" % (i, z0), (x - 2.7, IY + 6, z0 + .1), (x + 2.7, IY + 6.1, z0 + .2), rack_m); box("Beam2%d_%g" % (i, z0), (x - 2.7, IY + 7.2, z0 + .1), (x + 2.7, IY + 7.3, z0 + .2), rack_m)
        for k in range(2):
            box("BoxP%d_%g_%d" % (i, z0, k), (x - 2.5 + k * 2.6, IY + 6.05, z0 + .2), (x - .3 + k * 2.6, IY + 7.25, z0 + .2 + random.uniform(.9, 1.4)), cardb)
    for yy in (IY + 6, IY + 7.3): box("Upr%d_%g" % (i, yy), (x - 2.75, yy - .05, 0), (x - 2.65, yy + .05, 5.2), rack_m); box("Upr2%d_%g" % (i, yy), (x + 2.65, yy - .05, 0), (x + 2.75, yy + .05, 5.2), rack_m)
bucket = cyl("Bucket", (IX + 6, IY - 3, 0), .14, .36, bagm, 16, .15)
bpy.ops.mesh.primitive_uv_sphere_add(radius=.012, location=(IX + 6, IY - 3, ZF - .16), segments=8, ring_count=6); drop = bpy.context.object; drop.name = "Drop"; drop.data.materials.append(wat)
drop.scale = (1, 1, 1.6)

# ---------------------------------------------------------------- cameras and the stage keys per shot
bpy.ops.object.camera_add(); cam = bpy.context.object; cam.name = "Cam"; sc.camera = cam; cam.rotation_mode = "QUATERNION"
cd = cam.data; cd.sensor_width = 36; cd.dof.use_dof = True; cd.dof.aperture_fstop = 5.6; cd.clip_end = 3000
def aim(p, t): return (Vector(t) - Vector(p)).to_track_quat("-Z", "Y")
CAMS = {   # name: (pos0, tgt0, pos1, tgt1, lens, fstop)
 "A": ((45.5, -13.4, ZF + 4.3), (-2, 1, ZF + .5), (44.2, -12.6, ZF + 4.1), (-3, 1.5, ZF + .5), 28, 8),
 "E": ((MX0 + 12.0, -13.2, ZE + 1.0), (MX0 + 9.4, -9.0, ZE + .55), (MX0 + 12.3, -13.0, ZE + .98), (MX0 + 9.4, -9.0, ZE + .55), 35, 3.5),
 "D": ((d1[0] + 2.6, d1[1] - 2.2, ZF + 1.05), (d1[0] + .1, d1[1] + .1, ZF - .05), (d1[0] + 2.4, d1[1] - 2.4, ZF + 1.0), (d1[0] + .1, d1[1] + .1, ZF - .05), 35, 4),
 "B": ((bx + 7.5, by - 3.5, ZF + .38), (bx - 2.0, by + 2.0, ZF + .08), (bx + 7.1, by - 3.2, ZF + .4), (bx - 2.0, by + 2.0, ZF + .08), 30, 4),
 "C": ((RTUS[0][0][0] + 4.2, RTUS[0][0][1] - 3.0, ZF + 1.2), (RTUS[0][0][0] + 1.5, RTUS[0][0][1] - .9, ZF + .25), (RTUS[0][0][0] + 4.0, RTUS[0][0][1] - 3.2, ZF + 1.15), (RTUS[0][0][0] + 1.5, RTUS[0][0][1] - .9, ZF + .25), 35, 4),
 "F": ((IX + 2.0, IY - 8.5, 1.5), (IX + 5.8, IY - 3.2, 2.5), (IX + 2.3, IY - 8.3, 1.5), (IX + 5.8, IY - 3.2, 2.5), 24, 4),
 "G": ((hx - 5.5, hy + 4.5, ZF + 1.6), (hx + 1.5, hy - 1.0, ZF + .3), (hx - 5.2, hy + 4.2, ZF + 1.55), (hx + 1.5, hy - 1.0, ZF + .3), 32, 5.6),
 "H": ((45.5, -13.4, ZF + 4.3), (-2, 1, ZF + .5), (34.0, -13.2, ZF + 2.6), (-2, 2, ZF + .7), 28, 8),
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
    steps = max(1, int(math.ceil(abs(s1 - s0) / 0.05)))
    for i in range(steps + 1):
        u = i / steps
        ue = u * u * (3 - 2 * u) if s0 != s1 else 0
        STAGE_KEYS.append((int(round(fa + (fb - fa) * u)), s0 + (s1 - s0) * ue))
    # the drip inside: a droplet falling every 0.6 s while the interior shot runs (drip param > 0)
    if sh["cam"] == "F":
        for k in range(0, n + 14, 14):
            drop.location = (IX + 6, IY - 3, ZF - .16); drop.keyframe_insert("location", frame=fa + k)
            drop.location = (IX + 6, IY - 3, .36); drop.keyframe_insert("location", frame=fa + k + 13)
    f = fb + 1
drop.hide_render = True
f = 1
for sh in SHOTS:
    n = int(round(sh["dur"] * FPS))
    if sh["cam"] == "F":
        drop.hide_render = False; drop.keyframe_insert("hide_render", frame=f); drop.hide_render = True; drop.keyframe_insert("hide_render", frame=f + n)
    f += n
drop.keyframe_insert("hide_render", frame=1)
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
ids = [o for o in bpy.data.objects] + list(bpy.data.materials) + list(bpy.data.node_groups) + [w, sun.data, cd] + [roof.data.shape_keys] + list(bpy.data.worlds)
for idb in ids:
    for fc in all_curves(idb):
        for k in fc.keyframe_points:
            k.interpolation = "LINEAR"
for idb in (cam, cd):
    for fc in all_curves(idb):
        for k in fc.keyframe_points:
            k.interpolation = "CONSTANT" if int(k.co[0]) in cut else "BEZIER"; k.easing = "EASE_IN_OUT"

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
