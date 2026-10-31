const CONFIG = Object.freeze({snapDistance:.12,snapDelay:180,snapDuration:280,folderShift:865,scanShift:230,pulseDuration:2300,scatterDuration:850,minFont:10,maxFont:38,cardStart:.10,cardStagger:.045,cardReveal:.18,readStart:.14,readSpan:.41,readMinPercent:.05,readMaxPercent:.40,phraseIn:.12,phraseFade:.22,phraseOut:.88,arrowStart:.20,starStart:.45,finalFade:.22});
const $=(s,r=document)=>r.querySelector(s), $$=(s,r=document)=>[...r.querySelectorAll(s)], clamp=(x,a=0,b=1)=>Math.max(a,Math.min(b,x)), smooth=x=>1-Math.pow(1-clamp(x),3), NS='http://www.w3.org/2000/svg';
document.documentElement.style.setProperty('--pulse-duration',CONFIG.pulseDuration+'ms');
const screens=$$('.screen'), reduced=matchMedia('(prefers-reduced-motion: reduce)'), reference=new URLSearchParams(location.search).has('reference');
const part=(s,n)=>$(`[data-part="${n}"]`,s);
const svgEl=(name,attrs={})=>{const n=document.createElementNS(NS,name);Object.entries(attrs).forEach(([k,v])=>n.setAttribute(k,v));return n};
let activeDrag=false, frame=0, snapFrame=0, snapTimer=0, lastInput=0, lastY=scrollY, velocity=0, lastTime=performance.now(),autoScrolling=false;
function move(n,x=0,y=0){if(n)n.setAttribute('transform',`translate(${x} ${y})`)}
// Source text transcribed from Frame 62.svg; original repetitions and word order retained.
const paragraph='Мы читаем переписки, новости, посты, отзывы и подписи к видео. Текст сопровождает нас с утра до вечера. Но когда нужно прочитать большую статью или главу книги, бывает трудно удержаться на странице: хочется проверить сообщения, пролистать дальше или сразу найти краткий пересказ. В XXI веке длинный текст постоянно конкурирует с другими занятиями. На одном экране находятся книга, рабочий чат и лента новостей. Любой непонятный термин можно мгновенно поискать, но вместе с ответом легко открыть ещё несколько вкладок и потерять исходную мысль. После возвращения приходится вспоминать, на чём остановился и как связаны прочитанные части. Сложность возникает и из-за самого устройства текста. Большой объём легче воспринимать, когда понятны его цель и логика. Если заголовки мало о чём говорят, аргументы теряются среди примеров, а выводы приходится искать самостоятельно, чтение требует дополнительных усилий. Иногда желание закрыть статью связано с тем, что читатель не понимает, зачем продолжать. Краткие пересказы и нейросети предлагают удобный выход. Они помогают познакомиться с темой и решить, стоит ли читать оригинал. Однако пересказ неизбежно отбирает информацию за нас. В нём могут исчезнуть оговорки, противоречия и ход рассуждений — всё то, благодаря чему становится понятно, как автор пришёл к своему выводу.';
const ending=' Для вдумчивого чтения нужны условия: время без постоянных переключений, ясный вопрос к материалу и возможность делать паузы. Помогают короткие заметки своими словами и возвращение к сложным фрагментам. При этом далеко не каждый текст требует одинакового внимания: иногда достаточно просмотра, иногда необходимо подробное изучение.';
const fullText=paragraph+ending+' Длинный текст в эпоху короткого внимания. '+paragraph+ending.slice(0,-1)+'Длинный текст в эпоху короткого внимания '+paragraph;
const range=$('.size-range'),copy=$('.dynamic-copy'),thumb=part(screens[8],'size-thumb');
function fitCopy(){
 const size=+range.value;copy.style.fontSize=`${size*$('.stage',screens[8]).clientWidth/1680}px`;
 const words=fullText.split(/\s+/);let lo=0,hi=words.length;
 while(lo<hi){const mid=Math.ceil((lo+hi)/2);copy.textContent=words.slice(0,mid).join(' ');if(copy.scrollHeight<=copy.clientHeight+.5)lo=mid;else hi=mid-1}
 copy.textContent=words.slice(0,lo).join(' ');range.setAttribute('aria-valuetext',`${size} — размер текста`);
 move(thumb,(size-10)/28*(954-52)-88,0);
}
function updateSize(){part(screens[8],'original-copy').style.display='none';copy.hidden=false;fitCopy()}
range.addEventListener('input',updateSize);range.addEventListener('pointerdown',()=>{activeDrag=true;cancelSnap()});addEventListener('pointerup',()=>{activeDrag=false});range.addEventListener('keydown',cancelSnap);
// One active animation per symbol, with a bounding circle tested against the actual dome path.
const dome=part(screens[7],'dome-shape'),symbols=$$('[data-part=symbol]',screens[7]).map(n=>{const b=n.getBBox();return{n,cx:b.x+b.width/2,cy:b.y+b.height/2,r:Math.hypot(b.width,b.height)/2+4,x:0,y:0,a:0}});
function insideCircle(x,y,r){for(let i=0;i<32;i++){const a=i*Math.PI/16;if(!dome.isPointInFill(new DOMPoint(x+Math.cos(a)*r,y+Math.sin(a)*r)))return false}return true}
function scatter(){for(const s of symbols){let x,y;for(let k=0;k<1000;k++){x=270+Math.random()*1140;y=520+Math.random()*530;if(insideCircle(x,y,s.r))break}if(!insideCircle(x,y,s.r))continue;
 const from={x:s.x,y:s.y,a:s.a},to={x:x-s.cx,y:y-s.cy,a:Math.random()*300-150};cancelAnimationFrame(s.frame);
 const start=performance.now();const tick=now=>{const p=reduced.matches?1:smooth((now-start)/CONFIG.scatterDuration);s.x=from.x+(to.x-from.x)*p;s.y=from.y+(to.y-from.y)*p;s.a=from.a+(to.a-from.a)*p;s.n.setAttribute('transform',`translate(${s.x} ${s.y}) rotate(${s.a} ${s.cx} ${s.cy})`);if(p<1)s.frame=requestAnimationFrame(tick)};s.frame=requestAnimationFrame(tick);
 }}
