import json,pathlib,html
s=pathlib.Path('review/bounds.html').read_text(encoding='utf-8-sig'); data=json.loads(html.unescape(s[s.index('<pre>')+5:s.index('</pre>')]))
pathlib.Path('review/bounds.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
for f,items in data.items():
 print('\n'+f)
 for n in items:
  if n['depth']<3 or f in ['Frame 61.svg','Frame 62.svg','Frame 60.svg']: print(n)
