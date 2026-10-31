import pathlib,xml.etree.ElementTree as E
E.register_namespace('','http://www.w3.org/2000/svg'); t=E.parse('assets/Frame 62.svg'); r=t.getroot();r.set('viewBox','290 310 1100 460');r.set('width','2200');r.set('height','920');pathlib.Path('review/text.svg').write_bytes(E.tostring(r));pathlib.Path('review/text.html').write_text('<style>body{margin:0}</style><img src="text.svg">')
