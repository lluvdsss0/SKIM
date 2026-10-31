from browser import Browser
from pathlib import Path
import time,json
b=Browser();b.call('Network.enable');b.call('Network.setCacheDisabled',{'cacheDisabled':True});b.call('Runtime.enable');b.call('Emulation.setDeviceMetricsOverride',{'width':1680,'height':1079,'deviceScaleFactor':1,'mobile':False});b.call('Page.navigate',{'url':'http://127.0.0.1:8000/'});time.sleep(.4)
def progress(i,p):
 b.js(f'scrollTo(0,SKIM.playback.states[{i}].start+{p}*(SKIM.playback.states[{i}].end-SKIM.playback.states[{i}].start));SKIM.render()');time.sleep(.05)
assert b.js('!!window.SKIM')
for p in [0,.5,1]:
 progress(9,p)
 assert b.js('[...document.querySelectorAll(".collage-word")].some(n=>n.textContent==="unexpected"&&getComputedStyle(n).visibility!=="hidden")')
 assert not b.js('document.body.innerText.includes("respected")')
 if p==0:b.screenshot('review/unexpected-visible.png')
progress(9,1);b.js('document.querySelector("[data-tooltip-key=final-4]").click()');time.sleep(.2)
assert b.js('document.querySelector("#floating-tooltip strong").textContent')=='Неожиданный'
assert b.js('document.querySelector("#floating-tooltip small").textContent')=='unexpected'
print('Tooltip: '+b.js('document.querySelector("#floating-tooltip").innerText'))
for p,expected in [(.15,0),(.30,1),(.45,2),(.61,3)]:
 progress(11,p);assert b.js('[...document.querySelectorAll(".p2-indicator i")].findIndex(n=>n.classList.contains("is-active"))')==expected
progress(11,.85);print('Indicator desktop: '+str(b.js('({top:getComputedStyle(document.querySelector(".p2-indicator")).top,left:getComputedStyle(document.querySelector(".p2-indicator")).left})')));b.screenshot('review/indicator-raised.png')
for p,expected in [(0,1),(.5,1),(1,2)]:
 progress(15,p);assert b.js('SKIM_PART2.objects.filter(o=>o.node.innerText.includes("unexpected")&&+o.node.style.opacity>.99).length')==expected
b.call('Emulation.setDeviceMetricsOverride',{'width':390,'height':844,'deviceScaleFactor':1,'mobile':False});time.sleep(.15);progress(11,.85);b.screenshot('review/indicator-raised-mobile.png')
print('Indicator mobile bottom: '+b.js('getComputedStyle(document.querySelector(".p2-indicator")).bottom'))
assert not [e for e in b.events if e.get('method')=='Runtime.exceptionThrown']
print('PASS: visible unexpected in collage states and repetitions, tooltip text, synchronized indicator, desktop/mobile; no JS errors.')
