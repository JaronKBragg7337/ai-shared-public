# Heartbeat News - concept render of the studio at film quality (Blender/Cycles). Same layout as news/studio3d.js:
# curved anchor desk (R 4 m, top 0.80 m), LED wall 7 x 3 m, truss, portrait monitors. Three.js (x, y, z) -> Blender (x, -z, y).
# blender -b -P newsroom.py -- wall.png out.png [samples]
import bpy, math, sys, random
from mathutils import Vector
argv = sys.argv[sys.argv.index("--") + 1:]
WALL_IMG, OUT = argv[0], argv[1]; SAMPLES = int(argv[2]) if len(argv) > 2 else 256
random.seed(3)
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = "CYCLES"
p = bpy.context.preferences.addons["cycles"].preferences; p.compute_device_type = "OPTIX"; p.get_devices()
for d in p.devices: d.use = d.type == "OPTIX"
sc.cycles.device = "GPU"; sc.cycles.samples = SAMPLES; sc.cycles.use_denoising = True; sc.cycles.denoiser = "OPTIX"
sc.render.resolution_x, sc.render.resolution_y = 1920, 1080
sc.view_settings.view_transform = "AgX"; sc.view_settings.look = "AgX - Medium High Contrast"; sc.view_settings.exposure = 0.0
w = bpy.data.worlds.new("W"); sc.world = w; w.node_tree.nodes["Background"].inputs[0].default_value = (0.004, 0.006, 0.01, 1); w.node_tree.nodes["Background"].inputs[1].default_value = 1

def mat(name, color=(0.5, 0.5, 0.5), rough=0.5, metal=0.0, emit=None, estr=0.0, coat=0.0):
    m = bpy.data.materials.new(name); b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*color, 1); b.inputs["Roughness"].default_value = rough; b.inputs["Metallic"].default_value = metal
    b.inputs["Coat Weight"].default_value = coat
    if emit: b.inputs["Emission Color"].default_value = (*emit, 1); b.inputs["Emission Strength"].default_value = estr
    return m

def T(x, y, z): return (x, -z, y)           # three.js -> blender

def box(a, b, m, bevel=0.0):
    c = [(a[i] + b[i]) / 2 for i in range(3)]
    bpy.ops.mesh.primitive_cube_add(size=1, location=c); o = bpy.context.object
    o.scale = [abs(b[i] - a[i]) for i in range(3)]; bpy.ops.object.transform_apply(scale=True); o.data.materials.append(m)
    if bevel: bv = o.modifiers.new("b", "BEVEL"); bv.width = bevel; bv.segments = 3
    return o

# ---- floor: dark polished epoxy tiles (reflective, roughness varies per tile) ----
floor_m = bpy.data.materials.new("Epoxy"); n = floor_m.node_tree.nodes; l = floor_m.node_tree.links; bs = n["Principled BSDF"]
bs.inputs["Base Color"].default_value = (0.012, 0.015, 0.022, 1); bs.inputs["Metallic"].default_value = 0.1
tc = n.new("ShaderNodeTexCoord"); br = n.new("ShaderNodeTexBrick"); br.inputs["Scale"].default_value = 0.5; br.inputs["Mortar Size"].default_value = 0.004
br.inputs["Brick Width"].default_value = 1.0; br.inputs["Row Height"].default_value = 1.0; br.offset = 0
br.inputs["Color1"].default_value = (0.1, 0.1, 0.1, 1); br.inputs["Color2"].default_value = (0.2, 0.2, 0.2, 1); br.inputs["Mortar"].default_value = (0.7, 0.7, 0.7, 1)
l.new(tc.outputs["Object"], br.inputs["Vector"])
nz = n.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 3; l.new(tc.outputs["Object"], nz.inputs["Vector"])
mx = n.new("ShaderNodeMath"); mx.operation = "MULTIPLY_ADD"; mx.inputs[1].default_value = 0.25
l.new(nz.outputs["Fac"], mx.inputs[0]); l.new(br.outputs["Color"], mx.inputs[2])
rr = n.new("ShaderNodeMapRange"); rr.inputs["To Min"].default_value = 0.05; rr.inputs["To Max"].default_value = 0.3
l.new(mx.outputs[0], rr.inputs["Value"]); l.new(rr.outputs["Result"], bs.inputs["Roughness"])
bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 0, 0)); bpy.context.object.data.materials.append(floor_m)

