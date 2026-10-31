from browser import Browser
from pathlib import Path
import time,json
b=Browser();b.call('Emulation.setTouchEmulationEnabled',{'enabled':False});b.call('Runtime.enable');b.call('Log.enable')
b.call('Emulation.setDeviceMetricsOverride',{'width':1680,'height':1079,'deviceScaleFactor':1,'mobile':False})
b.call('Page.navigate',{'url':'http://127.0.0.1:8000/'})
time.sleep(.4);results={}
def js(s):return b.js(s)
def goto(i):
 js(f'scrollTo(0,document.querySelectorAll(".scene")[{i}].offsetTop);SKIM.render()');time.sleep(.06)
results['interface']=js('({sections:document.querySelectorAll("section").length,forbidden:document.querySelectorAll("svg,path,img,canvas,object,embed,iframe").length,text:document.querySelector("h1").textContent})')
js('document.querySelector(".definition-trigger").focus()');time.sleep(.25)
results['focus_tooltip']=js('getComputedStyle(document.querySelector(".tooltip")).visibility')
js('document.querySelector(".definition-trigger").click()');results['touch_toggle']=js('document.querySelector(".definition").classList.contains("open")')
js('document.querySelector(".learn").click()');time.sleep(.9)
results['learn']=js('Math.abs(scrollY-document.querySelectorAll(".scene")[1].offsetTop)<3')
goto(1);results['pulse_visible']=js('getComputedStyle(document.querySelector(".year span")).animationPlayState')
goto(7);results['pulse_offscreen']=js('getComputedStyle(document.querySelector(".year span")).animationPlayState')
js('SKIM.scatter()');samples=[]
for _ in range(9):
 time.sleep(.10);samples.append(js('(()=>{const m=SKIM.domeMetrics();return SKIM.symbols.every(s=>SKIM.circleInside(s.x*m.width/1680,s.y*m.height/1079,SKIM.symbolRadius(s),m.polygon))})()'))
results['dome_all_trajectory_samples']=samples
js('SKIM.scatter();SKIM.scatter();SKIM.scatter()');time.sleep(.95)
results['dome_repeat']=js('(()=>{const m=SKIM.domeMetrics();return SKIM.symbols.every(s=>SKIM.circleInside(s.x*m.width/1680,s.y*m.height/1079,SKIM.symbolRadius(s),m.polygon)&&!s.frame)})()')
saved=js('SKIM.symbols.map(s=>[s.x,s.y,s.a])');goto(0);goto(7);results['dome_persistence']=saved==js('SKIM.symbols.map(s=>[s.x,s.y,s.a])')
goto(8);lengths=[]
for size in [10,38,20]:
 js(f'var r=document.querySelector("#text-size");r.value={size};r.dispatchEvent(new Event("input"))')
 lengths.append(js('({length:document.querySelector(".resize-copy").textContent.length,overflow:document.querySelector(".resize-copy").scrollHeight>document.querySelector(".resize-copy").clientHeight+1})'))
results['slider_extremes']=lengths
goto(0);goto(8);results['slider_persistence']=js('document.querySelector("#text-size").value')
js('document.querySelector("#text-size").focus()')
for key in ['End','Home']:
 b.call('Input.dispatchKeyEvent',{'type':'keyDown','key':key,'code':key});b.call('Input.dispatchKeyEvent',{'type':'keyUp','key':key,'code':key});results['keyboard_'+key]=js('document.querySelector("#text-size").value')
js('document.activeElement.blur()')
goto(2);state=js('[...document.querySelectorAll(".scanner")].map(n=>n.style.transform)');goto(9);goto(2)
results['reverse_scan']=state==js('[...document.querySelectorAll(".scanner")].map(n=>n.style.transform)')
goto(5);state=js('({words:document.querySelectorAll(".is-read").length,counter:document.querySelector(".counter-tape").style.transform})');goto(9);goto(5)
results['reverse_reading']=state==js('({words:document.querySelectorAll(".is-read").length,counter:document.querySelector(".counter-tape").style.transform})')
js('scrollTo(0,document.querySelectorAll(".scene")[1].offsetTop-55)');time.sleep(.2)
b.call('Input.dispatchMouseEvent',{'type':'mouseWheel','x':800,'y':500,'deltaX':0,'deltaY':400});time.sleep(.5)
results['cancel_correction']=js('scrollY>document.querySelectorAll(".scene")[1].offsetTop+100')
b.call('Emulation.setEmulatedMedia',{'features':[{'name':'prefers-reduced-motion','value':'reduce'}]});goto(3)
results['reduced_motion']=js('({pulse:getComputedStyle(document.querySelector(".year span")).animationName,cards:[...document.querySelectorAll(".card-motion")].every(n=>n.style.opacity==="1")})')
b.call('Emulation.setEmulatedMedia',{'features':[]})
for width,height in [(390,844),(768,1024),(1920,800)]:
 b.call('Emulation.setDeviceMetricsOverride',{'width':width,'height':height,'deviceScaleFactor':1,'mobile':False});time.sleep(.15);goto(8)
 results['layout_'+str(width)]=js('({overflow:document.documentElement.scrollWidth>innerWidth,textFits:document.querySelector(".resize-copy").scrollHeight<=document.querySelector(".resize-copy").clientHeight+1,font:parseFloat(getComputedStyle(document.querySelector(".resize-copy")).fontSize)})')
 b.screenshot(f'review/after/slider-{width}.png')
 if width==390:
  for index in [0,1,2,3,5,6,7,9]:goto(index);b.screenshot(f'review/after/mobile-{index+1}.png')
  goto(7);js('SKIM.scatter()');time.sleep(.95)
  results['mobile_dome']=js('(()=>{const m=SKIM.domeMetrics();return SKIM.symbols.every(s=>SKIM.circleInside(s.x*m.width/1680,s.y*m.height/1079,SKIM.symbolRadius(s),m.polygon))})()')
results['errors']=[e for e in b.events if e.get('method')=='Runtime.exceptionThrown' or e.get('method')=='Log.entryAdded' and e['params']['entry']['level']=='error']
Path('review/after/qa.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
print(json.dumps(results))
