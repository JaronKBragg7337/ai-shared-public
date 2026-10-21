# The Necklace - Episode 1 "Rum and Regret in Rosetown", Part 1 (the opening of chapter 1, up to Mateo's first warning).
# Pure-script Blender scene: the Rusty Anchor set (sets/rusty_anchor.py, procedural materials, real sizes) + the Loft's
# MetaHuman people (homes/people/*.glb: isaiah = Jalen, walter = Mateo, the others as patrons) + a night harbour outside.
# Cycles OptiX on the RTX 4060.  blender -b -P build.py -- [--still FRAME out.png] [--anim OUTDIR] [--samples N] [--cpu]
#                                                        [--start F --end F] [--save out.blend]
# Faces are the phone-weight LOD (1024 px, no lip rig): no shot holds on a talking mouth - the listener, the hands, the room
# and the doorway carry the dialogue (the same "frame around it" rule The Keeper's Light used for the rocks).
import bpy, math, random, sys, os, runpy, json
from mathutils import Vector, Matrix, Quaternion

HERE = os.path.dirname(os.path.abspath(__file__))
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def arg(k, d=None): return argv[argv.index(k) + 1] if k in argv else d
FPS = 24
DUR_S = 116.0
DUR = int(DUR_S * FPS)
random.seed(5)

# ---------------------------------------------------------------- the set (builds the whole bar, sets Cycles/OptiX up)
SETPY = os.path.join(HERE, "..", "sets", "rusty_anchor.py")
sys.argv = ["blender", "--", "--out", os.path.join(HERE, "_set")]
S = runpy.run_path(SETPY)
sys.argv = ["blender"] + (["--"] + argv if argv else [])
sc = bpy.context.scene
W, D, H = S["W"], S["D"], S["H"]; STOOLS = S["STOOLS"]; BX0, BX1, BY0, BY1 = S["BX0"], S["BX1"], S["BY0"], S["BY1"]
M = S["M"]; box, cyl, lathe, mat_ = S["box"], S["cyl"], S["lathe"], S["mat"]
JX = STOOLS[4][0]; MX = STOOLS[5][0]; SY = STOOLS[4][1]
PEOPLE = "C:/Users/lilli/Projects/heartbeat-observatory/homes/people/"

# ---------------------------------------------------------------- render settings
sc.render.fps = FPS; sc.frame_start, sc.frame_end = 1, DUR
sc.render.resolution_x, sc.render.resolution_y = 1280, 720; sc.render.resolution_percentage = 100
sc.cycles.device = "CPU" if "--cpu" in argv else "GPU"
sc.cycles.samples = int(arg("--samples", "64")); sc.cycles.use_adaptive_sampling = True; sc.cycles.adaptive_threshold = 0.03
sc.cycles.use_denoising = True; sc.cycles.denoiser = "OPENIMAGEDENOISE" if "--cpu" in argv else "OPTIX"
sc.cycles.max_bounces = 6; sc.cycles.diffuse_bounces = 3; sc.cycles.glossy_bounces = 3; sc.cycles.volume_bounces = 0
sc.cycles.caustics_reflective = False; sc.cycles.caustics_refractive = False
sc.cycles.blur_glossy = 1.0; sc.cycles.sample_clamp_indirect = 8.0
sc.render.use_motion_blur = False
sc.view_settings.view_transform = "AgX"
try: sc.view_settings.look = "AgX - Medium High Contrast"
except Exception: pass
sc.view_settings.exposure = 1.1
sc.render.image_settings.file_format = "PNG"; sc.render.image_settings.color_mode = "RGB"
sc.render.film_transparent = False

# chairs in the set face away from their tables (the back slats sit on the sitter's side): turn them round
for e in [o for o in bpy.data.objects if o.type == "EMPTY" and any(c.name.startswith("Chair") for c in o.children)]:
    e.rotation_euler.z += math.pi

# ---------------------------------------------------------------- outside: night, calm harbour water, pilings, string lights
w = bpy.data.worlds.new("Night"); sc.world = w; wn, wl = w.node_tree.nodes, w.node_tree.links; wn.clear()
tc = wn.new("ShaderNodeTexCoord"); sep = wn.new("ShaderNodeSeparateXYZ"); wl.new(tc.outputs["Generated"], sep.inputs[0])
hz = wn.new("ShaderNodeMapRange"); hz.inputs["From Min"].default_value = -0.02; hz.inputs["From Max"].default_value = 0.14
wl.new(sep.outputs["Z"], hz.inputs["Value"])
cr = wn.new("ShaderNodeValToRGB"); cr.color_ramp.elements[0].color = (0.016, 0.006, 0.013, 1); cr.color_ramp.elements[1].color = (0.0015, 0.0025, 0.007, 1)   # bruised twilight at the horizon
cr.color_ramp.elements[1].position = 0.6
wl.new(hz.outputs[0], cr.inputs[0])
stars = wn.new("ShaderNodeTexNoise"); stars.inputs["Scale"].default_value = 900; stars.inputs["Detail"].default_value = 0
wl.new(tc.outputs["Generated"], stars.inputs["Vector"])
sm = wn.new("ShaderNodeMath"); sm.operation = "GREATER_THAN"; sm.inputs[1].default_value = 0.86; wl.new(stars.outputs["Fac"], sm.inputs[0])
sk = wn.new("ShaderNodeMath"); sk.operation = "MULTIPLY"; wl.new(sm.outputs[0], sk.inputs[0]); wl.new(hz.outputs[0], sk.inputs[1])
sa = wn.new("ShaderNodeMix"); sa.data_type = "RGBA"; wl.new(sk.outputs[0], sa.inputs["Factor"]); wl.new(cr.outputs[0], sa.inputs["A"]); sa.inputs["B"].default_value = (0.5, 0.5, 0.55, 1)
bg = wn.new("ShaderNodeBackground"); bg.inputs["Strength"].default_value = 1.0; out = wn.new("ShaderNodeOutputWorld")
wl.new(sa.outputs["Result"], bg.inputs[0]); wl.new(bg.outputs[0], out.inputs["Surface"])
# moon: a cool sun lamp from the south-west, low
bpy.ops.object.light_add(type="SUN"); moon = bpy.context.object; moon.name = "Moon"
moon.data.energy = 0.12; moon.data.color = (0.7, 0.8, 1.0); moon.data.angle = math.radians(0.6)
mdir = Vector((-0.5, -1.0, 0.0)); mdir.z = math.tan(math.radians(32)) * mdir.length; mdir.normalize()
moon.rotation_euler = (-mdir).to_track_quat("-Z", "Y").to_euler()

