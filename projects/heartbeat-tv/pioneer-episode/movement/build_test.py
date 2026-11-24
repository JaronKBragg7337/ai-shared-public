# Pioneer episode - MOVEMENT TEST in Unreal (Jaron 11/15: check walking before the long render).
# Builds the news studio (news_studio.py, build-only), then one sequence from motion.json (plan.py):
#   Joe  = MetaHuman, UEFN locomotion clips (start / loop / stop / idle) crossfaded at matched foot phases; his travel is
#          derived from the clips' planted foot (no skating by design); turns are arcs while walking.
#   Vex  = the show's robot bust on a small hover base (he has no legs): eased glides, lean into speed, bank in turns, bob.
#   Walk-and-talk: Vex's mouth light from his line, Joe's line lip-synced (MetaHuman Animator) through the face AnimBP slot.
# Cameras: wide, low feet camera (for foot sliding), tracking camera for the walk-and-talk. Frames -> Saved/MovieRenders/MoveTest.
# Run:  UnrealEditor NecklaceFilm.uproject -ExecCmds="py <this file>"     Env: MT_SPATIAL / MT_TEMPORAL (samples), MT_RES (e.g. 1920x1080)
import os, json, math, unreal
L = lambda m: unreal.log_warning("MOVETEST | " + str(m))
HERE = "C:/Users/lilli/AI-Shared/projects/heartbeat-tv/pioneer-episode/movement"
M = json.load(open(HERE + "/motion.json")); FR = M["frames"]; FPS = M["fps"]
os.environ.update({"NEWS_BUILD_ONLY": "1", "NEWS_ANCHORS": "1", "NEWS_SHOTS": "wide", "NEWS_WALL_ATLAS": "", "NEWS_JOE_FACE": "1", "NEWS_REIMPORT": "0"})
try: exec(open("C:/Users/lilli/Projects/necklace-unreal/news_studio.py").read())
except SystemExit: pass
L("studio built")
eal = unreal.EditorAssetLibrary; tools = unreal.AssetToolsHelpers.get_asset_tools()
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
U = lambda x, z, h=0.0: unreal.Vector(x, z, h)      # plan cm (x, z toward camera, height) -> Unreal

# ---- soft lights for the open floor (the show lights aim at the desk). v2: from the camera side at face height-ish angles
# (v1 lit straight down: faces in shadow, Vex's top blown out) and with low specular so they don't mirror as white slabs in the floor.
for lbl, pos, tgt, w, h, cd, temp, spec in (("FloorKey", T(-3.2, 3.3, 10.0), T(0.2, 1.2, 3.6), 320, 220, 1150, 5000, 0.25),
                                            ("FloorFill", T(4.6, 2.4, 8.5), T(0.6, 1.2, 3.2), 300, 200, 380, 6000, 0.15),
                                            ("FloorRim", T(0.5, 4.2, 0.3), T(0.5, 1.0, 4.2), 250, 120, 700, 7200, 0.1)):
    a = spawn(unreal.RectLight, pos, lbl, tgt); c = a.get_component_by_class(unreal.RectLightComponent)
    c.set_editor_property("source_width", float(w)); c.set_editor_property("source_height", float(h))
    c.set_editor_property("intensity_units", unreal.LightUnits.CANDELAS); c.set_editor_property("intensity", float(cd) * float(os.environ.get("MT_LIGHT", "1")))
    c.set_editor_property("temperature", float(temp)); c.set_editor_property("use_temperature", True); c.set_editor_property("attenuation_radius", 2500.0)
    try: c.set_editor_property("specular_scale", spec)
    except Exception as e: L("spec %r" % e)

