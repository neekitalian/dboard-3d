import bpy,json
from mathutils import Vector
from pathlib import Path
records=[]
for s in bpy.data.scenes:
 if 'output_name' not in s:continue
 bpy.context.window.scene=s;bpy.context.view_layer.update()
 cad=[o for o in s.objects if 'cad_source_name' in o]
 glyphs={o.get('glyph') for o in s.objects if o.get('glyph')}
 checks={'cycles':s.render.engine=='CYCLES','samples_256':s.cycles.samples==256,'long_edge_3000':max(s.render.resolution_x,s.render.resolution_y)==3000,'lens_85mm':s.camera.data.lens==85,'denoising':s.cycles.use_denoising,'agx':s.view_settings.view_transform=='AgX','nine_hangul':glyphs==set('ㅅㅜㄱㅏㅇㅓㄴㅗㅁ')}
 for glyph,stem_col in [('ㅏ',0),('ㅓ',4)]:
  dots=[o for o in s.objects if o.type=='MESH' and o.get('glyph')==glyph]
  center_y=lambda o:(o.matrix_world @ (sum((v.co for v in o.data.vertices),Vector())/len(o.data.vertices))).y
  ys=[center_y(o) for o in dots]
  midpoint=(min(ys)+max(ys))/2
  arms=[o for o in dots if '_dot_04_' in o.name and int(o.name.split('_dot_04_')[1].split('.')[0])!=stem_col]
  assert len(arms)==4
  print(s.name,glyph,'mid',midpoint,'arms',[center_y(o) for o in arms],flush=True)
  assert all(abs(center_y(o)-midpoint)<1e-7 for o in arms)
 checks['vowel_arms_centered']=True
 records.append({'scene':s.name,'source_mesh_count':len(cad),'glyphs':sorted(glyphs),'checks':checks})
 assert all(checks.values()),records[-1]
assert len(records)==4
(Path(__file__).resolve().parents[1]/'outputs/renders-white/validation-v05.json').write_text(json.dumps({'scenes':records,'scope':'Scene configuration and editable glyph checks. Final image review is separate; no physical validation.'},indent=2,ensure_ascii=False))
print('VALIDATED',len(records),'scenes')
