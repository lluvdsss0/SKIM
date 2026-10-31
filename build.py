"""Validate the editable, buildless HTML page. No SVG generation."""
from html.parser import HTMLParser
from pathlib import Path
import re
class Check(HTMLParser):
    def __init__(self):
        super().__init__();self.errors=[];self.sections=0;self.footers=0;self.ids=[]
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        logo=tag=='img' and attrs.get('data-logo')=='skim-mark' and attrs.get('src')=='assets/skim-mark.svg'
        if tag in {'svg','path','img','canvas','object','embed','iframe'} and not logo:
            self.errors.append('Forbidden interface element: '+tag)
        if tag=='section':self.sections+=1
        if tag=='footer':self.footers+=1
        if 'id' in attrs:self.ids.append(attrs['id'])
        for key,value in attrs.items():
            if value and ('.svg' in value.lower() or 'data:image' in value.lower()) and not logo:
                self.errors.append('Graphic reference: '+value[:80])
check=Check();check.feed(Path('index.html').read_text(encoding='utf-8'))
assert check.sections==18,check.sections
assert check.footers==1,check.footers
assert len(check.ids)==len(set(check.ids)),'Duplicate IDs'
for name in ['stylesheet/skim.css','stylesheet/dome.css','script.js','geometry.js','playback.js','interactions.js','stylesheet/revision.css','stylesheet/part2.css','part2.js']:
    text=Path(name).read_text(encoding='utf-8-sig')
    assert not re.search(r'url\([^)]*\.svg|data:image|createElementNS|createElement\([\x27\x22]canvas',text,re.I),name
assert not check.errors,check.errors
print('PASS: 18 HTML sections, one footer, unique IDs; only the small SKIM logo uses SVG.')
