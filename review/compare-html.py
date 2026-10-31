"""Offline screenshot comparison. Canvas is used ONLY on the QA page."""
from pathlib import Path
from browser import Browser
import json,time,base64
Path('review/after/compare.html').write_text('<meta charset="utf-8"><style>body{margin:0}canvas{display:block}</style><canvas width="1680" height="1079"></canvas>')
b=Browser();b.call('Emulation.setDeviceMetricsOverride',{'width':1680,'height':1079,'deviceScaleFactor':1,'mobile':False})
b.call('Page.navigate',{'url':'http://127.0.0.1:8000/review/after/compare.html'});time.sleep(.1)
results=[]
for i in range(1,11):
 code='''(async()=>{const index=INDEX,canvas=document.querySelector('canvas'),ctx=canvas.getContext('2d',{willReadFrequently:true});const before=new Image(),after=new Image();before.src=`../before/screen-${index}.png`;after.src=`screen-${index}.png`;await Promise.all([before.decode(),after.decode()]);ctx.drawImage(before,0,0);const a=ctx.getImageData(0,0,1680,1079).data;ctx.drawImage(after,0,0);const b=ctx.getImageData(0,0,1680,1079).data;let difference=0,changed=0;for(let k=0;k<a.length;k+=4){const d=Math.max(Math.abs(a[k]-b[k]),Math.abs(a[k+1]-b[k+1]),Math.abs(a[k+2]-b[k+2]));difference+=Math.abs(a[k]-b[k])+Math.abs(a[k+1]-b[k+1])+Math.abs(a[k+2]-b[k+2]);if(d>32)changed++}ctx.clearRect(0,0,1680,1079);ctx.globalAlpha=1;ctx.drawImage(before,0,0);ctx.globalAlpha=.5;ctx.drawImage(after,0,0);ctx.globalAlpha=1;return{screen:index,meanAbsoluteRgbDifference:difference/(1680*1079*3),pixelsChangedOver32Percent:100*changed/(1680*1079)}})()'''.replace('INDEX',str(i))
 results.append(b.js(code));b.screenshot(f'review/after/overlay-{i}.png')
Path('review/after/comparison.json').write_text(json.dumps(results,indent=2))
print(json.dumps(results))
