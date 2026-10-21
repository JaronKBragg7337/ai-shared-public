# Heartbeat Homes - "The Loft" (penthouse, blue hour). Built by script, lit in Cycles, lighting baked to textures, exported to GLB.
# blender -b -P loft.py -- --city city.png --out DIR [--res 4096] [--samples 512] [--preview still.png] [--only-build]
import bpy, bmesh, math, random, sys, os, json
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:]
def arg(k, d=None):
    return argv[argv.index(k) + 1] if k in argv else d
CITY = arg("--city"); OUT = arg("--out", "."); RES = int(arg("--res", "2048")); SAMPLES = int(arg("--samples", "256"))
random.seed(5)
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = "CYCLES"
p = bpy.context.preferences.addons["cycles"].preferences; p.compute_device_type = "OPTIX"; p.get_devices()
for d in p.devices: d.use = d.type == "OPTIX"
sc.cycles.device = "GPU"
sc.view_settings.view_transform = "AgX"; sc.view_settings.look = "AgX - Medium High Contrast"
sc.view_settings.exposure = 0.0

# ------------------------------------------------------------------ materials
MATS = {}
def pmat(name, color=(0.8, 0.8, 0.8), rough=0.5, metal=0.0, emit=None, estr=0.0, trans=0.0, ior=1.45):
    m = bpy.data.materials.new(name); b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*color, 1); b.inputs["Roughness"].default_value = rough; b.inputs["Metallic"].default_value = metal
    if emit: b.inputs["Emission Color"].default_value = (*emit, 1); b.inputs["Emission Strength"].default_value = estr
    if trans: b.inputs["Transmission Weight"].default_value = trans; b.inputs["IOR"].default_value = ior
    MATS[name] = m; return m

def nodes_of(m): return m.node_tree.nodes, m.node_tree.links

def wood_mat(name, base, dark, plank_w, plank_l, grain=40):
    m = pmat(name, base, 0.45); n, l = nodes_of(m); b = n["Principled BSDF"]
    tc = n.new("ShaderNodeTexCoord")
    br = n.new("ShaderNodeTexBrick"); br.inputs["Scale"].default_value = 1; br.inputs["Mortar Size"].default_value = 0.0015
    br.inputs["Brick Width"].default_value = plank_l; br.inputs["Row Height"].default_value = plank_w; br.offset = 0.37; br.offset_frequency = 1
    br.inputs["Color1"].default_value = (*base, 1); br.inputs["Color2"].default_value = (*[c * 0.8 for c in base], 1); br.inputs["Mortar"].default_value = (*[c * 0.35 for c in dark], 1)
    br.inputs["Bias"].default_value = 0
    mp = n.new("ShaderNodeMapping"); l.new(tc.outputs["Object"], mp.inputs[0]); l.new(mp.outputs[0], br.inputs["Vector"])
    wv = n.new("ShaderNodeTexWave"); wv.inputs["Scale"].default_value = grain; wv.inputs["Distortion"].default_value = 6; wv.inputs["Detail"].default_value = 3
    wv.bands_direction = "X"; l.new(mp.outputs[0], wv.inputs["Vector"])
    gr = n.new("ShaderNodeMix"); gr.data_type = "RGBA"; gr.blend_type = "MULTIPLY"; gr.inputs["Factor"].default_value = 0.35
    rr = n.new("ShaderNodeValToRGB"); rr.color_ramp.elements[0].color = (*[c * 0.55 for c in dark], 1); rr.color_ramp.elements[1].color = (1, 1, 1, 1)
    l.new(wv.outputs["Fac"], rr.inputs[0]); l.new(br.outputs["Color"], gr.inputs["A"]); l.new(rr.outputs[0], gr.inputs["B"])
    l.new(gr.outputs["Result"], b.inputs["Base Color"])
    return m

def noisy_mat(name, c1, c2, scale=8, rough=0.8, bump=0.1):
    m = pmat(name, c1, rough); n, l = nodes_of(m); b = n["Principled BSDF"]
    tc = n.new("ShaderNodeTexCoord"); nz = n.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = scale; nz.inputs["Detail"].default_value = 8
    l.new(tc.outputs["Object"], nz.inputs["Vector"])
    rr = n.new("ShaderNodeValToRGB"); rr.color_ramp.elements[0].color = (*c1, 1); rr.color_ramp.elements[1].color = (*c2, 1)
    l.new(nz.outputs["Fac"], rr.inputs[0]); l.new(rr.outputs[0], b.inputs["Base Color"])
    if bump:
        bp = n.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = bump; l.new(nz.outputs["Fac"], bp.inputs["Height"]); l.new(bp.outputs[0], b.inputs["Normal"])
    return m

