"""Lost Places 22.1. Earth 17.1 schema + tv-lib typography/caption/timeline pipeline.
Original Pillow illustrations only; CPU H.264. No GPU or remote assets.
Picture is separately composed from captions so the vertical cut has captions below.
"""
import os,sys,json,math,subprocess,argparse,time
from functools import lru_cache
from pathlib import Path
sys.path.insert(0,'C:/Users/lilli/AI-Shared/projects/tv-lib')
import tvlib as tv
from PIL import Image,ImageDraw,ImageFont,ImageFilter

SCR=json.loads(Path('script.json').read_text(encoding='utf8'))
TL=json.loads(Path('timeline.json').read_text())
TOTAL=TL['total']; FPS=12
PAPER=(239,224,197); INK=(51,43,33); RUST=(154,70,43)
MUTED=(109,94,73); GOLD=(186,137,60); GREEN=(72,102,80); STONE=(193,167,125)
DARK=(35,33,28); CREAM=(255,244,219)
tv.BG=PAPER; tv.TXT=INK; tv.DIM=MUTED; tv.SS=1
tv.configure({s['id']:s['disp'] for s in SCR},[(s['id'],s['head'],s['source'],None) for s in SCR])

@lru_cache(None)
def font(size,bold=False,serif=False):
    name=('georgiab.ttf' if bold else 'georgia.ttf') if serif else ('segoeuib.ttf' if bold else 'segoeui.ttf')
    return ImageFont.truetype('C:/Windows/Fonts/'+name,size)

def text(d,xy,s,size=40,col=INK,bold=False,serif=False,anchor=None):
    d.text(xy,s,font=font(size,bold,serif),fill=col,anchor=anchor)

def lines(d,s,x,y,w,size=44,col=INK,bold=False,serif=False,leading=1.25):
    f=font(size,bold,serif); words=s.split(); cur=''; out=[]
    for word in words:
        candidate=(cur+' '+word).strip()
        if f.getlength(candidate)>w and cur: out.append(cur);cur=word
        else:cur=candidate
    if cur:out.append(cur)
    for k,line in enumerate(out):text(d,(x,y+k*size*leading),line,size,col,bold,serif)
    return y+len(out)*size*leading

def arrow(d,a,b,col=RUST,width=6):
    d.line([a,b],fill=col,width=width)
    ang=math.atan2(b[1]-a[1],b[0]-a[0])
    pts=[b]+[(b[0]-24*math.cos(ang+o),b[1]-24*math.sin(ang+o)) for o in (-.45,.45)]
    d.polygon(pts,fill=col)

def pillar(d,x,y,h=340,w=90,colour=STONE,details=True):
    # Generic T pillar; no claim to copy one excavated relief.
    pts=[(x-w,y-h),(x+w,y-h),(x+w,y-h+.20*h),(x+.48*w,y-h+.20*h),(x+.48*w,y),(x-.48*w,y),(x-.48*w,y-h+.20*h),(x-w,y-h+.20*h)]
    d.polygon([(a+16,b+15) for a,b in pts],fill=(168,144,106))
    d.polygon(pts,fill=colour,outline=MUTED)
    d.line(pts+[pts[0]],fill=MUTED,width=4)
    if details:
        d.line([(x-w*.32,y-h*.52),(x-w*.32,y-h*.25),(x,y-h*.17),(x+w*.32,y-h*.25),(x+w*.32,y-h*.52)],fill=MUTED,width=6)
        d.line([(x-w*.43,y-h*.12),(x+w*.43,y-h*.12)],fill=RUST,width=5)

def ringplan(d,cx,cy,r=215):
    d.ellipse((cx-r,cy-r*.72,cx+r,cy+r*.72),fill=(224,207,176),outline=MUTED,width=13)
    for k in range(10):
        a=2*math.pi*k/10;x=cx+math.cos(a)*r*.86;y=cy+math.sin(a)*r*.62
        d.rounded_rectangle((x-14,y-21,x+14,y+21),radius=3,fill=RUST)
    for x in (cx-55,cx+55):
        d.rectangle((x-12,cy-53,x+12,cy+53),fill=GOLD)
        d.rectangle((x-32,cy-53,x+32,cy-28),fill=GOLD)

def grain(d,x,y,scale=1):
    d.line([(x,y),(x+20*scale,y-190*scale)],fill=GREEN,width=max(2,int(5*scale)))
    for k in range(5):
        yy=y-(45+k*25)*scale; xx=x+(y-yy)/190*20
        for sign in (-1,1):
            d.ellipse((xx+(3 if sign>0 else -37)*scale,yy-28*scale,xx+(37 if sign>0 else -3)*scale,yy+3*scale),fill=GOLD)

