'use strict';
// One timeline owns each scene. Input is discarded during a hold, never queued.
class ScenePlayback {
  constructor(scenes, config, {reduced, reference, onFrame}) {
    this.scenes=scenes;this.config=config;this.reduced=reduced;this.reference=reference;this.onFrame=onFrame;
    this.states=scenes.map(()=>({played:false,value:0,starts:0}));this.active=null;this.frame=0;this.touchY=0;
    this.onWheel=e=>{if(!this.active)return;if(e.deltaY<0){this.release();return}if(e.cancelable)e.preventDefault()};
    this.onKey=e=>{
      if(!this.active||e.ctrlKey||e.metaKey||e.altKey)return;
      if(e.key==='Escape'){this.release();return}
      if(e.target.closest('input,textarea,select,[contenteditable=true]'))return;
      if(['ArrowUp','PageUp','Home'].includes(e.key)){this.release();return}
      if(e.key===' '&&e.target.closest('button,a'))return;
      if(['ArrowDown','PageDown','End',' '].includes(e.key))e.preventDefault();
    };
    addEventListener('wheel',this.onWheel,{passive:false});addEventListener('keydown',this.onKey);
    addEventListener('touchstart',e=>{this.touchY=e.touches[0]?.clientY||0},{passive:true});
    addEventListener('touchmove',e=>{
      if(!this.active||e.touches.length!==1||e.target.closest('input,button,a,[contenteditable=true]')||!getSelection().isCollapsed)return;
      const dy=this.touchY-e.touches[0].clientY;
      if(dy < -8){this.release();return}
      if(e.cancelable)e.preventDefault();
    },{passive:false});
    reduced.addEventListener('change',()=>{if(reduced.matches)this.release();this.onFrame()});
  }
  observe(direction=1, dragging=false) {
    if(this.active||this.reference||this.reduced.matches||direction<0||dragging)return;
    let candidate=-1,best=0;
    for(let i=1;i<this.scenes.length;i++) {
      if(this.states[i].played)continue;
      const scene=this.scenes[i],r=scene.getBoundingClientRect(),c=scene.querySelector('.composition').getBoundingClientRect();
      const visible=Math.max(0,Math.min(c.bottom,innerHeight)-Math.max(c.top,0))/Math.min(c.height,innerHeight);
      if(i===9) {
        if(r.top>this.config.finalSettleTolerance||r.top < -innerHeight*.25||c.top < -innerHeight*.12)continue;
      } else if(visible<this.config.entryVisibility)continue;
      if(visible>best){best=visible;candidate=i}
    }
    if(candidate>=0)this.start(candidate);
  }
  start(index) {
    if(this.active||this.states[index].played||this.reference||this.reduced.matches)return false;
    const state=this.states[index];state.played=true;state.starts++;state.value=0;
    this.active={index,started:performance.now(),from:scrollY,anchor:this.anchor(index)};
    this.frame=requestAnimationFrame(now=>this.tick(now));return true;
  }
  anchor(index) {
    return Math.max(0,Math.min(this.scenes[index].offsetTop,document.documentElement.scrollHeight-innerHeight));
  }
  tick(now) {
    if(!this.active)return;
    const a=this.active,elapsed=Math.max(0,now-a.started);
    a.anchor=this.anchor(a.index);
    const alignment=Math.min(1,elapsed/this.config.entryAlignMs),eased=1-Math.pow(1-alignment,3);
    const y=a.from+(a.anchor-a.from)*eased;
    if(Math.abs(scrollY-y)>.5)scrollTo({top:y,behavior:'instant'});
    this.states[a.index].value=Math.min(1,elapsed/this.config.holdMs);
    if(elapsed>=this.config.holdMs){this.states[a.index].value=1;this.active=null;this.frame=0;this.onFrame();return}
    try{this.onFrame()}finally{if(this.active)this.frame=requestAnimationFrame(t=>this.tick(t))}
  }
  release() {
    if(!this.active)return;
    this.states[this.active.index].value=1;this.active=null;
    cancelAnimationFrame(this.frame);this.frame=0;this.onFrame();
  }
  value(index){return this.reference||this.reduced.matches?1:this.states[index].value}
  finishAll(){this.release();for(const state of this.states){state.played=true;state.value=1}this.onFrame()}
}