# ---- Vex rig: the bust pieces on a hover base, all under one parent actor
vparts = [a for a in eas.get_all_level_actors() if a.get_actor_label().startswith("Vex_")]
rig = eas.spawn_actor_from_class(unreal.StaticMeshActor, unreal.Vector(0, 0, 0), unreal.Rotator(0, 0, 0)); rig.set_actor_label("VexRig")
rig.root_component.set_mobility(unreal.ComponentMobility.MOVABLE)
cone = eas.spawn_actor_from_object(unreal.load_asset("/Engine/BasicShapes/Cone"), unreal.Vector(0, 0, 0), unreal.Rotator(0, 180, 0))   # roll 180 -> point down
cone.set_actor_label("VexHoverCone"); cone.root_component.set_mobility(unreal.ComponentMobility.MOVABLE); cone.set_actor_scale3d(unreal.Vector(0.34, 0.34, 0.36))
body = next((a for a in vparts if "body" in a.get_actor_label().lower()), vparts[0])
def dark_material():   # v2: graphite base (the white shell material on the cone glared under its own glow light)
    path = "/Game/Sets/NewsMats/M_VexHoverBase"
    if eal.does_asset_exist(path): return unreal.load_asset(path)
    m = tools.create_asset("M_VexHoverBase", "/Game/Sets/NewsMats", unreal.Material, unreal.MaterialFactoryNew())
    c = mel.create_material_expression(m, unreal.MaterialExpressionConstant3Vector, -500, -200); c.set_editor_property("constant", unreal.LinearColor(0.035, 0.04, 0.05, 1))
    mel.connect_material_property(c, "", unreal.MaterialProperty.MP_BASE_COLOR)
    for val, prop, y in ((0.42, unreal.MaterialProperty.MP_ROUGHNESS, 0), (0.7, unreal.MaterialProperty.MP_METALLIC, 150)):
        k = mel.create_material_expression(m, unreal.MaterialExpressionConstant, -500, y); k.set_editor_property("r", val); mel.connect_material_property(k, "", prop)
    mel.recompile_material(m); eal.save_loaded_asset(m); return m
try: cone.static_mesh_component.set_material(0, dark_material())
except Exception as e: L("cone material %r" % e)
o, ext = cone.get_actor_bounds(False); cone.set_actor_location(unreal.Vector(0, 0, 70 - ext.z - (o.z - 0)), False, False)   # cone top at 70 cm (inside the round torso)
o, ext = cone.get_actor_bounds(False); apex = o.z - ext.z; L("cone %s..%s" % (apex, o.z + ext.z))
puck = eas.spawn_actor_from_object(unreal.load_asset("/Engine/BasicShapes/Cylinder"), unreal.Vector(0, 0, apex - 1), unreal.Rotator(0, 0, 0))
puck.set_actor_label("VexHoverGlow"); puck.root_component.set_mobility(unreal.ComponentMobility.MOVABLE); puck.set_actor_scale3d(unreal.Vector(0.16, 0.16, 0.03))
puck.static_mesh_component.set_material(0, glow_material("M_VexHoverGlow", (0.25, 0.7, 1.0), 6))
gl = eas.spawn_actor_from_class(unreal.PointLight, unreal.Vector(0, 0, apex - 6), unreal.Rotator(0, 0, 0)); gl.set_actor_label("VexHoverLight")
glc = gl.get_component_by_class(unreal.PointLightComponent); glc.set_mobility(unreal.ComponentMobility.MOVABLE)
glc.set_intensity(60.0); glc.set_light_color(unreal.LinearColor(0.35, 0.75, 1.0, 1)); glc.set_editor_property("attenuation_radius", 160.0); glc.set_cast_shadows(False)
for a in vparts:   # the bust sat at the desk spot; re-centre it on the rig (same height, it now floats on the base)
    a.root_component.set_mobility(unreal.ComponentMobility.MOVABLE); a.set_actor_location(unreal.Vector(0, 0, 0), False, False)
for a in vparts + [cone, puck, gl]: a.attach_to_actor(rig, "", unreal.AttachmentRule.KEEP_WORLD, unreal.AttachmentRule.KEEP_WORLD, unreal.AttachmentRule.KEEP_WORLD, False)
L("vex rig: %d parts" % len(vparts))

