'use strict';
// One local scroll progress per scene; no timers or gesture interception.
window.SKIM_PART2=(()=>{
 const data=window.PART_TWO_DATA;
 const config={fadeIn:.20,fadeOut:.82,notifications:[.06,.21,.36,.51],noticeSpan:.08,outro:[.68,.78],density:[[.08,.42],[.55,.85]],densityFade:.05,messagesIn:[.12,.24],messagesMove:[.42,.70],highlight:[.74,.82]};
 const clamp=x=>Math.max(0,Math.min(1,x)),ramp=(p,a,b)=>clamp((p-a)/(b-a)),smooth=x=>x*x*(3-2*x),opacity=(n,a)=>{n.style.opacity=a;n.setAttribute('aria-hidden',a<.01?'true':'false')};
 const fade=p=>Math.min(ramp(p,0,config.fadeIn),1-ramp(p,config.fadeOut,1));
 const nodes=[...document.querySelectorAll('[data-part2]')],footer=document.querySelector('.p2-footer');
 for(const scene of nodes)scene.dataset.scrollTravel=data.sequence.find(item=>item.id===scene.dataset.part2).travel;
 const density=document.querySelector('.p2-density');
 const place=(n,box)=>['x','y','w','h'].forEach((key,i)=>n.style.setProperty('--'+key,box[i]));
 const objects=data.objects.map(o=>{
  const n=document.createElement('div');n.id=o.id;n.className='p2-density-object'+(o.kind==='star'?' p2-density-star':'');place(n,o.box);n.dataset.stage=o.stage;
  if(o.kind!=='star'){
   const strip=document.createElement('div');strip.className='p2-strip';strip.style.setProperty('--length',Math.max(o.box[2],o.box[3]));
   if(o.angle===90){strip.style.left='calc(83*var(--u))';strip.style.transform='rotate(90deg)'}
   if(o.angle===-90){strip.style.top='calc('+o.box[3]+'*var(--u))';strip.style.transform='rotate(-90deg)'}
   for(const word of data.templates[o.template]){const w=document.createElement('span');w.className='p2-strip-word p2-font-'+word.font;w.textContent=word.text;w.style.setProperty('--wx',word.x+(word.inkLeft||0));w.style.setProperty('--wy',word.y-(word.inkTop||0));w.style.setProperty('--font-size',word.fontSize||word.h*1.22);w.style.transform=`scaleX(${word.inkScale||1})`;strip.append(w)}n.append(strip);
  }density.append(n);return {...o,node:n};
 });
 const grid=document.querySelector('.p2-people-grid');
 const people=data.people.map((box,i)=>{const n=document.createElement('span');n.className='p2-person';place(n,box);n.dataset.person=i;n.innerHTML='<i class="p2-head"></i><i class="p2-torso"></i><i class="p2-arm p2-arm--left"></i><i class="p2-arm p2-arm--right"></i><i class="p2-leg p2-leg--left"></i><i class="p2-leg p2-leg--right"></i>';grid.append(n);return n});
 const layer=document.querySelector('.p2-people-message-layer');
 const messages=data.messages.map(m=>{const n=document.createElement('p');n.className='p2-people-message';place(n,m.box);n.textContent=m.text;layer.append(n);return {node:n,distance:0}});
 document.querySelectorAll('.p2-notice').forEach((n,i)=>n.style.setProperty('--notice-index',i));
 const stageObjects=[1,2].map(stage=>objects.filter(o=>o.stage===stage).sort((a,b)=>a.z[stage]-b.z[stage]));
 function measure(){
  const compact=matchMedia('(max-width:1100px)').matches;
  objects.forEach((o,i)=>{
   const n=o.node;
   if(!compact){n.style.removeProperty('--u');n.style.removeProperty('left');n.style.removeProperty('top');n.style.removeProperty('width');n.style.removeProperty('height');return}
   const star=o.kind==='star',w=density.clientWidth;
   const length=Math.max(o.box[2],o.box[3]);
   // Recompose the strips across the viewport rather than shrink the artboard.
   const unit=star?0.65:Math.min((w*.82)/length,.85);
   n.style.setProperty('--u',unit+'px');
   n.style.left=(star?8+(i*31)%78:4+(i*13)%10)+'%';
   n.style.top=(4+(i*17)%84)+'%';
   n.style.width=(star?50:w*.82)+'px';n.style.height=(star?50:83*unit)+'px';
   const strip=n.querySelector('.p2-strip');
   if(strip){
    strip.style.transform='none';strip.style.left='0';strip.style.top='0';
    const origin=n.getBoundingClientRect().left;
    const inkRight=Math.max(...[...strip.children].map(word=>word.getBoundingClientRect().right-origin));
    if(inkRight>w*.82)n.style.setProperty('--u',(unit*w*.82/inkRight)+'px');
   }
  });
  if(!compact)objects.forEach(o=>{const strip=o.node.querySelector('.p2-strip');if(strip){strip.style.left=o.angle===90?'calc(83*var(--u))':'';strip.style.top=o.angle===-90?'calc('+o.box[3]+'*var(--u))':'';strip.style.transform=o.angle?'rotate('+o.angle+'deg)':''}});
  messages.forEach((m,i)=>m.node.style.setProperty('--message-index',i));
  for(const m of messages){const old=m.node.style.transform;m.node.style.transform='none';m.distance=layer.getBoundingClientRect().right-m.node.getBoundingClientRect().left+Math.max(32,layer.clientWidth*24/1680);m.node.style.transform=old}
 }
 function render(scene,p,{reference=false,reduced=false}={}){
  const key=scene.dataset.part2,all=s=>[...scene.querySelectorAll(s)],one=s=>scene.querySelector(s),frame=+(new URLSearchParams(location.search).get('referenceFrame')||0);
  if(key==='words'||key==='question'||key==='try-reading')opacity(one('.p2-fading-quote'),reference||reduced?1:fade(p));
  if(key==='notifications'){
   let active=-1;all('.p2-notice').forEach((n,i)=>{const a=reference||reduced?1:ramp(p,config.notifications[i],config.notifications[i]+config.noticeSpan);opacity(n,a);if(a>0)active=i});
   all('.p2-indicator i').forEach((n,i)=>n.classList.toggle('is-active',i===active));opacity(one('.p2-notice-outro'),reference||reduced?1:ramp(p,...config.outro));
  }
  if(key==='replies')all('.p2-reply').forEach((n,i)=>opacity(n,reduced?1:reference?(i===(frame>=67&&frame<=69?frame-67:2)?1:0):fade(p*3-i)));
  if(key==='density'){
   if(reference)p=frame===70?0:frame===72?.5:1;if(reduced)p=1;
   const stage=p<.5?0:p<1?1:2;
   for(const o of objects){let a=1;if(o.stage){const list=stageObjects[o.stage-1],index=list.indexOf(o),[a0,a1]=config.density[o.stage-1],at=a0+(a1-a0)*index/Math.max(1,list.length-1);a=ramp(p,at,at+config.densityFade)}opacity(o.node,a);o.node.style.zIndex=o.z[stage]??o.z[o.stage];o.node.style.transform=`translateY(${(1-a)*8}px)`}
  }
  if(key==='after-scroll'){
   if(reference)p=frame===74?.25:.83;
   const mix=reduced?1:ramp(p,.43,.60);one('.p2-bg--light').style.opacity=mix;scene.style.backgroundColor=`rgb(${9+235*mix},${9+235*mix},${9+235*mix})`;
   opacity(one('.p2-after-dark'),reduced?1:Math.min(ramp(p,0,.10),1-ramp(p,.36,.47)));opacity(one('.p2-after-light'),reduced?1:Math.min(ramp(p,.62,.72),1-ramp(p,.96,1)));
  }
  if(key==='people'){
   if(reference)p=frame===76?0:frame===77?.35:1;if(reduced)p=1;
   const a=reduced?0:ramp(p,...config.messagesIn),move=smooth(ramp(p,...config.messagesMove)),h=ramp(p,...config.highlight);
   for(const m of messages){opacity(m.node,a);m.node.style.transform=`translateX(${move*m.distance}px)`}
   people[data.selectedPerson].style.color=`rgb(${9+69*h},${9+161*h},${9+246*h})`;
   opacity(one('.p2-people-heading--initial'),1-h);opacity(one('.p2-people-heading--final'),h);footer.style.visibility=p>=1?'visible':'hidden';
  }
 }
 return {config,data,objects,people,messages,nodes,measure,render};
})();
