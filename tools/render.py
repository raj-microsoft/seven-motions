from pathlib import Path
import subprocess,base64,math,struct,wave,random,json,concurrent.futures
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
NAMES=['one-line','one-ball','ascii','pixel','risograph','codex','ink']
EDGE=r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
def sound(k,dur,path):
 sr=44100;n=int(sr*dur);data=[0.0]*n;rng=random.Random(310+k);bpms=[110,128,124,140,100,72,48];beat=60/bpms[k]
 notes=[261.63,329.63,392,523.25,440,392,329.63,293.66];events=[]
 for j in range(int(dur/beat)+1):events.append((j*beat,notes[(j+k)%8],.5 if k!=6 else 2.8,.13))
 hits=[[0,1.5,3,4.5,6],[0,.4,.8,1.2,2.6,4,5.2,6.4],[0,1,3,4.5,5.5,7],[0,1.2,1.6,2,2.4,4,5.2,6.6],[0,1.5,3,4.5,6,7.5],[0,1.5,3.5,4.5,6.5],[0,3.5,4.5,7]][k]
 for at,f,length,vol in events:
  for j in range(min(int(length*sr),n-int(at*sr))):
   t=j/sr;env=math.exp(-t*(7 if k<6 else 1.5));a=math.sin(2*math.pi*f*t)
   if k==3:a=(1 if a>0 else -1)*.6+math.asin(math.sin(2*math.pi*f*.5*t))*.3
   elif k==1 or k==2:a=math.sin(2*math.pi*f*.25*t)*.7+math.sin(2*math.pi*f*t)*.2
   elif k==5:a+=.4*math.sin(2*math.pi*f*2*t)+.2*math.sin(2*math.pi*f*3*t)
   else:a+=.25*math.sin(2*math.pi*f*2.7*t)
   data[int(at*sr)+j]+=vol*a*env*min(1,t*120)
 for at in hits:
  length=.35 if k!=6 else 1.4
  for j in range(min(int(length*sr),n-int(at*sr))):
   t=j/sr;env=math.exp(-t*(18 if k!=6 else 3));noise=rng.uniform(-1,1);a=math.sin(2*math.pi*(100*t-60*t*t))
   data[int(at*sr)+j]+=.18*(a+.2*noise)*env
 if k in [0,4,5]:
  for i in range(n):data[i]+=rng.uniform(-1,1)*.014*(.5+.5*math.sin(i/sr*11))
 with wave.open(str(path),'wb') as w:
  w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes(b''.join(struct.pack('<h',int(max(-.95,min(.95,v))*32767)) for v in data))
def render(k):
 name=NAMES[k];dur=8 if k<4 else 9;folder=ROOT/'films'/name;tmp=ROOT/'.review'/name;tmp.mkdir(parents=True,exist_ok=True)
 sound(k,dur,tmp/'audio.wav')
 with sync_playwright() as pw:
  b=pw.chromium.launch(executable_path=EDGE,headless=True,args=['--disable-gpu']);page=b.new_page(viewport={'width':1080,'height':1920},device_scale_factor=1);page.goto((folder/'index.html').as_uri());page.wait_for_function('window.ready === true')
  cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','image2pipe','-vcodec','png','-r','30','-i','-','-an','-c:v','libx264','-preset','fast','-crf','25','-pix_fmt','yuv420p','-movflags','+faststart',str(tmp/'silent.mp4')]
  enc=subprocess.Popen(cmd,stdin=subprocess.PIPE);beats=[.4,2.2,4.2,6.8] if dur==8 else [.4,2.2,4.7,7.8];keys={round(t*30):j for j,t in enumerate(beats)}
  for f in range(dur*30):
   data=page.evaluate('(t)=>{seek(t);return document.querySelector("canvas").toDataURL("image/png").split(",")[1]}',f/30);raw=base64.b64decode(data);enc.stdin.write(raw)
   if f in keys:(tmp/f'beat-{keys[f]}.png').write_bytes(raw)
   if f==round((6.8 if k<4 else 7.5)*30):(folder/'poster.png').write_bytes(raw)
  enc.stdin.close();rc=enc.wait();assert rc==0
  # Seek purity: no dependence on previous calls.
  a=page.evaluate('()=>{seek(3);return document.querySelector("canvas").toDataURL()}');page.evaluate('seek(1)');bb=page.evaluate('()=>{seek(3);return document.querySelector("canvas").toDataURL()}');assert a==bb,(name,'nondeterministic');b.close()
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(tmp/'silent.mp4'),'-i',str(tmp/'audio.wav'),'-c:v','copy','-af','loudnorm=I=-14:TP=-1:LRA=11','-c:a','aac','-b:a','128k','-movflags','+faststart','-shortest',str(folder/'film.mp4')],check=True)
 sheet=Image.new('RGB',(1080,480))
 for j in range(4):sheet.paste(Image.open(tmp/f'beat-{j}.png').resize((270,480)),(j*270,0))
 sheet.save(folder/'contact-sheet.jpg',quality=90)
 Image.open(folder/'poster.png').convert('RGB').save(folder/'poster.jpg',quality=88);(folder/'poster.png').unlink()
 size=(folder/'film.mp4').stat().st_size;assert size<8*1024*1024,(name,size);print(name,'rendered',round(size/1024/1024,2),'MB; deterministic seek verified',flush=True)
 return {'name':name,'duration':dur,'bytes':size,'deterministic':True}
if __name__=='__main__':
 import sys
 ks=[int(x) for x in sys.argv[1:]] or list(range(7))
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:results=list(pool.map(render,ks))
 (ROOT/'.review'/'render-report.json').write_text(json.dumps(results,indent=2));print('DONE')