# ---- cameras: wide, low feet camera, tracking
def cine(label, lens, fstop, pos, tgt):
    cam = spawn(unreal.CineCameraActor, pos, label, tgt); cc = cam.get_cine_camera_component()
    fb = cc.get_editor_property("filmback"); fb.set_editor_property("sensor_width", 36.0); fb.set_editor_property("sensor_height", 20.25); cc.set_editor_property("filmback", fb)
    cc.set_editor_property("current_focal_length", float(lens)); cc.set_editor_property("current_aperture", float(fstop))
    fs = cc.get_editor_property("focus_settings"); fs.set_editor_property("manual_focus_distance", (tgt - pos).length()); cc.set_editor_property("focus_settings", fs)
    return cam
# pass 2: ONE moving camera for the whole take (no cuts); f/8 so the pair stays sharp from the wide to the close two-shot.
ct = cine("Cam_MT_main", 35, 8.0, T(0.1, 1.75, 11.2), T(0.1, 0.95, 5.2))
CHK = M["footchecks"]    # low static cameras for the labelled foot-check replays (same take, rendered as extra jobs)
ccams = [cine("Cam_MT_check%d" % i, 28, 5.6, unreal.Vector(*c["pos"]), unreal.Vector(*c["aim"])) for i, c in enumerate(CHK)]
facec0 = next(c for c in joe.get_components_by_class(unreal.SkeletalMeshComponent) if c.get_name() == "Face")
if os.environ.get("MT_FACE", "single") == "single" and facec0.get_editor_property("animation_mode") != unreal.AnimationMode.ANIMATION_SINGLE_NODE:
    facec0.set_editor_property("animation_mode", unreal.AnimationMode.ANIMATION_SINGLE_NODE)

# ---- lip-sync Joe's line (same as episode_render.py)
DEST = "/Game/NewsAudio/MoveTest"
def lipsync(wav, name):
    t = unreal.AssetImportTask(); t.filename = wav; t.destination_path = DEST; t.destination_name = "SW_" + name; t.automated = True; t.replace_existing = True; t.save = True
    tools.import_asset_tasks([t]); sw = unreal.load_asset(DEST + "/SW_" + name)
    for pth in (DEST + "/PF_" + name, DEST + "/AS_" + name):
        if eal.does_asset_exist(pth): eal.delete_asset(pth)
    perf = tools.create_asset("PF_" + name, DEST, unreal.MetaHumanPerformance, unreal.MetaHumanPerformanceFactoryNew())
    perf.set_editor_property("input_type", unreal.DataInputType.AUDIO); perf.set_editor_property("audio", sw)
    so = unreal.AudioDrivenAnimationSolveOverrides(); so.mood = unreal.AudioDrivenAnimationMood.CONFIDENCE; so.mood_intensity = 0.5
    perf.set_editor_property("audio_driven_animation_solve_overrides", so)
    perf.set_editor_property("audio_driven_animation_output_controls", unreal.AudioDrivenAnimationOutputControls.FULL_FACE)
    perf.set_editor_property("head_movement_mode", unreal.PerformanceHeadMovementMode.DISABLED)
    so.mood_intensity = float(os.environ.get("MT_MOOD", "1.0")); perf.set_editor_property("audio_driven_animation_solve_overrides", so)   # pass 2: fuller mouth shapes
    perf.set_blocking_processing(True); perf.start_pipeline()
    es = unreal.MetaHumanPerformanceExportAnimationSettings(); es.show_export_dialog = False; es.package_path = DEST; es.asset_name = "AS_" + name
    es.target_skeleton_or_skeletal_mesh = unreal.load_asset("/Game/MetaHumans/Common/Face/Face_Archetype_Skeleton"); es.enable_head_movement = False
    es.export_range = unreal.PerformanceExportRange.PROCESSING_RANGE
    return unreal.MetaHumanPerformanceExportUtils.export_animation_sequence(perf, es)
jl = next(l for l in M["lines"] if l["who"] == "joe"); vl = next(l for l in M["lines"] if l["who"] == "vex")
joe_anim = lipsync(jl["file"], "joe_line"); L("lip-sync -> %s" % joe_anim)

