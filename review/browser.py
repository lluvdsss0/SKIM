"""Small Chrome DevTools client for local QA (Python standard library only)."""
import json,socket,urllib.request,urllib.parse,base64,os,struct,time
class Browser:
 def __init__(self):
  pages=json.load(urllib.request.urlopen('http://127.0.0.1:9222/json'))
  page=next(p for p in pages if p['type']=='page')
  u=urllib.parse.urlparse(page['webSocketDebuggerUrl']);self.s=socket.create_connection((u.hostname,u.port));self.s.settimeout(20)
  key=base64.b64encode(os.urandom(16)).decode();self.s.sendall(f'GET {u.path} HTTP/1.1\r\nHost: {u.netloc}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n'.encode());header=b''
  while not header.endswith(b'\r\n\r\n'):header+=self.s.recv(1)
  self.i=0;self.events=[]
 def read(self,n):
  b=b''
  while len(b)<n:b+=self.s.recv(n-len(b))
  return b
 def call(self,method,params={}):
  self.i+=1;raw=json.dumps({'id':self.i,'method':method,'params':params}).encode();mask=os.urandom(4);size=len(raw)
  head=bytes([129,128|size]) if size<126 else bytes([129,254])+struct.pack('!H',size) if size<65536 else bytes([129,255])+struct.pack('!Q',size)
  self.s.sendall(head+mask+bytes(c^mask[i%4] for i,c in enumerate(raw)))
  while True:
   a,b=self.read(2);n=b&127
   if n==126:n=struct.unpack('!H',self.read(2))[0]
   elif n==127:n=struct.unpack('!Q',self.read(8))[0]
   msg=json.loads(self.read(n))
   if msg.get('id')==self.i:
    if 'error' in msg:raise RuntimeError(msg)
    return msg.get('result')
   self.events.append(msg)
 def js(self,expression):
  r=self.call('Runtime.evaluate',{'expression':expression,'returnByValue':True,'awaitPromise':True})
  if 'exceptionDetails' in r:raise RuntimeError(r)
  return r.get('result',{}).get('value')
 def screenshot(self,path):
  r=self.call('Page.captureScreenshot',{'format':'png','captureBeyondViewport':False});open(path,'wb').write(base64.b64decode(r['data']))
if __name__=='__main__':
 b=Browser();print(b.js('({title:document.title,ready:!!window.SKIM})'))
