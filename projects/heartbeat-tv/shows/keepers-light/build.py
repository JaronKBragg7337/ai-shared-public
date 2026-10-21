# Heartbeat TV - "The Keeper's Light". Pure-script Blender scene (no downloaded assets).
#   ep.1 "First Light" (dawn) - the default; ep.2 "Storm Night" (--ep 2: night gale, rain, lightning, the beam through it);
#   ep.3 "The Keeper" (--ep 3: the morning after - the lamp goes out, the keeper (Walter, a Loft person) walks out to the rail).
# blender -b -P build.py -- [--ep 2] [--still FRAME out.png] [--save out.blend] [--anim OUTDIR]
import bpy, math, random, sys
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
EP = int(argv[argv.index("--ep") + 1]) if "--ep" in argv else 1
FPS = 24
DUR = 42 * FPS          # 42 s
random.seed(7)

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.fps = FPS
sc.frame_start, sc.frame_end = 1, DUR

# ---------- render ----------
sc.render.engine = "CYCLES"
prefs = bpy.context.preferences.addons["cycles"].preferences
prefs.compute_device_type = "OPTIX"
prefs.get_devices()
for d in prefs.devices:
    d.use = d.type == "OPTIX"
sc.cycles.device = "CPU" if "--cpu" in argv else "GPU"
if "--samples" in argv:
    pass  # set after the defaults below
sc.cycles.samples = int(argv[argv.index("--samples") + 1]) if "--samples" in argv else 96
sc.cycles.use_adaptive_sampling = True
sc.cycles.adaptive_threshold = 0.02
sc.cycles.use_denoising = True
sc.cycles.denoiser = "OPENIMAGEDENOISE" if "--cpu" in argv else "OPTIX"
sc.cycles.max_bounces = 8
sc.cycles.volume_bounces = 1
sc.cycles.caustics_reflective = False
sc.cycles.caustics_refractive = False
sc.render.resolution_x, sc.render.resolution_y = 1280, 720
sc.render.use_motion_blur = True
sc.render.motion_blur_shutter = 0.4
try:
    sc.view_settings.view_transform = "AgX"
    sc.view_settings.look = "AgX - Medium High Contrast"
except Exception as e:
    print("look", e)
sc.view_settings.exposure = {1: 0.0, 2: 1.3, 3: 0.0}[EP]     # ep.2 night: lifted so it reads on a phone, still dark


def mat(name):
    m = bpy.data.materials.new(name)
    return m, m.node_tree.nodes, m.node_tree.links


def curves_of(idb):
    ad = idb.animation_data
    if not ad or not ad.action:
        return []
    act = ad.action
    cs = getattr(act, "fcurves", None)
    if cs is not None:
        return list(cs)
    try:
        return [fc for layer in act.layers for strip in layer.strips for bag in strip.channelbags for fc in bag.fcurves]
    except Exception:
        return []


def set_interp(idb, kind):
    for fc in curves_of(idb):
        for k in fc.keyframe_points:
            k.interpolation = kind


def link(l, a, b):
    l.new(a, b)


def add(obj_list, o):
    obj_list.append(o)
    return o


def storm_world():
    # night gale: a low, lumpy cloud deck (noise on the view direction), a touch lighter toward the horizon. Lightning
    # flashes are keyframed on the background strength (see FLASHES).
    w = bpy.data.worlds.new("StormSky"); sc.world = w
    wn, wl = w.node_tree.nodes, w.node_tree.links; wn.clear()
    tc = wn.new("ShaderNodeTexCoord")
    mp = wn.new("ShaderNodeMapping"); mp.inputs["Scale"].default_value = (2.2, 2.2, 5.0)
    nz = wn.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 2.4; nz.inputs["Detail"].default_value = 10
    nz.inputs["Roughness"].default_value = 0.62
    wl.new(tc.outputs["Generated"], mp.inputs[0]); wl.new(mp.outputs[0], nz.inputs["Vector"])
    ramp = wn.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].position = 0.38; ramp.color_ramp.elements[0].color = (0.0025, 0.003, 0.0045, 1)
    ramp.color_ramp.elements[1].position = 0.72; ramp.color_ramp.elements[1].color = (0.018, 0.021, 0.028, 1)
    wl.new(nz.outputs["Fac"], ramp.inputs[0])
    # horizon glow: brighter where the view direction is level
    sep = wn.new("ShaderNodeSeparateXYZ"); wl.new(tc.outputs["Generated"], sep.inputs[0])
    hz = wn.new("ShaderNodeMapRange"); hz.inputs["From Min"].default_value = 0.35; hz.inputs["From Max"].default_value = 0.0
    hz.inputs["To Min"].default_value = 1.0; hz.inputs["To Max"].default_value = 2.2
    ab = wn.new("ShaderNodeMath"); ab.operation = "ABSOLUTE"; wl.new(sep.outputs["Z"], ab.inputs[0]); wl.new(ab.outputs[0], hz.inputs["Value"])
    mul = wn.new("ShaderNodeMix"); mul.data_type = "RGBA"; mul.blend_type = "MULTIPLY"; mul.inputs["Factor"].default_value = 1
    wl.new(ramp.outputs[0], mul.inputs["A"])
    cm = wn.new("ShaderNodeCombineXYZ"); wl.new(hz.outputs["Result"], cm.inputs[0]); wl.new(hz.outputs["Result"], cm.inputs[1]); wl.new(hz.outputs["Result"], cm.inputs[2])
    wl.new(cm.outputs[0], mul.inputs["B"])
    bg = wn.new("ShaderNodeBackground"); bg.inputs["Strength"].default_value = 1.0
    out = wn.new("ShaderNodeOutputWorld")
    wl.new(mul.outputs["Result"], bg.inputs[0]); wl.new(bg.outputs[0], out.inputs["Surface"])
    return bg


