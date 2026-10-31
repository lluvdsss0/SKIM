from browser import Browser
from pathlib import Path
import json,time
b=Browser();b.call('Page.navigate',{'url':'http://127.0.0.1:8000/?reference'});time.sleep(.4)
metrics=b.js('''(()=>{const c=document.createElement('canvas').getContext('2d'),out={};for(const [key,words] of Object.entries(PART_TWO_DATA.templates)){out[key]=words.map(w=>{const el=document.querySelector('.p2-font-'+w.font),s=getComputedStyle(el);c.font=s.fontStyle+' '+s.fontWeight+' 100px '+s.fontFamily;const m=c.measureText(w.text),size=w.h/(m.actualBoundingBoxAscent+m.actualBoundingBoxDescent)*100,scale=w.w/((m.actualBoundingBoxLeft+m.actualBoundingBoxRight)*size/100),baseline=(100-m.fontBoundingBoxAscent-m.fontBoundingBoxDescent)/2+m.fontBoundingBoxAscent;return {fontSize:size,inkTop:(baseline-m.actualBoundingBoxAscent)*size/100,inkLeft:m.actualBoundingBoxLeft*size/100*scale,inkScale:scale}})}return out})()''')
p=Path('part2-data.js');s=p.read_text(encoding='utf-8');data=json.loads(s[s.index('{'):s.rindex('}')+1])
for k,words in data['templates'].items():
 for w,m in zip(words,metrics[k]):w.update({k:round(v,4) for k,v in m.items()})
p.write_text('// Editable scene/state reference map. SVG files are never loaded by the site.\nwindow.PART_TWO_DATA = '+json.dumps(data,ensure_ascii=False,indent=2)+';\n',encoding='utf-8')
print('Stored glyph measurements for project fonts; canvas used only in this offline QA helper.')