def illustration(d,i):
    # Left-side picture panels vary with the evidence being discussed.
    if i in (0,2):
        for k in range(7):
            x=170+k*104; y=705+int(30*math.sin(k*.9)); pillar(d,x,y,180,45,details=False)
        d.arc((90,400,850,820),0,180,fill=MUTED,width=22)
        pillar(d,355,745,390,95);pillar(d,610,730,435,102)
        if i==2:
            # Snake icon, deliberately generic.
            pts=[(744+35*math.sin(t*.4),310+t*8) for t in range(38)]
            d.line(pts,fill=RUST,width=11);d.ellipse((723,300,758,331),fill=RUST)
    elif i==1:
        x0,x1=150,825;y=525
        d.line([(x0,y),(x1,y)],fill=MUTED,width=6)
        for x,year in ((x0,'9500'),(x0+225,'9000'),(x0+450,'8500'),(x1,'8000')):
            d.line([(x,y-18),(x,y+18)],fill=INK,width=4);text(d,(x,y+30),year,37,anchor='mt')
        d.rounded_rectangle((x0,410,x1,465),radius=15,fill=RUST)
        text(d,(488,340),'SETTLEMENT HISTORY',35,RUST,True,anchor='mt')
        text(d,(488,620),'BCE · approximate range',36,MUTED,anchor='mt')
        lines(d,'Construction, repair and fill need their own dates.',150,710,680,40)
    elif i==3:
        for k,(label,col) in enumerate([('Gather',GREEN),('Build',RUST),('Feed',GOLD)]):
            yy=315+k*165;d.rounded_rectangle((220,yy,760,yy+105),radius=25,fill=col)
            text(d,(490,yy+20),label,53,CREAM,True,anchor='mt')
            if k<2:arrow(d,(490,yy+113),(490,yy+154),MUTED)
        text(d,(490,845),'Does this encourage farming?',35,RUST,True,anchor='mt')
    elif i==4:
        ringplan(d,475,560,210)
        for x,y in [(170,300),(340,270),(610,290),(760,390),(760,720),(240,780)]:
            d.ellipse((x-59,y-45,x+59,y+45),fill=(222,205,174),outline=MUTED,width=8)
            d.ellipse((x-12,y-8,x+12,y+8),fill=RUST)
        d.ellipse((100,570,235,680),fill=(121,158,161),outline=MUTED,width=7)
        for xx in range(120,225,23):d.line([(xx,530),(xx-6,565)],fill=(90,133,148),width=4)
    elif i==5:
        for x in (270,420,570):grain(d,x,550,1.0)
        d.ellipse((180,635,770,790),fill=MUTED)
        d.ellipse((215,624,740,749),fill=(158,150,127),outline=INK,width=4)
        d.ellipse((350,600,595,666),fill=(111,107,94),outline=INK,width=4)
        text(d,(480,835),'Grain processing ≠ crop domestication',31,RUST,True,anchor='mt')
    elif i==6:
        d.ellipse((125,360,595,800),fill=(209,198,163),outline=GREEN,width=6)
        d.ellipse((405,360,875,800),outline=RUST,width=6)
        text(d,(330,520),'DAILY',44,GREEN,True,anchor='mt');text(d,(330,575),'LIFE',44,GREEN,True,anchor='mt')
        text(d,(690,520),'RITUAL',44,RUST,True,anchor='mt');text(d,(690,575),'LIFE?',44,RUST,True,anchor='mt')
        text(d,(500,830),'The categories can overlap.',35,MUTED,anchor='mt')
    elif i==7:
        d.polygon([(120,380),(820,690),(820,840),(120,840)],fill=STONE)
        for k in range(6):
            yy=440+k*58;d.line([(120,yy),(820,min(838,yy+210))],fill=MUTED,width=3)
        d.ellipse((490,645,835,850),fill=PAPER,outline=MUTED,width=14)
        pillar(d,650,810,190,48,details=False)
        for k in range(18):
            x=340+k*24;y=430+k*12;d.ellipse((x,y,x+20,y+13),fill=MUTED)
        arrow(d,(260,350),(665,600),RUST,9)
        text(d,(470,295),'DEBRIS MOVES DOWNSLOPE',33,RUST,True,anchor='mt')
    elif i==8:
        pts=[(280,420,'Göbekli Tepe'),(690,690,'Karahan Tepe'),(240,770,'Other sites')]
        d.line([(280,420),(690,690),(240,770),(280,420)],fill=STONE,width=5)
        for x,y,label in pts:
            d.ellipse((x-15,y-15,x+15,y+15),fill=RUST)
            text(d,(x,y+34),label,34,INK,True,anchor='mt')
        text(d,(470,300),'ŞANLIURFA REGION · TÜRKİYE',33,MUTED,True,anchor='mt')
        text(d,(470,865),'Relationship diagram · not a map',30,MUTED,anchor='mt')
    elif i==9:
        d.rounded_rectangle((120,470,850,800),radius=20,fill=STONE)
        for yy in (540,610,680,750):d.line([(120,yy),(850,yy)],fill=MUTED,width=3)
        # Unfinished pillar in bedrock, shown horizontally.
        d.polygon([(220,600),(690,600),(690,560),(780,560),(780,730),(690,730),(690,690),(220,690)],fill=PAPER,outline=RUST)
        d.line([(205,580),(670,580),(670,540),(800,540),(800,750),(670,750),(670,710),(205,710)],fill=RUST,width=7)
        text(d,(480,350),'UNFINISHED WORK IS EVIDENCE',35,RUST,True,anchor='mt')
        text(d,(480,845),'Generic quarry diagram',31,MUTED,anchor='mt')
    elif i==10:
        nodes=[(480,340,'Gathering'),(215,650,'Building'),(740,650,'Food')]
        for a,b in [(0,1),(1,2),(2,0)]:
            x,y,_=nodes[a];xx,yy,_=nodes[b];arrow(d,(x,y+35),(xx,yy-30),GOLD)
        for x,y,label in nodes:
            d.ellipse((x-126,y-66,x+126,y+66),fill=GREEN)
            text(d,(x,y-27),label,39,CREAM,True,anchor='mt')
        text(d,(480,840),'Interacting changes, not one ladder',34,RUST,True,anchor='mt')
    else:
        ringplan(d,470,515,240)
        text(d,(470,770),'WHAT WE KNOW',42,GREEN,True,anchor='mt')
        text(d,(470,830),'WHAT WE DON’T',42,RUST,True,anchor='mt')

