# Pioneer episode - space + truck scenes in Unreal (space builder agent, 11/15).
# Imports the procedural meshes (meshgen.py) and textures (textures.py), makes materials, builds /Game/Pioneer/Maps/PioneerSpace,
# one LevelSequence per scene from plan.json (plan.py), and renders through Movie Render Queue.
# Run (via run_unreal.py, which holds UNREAL.lock):  UnrealEditor NecklaceFilm.uproject -ExecCmds="py <this file>"
# Env: PIO_SCENES=s04,s05  PIO_TEST=1 (a few frames per scene; PIO_FRAMES=s04:0+300,s05:10)  PIO_RES=1920x1080
#      PIO_TS=temporal samples  PIO_WARM=warm-up frames  PIO_REIMPORT=1  PIO_EV=exposure bias  PIO_OUT=folder suffix
import os, json, math, glob, unreal
L = lambda m: unreal.log_warning("PIONEER | " + str(m))
HERE = "C:/Users/lilli/AI-Shared/projects/heartbeat-tv/pioneer-episode/space"
PROJ = "C:/Users/lilli/Projects/necklace-unreal"
ROOT = "/Game/Pioneer"; MAP = ROOT + "/Maps/PioneerSpace"
eal = unreal.EditorAssetLibrary; mel = unreal.MaterialEditingLibrary; tools = unreal.AssetToolsHelpers.get_asset_tools()
les = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem); eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
unreal.SystemLibrary.execute_console_command(None, "Editor.AsyncTextureCompilation 0")
PLAN = json.load(open(HERE + "/plan.json"))
REIMPORT = os.environ.get("PIO_REIMPORT", "0") == "1"
def sp(o, k, v):
    try: o.set_editor_property(k, v); return True
    except Exception as e: L("skip %s.%s (%s)" % (type(o).__name__, k, str(e)[:90])); return False

# ------------------------------------------------------------------ textures
TEX = {}
for png in sorted(glob.glob(HERE + "/tex/*.png")):
    name = os.path.splitext(os.path.basename(png))[0]; path = ROOT + "/Tex/" + name
    if REIMPORT or not eal.does_asset_exist(path):
        t = unreal.AssetImportTask(); t.filename = png; t.destination_path = ROOT + "/Tex"; t.destination_name = name; t.automated = True; t.replace_existing = True; t.save = True
        tools.import_asset_tasks([t])
    tx = unreal.load_asset(path)
    if name.endswith("_N"):
        sp(tx, "compression_settings", unreal.TextureCompressionSettings.TC_NORMALMAP); sp(tx, "srgb", False); eal.save_loaded_asset(tx)
    if name in ("T_Sky", "T_Flame"):
        sp(tx, "address_x", unreal.TextureAddress.TA_CLAMP); sp(tx, "address_y", unreal.TextureAddress.TA_CLAMP); eal.save_loaded_asset(tx)
    TEX[name] = tx
L("textures %d" % len(TEX))

# ------------------------------------------------------------------ meshes
MESH = {}
for glb in sorted(glob.glob(HERE + "/meshes/*.glb")):
    base = os.path.splitext(os.path.basename(glb))[0]; dest = ROOT + "/Meshes/" + base
    if REIMPORT or not eal.does_directory_exist(dest) or not eal.list_assets(dest):
        if eal.does_directory_exist(dest): eal.delete_directory(dest)
        t = unreal.AssetImportTask(); t.filename = glb; t.destination_path = dest; t.automated = True; t.replace_existing = True; t.save = True
        tools.import_asset_tasks([t])
    for p in eal.list_assets(dest, recursive=True):
        ad = eal.find_asset_data(p)
        if ad.asset_class_path.asset_name == "StaticMesh":
            m = unreal.load_asset(p); MESH[m.get_name()] = m
L("meshes %d: %s" % (len(MESH), sorted(MESH)[:80]))
def mesh(prefix):
    for k in (prefix, "SM_" + prefix):
        if k in MESH: return MESH[k]
    c = [k for k in MESH if k.endswith(prefix) or k.startswith(prefix + "_") or ("_" + prefix) in k]
    return MESH[c[0]] if c else None

# ------------------------------------------------------------------ materials
MPATH = ROOT + "/Mat"
MPC_PATH = MPATH + "/MPC_Pioneer"
mpc = unreal.load_asset(MPC_PATH) if eal.does_asset_exist(MPC_PATH) else tools.create_asset("MPC_Pioneer", MPATH, unreal.MaterialParameterCollection, unreal.MaterialParameterCollectionFactoryNew())
ps_ = []
for nm_, dv in (("SkyAmount", 0.0), ("RTGGlow", 0.0)):
    x = unreal.CollectionScalarParameter(); x.set_editor_property("parameter_name", nm_); x.set_editor_property("default_value", dv); ps_.append(x)
if [str(p.get_editor_property("parameter_name")) for p in mpc.get_editor_property("scalar_parameters")] != ["SkyAmount", "RTGGlow"]:
    mpc.set_editor_property("scalar_parameters", ps_); eal.save_loaded_asset(mpc)

