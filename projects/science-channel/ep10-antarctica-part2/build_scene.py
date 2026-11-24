
# ================================================================ Science 8.10 "Antarctica Part 2: the sky in the ice"
# Generic scenes built from primitives in code (no downloaded assets); every one is labelled ILLUSTRATION on screen.  1 unit = 1 m.
#   FIELD  a flat polar snow plateau under a low sun (generic, not a real site); a few falling ice crystals for "it starts as snow"
#   CORE   a cold-room bench: a clear ice core with air bubbles lying in a foam cradle; hairline cracks grow (brittle ice)
#   LAB    a lab bench: a small ice piece beside three sugar cubes for scale; a laser beam turns the ice to vapor; a gas readout
#   GLASS  a glass of water with a chunk of glacier-style ice; bubbles stream out as it melts (generic, no brand)
#   CAPE   a windy coastal headland with a small white air station, an intake mast and steel cylinders (generic, not Cape Grim)
#   SHELF  an archive store room: rows of air cylinders, one old olive-drab cylinder, and an old scuba tank on a shelf
#   JAR    a jar with a lid and a dated paper tag on an outdoor wooden table
ORG = {"CORE": Vector((0, 0, 0)), "LAB": Vector((50, 0, 0)), "GLASS": Vector((100, 0, 0)), "SHELF": Vector((150, 0, 0)),
       "JAR": Vector((0, 3000, 0)), "CAPE": Vector((0, 20000, 0)), "FIELD": Vector((10000, 0, 0))}
LINEAR_ANIM = set(); SMOOTH_ANIM = set()

def lathe(name, prof, setname, segs=64, cap_top=False):
    """revolve a closed (r, z) profile around Z"""
    V = []; F = []; n = len(prof)
    for i in range(segs):
        a_ = 2 * math.pi * i / segs
        for r, z in prof: V.append((r * math.cos(a_), r * math.sin(a_), z))
    for i in range(segs):
        i2 = (i + 1) % segs
        for k in range(n - 1):
            F.append((i * n + k, i2 * n + k, i2 * n + k + 1, i * n + k + 1))
        F.append((i * n + n - 1, i2 * n + n - 1, i2 * n, i * n))
    o = mesh_obj(name, V, F, setname)
    bm = bmesh.new(); bm.from_mesh(o.data); bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-6)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces); bm.to_mesh(o.data); bm.free(); o.data.update()
    return o

def glass_mat(name, ior=1.5, col=(1, 1, 1), rough=0.0):
    m, nt = mat(name); b = principled(nt, col, rough, trans=1.0, ior=ior); finish(nt, b.outputs[0]); return m
def ice_mat(name, rough=.04, frost=0.0):
    m, nt = mat(name); ob, gen = coords(nt); h = NOISE(nt, ob, 60.0, 5, .6)
    r = M(nt, "ADD", M(nt, "MULTIPLY", h, .08 + frost), rough)
    b = principled(nt, (.86, .93, 1.0), r, trans=1.0, ior=1.31, normal=BUMP(nt, h, .04 + frost, .002)); finish(nt, b.outputs[0]); return m
def snow_mat(name, scale=1.0):
    m, nt = mat(name); ob, gen = coords(nt)
    v = VORO(nt, ob, 900.0 * scale); h1 = NOISE(nt, ob, 3.0 * scale, 6, .6); h2 = NOISE(nt, ob, 40.0 * scale, 4, .5)
    hh = M(nt, "ADD", M(nt, "MULTIPLY", v.outputs["Distance"], .4), M(nt, "ADD", h1, M(nt, "MULTIPLY", h2, .5)))
    col = MIXC(nt, h1, (.86, .9, .96), (.97, .975, .985))
    b = principled(nt, col, .5, sss=.25, sss_r=(.4, .6, 1.0), normal=BUMP(nt, hh, .5, .05)); finish(nt, b.outputs[0]); return m
