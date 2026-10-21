# The Necklace - "The Rusty Anchor", the waterfront dive bar in Rosetown (book ch.1). Real-world scale, metres.
# Built by script in Blender, surfaces baked to texture atlases (colour / roughness / normal), exported as GLB for Unreal.
# blender -b -P rusty_anchor.py -- --out DIR [--res 4096] [--preview still.png] [--bake]
#
# Sizes (all real): room 10 x 7 m, ceiling 3.2 m, bar counter 1.07 m high x 0.65 m deep x 5.6 m long, bar stools 0.76 m seat,
# tables 0.75 m, chairs 0.45 m seat, bottles 0.24-0.33 m, doors 2.1 m, windows sill 0.95 m / head 2.25 m, life ring 0.76 m across.
import bpy, bmesh, math, random, sys, os, json
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def arg(k, d=None): return argv[argv.index(k) + 1] if k in argv else d
OUT = arg("--out", "."); RES = int(arg("--res", "4096")); os.makedirs(OUT, exist_ok=True)
random.seed(11)
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene; sc.unit_settings.system = "METRIC"
sc.render.engine = "CYCLES"
p = bpy.context.preferences.addons["cycles"].preferences; p.compute_device_type = "OPTIX"; p.get_devices()
for d in p.devices: d.use = d.type == "OPTIX"
sc.cycles.device = "GPU"
sc.view_settings.view_transform = "AgX"

W, D, H = 10.0, 7.0, 3.2          # room: x 0..W (west->east), y 0..D (south/harbour -> north/back wall), z up
# ------------------------------------------------------------------ materials (procedural; baked later)
def mat(name, color, rough=0.6, metal=0.0, emit=None, estr=0.0):
    m = bpy.data.materials.new(name); b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*color, 1); b.inputs["Roughness"].default_value = rough; b.inputs["Metallic"].default_value = metal
    if emit: b.inputs["Emission Color"].default_value = (*emit, 1); b.inputs["Emission Strength"].default_value = estr
    return m
def N(m): return m.node_tree.nodes, m.node_tree.links

def planks(name, base, dark, board_w, board_l, axis="X", rough=(0.55, 0.85), grain=30, wear=0.0, paint=None, bump=0.35):
    """boards with gaps, grain, colour variation per board, optional peeling paint over the wood."""
    m = mat(name, base); n, l = N(m); b = n["Principled BSDF"]
    tc = n.new("ShaderNodeTexCoord"); mp = n.new("ShaderNodeMapping"); l.new(tc.outputs["Object"], mp.inputs[0])
    if axis == "Z": mp.inputs["Rotation"].default_value = (0, math.pi / 2, 0)
    if axis == "Y": mp.inputs["Rotation"].default_value = (0, 0, math.pi / 2)
    br = n.new("ShaderNodeTexBrick"); br.inputs["Scale"].default_value = 1; br.inputs["Mortar Size"].default_value = 0.004
    br.inputs["Brick Width"].default_value = board_l; br.inputs["Row Height"].default_value = board_w; br.offset = 0.43; br.offset_frequency = 1
    br.inputs["Color1"].default_value = (1, 1, 1, 1); br.inputs["Color2"].default_value = (0.72, 0.72, 0.72, 1); br.inputs["Mortar"].default_value = (0, 0, 0, 1)
    br.inputs["Mortar Smooth"].default_value = 0.2
    l.new(mp.outputs[0], br.inputs["Vector"])
    wv = n.new("ShaderNodeTexWave"); wv.inputs["Scale"].default_value = grain; wv.inputs["Distortion"].default_value = 3.5; wv.inputs["Detail"].default_value = 4
    wv.bands_direction = "X"; l.new(mp.outputs[0], wv.inputs["Vector"])
    nz = n.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 3.0; nz.inputs["Detail"].default_value = 10; l.new(mp.outputs[0], nz.inputs["Vector"])
    ramp = n.new("ShaderNodeValToRGB"); ramp.color_ramp.elements[0].color = (*dark, 1); ramp.color_ramp.elements[1].color = (*base, 1)
    mix = n.new("ShaderNodeMath"); mix.operation = "MULTIPLY"
    wmix = n.new("ShaderNodeMix"); wmix.data_type = "FLOAT"; wmix.inputs["Factor"].default_value = 0.35
    l.new(nz.outputs["Fac"], wmix.inputs["A"]); l.new(wv.outputs["Fac"], wmix.inputs["B"])
    l.new(wmix.outputs["Result"], mix.inputs[0]); l.new(br.outputs["Color"], mix.inputs[1])    # board brightness * grain
    l.new(mix.outputs[0], ramp.inputs[0])
    col = ramp.outputs[0]; rough_in = br.outputs["Fac"]
    if paint:   # weathered paint: noise mask decides where paint survived; wood shows through where it peeled
        pn = n.new("ShaderNodeTexNoise"); pn.inputs["Scale"].default_value = 2.2; pn.inputs["Detail"].default_value = 14; pn.inputs["Roughness"].default_value = 0.65
        l.new(mp.outputs[0], pn.inputs["Vector"])
        pm = n.new("ShaderNodeValToRGB"); pm.color_ramp.elements[0].position = 0.40; pm.color_ramp.elements[1].position = 0.45
        l.new(pn.outputs["Fac"], pm.inputs[0])
        pv = n.new("ShaderNodeTexNoise"); pv.inputs["Scale"].default_value = 9; l.new(mp.outputs[0], pv.inputs["Vector"])
        pr = n.new("ShaderNodeValToRGB"); pr.color_ramp.elements[0].color = (*[c * 0.78 for c in paint], 1); pr.color_ramp.elements[1].color = (*paint, 1)
        l.new(pv.outputs["Fac"], pr.inputs[0])
        pmix = n.new("ShaderNodeMix"); pmix.data_type = "RGBA"; l.new(pm.outputs[0], pmix.inputs["Factor"])
        l.new(col, pmix.inputs["A"]); l.new(pr.outputs[0], pmix.inputs["B"])
        gap = n.new("ShaderNodeMix"); gap.data_type = "RGBA"; l.new(br.outputs["Fac"], gap.inputs["Factor"])  # gaps stay dark
        gap.inputs["B"].default_value = (*[c * 0.25 for c in dark], 1); l.new(pmix.outputs[2], gap.inputs["A"])   # Fac=1 in the gaps -> dark
        col = gap.outputs[2]
    l.new(col, b.inputs["Base Color"])
    rr = n.new("ShaderNodeMapRange"); rr.inputs["To Min"].default_value = rough[1]; rr.inputs["To Max"].default_value = rough[0]
    l.new(wv.outputs["Fac"], rr.inputs["Value"]); l.new(rr.outputs[0], b.inputs["Roughness"])
    bp = n.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = bump; bp.inputs["Distance"].default_value = 0.0015
    hm = n.new("ShaderNodeMath"); hm.operation = "ADD"; l.new(br.outputs["Fac"], hm.inputs[0]); l.new(wv.outputs["Fac"], hm.inputs[1]); hm.inputs[1].default_value = 0
    hw = n.new("ShaderNodeMath"); hw.operation = "MULTIPLY"; hw.inputs[1].default_value = 0.15; l.new(wv.outputs["Fac"], hw.inputs[0])
    hs = n.new("ShaderNodeMath"); hs.operation = "ADD"; l.new(br.outputs["Fac"], hs.inputs[0]); l.new(hw.outputs[0], hs.inputs[1])
    l.new(hs.outputs[0], bp.inputs["Height"]); l.new(bp.outputs[0], b.inputs["Normal"])
    return m

