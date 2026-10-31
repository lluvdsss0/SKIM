'use strict';
// The sole scene progress source is scroll position. No clocks or input handlers.
class ScenePlayback {
  constructor(scenes,config,{reduced,reference}){
    this.scenes=scenes;this.config=config;this.reduced=reduced;this.reference=reference;
    this.states=scenes.map(()=>({value:0,start:0,end:1}));
    this.scrollScenes=[1,2,3,4,5,9];
    for(const index of this.scrollScenes)scenes[index].classList.add('scene--scrub');
  }
  measure(){
    for(const index of this.scrollScenes){
      const scene=this.scenes[index],composition=scene.querySelector('.composition'),style=getComputedStyle(scene);
      const paddingTop=parseFloat(style.paddingTop)||0,paddingBottom=parseFloat(style.paddingBottom)||0;
      const height=composition.getBoundingClientRect().height;
      const desktopExtended=innerWidth>1000&&scene.classList.contains('scene--extended');
      const top=desktopExtended?Math.max(0,(innerHeight-innerWidth*1079/1680)/2):Math.max(paddingTop,(innerHeight-height)/2);
      const travel=innerHeight*(index===9?this.config.finalScrollTravel:this.config.scrollTravel);
      scene.style.height=Math.ceil(Math.max(innerHeight,height+paddingTop+paddingBottom)+travel)+'px';
      composition.style.setProperty('--sticky-top',Math.max(0,top)+'px');
    }
    // All heights must be final before offsets of later scenes are read.
    for(const index of this.scrollScenes){
      const scene=this.scenes[index],composition=scene.querySelector('.composition'),style=getComputedStyle(scene);
      const paddingBottom=parseFloat(style.paddingBottom)||0,top=parseFloat(getComputedStyle(composition).top)||0;
      const start=scene.offsetTop-(index===1||index===9?0:innerHeight*this.config.scrollLead);
      const end=Math.min(scene.offsetTop+scene.offsetHeight-paddingBottom-composition.offsetHeight-top,document.documentElement.scrollHeight-innerHeight);
      this.states[index].start=start;this.states[index].end=Math.max(start+1,end);
    }
    this.observe();
  }
  observe(){
    for(const index of this.scrollScenes){const state=this.states[index];state.value=Math.max(0,Math.min(1,(scrollY-state.start)/(state.end-state.start)))}
  }
  value(index){return this.reference||this.reduced.matches?1:this.states[index].value}
}