def marble_mat(name):
    m = pmat(name, (0.86, 0.85, 0.83), 0.15); n, l = nodes_of(m); b = n["Principled BSDF"]
    tc = n.new("ShaderNodeTexCoord"); nz = n.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 2.2; nz.inputs["Detail"].default_value = 12; nz.inputs["Distortion"].default_value = 3
    l.new(tc.outputs["Object"], nz.inputs["Vector"])
    wv = n.new("ShaderNodeTexWave"); wv.inputs["Scale"].default_value = 1.4; wv.inputs["Distortion"].default_value = 14; wv.inputs["Detail"].default_value = 8
    l.new(tc.outputs["Object"], wv.inputs["Vector"])
    rr = n.new("ShaderNodeValToRGB"); rr.color_ramp.elements[0].position = 0.0; rr.color_ramp.elements[0].color = (0.35, 0.34, 0.33, 1)
    rr.color_ramp.elements[1].position = 0.12; rr.color_ramp.elements[1].color = (0.88, 0.87, 0.85, 1)
    l.new(wv.outputs["Fac"], rr.inputs[0]); l.new(rr.outputs[0], b.inputs["Base Color"])
    return m

oak = wood_mat("Oak", (0.46, 0.34, 0.24), (0.28, 0.18, 0.11), 0.19, 1.9)
walnut = wood_mat("Walnut", (0.2, 0.11, 0.06), (0.1, 0.05, 0.03), 0.3, 2.5, 60)
plaster = noisy_mat("Plaster", (0.74, 0.72, 0.69), (0.8, 0.78, 0.75), 3, 0.85, 0.03)
concrete = noisy_mat("Concrete", (0.32, 0.31, 0.3), (0.45, 0.44, 0.42), 5, 0.7, 0.08)
fabric = noisy_mat("Boucle", (0.62, 0.6, 0.56), (0.74, 0.72, 0.68), 90, 0.95, 0.25)
rugm = noisy_mat("Rug", (0.5, 0.45, 0.38), (0.6, 0.55, 0.47), 60, 1.0, 0.3)
steel = pmat("BlackSteel", (0.02, 0.02, 0.022), 0.35, 0.9)
blackmatte = pmat("BlackCabinet", (0.025, 0.025, 0.027), 0.55)
marble = marble_mat("Marble")
brass = pmat("Brass", (0.8, 0.6, 0.3), 0.25, 1.0)
stonet = noisy_mat("Travertine", (0.62, 0.55, 0.45), (0.72, 0.65, 0.55), 14, 0.5, 0.1)
tiles = noisy_mat("Tiles", (0.28, 0.28, 0.29), (0.34, 0.34, 0.35), 6, 0.6, 0.05)
leaf = noisy_mat("Leaf", (0.06, 0.16, 0.05), (0.1, 0.24, 0.07), 20, 0.5, 0.05)
potm = pmat("Pot", (0.08, 0.075, 0.07), 0.6)
linen = noisy_mat("Linen", (0.78, 0.77, 0.74), (0.85, 0.84, 0.81), 70, 0.9, 0.15)
glass = pmat("Glass", (0.95, 0.97, 0.97), 0.0, trans=1.0, ior=1.5)
tvblack = pmat("TVBlack", (0.01, 0.01, 0.012), 0.25)
screen = pmat("Screen", (0, 0, 0), 0.2, emit=(0.35, 0.45, 0.8), estr=1.2)
led_warm = pmat("LEDWarm", (1, 1, 1), 0.5, emit=(1.0, 0.72, 0.42), estr=18)
led_cyan = pmat("LEDCyan", (1, 1, 1), 0.5, emit=(0.1, 0.8, 1.0), estr=14)
led_pink = pmat("LEDPink", (1, 1, 1), 0.5, emit=(1.0, 0.1, 0.55), estr=14)
led_purple = pmat("LEDPurple", (1, 1, 1), 0.5, emit=(0.55, 0.2, 1.0), estr=14)
tvglow = pmat("TVGlow", (1, 1, 1), 0.5, emit=(0.45, 0.2, 1.0), estr=3)
monitor = pmat("Monitor", (0, 0, 0), 0.2, emit=(0.5, 0.6, 0.9), estr=2.5)

# ------------------------------------------------------------------ geometry helpers
def tag(o, g, solid=True, walk=False):
    o["g"] = g; o["solid"] = solid; o["walk"] = walk; return o

def box(name, a, b, mat, g="shell", solid=True, walk=False, bevel=0.0, top=None):
    """axis-aligned box from corner a to corner b. top= material for the upward face."""
    cx, cy, cz = [(a[i] + b[i]) / 2 for i in range(3)]
    bpy.ops.mesh.primitive_cube_add(size=1, location=(cx, cy, cz))
    o = bpy.context.object; o.name = name
    o.scale = tuple(abs(b[i] - a[i]) for i in range(3)); bpy.ops.object.transform_apply(scale=True)
    o.data.materials.append(mat)
    if top is not None:
        o.data.materials.append(top)
        for f in o.data.polygons:
            if f.normal.z > 0.9: f.material_index = 1
    if bevel:
        bv = o.modifiers.new("bv", "BEVEL"); bv.width = bevel; bv.segments = 3; bv.limit_method = "ANGLE"
    return tag(o, g, solid, walk)