def grimy(name, c1, c2, scale=6, rough=0.7, metal=0.0, bump=0.15):
    m = mat(name, c1, rough, metal); n, l = N(m); b = n["Principled BSDF"]
    tc = n.new("ShaderNodeTexCoord"); nz = n.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = scale; nz.inputs["Detail"].default_value = 12
    l.new(tc.outputs["Object"], nz.inputs["Vector"])
    r = n.new("ShaderNodeValToRGB"); r.color_ramp.elements[0].color = (*c1, 1); r.color_ramp.elements[1].color = (*c2, 1)
    l.new(nz.outputs["Fac"], r.inputs[0]); l.new(r.outputs[0], b.inputs["Base Color"])
    rr = n.new("ShaderNodeMapRange"); rr.inputs["To Min"].default_value = max(0.05, rough - 0.2); rr.inputs["To Max"].default_value = min(1, rough + 0.2)
    l.new(nz.outputs["Fac"], rr.inputs["Value"]); l.new(rr.outputs[0], b.inputs["Roughness"])
    if bump:
        bp = n.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = bump; bp.inputs["Distance"].default_value = 0.002
        l.new(nz.outputs["Fac"], bp.inputs["Height"]); l.new(bp.outputs[0], b.inputs["Normal"])
    return m

M = {
 "floor": planks("Floor", (0.33, 0.22, 0.13), (0.10, 0.06, 0.035), 0.19, 2.2, rough=(0.45, 0.8), grain=26),
 "wall": planks("WallBoards", (0.36, 0.26, 0.17), (0.12, 0.08, 0.05), 0.16, 3.0, rough=(0.6, 0.9), paint=(0.16, 0.36, 0.36), grain=22, bump=0.5),
 "wainscot": planks("Wainscot", (0.30, 0.19, 0.11), (0.08, 0.05, 0.03), 0.11, 1.4, axis="Z", rough=(0.5, 0.8), paint=(0.52, 0.47, 0.36), grain=30),
 "ceiling": planks("Ceiling", (0.40, 0.31, 0.21), (0.14, 0.10, 0.07), 0.14, 2.6, axis="Y", rough=(0.7, 0.9), grain=20),
 "beam": planks("Beams", (0.20, 0.13, 0.08), (0.05, 0.03, 0.02), 0.25, 4.0, rough=(0.6, 0.9), grain=14, bump=0.6),
 "bartop": planks("BarTop", (0.19, 0.095, 0.045), (0.05, 0.022, 0.01), 0.66, 6.0, rough=(0.22, 0.4), grain=60, bump=0.0),
 "barfront": planks("BarFront", (0.26, 0.15, 0.08), (0.06, 0.035, 0.02), 0.12, 1.2, axis="Z", rough=(0.4, 0.7), grain=28),
 "shelf": planks("Shelves", (0.24, 0.14, 0.08), (0.06, 0.035, 0.02), 0.3, 3.0, rough=(0.4, 0.7), grain=30),
 "stool": planks("StoolWood", (0.22, 0.12, 0.06), (0.06, 0.03, 0.015), 0.4, 0.4, rough=(0.3, 0.6), grain=40, bump=0.1),
 "table": planks("TableWood", (0.34, 0.22, 0.12), (0.09, 0.05, 0.03), 0.12, 0.9, rough=(0.35, 0.7), grain=36),
 "sign": grimy("SignBoard", (0.07, 0.10, 0.10), (0.03, 0.05, 0.05), 5, 0.75),
 "signpaint": grimy("SignPaint", (0.78, 0.66, 0.45), (0.55, 0.45, 0.30), 18, 0.6),
 "mirror": mat("Mirror", (0.8, 0.8, 0.8), 0.06, 1.0),
 "brass": grimy("Brass", (0.62, 0.46, 0.20), (0.34, 0.24, 0.10), 20, 0.35, metal=1.0, bump=0.05),
 "iron": grimy("Iron", (0.10, 0.09, 0.08), (0.30, 0.16, 0.08), 7, 0.7, metal=0.8, bump=0.2),
 "enamel": grimy("LampEnamel", (0.07, 0.20, 0.14), (0.04, 0.10, 0.07), 8, 0.4),
 "ringred": grimy("RingRed", (0.62, 0.10, 0.07), (0.38, 0.08, 0.05), 10, 0.7),
 "ringwhite": grimy("RingWhite", (0.80, 0.76, 0.66), (0.55, 0.50, 0.42), 10, 0.7),
 "rope": grimy("Rope", (0.55, 0.45, 0.30), (0.33, 0.26, 0.16), 40, 0.9, bump=0.4),
 "shutter": planks("Shutters", (0.30, 0.22, 0.14), (0.10, 0.07, 0.05), 0.06, 0.8, rough=(0.6, 0.9), paint=(0.55, 0.28, 0.16), grain=24),
 "fabric": grimy("Cushion", (0.28, 0.10, 0.08), (0.16, 0.06, 0.05), 30, 0.95),
 "bulb": mat("Bulb", (1, 0.8, 0.55), 0.3, emit=(1.0, 0.62, 0.30), estr=12),
 "neon": mat("NeonRum", (1, 0.3, 0.2), 0.3, emit=(1.0, 0.22, 0.12), estr=18),
 "cola": grimy("RumCola", (0.05, 0.022, 0.01), (0.09, 0.04, 0.015), 4, 0.06, bump=0.0),
 "ice": mat("Ice", (0.75, 0.80, 0.82), 0.08),
}
GLASS_COLS = [(0.35, 0.18, 0.05), (0.10, 0.22, 0.10), (0.55, 0.50, 0.40), (0.25, 0.08, 0.04), (0.08, 0.10, 0.06), (0.60, 0.35, 0.10)]
M_BOTTLE = [mat("BottleGlass%d" % i, c, 0.08) for i, c in enumerate(GLASS_COLS)]
M_LABEL = [grimy("Label%d" % i, c, tuple(x * 0.7 for x in c), 30, 0.7) for i, c in enumerate([(0.85, 0.80, 0.65), (0.75, 0.15, 0.10), (0.15, 0.15, 0.15), (0.85, 0.70, 0.30)])]

