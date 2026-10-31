import pathlib,xml.etree.ElementTree as E,json
out=[]
for i in range(64,79):
 f=pathlib.Path(f'assets/Frame {i}.svg');r=E.parse(f).getroot();counts={}
 for n in r.iter():
  tag=n.tag.split('}')[-1];counts[tag]=counts.get(tag,0)+1
 out.append({'file':f.name,'dimensions':[r.get('width'),r.get('height')],'viewBox':r.get('viewBox'),'counts':counts})
pathlib.Path('review/part2-inventory.json').write_text(json.dumps(out,indent=2))
pathlib.Path('review/part2-sources.html').write_text('<meta charset="utf-8"><style>body{margin:0;display:grid;grid-template-columns:1fr 1fr;background:#ddd}figure{margin:0}img{width:100%;display:block}figcaption{font:20px Arial}</style>'+''.join(f'<figure><figcaption>Frame {i}.svg</figcaption><img src="../assets/Frame {i}.svg"></figure>' for i in range(64,79)))
print(json.dumps(out))