# ---------- sky ----------
w = bpy.data.worlds.new("Sky")
sc.world = w
wn, wl = w.node_tree.nodes, w.node_tree.links
wn.clear()
sky = wn.new("ShaderNodeTexSky")
sky.sky_type = "MULTIPLE_SCATTERING"
sky.sun_disc = True
sky.sun_size = math.radians(0.8)
sky.sun_intensity = 0.6
sky.altitude = 40
sky.air_density = 1.0
sky.aerosol_density = 2.2          # hazy sea air
sky.ozone_density = 1.0
SUN_AZ = math.radians(8)
sky.sun_rotation = SUN_AZ
bg = wn.new("ShaderNodeBackground")
bg.inputs["Strength"].default_value = 0.35
out = wn.new("ShaderNodeOutputWorld")
wl.new(sky.outputs[0], bg.inputs[0])
wl.new(bg.outputs[0], out.inputs["Surface"])
# sunrise: sun climbs from just under the horizon to ~7 degrees
sky.sun_elevation = math.radians(-1.5)
sky.keyframe_insert("sun_elevation", frame=1)
sky.sun_elevation = math.radians(7.0)
sky.keyframe_insert("sun_elevation", frame=DUR)
STORM_BG = storm_world() if EP == 2 else None
if EP == 3:
    # the morning after: the same physical sky with its sun disc off (a sun lamp gives the direct light), broken grey cloud
    # over it, only above the horizon
    SUN3 = Vector((0.8, -0.5, 0.0)); SUN3.z = math.tan(math.radians(11)) * SUN3.length; SUN3.normalize()
    if w.node_tree.animation_data:
        w.node_tree.animation_data_clear()
    sky.sun_disc = False
    sky.sun_rotation = math.atan2(SUN3.x, SUN3.y)
    sky.aerosol_density = 1.6
    sky.sun_elevation = math.radians(11)
    tc3 = wn.new("ShaderNodeTexCoord"); mp3 = wn.new("ShaderNodeMapping"); mp3.inputs["Scale"].default_value = (1.6, 1.6, 6.0)
    nz3 = wn.new("ShaderNodeTexNoise"); nz3.inputs["Scale"].default_value = 2.2; nz3.inputs["Detail"].default_value = 9
    nz3.inputs["Roughness"].default_value = 0.6
    wl.new(tc3.outputs["Generated"], mp3.inputs[0]); wl.new(mp3.outputs[0], nz3.inputs["Vector"])
    cm3 = wn.new("ShaderNodeMapRange"); cm3.inputs["From Min"].default_value = 0.4; cm3.inputs["From Max"].default_value = 0.52
    wl.new(nz3.outputs["Fac"], cm3.inputs["Value"])
    sp3 = wn.new("ShaderNodeSeparateXYZ"); wl.new(tc3.outputs["Generated"], sp3.inputs[0])
    hz3 = wn.new("ShaderNodeMapRange"); hz3.inputs["From Min"].default_value = 0.0; hz3.inputs["From Max"].default_value = 0.12
    wl.new(sp3.outputs["Z"], hz3.inputs["Value"])
    mk3 = wn.new("ShaderNodeMath"); mk3.operation = "MULTIPLY"
    wl.new(cm3.outputs["Result"], mk3.inputs[0]); wl.new(hz3.outputs["Result"], mk3.inputs[1])
    cc3 = wn.new("ShaderNodeMix"); cc3.data_type = "RGBA"; cc3.inputs["Factor"].default_value = 0.35
    wl.new(sky.outputs[0], cc3.inputs["A"]); cc3.inputs["B"].default_value = (0.42, 0.42, 0.43, 1)
    ccm = wn.new("ShaderNodeMix"); ccm.data_type = "RGBA"
    wl.new(mk3.outputs[0], ccm.inputs["Factor"]); wl.new(sky.outputs[0], ccm.inputs["A"]); wl.new(cc3.outputs["Result"], ccm.inputs["B"])
    wl.new(ccm.outputs["Result"], bg.inputs[0])
    bg.inputs["Strength"].default_value = 0.45
    bpy.ops.object.light_add(type="SUN"); sun3 = bpy.context.object
    sun3.data.energy = 3.2; sun3.data.color = (1.0, 0.86, 0.68); sun3.data.angle = math.radians(1.2)
    sun3.rotation_euler = (-SUN3).to_track_quat("-Z", "Y").to_euler()

# ---------- ocean ----------
water, n, l = mat("Water")
n.clear()
bs = n.new("ShaderNodeBsdfPrincipled")
bs.inputs["Base Color"].default_value = (0.004, 0.018, 0.026, 1)
bs.inputs["Roughness"].default_value = 0.035
bs.inputs["IOR"].default_value = 1.333
bs.inputs["Subsurface Weight"].default_value = 0.0
foam_attr = n.new("ShaderNodeAttribute"); foam_attr.attribute_name = "foam"
foam_ramp = n.new("ShaderNodeValToRGB")
foam_ramp.color_ramp.elements[0].position = 0.35
foam_ramp.color_ramp.elements[1].position = 0.9
foam_noise = n.new("ShaderNodeTexNoise"); foam_noise.inputs["Scale"].default_value = 30; foam_noise.inputs["Detail"].default_value = 8
fmul = n.new("ShaderNodeMath"); fmul.operation = "MULTIPLY"
link(l, foam_attr.outputs["Fac"], foam_ramp.inputs[0])
link(l, foam_ramp.outputs[0], fmul.inputs[0])
link(l, foam_noise.outputs["Fac"], fmul.inputs[1])
fmix = n.new("ShaderNodeMix"); fmix.data_type = "RGBA"
fmix.inputs["A"].default_value = (0.004, 0.018, 0.026, 1)
fmix.inputs["B"].default_value = (0.8, 0.82, 0.83, 1)
link(l, fmul.outputs[0], fmix.inputs["Factor"])
link(l, fmix.outputs["Result"], bs.inputs["Base Color"])
rmix = n.new("ShaderNodeMapRange")
rmix.inputs["To Min"].default_value = 0.035; rmix.inputs["To Max"].default_value = 0.6
link(l, fmul.outputs[0], rmix.inputs["Value"])
link(l, rmix.outputs["Result"], bs.inputs["Roughness"])
wo = n.new("ShaderNodeOutputMaterial")
link(l, bs.outputs[0], wo.inputs["Surface"])

bpy.ops.mesh.primitive_plane_add(size=1)
ocean = bpy.context.object; ocean.name = "Ocean"; ocean.location = (-300, -300, 0)
om = ocean.modifiers.new("Ocean", "OCEAN")
om.geometry_mode = "GENERATE"
om.resolution = 18
om.viewport_resolution = 4
om.spatial_size = 100
om.size = 1.0
om.repeat_x = om.repeat_y = 7
om.wave_scale = {1: 1.1, 2: 2.0, 3: 1.3}[EP]
om.choppiness = {1: 1.1, 2: 1.45, 3: 1.2}[EP]
om.wind_velocity = {1: 11, 2: 20, 3: 13}[EP]      # ep.3: the swell left over from the storm
om.wave_alignment = {1: 0.35, 2: 0.55, 3: 0.5}[EP]
om.wave_direction = math.radians(200)
om.use_normals = True
om.use_foam = True
om.foam_layer_name = "foam"
om.foam_coverage = {1: 0.25, 2: 0.6, 3: 0.35}[EP]
om.random_seed = 3
om.time = 1.0
om.keyframe_insert("time", frame=1)
om.time = 1.0 + DUR / FPS * 0.9
om.keyframe_insert("time", frame=DUR)
for fc in ocean.animation_data.action.fcurves if hasattr(ocean.animation_data.action, "fcurves") else []:
    for k in fc.keyframe_points:
        k.interpolation = "LINEAR"
ocean.data.materials.append(water)
bpy.ops.object.shade_smooth()

# far water out to the horizon (bump-only waves), sits just under the simulated tile
far_m, n, l = mat("FarWater")
n.clear()
fb = n.new("ShaderNodeBsdfPrincipled")
fb.inputs["Base Color"].default_value = (0.004, 0.018, 0.026, 1)
fb.inputs["Roughness"].default_value = 0.06
fb.inputs["IOR"].default_value = 1.333
tc = n.new("ShaderNodeTexCoord")
mp = n.new("ShaderNodeMapping"); mp.inputs["Scale"].default_value = (0.08, 0.2, 0.08)
wv = n.new("ShaderNodeTexNoise"); wv.inputs["Scale"].default_value = 6; wv.inputs["Detail"].default_value = 12; wv.inputs["Roughness"].default_value = 0.6
bump = n.new("ShaderNodeBump"); bump.inputs["Strength"].default_value = 0.35; bump.inputs["Distance"].default_value = 0.5
link(l, tc.outputs["Object"], mp.inputs[0]); link(l, mp.outputs[0], wv.inputs[0])
link(l, wv.outputs["Fac"], bump.inputs["Height"]); link(l, bump.outputs[0], fb.inputs["Normal"])
fo = n.new("ShaderNodeOutputMaterial"); link(l, fb.outputs[0], fo.inputs["Surface"])
bpy.ops.mesh.primitive_circle_add(vertices=64, radius=20000, fill_type="NGON", location=(0, 0, -1.15))
far = bpy.context.object; far.name = "FarWater"
far.data.materials.append(far_m)

