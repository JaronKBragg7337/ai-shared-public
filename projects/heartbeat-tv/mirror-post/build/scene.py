# Blender script: the mirror shot.  Opens build/person.blend, builds room + mirror + lights, renders passes.
#   blender -b build/person.blend --python build/scene.py -- <port|land> <scale%> <samples> <passes e.g. H,A,E,M> [png]
# The mirror is built the exact way a flat mirror works: an opening in the wall onto a mirrored copy of the room,
# the person and the lights.  The copy is the reflection, so it can change while the real person stays human.
# Passes (same camera, same geometry, only the reflection's surface changes; blended later in comp.py):
#   H = human reflection      A = AI reflection, glow off      E = AI glow only (lights off)      M = transition map
import bpy, sys, os, math
import numpy as np
from mathutils import Vector, Matrix
from bpy_extras.object_utils import world_to_camera_view

argv = sys.argv[sys.argv.index('--') + 1:]
FMT = argv[0]; SCALE = int(argv[1]); SAMPLES = int(argv[2]); PASSES = argv[3].split(','); PNG = len(argv) > 4 and argv[4] == 'png'
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'passes'); os.makedirs(OUT, exist_ok=True)
sc = bpy.context.scene
MY = -0.45                                    # mirror plane
REFL = Matrix.Translation((0, 2 * MY, 0)) @ Matrix.Diagonal((1, -1, 1, 1))
def mir(p): return Vector((p[0], 2 * MY - p[1], p[2]))
GOLD = (1.0, 0.58, 0.15, 1)

person = bpy.data.objects['Person']; eyes = bpy.data.objects['P_eyes']; shirt = bpy.data.objects['P_shirt']
brows = bpy.data.objects['P_brows']; lashes = bpy.data.objects['P_lashes']; rig = bpy.data.objects['Rig']
for n in ('P_hair', 'P_teeth'):
    bpy.data.objects.remove(bpy.data.objects[n], do_unlink=True)
bpy.context.view_layer.update()

def bbox_center(vs):
    a = np.array(vs); return Vector(((a.min(0) + a.max(0)) / 2).tolist())
ev = [eyes.matrix_world @ v.co for v in eyes.data.vertices]
cL = bbox_center([p for p in ev if p.x < 0]); cR = bbox_center([p for p in ev if p.x > 0])
EYE_MID = (cL + cR) / 2
VFACE = mir(EYE_MID)                           # where the reflected face is

# ---------------------------------------------------------------- camera
CAMS = {
    'port': dict(loc=(0.34, 0.95, 1.70), aim=(0.035, -0.767, 1.585), lens=64, res=(1210, 2150)),
    'land': dict(loc=(0.40, 0.98, 1.69), aim=(0.125, -0.767, 1.615), lens=58, res=(2150, 1210)),
}
C = CAMS[FMT]
cam = bpy.data.objects.new('Cam', bpy.data.cameras.new('Cam')); sc.collection.objects.link(cam); sc.camera = cam
cam.location = C['loc']; cam.data.lens = C['lens']; cam.data.sensor_width = 36
aim = bpy.data.objects.new('Aim', None); sc.collection.objects.link(aim); aim.location = C['aim']
tc = cam.constraints.new('TRACK_TO'); tc.target = aim; tc.track_axis = 'TRACK_NEGATIVE_Z'; tc.up_axis = 'UP_Y'
cam.data.dof.use_dof = True; cam.data.dof.focus_distance = (Vector(C['loc']) - VFACE).length
cam.data.dof.aperture_fstop = 2.2; cam.data.dof.aperture_blades = 9
sc.render.resolution_x, sc.render.resolution_y = C['res']; sc.render.resolution_percentage = SCALE

