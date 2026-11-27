"""Nothing-inspired product studio. Blender 5.3, headless Cycles.

Usage:
  Blender --background --python render/render_keyboard.py -- --preview
  Blender --background outputs/renders/keyboard-studio-v05.blend --python render/render_keyboard.py -- --final

Actual keyboard geometry is imported from the approved GLB. Hangul legends,
grid, indicator and PCB surface artwork are editable render-only additions.
"""
import argparse
import json
import math
import sys
from pathlib import Path
import bpy
from mathutils import Vector, Matrix
from bpy_extras.object_utils import world_to_camera_view

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'outputs/renders-white'
OUT.mkdir(parents=True, exist_ok=True)
GLB = ROOT / 'outputs/exports/hangul-card-review-v02.glb'
PHONE_GLB = ROOT / 'outputs/exports/iphone16-keyboard-attached-v02.glb'
BLEND = OUT / 'keyboard-studio-v05.blend'
MM = .001
SAMPLES = 256
PREVIEW_SAMPLES = 32
PREVIEW_SIZE = 1000
LENS_MM = 85
GLYPH_PITCH = .00052
DOT_RADIUS = .00020
PRINT_Z = .005807
COLOR_HEX = {'shell':'F3F3F0','pcb':'101A18','ink':'202020','metal':'BAC1C5',
             'copper':'B8A38D','red':'F3F3F0','floor':'DADAD8','glass':'EDF3F6'}


def rgb(value):
    vals=[int(value[i:i+2],16)/255 for i in (0,2,4)]
    return tuple(c/12.92 if c<.04045 else ((c+.055)/1.055)**2.4 for c in vals)


def mat(name, color, rough=.4, metal=0, transmission=0, ior=1.49, texture=False):
    m=bpy.data.materials.new(name);m.use_nodes=True
    n=m.node_tree.nodes.get('Principled BSDF')
    n.inputs['Base Color'].default_value=(*rgb(color),1)
    n.inputs['Roughness'].default_value=rough
    n.inputs['Metallic'].default_value=metal
    n.inputs['IOR'].default_value=ior
    n.inputs['Transmission Weight'].default_value=transmission
    if metal:
        n.inputs['Anisotropic'].default_value=.32
    if texture:
        noise=m.node_tree.nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=190
        noise.inputs['Detail'].default_value=2
        tex=m.node_tree.nodes.new('ShaderNodeTexCoord')
        bump=m.node_tree.nodes.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.14;bump.inputs['Distance'].default_value=.000012
        m.node_tree.links.new(tex.outputs['Generated'],noise.inputs['Vector'])
        m.node_tree.links.new(noise.outputs['Fac'],bump.inputs['Height'])
        m.node_tree.links.new(bump.outputs['Normal'],n.inputs['Normal'])
    return m


def assign(o,m):
    o.data.materials.clear();o.data.materials.append(m)


def optical_bond():
    """Bonded inner films have no extra air/glass interface in the beauty pass."""
    m=bpy.data.materials.new('Bonded_Optical_Films');m.use_nodes=True
    n=m.node_tree.nodes;n.clear();surface=n.new('ShaderNodeBsdfTransparent');out=n.new('ShaderNodeOutputMaterial')
    m.node_tree.links.new(surface.outputs[0],out.inputs['Surface']);return m


def flatten(objects):
    bpy.context.view_layer.update()
    for o in objects:
        world=o.matrix_world.copy();o.parent=None
        if o.type=='MESH':
            # CAD GLB instances carry a 0.001 unit scale. Bake a private mesh
            # so normals, bevel widths and later offsets use actual meters.
            o.data=o.data.copy();o.data.transform(world);o.matrix_world=Matrix.Identity(4)
        else:
            o.matrix_world=world


def cylinder(name, x,y,z,r,depth,material,vertices=32):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices,radius=r,depth=depth,location=(x,y,z+depth/2))
    o=bpy.context.object;o.name=name;assign(o,material);return o