def E(m, cls, x, y): return mel.create_material_expression(m, cls, x, y)
def vpar(m, name, c, x, y):
    e = E(m, unreal.MaterialExpressionVectorParameter, x, y); e.set_editor_property("parameter_name", name); e.set_editor_property("default_value", unreal.LinearColor(*c, 1)); return e
def spar(m, name, v, x, y):
    e = E(m, unreal.MaterialExpressionScalarParameter, x, y); e.set_editor_property("parameter_name", name); e.set_editor_property("default_value", float(v)); return e
def tpar(m, name, tex, x, y, normal=False):
    e = E(m, unreal.MaterialExpressionTextureSampleParameter2D, x, y); e.set_editor_property("parameter_name", name); e.set_editor_property("texture", tex)
    if normal: sp(e, "sampler_type", unreal.MaterialSamplerType.SAMPLERTYPE_NORMAL)
    return e
def mul(m, a, b, x, y, ao="", bo=""):
    e = E(m, unreal.MaterialExpressionMultiply, x, y); mel.connect_material_expressions(a, ao, e, "A"); mel.connect_material_expressions(b, bo, e, "B"); return e
def const(m, v, x, y):
    e = E(m, unreal.MaterialExpressionConstant, x, y); e.set_editor_property("r", float(v)); return e
def lerp_(m, a, b, al, x, y, alo=""):
    e = E(m, unreal.MaterialExpressionLinearInterpolate, x, y); mel.connect_material_expressions(a, "", e, "A"); mel.connect_material_expressions(b, "", e, "B"); mel.connect_material_expressions(al, alo, e, "Alpha"); return e
P = unreal.MaterialProperty
def material(name, build, blend=None, unlit=False, two=False):
    path = MPATH + "/" + name
    if eal.does_asset_exist(path):
        if os.environ.get("PIO_REMAT", "0") != "1": return unreal.load_asset(path)
        eal.delete_asset(path)
    m = tools.create_asset(name, MPATH, unreal.Material, unreal.MaterialFactoryNew())
    if unlit: m.set_editor_property("shading_model", unreal.MaterialShadingModel.MSM_UNLIT)
    if blend: m.set_editor_property("blend_mode", blend)
    if two: m.set_editor_property("two_sided", True)
    build(m); mel.recompile_material(m); eal.save_loaded_asset(m); return m
def b_lit(m):
    c = vpar(m, "Color", (0.8, 0.8, 0.8), -500, -200); mel.connect_material_property(c, "", P.MP_BASE_COLOR)
    mel.connect_material_property(spar(m, "Rough", 0.5, -500, 0), "", P.MP_ROUGHNESS); mel.connect_material_property(spar(m, "Metal", 0.0, -500, 100), "", P.MP_METALLIC)
    mel.connect_material_property(spar(m, "Spec", 0.5, -500, 200), "", P.MP_SPECULAR)
def b_littex(m):
    t = tpar(m, "Tex", TEX["T_White"], -800, -200); c = vpar(m, "Color", (1, 1, 1), -800, 50)
    mel.connect_material_property(mul(m, t, c, -450, -150, "RGB"), "", P.MP_BASE_COLOR)
    mel.connect_material_property(spar(m, "Rough", 0.5, -500, 150), "", P.MP_ROUGHNESS); mel.connect_material_property(spar(m, "Metal", 0.0, -500, 250), "", P.MP_METALLIC)
def b_mli(m):
    tc = E(m, unreal.MaterialExpressionTextureCoordinate, -1100, 0); sp(tc, "u_tiling", 2.2); sp(tc, "v_tiling", 2.2)
    t = tpar(m, "Tex", TEX["T_MLI"], -800, -250); n = tpar(m, "Nrm", TEX["T_MLI_N"], -800, 150, normal=True)
    mel.connect_material_expressions(tc, "", t, "UVs"); mel.connect_material_expressions(tc, "", n, "UVs")
    c = vpar(m, "Color", (1.0, 0.72, 0.32), -800, -20)
    mel.connect_material_property(mul(m, t, c, -450, -150, "RGB"), "", P.MP_BASE_COLOR); mel.connect_material_property(n, "RGB", P.MP_NORMAL)
    mel.connect_material_property(spar(m, "Rough", 0.24, -500, 350), "", P.MP_ROUGHNESS); mel.connect_material_property(spar(m, "Metal", 1.0, -500, 450), "", P.MP_METALLIC)
def b_plaque(m):
    t = tpar(m, "Tex", TEX["T_Plaque"], -900, 0); c = vpar(m, "Color", (0.92, 0.62, 0.26), -900, -250)
    k = lerp_(m, const(m, 0.10, -600, -100), const(m, 1.0, -600, -40), t, -400, -100, "R")
    mel.connect_material_property(mul(m, c, k, -200, -200), "", P.MP_BASE_COLOR)
    mel.connect_material_property(lerp_(m, const(m, 0.7, -600, 150), const(m, 0.42, -600, 210), t, -400, 150, "R"), "", P.MP_ROUGHNESS)
    mel.connect_material_property(const(m, 0.35, -400, 300), "", P.MP_METALLIC)
