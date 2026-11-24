# Pioneer episode - the four STUDIO scenes (s01, s02, s10, s15) in Unreal. Fable, 11/15.
# Builds the news studio with the show's own builder (news_studio.py, build-only, NOT edited), then adds on top:
#   - the Joe/Vex walking rig from the approved movement test (movement/plan.py -> here studio/plan_s02.py -> motion_s02.json)
#   - the Heartbeat News live truck with a rocket on the back (primitives), parked stage left, and soft lights for the walk
#   - one level sequence per scene: desk scenes use the show's four cameras cut on the lines; s02 is one moving camera; s10 a slow push-in
# Things a scene does not use are parked far under the floor by their transform keys (Joe and Vex in s10, the truck stage in desk scenes).
# Every sequence has PRE frames of pre-roll that the encoder drops (frame 0 of a render shows a ghost of Joe's default pose).
# Run: UnrealEditor NecklaceFilm.uproject -ExecCmds="py <this file>"   Env: PIO_SCENES (s01,s02,s10,s15) PIO_RES PIO_SPATIAL PIO_TEMPORAL PIO_TAG
import os, json, math, wave, struct, unreal
L = lambda m: unreal.log_warning("PIOSTUDIO | " + str(m))
EP = "C:/Users/lilli/AI-Shared/projects/heartbeat-tv/pioneer-episode"; ST = EP + "/studio"; FPS = 24; PRE = 8; FAR = -6000.0
TL = json.load(open(EP + "/timeline.json", encoding="utf-8")); SCN = {s["id"]: s for s in TL["scenes"]}
WANT = os.environ.get("PIO_SCENES", "s01,s02,s10,s15").split(","); TAG = os.environ.get("PIO_TAG", "")
M2 = json.load(open(ST + "/motion_s02.json"))
WALLIDX = {"s02": 0, "s01": 1, "s10": 2, "s15": 3}     # cells of studio/wall_atlas.png (2x2), built by run_studio.ps1 from walls/*.png
os.environ.update({"NEWS_BUILD_ONLY": "1", "NEWS_ANCHORS": "1", "NEWS_SHOTS": "wide,two,vex,joe", "NEWS_WALL_ATLAS": ST + "/wall_atlas.png", "NEWS_WALL_GRID": "2x2",
                   "NEWS_JOE_FACE": "1", "NEWS_REIMPORT": "0"})
try: exec(open("C:/Users/lilli/Projects/necklace-unreal/news_studio.py").read())
except SystemExit: pass
L = lambda m: unreal.log_warning("PIOSTUDIO | " + str(m))   # (news_studio.py set its own L)
L("studio built; cameras %s" % list(cams))
eal = unreal.EditorAssetLibrary; tools = unreal.AssetToolsHelpers.get_asset_tools(); eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
KEEP = unreal.AttachmentRule.KEEP_WORLD
def attach(a, parent): a.attach_to_actor(parent, "", KEEP, KEEP, KEEP, False)
def empty(label):
    a = eas.spawn_actor_from_class(unreal.StaticMeshActor, unreal.Vector(0, 0, 0), unreal.Rotator(0, 0, 0)); a.set_actor_label(label)
    a.root_component.set_mobility(unreal.ComponentMobility.MOVABLE); return a
PD = "/Game/Pioneer/Studio"
def mat(name, rgb, rough=0.5, metal=0.0, glow=0.0):
    path = PD + "/" + name
    if eal.does_asset_exist(path): eal.delete_asset(path)
    m = tools.create_asset(name, PD, unreal.Material, unreal.MaterialFactoryNew())
    c = mel.create_material_expression(m, unreal.MaterialExpressionConstant3Vector, -500, -200); c.set_editor_property("constant", unreal.LinearColor(rgb[0], rgb[1], rgb[2], 1))
    mel.connect_material_property(c, "", unreal.MaterialProperty.MP_BASE_COLOR)
    for val, prop, y in ((rough, unreal.MaterialProperty.MP_ROUGHNESS, 0), (metal, unreal.MaterialProperty.MP_METALLIC, 150)):
        k = mel.create_material_expression(m, unreal.MaterialExpressionConstant, -500, y); k.set_editor_property("r", val); mel.connect_material_property(k, "", prop)
    if glow > 0:
        e = mel.create_material_expression(m, unreal.MaterialExpressionConstant3Vector, -500, 300); e.set_editor_property("constant", unreal.LinearColor(rgb[0] * glow, rgb[1] * glow, rgb[2] * glow, 1))
        mel.connect_material_property(e, "", unreal.MaterialProperty.MP_EMISSIVE_COLOR)
    mel.recompile_material(m); eal.save_loaded_asset(m); return m