def line(name,points,radius,material):
    curve=bpy.data.curves.new(name,'CURVE');curve.dimensions='3D';curve.resolution_u=2
    sp=curve.splines.new('POLY');sp.points.add(len(points)-1)
    for p,v in zip(sp.points,points):p.co=(*v,1)
    curve.bevel_depth=radius;curve.bevel_resolution=2
    o=bpy.data.objects.new(name,curve);bpy.context.scene.collection.objects.link(o)
    o.data.materials.append(material);return o


def role(name):
    if name.startswith('legend_') or name.startswith('Hangul_') or name.startswith('Grid_') or name.startswith('Status_'):
        return 'cover'
    if 'top_cover' in name or 'finish_with' in name or name=='top_frame' or name.startswith('screw_'):return 'cover'
    if 'touch_sensor' in name or name=='perimeter_bond':return 'touch'
    if name.startswith(('dome_','actuator_')):return 'domes'
    if name.startswith(('pcb_','Trace_','Silk_','Pad_')):return 'pcb'
    if 'magnet' in name:return 'magnet'
    if name.startswith(('lipo_','ble_','touch_ic','usb_c','battery_mount','ble_mount','ic_mount')):return 'electronics'
    return 'shell'


PATTERNS={
 'siot':['000010000','000101000','001000100','010000010','100000001'],
 'u':['111111111','000010000','000010000','000010000','000010000','000010000'],
 'giyeok':['111111111','000000001','000000001','000000001','000000001','000000001','000000001','000000001','000000001'],
 'a':['10000','10000','10000','10000','11111','10000','10000','10000','10000'],
 'ieung':['001111100','010000010','100000001','100000001','100000001','100000001','100000001','010000010','001111100'],
 'eo':['00001','00001','00001','00001','11111','00001','00001','00001','00001'],
 'nieun':['100000000','100000000','100000000','100000000','100000000','100000000','100000000','100000000','111111111'],
 'o':['000010000','000010000','000010000','000010000','000010000','111111111'],
 'mieum':['111111111','100000001','100000001','100000001','100000001','100000001','100000001','100000001','111111111'],
}
GLYPHS=[('siot','ㅅ',-18,18),('u','ㅜ',0,18),('giyeok','ㄱ',18,18),
        ('a','ㅏ',-18,0),('ieung','ㅇ',0,0),('eo','ㅓ',18,0),
        ('nieun','ㄴ',-18,-18),('o','ㅗ',0,-18),('mieum','ㅁ',18,-18)]


def make_camera(scene, location, target, fit_objects, aspect, fill=.76, dof=False):
    d=bpy.data.cameras.new(scene.name+'_85mm');cam=bpy.data.objects.new(scene.name+'_Camera',d)
    scene.collection.objects.link(cam);scene.camera=cam;cam.location=location
    target=Vector(target);d.lens=LENS_MM;d.clip_start=.001;d.clip_end=10
    cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
    scene.render.resolution_x=aspect[0];scene.render.resolution_y=aspect[1]
    bpy.context.view_layer.update()
    pts=[o.matrix_world@Vector(p) for o in fit_objects if o.type=='MESH' and not o.hide_render for p in o.bound_box]
    for _ in range(5):
        xy=[world_to_camera_view(scene,cam,p) for p in pts]
        maxdev=max(max(abs(p.x-.5)*2,abs(p.y-.5)*2) for p in xy)
        cam.location=target+(cam.location-target)*(maxdev/fill)
        bpy.context.view_layer.update()
    if dof:
        focus=bpy.data.objects.new('Hero_Focus',None);scene.collection.objects.link(focus);focus.location=target
        d.dof.use_dof=True;d.dof.focus_object=focus;d.dof.aperture_fstop=11
    return cam


def area(scene,name,loc,target,power,size,color=(1,1,1),ratio=1):
    d=bpy.data.lights.new(name,'AREA');d.energy=power;d.shape='RECTANGLE';d.size=size;d.size_y=size*ratio;d.color=color
    o=bpy.data.objects.new(name,d);scene.collection.objects.link(o);o.location=loc
    o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
    return o


