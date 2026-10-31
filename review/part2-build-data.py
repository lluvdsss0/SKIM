"""Read-only reference measurements → editable HTML component data (no SVG paths)."""
from pathlib import Path
import json
g=json.loads(Path('review/part2-geometry.json').read_text(encoding='utf-8'))

def part(text,font,x,y,w,h):return dict(text=text,font=font,x=x,y=y,w=w,h=h)
templates={
 'unexpected':[part('unexpected','italic',15.38,4.02,305.62,76.25),part('moments','condensed',333.59,6.46,303.95,63.54),part('combinations','times',651.54,6.02,413.20,58.86)],
 'observations':[part('and','sans',19.13,1.16,127.13,61.95),part('observations','italic',296.75,4.02,340.52,59.02)],
 'experiments':[part('experiments','sans',14.94,4.45,383.71,72.36)],
 'perspectives':[part('new','condensed',-7.41,15.4,147.33,55.6),part('perspectives','sans-heavy',157.09,7.45,393.01,72.36),part('collection','italic',564.27,6.02,255.93,59.01)],
 'culture':[part('contemporary','sans',9.94,7.86,439.72,69.66),part('culture','heavy',461.65,.16,240.13,61.95)],
 'visual':[part('of','sans',14.34,5.22,68.65,59.81),part('visual','condensed',160.59,-11.02,175.84,81.02)],
 'moments':[part('moments','condensed',41.59,9.46,303.95,63.54)],
 'small':[part('from','heavy',17.26,1.89,170.12,63.22),part('small','sans',303.54,10.45,158.33,57.82)],
 'and-new':[part('and','sans',14.13,5.16,127.13,61.95),part('new','condensed',155.59,9.4,147.33,55.6),part('perspectives','sans-heavy',320.08,5.45,393.02,72.36),part('collection','italic',727.27,9.02,255.93,59.02)],
 'built':[part('is','slender',8,-28,34.8,117.74),part('built','italic',201.03,10.02,135.16,59.01)],
 'fragments':[part('fragments','condensed',11.59,-15.85,327.78,113.58),part('and','sans',385.13,3.16,127.13,61.95),part('observations','italic',556.75,6.02,340.52,59.02)],
 'visual-built':[part('experiments','sans',12.94,5.45,383.71,72.36),part('of','sans',437.33,11.22,68.65,59.81),part('visual','condensed',514.59,-5.02,175.84,81.02),part('built','italic',751.03,13.02,135.16,59.01)]
}
# Identity is the rectangle and its orientation, not a complete screenshot layer.
def type_for(b):
 x,y,w,h=b;size=round(max(w,h))
 if size==1075:return 'unexpected'
 if size==666:return 'observations'
 if size==415:return 'experiments'
 if size==826:return 'perspectives'
 if size==710:return 'culture'
 if size==388:return 'moments'
 if size==487:return 'small'
 if size==995:return 'and-new'
 if size==345:return 'built' if (x,y) in [(485,243),(118,908)] else 'visual'
 if size==906:return 'fragments' if x==120 else 'visual-built'
 raise ValueError(b)
def angle_for(b,kind):
 x,y,w,h=b
 if h<=w:return 0
 if kind in ['experiments','visual','small']:return 90
 if kind=='culture':return -90
 if kind=='perspectives':return 90 if x==1337 else -90
 return -90
objects={};stages=[]
for stage,f in enumerate([70,72,73]):
 nodes=g[str(f)];keys=[]
 for n in nodes:
  if n['depth']!=2 or n['tag']!='g' or 'filter' not in n['attrs']:continue
  child=nodes[n['index']+1];is_star=child['tag']=='circle';b=n['b'];key=('star' if is_star else 'card')+':'+','.join(str(v) for v in b)
  keys.append(key)
  if key not in objects:
   kind=None if is_star else type_for(b)
   objects[key]={'id':'p2-object-'+str(len(objects)),'kind':'star' if is_star else 'card','box':b,'template':kind,'angle':0 if is_star else angle_for(b,kind),'stage':stage,'z':[0,0,0],'refs':[]}
  objects[key]['z'][stage]=n['index'];objects[key]['refs'].append(f'assets/Frame {f}.svg')
 stages.append(keys)
assert [sum(objects[k]['kind']=='card' for k in keys) for keys in stages]==[13,17,27]
assert [sum(objects[k]['kind']=='star' for k in keys) for keys in stages]==[5,9,20]
people=[n['b'] for n in g['76'] if n['tag']=='path' and n['attrs'].get('fill')=='black']
selected=next(i for i,b in enumerate(people) if abs(b[0]-842.31)<.1 and b[1]==536)
data={
 'sequence':[
  {'id':'words','sources':['assets/Frame 64.svg'],'travel':.65},
  {'id':'notifications','sources':['assets/Frame 65.svg'],'travel':1.35},
  {'id':'question','sources':['assets/Frame 66.svg'],'travel':.65},
  {'id':'replies','sources':[f'assets/Frame {i}.svg' for i in [67,68,69]],'travel':1.5},
  {'id':'try-reading','sources':['assets/Frame 71.svg'],'travel':.65},
  {'id':'density','sources':[f'assets/Frame {i}.svg' for i in [70,72,73]],'travel':1.65},
  {'id':'after-scroll','sources':[f'assets/Frame {i}.svg' for i in [74,75]],'travel':1.1},
  {'id':'people','sources':[f'assets/Frame {i}.svg' for i in [76,77,78]],'travel':1.8}
 ],
 'templates':templates,'objects':list(objects.values()),'people':people,'selectedPerson':selected,
 'messages':[
  {'box':[110,191,367,124],'text':'Одинаковые знания'},
  {'box':[556,514,397,124],'text':'Одинаковые интересы'},
  {'box':[706,837,327,124],'text':'Все одинаковые'},
  {'box':[1243,398,327,124],'text':'Все одинаковые'},
  {'box':[110,622,327,124],'text':'Все одинаковые'},
  {'box':[934,191,380,124],'text':'Одинаковые взгляды'},
  {'box':[110,837,462,124],'text':'Одинаковое мировоззрение'},
  {'box':[1171,840,399,124],'text':'Одинаковые суждения'}
 ]}
Path('part2-data.js').write_text('// Editable scene/state reference map. SVG files are never loaded by the site.\nwindow.PART_TWO_DATA = '+json.dumps(data,ensure_ascii=False,indent=2)+';\n',encoding='utf-8')
print('Union:',len(objects),'objects;',len(people),'people; selected index',selected)
