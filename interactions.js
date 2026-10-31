'use strict';
// Explicit star → English expression → Russian translation mapping, in DOM order.
const FINAL_TRANSLATIONS=[
  {key:'final-0',english:'visual',russian:'Визуальный'},
  {key:'final-1',english:'culture',russian:'Культура'},
  {key:'final-2',english:'contemporary',russian:'Современный'},
  {key:'final-3',english:'built',russian:'Созданный'},
  {key:'final-4',english:'unexpected',russian:'Неожиданный'},
  {key:'final-5',english:'moments',russian:'Моменты'},
  {key:'final-6',english:'small',russian:'Небольшой'},
  {key:'final-7',english:'new',russian:'Новый'},
  {key:'final-8',english:'fragments',russian:'Фрагменты'},
  {key:'final-9',english:'collection',russian:'Собрание'},
  {key:'final-10',english:'SKIM',russian:'Бегло просматривать',caption:'eng idiom'},
  {key:'final-11',english:'observations',russian:'Наблюдения'}
];
const DISTRACTIONS=[
  'Привет! У меня к тебе важное дело',
  'Давай в другой раз',
  'Да ладно, потом прочитаешь',
  'Может, отложим на потом?',
  'Низкий заряд батареи компьютера'
];
(()=>{
  const tips=new Map(FINAL_TRANSLATIONS.map(t=>[t.key,t]));
  tips.set('cover',{russian:'Бегло просматривать',caption:'eng idiom'});
  tips.set('scan',{russian:'Привыкнув скользить между отдельными блоками информации, человеку бывает трудно сразу переключиться на последовательное чтение линейного текста'});
  const layer=document.createElement('div');layer.id='floating-tooltip';layer.className='floating-tooltip';layer.role='tooltip';layer.setAttribute('aria-hidden','true');document.body.append(layer);
  let active=null,pinned=false,closeTimer=0;
  function place(){
    if(!active)return;
    const r=active.getBoundingClientRect();
    if(r.bottom<0||r.top>innerHeight){hide();return}
    const viewportWidth=document.documentElement.clientWidth;layer.style.maxWidth=Math.min(420,viewportWidth-24)+'px';const box=layer.getBoundingClientRect(),left=Math.max(12,Math.min(viewportWidth-box.width-12,r.left+r.width/2-box.width/2));
    let top=r.bottom+14;if(top+box.height>innerHeight-12)top=r.top-box.height-14;
    layer.style.left=left+'px';layer.style.top=Math.max(12,top)+'px';
  }
  function show(button,pin=false){
    clearTimeout(closeTimer);
    if(active&&active!==button){active.setAttribute('aria-expanded','false');active.removeAttribute('aria-describedby')}
    active=button;pinned=pin;
    const data=tips.get(button.dataset.tooltipKey);if(!data)return;
    layer.replaceChildren();
    const main=document.createElement(data.caption||data.english?'strong':'span');main.textContent=data.russian;layer.append(main);
    if(data.caption||data.english){const caption=document.createElement('small');caption.textContent=data.caption||data.english;layer.append(caption)}
    button.setAttribute('aria-expanded','true');button.setAttribute('aria-describedby',layer.id);
    layer.classList.add('open');layer.setAttribute('aria-hidden','false');place();
  }
  function hide(){
    clearTimeout(closeTimer);
    if(active){active.setAttribute('aria-expanded','false');active.removeAttribute('aria-describedby')}
    active=null;pinned=false;layer.classList.remove('open');layer.setAttribute('aria-hidden','true');
  }
  function scheduleHide(){if(!pinned)closeTimer=setTimeout(()=>{if(document.activeElement!==active&&!layer.matches(':hover'))hide()},180)}
  for(const button of document.querySelectorAll('[data-tooltip-key]')){
    const data=tips.get(button.dataset.tooltipKey);
    if(!button.hasAttribute('aria-label'))button.setAttribute('aria-label',data.english?`Перевод: ${data.english}`:data.russian);
    button.addEventListener('pointerenter',()=>show(button,pinned&&active===button));
    button.addEventListener('pointerleave',scheduleHide);
    button.addEventListener('focus',()=>show(button,pinned&&active===button));
    button.addEventListener('blur',scheduleHide);
    button.addEventListener('click',()=>{if(active===button&&pinned)hide();else show(button,true)});
  }
  layer.addEventListener('pointerenter',()=>clearTimeout(closeTimer));layer.addEventListener('pointerleave',scheduleHide);
  addEventListener('scroll',place,{passive:true});addEventListener('resize',place);
  document.addEventListener('keydown',e=>{if(e.key==='Escape')hide()});
  document.addEventListener('pointerdown',e=>{if(active&&!active.contains(e.target)&&!layer.contains(e.target))hide()});

  const toast=document.createElement('div');toast.className='distraction-toast';toast.role='status';toast.setAttribute('aria-live','polite');toast.hidden=true;
  const message=document.createElement('span'),close=document.createElement('button');close.className='toast-close';close.type='button';close.textContent='×';close.setAttribute('aria-label','Закрыть уведомление');toast.append(message,close);document.body.append(toast);
  let messageIndex=0,toastTimer=0,lock=null;
  function closeToast(){clearTimeout(toastTimer);toast.hidden=true;if(lock)lock.setAttribute('aria-expanded','false');lock=null}
  function placeToast(){if(!lock)return;const r=lock.getBoundingClientRect();if(r.bottom<0||r.top>innerHeight){closeToast();return}const b=toast.getBoundingClientRect();toast.style.left=Math.max(16,Math.min(innerWidth-b.width-16,r.left+r.width/2-b.width/2))+'px';const below=r.bottom+16;toast.style.top=Math.max(12,below+b.height<innerHeight-12?below:r.top-b.height-16)+'px'}
  for(const button of document.querySelectorAll('.lock-badge'))button.addEventListener('click',()=>{
    if(lock)lock.setAttribute('aria-expanded','false');lock=button;lock.setAttribute('aria-expanded','true');
    message.textContent=DISTRACTIONS[messageIndex++%DISTRACTIONS.length];toast.hidden=false;placeToast();clearTimeout(toastTimer);toastTimer=setTimeout(closeToast,window.SKIM.CONFIG.toastMs);
  });
  close.addEventListener('click',closeToast);addEventListener('scroll',placeToast,{passive:true});addEventListener('resize',placeToast);
  document.addEventListener('keydown',e=>{if(e.key==='Escape')closeToast()});document.addEventListener('pointerdown',e=>{if(lock&&!toast.contains(e.target)&&!e.target.closest('.lock-badge'))closeToast()});
  window.SKIM_TIPS={translations:FINAL_TRANSLATIONS,distractions:DISTRACTIONS,show,hide,closeToast};
})();
