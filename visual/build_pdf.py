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
font=TTCollection('/System/Library/Fonts/STHeiti Light.ttc').fonts[1];font.save('work/HeitiSC-print.ttf');pdfmetrics.registerFont(TTFont('CJK','work/HeitiSC-print.ttf'))
W,H=A4;BLACK=HexColor('#17191a');GREY=HexColor('#62676a');LIGHT=HexColor('#d8dcde')
source=etree.parse('work/anatomy-print-source.svg');root=source.getroot();root.set('viewBox','260 70 540 620');root.set('width','540');root.set('height','620');drawing=svg2rlg(BytesIO(etree.tostring(root)))
anchors={p['name']:p for p in json.load(open('work/anatomy-print-anchors.json'))}
parts=[('top_cover_flexible_pc','不透明触控面层','光滑白色表面，覆盖九个触觉区。','连续面层支持跨区拖动。'),('touch_sensor_flex_placeholder','触控层','感应手指位置与滑动方向。','当前为几何占位，电极未设计。'),('dome_carrier_pet','Dome 触觉组件','九个金属 dome、载体与传力柱。','按压力、行程与寿命待测试。'),('pcb_sparse_placeholder','PCB 占位','承载触点及电子连接。','当前为开放式占位，非布线文件。'),('lipo_envelope_no_capacity_claim','电池与电子模块','包含电池、BLE、触控 IC 和 USB-C。','体积为占位，不承诺电池容量。'),('magnet_ring_envelope_no_polarization','磁吸环','中心磁环外径 57 mm、内径 46 mm。','厚 0.8 mm；磁极与分段待确定。'),('battery_mount_bond','固定胶层','固定电池、磁环及电子模块。','材料、厚度公差与寿命待选定。'),('bottom_shell','底壳与支撑','0.60 mm 底板、1.00 mm 侧壁。','容纳部件、螺柱及面层支撑。')]
def text(c,x,y,s,size=10,color=BLACK):c.setFillColor(color);c.setFont('CJK',size);c.drawString(x,y,s)
def wrap(c,s,x,y,width,size=9,leading=15,color=GREY):
 line=''
 for char in s:
  if pdfmetrics.stringWidth(line+char,'CJK',size)>width and char not in '，。；：、！？）》':text(c,x,y,line,size,color);y-=leading;line=''
  line+=char
 if line:text(c,x,y,line,size,color);y-=leading
 return y
def rule(c,y):c.setStrokeColor(LIGHT);c.setLineWidth(.5);c.line(36,y,W-36,y)
def footer(c,page):
 rule(c,45);text(c,36,29,'DBOARD / 结构说明 / v05',8,GREY);text(c,W-95,29,page,8,GREY)
def head(c,title,sub):
 text(c,36,H-55,title,24);text(c,36,H-80,sub,10,GREY);rule(c,H-96)
def overview(c,page='01 / 02'):
 head(c,'键盘结构','网站解剖图中文说明 · 2026-11-27')
 for x,big,small in [(36,'60 × 90 mm','当前外形尺寸'),(218,'5.8 mm','当前 CAD 厚度'),(400,'约 3 mm','下一版厚度目标')]:text(c,x,718,big,19);text(c,x,698,small,9,GREY)
 c.saveState();c.translate(30,325);c.scale(.75,.75);renderPDF.draw(drawing,c,0,0);c.restoreState()
 # Numbered pins attach to the same mesh positions used by the website.
 for i,(name,title,a,b) in enumerate(parts):
  p=anchors[name];x=30+(p['right']-260)*.5625;y=325+(690-p['y'])*.5625;ly=638-i*41
  if i==4:y-=11
  c.setStrokeColor(HexColor('#90979b'));c.setLineWidth(.45);c.lines([(x,y,334,y),(334,y,350,ly-2)])
  c.setFillColor(BLACK);c.circle(x,y,7,fill=1,stroke=0);c.setFillColor(HexColor('#ffffff'));c.setFont('Helvetica',7);c.drawCentredString(x,y-2.5,str(i+1))
  text(c,360,ly,f'{i+1:02d}  {title}',10);wrap(c,a,360,ly-16,197,8.4,13);wrap(c,b,360,ly-29,197,8.4,13)
 rule(c,287)
 text(c,36,264,'如何阅读',12)
 y=wrap(c,'图形直接来自网站的 49 个 CAD 部件，放大仍为矢量线条。沿高度分离仅用于说明层次，不代表真实拆装路径或按键运动。',36,244,W-72,10,17)
 y=wrap(c,('解剖图沿用网站的结构示意字样；最新韩文字样与纯白外观见下一页。' if page=='01 / 02' else '解剖图沿用网站的结构示意字样；最新韩文字样与纯白外观见网站产品图。')+'现有实体几何仍为 5.8 mm，未将内部件压缩成 3 mm。',36,y-8,W-72,10,17)
 text(c,36,142,'图形来源',10)
 text(c,36,123,'dboard-3d.vercel.app · Anatomy / 实际 CAD 网格投影',9,GREY)
 text(c,36,105,'结构、触控、电气、磁吸和无线充电均需厂商继续验证。',9,GREY)
 c.linkURL('https://dboard-3d.vercel.app/',(36,115,380,138),relative=0)
 footer(c,page);c.showPage()