@lru_cache(maxsize=12)
def picture(i):
    # Full 16:9 graphic, cached once per scene; motion is added during composition.
    im=Image.new('RGB',(1920,1080),PAPER);d=ImageDraw.Draw(im)
    for k in range(13):
        yy=240+k*51;d.arc((-700,yy-500,1050,yy+800),235,340,fill=(227,210,181),width=2)
    d.rectangle((0,0,22,1080),fill=RUST)
    text(d,(80,38),'HEARTBEAT TV   /   CH 22',30,MUTED,True)
    text(d,(1840,38),'LOST PLACES   ·   22.1',30,RUST,True,anchor='rt')
    s=SCR[i]
    if i==0:
        lines(d,'Did we build civilization backward?',975,280,850,83,INK,True,True,1.12)
        text(d,(980,570),'GÖBEKLI TEPE',44,RUST,True)
        lines(d,'Ruins and cities. What we know — and what we don’t.',980,660,790,43,MUTED)
    else:
        text(d,(80,112),s['head'],70,INK,True,True)
        d.rectangle((80,213,220,220),fill=RUST)
        status=s['status']; colour=GREEN if status=='ESTABLISHED' else RUST
        text(d,(990,285),status,31,colour,True)
        y=360
        size=42 if i==11 else 48
        gap=25 if i==11 else 39
        for n,p in enumerate(s['points']):
            d.ellipse((995,y+17,1005,y+27),fill=colour)
            y=lines(d,p,1030,y,780,size,INK,n==0,False,1.22)+gap
    art=Image.new('RGB',(1920,1080),PAPER)
    illustration(ImageDraw.Draw(art),i)
    im.paste(art.crop((40,220,930,940)).resize((890,560),Image.Resampling.LANCZOS),(40,250))
    d=ImageDraw.Draw(im)
    text(d,(80,820),'ILLUSTRATIVE DIAGRAMS · NOT TO SCALE',22,MUTED,True)
    d.line([(80,997),(1840,997)],fill=(184,164,131),width=2)
    lines(d,s['source'],80,1013,1740,27,MUTED)
    return im

def scene_at(t):
    for i,(a,b) in enumerate(tv.bounds):
        if a<=t<b:return i
    return len(SCR)-1

@lru_cache(maxsize=12)
def blurred(i):
    bg=picture(i).resize((270,480)).filter(ImageFilter.GaussianBlur(18)).resize((1080,1920))
    return Image.blend(bg,Image.new('RGB',bg.size,DARK),.83)

