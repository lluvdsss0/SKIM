from browser import Browser
from pathlib import Path
import json,time
Path('review/scroll-after').mkdir(exist_ok=True)
b=Browser();b.call('Network.enable');b.call('Network.setCacheDisabled',{'cacheDisabled':True});b.call('Runtime.enable');b.call('Log.enable');b.call('Emulation.setTouchEmulationEnabled',{'enabled':False});b.call('Emulation.setEmulatedMedia',{'features':[]})
def js(s):return b.js(s)
def resize(w,h):
 b.call('Emulation.setDeviceMetricsOverride',{'width':w,'height':h,'deviceScaleFactor':1,'mobile':False});b.call('Page.navigate',{'url':'http://127.0.0.1:8000/'});time.sleep(.25);js('document.fonts.ready.then(()=>true)');time.sleep(.05)
def phase(index,t):
 js(f'var state=SKIM.playback.states[{index}];scrollTo(0,state.start+(state.end-state.start)*{t});SKIM.render()');time.sleep(.05)
def signature(i):
 selectors={1:'.folder-tape',2:'.scanner,.white-block,.scan-line',3:'.card-motion',4:'.revealing-phrase',5:'.counter-tape,.read-runner,.reading-word'}
 return js(f'''JSON.stringify([...document.querySelectorAll('{selectors[i]}')].map(n=>[n.style.transform,n.style.opacity,n.style.getPropertyValue('--enter-y'),n.style.getPropertyValue('--y'),n.style.width,n.className]))''')
out={};resize(1680,1079)
for i in range(1,6):
 t=.18 if i==4 else .32;phase(i,t);a=signature(i);y=js('scrollY');time.sleep(.45);idle=signature(i)==a and js('scrollY')==y
 js('scrollBy(0,18)');time.sleep(.08);changed=signature(i)!=a;phase(i,t);reverse=signature(i)==a
 phase(i,1);phase(i,t);replay=signature(i)==a
 out['scene_'+str(i+1)]={'idle_stops':idle,'small_scroll_changes':changed,'reverse_restores':reverse,'after_full_scroll_still_linked':replay}
out['scroll_engine_no_lock']=js('({noActiveHold:SKIM.playback.active===undefined,noOnceFlag:SKIM.playback.states.every(s=>s.played===undefined)})')
for width,height in [(390,844),(768,1024),(1680,1079),(1920,800)]:
 resize(width,height);records=[]
 for t in [0,.5,1]:
  phase(1,t)
  records.append(js('''(()=>{const v=document.querySelector('.folder-viewport'),row=document.querySelector('.folder-tape'),vr=v.getBoundingClientRect(),li=[...row.children],first=li[0].getBoundingClientRect(),last=li.at(-1).getBoundingClientRect(),style=getComputedStyle(v);const full=r=>r.left>=vr.left-.2&&r.right<=vr.right+.2;const safe=li.filter(n=>full(n.getBoundingClientRect())).every(n=>{const icon=n.querySelector('.folder-icon'),r=icon.getBoundingClientRect(),p=n.querySelector('p').getBoundingClientRect(),tab=parseFloat(getComputedStyle(icon,'::before').top);return r.top+tab>=vr.top-.2&&p.bottom<=vr.bottom+.2});return{progress:SKIM.playback.value(1),maxShift:SKIM.folderMetrics.maxShift,firstFull:full(first),lastFull:full(last),allInsideItemsVerticallySafe:safe,overflowX:style.overflowX,overflowY:style.overflowY,clipPath:style.clipPath,panelHeight:document.querySelector('.folder-window').getBoundingClientRect().height}})()'''))
  b.screenshot(f'review/scroll-after/folders-{width}-{int(t*100)}.png')
 out['folders_'+str(width)]={'records':records,'startFull':records[0]['firstFull'],'endFull':records[2]['lastFull'],'verticalSafe':all(r['allInsideItemsVerticallySafe'] for r in records)}
 out['overflow_'+str(width)]=js('document.documentElement.scrollWidth>innerWidth')

resize(1680,1079)
manual={}
for i in [6,7,8,9]:
 js(f'scrollTo(0,document.querySelectorAll(".scene")[{i}].offsetTop);SKIM.render()');time.sleep(.05)
 if i==6:js('document.querySelector(".lock-badge").click()')
 if i==7:js('document.querySelector(".break-button").click()')
 if i==8:js('document.querySelector("#text-size").value=30;document.querySelector("#text-size").dispatchEvent(new Event("input"))')
 if i==9:phase(9,1);js('document.querySelector("[data-tooltip-key=final-10]").click()')
 y=js('scrollY');b.call('Input.dispatchMouseEvent',{'type':'mouseWheel','x':800,'y':500,'deltaX':0,'deltaY':-170 if i==9 else 170});time.sleep(.17);new=js('scrollY');time.sleep(.28)
 manual[str(i+1)]={'immediateScroll':new<y-50 if i==9 else new>y+50,'noAnchorReturn':abs(js('scrollY')-new)<1}
out['manual_sections']=manual
out['interactive_results']=js('({toastExists:document.querySelector(".distraction-toast")!==null,rangeValue:document.querySelector("#text-size").value,scatterMoved:SKIM.symbols.some(s=>Math.abs(s.x-s.cx)>1),translations:SKIM_TIPS.translations.length})')
phase(9,1);js('document.querySelector("[data-tooltip-key=final-10]").focus()');time.sleep(.2);out['tip_still_works']=js('document.querySelector(".floating-tooltip").textContent.includes("Бегло просматривать")')
b.call('Emulation.setEmulatedMedia',{'features':[{'name':'prefers-reduced-motion','value':'reduce'}]});phase(1,.4);out['reduced_motion']=js('getComputedStyle(document.querySelector(".year span")).animationName')
out['errors']=[e for e in b.events if e.get('method')=='Runtime.exceptionThrown' or e.get('method')=='Log.entryAdded' and e['params']['entry']['level']=='error']
Path('review/scroll-qa.json').write_text(json.dumps(out,indent=2),encoding='utf-8');print(json.dumps(out))
