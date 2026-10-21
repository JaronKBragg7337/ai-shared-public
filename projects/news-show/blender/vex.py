# Heartbeat News - AI Robot Vex, realistic. A high-end android bust seated at the desk: glossy white ceramic shell with panel seams,
# black glass visor with eye lights behind it, a light-strip mouth driven by his voice in Unreal, brushed-metal ear discs with
# blue rings, graphite neck with pistons. Human scale (head 0.24 m tall, shoulders 0.46 m). Built at the origin, seat at z=0.55,
# facing -Y (toward the show camera). Surfaces baked to atlases; the lights stay separate ("VX_glow_*") so Unreal can animate them.
# blender -b -P vex.py -- --out DIR [--preview still.png] [--bake]
import bpy, bmesh, math, sys, os
from mathutils import Vector
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def arg(k, d=None): return argv[argv.index(k) + 1] if k in argv else d
OUT = arg("--out", "."); RES = int(arg("--res", "2048")); os.makedirs(OUT, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene; sc.render.engine = "CYCLES"
p = bpy.context.preferences.addons["cycles"].preferences; p.compute_device_type = "OPTIX"; p.get_devices()
for d in p.devices: d.use = d.type == "OPTIX"
sc.cycles.device = "GPU"; sc.view_settings.view_transform = "AgX"

def mat(name, color, rough=0.4, metal=0.0, coat=0.0, emit=None, estr=0.0, noise=0.0, nscale=40.0):
    m = bpy.data.materials.new(name); n = m.node_tree.nodes; l = m.node_tree.links; b = n["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*color, 1); b.inputs["Roughness"].default_value = rough; b.inputs["Metallic"].default_value = metal
    b.inputs["Coat Weight"].default_value = coat
    if emit: b.inputs["Emission Color"].default_value = (*emit, 1); b.inputs["Emission Strength"].default_value = estr
    if noise:   # fine surface variation: brushed / worn so nothing reads as flat CG
        tc = n.new("ShaderNodeTexCoord"); nz = n.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = nscale; nz.inputs["Detail"].default_value = 10
        mp = n.new("ShaderNodeMapping"); mp.inputs["Scale"].default_value = (1, 1, 30 if "Brushed" in name else 1)
        l.new(tc.outputs["Object"], mp.inputs[0]); l.new(mp.outputs[0], nz.inputs["Vector"])
        rr = n.new("ShaderNodeMapRange"); rr.inputs["To Min"].default_value = max(0.02, rough - noise); rr.inputs["To Max"].default_value = rough + noise
        l.new(nz.outputs["Fac"], rr.inputs["Value"]); l.new(rr.outputs[0], b.inputs["Roughness"])
        bp = n.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.05; bp.inputs["Distance"].default_value = 0.0005
        l.new(nz.outputs["Fac"], bp.inputs["Height"]); l.new(bp.outputs[0], b.inputs["Normal"])
    return m
M = {"shell": mat("VexCeramic", (0.86, 0.87, 0.88), 0.18, coat=0.8, noise=0.05, nscale=60),
     "graphite": mat("VexGraphite", (0.035, 0.037, 0.042), 0.35, 0.9, noise=0.12, nscale=80),
     "alu": mat("VexBrushed", (0.72, 0.73, 0.75), 0.28, 1.0, noise=0.1, nscale=120),
     "glass": mat("VexVisor", (0.004, 0.005, 0.007), 0.05, 0.0, coat=1.0),
     "seam": mat("VexSeam", (0.02, 0.02, 0.022), 0.6),
     "rubber": mat("VexRubber", (0.02, 0.02, 0.022), 0.75, noise=0.1, nscale=30)}
GLOW = {"eyes": mat("VX_glow_eyes", (0.3, 0.8, 1), 0.3, emit=(0.35, 0.8, 1.0), estr=18),
        "mouth": mat("VX_glow_mouth", (0.3, 0.8, 1), 0.3, emit=(0.35, 0.8, 1.0), estr=14),
        "ring": mat("VX_glow_ring", (0.2, 0.5, 1), 0.3, emit=(0.18, 0.49, 1.0), estr=10)}

def tag(o, g): o["g"] = g; return o
def smooth(o, lv=2):
    s = o.modifiers.new("sub", "SUBSURF"); s.levels = lv; s.render_levels = lv
    for f in o.data.polygons: f.use_smooth = True
    return o
def ell(name, loc, scale, m, g, lv=2):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=24, radius=1, location=loc); o = bpy.context.object; o.name = name
    o.scale = scale; bpy.ops.object.transform_apply(scale=True); o.data.materials.append(m)
    for f in o.data.polygons: f.use_smooth = True
    return tag(o, g)
def cyl(name, loc, r, h, m, g, rot=(0, 0, 0), verts=48, r2=None):
    if r2 is None: bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=h, location=loc, rotation=rot)
    else: bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=r, radius2=r2, depth=h, location=loc, rotation=rot)
    o = bpy.context.object; o.name = name; o.data.materials.append(m)
    bv = o.modifiers.new("bv", "BEVEL"); bv.width = min(r, h) * 0.12; bv.segments = 3; bv.limit_method = "ANGLE"
    for f in o.data.polygons: f.use_smooth = True
    return tag(o, g)