# ---------- rock ----------
rock_m, n, l = mat("Rock")
n.clear()
rb = n.new("ShaderNodeBsdfPrincipled")
tc = n.new("ShaderNodeTexCoord")
rn = n.new("ShaderNodeTexNoise"); rn.inputs["Scale"].default_value = 1.8; rn.inputs["Detail"].default_value = 14; rn.inputs["Roughness"].default_value = 0.65
rv = n.new("ShaderNodeTexVoronoi"); rv.inputs["Scale"].default_value = 3.5
link(l, tc.outputs["Object"], rn.inputs["Vector"]); link(l, tc.outputs["Object"], rv.inputs["Vector"])
rr = n.new("ShaderNodeValToRGB")
rr.color_ramp.elements[0].color = (0.035, 0.032, 0.03, 1)
rr.color_ramp.elements[1].color = (0.23, 0.21, 0.18, 1)
link(l, rn.outputs["Fac"], rr.inputs[0])
# wet band near the waterline: darker + glossy
geo = n.new("ShaderNodeNewGeometry")
sep = n.new("ShaderNodeSeparateXYZ"); link(l, geo.outputs["Position"], sep.inputs[0])
wet = n.new("ShaderNodeMapRange"); wet.inputs["From Min"].default_value = 1.4; wet.inputs["From Max"].default_value = 0.2
wet.inputs["To Min"].default_value = 0; wet.inputs["To Max"].default_value = 1
link(l, sep.outputs["Z"], wet.inputs["Value"])
dark = n.new("ShaderNodeMix"); dark.data_type = "RGBA"; dark.blend_type = "MULTIPLY"
link(l, wet.outputs["Result"], dark.inputs["Factor"]); link(l, rr.outputs[0], dark.inputs["A"])
dark.inputs["B"].default_value = (0.35, 0.36, 0.34, 1)
# lichen / salt crust on top
top = n.new("ShaderNodeMapRange"); top.inputs["From Min"].default_value = 2.5; top.inputs["From Max"].default_value = 4.0
link(l, sep.outputs["Z"], top.inputs["Value"])
lich_n = n.new("ShaderNodeTexNoise"); lich_n.inputs["Scale"].default_value = 9 if EP != 3 else 30; lich_n.inputs["Detail"].default_value = 6
link(l, tc.outputs["Object"], lich_n.inputs["Vector"])
lmul = n.new("ShaderNodeMath"); lmul.operation = "MULTIPLY"
lstep = n.new("ShaderNodeMath"); lstep.operation = "GREATER_THAN"; lstep.inputs[1].default_value = 0.55 if EP != 3 else 0.74
link(l, lich_n.outputs["Fac"], lstep.inputs[0]); link(l, lstep.outputs[0], lmul.inputs[0]); link(l, top.outputs["Result"], lmul.inputs[1])
lich = n.new("ShaderNodeMix"); lich.data_type = "RGBA"
link(l, lmul.outputs[0], lich.inputs["Factor"]); link(l, dark.outputs["Result"], lich.inputs["A"])
lich.inputs["B"].default_value = (0.42, 0.38, 0.16, 1)
link(l, lich.outputs["Result"], rb.inputs["Base Color"])
rrough = n.new("ShaderNodeMapRange"); rrough.inputs["To Min"].default_value = 0.85 if EP != 3 else 0.42   # ep.3: still wet
rrough.inputs["To Max"].default_value = 0.18
link(l, wet.outputs["Result"], rrough.inputs["Value"]); link(l, rrough.outputs["Result"], rb.inputs["Roughness"])
rbump = n.new("ShaderNodeBump"); rbump.inputs["Strength"].default_value = 0.6
if EP == 3:
    gpos = n.new("ShaderNodeNewGeometry")
    gfine = n.new("ShaderNodeTexNoise"); gfine.inputs["Scale"].default_value = 7; gfine.inputs["Detail"].default_value = 15
    gfine.inputs["Roughness"].default_value = 0.7
    link(l, gpos.outputs["Position"], gfine.inputs["Vector"])
    gcr = n.new("ShaderNodeTexVoronoi"); gcr.feature = "DISTANCE_TO_EDGE"; gcr.inputs["Scale"].default_value = 2.2
    link(l, gpos.outputs["Position"], gcr.inputs["Vector"])
    fb2 = n.new("ShaderNodeBump"); fb2.inputs["Strength"].default_value = 0.45; fb2.inputs["Distance"].default_value = 0.02
    gmx = n.new("ShaderNodeMath"); gmx.operation = "ADD"
    gcl = n.new("ShaderNodeMath"); gcl.operation = "MINIMUM"; gcl.inputs[1].default_value = 0.04
    link(l, gcr.outputs["Distance"], gcl.inputs[0])
    link(l, gfine.outputs["Fac"], gmx.inputs[0]); link(l, gcl.outputs[0], gmx.inputs[1])
    link(l, gmx.outputs[0], fb2.inputs["Height"])
bmix = n.new("ShaderNodeMath"); bmix.operation = "ADD"
link(l, rn.outputs["Fac"], bmix.inputs[0]); link(l, rv.outputs["Distance"], bmix.inputs[1])
link(l, bmix.outputs[0], rbump.inputs["Height"]); link(l, rbump.outputs[0], rb.inputs["Normal"])
if EP == 3:
    link(l, rbump.outputs[0], fb2.inputs["Normal"]); link(l, fb2.outputs[0], rb.inputs["Normal"])
ro = n.new("ShaderNodeOutputMaterial"); link(l, rb.outputs[0], ro.inputs["Surface"])

tex_a = bpy.data.textures.new("rockA", "VORONOI"); tex_a.noise_scale = 2.6
tex_b = bpy.data.textures.new("rockB", "CLOUDS"); tex_b.noise_scale = 1.6; tex_b.noise_depth = 5
tex_c = bpy.data.textures.new("rockC", "CLOUDS"); tex_c.noise_scale = 0.25; tex_c.noise_depth = 2