def b_unlit(m):
    t = tpar(m, "Tex", TEX["T_White"], -900, -100); c = vpar(m, "Color", (1, 1, 1), -900, 150); g = spar(m, "Glow", 1.0, -900, 300)
    mel.connect_material_property(mul(m, mul(m, t, c, -600, 0, "RGB"), g, -350, 50), "", P.MP_EMISSIVE_COLOR)
def b_add(m):
    t = tpar(m, "Tex", TEX["T_White"], -1000, -100); c = vpar(m, "Color", (1, 1, 1), -1000, 150); g = spar(m, "Glow", 1.0, -1000, 300)
    fr = E(m, unreal.MaterialExpressionFresnel, -1000, 450); sp(fr, "exponent", 1.6)
    om = E(m, unreal.MaterialExpressionOneMinus, -800, 450); mel.connect_material_expressions(fr, "", om, "")
    fa = spar(m, "FresnelAmt", 0.0, -800, 600); edge = lerp_(m, const(m, 1.0, -600, 400), om, fa, -500, 450)
    base = mul(m, mul(m, t, c, -700, 0, "RGB"), g, -450, 100)
    mel.connect_material_property(mul(m, base, edge, -250, 200), "", P.MP_EMISSIVE_COLOR)
def b_smoke(m):
    c = vpar(m, "Color", (0.75, 0.74, 0.72), -700, -200); mel.connect_material_property(c, "", P.MP_BASE_COLOR)
    fr = E(m, unreal.MaterialExpressionFresnel, -900, 100); sp(fr, "exponent", 1.3)
    om = E(m, unreal.MaterialExpressionOneMinus, -700, 100); mel.connect_material_expressions(fr, "", om, "")
    mel.connect_material_property(mul(m, om, spar(m, "Opac", 0.55, -700, 250), -450, 150), "", P.MP_OPACITY)
def b_sky(m):
    t = tpar(m, "Tex", TEX["T_Sky"], -900, -100); g = spar(m, "Glow", 1.0, -900, 150)
    mel.connect_material_property(mul(m, t, g, -500, 0, "RGB"), "", P.MP_EMISSIVE_COLOR)
    cp = E(m, unreal.MaterialExpressionCollectionParameter, -900, 300); cp.set_editor_property("collection", mpc); cp.set_editor_property("parameter_name", "SkyAmount")
    mel.connect_material_property(cp, "", P.MP_OPACITY)
def b_rtg(m):
    b_lit(m)
    cp = E(m, unreal.MaterialExpressionCollectionParameter, -900, 400); cp.set_editor_property("collection", mpc); cp.set_editor_property("parameter_name", "RTGGlow")
    ec = vpar(m, "Emit", (1.0, 0.33, 0.05), -900, 550)
    mel.connect_material_property(mul(m, ec, cp, -500, 450), "", P.MP_EMISSIVE_COLOR)
BL = unreal.BlendMode
PARENTS = {"lit": material("M_PLit", b_lit), "littex": material("M_PLitTex", b_littex), "littex2": material("M_PLitTex2", b_littex, two=True),
           "mli": material("M_PMLI", b_mli), "plaque": material("M_PPlaque", b_plaque), "unlit": material("M_PUnlit", b_unlit, unlit=True),
           "add": material("M_PAdd", b_add, blend=BL.BLEND_ADDITIVE, unlit=True, two=True), "smoke": material("M_PSmoke", b_smoke, blend=BL.BLEND_TRANSLUCENT),
           "sky": material("M_PSky", b_sky, blend=BL.BLEND_TRANSLUCENT, unlit=True, two=True), "rtg": material("M_PRTG", b_rtg)}
MI = {}
def mi(name, parent, tex=None, **kw):
    path = MPATH + "/" + name
    m = unreal.load_asset(path) if eal.does_asset_exist(path) else tools.create_asset(name, MPATH, unreal.MaterialInstanceConstant, unreal.MaterialInstanceConstantFactoryNew())
    m.set_editor_property("parent", PARENTS[parent])
    if tex: mel.set_material_instance_texture_parameter_value(m, "Tex", TEX[tex])
    for k, v in kw.items():
        if isinstance(v, tuple): mel.set_material_instance_vector_parameter_value(m, k, unreal.LinearColor(*v, 1))
        else: mel.set_material_instance_scalar_parameter_value(m, k, float(v))
    eal.save_loaded_asset(m); MI[name] = m; return m