def cyl(name, c, r, h, mat, g="furn", verts=32, solid=True, rot=None):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=h, location=(c[0], c[1], c[2] + h / 2))
    o = bpy.context.object; o.name = name; o.data.materials.append(mat)
    if rot: o.rotation_euler = rot
    bpy.ops.object.shade_smooth()
    return tag(o, g, solid)

def sphere(name, c, r, mat, g="furn", scale=(1, 1, 1), solid=False, seg=24):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=seg // 2, radius=r, location=c)
    o = bpy.context.object; o.name = name; o.scale = scale; o.data.materials.append(mat); bpy.ops.object.shade_smooth()
    return tag(o, g, solid)

def soft(o, w=0.04):
    bv = o.modifiers.new("soft", "BEVEL"); bv.width = w; bv.segments = 4
    o.modifiers.new("sub", "SUBSURF").levels = 1
    for f in o.data.polygons: f.use_smooth = True
    return o

# ------------------------------------------------------------------ shell (x 0..16 west->east, y 0..10 south->north, z up)
H1, H2, TOP = 3.2, 3.4, 6.6
box("Floor1", (-0.2, -0.2, -0.3), (16.2, 10.2, 0), concrete, "floor", walk=True, top=oak)
# mezzanine slab (x 9..16) with a hole over the stairs (y 0..1.4, x 10..15.6)
for i, (a, b) in enumerate([((9, 1.4, H1), (16, 10, H2)), ((9, 0, H1), (10, 1.4, H2)), ((15.6, 0, H1), (16, 1.4, H2))]):
    box(f"Slab{i}", a, b, plaster, "floor", walk=True, top=oak)
box("Roof", (-0.2, -0.2, TOP), (16.2, 10.2, TOP + 0.3), plaster, "shell")
box("WallS", (-0.2, -0.2, 0), (16.2, 0, TOP), plaster, "shell")
box("WallW", (-0.2, 0, 0), (0, 10, TOP), plaster, "shell")
box("WallE1", (16, 0, 0), (16.2, 2, TOP), plaster, "shell")
box("WallE2", (16, 3.2, 0), (16.2, 10, TOP), plaster, "shell")
box("WallE3", (16, 2, 2.3), (16.2, 3.2, TOP), plaster, "shell")
box("FrontDoor", (15.95, 2.02, 0), (16.02, 3.18, 2.28), walnut, "furn")
cyl("DoorHandle", (15.9, 2.25, 1.0), 0.015, 0.35, brass, "furn", 12, solid=False)
# north curtain wall: steel mullions every 2 m, transom at the slab line, glass panes (not baked)
for x in range(0, 17, 2):
    box(f"Mullion{x}", (x - 0.05, 10.0, 0), (x + 0.05, 10.18, TOP), steel, "shell")
box("Transom", (0, 10.0, H1), (16, 10.2, H2), steel, "shell")
box("Sill", (0, 10.0, 0), (16, 10.2, 0.08), steel, "shell")
for x in range(0, 16, 2):
    box(f"Pane1_{x}", (x + 0.05, 10.07, 0.08), (x + 1.95, 10.1, H1), glass, "glass")
    if x != 10:                                 # the bay at x 10..12 upstairs is the open balcony door
        box(f"Pane2_{x}", (x + 0.05, 10.07, H2), (x + 1.95, 10.1, TOP), glass, "glass")
# balcony
box("Balcony", (9, 10.2, H1 - 0.1), (16, 12.6, H2), concrete, "floor", walk=True, top=tiles)
for a, b in [((9, 12.55, H2), (16, 12.6, H2 + 1.1)), ((9, 10.2, H2), (9.05, 12.6, H2 + 1.1)), ((15.95, 10.2, H2), (16, 12.6, H2 + 1.1))]:
    box("BalcGlass", a, b, glass, "glass")
box("BalcRail", (9, 12.52, H2 + 1.1), (16, 12.63, H2 + 1.15), steel, "furn")
# mezzanine edge: glass balustrade along x=9 and along the stair hole, steel cap
box("MezzGlass", (8.97, 0, H2), (9.02, 10, H2 + 1.05), glass, "glass")
box("MezzCap", (8.95, 0, H2 + 1.05), (9.04, 10, H2 + 1.1), steel, "furn")
box("MezzFascia", (8.95, 0, H1 - 0.02), (9.02, 10, H2), steel, "shell")
box("HoleGlass", (10, 1.38, H2), (15.6, 1.43, H2 + 1.05), glass, "glass")
box("HoleCap", (10, 1.36, H2 + 1.05), (15.6, 1.45, H2 + 1.1), steel, "furn")
# floating stairs along the south wall, rising westward from x 15.6 to the mezzanine
RUN, RISE = 0.33, 0.2
for i in range(17):
    ztop = (i + 1) * RISE; x1 = 15.6 - i * RUN; x0 = x1 - RUN - 0.02
    box(f"Tread{i}", (x0, 0.02, ztop - 0.06), (x1, 1.34, ztop), oak, "stairs", walk=True)
    box(f"TreadLED{i}", (x0 + 0.02, 0.1, ztop - 0.075), (x0 + 0.05, 1.26, ztop - 0.06), led_warm, "stairs", solid=False)