# the person looks at the camera through the mirror (each eyeball turns about its own centre)
cam_img = mir(C['loc'])
inv = eyes.matrix_world.inverted()
iris = eyes.data.attributes.new('irisr', 'FLOAT', 'POINT')
for c in (cL, cR):
    d = (cam_img - c).normalized()
    rot = Vector((0, -1, 0)).rotation_difference(d).to_matrix()
    for v in eyes.data.vertices:
        p = eyes.matrix_world @ v.co
        if (p.x < 0) == (c.x < 0):
            q = c + rot @ (p - c)
            v.co = inv @ q
            r = q - c; along = r.dot(d); rad = (r - along * d).length
            iris.data[v.index].value = rad if along > 0 else 1.0

# ---------------------------------------------------------------- node helpers
def newmat(name):
    m = bpy.data.materials.new(name); m.use_nodes = True; m.node_tree.nodes.clear(); return m, m.node_tree
def N(t, typ, **kw):
    n = t.nodes.new(typ)
    for k, v in kw.items():
        if k == 'ins':
            for kk, vv in v.items(): n.inputs[kk].default_value = vv
        else: setattr(n, k, v)
    return n
def L(t, a, b): t.links.new(a, b)
def val(t, name, v=0.0):
    n = t.nodes.new('ShaderNodeValue'); n.name = name; n.label = name; n.outputs[0].default_value = v; return n
def math_(t, op, a, b=None):
    n = t.nodes.new('ShaderNodeMath'); n.operation = op
    for i, x in enumerate((a, b)):
        if x is None: continue
        if hasattr(x, 'is_output'): L(t, x, n.inputs[i])
        else: n.inputs[i].default_value = x
    return n.outputs[0]
def modal_out(t, human, ai, tm):
    """reflection surface: human / AI / transition map, chosen by the mode values"""
    ai_mix = val(t, 'ai_mix'); mask_on = val(t, 'mask_on')
    m1 = N(t, 'ShaderNodeMixShader'); L(t, ai_mix.outputs[0], m1.inputs[0]); L(t, human, m1.inputs[1]); L(t, ai, m1.inputs[2])
    em = N(t, 'ShaderNodeEmission'); cmb = N(t, 'ShaderNodeCombineColor'); cmb.inputs[1].default_value = 1.0; cmb.inputs[2].default_value = 0.0
    if tm is not None: L(t, tm, cmb.inputs[0])
    L(t, cmb.outputs[0], em.inputs['Color'])
    m2 = N(t, 'ShaderNodeMixShader'); L(t, mask_on.outputs[0], m2.inputs[0]); L(t, m1.outputs[0], m2.inputs[1]); L(t, em.outputs[0], m2.inputs[2])
    out = N(t, 'ShaderNodeOutputMaterial'); L(t, m2.outputs[0], out.inputs['Surface'])

skin_img = bpy.data.images['young_lightskinned_male_diffuse.png']
def skin_shader(t):
    tex = N(t, 'ShaderNodeTexImage', image=skin_img)
    tint = N(t, 'ShaderNodeMix', data_type='RGBA', blend_type='MULTIPLY'); tint.inputs[0].default_value = 1.0
    L(t, tex.outputs['Color'], tint.inputs[6]); tint.inputs[7].default_value = (0.86, 0.72, 0.62, 1)
    geo = N(t, 'ShaderNodeNewGeometry')
    pore = N(t, 'ShaderNodeTexNoise', ins={'Scale': 1500.0, 'Detail': 2.0}); L(t, geo.outputs['Position'], pore.inputs['Vector'])
    mid = N(t, 'ShaderNodeTexNoise', ins={'Scale': 260.0, 'Detail': 3.0}); L(t, geo.outputs['Position'], mid.inputs['Vector'])
    b1 = N(t, 'ShaderNodeBump', ins={'Strength': 0.25, 'Distance': 0.0004}); L(t, pore.outputs['Fac'], b1.inputs['Height'])
    b2 = N(t, 'ShaderNodeBump', ins={'Strength': 0.14, 'Distance': 0.0012}); L(t, mid.outputs['Fac'], b2.inputs['Height']); L(t, b1.outputs[0], b2.inputs['Normal'])
    rough = N(t, 'ShaderNodeMapRange', ins={'To Min': 0.34, 'To Max': 0.50}); L(t, mid.outputs['Fac'], rough.inputs['Value'])
    sk = N(t, 'ShaderNodeBsdfPrincipled', ins={'Subsurface Weight': 1.0, 'Subsurface Scale': 0.003, 'Specular IOR Level': 0.5})
    sk.inputs['Subsurface Radius'].default_value = (1.0, 0.36, 0.2)
    L(t, tint.outputs[2], sk.inputs['Base Color']); L(t, rough.outputs[0], sk.inputs['Roughness']); L(t, b2.outputs[0], sk.inputs['Normal'])
    return sk.outputs[0]

