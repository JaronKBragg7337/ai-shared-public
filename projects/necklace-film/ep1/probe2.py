import bpy, math
from mathutils import Vector, Matrix
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath="C:/Users/lilli/Projects/heartbeat-observatory/homes/people/isaiah.glb")
arm = next(o for o in bpy.data.objects if o.type == "ARMATURE")
print("rotmode", arm.rotation_mode, arm.rotation_quaternion[:], arm.scale[:])
print([b.name for b in arm.pose.bones if "metacarpal" in b.name or "hand" in b.name or "ball" in b.name][:12])
ad = arm.animation_data; sit = next(a for a in bpy.data.actions if a.name.startswith("Sit")); ad.action = sit
try: ad.action_slot = sit.slots[0]
except Exception as e: print("slot", e)
bpy.context.scene.frame_set(1); bpy.context.view_layer.update()
def W(n, t=False):
    pb = arm.pose.bones[n]; return arm.matrix_world @ (pb.tail if t else pb.head)
for n in ("pelvis", "head", "upperarm_r", "lowerarm_r", "hand_r", "middle_metacarpal_r", "foot_r", "ball_r"):
    print(n, [round(x, 3) for x in W(n)], [round(x, 3) for x in W(n, True)], "len", round((arm.pose.bones[n].tail - arm.pose.bones[n].head).length, 2), "scale", arm.pose.bones[n].scale[:])
NEXT = {"upperarm_r": "lowerarm_r", "lowerarm_r": "hand_r", "hand_r": "middle_metacarpal_r"}
def align(name, d):
    pb = arm.pose.bones[name]; bpy.context.view_layer.update()
    nx = NEXT.get(name); cur = (arm.pose.bones[nx].head - pb.head).normalized(); q = cur.rotation_difference(Vector(d).normalized())
    Mx = pb.matrix.copy(); t = Mx.to_translation()
    pb.matrix = Matrix.Translation(t) @ q.to_matrix().to_4x4() @ Matrix.Translation(-t) @ Mx
    bpy.context.view_layer.update()
    print("after", name, "next head", [round(x, 3) for x in W(nx)], "dir", [round(x,2) for x in (arm.pose.bones[nx].head - pb.head).normalized()])
align("upperarm_r", (-0.12, -0.32, -0.94)); align("lowerarm_r", (0.05, -1.0, 0.02)); align("hand_r", (0, -1, -0.15))
print("hand_r tail", [round(x,3) for x in W("hand_r", True)])