# ------------------------------------------------------------------ helpers
def tag(o, g): o["g"] = g; return o
def box(name, a, b, m, g, bevel=0.0, seg=2):
    c = [(a[i] + b[i]) / 2 for i in range(3)]
    bpy.ops.mesh.primitive_cube_add(size=1, location=c); o = bpy.context.object; o.name = name
    o.scale = [abs(b[i] - a[i]) for i in range(3)]; bpy.ops.object.transform_apply(scale=True)
    o.data.materials.append(m)
    if bevel: bv = o.modifiers.new("bv", "BEVEL"); bv.width = bevel; bv.segments = seg; bv.limit_method = "ANGLE"
    return tag(o, g)
def cyl(name, c, r, h, m, g, verts=32, rot=None, r2=None):
    if r2 is None: bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=h, location=(0, 0, 0))
    else: bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=r, radius2=r2, depth=h, location=(0, 0, 0))
    o = bpy.context.object; o.name = name; o.data.materials.append(m)
    if rot: o.rotation_euler = rot
    o.location = Vector(c) + (Vector((0, 0, h / 2)) if not rot else Vector((0, 0, 0)))
    bpy.ops.object.shade_smooth(); return tag(o, g)
def lathe(name, prof, loc, m, g, steps=32):
    """revolve a (radius, z) profile around Z - bottles, glasses, lamp shades."""
    bm = bmesh.new(); vs = [bm.verts.new((r, 0, z)) for r, z in prof]
    for i in range(len(vs) - 1): bm.edges.new((vs[i], vs[i + 1]))
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); bpy.context.collection.objects.link(o)
    s = o.modifiers.new("lathe", "SCREW"); s.steps = steps; s.render_steps = steps; s.use_merge_vertices = True; s.use_normal_calculate = True
    o.location = loc; o.data.materials.append(m)
    for f in o.data.polygons: f.use_smooth = True
    return tag(o, g)
def torus(name, loc, R, r, m, g, rot=(0, 0, 0), seg=48):
    bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=r, major_segments=seg, minor_segments=16, location=loc, rotation=rot)
    o = bpy.context.object; o.name = name; o.data.materials.append(m); bpy.ops.object.shade_smooth(); return tag(o, g)