def ai_shader(t, centre):
    """satin dark metal; fine gold contour lines (a machine's depth map of the same face)"""
    geo = N(t, 'ShaderNodeNewGeometry')
    sep = N(t, 'ShaderNodeSeparateXYZ'); L(t, geo.outputs['Position'], sep.inputs[0])
    wob = N(t, 'ShaderNodeTexNoise', ins={'Scale': 9.0, 'Detail': 1.0}); L(t, geo.outputs['Position'], wob.inputs['Vector'])
    depth = math_(t, 'ADD', sep.outputs['Y'], math_(t, 'MULTIPLY', math_(t, 'SUBTRACT', wob.outputs['Fac'], 0.5), 0.004))
    fr = math_(t, 'FRACT', math_(t, 'MULTIPLY', depth, 1 / 0.0052))
    tri = math_(t, 'ABSOLUTE', math_(t, 'SUBTRACT', fr, 0.5))                    # 0.5 at a line, 0 between
    line = N(t, 'ShaderNodeMapRange', interpolation_type='SMOOTHSTEP', ins={'From Min': 0.40, 'From Max': 0.5}); L(t, tri, line.inputs['Value'])
    seg = N(t, 'ShaderNodeTexNoise', ins={'Scale': 30.0, 'Detail': 2.0}); L(t, geo.outputs['Position'], seg.inputs['Vector'])
    segm = N(t, 'ShaderNodeMapRange', ins={'From Min': 0.35, 'From Max': 0.7, 'To Min': 0.25, 'To Max': 1.0}); L(t, seg.outputs['Fac'], segm.inputs['Value'])
    grain = N(t, 'ShaderNodeTexNoise', ins={'Scale': 500.0, 'Detail': 2.0}); L(t, geo.outputs['Position'], grain.inputs['Vector'])
    rough = N(t, 'ShaderNodeMapRange', ins={'To Min': 0.26, 'To Max': 0.40}); L(t, grain.outputs['Fac'], rough.inputs['Value'])
    bp = N(t, 'ShaderNodeBump', ins={'Strength': 0.35, 'Distance': 0.0003}); L(t, line.outputs[0], bp.inputs['Height']); bp.invert = True
    emit_on = val(t, 'emit_on')
    ai = N(t, 'ShaderNodeBsdfPrincipled', ins={'Metallic': 1.0, 'Coat Weight': 0.3, 'Coat Roughness': 0.1})
    ai.inputs['Base Color'].default_value = (0.36, 0.39, 0.45, 1)
    L(t, rough.outputs[0], ai.inputs['Roughness']); L(t, bp.outputs[0], ai.inputs['Normal'])
    ai.inputs['Emission Color'].default_value = GOLD
    nrm = N(t, 'ShaderNodeSeparateXYZ'); L(t, geo.outputs['Normal'], nrm.inputs[0])
    facing = math_(t, 'POWER', math_(t, 'ABSOLUTE', nrm.outputs['Y']), 1.6)
    e = math_(t, 'MULTIPLY', math_(t, 'MULTIPLY', math_(t, 'MULTIPLY', line.outputs[0], segm.outputs[0]), facing), 9.0)
    L(t, math_(t, 'MULTIPLY', e, emit_on.outputs[0]), ai.inputs['Emission Strength'])
    return ai.outputs[0]

