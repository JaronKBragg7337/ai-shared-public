# Blender 5.1 / Cycles: two looping macro shots for Still Unknown 10.3. Run:
#   blender -b -P shots.py -- <usm|saw> <outdir> [first last] [--cpu] [--test]
# Everything procedural, no assets.  Loops: usm = 48 frames @24 fps (vibration deliberately slowed), saw = 72 frames.
import bpy, math, random, sys, os
argv = sys.argv[sys.argv.index('--') + 1:]
shot, outdir = argv[0], os.path.abspath(argv[1])
rng = random.Random(3)
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = 'CYCLES'
cy = sc.cycles
cy.samples = 8 if '--test' in argv else 40
cy.use_adaptive_sampling = True; cy.adaptive_threshold = 0.05
cy.use_denoising = True
sc.render.resolution_x, sc.render.resolution_y = (640, 360) if '--test' in argv else (1280, 720)
sc.render.film_transparent = False
sc.render.image_settings.file_format = 'PNG'
try:
    sc.view_settings.view_transform = 'AgX'
except Exception:
    pass
if '--cpu' in argv:
    cy.device = 'CPU'
else:
    cy.device = 'GPU'
    prefs = bpy.context.preferences.addons['cycles'].preferences
    for t in ('OPTIX', 'CUDA'):
        try:
            prefs.compute_device_type = t; prefs.get_devices(); break
        except Exception:
            pass
    for d in prefs.devices:
        d.use = d.type != 'CPU'


def mat(name, col, rough=0.5, metal=0.0, emit=None, es=0.0, alpha=1.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*col, 1); b.inputs['Roughness'].default_value = rough; b.inputs['Metallic'].default_value = metal
    b.inputs['Alpha'].default_value = alpha
    if emit:
        b.inputs['Emission Color'].default_value = (*emit, 1); b.inputs['Emission Strength'].default_value = es
    return m


def granite(name, base=(0.36, 0.30, 0.30)):
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; b = nt.nodes['Principled BSDF']
    tc = nt.nodes.new('ShaderNodeTexCoord'); vor = nt.nodes.new('ShaderNodeTexVoronoi'); vor.inputs['Scale'].default_value = 38
    ramp = nt.nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].position = 0.30; ramp.color_ramp.elements[0].color = (0.10, 0.09, 0.10, 1)
    ramp.color_ramp.elements[1].position = 0.50; ramp.color_ramp.elements[1].color = (*base, 1)
    e = ramp.color_ramp.elements.new(0.75); e.color = (0.62, 0.50, 0.46, 1)
    noise = nt.nodes.new('ShaderNodeTexNoise'); noise.inputs['Scale'].default_value = 60; noise.inputs['Detail'].default_value = 6
    bump = nt.nodes.new('ShaderNodeBump'); bump.inputs['Strength'].default_value = 0.25
    nt.links.new(tc.outputs['Object'], vor.inputs['Vector']); nt.links.new(vor.outputs['Distance'], ramp.inputs['Fac'])
    nt.links.new(ramp.outputs['Color'], b.inputs['Base Color'])
    nt.links.new(tc.outputs['Object'], noise.inputs['Vector']); nt.links.new(noise.outputs['Fac'], bump.inputs['Height'])
    nt.links.new(bump.outputs['Normal'], b.inputs['Normal']); b.inputs['Roughness'].default_value = 0.55
    return m