# ---- the walk stage: everything only s02 uses hangs under one parent, so one transform key parks it for the desk scenes
stage = empty("WalkStage"); truck = empty("TruckStage")   # lights / the truck: separate parents (s15 shows the truck parked crooked by the desk, without the walk lights)
for lbl, pos, tgt, w, h, cd, temp, spec in (("WalkKeyA", T(2.5, 3.3, 9.5), T(0.8, 1.2, 3.2), 320, 220, 1000, 5000, 0.25),
                                            ("WalkKeyB", T(-4.5, 3.5, 11.5), T(-4.0, 1.3, 4.8), 420, 240, 1100, 5000, 0.25),
                                            ("WalkKeyC", T(-6.2, 2.7, 10.2), T(-7.6, 1.25, 5.0), 260, 180, 1700, 5000, 0.25),
                                            ("WalkFill", T(5.0, 2.4, 8.0), T(0.5, 1.2, 3.5), 300, 200, 320, 6000, 0.15),
                                            ("WalkRim", T(-2.5, 4.2, 0.6), T(-2.5, 1.0, 5.0), 300, 120, 650, 7200, 0.1),
                                            ("TruckTop", T(-7.0, 5.2, 4.6), T(-7.0, 1.0, 3.2), 420, 200, 220, 5600, 0.3)):
    a = spawn(unreal.RectLight, pos, lbl, tgt); c = a.get_component_by_class(unreal.RectLightComponent)
    c.set_editor_property("source_width", float(w)); c.set_editor_property("source_height", float(h))
    c.set_editor_property("intensity_units", unreal.LightUnits.CANDELAS); c.set_editor_property("intensity", float(cd))
    c.set_editor_property("temperature", float(temp)); c.set_editor_property("use_temperature", True); c.set_editor_property("attenuation_radius", 2200.0)
    try: c.set_editor_property("specular_scale", spec)
    except Exception as e: L("spec %r" % e)
    attach(a, stage)

# ---- the Heartbeat News live truck (ours, a gag: not real hardware). Long axis along X, nose toward -X, camera-side face at near_y.
V = M2["van"]; RX = V["rear_x"] * 100; NY = V["near_z"] * 100; WD = V["width"] * 100; CY = NY - WD / 2
CUBE, CYL, CONE, SPH = [unreal.load_asset("/Engine/BasicShapes/" + n) for n in ("Cube", "Cylinder", "Cone", "Sphere")]
MW = mat("M_TruckWhite", (0.6, 0.61, 0.63), 0.35, 0.1); MD = mat("M_TruckDark", (0.02, 0.022, 0.026), 0.5, 0.2); MG = mat("M_TruckGlass", (0.015, 0.02, 0.03), 0.08, 0.6)
MR = mat("M_TruckRed", (0.75, 0.04, 0.07), 0.4); MB = mat("M_TruckBlue", (0.03, 0.12, 0.6), 0.4); MM = mat("M_TruckMetal", (0.45, 0.47, 0.5), 0.3, 0.9)
MY = mat("M_TruckStrap", (0.9, 0.62, 0.05), 0.6); MHL = mat("M_TruckHead", (1.0, 0.85, 0.6), 0.3, 0, 6.0); MTL = mat("M_TruckTail", (1.0, 0.05, 0.04), 0.3, 0, 4.0)
def part(mesh, label, loc, scale, m, roll=0.0, pitch=0.0, yaw=0.0):
    a = eas.spawn_actor_from_object(mesh, unreal.Vector(*loc), unreal.Rotator(roll=roll, pitch=pitch, yaw=yaw)); a.set_actor_label("Truck_" + label)
    a.root_component.set_mobility(unreal.ComponentMobility.MOVABLE); a.set_actor_scale3d(unreal.Vector(*scale)); a.static_mesh_component.set_material(0, m); attach(a, truck); return a