box("StairRail", (9.95, 1.3, 0.9), (15.6, 1.34, 0.95), steel, "stairs", solid=False)  # (visual only; sloped rail below)
bpy.data.objects.remove(bpy.data.objects["StairRail"])
# upstairs bedroom walls
box("BedWallS1", (12, 4.94, H2), (14.4, 5.06, TOP), plaster, "shell")
box("BedWallS2", (15.4, 4.94, H2), (16, 5.06, TOP), plaster, "shell")
box("BedWallS3", (14.4, 4.94, H2 + 2.2), (15.4, 5.06, TOP), plaster, "shell")
box("BedWallW", (11.94, 5.06, H2), (12.06, 10, TOP), plaster, "shell")
# cove LED around the living-room ceiling + under the mezzanine edge
box("CoveW", (0.02, 0.2, TOP - 0.06), (0.06, 9.8, TOP - 0.02), led_warm, "shell", solid=False)
box("CoveS", (0.2, 0.02, TOP - 0.06), (8.9, 0.06, TOP - 0.02), led_warm, "shell", solid=False)
box("MezzUnderLED", (9.05, 0.2, H1 - 0.05), (9.1, 9.8, H1 - 0.02), led_warm, "shell", solid=False)

# ------------------------------------------------------------------ living room
# walnut slat TV wall
for k in range(84):
    y = 2.3 + k * 0.065
    box(f"Slat{k}", (0, y, 0), (0.05, y + 0.042, H1), walnut, "tvwall", solid=False)
box("SlatBack", (0, 2.28, 0), (0.012, 7.8, H1), blackmatte, "tvwall")
box("TV", (0.06, 3.7, 1.15), (0.13, 6.3, 2.62), tvblack, "furn")
box("TVScreen", (0.131, 3.73, 1.18), (0.135, 6.27, 2.59), screen, "screen", solid=False)
box("TVGlow", (0.052, 3.6, 1.05), (0.058, 6.4, 2.72), tvglow, "furn", solid=False)
box("Console", (0.05, 3.1, 0.28), (0.55, 6.9, 0.62), walnut, "furn", bevel=0.01)
box("ConsoleLED", (0.3, 3.15, 0.26), (0.54, 6.85, 0.28), led_warm, "furn", solid=False)
box("Rug", (1.4, 2.6, 0), (4.6, 7.4, 0.015), rugm, "furn", solid=False)
# sofa: a deep L of soft blocks
def sofa_block(nm, a, b):
    o = box(nm, a, b, fabric, "sofa"); soft(o, 0.05); return o
sofa_block("SofaBase", (3.9, 2.7, 0.08), (5.0, 7.3, 0.42))
sofa_block("SofaBack", (4.7, 2.7, 0.42), (5.05, 7.3, 0.95))
sofa_block("ChaiseBase", (2.6, 6.3, 0.08), (3.9, 7.3, 0.42))
sofa_block("ChaiseBack", (2.6, 7.0, 0.42), (5.05, 7.35, 0.9))
sofa_block("ArmS", (3.9, 2.55, 0.08), (5.05, 2.85, 0.68))
for k, yy in enumerate((3.0, 4.1, 5.2)):
    sofa_block(f"Cushion{k}", (3.95, yy, 0.42), (4.72, yy + 1.05, 0.58))
    sofa_block(f"BackPillow{k}", (4.5, yy + 0.05, 0.55), (4.75, yy + 0.95, 1.0))
sofa_block("ChaiseCushion", (2.65, 6.35, 0.42), (3.9, 6.98, 0.56))
for yy in (2.75, 7.2):
    pass
cyl("CoffeeTable", (2.5, 5.0, 0.0), 0.62, 0.36, stonet, "furn", 64)
cyl("SideTable", (4.4, 2.2, 0.0), 0.22, 0.52, brass, "furn", 32)
# arc floor lamp over the sofa
cyl("LampBase", (5.4, 7.7, 0), 0.2, 0.04, stonet, "furn", 32)
cyl("LampPole", (5.4, 7.7, 0.04), 0.015, 2.1, brass, "furn", 12, solid=False)
_a, _b = Vector((5.4, 7.7, 2.14)), Vector((3.95, 6.2, 2.12))
bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.013, depth=(_b - _a).length, location=(_a + _b) / 2)
arm = bpy.context.object; arm.rotation_euler = (_b - _a).to_track_quat("Z", "Y").to_euler(); arm.data.materials.append(brass); tag(arm, "furn", False)
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.3, location=(3.95, 6.2, 1.95))
shade = bpy.context.object; shade.scale = (1, 1, 0.55); shade.location.z = 1.95; shade.data.materials.append(brass); tag(shade, "furn", False)
bpy.ops.object.shade_smooth()
# plants: potted fig trees
def plant(nm, x, y, h=2.0):
    cyl(nm + "Pot", (x, y, 0 if h < 3 else 0), 0.3, 0.55, potm, "furn", 32)
    cyl(nm + "Trunk", (x, y, 0.55), 0.03, h * 0.55, walnut, "furn", 8, solid=False)
    for k in range(70):
        a = random.uniform(0, 2 * math.pi); r = random.uniform(0.05, 0.55); z = random.uniform(0.9, h + 0.35)
        o = sphere(nm + f"Leaf{k}", (x + math.cos(a) * r, y + math.sin(a) * r, z), 0.14, leaf, "plant", (1.0, 0.55, 0.08), seg=12)
        o.rotation_euler = (random.uniform(-.9, .9), random.uniform(-.9, .9), a)
