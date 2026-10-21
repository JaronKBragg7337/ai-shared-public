# The Loft's people, part 2 (part 1 = necklace-unreal/loft_people.py, which builds a MetaHuman preset at "optimized LOW" and
# exports FBX). This turns that export into one phone-weight GLB for the Loft page:
#   - face + body + clothes + beard on ONE skeleton, the ~320 helper/corrective bones folded into ~70 main ones
#   - Epic's stand and walk loops copied on, plus a sitting pose made here (couch: hips down, knees up, hands on thighs)
#   - small JPEG textures (face 1024, body 1024), clothes coloured per person
# blender -b --python person.py -- Isaiah [--shirt 0.35,0.36,0.38] [--shorts 0.05,0.07,0.12] [--render]
import bpy, os, sys, re, math, json, glob
from mathutils import Vector, Matrix
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else ["Isaiah"]
NAME = argv[0]
opt = lambda k, d: argv[argv.index(k) + 1] if k in argv else d
rgb = lambda s: tuple(float(x) for x in s.split(",")) + (1.0,)
SHIRT, SHORTS = rgb(opt("--shirt", "0.30,0.31,0.33")), rgb(opt("--shorts", "0.04,0.06,0.11"))
D = f"C:/Users/lilli/Projects/necklace-unreal/Saved/LoftPeople/{NAME}/"
OUT = "C:/Users/lilli/Projects/heartbeat-observatory/homes/people/"
CHK = "C:/Users/lilli/Projects/necklace-unreal/Saved/LoftPeople/_checks/"   # check renders stay off the site
os.makedirs(CHK, exist_ok=True)
os.makedirs(OUT, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
P = lambda *a: print("PERSON |", *a, flush=True)

def imp(f, anim=False):
    before = set(bpy.data.objects)
    bpy.ops.import_scene.fbx(filepath=D + f, use_anim=anim, ignore_leaf_bones=True, automatic_bone_orientation=False)
    new = [o for o in bpy.data.objects if o not in before]
    return next((o for o in new if o.type == "ARMATURE"), None), [o for o in new if o.type == "MESH"]

arm, (body,) = imp(f"SKM_{NAME}_BodyMesh.fbx")
farm, (face,) = imp(f"SKM_{NAME}_FaceMesh.fbx")
oarm, outfits = imp(f"{NAME}_Outfits.fbx")
arm.name = "Person"; body.name = "Body"; face.name = "Face"

KEEP = re.compile(r"^(pelvis|spine_0[1-5]|neck_0[12]|head|clavicle_[lr]|upperarm_[lr]|lowerarm_[lr]|hand_[lr]|"
                  r"(thumb|index|middle|ring|pinky)_0[123]_[lr]|(index|middle|ring|pinky)_metacarpal_[lr]|thigh_[lr]|calf_[lr]|foot_[lr]|ball_[lr])$")

# the body skeleton stops at the neck; the head bone lives in the face skeleton - add it to the master
bpy.context.view_layer.objects.active = arm; bpy.ops.object.mode_set(mode="EDIT")
eb = arm.data.edit_bones; fh = farm.data.bones["head"]
hb = eb.new("head"); fmw = farm.matrix_world
hb.head = (0, 0, 0); hb.tail = (0, fh.length, 0)
hb.matrix = arm.matrix_world.inverted() @ fmw @ fh.matrix_local   # same orientation as Epic's head bone, so the loops' head turns fit
hb.parent = eb["neck_02"]
bpy.ops.object.mode_set(mode="OBJECT")

def keep_of(src_arm, name):   # walk up the source skeleton to the first bone we keep
    b = src_arm.data.bones.get(name)
    while b is not None and not KEEP.match(b.name): b = b.parent
    return b.name if b is not None else "pelvis"

def rebind(mesh, src_arm):
    groups = {g.index: g.name for g in mesh.vertex_groups}
    target = {i: keep_of(src_arm, n) if not KEEP.match(n) else n for i, n in groups.items()}
    acc = {}
    for v in mesh.data.vertices:
        w = {}
        for g in v.groups:
            t = target.get(g.group)
            if t: w[t] = w.get(t, 0) + g.weight
        acc[v.index] = w
    for g in list(mesh.vertex_groups): mesh.vertex_groups.remove(g)
    vg = {}
    for vi, w in acc.items():
        tot = sum(w.values()) or 1
        for n, x in sorted(w.items(), key=lambda kv: -kv[1])[:4]:   # glTF: 4 influences
            if n not in vg: vg[n] = mesh.vertex_groups.new(name=n)
            vg[n].add([vi], x / tot, "REPLACE")
    mw = mesh.matrix_world.copy(); mesh.parent = arm; mesh.matrix_world = mw
    for m in list(mesh.modifiers):
        if m.type == "ARMATURE": mesh.modifiers.remove(m)
    mod = mesh.modifiers.new("Armature", "ARMATURE"); mod.object = arm
    P("rebound", mesh.name, "groups", len(mesh.vertex_groups))

rebind(body, arm); rebind(face, farm)
for i, o in enumerate(outfits): o.name = "Outfit%d" % i; rebind(o, oarm)
# hair / beard / moustache: Epic's strand CARDS with their cut-out atlas (eyes.py bakes _<groom>_card.png: colour + strands
# in the alpha), riding on the head bone. Falls back to the solid LOD5 "helmet" shell if a card texture is missing.
hair_objs = []   # (object, groom, card texture path or None)
grooms = sorted({os.path.basename(f).split("_CardsMesh")[0] for f in glob.glob(D + "*_CardsMesh_Group0_LOD0.fbx")}) or          sorted({os.path.basename(f).split("_Helmet")[0] for f in glob.glob(D + "*_Helmet_LOD5.fbx")})
for g in grooms:
    card = D + f"groom/_{g}_card.png"
    lod = 2 if g.startswith("Hair") else 3   # head hair: more cards; beards and moustaches: fewer
    f = D + f"{g}_CardsMesh_Group0_LOD{lod}.fbx"
    if not (os.path.exists(card) and os.path.exists(f)): f, card = D + f"{g}_Helmet_LOD5.fbx", None
    _, ms = imp(os.path.basename(f))
    for m in ms:
        m.name = g; vg = m.vertex_groups.new(name="head"); vg.add(list(range(len(m.data.vertices))), 1.0, "REPLACE")
        mw = m.matrix_world.copy(); m.parent = arm; m.matrix_world = mw
        md = m.modifiers.new("Armature", "ARMATURE"); md.object = arm; hair_objs.append((m, g, card))
        P("hair", g, "cards" if card else "helmet", sum(len(p.vertices) - 2 for p in m.data.polygons), "tris")
for o in (farm, oarm): bpy.data.objects.remove(o, do_unlink=True)

# fold the helper bones away
bpy.context.view_layer.objects.active = arm; bpy.ops.object.mode_set(mode="EDIT")
for b in [b for b in arm.data.edit_bones if not KEEP.match(b.name)]: arm.data.edit_bones.remove(b)
bpy.ops.object.mode_set(mode="OBJECT"); P("bones kept", len(arm.data.bones))

# lighter clothes: 25k -> ~7k triangles
for o in outfits:
    d = o.modifiers.new("dec", "DECIMATE"); d.ratio = 0.28
    bpy.context.view_layer.objects.active = o; bpy.ops.object.modifier_move_to_index(modifier="dec", index=0); bpy.ops.object.modifier_apply(modifier="dec")
    P("outfit tris", sum(len(p.vertices) - 2 for p in o.data.polygons))

# ---- materials (glTF-friendly): baked MetaHuman colour maps, shrunk
def img(name, size):
    p = D + "tex/" + name + ".png"
    if not os.path.exists(p): P("missing", name); return None
    im = bpy.data.images.load(p); im.scale(size, size) if im.size[0] > size else None; im.file_format = "JPEG"; return im
def mat(name, im=None, color=(0.5, 0.5, 0.5, 1), rough=0.6, nrm=None):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; bs = nt.nodes["Principled BSDF"]
    bs.inputs["Roughness"].default_value = rough
    if im: t = nt.nodes.new("ShaderNodeTexImage"); t.image = im; nt.links.new(t.outputs["Color"], bs.inputs["Base Color"])
    else: bs.inputs["Base Color"].default_value = color
    if nrm:
        nrm.colorspace_settings.name = "Non-Color"; t = nt.nodes.new("ShaderNodeTexImage"); t.image = nrm; nm = nt.nodes.new("ShaderNodeNormalMap")
        nt.links.new(t.outputs["Color"], nm.inputs["Color"]); nt.links.new(nm.outputs["Normal"], bs.inputs["Normal"])
    return m
M_BODY = mat("Skin_Body", img("T_Body_BC", 1024), rough=0.55)
M_FACE = mat("Skin_Face", img("T_Head_LOD5to7_BC", 1024), rough=0.5, nrm=img("T_Head_LOD5to7_N", 1024))
M_TEETH = mat("Teeth", img("T_Teeth_BC", 256), rough=0.3)
# Unreal draws the iris over the sclera in its eye shader; here it is painted in: iris disc (UV radius ~0.15) at the centre
def eye_tex(side):   # painted by eyes.py (normal Python has the image library; Blender's doesn't)
    p = D + f"tex/_eye{side}.png"
    if not os.path.exists(p): return img(f"T_EyeSclera{side}_BC", 256)
    im = bpy.data.images.load(p); im.file_format = "JPEG"; return im
M_EYEL = mat("EyeL", eye_tex("L"), rough=0.12); M_EYER = mat("EyeR", eye_tex("R"), rough=0.12)
M_SHIRT = mat("Shirt", color=SHIRT, rough=0.85); M_SHORTS = mat("Shorts", color=SHORTS, rough=0.8)
HAIRC = rgb(opt("--hair", "0.018,0.012,0.009"))
M_HAIR = mat("Hair", color=HAIRC, rough=0.75)
def card_mat(g, path):   # strands: colour + cut-out alpha; the page sets alpha-test + double-sided on "HairCard_*"
    im = bpy.data.images.load(path); im.file_format = "PNG"
    m = bpy.data.materials.new("HairCard_" + g); m.use_nodes = True; nt = m.node_tree; bs = nt.nodes["Principled BSDF"]
    t = nt.nodes.new("ShaderNodeTexImage"); t.image = im
    nt.links.new(t.outputs["Color"], bs.inputs["Base Color"]); nt.links.new(t.outputs["Alpha"], bs.inputs["Alpha"])
    bs.inputs["Roughness"].default_value = 0.55
    try: m.surface_render_method = "DITHERED"
    except Exception: m.blend_method = "CLIP"
    m.use_backface_culling = False
    return m
def remat(o, pick):
    for i, s in enumerate(o.material_slots): o.material_slots[i].material = pick(s.material.name if s.material else "")
remat(body, lambda n: M_BODY)
# the FBX slot names don't line up with the polygons, so tell the parts apart by shape: the skin is by far the biggest set,
# the eyes are the two balls either side, whatever is left is the teeth
from collections import defaultdict
fs = defaultdict(list)
for pg in face.data.polygons: fs[pg.material_index].append(face.matrix_world @ pg.center)
info = {i: (len(c), sum(c, Vector()) / len(c)) for i, c in fs.items()}
skin = max(info, key=lambda i: info[i][0]); rest = [i for i in info if i != skin]
eyes = sorted([i for i in rest if abs(info[i][1].x) > 0.015], key=lambda i: -info[i][0])[:2]
by_slot = {skin: M_FACE}
for i in eyes: by_slot[i] = M_EYEL if info[i][1].x > 0 else M_EYER
for i in rest:
    if i not in by_slot: by_slot[i] = M_TEETH
P("face parts", {i: (info[i][0], round(info[i][1].x, 3), by_slot[i].name) for i in info})
for i in range(len(face.material_slots)): face.material_slots[i].material = by_slot.get(i, M_FACE)
for o in outfits: remat(o, lambda n: M_SHIRT if "Shirt" in n else M_SHORTS)
for o, g, card in hair_objs:
    cm = card_mat(g, card) if card else M_HAIR
    remat(o, lambda n: cm)
hair_objs = [o for o, g, card in hair_objs]
for o in [body, face] + outfits + hair_objs:
    bpy.context.view_layer.objects.active = o; o.select_set(True)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True); o.select_set(False)

