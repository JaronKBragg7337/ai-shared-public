import bpy, sys
bpy.ops.wm.read_factory_settings(use_empty=True)
for nm in ("isaiah", "walter", "jorge"):
    before = set(bpy.data.objects); acts = set(bpy.data.actions); mats=set(bpy.data.materials)
    bpy.ops.import_scene.gltf(filepath=f"C:/Users/lilli/Projects/heartbeat-observatory/homes/people/{nm}.glb")
    new = [o for o in bpy.data.objects if o not in before]
    arm = next(o for o in new if o.type == "ARMATURE")
    print("==", nm, "objs", [(o.name, o.type, tuple(round(x,2) for x in o.dimensions)) for o in new])
    print("actions", [(a.name, a.frame_range[:]) for a in bpy.data.actions if a not in acts])
    print("mats", [m.name for m in bpy.data.materials if m not in mats])
    for m in bpy.data.materials:
        if m in mats: continue
        for n in m.node_tree.nodes:
            if n.type == "TEX_IMAGE": print("  ", m.name, "img", n.image.name if n.image else None, n.image.size[:] if n.image else None)
    print("bones", len(arm.pose.bones), [b.name for b in arm.pose.bones if b.name in ("pelvis","head","neck_01","spine_03","hand_r","hand_l","upperarm_r","lowerarm_r","clavicle_r","thigh_r")])
    print("arm loc/rot/scale", arm.location[:], arm.rotation_euler[:], arm.scale[:], "dims", arm.dimensions[:])
    hb = arm.pose.bones.get("head"); print("head world z", (arm.matrix_world @ hb.head).z if hb else None)