plant("FigA", 0.8, 8.9, 2.1)
plant("FigB", 8.3, 9.3, 1.7)
plant("FigC", 0.8, 1.0, 1.6)
# double-height chandelier: a lit ring on three cables
bpy.ops.mesh.primitive_torus_add(major_radius=1.1, minor_radius=0.035, major_segments=96, minor_segments=12, location=(3.2, 5.0, 4.6))
ring = bpy.context.object; ring.data.materials.append(led_warm); tag(ring, "furn", False)
bpy.ops.mesh.primitive_torus_add(major_radius=1.1, minor_radius=0.045, major_segments=96, minor_segments=12, location=(3.2, 5.0, 4.64))
bpy.context.object.data.materials.append(brass); tag(bpy.context.object, "furn", False)
for k in range(3):
    a = k * 2 * math.pi / 3
    cyl(f"Cable{k}", (3.2 + math.cos(a) * 1.1, 5.0 + math.sin(a) * 1.1, 4.65), 0.004, TOP - 4.65, steel, "furn", 6, solid=False)
# neon sign above the TV wall
bpy.ops.object.text_add(location=(0.07, 5.0, 4.1))
tx = bpy.context.object; tx.data.body = "HEARTBEAT"; tx.data.align_x = "CENTER"; tx.data.size = 0.62; tx.data.extrude = 0.012
tx.rotation_euler = (math.radians(90), 0, math.radians(90)); tx.data.materials.append(led_pink)
bpy.ops.object.convert(target="MESH"); tag(tx, "furn", False)

# ------------------------------------------------------------------ kitchen (under the mezzanine)
box("Cabinets", (15.35, 4.6, 0), (16, 9.8, 0.88), blackmatte, "kitchen", bevel=0.005)
box("Counter", (15.3, 4.6, 0.88), (16, 9.8, 0.92), marble, "kitchen")
box("Backsplash", (15.97, 4.6, 0.92), (16, 9.8, 1.55), marble, "kitchen", solid=False)
box("Uppers", (15.6, 5.6, 1.55), (16, 9.8, H1), blackmatte, "kitchen", bevel=0.005)
box("UnderLED", (15.58, 5.65, 1.53), (15.62, 9.75, 1.55), led_warm, "kitchen", solid=False)
box("Fridge", (15.3, 4.6, 0), (16, 5.55, H1), blackmatte, "kitchen", bevel=0.005)
box("Island", (11.9, 6.3, 0), (13.9, 7.5, 0.88), blackmatte, "kitchen", bevel=0.005)
box("IslandTop", (11.85, 6.25, 0.88), (13.95, 7.55, 0.93), marble, "kitchen")
box("IslandSideA", (11.85, 6.25, 0), (11.9, 7.55, 0.88), marble, "kitchen")
box("IslandSideB", (13.9, 6.25, 0), (13.95, 7.55, 0.88), marble, "kitchen")
for k, yy in enumerate((6.55, 6.9, 7.25)):
    cyl(f"Stool{k}", (11.45, yy, 0), 0.02, 0.62, steel, "kitchen", 8, solid=False)
    cyl(f"StoolSeat{k}", (11.45, yy, 0.62), 0.19, 0.06, walnut, "kitchen", 32)
    cyl(f"StoolFoot{k}", (11.45, yy, 0), 0.2, 0.015, steel, "kitchen", 32, solid=False)
for k, xx in enumerate((12.3, 12.9, 13.5)):
    sphere(f"Pendant{k}", (xx, 6.9, 2.2), 0.13, led_warm, "kitchen")
    cyl(f"PendCord{k}", (xx, 6.9, 2.33), 0.004, H1 - 2.33, steel, "kitchen", 6, solid=False)
for k, (xx, yy) in enumerate([(10.5, 5.5), (10.5, 8.5), (13, 5.2), (13, 8.8), (14.6, 7.0), (12.8, 2.6), (10.4, 2.6)]):
    cyl(f"Downlight{k}", (xx, yy, H1 - 0.012), 0.06, 0.01, led_warm, "kitchen", 24, solid=False)

