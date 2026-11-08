"""Two-pass loudness normalization from original synthesized masters."""
from pathlib import Path
import subprocess,json,re
R=Path(__file__).resolve().parents[1]
for folder in (R/'films').iterdir():
 if not folder.is_dir():continue
 tmp=R/'.review'/folder.name;wav=tmp/'audio.wav'
 first=subprocess.run(['ffmpeg','-hide_banner','-i',str(wav),'-af','loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json','-f','null','NUL'],capture_output=True,text=True,check=True)
 d=json.loads(re.search(r'\{[^{}]+\}',first.stderr).group())
 af=f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={d['input_i']}:measured_TP={d['input_tp']}:measured_LRA={d['input_lra']}:measured_thresh={d['input_thresh']}:offset={d['target_offset']}:linear=true"
 subprocess.run(['ffmpeg','-loglevel','error','-y','-i',str(tmp/'silent.mp4'),'-i',str(wav),'-c:v','copy','-af',af,'-c:a','aac','-b:a','128k','-movflags','+faststart','-shortest',str(folder/'film.mp4')],check=True)
 encoded=folder/'film.mp4'
 second=subprocess.run(['ffmpeg','-hide_banner','-i',str(encoded),'-af','loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json','-f','null','NUL'],capture_output=True,text=True,check=True)
 measured=json.loads(re.search(r'\{[^{}]+\}',second.stderr).group());gain=-14-float(measured['input_i'])
 subprocess.run(['ffmpeg','-loglevel','error','-y','-i',str(encoded),'-c:v','copy','-af',f'volume={gain}dB,alimiter=limit=0.8414:level=false:attack=1:release=50','-c:a','aac','-b:a','128k','-movflags','+faststart',str(tmp/'final-audio.mp4')],check=True)
 encoded.write_bytes((tmp/'final-audio.mp4').read_bytes())
 print(folder.name,'two-pass normalized, encoded level trimmed and peaks limited',flush=True)
