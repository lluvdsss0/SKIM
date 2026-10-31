from browser import Browser
from pathlib import Path
import json,time
b=Browser();b.call('Network.enable');b.call('Network.setCacheDisabled',{'cacheDisabled':True});b.call('Runtime.enable');b.call('Log.enable');b.call('Emulation.setEmulatedMedia',{'features':[]});b.call('Emulation.setTouchEmulationEnabled',{'enabled':False});b.call('Emulation.setDeviceMetricsOverride',{'width':1680,'height':1079,'deviceScaleFactor':1,'mobile':False});b.call('Page.navigate',{'url':'http://127.0.0.1:8000/'});time.sleep(.25)
def js(s):return b.js(s)
def go(i):js(f'scrollTo(0,document.querySelectorAll(".scene")[{i}].offsetTop);SKIM.render()');time.sleep(.07)
out={}
js('var s=SKIM.playback.states[3];scrollTo(0,s.start+(s.end-s.start)*.3);SKIM.render()');time.sleep(.07);a=js('SKIM.playback.value(3)')
b.call('Input.dispatchMouseEvent',{'type':'mouseWheel','x':800,'y':500,'deltaX':0,'deltaY':40});time.sleep(.2);p=js('SKIM.playback.value(3)');out['wheel_changes_progress']=p>a
time.sleep(.35);out['wheel_stop_stable']=p==js('SKIM.playback.value(3)')
y=js('scrollY')
for t in ['keyDown','keyUp']:b.call('Input.dispatchKeyEvent',{'type':t,'key':'PageDown','code':'PageDown','windowsVirtualKeyCode':34,'nativeVirtualKeyCode':34})
time.sleep(.35);out['keyboard_scroll_free']=js('scrollY')>y+200
go(6);js('document.querySelector(".lock-badge").click()');out['notification_opens']=js('!document.querySelector(".distraction-toast").hidden&&document.querySelector(".distraction-toast span").textContent.length>0')
go(7);js('document.querySelector(".break-button").click()');time.sleep(.15);y=js('scrollY');b.call('Input.dispatchMouseEvent',{'type':'mouseWheel','x':800,'y':500,'deltaX':0,'deltaY':200});time.sleep(.15);out['leave_scattering_immediately']=js('scrollY')>y+100
go(8);r=js('document.querySelector("#text-size").getBoundingClientRect().toJSON()');thumb=js('document.querySelector(".size-thumb").getBoundingClientRect().toJSON()');x=thumb['x']+thumb['width']/2;y=r['y']+r['height']/2;end=r['x']+r['width']*.9
for t,xx,button,buttons in [('mouseMoved',x,'none',0),('mousePressed',x,'left',1),('mouseMoved',end,'left',1),('mouseReleased',end,'left',0)]:b.call('Input.dispatchMouseEvent',{'type':t,'x':xx,'y':y,'button':button,'buttons':buttons,'clickCount':1});time.sleep(.04)
out['mouse_slider_value']=js('document.querySelector("#text-size").value')
y=js('scrollY');b.call('Input.dispatchMouseEvent',{'type':'mouseWheel','x':800,'y':500,'deltaX':0,'deltaY':170});time.sleep(.2);out['after_slider_scroll_free']=js('scrollY')>y+80
b.call('Emulation.setDeviceMetricsOverride',{'width':390,'height':844,'deviceScaleFactor':1,'mobile':True});b.call('Emulation.setTouchEmulationEnabled',{'enabled':True,'maxTouchPoints':1});go(6);js('document.querySelector(".lock-badge").click()');y=js('scrollY')
b.call('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':185,'y':670}]})
for touchY in [620,560,490,410]:b.call('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':185,'y':touchY}]});time.sleep(.05)
b.call('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]});time.sleep(.3);out['touch_with_toast_scrolls']=js('scrollY')>y+80
out['errors']=[e for e in b.events if e.get('method')=='Runtime.exceptionThrown' or e.get('method')=='Log.entryAdded' and e['params']['entry']['level']=='error']
Path('review/scroll-input.json').write_text(json.dumps(out,indent=2));print(out)