# ---- real clothes (Jaron 9/27): long pants + shoes grown from the person's own skin (offset outward, same skinning, so they
# bend exactly with the body), replacing Epic's shorts and the bare feet. The skin under them is removed.
import bmesh
PANTS, SHOES = rgb(opt("--pants", "0.035,0.055,0.11")), rgb(opt("--shoes", "0.85,0.85,0.84"))
M_PANTS = mat("Pants", color=PANTS, rough=0.9); M_SHOES = mat("Shoes", color=SHOES, rough=0.6)
gnames = {g.index: g.name for g in body.vertex_groups}
dom = {v.index: gnames.get(max(v.groups, key=lambda g: g.weight).group) if len(v.groups) else None for v in body.data.vertices}
pel_z = (arm.matrix_world @ arm.data.bones["pelvis"].head_local).z
WAIST, ANKLE = pel_z + 0.08, 0.115
LEGS = re.compile(r"^(pelvis|spine_01|thigh_[lr]|calf_[lr])$"); FEET = re.compile(r"^(foot_[lr]|ball_[lr])$")
BW = body.matrix_world.copy(); BS = BW.to_scale().z   # measure in metres (the mesh itself may still be in Unreal's cm)
co = {v.index: BW @ v.co for v in body.data.vertices}
P("body z range", round(min(c.z for c in co.values()), 3), round(max(c.z for c in co.values()), 3), "pelvis", round(pel_z, 3), "legs", sum(1 for i in co if dom[i] and LEGS.match(dom[i])))
in_pants = {i for i, c in co.items() if ANKLE - 0.01 < c.z < WAIST and dom[i] and LEGS.match(dom[i])}
in_shoes = {i for i, c in co.items() if (dom[i] and FEET.match(dom[i])) or (c.z < ANKLE + 0.015 and dom[i] and re.match(r"calf_", dom[i]))}
def grow(name, keep, off, m, smooth=0):
    o = body.copy(); o.data = body.data.copy(); o.name = name; bpy.context.collection.objects.link(o)
    bm = bmesh.new(); bm.from_mesh(o.data); bm.verts.ensure_lookup_table()
    bmesh.ops.delete(bm, geom=[f for f in bm.faces if not all(v.index in keep for v in f.verts)], context="FACES")
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if not v.link_faces], context="VERTS")
    if smooth:   # shoes: wrap each foot in its own smooth shell (a convex hull) - one rounded toe box, like a sneaker
        dl = bm.verts.layers.deform.active; side = {}
        for v in bm.verts:
            w = v[dl] if dl else {}
            best = max(w.items(), key=lambda kv: kv[1])[0] if len(w) else None
            side.setdefault(gnames.get(best, "_l")[-2:], []).append(v)
        bmesh.ops.delete(bm, geom=list(bm.faces), context="FACES_ONLY")   # the bare foot surface goes; its points stay for the hull
        for vs in side.values():
            if len(vs) > 8: bmesh.ops.convex_hull(bm, input=vs, use_existing_faces=False)
        bmesh.ops.delete(bm, geom=[v for v in bm.verts if not v.link_faces], context="VERTS")   # points inside the shoe
        for _ in range(smooth): bmesh.ops.smooth_vert(bm, verts=bm.verts, factor=0.35, use_axis_x=True, use_axis_y=True, use_axis_z=True)
    bm.normal_update()
    for v in bm.verts: v.co += v.normal * (off / BS)
    bm.to_mesh(o.data); bm.free()
    o.data.materials.clear(); o.data.materials.append(m)
    P("grew", name, len(o.data.polygons), "faces"); return o