# ---- Vex mouth levels from his line (same scale as episode_plan.py)
import wave, struct
w = wave.open(vl["file"]); sr = w.getframerate(); n = w.getnframes(); raw = w.readframes(n); ch = w.getnchannels()
smp = struct.unpack("<%dh" % (n * ch), raw)[::ch]; hop = sr // FPS
levels = [min(1.0, math.sqrt(sum(x * x for x in smp[a:a + hop]) / max(1, len(smp[a:a + hop]))) / 32768 * 5.0) for a in range(0, len(smp), hop)]

# ---- the sequence
NAME = "MoveTest"; SEQ = "/Game/Cinematics/" + NAME
if eal.does_asset_exist(SEQ): eal.delete_asset(SEQ)
seq = tools.create_asset(NAME, "/Game/Cinematics", unreal.LevelSequence, unreal.LevelSequenceFactoryNew())
seq.set_display_rate(unreal.FrameRate(FPS, 1)); seq.set_playback_start(0); seq.set_playback_end(FR)
tick = seq.get_tick_resolution(); TPF = tick.numerator / tick.denominator / FPS   # ticks per display frame
bid = lambda b: seq.get_binding_id(b) if hasattr(seq, "get_binding_id") else b.get_binding_id()
LIN = unreal.MovieSceneKeyInterpolation.LINEAR
def key_transform(binding, rows):   # rows: per frame (x, y, z, roll, pitch, yaw)
    tr = binding.add_track(unreal.MovieScene3DTransformTrack); sec = tr.add_section(); sec.set_range(0, FR)
    chs = sec.get_all_channels()   # loc x y z, rot x(roll) y(pitch) z(yaw), scale x y z
    for c in chs[:6]:
        for k in list(c.get_keys()): c.remove_key(k)
    for f, r in enumerate(rows):
        for i in range(6): chs[i].add_key(unreal.FrameNumber(f), float(r[i]), interpolation=LIN)
    for c in chs[6:]: c.set_default(1.0)
def set_rate(p, r):   # UE 5.8: PlayRate is a MovieSceneTimeWarpVariant struct, not a float
    try: p.set_editor_property("play_rate", r); return p
    except Exception: pass
    tw = unreal.MovieSceneTimeWarpVariant()
    for how in ("set_fixed_play_rate", "set_fixed"):
        if hasattr(tw, how):
            try: getattr(tw, how)(r); p.set_editor_property("play_rate", tw); L("play rate via %s" % how); return p
            except Exception as e: L("rate %s %r" % (how, e))
    for lib in [x for x in dir(unreal) if "TimeWarp" in x]: L("timewarp api: %s %s" % (lib, [m for m in dir(getattr(unreal, lib)) if not m.startswith("_")][:40]))
    L("tw dir %s" % [m for m in dir(tw) if not m.startswith("_")])
    raise RuntimeError("no play rate api")