lit = lambda n, c, r=0.5, mt=0.0, s=0.5: mi(n, "lit", Color=c, Rough=r, Metal=mt, Spec=s)
unl = lambda n, c, g=1.0, tex=None: mi(n, "unlit", tex, Color=c, Glow=g)
add = lambda n, c, g=1.0, tex="T_White", fr=0.0: mi(n, "add", tex, Color=c, Glow=g, FresnelAmt=fr)
# normal look
mi("MI_Dish", "littex", "T_Dish", Color=(0.92, 0.92, 0.9), Rough=0.55); mi("MI_DishBack", "littex", "T_Dish", Color=(0.8, 0.8, 0.78), Rough=0.6)
lit("MI_Metal", (0.62, 0.62, 0.64), 0.35, 1.0); lit("MI_Feed", (0.85, 0.85, 0.83), 0.5); mi("MI_MLI", "mli", Rough=0.4); lit("MI_Black", (0.025, 0.025, 0.03), 0.55)
lit("MI_Louver", (0.92, 0.92, 0.94), 0.14, 1.0); mi("MI_Plaque", "plaque"); lit("MI_Boom", (0.5, 0.5, 0.5), 0.4, 0.7)
mi("MI_RTG", "rtg", Color=(0.16, 0.16, 0.17), Rough=0.45, Metal=0.6, Emit=(1.0 * 0.3, 0.3 * 0.3, 0.04 * 0.3))
mi("MI_RTGCore", "rtg", Color=(0.22, 0.22, 0.23), Rough=0.4, Metal=0.7, Emit=(1.0 * 0.45, 0.38 * 0.45, 0.06 * 0.45))
mi("MI_Livery", "littex", "T_Livery", Rough=0.32); lit("MI_Paint", (0.86, 0.87, 0.89), 0.3); lit("MI_Trim", (0.3, 0.3, 0.32), 0.3, 0.8)
lit("MI_Glass", (0.01, 0.012, 0.015), 0.04, 0.0, 1.0); lit("MI_Tire", (0.02, 0.02, 0.02), 0.85); lit("MI_Chrome", (0.85, 0.85, 0.86), 0.15, 1.0)
lit("MI_DarkPlastic", (0.035, 0.035, 0.04), 0.5); unl("MI_Lamp", (1.0, 0.95, 0.85), 3.0); unl("MI_Tail", (1.0, 0.05, 0.04), 2.0)
lit("MI_RocketWhite", (0.9, 0.9, 0.9), 0.25, 0.2); lit("MI_RocketRed", (0.75, 0.04, 0.05), 0.3); lit("MI_Strap", (0.02, 0.02, 0.02), 0.6)
lit("MI_Nozzle", (0.16, 0.14, 0.12), 0.35, 1.0); lit("MI_RoofDish", (0.9, 0.9, 0.9), 0.4)
lit("MI_CabFloor", (0.03, 0.03, 0.03), 0.9); lit("MI_CabLiner", (0.42, 0.42, 0.41), 0.9); lit("MI_CabPanel", (0.13, 0.13, 0.14), 0.6)
lit("MI_CabSeat", (0.05, 0.07, 0.15), 0.85); lit("MI_CabDash", (0.05, 0.05, 0.055), 0.55); lit("MI_Cable", (0.01, 0.01, 0.01), 0.5)
for k in (1, 2, 3): unl("MI_Mon%d" % k, (1, 1, 1), 1.6, "T_Mon%d" % k)
lit("MI_Cup", (0.9, 0.9, 0.88), 0.2); lit("MI_CupRed", (0.7, 0.04, 0.05), 0.3); lit("MI_Coffee", (0.08, 0.035, 0.015), 0.08)
mi("MI_Paper", "littex2", "T_Paper", Rough=0.85)
add("MI_Flame", (1, 1, 1), 22.0, "T_Flame", 1.0); add("MI_FlameCore", (1, 1, 1), 40.0, "T_Flame", 0.8)
add("MI_Ring", (0.3, 0.85, 1.0), 5.0, fr=0.0); add("MI_HeatArrow", (1.0, 0.72, 0.25), 6.0); add("MI_BigArrow", (0.45, 1.0, 0.6), 9.0)
mi("MI_Smoke", "smoke")
for b_, g_ in (("D", 0.45), ("M", 1.1), ("B", 3.5)):
    unl("MI_Star%sw" % b_, (1.0, 0.95, 0.88), g_, "T_Radial"); unl("MI_Star%sb" % b_, (0.8, 0.88, 1.0), g_, "T_Radial")