def flatten_group(xr, yr, zmax):
    # Geometry Nodes, world space: z <= zmax inside the rectangle, rising 1.1 m per metre outside it
    ng = bpy.data.node_groups.new("FlattenUnderLanding", "GeometryNodeTree")
    ng.interface.new_socket("Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
    ng.interface.new_socket("Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    N, Lk = ng.nodes, ng.links
    gi = N.new("NodeGroupInput"); go = N.new("NodeGroupOutput")
    setp = N.new("GeometryNodeSetPosition"); pos = N.new("GeometryNodeInputPosition")
    selfo = N.new("GeometryNodeSelfObject"); oi = N.new("GeometryNodeObjectInfo")
    Lk.new(selfo.outputs[0], oi.inputs["Object"])
    tr_out = next(o for o in oi.outputs if "Transform" in o.name)
    tw = N.new("FunctionNodeTransformPoint"); Lk.new(pos.outputs[0], tw.inputs[0]); Lk.new(tr_out, tw.inputs[1])
    sep = N.new("ShaderNodeSeparateXYZ"); Lk.new(tw.outputs[0], sep.inputs[0])
    mn = N.new("ShaderNodeMath"); mn.operation = "MINIMUM"; mn.inputs[1].default_value = zmax
    Lk.new(sep.outputs["Z"], mn.inputs[0])
    comb = N.new("ShaderNodeCombineXYZ")
    Lk.new(sep.outputs["X"], comb.inputs[0]); Lk.new(sep.outputs["Y"], comb.inputs[1]); Lk.new(mn.outputs[0], comb.inputs[2])
    inv = N.new("FunctionNodeInvertMatrix"); Lk.new(tr_out, inv.inputs[0])
    back = N.new("FunctionNodeTransformPoint"); Lk.new(comb.outputs[0], back.inputs[0]); Lk.new(inv.outputs[0], back.inputs[1])
    cx, cy, hx, hy = (xr[0] + xr[1]) / 2, (yr[0] + yr[1]) / 2, (xr[1] - xr[0]) / 2, (yr[1] - yr[0]) / 2
    flat2 = N.new("ShaderNodeCombineXYZ"); Lk.new(sep.outputs["X"], flat2.inputs[0]); Lk.new(sep.outputs["Y"], flat2.inputs[1])
    v1 = N.new("ShaderNodeVectorMath"); v1.operation = "SUBTRACT"; v1.inputs[1].default_value = (cx, cy, 0)
    Lk.new(flat2.outputs[0], v1.inputs[0])
    v2 = N.new("ShaderNodeVectorMath"); v2.operation = "ABSOLUTE"; Lk.new(v1.outputs[0], v2.inputs[0])
    v3 = N.new("ShaderNodeVectorMath"); v3.operation = "SUBTRACT"; v3.inputs[1].default_value = (hx, hy, 0); Lk.new(v2.outputs[0], v3.inputs[0])
    v4 = N.new("ShaderNodeVectorMath"); v4.operation = "MAXIMUM"; v4.inputs[1].default_value = (0, 0, 0); Lk.new(v3.outputs[0], v4.inputs[0])
    v5 = N.new("ShaderNodeVectorMath"); v5.operation = "LENGTH"; Lk.new(v4.outputs[0], v5.inputs[0])
    lim = N.new("ShaderNodeMath"); lim.operation = "MULTIPLY_ADD"; lim.inputs[1].default_value = 1.1; lim.inputs[2].default_value = zmax
    Lk.new(v5.outputs["Value"], lim.inputs[0])
    nzg = N.new("ShaderNodeTexNoise"); nzg.inputs["Scale"].default_value = 0.9; nzg.inputs["Detail"].default_value = 6
    Lk.new(flat2.outputs[0], nzg.inputs["Vector"])
    nzm = N.new("ShaderNodeMath"); nzm.operation = "MULTIPLY_ADD"; nzm.inputs[1].default_value = 1.4; nzm.inputs[2].default_value = -0.7
    Lk.new(nzg.outputs["Fac"], nzm.inputs[0])
    nzd = N.new("ShaderNodeMath"); nzd.operation = "MULTIPLY"; Lk.new(nzm.outputs[0], nzd.inputs[0]); Lk.new(v5.outputs["Value"], nzd.inputs[1])
    lim2 = N.new("ShaderNodeMath"); lim2.operation = "ADD"; Lk.new(lim.outputs[0], lim2.inputs[0]); Lk.new(nzd.outputs[0], lim2.inputs[1])
    Lk.new(lim2.outputs[0], mn.inputs[1])
    Lk.new(gi.outputs[0], setp.inputs["Geometry"])
    Lk.new(back.outputs[0], setp.inputs["Position"]); Lk.new(setp.outputs[0], go.inputs[0])
    return ng


def boulder(loc, scale, rot=0):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=6, radius=1, location=loc)
    o = bpy.context.object
    o.scale = scale
    o.rotation_euler = (random.uniform(-.3, .3), random.uniform(-.3, .3), rot)
    d1 = o.modifiers.new("d1", "DISPLACE"); d1.texture = tex_a; d1.strength = -0.9; d1.texture_coords = "GLOBAL"
    d2 = o.modifiers.new("d2", "DISPLACE"); d2.texture = tex_b; d2.strength = 1.1; d2.texture_coords = "GLOBAL"
    d3 = o.modifiers.new("d3", "DISPLACE"); d3.texture = tex_c; d3.strength = 0.18; d3.texture_coords = "GLOBAL"
    o.data.materials.append(rock_m)
    bpy.ops.object.shade_smooth()
    return o


# island: a main mass under the tower plus a scatter of boulders into the surf
boulder((0, 0, 0.6), (9, 8, 3.0))
boulder((3.5, -2, 1.8), (5, 4.5, 2.2), 0.6)
boulder((-4, 2.5, 1.4), (4.5, 5, 2.0), 1.2)
for i in range(22):
    a = random.uniform(0, 2 * math.pi); r = random.uniform(8.5, 15)
    s = random.uniform(0.7, 2.6)
    boulder((math.cos(a) * r, math.sin(a) * r, random.uniform(-0.6, 0.1)),
            (s * random.uniform(.8, 1.4), s * random.uniform(.8, 1.4), s * random.uniform(.5, .9)), a)

# ---------- lighthouse ----------
paint, n, l = mat("Paint")
n.clear()
pb = n.new("ShaderNodeBsdfPrincipled"); pb.inputs["Roughness"].default_value = 0.55
geo = n.new("ShaderNodeNewGeometry"); sep = n.new("ShaderNodeSeparateXYZ"); link(l, geo.outputs["Position"], sep.inputs[0])
band = n.new("ShaderNodeMath"); band.operation = "DIVIDE"; band.inputs[1].default_value = 3.4
flo = n.new("ShaderNodeMath"); flo.operation = "FLOOR"
mod = n.new("ShaderNodeMath"); mod.operation = "MODULO"; mod.inputs[1].default_value = 2
link(l, sep.outputs["Z"], band.inputs[0]); link(l, band.outputs[0], flo.inputs[0]); link(l, flo.outputs[0], mod.inputs[0])
col = n.new("ShaderNodeMix"); col.data_type = "RGBA"
col.inputs["A"].default_value = (0.82, 0.8, 0.76, 1)
col.inputs["B"].default_value = (0.42, 0.04, 0.03, 1)
link(l, mod.outputs[0], col.inputs["Factor"])
grime = n.new("ShaderNodeTexNoise"); grime.inputs["Scale"].default_value = 4; grime.inputs["Detail"].default_value = 10
streak = n.new("ShaderNodeMapping"); streak.inputs["Scale"].default_value = (6, 6, 0.4)
tc = n.new("ShaderNodeTexCoord"); link(l, tc.outputs["Object"], streak.inputs[0]); link(l, streak.outputs[0], grime.inputs[0])
gr = n.new("ShaderNodeValToRGB"); gr.color_ramp.elements[0].color = (0.55, 0.52, 0.48, 1) if EP != 3 else (0.36, 0.34, 0.31, 1); gr.color_ramp.elements[1].color = (1, 1, 1, 1)
gr.color_ramp.elements[0].position = 0.35
link(l, grime.outputs["Fac"], gr.inputs[0])
gm = n.new("ShaderNodeMix"); gm.data_type = "RGBA"; gm.blend_type = "MULTIPLY"; gm.inputs["Factor"].default_value = 1
link(l, col.outputs["Result"], gm.inputs["A"]); link(l, gr.outputs[0], gm.inputs["B"])
link(l, gm.outputs["Result"], pb.inputs["Base Color"])
pbump = n.new("ShaderNodeBump"); pbump.inputs["Strength"].default_value = 0.15
link(l, grime.outputs["Fac"], pbump.inputs["Height"]); link(l, pbump.outputs[0], pb.inputs["Normal"])
po = n.new("ShaderNodeOutputMaterial"); link(l, pb.outputs[0], po.inputs["Surface"])

metal, n, l = mat("DarkMetal")
mb = n["Principled BSDF"]; mb.inputs["Base Color"].default_value = (0.03, 0.035, 0.035, 1)
mb.inputs["Metallic"].default_value = 0.9; mb.inputs["Roughness"].default_value = 0.42

glass, n, l = mat("Glass")
gb = n["Principled BSDF"]; gb.inputs["Transmission Weight"].default_value = 1.0
gb.inputs["Roughness"].default_value = 0.02; gb.inputs["IOR"].default_value = 1.45
gb.inputs["Base Color"].default_value = (0.9, 0.95, 0.95, 1)

lamp_m, n, l = mat("Lamp")
lb = n["Principled BSDF"]; lb.inputs["Emission Color"].default_value = (1.0, 0.78, 0.45, 1)
lb.inputs["Emission Strength"].default_value = 60

stone, n, l = mat("Stone")
sb = n["Principled BSDF"]; sb.inputs["Base Color"].default_value = (0.36, 0.34, 0.31, 1); sb.inputs["Roughness"].default_value = 0.8

BASE = 3.2
bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=2.9, depth=1.2, location=(0, 0, BASE - 0.1))
bpy.context.object.data.materials.append(stone)
bpy.ops.mesh.primitive_cone_add(vertices=64, radius1=2.3, radius2=1.55, depth=15, location=(0, 0, BASE + 7.5))
tower = bpy.context.object
tower.data.materials.append(paint)
bv = tower.modifiers.new("b", "BEVEL"); bv.width = 0.04; bv.segments = 2
bpy.ops.object.shade_smooth()
TOP = BASE + 15
bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=2.25, depth=0.25, location=(0, 0, TOP + 0.1))
bpy.context.object.data.materials.append(metal)
# railing: posts + two rails
for i in range(36):
    a = i / 36 * 2 * math.pi
    bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.025, depth=1.05, location=(math.cos(a) * 2.15, math.sin(a) * 2.15, TOP + 0.75))
    bpy.context.object.data.materials.append(metal)