def box(name, loc, size, m, bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(location=loc); o = bpy.context.object; o.name = name
    o.scale = (size[0] / 2, size[1] / 2, size[2] / 2); bpy.ops.object.transform_apply(scale=True)
    if bevel:
        md = o.modifiers.new('b', 'BEVEL'); md.width = bevel; md.segments = 3
    o.data.materials.append(m); return o


def cyl(name, loc, r, h, m, verts=48):
    bpy.ops.mesh.primitive_cylinder_add(location=loc, radius=r, depth=h, vertices=verts); o = bpy.context.object; o.name = name
    o.data.materials.append(m); bpy.ops.object.shade_smooth(); return o


def sphere(name, loc, r, m, seg=10):
    bpy.ops.mesh.primitive_uv_sphere_add(location=loc, radius=r, segments=seg, ring_count=seg // 2 + 1); o = bpy.context.object; o.name = name
    o.data.materials.append(m); bpy.ops.object.shade_smooth(); return o


def world(col=(0.012, 0.012, 0.03)):
    w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True
    w.node_tree.nodes['Background'].inputs['Color'].default_value = (*col, 1); w.node_tree.nodes['Background'].inputs['Strength'].default_value = 1.0


def light(loc, energy, size, col, target):
    bpy.ops.object.light_add(type='AREA', location=loc); l = bpy.context.object
    l.data.energy = energy; l.data.size = size; l.data.color = col
    c = l.constraints.new('TRACK_TO'); c.target = target; c.track_axis = 'TRACK_NEGATIVE_Z'; c.up_axis = 'UP_Y'


def camera(loc, target_loc, lens=50):
    bpy.ops.object.camera_add(location=loc); c = bpy.context.object; c.data.lens = lens
    tg = bpy.data.objects.new('tg', None); sc.collection.objects.link(tg); tg.location = target_loc
    k = c.constraints.new('TRACK_TO'); k.target = tg; k.track_axis = 'TRACK_NEGATIVE_Z'; k.up_axis = 'UP_Y'
    sc.camera = c; return c


world()

if shot == 'usm':
    N = 48; cycles = 4
    stone = box('stone', (0, 0, -0.5), (3.6, 2.2, 1.0), granite('g'), 0.03)
    water = mat('water', (0.25, 0.55, 0.75), 0.05, alpha=0.22)
    grit_m = mat('grit', (0.78, 0.86, 0.80), 0.25, 0.0, emit=(0.2, 0.9, 0.9), es=0.6)
    tool_m = mat('steel', (0.55, 0.58, 0.64), 0.28, 1.0)
    horn_m = mat('horn', (0.40, 0.43, 0.50), 0.35, 1.0)
    gap0 = 0.34; amp = 0.16
    tool = cyl('tool', (0, 0, gap0 + 0.7), 0.62, 1.4, tool_m)
    horn = cyl('horn', (0, 0, gap0 + 2.2), 0.32, 1.7, horn_m)
    cyl('pool', (0, 0, 0.012), 0.95, 0.02, water)
    grits = []
    for i in range(70):
        r = 0.55 * math.sqrt(rng.random()); a = rng.uniform(0, 6.283)
        g = sphere(f'g{i}', (r * math.cos(a), r * math.sin(a), 0.05), rng.uniform(0.035, 0.055), grit_m, 8)
        grits.append((g, rng.randrange(0, 6), rng.uniform(0.4, 1.0), r * math.cos(a), r * math.sin(a)))
    chips = [(sphere(f'c{i}', (0, 0, -5), 0.02, grit_m, 6), rng.uniform(0, 1), rng.uniform(0, 6.283)) for i in range(16)]
    sc.frame_start, sc.frame_end = 1, N
    for f in range(1, N + 1):
        ph = (f - 1) / N * cycles * 2 * math.pi
        z = gap0 + amp * (0.5 - 0.5 * math.cos(ph))
        tool.location.z = z + 0.7; horn.location.z = z + 2.2
        tool.keyframe_insert('location', frame=f); horn.keyframe_insert('location', frame=f)
        for g, off, h, x, y in grits:
            gp = ph + off * 0.9
            top = z - 0.05
            zz = 0.06 + max(0, (top - 0.06) * (0.5 - 0.5 * math.cos(gp)) ** 1.5) * h
            g.location = (x + 0.02 * math.sin(gp * 0.5 + off), y + 0.02 * math.cos(gp * 0.5), zz); g.keyframe_insert('location', frame=f)
        for c, p0, a0 in chips:
            u = (f / N * 2 + p0) % 1.0
            rr = 0.62 + 0.35 * u
            c.location = (rr * math.cos(a0), rr * math.sin(a0), 0.04 + 1.0 * u * (1 - u)); c.scale = (1 - u,) * 3
            c.keyframe_insert('location', frame=f); c.keyframe_insert('scale', frame=f)
    camera((5.2, -6.6, 2.4), (0, 0, 0.9), 50)
    light((-3, -3, 4), 900, 4, (0.8, 0.9, 1.0), stone); light((4, 1, 2.5), 500, 3, (1.0, 0.8, 0.6), stone)
elif shot == 'saw':
    N = 72
    stone = box('stone', (0, 0, -0.6), (6.0, 3.0, 1.2), granite('g', (0.42, 0.34, 0.33)), 0.04)
    cu = mat('copper', (0.80, 0.38, 0.20), 0.30, 1.0)
    sand_m = mat('sand', (0.80, 0.68, 0.46), 0.8)
    rope_m = mat('rope', (0.55, 0.45, 0.30), 0.9)
    box('slot', (0, 0, -0.04), (4.6, 0.20, 0.10), mat('dark', (0.02, 0.018, 0.02), 0.9))
    blade = box('blade', (0, 0, 0.12), (2.8, 0.55, 0.06), cu, 0.01)
    h1 = cyl('h1', (-1.6, 0, 0.22), 0.11, 0.55, rope_m, 16); h2 = cyl('h2', (1.6, 0, 0.22), 0.11, 0.55, rope_m, 16)
    sand = []
    for i in range(260):
        x = rng.uniform(-1.9, 1.9); y = rng.gauss(0, 0.28)
        if abs(y) < 0.09: y = 0.1 * (1 if y >= 0 else -1)
        s = sphere(f's{i}', (x, y, 0.025), rng.uniform(0.018, 0.034), sand_m, 6)
        sand.append((s, x, y))
    sc.frame_start, sc.frame_end = 1, N
    for f in range(1, N + 1):
        ph = (f - 1) / N * 2 * math.pi
        dx = 0.55 * math.sin(ph)
        for o, bx in ((blade, 0.0), (h1, -1.6), (h2, 1.6)):
            o.location.x = bx + dx; o.keyframe_insert('location', frame=f)
        for s, x, y in sand:
            if abs(y) < 0.4 and abs(x - dx) < 1.6:
                s.location.z = 0.025 + 0.012 * math.sin(ph * 6 + x * 7)
            s.keyframe_insert('location', frame=f)
    camera((3.6, -5.6, 3.0), (0, 0, 0.1), 50)
    light((-3, -3, 5), 1100, 5, (0.9, 0.95, 1.0), stone); light((4, 2, 3), 700, 3, (1.0, 0.8, 0.6), stone)

first = int(argv[2]) if len(argv) > 3 and argv[2].isdigit() else sc.frame_start
last = int(argv[3]) if len(argv) > 3 and argv[3].isdigit() else sc.frame_end
outdir = os.path.abspath(outdir); os.makedirs(outdir, exist_ok=True)
for f in range(first, last + 1):
    p = os.path.join(outdir, f'f{f:04d}.png')
    if os.path.exists(p):
        continue
    sc.frame_set(f); sc.render.filepath = p; bpy.ops.render.render(write_still=True)
print('DONE', shot)
