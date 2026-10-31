from browser import Browser
import time,json
b=Browser();b.call('Runtime.enable');b.call('Log.enable');b.call('Page.navigate',{'url':'http://127.0.0.1:8000/'});time.sleep(.5)
def js(x):return b.js(x)
def wait():time.sleep(.1)
results={}
results['ready']=js('!!window.SKIM')
results['tooltip']=js("document.querySelector('.info button').click();document.querySelector('.info button').getAttribute('aria-expanded')")
js("document.querySelector('.learn').click()");time.sleep(1);results['learn']=js('Math.abs(scrollY-document.querySelectorAll(".screen")[1].offsetTop)<3')
js('scrollTo(0,document.querySelectorAll(".screen")[7].offsetTop);SKIM.scatter()')
inside=[]
for _ in range(8):
 time.sleep(.12);inside.append(js('SKIM.symbols.every(s=>{const d=document.querySelector("[data-part=dome-shape]");for(let i=0;i<32;i++){const a=i*Math.PI/16;if(!d.isPointInFill(new DOMPoint(s.cx+s.x+Math.cos(a)*s.r,s.cy+s.y+Math.sin(a)*s.r)))return false}return true})'))
results['dome_trajectory']=inside
js('SKIM.scatter();SKIM.scatter();SKIM.scatter()');time.sleep(1);results['dome_repeat']=js('SKIM.symbols.every(s=>Number.isFinite(s.x)&&Number.isFinite(s.a))')
lengths=[]
for size in [10,38,20]:
 js(f'var r=document.querySelector(".size-range");r.value={size};r.dispatchEvent(new Event("input"))')
 lengths.append(js('({length:document.querySelector(".dynamic-copy").textContent.length,overflow:document.querySelector(".dynamic-copy").scrollHeight>document.querySelector(".dynamic-copy").clientHeight+1})'))
results['slider']=lengths
js('scrollTo(0,0)');wait();js('scrollTo(0,document.querySelectorAll(".screen")[8].offsetTop)');wait();results['slider_persistence']=js('document.querySelector(".size-range").value')
b.screenshot('review/slider-active.png')
for width,height in [(1920,800),(390,844),(768,1024)]:
 b.call('Emulation.setDeviceMetricsOverride',{'width':width,'height':height,'deviceScaleFactor':1,'mobile':False});wait();
 results[f'layout_{width}']=js('({overflow:document.documentElement.scrollWidth>innerWidth,svg:document.querySelectorAll(".screen")[8].querySelector("svg").getBoundingClientRect().toJSON(),stage:document.querySelectorAll(".stage")[8].getBoundingClientRect().toJSON(),copyFits:document.querySelector(".dynamic-copy").scrollHeight<=document.querySelector(".dynamic-copy").clientHeight+1})')
 if width==390:b.screenshot('review/mobile.png')
b.call('Emulation.setDeviceMetricsOverride',{'width':1680,'height':1079,'deviceScaleFactor':1,'mobile':False});js('scrollTo(0,document.querySelectorAll(".screen")[5].offsetTop)');wait();b.screenshot('review/reading-active.png')
results['errors']=[e for e in b.events if e.get('method')=='Runtime.exceptionThrown' or e.get('method')=='Log.entryAdded' and e['params']['entry']['level']=='error']
open('review/qa.json','w').write(json.dumps(results,indent=2));print(json.dumps(results))