for zz in (TOP + 0.75, TOP + 1.25):
    bpy.ops.mesh.primitive_torus_add(major_radius=2.15, minor_radius=0.03, major_segments=96, minor_segments=8, location=(0, 0, zz))
    bpy.context.object.data.materials.append(metal)
# lantern room
bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=1.25, depth=0.7, location=(0, 0, TOP + 0.55))
bpy.context.object.data.materials.append(metal)
bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=1.2, depth=2.2, location=(0, 0, TOP + 2.0))
bpy.context.object.data.materials.append(glass)
for i in range(12):
    a = (i + 0.5) / 12 * 2 * math.pi
    bpy.ops.mesh.primitive_cube_add(size=1, location=(math.cos(a) * 1.18, math.sin(a) * 1.18, TOP + 2.0))
    o = bpy.context.object; o.scale = (0.05, 0.05, 2.25); o.rotation_euler[2] = a
    o.data.materials.append(metal)
bpy.ops.mesh.primitive_cone_add(vertices=12, radius1=1.45, radius2=0.15, depth=1.3, location=(0, 0, TOP + 3.75))
bpy.context.object.data.materials.append(metal)
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.22, location=(0, 0, TOP + 4.55))
bpy.context.object.data.materials.append(metal)
# Fresnel lens: stacked prism rings around the lamp
for k in range(-6, 7):
    zz = TOP + 1.95 + k * 0.1
    rr = 0.62 - abs(k) * 0.035
    bpy.ops.mesh.primitive_torus_add(major_radius=rr, minor_radius=0.05, major_segments=48, minor_segments=10, location=(0, 0, zz))
    bpy.context.object.data.materials.append(glass)
# the lamp and its turning beam
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.16, location=(0, 0, TOP + 1.95))
bpy.context.object.data.materials.append(lamp_m)
bpy.ops.object.empty_add(location=(0, 0, TOP + 1.95))
rig = bpy.context.object; rig.name = "BeamRig"
for side in (0, math.pi):
    bpy.ops.object.light_add(type="SPOT", location=(0, 0, TOP + 1.95))
    sp = bpy.context.object
    sp.data.energy = 200000; sp.data.color = (1.0, 0.82, 0.55)
    sp.data.spot_size = math.radians(9); sp.data.spot_blend = 0.4; sp.data.shadow_soft_size = 0.2
    sp.rotation_euler = (math.radians(90), 0, side)
    sp.parent = rig
    if EP == 3:     # morning: the keeper switches the light off at 8.5 s
        for f, e in ((1, 200000), (int(8.5 * FPS), 200000), (int(9.0 * FPS), 0)):
            sp.data.energy = e; sp.data.keyframe_insert("energy", frame=f)
if EP == 3:
    for f, e in ((1, 60), (int(8.5 * FPS), 60), (int(9.0 * FPS), 0.3)):
        lb.inputs["Emission Strength"].default_value = e; lb.inputs["Emission Strength"].keyframe_insert("default_value", frame=f)