add("MI_Sun", (1.0, 0.97, 0.9), float(os.environ.get("PIO_SUN", "500")), "T_Radial"); add("MI_Earth", (0.35, 0.6, 1.0), 2.5, "T_Radial")
mi("MI_Sky", "sky", "T_Sky", Glow=1.0)
mi("MI_Lot", "littex", "T_Lot", Rough=0.85); lit("MI_Grass", (0.10, 0.2, 0.05), 0.95); lit("MI_Wall", (0.62, 0.6, 0.56), 0.8); lit("MI_GDark", (0.06, 0.06, 0.065), 0.6)
unl("MI_Sign", (1, 1, 1), 2.0, "T_Sign"); lit("MI_GMetal", (0.5, 0.5, 0.5), 0.4, 1.0); unl("MI_GLamp", (1.0, 0.92, 0.8), 2.0)
for i, c in enumerate(((0.5, 0.05, 0.05), (0.05, 0.15, 0.4), (0.6, 0.6, 0.62), (0.02, 0.02, 0.02))): lit("MI_Car%d" % (i + 1), c, 0.3, 0.3)
lit("MI_Tree", (0.04, 0.1, 0.03), 0.9)
# false-colour heat palette (unlit, 'ironbow': cold = deep blue/purple, warm = red/orange, hot = yellow-white)
unl("MI_H_Hot", (1.0, 0.58, 0.14), 3.2); unl("MI_H_Hotter", (1.0, 0.82, 0.4), 4.2); unl("MI_H_Warm", (0.85, 0.2, 0.06), 1.5); unl("MI_H_WarmDark", (0.55, 0.08, 0.14), 1.1)
unl("MI_H_Aft", (0.95, 0.38, 0.08), 1.9); unl("MI_H_Cold", (0.05, 0.04, 0.28), 1.0); unl("MI_H_Cool", (0.22, 0.05, 0.42), 1.1); unl("MI_H_Strut", (0.36, 0.06, 0.34), 1.0)
L("materials ok (%d instances)" % len(MI))
LOOK = {"PIO_DishFront": "MI_Dish", "PIO_DishBack": "MI_DishBack", "PIO_Metal": "MI_Metal", "PIO_Feed": "MI_Feed", "PIO_MLI": "MI_MLI", "PIO_Dark": "MI_Black",
        "PIO_Louver": "MI_Louver", "PIO_Plaque": "MI_Plaque", "PIO_Boom": "MI_Boom", "PIO_RTG": "MI_RTG", "PIO_RTGCore": "MI_RTGCore",
        "TRK_LiveryL": "MI_Livery", "TRK_LiveryR": "MI_Livery", "TRK_White": "MI_Paint", "TRK_Rear": "MI_Paint", "TRK_Trim": "MI_Trim", "TRK_Glass": "MI_Glass",
        "TRK_Tire": "MI_Tire", "TRK_Metal": "MI_Chrome", "TRK_Dark": "MI_DarkPlastic", "TRK_Lamp": "MI_Lamp", "TRK_Tail": "MI_Tail", "TRK_RocketBody": "MI_RocketWhite",
        "TRK_RocketRed": "MI_RocketRed", "TRK_Strap": "MI_Strap", "TRK_Nozzle": "MI_Nozzle", "RD_Dish": "MI_RoofDish", "RD_Metal": "MI_Metal",
        "CAB_Floor": "MI_CabFloor", "CAB_Liner": "MI_CabLiner", "CAB_Panel": "MI_CabPanel", "CAB_Seat": "MI_CabSeat", "CAB_Dash": "MI_CabDash", "CAB_Dark": "MI_DarkPlastic",
        "CAB_Metal": "MI_Chrome", "CAB_Cable": "MI_Cable", "CAB_Mon1": "MI_Mon1", "CAB_Mon2": "MI_Mon2", "CAB_Mon3": "MI_Mon3",
        "PROP_Cup": "MI_Cup", "PROP_CupRed": "MI_CupRed", "PROP_Coffee": "MI_Coffee", "PROP_Paper": "MI_Paper", "PROP_Ball": "MI_Paper",
        "GND_Lot": "MI_Lot", "GND_Grass": "MI_Grass", "GND_Wall": "MI_Wall", "GND_Dark": "MI_GDark", "GND_Glass": "MI_Glass", "GND_Sign": "MI_Sign", "GND_Dish": "MI_RoofDish",
        "GND_Metal": "MI_GMetal", "GND_Lamp": "MI_GLamp", "GND_Car1": "MI_Car1", "GND_Car2": "MI_Car2", "GND_Car3": "MI_Car3", "GND_Car4": "MI_Car4", "GND_Tree": "MI_Tree"}
HEAT = {"PIO_DishFront": "MI_H_Cold", "PIO_DishBack": "MI_H_Cool", "PIO_Metal": "MI_H_Strut", "PIO_Feed": "MI_H_Cold", "PIO_MLI": "MI_H_Warm", "PIO_Dark": "MI_H_WarmDark",
        "PIO_Louver": "MI_H_Aft", "PIO_Plaque": "MI_H_Cool", "PIO_Boom": "MI_H_Cool", "PIO_RTG": "MI_H_Hot", "PIO_RTGCore": "MI_H_Hotter"}

# ------------------------------------------------------------------ the level
les.new_level(MAP) if not eal.does_asset_exist(MAP) else les.load_level(MAP)
for a in eas.get_all_level_actors(): eas.destroy_actor(a)
def spawn(cls, label, loc=(0, 0, 0)):
    a = eas.spawn_actor_from_class(cls, unreal.Vector(*loc), unreal.Rotator(0, 0, 0)); a.set_actor_label(label)
    try: a.root_component.set_mobility(unreal.ComponentMobility.MOVABLE)
    except Exception: pass
    return a
def part(mesh_, mat, label, shadows=True):
    a = eas.spawn_actor_from_object(mesh_, unreal.Vector(0, 0, 0), unreal.Rotator(0, 0, 0)); a.set_actor_label(label)
    c = a.static_mesh_component; c.set_mobility(unreal.ComponentMobility.MOVABLE)
    for i in range(max(1, c.get_num_materials())): c.set_material(i, mat)
    if not shadows: c.set_cast_shadow(False)
    return a
