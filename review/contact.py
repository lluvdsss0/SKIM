from pathlib import Path
from browser import Browser
import time
p=Path('review/rendered.html');p.write_text('<meta charset="utf-8"><style>body{margin:0;display:grid;grid-template-columns:1fr 1fr;background:#f4f4f4}img{width:100%}</style>'+''.join(f'<img src="screen-{i}.png">' for i in range(1,11)))
b=Browser();b.call('Emulation.setDeviceMetricsOverride',{'width':1680,'height':2780,'deviceScaleFactor':1,'mobile':False});b.call('Page.navigate',{'url':'http://127.0.0.1:8000/review/rendered.html'});time.sleep(.4);b.screenshot('review/rendered.png')
