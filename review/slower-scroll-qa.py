from browser import Browser
import time,json
b=Browser();b.call('Network.enable');b.call('Network.setCacheDisabled',{'cacheDisabled':True});b.call('Runtime.enable');b.call('Page.navigate',{'url':'http://127.0.0.1:8000/'});time.sleep(.3)
results=[]
for width,height in [(1680,1079),(390,844),(768,1024),(1920,1080)]:
 b.call('Emulation.setDeviceMetricsOverride',{'width':width,'height':height,'deviceScaleFactor':1,'mobile':False});time.sleep(.2)
 ratios=b.js('''(()=>{const p=SKIM.playback,config=p.config;p.config={...config,scrollScale:1,staticHold:0};p.measure();const old=p.states.map(s=>s.end-s.start);p.config=config;p.measure();return p.states.map((s,i)=>({scene:i+1,ratio:(s.end-s.start)/old[i],range:s.end-s.start,height:p.scenes[i].offsetHeight}))})()''')
 assert all(r['range']>0 for r in ratios)
 for i in [1,2,3,4,5,9,10,11,12,13,14,15,16,17]:assert 1.3<ratios[i]['ratio']<1.6,(width,ratios[i])
 for i in [0,6,7,8]:
  b.js(f'scrollTo(0,document.querySelectorAll(".scene")[{i}].offsetTop+20);SKIM.render()');time.sleep(.03)
  top=b.js(f'document.querySelectorAll(".composition")[{i}].getBoundingClientRect().top')
  b.js('scrollBy(0,80);SKIM.render()');time.sleep(.03)
  assert abs(top-b.js(f'document.querySelectorAll(".composition")[{i}].getBoundingClientRect().top'))<1,(width,i,'sticky jump')
 for i in range(17):
  gap=b.js(f'document.querySelectorAll(".scene")[{i+1}].offsetTop-document.querySelectorAll(".scene")[{i}].offsetTop-document.querySelectorAll(".scene")[{i}].offsetHeight')
  assert abs(gap)<2,(width,i,gap)
 assert b.js('document.documentElement.scrollWidth<=innerWidth')
 results.append({'width':width,'animationRangeRatios':[round(r['ratio'],2) for r in ratios if r['scene'] in [2,5,12,16,18]],'contiguousSections':True,'staticScenesPinned':True})
print(json.dumps(results))
# Readable opacity plateau and notification/indicator synchronization, forward and reverse.
for i,selector in [(4,'.revealing-phrase'),(10,'.p2-fading-quote'),(12,'.p2-fading-quote'),(14,'.p2-fading-quote')]:
 for p in [.3,.6,.79,.6]:
  b.js(f'scrollTo(0,SKIM.playback.states[{i}].start+{p}*(SKIM.playback.states[{i}].end-SKIM.playback.states[{i}].start));SKIM.render()');time.sleep(.03)
  assert b.js(f'+getComputedStyle(document.querySelectorAll(".scene")[{i}].querySelector("{selector}")).opacity')>.99
for p,active in [(.15,0),(.30,1),(.45,2),(.61,3),(.30,1)]:
 b.js(f'scrollTo(0,SKIM.playback.states[11].start+{p}*(SKIM.playback.states[11].end-SKIM.playback.states[11].start));SKIM.render()');time.sleep(.03)
 assert b.js('[...document.querySelectorAll(".p2-indicator i")].findIndex(n=>n.classList.contains("is-active"))')==active
assert not [e for e in b.events if e.get('method')=='Runtime.exceptionThrown']
print('PASS: slower ranges, readable holds, contiguous sections, stable sticky, notification synchronization, reverse and no horizontal overflow/JS errors.')