rig.rotation_euler[2] = 0
rig.keyframe_insert("rotation_euler", index=2, frame=1)
rig.rotation_euler[2] = -2 * math.pi * DUR / FPS / 8   # one turn per 8 s
rig.keyframe_insert("rotation_euler", index=2, frame=DUR)
# keeper's cottage
bpy.ops.mesh.primitive_cube_add(size=1, location=(4.2, 1.2, BASE + 1.2))
hut = bpy.context.object; hut.scale = (4, 3, 2.6); hut.data.materials.append(paint)
bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=2.9, radius2=0, depth=1.6, location=(4.2, 1.2, BASE + 3.3))
roof = bpy.context.object; roof.rotation_euler[2] = math.radians(45); roof.scale = (1.45, 1.1, 1)
roof.data.materials.append(metal)
DOOR_OPEN = int(12.0 * FPS)
if EP == 3:
    # hollow cottage with a doorway, a door that swings open onto a lit room, a concrete landing and an iron rail
    so = hut.modifiers.new("walls", "SOLIDIFY"); so.thickness = 0.06; so.offset = -1      # scaled cube: ~0.2 m walls
    bpy.ops.mesh.primitive_cube_add(size=1, location=(4.2, -0.3, BASE + 0.9))
    cut = bpy.context.object; cut.scale = (1.0, 0.9, 2.0); cut.hide_render = True; cut.hide_viewport = True
    bo = hut.modifiers.new("doorway", "BOOLEAN"); bo.object = cut; bo.operation = "DIFFERENCE"
    wood, n, l = mat("DoorWood")
    dbs = n["Principled BSDF"]; dbs.inputs["Base Color"].default_value = (0.025, 0.06, 0.045, 1); dbs.inputs["Roughness"].default_value = 0.55
    bpy.ops.object.empty_add(location=(3.72, -0.32, BASE - 0.08)); hinge = bpy.context.object; hinge.name = "DoorHinge"
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0.48, 0, 0.99)); door = bpy.context.object
    door.scale = (0.95, 0.05, 1.96); door.parent = hinge; door.data.materials.append(wood)
    hinge.rotation_euler[2] = 0; hinge.keyframe_insert("rotation_euler", index=2, frame=DOOR_OPEN)
    hinge.rotation_euler[2] = math.radians(-105); hinge.keyframe_insert("rotation_euler", index=2, frame=DOOR_OPEN + 20)
    bpy.ops.object.light_add(type="POINT", location=(4.2, 1.3, BASE + 1.9)); rl = bpy.context.object
    rl.data.energy = 90; rl.data.color = (1.0, 0.7, 0.42); rl.data.shadow_soft_size = 0.4
    conc, n, l = mat("Concrete")
    cb = n["Principled BSDF"]; ctc = n.new("ShaderNodeTexCoord")
    cn = n.new("ShaderNodeTexNoise"); cn.inputs["Scale"].default_value = 1.4; cn.inputs["Detail"].default_value = 12
    l.new(ctc.outputs["Object"], cn.inputs["Vector"])
    cr = n.new("ShaderNodeValToRGB"); cr.color_ramp.elements[0].color = (0.07, 0.07, 0.068, 1); cr.color_ramp.elements[1].color = (0.24, 0.235, 0.22, 1)
    l.new(cn.outputs["Fac"], cr.inputs[0]); l.new(cr.outputs[0], cb.inputs["Base Color"])
    crr = n.new("ShaderNodeMapRange"); crr.inputs["From Min"].default_value = 0.38; crr.inputs["From Max"].default_value = 0.46
    crr.inputs["To Min"].default_value = 0.03; crr.inputs["To Max"].default_value = 0.6     # puddles in the low spots
    l.new(cn.outputs["Fac"], crr.inputs["Value"]); l.new(crr.outputs["Result"], cb.inputs["Roughness"])
    cg = n.new("ShaderNodeNewGeometry"); cz = n.new("ShaderNodeSeparateXYZ"); l.new(cg.outputs["Position"], cz.inputs[0])
    cw = n.new("ShaderNodeMapRange"); cw.inputs["From Min"].default_value = 1.4; cw.inputs["From Max"].default_value = 0.3
    l.new(cz.outputs["Z"], cw.inputs["Value"])
    calg = n.new("ShaderNodeMix"); calg.data_type = "RGBA"; l.new(cw.outputs["Result"], calg.inputs["Factor"])
    l.new(cr.outputs[0], calg.inputs["A"]); calg.inputs["B"].default_value = (0.012, 0.02, 0.012, 1)
    l.new(calg.outputs["Result"], cb.inputs["Base Color"])
    cbm = n.new("ShaderNodeBump"); cbm.inputs["Strength"].default_value = 0.2
    l.new(cn.outputs["Fac"], cbm.inputs["Height"]); l.new(cbm.outputs[0], cb.inputs["Normal"])
    G3 = BASE - 0.08
    LX0, LX1, LY0, LY1, LZ0 = -3.4, 7.5, -6.5, 3.3, -1.6
    bpy.ops.mesh.primitive_cube_add(size=1, location=((LX0 + LX1) / 2, (LY0 + LY1) / 2, (G3 + LZ0) / 2))
    apron = bpy.context.object; apron.name = "Base"
    apron.scale = (LX1 - LX0, LY1 - LY0, G3 - LZ0); apron.data.materials.append(conc)
    for o in list(bpy.data.objects):
        if o.type == "MESH" and o.data.materials and o.data.materials[0] == rock_m:
            bb = [o.matrix_world @ Vector(c) for c in o.bound_box]
            if min(v.x for v in bb) < LX1 + 1.2 and max(v.x for v in bb) > LX0 - 1.2 and min(v.y for v in bb) < LY1 + 1.2 and max(v.y for v in bb) > LY0 - 1.2:
                bpy.data.objects.remove(o)
    # rock armour piled on the far (north and west) sides - the wide shots keep the rocky island; the close cameras look
    # south and east, over clean concrete
    rr_ = random.Random(33)
    for i in range(16):
        a = math.radians(rr_.uniform(75, 255)); r = rr_.uniform(8.2, 12.5)
        x, y = 2.05 + math.cos(a) * r, -1.6 + math.sin(a) * r
        sz = rr_.uniform(1.0, 2.4)
        boulder((x, y, rr_.uniform(-0.5, 0.3)), (sz * rr_.uniform(.8, 1.3), sz * rr_.uniform(.8, 1.3), sz * rr_.uniform(.5, .85)), a)
    bv2 = apron.modifiers.new("b", "BEVEL"); bv2.width = 0.04; bv2.segments = 2
    railm, n, l = mat("RailPaint")
    rb2 = n["Principled BSDF"]; rb2.inputs["Base Color"].default_value = (0.62, 0.62, 0.6, 1); rb2.inputs["Roughness"].default_value = 0.45
    RAIL_Y = -6.2
    for i in range(8):
        bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.028, depth=1.08, location=(-1.2 + i * 1.2, RAIL_Y, G3 + 0.54))
        bpy.context.object.data.materials.append(railm)
    for zz in (0.55, 1.06):
        bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.024, depth=8.5, location=(3.0, RAIL_Y, G3 + zz))
        o = bpy.context.object; o.rotation_euler[1] = math.radians(90); o.data.materials.append(railm)
    RAIL_X = 7.2
    for i in range(5):
        bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.028, depth=1.08, location=(RAIL_X, RAIL_Y + i * 1.2, G3 + 0.54))
        bpy.context.object.data.materials.append(railm)
    for zz in (0.55, 1.06):
        bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.024, depth=4.8, location=(RAIL_X, RAIL_Y + 2.4, G3 + zz))
        o = bpy.context.object; o.rotation_euler[0] = math.radians(90); o.data.materials.append(railm)
win_m, n, l = mat("Window")
wb = n["Principled BSDF"]; wb.inputs["Emission Color"].default_value = (1.0, 0.62, 0.3, 1); wb.inputs["Emission Strength"].default_value = {1: 6, 2: 14, 3: 3}[EP]
wb.inputs["Base Color"].default_value = (0.05, 0.04, 0.03, 1)
if EP == 3:
    wb.inputs["Emission Strength"].default_value = 0.04; wb.inputs["Roughness"].default_value = 0.02
    wb.inputs["Base Color"].default_value = (0.02, 0.022, 0.025, 1)
for x in (3.2, 5.2):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, -0.31, BASE + 1.3))
    o = bpy.context.object; o.scale = (0.6, 0.04, 0.8); o.data.materials.append(win_m)

# ---------- air: light haze so the beam reads ----------
haze, n, l = mat("Haze")
n.clear()
pv = n.new("ShaderNodeVolumePrincipled"); pv.inputs["Density"].default_value = {1: 0.0011, 2: 0.003, 3: 0.0014}[EP]
pv.inputs["Color"].default_value = (0.8, 0.85, 0.95, 1); pv.inputs["Anisotropy"].default_value = 0.6
vo = n.new("ShaderNodeOutputMaterial"); link(l, pv.outputs[0], vo.inputs["Volume"])
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 40))
hz = bpy.context.object; hz.name = "Haze"; hz.scale = (700, 700, 90); hz.data.materials.append(haze)
hz.visible_shadow = False

# ---------- cameras (4 shots, switched by markers) ----------
def cam(name, lens, keys, target=None, fstop=None, focus=None):
    cd = bpy.data.cameras.new(name); cd.lens = lens; cd.clip_end = 30000
    if fstop:
        cd.dof.use_dof = True; cd.dof.aperture_fstop = fstop; cd.dof.focus_distance = focus
    c = bpy.data.objects.new(name, cd); sc.collection.objects.link(c)
    for f, loc in keys:
        c.location = loc; c.keyframe_insert("location", frame=f)
    if target:
        t = bpy.data.objects.new(name + "_T", None); sc.collection.objects.link(t)
        for f, loc in target:
            t.location = loc; t.keyframe_insert("location", frame=f)
        tr = c.constraints.new("TRACK_TO"); tr.target = t; tr.track_axis = "TRACK_NEGATIVE_Z"; tr.up_axis = "UP_Y"
    return c


S = [1, 11 * FPS, 22 * FPS, 32 * FPS]
if EP == 1:
    c1 = cam("Shot1_Approach", 32, [(S[0], (6, -140, 1.6)), (S[1] + 6, (4, -85, 2.4))],
             target=[(S[0], (0, 0, 12)), (S[1] + 6, (0, 0, 13))])
    c2 = cam("Shot2_Orbit", 28, [(S[1] - 6, (-50, -30, 8)), (S[2] + 6, (-36, 38, 15))],
             target=[(S[1] - 6, (0, 0, 11)), (S[2] + 6, (0, 0, 12))])
    c3 = cam("Shot3_Lantern", 70, [(S[2] - 6, (9, -10, TOP + 1.5)), (S[3] + 6, (6.5, -11.5, TOP + 2.6))],
             target=[(S[2] - 6, (0, 0, TOP + 1.9)), (S[3] + 6, (0, 0, TOP + 2.1))], fstop=2.8, focus=14)
    c4 = cam("Shot4_Rise", 24, [(S[3] - 6, (10, -40, 4)), (DUR, (18, -95, 38))],
             target=[(S[3] - 6, (0, 0, 10)), (DUR, (0, 20, 6))])
