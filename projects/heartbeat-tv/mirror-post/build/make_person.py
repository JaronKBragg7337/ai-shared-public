# Blender script: builds the person (CC0 MakeHuman/MPFB generator) and saves build/person.blend.
#   blender -b --python build/make_person.py
import bpy, os, sys
from bl_ext.user_default.mpfb.services.humanservice import HumanService
from bl_ext.user_default.mpfb.services.locationservice import LocationService
from bl_ext.user_default.mpfb.services.assetservice import AssetService

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = LocationService.get_user_data()
def A(*p): return os.path.join(DATA, *p)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.preferences.addon_enable(module='bl_ext.user_default.mpfb') if 'bl_ext.user_default.mpfb' not in bpy.context.preferences.addons else None
AssetService.update_all_asset_lists()

macro = {"gender": 1.0, "age": 0.5, "muscle": 0.6, "weight": 0.38, "proportions": 0.6, "height": 0.55,
         "cupsize": 0.5, "firmness": 0.5, "race": {"asian": 0.34, "caucasian": 0.33, "african": 0.33}}
base = HumanService.create_human(scale=0.1, macro_detail_dict=macro)
base.name = 'Person'
rig = HumanService.add_builtin_rig(base, 'default')
rig = rig or [o for o in bpy.data.objects if o.type == 'ARMATURE'][0]
rig.name = 'Rig'
print('BONES', [b.name for b in rig.data.bones if any(k in b.name.lower() for k in ('arm', 'shoulder', 'clav'))])

HumanService.set_character_skin(A('skins', 'young_caucasian_male', 'young_caucasian_male.mhmat'), base, skin_type='ENHANCED_SSS')
parts = [
    ('eyes', A('eyes', 'high-poly', 'high-poly.mhclo'), 'Eyes', 'PROCEDURAL_EYES'),
    ('brows', A('eyebrows', 'eyebrow012', 'eyebrow012.mhclo'), 'Eyebrows', 'MAKESKIN'),
    ('lashes', A('eyelashes', 'eyelashes02', 'eyelashes02.mhclo'), 'Eyelashes', 'MAKESKIN'),
    ('hair', A('hair', 'short02', 'short02.mhclo'), 'Hair', 'MAKESKIN'),
    ('teeth', A('teeth', 'teeth_base', 'teeth_base.mhclo'), 'Teeth', 'MAKESKIN'),
    ('shirt', A('clothes', 'male_casualsuit02', 'male_casualsuit02.mhclo'), 'Clothes', 'MAKESKIN'),
]
for key, path, typ, mat in parts:
    ob = HumanService.add_mhclo_asset(path, base, asset_type=typ, subdiv_levels=1, material_type=mat)
    ob.name = 'P_' + key
    print('ADDED', key, ob.name, [m.name for m in ob.data.materials])

sub = base.modifiers.new('Subdivision', 'SUBSURF'); sub.levels = 1; sub.render_levels = 2
# arms down at the sides (the generator's rest pose holds them out)
import math
from mathutils import Matrix
bpy.context.view_layer.update()
def swing(name, deg):
    pb = rig.pose.bones[name]
    head = rig.matrix_world @ pb.head
    R = Matrix.Translation(head) @ Matrix.Rotation(math.radians(deg), 4, 'Y') @ Matrix.Translation(-head)
    pb.matrix = rig.matrix_world.inverted() @ R @ rig.matrix_world @ pb.matrix
    bpy.context.view_layer.update()
ARM = float(os.environ.get('ARM_DEG', '36'))
for side, sg in (('.L', 1), ('.R', -1)):
    swing('shoulder01' + side, sg * 9)
    swing('upperarm01' + side, sg * (ARM - 9))
for ob in bpy.data.objects:
    print('OBJ', ob.name, ob.type, tuple(round(v, 3) for v in ob.dimensions), [m.name for m in ob.modifiers])
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(HERE, 'person.blend'))
print('SAVED')
