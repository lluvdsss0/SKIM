from browser import Browser
from pathlib import Path
import time,json
b=Browser();b.call('Network.enable');b.call('Network.setCacheDisabled',{'cacheDisabled':True});b.call('Emulation.setDeviceMetricsOverride',{'width':1680,'height':1079,'deviceScaleFactor':1,'mobile':False});b.call('Page.navigate',{'url':'http://127.0.0.1:8000/review/part2-sources.html'});time.sleep(.1)
code='''(async()=>{const out={};for(let i=64;i<=78;i++){const xml=await(await fetch(`../assets/Frame ${i}.svg`)).text(),root=new DOMParser().parseFromString(xml,'image/svg+xml').documentElement;document.body.append(root);let a=[];function walk(n,depth){if(['defs','filter','mask','clipPath','pattern','linearGradient'].includes(n.tagName))return;let b;try{b=n.getBBox()}catch{};a.push({index:a.length,tag:n.tagName,depth,b:b?[b.x,b.y,b.width,b.height].map(x=>+x.toFixed(2)):null,attrs:Object.fromEntries([...n.attributes].filter(a=>a.name!=='d').map(a=>[a.name,a.value])),start:n.getAttribute('d')?.slice(0,90)});[...n.children].forEach(c=>walk(c,depth+1))}walk(root,0);out[i]=a;root.remove()}return out})()'''
d=b.js(code);Path('review/part2-geometry.json').write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
for i in [64,65,66,67,68,69,71,74,75,76,77,78]:
 print('\nFrame',i)
 for n in d[str(i)]:
  if n['depth']==2 and (i not in [76,78] or n['tag']!='path' or n['index']<6 or n['attrs'].get('fill') not in ['#090909','#161616','black']):print(n)