def tm_nodes(t, centre):
    """transition time 0..1: spreads outward from between the eyes, with an organic edge"""
    geo = N(t, 'ShaderNodeNewGeometry')
    sub = N(t, 'ShaderNodeVectorMath', operation='SUBTRACT'); L(t, geo.outputs['Position'], sub.inputs[0]); sub.inputs[1].default_value = centre
    ln = N(t, 'ShaderNodeVectorMath', operation='LENGTH'); L(t, sub.outputs[0], ln.inputs[0])
    d = math_(t, 'MULTIPLY', ln.outputs['Value'], 1 / 0.27)
    nz = N(t, 'ShaderNodeTexNoise', ins={'Scale': 16.0, 'Detail': 3.0, 'Roughness': 0.55}); L(t, geo.outputs['Position'], nz.inputs['Vector'])
    nn = math_(t, 'MULTIPLY', math_(t, 'SUBTRACT', nz.outputs['Fac'], 0.5), 0.34)
    s = math_(t, 'ADD', math_(t, 'ADD', math_(t, 'MULTIPLY', d, 0.8), nn), 0.04)
    c = N(t, 'ShaderNodeClamp'); L(t, s, c.inputs['Value'])
    return c.outputs[0]

def eye_human(t):
    tex = N(t, 'ShaderNodeTexImage', image=eye_img)
    he = N(t, 'ShaderNodeBsdfPrincipled', ins={'Roughness': 0.25, 'Coat Weight': 1.0, 'Coat Roughness': 0.015, 'Subsurface Weight': 0.3, 'Subsurface Scale': 0.002})
    L(t, tex.outputs['Color'], he.inputs['Base Color'])
    # the eye mesh has a clear outer shell (texture alpha 0): see through it, keep a wet glint on it
    tr = N(t, 'ShaderNodeBsdfTransparent'); gl = N(t, 'ShaderNodeBsdfGlossy', ins={'Roughness': 0.02})
    cor = N(t, 'ShaderNodeMixShader'); cor.inputs[0].default_value = 0.05; L(t, tr.outputs[0], cor.inputs[1]); L(t, gl.outputs[0], cor.inputs[2])
    mx = N(t, 'ShaderNodeMixShader'); L(t, tex.outputs['Alpha'], mx.inputs[0]); L(t, cor.outputs[0], mx.inputs[1]); L(t, he.outputs[0], mx.inputs[2])
    return mx.outputs[0]
def eye_ai(t):
    at = N(t, 'ShaderNodeAttribute', attribute_name='irisr')
    a = N(t, 'ShaderNodeMapRange', interpolation_type='SMOOTHSTEP', ins={'From Min': 0.0024, 'From Max': 0.0034})
    b = N(t, 'ShaderNodeMapRange', interpolation_type='SMOOTHSTEP', ins={'From Min': 0.0050, 'From Max': 0.0060, 'To Min': 1.0, 'To Max': 0.0})
    L(t, at.outputs['Fac'], a.inputs['Value']); L(t, at.outputs['Fac'], b.inputs['Value'])
    ring = math_(t, 'MULTIPLY', a.outputs[0], b.outputs[0])
    emit_on = val(t, 'emit_on')
    ae = N(t, 'ShaderNodeBsdfPrincipled', ins={'Roughness': 0.05, 'Coat Weight': 1.0, 'Coat Roughness': 0.02})
    ae.inputs['Base Color'].default_value = (0.02, 0.022, 0.03, 1); ae.inputs['Emission Color'].default_value = GOLD
    L(t, math_(t, 'MULTIPLY', math_(t, 'MULTIPLY', ring, 30.0), emit_on.outputs[0]), ae.inputs['Emission Strength'])
    return ae.outputs[0]

