"""Export actual CAD surface tessellation for Anatomy, not a replacement model."""
import json, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
import build123d as bd
from cad.build123d import leaves
import hangul_card as c
import phone_comparison as p

out=Path(__file__).resolve().parents[1]/'outputs/anatomy'
out.mkdir(parents=True,exist_ok=True)
def meshes(tree):
    result=[]
    for s in leaves(tree):
        vs,fs=s.tessellate(0.08,0.25)
        bb=s.bounding_box()
        result.append({'name':s.label,'vertices':[[round(v.X,6),round(v.Y,6),round(v.Z,6)] for v in vs],
          'triangles':fs,'center':list(bb.center()),'bounds':{'min':list(bb.min),'max':list(bb.max)}})
    return result
data={'units':'mm','card':meshes(c.assembly().shape),'phone':meshes(p.iphone16_reference().shape),
      'dimensions':{'card':[c.WIDTH,c.LENGTH,c.HEIGHT],'phone':[p.PHONE_W,p.PHONE_L,p.PHONE_T]},
      'source':'src/hangul_card.py, src/phone_comparison.py; CAD tessellation 0.08 mm / 0.25 rad',
      'phone_source':'https://support.apple.com/en-gb/121029',
      'limits':'Phone details schematic; charging, forces and print failures remain unverified.'}
(out/'cad-parts-v02.json').write_text(json.dumps(data,separators=(',',':')))
print('exported',len(data['card']),'card parts',len(data['phone']),'phone parts')