# Joe: transform + body clips
jb = seq.add_possessable(joe)
key_transform(jb, [(r[0], r[1], 0.0, 0.0, 0.0, r[2]) for r in M["joe"]])
bodyc = next(c for c in joe.get_components_by_class(unreal.SkeletalMeshComponent) if c.get_name() == "Body")
facec = next(c for c in joe.get_components_by_class(unreal.SkeletalMeshComponent) if c.get_name() == "Face")
L("face mode %s anim class %s" % (facec.get_editor_property("animation_mode"), facec.get_editor_property("anim_class")))
bb = seq.add_possessable(bodyc)
try: bb.set_parent(jb)
except Exception: pass
btr = bb.add_track(unreal.MovieSceneSkeletalAnimationTrack)
secs = M["joe_sections"]
for i, s in enumerate(secs):
    a = int(round(s["start"] * FPS)); b = min(FR, int(round(s["end"] * FPS))); bi = int(round(s["blend_in"] * FPS)); bo = int(round(s["blend_out"] * FPS))
    sc = btr.add_section(); sc.set_range(a, b); sc.set_row_index(i % 2)
    p = sc.get_editor_property("params"); p.set_editor_property("animation", unreal.load_asset(M["loco"] + s["anim"]))
    p = set_rate(p, float(s.get("rate", M["rate"])))
    p.set_editor_property("first_loop_start_frame_offset", unreal.FrameNumber(int(round(s["offset"] * FPS * TPF))))   # phase of the first loop only (start_frame_offset would trim every loop)
    sc.set_editor_property("params", p)
    wch = next((c for c in sc.get_all_channels() if "eight" in str(c.get_name())), None)
    if wch:   # crossfade weights: ramp in over the blend at the start, out at the end (first/last stay full)
        for k in list(wch.get_keys()): wch.remove_key(k)
        if bi > 0: wch.add_key(unreal.FrameNumber(a), 0.0, interpolation=LIN); wch.add_key(unreal.FrameNumber(a + bi), 1.0, interpolation=LIN)
        else: wch.add_key(unreal.FrameNumber(a), 1.0, interpolation=LIN)
        if bo > 0: wch.add_key(unreal.FrameNumber(b - bo), 1.0, interpolation=LIN); wch.add_key(unreal.FrameNumber(b), 0.0, interpolation=LIN)
    else: L("no weight channel on section %d" % i)
L("joe body: %d clips" % len(secs))
# Joe's face. v1 kept ABP_Face and played the line through "DefaultSlot" - ABP_Face has no slot (it is only CopyPoseFromMesh), so his
# mouth never moved. v2: the face plays Sequencer tracks directly (single node, like the daily show); the face mesh's post-process
# AnimBP still copies the neck/head from the walking body and runs RigLogic. Between lines: the quiet face idle (blinks).
fb_ = seq.add_possessable(facec)
try: fb_.set_parent(jb)
except Exception: pass
ftr = fb_.add_track(unreal.MovieSceneSkeletalAnimationTrack)
flen = int(math.ceil(joe_anim.get_editor_property("sequence_length") * FPS)) if joe_anim else 96
fidle = unreal.load_asset("/MetaHumanCharacter/Optional/Animation/TemplateAnimations/Technical_Loops/Idle/mhc_mh001_fmn_f_idle")
def fput(anim, a, b):
    if b <= a or not anim: return
    s_ = ftr.add_section(); s_.set_range(a, b); p_ = s_.get_editor_property("params"); p_.set_editor_property("animation", anim); s_.set_editor_property("params", p_)
fput(fidle, 0, jl["start"]); fput(joe_anim, jl["start"], min(FR, jl["start"] + flen)); fput(fidle, min(FR, jl["start"] + flen), FR)
# Vex: rig transform (x, y, hover z, roll = lean forward, pitch = bank, yaw)
vb = seq.add_possessable(rig)
key_transform(vb, [tuple(r) for r in M["vex"]])   # x, y, hover z, roll, pitch, yaw
# Vex mouth light
mt = seq.add_track(unreal.MovieSceneMaterialParameterCollectionTrack); mt.set_editor_property("mpc", mpc)
ms = mt.add_section(); ms.set_range(0, FR); ms.add_scalar_parameter_key("VexTalk", unreal.FrameNumber(0), 0.04)
talk = next(c for c in ms.get_all_channels() if str(c.get_name()).startswith("VexTalk"))
for k in list(talk.get_keys()): talk.remove_key(k)
talk.add_key(unreal.FrameNumber(0), 0.04); talk.add_key(unreal.FrameNumber(vl["start"] - 1), 0.04)
for f, v in enumerate(levels): talk.add_key(unreal.FrameNumber(vl["start"] + f), 0.04 + 1.8 * (v ** 0.7))
talk.add_key(unreal.FrameNumber(vl["start"] + len(levels)), 0.04)
# tracking camera path
tb = seq.add_possessable(ct); rows = []
for r in M["cam"]:
    pos = unreal.Vector(r[0], r[1], r[2]); tgt = unreal.Vector(r[3], r[4], r[5]); rot = unreal.MathLibrary.find_look_at_rotation(pos, tgt)
    rows.append((pos.x, pos.y, pos.z, rot.roll, rot.pitch, rot.yaw))
