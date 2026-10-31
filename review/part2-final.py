from browser import Browser
import time
b=Browser();b.call('Emulation.setDeviceMetricsOverride',{'width':1680,'height':1369,'deviceScaleFactor':1,'mobile':False});b.call('Page.navigate',{'url':'http://127.0.0.1:8000/?reference&referenceFrame=78'});time.sleep(.3)
b.js('''(()=>{const style=document.createElement('style');style.textContent='html{scrollbar-width:none}#screen-18{height:1050.23px!important;min-height:0!important}#screen-18 .composition{position:relative!important;top:0!important}';document.head.append(style)})()''');time.sleep(.2);b.js('document.querySelector("#screen-18").scrollIntoView();SKIM.render()');time.sleep(.1);b.screenshot('review/part2-final-with-footer.png')