# calm water with the Ocean modifier (same tool as The Keeper's Light), top at z = -1.2
for o in [o for o in bpy.data.objects if o.name == "Water"]: bpy.data.objects.remove(o)
water_m, n, l = mat_("Harbour water", (0.004, 0.012, 0.02), 0.04), None, None
n, l = water_m.node_tree.nodes, water_m.node_tree.links; b = n["Principled BSDF"]
b.inputs["IOR"].default_value = 1.333; b.inputs["Base Color"].default_value = (0.004, 0.012, 0.02, 1); b.inputs["Roughness"].default_value = 0.03
bpy.ops.mesh.primitive_plane_add(size=1); ocean = bpy.context.object; ocean.name = "Ocean"; ocean.location = (W / 2 - 60, -60, -1.2)
om = ocean.modifiers.new("Ocean", "OCEAN"); om.geometry_mode = "GENERATE"; om.resolution = 14; om.viewport_resolution = 4
om.spatial_size = 40; om.size = 1.0; om.repeat_x = om.repeat_y = 3; om.wave_scale = 0.22; om.choppiness = 0.8
om.wind_velocity = 4.0; om.wave_alignment = 0.2; om.wave_direction = math.radians(160); om.use_normals = True; om.random_seed = 9
om.time = 1.0; om.keyframe_insert("time", frame=1); om.time = 1.0 + DUR_S * 0.7; om.keyframe_insert("time", frame=DUR)
ocean.data.materials.append(water_m); bpy.ops.object.shade_smooth()
def linear(idb):
    ad = idb.animation_data
    if not ad or not ad.action: return
    cs = getattr(ad.action, "fcurves", None)
    if cs is None:
        try: cs = [fc for layer in ad.action.layers for strip in layer.strips for bag in strip.channelbags for fc in bag.fcurves]
        except Exception: cs = []
    for fc in cs:
        for k in fc.keyframe_points: k.interpolation = "LINEAR"
linear(ocean)
# pilings under the dock, weathered and wet at the waterline
pile_m = S["grimy"]("Piling", (0.09, 0.07, 0.05), (0.16, 0.13, 0.09), 9, 0.85, bump=0.5)
for x in [-1.6, -0.2, 1.3, 2.9, 4.4, 5.9, 7.4, 8.9, 10.3, 11.7]:
    for y in (-3.0, -1.55):
        cyl("Pile_%g_%g" % (x, y), (x + random.uniform(-0.08, 0.08), y, -2.6), 0.14, 2.4, pile_m, "x", verts=14)
# the building's back wall and sides seen from outside already exist; add the roof overhang + a sign + string lights
box("Overhang", (-0.3, -1.1, H), (W + 0.3, 0.1, H + 0.12), M["iron"], "x")
for x in (0.3, 3.5, 6.5, 9.7): box("OverPost%g" % x, (x - 0.06, -1.05, 0), (x + 0.06, -0.93, H), M["beam"], "x")
for sgn, nm in ((1, "RoofS"), (-1, "RoofN")):      # a low pitched tin roof: ridge along the room, eaves out past the walls
    bpy.ops.mesh.primitive_cube_add(size=1); r = bpy.context.object; r.name = nm; r.data.materials.append(M["iron"])
    r.scale = (W + 1.2, 3.9, 0.1); r.location = (W / 2, D / 2 + sgn * 1.8, H + 0.1 + 0.62); r.rotation_euler = (-sgn * math.atan2(1.24, 3.6), 0, 0)
box("Gable", (0, 0, H + 0.1), (W, D, H + 0.12), M["beam"], "x")
box("OutSignBoard", (3.3, -0.19, 2.42), (6.7, -0.15, 2.9), M["sign"], "x", bevel=0.01)
S["text"]("OutSignText", "THE RUSTY ANCHOR", (5.0, -0.195, 2.68), 0.22, M["signpaint"], "x", rot=(math.pi / 2, 0, 0))
S["text"]("OutSignSub", "RUM  ·  BEER  ·  ROOMS", (5.0, -0.195, 2.52), 0.07, M["signpaint"], "x", rot=(math.pi / 2, 0, 0))
STRING = []
for seg in ((0.3, 3.5), (3.5, 6.5), (6.5, 9.7)):
    x0, x1 = seg; L = x1 - x0; k = 0
    while True:
        x = x0 + 0.42 * (k + 0.5)
        if x > x1 - 0.1: break
        u = (x - x0) / L; z = 2.95 - 0.28 * math.sin(math.pi * u)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.028, location=(x, -0.98, z), segments=12, ring_count=8)
        bb = bpy.context.object; bb.name = "StringBulb"; bb.data.materials.append(M["bulb"]); bpy.ops.object.shade_smooth()
        STRING.append((x, -0.98, z)); k += 1
        if k % 2 == 0:
            bpy.ops.object.light_add(type="POINT", location=(x, -0.98, z - 0.04)); sl = bpy.context.object; sl.name = "StringLight"
            sl.data.energy = 4.5; sl.data.color = (1, 0.58, 0.28); sl.data.shadow_soft_size = 0.03
