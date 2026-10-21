# denoise baked EXR atlases (OIDN via the compositor) and write display-ready JPGs with the AgX look
# blender -b -P post.py -- DIR
import bpy, sys, os
D = sys.argv[sys.argv.index("--") + 1:][0]
sc = bpy.context.scene
sc.view_settings.view_transform = "AgX"; sc.view_settings.look = "AgX - Medium High Contrast"
EXPO = float(os.environ.get("HB_EXPO", "0"))
sc.view_settings.exposure = EXPO
for name in ("floor", "shell", "living", "upper"):
    src = os.path.join(D, f"atlas_{name}.exr")
    if not os.path.exists(src): continue
    img = bpy.data.images.load(src)
    W, H = img.size
    tree = bpy.data.node_groups.new("comp_" + name, "CompositorNodeTree")
    sc.compositing_node_group = tree
    n = tree.nodes
    tree.interface.new_socket("Image", in_out="OUTPUT", socket_type="NodeSocketColor")
    i = n.new("CompositorNodeImage"); i.image = img
    dn = n.new("CompositorNodeDenoise")
    try: dn.prefilter = "ACCURATE"
    except Exception: pass
    out = n.new("NodeGroupOutput")
    tree.links.new(i.outputs["Image"], dn.inputs["Image"]); tree.links.new(dn.outputs[0], out.inputs[0])
    sc.render.resolution_x, sc.render.resolution_y = W, H; sc.render.resolution_percentage = 100
    sc.render.engine = "BLENDER_WORKBENCH"
    sc.render.image_settings.file_format = "JPEG"; sc.render.image_settings.quality = 90
    sc.render.filepath = os.path.join(D, f"atlas_{name}.jpg")
    bpy.ops.render.render(write_still=True)
    print("POST", name, W)