def text(name, s, loc, size, m, g, rot=(math.pi / 2, 0, 0), depth=0.012):
    bpy.ops.object.text_add(location=loc, rotation=rot); o = bpy.context.object; o.name = name
    o.data.body = s; o.data.size = size; o.data.extrude = depth; o.data.align_x = "CENTER"; o.data.align_y = "CENTER"
    o.data.bevel_depth = 0.002; o.data.materials.append(m); return tag(o, g)

LIGHTS = []   # handed to Unreal: real lamps become real lights there
def lamp(x, y, drop=0.95):
    z = H - drop
    cyl("Cord_%g" % x, (x, y, z + 0.22), 0.005, drop - 0.22, M["iron"], "metal", verts=8)
    lathe("Shade_%g" % x, [(0.03, 0.26), (0.045, 0.24), (0.07, 0.20), (0.16, 0.06), (0.20, 0.0), (0.195, -0.005), (0.15, 0.055), (0.06, 0.19), (0.025, 0.24), (0.0, 0.245)], (x, y, z), M["enamel"], "metal")
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.045, location=(x, y, z + 0.035), segments=24, ring_count=12); b = bpy.context.object; b.name = "Bulb_%g" % x
    b.data.materials.append(M["bulb"]); bpy.ops.object.shade_smooth(); tag(b, "emit")
    LIGHTS.append({"type": "pendant", "pos": [x, y, z + 0.02]})

# ------------------------------------------------------------------ shell
box("Floor", (0, 0, -0.1), (W, D, 0), M["floor"], "floor")
box("Ceiling", (0, 0, H), (W, D, H + 0.1), M["ceiling"], "floor")
for i in range(6):   # heavy cross beams
    x = 0.8 + i * 1.7; box("Beam%d" % i, (x - 0.11, 0, H - 0.26), (x + 0.11, D, H), M["beam"], "shell", bevel=0.01)
box("BeamLong", (0, 3.3, H - 0.3), (W, 3.52, H - 0.26), M["beam"], "shell", bevel=0.01)
# walls: back (north) solid, east solid with door, west with windows, south = harbour side, big open shuttered windows
def wall_with_holes(name, axis, pos, length, holes, thick=0.14):
    """a wall along X (axis='x', at y=pos) or along Y (axis='y', at x=pos) with rectangular openings (start, end, bottom, top)."""
    segs, last = [], 0.0
    for (s, e, zb, zt) in sorted(holes):
        segs.append((last, s, 0, H)); segs.append((s, e, 0, zb)); segs.append((s, e, zt, H)); last = e
    segs.append((last, length, 0, H))
    for i, (s, e, zb, zt) in enumerate(segs):
        if e - s < 1e-4 or zt - zb < 1e-4: continue
        for (mname, z0, z1) in (("wainscot", zb, min(zt, 1.0)), ("wall", max(zb, 1.0), zt)):
            if z1 - z0 < 1e-4: continue
            if axis == "x": box(f"{name}_{i}_{mname}", (s, pos - thick / 2, z0), (e, pos + thick / 2, z1), M[mname], "shell")
            else: box(f"{name}_{i}_{mname}", (pos - thick / 2, s, z0), (pos + thick / 2, e, z1), M[mname], "shell")
WIN = [(1.2, 2.8, 0.95, 2.25), (4.2, 5.8, 0.95, 2.25), (7.2, 8.8, 0.95, 2.25)]
wall_with_holes("WallS", "x", 0.0, W, WIN)                    # harbour side: three big open windows
wall_with_holes("WallN", "x", D, W, [])
wall_with_holes("WallW", "y", 0.0, D, [(1.0, 2.6, 0.95, 2.25)])
wall_with_holes("WallE", "y", W, D, [(1.2, 2.3, 0.0, 2.1)])   # door out to the street
for (s, e, zb, zt) in WIN:   # frames + open shutters folded back against the wall
    box("SillS%g" % s, (s - 0.05, -0.12, zb - 0.05), (e + 0.05, 0.1, zb), M["beam"], "shell")
    box("HeadS%g" % s, (s - 0.05, -0.1, zt), (e + 0.05, 0.1, zt + 0.08), M["beam"], "shell")
    for side, x0 in (("L", s - 0.78), ("R", e + 0.02)):
        box(f"Shut{side}{s}", (x0, -0.12, zb), (x0 + 0.76, -0.09, zt), M["shutter"], "props")
        for k in range(12):
            z = zb + 0.08 + k * (zt - zb - 0.16) / 11
            box(f"Slat{side}{s}_{k}", (x0 + 0.05, -0.15, z), (x0 + 0.71, -0.11, z + 0.03), M["shutter"], "props")
box("SillW", (-0.1, 1.0, 0.9), (0.12, 2.6, 0.95), M["beam"], "shell")
box("DoorFrameE", (W - 0.1, 1.12, 2.1), (W + 0.1, 2.38, 2.2), M["beam"], "shell")
# the door stands open into the room, swung against the wall
box("Door", (W - 0.9, 2.32, 0.01), (W - 0.1, 2.36, 2.08), M["shutter"], "props", bevel=0.005)