bpy.ops.object.light_add(type="POINT", location=(3.0, -0.5, 2.75)); dk = bpy.context.object; dk.name = "DockLamp"; dk.data.energy = 40; dk.data.color = (1, 0.6, 0.3); dk.data.shadow_soft_size = 0.06
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.045, location=(3.0, -0.5, 2.75), segments=12, ring_count=8); bpy.context.object.data.materials.append(M["bulb"])
# a lamp over the street door (east) so the doorway reads from inside
bpy.ops.object.light_add(type="POINT", location=(W + 0.6, 1.75, 2.3)); dl = bpy.context.object; dl.data.energy = 30; dl.data.color = (1, 0.6, 0.3); dl.data.shadow_soft_size = 0.08
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.04, location=(W + 0.6, 1.75, 2.3), segments=12, ring_count=8); bpy.context.object.data.materials.append(M["bulb"])
box("Street", (W, -3, -0.05), (W + 2.6, 9, 0), M["floor"], "x")      # the quay outside the door, then the water
for x in (W + 2.5,):
    for yy in (0.0, 1.2, 2.4, 3.6, 4.8, 6.0): cyl("Bollard%g" % yy, (x, yy, 0), 0.05, 0.9, M["beam"], "x", verts=10)
    box("QuayRail", (x - 0.03, -0.2, 0.86), (x + 0.03, 6.2, 0.92), M["beam"], "x")
box("DoorBracket", (W + 0.1, 1.72, 2.28), (W + 0.6, 1.78, 2.32), M["iron"], "x")

# ---------------------------------------------------------------- inside: real lamps
LIGHTS = S["LIGHTS"]
for L_ in LIGHTS:
    if L_["type"] == "pendant":
        bpy.ops.object.light_add(type="POINT", location=L_["pos"]); li = bpy.context.object; li.name = "Pendant"
        li.data.energy = 85; li.data.color = (1.0, 0.56, 0.26); li.data.shadow_soft_size = 0.035
bpy.ops.object.light_add(type="AREA", location=(5.4, D - 0.4, 2.26)); bb_ = bpy.context.object; bb_.name = "BackBar"
bb_.data.energy = 9; bb_.data.size = 5.4; bb_.data.size_y = 0.3; bb_.data.color = (1, 0.52, 0.22); bb_.rotation_euler = (math.radians(100), 0, 0)
bpy.ops.object.light_add(type="AREA", location=(8.9, D - 0.3, 2.2)); ne = bpy.context.object; ne.name = "NeonFill"
ne.data.energy = 8; ne.data.size = 0.9; ne.data.size_y = 0.35; ne.data.color = (1, 0.18, 0.1); ne.rotation_euler = (math.radians(95), 0, 0)
bpy.ops.object.light_add(type="AREA", location=(W / 2, D / 2, H - 0.05)); amb = bpy.context.object; amb.name = "RoomAmbient"
amb.data.energy = 60; amb.data.size = 9; amb.data.size_y = 6; amb.data.color = (1, 0.62, 0.36); amb.rotation_euler = (0, 0, 0)
# light haze so the pendants cone and the far room softens
haze = bpy.data.materials.new("Haze"); hn, hl = haze.node_tree.nodes, haze.node_tree.links; hn.clear()
vs = hn.new("ShaderNodeVolumeScatter"); vs.inputs["Density"].default_value = 0.018; vs.inputs["Anisotropy"].default_value = 0.35
ho = hn.new("ShaderNodeOutputMaterial"); hl.new(vs.outputs[0], ho.inputs["Volume"])
hz_ = box("HazeVol", (0.05, 0.05, 0.02), (W - 0.05, D - 0.05, H - 0.02), haze, "x")
hz_.display_type = "WIRE"; hz_.visible_shadow = False

# ---------------------------------------------------------------- people
NEXT = {"spine_01": "spine_02", "spine_03": "spine_04", "neck_01": "neck_02", "neck_02": "head"}
for s_ in "lr":
    NEXT.update({f"thigh_{s_}": f"calf_{s_}", f"calf_{s_}": f"foot_{s_}", f"foot_{s_}": f"ball_{s_}", f"upperarm_{s_}": f"lowerarm_{s_}",
                 f"lowerarm_{s_}": f"hand_{s_}", f"hand_{s_}": f"middle_metacarpal_{s_}"})

def load_person(name, tag):
    before = set(bpy.data.objects); bm = set(bpy.data.materials); ba = set(bpy.data.actions)
    bpy.ops.import_scene.gltf(filepath=PEOPLE + name + ".glb")
    for o in [o for o in bpy.data.objects if o not in before and o.name.startswith("Icosphere")]: bpy.data.objects.remove(o)
    arm = next(o for o in bpy.data.objects if o.type == "ARMATURE" and o not in before); arm.name = tag
    mats = {m.name.split(".")[0]: m for m in bpy.data.materials if m not in bm}
    acts = {a.name.split(".")[0]: a for a in bpy.data.actions if a not in ba}
    for o in [o for o in bpy.data.objects if o not in before]:
        o.visible_shadow = True
        if o.type == "MESH":
            for pg in o.data.polygons: pg.use_smooth = True
    return arm, mats, acts

