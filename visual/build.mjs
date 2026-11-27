/** Anatomy CAD adapter. Actual CAD triangles, projected by Anatomy iso-kit.
 * MIT kit provenance: neekitalian/anatomy@1482e8469b0a9e0d8cc18ea2740a01423d29ae80.
 * Mesh drawing is an adapter: kit primitive SDF audits do not accept these meshes.
 * CAD interference evidence is retained separately; no primitive audit pass claimed.
 */
import {readFileSync,writeFileSync,mkdirSync} from 'node:fs';
import {resolve,dirname} from 'node:path';
import {fileURLToPath} from 'node:url';
import * as k from './vendor/anatomy/iso-kit.mjs';
import * as G from './vendor/anatomy/lathe.mjs';
const root=resolve(dirname(fileURLToPath(import.meta.url)),'..');
const out=resolve(root,'outputs/anatomy');mkdirSync(out,{recursive:true});
const data=JSON.parse(readFileSync(resolve(out,'cad-parts-v02.json'),'utf8'));
const theme=process.argv.includes('--light')?'light':'dark';
const W=1060,H=760;
const groups=[
 {id:'shell',title:'底壳与背垫',en:'ENCLOSURE',detail:'0.60 mm 底板 · 1.00 mm 侧壁',text:'包住全部内部零件。四个螺柱和膜片承台都属于底壳。当前承台存在树脂打印薄位，仍需修订。',move:[0,0,0]},
 {id:'bonds',title:'安装胶层',en:'MOUNTING BONDS',detail:'0.20 mm · 电池 / 磁环 / 模块',text:'占位胶层用于固定磁环、电池与模块，未指定胶材，也未验证长期保持力。',move:[0,0,5]},
 {id:'magnet',title:'磁吸环',en:'MAGNET RING',detail:'Ø57 / Ø46 × 0.80 mm',text:'磁环保持卡片居中，外缘距产品边缘1.50 mm。这里是包络环，尚无分段、磁极或磁力数据。',move:[0,0,18]},
 {id:'power',title:'电池与电子模块',en:'POWER + BLE',detail:'电池 24 × 10 × 2.50 mm',text:'上端是LiPo占位；下端是BLE、触控IC与USB-C。没有容量、续航、射频或器件适配承诺。',move:[0,0,30]},
 {id:'pcb',title:'PCB 支撑轨',en:'PCB SUBSTRATE',detail:'54 × 76 × 0.60 mm',text:'开放式PCB与三条6 mm支撑轨承托九个dome。开放区域不等于通过无线充电测试。',move:[0,0,44]},
 {id:'domes',title:'九点触觉机构',en:'TACTILE ARRAY',detail:'9 × Ø5 mm · 行程目标 0.20 mm',text:'九个金属dome、驱动柱与连续PET载膜。dome是几何帽壳，没有验证按压力、疲劳或邻区串扰。',move:[0,0,59]},
 {id:'touch',title:'连续触控层',en:'TOUCH FLEX',detail:'54 × 60 × 0.20 mm',text:'连续柔性触控层支持跨区滑动。这里保留厚度与空间，尚未设计电极、走线和控制电路。',move:[0,0,76]},
 {id:'cover',title:'透明面层与图标',en:'FACE + LEGENDS',detail:'56 × 64 × 0.50 mm · 黑白点阵',text:'一整片柔性透明PC，九组独立可编辑图标；没有切成九颗独立键帽。顶框与四个螺钉也在这一层展示。',move:[0,0,96]},
];
function layer(n){
 if(n==='bottom_shell'||n==='phone_contact_pad')return 0;
 if(n.includes('mount_bond'))return 1;
 if(n.startsWith('magnet_ring'))return 2;
 if(n.startsWith('lipo_')||n.startsWith('ble_')||n.startsWith('touch_ic')||n.startsWith('usb_c'))return 3;
 if(n.startsWith('pcb_'))return 4;
 if(n.startsWith('dome_')||n.startsWith('actuator_'))return 5;
 if(n.startsWith('touch_sensor')||n==='perimeter_bond')return 6;
 return 7;
}
const map=v=>[v[0],-v[1],v[2]];
const extents=[[-32,-47,0],[32,47,6],[-32,-47,102],[32,47,102]];
const P=k.fitProjection(extents,W,H,{pad:52,azimuth:36,elevation:37});
const PC=k.fitProjection([[-82,-75,-8],[85,75,8]],W,H,{pad:76,azimuth:36,elevation:43});
const PI=k.fitProjection(k.boxCorners({x:-31,y:-46,w:62,d:92,r:0},0,6),W,H,{pad:120,azimuth:36,elevation:37});
function body(mesh,P,offset=[0,0,0]){
 const vs=mesh.vertices.map(v=>map(v).map((n,i)=>n+offset[i]));
 const screen=vs.map(v=>k.iso(v,P)); const faces=[],edges=new Map();
 const V=G.viewOf(P),L=G.lightOf(P);
 const ptkey=v=>v.map(n=>n.toFixed(4)).join(',');
 for(const tri of mesh.triangles){
  // Y reflection reverses winding; reverse it back for outward normals.
  const [ia,ic,ib]=tri,a=vs[ia],b=vs[ib],c=vs[ic];
  const N=G.unit3(G.cross3(G.sub3(b,a),G.sub3(c,a)));
  const facing=G.dot3(N,V);const front=facing>1e-7;
  const tone=N[2]>.98?4:G.bandOf(G.dot3(N,L));
  if(front)faces.push({tri:[ia,ib,ic],tone,depth:k.depthOf(G.mul3(G.add3(G.add3(a,b),c),1/3),P)});
  for(const [i,j] of [[ia,ib],[ib,ic],[ic,ia]]){
   const keys=[ptkey(vs[i]),ptkey(vs[j])].sort();const key=keys.join('|');
   if(!edges.has(key))edges.set(key,{i,j,faces:[]});edges.get(key).faces.push({front,N});
  }
 }
 faces.sort((a,b)=>a.depth-b.depth);
 const path=(tri)=>tri.map((i,n)=>(n?'L':'M')+screen[i].map(v=>v.toFixed(2)).join(' ')).join('')+'Z';
 const batches=[];
 for(const f of faces){let last=batches.at(-1);if(!last||last.tone!==f.tone){last={tone:f.tone,d:''};batches.push(last);}last.d+=path(f.tri);}
 let outline='';
 for(const e of edges.values()){
  const visible=e.faces.filter(f=>f.front);if(!visible.length)continue;
  const silhouette=visible.length<e.faces.length||e.faces.length===1;
  const crease=e.faces.length>1&&G.dot3(e.faces[0].N,e.faces[1].N)<.7;
  if(silhouette||crease)outline+='M'+screen[e.i].map(v=>v.toFixed(2)).join(' ')+'L'+screen[e.j].map(v=>v.toFixed(2)).join(' ');
 }
 // Closed mesh silhouettes and actual CAD edges: no decorative open rule lines.
 return batches.map(b=>`<path class="mesh-face shade-${Math.min(4,b.tone)}" d="${b.d}"/>`).join('')+`<path class="iso-line iso-edge" data-tone="mid" d="${outline}"/>`;
}
function scene(mode){
 const p=mode==='compare'?PC:mode==='inside'?PI:P;const list=[];
 if(mode==='compare')for(const m of data.phone){const off=[-44,0,0];list.push({mesh:m,p,offset:off,group:-1});}
 for(const m of data.card)list.push({mesh:m,p,offset:mode==='compare'?[44,0,0]:[0,0,0],group:layer(m.name)});
 // Depth keys are from the real CAD part centre, transformed into this projection.
 const items=list.map(({mesh,p,offset,group})=>{
  const center=map(mesh.center).map((v,i)=>v+offset[i]);
  const move=group>=0&&mode==='anatomy'?groups[group].move:[0,0,0];
  const origin=k.iso([0,0,0],p),shift=k.iso(move,p).map((v,i)=>v-origin[i]);
  const key=group<0?-10000+mesh.center[2]*10+k.depthOf(center,p)*0.001:group*1000+mesh.center[2]*10+k.depthOf(center,p)*0.001;
  const lift=k.depthOf(move,p)-k.depthOf([0,0,0],p);
  return {key,lift,group,move,shift,svg:`<g class="cad-part${mesh.name.startsWith('legend_')?' glyph':''}" data-name="${mesh.name}" data-layer="${group}" data-key="${key}" data-lift="${lift}" data-dx="${shift[0]}" data-dy="${shift[1]}">${body(mesh,p,offset)}</g>`};
 });
 items.sort((a,b)=>(a.key+a.lift*.78)-(b.key+b.lift*.78));
 return k.figureSvg({width:W,height:H,label:mode==='compare'?'iPhone16和60乘90毫米九键输入卡的等比例尺寸对比':'当前CAD的49个部件，分层展示底壳、磁环、电子件、PCB、九个dome与连续触控面层',body:`<g class="scene-parts">${items.map(i=>i.svg).join('')}</g>`});
}
const rows=groups.map((g,i)=>`<button class="part-button" data-select="${i}" aria-pressed="false"><span class="part-no">0${i+1}</span><span><strong>${g.title}</strong><small>${g.en}</small></span><span class="part-arrow" aria-hidden="true">↗</span></button>`).join('');
const extraCSS=`
.iso[data-theme="dark"]{--anatomy-top:#343434;--anatomy-shade-0:#191919;--anatomy-shade-1:#202020;--anatomy-shade-2:#282828;--anatomy-shade-3:#303030;--anatomy-mid:#969696;--anatomy-lit-top:#555555;--anatomy-lit-shade:#383838}
.compare-active .controlbar{display:none}
.cad-part[data-layer="0"] .shade-4{fill:var(--anatomy-shade-2);stroke:var(--anatomy-shade-2)}
.cad-part[data-layer="5"] .shade-4{fill:var(--anatomy-hi);stroke:var(--anatomy-hi)}
.cad-part[data-layer="5"][data-dim] .shade-4{fill:var(--anatomy-top);stroke:var(--anatomy-top)}
:root{font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Noto Sans CJK SC",sans-serif}
.iso-page{width:min(1376px,100% - 80px);margin:40px auto 44px}.topline{display:flex;justify-content:space-between;align-items:center;font:11px var(--anatomy-mono);letter-spacing:.08em;color:var(--anatomy-muted);padding-bottom:20px;border-bottom:1px solid var(--anatomy-faint)}
.theme-button{background:none;border:1px solid var(--anatomy-faint);color:var(--anatomy-text);padding:8px 12px;cursor:pointer;font:inherit}.heading{display:flex;justify-content:space-between;align-items:flex-end;margin:38px 0 28px;gap:20px}h1{font-size:36px;letter-spacing:-.045em;font-weight:550;color:var(--anatomy-strong);line-height:1.2;margin:0 0 12px}.subtitle{margin:0;font-size:13px;color:var(--anatomy-muted)}.specs{display:flex;gap:26px;font:12px var(--anatomy-mono);text-align:right}.specs b{display:block;color:var(--anatomy-strong);font-size:23px;font-weight:450;margin-bottom:7px}.specs span{font-size:10px;color:var(--anatomy-muted)}
.workbench{display:grid;grid-template-columns:minmax(0,1fr) 282px;gap:24px}.iso-figure{margin:0}.iso-plate{box-shadow:none;border:1px solid var(--anatomy-faint);border-radius:3px;background:var(--anatomy-card);overflow:hidden}.iso-stage{width:100%;min-height:430px;position:relative;touch-action:pan-y;overflow:hidden}.iso-svg{width:100%;height:auto;display:block}.iso-plate-corner{font-size:10px;letter-spacing:.025em}.iso-plate-corners{pointer-events:none}.iso-legend{margin-top:12px;font-size:11px;line-height:1.8;max-width:700px}.iso-caption{color:var(--anatomy-muted)}.scene[hidden]{display:none}.scene{transform-origin:center}.mesh-face{stroke-width:.12px;stroke-linejoin:round;vector-effect:non-scaling-stroke}.shade-0{fill:var(--anatomy-shade-0);stroke:var(--anatomy-shade-0)}.shade-1{fill:var(--anatomy-shade-1);stroke:var(--anatomy-shade-1)}.shade-2{fill:var(--anatomy-shade-2);stroke:var(--anatomy-shade-2)}.shade-3{fill:var(--anatomy-shade-3);stroke:var(--anatomy-shade-3)}.shade-4{fill:var(--anatomy-top);stroke:var(--anatomy-top)}
.cad-part .iso-edge{stroke-width:.42px}.cad-part{transition:opacity 180ms ease}.cad-part[data-dim]{opacity:.18}.cad-part[data-on] .shade-4{fill:var(--anatomy-lit-top);stroke:var(--anatomy-lit-top)}.cad-part[data-on] .iso-edge{stroke:var(--anatomy-lit);stroke-width:.7px}.glyph .mesh-face{fill:var(--anatomy-hi);stroke:var(--anatomy-hi)}
.toolbar{display:flex;justify-content:space-between;gap:12px;align-items:center;margin-bottom:12px}.tabs{display:flex;gap:3px;border:1px solid var(--anatomy-faint);padding:3px;border-radius:3px}.tabs button,.action{background:none;color:var(--anatomy-text);border:0;padding:8px 13px;font-size:12px;font-family:inherit;cursor:pointer;border-radius:1px}.tabs button[aria-pressed="true"]{background:var(--anatomy-faint);color:var(--anatomy-strong)}.action{border:1px solid var(--anatomy-faint)}
.part-list{border-top:1px solid var(--anatomy-faint);margin-top:45px}.part-button{display:flex;align-items:center;gap:14px;width:100%;text-align:left;background:none;border:0;border-bottom:1px solid var(--anatomy-faint);padding:13px 3px;color:var(--anatomy-text);cursor:pointer}.part-button strong{font-weight:450;font-size:13px;display:block;color:var(--anatomy-strong)}.part-button small{display:block;font:9px var(--anatomy-mono);letter-spacing:.07em;margin-top:5px;color:var(--anatomy-muted)}.part-no{font:10px var(--anatomy-mono);color:var(--anatomy-muted)}.part-arrow{margin-left:auto;color:var(--anatomy-muted)}.part-button[aria-pressed="true"]{background:var(--anatomy-faint)}.part-button:hover strong{color:var(--anatomy-lit)}
.part-info{min-height:153px;padding-top:20px}.part-info h2{font-weight:500;color:var(--anatomy-strong);font-size:15px;margin:0 0 10px}.part-info p{margin:0;font-size:12px;line-height:1.9;color:var(--anatomy-muted)}.part-info .measure{font:10px var(--anatomy-mono);margin-bottom:10px;color:var(--anatomy-text)}.controlbar{display:flex;gap:20px;align-items:center;border-top:1px solid var(--anatomy-faint);margin-top:20px;padding-top:18px;font:11px var(--anatomy-mono)}.range-wrap{display:flex;align-items:center;gap:15px;flex:1}.range-wrap label{white-space:nowrap}input[type=range]{width:100%;accent-color:var(--anatomy-strong);height:20px;cursor:pointer}output{width:34px;text-align:right;font-variant-numeric:tabular-nums}.foot{display:flex;justify-content:space-between;align-items:start;gap:24px;border-top:1px solid var(--anatomy-faint);margin-top:32px;padding-top:18px;font-size:11px;color:var(--anatomy-muted)}a{color:var(--anatomy-text);text-underline-offset:4px}button:focus-visible,input:focus-visible,.iso-stage:focus-visible{outline:2px solid var(--anatomy-strong);outline-offset:4px}.compare-label{display:none}.compare-active .compare-label{display:block}.note{max-width:690px;line-height:1.8}.aside-label{font:10px var(--anatomy-mono);color:var(--anatomy-muted);letter-spacing:.07em;margin:0 0 -31px;padding-top:10px}.sr-only{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0,0,0,0)}
@media(max-width:900px){.iso-page{width:calc(100% - 40px);margin:24px auto}.workbench{grid-template-columns:1fr}.part-list{margin-top:15px;display:grid;grid-template-columns:1fr 1fr}.part-button{padding:13px 8px}.part-info{min-height:auto;padding-bottom:12px}.aside-label{margin:4px 0}.heading{margin-top:28px}.specs{gap:16px}.specs b{font-size:19px}.iso-stage{min-height:0}.foot{flex-direction:column;gap:12px}}
@media(max-width:540px){.iso-page{width:calc(100% - 28px);margin:18px auto}.heading{display:block;margin-bottom:20px}h1{font-size:28px}.specs{margin-top:24px;text-align:left;justify-content:space-between}.specs b{font-size:20px}.subtitle{font-size:12px;line-height:1.8}.toolbar{gap:6px}.tabs button{padding:8px 9px;font-size:11px}.action{padding:8px;font-size:11px}.iso-plate-corner{font-size:8px}.controlbar{gap:12px;margin-top:14px}.part-button strong{font-size:12px}.part-button small{font-size:8px}.part-button{gap:9px}.topline{font-size:9px}.iso-caption{font-size:10px}.part-info p{font-size:12px}.note{font-size:10px}.controlbar .action{white-space:nowrap}}
@media(prefers-reduced-motion:reduce){*,*::before,*::after{transition:none!important;animation:none!important}}
`;
const stages=`<div class="iso-stage" role="group" aria-label="内部部件可视化；方向键调整分层距离，空格切换合拢与分层" tabindex="0"><div class="scene" data-scene="anatomy">${scene('anatomy')}</div><div class="scene" data-scene="inside" hidden>${scene('inside')}</div><div class="scene" data-scene="compare" hidden>${scene('compare')}</div></div>`;
const plate=k.plateHtml({fig:'FIG. 01',title:'NINE-KEY CARD / CAD v02',hint:'拖动滑块拆解 · 点击部件查看',readout:'49 PARTS · 60 × 90 × 5.8 mm',caption:'基于实际 CAD 网格。分层距离仅为展示；不是装配路径或按压仿真。',body:stages});
const htmlbody=`<header class="topline"><span>ANATOMY / HANGUL INPUT CARD</span><button class="theme-button" id="theme" aria-label="切换明暗主题">${theme==='dark'?'浅色':'深色'} ↗</button></header><section class="heading"><div><h1>九键输入卡，拆开看。</h1><p class="subtitle">连续触控表面之下，是九组触觉机构与一圈磁吸结构。</p></div><div class="specs"><div><b>60 × 90</b><span>外形 / mm</span></div><div><b>5.8</b><span>厚度 / mm</span></div><div><b>09</b><span>触觉区域</span></div></div></section><div class="workbench"><section><div class="toolbar"><nav class="tabs" aria-label="查看方式"><button data-view="exploded" aria-pressed="true">分层拆解</button><button data-view="inside" aria-pressed="false">内部结构</button><button data-view="compare" aria-pressed="false">iPhone 对比</button></nav><button class="action" id="reset">重置视图</button></div>${plate}<div class="controlbar"><div class="range-wrap"><label for="explode">分层距离</label><input id="explode" type="range" min="0" max="100" value="78" aria-label="分层展示距离"><output for="explode" id="percent">78%</output></div><button class="action" id="tour" aria-pressed="false">自动演示</button></div><p class="compare-label subtitle" id="compare-caption">iPhone 16：71.6 × 147.6 × 7.8 mm。键盘宽度约为机身的 ${(60/71.6*100).toFixed(1)}%，高度约 ${(90/147.6*100).toFixed(1)}%。</p></section><aside><p class="aside-label">EXPLORE THE ASSEMBLY</p><div class="part-list">${rows}</div><section class="part-info" aria-live="polite"><h2 id="part-title">49 个部件，同一套几何。</h2><p class="measure" id="part-measure">CAD SOURCE / MILLIMETRES</p><p id="part-description">选择一个部件组，查看它的尺寸与作用。可视化沿用当前评审模型，不会隐藏打印检查失败项。</p></section></aside></div><footer class="foot"><div class="note">评审原型 · 树脂打印薄位尚待修复；无线充电、真实按压力与手机适配未验证。iPhone 仅作尺寸参照，相机与圆角为示意。</div><div><a href="../exports/iphone16-keyboard-beside-v02.glb">下载含 iPhone 的 3D 模型 ↗</a><br><a href="https://github.com/neekitalian/anatomy">Built with Anatomy ↗</a></div></footer>`;
const live=`
const groups=${JSON.stringify(groups)};
const stage=document.querySelector('.iso-stage'), range=document.querySelector('#explode'),readout=document.querySelector('[data-readout]'),percent=document.querySelector('#percent');
const scene=document.querySelector('[data-scene=anatomy]'), layerRoot=scene.querySelector('.scene-parts'), parts=[...layerRoot.children];
const compare=document.querySelector('[data-scene=compare]');
const internal=document.querySelector('[data-scene=inside]');
let view='exploded',x=.78,target=.78,selected=-1,raf=0,last=0,visible=true,touring=false,clock=0,zoom=1,panX=0,panY=0,drag=null;
const still=matchMedia('(prefers-reduced-motion: reduce)');
let order='';
function paint(){
 for(const p of parts){const g=+p.dataset.layer;p.setAttribute('transform','translate('+((+p.dataset.dx)*x).toFixed(3)+' '+((+p.dataset.dy)*x).toFixed(3)+')');p.hidden=false;p.style.display=view==='inside'&&g>=6?'none':'';p.toggleAttribute('data-on',selected===g);p.toggleAttribute('data-dim',selected>=0&&selected!==g);}
 const sorted=parts.map((p,i)=>({p,i,k:+p.dataset.key+(+p.dataset.lift)*x})).sort((a,b)=>a.k-b.k), next=sorted.map(o=>o.i).join(',');
 if(next!==order){const f=document.createDocumentFragment();sorted.forEach(o=>f.appendChild(o.p));layerRoot.appendChild(f);order=next;}
 percent.textContent=Math.round(x*100)+'%';
 readout.textContent=view==='compare'?'iPHONE 16 / 71.6 × 147.6 mm':selected<0?'49 PARTS · 60 × 90 × 5.8 mm':groups[selected].en;
 for(const p of compare.querySelectorAll('.cad-part')){const g=+p.dataset.layer;p.toggleAttribute('data-on',selected===g);p.toggleAttribute('data-dim',selected>=0&&selected!==g);}
 for(const p of internal.querySelectorAll('.cad-part')){const g=+p.dataset.layer;p.style.display=g>=6||p.dataset.name==='dome_carrier_pet'?'none':'';p.toggleAttribute('data-on',selected===g);p.toggleAttribute('data-dim',selected>=0&&selected!==g);}
}
function zoomTo(value){zoom=value;panX=0;panY=0;setViewBox();document.querySelector('#zoom').textContent=zoom>2?'缩小 −':'放大 +';}
function setViewBox(){stage.querySelectorAll('svg').forEach(svg=>svg.setAttribute('viewBox',[(1060-1060/zoom)/2+panX,(760-760/zoom)/2+panY,1060/zoom,760/zoom].join(' ')));}
function tick(now){const dt=last?Math.min((now-last)/1000,1/30):1/60;last=now;if(touring&&!still.matches){clock+=dt;target=.5+.42*Math.sin(clock*.42);range.value=Math.round(target*100);}x=still.matches?target:x+(target-x)*(1-Math.exp(-dt/.24));if(Math.abs(x-target)<.0001)x=target;paint();raf=visible&&(touring||x!==target)?requestAnimationFrame(tick):0;}
function run(){if(!raf&&visible){last=0;raf=requestAnimationFrame(tick);}}
function tour(on){touring=on&&!still.matches;document.querySelector('#tour').setAttribute('aria-pressed',String(touring));document.querySelector('#tour').textContent=touring?'暂停演示':'自动演示';if(touring)run();}
function select(n){selected=selected===n?-1:n;document.querySelectorAll('[data-select]').forEach(b=>b.setAttribute('aria-pressed',String(+b.dataset.select===selected)));document.querySelector('#part-title').textContent=selected<0?'49 个部件，同一套几何。':groups[selected].title;document.querySelector('#part-measure').textContent=selected<0?'CAD SOURCE / MILLIMETRES':groups[selected].detail;document.querySelector('#part-description').textContent=selected<0?'选择一个部件组，查看它的尺寸与作用。可视化沿用当前评审模型，不会隐藏打印检查失败项。':groups[selected].text;paint();}
function mode(next){view=next;tour(false);zoomTo(1);document.querySelectorAll('[data-view]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.view===view)));scene.hidden=view!=='exploded';internal.hidden=view!=='inside';compare.hidden=view!=='compare';document.body.classList.toggle('compare-active',view==='compare');range.disabled=view!=='exploded';target=view==='inside'?0:.78;range.value=Math.round(target*100);paint();run();}
range.addEventListener('input',()=>{tour(false);target=+range.value/100;run();});
document.querySelectorAll('[data-select]').forEach(b=>b.addEventListener('click',()=>select(+b.dataset.select)));
stage.addEventListener('click',e=>{const p=e.target.closest('.cad-part');if(p&&+p.dataset.layer>=0)select(+p.dataset.layer);});
document.querySelectorAll('[data-view]').forEach(b=>b.addEventListener('click',()=>mode(b.dataset.view)));
document.querySelector('#theme').onclick=()=>{const light=document.body.dataset.theme!=='light';document.body.dataset.theme=light?'light':'dark';document.querySelector('#theme').textContent=light?'深色 ↗':'浅色 ↗';};
document.querySelector('#tour').onclick=()=>{if(view!=='exploded')mode('exploded');tour(!touring);};
document.querySelector('#zoom').onclick=()=>zoomTo(zoom===1?1.6:zoom===1.6?2.4:1);
stage.addEventListener('pointerdown',e=>{if(zoom<=1)return;const box=stage.getBoundingClientRect();drag={x:e.clientX,y:e.clientY,px:panX,py:panY,s:1060/zoom/box.width};stage.setPointerCapture(e.pointerId);});
stage.addEventListener('pointermove',e=>{if(!drag)return;panX=drag.px-(e.clientX-drag.x)*drag.s;panY=drag.py-(e.clientY-drag.y)*drag.s;setViewBox();});
stage.addEventListener('pointerup',()=>drag=null);stage.addEventListener('pointercancel',()=>drag=null);
document.querySelector('#reset').onclick=()=>{selected=-1;select(-2);selected=-1;document.querySelectorAll('[data-select]').forEach(b=>b.setAttribute('aria-pressed','false'));document.querySelector('#part-title').textContent='49 个部件，同一套几何。';document.querySelector('#part-measure').textContent='CAD SOURCE / MILLIMETRES';document.querySelector('#part-description').textContent='选择一个部件组，查看它的尺寸与作用。';mode('exploded');paint();};
stage.addEventListener('keydown',e=>{if(e.key==='Escape'){if(selected>=0)select(selected);return;}if(e.key===' '){e.preventDefault();tour(false);target=target>.5?0:1;range.value=target*100;run();return;}if(['ArrowLeft','ArrowRight','Home','End'].includes(e.key)){e.preventDefault();tour(false);target=e.key==='Home'?0:e.key==='End'?1:Math.max(0,Math.min(1,target+(e.key==='ArrowRight'?.05:-.05)));range.value=Math.round(target*100);run();}});
new IntersectionObserver(es=>{visible=es.at(-1).isIntersecting;if(visible)run();else if(raf){cancelAnimationFrame(raf);raf=0;}}).observe(stage);
document.addEventListener('visibilitychange',()=>{if(document.hidden&&raf){cancelAnimationFrame(raf);raf=0;}else run();});
still.addEventListener('change',()=>{if(still.matches)tour(false);run();});
window.anatomy={mode,select,setExplode(value){tour(false);target=value;range.value=Math.round(value*100);run();},state:()=>({view,x,target,selected,partCount:parts.length,reduced:still.matches,touring}),source:${JSON.stringify(data.source)}};
paint();
`;
// Reset avoids fake part IDs; all UI state remains based on the actual part list.
const fixedLive=live.replace("selected=-1;select(-2);selected=-1;","zoomTo(1);selected=-1;");
let html=k.pageHtml({title:'九键输入卡 · Anatomy 内部结构',theme,body:htmlbody,script:fixedLive,width:1376});
html=html.replace('<html lang="en">','<html lang="zh-CN">').replace('</style>','\n'+extraCSS+'</style>');
html=html.replace('<button class="action" id="reset">重置视图</button>','<div style="display:flex;gap:6px"><button class="action" id="zoom" aria-label="放大模型；放大后可拖动查看细节">放大 +</button><button class="action" id="reset">重置</button></div>');
writeFileSync(resolve(out,theme==='light'?'index-light.html':'index.html'),html);
writeFileSync(resolve(out,'provenance.json'),JSON.stringify({repository:'https://github.com/neekitalian/anatomy',commit:'1482e8469b0a9e0d8cc18ea2740a01423d29ae80',adapter:'actual CAD triangle meshes projected through iso-kit, four-tone shading and SVG animation; not primitive-based A.audit geometry',cad:data.source,partCount:data.card.length,phone:data.dimensions.phone},null,2));
console.log('wrote',theme,'actual CAD parts',data.card.length,'HTML MB',(html.length/1e6).toFixed(2));