elif EP == 3:
    KX0, KY0, KX1, KY1 = 4.25, 1.0, 3.5, -5.75          # the keeper: inside the door -> at the rail
    c1 = cam("Shot1_After", 30, [(S[0], (-24, -118, 5)), (S[1] + 6, (-16, -78, 7))],
             target=[(S[0], (0, 0, 12)), (S[1] + 6, (0, 0, 13))])
    c2 = cam("Shot2_Door", 30, [(S[1] - 6, (0.2, -4.9, G3 + 1.65)), (S[2] + 6, (0.7, -5.3, G3 + 1.6))],
             target=[(S[1] - 6, (4.2, -0.3, G3 + 1.25)), (int(12.5 * FPS), (4.2, -0.4, G3 + 1.25)),
                     (int(17.3 * FPS), (3.6, -5.4, G3 + 1.2)), (S[2] + 6, (3.4, -6.2, G3 + 1.1))])
    c3 = cam("Shot3_Rail", 40, [(S[2] - 6, (2.5, -3.7, G3 + 1.72)), (S[3] + 6, (5.4, -5.0, G3 + 1.62))],
             target=[(S[2] - 6, (4.4, -7.75, G3 + 1.3)), (S[3] + 6, (3.45, -5.95, G3 + 1.5))], fstop=2.8, focus=2.2)
    c4 = cam("Shot4_Away", 26, [(S[3] - 6, (9, -13, G3 + 2.4)), (DUR, (24, -62, 32))],
             target=[(S[3] - 6, (3.5, -5.8, G3 + 1.2)), (DUR, (0, 0, 9))])
else:
    # Storm Night: 1) out on the heaving sea, the far flash shows the tower; 2) along the surf as waves break on the rocks;
    # 3) up at the gallery, rain streaming through the turning beam; 4) the keeper's lit window, then a close strike and the
    # rise off the island.
    c1 = cam("Shot1_Sea", 35, [(S[0], (16, -112, 6.5)), (S[1] + 6, (10, -74, 7.5))],
             target=[(S[0], (0, 0, 13)), (S[1] + 6, (0, 0, 14))])
    c2 = cam("Shot2_Surf", 28, [(S[1] - 6, (-36, -26, 7)), (S[2] + 6, (-31, 24, 10))],
             target=[(S[1] - 6, (0, 0, 8)), (S[2] + 6, (0, 0, 10))])
    c3 = cam("Shot3_Gallery", 55, [(S[2] - 6, (8, -9.5, TOP + 0.6)), (S[3] + 6, (6.2, -11, TOP + 1.8))],
             target=[(S[2] - 6, (0, 0, TOP + 2.0)), (S[3] + 6, (0, 0, TOP + 2.2))], fstop=2.8, focus=12.5)
    c4 = cam("Shot4_Window", 26, [(S[3] - 6, (9, -12, BASE + 2.2)), (DUR, (26, -78, 30))],
             target=[(S[3] - 6, (4.2, 0.6, BASE + 1.6)), (S[3] + 5 * FPS, (2, 0, 9)), (DUR, (0, 0, 12))])
for i, c in enumerate((c1, c2, c3, c4)):
    mk = sc.timeline_markers.new(f"shot{i + 1}", frame=S[i]); mk.camera = c
sc.camera = c1


def ease_all():
    for ob in bpy.data.objects:
        ad = ob.animation_data
        if not ad or not ad.action:
            continue
        act = ad.action
        curves = getattr(act, "fcurves", None)
        if curves is None:
            try:
                curves = [fc for layer in act.layers for strip in layer.strips for bag in strip.channelbags for fc in bag.fcurves]
            except Exception:
                curves = []
        for fc in curves:
            for k in fc.keyframe_points:
                k.interpolation = "LINEAR" if ob.name in ("BeamRig", "Ocean") else "SINE"
                k.easing = "EASE_IN_OUT"


ease_all()


# ---------- ep.2 storm: rain, lightning, moonlight (after ease_all: these keys must stay linear / stepped) ----------
if EP == 3:
    # Walter from the Loft people (a MetaHuman preset) as the keeper: navy wool jumper, dark work trousers, black boots.
    # Walk slowed to an old man's pace (x0.75 -> ~1.4 m/s), then his idle at the rail.
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath="C:/Users/lilli/Projects/heartbeat-observatory/homes/people/walter.glb")
    for o in [o for o in bpy.data.objects if o not in before and o.name.startswith("Icosphere")]:
        bpy.data.objects.remove(o)
    keeper = next(o for o in bpy.data.objects if o.type == "ARMATURE" and o not in before)
    keeper.name = "Keeper"
    for mn, c in (("Shirt", (0.022, 0.03, 0.055)), ("Shorts", (0.03, 0.03, 0.032)), ("Pants", (0.03, 0.03, 0.032)), ("Shoes", (0.012, 0.011, 0.01))):
        m = bpy.data.materials.get(mn)
        b = m and next((x for x in m.node_tree.nodes if x.type == "BSDF_PRINCIPLED"), None)
        if b and not b.inputs["Base Color"].is_linked:
            b.inputs["Base Color"].default_value = c + (1,); b.inputs["Roughness"].default_value = 0.8
    ad = keeper.animation_data
    for t in list(ad.nla_tracks):
        ad.nla_tracks.remove(t)
    ad.action = None
    walk_a, idle_a = bpy.data.actions["Walk"], bpy.data.actions["Idle"]
    W0, W1 = int(12.5 * FPS), int(17.3 * FPS)
    tw = ad.nla_tracks.new(); sw = tw.strips.new("walk", W0, walk_a); sw.scale = 1.33
    ti = ad.nla_tracks.new(); si = ti.strips.new("idle", W1 - 4, idle_a); si.extrapolation = "NOTHING"
    si.blend_in = 14; si.repeat = math.ceil((DUR - W1 + 20) / (idle_a.frame_range[1] - idle_a.frame_range[0]))
    for st, a in ((sw, walk_a), (si, idle_a)):
        try:
            st.action_slot = a.slots[0]
        except Exception as e:
            print("slot", e)
    head = math.atan2(-(KX1 - KX0), -(KY1 - KY0))
    keeper.rotation_euler = (0, 0, -head)
    keeper.location = (KX0, KY0, G3); keeper.keyframe_insert("location", frame=W0)
    keeper.location = (KX1, KY1, G3); keeper.keyframe_insert("location", frame=W1)
    set_interp(keeper, "LINEAR")