def group(label, prefixes, table=LOOK, shadows=True, only=None):
    root = spawn(unreal.StaticMeshActor, label); n = 0
    for name, m in sorted(MESH.items()):
        key = next((k for k in table if name == k or name.endswith(k) or name == "SM_" + k), None)
        if not key or not any(key.startswith(p) for p in prefixes): continue
        if only and key not in only: continue
        a = part(m, MI[table[key]], label + "_" + key, shadows)
        a.attach_to_actor(root, "", unreal.AttachmentRule.KEEP_WORLD, unreal.AttachmentRule.KEEP_WORLD, unreal.AttachmentRule.KEEP_WORLD, False); n += 1
    L("group %s: %d parts" % (label, n)); return root
ACT = {}
ACT["Pioneer"] = group("Pioneer", ["PIO_"]); ACT["PioneerHeat"] = group("PioneerHeat", ["PIO_"], HEAT, shadows=False)
ACT["Truck"] = group("Truck", ["TRK_"]); ACT["RoofDish"] = group("RoofDish", ["RD_"]); ACT["Cab"] = group("Cab", ["CAB_"])
ACT["Ground"] = group("Ground", ["GND_"])
ACT["Cup"] = group("Cup", ["PROP_Cup", "PROP_Coffee"]) ; ACT["Paper"] = group("Paper", ["PROP_Paper"]); ACT["Ball"] = group("Ball", ["PROP_Ball"])
def single(label, key, mat, shadows=False):
    m = mesh(key)
    if m is None: L("MISSING mesh %s" % key); return spawn(unreal.StaticMeshActor, label)
    return part(m, MI[mat], label, shadows)
ACT["Blob"] = single("Blob", "FX_Smoke", "MI_Coffee")   # a floating coffee droplet (lumpy sphere, scaled down)
ACT["Flame"] = single("Flame", "FX_Flame", "MI_Flame"); ACT["FlameCore"] = single("FlameCore", "FX_FlameCore", "MI_FlameCore")
for i in range(7): ACT["Ring%d" % i] = single("Ring%d" % i, "FX_Ring", "MI_Ring")
for i in range(44): ACT["Arrow%d" % i] = single("Arrow%d" % i, "FX_Arrow", "MI_HeatArrow")
ACT["BigArrow"] = single("BigArrow", "FX_Arrow", "MI_BigArrow")
for i in range(10): ACT["Smoke%d" % i] = single("Smoke%d" % i, "FX_Smoke", "MI_Smoke")
ACT["Sun"] = single("Sun", "SKY_Quad", "MI_Sun"); ACT["Earth"] = single("Earth", "SKY_Quad", "MI_Earth")
ACT["Sky"] = single("Sky", "SKY_Dome", "MI_Sky")
for k in ("SKY_SDw", "SKY_SDb", "SKY_SMw", "SKY_SMb", "SKY_SBw", "SKY_SBb"):
    a = single("Stars_" + k, k, "MI_Star" + k[5:]); a.static_mesh_component.set_mobility(unreal.ComponentMobility.STATIC)
# lights
def light(cls, label, comp_cls, **kw):
    a = spawn(cls, label); c = a.get_component_by_class(comp_cls); c.set_mobility(unreal.ComponentMobility.MOVABLE)
    for k, v in kw.items(): sp(c, k, v)
    return a, c
sun, sunc = light(unreal.DirectionalLight, "SunLight", unreal.DirectionalLightComponent, intensity=float(os.environ.get("PIO_LUX", "6.0")), light_source_angle=0.05,
                  light_color=unreal.Color(255, 250, 242, 255), cast_shadows=True)
sp(sunc, "dynamic_shadow_distance_movable_light", 60000.0)
fill, fillc = light(unreal.DirectionalLight, "FillLight", unreal.DirectionalLightComponent, intensity=float(os.environ.get("PIO_FILL", "1.9")), cast_shadows=False,
                    light_color=unreal.Color(190, 205, 255, 255), specular_scale=0.25)
sp(fillc, "forward_shading_priority", 1)
ACT["SunLight"] = sun; ACT["FillLight"] = fill
ACT["CabLight"], _ = light(unreal.PointLight, "CabLight", unreal.PointLightComponent, intensity=18.0, attenuation_radius=420.0, light_color=unreal.Color(255, 220, 175, 255), cast_shadows=False)
ACT["PlaqueLight"], _ = light(unreal.SpotLight, "PlaqueLight", unreal.SpotLightComponent, intensity=7.0, attenuation_radius=700.0, outer_cone_angle=22.0, inner_cone_angle=10.0,
                              light_color=unreal.Color(255, 236, 210, 255), cast_shadows=True)
ACT["FlameLight"], _ = light(unreal.PointLight, "FlameLight", unreal.PointLightComponent, intensity=3000.0, attenuation_radius=4000.0, light_color=unreal.Color(255, 150, 60, 255), cast_shadows=False)
skyl, skylc = light(unreal.SkyLight, "SkyAmbient", unreal.SkyLightComponent, intensity=0.0, real_time_capture=True)
skyl.set_actor_location(unreal.Vector(*PLAN["G"][:2], PLAN["G"][2] + 300), False, False)
for c in [sunc, fillc]: sp(c, "atmosphere_sun_light", False)
# post: manual exposure, gentle bloom, no post motion blur (MRQ temporal samples give real motion blur)
pp = spawn(unreal.PostProcessVolume, "SpaceLook"); pp.set_editor_property("unbound", True); s = pp.settings
def ov(k, v):
    try: s.set_editor_property("override_" + k, True); s.set_editor_property(k, v)
    except Exception as e: L("pp %s: %r" % (k, str(e)[:80]))