# ------------------------------------------------------------------ the bar (runs east-west, patrons on the south side)
BX0, BX1, BY0, BY1 = 2.6, 8.2, 4.35, 5.0          # counter footprint
box("BarBody", (BX0, BY0 + 0.05, 0), (BX1, BY1, 1.02), M["barfront"], "bar")
box("BarTop", (BX0 - 0.06, BY0 - 0.06, 1.02), (BX1 + 0.06, BY1 + 0.04, 1.07), M["bartop"], "bar", bevel=0.012, seg=3)
box("BarKick", (BX0, BY0 + 0.02, 0), (BX1, BY0 + 0.08, 0.12), M["beam"], "bar")
for k in range(9):   # vertical posts on the front panel
    x = BX0 + 0.02 + k * (BX1 - BX0 - 0.04) / 8; box("BarPost%d" % k, (x - 0.04, BY0 + 0.02, 0.12), (x + 0.04, BY0 + 0.07, 1.0), M["beam"], "bar")
# brass foot rail with brackets, 0.2 m up
cyl("FootRail", ((BX0 + BX1) / 2, BY0 - 0.14, 0.2), 0.025, BX1 - BX0 - 0.1, M["brass"], "metal", rot=(0, math.pi / 2, 0))
for k in range(6):
    x = BX0 + 0.1 + k * (BX1 - BX0 - 0.2) / 5; box("RailBr%d" % k, (x - 0.012, BY0 - 0.14, 0.19), (x + 0.012, BY0 + 0.02, 0.21), M["brass"], "metal")
# back bar: low cabinet, three shelves, mirror, sign
BB = D - 0.07
box("BackCab", (BX0 - 0.2, BB - 0.55, 0), (BX1 + 0.2, BB, 0.95), M["barfront"], "bar")
box("BackCabTop", (BX0 - 0.22, BB - 0.58, 0.95), (BX1 + 0.22, BB, 0.99), M["bartop"], "bar", bevel=0.008)
box("Mirror", (BX0 + 0.3, BB - 0.03, 1.05), (BX1 - 0.3, BB - 0.01, 2.2), M["mirror"], "metal")
for k, z in enumerate((1.28, 1.62, 1.96)):
    box("Shelf%d" % k, (BX0 - 0.1, BB - 0.26, z), (BX1 + 0.1, BB - 0.02, z + 0.035), M["shelf"], "bar", bevel=0.004)
for x in (BX0 - 0.12, (BX0 + BX1) / 2, BX1 + 0.08):
    box("Upright%g" % x, (x, BB - 0.27, 0.99), (x + 0.05, BB - 0.01, 2.3), M["shelf"], "bar")
box("SignBoard", (3.7, BB - 0.06, 2.34), (7.1, BB - 0.02, 2.86), M["sign"], "props", bevel=0.01)
text("SignText", "THE RUSTY ANCHOR", (5.4, BB - 0.075, 2.62), 0.24, M["signpaint"], "props")
text("SignSub", "ROSETOWN  ·  SINCE 1961", (5.4, BB - 0.075, 2.42), 0.075, M["signpaint"], "props")
text("NeonRum", "RUM", (8.9, BB - 0.03, 2.2), 0.26, M["neon"], "emit", depth=0.02)
# bottles on the back bar: real bottle sizes (0.24 - 0.33 m), lathed so the necks and shoulders read
def bottle(i, x, y, z):
    h = random.uniform(0.24, 0.33); r = random.uniform(0.034, 0.045); kind = random.random()
    neck = 0.012 if kind < 0.7 else 0.016; sh = h * random.uniform(0.55, 0.68)
    prof = [(0, 0), (r * 0.96, 0), (r, 0.01), (r, sh), (r * 0.8, sh + 0.02), (neck * 1.3, h - 0.07), (neck, h - 0.05), (neck, h - 0.005), (neck * 0.8, h), (0, h)]
    lathe("Bottle%d" % i, prof, (x, y, z), M_BOTTLE[i % len(M_BOTTLE)], "bottles", steps=24)
    if random.random() < 0.8:
        lh = sh * random.uniform(0.35, 0.6)
        lathe("Label%d" % i, [(r + 0.0015, sh * 0.25), (r + 0.0015, sh * 0.25 + lh)], (x, y, z), random.choice(M_LABEL), "bottles", steps=24)
bi = 0
for z in (0.99, 1.315, 1.655, 1.995):
    x = BX0 - 0.02
    while x < BX1 - 0.02:
        x += random.uniform(0.09, 0.13)
        if random.random() < 0.12: x += 0.2; continue
        bottle(bi, x, BB - (0.4 if z < 1.0 else 0.13) + random.uniform(-0.02, 0.02), z); bi += 1
# stools on the patron side (seat 0.76 m, 0.38 m across)
def stool(i, x, y):
    cyl("StoolSeat%d" % i, (x, y, 0.72), 0.19, 0.045, M["stool"], "props", verts=40)
    cyl("StoolCush%d" % i, (x, y, 0.765), 0.17, 0.02, M["fabric"], "props", verts=40)
    for k in range(4):
        a = k * math.pi / 2 + math.pi / 4; dx, dy = math.cos(a), math.sin(a)
        leg = cyl(f"StoolLeg{i}_{k}", (x + dx * 0.15, y + dy * 0.15, 0.36), 0.018, 0.74, M["stool"], "props", verts=12,
                  rot=(math.radians(-5) * dy * -1, math.radians(5) * dx, 0))
        leg.location = (x + dx * 0.16, y + dy * 0.16, 0.36)
    torus("StoolRing%d" % i, (x, y, 0.28), 0.17, 0.011, M["iron"], "metal")
