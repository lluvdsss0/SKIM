from browser import Browser
import time,json
b=Browser();b.call('Network.enable');b.call('Network.setCacheDisabled',{'cacheDisabled':True});b.call('Runtime.enable')
b.call('Emulation.setDeviceMetricsOverride',{'width':1680,'height':1079,'deviceScaleFactor':1,'mobile':False})
b.call('Page.navigate',{'url':'http://127.0.0.1:8000/?reference&referenceFrame=70'});time.sleep(.6)
print(b.js('({scenes:document.querySelectorAll(".scene").length,ready:!!window.SKIM,p2:!!window.SKIM_PART2,objects:window.SKIM_PART2?.objects.length})'))
print([x for x in b.events if x.get('method')=='Runtime.exceptionThrown'])
print(b.js('window.SKIM_PART2?.objects.slice(0,2).map(o=>({kind:o.kind,box:o.box,z:o.z}))'))
b.js('document.querySelector("#screen-16").scrollIntoView();SKIM.render()');time.sleep(.15);b.screenshot('review/part2-density-70.png')