ov("auto_exposure_method", unreal.AutoExposureMethod.AEM_MANUAL); ov("auto_exposure_apply_physical_camera_exposure", False); ov("auto_exposure_bias", float(os.environ.get("PIO_EV", "0")))
ov("bloom_intensity", 0.7); ov("vignette_intensity", 0.32); ov("film_grain_intensity", 0.035); ov("motion_blur_amount", 0.0); ov("lens_flare_intensity", 0.15); ov("scene_fringe_intensity", 0.15)
pp.set_editor_property("settings", s)
# cameras (one per shot)
CAM = {}
for sid, sc in PLAN["scenes"].items():
    for c in sc["cams"]:
        cam = spawn(unreal.CineCameraActor, c["name"]); cc = cam.get_cine_camera_component()
        fb = cc.get_editor_property("filmback"); fb.set_editor_property("sensor_width", 36.0); fb.set_editor_property("sensor_height", 20.25); cc.set_editor_property("filmback", fb)
        cc.set_editor_property("current_focal_length", float(c["lens"])); cc.set_editor_property("current_aperture", float(c["fstop"]))
        fs = cc.get_editor_property("focus_settings"); fs.set_editor_property("manual_focus_distance", float(c["focus"])); cc.set_editor_property("focus_settings", fs)
        CAM[c["name"]] = cam
les.save_current_level(); unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
L("level built: %d actors" % len(eas.get_all_level_actors()))

# ------------------------------------------------------------------ sequences
LIN = unreal.MovieSceneKeyInterpolation.LINEAR; CON = unreal.MovieSceneKeyInterpolation.CONSTANT
def key_channels(chs, rows, N, cuts):
    cutset = set(c - 1 for c in cuts)
    for i, ch in enumerate(chs):
        for k in list(ch.get_keys()): ch.remove_key(k)
        vals = [r[i] for r in rows]
        if all(abs(v - vals[0]) < 1e-6 for v in vals): ch.set_default(vals[0]); ch.add_key(unreal.FrameNumber(0), float(vals[0]), interpolation=LIN); continue
        for f in range(N):
            same_prev = f > 0 and abs(vals[f] - vals[f - 1]) < 1e-6; same_next = f < N - 1 and abs(vals[f] - vals[f + 1]) < 1e-6
            if same_prev and same_next and f not in cutset: continue
            jump = f < N - 1 and (abs(vals[f + 1] - vals[f]) > (800.0 if i < 3 else 90.0))
            ch.add_key(unreal.FrameNumber(f), float(vals[f]), interpolation=CON if (f in cutset or jump) else LIN)
def transform_track(binding, rows, N, cuts):
    tr = binding.add_track(unreal.MovieScene3DTransformTrack); sec = tr.add_section(); sec.set_range(0, N)
    chs = sec.get_all_channels()
    if len(rows[0]) == 6: rows = [r + [1.0, 1.0, 1.0] for r in rows]
    key_channels(chs[:9], rows, N, cuts)
def float_prop(binding, prop, keys, N):
    try:
        tr = binding.add_track(unreal.MovieSceneFloatTrack); tr.set_property_name_and_path(prop, prop); sec = tr.add_section(); sec.set_range(0, N)
        ch = sec.get_all_channels()[0]
        for f, v in keys: ch.add_key(unreal.FrameNumber(int(f)), float(v), interpolation=LIN)
        return True
    except Exception as e: L("float track %s failed %r" % (prop, e)); return False