STOOLS = [(3.1 + k * 0.62, 4.0) for k in range(9)]
for i, (x, y) in enumerate(STOOLS):
    if i != 4: stool(i, x, y)   # stool 4 is Jalen's: in the shot he's on it, the camera never sees below the counter
stool(4, STOOLS[4][0], STOOLS[4][1])
# Jalen's drink: a highball of rum and coke with ice, on a coaster (glass 0.14 m tall)
JX = STOOLS[4][0]
lathe("Coaster", [(0, 0), (0.05, 0), (0.05, 0.004), (0, 0.004)], (JX + 0.30, BY0 + 0.07, 1.07), M["ringwhite"], "props")
lathe("Highball", [(0, 0), (0.036, 0), (0.038, 0.004), (0.04, 0.14), (0.0385, 0.14), (0.0372, 0.118), (0, 0.118)], (JX + 0.30, BY0 + 0.07, 1.074), M["cola"], "bottles")
for k in range(3):
    box("Ice%d" % k, (JX + 0.28 + k * 0.014, BY0 + 0.05 + k * 0.01, 1.186), (JX + 0.303 + k * 0.014, BY0 + 0.073 + k * 0.01, 1.205), M["ice"], "bottles", bevel=0.004)
# tables + chairs on the harbour side
def chair(nm, x, y, rotz):
    parts = []
    bpy.ops.object.empty_add(location=(x, y, 0)); root = bpy.context.object
    parts.append(box(nm + "_seat", (-0.21, -0.2, 0.43), (0.21, 0.2, 0.46), M["table"], "props", bevel=0.008))
    for sx in (-0.18, 0.18):
        for sy in (-0.17, 0.17):
            top = 0.95 if sy > 0 else 0.43
            parts.append(box(nm + "_leg%d" % len(parts), (sx - 0.016, sy - 0.016, 0), (sx + 0.016, sy + 0.016, top), M["table"], "props", bevel=0.004))
    for k, z in enumerate((0.62, 0.74, 0.86)):
        parts.append(box(nm + "_slat%d" % k, (-0.18, 0.165, z), (0.18, 0.18, z + 0.05), M["table"], "props", bevel=0.004))
    parts.append(box(nm + "_rail", (-0.18, -0.17, 0.12), (0.18, -0.155, 0.15), M["table"], "props"))
    for o in parts: o.parent = root
    root.rotation_euler = (0, 0, rotz)
def table(i, x, y):
    cyl("TableTop%d" % i, (x, y, 0.72), 0.4, 0.035, M["table"], "props", verts=48)
    cyl("TablePed%d" % i, (x, y, 0.05), 0.045, 0.67, M["iron"], "metal", verts=16)
    cyl("TableFoot%d" % i, (x, y, 0.0), 0.26, 0.05, M["iron"], "metal", verts=32, r2=0.2)
    for k in range(3):
        a = k * 2 * math.pi / 3 + i; chair(f"Chair{i}_{k}", x + math.cos(a) * 0.62, y + math.sin(a) * 0.62, a + math.pi / 2)
for i, (x, y) in enumerate([(1.9, 1.5), (4.9, 1.6), (8.0, 1.5), (1.5, 3.4)]): table(i, x, y)
# nautical things the port would have: a life ring, a ship's wheel, crossed oars, a coil of rope, a net of floats
ring = mat("LifeRing", (0.8, 0.76, 0.66), 0.7); n, l = N(ring); b = n["Principled BSDF"]   # four red bands, four white
tc = n.new("ShaderNodeTexCoord"); gt = n.new("ShaderNodeTexGradient"); gt.gradient_type = "RADIAL"; l.new(tc.outputs["Object"], gt.inputs["Vector"])
m4 = n.new("ShaderNodeMath"); m4.operation = "MULTIPLY"; m4.inputs[1].default_value = 4; l.new(gt.outputs["Fac"], m4.inputs[0])
fr = n.new("ShaderNodeMath"); fr.operation = "FRACT"; l.new(m4.outputs[0], fr.inputs[0])
st = n.new("ShaderNodeMath"); st.operation = "GREATER_THAN"; st.inputs[1].default_value = 0.5; l.new(fr.outputs[0], st.inputs[0])
cm = n.new("ShaderNodeMix"); cm.data_type = "RGBA"; l.new(st.outputs[0], cm.inputs["Factor"])
cm.inputs["A"].default_value = (0.78, 0.74, 0.64, 1); cm.inputs["B"].default_value = (0.58, 0.09, 0.06, 1); l.new(cm.outputs[2], b.inputs["Base Color"])
torus("LifeRing", (0.08, 4.2, 1.9), 0.3, 0.075, ring, "props", rot=(0, math.pi / 2, 0))
torus("Wheel", (0.09, 5.8, 1.75), 0.34, 0.03, M["beam"], "props", rot=(0, math.pi / 2, 0))
for k in range(8):
    a = k * math.pi / 4
    cyl("Spoke%d" % k, (0.1, 5.8, 1.75), 0.018, 0.9, M["beam"], "props", verts=10, rot=(a, 0, 0))
    bpy.context.object.location = (0.1, 5.8, 1.75)
