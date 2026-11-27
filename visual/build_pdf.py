from pathlib import Path
from io import BytesIO
import json
from lxml import etree
from fontTools.ttLib import TTCollection
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from reportlab.graphics import renderPDF
from svglib.svglib import svg2rlg
ROOT=Path.cwd();OUT=ROOT/'outputs/pdf';OUT.mkdir(exist_ok=True)
for name,path,index in [('Body','/System/Library/Fonts/Supplemental/Songti.ttc',6),('Head','/System/Library/Fonts/STHeiti Medium.ttc',1)]:
 face=TTCollection(path).fonts[index];target=Path('work')/(name+'-print.ttf');face.save(str(target));pdfmetrics.registerFont(TTFont(name,str(target)))
W,H=A4;BLACK=HexColor('#17191a');GREY=HexColor('#62676a');LIGHT=HexColor('#d8dcde')
source=etree.parse('work/anatomy-print-source.svg');root=source.getroot();root.set('viewBox','260 70 540 620');root.set('width','540');root.set('height','620');drawing=svg2rlg(BytesIO(etree.tostring(root)))
anchors={p['name']:p for p in json.load(open('work/anatomy-print-anchors.json'))}
parts=[
 ('top_cover_flexible_pc','触控面层','白色不透明表面，连续覆盖九个触觉区。'),
 ('touch_sensor_flex_placeholder','触控层','识别手指位置与跨区滑动方向。'),
 ('dome_carrier_pet','金属弹片组件','九个弹片与传力柱提供局部按压反馈。'),
 ('pcb_sparse_placeholder','PCB','连接触点、控制电路与电子模块。'),
 ('lipo_envelope_no_capacity_claim','电池与电子模块','内置电池、蓝牙模块、触控芯片及接口。'),
 ('magnet_ring_envelope_no_polarization','磁吸环','居中设置，用于固定在手机背面。'),
 ('battery_mount_bond','固定胶层','固定电池、磁环与电子模块。'),
 ('bottom_shell','底壳与支撑','容纳内部部件，并支撑面层与螺柱。')]
def text(c,x,y,s,size=11,color=BLACK,font='Body'):
 c.setFillColor(color);c.setFont(font,size);c.drawString(x,y,s)
def wrap(c,s,x,y,width,size=11,leading=15.5,color=BLACK):
 line=''
 for char in s:
  if pdfmetrics.stringWidth(line+char,'Body',size)>width and char not in '，。；：、！？）》':
   text(c,x,y,line,size,color);y-=leading;line=''
  line+=char
 if line:text(c,x,y,line,size,color);y-=leading
 return y
def head(c,title):text(c,42,H-60,title,22,font='Head')
def overview(c,page=None):
 c.saveState();c.translate(30,300);c.scale(.75,.75);renderPDF.draw(drawing,c,0,0);c.restoreState()
 for i,(name,title,description) in enumerate(parts):
  p=anchors[name];x=30+(p['right']-260)*.5625;y=300+(690-p['y'])*.5625;ly=629-i*42
  if i==4:y-=11
  c.setStrokeColor(HexColor('#a0a5a8'));c.setLineWidth(.4);c.lines([(x,y,334,y),(334,y,350,ly-3)])
  text(c,360,ly,title,11,font='Head');wrap(c,description,360,ly-17,192,9.5,13.2,GREY)
 c.showPage()
def detail(c,page=None):
 head(c,'部件说明')
 image=ROOT/'outputs/renders-white/02-top-v05.png'
 if not image.exists():image=ROOT/'outputs/keyboard-white-v05/outputs/renders-white/02-top-v05.png'
 c.drawImage(str(image),42,470,width=190,height=237.5,preserveAspectRatio=True,mask='auto')
 text(c,262,698,'外观',13,font='Head')
 y=wrap(c,'全白、不透明的光滑触控面。九个触觉区由浅灰分区线和点阵韩文字样识别。',262,673,291,11,16)
 wrap(c,'点按与跨区滑动共用一块连续面层。',262,y-10,291,11,16)
 text(c,42,426,'关键尺寸',14,font='Head')
 rows=[('磁吸环','外径 57 mm，内径 46 mm，厚 0.8 mm'),('电池','24 × 10 × 2.5 mm'),('PCB','54 × 76 × 0.6 mm'),('金属弹片','9 个，直径 5 mm，自由高度 0.3 mm'),('USB C 接口','8.4 × 7 × 2.6 mm')]
 y=392
 for label,value in rows:
  text(c,42,y,label,11);text(c,145,y,value,11);y-=28
 c.showPage()
def make(name,pages):
 c=canvas.Canvas(str(OUT/name),pagesize=A4,pageCompression=1);c.setTitle('键盘结构说明');c.setAuthor('dboard3d')
 for p in pages:p(c)
 c.save()
make('keyboard-anatomy-zh-v05.pdf',[overview])
make('keyboard-anatomy-poster-zh-v05.pdf',[overview])
make('keyboard-anatomy-notes-zh-v05.pdf',[detail])
print('Created clean typography PDF editions')
