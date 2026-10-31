from pathlib import Path
from browser import Browser
import time
b=Browser();b.call('Emulation.setDeviceMetricsOverride',{'width':1680,'height':1079,'deviceScaleFactor':1,'mobile':False});b.call('Page.navigate',{'url':'http://127.0.0.1:8000/?reference'});time.sleep(.4)
for i in range(10):
 b.js(f'window.scrollTo(0,document.querySelectorAll(".screen")[{i}].offsetTop);SKIM.render()');time.sleep(.06);b.screenshot(f'review/before/screen-{i+1}.png')
print('Saved 10 baseline screenshots before migration')