pants = grow("Pants", in_pants, 0.011, M_PANTS)
shoes = grow("Shoes", in_shoes, 0.02, M_SHOES, smooth=8)
# skin that is fully covered goes (fewer triangles, nothing poking through at the knees)
covered = {i for i in in_pants if ANKLE + 0.03 < co[i].z < WAIST - 0.07} | in_shoes
bm = bmesh.new(); bm.from_mesh(body.data); bm.verts.ensure_lookup_table()
bmesh.ops.delete(bm, geom=[f for f in bm.faces if all(v.index in covered for v in f.verts)], context="FACES")
bm.to_mesh(body.data); bm.free()
# Epic's light build has no skin under the shorts, so the shorts stay and take the pants colour: shorts + the legs grown
# below them read as one pair of long pants
M_SHORTS.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = PANTS
M_SHORTS.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.9
outfits += [pants, shoes]

# ---- animation: copy Epic's loops bone by bone (same MetaHuman skeleton; local rotations carry over)
arm.rotation_mode = "XYZ"
for pb in arm.pose.bones: pb.rotation_mode = "QUATERNION"
REST_PELVIS = (arm.matrix_world @ arm.pose.bones["pelvis"].head).z
def copy_loop(fbx, action_name, step=1):
    src, ms = imp(fbx, anim=True)
    for m in ms: bpy.data.objects.remove(m, do_unlink=True)
    for pb in src.pose.bones: pb.rotation_mode = "QUATERNION"
    a = src.animation_data.action; f0, f1 = [int(x) for x in a.frame_range]
    bpy.context.scene.frame_set(f0); src_rest = None
    src_scale = src.matrix_world.to_scale().z
    act = bpy.data.actions.new(action_name); arm.animation_data_create(); arm.animation_data.action = act
    # neck + head stay this person's own: the loops were made on another body, and its neck angle tipped the head back
    sc = bpy.context.scene; names = [b.name for b in arm.pose.bones if b.name in src.pose.bones and b.name not in ("neck_01", "neck_02", "head")]
    # the source skeleton's resting hip height, to scale the hip bob to this person
    s_pel_rest = (src.matrix_world @ src.data.bones["pelvis"].head_local).z
    k = REST_PELVIS / max(0.3, s_pel_rest)
    out_f = 1
    for f in range(f0, f1 + 1, step):
        sc.frame_set(f)
        for n in names:
            d, s = arm.pose.bones[n], src.pose.bones[n]
            d.rotation_quaternion = s.rotation_quaternion.copy(); d.keyframe_insert("rotation_quaternion", frame=out_f, group=n)
        pl = arm.pose.bones["pelvis"]; pl.location = src.pose.bones["pelvis"].location * src_scale * k; pl.keyframe_insert("location", frame=out_f, group="pelvis")
        out_f += 1
    act.use_fake_user = True
    bpy.data.objects.remove(src, do_unlink=True)
    P("action", action_name, "frames", out_f - 1)
    return act
