# Blue-hour city seen from a penthouse ~80 m up. Renders a 360 panorama used as the view out of the Homes loft windows.
# blender -b -P city.py -- out.png [width]
import bpy, math, random, sys
argv = sys.argv[sys.argv.index("--") + 1:]
OUT = argv[0]; W = int(argv[1]) if len(argv) > 1 else 8192
random.seed(42)
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = "CYCLES"
p = bpy.context.preferences.addons["cycles"].preferences; p.compute_device_type = "OPTIX"; p.get_devices()
for d in p.devices: d.use = d.type == "OPTIX"
sc.cycles.device = "GPU"; sc.cycles.samples = 128; sc.cycles.use_denoising = True; sc.cycles.denoiser = "OPTIX"
sc.render.resolution_x, sc.render.resolution_y = W, W // 2
sc.view_settings.view_transform = "AgX"; sc.view_settings.look = "AgX - Medium High Contrast"
sc.view_settings.exposure = 0.3

w = bpy.data.worlds.new("Sky"); sc.world = w
n, l = w.node_tree.nodes, w.node_tree.links; n.clear()
sky = n.new("ShaderNodeTexSky"); sky.sky_type = "MULTIPLE_SCATTERING"; sky.sun_elevation = math.radians(-3.5)
sky.sun_rotation = math.radians(200); sky.sun_disc = False; sky.aerosol_density = 1.5; sky.altitude = 80
bg = n.new("ShaderNodeBackground"); bg.inputs[1].default_value = 0.9
o = n.new("ShaderNodeOutputWorld"); l.new(sky.outputs[0], bg.inputs[0]); l.new(bg.outputs[0], o.inputs[0])


def material(name, build):
    m = bpy.data.materials.new(name); build(m.node_tree.nodes, m.node_tree.links); return m


def tower_mat(nodes, links):
    # facade: dark glass; a window grid (1.8 m x 3.5 m floors); each window on/off by per-building odds, warm or cool
    b = nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (0.015, 0.017, 0.022, 1); b.inputs["Roughness"].default_value = 0.2; b.inputs["Metallic"].default_value = 0.5
    geo = nodes.new("ShaderNodeNewGeometry"); sep = nodes.new("ShaderNodeSeparateXYZ"); links.new(geo.outputs["Position"], sep.inputs[0])
    at = nodes.new("ShaderNodeAttribute"); at.attribute_name = "rnd"; at.attribute_type = "GEOMETRY"
    u = nodes.new("ShaderNodeMath"); u.operation = "ADD"; links.new(sep.outputs["X"], u.inputs[0]); links.new(sep.outputs["Y"], u.inputs[1])
    def M(op, a, bb=None, v=None):
        m = nodes.new("ShaderNodeMath"); m.operation = op
        links.new(a, m.inputs[0]) if not isinstance(a, (int, float)) else m.inputs[0].__setattr__("default_value", a)
        if bb is not None: links.new(bb, m.inputs[1])
        if v is not None: m.inputs[1].default_value = v
        return m.outputs[0]
    cu = M("DIVIDE", u.outputs[0], v=1.8); cv = M("DIVIDE", sep.outputs["Z"], v=3.5)
    fu = M("FRACT", cu); fv = M("FRACT", cv)
    inu = M("LESS_THAN", fu, v=0.72); inv = M("MULTIPLY", M("GREATER_THAN", fv, v=0.22), M("LESS_THAN", fv, v=0.86))
    win = M("MULTIPLY", inu, inv)
    comb = nodes.new("ShaderNodeCombineXYZ"); links.new(M("FLOOR", cu), comb.inputs["X"]); links.new(M("FLOOR", cv), comb.inputs["Y"])
    links.new(M("MULTIPLY", at.outputs["Fac"], v=97.0), comb.inputs["Z"])
    wn = nodes.new("ShaderNodeTexWhiteNoise"); wn.noise_dimensions = "3D"; links.new(comb.outputs[0], wn.inputs["Vector"])
    odds = M("ADD", M("MULTIPLY", at.outputs["Fac"], v=0.38), v=0.08)          # 8-46% lit per building
    on = M("LESS_THAN", wn.outputs["Value"], odds)
    lit = M("MULTIPLY", on, win)
    tint = nodes.new("ShaderNodeValToRGB"); cr = tint.color_ramp
    cr.elements[0].color = (1.0, 0.55, 0.25, 1); cr.elements[1].color = (0.7, 0.82, 1.0, 1); cr.elements[1].position = 0.9
    e = cr.elements.new(0.6); e.color = (1.0, 0.85, 0.65, 1)
    wn2 = nodes.new("ShaderNodeTexWhiteNoise"); wn2.noise_dimensions = "3D"; links.new(comb.outputs[0], wn2.inputs["Vector"])
    sep2 = nodes.new("ShaderNodeSeparateColor"); links.new(wn2.outputs["Color"], sep2.inputs[0]); links.new(sep2.outputs[0], tint.inputs[0])
    b.inputs["Emission Color"].default_value = (1, 1, 1, 1); links.new(tint.outputs[0], b.inputs["Emission Color"])
    strength = M("MULTIPLY", lit, M("POWER", M("ADD", M("MULTIPLY", sep2.outputs[1], v=1.4), v=0.15), v=2.0))
    links.new(strength, b.inputs["Emission Strength"])
    # unlit windows are glass: a bit glossier
    links.new(M("SUBTRACT", 0.3, M("MULTIPLY", win, v=0.25)), b.inputs["Roughness"])