cyl("WheelHub", (0.1, 5.8, 1.75), 0.06, 0.08, M["brass"], "metal", rot=(0, math.pi / 2, 0)); bpy.context.object.location = (0.1, 5.8, 1.75)
for k, a in enumerate((0.5, -0.5)):
    cyl("Oar%d" % k, (W - 0.09, 4.6, 1.9), 0.025, 2.4, M["table"], "props", verts=12, rot=(a, 0, 0)); bpy.context.object.location = (W - 0.09, 4.6, 1.9)
for k in range(5): torus("Rope%d" % k, (W - 0.35, 6.4, 0.05 + k * 0.045), 0.22 - k * 0.012, 0.022, M["rope"], "props")
# fans + lamps
for x in (2.5, 7.5):
    cyl("FanRod%g" % x, (x, 2.0, H - 0.5), 0.012, 0.5, M["iron"], "metal", verts=8)
    cyl("FanHub%g" % x, (x, 2.0, H - 0.58), 0.08, 0.1, M["iron"], "metal")
    for k in range(4):
        a = k * math.pi / 2 + (0.3 if x > 5 else 0.0)
        b = box(f"Blade{x}_{k}", (-0.06, 0.1, -0.006), (0.06, 0.62, 0.006), M["table"], "props"); b.location = (x, 2.0, H - 0.53); b.rotation_euler = (0.08, 0, a)
for x in (3.3, 4.7, 6.1, 7.5): lamp(x, 4.65, 0.95)          # over the bar
for (x, y) in [(1.9, 1.5), (4.9, 1.6), (8.0, 1.5)]: lamp(x, y, 1.1)   # over the tables
LIGHTS.append({"type": "neon", "pos": [8.9, BB - 0.15, 2.2]})
LIGHTS.append({"type": "backbar", "pos": [5.4, BB - 0.35, 2.28]})

# ------------------------------------------------------------------ outside: the night harbour seen through the windows
harb = mat("Harbour", (0, 0, 0), 1.0); n, l = N(harb); b = n["Principled BSDF"]
img = bpy.data.images.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), "harbour_night.png")) if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), "harbour_night.png")) else None
if img:
    t = n.new("ShaderNodeTexImage"); t.image = img; l.new(t.outputs["Color"], b.inputs["Emission Color"]); b.inputs["Emission Strength"].default_value = 1.0
    b.inputs["Base Color"].default_value = (0, 0, 0, 1)
bpy.ops.mesh.primitive_plane_add(size=1, location=(W / 2, -22, 3.1)); hp = bpy.context.object; hp.name = "HarbourView"
hp.scale = (60, 15, 1); hp.rotation_euler = (math.pi / 2, 0, math.pi); bpy.ops.object.transform_apply(rotation=True, scale=True)
hp.data.materials.append(harb); tag(hp, "harbour")
bpy.ops.mesh.primitive_plane_add(size=1, location=(W / 2, -10, -1.2)); wp = bpy.context.object; wp.name = "Water"; wp.scale = (60, 24, 1)
bpy.ops.object.transform_apply(scale=True); wp.data.materials.append(mat("WaterNight", (0.004, 0.008, 0.012), 0.04)); tag(wp, "water")
box("Dock", (-2, -3.2, -0.25), (W + 2, 0, -0.1), M["floor"], "shell")

with open(os.path.join(OUT, "lights.json"), "w") as f:
    json.dump({"units": "metres, Blender axes (x east, y north, z up)", "stools": STOOLS, "jalen_stool": STOOLS[4], "bar": [BX0, BX1, BY0, BY1],
               "lights": LIGHTS, "room": [W, D, H]}, f, indent=1)

# ------------------------------------------------------------------ preview render (Cycles, lamps as real lights) to check the look
def preview(path):
    for L_ in LIGHTS:
        if L_["type"] == "pendant":
            bpy.ops.object.light_add(type="POINT", location=L_["pos"]); li = bpy.context.object; li.data.energy = 120; li.data.color = (1, 0.72, 0.45); li.data.shadow_soft_size = 0.05
    bpy.ops.object.light_add(type="AREA", location=(5.4, 6.4, 2.3)); li = bpy.context.object; li.data.energy = 80; li.data.size = 4; li.data.color = (1, 0.6, 0.35); li.rotation_euler = (math.radians(100), 0, 0)
    w = bpy.data.worlds.new("w"); sc.world = w; w.node_tree.nodes["Background"].inputs[0].default_value = (0.01, 0.015, 0.03, 1)
    bpy.ops.object.camera_add(location=(JX - 0.1, 5.7, 1.42), rotation=(math.radians(82), 0, math.radians(180)))
    cam = bpy.context.object; cam.data.lens = 35; sc.camera = cam
    sc.render.resolution_x, sc.render.resolution_y = 1600, 900; sc.cycles.samples = 128; sc.cycles.use_denoising = True
    sc.render.filepath = path; bpy.ops.render.render(write_still=True)
if arg("--preview"): preview(arg("--preview"))

# ------------------------------------------------------------------ bake + export
def select_only(objs):
    bpy.ops.object.select_all(action="DESELECT")
    for o in objs: o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