# ---------------------------------------------------------------- real person's materials
m, t = newmat('Skin'); o = N(t, 'ShaderNodeOutputMaterial'); L(t, skin_shader(t), o.inputs['Surface'])
person.data.materials.clear(); person.data.materials.append(m)
for p in person.data.polygons: p.material_index = 0
eye_img = bpy.data.images.load(os.path.join(os.path.dirname(bpy.path.abspath(skin_img.filepath)), '..', '..', 'eyes', 'materials', 'brown_eye.png'))
m, t = newmat('Eye'); o = N(t, 'ShaderNodeOutputMaterial'); L(t, eye_human(t), o.inputs['Surface'])
eyes.data.materials.clear(); eyes.data.materials.append(m)
for ob in (brows, lashes):
    pr = [n for n in ob.data.materials[0].node_tree.nodes if n.bl_idname == 'ShaderNodeBsdfPrincipled'][0]
    pr.inputs['Roughness'].default_value = 0.6
    for lk in list(pr.inputs['Base Color'].links):
        mx = N(ob.data.materials[0].node_tree, 'ShaderNodeMix', data_type='RGBA', blend_type='MULTIPLY'); mx.inputs[0].default_value = 1.0
        L(ob.data.materials[0].node_tree, lk.from_socket, mx.inputs[6]); mx.inputs[7].default_value = (0.25, 0.2, 0.17, 1)
        L(ob.data.materials[0].node_tree, mx.outputs[2], pr.inputs['Base Color'])

# hair: real strands on the scalp, cropped short
m, t = newmat('Hair')
hb = N(t, 'ShaderNodeBsdfHairPrincipled'); hb.parametrization = 'MELANIN'
hb.inputs['Melanin'].default_value = 0.96; hb.inputs['Melanin Redness'].default_value = 0.2; hb.inputs['Roughness'].default_value = 0.4
o = N(t, 'ShaderNodeOutputMaterial'); L(t, hb.outputs[0], o.inputs['Surface'])
person.data.materials.append(m)
ps_mod = person.modifiers.new('Hair', 'PARTICLE_SYSTEM'); st = ps_mod.particle_system.settings
st.type = 'HAIR'; st.count = 22000; st.hair_length = 0.0065; st.emit_from = 'FACE'; st.use_modifier_stack = False
st.child_type = 'INTERPOLATED'; st.rendered_child_count = 14; st.child_length = 1.0; st.child_radius = 0.003
st.roughness_2 = 0.0015; st.roughness_endpoint = 0.001; st.clump_factor = 0.0
st.hair_step = 2; st.render_step = 2; st.material = 2
st.root_radius = 0.006; st.tip_radius = 0.003; st.radius_scale = 0.01
st.normal_factor = 0.006; st.factor_random = 0.0015
ps_mod.particle_system.vertex_group_density = 'scalp'

m, t = newmat('Shirt')
geo = N(t, 'ShaderNodeNewGeometry')
wv = N(t, 'ShaderNodeTexNoise', ins={'Scale': 900.0, 'Detail': 1.0}); L(t, geo.outputs['Position'], wv.inputs['Vector'])
bp = N(t, 'ShaderNodeBump', ins={'Strength': 0.3, 'Distance': 0.0005}); L(t, wv.outputs['Fac'], bp.inputs['Height'])
sh = N(t, 'ShaderNodeBsdfPrincipled', ins={'Roughness': 0.92, 'Sheen Weight': 0.12}); sh.inputs['Base Color'].default_value = (0.016, 0.018, 0.024, 1)
L(t, bp.outputs[0], sh.inputs['Normal'])
o = N(t, 'ShaderNodeOutputMaterial'); L(t, sh.outputs[0], o.inputs['Surface'])
shirt.data.materials.clear(); shirt.data.materials.append(m)

