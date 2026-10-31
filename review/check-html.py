from browser import Browser
from pathlib import Path
import time,json
Path('review/after').mkdir(exist_ok=True)
b=Browser();b.call('Emulation.setTouchEmulationEnabled',{'enabled':False});b.call('Runtime.enable');b.call('Log.enable');b.call('Emulation.setDeviceMetricsOverride',{'width':1680,'height':1079,'deviceScaleFactor':1,'mobile':False});b.call('Page.navigate',{'url':'http://127.0.0.1:8000/?reference'});time.sleep(.5)
print(b.js('({ready:!!window.SKIM,svg:document.querySelectorAll("svg,path,img,canvas,object,embed").length,sections:document.querySelectorAll(".scene").length,bodyWidth:document.body.scrollWidth,words:window.SKIM?.readingWords.length})'))
for i in range(10):
 b.js(f'window.scrollTo(0,document.querySelectorAll(".scene")[{i}].offsetTop);SKIM.render()');time.sleep(.06);b.screenshot(f'review/after/screen-{i+1}.png')
print([e for e in b.events if e.get('method')=='Runtime.exceptionThrown' or e.get('method')=='Log.entryAdded' and e['params']['entry']['level']=='error'])
Path('review/after/contact.html').write_text('<style>body{margin:0;display:grid;grid-template-columns:1fr 1fr}img{width:100%}</style>'+''.join(f'<img src="screen-{i}.png">' for i in range(1,11)))
b.call('Emulation.setDeviceMetricsOverride',{'width':1680,'height':2780,'deviceScaleFactor':1,'mobile':False});b.call('Page.navigate',{'url':'http://127.0.0.1:8000/review/after/contact.html'});time.sleep(.3);b.screenshot('review/after/contact.png')
