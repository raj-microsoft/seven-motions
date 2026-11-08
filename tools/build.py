from pathlib import Path
import base64,json
ROOT=Path(__file__).resolve().parents[1]
code=(ROOT/'tools/motion.js').read_text(encoding='utf-8');font=base64.b64encode((ROOT/'assets/Anton-Regular.ttf').read_bytes()).decode()
names=['one-line','one-ball','ascii','pixel','risograph','codex','ink']
for i,name in enumerate(names):
    p=ROOT/'films'/name;p.mkdir(parents=True,exist_ok=True)
    html='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+name+' — Seven motions</title><style>@font-face{font-family:Anton;src:url(data:font/ttf;base64,'+font+')}html,body{margin:0;background:#111}canvas{display:block;width:100vw;height:100vh;object-fit:contain}</style><canvas aria-label="Original '+name+' seed journey"></canvas><script>'+code+'\ndocument.fonts.load("100px Anton").then(()=>{window.film=makeFilm(document.querySelector("canvas"),'+str(i)+');window.seek=t=>film.seek(t);seek(3);window.ready=true;});</script></html>'
    (p/'index.html').write_text(html,encoding='utf-8')
print('Seven self-contained deterministic HTML films built.')