# ---------------------------------------------------------------- the reflection: a mirrored copy
src = [rig, person, eyes, brows, lashes, shirt]
bpy.ops.object.select_all(action='DESELECT')
for ob in src: ob.select_set(True)
bpy.context.view_layer.objects.active = rig
bpy.ops.object.duplicate()
dup = {o.name.split('.')[0]: o for o in bpy.context.selected_objects}
print('DUP', {k: v.name for k, v in dup.items()})
r_rig = dup['Rig']; r_person = dup['Person']; r_eyes = dup['P_eyes']; r_brows = dup['P_brows']; r_lashes = dup['P_lashes']
r_rig.matrix_world = REFL @ rig.matrix_world
bpy.context.view_layer.update()
R_MID = mir(EYE_MID)
m, t = newmat('SkinR'); modal_out(t, skin_shader(t), ai_shader(t, R_MID), tm_nodes(t, R_MID))
r_person.data.materials[0] = m
m, t = newmat('EyeR'); modal_out(t, eye_human(t), eye_ai(t), None)
r_eyes.data.materials[0] = m
r_hair = [md for md in r_person.modifiers if md.type == 'PARTICLE_SYSTEM'][0]

# ---------------------------------------------------------------- room
def quad(name, v, mat):
    me = bpy.data.meshes.new(name); me.from_pydata(v, [], [(0, 1, 2, 3)]); ob = bpy.data.objects.new(name, me)
    sc.collection.objects.link(ob); ob.data.materials.append(mat); return ob
def box(name, lo, hi, mat):
    bpy.ops.mesh.primitive_cube_add(size=1, location=[(lo[i] + hi[i]) / 2 for i in range(3)])
    ob = bpy.context.object; ob.name = name; ob.scale = [hi[i] - lo[i] for i in range(3)]; ob.data.materials.append(mat)
    bv = ob.modifiers.new('Bevel', 'BEVEL'); bv.width = 0.004; bv.segments = 3
    return ob
