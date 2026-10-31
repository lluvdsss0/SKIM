from pathlib import Path
p=Path('part2.js');s=p.read_text(encoding='utf-8');s=s.replace("w.style.setProperty('--wx',word.x);w.style.setProperty('--wy',word.y);w.style.setProperty('--font-size',word.h*1.22);w.dataset.targetWidth=word.w;", "w.style.setProperty('--wx',word.x+(word.inkLeft||0));w.style.setProperty('--wy',word.y-(word.inkTop||0));w.style.setProperty('--font-size',word.fontSize||word.h*1.22);w.style.transform=`scaleX(${word.inkScale||1})`;")
s=s.replace("  for(const w of density.querySelectorAll('.p2-strip-word')){w.style.transform='none';const u=density.clientWidth/1680,width=w.offsetWidth;w.style.transform=`scaleX(${+w.dataset.targetWidth*u/Math.max(1,width)})`}\n",'')
p.write_text(s,encoding='utf-8')