IDLE = copy_loop("AS_MH_Neutral_Stand_Idle_Loop.fbx", "Idle", step=2)
WALK = copy_loop("AS_MH_Neutral_Walk_Loop_F.fbx", "Walk", step=1)

# ---- sitting: built here. Forward is -Y, up +Z, the character's left is +X. Hips drop so the seat contact is at z = 0.
def reset_pose():
    for pb in arm.pose.bones: pb.rotation_quaternion = (1, 0, 0, 0); pb.location = (0, 0, 0)
    bpy.context.view_layer.update()
# Unreal bones don't point down the limb in Blender, so aim each joint at the next one instead
NEXT = {"spine_01": "spine_02", "spine_03": "spine_04", "neck_01": "neck_02", "neck_02": "head", "head": None}
for s_ in "lr":
    NEXT.update({f"thigh_{s_}": f"calf_{s_}", f"calf_{s_}": f"foot_{s_}", f"foot_{s_}": f"ball_{s_}", f"upperarm_{s_}": f"lowerarm_{s_}",
                 f"lowerarm_{s_}": f"hand_{s_}", f"hand_{s_}": f"middle_metacarpal_{s_}"})
def align(name, d):
    pb = arm.pose.bones[name]; bpy.context.view_layer.update()
    nx = NEXT.get(name)
    if not nx: return
    cur = (arm.pose.bones[nx].head - pb.head).normalized(); q = cur.rotation_difference(Vector(d).normalized())
    M = pb.matrix.copy(); t = M.to_translation()
    pb.matrix = Matrix.Translation(t) @ q.to_matrix().to_4x4() @ Matrix.Translation(-t) @ M
    bpy.context.view_layer.update()
