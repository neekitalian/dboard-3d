import bpy,json
from pathlib import Path
records=[]
for s in bpy.data.scenes:
 if 'output_name' not in s:continue
 cad=[o for o in s.objects if 'cad_source_name' in o]
 glyphs={o.get('glyph') for o in s.objects if o.get('glyph')}
 checks={'cycles':s.render.engine=='CYCLES','samples_256':s.cycles.samples==256,'long_edge_3000':max(s.render.resolution_x,s.render.resolution_y)==3000,'lens_85mm':s.camera.data.lens==85,'denoising':s.cycles.use_denoising,'agx':s.view_settings.view_transform=='AgX','nine_hangul':glyphs==set('ㅅㅜㄱㅏㅇㅓㄴㅗㅁ')}
 records.append({'scene':s.name,'source_mesh_count':len(cad),'glyphs':sorted(glyphs),'checks':checks})
 assert all(checks.values()),records[-1]
assert len(records)==4
(Path(__file__).resolve().parents[1]/'outputs/renders-opaque/validation-v04.json').write_text(json.dumps({'scenes':records,'scope':'Scene configuration and editable glyph checks. Final image review is separate; no physical validation.'},indent=2,ensure_ascii=False))
print('VALIDATED',len(records),'scenes')