def wood_mat(name, c1, c2, scale=8.0):
    m, nt = mat(name); ob, gen = coords(nt)
    st = VSCALE(nt, ob, 1.0, 30.0, 1.0); h = NOISE(nt, st, scale, 6, .6)
    col = MIXC(nt, h, c1, c2); b = principled(nt, col, .5, normal=BUMP(nt, h, .2, .002)); finish(nt, b.outputs[0]); return m
def foam_mat(name, col):
    m, nt = mat(name); ob, gen = coords(nt); h = NOISE(nt, ob, 500.0, 4)
    b = principled(nt, col, .9, normal=BUMP(nt, h, .2, .001), sss=.1); finish(nt, b.outputs[0]); return m
def paper_mat(name):
    m, nt = mat(name); ob, gen = coords(nt); h = NOISE(nt, ob, 300.0, 5)
    col = MIXC(nt, h, (.86, .82, .72), (.93, .9, .82)); b = principled(nt, col, .85, normal=BUMP(nt, h, .1, .001)); finish(nt, b.outputs[0]); return m
def ink_mat(name, col=(.03, .04, .08)):
    m, nt = mat(name); b = principled(nt, col, .6); finish(nt, b.outputs[0]); return m

M_AIRB = glass_mat("AirBubble", 1.0 / 1.31)
M_WATER = glass_mat("Water", 1.333, (.95, .98, 1.0))
M_GLASS = glass_mat("Glass", 1.5, (.97, .99, .98))

# ================================================================ FIELD: polar plateau
o = ORG["FIELD"]
def plateau_h(X, Y):
    sast = .3 * fbm2(X * 1.0, Y * 4.0, .05, 4, 2.0)          # wind-carved ridges run across Y
    return sast + 1.2 * fbm2(X, Y, .002, 3, 5.0)
give(grid("Plateau", 900, 900, 260, 260, plateau_h, "FIELD", origin=o), snow_mat("Snow", 1.0))
def near_h(X, Y):   # sastrugi: wind-cut ridges, finer near the cameras
    return plateau_h(X, Y - 2.0) + .03 + .22 * np.abs(fbm2(X * .3, Y * 1.2, .6, 3, 8.0)) + .025 * fbm2(X, Y, 3.0, 2, 3.0)
give(grid("SnowNear", 40, 40, 320, 320, near_h, "FIELD", origin=o + Vector((0, -2, 0))), snow_mat("SnowFine", 3.0))
# falling ice crystals near the low camera (FIELD_B); one empty carries them down
flake_src = blob("FlakeSrc", .006, 1.0, "FIELD", 1, .25, 2.0, (1, 1, .3)); give(flake_src, foam_mat("Flake", (.95, .97, 1.0)))
FL = bpy.data.objects.new("Flakes", None); link(FL, "FIELD"); FL.location = o + Vector((0, 0, 0))
z_near = float(plateau_h(np.array([0.0]), np.array([-2.0]))[0]) + .02
rs = random.Random(3); fl_pts = [o + Vector((rs.uniform(-.6, .6), rs.uniform(-3.5, -2.0), z_near + rs.uniform(.05, 1.7))) for _ in range(220)]
fls = scatter_instances("Fl", flake_src, fl_pts, [rs.uniform(.6, 1.4) for _ in fl_pts], "FIELD", [(rs.uniform(0, 3), rs.uniform(0, 3), rs.uniform(0, 3)) for _ in fl_pts])
for f_ in fls: f_.parent = FL; f_.location = f_.location - FL.location
flake_src.hide_render = True
LINEAR_ANIM.add(FL.name)

