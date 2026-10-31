from browser import Browser
from pathlib import Path
import json,time
b=Browser();b.call('Emulation.setTouchEmulationEnabled',{'enabled':False});b.call('Emulation.setEmulatedMedia',{'features':[]});b.call('Emulation.setDeviceMetricsOverride',{'width':844,'height':390,'deviceScaleFactor':1,'mobile':False});b.call('Page.navigate',{'url':'http://127.0.0.1:8000/?reference'});time.sleep(.25)
r=b.js('(()=>{const title=document.querySelector(".cover-title").getBoundingClientRect(),p=document.querySelector(".cover-description").getBoundingClientRect(),button=document.querySelector(".learn").getBoundingClientRect();return{titleBeforeParagraph:title.bottom<=p.top,paragraphBeforeButton:p.bottom<=button.top,overflow:document.documentElement.scrollWidth>innerWidth}})()');print(r)
Path('review/revision-landscape.json').write_text(json.dumps(r,indent=2))
b.call('Emulation.setDeviceMetricsOverride',{'width':1680,'height':1079,'deviceScaleFactor':1,'mobile':False});b.call('Page.navigate',{'url':'http://127.0.0.1:8000/'});time.sleep(.15)
print(b.js('({ready:!!window.SKIM,holdMs:SKIM.CONFIG.holdMs,pulseMs:SKIM.CONFIG.pulseDuration,sections:document.querySelectorAll(".scene").length,stars:document.querySelectorAll(".collage-stars button").length})'))
