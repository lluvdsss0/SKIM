from browser import Browser
from pathlib import Path
import json,time
Path('review/revision-after').mkdir(exist_ok=True)
b=Browser();b.call('Runtime.enable');b.call('Log.enable');out={}
def js(s):return b.js(s)
def reload(width,height,mobile=False):
 b.call('Emulation.setDeviceMetricsOverride',{'width':width,'height':height,'deviceScaleFactor':1,'mobile':mobile});b.call('Page.navigate',{'url':'http://127.0.0.1:8000/'});time.sleep(.25)
def go(i):js(f'scrollTo(0,document.querySelectorAll(".scene")[{i}].offsetTop);SKIM.render()');time.sleep(.05)
for width,height in [(390,844),(768,1024),(1920,800)]:
 reload(width,height);js('SKIM.playback.finishAll()');go(2)
 out['geometry_'+str(width)]=js('''(()=>{let safe=true,inside=true;const overlap=(a,b)=>Math.min(a.right,b.right)>Math.max(a.left,b.left)+.1&&Math.min(a.bottom,b.bottom)>Math.max(a.top,b.top)+.1;for(let i=0;i<=200;i++){SKIM.playback.states[2].value=i/200;SKIM.render();const p=document.querySelector('.scan-panel--left').getBoundingClientRect(),whites=[...document.querySelectorAll('.white-block')].map(n=>n.getBoundingClientRect()),blacks=[...document.querySelectorAll('.scanner')].map(n=>n.getBoundingClientRect());safe&&=!whites.some(a=>blacks.some(b=>overlap(a,b)));inside&&=[...whites,...blacks].every(r=>r.left>=p.left-.2&&r.right<=p.right+.2&&r.top>=p.top-.2&&r.bottom<=p.bottom+.2)}return{safe,inside,overflow:document.documentElement.scrollWidth>innerWidth}})()''')
 go(1);out['lines_'+str(width)]=js('''[...document.querySelectorAll('.history-card')].map((n,i)=>{const c=n.getBoundingClientRect(),line=document.querySelectorAll('.history-connector')[i].getBoundingClientRect(),year=document.querySelectorAll('.year')[i].getBoundingClientRect();return{startsAtBottom:Math.abs(c.bottom-line.top)<1,endsAtYear:Math.abs(line.bottom-year.top)<1,centered:Math.abs(c.x+c.width/2-line.x)<1,opaque:getComputedStyle(n).backgroundColor}})''')
 go(7);out['dome_gap_'+str(width)]=js('''(()=>{const b=document.querySelector('.break-button').getBoundingClientRect(),h=document.querySelector('.dome-heading').getBoundingClientRect(),d=document.querySelector('.dome-shape').getBoundingClientRect();return{headingAboveButton:h.bottom<=b.top,buttonAboveDome:b.bottom<d.top+d.height*503/1079,gap:d.top+d.height*503/1079-b.bottom}})()''')
 js('document.querySelector(".break-button").click()');time.sleep(.9);out['scatter_'+str(width)]=js('(()=>{const m=SKIM.domeMetrics();return SKIM.symbols.every(s=>SKIM.circleInside(s.x*m.width/1680,s.y*m.height/1079,SKIM.symbolRadius(s),m.polygon))})()')
 go(8);out['copy_'+str(width)]=js('({fits:document.querySelector(".resize-copy").scrollHeight<=document.querySelector(".resize-copy").clientHeight+1})')
 if width==390:
  for i in [0,1,2,5,6,7,8,9]:go(i);b.screenshot(f'review/revision-after/mobile-{i+1}.png')
  js('document.querySelector("[data-tooltip-key=final-11]").focus()');time.sleep(.2);out['mobile_tip']=js('(()=>{const r=document.querySelector(".floating-tooltip").getBoundingClientRect();return r.left>=0&&r.right<=document.documentElement.clientWidth&&r.top>=0&&r.bottom<=innerHeight})()');b.screenshot('review/revision-after/mobile-tip.png')
reload(390,844,True);b.call('Emulation.setTouchEmulationEnabled',{'enabled':True,'maxTouchPoints':1});go(1);time.sleep(.24)
anchor=js('scrollY')
b.call('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':185,'y':650}]})
for y in [600,540,470,390]:b.call('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':185,'y':y}]});time.sleep(.04)
b.call('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]});time.sleep(.1)
out['touch_hold_discards_scroll']=abs(js('scrollY')-anchor)<2
js('SKIM.playback.finishAll()');go(8)
r=js('document.querySelector("#text-size").getBoundingClientRect().toJSON()');y=r['y']+r['height']/2
b.call('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':r['x']+r['width']*.2,'y':y}]});b.call('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':r['x']+r['width']*.9,'y':y}]});b.call('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]});out['touch_range']=js('document.querySelector("#text-size").value')
out['errors']=[e for e in b.events if e.get('method')=='Runtime.exceptionThrown' or e.get('method')=='Log.entryAdded' and e['params']['entry']['level']=='error']
Path('review/revision-mobile.json').write_text(json.dumps(out,indent=2),encoding='utf-8');print(json.dumps(out))