# ---- the LED wall with a real news graphic ----
wall_m = bpy.data.materials.new("LEDWall"); n = wall_m.node_tree.nodes; l = wall_m.node_tree.links; n.clear()
img = n.new("ShaderNodeTexImage"); img.image = bpy.data.images.load(WALL_IMG)
em = n.new("ShaderNodeEmission"); em.inputs["Strength"].default_value = 0.9
# LED pixel grid: darken cabinet seams + pixel pitch
tc = n.new("ShaderNodeTexCoord"); grid = n.new("ShaderNodeTexBrick"); grid.inputs["Scale"].default_value = 1.0
grid.inputs["Brick Width"].default_value = 1 / 14; grid.inputs["Row Height"].default_value = 1 / 6; grid.inputs["Mortar Size"].default_value = 0.0006; grid.offset = 0
grid.inputs["Color1"].default_value = grid.inputs["Color2"].default_value = (1, 1, 1, 1); grid.inputs["Mortar"].default_value = (0.35, 0.35, 0.35, 1)
l.new(tc.outputs["UV"], grid.inputs["Vector"]); l.new(tc.outputs["UV"], img.inputs["Vector"])
mul = n.new("ShaderNodeMix"); mul.data_type = "RGBA"; mul.blend_type = "MULTIPLY"; mul.inputs["Factor"].default_value = 1
l.new(img.outputs["Color"], mul.inputs["A"]); l.new(grid.outputs["Color"], mul.inputs["B"]); l.new(mul.outputs["Result"], em.inputs["Color"])
out = n.new("ShaderNodeOutputMaterial"); l.new(em.outputs[0], out.inputs["Surface"])
WZ, WW, WH, WY0 = -3.3, 7.0, 3.0, 0.45
bpy.ops.mesh.primitive_plane_add(size=1, location=T(0, WY0 + WH / 2, WZ)); wo = bpy.context.object
wo.rotation_euler = (math.radians(90), 0, 0); wo.scale = (WW, WH, 1); wo.data.materials.append(wall_m)
dark = mat("DarkMetal", (0.02, 0.022, 0.026), 0.4, 0.85); black = mat("BlackMatte", (0.01, 0.011, 0.013), 0.8)
box(T(-WW / 2 - 0.1, 0, WZ - 0.25), T(WW / 2 + 0.1, WY0, WZ + 0.02), black)
box(T(-WW / 2 - 0.12, WY0 - 0.02, WZ - 0.05), T(-WW / 2, WY0 + WH + 0.02, WZ - 0.12), dark)
box(T(WW / 2, WY0 - 0.02, WZ - 0.05), T(WW / 2 + 0.12, WY0 + WH + 0.02, WZ - 0.12), dark)
box(T(-WW / 2 - 0.12, WY0 + WH, WZ - 0.05), T(WW / 2 + 0.12, WY0 + WH + 0.12, WZ - 0.12), dark)
blue_led = mat("BlueLED", (0, 0, 0), 0.5, emit=(0.18, 0.49, 1.0), estr=12)
box(T(-WW / 2 - 0.1, WY0 - 0.035, WZ + 0.1), T(WW / 2 + 0.1, WY0 - 0.02, WZ + 0.11), blue_led)

