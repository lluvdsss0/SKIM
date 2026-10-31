from browser import Browser
from pathlib import Path
import time,json
b=Browser();b.call('Emulation.setTouchEmulationEnabled',{'enabled':False});b.call('Emulation.setDeviceMetricsOverride',{'width':1680,'height':1079,'deviceScaleFactor':1,'mobile':False})
b.call('Page.navigate',{'url':'http://127.0.0.1:8000/'});time.sleep(.3)
def js(s):return b.js(s)
out={}
js('scrollTo(0,document.querySelectorAll(".scene")[8].offsetTop)');time.sleep(.1)
r=js('document.querySelector("#text-size").getBoundingClientRect().toJSON()');thumb=js('document.querySelector(".size-thumb").getBoundingClientRect().toJSON()');x=thumb['x']+thumb['width']/2;y=r['y']+r['height']/2
for t,xx in [('mouseMoved',x),('mousePressed',x),('mouseMoved',r['x']+r['width']*.95),('mouseReleased',r['x']+r['width']*.95)]:
 p={'type':t,'x':xx,'y':y}
 if t in ['mousePressed','mouseReleased']:p.update({'button':'left','clickCount':1})
 elif t=='mouseMoved':p.update({'buttons':1 if xx!=x else 0,'button':'left' if xx!=x else 'none'})
 b.call('Input.dispatchMouseEvent',p);time.sleep(.05)
out['mouse_drag_value']=js('document.querySelector("#text-size").value')
js('scrollTo(0,document.querySelectorAll(".scene")[7].offsetTop)');time.sleep(.1)
r=js('document.querySelector(".break-button").getBoundingClientRect().toJSON()');x=r['x']+r['width']/2;y=r['y']+r['height']/2
before=js('SKIM.symbols.map(s=>s.x)')
for t in ['mousePressed','mouseReleased']:b.call('Input.dispatchMouseEvent',{'type':t,'x':x,'y':y,'button':'left','clickCount':1})
time.sleep(.95);out['break_mouse_click']=before!=js('SKIM.symbols.map(s=>s.x)')
out['symbol_dom_coordinates']=js('(()=>{const m=SKIM.domeMetrics(),layer=document.querySelector(".dome-symbols").getBoundingClientRect();return SKIM.symbols.every(s=>{const r=s.n.getBoundingClientRect();return Math.abs(r.x+r.width/2-layer.x-s.x*m.width/1680)<1&&Math.abs(r.y+r.height/2-layer.y-s.y*m.height/1079)<1})})()')
b.call('Emulation.setDeviceMetricsOverride',{'width':390,'height':844,'deviceScaleFactor':1,'mobile':True})
b.call('Emulation.setTouchEmulationEnabled',{'enabled':True,'maxTouchPoints':1});js('scrollTo(0,0)');time.sleep(.15)
r=js('document.querySelector(".definition-trigger").getBoundingClientRect().toJSON()');point={'x':r['x']+r['width']/2,'y':r['y']+r['height']/2}
b.call('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[point]});b.call('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]});time.sleep(.25)
out['touch_tooltip']=js('document.querySelector(".definition").classList.contains("open")')
js('scrollTo(0,document.querySelectorAll(".scene")[8].offsetTop)');time.sleep(.15)
r=js('document.querySelector("#text-size").getBoundingClientRect().toJSON()');y=r['y']+r['height']/2;start=r['x']+r['width']*.2;end=r['x']+r['width']*.9
b.call('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':start,'y':y}]});b.call('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':end,'y':y}]});b.call('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]})
out['touch_slider_value']=js('document.querySelector("#text-size").value')
Path('review/after/pointer.json').write_text(json.dumps(out,indent=2));print(out)
