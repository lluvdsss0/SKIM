from browser import Browser
from pathlib import Path
import time
b=Browser();b.call('Network.enable');b.call('Network.setCacheDisabled',{'cacheDisabled':True});b.call('Emulation.setEmulatedMedia',{'features':[]});b.call('Emulation.setDeviceMetricsOverride',{'width':1680,'height':4600,'deviceScaleFactor':1,'mobile':False});b.call('Page.navigate',{'url':'http://127.0.0.1:8000/review/part2-sources.html'});time.sleep(.25);b.screenshot('review/part2-sources.png')
