import pathlib,xml.etree.ElementTree as E,json
p=pathlib.Path('review'); files=list(pathlib.Path('assets').glob('*.svg'))
html='<meta charset="utf-8"><body>'
for f in files:
 html+='<div data-file="'+f.name+'">'+f.read_text(encoding='utf-8')+'</div>'
html+='''<script>let out={};document.querySelectorAll('[data-file]').forEach(d=>{let a=[];function walk(n,depth){if(['defs','filter','mask','clipPath','pattern'].includes(n.tagName))return;let b;try{b=n.getBBox()}catch{};a.push({i:a.length,tag:n.tagName,depth,b:b?[b.x,b.y,b.width,b.height].map(x=>Math.round(x*10)/10):null,attrs:[...n.attributes].filter(a=>a.name!=='d').map(a=>[a.name,a.value]),start:n.getAttribute('d')?.slice(0,70)});[...n.children].forEach(c=>walk(c,depth+1))};walk(d.querySelector('svg'),0);out[d.dataset.file]=a});document.body.innerHTML='<pre>'+JSON.stringify(out)+'</pre>'</script>'''
p.joinpath('inspect.html').write_text(html,encoding='utf-8')
