from browser import Browser
from pathlib import Path
import time,json,re
b=Browser();b.call('Network.enable');b.call('Network.setCacheDisabled',{'cacheDisabled':True});b.call('Runtime.enable')
def nav(query=''):
 b.call('Page.navigate',{'url':'http://127.0.0.1:8000/'+query});time.sleep(.3)
def size(w,h):b.call('Emulation.setDeviceMetricsOverride',{'width':w,'height':h,'deviceScaleFactor':1,'mobile':False})
def progress(index,p):
 b.js(f'window.scrollTo(0,SKIM.playback.states[{index}].start+({p})*(SKIM.playback.states[{index}].end-SKIM.playback.states[{index}].start));SKIM.render()');time.sleep(.04)
def state():return b.js('JSON.stringify([...document.querySelectorAll(".part-two [style]")].map(n=>n.getAttribute("style")))')
size(1680,1079);nav()
assert b.js('SKIM_PART2.people.length')==168
assert b.js('document.querySelectorAll("footer").length')==1
for i in range(10,18):
 progress(i,.35);a=state();time.sleep(.2);assert a==state(),('idle',i)
 progress(i,.8);progress(i,.35);assert a==state(),('reverse',i)
for p,count in [(0,0),(.15,1),(.30,2),(.45,3),(.61,4)]:
 progress(11,p);actual=b.js('[...document.querySelectorAll(".p2-notice")].filter(n=>+n.style.opacity>.99).length');assert actual==count,(p,actual)
for p,cards,stars in [(0,13,5),(.5,17,9),(1,27,20)]:
 progress(15,p)
 got=b.js('SKIM_PART2.objects.filter(o=>+o.node.style.opacity>.99).reduce((a,o)=>(a[o.kind]++,a),{card:0,star:0})');assert got=={'card':cards,'star':stars},got
 b.screenshot(f'review/part2-density-{[70,72,73][[0,.5,1].index(p)]}.png')
for p in [0,.18,.35,.55,.70,.73,.83,1]:
 progress(17,p)
 info=b.js('({a:SKIM_PART2.messages.map(m=>m.node.style.opacity),left:SKIM_PART2.messages.map(m=>m.node.getBoundingClientRect().left),edge:document.querySelector(".p2-people-message-layer").getBoundingClientRect().right,heading:+document.querySelector(".p2-people-heading--final").style.opacity,footer:getComputedStyle(document.querySelector("footer")).visibility})')
 assert len(set(info['a']))==1,info
 if p>=.70:assert min(info['left'])>info['edge']+20,info
 if p<=.73:assert info['heading']==0,info
 if p<1:assert info['footer']=='hidden',info
 if p==.35:b.screenshot('review/part2-people-77.png')
 if p==1:b.screenshot('review/part2-people-78.png')
for w,h in [(390,844),(768,1024),(1920,1080)]:
 size(w,h);time.sleep(.15)
 for i in [11,15,17]:
  progress(i,.55);assert b.js('document.documentElement.scrollWidth<=innerWidth'),('overflow',w,i)
 progress(17,.7);assert b.js('Math.min(...SKIM_PART2.messages.map(m=>m.node.getBoundingClientRect().left))>document.querySelector(".p2-people-message-layer").getBoundingClientRect().right'),('exit',w)
 if w==390:progress(11,.85);b.screenshot('review/part2-mobile-notifications.png')
size(1680,1079)
b.call('Emulation.setEmulatedMedia',{'features':[{'name':'prefers-reduced-motion','value':'reduce'}]});time.sleep(.15)
progress(13,.3);assert b.js('[...document.querySelectorAll(".p2-reply")].every(n=>+n.style.opacity===1)')
assert b.js('document.querySelector("#screen-14").offsetHeight<innerHeight+2')
b.call('Emulation.setEmulatedMedia',{'features':[]})
old=Path('review/part2-before/index.html').read_text(encoding='utf-8');new=Path('index.html').read_text(encoding='utf-8')
assert re.findall(r'<section\b.*?</section>',old.replace('>respected</span>','>unexpected</span>'),re.S)==re.findall(r'<section\b.*?</section>',new,re.S)[:10]
errors=[x for x in b.events if x.get('method')=='Runtime.exceptionThrown'];assert not errors,errors
print('PASS: 18 scenes, 47 persistent collage objects, 168 people; idle/reverse/replay, notification order, density 70/72/73, complete message exit before highlight, footer gate, 390/768/1920 widths, reduced motion, original ten section bodies unchanged; no JS exceptions.')
