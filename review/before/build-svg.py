"""Build the local, dependency-free page from the unchanged assets."""
from pathlib import Path
import xml.etree.ElementTree as E
import re, json

NS='http://www.w3.org/2000/svg'
E.register_namespace('',NS)
E.register_namespace('xlink','http://www.w3.org/1999/xlink')
def tag(n): return n.tag.split('}')[-1]
def el(t,**attrs): return E.Element('{'+NS+'}'+t,{k.replace('_','-'):str(v) for k,v in attrs.items()})
def walk(n):
    if tag(n) in ['defs','filter','mask','clipPath','pattern']: return []
    return [n]+[v for c in n for v in walk(c)]
def wrap(nodes,name):
    parent=next(p for p in root.iter() if nodes[0] in list(p))
    g=el('g',data_part=name); parent.insert(list(parent).index(nodes[0]),g)
    for n in nodes: parent.remove(n);g.append(n)
    return g

files=['Group 1063.svg']+['Frame '+str(n)+'.svg' for n in range(55,64)]
kinds=['cover','folders','scan','cards','phrase','reading','locks','dome','slider','final']
star=el('svg',viewBox='888 421 31 29',aria_hidden='true')
star.append(E.fromstring(E.tostring(walk(E.parse('assets/Frame 56.svg').getroot())[14])))
star_markup=E.tostring(star,encoding='unicode')
sections=[]
for i,(file,kind) in enumerate(zip(files,kinds)):
    root=E.parse(Path('assets')/file).getroot(); nodes=walk(root)
    root.set('preserveAspectRatio','xMidYMid meet');root.set('role','img');root.set('aria-label',f'SKIM — экран {i+1}')
    if kind=='folders':
        for a,b in [(15,17),(16,18)]:wrap([nodes[a],nodes[b]],'year')
        tape=wrap(nodes[19:33],'folder-tape')
        questions=['Как работает память?','Почему океан солёный?','Почему мы зеваем?','Откуда берётся молния?','Как животные находят дорогу домой?']
        for j,q in enumerate(questions):
            r=E.fromstring(E.tostring(nodes[19])); r.set('x',str(1470.5+173*j));tape.append(r)
            tx=el('text',x=1532.5+173*j,y=968,fill='#090909',font_family='Arial, sans-serif',font_size=14,text_anchor='middle')
            words=q.split(); lines=[];line=''
            for w in words:
                if len(line+' '+w)>19:lines.append(line);line=w
                else:line=(line+' '+w).strip()
            lines.append(line)
            for k,line in enumerate(lines):s=el('tspan',x=1532.5+173*j,dy=0 if k==0 else 17);s.text=line;tx.append(s)
            tape.append(tx)
        defs=root.find('{'+NS+'}defs');clip=el('clipPath',id='folder-area');clip.append(el('rect',x=250,y=825,width=1185,height=195));defs.append(clip)
        wrap([tape],'folder-clip').set('clip-path','url(#folder-area)')
    if kind=='scan':
        defs=root.find('{'+NS+'}defs');clip=el('clipPath',id='scan-area');clip.append(el('rect',x=124,y=405,width=712,height=610));defs.append(clip)
        for j,n in enumerate([nodes[22],nodes[49]]):
            g=wrap([n],'scanner');g.set('data-direction',str(1 if j else -1));outer=wrap([g],'scanner-clip');outer.set('clip-path','url(#scan-area)')
    if kind=='cards':
        groups=[[3,4,7,8,9],[11,12,13,14],[15,17,18,19],[20,21,22,23],[24,25,26,29,30,31],[32,34,35,36],[37,38,39,40]]
        for j,ids in enumerate(groups):wrap([nodes[n] for n in ids],'card').set('data-order',str(j))
    if kind=='phrase':nodes[3].set('data-part','phrase')
    if kind=='reading':
        nodes[5].set('data-part','read-bar');nodes[9].set('display','none')
        nodes[15].set('data-part','read-copy')
    if kind=='locks':
        for n in range(22,34,2):wrap([nodes[n],nodes[n+1]],'lock')
    if kind=='dome':
        nodes[11].set('data-part','dome-shape')
        defs=root.find('{'+NS+'}defs');clip=el('clipPath',id='dome-area');shape=E.fromstring(E.tostring(nodes[11]));shape.attrib.pop('data-part',None);clip.append(shape);defs.append(clip)
        for n in range(15,32):
            g=wrap([nodes[n]],'symbol');outer=wrap([g],'symbol-clip');outer.set('clip-path','url(#dome-area)')
    if kind=='slider':
        nodes[6].set('data-part','original-copy');wrap([nodes[9],nodes[11]],'size-thumb')
    if kind=='final':
        for n in [15,16,77]+list(range(78,106)):nodes[n].set('data-part','arrows')
        for n in [12]+list(range(106,137,3)):wrap([nodes[n],nodes[n+2]],'star')
    # Prefix every ID and every fragment reference in all attributes and styles.
    ids={n.get('id'):f's{i+1}-{n.get("id")}' for n in root.iter() if n.get('id')}
    for n in root.iter():
        for key,value in list(n.attrib.items()):
            if key=='id':n.set(key,ids[value]);continue
            value=re.sub(r'#([\w.-]+)',lambda m:'#'+ids.get(m[1],m[1]),value);n.set(key,value)
        if tag(n)=='style' and n.text:n.text=re.sub(r'#([\w.-]+)',lambda m:'#'+ids.get(m[1],m[1]),n.text)
    extra=''
    if kind=='cover':extra='<div class="info"><button aria-label="Значение SKIM" aria-expanded="false" aria-describedby="definition">'+star_markup+'</button><div id="definition" role="tooltip"><strong>Бегло просматривать</strong><small>eng idiom</small></div></div><button class="learn">Изучить <span aria-hidden="true">→</span></button>'
    if kind=='dome':extra='<button class="break hit" aria-label="Сломать"></button>'
    if kind=='slider':extra='<div class="dynamic-copy" aria-label="Текст с изменяемым размером"></div><input class="size-range" aria-label="Размер текста" type="range" min="10" max="38" step="1" value="10">'
    sections.append(f'<section id="screen-{i+1}" class="screen" data-kind="{kind}" aria-label="Экран {i+1}"><div class="stage">'+E.tostring(root,encoding='unicode')+extra+'</div></section>')
Path('index.html').write_text('<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="SKIM — интерактивный лонгрид о чтении и коротком контенте"><title>SKIM — как мы читаем</title><link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 32 32%27%3E%3Crect width=%2732%27 height=%2732%27 rx=%278%27 fill=%27%2378B7F3%27/%3E%3Ctext x=%276%27 y=%2725%27 font-size=%2727%27%3ES%3C/text%3E%3C/svg%3E"><link rel="stylesheet" href="stylesheet/skim.css"></head><body><a class="skip" href="#screen-2">К содержанию</a><main>'+''.join(sections)+'</main><noscript>Для интерактивных элементов включите JavaScript. Все исходные композиции доступны ниже.</noscript><script src="script.js"></script></body></html>',encoding='utf-8')
print('Built 10 inline SVG screens: index.html')