def ground_mat(nodes, links):
    b = nodes["Principled BSDF"]; b.inputs["Base Color"].default_value = (0.01, 0.01, 0.012, 1); b.inputs["Roughness"].default_value = 0.6
    tc = nodes.new("ShaderNodeTexCoord"); sep = nodes.new("ShaderNodeSeparateXYZ"); links.new(tc.outputs["Object"], sep.inputs[0])
    # street grid glow every 90 m
    def line(axis):
        m = nodes.new("ShaderNodeMath"); m.operation = "PINGPONG"; m.inputs[1].default_value = 45
        off = nodes.new("ShaderNodeMath"); off.operation = "ADD"; off.inputs[1].default_value = 45
        links.new(sep.outputs[axis], off.inputs[0]); links.new(off.outputs[0], m.inputs[0])
        g = nodes.new("ShaderNodeMath"); g.operation = "LESS_THAN"; g.inputs[1].default_value = 0.8
        links.new(m.outputs[0], g.inputs[0]); return g
    a, c = line("X"), line("Y")
    mx = nodes.new("ShaderNodeMath"); mx.operation = "MAXIMUM"; links.new(a.outputs[0], mx.inputs[0]); links.new(c.outputs[0], mx.inputs[1])
    st = nodes.new("ShaderNodeMath"); st.operation = "MULTIPLY"; st.inputs[1].default_value = 2.5
    links.new(mx.outputs[0], st.inputs[0])
    b.inputs["Emission Color"].default_value = (1.0, 0.55, 0.2, 1); links.new(st.outputs[0], b.inputs["Emission Strength"])


tm = material("Tower", tower_mat)
gm = material("Ground", ground_mat)
bpy.ops.mesh.primitive_plane_add(size=8000, location=(0, 0, 0)); bpy.context.object.data.materials.append(gm)
# the city: towers on a 90 m block grid, taller near the middle distance, none within 90 m. One mesh, per-building "rnd".
verts, faces, rnds, beacons = [], [], [], []
for gx in range(-22, 23):
    for gy in range(-22, 23):
        for k in range(random.randint(1, 3)):
            x = gx * 90 + random.uniform(-30, 30); y = gy * 90 + random.uniform(-30, 30)
            r = math.hypot(x, y)
            if r < 90 or r > 2000: continue
            h = random.uniform(15, 60) + (random.random() ** 3) * (230 if r < 900 else 120)
            sx, sy = random.uniform(14, 34) / 2, random.uniform(14, 34) / 2
            i0 = len(verts)
            for zz in (0, h):
                for dx, dy in ((-sx, -sy), (sx, -sy), (sx, sy), (-sx, sy)):
                    verts.append((x + dx, y + dy, zz))
            for f in ((0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7), (4, 5, 6, 7)):
                faces.append(tuple(i0 + j for j in f)); rnds.append(random.random() if f[0] != 4 else 0.99)
            if h > 150 and random.random() < 0.5: beacons.append((x, y, h + 1.5))
me = bpy.data.meshes.new("City"); me.from_pydata(verts, [], faces); me.update()
at = me.attributes.new("rnd", "FLOAT", "FACE"); at.data.foreach_set("value", rnds)
ob = bpy.data.objects.new("City", me); sc.collection.objects.link(ob); me.materials.append(tm)
av = material("Aviation", lambda n_, l_: (n_["Principled BSDF"].inputs["Emission Color"].__setattr__("default_value", (1, 0.05, 0.02, 1)), n_["Principled BSDF"].inputs["Emission Strength"].__setattr__("default_value", 40)))
for loc in beacons:
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1.2, location=loc); bpy.context.object.data.materials.append(av)
cd = bpy.data.cameras.new("Pano"); cd.type = "PANO"
try:
    cd.panorama_type = "EQUIRECTANGULAR"
except Exception:
    cd.cycles.panorama_type = "EQUIRECTANGULAR"
cam = bpy.data.objects.new("Pano", cd); sc.collection.objects.link(cam)
cam.location = (0, 0, 84); cam.rotation_euler = (math.radians(90), 0, 0)
sc.camera = cam
sc.render.filepath = OUT
bpy.ops.render.render(write_still=True)
print("CITY OK")