# ---- curved anchor desk: white glossy top, black gloss shell, lit LED band, chrome rails ----
DESK_R, DESK_CZ, DESK_H, DEPTH, HALF = 4.0, -3.6, 0.80, 0.62, 1.5
a0, a1, N = -HALF / DESK_R, HALF / DESK_R, 64
def arc_band(r0, r1, y0, y1, m, name):
    verts, faces = [], []
    for i in range(N + 1):
        a = a0 + (a1 - a0) * i / N
        for r in (r0, r1):
            for y in (y0, y1):
                verts.append(T(r * math.sin(a), y, DESK_CZ + r * math.cos(a)))
    for i in range(N):
        b = i * 4; c = b + 4
        faces += [(b, b + 2, c + 2, c), (b + 1, c + 1, c + 3, b + 3), (b, c, c + 1, b + 1), (b + 2, b + 3, c + 3, c + 2)]
    faces += [(0, 1, 3, 2), (N * 4, N * 4 + 2, N * 4 + 3, N * 4 + 1)]
    me = bpy.data.meshes.new(name); me.from_pydata(verts, [], faces); me.update()
    o = bpy.data.objects.new(name, me); sc.collection.objects.link(o); me.materials.append(m)
    for f in me.polygons: f.use_smooth = True
    return o
white_top = mat("DeskTop", (0.85, 0.86, 0.87), 0.25, coat=0.6)
gloss = mat("BlackGloss", (0.006, 0.007, 0.01), 0.12, 0.2, coat=1.0)
chrome = mat("Chrome", (0.85, 0.87, 0.9), 0.15, 1.0)
arc_band(DESK_R - DEPTH, DESK_R + 0.02, DESK_H - 0.04, DESK_H, white_top, "DeskTop")
arc_band(DESK_R - 0.02, DESK_R, 0.06, DESK_H - 0.04, gloss, "DeskShell")
led_img = bpy.data.materials.new("DeskLED"); n = led_img.node_tree.nodes; l = led_img.node_tree.links; n.clear()
geo = n.new("ShaderNodeNewGeometry"); sp = n.new("ShaderNodeSeparateXYZ"); l.new(geo.outputs["Position"], sp.inputs[0])
mr = n.new("ShaderNodeMapRange"); mr.inputs["From Min"].default_value = 0.28; mr.inputs["From Max"].default_value = 0.62; l.new(sp.outputs["Z"], mr.inputs["Value"])
cr = n.new("ShaderNodeValToRGB"); e = cr.color_ramp.elements
e[0].position = 0.0; e[0].color = (0.004, 0.012, 0.06, 1); e[1].position = 1.0; e[1].color = (0.02, 0.08, 0.35, 1)
for pos, col in ((0.47, (0.03, 0.06, 0.25, 1)), (0.49, (1.0, 0.05, 0.1, 1)), (0.51, (1.0, 0.05, 0.1, 1)), (0.53, (0.04, 0.08, 0.3, 1))):
    x = e.new(pos); x.color = col
l.new(mr.outputs["Result"], cr.inputs[0]); em = n.new("ShaderNodeEmission"); em.inputs["Strength"].default_value = 1.8; l.new(cr.outputs[0], em.inputs["Color"])
o2 = n.new("ShaderNodeOutputMaterial"); l.new(em.outputs[0], o2.inputs["Surface"])
arc_band(DESK_R + 0.001, DESK_R + 0.006, 0.28, 0.62, led_img, "DeskLED")
arc_band(DESK_R + 0.005, DESK_R + 0.03, DESK_H - 0.012, DESK_H + 0.004, chrome, "RailTop")
arc_band(DESK_R + 0.005, DESK_R + 0.02, 0.05, 0.07, chrome, "RailLow")
arc_band(DESK_R - 0.1, DESK_R - 0.05, 0.0, 0.05, blue_led, "Plinth")
# desk props: papers, tablet, mugs with the red logo stripe
paper = mat("Paper", (0.9, 0.9, 0.88), 0.7)
for x in (-0.62, 0.62):
    ctr = Vector(T(x, DESK_H + 0.002, -0.75 + 0.0))
    bpy.ops.mesh.primitive_plane_add(size=1, location=ctr); pp = bpy.context.object; pp.scale = (0.216, 0.279, 1); pp.rotation_euler[2] = random.uniform(-.15, .15); pp.data.materials.append(paper)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.04, depth=0.095, location=Vector(T(x + 0.38, DESK_H + 0.048, -0.8)))
    bpy.context.object.data.materials.append(mat("Mug", (0.9, 0.9, 0.9), 0.3, coat=0.5))