# ================================================================ CORE: ice core on a foam cradle in a cold room
o = ORG["CORE"]
give(prim_box("CoreTable", (1.6, .7, .04), "CORE", loc=o + Vector((0, 0, .78))), metal("TableSteel", (.55, .56, .58), .35))
give(prim_box("LightTable", (1.5, .5, .004), "CORE", loc=o + Vector((0, 0, .802))), EMITM("LightTableE", (.92, .96, 1.0), 2.5))
give(prim_box("CoreBack", (8, .1, 4), "CORE", loc=o + Vector((0, 1.4, 1.5))), plastic("ColdWall", (.42, .5, .58), .7))
give(grid("CoreFloor", 8, 8, 1, 1, lambda X, Y: X * 0, "CORE", origin=o), plastic("ColdFloor", (.1, .11, .13), .6))
M_FOAM = foam_mat("Foam", (.75, .8, .85))
CZ = .804 + .05
for x_ in (-.36, .36):   # small foam chocks hold the core on the light table
    for s_ in (-1, 1): give(prim_box("Chock%g%d" % (x_, s_), (.05, .03, .025), "CORE", loc=o + Vector((x_, s_ * .055, .804 + .0125))), M_FOAM)
core = give(prim_cyl("Core", .05, .8, "CORE", 96, loc=o + Vector((0, 0, CZ)), rot=(0, math.pi / 2, 0)), ice_mat("CoreIce", .03, .02))
core2 = give(prim_cyl("Core2", .05, .4, "CORE", 96, loc=o + Vector((.68, -.02, CZ)), rot=(0, math.pi / 2, math.radians(4))), ice_mat("CoreIce2", .05, .04))
for x_ in (.52, .84):
    for s_ in (-1, 1): give(prim_box("Chock2%g%d" % (x_, s_), (.05, .03, .025), "CORE", loc=o + Vector((x_, -.02 + s_ * .055, .804 + .0125)), rot=(0, 0, math.radians(4))), M_FOAM)
bub_src = blob("BubSrc", .001, 2.0, "CORE", 2, .08, 2.0, (1, 1, 1.25)); give(bub_src, M_AIRB)
rs = random.Random(11); bp = []; bsc = []
while len(bp) < 900:
    x = rs.uniform(-.39, .39); y = rs.uniform(-.045, .045); z = rs.uniform(-.045, .045)
    if y * y + z * z > .044 ** 2: continue
    bp.append(o + Vector((x, y, CZ + z))); bsc.append(rs.uniform(.35, 1.5) if rs.random() > .1 else rs.uniform(1.5, 2.6))
scatter_instances("Bub", bub_src, bp, bsc, "CORE", [(rs.uniform(0, 3), rs.uniform(0, 3), rs.uniform(0, 3)) for _ in bp])
bub_src.hide_render = True
CRACKS = []
M_CRACK = mat("CrackM"); _b = principled(M_CRACK[1], (.9, .93, .97), .25, trans=0.0); finish(M_CRACK[1], _b.outputs[0]); M_CRACK = M_CRACK[0]
for k, (x, ang, r_) in enumerate(((-.16, 18, .042), (.05, -25, .045), (.21, 32, .04), (-.30, -12, .038))):
    c_ = give(prim_cyl("Crack%d" % k, r_, .00015, "CORE", 48, loc=o + Vector((x, 0, CZ)), rot=(math.radians(ang), math.radians(90 + ang * .6), 0)), M_CRACK)
    CRACKS.append(c_); SMOOTH_ANIM.add(c_.name)
add_light("CoreTop", "AREA", "CORE", o + Vector((0, -.3, 2.0)), 120, (.85, .92, 1.0), 1.2, target=o + Vector((0, 0, CZ)))
add_light("CoreRim", "AREA", "CORE", o + Vector((.2, .9, 1.1)), 90, (.75, .85, 1.0), .6, target=o + Vector((0, 0, CZ)))
add_light("CoreUnder", "AREA", "CORE", o + Vector((-.6, -.4, .95)), 12, (1.0, .9, .8), .3, target=o + Vector((0, 0, CZ)))

