"""Convert the corrected white GLB; keep mesh coordinates in mm for OBJ/STL/PLY."""
import bpy,json,shutil
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'outputs/exports/white-v05';OUT.mkdir(exist_ok=True)
source=OUT/'keyboard-white-v05.glb'
blend=ROOT/'outputs/renders-white/keyboard-studio-v05.blend'
if not blend.exists():blend=ROOT/'outputs/keyboard-white-v05/outputs/renders-white/keyboard-studio-v05.blend'
bpy.ops.wm.open_mainfile(filepath=str(blend))
bpy.context.window.scene=bpy.data.scenes['01 Hero'];bpy.context.view_layer.update()
bpy.ops.object.select_all(action='DESELECT')
allowed={'cover','touch','domes','pcb','magnet','electronics','shell'}
for o in bpy.context.scene.objects:
 if o.type in ('MESH','CURVE') and o.get('role') in allowed and not o.hide_render:o.select_set(True)
bpy.ops.export_scene.gltf(filepath=str(source),use_selection=True,use_active_scene=True,export_apply=True)
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(source))
bpy.context.scene.unit_settings.system='METRIC';bpy.context.scene.unit_settings.scale_length=1
bpy.context.view_layer.update()
def bounds_mm(objects,unit=1000):
 pts=[o.matrix_world@Vector(v) for o in objects if o.type=='MESH' for v in o.bound_box]
 return [(max(p[i] for p in pts)-min(p[i] for p in pts))*unit for i in range(3)]
original=bounds_mm(bpy.context.scene.objects);count=len([o for o in bpy.context.scene.objects if o.type=='MESH'])
base=OUT/'keyboard-white-v05'
bpy.ops.wm.obj_export(filepath=str(base.with_suffix('.obj')),global_scale=1000,forward_axis='Y',up_axis='Z',export_materials=True)
bpy.ops.wm.stl_export(filepath=str(base.with_suffix('.stl')),global_scale=1000,forward_axis='Y',up_axis='Z')
bpy.ops.wm.ply_export(filepath=str(base.with_suffix('.ply')),global_scale=1000,forward_axis='Y',up_axis='Z')
bpy.ops.export_scene.fbx(filepath=str(base.with_suffix('.fbx')),axis_forward='-Y',axis_up='Z',add_leaf_bones=False,bake_anim=False)
bpy.ops.export_scene.gltf(filepath=str(base.with_suffix('.gltf')),export_format='GLTF_SEPARATE')

shutil.copyfile(ROOT/'outputs/exports/hangul-card-review-v02.step',OUT/'keyboard-structure-review-v02.step')
# Reimport each mesh format to check geometry survives and units are documented.
checks=[]
for ext in ['obj','stl','ply','fbx','gltf']:
 bpy.ops.wm.read_factory_settings(use_empty=True)
 path=str(base.with_suffix('.'+ext))
 if ext=='obj':bpy.ops.wm.obj_import(filepath=path,forward_axis='Y',up_axis='Z')
 elif ext=='stl':bpy.ops.wm.stl_import(filepath=path,forward_axis='Y',up_axis='Z')
 elif ext=='ply':bpy.ops.wm.ply_import(filepath=path,forward_axis='Y',up_axis='Z')
 elif ext=='fbx':bpy.ops.import_scene.fbx(filepath=path)
 else:bpy.ops.import_scene.gltf(filepath=path)
 bpy.context.view_layer.update();b=bounds_mm(bpy.context.scene.objects,1 if ext in ['obj','stl','ply'] else 1000)
 assert all(abs(a-z)<.02 for a,z in zip(original,b)),(ext,original,b)
 checks.append({'format':ext,'bounds_mm':b,'meshes':len([o for o in bpy.context.scene.objects if o.type=='MESH']),'round_trip_bounds_pass':True})
report={'source_glb':source.name,'source_mesh_count':count,'source_bounds_mm':original,'axis':'+Z up','body_nominal_mm':[60,90,5.8],'appearance_details':'Printed dots and status proxy may extend beyond nominal body thickness.','checks':checks,'scope':'File conversion and round-trip bounds only; no physical or printability validation.'}
(OUT/'conversion-checks.json').write_text(json.dumps(report,indent=2))
print('FORMAT_EXPORT_OK',json.dumps(report),flush=True)