MX0, MX1, MZ0, MZ1 = -0.115, 0.250, 1.02, 1.945
fm, t = newmat('Frame'); f = N(t, 'ShaderNodeBsdfPrincipled', ins={'Metallic': 1.0, 'Roughness': 0.30}); f.inputs['Base Color'].default_value = (0.60, 0.42, 0.18, 1)
o = N(t, 'ShaderNodeOutputMaterial'); L(t, f.outputs[0], o.inputs['Surface'])
fw, fd = 0.020, 0.028
box('F_l', (MX0 - fw, MY - 0.004, MZ0 - fw), (MX0, MY + fd, MZ1 + fw), fm)
box('F_r', (MX1, MY - 0.004, MZ0 - fw), (MX1 + fw, MY + fd, MZ1 + fw), fm)
box('F_b', (MX0, MY - 0.004, MZ0 - fw), (MX1, MY + fd, MZ0), fm)
box('F_t', (MX0, MY - 0.004, MZ1), (MX1, MY + fd, MZ1 + fw), fm)
wm, t = newmat('Wall'); geo = N(t, 'ShaderNodeNewGeometry')
nz = N(t, 'ShaderNodeTexNoise', ins={'Scale': 30.0, 'Detail': 6.0}); L(t, geo.outputs['Position'], nz.inputs['Vector'])
bp = N(t, 'ShaderNodeBump', ins={'Strength': 0.25, 'Distance': 0.004}); L(t, nz.outputs['Fac'], bp.inputs['Height'])
w = N(t, 'ShaderNodeBsdfPrincipled', ins={'Roughness': 0.8}); w.inputs['Base Color'].default_value = (0.032, 0.048, 0.080, 1); L(t, bp.outputs[0], w.inputs['Normal'])
o = N(t, 'ShaderNodeOutputMaterial'); L(t, w.outputs[0], o.inputs['Surface'])
yw = MY
quad('W_l', [(-6, yw, -1), (MX0, yw, -1), (MX0, yw, 4), (-6, yw, 4)], wm)
quad('W_r', [(MX1, yw, -1), (6, yw, -1), (6, yw, 4), (MX1, yw, 4)], wm)
quad('W_b', [(MX0, yw, -1), (MX1, yw, -1), (MX1, yw, MZ0), (MX0, yw, MZ0)], wm)
quad('W_t', [(MX0, yw, MZ1), (MX1, yw, MZ1), (MX1, yw, 4), (MX0, yw, 4)], wm)
quad('Back', [(6, 4.0, -1), (-6, 4.0, -1), (-6, 4.0, 4), (6, 4.0, 4)], wm)
quad('BackR', [(-6, 2 * MY - 4.0, -1), (6, 2 * MY - 4.0, -1), (6, 2 * MY - 4.0, 4), (-6, 2 * MY - 4.0, 4)], wm)
# a door left ajar far behind the person: soft blue depth in the mirror
DX = {'port': -0.30, 'land': -0.62}[FMT]; dy = 2 * MY - 3.98
dm, t = newmat('Door'); e = N(t, 'ShaderNodeEmission'); e.inputs['Color'].default_value = (0.22, 0.42, 1.0, 1)
geo = N(t, 'ShaderNodeNewGeometry'); sp = N(t, 'ShaderNodeSeparateXYZ'); L(t, geo.outputs['Position'], sp.inputs[0])
gx = math_(t, 'DIVIDE', math_(t, 'SUBTRACT', sp.outputs['X'], DX), 0.16)
gz = math_(t, 'DIVIDE', math_(t, 'SUBTRACT', sp.outputs['Z'], 1.45), 0.75)
fall = math_(t, 'EXPONENT', math_(t, 'MULTIPLY', math_(t, 'ADD', math_(t, 'MULTIPLY', gx, gx), math_(t, 'MULTIPLY', gz, gz)), -1.0))
dstr = val(t, 'door', 1.0); L(t, math_(t, 'MULTIPLY', math_(t, 'MULTIPLY', fall, 0.40), dstr.outputs[0]), e.inputs['Strength'])
o = N(t, 'ShaderNodeOutputMaterial'); L(t, e.outputs[0], o.inputs['Surface'])
quad('DoorR', [(DX - 0.7, dy, -0.5), (DX + 0.7, dy, -0.5), (DX + 0.7, dy, 3.4), (DX - 0.7, dy, 3.4)], dm)
quad('Door', [(DX + 0.7, 3.98, -0.5), (DX - 0.7, 3.98, -0.5), (DX - 0.7, 3.98, 3.4), (DX + 0.7, 3.98, 3.4)], dm)

# ---------------------------------------------------------------- lights (each one has its mirror twin, as a real mirror gives)
LIGHTS = []
def light(name, loc, energy, size, col, tgt, spot=None):
    for suffix, f in (('', lambda p: Vector(p)), ('R', mir)):
        if spot:
            l = bpy.data.lights.new(name + suffix, 'SPOT'); l.spot_size = math.radians(spot); l.spot_blend = 0.6; l.shadow_soft_size = size
        else:
            l = bpy.data.lights.new(name + suffix, 'AREA'); l.size = size
        l.energy = energy; l.color = col
        ob = bpy.data.objects.new(name + suffix, l); sc.collection.objects.link(ob); ob.location = f(loc)
        e = bpy.data.objects.new(name + suffix + 'T', None); sc.collection.objects.link(e); e.location = f(tgt)
        cc = ob.constraints.new('TRACK_TO'); cc.target = e; cc.track_axis = 'TRACK_NEGATIVE_Z'; cc.up_axis = 'UP_Y'
        ob.visible_camera = False; LIGHTS.append(ob)
HEAD = (0, -0.05, 1.66)
light('Key', (-0.50, MY + 0.06, 1.84), 15, 0.26, (1.0, 0.84, 0.66), HEAD)              # warm lamp beside the mirror
light('Fill', (0.30, MY + 0.05, 1.60), 1.3, 0.45, (0.70, 0.80, 1.0), HEAD)              # faint cool fill, also the glint in the eyes
light('Wash', (-0.25, MY + 0.55, 2.35), 7, 0.3, (1.0, 0.82, 0.62), (-0.2, MY, 1.9))       # warm wash on the wall and frame
light('Rim', (0.75, 0.85, 2.35), 24, 0.22, (0.60, 0.74, 1.0), HEAD, spot=38)            # cool edge on the back of the head
wd = bpy.data.worlds.new('W'); sc.world = wd; wd.use_nodes = True
WBG = wd.node_tree.nodes['Background']; WBG.inputs[0].default_value = (0.010, 0.016, 0.032, 1); WBG.inputs[1].default_value = 0.4