def torus(name, loc, R, r, m, g, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=r, major_segments=64, minor_segments=12, location=loc, rotation=rot)
    o = bpy.context.object; o.name = name; o.data.materials.append(m); bpy.ops.object.shade_smooth(); return tag(o, g)
def rbox(name, a, b, m, g, bevel=0.01, lv=0):
    c = [(a[i] + b[i]) / 2 for i in range(3)]
    bpy.ops.mesh.primitive_cube_add(size=1, location=c); o = bpy.context.object; o.name = name
    o.scale = [abs(b[i] - a[i]) for i in range(3)]; bpy.ops.object.transform_apply(scale=True); o.data.materials.append(m)
    bv = o.modifiers.new("bv", "BEVEL"); bv.width = bevel; bv.segments = 4
    if lv: smooth(o, lv)
    for f in o.data.polygons: f.use_smooth = True
    return tag(o, g)

HZ = 1.25                                          # head centre height (seated at the desk)
# ---- head: ceramic egg, slightly flattened face, seam line, visor, eyes, mouth strip, ear discs
head = ell("Head", (0, 0, HZ), (0.083, 0.095, 0.118), M["shell"], "body")
torus("HeadSeam", (0, 0.004, HZ + 0.03), 0.0905, 0.0022, M["seam"], "body", rot=(math.radians(78), 0, 0))
# visor: a curved band of black glass wrapping the front of the face at eye height
bm = bmesh.new(); segs = 40; a0, a1 = math.radians(-58), math.radians(58); vz0, vz1 = HZ - 0.012, HZ + 0.03
verts = []
for i in range(segs + 1):
    a = a0 + (a1 - a0) * i / segs
    for z in (vz0, vz1):
        k = 1 - ((z - HZ) / 0.118) ** 2; rx, ry = 0.0855 * math.sqrt(max(k, 0)), 0.0975 * math.sqrt(max(k, 0))
        verts.append(bm.verts.new((rx * math.sin(a), -ry * math.cos(a), z)))
for i in range(segs):
    bm.faces.new((verts[2 * i], verts[2 * i + 2], verts[2 * i + 3], verts[2 * i + 1]))
me = bpy.data.meshes.new("Visor"); bm.to_mesh(me); bm.free(); vis = bpy.data.objects.new("Visor", me); sc.collection.objects.link(vis)
sol = vis.modifiers.new("th", "SOLIDIFY"); sol.thickness = 0.004; me.materials.append(M["glass"])
for f in me.polygons: f.use_smooth = True
tag(vis, "body")
for sx in (-1, 1):   # eye lights just behind the glass
    e = ell("Eye%d" % sx, (sx * 0.032, -0.089, HZ + 0.009), (0.013, 0.004, 0.0055), GLOW["eyes"], "glow_eyes", 0)
    cyl("Ear%d" % sx, (sx * 0.084, 0.004, HZ + 0.004), 0.03, 0.018, M["alu"], "body", rot=(0, math.radians(90), 0))
    torus("EarRing%d" % sx, (sx * 0.0935, 0.004, HZ + 0.004), 0.022, 0.0028, GLOW["ring"], "glow_ring", rot=(0, math.radians(90), 0))
