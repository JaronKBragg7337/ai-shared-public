import unreal
L = lambda m: unreal.log_warning("PROBE | " + str(m))
eal = unreal.EditorAssetLibrary
bp = unreal.load_asset("/Game/MetaHumansSM6/Joe/BP_Joe")
L("bp %s" % bp)
for p in eal.list_assets("/Game/MetaHumansSM6/Joe", recursive=True):
    ad = eal.find_asset_data(p); L("asset %s %s" % (ad.asset_class_path.asset_name, p))
LOCO = "/MetaHumanCharacter/Optional/Animation/UEFNAnimPreset/Locomotion/"
for n in ("AS_MH_Neutral_Walk_Loop_F", "AS_MH_Neutral_Walk_Start_F_Rfoot", "AS_MH_Neutral_Walk_Stop_F_Lfoot", "AS_MH_Neutral_Stand_Idle_Loop", "AS_MH_Neutral_Walk_Loop_B"):
    a = unreal.load_asset(LOCO + n)
    if not a: L("missing " + n); continue
    ln = a.get_editor_property("sequence_length") if hasattr(a, "sequence_length") else unreal.AnimationLibrary.get_sequence_length(a)
    sk = a.get_editor_property("skeleton")
    rm = a.get_editor_property("enable_root_motion")
    try:
        p0 = unreal.AnimationLibrary.get_bone_pose_for_time(a, "root", 0.0, True)
        p1 = unreal.AnimationLibrary.get_bone_pose_for_time(a, "root", ln, True)
        pp0 = unreal.AnimationLibrary.get_bone_pose_for_time(a, "pelvis", 0.0, True)
        pp1 = unreal.AnimationLibrary.get_bone_pose_for_time(a, "pelvis", ln, True)
        L("%s len %.3f rootmotion %s skel %s root %s -> %s pelvis %s -> %s" % (n, ln, rm, sk.get_path_name(), p0.translation, p1.translation, pp0.translation, pp1.translation))
    except Exception as e: L("%s len %.3f rm %s skel %s err %r" % (n, ln, rm, sk.get_path_name(), e))
