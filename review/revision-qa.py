from browser import Browser
from pathlib import Path
import time,json
b=Browser();b.call('Runtime.enable');b.call('Log.enable');b.call('Emulation.setTouchEmulationEnabled',{'enabled':False});b.call('Emulation.setDeviceMetricsOverride',{'width':1680,'height':1079,'deviceScaleFactor':1,'mobile':False})
out={}
def js(s):return b.js(s)
def fresh():
 b.call('Page.navigate',{'url':'http://127.0.0.1:8000/'});time.sleep(.22)
def go(i,offset=0):
 js(f'scrollTo(0,document.querySelectorAll(".scene")[{i}].offsetTop+({offset}));SKIM.render()');time.sleep(.04)
def active():return js('SKIM.playback.active?.index ?? null')
def wheel(d):b.call('Input.dispatchMouseEvent',{'type':'mouseWheel','x':800,'y':500,'deltaX':0,'deltaY':d})
fresh();go(1,-inner if False else -300);start=time.monotonic();time.sleep(.16)
out['hold_begins_on_entry']=active()==1
out['animation_without_extra_gesture']=js('document.querySelector(".folder-tape").style.transform!=="translateX(0px)"')
for _ in range(10):wheel(250);time.sleep(.025)
out['one_start_despite_wheels']=js('SKIM.playback.states[1].starts')
while time.monotonic()-start<3.15:time.sleep(.08)
out['hold_released_at_3s']=active() is None
y=js('scrollY');time.sleep(.2);out['no_queued_scroll_or_auto_advance']=abs(js('scrollY')-y)<1
out['held_at_section_anchor']=js('Math.abs(scrollY-document.querySelectorAll(".scene")[1].offsetTop)<2')
wheel(400);time.sleep(.15);out['new_intent_moves_page']=js('scrollY')>y+150
go(1);out['return_no_hold']=active() is None and js('SKIM.playback.states[1].starts')==1

fresh();go(2);samples=[];states=[];start=time.monotonic()
while time.monotonic()-start<3.12:
 samples.append(js('''(()=>{const p=document.querySelector('.scan-panel--left').getBoundingClientRect(),white=[...document.querySelectorAll('.white-block')].map(n=>n.getBoundingClientRect()),black=[...document.querySelectorAll('.scanner')].map(n=>n.getBoundingClientRect());const overlap=(a,b)=>Math.min(a.right,b.right)>Math.max(a.left,b.left)+.2&&Math.min(a.bottom,b.bottom)>Math.max(a.top,b.top)+.2;return {safe:!white.some(a=>black.some(b=>overlap(a,b))),inside:[...white,...black].every(r=>r.left>=p.left-.2&&r.right<=p.right+.2&&r.top>=p.top-.2&&r.bottom<=p.bottom+.2),x:black[0].x,y:white[0].y}})()'''))
 states.append(js('[...document.querySelectorAll(".scan-line")].map(n=>+n.style.getPropertyValue("--y"))'));time.sleep(.10)
out['scan_safe_all_samples']=all(s['safe'] and s['inside'] for s in samples)
out['scan_black_and_white_move']=max(s['x'] for s in samples)-min(s['x'] for s in samples)>100 and max(s['y'] for s in samples)-min(s['y'] for s in samples)>20
out['right_discrete_states']=len({tuple(s) for s in states})>=4 and all(all(y in [42+47*i for i in range(13)] for y in s) for s in states)
out['scan_back_to_origin']=js('[...document.querySelectorAll(".scanner,.white-block")].every(n=>parseFloat(n.style.transform.match(/[-.\\d]+/)?.[0]||0)===0)')
js('document.querySelector(".scan-star").focus()');time.sleep(.2);out['scan_tip']=js('document.querySelector(".floating-tooltip").textContent.startsWith("Привыкнув скользить")')

fresh();go(4);start=time.monotonic();phrase=[]
for target in [.08,.65,1.5,2.6,3.12]:
 while time.monotonic()-start<target:time.sleep(.02)
 phrase.append(float(js('getComputedStyle(document.querySelector(".revealing-phrase")).opacity')))
