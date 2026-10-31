'use strict';
/* Shared motion settings. Scene text is edited directly in index.html. */
const CONFIG=Object.freeze({
  // Controlled first-view episode; repeated input never resets this clock.
  holdMs:3000,entryVisibility:.65,entryAlignMs:200,finalSettleTolerance:24,
  // Final collage: words first, arrows, stars, then time to view the result.
  finalWordsMs:450,finalArrowsSpan:.20,finalStarsAt:.47,finalStarsSpan:.20,
  pulseDuration:1700,rightStepMs:240,toastMs:3000,
  snapDistance:.12,snapDelay:180,snapDuration:280,
  folderShift:865,scanShift:230,mobileScanRatio:.324,
  whiteDownRatio:.078,whiteUpRatio:.147,
  cardStart:.10,cardStagger:.045,cardReveal:.18,cardRise:700,
  phraseFadeInEnd:.30,phraseFadeOutStart:.65,
  readMinPercent:.05,readMaxPercent:.40,scatterDuration:850
});
const $=(s,r=document)=>r.querySelector(s),$$=(s,r=document)=>[...r.querySelectorAll(s)];
const clamp=(v,a=0,b=1)=>Math.max(a,Math.min(b,v)),ease=t=>1-Math.pow(1-clamp(t),3);
const scenes=$$('.scene'),reduced=matchMedia('(prefers-reduced-motion: reduce)'),mobile=matchMedia('(max-width:1000px)'),reference=new URLSearchParams(location.search).has('reference');
document.documentElement.style.setProperty('--pulse-duration',CONFIG.pulseDuration+'ms');
let renderFrame=0,snapFrame=0,snapTimer=0,autoScrolling=false,dragging=false,lastScroll=scrollY,lastDirection=0;
function cancelSnap(){clearTimeout(snapTimer);cancelAnimationFrame(snapFrame);snapFrame=0;autoScrolling=false}
function snap(){if(dragging||reduced.matches||reference||playback.active)return;const current=scrollY,candidates=scenes.map(s=>s.offsetTop),target=candidates.reduce((a,b)=>Math.abs(b-current)<Math.abs(a-current)?b:a);if(Math.abs(target-current)>innerHeight*CONFIG.snapDistance||Math.abs(target-current)<2||(target-current)*lastDirection<0)return;autoScrolling=true;const start=performance.now();const tick=now=>{const t=clamp((now-start)/CONFIG.snapDuration);scrollTo(0,current+(target-current)*ease(t));if(t<1)snapFrame=requestAnimationFrame(tick);else{autoScrolling=false;snapFrame=0}};snapFrame=requestAnimationFrame(tick)}
$('.learn').addEventListener('click',e=>{e.preventDefault();cancelSnap();scenes[1].scrollIntoView({behavior:reduced.matches?'instant':'smooth'})});
// Preserve every whitespace text node and explicit line break while wrapping words.
const paragraph=$('.reading-paragraph'),walker=document.createTreeWalker(paragraph,NodeFilter.SHOW_TEXT),textNodes=[];while(walker.nextNode())textNodes.push(walker.currentNode);
for(const node of textNodes){const fragment=document.createDocumentFragment();for(const word of node.textContent.split(/(\s+)/)){if(!word)continue;if(/^\s+$/.test(word))fragment.append(document.createTextNode(word));else{const span=document.createElement('span');span.className='reading-word';span.append(document.createTextNode(word));const bold=document.createElement('span');bold.className='word-bold';bold.textContent=word;bold.setAttribute('aria-hidden','true');span.append(bold);fragment.append(span)}}node.replaceWith(fragment)}
const readingWords=$$('.reading-word'),counter=$('.counter-tape'),runner=$('.read-runner');
function fitBoldWords(){for(const word of readingWords){const bold=$('.word-bold',word);if(!bold)continue;const regular=word.getBoundingClientRect().width,style=getComputedStyle(word),spacing=parseFloat(style.letterSpacing)||0;bold.style.letterSpacing=spacing+'px';const difference=regular-bold.getBoundingClientRect().width;bold.style.letterSpacing=(spacing+difference/Math.max(1,bold.textContent.length))+'px'}}
function positionConnectors(){const comp=$('.composition',scenes[1]),origin=comp.getBoundingClientRect();for(const kind of ['past','present']){const card=$('.history-card--'+kind),year=$('.year--'+kind),line=$('.history-connector--'+kind),c=card.getBoundingClientRect();if(mobile.matches)year.style.top=(c.bottom-origin.top+24)+'px';else year.style.top='';year.style.left=(c.left-origin.left+c.width/2-year.offsetWidth/2)+'px';const y=year.getBoundingClientRect();line.style.left=(c.left-origin.left+c.width/2)+'px';line.style.top=(c.bottom-origin.top)+'px';line.style.height=Math.max(0,y.top-c.bottom)+'px'}}
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
const playback=new ScenePlayback(scenes,CONFIG,{reduced,reference,onFrame:()=>render()});
const RIGHT_STATES=[Array.from({length:13},(_,i)=>i),[3,0,6,1,8,2,10,4,12,5,11,7,9],Array.from({length:13},(_,i)=>12-i),Array.from({length:13},(_,i)=>(i+4)%13)];
function render(){renderFrame=0;playback.observe(lastDirection,dragging);scenes.forEach((scene,i)=>{const r=scene.getBoundingClientRect(),visible=r.bottom>0&&r.top<innerHeight,t=playback.value(i),complete=reference||reduced.matches;scene.classList.toggle('is-visible',visible);if(!visible&&!reference)return;const u=$('.composition',scene).clientWidth/1680;
 if(i===1){const maxShift=mobile.matches?Math.min(760,$('.folder-tape').scrollWidth-$('.folder-viewport').clientWidth):CONFIG.folderShift*u;$('.folder-tape').style.transform=`translateX(${complete?0:-maxShift*t}px)`}
 if(i===2){const panel=$('.scan-panel--left'),wave=complete||t>=1?0:Math.pow(Math.sin(Math.PI*t),2),distance=mobile.matches?panel.clientWidth*CONFIG.mobileScanRatio:CONFIG.scanShift*u;$$('.scanner').forEach(n=>n.style.transform=`translateX(${+n.dataset.direction*distance*wave}px)`);$('.white-block--top').style.transform=`translateY(${panel.clientHeight*CONFIG.whiteDownRatio*wave}px)`;$('.white-block--bottom').style.transform=`translateY(${-panel.clientHeight*CONFIG.whiteUpRatio*wave}px)`;const step=complete||t>=1?0:Math.floor(t*CONFIG.holdMs/CONFIG.rightStepMs)%RIGHT_STATES.length;$$('.scan-line').forEach((n,j)=>n.style.setProperty('--y',42+47*RIGHT_STATES[step][j]));}
 if(i===3){const p=complete?1:CONFIG.cardStart+t*(CONFIG.cardStagger*6+CONFIG.cardReveal);$$('.card-motion').forEach((n,j)=>{const local=complete?1:ease((p-CONFIG.cardStart-j*CONFIG.cardStagger)/CONFIG.cardReveal);n.style.setProperty('--enter-y',(1-local)*(mobile.matches?240:CONFIG.cardRise*u)+'px');n.style.opacity=local})}
 if(i===4)$('.revealing-phrase').style.opacity=complete?1:t<CONFIG.phraseFadeInEnd?t/CONFIG.phraseFadeInEnd:t<=CONFIG.phraseFadeOutStart?1:clamp((1-t)/(1-CONFIG.phraseFadeOutStart));
 if(i===5){const local=reference?0:t;counter.style.transform=`translateX(${-local*7*100}%)`;runner.style.width=(100*(CONFIG.readMinPercent+(CONFIG.readMaxPercent-CONFIG.readMinPercent)*local))+'%';runner.style.transform='none';readingWords.forEach((n,j)=>n.classList.toggle('is-read',j<Math.round(local*readingWords.length*.5)))}
 if(i===9){const arrows=complete?1:clamp((t-CONFIG.finalWordsMs/CONFIG.holdMs)/CONFIG.finalArrowsSpan),stars=complete?1:clamp((t-CONFIG.finalStarsAt)/CONFIG.finalStarsSpan);$('.collage-arrows').style.opacity=arrows;const group=$('.collage-stars');group.style.opacity=stars;group.inert=stars<.95;}
 })}