SIT = bpy.data.actions.new("Sit"); arm.animation_data.action = SIT; reset_pose()
pl = arm.pose.bones["pelvis"]; M = pl.matrix.copy(); M.translation.z = 0.13; pl.matrix = M; bpy.context.view_layer.update()
align("spine_01", (0, 0.2, 1)); align("spine_03", (0, 0.1, 1)); align("neck_01", (0, -0.05, 1)); align("neck_02", (0, -0.1, 1))
for s, x in (("l", 1), ("r", -1)):
    # couch sitting: thighs a touch downhill, shins slanting out past the seat front, feet flat
    align(f"thigh_{s}", (0.1 * x, -1, -0.16)); align(f"calf_{s}", (0.05 * x, -0.32, -1)); align(f"foot_{s}", (0.05 * x, -1, -0.12))
    align(f"upperarm_{s}", (0.22 * x, -0.25, -0.94)); align(f"lowerarm_{s}", (-0.12 * x, -0.97, -0.2)); align(f"hand_{s}", (-0.08 * x, -0.9, -0.42))
for f in (1, 40):
    for pb in arm.pose.bones:
        pb.keyframe_insert("rotation_quaternion", frame=f, group=pb.name)
    pl.keyframe_insert("location", frame=f, group="pelvis")
SIT.use_fake_user = True
# gentle breathing on the sitter's chest
sp = arm.pose.bones["spine_03"]; bpy.context.scene.frame_set(20); q0 = sp.rotation_quaternion.copy()
from mathutils import Quaternion
sp.rotation_quaternion = q0 @ Quaternion((1, 0, 0), math.radians(1.2)); sp.keyframe_insert("rotation_quaternion", frame=20, group="spine_03")
P("sit pose made")