def frame(t,port=False,poster=False):
    i=0 if poster else scene_at(t);s=SCR[i];base=picture(i)
    local=t-tv.bounds[i][0]
    if not poster and i>0 and local<.7:
        u=max(0,min(1,local/.7));u=u*u*(3-2*u)
        base=Image.blend(picture(i-1),base,u)
    sub=tv.subtitle_at(s['id'],t) or ''
    if port:
        im=blurred(i).copy();d=ImageDraw.Draw(im)
        text(d,(70,110),'HEARTBEAT TV',32,CREAM,True)
        text(d,(70,167),'LOST PLACES',68,CREAM,True,True)
        text(d,(70,265),'CH 22  /  EPISODE 1',30,(213,181,126),True)
        im.paste(base.resize((1080,608),Image.Resampling.LANCZOS),(0,385))
        d=ImageDraw.Draw(im)
        text(d,(70,1050),s['status'],30,(225,188,125),True)
        end=lines(d,sub,70,1130,940,53,CREAM,False,False,1.32)
        if end>1650:raise ValueError('Portrait caption overflow')
        d.line([(70,1675),(1010,1675)],fill=(112,100,80),width=2)
        end=lines(d,s['source'],70,1710,935,29,(217,199,168))
        if end>1870:raise ValueError('Portrait source overflow')
        text(d,(70,1850),'Made with AI by Heartbeat Observatory',26,(217,199,168))
        d.rectangle((70,1630,70+940*t/TOTAL,1636),fill=(210,165,92))
        return im
    im=base.copy();d=ImageDraw.Draw(im)
    if not poster:
        # Fixed safe lower band; sources remain visible below.
        d.rectangle((25,850,1919,997),fill=DARK)
        f=font(44); words=sub.split();ls=[];cur=''
        for word in words:
            st=(cur+' '+word).strip()
            if f.getlength(st)>1690 and cur:ls.append(cur);cur=word
            else:cur=st
        if cur:ls.append(cur)
        if len(ls)>2:raise ValueError('Landscape caption overflow')
        yy=922-len(ls)*28
        for k,line in enumerate(ls):text(d,(960,yy+k*56),line,44,CREAM,anchor='mt')
        d.rectangle((25,994,25+1895*t/TOTAL,998),fill=GOLD)
    return im.resize((1280,720),Image.Resampling.LANCZOS)

def render(port,out):
    size=(1080,1920) if port else (1280,720)
    cmd=['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{size[0]}x{size[1]}','-r',str(FPS),'-i','-',
         '-an','-c:v','libx264','-preset','fast','-crf','19','-threads','4','-r','24','-pix_fmt','yuv420p',out]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    start=time.time();n=math.ceil(TOTAL*FPS)
    try:
        for k in range(n):
            proc.stdin.write(frame(k/FPS,port).tobytes())
            if k%360==0:print(f'{"port" if port else "land"}: {k}/{n} frames, {time.time()-start:.1f}s',flush=True)
    finally:proc.stdin.close()
    if proc.wait():raise RuntimeError('ffmpeg encoding failed')
    print('Render seconds:',round(time.time()-start,1),flush=True)

def qa():
    Path('stills').mkdir(exist_ok=True)
    tiles=[]
    for i,(a,b) in enumerate(tv.bounds):
        t=min(b-.4,a+max(3,(b-a)*.55))
        for port in (False,True):
            im=frame(t,port);im.save(f'stills/s{i+1:02d}-{"port" if port else "land"}.jpg',quality=88)
            if not port:tiles.append(im.resize((480,270)))
        # Check every caption in both orientations, not just representative frames.
        for j in range(len(SCR[i]['disp'])):
            tt=a+tv.cue(SCR[i]['id'],j)+.03
            frame(tt,False);frame(tt,True)
    sheet=Image.new('RGB',(1920,810),DARK)
    for k,im in enumerate(tiles):sheet.paste(im,((k%4)*480,(k//4)*270))
    sheet.save('stills/contact-land.jpg',quality=92)
    frame(3,False,True).save('lostplaces-ep1-gobekli.jpg',quality=94)
    print('All captions fit; 24 scene samples and contact sheet written.')

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('orientation',choices=['land','port'],nargs='?',default='land')
    ap.add_argument('--out');ap.add_argument('--qa',action='store_true');ap.add_argument('--still',nargs=2)
    args=ap.parse_args()
    if args.qa:qa()
    elif args.still:frame(float(args.still[0]),args.orientation=='port').save(args.still[1])
    else:render(args.orientation=='port',args.out or f'video_{args.orientation}.mp4')