addEventListener('scroll',()=>{const delta=scrollY-lastScroll;if(!autoScrolling&&!playback.active&&delta)lastDirection=Math.sign(delta);lastScroll=scrollY;if(!renderFrame)renderFrame=requestAnimationFrame(render);if(!autoScrolling&&!dragging&&!playback.active){clearTimeout(snapTimer);snapTimer=setTimeout(snap,CONFIG.snapDelay)}},{passive:true});
for(const type of ['wheel','touchstart','pointerdown','keydown'])addEventListener(type,cancelSnap,{passive:true});
let resizeFrame=0;function resized(){cancelAnimationFrame(resizeFrame);resizeFrame=requestAnimationFrame(()=>{fitCopy();fitBoldWords();positionConnectors();const m=domeMetrics();symbols.forEach(s=>{cancelAnimationFrame(s.frame);s.frame=0;safeSymbol(s,m)});render()})}
new ResizeObserver(resized).observe(document.body);document.fonts.ready.then(resized);addEventListener('resize',resized);reduced.addEventListener('change',render);mobile.addEventListener('change',resized);
fitCopy();fitBoldWords();positionConnectors();render();
window.SKIM={CONFIG,playback,RIGHT_STATES,fitBoldWords,positionConnectors,render,scatter,fitCopy,symbols,domeMetrics,circleInside,symbolRadius,readingWords,fullText};