def detail(c,page='02 / 02'):
 head(c,'部件与验证','厂商沟通用 · 当前设计与下一步需求')
 c.drawImage(str(ROOT/'outputs/renders-white/02-top-v05.png'),36,490,width=175,height=219,preserveAspectRatio=True,mask='auto')
 text(c,238,704,'当前外观',13)
 y=wrap(c,'全白、不透明、光滑的连续触控面。九个触觉区通过灰色边界与点阵韩文字样识别；不是九枚独立机械键帽。',238,680,320,10,17)
 y=wrap(c,'左右两个元音的横向笔画已居中，上下各四行点。字样和点对象在可编辑场景文件中分别保留。',238,y-9,320,10,17)
 y=wrap(c,'“屏幕感”指表面外观。目前没有加入 LCD 或 OLED 显示模组。',238,y-9,320,10,17)
 text(c,238,526,'厚度基准',12)
 wrap(c,'PLAUD Note 官方机身厚度为 2.99 mm。此数值仅作为下一版约 3 mm 的目标，不代表当前方案已能制造。',238,505,320,9,15)
 rule(c,472)
 text(c,36,449,'关键占位尺寸',13)
 rows=[('磁吸环','外径 57 / 内径 46 / 厚 0.8 mm','仅包络；磁极、分段及保持力待定'),('电池','24 × 10 × 2.5 mm','仅包络；容量与续航未承诺'),('PCB','54 × 76 × 0.6 mm','开放式占位；需要重新布板'),('Dome','9 个 / 直径 5 mm / 自由高 0.3 mm','目标行程 0.2 mm；未验证按压力'),('USB-C','8.4 × 7 × 2.6 mm 占位','未选连接器；约 3 mm 方案需重审')]
 y=422
 for a,b,d in rows:
  text(c,36,y,a,9);text(c,101,y,b,9);text(c,101,y-16,d,8.4,GREY);rule(c,y-25);y-=44
 text(c,36,176,'下一步交给厂商验证',12)
 wrap(c,'1. 重排约 3 mm 截面：真实电池、连接器、触控层、胶层及外壳公差。\n2. 测试按压力、回弹、拖动连续性、邻区误触和表面耐磨。\n3. 验证装在手机背面时的无线充电、温升、磁吸和相机避让。'.replace('\n','  '),36,154,W-72,9,16)
 text(c,36,81,'参考：jp.plaud.ai/products/plaud-note-ai-voice-recorder',8,GREY)
 c.linkURL('https://jp.plaud.ai/products/plaud-note-ai-voice-recorder',(36,74,W-36,91),relative=0)
 footer(c,page);c.showPage()
def make(name,pages):
 c=canvas.Canvas(str(OUT/name),pagesize=A4,pageCompression=1);c.setTitle('键盘解剖图 - 中文注解');c.setAuthor('dboard-3d');
 for p in pages:p(c)
 c.save()
make('keyboard-anatomy-zh-v05.pdf',[overview,detail])
make('keyboard-anatomy-poster-zh-v05.pdf',[lambda c:overview(c,'01 / 01')])
make('keyboard-anatomy-notes-zh-v05.pdf',[lambda c:detail(c,'01 / 01')])
print('Created three PDF editions')