ATLAS_RES = {"floor": RES, "shell": RES, "bar": RES, "props": RES, "bottles": RES // 2, "metal": RES // 2}
def bake_group(j, gname, res):
    select_only([j])
    while len(j.data.uv_layers): j.data.uv_layers.remove(j.data.uv_layers[0])
    j.data.uv_layers.new(name="UV")
    bpy.ops.object.mode_set(mode="EDIT"); bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.smart_project(angle_limit=math.radians(55), island_margin=0.002, area_weight=1.0, scale_to_bounds=False)
    bpy.ops.uv.pack_islands(margin=0.002, rotate=True); bpy.ops.object.mode_set(mode="OBJECT")
    out = {}
    for kind, btype in (("BC", "DIFFUSE"), ("R", "ROUGHNESS"), ("N", "NORMAL"), ("M", "EMIT")):
        img = bpy.data.images.new(f"{gname}_{kind}", res, res, float_buffer=False, is_data=kind != "BC")
        saved = {}
        for m in j.data.materials:
            nt = m.node_tree; nd = nt.nodes.get("BAKE") or nt.nodes.new("ShaderNodeTexImage"); nd.name = "BAKE"; nd.image = img
            for x in nt.nodes: x.select = False
            nd.select = True; nt.nodes.active = nd
            if kind == "M":   # metallic has no bake type: route it through emission for this pass
                b = nt.nodes["Principled BSDF"]; saved[m.name] = [lk for lk in nt.links if lk.to_socket == b.inputs["Emission Color"]]
                for lk in saved[m.name]: nt.links.remove(lk)
                mv = b.inputs["Metallic"].default_value; b.inputs["Emission Color"].default_value = (mv, mv, mv, 1)
                saved[m.name + "_s"] = b.inputs["Emission Strength"].default_value; b.inputs["Emission Strength"].default_value = 1.0
        if kind == "BC":
            sc.render.bake.use_pass_direct = False; sc.render.bake.use_pass_indirect = False; sc.render.bake.use_pass_color = True
        sc.cycles.samples = 4
        bpy.ops.object.bake(type=btype, margin=8)
        if kind == "M":
            for m in j.data.materials:
                b = m.node_tree.nodes["Principled BSDF"]; b.inputs["Emission Strength"].default_value = saved[m.name + "_s"]
        path = os.path.join(OUT, f"{gname}_{kind}.png"); img.filepath_raw = path; img.file_format = "PNG"; img.save(); out[kind] = img
        print("BAKED", gname, kind, flush=True)
    # one clean material per group with the baked maps, which glTF (and so Unreal) understands
    nm = bpy.data.materials.new("RA_" + gname); nt = nm.node_tree; b = nt.nodes["Principled BSDF"]
    t = nt.nodes.new("ShaderNodeTexImage"); t.image = out["BC"]; nt.links.new(t.outputs["Color"], b.inputs["Base Color"])
    r = nt.nodes.new("ShaderNodeTexImage"); r.image = out["R"]; r.image.colorspace_settings.name = "Non-Color"; nt.links.new(r.outputs["Color"], b.inputs["Roughness"])
    mm = nt.nodes.new("ShaderNodeTexImage"); mm.image = out["M"]; mm.image.colorspace_settings.name = "Non-Color"; nt.links.new(mm.outputs["Color"], b.inputs["Metallic"])
    nn = nt.nodes.new("ShaderNodeTexImage"); nn.image = out["N"]; nn.image.colorspace_settings.name = "Non-Color"
    nmap = nt.nodes.new("ShaderNodeNormalMap"); nt.links.new(nn.outputs["Color"], nmap.inputs["Color"]); nt.links.new(nmap.outputs[0], b.inputs["Normal"])
    j.data.materials.clear(); j.data.materials.append(nm)

if "--bake" in argv:
    for o in [o for o in bpy.data.objects if o.type == "FONT"]:
        select_only([o]); bpy.ops.object.convert(target="MESH")
    meshes = [o for o in bpy.data.objects if o.type == "MESH"]
    select_only(meshes); bpy.ops.object.convert(target="MESH")
    for o in meshes:   # un-parent (chairs) keeping world positions, then freeze transforms so every piece sits at the world origin
        if o.parent:
            mw = o.matrix_world.copy(); o.parent = None; o.matrix_world = mw
    select_only(meshes); bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    for o in [o for o in bpy.data.objects if o.type == "EMPTY"]: bpy.data.objects.remove(o)
    groups = {}
    for o in meshes: groups.setdefault(o["g"], []).append(o)
    joined = {}
    for g, objs in groups.items():
        select_only(objs); bpy.ops.object.join(); j = bpy.context.object; j.name = "RA_" + g; joined[g] = j
    sc.render.bake.margin = 8
    for g, res in ATLAS_RES.items():
        if g in joined: bake_group(joined[g], g, res)
    bpy.ops.export_scene.gltf(filepath=os.path.join(OUT, "rusty_anchor.glb"), export_format="GLB", export_apply=True,
                              export_lights=False, export_cameras=False, export_materials="EXPORT", export_yup=True, export_image_format="AUTO")
    print("EXPORTED", flush=True)
if arg("--save"): bpy.ops.wm.save_as_mainfile(filepath=arg("--save"))
print("RUSTY ANCHOR OK", flush=True)
