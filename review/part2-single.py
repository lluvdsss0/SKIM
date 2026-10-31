from browser import Browser
from pathlib import Path
import time
b=Browser()
for i in [65,70,72,73,77,78]:
 h=1369 if i==78 else 1079
 Path('review/part2-single.html').write_text(f'<style>body{{margin:0}}img{{display:block;width:1680px}}</style><img src="../assets/Frame {i}.svg">')
 b.call('Emulation.setDeviceMetricsOverride',{'width':1680,'height':h,'deviceScaleFactor':1,'mobile':False});b.call('Page.navigate',{'url':f'http://127.0.0.1:8000/review/part2-single.html?frame={i}'});time.sleep(.12);b.screenshot(f'review/source-{i}.png')
