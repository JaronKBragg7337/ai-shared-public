# pass 2 probe: feet of the MetaHuman body idle (for the foot lock) + how alive each idle is + how much the hips rise in the walk
import unreal, json
AL = unreal.AnimationLibrary
LOCO = "/MetaHumanCharacter/Optional/Animation/UEFNAnimPreset/Locomotion/"
IDLE2 = "/MetaHumanCharacter/Optional/Animation/TemplateAnimations/Technical_Loops/Idle/mhc_mh001_fmn_b_idle"
SP = ["pelvis", "spine_01", "spine_02", "spine_03", "spine_04", "spine_05"]
CH = {"l": ["pelvis", "thigh_l", "calf_l", "foot_l", "ball_l"], "r": ["pelvis", "thigh_r", "calf_r", "foot_r", "ball_r"], "pelvis": ["pelvis"],
      "head": SP + ["neck_01", "neck_02", "head"], "hand": SP + ["clavicle_l", "upperarm_l", "lowerarm_l", "hand_l"]}
out = {}
for n, path in (("AS_MH_Neutral_Stand_Idle_Loop", LOCO + "AS_MH_Neutral_Stand_Idle_Loop"), ("mhc_mh001_fmn_b_idle", IDLE2), ("AS_MH_Neutral_Walk_Loop_F", LOCO + "AS_MH_Neutral_Walk_Loop_F"),
                ("AS_MH_Neutral_Walk_Start_F_Rfoot", LOCO + "AS_MH_Neutral_Walk_Start_F_Rfoot")):
    a = unreal.load_asset(path)
    if not a: out[n] = None; continue
    ln = AL.get_sequence_length(a); fr = []; t = 0.0; step = 1.0 / 120 if ln < 12 else 1.0 / 30
    while t <= ln + 1e-6:
        row = {"t": round(t, 4)}
        for k, chain in CH.items():
            w = unreal.Transform()
            try:
                for b in chain:
                    lp = AL.get_bone_pose_for_time(a, b, t, False); w = lp.multiply(w) if hasattr(lp, "multiply") else lp * w
                p = w.translation; row[k] = [p.x, p.y, p.z]
            except Exception as e: row[k] = None; row["err"] = str(e)[:80]
        fr.append(row); t += step
    out[n] = {"len": ln, "step": step, "frames": fr}
json.dump(out, open("C:/Users/lilli/AI-Shared/projects/heartbeat-tv/pioneer-episode/movement/feet2.json", "w"))
