# foot-lock speed profiles of the MetaHuman locomotion clips (in-place, no root motion) -> velocities.json
import unreal, json
L = lambda m: unreal.log_warning("PROBE | " + str(m))
AL = unreal.AnimationLibrary
LOCO = "/MetaHumanCharacter/Optional/Animation/UEFNAnimPreset/Locomotion/"
NAMES = ["AS_MH_Neutral_Walk_Loop_F", "AS_MH_Neutral_Walk_Start_F_Rfoot", "AS_MH_Neutral_Walk_Stop_F_Lfoot", "AS_MH_Neutral_Stand_Idle_Loop",
         "AS_MH_Neutral_Walk_Loop_B", "AS_MH_Neutral_Walk_Start_B_Lfoot", "AS_MH_Neutral_Walk_Stop_B_Rfoot", "AS_MH_Neutral_Walk_Loop_LR", "AS_MH_Neutral_Walk_Loop_RL"]
CH = {s: ["pelvis", "thigh_" + s, "calf_" + s, "foot_" + s, "ball_" + s] for s in "lr"}
out = {}
for n in NAMES:
    a = unreal.load_asset(LOCO + n); ln = AL.get_sequence_length(a); fr = []
    t = 0.0
    while t <= ln + 1e-6:
        row = {"t": round(t, 4)}
        for s, chain in CH.items():
            x = unreal.Transform()
            for b in chain:
                x = AL.get_bone_pose_for_time(a, b, t, False).multiply(x) if False else AL.get_bone_pose_for_time(a, b, t, False) * x if False else x
            # compose child * parent properly: world = local_child * parent_world
            w = unreal.Transform()
            for b in chain:
                lp = AL.get_bone_pose_for_time(a, b, t, False)
                w = lp.multiply(w) if hasattr(lp, "multiply") else lp * w
            p = w.translation; row[s] = [p.x, p.y, p.z]
        fr.append(row); t += 1.0 / 120
    out[n] = {"len": ln, "frames": fr}
    L("%s %.3f %d" % (n, ln, len(fr)))
json.dump(out, open("C:/Users/lilli/AI-Shared/projects/heartbeat-tv/pioneer-episode/movement/feet.json", "w"))
L("done")