# ------------------------------------------------------------------ mezzanine: stream setup against the bedroom wall
box("Desk", (11.1, 5.9, H2 + 0.72), (11.93, 8.3, H2 + 0.76), walnut, "stream", bevel=0.005)
for yy in (6.0, 8.15):
    box("DeskLeg", (11.15, yy, H2), (11.88, yy + 0.05, H2 + 0.72), steel, "stream")
box("MonC", (11.72, 6.55, H2 + 0.95), (11.77, 7.65, H2 + 1.58), tvblack, "stream")
box("MonCScreen", (11.715, 6.58, H2 + 0.98), (11.72, 7.62, H2 + 1.55), monitor, "stream", solid=False)
for side, (y0, y1) in enumerate([(5.95, 6.55), (7.65, 8.25)]):
    box(f"MonS{side}", (11.62, y0, H2 + 1.0), (11.67, y1, H2 + 1.42), tvblack, "stream")
    box(f"MonSScr{side}", (11.615, y0 + 0.02, H2 + 1.02), (11.62, y1 - 0.02, H2 + 1.4), monitor, "stream", solid=False)
cyl("MicArm", (11.5, 6.3, H2 + 0.76), 0.012, 0.5, steel, "stream", 8, solid=False)
cyl("Mic", (11.5, 6.3, H2 + 1.26), 0.035, 0.16, steel, "stream", 16, solid=False)
# gaming chair
sofa_block("ChairSeat", (10.4, 6.8, H2 + 0.42), (10.95, 7.4, H2 + 0.55))
sofa_block("ChairBack", (10.25, 6.82, H2 + 0.55), (10.4, 7.38, H2 + 1.45))
cyl("ChairPost", (10.65, 7.1, H2), 0.03, 0.42, steel, "stream", 12, solid=False)
cyl("ChairFoot", (10.65, 7.1, H2), 0.32, 0.03, steel, "stream", 5, solid=False)
# RGB hex panels on the wall above the desk
for k, (yy, zz, m) in enumerate([(6.3, 5.3, led_cyan), (6.7, 5.55, led_purple), (7.1, 5.3, led_pink), (7.5, 5.55, led_cyan), (7.9, 5.3, led_purple), (6.7, 5.05, led_pink), (7.5, 5.05, led_purple)]):
    cyl(f"Hex{k}", (11.93, yy, zz), 0.2, 0.02, m, "stream", 6, solid=False, rot=(0, math.radians(90), 0))
box("DeskLED", (11.9, 5.9, H2 + 0.7), (11.93, 8.3, H2 + 0.72), led_cyan, "stream", solid=False)
# lounge chairs by the railing
for k, yy in enumerate((3.0, 4.4)):
    sofa_block(f"Lounge{k}", (9.5, yy, H2 + 0.05), (10.4, yy + 0.9, H2 + 0.42))
    sofa_block(f"LoungeBack{k}", (10.25, yy, H2 + 0.42), (10.5, yy + 0.9, H2 + 0.85))
plant("FigD", 11.5, 2.2, 1.4)
for o in [o for o in bpy.data.objects if o.name.startswith("FigD")]:
    o.location.z += H2

# ------------------------------------------------------------------ bedroom
box("BedBase", (13.7, 6.4, H2), (16, 8.6, H2 + 0.32), walnut, "bed", bevel=0.01)
o = box("Mattress", (13.75, 6.45, H2 + 0.32), (15.9, 8.55, H2 + 0.58), linen, "bed"); soft(o, 0.06)
o = box("Duvet", (13.72, 6.42, H2 + 0.5), (15.2, 8.58, H2 + 0.64), linen, "bed"); soft(o, 0.07)
for k, yy in enumerate((6.6, 7.55)):
    o = box(f"Pillow{k}", (15.3, yy, H2 + 0.58), (15.75, yy + 0.85, H2 + 0.76), linen, "bed", solid=False); soft(o, 0.06)
o = box("Headboard", (15.85, 6.2, H2), (16, 8.8, H2 + 1.35), fabric, "bed"); soft(o, 0.04)
for k, yy in enumerate((5.75, 8.8)):
    box(f"Nightstand{k}", (15.45, yy, H2), (15.98, yy + 0.45, H2 + 0.5), walnut, "bed", bevel=0.005)
    sphere(f"BedLamp{k}", (15.72, yy + 0.22, H2 + 0.68), 0.14, led_warm, "bed")

# ------------------------------------------------------------------ balcony furniture
for k, xx in enumerate((12.6, 14.2)):
    sofa_block(f"BalcChair{k}", (xx, 11.4, H2), (xx + 0.9, 12.2, H2 + 0.38))
    sofa_block(f"BalcChairBack{k}", (xx, 12.05, H2 + 0.38), (xx + 0.9, 12.3, H2 + 0.8))
cyl("BalcTable", (13.95, 11.2, H2), 0.3, 0.4, stonet, "furn", 32)
plant("FigE", 9.6, 12.0, 1.3)
for o in [o for o in bpy.data.objects if o.name.startswith("FigE")]:
    o.location.z += H2

