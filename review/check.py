from browser import Browser
import json,time,pathlib
b=Browser();b.call('Runtime.enable');b.call('Log.enable');b.call('Emulation.setDeviceMetricsOverride',{'width':1680,'height':1079,'deviceScaleFactor':1,'mobile':False});b.call('Page.navigate',{'url':'http://127.0.0.1:8000/?reference'});time.sleep(1)
print(b.js('JSON.stringify({screens:document.querySelectorAll(".screen").length,ids:[...document.querySelectorAll("[id]")].length,unique:new Set([...document.querySelectorAll("[id]")].map(n=>n.id)).size,words:SKIM.wordMasks.length,symbols:SKIM.symbols.length,stages:[...document.querySelectorAll(".stage")].map(n=>[n.clientWidth,n.clientHeight])})'))
for i in range(10):
 b.js(f'window.scrollTo(0,document.querySelectorAll(".screen")[{i}].offsetTop);SKIM.render()');time.sleep(.1);b.screenshot(f'review/screen-{i+1}.png')
print(b.js('JSON.stringify({overflow:document.documentElement.scrollWidth>innerWidth,copy:document.querySelector(".dynamic-copy").hidden})'))
print([e for e in b.events if e.get('method') in ['Runtime.exceptionThrown','Log.entryAdded']])