# ================================================================ LAB: ice piece, sugar cubes, laser, readout
o = ORG["LAB"]
give(prim_box("LabBench", (1.4, .8, .04), "LAB", loc=o + Vector((0, 0, .88))), floor_mat("Slate", (.08, .085, .09), (.12, .125, .13), 30.0, .55, .05))
give(prim_box("LabBack", (6, .1, 3), "LAB", loc=o + Vector((0, .7, 1.4))), plastic("LabWall", (.5, .52, .54), .8))
BZ = .90
plate = give(prim_cyl("LabPlate", .03, .004, "LAB", 64, loc=o + Vector((0, 0, BZ + .002))), M_STEEL)
icep = give(blob("IcePiece", .0135, 4.0, "LAB", 4, .18, 2.2, (1.05, .95, .8), flat_bottom=-.009), ice_mat("IcePieceM", .05, .06))
icep.location = o + Vector((0, 0, BZ + .004 + .009)); SMOOTH_ANIM.add(icep.name)
M_SUGAR = foam_mat("Sugar", (.93, .92, .9))
for k in range(3):
    sc_ = give(prim_box("Sugar%d" % k, (.016, .016, .016), "LAB", loc=o + Vector((.06 + k * .02, -.012 + (k % 2) * .006, BZ + .008)), rot=(0, 0, math.radians(rs.uniform(-12, 12)))), M_SUGAR)
    bevel(sc_, .0012, 2)
head_ = give(prim_cyl("LaserHead", .012, .06, "LAB", 48, loc=o + Vector((0, 0, BZ + .16))), M_BLACK)
give(prim_cyl("LaserLens", .006, .004, "LAB", 32, loc=o + Vector((0, 0, BZ + .128))), M_CHROME)
give(prim_box("LaserArm", (.012, .2, .012), "LAB", loc=o + Vector((0, .1, BZ + .17))), M_ALU)
give(prim_cyl("LaserPost", .008, .3, "LAB", 24, loc=o + Vector((0, .2, BZ + .03))), M_ALU)
beam = give(prim_cyl("Beam", .0007, .12, "LAB", 16, loc=o + Vector((0, 0, BZ + .067))), EMITM("BeamE", (1.0, .12, .08), 60))
glow = add_light("BeamGlow", "POINT", "LAB", o + Vector((0, 0, BZ + .02)), 0.0, (1.0, .35, .2), .003)
scr_ = give(prim_box("Readout", (.22, .015, .13), "LAB", loc=o + Vector((-.17, .12, BZ + .1)), rot=(math.radians(-8), 0, math.radians(12))), M_BLACK)
M_SCR = EMITM("ReadoutE", (.06, .12, .1), 1.0); M_TXT = EMITM("ReadoutT", (.55, 1.0, .7), 3.0)
give(prim_box("ReadoutGlass", (.2, .002, .11), "LAB", loc=o + Vector((-.17, .112, BZ + .1)), rot=(math.radians(-8), 0, math.radians(12))), M_SCR)
for k, t_ in enumerate(("CO2", "CH4", "N2O")):
    txo = text_obj("RdT%d" % k, t_, .022, "LAB", o + Vector((-.215, .109, BZ + .135 - k * .032)), (math.radians(82), 0, math.radians(12)), M_TXT)
    txo.data.align_x = "LEFT"
    give(prim_box("RdBar%d" % k, (.07 * (1 - .2 * k), .001, .008), "LAB", loc=o + Vector((-.125, .108, BZ + .136 - k * .032)), rot=(math.radians(-8), 0, math.radians(12))), M_TXT)
add_light("LabKey", "AREA", "LAB", o + Vector((-.3, -.5, 1.4)), 40, (1, .97, .92), .8, target=o + Vector((0, 0, BZ)))
add_light("LabRim", "AREA", "LAB", o + Vector((.4, .4, 1.2)), 25, (.8, .88, 1.0), .5, target=o + Vector((0, 0, BZ)))

