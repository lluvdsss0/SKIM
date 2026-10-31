from pathlib import Path
import xml.etree.ElementTree as E

def scene(n,key,travel,content,dark=False):
    return f'''\n<!-- Part II: {key} -->
<section id="screen-{n}" class="scene scene--extended part-two{' p2-night' if dark else ''}" data-scene="part2-{key}" data-part2="{key}" data-scroll-travel="{travel}" data-scroll-lead="0" aria-label="Продолжение: {key}"><div class="composition p2-canvas">
{content}
</div></section>\n'''

parts=[]
parts.append(scene(11,'words',.65,'<p class="p2-quote p2-fading-quote">Увидеть слова. Прочитать предложения. Удержать мысль.</p>'))
parts.append(scene(12,'notifications',1.35,'''
<h2 class="p2-top-heading">Проблема начинается раньше: в момент выбора</h2>
<p class="p2-notice-intro">В эксперименте 2015 года телефонные уведомления<br class="p2-desktop-br"> ухудшали выполнение задания на внимание, даже когда<br class="p2-desktop-br"> участники не брали телефон в руки. Иногда достаточно<br class="p2-desktop-br"> самого сигнала.</p>
<div class="p2-notices">
  <article class="p2-notice" data-notice="0" style="--nx:120;--ny:379;"><header><i class="p2-message-icon" aria-hidden="true"></i><span>MESSAGES</span><small>now</small></header><div class="p2-notice-body"><p>Вам может понравиться это видео.</p></div></article>
  <article class="p2-notice" data-notice="1" style="--nx:879;--ny:243;"><header><i class="p2-message-icon" aria-hidden="true"></i><span>MESSAGES</span><small>now</small></header><div class="p2-notice-body"><p>Ты здесь?</p></div></article>
  <article class="p2-notice" data-notice="2" style="--nx:120;--ny:616.09;"><header><i class="p2-message-icon" aria-hidden="true"></i><span>MESSAGES</span><small>now</small></header><div class="p2-notice-body"><p>Посмотри, это всего на минуту.</p></div></article>
  <article class="p2-notice" data-notice="3" style="--nx:879;--ny:481.09;"><header><i class="p2-message-icon" aria-hidden="true"></i><span>MESSAGES</span><small>now</small></header><div class="p2-notice-body"><p>Ты видел, что я скинула?</p></div></article>
</div>
<div class="p2-indicator" role="img" aria-label="Последовательность четырёх уведомлений"><i></i><i></i><i></i><i></i></div>
<p class="p2-notice-outro">Возможно, текст кажется неподъёмным ещё и потому,<br class="p2-desktop-br"> что ему постоянно приходится начинаться заново.</p>
'''))
parts.append(scene(13,'question',.65,'<p class="p2-quote p2-fading-quote">А твое внимание тоже подвластно отвлечениям?</p>',True))
parts.append(scene(14,'replies',1.5,'''
<div class="p2-reply-stack">
<p class="p2-quote p2-reply p2-reply--blue">Статья никуда не делась. Ты всё ещё хочешь разобраться.<br class="p2-desktop-br"> Но каждый раз что-нибудь оказывается срочнее.</p>
<p class="p2-quote p2-reply p2-reply--light">Сколько интересных тебе вещей так и осталось между<br class="p2-desktop-br"> «сохранить» и «когда-нибудь прочитать»?</p>
<p class="p2-quote p2-reply p2-reply--large">Разберусь потом.<br>А сейчас — что-нибудь попроще.</p>
</div>
''',True))
parts.append(scene(15,'try-reading',.65,'<p class="p2-quote p2-fading-quote">А если все-таки попробовать прочитать?</p>'))
parts.append(scene(16,'density',1.65,'<div class="p2-density" aria-label="Нарастающее наслаивание типографических блоков"></div>'))
parts.append(scene(17,'after-scroll',1.1,'''
<div class="p2-bg p2-bg--dark" aria-hidden="true"></div><div class="p2-bg p2-bg--light" aria-hidden="true"></div>
<p class="p2-quote p2-after-dark"><span>Слишком много всего. Мысли путаются, внимание скачет.</span><br><span>Подожди... </span><span class="p2-paper">О чём вообще был текст?</span></p>
<p class="p2-quote p2-after-light">А что останется после скролла?</p>
''',True))
parts.append(scene(18,'people',1.8,'''
<h2 class="p2-people-heading p2-people-heading--initial">Ты будешь такой, как все</h2>
<h2 class="p2-people-heading p2-people-heading--final">А если все-таки прочитать до конца?</h2>
<div class="p2-people-grid" role="img" aria-label="168 одинаковых людей; при завершении один человек выделяется голубым"></div>
<div class="p2-people-message-layer"></div>
'''))
footer='''
<footer class="p2-footer" id="skim-footer" aria-label="SKIM — завершение">
  <div class="p2-footer-content"><p>SKIM</p><img class="p2-footer-logo" data-logo="skim-mark" src="assets/skim-mark.svg" alt="Знак SKIM" width="81" height="81"></div>
</footer>
'''
p=Path('index.html');s=p.read_text(encoding='utf-8');assert 'data-part2=' not in s
s=s.replace('</main>',''.join(parts)+'</main>'+footer)
s=s.replace('<script src="script.js?v=scroll-linked-1" defer></script>','<script src="part2-data.js?v=1" defer></script>\n  <script src="part2.js?v=1" defer></script>\n  <script src="script.js?v=part-two-1" defer></script>')
s=s.replace('src="playback.js?v=scroll-linked-1"','src="playback.js?v=part-two-1"')
s=s.replace('<link rel="stylesheet" href="stylesheet/dome.css">','<link rel="stylesheet" href="stylesheet/dome.css">\n  <link rel="stylesheet" href="stylesheet/part2.css?v=1">')
p.write_text(s,encoding='utf-8')
# The sole graphic exception: extract only the pre-existing 81px logo, never a screen.
ns='http://www.w3.org/2000/svg';E.register_namespace('',ns)
source=E.parse('assets/Frame 78.svg').getroot();paths=list(source.iter('{'+ns+'}path'))
logo=E.Element('{'+ns+'}svg',{'viewBox':'799 1216.5 81 81','width':'81','height':'81','fill':'none'})
for path in paths[-2:]:logo.append(E.fromstring(E.tostring(path)))
Path('assets/skim-mark.svg').write_bytes(E.tostring(logo,encoding='utf-8',xml_declaration=True))
print('Added eight scenes and one footer. Original ten section bodies untouched.')
