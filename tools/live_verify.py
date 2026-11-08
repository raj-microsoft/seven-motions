from pathlib import Path
import urllib.request,time,subprocess,json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];url='https://raj-microsoft.github.io/seven-motions/';EDGE=r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
for attempt in range(24):
 try:
  with urllib.request.urlopen(url,timeout=20) as r:
   if r.status==200:print('LIVE HTTP 200',flush=True);break
 except Exception as e:print('Pages pending',attempt+1,flush=True)
 time.sleep(10)
else:raise RuntimeError('Pages did not return HTTP 200 within four minutes')
for width,height in [(1440,1000),(390,844)]:
 cmd=[EDGE,'--headless=new','--disable-gpu','--no-first-run','--hide-scrollbars','--force-prefers-reduced-motion','--window-size='+str(width)+','+str(height),'--screenshot='+str(ROOT/'.review'/f'live-edge-{width}.png'),'--virtual-time-budget=7000',url]
 subprocess.run(cmd,check=True,timeout=90,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path=EDGE,headless=True);p=b.new_page(viewport={'width':390,'height':844},reduced_motion='reduce');errs=[];p.on('pageerror',lambda e:errs.append(str(e)));p.goto(url);p.wait_for_timeout(1500);p.screenshot(path=str(ROOT/'.review'/'live-viewport-390.png'));assert p.locator('.room').count()==7;assert p.evaluate('document.documentElement.scrollWidth <= innerWidth');assert p.evaluate('Array.from(document.querySelectorAll("video")).every(v=>v.paused&&v.muted)');p.locator('.play').first.click();p.wait_for_timeout(2000);assert p.locator('video').first.evaluate('(v)=>v.currentTime>0&&!v.paused');p.locator('.sound').first.click();assert p.locator('video').first.evaluate('(v)=>!v.muted');p.locator('.play').first.click();assert not errs,errs
 for name in ['one-line','one-ball','ascii','pixel','risograph','codex','ink']:
  r=p.request.get(url+'films/'+name+'/film.mp4');assert r.status==200;print(name,'MP4 HTTP 200',flush=True)
 b.close()
print('Live Edge screenshots and playback/reduced-motion checks passed.',flush=True)
