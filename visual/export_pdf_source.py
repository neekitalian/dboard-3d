from pathlib import Path
from lxml import etree
import re,json
html=Path('outputs/anatomy/index.html').read_text();i=html.index('data-scene="anatomy"');a=html.index('<svg',i);b=html.index('</svg>',a)+6
svg=etree.fromstring(html[a:b].encode())
colors=['#dcdcd9','#e5e5e2','#ededea','#f4f4f1','#ffffff'];anchors=[]
for g in svg.xpath('.//*[@data-name]'):
 layer=int(g.get('data-layer'));dx=float(g.get('data-dx','0'));dy=float(g.get('data-dy','0'));g.set('transform',f'translate({dx} {dy})')
 coords=[]
 for p in g.xpath('.//*[local-name()="path"]'):
  cls=p.get('class','');nums=[float(n) for n in re.findall(r'-?\d+(?:\.\d+)?',p.get('d',''))];coords+=list(zip(nums[::2],nums[1::2]))
  if 'mesh-face' in cls:
   grade=int(re.search(r'shade-(\d)',cls)[1]);c=colors[grade]
   if layer==0 and grade==4:c=colors[2]
   if layer==5 and grade==4:c='#26262a'
   if layer==7:c='#f3f3f0'
   if 'glyph' in g.get('class',''):c='#444444'
   p.set('fill',c);p.set('stroke',c);p.set('stroke-width','.12');p.set('stroke-linejoin','round')
  else:p.set('fill','none');p.set('stroke','#aaaaaa' if layer==7 else '#8a8a8f');p.set('stroke-width','.42');p.set('stroke-linejoin','round')
  p.attrib.pop('class',None)
 if coords:
  xs,ys=zip(*coords);anchors.append({'name':g.get('data-name'),'layer':layer,'x':(min(xs)+max(xs))/2+dx,'y':(min(ys)+max(ys))/2+dy,'left':min(xs)+dx,'right':max(xs)+dx})
 g.attrib.pop('class',None)
Path('work/anatomy-print-source.svg').write_bytes(etree.tostring(svg))
Path('work/anatomy-print-anchors.json').write_text(json.dumps(anchors))
print('Frozen SVG source, parts:',len(anchors))