# ================================================================ GLASS: a glass of water with glacier-style ice, bubbles streaming
o = ORG["GLASS"]
give(prim_box("Bar", (1.6, .7, .04), "GLASS", loc=o + Vector((0, 0, .98))), wood_mat("BarWood", (.12, .06, .03), (.22, .12, .06), 6.0))
give(prim_box("BarBack", (6, .1, 3), "GLASS", loc=o + Vector((0, 1.0, 1.5))), plastic("BarWall", (.3, .22, .15), .8))
GZ = 1.0
tumbler = give(prim_cyl("Tumbler", .041, .11, "GLASS", 96, loc=o + Vector((0, 0, GZ + .055))), M_GLASS)
bm = bmesh.new(); bm.from_mesh(tumbler.data)
bmesh.ops.delete(bm, geom=[f_ for f_ in bm.faces if f_.normal.z > .9], context="FACES"); bm.to_mesh(tumbler.data); bm.free()
so = tumbler.modifiers.new("solid", "SOLIDIFY"); so.thickness = .0026; so.offset = -1.0; so.use_even_offset = True
tumbler.data.polygons.foreach_set("use_smooth", [True] * len(tumbler.data.polygons))
bev_ = tumbler.modifiers.new("bev", "BEVEL"); bev_.width = .0008; bev_.segments = 2; bev_.limit_method = "ANGLE"
water = give(prim_cyl("WaterIn", .0381, .0752, "GLASS", 96, loc=o + Vector((0, 0, GZ + .0028 + .0376))), M_WATER)
gice = give(blob("GlassIce", .021, 7.0, "GLASS", 4, .22, 1.8, (1.1, .9, .95)), ice_mat("GlassIceM", .01, 0.0)); gice.location = o + Vector((.003, 0, GZ + .074))
rs = random.Random(21); gb = []
for k in range(40):   # a few bubbles trapped in the chunk
    p_ = Vector((rs.uniform(-.014, .014), rs.uniform(-.012, .012), rs.uniform(-.012, .012)))
    gb.append(o + Vector((.003, 0, GZ + .074)) + p_)
gbsrc = blob("GBSrc", .0008, 3.0, "GLASS", 2, .05, 2.0); give(gbsrc, M_AIRB)
scatter_instances("GB", gbsrc, gb, [rs.uniform(.5, 1.8) for _ in gb], "GLASS"); gbsrc.hide_render = True
RISERS = []
rsrc = blob("RiseSrc", .0007, 5.0, "GLASS", 2, .03, 2.0); give(rsrc, M_AIRB); rsrc.hide_render = True
for k in range(36):
    b_ = bpy.data.objects.new("Rise%02d" % k, rsrc.data); link(b_, "GLASS")
    b_.scale = (rs.uniform(.6, 1.4),) * 3; RISERS.append((b_, rs.uniform(-.012, .012), rs.uniform(-.01, .01), rs.uniform(0, 1), rs.uniform(1.4, 2.4)))
    LINEAR_ANIM.add(b_.name)
add_light("BarKey", "AREA", "GLASS", o + Vector((-.4, -.3, 1.5)), 30, (1.0, .9, .78), .5, target=o + Vector((0, 0, GZ + .06)))
add_light("BarBackL", "AREA", "GLASS", o + Vector((.1, .45, 1.15)), 25, (1.0, .85, .65), .3, target=o + Vector((0, 0, GZ + .06)))
give(prim_box("BarGlow", (1.4, .02, .5), "GLASS", loc=o + Vector((.05, .93, 1.2))), EMITM("BarGlowE", (1.0, .75, .5), 3.0))

# ================================================================ CAPE: coastal headland, small station, mast, cylinders
o = ORG["CAPE"]
def cape_h(X, Y):
    land = np.clip((60 - Y) / 25.0, 0, 1)                       # cliff edge near y = 60 .. 85 drops to the sea
    land = land * land * (3 - 2 * land)
    return -2 + land * (32 + 2.5 * fbm2(X, Y, .008, 3, 1.0)) + .5 * fbm2(X, Y, .1, 3, 4.0) * land