# ------------------------------------------------------------------ lights (Cycles; baked into the textures)
def light(kind, loc, energy, color=(1, 0.78, 0.55), size=0.1, rot=(0, 0, 0), spot=None):
    ld = bpy.data.lights.new("L", kind); ld.energy = energy; ld.color = color
    if kind in ("POINT", "SPOT"): ld.shadow_soft_size = size
    if kind == "AREA": ld.size = size
    if spot: ld.spot_size = math.radians(spot); ld.spot_blend = 0.6
    o = bpy.data.objects.new("L", ld); o.location = loc; o.rotation_euler = rot; sc.collection.objects.link(o); return o

for k, (xx, yy) in enumerate([(10.5, 5.5), (10.5, 8.5), (13, 5.2), (13, 8.8), (14.6, 7.0), (12.8, 2.6), (10.4, 2.6)]):
    light("SPOT", (xx, yy, H1 - 0.03), 90, size=0.05, spot=70)
for xx in (12.3, 12.9, 13.5):
    light("POINT", (xx, 6.9, 2.2), 25, size=0.12)
light("POINT", (3.95, 6.2, 1.85), 70, size=0.2)                        # arc lamp
light("POINT", (3.2, 5.0, 4.5), 250, (1, 0.8, 0.6), size=1.0)          # chandelier fill
for xx, yy in [(2, 2.5), (6, 2.5), (2, 7.5), (6, 7.5)]:
    light("SPOT", (xx, yy, TOP - 0.03), 110, size=0.05, spot=55)         # living room ceiling spots
for xx, yy in [(10.5, 3.2), (10.5, 8.0), (13.8, 3.0), (14.2, 7.5)]:
    light("SPOT", (xx, yy, TOP - 0.03), 70, size=0.05, spot=60)
for yy in (5.97, 9.02):
    light("POINT", (15.72, yy, H2 + 0.7), 18, size=0.12)
light("POINT", (11.75, 7.1, H2 + 1.3), 20, (0.5, 0.6, 1.0), size=0.4)   # monitor spill
light("AREA", (0.3, 5.0, 1.9), 30, (0.45, 0.4, 0.95), size=1.5, rot=(0, math.radians(90), 0))  # TV spill
for bx in (9.3, 15.7):
    light("POINT", (bx, 10.35, H2 + 2.3), 90, size=0.1)                 # balcony sconces
    box(f"Sconce{bx}", (bx - 0.08, 10.2, H2 + 2.2), (bx + 0.08, 10.26, H2 + 2.45), led_warm, "furn", solid=False)

# world: the city panorama (lights the room through the glass at blue hour)
w = bpy.data.worlds.new("City"); sc.world = w
n, l = w.node_tree.nodes, w.node_tree.links; n.clear()
tc = n.new("ShaderNodeTexCoord"); mp = n.new("ShaderNodeMapping"); mp.inputs["Rotation"].default_value = (0, 0, math.radians(0))
env = n.new("ShaderNodeTexEnvironment"); env.image = bpy.data.images.load(CITY)
bg = n.new("ShaderNodeBackground"); bg.inputs[1].default_value = 1.0
o = n.new("ShaderNodeOutputWorld")
l.new(tc.outputs["Generated"], mp.inputs[0]); l.new(mp.outputs[0], env.inputs[0]); l.new(env.outputs[0], bg.inputs[0]); l.new(bg.outputs[0], o.inputs[0])

bpy.ops.object.select_all(action="DESELECT")
print("BUILT", len(bpy.data.objects), "objects")

# ------------------------------------------------------------------ colliders / walk surfaces (three.js coords: x, z, -y)
def aabb(o):
    dg = bpy.context.evaluated_depsgraph_get(); e = o.evaluated_get(dg)
    cs = [e.matrix_world @ Vector(c) for c in e.bound_box]
    mn = [min(c[i] for c in cs) for i in range(3)]; mx = [max(c[i] for c in cs) for i in range(3)]
    return [round(mn[0], 3), round(mn[2], 3), round(-mx[1], 3), round(mx[0], 3), round(mx[2], 3), round(-mn[1], 3)]
col = {"solids": [], "walk": [], "spawn": [7.2, 0.0, -2.2], "spawnYaw": math.radians(53)}
for ob in bpy.data.objects:
    if ob.type != "MESH": continue
    if ob.get("walk"): col["walk"].append(aabb(ob))
    elif ob.get("solid"): col["solids"].append(aabb(ob))
os.makedirs(OUT, exist_ok=True)
json.dump(col, open(os.path.join(OUT, "colliders.json"), "w"))

if "--preview" in argv:
    cd = bpy.data.cameras.new("Cam"); cd.lens = 18; cam = bpy.data.objects.new("Cam", cd); sc.collection.objects.link(cam)
    cam.location = (8.6, 1.0, 1.65); cam.rotation_euler = (math.radians(86), 0, math.radians(55)); sc.camera = cam
    sc.render.resolution_x, sc.render.resolution_y = 1280, 720; sc.cycles.samples = 128; sc.cycles.use_denoising = True; sc.cycles.denoiser = "OPTIX"
    sc.render.filepath = arg("--preview"); bpy.ops.render.render(write_still=True)