def box(label, x0, x1, y0, y1, z0, z1, m): return part(CUBE, label, ((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2), (abs(x1 - x0) / 100, abs(y1 - y0) / 100, abs(z1 - z0) / 100), m)
box("cargo", RX, RX - 330, CY - WD / 2, CY + WD / 2, 58, 268, MW)
box("cab", RX - 330, RX - 500, CY - 97, CY + 97, 58, 208, MW)
box("chassis", RX - 5, RX - 495, CY - 90, CY + 90, 32, 60, MD)
box("windshield", RX - 499, RX - 503, CY - 86, CY + 86, 128, 198, MG)
box("grille", RX - 499, RX - 504, CY - 80, CY + 80, 66, 100, MD)
box("bumperF", RX - 498, RX - 512, CY - 99, CY + 99, 40, 62, MD); box("bumperR", RX + 8, RX - 4, CY - 99, CY + 99, 40, 62, MD)
for s_, yy in (("n", CY + 97), ("f", CY - 97)):
    box("win_" + s_, RX - 352, RX - 470, yy - 2, yy + 2, 128, 194, MG)
box("red_n", RX - 2, RX - 328, NY - 0.5, NY + 1.5, 96, 111, MR); box("blue_n", RX - 2, RX - 328, NY - 0.5, NY + 1.5, 113, 124, MB)
box("red_c", RX - 330, RX - 498, CY + 96.5, CY + 98.8, 96, 111, MR); box("blue_c", RX - 330, RX - 498, CY + 96.5, CY + 98.8, 113, 124, MB)
box("red_f", RX - 2, RX - 328, CY - WD / 2 - 1.5, CY - WD / 2 + 0.5, 96, 111, MR); box("blue_f", RX - 2, RX - 328, CY - WD / 2 - 1.5, CY - WD / 2 + 0.5, 113, 124, MB)
box("doorline", RX - 331, RX - 333, CY + 96.5, CY + 98.6, 62, 204, MD)
for nm, x in (("r", RX - 85), ("f", RX - 425)):
    for s_, yy in (("n", CY + 88), ("o", CY - 88)):
        part(CYL, "tyre_%s%s" % (nm, s_), (x, yy, 40), (0.8, 0.8, 0.26), MD, roll=90.0); part(CYL, "hub_%s%s" % (nm, s_), (x, yy + (14 if s_ == "n" else -14), 40), (0.42, 0.42, 0.03), MM, roll=90.0)
for yy in (CY - 72, CY + 72):
    box("head%d" % yy, RX - 500, RX - 505, yy - 14, yy + 14, 104, 120, MHL); box("tail%d" % yy, RX + 1.5, RX - 1, yy - 9, yy + 9, 100, 128, MTL)
# roof dish, pointed back at the station (toward the desk)
part(CYL, "mast", (RX - 215, CY, 290), (0.12, 0.12, 0.5), MM); part(SPH, "dish", (RX - 198, CY, 338), (1.35, 1.35, 0.3), MW, pitch=-48.0)
part(CYL, "feed", (RX - 170, CY, 362), (0.035, 0.035, 0.42), MM, pitch=-48.0); part(SPH, "feedhorn", (RX - 153, CY, 377), (0.12, 0.12, 0.12), MD)
box("roofrack", RX - 120, RX - 300, CY - 55, CY + 55, 268, 274, MD)
# the rocket a crew has bolted to the back: body along X, nozzle pointing backward (+X)
RZ = 150; R0 = RX + 14; RL = 185
part(CYL, "rocket", (R0 + RL / 2, CY, RZ), (0.76, 0.76, RL / 100.0), MW, pitch=90.0)
for i_, x in enumerate((R0 + 8, R0 + RL - 8)): part(CYL, "rocket_band%d" % i_, (x, CY, RZ), (0.775, 0.775, 0.12), MR, pitch=90.0)
for i_, x in enumerate((R0 + 50, R0 + 125)): part(CYL, "strap%d" % i_, (x, CY, RZ), (0.80, 0.80, 0.07), MY, pitch=90.0)
part(CONE, "nozzle", (R0 + RL + 24, CY, RZ), (0.74, 0.74, 0.6), MD, pitch=90.0)
box("bracket", RX + 2, R0 + 2, CY - 48, CY + 48, 100, 200, MM)
for i_, (y0, y1, z0, z1) in enumerate(((CY - 2, CY + 2, RZ + 36, RZ + 78), (CY - 2, CY + 2, RZ - 78, RZ - 36), (CY + 36, CY + 78, RZ - 2, RZ + 2), (CY - 78, CY - 36, RZ - 2, RZ + 2))):
    box("fin%d" % i_, R0 + RL - 52, R0 + RL - 4, y0, y1, z0, z1, MR)
for i_, yy in enumerate((CY - 30, CY + 30)): box("strut%d" % i_, R0 + 60, R0 + 68, yy - 3, yy + 3, 58, RZ - 36, MM)
box("strutbar", RX + 2, R0 + 70, CY - 34, CY + 34, 52, 60, MM)
def text(label, s, loc, size, color):
    a = eas.spawn_actor_from_class(unreal.TextRenderActor, unreal.Vector(*loc), unreal.Rotator(roll=0, pitch=0, yaw=90)); a.set_actor_label("Truck_" + label)
    a.root_component.set_mobility(unreal.ComponentMobility.MOVABLE); c = a.text_render
    c.set_text(s) if hasattr(c, "set_text") else c.set_editor_property("text", s)
    c.set_world_size(float(size)); c.set_text_render_color(unreal.Color(r=color[0], g=color[1], b=color[2], a=255))
    c.set_horizontal_alignment(unreal.HorizTextAligment.EHTA_CENTER); c.set_vertical_alignment(unreal.VerticalTextAligment.EVRTA_TEXT_CENTER); attach(a, truck)
try:
    text("logo", "HBN", (RX - 165, NY + 2.5, 205), 78, (10, 40, 150)); text("name", "HEARTBEAT NEWS", (RX - 165, NY + 2.5, 158), 26, (190, 20, 30))
    text("live", "LIVE TRUCK", (RX - 165, NY + 2.5, 136), 15, (20, 20, 24))
except Exception as e: L("truck text %r" % e)
TRUCK15 = [float(v) for v in os.environ.get("PIO_TRUCK15", "-690,200,-18").split(",")]   # s15: truck centre x, y (cm) and yaw
L("truck built: rear x %.0f, near y %.0f" % (RX, NY))

# ---- Vex: the bust on its own parent (desk pose = where the show seats him), the hover base on another (parked unless he is flying)
vparts = [a for a in eas.get_all_level_actors() if a.get_actor_label().startswith("Vex_")]
VEX_DESK = vparts[0].get_actor_location()
rig = empty("VexRig"); base = empty("VexBase")
cone = eas.spawn_actor_from_object(CONE, unreal.Vector(0, 0, 0), unreal.Rotator(roll=0, pitch=180, yaw=0)); cone.set_actor_label("VexHoverCone")
cone.root_component.set_mobility(unreal.ComponentMobility.MOVABLE); cone.set_actor_scale3d(unreal.Vector(0.34, 0.34, 0.36)); cone.static_mesh_component.set_material(0, mat("M_VexHoverBase", (0.035, 0.04, 0.05), 0.42, 0.7))
o, ext = cone.get_actor_bounds(False); cone.set_actor_location(unreal.Vector(0, 0, 70 - ext.z - o.z), False, False)
o, ext = cone.get_actor_bounds(False); apex = o.z - ext.z
puck = eas.spawn_actor_from_object(CYL, unreal.Vector(0, 0, apex - 1), unreal.Rotator(0, 0, 0)); puck.set_actor_label("VexHoverGlow")
puck.root_component.set_mobility(unreal.ComponentMobility.MOVABLE); puck.set_actor_scale3d(unreal.Vector(0.16, 0.16, 0.03)); puck.static_mesh_component.set_material(0, glow_material("M_VexHoverGlow", (0.25, 0.7, 1.0), 6))
gl = eas.spawn_actor_from_class(unreal.PointLight, unreal.Vector(0, 0, apex - 6), unreal.Rotator(0, 0, 0)); gl.set_actor_label("VexHoverLight")
glc = gl.get_component_by_class(unreal.PointLightComponent); glc.set_mobility(unreal.ComponentMobility.MOVABLE)
glc.set_intensity(60.0); glc.set_light_color(unreal.LinearColor(0.35, 0.75, 1.0, 1)); glc.set_editor_property("attenuation_radius", 160.0); glc.set_cast_shadows(False)
for a in vparts:
    a.root_component.set_mobility(unreal.ComponentMobility.MOVABLE); a.set_actor_location(unreal.Vector(0, 0, 0), False, False); attach(a, rig)
for a in (cone, puck, gl): attach(a, base)
JOE_DESK = joe.get_actor_location(); L("desk spots: joe %s vex %s" % (JOE_DESK, VEX_DESK))
bodyc = next(c for c in joe.get_components_by_class(unreal.SkeletalMeshComponent) if c.get_name() == "Body")
facec = next(c for c in joe.get_components_by_class(unreal.SkeletalMeshComponent) if c.get_name() == "Face")
if facec.get_editor_property("animation_mode") != unreal.AnimationMode.ANIMATION_SINGLE_NODE: facec.set_editor_property("animation_mode", unreal.AnimationMode.ANIMATION_SINGLE_NODE)

# ---- cameras of our own (the desk scenes use the show's: cams["wide"|"two"|"vex"|"joe"])
def cine(label, lens, fstop, pos, tgt, focus=None):
    cam = spawn(unreal.CineCameraActor, pos, label, tgt); cc = cam.get_cine_camera_component()
    fb = cc.get_editor_property("filmback"); fb.set_editor_property("sensor_width", 36.0); fb.set_editor_property("sensor_height", 20.25); cc.set_editor_property("filmback", fb)
    cc.set_editor_property("current_focal_length", float(lens)); cc.set_editor_property("current_aperture", float(fstop))
    fs = cc.get_editor_property("focus_settings"); fs.set_editor_property("manual_focus_distance", focus or (tgt - pos).length()); cc.set_editor_property("focus_settings", fs)
    return cam
cam_walk = cine("Cam_PIO_walk", 35, 8.0, T(2, 1.5, 6), T(2, 1.2, 1.5), 520.0)
cam_push = cine("Cam_PIO_push", 32, 5.6, T(0, 1.55, 6.4), T(0, 1.3, -1.5), 700.0)

# ---- lip-sync every Joe line of the wanted scenes (same solve as the daily show, fuller mouth)
DEST = "/Game/Pioneer/Studio/Audio"
def lipsync(wav, name):
    t = unreal.AssetImportTask(); t.filename = wav; t.destination_path = DEST; t.destination_name = "SW_" + name; t.automated = True; t.replace_existing = True; t.save = True
    tools.import_asset_tasks([t]); sw = unreal.load_asset(DEST + "/SW_" + name)
    for pth in (DEST + "/PF_" + name, DEST + "/AS_" + name):
        if eal.does_asset_exist(pth): eal.delete_asset(pth)
    perf = tools.create_asset("PF_" + name, DEST, unreal.MetaHumanPerformance, unreal.MetaHumanPerformanceFactoryNew())
    perf.set_editor_property("input_type", unreal.DataInputType.AUDIO); perf.set_editor_property("audio", sw)
    so = unreal.AudioDrivenAnimationSolveOverrides(); so.mood = unreal.AudioDrivenAnimationMood.CONFIDENCE; so.mood_intensity = 1.0
    perf.set_editor_property("audio_driven_animation_solve_overrides", so)
    perf.set_editor_property("audio_driven_animation_output_controls", unreal.AudioDrivenAnimationOutputControls.FULL_FACE)
    perf.set_editor_property("head_movement_mode", unreal.PerformanceHeadMovementMode.DISABLED)
    perf.set_blocking_processing(True); perf.start_pipeline()
    es = unreal.MetaHumanPerformanceExportAnimationSettings(); es.show_export_dialog = False; es.package_path = DEST; es.asset_name = "AS_" + name
    es.target_skeleton_or_skeletal_mesh = unreal.load_asset("/Game/MetaHumans/Common/Face/Face_Archetype_Skeleton"); es.enable_head_movement = False
    es.export_range = unreal.PerformanceExportRange.PROCESSING_RANGE
    return unreal.MetaHumanPerformanceExportUtils.export_animation_sequence(perf, es)
def levels(wav):
    w = wave.open(wav); sr = w.getframerate(); n = w.getnframes(); raw = w.readframes(n); ch = w.getnchannels(); smp = struct.unpack("<%dh" % (n * ch), raw)[::ch]; hop = sr // FPS
    return [min(1.0, math.sqrt(sum(x * x for x in smp[a:a + hop]) / max(1, len(smp[a:a + hop]))) / 32768 * 5.0) for a in range(0, len(smp), hop)]
ANIM = {}
for sid in WANT:
    for l in SCN[sid]["lines"]:
        if l["who"] == "joe" and sid != "s10":     # s10 is voice-over: nobody is at the desk
            ANIM[l["file"]] = lipsync(EP + "/voices/" + l["file"], l["file"][:-4]); L("lip-sync %s -> %s" % (l["file"], bool(ANIM[l["file"]])))
unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)