def studio(scene,z=0):
    w=bpy.data.worlds.new(scene.name+'_NeutralWorld');w.use_nodes=True
    w.node_tree.nodes['Background'].inputs['Color'].default_value=(.82,.84,.86,1)
    w.node_tree.nodes['Background'].inputs['Strength'].default_value=.20;scene.world=w
    area(scene,'Key_Softbox',(-.13,-.10,.23+z),(0,0,z),1.5,.19,(1,.98,.96),1.35)
    area(scene,'Cool_Rim',(.09,.14,.17+z),(0,0,z+.015),1,.14,(.84,.91,1),.35)
    area(scene,'Bounce_Fill',(.16,-.04,.11+z),(0,0,z),.4,.17,(1,1,1),1.3)
    area(scene,'Strip_Reflection',(-.05,.11,.22+z),(0,0,z),.5,.20,(1,1,1),.12)
    # A large flat cyclorama fills the complete view, with no visible horizon.
    bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.00012))
    floor=bpy.context.object;floor.name='Studio_Cyclorama';assign(floor,MATS['floor'])
    scene.render.engine='CYCLES';scene.cycles.device='GPU';scene.cycles.samples=SAMPLES
    scene.cycles.use_denoising=True;scene.cycles.use_adaptive_sampling=True
    scene.cycles.adaptive_threshold=.012;scene.cycles.adaptive_min_samples=32
    scene.cycles.max_bounces=16;scene.cycles.transmission_bounces=16
    scene.cycles.transparent_max_bounces=12
    scene.cycles.sample_clamp_indirect=4
    scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA'
    scene.render.image_settings.color_depth='8';scene.render.film_transparent=False
    scene.render.resolution_percentage=100
    scene.view_settings.view_transform='AgX'
    scene.view_settings.look='AgX - Medium High Contrast';scene.view_settings.exposure=-.5
    scene.render.use_file_extension=True