# ---------------------------------------------------------------- report framing
bpy.context.view_layer.update()
def pv(p):
    v = world_to_camera_view(sc, cam, Vector(p)); return (round(v.x, 3), round(1 - v.y, 3))
print('FRAME vface', pv(VFACE), ' head top', pv((0, 0.0, 1.775)), ' ears', pv((0.095, 0.0, 1.66)), pv((-0.095, 0, 1.66)),
      ' mirror', pv((MX0, MY, MZ1)), pv((MX1, MY, MZ0)), ' door', pv((DX, dy, 1.45)))

# ---------------------------------------------------------------- render
sc.render.engine = 'CYCLES'
prefs = bpy.context.preferences.addons['cycles'].preferences
for typ in ('OPTIX', 'CUDA'):
    try:
        prefs.compute_device_type = typ; prefs.get_devices()
        for dv in prefs.devices: dv.use = dv.type != 'CPU'
        break
    except Exception as ex: print('no', typ, ex)
sc.cycles.device = 'GPU'
sc.cycles.max_bounces = 8; sc.cycles.caustics_reflective = False; sc.cycles.caustics_refractive = False
sc.cycles.sample_clamp_indirect = 8.0
sc.view_settings.view_transform = 'AgX' if PNG else 'Standard'
if PNG: sc.view_settings.look = 'AgX - Medium High Contrast'

def set_mode(ai_mix, emit_on, mask_on, lights):
    for mat in bpy.data.materials:
        if not mat.node_tree: continue
        for n in mat.node_tree.nodes:
            if n.bl_idname != 'ShaderNodeValue': continue
            if n.name == 'ai_mix': n.outputs[0].default_value = ai_mix
            if n.name == 'emit_on': n.outputs[0].default_value = emit_on
            if n.name == 'mask_on': n.outputs[0].default_value = mask_on
            if n.name == 'door': n.outputs[0].default_value = 1.0 if lights else 0.0
    human = not (ai_mix or mask_on)
    r_hair.show_render = human; r_brows.hide_render = not human; r_lashes.hide_render = not human
    for l in LIGHTS: l.hide_render = not lights
    WBG.inputs[1].default_value = 0.4 if lights else 0.0

MODES = {'H': (0, 0, 0, True), 'A': (1, 0, 0, True), 'E': (1, 1, 0, False), 'M': (0, 0, 1, False)}
for p in PASSES:
    set_mode(*MODES[p])
    sc.cycles.samples = SAMPLES if p != 'M' else max(48, SAMPLES // 6)
    sc.cycles.use_denoising = p != 'M'
    base = os.path.join(OUT, f'{FMT}_{p}')
    if PNG:
        sc.render.image_settings.file_format = 'PNG'; sc.render.filepath = base + '.png'
        bpy.ops.render.render(write_still=True); continue
    sc.render.image_settings.file_format = 'OPEN_EXR'; sc.render.image_settings.color_depth = '32'
    sc.render.filepath = base + '.exr'
    bpy.ops.render.render(write_still=True)
    img = bpy.data.images.load(base + '.exr'); w, h = img.size
    arr = np.empty(w * h * 4, np.float32); img.pixels.foreach_get(arr)
    arr = arr.reshape(h, w, 4)[::-1, :, :3]
    np.save(base + '.npy', arr.astype(np.float16)); bpy.data.images.remove(img); os.remove(base + '.exr')
    print('PASS', p, arr.shape, float(arr.mean()), float(arr.max()))
print('DONE')