def cloth(mats, shirt=None, pants=None, shoes=None, rough=0.85):
    for mn, c in (("Shirt", shirt), ("Pants", pants), ("Shorts", pants), ("Shoes", shoes)):
        m = mats.get(mn)
        if not m or not c: continue
        b = next((x for x in m.node_tree.nodes if x.type == "BSDF_PRINCIPLED"), None)
        if b and not b.inputs["Base Color"].is_linked:
            b.inputs["Base Color"].default_value = c + (1,); b.inputs["Roughness"].default_value = rough

def tint_skin(mats, color, fac):
    # lift / warm the baked skin maps (face + body together so they keep matching)
    for mn in ("Skin_Face", "Skin_Body"):
        m = mats.get(mn)
        if not m: continue
        nt = m.node_tree; b = next(x for x in nt.nodes if x.type == "BSDF_PRINCIPLED")
        src = b.inputs["Base Color"].links[0].from_socket if b.inputs["Base Color"].is_linked else None
        if not src: continue
        mx = nt.nodes.new("ShaderNodeMix"); mx.data_type = "RGBA"; mx.blend_type = "SOFT_LIGHT"; mx.inputs["Factor"].default_value = fac
        nt.links.new(src, mx.inputs["A"]); mx.inputs["B"].default_value = color + (1,)
        nt.links.new(mx.outputs["Result"], b.inputs["Base Color"])
        b.inputs["Roughness"].default_value = 0.45

def hair_tint(mats, f):
    for mn, m in mats.items():
        if not mn.startswith("Hair"): continue
        nt = m.node_tree; b = next((x for x in nt.nodes if x.type == "BSDF_PRINCIPLED"), None)
        if not b: continue
        if b.inputs["Base Color"].is_linked:
            src = b.inputs["Base Color"].links[0].from_socket
            mx = nt.nodes.new("ShaderNodeMix"); mx.data_type = "RGBA"; mx.blend_type = "MULTIPLY"; mx.inputs["Factor"].default_value = 1.0
            nt.links.new(src, mx.inputs["A"]); mx.inputs["B"].default_value = (f, f, f, 1); nt.links.new(mx.outputs["Result"], b.inputs["Base Color"])
        else:
            c = b.inputs["Base Color"].default_value; b.inputs["Base Color"].default_value = (c[0] * f, c[1] * f, c[2] * f, 1)

def align(arm, name, d):
    pb = arm.pose.bones[name]; bpy.context.view_layer.update()
    nx = NEXT.get(name)
    if not nx: return
    cur = (arm.pose.bones[nx].head - pb.head).normalized(); q = cur.rotation_difference(Vector(d).normalized())
    Mx = pb.matrix.copy(); t = Mx.to_translation()
    pb.matrix = Matrix.Translation(t) @ q.to_matrix().to_4x4() @ Matrix.Translation(-t) @ Mx
    bpy.context.view_layer.update()

def turn(arm, name, axis, deg):
    # rotate one bone about an armature-space axis through its head (yaw about Z, nod about X)
    pb = arm.pose.bones[name]; bpy.context.view_layer.update()
    Mx = pb.matrix.copy(); t = Mx.to_translation()
    R = Matrix.Rotation(math.radians(deg), 4, axis)
    pb.matrix = Matrix.Translation(t) @ R @ Matrix.Translation(-t) @ Mx
    bpy.context.view_layer.update()

def key_all(arm, f):
    for pb in arm.pose.bones:
        pb.keyframe_insert("rotation_quaternion", frame=f, group=pb.name)
    arm.pose.bones["pelvis"].keyframe_insert("location", frame=f, group="pelvis")

def key(arm, names, f):
    for nm in names: arm.pose.bones[nm].keyframe_insert("rotation_quaternion", frame=f, group=nm)

def bone_world(arm, name, tail=False):
    bpy.context.view_layer.update(); pb = arm.pose.bones[name]
    return arm.matrix_world @ (pb.tail if tail else pb.head)

def facing(dx, dy):
    # the armature's forward is -Y (the importer leaves the object in QUATERNION mode - set XYZ before using this)
    return math.atan2(dx, -dy)

def seat(arm, acts, x, y, z, rotz, arms="bar"):
    """put a person in the Sit pose at (x,y,z) (z = seat top), facing rotz; bake it into a fresh action we then animate on."""
    arm.rotation_mode = "XYZ"; arm.location = (x, y, z); arm.rotation_euler = (0, 0, rotz)
    ad = arm.animation_data or arm.animation_data_create()
    for t in list(ad.nla_tracks): ad.nla_tracks.remove(t)
    ad.action = acts["Sit"]
    try: ad.action_slot = acts["Sit"].slots[0]
    except Exception as e: print("slot", e)
    sc.frame_set(1); bpy.context.view_layer.update()
    pose = {pb.name: pb.rotation_quaternion.copy() for pb in arm.pose.bones}; ploc = arm.pose.bones["pelvis"].location.copy()
    act = bpy.data.actions.new(arm.name + "_act"); ad.action = act
    for pb in arm.pose.bones: pb.rotation_quaternion = pose[pb.name]
    arm.pose.bones["pelvis"].location = ploc
    bpy.context.view_layer.update()
    ls = 1 if arm.pose.bones["upperarm_l"].head.x > arm.pose.bones["upperarm_r"].head.x else -1   # which way is the person's left
    if arms == "bar":       # a slight lean in, forearms resting on the counter (forward = -Y in armature space; spine first)
        align(arm, "spine_01", (0, -0.12, 1)); align(arm, "spine_03", (0, -0.16, 1)); align(arm, "neck_01", (0, 0.1, 1))
        for s, xs in (("l", ls), ("r", -ls)):
            align(arm, f"upperarm_{s}", (0.12 * xs, -0.8, -0.6)); align(arm, f"lowerarm_{s}", (-0.05 * xs, -1.0, 0.1)); align(arm, f"hand_{s}", (0.0, -1.0, -0.1))
    elif arms == "table":
        for s, xs in (("l", ls), ("r", -ls)):
            align(arm, f"upperarm_{s}", (0.2 * xs, -0.55, -0.75)); align(arm, f"lowerarm_{s}", (-0.3 * xs, -0.95, 0.05)); align(arm, f"hand_{s}", (-0.2 * xs, -1.0, -0.1))
    key_all(arm, 1); key_all(arm, DUR)
    return act

