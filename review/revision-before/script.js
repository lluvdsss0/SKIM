'use strict';
/* Shared motion settings. Scene text is edited directly in index.html. */
const CONFIG=Object.freeze({snapDistance:.12,snapDelay:180,snapDuration:280,folderShift:865,folderStart:.18,folderSpan:.62,scanShift:230,scanStart:.15,scanSpan:.70,scanAcceleration:2.5,pulseDuration:2300,scatterDuration:850,cardStart:.10,cardStagger:.045,cardReveal:.18,cardRise:700,readStart:.14,readSpan:.41,readMinPercent:.05,readMaxPercent:.40,phraseIn:.12,phraseFade:.22,phraseOut:.88,arrowStart:.20,starStart:.45,finalFade:.22});
const $=(s,r=document)=>r.querySelector(s),$$=(s,r=document)=>[...r.querySelectorAll(s)];
const clamp=(v,a=0,b=1)=>Math.max(a,Math.min(b,v)),ease=t=>1-Math.pow(1-clamp(t),3);
const scenes=$$('.scene'),reduced=matchMedia('(prefers-reduced-motion: reduce)'),mobile=matchMedia('(max-width:1000px)'),reference=new URLSearchParams(location.search).has('reference');
document.documentElement.style.setProperty('--pulse-duration',CONFIG.pulseDuration+'ms');
let renderFrame=0,snapFrame=0,snapTimer=0,autoScrolling=false,dragging=false,lastScroll=scrollY,lastDirection=0;
function progress(scene){const r=scene.getBoundingClientRect();return clamp((innerHeight-r.top)/(r.height+innerHeight))}
function cancelSnap(){clearTimeout(snapTimer);cancelAnimationFrame(snapFrame);snapFrame=0;autoScrolling=false}
function snap(){if(dragging||reduced.matches||reference)return;const current=scrollY,candidates=scenes.map(s=>s.offsetTop),target=candidates.reduce((a,b)=>Math.abs(b-current)<Math.abs(a-current)?b:a);if(Math.abs(target-current)>innerHeight*CONFIG.snapDistance||Math.abs(target-current)<2||(target-current)*lastDirection<0)return;autoScrolling=true;const start=performance.now();const tick=now=>{const t=clamp((now-start)/CONFIG.snapDuration);scrollTo(0,current+(target-current)*ease(t));if(t<1)snapFrame=requestAnimationFrame(tick);else{autoScrolling=false;snapFrame=0}};snapFrame=requestAnimationFrame(tick)}
// Tooltip remains open across the trigger-to-tooltip gap; click pins it for touch.
const definition=$('.definition'),trigger=$('.definition-trigger');
function syncExpanded(){trigger.setAttribute('aria-expanded',definition.classList.contains('open')||definition.matches(':hover,:focus-within')?'true':'false')}
trigger.addEventListener('click',()=>{definition.classList.toggle('open');syncExpanded()});
for(const event of ['pointerenter','pointerleave','focusin','focusout'])definition.addEventListener(event,()=>requestAnimationFrame(syncExpanded));
document.addEventListener('pointerdown',e=>{if(!definition.contains(e.target)){definition.classList.remove('open');syncExpanded()}});
document.addEventListener('keydown',e=>{if(e.key==='Escape'){definition.classList.remove('open');trigger.blur();syncExpanded()}});
$('.learn').addEventListener('click',e=>{e.preventDefault();cancelSnap();scenes[1].scrollIntoView({behavior:reduced.matches?'instant':'smooth'})});
// Preserve every whitespace text node and explicit line break while wrapping words.
const paragraph=$('.reading-paragraph'),walker=document.createTreeWalker(paragraph,NodeFilter.SHOW_TEXT),textNodes=[];while(walker.nextNode())textNodes.push(walker.currentNode);
for(const node of textNodes){const fragment=document.createDocumentFragment();for(const word of node.textContent.split(/(\s+)/)){if(!word)continue;if(/^\s+$/.test(word))fragment.append(document.createTextNode(word));else{const span=document.createElement('span');span.className='reading-word';span.textContent=word;fragment.append(span)}}node.replaceWith(fragment)}
const readingWords=$$('.reading-word'),counter=$('.counter-tape'),runner=$('.read-runner');
// Text capacity is measured against the actual container, not an estimated character count.
const range=$('#text-size'),copy=$('.resize-copy'),fullText=copy.textContent.trim(),articleWords=fullText.split(/\s+/),sizeThumb=$('.size-thumb'),sizeControl=$('.text-size-control');
function fitCopy(){const value=+range.value,scale=$('.composition',scenes[8]).clientWidth/1680,fontSize=(mobile.matches?12:Math.max(11.8,12*scale))+(value-10)*(mobile.matches?1:scale);copy.style.fontSize=fontSize+'px';let lo=0,hi=articleWords.length;
 while(lo<hi){const mid=Math.ceil((lo+hi)/2);copy.textContent=articleWords.slice(0,mid).join(' ');if(copy.scrollHeight<=copy.clientHeight+.5)lo=mid;else hi=mid-1}
 copy.textContent=articleWords.slice(0,lo).join(' ');const t=(value-+range.min)/(+range.max-+range.min),thumbWidth=sizeThumb.offsetWidth;sizeThumb.style.left=(thumbWidth/2+(sizeControl.clientWidth-thumbWidth)*t)+'px';range.setAttribute('aria-valuetext',`${fontSize.toFixed(1)} пикселей — размер текста`)
}
range.addEventListener('input',fitCopy);range.addEventListener('pointerdown',()=>{dragging=true;cancelSnap()});range.addEventListener('keydown',cancelSnap);addEventListener('pointerup',()=>{dragging=false;clearTimeout(snapTimer)});addEventListener('pointercancel',()=>{dragging=false});
// Dome geometry is a normal convex polygon shared with stylesheet/dome.css.
// A bounding circle is safe for EVERY rotation of a symbol. Interpolating two
// valid circle centres stays valid throughout the motion in a convex domain.
const domeLayer=$('.dome-symbols'),symbols=$$('.dome-symbol').map(n=>({n,cx:+n.style.getPropertyValue('--x'),cy:+n.style.getPropertyValue('--y'),x:+n.style.getPropertyValue('--x'),y:+n.style.getPropertyValue('--y'),a:parseFloat(n.style.getPropertyValue('--angle')),frame:0}));
function domeMetrics(){const r=domeLayer.getBoundingClientRect();return{width:r.width,height:r.height,polygon:DOME_BOUNDARY.map(([x,y])=>[(840+(x-840)*.982)*r.width/1680,(875+(y-875)*.975)*r.height/1079])}}
function pointInside(x,y,polygon){let inside=false;for(let i=0,j=polygon.length-1;i<polygon.length;j=i++){const a=polygon[i],b=polygon[j];if((a[1]>y)!==(b[1]>y)&&x<(b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0])inside=!inside}return inside}
function circleInside(x,y,r,polygon){if(!pointInside(x,y,polygon))return false;for(let i=0;i<polygon.length;i++){const a=polygon[i],b=polygon[(i+1)%polygon.length],dx=b[0]-a[0],dy=b[1]-a[1],t=clamp(((x-a[0])*dx+(y-a[1])*dy)/(dx*dx+dy*dy||1)),distance=Math.hypot(x-a[0]-t*dx,y-a[1]-t*dy);if(distance<r)return false}return true}
function symbolRadius(s){return Math.hypot(s.n.offsetWidth,s.n.offsetHeight)/2+2}
function applySymbol(s,m=domeMetrics()){s.n.style.setProperty('--dx',(s.x-s.cx)*m.width/1680+'px');s.n.style.setProperty('--dy',(s.y-s.cy)*m.height/1079+'px');s.n.style.setProperty('--angle',s.a+'deg')}
function safeSymbol(s,m){const radius=symbolRadius(s);for(let i=0;i<30&&!circleInside(s.x*m.width/1680,s.y*m.height/1079,radius,m.polygon);i++){s.x+=(840-s.x)*.15;s.y+=(850-s.y)*.15}applySymbol(s,m)}
function scatter(){const m=domeMetrics();for(const s of symbols){cancelAnimationFrame(s.frame);safeSymbol(s,m);let x,y,found=false;const radius=symbolRadius(s);
 for(let k=0;k<1200;k++){x=260+Math.random()*1160;y=510+Math.random()*540;if(circleInside(x*m.width/1680,y*m.height/1079,radius,m.polygon)){found=true;break}}
 if(!found)continue;const from={x:s.x,y:s.y,a:s.a},to={x,y,a:Math.random()*360-180},start=performance.now();const tick=now=>{const t=reduced.matches?1:ease((now-start)/CONFIG.scatterDuration);s.x=from.x+(to.x-from.x)*t;s.y=from.y+(to.y-from.y)*t;s.a=from.a+(to.a-from.a)*t;applySymbol(s);if(t<1)s.frame=requestAnimationFrame(tick);else s.frame=0};s.frame=requestAnimationFrame(tick)
 }}