# ---- anchor chairs (backs visible behind the desk) ----
leather = mat("Leather", (0.008, 0.008, 0.01), 0.35, coat=0.4)
for x in (-0.62, 0.62):
    box(T(x - 0.24, 0.56 + 0.05, -0.45 - 0.31), T(x + 0.24, 0.56 + 0.7, -0.45 - 0.22), leather, bevel=0.03)

# ---- portrait monitors on stands, left and right ----
scr_m = bpy.data.materials.new("Monitor"); n = scr_m.node_tree.nodes; l = scr_m.node_tree.links; n.clear()
gr = n.new("ShaderNodeTexGradient"); cr = n.new("ShaderNodeValToRGB"); cr.color_ramp.elements[0].color = (0.02, 0.08, 0.35, 1); cr.color_ramp.elements[1].color = (0.25, 0.02, 0.06, 1)
tc = n.new("ShaderNodeTexCoord"); l.new(tc.outputs["UV"], gr.inputs["Vector"]); l.new(gr.outputs["Fac"], cr.inputs[0])
em = n.new("ShaderNodeEmission"); em.inputs["Strength"].default_value = 0.9; l.new(cr.outputs[0], em.inputs["Color"]); o3 = n.new("ShaderNodeOutputMaterial"); l.new(em.outputs[0], o3.inputs["Surface"])
for sx in (-1, 1):
    X = sx * 4.6
    box(T(X - 0.67, 0.55, -1.8 - 0.04), T(X + 0.67, 0.55 + 2.14, -1.8 + 0.04), dark, bevel=0.015)
    bpy.ops.mesh.primitive_plane_add(size=1, location=T(X, 0.55 + 1.07, -1.8 + 0.045)); s = bpy.context.object
    s.rotation_euler = (math.radians(90), 0, 0); s.scale = (1.26, 2.04, 1); s.data.materials.append(scr_m)
    box(T(X - 0.05, 0, -1.8 - 0.3), T(X + 0.05, 0.56, -1.8 - 0.2), chrome)

# ---- back of the set: dark slatted panels with vertical light strips, framing the wall ----
slat = mat("Slat", (0.015, 0.017, 0.022), 0.5, 0.3)
strip_r = mat("StripRed", (0,0,0), 0.5, emit=(1.0, 0.08, 0.14), estr=5)
strip_b = mat("StripBlue", (0,0,0), 0.5, emit=(0.15, 0.4, 1.0), estr=5)
for sx in (-1, 1):
    for k in range(6):
        X = sx * (4.2 + k * 0.55)
        box(T(X - 0.24, 0, -3.6 - k * 0.15), T(X + 0.24, 4.2, -3.5 - k * 0.15), slat)
        box(T(X + 0.245 * sx, 0.3, -3.45 - k * 0.15), T(X + 0.27 * sx, 3.9, -3.44 - k * 0.15), strip_r if k % 2 else strip_b)
box(T(-12, 0, -6.5), T(12, 6, -6.4), slat)
# ---- lighting grid: box truss overhead with fixtures; key/fill softboxes; back rim ----
truss_m = mat("Truss", (0.55, 0.56, 0.58), 0.35, 1.0)
for z in (-1.5, 1.0, 3.2):
    for off in (-0.145, 0.145):
        for yy in (4.2, 4.49):
            bpy.ops.mesh.primitive_cylinder_add(radius=0.024, depth=14, location=T(0, yy, z + off), rotation=(0, math.radians(90), 0))
            bpy.context.object.data.materials.append(truss_m)