def breathe(arm, amp=0.7, period=4.2, phase=0.0):
    sp = arm.pose.bones["spine_03"]; sc.frame_set(1); q0 = sp.rotation_quaternion.copy()
    t = phase
    while t < DUR_S + period:
        f = int(t * FPS)
        if 1 < f < DUR:
            sp.rotation_quaternion = q0 @ Quaternion((1, 0, 0), math.radians(amp)); sp.keyframe_insert("rotation_quaternion", frame=f, group="spine_03")
        f2 = int((t + period / 2) * FPS)
        if 1 < f2 < DUR:
            sp.rotation_quaternion = q0; sp.keyframe_insert("rotation_quaternion", frame=f2, group="spine_03")
        t += period

HEADS = ("neck_01", "neck_02", "head")
def look(arm, t0, t1, yaw=0.0, nod=0.0, hold=None):
    """from t0 turn the head (yaw +left/-right about Z, nod +down about X), reached at t1; hold until `hold` s then keys stay."""
    f0, f1 = int(t0 * FPS), int(t1 * FPS)
    sc.frame_set(f0); key(arm, HEADS, f0)
    sc.frame_set(f1)
    turn(arm, "neck_01", "Z", yaw * 0.35); turn(arm, "head", "Z", yaw * 0.65)
    if nod: turn(arm, "neck_01", "X", nod * 0.4); turn(arm, "head", "X", nod * 0.6)
    key(arm, HEADS, f1)
    if hold: sc.frame_set(int(hold * FPS)); key(arm, HEADS, int(hold * FPS))

# Jalen: isaiah (lean, dark hair, beard) lifted toward the decided medium mixed tone; worn brown field shirt (the bible's coat)
jalen, jm, ja = load_person("isaiah", "Jalen")
tint_skin(jm, (0.78, 0.55, 0.40), 0.55)
cloth(jm, shirt=(0.19, 0.12, 0.07), pants=(0.09, 0.08, 0.07), shoes=(0.05, 0.04, 0.03))
seat(jalen, ja, JX, SY + 0.02, 0.785, facing(0, 1))
# his right hand rests against the glass: move the set's glass to the hand
hr = bone_world(jalen, "middle_metacarpal_r")      # (bone tails from the glTF import are junk - use the next joint's head)
for nm in ("Coaster", "Highball"):
    o = bpy.data.objects[nm]; o.location = (hr.x + 0.07, hr.y + 0.03, o.location.z)
for k in range(3):
    o = bpy.data.objects["Ice%d" % k]; o.location = (hr.x + 0.07 + (k - 1) * 0.012, hr.y + 0.03 + (k - 1) * 0.01, o.location.z + 0.0)
# condensation: a beaded, half-wet glass reads at macro
gl = bpy.data.objects["Highball"]; gm = mat_("HighballGlass", (0.9, 0.92, 0.9), 0.05); gl.data.materials.clear(); gl.data.materials.append(gm)
gn = gm.node_tree; gb = gn.nodes["Principled BSDF"]; gb.inputs["Transmission Weight"].default_value = 1.0; gb.inputs["IOR"].default_value = 1.5
cola = mat_("ColaLiquid", (0.12, 0.05, 0.015), 0.05); cb = cola.node_tree.nodes["Principled BSDF"]; cb.inputs["Transmission Weight"].default_value = 0.7; cb.inputs["IOR"].default_value = 1.34
liq = cyl("ColaInGlass", (gl.location.x, gl.location.y, gl.location.z + 0.004), 0.0355, 0.108, cola, "x", verts=32)
liq.parent = gl; liq.matrix_parent_inverse = gl.matrix_world.inverted()
gb.inputs["Roughness"].default_value = 0.05
nz = gn.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 260; nz.inputs["Detail"].default_value = 2
vr = gn.nodes.new("ShaderNodeValToRGB"); vr.color_ramp.elements[0].position = 0.52; vr.color_ramp.elements[1].position = 0.6
gn.links.new(nz.outputs["Fac"], vr.inputs[0])
bp = gn.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.6; bp.inputs["Distance"].default_value = 0.0008
gn.links.new(vr.outputs[0], bp.inputs["Height"]); gn.links.new(bp.outputs[0], gb.inputs["Normal"])
rr = gn.nodes.new("ShaderNodeMapRange"); rr.inputs["To Min"].default_value = 0.45; rr.inputs["To Max"].default_value = 0.06
gn.links.new(vr.outputs[0], rr.inputs["Value"]); gn.links.new(rr.outputs[0], gb.inputs["Roughness"])