SEQS = {}
for sid, sc in PLAN["scenes"].items():
    N = sc["frames"]; name = "PS_" + sid; path = ROOT + "/Seq/" + name
    if eal.does_asset_exist(path): eal.delete_asset(path)
    seq = tools.create_asset(name, ROOT + "/Seq", unreal.LevelSequence, unreal.LevelSequenceFactoryNew())
    seq.set_display_rate(unreal.FrameRate(24, 1)); seq.set_playback_start(0); seq.set_playback_end(N)
    bid = lambda b: seq.get_binding_id(b) if hasattr(seq, "get_binding_id") else b.get_binding_id()
    for an, rows in sc["tracks"].items():
        if an not in ACT: L("no actor %s" % an); continue
        transform_track(seq.add_possessable(ACT[an]), rows, N, sc["cuts"])
    cuts_tr = seq.add_track(unreal.MovieSceneCameraCutTrack)
    for c in sc["cams"]:
        b = seq.add_possessable(CAM[c["name"]]); rows = [c["rows"][0]] * c["f0"] + c["rows"] + [c["rows"][-1]] * (N - c["f1"])
        transform_track(b, rows, N, sc["cuts"])
        cs = cuts_tr.add_section(); cs.set_range(c["f0"], c["f1"]); cs.set_camera_binding_id(bid(b))
    # MPC values, every param keyed in every scene
    mt = seq.add_track(unreal.MovieSceneMaterialParameterCollectionTrack); mt.set_editor_property("mpc", mpc)
    ms = mt.add_section(); ms.set_range(0, N)
    for prm in ("SkyAmount", "RTGGlow"): ms.add_scalar_parameter_key(prm, unreal.FrameNumber(0), 0.0)
    chs = {str(c.get_name()).split("_")[0]: c for c in ms.get_all_channels()}
    for prm in ("SkyAmount", "RTGGlow"):
        ch = chs.get(prm)
        if ch is None: L("no mpc channel %s (%s)" % (prm, list(chs))); continue
        for k in list(ch.get_keys()): ch.remove_key(k)
        ks = sc["mpc"].get(prm, [[0, 0.0]])
        for f, v in ks: ch.add_key(unreal.FrameNumber(int(f)), float(v), interpolation=LIN)
    # daylight ambient only on the ground (s03)
    sb = seq.add_possessable(skylc)
    try: sb.set_parent(seq.add_possessable(skyl))
    except Exception: pass
    float_prop(sb, "Intensity", [(0, 1.0), (130, 1.0), (215, 0.25), (262, 0.0)] if sid == "s03" else [(0, 0.0)], N)
    eal.save_loaded_asset(seq); SEQS[sid] = path; L("sequence %s: %d frames, %d tracks, %d cams" % (sid, N, len(sc["tracks"]), len(sc["cams"])))
unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)

# ------------------------------------------------------------------ render
want = [x for x in os.environ.get("PIO_SCENES", ",".join(PLAN["scenes"])).split(",") if x in SEQS]
TEST = os.environ.get("PIO_TEST", "0") == "1"
frames = {}
for item in [x for x in os.environ.get("PIO_FRAMES", "").split(",") if ":" in x]:
    k, v = item.split(":"); frames[k] = [int(q) for q in v.split("+")]
rx, ry = [int(v) for v in os.environ.get("PIO_RES", "1920x1080").split("x")]
qs = unreal.get_editor_subsystem(unreal.MoviePipelineQueueSubsystem); q = qs.get_queue()
for j in list(q.get_jobs()): q.delete_job(j)
jobs = []
for sid in want:
    N = PLAN["scenes"][sid]["frames"]
    ranges = [(f, f + 1) for f in frames.get(sid, [0, N // 2, N - 1])] if TEST else [(int(os.environ.get("PIO_START_" + sid, "0")), N)]
    for a, b in ranges:
        job = q.allocate_new_job(unreal.MoviePipelineExecutorJob); job.sequence = unreal.SoftObjectPath(SEQS[sid]); job.map = unreal.SoftObjectPath(MAP)
        cfg = job.get_configuration()
        out = cfg.find_or_add_setting_by_class(unreal.MoviePipelineOutputSetting); out.output_resolution = unreal.IntPoint(rx, ry)
        out.output_directory = unreal.DirectoryPath(PROJ + "/Saved/MovieRenders/Pio_" + sid + os.environ.get("PIO_OUT", "")); out.file_name_format = "f_{frame_number}"
        if (a, b) != (0, N): out.use_custom_playback_range = True; out.custom_start_frame = a; out.custom_end_frame = b
        cfg.find_or_add_setting_by_class(unreal.MoviePipelineDeferredPassBase); cfg.find_or_add_setting_by_class(unreal.MoviePipelineImageSequenceOutput_PNG)
        aa = cfg.find_or_add_setting_by_class(unreal.MoviePipelineAntiAliasingSetting)
        aa.spatial_sample_count = int(os.environ.get("PIO_SS", "1")); aa.temporal_sample_count = int(os.environ.get("PIO_TS", "2" if TEST else "6"))
        aa.override_anti_aliasing = True; aa.engine_warm_up_count = int(os.environ.get("PIO_WARM", "12" if TEST else "40")); aa.render_warm_up_frames = True
        try:
            cs = cfg.find_or_add_setting_by_class(unreal.MoviePipelineCameraSetting); cs.shutter_timing = unreal.MoviePipelineShutterTiming.FRAME_OPEN
        except Exception as e: L("camera setting %r" % e)
        cv = cfg.find_or_add_setting_by_class(unreal.MoviePipelineConsoleVariableSetting)
        for k, v in (("r.Streaming.FullyLoadUsedTextures", 1), ("r.TextureStreaming", 0)): cv.add_or_update_console_variable(k, v)
        jobs.append("%s[%d:%d]" % (sid, a, b))
L("queue: %s" % jobs)
if os.environ.get("PIO_NORENDER") == "1":
    L("build only, quitting"); unreal.SystemLibrary.quit_editor()
else:
    ex = qs.render_queue_with_executor(unreal.MoviePipelinePIEExecutor)
    def done(executor, success): L("render finished success=%s" % success); unreal.SystemLibrary.quit_editor()
    ex.on_executor_finished_delegate.add_callable_unique(done)
    L("render started (%d jobs)" % len(jobs))