$('.break-button').addEventListener('click',scatter);
function render(){renderFrame=0;scenes.forEach((scene,i)=>{const r=scene.getBoundingClientRect(),visible=r.bottom>0&&r.top<innerHeight,p=progress(scene),complete=reference||reduced.matches;scene.classList.toggle('is-visible',visible);if(!visible&&!reference)return;const u=$('.composition',scene).clientWidth/1680;
 if(i===1){const maxShift=mobile.matches?Math.min(760,$('.folder-tape').scrollWidth-$('.folder-window').clientWidth):CONFIG.folderShift*u;$('.folder-tape').style.transform=`translateX(${complete?0:-maxShift*clamp((p-CONFIG.folderStart)/CONFIG.folderSpan)}px)`}
 if(i===2)$$('.scanner').forEach(n=>{const distance=mobile.matches?70:CONFIG.scanShift*u;n.style.transform=`translateX(${complete?0:+n.dataset.direction*distance*Math.pow(clamp((p-CONFIG.scanStart)/CONFIG.scanSpan),CONFIG.scanAcceleration)}px)`});
 if(i===3)$$('.card-motion').forEach((n,j)=>{const t=complete?1:ease((p-CONFIG.cardStart-j*CONFIG.cardStagger)/CONFIG.cardReveal);n.style.setProperty('--enter-y',(1-t)*(mobile.matches?240:CONFIG.cardRise*u)+'px');n.style.opacity=t});
 if(i===4)$('.revealing-phrase').style.opacity=complete?1:Math.min(clamp((p-CONFIG.phraseIn)/CONFIG.phraseFade),clamp((CONFIG.phraseOut-p)/CONFIG.phraseFade));
 if(i===5){const t=reference?0:reduced.matches?1:clamp((p-CONFIG.readStart)/CONFIG.readSpan);counter.style.transform=`translateX(${-t*7*100}%)`;const max=$('.read-track').clientWidth-runner.clientWidth;runner.style.transform=`translateX(${max*(CONFIG.readMaxPercent-CONFIG.readMinPercent)*t}px)`;readingWords.forEach((n,j)=>n.classList.toggle('is-read',j<Math.round(t*readingWords.length*.5)))}
 if(i===9){const local=clamp((innerHeight-r.top)/r.height);$('.collage-arrows').style.opacity=complete?1:clamp((local-CONFIG.arrowStart)/CONFIG.finalFade);$('.collage-stars').style.opacity=complete?1:clamp((local-CONFIG.starStart)/CONFIG.finalFade)}
 })}
addEventListener('scroll',()=>{const delta=scrollY-lastScroll;if(!autoScrolling&&delta)lastDirection=Math.sign(delta);lastScroll=scrollY;if(!renderFrame)renderFrame=requestAnimationFrame(render);if(!autoScrolling&&!dragging){clearTimeout(snapTimer);snapTimer=setTimeout(snap,CONFIG.snapDelay)}},{passive:true});
for(const type of ['wheel','touchstart','pointerdown','keydown'])addEventListener(type,cancelSnap,{passive:true});
let resizeFrame=0;function resized(){cancelAnimationFrame(resizeFrame);resizeFrame=requestAnimationFrame(()=>{fitCopy();const m=domeMetrics();symbols.forEach(s=>{cancelAnimationFrame(s.frame);s.frame=0;safeSymbol(s,m)});render()})}
new ResizeObserver(resized).observe(document.body);document.fonts.ready.then(resized);addEventListener('resize',resized);reduced.addEventListener('change',render);mobile.addEventListener('change',resized);
fitCopy();render();
window.SKIM={CONFIG,render,scatter,fitCopy,progress,symbols,domeMetrics,circleInside,symbolRadius,readingWords,fullText};
