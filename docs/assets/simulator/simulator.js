import {prepareGrating,evaluateImage,traceSixF,phaseRate,FOCAL_UM} from './optics-engine.mjs';

const form=document.getElementById('simulator-controls');
const labels=JSON.parse(document.getElementById('simulator-strings').textContent);
const tr=(key,values={})=>labels[key].replace(/\{(\w+)\}/g,(_,name)=>String(values[name]??''));
const languageLink=document.getElementById('language-switch');
const languageURL=new URL(languageLink.href);
const defaults=JSON.parse(document.getElementById('simulator-defaults').textContent);
const fields=[...Object.keys(defaults),'focus_um'];
const el=Object.fromEntries(fields.map(name=>[name,document.getElementById(name)]));
const frequency=document.getElementById('frequency_u');
const colors={zero:'#facc15',positive:'#fb7185',negative:'#4ade80',higher:'#c4b5fd',blue:'#38bdf8',pink:'#e879bc',muted:'#9aabc2',grid:'#29384d'};
const focusDetail=document.getElementById('focus-detail');
let frame=0,prepared=null,preparedKey=null,latest=null,worker=null,workerBusy=false,inFlightKey=null,pendingMap=null,map=null,mapFailed=false;
const f=(v,d=2)=>Number(v).toFixed(d);
const text=(id,value)=>{const e=document.getElementById(id);if(e.textContent!==String(value))e.textContent=value;};
function orderColor(j){return j===0?colors.zero:j===1?colors.positive:j===-1?colors.negative:['#7dd3fc','#c4b5fd','#fdba74','#f9a8d4'][Math.abs(j)%4];}
function surface(id){
  const canvas=document.getElementById(id),r=canvas.getBoundingClientRect(),dpr=window.devicePixelRatio||1;
  if(!r.width||!r.height)return null;
  const pw=Math.round(r.width*dpr),ph=Math.round(r.height*dpr);
  if(canvas.width!==pw)canvas.width=pw;if(canvas.height!==ph)canvas.height=ph;
  const ctx=canvas.getContext('2d');ctx.setTransform(dpr,0,0,dpr,0,0);ctx.clearRect(0,0,r.width,r.height);
  ctx.lineCap='round';return {canvas,ctx,w:r.width,h:r.height};
}
function line(ctx,points,color,width=1,alpha=1,dash=[]){
  ctx.save();ctx.strokeStyle=color;ctx.lineWidth=width;ctx.globalAlpha=alpha;ctx.setLineDash(dash);ctx.beginPath();
  points.forEach(([x,y],i)=>i?ctx.lineTo(x,y):ctx.moveTo(x,y));ctx.stroke();ctx.restore();
}
function dot(ctx,x,y,r,color){ctx.fillStyle=color;ctx.beginPath();ctx.arc(x,y,r,0,2*Math.PI);ctx.fill();}
function drawRays(data,p){
  const s=surface('ray-chart');if(!s)return;
  const {ctx,canvas,w,h}=s;ctx.scale(w/1120,h/370);
  const axis=184,R=108,x=z=>65+155*z,y=height=>axis-R*height;
  const dz=p.focus_um/FOCAL_UM,magnification=2000,wafer=6+dz*magnification;
  line(ctx,[[20,axis],[1100,axis]],colors.grid,1,1,[5,5]);
  const planes=labels.planes;
  ctx.font='13px system-ui';ctx.textAlign='center';
  planes.forEach((label,i)=>{
    ctx.fillStyle=colors.muted;ctx.fillText(label,x(i),22);
    if([1,3,5].includes(i)){
      ctx.fillStyle='rgba(56,189,248,.07)';ctx.strokeStyle='#3b7896';ctx.lineWidth=1.3;
      ctx.beginPath();ctx.ellipse(x(i),axis,9,146,0,0,2*Math.PI);ctx.fill();ctx.stroke();
    }else line(ctx,[[x(i),38],[x(i),330]],i===4?'#496178':'#3a4b62',1.2);
  });
  // Aperture is the only stop in this ideal relay; all lens clear apertures are unlimited.
  line(ctx,[[x(4),36],[x(4),y(p.na)]],'#ef6b73',5);
  line(ctx,[[x(4),y(-p.na)],[x(4),332]],'#ef6b73',5);
  line(ctx,[[x(4),y(p.na)],[x(4),y(-p.na)]],colors.blue,3,.55);
  if(Math.abs(dz)>1e-12){
    line(ctx,[[x(6),38],[x(6),330]],'#536178',1,1,[4,5]);
    line(ctx,[[x(wafer),38],[x(wafer),330]],colors.blue,2);
    ctx.fillStyle=colors.blue;ctx.fillText(`z=${f(p.focus_um)} µm`,x(wafer),351);
  }
  const pitchUm=p.pitch_nm/1000;
  const a=Math.max(1,Math.round(.28*FOCAL_UM/pitchUm))*pitchUm/FOCAL_UM;
  const maskPoints=document.getElementById('ray-bundles').checked?[-a,0,a]:[0];
  maskPoints.forEach(height=>{
    const ray=traceSixF(p.source_u,p.source_u,height);
    line(ctx,ray.slice(0,3).map(q=>[x(q.z),y(q.h)]),colors.zero,1.4,.38);
    dot(ctx,x(2),y(height),2.5,'#c4d4e7');
  });
  dot(ctx,x(0),y(-p.source_u),5.5,colors.zero);
  const rays=data.spectrum.filter(q=>Math.abs(q.coefficient)>1e-12&&Math.abs(q.u)<=1+1e-12);
  rays.sort((a,b)=>Math.abs(b.order)-Math.abs(a.order));
  rays.forEach(order=>{
    const color=orderColor(order.order),major=Math.abs(order.order)<=1;
    maskPoints.forEach(height=>{
      const points=traceSixF(p.source_u,order.u,height,p.focus_um);
      const projected=points.map((q,i)=>{
        if(i===6)return[x(6+(q.z-6)*magnification),y(-height+(q.h+height)*magnification)];
        return[x(q.z),y(q.h)];
      });
      line(ctx,projected.slice(2,5),color,major?1.7:1.1,order.passed?(major?.7:.4):.18,order.passed?[]:[4,4]);
      if(order.passed)line(ctx,projected.slice(4),color,major?1.7:1.1,major?.7:.4);
    });
    const yy=y(order.u);
    if(order.passed){
      dot(ctx,x(4),yy,major?5:3.5,color);
      if(major){
        ctx.strokeStyle=color;ctx.globalAlpha=.8;ctx.beginPath();ctx.arc(x(4),yy,13,0,2*Math.PI);ctx.stroke();
        const angle=order.total_phase_pi*Math.PI;
        line(ctx,[[x(4),yy],[x(4)+11*Math.cos(angle),yy-11*Math.sin(angle)]],color,1.6);
        ctx.globalAlpha=1;
      }
    }else{dot(ctx,x(4),yy,3,'#68768a');}
    if(major){ctx.fillStyle=order.passed?color:'#68768a';ctx.textAlign='left';ctx.fillText(`${order.order>0?'+':''}${order.order}${order.passed?'':` ${tr('blocked')}`}`,x(4)+18,yy+4);ctx.textAlign='center';}
  });
  ctx.fillStyle=colors.muted;ctx.font='12px system-ui';
  ctx.fillText(tr('collimated'),x(1),351);
  ctx.fillText(tr('relay'),x(4),351);
  canvas.dataset.transmitted=data.active_orders.join(',');
  canvas.dataset.blocked=rays.filter(q=>!q.passed).map(q=>q.order).join(',');
  canvas.dataset.rayCount=String(rays.length*maskPoints.length);
  canvas.dataset.geometry='thin-lens-6f';
}
function axes(id,xmin,xmax,ymin,ymax,xlabel,ylabel,rightMargin=18){
  const s=surface(id);if(!s)return null;
  const {ctx,w,h}=s,left=44,right=w-rightMargin,top=24,bottom=h-36;
  const sx=v=>left+(v-xmin)/(xmax-xmin)*(right-left),sy=v=>bottom-(v-ymin)/(ymax-ymin)*(bottom-top);
  ctx.font='11px system-ui';ctx.fillStyle=colors.muted;
  const ticks=w<450?2:4;
  for(let i=0;i<=ticks;i++){
    const value=ymin+(ymax-ymin)*i/ticks;
    line(ctx,[[left,sy(value)],[right,sy(value)]],colors.grid);
    ctx.textAlign='right';ctx.fillText(f(value,Math.abs(ymax-ymin)<1?2:1),left-7,sy(value)+4);
    const xx=xmin+(xmax-xmin)*i/ticks;ctx.textAlign='center';ctx.fillText(f(xx,1),sx(xx),bottom+17);
  }
  ctx.textAlign='left';ctx.fillText(ylabel,3,13);ctx.textAlign='center';ctx.fillText(xlabel,(left+right)/2,h-4);
  return {...s,left,right,top,bottom,sx,sy};
}
function curve(ctx,x,values,sx,sy,color,width=2,dash=[]){
  ctx.save();ctx.strokeStyle=color;ctx.lineWidth=width;ctx.setLineDash(dash);ctx.beginPath();
  for(let k=0;k<x.length;k++)k?ctx.lineTo(sx(x[k]),sy(values[k])):ctx.moveTo(sx(x[k]),sy(values[k]));
  ctx.stroke();ctx.restore();
}
function drawPupil(data,p){
  const extent=Math.max(p.na*1.2,Math.min(2,Math.abs(p.source_u)+1.5*data.u0));
  const ymax=Math.max(.12,...data.spectrum.map(s=>Math.abs(s.coefficient)*1.25));
  const a=axes('pupil-chart',-extent,extent,0,ymax,tr('pupilAxis'),'|cⱼ|',49);if(!a)return;
  const {ctx,sx,sy,top,bottom,w}=a;
  ctx.fillStyle='rgba(56,189,248,.08)';ctx.fillRect(sx(-p.na),top,sx(p.na)-sx(-p.na),bottom-top);
  [-p.na,p.na].forEach(u=>line(ctx,[[sx(u),top],[sx(u),bottom]],colors.blue,1,.6,[3,4]));
  data.spectrum.filter(s=>Math.abs(s.u)<=extent).forEach(s=>{
    const amp=Math.abs(s.coefficient),c=s.passed?orderColor(s.order):'#526176';
    line(ctx,[[sx(s.u),bottom],[sx(s.u),sy(amp)]],c,2.3);dot(ctx,sx(s.u),sy(amp),3,c);
    if(amp>.025&&(Math.abs(s.order)<=1||data.spectrum.length<15)){ctx.fillStyle=c;ctx.textAlign='center';ctx.fillText(`${s.order>0?'+':''}${s.order}`,sx(s.u),sy(amp)-8);}
  });
  const us=Float64Array.from({length:101},(_,k)=>-p.na+2*p.na*k/100);
  const phi=Float64Array.from(us,u=>phaseRate(u,p.wavelength_nm/1000,p.phase_model)*p.focus_um/Math.PI);
  const max=Math.max(.1,...phi.map(Math.abs)),py=v=>(top+bottom)/2-v/max*(bottom-top)/2;
  curve(ctx,us,phi,sx,py,colors.pink,1.4);
  ctx.textAlign='right';ctx.fillStyle=colors.pink;ctx.fillText(`+${f(max,1)}π`,w-2,top+4);ctx.fillText(`−${f(max,1)}π`,w-2,bottom);
}
function drawImage(data){
  const a=axes('image-chart',-1.5,1.5,0,Math.max(1.35,data.maximum_bound*1.07),tr('imageAxis'),tr('intensityAxis'));if(!a)return;
  curve(a.ctx,data.x_over_pitch,data.mask,a.sx,a.sy,'#69788f',1.1,[5,4]);
  curve(a.ctx,data.x_over_pitch,data.intensity,a.sx,a.sy,colors.blue,2.1);
}
function drawField(data){
  if(!document.getElementById('field-detail').open)return;
  const max=Math.max(.2,...data.re.map(Math.abs),...data.im.map(Math.abs))*1.1;
  const a=axes('field-chart',-1.5,1.5,-max,max,tr('waferAxis'),tr('fieldAxis'));if(!a)return;
  curve(a.ctx,data.x_over_pitch,data.re,a.sx,a.sy,colors.blue);curve(a.ctx,data.x_over_pitch,data.im,a.sx,a.sy,colors.pink);
}
function drawFocus(focus){
  if(!focusDetail.open)return;
  const a=axes('focus-chart',-1.5,1.5,-1,1,tr('waferAxis'),tr('focusAxis'));if(!a)return;
  if(map&&map.key===preparedKey){
    a.ctx.drawImage(map.image,a.left,a.top,a.right-a.left,a.bottom-a.top);
    line(a.ctx,[[a.left,a.sy(focus)],[a.right,a.sy(focus)]],colors.blue,1.8,1,[6,4]);
    text('color-maximum',f(map.maximum,3));
  }
}
function ensureWorker(){
  if(worker||mapFailed)return;
  try{
    worker=new Worker(new URL('./simulator-worker.js',import.meta.url),{type:'module'});
    worker.onmessage=({data})=>{
      workerBusy=false;inFlightKey=null;
      if(data.key===preparedKey){
        if(data.error){text('map-status',tr('mapError',{error:data.error}));}
        else{
          const image=document.createElement('canvas');image.width=data.columns;image.height=data.rows;
          image.getContext('2d').putImageData(new ImageData(new Uint8ClampedArray(data.pixels),data.columns,data.rows),0,0);
          map={key:data.key,image,maximum:data.maximum};text('map-status',tr('mapReady'));
          if(latest)drawFocus(latest.data.focus_um);
        }
      }
      runPendingMap();
    };
    worker.onerror=()=>{mapFailed=true;workerBusy=false;worker.terminate();worker=null;text('map-status',tr('mapUnavailable'));};
  }catch(_error){mapFailed=true;text('map-status',tr('mapUnavailable'));}
}
function runPendingMap(){
  if(!pendingMap||workerBusy||!focusDetail.open)return;
  ensureWorker();if(!worker)return;
  const next=pendingMap;pendingMap=null;
  if(next.key!==preparedKey||(map&&map.key===next.key))return;
  workerBusy=true;inFlightKey=next.key;worker.postMessage(next);
}
function requestMap(config,key){
  if(!focusDetail.open||mapFailed||key===inFlightKey||(map&&map.key===key))return;
  pendingMap={config,key};text('map-status',tr('mapCalculating'));runPendingMap();
}
function renderTable(data){
  if(!document.getElementById('spectrum-detail').open)return;
  const tbody=document.getElementById('spectrum-body');tbody.replaceChildren();
  data.spectrum.forEach(s=>{const row=document.createElement('tr');
    [s.order,f(s.u,3),f(s.coefficient,5),!s.passed?tr('blocked'):s.nonzero?tr('passed'):tr('zeroCoefficient'),s.total_phase_pi===null?'—':f(s.total_phase_pi,3)].forEach(value=>{const cell=document.createElement('td');cell.textContent=value;row.append(cell);});tbody.append(row);
  });
}
function updateOutputs(){
  ['duty_ratio','na','source_u','focus_um','max_order'].forEach(name=>{document.getElementById(`${name}-value`).value=f(el[name].value,name==='max_order'?0:name==='source_u'?3:2);});
  document.getElementById('frequency_u-value').value=f(Number(el.wavelength_nm.value)/Number(el.pitch_nm.value),3);
}
function syncFrequency(){
  const wavelength=Number(el.wavelength_nm.value),pitch=Number(el.pitch_nm.value);
  if(!(wavelength>=100&&wavelength<=1000&&pitch>=100&&pitch<=3000))return;
  const u=wavelength/pitch;
  frequency.min=Math.max(wavelength/3000,Math.min(.15,u));frequency.max=Math.min(wavelength/100,Math.max(.9,u));frequency.step='any';frequency.value=u;
}
function draw(){
  frame=0;const start=performance.now();updateOutputs();
  const error=document.getElementById('error-message');
  if(!form.checkValidity()){
    error.textContent=tr('inputError');error.hidden=false;
    text('calculation-status',tr('inputStatus'));document.getElementById('results').setAttribute('aria-busy','false');return;
  }
  error.hidden=true;
  const config=Object.fromEntries(Object.keys(defaults).map(name=>[name,name==='phase_model'?el[name].value:Number(el[name].value)]));
  const key=JSON.stringify(config),focus=Number(el.focus_um.value);
  if(key!==preparedKey){prepared=prepareGrating(config);preparedKey=key;pendingMap=null;}
  const data=evaluateImage(prepared,focus,true),p={...config,focus_um:focus};latest={data,parameters:p};
  drawRays(data,p);drawPupil(data,p);drawImage(data);drawField(data);drawFocus(focus);renderTable(data);
  text('active-orders',data.active_orders.length?data.active_orders.map(j=>j>0?`+${j}`:j).join(', '):tr('none'));text('contrast',`${f(data.contrast*100,1)}%`);
  text('current-focus',`z = ${f(focus)} µm`);text('source-description',tr('sourceReadout',{angle:f(data.source_angle_deg,1),pitch:f(config.pitch_nm,1)}));
  text('defocus-description',Math.abs(focus)<1e-12?tr('bestFocus'):tr('focusReadout',{focus:f(focus)}));
  const warning=document.getElementById('truncation-warning');warning.hidden=!data.omitted_orders.length;
  if(data.omitted_orders.length)warning.textContent=tr('truncation',{orders:data.omitted_orders.join(', ')});
  text('calculation-status',tr('liveStatus'));const results=document.getElementById('results');results.setAttribute('aria-busy','false');
  results.dataset.frameMs=f(performance.now()-start,2);results.dataset.focus=String(focus);results.dataset.model=config.phase_model;
  languageURL.hash=new URLSearchParams({...config,focus_um:focus}).toString();languageLink.href=languageURL.href;
  requestMap(config,key);
}
function schedule(){if(!frame)frame=requestAnimationFrame(draw);}
function apply(values,preset){
  Object.entries({...defaults,focus_um:0,...values}).forEach(([name,value])=>el[name].value=value);
  syncFrequency();document.querySelectorAll('[data-preset]').forEach(button=>button.dataset.active=String(button.dataset.preset===preset));schedule();
}
form.addEventListener('submit',event=>event.preventDefault());
form.addEventListener('input',event=>{
  if(event.target===frequency)el.pitch_nm.value=Number(el.wavelength_nm.value)/Number(frequency.value);
  else if(event.target===el.pitch_nm||event.target===el.wavelength_nm)syncFrequency();
  document.querySelectorAll('[data-preset]').forEach(button=>button.dataset.active='false');schedule();
});
form.addEventListener('change',schedule);
for(const id of ['field-detail','focus-detail','spectrum-detail','advanced-controls'])document.getElementById(id).addEventListener('toggle',schedule);
window.addEventListener('resize',schedule);
document.getElementById('reset').addEventListener('click',()=>apply({}));
document.querySelectorAll('[data-preset]').forEach(button=>button.addEventListener('click',()=>{
  const name=button.dataset.preset;
  apply(name==='two'?{pitch_nm:620,source_u:-.2,na:.5}:name==='even'?{pitch_nm:1240,duty_ratio:.3,na:.7,max_order:5}:{},name);
}));
// Language links carry valid physical settings in the fragment, without API calls.
const restored={};
for(const [name,value] of new URLSearchParams(location.hash.slice(1))){
 if(!fields.includes(name))continue;
 if(name==='phase_model'){
  if(['paraxial','angular'].includes(value))restored[name]=value;
 }else{
  const input=el[name],number=Number(value);
  if(value.trim()&&Number.isFinite(number)&&number>=Number(input.min)&&number<=Number(input.max)
      &&(name!=='max_order'||Number.isInteger(number)))restored[name]=number;
 }
}
if(Object.keys(restored).length)apply(restored);
else{syncFrequency();schedule();}