# ---- sequence helpers
LIN = unreal.MovieSceneKeyInterpolation.LINEAR; CONST = unreal.MovieSceneKeyInterpolation.CONSTANT
LOCO = M2["loco"]; IA = "/MetaHumanCharacter/Optional/Animation/TemplateAnimations/Technical_Loops/Idle/"
def set_rate(p, r):
    try: p.set_editor_property("play_rate", r); return p
    except Exception: pass
    tw = unreal.MovieSceneTimeWarpVariant(); tw.set_fixed_play_rate(r); p.set_editor_property("play_rate", tw); return p
def look(pos, tgt):
    r = unreal.MathLibrary.find_look_at_rotation(pos, tgt); return (pos.x, pos.y, pos.z, r.roll, r.pitch, r.yaw)
def held(a): l = a.get_actor_location(); r = a.get_actor_rotation(); return (l.x, l.y, l.z, r.roll, r.pitch, r.yaw)
def build(sid):
    sc = SCN[sid]; N = sc["f1"] - sc["f0"]; FR = N + PRE; NAME = "PIO_" + sid; SEQ = "/Game/Pioneer/Studio/" + NAME
    if eal.does_asset_exist(SEQ): eal.delete_asset(SEQ)
    seq = tools.create_asset(NAME, "/Game/Pioneer/Studio", unreal.LevelSequence, unreal.LevelSequenceFactoryNew())
    seq.set_display_rate(unreal.FrameRate(FPS, 1)); seq.set_playback_start(0); seq.set_playback_end(FR)
    tick = seq.get_tick_resolution(); TPF = tick.numerator / tick.denominator / FPS
    bid = lambda b: seq.get_binding_id(b) if hasattr(seq, "get_binding_id") else b.get_binding_id()
    def keyt(binding, rows):          # rows: one (x, y, z, roll, pitch, yaw) = held, or one per scene frame (pre-roll holds the first)
        tr = binding.add_track(unreal.MovieScene3DTransformTrack); sec = tr.add_section(); sec.set_range(0, FR + 1); chs = sec.get_all_channels()
        for c in chs[:6]:
            for k in list(c.get_keys()): c.remove_key(k)
        if len(rows) == 1: rows = [rows[0], rows[0]]; frames = [0, FR]
        else: frames = [0] + [PRE + f for f in range(len(rows))]; rows = [rows[0]] + list(rows)
        for f, r in zip(frames, rows):
            for i in range(6): chs[i].add_key(unreal.FrameNumber(f), float(r[i]), interpolation=LIN)
        for c in chs[6:]: c.set_default(1.0)
    walking = sid == "s02"; empty_desk = sid == "s10"
    # the walk stage (truck + lights)
    keyt(seq.add_possessable(stage), [(0, 0, 0, 0, 0, 0) if walking else (0, 0, FAR, 0, 0, 0)])
    if sid == "s15":    # back from the trip: parked crooked just off the desk, the rocket end poking into the wide shot
        th = math.radians(TRUCK15[2]); cx, cy = RX - 250, CY
        tx = TRUCK15[0] - (cx * math.cos(th) - cy * math.sin(th)); ty = TRUCK15[1] - (cx * math.sin(th) + cy * math.cos(th))
        keyt(seq.add_possessable(truck), [(tx, ty, 0, 0, 0, TRUCK15[2])])
    else: keyt(seq.add_possessable(truck), [(0, 0, 0, 0, 0, 0) if walking else (0, 0, FAR, 0, 0, 0)])
    # Joe
    jb = seq.add_possessable(joe)
    if walking: keyt(jb, [(r[0], r[1], 0.0, 0.0, 0.0, r[2]) for r in M2["joe"]])
    else: keyt(jb, [(JOE_DESK.x, JOE_DESK.y, FAR if empty_desk else JOE_DESK.z, 0, 0, 0)])
    bb = seq.add_possessable(bodyc); fbd = seq.add_possessable(facec)
    for b_ in (bb, fbd):
        try: b_.set_parent(jb)
        except Exception: pass
    btr = bb.add_track(unreal.MovieSceneSkeletalAnimationTrack)
    if walking:
        secs = M2["joe_sections"]
        for i, s in enumerate(secs):
            a = PRE + int(round(s["start"] * FPS)); b = min(FR, PRE + int(round(s["end"] * FPS))); bi = int(round(s["blend_in"] * FPS)); bo = int(round(s["blend_out"] * FPS))
            off = s["offset"]
            if i == 0: a = 0; off = (s["offset"] - PRE / FPS * s["rate"]) % 10.0     # pre-roll: the first idle simply starts earlier
            sx = btr.add_section(); sx.set_range(a, b); sx.set_row_index(i % 2)
            p = sx.get_editor_property("params"); p.set_editor_property("animation", unreal.load_asset(LOCO + s["anim"])); p = set_rate(p, float(s["rate"]))
            p.set_editor_property("first_loop_start_frame_offset", unreal.FrameNumber(int(round(off * FPS * TPF)))); sx.set_editor_property("params", p)
            wch = next((c for c in sx.get_all_channels() if "eight" in str(c.get_name())), None)
            for k in list(wch.get_keys()): wch.remove_key(k)
            if bi > 0 and i > 0: wch.add_key(unreal.FrameNumber(a), 0.0, interpolation=LIN); wch.add_key(unreal.FrameNumber(a + bi), 1.0, interpolation=LIN)
            else: wch.add_key(unreal.FrameNumber(a), 1.0, interpolation=LIN)
            if bo > 0: wch.add_key(unreal.FrameNumber(b - bo), 1.0, interpolation=LIN); wch.add_key(unreal.FrameNumber(b), 0.0, interpolation=LIN)
    else:      # at the desk: the standing idle (a slow 2 cm sway, head level; the desk hides his arms and legs). The MetaHuman body idle looked down too often.
        sx = btr.add_section(); sx.set_range(0, FR + 1); p = sx.get_editor_property("params"); p.set_editor_property("animation", unreal.load_asset(LOCO + "AS_MH_Neutral_Stand_Idle_Loop"))
        p.set_editor_property("first_loop_start_frame_offset", unreal.FrameNumber(int(round((3.0 if sid == "s01" else 6.0) * FPS * TPF)))); sx.set_editor_property("params", p)
    # Joe's face: his lines, the quiet idle (blinks) between them
    ftr = fbd.add_track(unreal.MovieSceneSkeletalAnimationTrack); fidle = unreal.load_asset(IA + "mhc_mh001_fmn_f_idle"); t = 0
    def fput(anim, a, b):
        if b <= a or not anim: return
        s_ = ftr.add_section(); s_.set_range(a, b); p_ = s_.get_editor_property("params"); p_.set_editor_property("animation", anim); s_.set_editor_property("params", p_)
    for l in sc["lines"]:
        if l["who"] != "joe" or l["file"] not in ANIM or not ANIM[l["file"]]: continue
        a = PRE + l["f0"] - sc["f0"]; b = min(FR, a + int(math.ceil(ANIM[l["file"]].get_editor_property("sequence_length") * FPS)))
        fput(fidle, t, a); fput(ANIM[l["file"]], a, b); t = b
    fput(fidle, t, FR + 1)
    # Vex
    vb = seq.add_possessable(rig); hb = seq.add_possessable(base)
    if walking: keyt(vb, [tuple(r) for r in M2["vex"]]); keyt(hb, [tuple(r) for r in M2["vex"]])
    else: keyt(vb, [(VEX_DESK.x, VEX_DESK.y, FAR if empty_desk else VEX_DESK.z, 0, 0, 0)]); keyt(hb, [(0, 0, FAR, 0, 0, 0)])
    # Vex's mouth light + which wall graphic
    mt = seq.add_track(unreal.MovieSceneMaterialParameterCollectionTrack); mt.set_editor_property("mpc", mpc); ms = mt.add_section(); ms.set_range(0, FR + 1)
    ms.add_scalar_parameter_key("VexTalk", unreal.FrameNumber(0), 0.04); ms.add_scalar_parameter_key("WallIndex", unreal.FrameNumber(0), 0.0)
    chs = {str(c.get_name()).split("_")[0]: c for c in ms.get_all_channels()}; talk, wall = chs.get("VexTalk"), chs.get("WallIndex")
    for c in (talk, wall):
        for k in list(c.get_keys()): c.remove_key(k)
    talk.add_key(unreal.FrameNumber(0), 0.04); wall.add_key(unreal.FrameNumber(0), float(WALLIDX[sid]), interpolation=CONST)
    for l in sc["lines"]:
        if l["who"] != "vex" or empty_desk: continue
        a = PRE + l["f0"] - sc["f0"]; lv = levels(EP + "/voices/" + l["file"]); talk.add_key(unreal.FrameNumber(a - 1), 0.04)
        for f, v in enumerate(lv): talk.add_key(unreal.FrameNumber(a + f), 0.04 + 1.8 * (v ** 0.7))
        talk.add_key(unreal.FrameNumber(a + len(lv)), 0.04)
    # cameras
    lf = {i: l["f0"] - sc["f0"] for i, l in enumerate(sc["lines"])}
    if walking:
        cb = seq.add_possessable(cam_walk); keyt(cb, [look(unreal.Vector(r[0], r[1], r[2]), unreal.Vector(r[3], r[4], r[5])) for r in M2["cam"]]); CUTS = [(0, cb)]
    elif empty_desk:
        cb = seq.add_possessable(cam_push); rows = []
        for f in range(N):
            u = f / max(1, N - 1); u = u * u * (3 - 2 * u)
            rows.append(look(T(0, 1.55 + 0.22 * u, 6.4 - 2.3 * u), T(0, 1.3 + 0.5 * u, -1.5)))
        keyt(cb, rows); CUTS = [(0, cb)]
    else:
        cbs = {k: seq.add_possessable(c) for k, c in cams.items()}
        if sid == "s01":   # open wide; singles on the hellos and the jokes; wide again while they explain the post, so the Grok card on the wall is readable
            plan = [(0, "wide"), (lf[0] - 3, "joe"), (lf[1] - 3, "vex"), (lf[2] - 3, "joe"), (lf[3] - 3, "wide"), (lf[4] - 3, "joe"), (lf[4] + 88, "wide"), (lf[5] - 3, "two"), (lf[6] - 3, "joe")]
        else:              # s15: wide welcome back, Joe's headline, Vex's lesson, wide for "File it under Science" (the wall card), Vex, wide good night
            plan = [(0, "wide"), (66, "joe"), (lf[1] - 3, "vex"), (lf[2] - 3, "joe"), (lf[2] + 62, "wide"), (lf[3] - 3, "vex"), (lf[4] - 3, "wide")]
        CUTS = [(0 if f <= 0 else PRE + f, cbs[k]) for f, k in plan]
    cuts = seq.add_track(unreal.MovieSceneCameraCutTrack)
    for i, (st, cb_) in enumerate(CUTS):
        en = CUTS[i + 1][0] if i + 1 < len(CUTS) else FR + 1
        s_ = cuts.add_section(); s_.set_range(st, en); s_.set_camera_binding_id(bid(cb_))
    eal.save_loaded_asset(seq); L("sequence %s: %d frames (+%d pre-roll), %d cuts" % (NAME, N, PRE, len(CUTS))); return SEQ, FR