def area(loc, target, size, energy, color=(1, 0.97, 0.92)):
    ld = bpy.data.lights.new("A", "AREA"); ld.size = size; ld.energy = energy; ld.color = color
    o = bpy.data.objects.new("A", ld); sc.collection.objects.link(o); o.location = loc
    d = Vector(target) - Vector(loc); o.rotation_euler = d.to_track_quat("-Z", "Y").to_euler(); return o
area(T(-2.2, 3.4, 3.2), T(0, 1.2, -0.5), 1.4, 420)             # key
area(T(2.4, 3.2, 3.0), T(0, 1.2, -0.5), 1.6, 260, (0.9, 0.95, 1))  # fill
area(T(0, 3.9, -2.6), T(0, 1.2, -0.4), 1.0, 300, (0.7, 0.8, 1))    # back rim
for i in range(9):
    x = -4 + i
    ld = bpy.data.lights.new("S", "SPOT"); ld.energy = 120; ld.spot_size = math.radians(28); ld.spot_blend = 0.5; ld.color = (0.4, 0.55, 1.0) if i % 2 else (1, 0.2, 0.3)
    o = bpy.data.objects.new("S", ld); sc.collection.objects.link(o); o.location = T(x, 4.1, -2.4); o.rotation_euler = (math.radians(20), 0, 0)
# thin haze so the beams read
hz = bpy.data.materials.new("Haze"); n = hz.node_tree.nodes; n.clear(); v = n.new("ShaderNodeVolumePrincipled"); v.inputs["Density"].default_value = 0.0025
o4 = n.new("ShaderNodeOutputMaterial"); hz.node_tree.links.new(v.outputs[0], o4.inputs["Volume"])
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 3)); h = bpy.context.object; h.scale = (18, 18, 6); h.data.materials.append(hz); h.visible_shadow = False

# ---- export mode (out path ends in .glb): set pieces only, for Unreal. Lights, haze and cameras are rebuilt there. ----
if OUT.lower().endswith(".glb"):
    import os
    for o in list(bpy.data.objects):
        if o.type == "LIGHT" or (o.type == "MESH" and o.data.materials and o.data.materials[0].name == "Haze"): bpy.data.objects.remove(o)
    for o in bpy.data.objects:
        if o.type == "MESH" and o.data.materials: o.name = "NR_" + o.data.materials[0].name   # Unreal finds pieces by material name
    bpy.ops.object.select_all(action="SELECT"); bpy.ops.object.convert(target="MESH")
    bpy.ops.export_scene.gltf(filepath=OUT, export_format="GLB", export_apply=True, export_lights=False, export_cameras=False,
                              export_materials="EXPORT", export_yup=True)
    print("NEWSROOM EXPORTED", OUT); raise SystemExit
# ---- camera: the show's wide shot ----
cd = bpy.data.cameras.new("Cam"); cd.lens = 32; cd.dof.use_dof = True; cd.dof.aperture_fstop = 4; cd.dof.focus_distance = 7.2
cam = bpy.data.objects.new("Cam", cd); sc.collection.objects.link(cam); sc.camera = cam
shots = [("wide", 32, T(0, 1.55, 6.4), T(0, 1.3, -1.5), 7.2), ("two", 50, T(-2.6, 1.35, 3.6), T(0.2, 1.15, -0.7), 5.2)]
for name, lens, loc, tgt, fd in shots:
    cd.lens = lens; cd.dof.focus_distance = fd; cam.location = loc
    cam.rotation_euler = (Vector(tgt) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    sc.render.filepath = OUT.replace(".png", "-" + name + ".png")
    bpy.ops.render.render(write_still=True)
print("NEWSROOM OK")