mouth = rbox("Mouth", (-0.024, -0.1005, HZ - 0.052), (0.024, -0.093, HZ - 0.047), GLOW["mouth"], "glow_mouth", bevel=0.002)
rbox("MouthBezel", (-0.03, -0.098, HZ - 0.056), (0.03, -0.09, HZ - 0.043), M["graphite"], "body", bevel=0.003)
# ---- neck: graphite segments + two pistons
for k in range(4):
    cyl("Neck%d" % k, (0, 0.012, HZ - 0.125 - k * 0.022), 0.034 - k * 0.001, 0.018, M["graphite"] if k % 2 == 0 else M["rubber"], "body")
for sx in (-1, 1):
    cyl("Piston%d" % sx, (sx * 0.028, 0.03, HZ - 0.15), 0.006, 0.09, M["alu"], "body", rot=(0, math.radians(sx * 10), 0), verts=16)
# ---- torso: chest shell, collar, shoulders, upper arms resting forward on the desk line
ell("Chest", (0, 0.03, HZ - 0.33), (0.19, 0.11, 0.2), M["shell"], "body")
torus("Collar", (0, 0.02, HZ - 0.19), 0.062, 0.014, M["graphite"], "body", rot=(math.radians(8), 0, 0))
rbox("ChestPlate", (-0.1, -0.082, HZ - 0.36), (0.1, -0.06, HZ - 0.22), M["shell"], "body", bevel=0.02, lv=2)
torus("ChestSeam", (0, -0.03, HZ - 0.3), 0.16, 0.002, M["seam"], "body", rot=(math.radians(90), 0, 0))
cyl("ChestLight", (0, -0.084, HZ - 0.265), 0.012, 0.004, GLOW["ring"], "glow_ring", rot=(math.radians(90), 0, 0), verts=32)
for sx in (-1, 1):
    ell("Shoulder%d" % sx, (sx * 0.2, 0.03, HZ - 0.22), (0.075, 0.075, 0.07), M["shell"], "body")
    cyl("ShoulderJoint%d" % sx, (sx * 0.165, 0.03, HZ - 0.23), 0.045, 0.03, M["graphite"], "body", rot=(0, math.radians(90), 0))
    arm = cyl("UpperArm%d" % sx, (sx * 0.215, -0.02, HZ - 0.36), 0.048, 0.24, M["shell"], "body", rot=(math.radians(-25), math.radians(sx * 8), 0), r2=0.04)
    cyl("Elbow%d" % sx, (sx * 0.22, -0.075, HZ - 0.47), 0.04, 0.07, M["graphite"], "body", rot=(0, math.radians(90), 0))
    cyl("Forearm%d" % sx, (sx * 0.19, -0.2, HZ - 0.47), 0.036, 0.24, M["shell"], "body", rot=(math.radians(90), 0, math.radians(-sx * 12)), r2=0.03)
    ell("Hand%d" % sx, (sx * 0.16, -0.33, HZ - 0.465), (0.045, 0.06, 0.022), M["graphite"], "body")
ell("Waist", (0, 0.04, HZ - 0.55), (0.14, 0.09, 0.08), M["graphite"], "body")
# small maker's mark on the chest: VEX
bpy.ops.object.text_add(location=(0.06, -0.083, HZ - 0.33), rotation=(math.radians(90), 0, 0)); t = bpy.context.object; t.name = "Mark"
t.data.body = "VEX"; t.data.size = 0.022; t.data.extrude = 0.0008; t.data.align_x = "CENTER"; t.data.materials.append(M["seam"]); tag(t, "body")

if arg("--preview"):
    bpy.ops.object.light_add(type="AREA", location=(-0.8, -1.2, 1.7)); L1 = bpy.context.object; L1.data.energy = 120; L1.data.size = 0.8
    L1.rotation_euler = (Vector((0, 0, HZ)) - L1.location).to_track_quat("-Z", "Y").to_euler()
    bpy.ops.object.light_add(type="AREA", location=(0.9, 0.9, 1.6)); L2 = bpy.context.object; L2.data.energy = 90; L2.data.size = 0.5; L2.data.color = (0.6, 0.75, 1)
    L2.rotation_euler = (Vector((0, 0, HZ)) - L2.location).to_track_quat("-Z", "Y").to_euler()
    w = bpy.data.worlds.new("w"); sc.world = w; w.node_tree.nodes["Background"].inputs[0].default_value = (0.01, 0.012, 0.018, 1)
    bpy.ops.object.camera_add(location=(0.35, -1.25, HZ + 0.02)); cam = bpy.context.object; cam.data.lens = 70; sc.camera = cam
    cam.rotation_euler = (Vector((0, 0, HZ - 0.12)) - cam.location).to_track_quat("-Z", "Y").to_euler()
    sc.render.resolution_x, sc.render.resolution_y = 1400, 1400; sc.cycles.samples = 128; sc.cycles.use_denoising = True
    sc.render.filepath = arg("--preview"); bpy.ops.render.render(write_still=True)

