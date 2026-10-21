import json,subprocess,sys
from concurrent.futures import ThreadPoolExecutor
ori=sys.argv[1]; tl=json.load(open('timeline.json'))
def one(s):
    t=s['start']+s['dur']*float(sys.argv[2] if len(sys.argv)>2 else 0.85)
    subprocess.run(['python','ep.py',ori,'--still',str(t),f'stills/{ori}_{s["id"]}.png'],check=True)
with ThreadPoolExecutor(6) as ex: list(ex.map(one,tl['segs']))
from PIL import Image
ims=[Image.open(f'stills/{ori}_{s["id"]}.png') for s in tl['segs']]
w,h=ims[0].size; k=0.3 if ori=='land' else 0.22
cols=3 if ori=='land' else 6; tw,th=int(w*k),int(h*k)
rows=(len(ims)+cols-1)//cols
for part in range(0,len(ims),6 if ori=='port' else 9):
    sub=ims[part:part+(6 if ori=='port' else 9)]
    c=3 if ori=='land' else 6; r=(len(sub)+c-1)//c
    sh=Image.new('RGB',(tw*c,th*r))
    for i,im in enumerate(sub): sh.paste(im.resize((tw,th)),((i%c)*tw,(i//c)*th))
    sh.save(f'stills/sheet_{ori}_{part//(6 if ori=="port" else 9)}.png')