if EP == 2:
    rain_m, n, l = mat("Rain")
    rbsdf = n["Principled BSDF"]
    rbsdf.inputs["Base Color"].default_value = (0.78, 0.82, 0.88, 1); rbsdf.inputs["Roughness"].default_value = 0.25
    rbsdf.inputs["Alpha"].default_value = 0.4
    try:
        rain_m.surface_render_method = "BLENDED"
    except Exception:
        pass
    FALL, SLANT = 9.0, 0.25          # m/s down; sideways drift per metre of fall (the gale leans the rain)

    def seg_dist(px, py, a, b):
        ax, ay = a; bx, by = b; dx, dy = bx - ax, by - ay
        t = max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / max(dx * dx + dy * dy, 1e-9)))
        return math.hypot(px - ax - t * dx, py - ay - t * dy)

    def rain_box(name, center, size, count, seed, clear=None, R=4.0):
        # crossed thin quads, stacked twice and slid down one box-height per cycle -> endless, seamless rain.
        # clear = the camera's path (x,y)->(x,y): no drops within R of the lens (they read as giant lines)
        rnd = random.Random(seed)
        sx, sy, H = size
        verts, faces = [], []
        W = 0.008
        for i in range(count):
            x = rnd.uniform(-sx / 2, sx / 2); y = rnd.uniform(-sy / 2, sy / 2); z = rnd.uniform(0, H)
            if clear and min(seg_dist(center[0] + x - s_, center[1] + y, *clear) for s_ in (0, SLANT * H / 2, SLANT * H,
                                                                                            -SLANT * H / 2)) < R:
                continue
            ln = 0.5 * rnd.uniform(0.7, 1.3); dx = SLANT * ln; b = len(verts)
            verts += [(x - W, y, z), (x + W, y, z), (x + W + dx, y, z + ln), (x - W + dx, y, z + ln),
                      (x, y - W, z), (x, y + W, z), (x + dx, y + W, z + ln), (x + dx, y - W, z + ln)]
            faces += [(b, b + 1, b + 2, b + 3), (b + 4, b + 5, b + 6, b + 7)]
        me = bpy.data.meshes.new(name); me.from_pydata(verts, [], faces); me.update(); me.materials.append(rain_m)
        per = H / FALL * FPS
        for j in (0, 1):
            o = bpy.data.objects.new(f"{name}_{j}", me); sc.collection.objects.link(o)
            o.visible_shadow = False
            try:
                o.cycles.use_motion_blur = False    # the streak is the blur; a cycle snap must not smear
            except Exception:
                pass
            bx, by, bz = center[0] + j * SLANT * H, center[1], center[2] + j * H
            o.location = (bx, by, bz); o.keyframe_insert("location", frame=0)
            o.location = (bx - SLANT * H, by, bz - H); o.keyframe_insert("location", frame=per)
            for fc in curves_of(o):
                for k in fc.keyframe_points:
                    k.interpolation = "LINEAR"
                fc.modifiers.new("CYCLES")
    rain_box("RainIsland", (0, 0, -2), (80, 80, 36), 60000, 11)
    rain_box("RainSea", (13, -88, -2), (34, 56, 18), 30000, 12, clear=((16, -112), (10, -74)))
    rain_box("RainSurf", (-34, 0, -2), (30, 66, 20), 32000, 13, clear=((-36, -26), (-31, 24)))
    rain_box("RainGallery", (7, -10, TOP - 6), (14, 14, 14), 14000, 14, clear=((8, -9.5), (6.2, -11)), R=2.5)
    rain_box("RainRise", (19, -50, -2), (32, 70, 38), 40000, 15, clear=((9, -12), (26, -78)))

    # moonlight barely through the cloud: just enough to find the wave tops
    bpy.ops.object.light_add(type="SUN"); moon = bpy.context.object
    moon.data.energy = 0.1; moon.data.color = (0.55, 0.65, 1.0); moon.data.angle = math.radians(4)
    moon.rotation_euler = (math.radians(62), 0, math.radians(160))
    # lightning: a big soft sun from behind the island + the whole sky brightening, stepped keys
    bpy.ops.object.light_add(type="SUN"); zap = bpy.context.object
    zap.data.color = (0.78, 0.84, 1.0); zap.data.angle = math.radians(12)
    zap.rotation_euler = (math.radians(55), 0, math.radians(200))

    def bolt(name, base, seed, height=520):
        rnd = random.Random(seed)
        cu = bpy.data.curves.new(name, "CURVE"); cu.dimensions = "3D"; cu.bevel_depth = 1.6; cu.bevel_resolution = 1
        def strand(x, y, z, zend, step):
            pts = [(x, y, z)]
            while z > zend:
                z -= step * rnd.uniform(0.6, 1.3); x += rnd.uniform(-0.45, 0.45) * step; y += rnd.uniform(-0.3, 0.3) * step
                pts.append((x, y, max(z, zend)))
            sp = cu.splines.new("POLY"); sp.points.add(len(pts) - 1)
            for p, q in zip(sp.points, pts):
                p.co = (q[0], q[1], q[2], 1)
            return pts
        main = strand(base[0], base[1], height, -2, 28)
        for bi in (3, 7, 11):
            if bi < len(main):
                bx, by, bz = main[bi]
                strand(bx, by, bz, bz - rnd.uniform(60, 140), 16)
        bm_, bn, bl = mat(name + "Glow"); bn.clear()
        em = bn.new("ShaderNodeEmission"); em.inputs["Color"].default_value = (0.8, 0.86, 1.0, 1); em.inputs["Strength"].default_value = 0
        bo = bn.new("ShaderNodeOutputMaterial"); bl.new(em.outputs[0], bo.inputs["Surface"])
        cu.materials.append(bm_)
        ob = bpy.data.objects.new(name, cu); sc.collection.objects.link(ob); ob.visible_shadow = False
        ob.hide_render = True; ob.keyframe_insert("hide_render", frame=0)
        return em.inputs["Strength"], bm_, ob

    far_bolt, far_bm, far_ob = bolt("BoltFar", (-420, 1000), 21)
    near_bolt, near_bm, near_ob = bolt("BoltNear", (-230, 520), 22)
    # (seconds, size, which bolt shows); the thunder in the soundtrack is timed from this same list
    FLASHES = [(3.1, 1.0, "far"), (14.6, 0.6, None), (24.2, 0.75, None), (35.4, 1.35, "near")]
    SHAPE = [(-1, 0), (0, 1), (1, 0.25), (2, 0.85), (3, 0.4), (5, 0.12), (8, 0)]
    bg_s = STORM_BG.inputs["Strength"]
    for sock in (bg_s, far_bolt, near_bolt):
        sock.keyframe_insert("default_value", frame=0)
    zap.data.energy = 0; zap.data.keyframe_insert("energy", frame=0)
    for t, amp, which in FLASHES:
        f0 = int(round(t * FPS))
        for off, lv in SHAPE:
            f = f0 + off
            bg_s.default_value = 1 + 3.2 * amp * lv; bg_s.keyframe_insert("default_value", frame=f)
            zap.data.energy = 1.5 * amp * lv; zap.data.keyframe_insert("energy", frame=f)
            for key, sock, bob in (("far", far_bolt, far_ob), ("near", near_bolt, near_ob)):
                sock.default_value = 900 * lv if which == key else 0; sock.keyframe_insert("default_value", frame=f)
                bob.hide_render = not (which == key and lv > 0.2); bob.keyframe_insert("hide_render", frame=f)
    for idb in (sc.world.node_tree, zap.data, far_bm.node_tree, near_bm.node_tree, far_ob, near_ob):
        set_interp(idb, "CONSTANT")

sc.render.image_settings.file_format = "PNG"
sc.render.use_overwrite = False
sc.render.use_placeholder = True
if "--save" in argv:
    bpy.ops.wm.save_as_mainfile(filepath=argv[argv.index("--save") + 1])
if "--still" in argv:
    i = argv.index("--still")
    for fr in argv[i + 1].split(","):          # one frame, or several: 60,380,640 -> OUT_0060.png ...
        sc.frame_set(int(fr))
        sc.render.filepath = argv[i + 2] if "," not in argv[i + 1] else argv[i + 2].replace(".png", f"_{int(fr):04d}.png")
        bpy.ops.render.render(write_still=True)
if "--anim" in argv:
    # resumable: finished frames are skipped (use_overwrite False + placeholders)
    sc.render.filepath = argv[argv.index("--anim") + 1].rstrip("/\\") + "/f_####"
    bpy.ops.render.render(animation=True)
print("BUILD OK")