grid("Headland", 700, 500, 220, 180, cape_h, "CAPE", origin=o + Vector((0, -150, 0)))
hl = bpy.data.objects["Headland"]
m_, nt_ = mat("Grass"); ob_, gen_ = coords(nt_); h_ = NOISE(nt_, ob_, .4, 6, .6); h2_ = NOISE(nt_, ob_, 6.0, 4, .6)
col_ = MIXC(nt_, h_, (.16, .2, .07), (.34, .32, .16)); col_ = MIXC(nt_, SMOOTH(nt_, h2_, .62, .7), col_, (.3, .28, .25))
b_ = principled(nt_, col_, .9, normal=BUMP(nt_, M(nt_, "ADD", h2_, h_), .6, .3)); finish(nt_, b_.outputs[0]); hl.data.materials.append(m_)
sea = grid("Sea", 6000, 6000, 1, 1, lambda X, Y: X * 0, "CAPE", origin=o + Vector((0, 2800, 0)))
m_, nt_ = mat("SeaM"); ob_, gen_ = coords(nt_)
nz = N(nt_, "ShaderNodeTexNoise"); nz.noise_dimensions = "4D"; nz.inputs["Scale"].default_value = .25; nz.inputs["Detail"].default_value = 8
L(nt_, ob_, nz.inputs["Vector"]); SEA_W = nz.inputs["W"]
b_ = principled(nt_, (.01, .03, .05), .06, normal=BUMP(nt_, nz.outputs["Fac"], .5, .4)); finish(nt_, b_.outputs[0]); sea.data.materials.append(m_)
SEA_NT = nt_
def cape_z(x, y): return float(cape_h(np.array([x]), np.array([y + 150]))[0])
hx, hy = 0.0, -130.0; hz = cape_z(hx, hy)
M_WHITE = painted("StationWhite", (.8, .8, .78), .4)
hut = give(prim_box("Hut", (8, 5, 3), "CAPE", loc=o + Vector((hx, hy, hz + 1.3))), M_WHITE); bevel(hut, .05)
give(prim_box("HutRoof", (8.6, 5.6, .25), "CAPE", loc=o + Vector((hx, hy, hz + 2.9))), painted("Roof", (.25, .27, .3), .5))
give(prim_box("HutDoor", (1.0, .05, 2.0), "CAPE", loc=o + Vector((hx - 2, hy - 2.52, hz + .9))), painted("Door", (.2, .3, .4), .4))
for k in range(3): give(prim_box("HutWin%d" % k, (1.1, .05, .7), "CAPE", loc=o + Vector((hx + .3 + k * 1.5, hy - 2.52, hz + 1.8))), glass_mat("Win", 1.5, (.3, .35, .4), .1))
mast = give(prim_cyl("Mast", .12, 14, "CAPE", 24, loc=o + Vector((hx + 6, hy + 1, hz + 7))), M_STEEL)
give(prim_cyl("Intake", .25, .5, "CAPE", 24, loc=o + Vector((hx + 6, hy + 1, hz + 14.1))), M_STEEL)
curve_obj("IntakeLine", [tuple(o + Vector((hx + 6, hy + 1, hz + 13.8))), tuple(o + Vector((hx + 5.2, hy + .5, hz + 6))), tuple(o + Vector((hx + 4.1, hy, hz + 2.2)))], .04, "CAPE", M_BLACK)
for k in range(5):
    give(prim_cyl("CapeCyl%d" % k, .12, 1.3, "CAPE", 32, loc=o + Vector((hx - 5.5 + k * .3, hy - 3.2, hz + .65))), M_ALU)
    give(prim_cyl("CapeVal%d" % k, .03, .12, "CAPE", 16, loc=o + Vector((hx - 5.5 + k * .3, hy - 3.2, hz + 1.36))), M_CHROME)