$('.break').addEventListener('click',scatter);
const info=$('.info'),infoButton=$('button',info);infoButton.addEventListener('click',()=>{const open=info.classList.toggle('open');infoButton.setAttribute('aria-expanded',open)});info.addEventListener('focusin',()=>infoButton.setAttribute('aria-expanded','true'));info.addEventListener('focusout',e=>{if(!info.contains(e.relatedTarget)&&!info.classList.contains('open'))infoButton.setAttribute('aria-expanded','false')});info.addEventListener('pointerenter',()=>infoButton.setAttribute('aria-expanded','true'));info.addEventListener('pointerleave',()=>{if(!info.matches(':focus-within')&&!info.classList.contains('open'))infoButton.setAttribute('aria-expanded','false')});document.addEventListener('keydown',e=>{if(e.key==='Escape'){info.classList.remove('open');infoButton.setAttribute('aria-expanded','false');infoButton.blur()}});document.addEventListener('pointerdown',e=>{if(!info.contains(e.target)){info.classList.remove('open');infoButton.setAttribute('aria-expanded','false')}});
$('.learn').addEventListener('click',()=>{cancelSnap();screens[1].scrollIntoView({behavior:reduced.matches?'instant':'smooth'})});
// The counter reuses its original frame; all values move horizontally under its clip.
const read=screens[5],readSvg=$('svg',read),defs=$('defs',readSvg),windowClip=svgEl('clipPath',{id:'reading-counter-window'});windowClip.append(svgEl('rect',{x:120,y:951,width:61.333,height:34}));defs.append(windowClip);
const counter=svgEl('g',{'clip-path':'url(#reading-counter-window)'}),numbers=svgEl('g',{'data-part':'counter-values'});for(let i=0;i<8;i++){const t=svgEl('text',{x:124+i*62,y:978,fill:'#090909','font-family':'Arial, sans-serif','font-size':28});t.textContent=`${5+i*5}%`;numbers.append(t)}counter.append(numbers);readSvg.append(counter);
// Derive word masks from the source outline's actual subpath bounds. No replacement lettering.
const original=part(read,'read-copy'),highlight=original.cloneNode(true);highlight.removeAttribute('data-part');highlight.setAttribute('fill','#090909');highlight.setAttribute('clip-path','url(#reading-word-window)');original.after(highlight);
const wordClip=svgEl('clipPath',{id:'reading-word-window'});defs.append(wordClip);
function sourceWords(){const subpaths=original.getAttribute('d').match(/[Mm][^Mm]*/g)||[],boxes=[];const probe=svgEl('path');readSvg.append(probe);
 for(const d of subpaths){probe.setAttribute('d',d);const b=probe.getBBox();if(b.width>1&&b.height>1)boxes.push({x:b.x,y:b.y,w:b.width,h:b.height})}probe.remove();
 const lines=[];for(const b of boxes.sort((a,b)=>a.y-b.y)){let line=lines.find(l=>Math.abs(l.bottom-(b.y+b.h))<16);if(!line){line={bottom:b.y+b.h,boxes:[]};lines.push(line)}line.boxes.push(b)}
 const words=[];for(const line of lines.sort((a,b)=>a.bottom-b.bottom)){let w=null;for(const b of line.boxes.sort((a,b)=>a.x-b.x)){if(!w||b.x>w.x+w.w+7){w={...b};words.push(w)}else{const right=Math.max(w.x+w.w,b.x+b.w),bottom=Math.max(w.y+w.h,b.y+b.h);w.y=Math.min(w.y,b.y);w.w=right-w.x;w.h=bottom-w.y}}}
 const firstParagraph=words.filter(b=>b.y<600);return firstParagraph.slice(0,Math.ceil(firstParagraph.length*.5)).map(b=>{const r=svgEl('rect',{x:b.x-1,y:b.y-1,width:b.w+2,height:b.h+2});wordClip.append(r);return r});
}
const wordMasks=sourceWords();
function progress(screen){const r=screen.getBoundingClientRect();return clamp((innerHeight-r.top)/(r.height+innerHeight))}
function render(){frame=0;screens.forEach((s,i)=>{const r=s.getBoundingClientRect(),p=progress(s),inView=r.bottom>0&&r.top<innerHeight;s.classList.toggle('active',inView);if(!inView&&!reference)return;
 const complete=reference||reduced.matches;
 if(i===1)move(part(s,'folder-tape'),complete?0:-CONFIG.folderShift*clamp((p-.18)/.62));
 if(i===2)$$('[data-part=scanner]',s).forEach(n=>move(n,complete?0:+n.dataset.direction*CONFIG.scanShift*Math.pow(clamp((p-.15)/.7),2.5)));
 if(i===3)$$('[data-part=card]',s).forEach((n,j)=>{const t=complete?1:smooth((p-CONFIG.cardStart-j*CONFIG.cardStagger)/CONFIG.cardReveal);move(n,0,(1-t)*700);n.style.opacity=t});
 if(i===4)part(s,'phrase').style.opacity=complete?1:Math.min(clamp((p-CONFIG.phraseIn)/CONFIG.phraseFade),clamp((CONFIG.phraseOut-p)/CONFIG.phraseFade));
 if(i===5&&reference){counter.style.display='none';highlight.style.display='none';$('g[mask]',readSvg).style.display='inline';part(s,'read-bar').setAttribute('width',184);part(s,'read-bar').setAttribute('x',120)}
 if(i===5&&!reference){const t=complete?1:clamp((p-CONFIG.readStart)/CONFIG.readSpan),step=t*7;move(numbers,-step*62);part(s,'read-bar').setAttribute('x',120+(1440-184)*(CONFIG.readMaxPercent-CONFIG.readMinPercent)*t);wordMasks.forEach((n,j)=>n.setAttribute('display',j<Math.round(t*wordMasks.length)?'inline':'none'))}
 if(i===9){const local=clamp((innerHeight-r.top)/(r.height));const a=complete?1:clamp((local-CONFIG.arrowStart)/CONFIG.finalFade),b=complete?1:clamp((local-CONFIG.starStart)/CONFIG.finalFade);$$('[data-part=arrows]',s).forEach(n=>n.style.opacity=a);$$('[data-part=star]',s).forEach(n=>n.style.opacity=b)}
 });}
