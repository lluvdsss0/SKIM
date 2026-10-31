from browser import Browser
import time,json
b=Browser();b.call('Runtime.enable');b.call('Page.navigate',{'url':'http://127.0.0.1:8000/'});time.sleep(.3)
b.call('Emulation.setDeviceMetricsOverride',{'width':1680,'height':1079,'deviceScaleFactor':1,'mobile':False})
r={}
def js(s):return b.js(s)
# Keyboard operates the actual native controls.
js('document.querySelector(".info button").focus()');time.sleep(.3);r['keyboard_tooltip']=js('getComputedStyle(document.querySelector("[role=tooltip]")).visibility')
js('document.querySelector(".size-range").focus()');b.call('Input.dispatchKeyEvent',{'type':'keyDown','key':'End','code':'End'});b.call('Input.dispatchKeyEvent',{'type':'keyUp','key':'End','code':'End'});time.sleep(.1);r['keyboard_slider_end']=js('document.querySelector(".size-range").value')
b.call('Input.dispatchKeyEvent',{'type':'keyDown','key':'Home','code':'Home'});b.call('Input.dispatchKeyEvent',{'type':'keyUp','key':'Home','code':'Home'});r['keyboard_slider_home']=js('document.querySelector(".size-range").value')
# Direct and reverse scroll to identical coordinates must yield identical states.
js('document.activeElement.blur();scrollTo(0,0)');time.sleep(.1)
a=js('JSON.stringify([...document.querySelectorAll("[data-kind=cover] [data-part]")].map(n=>[n.getAttribute("transform"),n.style.opacity]))')
js('scrollTo(0,document.documentElement.scrollHeight)');time.sleep(.05);js('scrollTo(0,0)');time.sleep(.05)
c=js('JSON.stringify([...document.querySelectorAll("[data-kind=cover] [data-part]")].map(n=>[n.getAttribute("transform"),n.style.opacity]))');r['reverse_cover_state']=a==c
# Compare a fully visible scanning scene before and after jumping beyond it.
js('scrollTo(0,document.querySelectorAll(".screen")[2].offsetTop)');time.sleep(.05);a=js('[...document.querySelectorAll("[data-part=scanner]")].map(n=>n.getAttribute("transform"))');js('scrollTo(0,document.documentElement.scrollHeight)');time.sleep(.05);js('scrollTo(0,document.querySelectorAll(".screen")[2].offsetTop)');time.sleep(.05);r['reverse_scanner_state']=a==js('[...document.querySelectorAll("[data-part=scanner]")].map(n=>n.getAttribute("transform"))')
# New wheel input cancels an active correction immediately.
js('scrollTo(0,document.querySelectorAll(".screen")[1].offsetTop-55)');time.sleep(.20)
b.call('Input.dispatchMouseEvent',{'type':'mouseWheel','x':800,'y':500,'deltaX':0,'deltaY':400});time.sleep(.5);r['wheel_cancels_snap']=js('scrollY>document.querySelectorAll(".screen")[1].offsetTop+100')
b.call('Emulation.setEmulatedMedia',{'features':[{'name':'prefers-reduced-motion','value':'reduce'}]});js('scrollTo(0,document.querySelectorAll(".screen")[3].offsetTop)');time.sleep(.1);r['reduced_motion']=js('({animation:getComputedStyle(document.querySelector("[data-part=year]")).animationName,cardOpacity:document.querySelector("[data-part=card]").style.opacity})')
b.call('Emulation.setEmulatedMedia',{'features':[]});js('scrollTo(0,0)');time.sleep(.1);b.screenshot('review/cover.png')
# Mobile screenshot at the actual slider position, after resize.
b.call('Emulation.setDeviceMetricsOverride',{'width':390,'height':844,'deviceScaleFactor':1,'mobile':False});js('scrollTo(0,document.querySelectorAll(".screen")[8].offsetTop)');time.sleep(.1);b.screenshot('review/mobile.png')
r['errors']=[e for e in b.events if e.get('method')=='Runtime.exceptionThrown'];open('review/scroll-keyboard.json','w').write(json.dumps(r,indent=2));print(r)