key_transform(tb, rows)
cuts = seq.add_track(unreal.MovieSceneCameraCutTrack)
s_ = cuts.add_section(); s_.set_range(0, FR); s_.set_camera_binding_id(bid(tb))
eal.save_loaded_asset(seq); unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
L("sequence %d frames" % FR)

# ---- foot-check copies of the sequence: same animation, the camera cut swapped to a low static camera, only that stretch
JOBS = [(SEQ, os.environ.get("MT_OUT", "MoveTest"))]
for i, c in enumerate(CHK):
    try:
        dpath = "/Game/Cinematics/%s_C%d" % (NAME, i)
        if eal.does_asset_exist(dpath): eal.delete_asset(dpath)
        d = eal.duplicate_asset(SEQ, dpath)
        for tr in list(d.get_tracks() if hasattr(d, "get_tracks") else d.get_master_tracks()):
            if isinstance(tr, unreal.MovieSceneCameraCutTrack): d.remove_track(tr) if hasattr(d, "remove_track") else d.remove_master_track(tr)
        ctr = d.add_track(unreal.MovieSceneCameraCutTrack); cs = ctr.add_section(); cs.set_range(0, FR)
        cb = d.add_possessable(ccams[i]); cs.set_camera_binding_id(d.get_binding_id(cb) if hasattr(d, "get_binding_id") else cb.get_binding_id())
        d.set_playback_start(max(0, c["f0"] - 3)); d.set_playback_end(min(FR, c["f1"]))
        eal.save_loaded_asset(d); JOBS.append((dpath, os.environ.get("MT_OUT", "MoveTest") + "_c%d" % i)); L("foot check %d: frames %d-%d" % (i, c["f0"], c["f1"]))
    except Exception as e: L("foot check %d FAILED %r" % (i, e))
unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)

# ---- render
qs = unreal.get_editor_subsystem(unreal.MoviePipelineQueueSubsystem); q = qs.get_queue()
for j in list(q.get_jobs()): q.delete_job(j)
rx, ry = [int(v) for v in os.environ.get("MT_RES", "1920x1080").split("x")]
for spath, odir in JOBS:
    job = q.allocate_new_job(unreal.MoviePipelineExecutorJob); job.sequence = unreal.SoftObjectPath(spath); job.map = unreal.SoftObjectPath(MAP)
    cfg = job.get_configuration()
    out = cfg.find_or_add_setting_by_class(unreal.MoviePipelineOutputSetting); out.output_resolution = unreal.IntPoint(rx, ry)
    out.output_directory = unreal.DirectoryPath(PROJ + "/Saved/MovieRenders/" + odir); out.file_name_format = "f_{frame_number}"
    cfg.find_or_add_setting_by_class(unreal.MoviePipelineDeferredPassBase); cfg.find_or_add_setting_by_class(unreal.MoviePipelineImageSequenceOutput_PNG)
    aa = cfg.find_or_add_setting_by_class(unreal.MoviePipelineAntiAliasingSetting)
    aa.spatial_sample_count = int(os.environ.get("MT_SPATIAL", "2")); aa.temporal_sample_count = int(os.environ.get("MT_TEMPORAL", "4"))
    aa.override_anti_aliasing = True; aa.engine_warm_up_count = 90; aa.render_warm_up_frames = True
    cv = cfg.find_or_add_setting_by_class(unreal.MoviePipelineConsoleVariableSetting)
    for k, v in (("r.Streaming.FullyLoadUsedTextures", 1), ("r.TextureStreaming", 0), ("r.SkeletalMeshLODBias", -5)): cv.add_or_update_console_variable(k, v)
ex = qs.render_queue_with_executor(unreal.MoviePipelinePIEExecutor)
def done(executor, success): L("render finished success=%s" % success); unreal.SystemLibrary.quit_editor()
ex.on_executor_finished_delegate.add_callable_unique(done)
L("render started (%d jobs)" % len(JOBS))