function cancelSnap(){clearTimeout(snapTimer);cancelAnimationFrame(snapFrame);snapFrame=0;autoScrolling=false;lastInput=performance.now()}
function snap(){if(activeDrag||reduced.matches||reference||Math.abs(velocity)>.12)return;const candidates=screens.map(s=>s.offsetTop),current=scrollY,target=candidates.reduce((a,b)=>Math.abs(b-current)<Math.abs(a-current)?b:a);if(Math.abs(target-current)>innerHeight*CONFIG.snapDistance||Math.abs(target-current)<2)return;
 // Never pull back against the most recent direction.
 if((target-current)*Math.sign(lastYDirection)<0)return;const start=performance.now();autoScrolling=true;
 const tick=now=>{const p=clamp((now-start)/CONFIG.snapDuration);scrollTo(0,current+(target-current)*smooth(p));if(p<1)snapFrame=requestAnimationFrame(tick);else{autoScrolling=false;snapFrame=0}};snapFrame=requestAnimationFrame(tick);
}
let lastYDirection=0;
addEventListener('scroll',()=>{const now=performance.now(),dy=scrollY-lastY;velocity=dy/Math.max(1,now-lastTime);if(!autoScrolling&&dy)lastYDirection=dy;lastY=scrollY;lastTime=now;if(!frame)frame=requestAnimationFrame(render);if(!autoScrolling){clearTimeout(snapTimer);snapTimer=setTimeout(()=>{velocity=0;snap()},CONFIG.snapDelay)}},{passive:true});
for(const event of ['wheel','touchstart','pointerdown','keydown'])addEventListener(event,cancelSnap,{passive:true});
new ResizeObserver(()=>{if(!copy.hidden)fitCopy();render()}).observe($('.stage',screens[8]));
document.fonts.ready.then(()=>{if(!copy.hidden)fitCopy()});reduced.addEventListener('change',render);
// Preserve original outlined copy until the user changes the slider.
copy.hidden=true;range.value=13;move(thumb,0,0);render();
window.SKIM={CONFIG,render,scatter,fitCopy,sourceWords,wordMasks,symbols,fullText,progress};
