from browser import Browser
from pathlib import Path
import json,time
b=Browser();b.call('Runtime.enable');b.call('Log.enable');b.call('Emulation.setTouchEmulationEnabled',{'enabled':False});b.call('Emulation.setEmulatedMedia',{'features':[]});b.call('Emulation.setDeviceMetricsOverride',{'width':1680,'height':1079,'deviceScaleFactor':1,'mobile':False})
def js(s):return b.js(s)
def fresh():b.call('Page.navigate',{'url':'http://127.0.0.1:8000/'});time.sleep(.25)
def key(k):
 b.call('Input.dispatchKeyEvent',{'type':'keyDown','key':k,'code':k,'windowsVirtualKeyCode':{'PageDown':34,'PageUp':33}.get(k,0),'nativeVirtualKeyCode':{'PageDown':34,'PageUp':33}.get(k,0)});b.call('Input.dispatchKeyEvent',{'type':'keyUp','key':k,'code':k,'windowsVirtualKeyCode':{'PageDown':34,'PageUp':33}.get(k,0),'nativeVirtualKeyCode':{'PageDown':34,'PageUp':33}.get(k,0)})
out={};fresh();js('scrollTo(0,document.querySelectorAll(".scene")[1].offsetTop)');time.sleep(.3);y=js('scrollY');key('PageDown');time.sleep(.16);out['keyboard_hold']=abs(js('scrollY')-y)<1
key('PageUp');time.sleep(.35);out['keyboard_reverse_state']=js('({active:SKIM.playback.active?.index??null,scroll:scrollY,anchor:document.querySelectorAll(".scene")[1].offsetTop,focus:document.activeElement.tagName})');out['keyboard_reverse_exits']=js('SKIM.playback.active===null&&scrollY<document.querySelectorAll(".scene")[1].offsetTop-20')
fresh();js('SKIM.playback.finishAll();scrollTo(0,document.querySelectorAll(".scene")[9].offsetTop);SKIM.render()');time.sleep(.1)
r=js('document.querySelector("[data-tooltip-key=final-0]").getBoundingClientRect().toJSON()')
b.call('Input.dispatchMouseEvent',{'type':'mouseMoved','x':r['x']+r['width']/2,'y':r['y']+r['height']/2});time.sleep(.1)
r=js('document.querySelector(".floating-tooltip").getBoundingClientRect().toJSON()')
b.call('Input.dispatchMouseEvent',{'type':'mouseMoved','x':r['x']+r['width']/2,'y':r['y']+r['height']/2});time.sleep(.25)
out['hover_bridge']=js('document.querySelector(".floating-tooltip").classList.contains("open")')
b.call('Input.dispatchMouseEvent',{'type':'mouseMoved','x':50,'y':20});time.sleep(.25);out['hover_leave']=js('!document.querySelector(".floating-tooltip").classList.contains("open")')
js('scrollTo(0,document.querySelectorAll(".scene")[8].offsetTop);SKIM.render()');time.sleep(.1)
r=js('document.querySelector("#text-size").getBoundingClientRect().toJSON()');thumb=js('document.querySelector(".size-thumb").getBoundingClientRect().toJSON()');x=thumb['x']+thumb['width']/2;y=r['y']+r['height']/2;end=r['x']+r['width']*.95
for t,xx,button,buttons in [('mouseMoved',x,'none',0),('mousePressed',x,'left',1),('mouseMoved',end,'left',1),('mouseReleased',end,'left',0)]:b.call('Input.dispatchMouseEvent',{'type':t,'x':xx,'y':y,'button':button,'buttons':buttons,'clickCount':1});time.sleep(.05)
out['mouse_range']=js('document.querySelector("#text-size").value')
js('scrollTo(0,document.querySelectorAll(".scene")[6].offsetTop);document.querySelector(".lock-badge").click()');time.sleep(3.1);out['toast_timeout']=js('document.querySelector(".distraction-toast").hidden')
out['errors']=[e for e in b.events if e.get('method')=='Runtime.exceptionThrown' or e.get('method')=='Log.entryAdded' and e['params']['entry']['level']=='error']
Path('review/revision-input.json').write_text(json.dumps(out,indent=2));print(out)