def select_only(objs):
    bpy.ops.object.select_all(action="DESELECT")
    for o in objs: o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
if "--bake" in argv:
    for o in [o for o in bpy.data.objects if o.type == "FONT"]: select_only([o]); bpy.ops.object.convert(target="MESH")
    meshes = [o for o in bpy.data.objects if o.type == "MESH"]
    select_only(meshes); bpy.ops.object.convert(target="MESH"); bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    groups = {}
    for o in meshes: groups.setdefault(o["g"], []).append(o)
    for g, objs in groups.items():
        select_only(objs); bpy.ops.object.join(); j = bpy.context.object; j.name = "VX_" + g
        if g != "body": continue
        while len(j.data.uv_layers): j.data.uv_layers.remove(j.data.uv_layers[0])
        j.data.uv_layers.new(name="UV"); bpy.ops.object.mode_set(mode="EDIT"); bpy.ops.mesh.select_all(action="SELECT")
        bpy.ops.uv.smart_project(angle_limit=math.radians(55), island_margin=0.003); bpy.ops.uv.pack_islands(margin=0.003, rotate=True); bpy.ops.object.mode_set(mode="OBJECT")
        out = {}
        for kind, btype in (("BC", "DIFFUSE"), ("R", "ROUGHNESS"), ("N", "NORMAL"), ("M", "EMIT")):
            img = bpy.data.images.new("vex_" + kind, RES, RES, is_data=kind != "BC")
            for m in j.data.materials:
                nt = m.node_tree; nd = nt.nodes.get("BAKE") or nt.nodes.new("ShaderNodeTexImage"); nd.name = "BAKE"; nd.image = img
                for x in nt.nodes: x.select = False
                nd.select = True; nt.nodes.active = nd
                if kind == "M":
                    b = nt.nodes["Principled BSDF"]; mv = b.inputs["Metallic"].default_value
                    b.inputs["Emission Color"].default_value = (mv, mv, mv, 1); b.inputs["Emission Strength"].default_value = 1.0
            if kind == "BC": sc.render.bake.use_pass_direct = False; sc.render.bake.use_pass_indirect = False; sc.render.bake.use_pass_color = True
            sc.cycles.samples = 4; bpy.ops.object.bake(type=btype, margin=8)
            img.filepath_raw = os.path.join(OUT, "vex_%s.png" % kind); img.file_format = "PNG"; img.save(); out[kind] = img; print("BAKED", kind, flush=True)
        nm = bpy.data.materials.new("VX_body"); nt = nm.node_tree; b = nt.nodes["Principled BSDF"]
        t_ = nt.nodes.new("ShaderNodeTexImage"); t_.image = out["BC"]; nt.links.new(t_.outputs["Color"], b.inputs["Base Color"])
        r_ = nt.nodes.new("ShaderNodeTexImage"); r_.image = out["R"]; nt.links.new(r_.outputs["Color"], b.inputs["Roughness"])
        m_ = nt.nodes.new("ShaderNodeTexImage"); m_.image = out["M"]; nt.links.new(m_.outputs["Color"], b.inputs["Metallic"])
        n_ = nt.nodes.new("ShaderNodeTexImage"); n_.image = out["N"]; nm_ = nt.nodes.new("ShaderNodeNormalMap"); nt.links.new(n_.outputs["Color"], nm_.inputs["Color"]); nt.links.new(nm_.outputs[0], b.inputs["Normal"])
        b.inputs["Coat Weight"].default_value = 0.5
        j.data.materials.clear(); j.data.materials.append(nm)
    bpy.ops.export_scene.gltf(filepath=os.path.join(OUT, "vex.glb"), export_format="GLB", export_apply=True, export_lights=False, export_cameras=False)
    print("VEX EXPORTED", flush=True)
print("VEX OK", flush=True)
