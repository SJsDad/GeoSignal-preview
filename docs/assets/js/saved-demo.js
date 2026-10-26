/* Saved presentation results only: no layout engine, calibration or new simulation. */
(() => {
  'use strict';
  const messages = {
    ko: {ready:'후보를 선택해 저장된 결과를 살펴보세요.',error:'결과를 불러오지 못했습니다. 새로고침하거나 아래 대표 그림을 확인해 주세요.',width:'선폭',space:'간격',candidate:'후보',available:'{total}개 저장 예시 중 {shown}개 표시',view:'크게 보기',none:'비교 기록 없음',missing:'측정 불가',measured:'측정됨',default:'정초점 · 세 상대 도즈의 윤곽 비교 · x/y는 검토 위치 기준 µm입니다.',condition:'초점 {focus} µm · 상대 도즈 {dose} · 파란 윤곽은 선택 조건입니다.',chart:'초점별 모델 치수, 상대 도즈 3개 비교. 측정 불가 값은 연결하지 않습니다.',axis:'모델 치수 (nm)',focus:'초점 (µm)',dose:'도즈'},
    en: {ready:'Select a candidate to explore its saved results.',error:'Could not load the results. Refresh or see the representative figures below.',width:'Width',space:'Space',candidate:'Candidate',available:'Showing {shown} of {total} saved examples',view:'Inspect',none:'No comparison record',missing:'Not measurable',measured:'Measured',default:'Best focus · Contours at three relative doses · x/y in µm relative to the review point.',condition:'Focus {focus} µm · Relative dose {dose} · Blue contour marks the selected condition.',chart:'Modeled dimension across focus for three relative doses. Unavailable measurements are not connected.',axis:'Modeled dimension (nm)',focus:'Focus (µm)',dose:'Dose'}
  };
  for (const root of document.querySelectorAll('[data-demo-viewer]')) init(root);
  async function init(root) {
    const lang=root.dataset.language==='ko'?'ko':'en',labels=messages[lang];
    const tr=(key,values={})=>labels[key].replace(/\{(\w+)\}/g,(_,name)=>String(values[name]??''));
    const el=name=>root.querySelector(`[data-${name}]`);
    const number=(value,digits=2)=>Number(value).toFixed(digits);
    const status=el('viewer-status'),content=el('viewer-content');
    const url=new URL(root.dataset.source,location.href);
    let data,layer=67,kind='width',selected=null,limit=6,focus=0,dose=1;
    try {
      const response=await fetch(url);if(!response.ok)throw new Error('Results unavailable');data=await response.json();
      if(data.version!==1||!Array.isArray(data.layers))throw new Error('Unsupported results');
    } catch (_) {status.textContent=tr('error');root.dataset.state='error';return;}
    const imageURL=path=>new URL(path,url).href;
    const candidates=()=>data.layers.find(item=>item.layer===layer).candidates.filter(item=>item.kind===kind);
    const current=()=>candidates().find(item=>item.id===selected)||candidates()[0];
    const sample=()=>current().samples.find(item=>item.focus_um===focus&&item.relative_dose===dose);
    function selectSample(value) {
      focus=value.focus_um;dose=value.relative_dose;el('focus').value=String(focus);el('dose').value=String(dose);renderDetail();
      root.querySelector(`[data-sample="${focus},${dose}"]`)?.focus({preventScroll:true});
    }
    function render() {
      const available=candidates();if(!available.some(item=>item.id===selected))selected=available[0].id;
      limit=Math.min(limit,available.length);el('count').value=String(limit);
      for(const option of el('count').options)option.disabled=Number(option.value)>available.length;
      el('gallery-note').textContent=tr('available',{total:available.length,shown:limit});
      for(const button of root.querySelectorAll('[data-kind]'))button.setAttribute('aria-pressed',String(button.dataset.kind===kind));
      const cards=el('cards');cards.replaceChildren();
      for(const candidate of available.slice(0,limit)) {
        const button=document.createElement('button');button.type='button';button.className='saved-card';button.dataset.candidate=candidate.id;
        button.setAttribute('aria-pressed',String(candidate.id===selected));
        const image=document.createElement('img');image.src=imageURL(candidate.image);image.alt=`${tr(kind)} ${candidate.number}`;image.loading='lazy';image.width=300;image.height=250;
        const title=document.createElement('strong');title.textContent=`${tr(kind)} ${candidate.number}`;
        const meta=document.createElement('span');meta.textContent=`${number(candidate.geometry_nm,0)} nm · ${tr('view')}`;
        button.append(image,title,meta);button.addEventListener('click',()=>{selected=candidate.id;render();root.querySelector(`[data-candidate="${selected}"]`)?.focus({preventScroll:true});});cards.append(button);
      }
      renderDetail();
    }
    function renderDetail() {
      const candidate=current(),condition=sample(),expanded=el('comparison').open;
      const image=expanded&&condition?condition.image:candidate.image;
      el('selected-title').textContent=`${layer}/20 · ${tr(kind)} ${candidate.number}`;
      el('geometry').textContent=`${number(candidate.geometry_nm,0)} nm`;
      const measurement=expanded?condition:candidate.samples.find(item=>item.focus_um===0&&item.relative_dose===1);
      el('measured').textContent=!measurement?tr('none'):measurement.cd_nm===null?tr('missing'):`${number(measurement.cd_nm)} nm`;
      el('selected-image').src=imageURL(image);el('selected-image').alt=el('selected-title').textContent;
      el('open-image').href=imageURL(image);
      el('image-caption').textContent=expanded&&condition?tr('condition',{focus:number(focus),dose:number(dose)}):tr('default');
      const hasComparison=candidate.samples.length>0;el('no-comparison').hidden=hasComparison;el('comparison-content').hidden=!hasComparison;
      root.dataset.layer=String(layer);root.dataset.kind=kind;root.dataset.selected=candidate.id;root.dataset.focus=String(focus);root.dataset.dose=String(dose);
      const table=el('measurements');table.replaceChildren();
      const grid=el('comparison-grid');grid.replaceChildren();
      for(const point of candidate.samples) {
        const active=point.focus_um===focus&&point.relative_dose===dose;
        const row=document.createElement('tr');row.dataset.selected=String(active);
        for(const value of [number(point.focus_um),number(point.relative_dose),point.cd_nm===null?'—':number(point.cd_nm),tr(point.cd_nm===null?'missing':'measured')]) {const cell=document.createElement('td');cell.textContent=value;row.append(cell);}table.append(row);
        const button=document.createElement('button');button.type='button';button.className='saved-sample';button.setAttribute('aria-pressed',String(active));
        button.dataset.sample=`${point.focus_um},${point.relative_dose}`;
        const thumb=document.createElement('img');thumb.src=imageURL(point.image);thumb.alt=`${tr('focus')} ${number(point.focus_um)} · ${tr('dose')} ${number(point.relative_dose)}`;thumb.loading='lazy';thumb.width=300;thumb.height=250;
        const label=document.createElement('span');label.textContent=`${number(point.focus_um)} µm · ${number(point.relative_dose)}`;
        button.append(thumb,label);button.addEventListener('click',()=>selectSample(point));grid.append(button);
      }
      drawChart();
    }
    function drawChart() {
      const host=el('bossung'),points=current().samples;if(!points.length||!el('comparison').open){host.replaceChildren();return;}
      const width=Math.max(240,Math.round(host.getBoundingClientRect().width)),height=260;
      const left=48,right=width-16,top=60,bottom=218;
      const values=points.filter(p=>p.cd_nm!==null).map(p=>p.cd_nm),low=Math.floor(Math.min(...values)/10)*10-5,high=Math.ceil(Math.max(...values)/10)*10+5;
      const x=value=>left+(value+.2)/.4*(right-left),y=value=>bottom-(value-low)/(high-low)*(bottom-top);
      const ns='http://www.w3.org/2000/svg',svg=document.createElementNS(ns,'svg');svg.setAttribute('viewBox',`0 0 ${width} ${height}`);svg.setAttribute('role','img');svg.setAttribute('aria-label',tr('chart'));
      const add=(tag,attrs,text)=>{const node=document.createElementNS(ns,tag);for(const [key,value] of Object.entries(attrs))node.setAttribute(key,value);if(text!==undefined)node.textContent=text;svg.append(node);return node;};
      add('text',{x:3,y:14,'font-size':12,fill:'#455766'},tr('axis'));
      for(let i=0;i<5;i++){const value=low+(high-low)*i/4;add('path',{d:`M${left} ${y(value)}H${right}`,stroke:'#e2e8ee',fill:'none'});add('text',{x:left-8,y:y(value)+4,'text-anchor':'end','font-size':11,fill:'#576774'},number(value,0));}
      for(const f of [-.2,0,.2])add('text',{x:x(f),y:bottom+18,'text-anchor':'middle','font-size':11,fill:'#576774'},number(f));
      add('text',{x:(left+right)/2,y:height-3,'text-anchor':'middle','font-size':12,fill:'#576774'},tr('focus'));
      for(const [i,d] of [.9,1,1.1].entries()) {
        const color=['#1672c4','#24715b','#cf6d1c'][i];add('text',{x:8+i*(width-12)/3,y:37,'font-size':11,fill:color},`${tr('dose')} ${number(d)}`);
        let previous=null;
        for(const point of points.filter(p=>p.relative_dose===d).sort((a,b)=>a.focus_um-b.focus_um)) {
          if(point.cd_nm===null){previous=null;continue;}
          const xx=x(point.focus_um),yy=y(point.cd_nm);
          if(previous)add('path',{d:`M${previous[0]} ${previous[1]}L${xx} ${yy}`,stroke:color,'stroke-width':2,fill:'none'});
          add('circle',{cx:xx,cy:yy,r:4,fill:color});previous=[xx,yy];
        }
      }
      host.replaceChildren(svg);
    }
    el('layer').addEventListener('change',event=>{layer=Number(event.target.value);selected=null;limit=layer===67?6:1;render();});
    for(const button of root.querySelectorAll('[data-kind]'))button.addEventListener('click',()=>{kind=button.dataset.kind;selected=null;render();});
    el('count').addEventListener('change',event=>{limit=Number(event.target.value);if(!candidates().slice(0,limit).some(item=>item.id===selected))selected=null;render();});
    el('focus').addEventListener('change',event=>{focus=Number(event.target.value);renderDetail();});
    el('dose').addEventListener('change',event=>{dose=Number(event.target.value);renderDetail();});
    el('comparison').addEventListener('toggle',renderDetail);
    let resize=0;window.addEventListener('resize',()=>{cancelAnimationFrame(resize);resize=requestAnimationFrame(drawChart);});
    content.hidden=false;status.textContent=tr('ready');root.dataset.state='ready';render();
  }
})();