ATLAS = {"floor": "floor", "shell": "shell", "tvwall": "living", "furn": "living", "sofa": "living", "plant": "living",
         "kitchen": "upper", "stairs": "upper", "stream": "upper", "bed": "upper"}
def select_only(objs):
    bpy.ops.object.select_all(action="DESELECT")
    for o in objs: o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]

def strip_hidden_faces():
    rules = {"Floor1": lambda n: n.z < -0.5, "Roof": lambda n: n.z > 0.5, "WallS": lambda n: n.y < -0.5, "WallW": lambda n: n.x < -0.5,
             "WallE1": lambda n: n.x > 0.5, "WallE2": lambda n: n.x > 0.5, "WallE3": lambda n: n.x > 0.5}
    for nm, rule in rules.items():
        o = bpy.data.objects[nm]; bm = bmesh.new(); bm.from_mesh(o.data)
        bmesh.ops.delete(bm, geom=[f for f in bm.faces if rule(f.normal)], context="FACES"); bm.to_mesh(o.data); bm.free()

def bake_all():
    strip_hidden_faces()
    # a diffuse-only bake turns metals black (they have no matte part). Bake them as painted versions of their colour.
    for m in bpy.data.materials:
        b = m.node_tree.nodes.get("Principled BSDF") if m.node_tree else None
        if b and b.inputs["Metallic"].default_value > 0.5:
            c = b.inputs["Base Color"].default_value
            b.inputs["Metallic"].default_value = 0.0
            b.inputs["Base Color"].default_value = (max(c[0] * 0.7, 0.03), max(c[1] * 0.7, 0.03), max(c[2] * 0.7, 0.035), 1)
    meshes = [o for o in bpy.data.objects if o.type == "MESH"]
    select_only(meshes); bpy.ops.object.convert(target="MESH")          # apply bevels/subsurf
    groups = {}
    for o in meshes: groups.setdefault(ATLAS.get(o["g"], o["g"]), []).append(o)
    joined = {}
    for gname, objs in groups.items():
        select_only(objs); bpy.ops.object.join(); j = bpy.context.object; j.name = "BK_" + gname; joined[gname] = j
    sc.cycles.samples = SAMPLES; sc.cycles.use_denoising = False
    sc.render.bake.margin = 16; sc.render.bake.use_pass_direct = True; sc.render.bake.use_pass_indirect = True
    sc.render.bake.use_pass_diffuse = True; sc.render.bake.use_pass_glossy = False; sc.render.bake.use_pass_transmission = False
    sc.render.bake.use_pass_emit = True
    for gname in ("floor", "shell", "living", "upper"):
        j = joined[gname]; select_only([j])
        while len(j.data.uv_layers): j.data.uv_layers.remove(j.data.uv_layers[0])
        j.data.uv_layers.new(name="bake")
        bpy.ops.object.mode_set(mode="EDIT"); bpy.ops.mesh.select_all(action="SELECT")
        bpy.ops.uv.smart_project(angle_limit=math.radians(60), island_margin=0.0025, area_weight=1.0, scale_to_bounds=False)
        bpy.ops.uv.pack_islands(margin=0.0025, rotate=True)
        bpy.ops.object.mode_set(mode="OBJECT")
        img = bpy.data.images.new("atlas_" + gname, RES, RES, float_buffer=True)
        for m in j.data.materials:
            nt = m.node_tree; nd = nt.nodes.get("BAKE") or nt.nodes.new("ShaderNodeTexImage"); nd.name = "BAKE"; nd.image = img
            for x in nt.nodes: x.select = False
            nd.select = True; nt.nodes.active = nd
        t0 = __import__("time").time()
        bpy.ops.object.bake(type="COMBINED")
        print("BAKED", gname, round(__import__("time").time() - t0, 1), "s")
        img.filepath_raw = os.path.join(OUT, f"atlas_{gname}.exr"); img.file_format = "OPEN_EXR"; img.save()
        # swap to one plain material so the GLB carries geometry + UVs only; the page loads the atlas images itself
        j.data.materials.clear(); bm_ = bpy.data.materials.new("BK_" + gname); j.data.materials.append(bm_)
    # glass + screen stay separate and unbaked
    for gname in ("glass", "screen"):
        j = joined[gname]
        while len(j.data.uv_layers) > 1: j.data.uv_layers.remove(j.data.uv_layers[-1])
    for o in [o for o in bpy.data.objects if o.type != "MESH"]: bpy.data.objects.remove(o)
    bpy.ops.export_scene.gltf(filepath=os.path.join(OUT, "loft.glb"), export_format="GLB", export_apply=True,
                              export_lights=False, export_cameras=False, export_materials="EXPORT", export_yup=True)
    print("EXPORTED")

if "--bake" in argv:
    bake_all()
if "--save" in argv:
    bpy.ops.wm.save_as_mainfile(filepath=arg("--save"))
print("LOFT OK")