def build():
    global MATS
    bpy.ops.wm.read_factory_settings(use_empty=True)
    pref=bpy.context.preferences.addons['cycles'].preferences;pref.compute_device_type='METAL';pref.get_devices()
    for d in pref.devices:d.use=d.type=='METAL'
    MATS={
      'shell':mat('PC_OffWhite_Sandblast',COLOR_HEX['shell'],.46,texture=True),
      'pcb':mat('PCB_GreenBlack_Matte',COLOR_HEX['pcb'],.6),
      'metal':mat('Brushed_Steel',COLOR_HEX['metal'],.23,1,texture=True),
      'magnet':mat('Silver_Magnet', 'B9BEC2',.29,1),
      'ink':mat('White_Printed_Ink',COLOR_HEX['ink'],.46),
      'copper':mat('Exposed_Copper_Desaturated',COLOR_HEX['copper'],.34,.92),
      'red':mat('Status_White',COLOR_HEX['red'],.28),
      'black':mat('Module_Matte_Black','141616',.58),
      'pad':mat('Back_Contact_Pad','878B8B',.72),
      'battery':mat('Battery_Silver_Pouch','B7BCBD',.43,.78),
      'glass':mat('Opaque_White_Touch_Face','F3F3F0',.12,0,0,1.49),
      'frost':mat('Opaque_White_Edges','F3F3F0',.25,0,0,1.49),
      'sensor':mat('Clear_Touch_Flex','FAFCFD',.08,0,1,1.49),
      'floor':mat('Light_Grey_Studio',COLOR_HEX['floor'],.38),
      'phone':mat('Phone_Dark_Silhouette','292D2E',.4),
      'bond':optical_bond(),
    }
    MATS['ink'].node_tree.nodes.get('Principled BSDF').inputs['Specular IOR Level'].default_value=0
    bpy.ops.import_scene.gltf(filepath=str(GLB))
    imported=[o for o in bpy.context.scene.objects if o.type=='MESH'];assert len(imported)==49
    flatten(imported)
    for o in imported:
        short=o.name.rsplit('/',1)[-1];o.name=short;o['cad_source_name']=short;o['role']=role(short)
        if short.startswith('legend_'):
            o.hide_render=True;o.hide_viewport=True;continue
        if 'top_cover' in short:
            assign(o,MATS['glass']);o.data.materials.append(MATS['frost'])
            for poly in o.data.polygons:
                n=(o.matrix_world.to_3x3()@poly.normal).normalized()
                poly.material_index=0 if abs(n.z)>.85 else 1
                if abs(n.z)>.85:poly.use_smooth=False
            bevel=o.modifiers.new('Optical_Edge_Highlight','BEVEL');bevel.width=.000035;bevel.segments=3;bevel.limit_method='ANGLE';bevel.material=1
        elif 'finish_with' in short or 'touch_sensor' in short or 'dome_carrier' in short:assign(o,MATS['bond'])
        elif short=='top_frame':assign(o,MATS['glass'])
        elif short=='bottom_shell':assign(o,MATS['shell'])
        elif short.startswith('pcb_'):assign(o,MATS['pcb'])
        elif short.startswith('screw_'):assign(o,MATS['shell'])
        elif short.startswith('dome_'):assign(o,MATS['metal'])
        elif short.startswith('actuator_'):assign(o,MATS['frost'])
        elif 'magnet' in short:assign(o,MATS['magnet'] if 'ring_envelope' in short else MATS['pad'])
        elif short.startswith('lipo_'):assign(o,MATS['battery'])
        elif short.startswith('usb_c'):assign(o,MATS['metal'])
        elif short=='phone_contact_pad':assign(o,MATS['pad'])
        else:assign(o,MATS['black'])
    # Sparse, supported surface artwork on the existing PCB row rails.
    for row,yy in enumerate((-.018,0,.018)):
        for lane,dy in enumerate((-.0023,-.0018,.0018,.0023)):
            pts=[(-.023,yy+dy,.004317),(-.017,yy+dy,.004317),(-.015,yy+dy*.65,.004317),(.015,yy+dy*.65,.004317),(.017,yy+dy,.004317),(.023,yy+dy,.004317)]
            o=line(f'Trace_row{row}_lane{lane}',pts,.000035,MATS['copper']);o['role']='pcb'
        for x in (-.022,-.012,.012,.022):
            o=cylinder(f'Pad_row{row}_{x}',x,yy,.004303,.00025,.000015,MATS['copper']);o['role']='pcb'
        for x in (-.023,-.011,.011,.023):
            o=line(f'Silk_row{row}_{x}',[(x,yy-.0027,.00432),(x+.0006,yy-.0027,.00432)],.000035,MATS['ink']);o['role']='pcb'
    # Nine glyph groups, with a separate mesh object for every printed dot.
    for name,char,x,y in GLYPHS:
        parent=bpy.data.objects.new(f'Hangul_{name}_{char}',None);bpy.context.scene.collection.objects.link(parent)
        parent['glyph']=char;pattern=PATTERNS[name]
        for row,st in enumerate(pattern):
            for col,val in enumerate(st):
                if val!='1':continue
                xx=x*MM+(col-(len(st)-1)/2)*GLYPH_PITCH
                yy=y*MM+((len(pattern)-1)/2-row)*GLYPH_PITCH
                o=cylinder(f'Hangul_{name}_dot_{row:02d}_{col:02d}',xx,yy,PRINT_Z,DOT_RADIUS,.000007,MATS['ink'],20)
                o['role']='cover';o['glyph']=char
                world=o.matrix_world.copy();o.parent=parent;o.matrix_world=world
    for axis in ('x','y'):
        for at in (-.009,.009):
            pts=[(at,-.027,PRINT_Z),(at,.027,PRINT_Z)] if axis=='x' else [(-.027,at,PRINT_Z),(.027,at,PRINT_Z)]
            o=line(f'Grid_{axis}_{at}',pts,.000035,MATS['ink']);o['role']='cover'
    o=line('Grid_Perimeter',[(-.027,-.027,PRINT_Z),(.027,-.027,PRINT_Z),(.027,.027,PRINT_Z),(-.027,.027,PRINT_Z),(-.027,-.027,PRINT_Z)],.000035,MATS['ink']);o['role']='cover'
    led=cylinder('Status_White_Dot',0,.037,.005807,.00055,.00008,MATS['red'],48);led['role']='cover'
    card_objects=[o for o in bpy.context.scene.objects if o.type in ('MESH','CURVE')]
    # Flatten newly created dot parents before per-shot copies and transforms.
    flatten(card_objects)
    before=set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=str(PHONE_GLB))
    new=[o for o in bpy.data.objects if o not in before]
    phone_objects=[o for o in new if o.type=='MESH' and any(s in o.name for s in ('iphone16_body_','camera_island_','illustrative_lens_'))]
    assert len(phone_objects)==4,len(phone_objects);flatten(phone_objects)
    for o in new:
        if o not in phone_objects:bpy.data.objects.remove(o,do_unlink=True)
    for o in phone_objects:
        assign(o,MATS['phone'] if 'lens_' not in o.name else MATS['black']);o['role']='phone';o.hide_render=True
    hero=bpy.context.scene;hero.name='01 Hero'
    base=[*card_objects,*phone_objects]
    for o in list(hero.objects):
        if o.type=='EMPTY':bpy.data.objects.remove(o,do_unlink=True)
    specs=[
      ('01 Hero','01-hero-v05',(3000,2400),(.16,-.22,.24),(0,0,.003),True,False),
      ('02 Top','02-top-v05',(2400,3000),(0,0,.33),(0,0,.004),False,False),
      ('03 Exploded','03-exploded-v05',(3000,3000),(.24,.30,.25),(0,0,.045),False,True),
      ('04 Attached','04-attached-v05',(2400,3000),(.12,-.23,.35),(0,0,.002),False,False),
    ]
    records=[]
    for index,(name,filename,aspect,camloc,target,dof,exploded) in enumerate(specs):
        scene=hero if index==0 else bpy.data.scenes.new(name)
        bpy.context.window.scene=scene
        if index==0:objects=base
        else:
            objects=[]
            for source in base:
                o=source.copy();scene.collection.objects.link(o);objects.append(o)
        attached=index==3
        for o in objects:
            r=o.get('role','shell')
            source_name=o.get('cad_source_name','')
            if r=='phone':o.hide_render=not attached
            elif attached:o.location.y-=.012
            # A bonded optical stack has one external optical interface. Keep
            # the original films editable, but omit their coincident inner
            # surfaces in assembled beauty passes; reveal them when separated.
            if any(t in source_name for t in ('finish_with','touch_sensor','dome_carrier')):
                o.hide_render=not exploded or 'finish_with' in source_name
                if exploded and 'finish_with' not in source_name:
                    o.material_slots[0].link='OBJECT';o.material_slots[0].material=MATS['sensor']
            if exploded:
                o.location.z+={'shell':0,'magnet':.012,'electronics':.022,'pcb':.037,'domes':.053,'touch':.068,'cover':.085}.get(r,0)
        # Lift the complete attached assembly so the front face of the phone
        # rests on the studio floor. Its back and the keyboard face the camera.
        if attached:
            for o in objects:o.location.z+=.0078
        for _,char,_,_ in GLYPHS:
            collection=bpy.data.collections.new(scene.name+' / Legend '+char)
            scene.collection.children.link(collection)
            for o in objects:
                if o.get('glyph')!=char:continue
                for previous in list(o.users_collection):previous.objects.unlink(o)
                collection.objects.link(o)
        studio(scene,.035 if exploded else 0)
        if attached:
            for light in scene.objects:
                if light.type!='LIGHT':continue
                if light.name.startswith('Strip_Reflection'):light.data.energy*=.1
                elif light.name.startswith('Cool_Rim'):light.data.energy*=.3
        fit=[o for o in objects if not o.hide_render]
        make_camera(scene,camloc,target,fit,aspect,.78 if not exploded else .80,dof)
        scene['output_name']=filename;scene['final_width']=aspect[0];scene['final_height']=aspect[1]
        scene.render.filepath=str(OUT/(filename+'.png'))
        records.append({'scene':name,'file':filename+'.png','size':aspect,'samples':SAMPLES,'lens_mm':LENS_MM})
    bpy.context.window.scene=hero
    bpy.ops.wm.save_as_mainfile(filepath=str(BLEND),compress=True)
    bpy.ops.object.select_all(action='DESELECT')
    for o in hero.objects:
        if o.type in ('MESH','CURVE') and o.get('role')!='phone' and ('role' in o):o.select_set(not o.hide_render)
    bpy.ops.export_scene.gltf(filepath=str(ROOT/'outputs/exports/hangul-card-white-v05.glb'),use_selection=True,export_apply=True)
    report={'source_glb':str(GLB.relative_to(ROOT)),'cad_source_meshes':49,'render_style':'solid white opaque body and smooth touch face; neutral grey legends for readability; no red accent',
      'skill':'kevinbadi/blender-skills/product-polish, custom headless Cycles adaptation','skill_commit':'b2f0f816d320b56ae86d52597a35284e0e6cc929',
      'shots':records,'legend_layout':[[g[1],g[2],g[3]] for g in GLYPHS],
      'render_only_additions':['Hangul printed dots replacing graphic symbols','thin white zone grid','one red status dot','illustrative PCB traces, pads and silkscreen','35 micrometer cover highlight bevel','opaque top face material revision; geometry unchanged'],
      'optical_stack':'Coincident bonded finish/sensor/carrier interfaces are omitted in assembled beauty passes; individual film meshes remain editable and sensor/carrier appear in exploded view.',
      'limits':['Surface traces are illustrative, not routed electronics','Attached phone and camera details remain schematic','No physical print/charging/force validation is implied','Appearance review retains 5.8 mm CAD geometry. New 2.99 mm thickness target requires structural redesign; this is not a 3 mm engineering model. Screen-like finish is passive, not an active display.']}
    (OUT/'render-settings-v05.json').write_text(json.dumps(report,indent=2,ensure_ascii=False))