give(prim_box("CylBase", (1.8, .5, .06), "CAPE", loc=o + Vector((hx - 4.9, hy - 3.2, hz - .02))), metal("RackSteel", (.3, .32, .35), .5))

# ================================================================ SHELF: archive store
o = ORG["SHELF"]
give(grid("StoreFloor", 14, 14, 1, 1, lambda X, Y: X * 0, "SHELF", origin=o), floor_mat("StoreConc", (.36, .35, .33), (.26, .25, .24), 3.0, .8, .15))
give(prim_box("StoreWall", (14, .1, 4), "SHELF", loc=o + Vector((0, 2.6, 2))), plastic("StoreWallM", (.55, .56, .55), .8))
M_RACK = painted("RackBlue", (.08, .16, .32), .45); M_ALU2 = metal("AluMatte", (.62, .63, .65), .5)
rs = random.Random(5)
for row in range(2):
    y0 = .8 + row * 1.2
    for x in (-3.6, 3.6):
        give(prim_box("Upr%d_%g" % (row, x), (.06, .5, 2.0), "SHELF", loc=o + Vector((x, y0, 1.0))), M_RACK)
    for lv in range(2):
        give(prim_box("Deck%d%d" % (row, lv), (7.3, .5, .04), "SHELF", loc=o + Vector((0, y0, .1 + lv * 1.05))), metal("Deck", (.5, .5, .52), .5))
        for k in range(16):
            x = -3.3 + k * .44
            h_c = .85
            give(prim_cyl("SC%d%d%02d" % (row, lv, k), .1, h_c, "SHELF", 32, loc=o + Vector((x, y0, .12 + lv * 1.05 + h_c / 2))), M_ALU2)
            give(prim_cyl("SV%d%d%02d" % (row, lv, k), .025, .08, "SHELF", 16, loc=o + Vector((x, y0, .12 + lv * 1.05 + h_c + .04))), M_CHROME)
            tg = give(prim_box("ST%d%d%02d" % (row, lv, k), (.07, .002, .04), "SHELF", loc=o + Vector((x, y0 - .101, .12 + lv * 1.05 + .55))), paper_mat("Tag%d" % (k % 3)))
# the old olive-drab cylinder on a low pallet in front
give(prim_box("Pallet", (.8, .6, .1), "SHELF", loc=o + Vector((-1.8, -.4, .05))), wood_mat("PalletW", (.35, .26, .16), (.5, .38, .24), 4.0))
od = give(capsule("OldCyl", .55, .14, "SHELF"), plastic("OliveDrab", (.045, .055, .02), .55, .2)); od.location = o + Vector((-1.8, -.4, .1 + .14))
give(prim_cyl("OldVal", .03, .1, "SHELF", 16, loc=o + Vector((-1.8 + .45, -.4, .1 + .14)), rot=(0, math.pi / 2, 0)), metal("Brass", (.75, .55, .25), .3))
# an old scuba tank on its own shelf to the right
give(prim_box("ScubaShelf", (.9, .45, .04), "SHELF", loc=o + Vector((4.6, 1.5, .9))), metal("Deck2", (.5, .5, .52), .5))
give(prim_box("ScubaLeg", (.05, .4, .9), "SHELF", loc=o + Vector((4.2, 1.5, .45))), M_RACK)
give(prim_box("ScubaLeg2", (.05, .4, .9), "SHELF", loc=o + Vector((5.0, 1.5, .45))), M_RACK)
sct = give(capsule("Scuba", .45, .09, "SHELF"), painted("ScubaYellow", (.55, .38, .04), .45)); sct.rotation_euler = (0, math.pi / 2, 0); sct.location = o + Vector((4.6, 1.5, 1.255))
give(prim_cyl("ScubaVal", .025, .09, "SHELF", 16, loc=o + Vector((4.6, 1.5, 1.61))), M_CHROME)
give(prim_cyl("ScubaKnob", .03, .02, "SHELF", 16, loc=o + Vector((4.6, 1.5, 1.66))), M_BLACK)
give(prim_box("ScubaTag", (.08, .002, .05), "SHELF", loc=o + Vector((4.6, 1.5 - .091, 1.25))), paper_mat("TagS"))
for k, x in enumerate((-3, 0, 3)):
    give(prim_box("StoreLamp%d" % k, (1.2, .15, .03), "SHELF", loc=o + Vector((x, .8, 3.3))), EMITM("LampE", (1, .98, .95), 12))
    add_light("StoreA%d" % k, "AREA", "SHELF", o + Vector((x, .3, 3.2)), 260, (.95, .97, 1.0), 1.0, rot=(0, 0, 0))