# Mateo: walter (older, grey) - beard darkened toward salt-and-pepper, faded work shirt. Walks in from the door, then seated.
mateo, mm, ma = load_person("walter", "Mateo")
hair_tint(mm, 0.35)
cloth(mm, shirt=(0.22, 0.26, 0.30), pants=(0.12, 0.10, 0.08), shoes=(0.06, 0.05, 0.04))
mateo_walk, mw, mwa = load_person("walter", "MateoWalk")
hair_tint(mw, 0.35); cloth(mw, shirt=(0.22, 0.26, 0.30), pants=(0.12, 0.10, 0.08), shoes=(0.06, 0.05, 0.04))

# ---- shot plan (seconds) --------------------------------------------------------------------------------------------
SH = {  # name: (start, end)
 "s1_exterior": (0, 11), "s2_wide": (11, 27), "s3_jalen": (27, 37), "s4_pilings": (37, 46), "s5_room": (46, 68.5),
 "s6_walkin": (68.5, 74.5), "s7_twoshot": (74.5, 87.5), "s8a_jalen_listens": (87.5, 92.3), "s8b_mateo_listens": (92.3, 96.5),
 "s8c_wide_bar": (96.5, 109.5), "s9_doorway": (109.5, 116),
}
WALK0, WALK1 = 68.8, 74.3

# Mateo seated (visible only from s7 on); the walking copy visible only during s6
seat(mateo, ma, MX, SY + 0.02, 0.785, facing(0, 1))
def visible(o, spans):
    """hide an object (and its children) outside the given (start,end) spans"""
    objs = [o] + list(o.children_recursive)
    for ob in objs:
        for f, hidden in [(1, True)] + [(int(a * FPS), False) for a, b_ in spans] + [(int(b_ * FPS) + 1, True) for a, b_ in spans]:
            ob.hide_render = hidden; ob.keyframe_insert("hide_render", frame=f)
            ob.hide_viewport = hidden; ob.keyframe_insert("hide_viewport", frame=f)
visible(mateo, [(SH["s7_twoshot"][0], DUR_S)])
visible(mateo_walk, [(SH["s6_walkin"][0], SH["s6_walkin"][1])])

# the walk: door (east wall, x=W, y 1.2-2.3) to the stool
P0 = Vector((W - 0.3, 1.75, 0)); P1 = Vector((MX + 0.35, SY - 0.55, 0))
d = P1 - P0; dist = d.length; dn = d / dist
mateo_walk.rotation_mode = "XYZ"; mateo_walk.location = P0; mateo_walk.rotation_euler = (0, 0, facing(dn.x, dn.y))
ad = mateo_walk.animation_data
for t in list(ad.nla_tracks): ad.nla_tracks.remove(t)
ad.action = None
walk_a, idle_a = mwa["Walk"], mwa["Idle"]
WF0, WF1 = int(WALK0 * FPS), int(WALK1 * FPS)
SPEED = 1.1     # m/s, an older man
walk_len = dist / SPEED
tw = ad.nla_tracks.new(); sw = tw.strips.new("walk", WF0, walk_a); sw.scale = 1.87 / SPEED
sw.repeat = max(1, math.ceil(walk_len * FPS / ((walk_a.frame_range[1] - walk_a.frame_range[0]) * sw.scale)))
ti = ad.nla_tracks.new(); si = ti.strips.new("idle", WF0 + int(walk_len * FPS) - 3, idle_a); si.extrapolation = "HOLD_FORWARD"; si.blend_in = 10
for st, a in ((sw, walk_a), (si, idle_a)):
    try: st.action_slot = a.slots[0]
    except Exception as e: print("slot", e)
mateo_walk.keyframe_insert("location", frame=WF0)
mateo_walk.location = P1; mateo_walk.keyframe_insert("location", frame=WF0 + int(walk_len * FPS))
linear(mateo_walk)

# patrons at the tables (the murmur): two couples and a man alone by the window
TABLES = [(1.9, 1.5), (4.9, 1.6), (8.0, 1.5), (1.5, 3.4)]
def at_table(name, tag, ti_, k, arms="table", shirt=None, pants=None):
    arm, ms, ac = load_person(name, tag)
    x, y = TABLES[ti_]; a = k * 2 * math.pi / 3 + ti_
    cx, cy = x + math.cos(a) * 0.62, y + math.sin(a) * 0.62
    cloth(ms, shirt=shirt, pants=pants, shoes=(0.05, 0.045, 0.04))
    seat(arm, ac, cx, cy, 0.46, a - math.pi / 2, arms=arms)
    breathe(arm, 0.6, random.uniform(3.6, 5.0), random.random() * 4)
    return arm
p1 = at_table("jorge", "P_jorge", 1, 0, shirt=(0.55, 0.50, 0.38), pants=(0.14, 0.12, 0.10))
p2 = at_table("sunita", "P_sunita", 1, 1, shirt=(0.45, 0.22, 0.18), pants=(0.10, 0.09, 0.09))
p3 = at_table("aoi", "P_aoi", 0, 2, shirt=(0.30, 0.34, 0.30), pants=(0.12, 0.11, 0.10))
p4 = at_table("zuri", "P_zuri", 0, 0, shirt=(0.62, 0.55, 0.30), pants=(0.15, 0.13, 0.11))
p5 = at_table("ada", "P_ada", 2, 1, shirt=(0.25, 0.28, 0.35), pants=(0.10, 0.10, 0.11))
for arm_ in (p1, p2, p3, p4, p5):
    look(arm_, 1 / FPS, 0.5, yaw=random.uniform(-10, 10), nod=random.uniform(10, 16))