def render(preview, shots, cpu=False):
    if not cpu:
        pref=bpy.context.preferences.addons['cycles'].preferences;pref.compute_device_type='METAL';pref.get_devices()
        for d in pref.devices:d.use=d.type=='METAL'
    for scene in sorted(bpy.data.scenes,key=lambda s:s.name):
        if 'output_name' not in scene:continue
        if shots and scene['output_name'].split('-')[0] not in shots:continue
        bpy.context.window.scene=scene
        scene.cycles.device='CPU' if cpu else 'GPU'
        w,h=scene['final_width'],scene['final_height']
        if preview:
            scale=PREVIEW_SIZE/max(w,h);scene.render.resolution_x=round(w*scale);scene.render.resolution_y=round(h*scale)
            scene.cycles.samples=PREVIEW_SAMPLES;scene.cycles.adaptive_min_samples=16
            folder=OUT/'previews';folder.mkdir(exist_ok=True)
        else:
            scene.render.resolution_x=w;scene.render.resolution_y=h;scene.cycles.samples=SAMPLES;scene.cycles.adaptive_min_samples=32
            folder=OUT
        scene.render.filepath=str(folder/(scene['output_name']+'.png'))
        print('RENDER_START',scene.name,scene.render.filepath,flush=True)
        bpy.ops.render.render(write_still=True)
        print('RENDER_DONE',scene.name,flush=True)


if __name__=='__main__':
    args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
    parser=argparse.ArgumentParser();parser.add_argument('--preview',action='store_true');parser.add_argument('--final',action='store_true');parser.add_argument('--shots',nargs='*')
    parser.add_argument('--reuse',action='store_true');parser.add_argument('--cpu',action='store_true');parser.add_argument('--preview-size',type=int,default=1000)
    opt=parser.parse_args(args)
    PREVIEW_SIZE=opt.preview_size
    if not opt.final and not opt.reuse:build()
    render(not opt.final,opt.shots,opt.cpu)
