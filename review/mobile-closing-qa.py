from browser import Browser
from pathlib import Path
import time,json
b=Browser();b.call('Runtime.enable')
b.call('Page.navigate',{'url':'http://127.0.0.1:8000/'})
time.sleep(.7)
results=[]
for w,h in [(320,640),(390,844),(430,932),(768,1024),(1024,768),(768,540),(540,768)]:
 b.call('Emulation.setDeviceMetricsOverride',{'width':w,'height':h,'deviceScaleFactor':1,'mobile':False})
 time.sleep(.25)
 assert b.js('!!window.SKIM'),'load'
 assert b.js('document.querySelector(".cover-description").textContent.includes("и\\u00a0исследования")')
 for i in range(12,18):
  for p in [.1,.3,.5,.7,.9,1]:
   b.js(f'window.scrollTo(0,SKIM.playback.states[{i}].start+{p}*(SKIM.playback.states[{i}].end-SKIM.playback.states[{i}].start));SKIM.render()')
   time.sleep(.025)
   info=b.js('''(()=>{const s=document.querySelectorAll('.scene')['''+str(i)+'''];return {overflow:document.documentElement.scrollWidth>innerWidth,quotes:[...s.querySelectorAll('.p2-quote,.p2-people-heading')].filter(n=>+n.style.opacity>.1).map(n=>{const r=n.getBoundingClientRect();return {left:r.left,right:r.right,top:r.top,bottom:r.bottom}})}})()''')
   assert not info['overflow'],(w,h,i,p,info)
   for r in info['quotes']:assert r['left']>=-1 and r['right']<=w+1 and r['top']>=-1 and r['bottom']<=h+1,(w,h,i,p,r)
  if w in [320,768,1024]:b.screenshot(f'review/closing-{w}-{i+1}.png')
 b.js('SKIM_PART2.render(document.querySelector("[data-part2=people]"),.71)')
 assert b.js('SKIM_PART2.messages.every(m=>m.node.getBoundingClientRect().left>innerWidth)'),('message exit',w)
 results.append({'width':w,'height':h,'scenes':6,'progressSamples':6,'overflow':False})
for w,h in [(320,640),(1024,768),(768,540)]:
 b.call('Emulation.setDeviceMetricsOverride',{'width':w,'height':h,'deviceScaleFactor':1,'mobile':False})
 b.call('Emulation.setEmulatedMedia',{'features':[{'name':'prefers-reduced-motion','value':'reduce'}]})
 time.sleep(.2)
 b.js('document.querySelector("#screen-14").scrollIntoView();SKIM.render()')
 assert b.js('[...document.querySelectorAll(".p2-reply")].every(n=>n.getBoundingClientRect().height<=n.parentElement.clientHeight && +n.style.opacity===1)')
b.call('Emulation.setEmulatedMedia',{'features':[]})
errors=[e for e in b.events if e.get('method')=='Runtime.exceptionThrown']
assert not errors,errors
Path('review/mobile-closing-qa.json').write_text(json.dumps(results,indent=2))
print('PASS: closing scenes, quote bounds, no horizontal overflow, complete message exit, resize/orientation, NBSP; no JS exceptions',results)