add_light("StoreFill", "AREA", "SHELF", o + Vector((0, -4, 1.6)), 120, (1, .95, .9), 3.0, target=o + Vector((0, 1, 1)))

# ================================================================ JAR: a jar with a dated tag on an outdoor table
o = ORG["JAR"]
JZ = .76
for k in range(6):
    give(prim_box("Plank%d" % k, (1.6, .145, .035), "JAR", loc=o + Vector((0, -.375 + k * .15, JZ - .018))), wood_mat("Plank%d" % (k % 2), (.33, .22, .13), (.45, .31, .19), 5.0 + k))
grid("Lawn", 200, 200, 80, 80, lambda X, Y: .2 * fbm2(X, Y, .05, 3, 6.0), "JAR", origin=o)
m_, nt_ = mat("LawnM"); ob_, gen_ = coords(nt_); h_ = NOISE(nt_, ob_, 2.0, 6, .6)
b_ = principled(nt_, MIXC(nt_, h_, (.08, .16, .04), (.2, .26, .08)), .85, normal=BUMP(nt_, h_, .5, .1)); finish(nt_, b_.outputs[0]); bpy.data.objects["Lawn"].data.materials.append(m_)
M_LEAF = plastic("Leaf", (.05, .13, .03), .8)
rs = random.Random(8)
for k in range(14):
    a_ = rs.uniform(-.9, .9) + math.pi / 2; d_ = rs.uniform(12, 30)
    bb = give(blob("Bush%d" % k, rs.uniform(1.5, 4), rs.uniform(0, 9), "JAR", 3, .3, 1.2, (1, 1, .8)), M_LEAF)
    bb.location = o + Vector((d_ * math.cos(a_), d_ * math.sin(a_), 1.0))
jar = lathe("Jar", [(0, 0), (.042, 0), (.045, .006), (.045, .1), (.036, .118), (.035, .13), (.032, .13), (.033, .118), (.042, .1), (.042, .006), (0, .004)], "JAR")
give(jar, M_GLASS); jar.location = o + Vector((0, 0, JZ))
lid = give(prim_cyl("JarLid", .038, .016, "JAR", 64, loc=o + Vector((0, 0, JZ + .134))), metal("LidMetal", (.7, .62, .45), .3)); bevel(lid, .002)
tag = give(prim_box("JarTag", (.09, .06, .0008), "JAR", loc=o + Vector((.1, -.07, JZ + .0005)), rot=(0, 0, math.radians(-14))), paper_mat("TagPaper"))
TR = Matrix.Rotation(math.radians(-14), 3, "Z")
for k, t_ in enumerate(("Air of ____", "Town: ______", "CO2 ___ ppm")):
    tt = text_obj("JarTxt%d" % k, t_, .0095, "JAR", o, (0, 0, math.radians(-14)), ink_mat("Ink"))
    tt.location = o + Vector((.1, -.07, JZ + .0011)) + TR @ Vector((0, .016 - k * .016, 0))
pencil = give(prim_cyl("Pencil", .0035, .15, "JAR", 6, loc=o + Vector((.17, .02, JZ + .0035)), rot=(0, math.pi / 2, math.radians(30))), painted("PencilY", (.8, .55, .05), .4))