out['phrase_samples']=phrase

fresh();go(5)
geometry=js('[...document.querySelectorAll(".reading-word")].map(n=>{const r=n.getBoundingClientRect();return[r.x,r.y,r.width,r.height]})')
colors=js('[...document.querySelectorAll(".reading-word")].map(n=>getComputedStyle(n).color)')
time.sleep(3.12)
out['bold_keeps_geometry']=geometry==js('[...document.querySelectorAll(".reading-word")].map(n=>{const r=n.getBoundingClientRect();return[r.x,r.y,r.width,r.height]})')
out['bold_keeps_color']=colors==js('[...document.querySelectorAll(".reading-word")].map(n=>getComputedStyle(n).color)')
out['bold_and_fill']=js('({bold:document.querySelectorAll(".is-read").length,total:SKIM.readingWords.length,weight:getComputedStyle(document.querySelector(".word-bold")).fontWeight,width:document.querySelector(".read-runner").getBoundingClientRect().width/document.querySelector(".read-track").clientWidth,left:document.querySelector(".read-runner").getBoundingClientRect().left-document.querySelector(".read-track").getBoundingClientRect().left,counter:document.querySelector(".counter-tape").style.transform})')

fresh();go(6);messages=[]
for i in range(6):
 js(f'document.querySelectorAll(".lock-badge")[{i}].click()');messages.append(js('document.querySelector(".distraction-toast span").textContent'))
out['all_locks_notifications']=len(messages)==6 and all(messages[i]!=messages[i-1] for i in range(1,6))
out['notifications_dont_restart_hold']=js('SKIM.playback.states[6].starts')==1
js('document.dispatchEvent(new KeyboardEvent("keydown",{key:"Escape",bubbles:true}))');out['notification_escape']=js('document.querySelector(".distraction-toast").hidden')

fresh();go(8);js('document.querySelector("#text-size").focus()');b.call('Input.dispatchKeyEvent',{'type':'keyDown','key':'End','code':'End'});b.call('Input.dispatchKeyEvent',{'type':'keyUp','key':'End','code':'End'})
out['manual_slider_during_hold']=js('({value:document.querySelector("#text-size").value,active:SKIM.playback.active?.index,starts:SKIM.playback.states[8].starts})')

fresh();go(9,-320);time.sleep(.5)
out['final_partial_words_only']=js('({active:SKIM.playback.active?.index??null,arrows:getComputedStyle(document.querySelector(".collage-arrows")).opacity,stars:getComputedStyle(document.querySelector(".collage-stars")).opacity})')
go(9);start=time.monotonic();phases=[]
for target in [.28,.85,1.8,3.12]:
 while time.monotonic()-start<target:time.sleep(.025)
 phases.append(js('({active:SKIM.playback.active?.index??null,arrows:+getComputedStyle(document.querySelector(".collage-arrows")).opacity,stars:+getComputedStyle(document.querySelector(".collage-stars")).opacity})'))
out['final_timeline']=phases
translations=[]
for i in range(12):
 js(f'document.querySelector("[data-tooltip-key=final-{i}]").focus()');translations.append(js('document.querySelector(".floating-tooltip").textContent'))
out['unique_translations']=len(set(translations))==12
out['translation_examples']=[translations[0],translations[10]]
out['tip_in_viewport']=js('(()=>{const r=document.querySelector(".floating-tooltip").getBoundingClientRect();return r.left>=0&&r.right<=innerWidth&&r.top>=0&&r.bottom<=innerHeight})()')
b.call('Emulation.setEmulatedMedia',{'features':[{'name':'prefers-reduced-motion','value':'reduce'}]});go(2);out['reduced_no_hold']=active() is None
out['errors']=[e for e in b.events if e.get('method')=='Runtime.exceptionThrown' or e.get('method')=='Log.entryAdded' and e['params']['entry']['level']=='error']
Path('review/revision-qa.json').write_text(json.dumps(out,indent=2),encoding='utf-8');print(json.dumps(out))