# ---- check renders (optional) and export
arm.animation_data.action = IDLE
def check_render():
    sc = bpy.context.scene
    try: sc.render.engine = "BLENDER_EEVEE"
    except Exception: sc.render.engine = "BLENDER_EEVEE_NEXT"
    sc.render.resolution_x, sc.render.resolution_y = 900, 1200
    w = bpy.data.worlds.new("W"); w.use_nodes = True; w.node_tree.nodes["Background"].inputs[0].default_value = (0.5, 0.52, 0.56, 1); w.node_tree.nodes["Background"].inputs[1].default_value = 0.8; sc.world = w
    sun = bpy.data.objects.new("Sun", bpy.data.lights.new("Sun", "SUN")); sun.data.energy = 3.5; sun.rotation_euler = (math.radians(50), 0, math.radians(-25)); sc.collection.objects.link(sun)
    cam = bpy.data.objects.new("Cam", bpy.data.cameras.new("Cam")); cam.data.lens = 50; sc.collection.objects.link(cam); sc.camera = cam
    for act, frame, tag, loc, look in ((IDLE, 1, "idle", (0.9, -3.6, 1.2), (0, 0, 0.95)), (WALK, 16, "walk", (2.4, -2.6, 1.1), (0, 0, 0.9)),
                                       (SIT, 1, "sit", (1.6, -2.6, 0.9), (0, -0.2, 0.3)), (IDLE, 1, "face", (0.18, -0.75, 1.68), (0, 0, 1.63))):
        arm.animation_data.action = act; sc.frame_set(frame)
        cam.location = loc; dvec = Vector(look) - Vector(loc); cam.rotation_euler = dvec.to_track_quat("-Z", "Y").to_euler()
        sc.render.filepath = CHK + f"_check_{NAME}_{tag}.png"; bpy.ops.render.render(write_still=True)
    arm.animation_data.action = None; reset_pose(); cam.location = (0.25, -1.1, 1.62); dvec = Vector((0, 0, 1.6)) - cam.location
    cam.rotation_euler = dvec.to_track_quat("-Z", "Y").to_euler(); sc.render.filepath = CHK + f"_check_{NAME}_rest.png"; bpy.ops.render.render(write_still=True)
    bpy.data.objects.remove(sun); bpy.data.objects.remove(cam)
if "--render" in argv: check_render()
arm.animation_data.action = IDLE
bpy.ops.object.select_all(action="DESELECT")
for o in [arm, body, face] + outfits + hair_objs: o.select_set(True)
bpy.ops.export_scene.gltf(filepath=OUT + NAME.lower() + ".glb", export_format="GLB", use_selection=True, export_animations=True,
                          export_animation_mode="ACTIONS", export_image_format="WEBP", export_image_quality=80, export_skins=True,
                          export_morph=False, export_apply=False, export_yup=True, export_force_sampling=True)
P("exported", OUT + NAME.lower() + ".glb", round(os.path.getsize(OUT + NAME.lower() + ".glb") / 1e6, 2), "MB")
