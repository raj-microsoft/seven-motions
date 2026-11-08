"""Original storyboard stills, not animation implementation. No source frames used."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math, random
OUT=Path(__file__).parent
W,H=1080,1920
FONTS=Path('C:/Windows/Fonts')
def font(n,mono=False): return ImageFont.truetype(str(FONTS/('consola.ttf' if mono else 'bahnschrift.ttf')),n)
def label(d,text,y,fill,mono=False,size=74):
    box=d.textbbox((0,0),text,font=font(size,mono)); d.text(((W-box[2])/2,y),text,font=font(size,mono),fill=fill)
def seed(d,x,y,r,c):
    d.ellipse((x-r*.62,y-r,x+r*.62,y+r),fill=c)
def line(d,pts,c,width=6): d.line(pts,fill=c,width=width,joint='curve')
def texture(d,bg,ink,n=4000):
    r=random.Random(301)
    for _ in range(n):
        x,y=r.randrange(W),r.randrange(H); d.point((x,y),fill=ink)
def build(k,b):
    palettes=[('#F4F1EA','#2F5BFF'),('#111116','#FF3319'),('#000000','#33FF66'),('#9BBC0F','#0F380F'),('#F3EFE6','#00838A'),('#E9D9B5','#5A3A1E'),('#FAFAFA','#1B1F6B')]
    bg,ink=palettes[k]; im=Image.new('RGB',(W,H),bg); d=ImageDraw.Draw(im)
    if k==0:
        for x in range(0,W,60): line(d,[(x,0),(x,H)],'#DAD5CA',1)
        for y in range(0,H,60): line(d,[(0,y),(W,y)],'#DAD5CA',1)
        pts=[]
        for i in range(800):
            u=i/799
            if b==0: x=100+880*u; y=1200-380*u+70*math.sin(11*u)
            elif b==1: x=540+350*math.sin(2*math.pi*u); y=960+470*math.cos(2*math.pi*u)+80*math.sin(9*u)
            elif b==2: x=100+880*u; y=1050+110*math.sin(5*math.pi*u)-260*math.sin(math.pi*u)
            else: x=540+300*math.sin(u*math.pi*5)*u; y=1270-700*u
            pts.append((x,y))
        line(d,pts,ink,8); label(d,['A seed stirs.','It catches the wind.','Over every horizon.','A new beginning.'][b],350,ink,size=65)
    elif k==1:
        if b==1: d.rectangle((0,0,W,H),fill=ink); ink='#111116'
        if b==2: d.rectangle((0,0,W,H),fill='#EFEBE4')
        if b==0:
            line(d,[(90,1370),(990,1370)],'#EFEBE4',4)
            for i in range(3): d.arc((100+i*240,700+i*100,470+i*240,1370),180,360,fill='#EFEBE4',width=4)
            seed(d,800,1230,100,ink)
        elif b==1:
            label(d,'GO',650,ink,size=440); seed(d,790,1170,100,'#EFEBE4')
        elif b==2:
            for j in range(70):
                a=j*2.399; rr=40+7*j; x=540+rr*math.cos(a);y=950+rr*.8*math.sin(a); d.ellipse((x-9,y-9,x+9,y+9),fill='#2A42FF')
            seed(d,540,950,110,'#FF3319')
        else:
            label(d,'GROW',820,'#EFEBE4',size=195); seed(d,540,1190,85,'#FF3319')
        label(d,['LEAVE THE GROUND','CROSS THE CITY','CIRCLE THE WORLD','FIND YOUR PLACE'][b],350,'#EFEBE4' if b!=2 else '#111116',size=53)
    elif k==2:
        label(d,'$ seed --destination earth',330,ink,True,48)
        chars=' .:-=+*#%@'; r=random.Random(70+b)
        for j in range(68):
            for i in range(90):
                x=(i-45)/36;y=(j-34)/27
                if b==0: inside=(x*x*2+y*y)<.6
                elif b==1: inside=abs(math.sqrt(x*x+y*y)-.78)<.19
                elif b==2: inside=abs(y-.2*math.sin(6*x))<.1 or x*x*2+(y+.4)**2<.12
                else: inside=abs(x)<.04 and y>-.5 or ((x-.3)**2*4+(y+.45)**2*12<.5) or ((x+.3)**2*4+(y+.2)**2*12<.5)
                if inside: d.text((i*12,560+j*13),chars[int(r.random()*8)+2],font=font(14,True),fill=ink)
        label(d,['[ seed detected ]','[ crossing longitude ]','[ landing sequence ]','[ life: online ]'][b],1510,ink,True,52)
    elif k==3:
        low=Image.new('RGB',(135,240),bg); p=ImageDraw.Draw(low); cs=['#0F380F','#306230','#8BAC0F','#9BBC0F']; bay=[[0,8,2,10],[12,4,14,6],[3,11,1,9],[15,7,13,5]]
        for y in range(105,220):
            for x in range(135):
                h=151+20*math.sin(x*.05+b)
                if y>h: p.point((x,y),fill=cs[0 if (bay[y%4][x%4]/16<(y-h)/90) else 1])
        cx=35+b*20;cy=round(110-10*math.sin(b))
        for y in range(cy-19,cy+19):
            for x in range(cx-14,cx+14):
                rad=((x-cx)/14)**2+((y-cy)/19)**2
                if rad<1:p.point((x,y),fill=cs[0 if bay[y%4][x%4]/16<rad else 2])
        if b==3:
            p.line((cx,cy,cx,cy-45),fill=cs[0],width=3);p.rectangle((cx,cy-42,cx+15,cy-36),fill=cs[0]);p.rectangle((cx-13,cy-28,cx,cy-22),fill=cs[0])
        im=low.resize((W,H),Image.Resampling.NEAREST);d=ImageDraw.Draw(im);label(d,['SEED / 001','WIND / EAST','LAND / FOUND','PRESS GROW'][b],350,ink,True,82)
    elif k==4:
        texture(d,bg,'#CFC9BB',12000);pink='#FF48B0';r=random.Random(17)
        for j in range(5):
            x=-100+j*300+b*25;y=round(1050+80*math.sin(j))
            pts=[(x,y),(x+180,y-350),(x+370,y+250),(x-40,y+320)]
            d.polygon([(a+4,c+5) for a,c in pts],fill=pink);d.polygon(pts,fill=ink)
            for yy in range(y-150,y+150,18):
                for xx in range(x+60,x+160,18):d.ellipse((xx,yy,xx+4,yy+4),fill=bg)
        d.ellipse((690,530,940,780),fill=pink); seed(d,260+b*145,820,75,pink)
        if b==3:
            line(d,[(695,850),(695,610)],pink,15);d.ellipse((695,560,850,650),fill=pink)
        label(d,['A PAPER WIND','A FOLDED SEA','A SOFT LANDING','ROOTED, AT LAST'][b],350,ink,size=66)
    elif k==5:
        texture(d,bg,'#CDBA93',14000)
        d.ellipse((160,560,920,1320),outline='#A4452C',width=3);d.rectangle((160,560,920,1320),outline='#A4452C',width=2)
        for j in range(0,760,40):line(d,[(160+j,550),(160+j,570)],'#A4452C',3)
        if b>0:
            seed(d,540,960,90,ink)
            for s in [-1,1]:
                pts=[(540,950),(540+s*330,700),(540+s*260,1000),(540+s*90,1100),(540,950)];line(d,pts,ink,6)
                if b>1:
                    for j in range(17):line(d,[(540+s*(100+j*10),820+j*8),(540+s*(90+j*8),1000+j*3)],ink,2)
            if b==3:line(d,[(540,1050),(540,1350)],ink,5);d.arc((400,1100,550,1210),0,175,ink,5);d.arc((530,1160,700,1270),0,175,ink,5)
        label(d,['The measure of wind','A wing for a seed','Across the old world','An invention called life'][b],350,ink,size=65)
    else:
        r=random.Random(700)
        for j in range(30000):
            a=r.random()*math.tau;rr=abs(r.gauss(0,1));q=r.random()
            if b==0:x=540+math.cos(a)*rr*28;y=640+math.sin(a)*rr*60
            elif b==1:x=540+math.cos(a)*rr*180;y=850+math.sin(a)*rr*230+80*math.sin(a*4)
            elif b==2:x=540+math.cos(a)*rr*220;y=1000+math.sin(a)*rr*190+95*math.sin(a*3)
            else:
                x=540+math.sin(a)*rr*100;y=1000+math.cos(a)*rr*190
                if q>.6:x+=190*math.sin(a);y-=200+120*math.cos(a)
            c='#C2185B' if b>=2 and q>.6 else '#1B1F6B';d.ellipse((x,y,x+2,y+2),fill=c)
        label(d,['One drop.','An ocean of possibility.','Two currents meet.','Something takes root.'][b],350,ink,size=63)
    return im
names=['one-line','one-ball','ascii','pixel','risograph','codex','ink']
for k,name in enumerate(names):
    folder=OUT/name;folder.mkdir(parents=True,exist_ok=True)
    sheet=Image.new('RGB',(1080,520),'#ffffff');sd=ImageDraw.Draw(sheet)
    for b in range(4):
        im=build(k,b);im.save(folder/f'key-{b+1}.png');sheet.paste(im.resize((270,480)),(b*270,0));sd.text((b*270+12,488),f'KEY {b+1}',font=font(18),fill='#111111')
    sheet.save(OUT/f'{name}-board.png')
print('28 original 1080x1920 key stills + 7 contact boards created')
