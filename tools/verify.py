from pathlib import Path
from playwright.sync_api import sync_playwright
import json,subprocess
ROOT=Path(__file__).resolve().parents[1];EDGE=r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path=EDGE,headless=True)
 errors=[];results={}
 for width in [1440,390]:
  p=b.new_page(viewport={'width':width,'height':1000 if width==1440 else 844},reduced_motion='reduce');p.on('pageerror',lambda e:errors.append(str(e)));p.goto((ROOT/'index.html').as_uri());p.wait_for_timeout(1200);p.screenshot(path=str(ROOT/'.review'/f'desktop-{width}.png'));assert p.locator('.room').count()==7
  assert p.evaluate('document.documentElement.scrollWidth <= innerWidth'), 'horizontal overflow'
  assert p.evaluate('Array.from(document.querySelectorAll("video")).every(v=>v.paused && v.muted)'), 'reduced motion or sound violation'
  for i in [3,4,6]:p.locator('.room').nth(i).scroll_into_view_if_needed();p.screenshot(path=str(ROOT/'.review'/f'room-{i+1}-{width}.png'))
  p.locator('.room').first.scroll_into_view_if_needed();p.locator('.play').first.click();p.wait_for_timeout(500);assert p.locator('video').first.evaluate('(v)=>!v.paused');p.locator('.sound').first.click();assert p.locator('video').first.evaluate('(v)=>!v.muted');p.locator('.play').first.click();assert p.locator('video').first.evaluate('(v)=>v.paused')
  results[str(width)]={'rooms':7,'noOverflow':True,'reducedMotion':True,'playPauseSound':True};p.close()
 b.close()
assert not errors,errors
for folder in (ROOT/'films').iterdir():
 if not folder.is_dir():continue
 data=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(folder/'film.mp4')]))
 video=next(s for s in data['streams'] if s['codec_type']=='video');audio=next(s for s in data['streams'] if s['codec_type']=='audio');assert video['width']==1080 and video['height']==1920 and video['r_frame_rate']=='30/1';assert float(data['format']['duration'])<10;assert int(data['format']['size'])<8*1024*1024
 results[folder.name]={'duration':data['format']['duration'],'bytes':data['format']['size'],'video':video['codec_name'],'audio':audio['codec_name']}
(ROOT/'.review'/'verification.json').write_text(json.dumps(results,indent=2));print(json.dumps(results,indent=2))