JOBS = [(sid,) + build(sid) for sid in WANT]
unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)

# ---- render every scene as its own job
qs = unreal.get_editor_subsystem(unreal.MoviePipelineQueueSubsystem); q = qs.get_queue()
for j in list(q.get_jobs()): q.delete_job(j)
rx, ry = [int(v) for v in os.environ.get("PIO_RES", "1920x1080").split("x")]
for sid, spath, FR in JOBS:
    job = q.allocate_new_job(unreal.MoviePipelineExecutorJob); job.sequence = unreal.SoftObjectPath(spath); job.map = unreal.SoftObjectPath(MAP)
    cfg = job.get_configuration()
    out = cfg.find_or_add_setting_by_class(unreal.MoviePipelineOutputSetting); out.output_resolution = unreal.IntPoint(rx, ry)
    out.output_directory = unreal.DirectoryPath(PROJ + "/Saved/MovieRenders/Pioneer_" + sid + TAG); out.file_name_format = "f_{frame_number}"
    cfg.find_or_add_setting_by_class(unreal.MoviePipelineDeferredPassBase); cfg.find_or_add_setting_by_class(unreal.MoviePipelineImageSequenceOutput_PNG)
    aa = cfg.find_or_add_setting_by_class(unreal.MoviePipelineAntiAliasingSetting)
    aa.spatial_sample_count = int(os.environ.get("PIO_SPATIAL", "2")); aa.temporal_sample_count = int(os.environ.get("PIO_TEMPORAL", "4"))
    aa.override_anti_aliasing = True; aa.engine_warm_up_count = 90; aa.render_warm_up_frames = True
    cv = cfg.find_or_add_setting_by_class(unreal.MoviePipelineConsoleVariableSetting)
    for k, v in (("r.Streaming.FullyLoadUsedTextures", 1), ("r.TextureStreaming", 0), ("r.SkeletalMeshLODBias", -5)): cv.add_or_update_console_variable(k, v)
ex = qs.render_queue_with_executor(unreal.MoviePipelinePIEExecutor)
def done(executor, success): L("render finished success=%s" % success); unreal.SystemLibrary.quit_editor()
ex.on_executor_finished_delegate.add_callable_unique(done)
L("render started (%d jobs)" % len(JOBS))