# a second glass for Mateo and glasses on the tables
for i, (x, y) in enumerate(TABLES[:3]):
    for k in range(2):
        lathe("TGlass%d_%d" % (i, k), [(0, 0), (0.034, 0), (0.036, 0.004), (0.038, 0.12), (0.0365, 0.12), (0.0352, 0.1), (0, 0.1)],
              (x + random.uniform(-0.2, 0.2), y + random.uniform(-0.2, 0.2), 0.7375), M["cola"], "x")
mh = bone_world(mateo, "middle_metacarpal_r")
lathe("MateoGlass", [(0, 0), (0.034, 0), (0.036, 0.004), (0.038, 0.11), (0.0365, 0.11), (0.0352, 0.09), (0, 0.09)], (mh.x + 0.08, mh.y + 0.02, 1.074), M["cola"], "x")

# ---- performances -------------------------------------------------------------------------------------------------------
breathe(jalen, 0.8, 4.4, 0.3); breathe(mateo, 0.7, 5.0, 1.1)
# Jalen alone: head down at the glass, a slow lift to the mirror and back
look(jalen, 1 / FPS, 0.5, yaw=4, nod=20)   # the rest pose looks ~12 deg up: everyone gets a base nod down
look(jalen, 29.0, 31.5, yaw=-3, nod=-7)
look(jalen, 34.5, 36.5, yaw=2, nod=5)
# Mateo arrives (s7): Jalen glances right at him, then back to the glass; Mateo looks at Jalen
look(jalen, 75.0, 76.3, yaw=-38, nod=-6)
look(jalen, 79.5, 81.0, yaw=30, nod=6)
look(mateo, 1 / FPS, 0.5, yaw=28, nod=14)
# "You look like a man with a story" (88-90.2): Jalen turns to him, wry; "Don't we all?" (90.8); Mateo: slow nod, looks to the door
look(jalen, 88.3, 89.6, yaw=-36, nod=-4)
look(mateo, 90.6, 91.8, nod=6); look(mateo, 92.6, 93.6, nod=-6)
look(jalen, 95.0, 96.5, yaw=8, nod=4)
# n09 "He gestured with his glass towards the open doorway" (95.5-104): Mateo turns toward the door (east = his right) and holds
look(mateo, 97.0, 99.0, yaw=-75, nod=-3)
look(jalen, 100.0, 101.8, yaw=-42, nod=-3)
look(mateo, 106.0, 108.0, yaw=35)

# ---- cameras ------------------------------------------------------------------------------------------------------------
bpy.ops.object.camera_add(); cam = bpy.context.object; cam.name = "Cam"; sc.camera = cam; cam.rotation_mode = "QUATERNION"
cd = cam.data; cd.sensor_width = 36; cd.dof.use_dof = True; cd.dof.aperture_blades = 7
HJ = bone_world(jalen, "head"); HM = bone_world(mateo, "head")
EYE_J = Vector((HJ.x, HJ.y, HJ.z + 0.07)); EYE_M = Vector((HM.x, HM.y, HM.z + 0.07))
print("heads", HJ, HM)
print("JALEN FOOT DIR (forward?)", (bone_world(jalen, "ball_r") - bone_world(jalen, "foot_r")).normalized())
print("HAND_R tail", hr, "GLASS", bpy.data.objects["Highball"].location[:], "EYE_J", EYE_J, "hand_l", bone_world(jalen, "middle_metacarpal_l"))

def aim(pos, target):
    dv = Vector(target) - Vector(pos); return dv.to_track_quat("-Z", "Y")

def shot(name, p0, t0, p1, t1, lens, fstop, focus0=None, focus1=None, roll=0.0):
    a, b_ = SH[name]; fa, fb = int(a * FPS) + 1, int(b_ * FPS)
    for f, p, t, fo in ((fa, p0, t0, focus0), (fb, p1, t1, focus1)):
        sc.frame_set(f)
        cam.location = p; cam.rotation_quaternion = aim(p, t)
        cam.keyframe_insert("location", frame=f); cam.keyframe_insert("rotation_quaternion", frame=f)
        cd.lens = lens; cd.keyframe_insert("lens", frame=f)
        cd.dof.aperture_fstop = fstop; cd.dof.keyframe_insert("aperture_fstop", frame=f)
        cd.dof.focus_distance = (Vector(fo) - Vector(p)).length if fo else (Vector(t) - Vector(p)).length
        cd.dof.keyframe_insert("focus_distance", frame=f)

# s1: from the water, the bar's lit front, string lights, pilings; slow drift to the right and in
shot("s1_exterior", (3.0, -14.0, 0.6), (5.2, -1.0, 1.9), (4.6, -11.5, 0.7), (5.4, -1.0, 1.9), 32, 4.0)
# s2: the room from inside the street door: tables, the bar beyond, Jalen alone under a pendant; slow push
shot("s2_wide", (W - 1.0, 2.75, 1.62), (JX - 0.3, SY + 0.3, 1.25), (W - 2.0, 2.95, 1.58), (JX - 0.2, SY + 0.3, 1.25), 30, 2.8, EYE_J, EYE_J)
# s3: from behind the bar, Jalen with the glass; focus pulls from the glass to his face
GL = Vector(bpy.data.objects["Highball"].location) + Vector((0, 0, 0.08))
shot("s3_jalen", (JX + 0.55, SY + 1.45, 1.30), (GL.x, GL.y, GL.z + 0.02), (JX + 0.45, SY + 1.35, 1.33), (EYE_J.x, EYE_J.y, EYE_J.z - 0.05), 50, 1.8, GL, EYE_J)
# s4: outside, low over the water: pilings, the slosh, the window glow on the water
shot("s4_pilings", (9.8, -6.6, -0.75), (2.6, -2.5, 1.1), (9.3, -6.3, -0.7), (2.4, -2.4, 1.15), 35, 2.8, (5.9, -3.0, -0.6), (5.9, -3.0, -0.6))
for f_, ex in ((1, 1.1), (int(SH["s4_pilings"][0] * FPS), 1.1), (int(SH["s4_pilings"][0] * FPS) + 1, 1.8), (int(SH["s4_pilings"][1] * FPS), 1.8), (int(SH["s4_pilings"][1] * FPS) + 1, 1.1)):
    sc.view_settings.exposure = ex; sc.view_settings.keyframe_insert("exposure", frame=f_)
for fc in (sc.animation_data.action.fcurves if sc.animation_data and sc.animation_data.action and hasattr(sc.animation_data.action, "fcurves") else []):
    for k in fc.keyframe_points: k.interpolation = "CONSTANT"
# s5: the room - starts on the table by the window, pans and tracks past the patrons to Jalen at the bar
shot("s5_room", (3.0, 0.55, 1.40), (4.9, 1.6, 0.95), (6.6, 0.5, 1.45), (JX + 0.1, SY + 0.2, 1.3), 35, 2.5, (4.9, 1.6, 0.95), EYE_J)
# s6: Mateo walks in - from behind the bar over Jalen's shoulder toward the door
shot("s6_walkin", (JX - 0.95, SY + 1.45, 1.45), (W - 0.6, 1.75, 1.45), (JX - 0.85, SY + 1.40, 1.45), (MX + 0.6, SY, 1.4), 35, 2.8, (W - 0.6, 1.75, 1.4), (MX + 0.4, SY, 1.4))
# s7: two-shot from behind the bar, both men above the counter, slow push
MID = (EYE_J + EYE_M) / 2
shot("s7_twoshot", (MID.x - 0.1, SY + 2.0, 1.42), MID, (MID.x - 0.05, SY + 1.85, 1.40), MID, 40, 2.5, EYE_J, EYE_J)
# s8a: over Mateo's shoulder onto Jalen as Mateo speaks (Jalen listens, turns)
shot("s8a_jalen_listens", (MX + 0.75, SY - 0.55, 1.50), EYE_J, (MX + 0.70, SY - 0.52, 1.50), EYE_J, 45, 2.0, EYE_J, EYE_J)
# s8b: over Jalen's shoulder onto Mateo for "Don't we all?" (Mateo listens, nods)
shot("s8b_mateo_listens", (JX - 0.75, SY - 0.55, 1.50), EYE_M, (JX - 0.70, SY - 0.52, 1.50), EYE_M, 45, 2.0, EYE_M, EYE_M)
# s8c: the wide along the bar from the west end, counter in the foreground, the two men small, the doorway far right
shot("s8c_wide_bar", (2.0, 4.45, 1.32), (MX, SY, 1.25), (2.15, 4.42, 1.32), (MX + 0.2, SY, 1.25), 35, 3.5, EYE_J, EYE_J)
# s9: the open doorway from inside - the lane, the lamp, the dark beyond; very slow push
shot("s9_doorway", (W - 3.6, 2.6, 1.45), (W + 0.4, 1.75, 1.3), (W - 3.1, 2.5, 1.45), (W + 0.5, 1.75, 1.3), 40, 2.8, (W + 0.4, 1.75, 1.3), (W + 0.4, 1.75, 1.3))

# camera keys: ease within a shot, hard cut between shots
cam_curves = []
for idb in (cam, cd):
    ad_ = idb.animation_data
    if not ad_ or not ad_.action: continue
    cs = getattr(ad_.action, "fcurves", None)
    if cs is None:
        try: cs = [fc for layer in ad_.action.layers for strip in layer.strips for bag in strip.channelbags for fc in bag.fcurves]
        except Exception: cs = []
    cam_curves += list(cs)
cut_frames = {int(b_ * FPS) for a, b_ in SH.values()}
for fc in cam_curves:
    for k in fc.keyframe_points:
        k.interpolation = "CONSTANT" if int(k.co[0]) in cut_frames else "BEZIER"
        k.easing = "EASE_IN_OUT"

# ---- outputs ---------------------------------------------------------------------------------------------------------------
if arg("--save"): bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(arg("--save")))
if arg("--still"):
    i = argv.index("--still"); f = int(argv[i + 1]); outp = argv[i + 2]
    sc.frame_set(f); sc.render.filepath = os.path.abspath(outp); bpy.ops.render.render(write_still=True); print("STILL", outp)
if arg("--stills"):
    outd = os.path.abspath(arg("--stills")); os.makedirs(outd, exist_ok=True)
    for f in [int(x) for x in arg("--frames", "120").split(",")]:
        sc.frame_set(f); sc.render.filepath = os.path.join(outd, "t_%04d.png" % f); bpy.ops.render.render(write_still=True); print("STILL", f, flush=True)
if arg("--anim"):
    outd = os.path.abspath(arg("--anim")); os.makedirs(outd, exist_ok=True)
    f0, f1 = int(arg("--start", sc.frame_start)), int(arg("--end", sc.frame_end))
    import time
    for f in range(f0, f1 + 1):
        p = os.path.join(outd, "f_%04d.png" % f)
        if os.path.exists(p) and os.path.getsize(p) > 1000: continue
        t0 = time.time(); sc.frame_set(f); sc.render.filepath = p; bpy.ops.render.render(write_still=True)
        print("FRAME %d %.1fs" % (f, time.time() - t0), flush=True)
