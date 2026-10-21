import json,subprocess,sys
from PIL import Image
tl=json.load(open('timeline.json'))['segs']
ids=[s['id'] for s in tl]
only=sys.argv[1:]
for o in ('land','port'):
    for s in tl:
        if only and s['id'] not in only: continue
        subprocess.run(['python','ep.py',o,'--still',str(s['start']+s['dur']-1.0),f"stills/{s['id']}_{o}.png"],check=True)
def sheet(o,cols,w,h,group,name):
    rows=(len(group)+cols-1)//cols
    S=Image.new('RGB',(cols*w,rows*h))
    for i,k in enumerate(group):
        S.paste(Image.open(f'stills/{k}_{o}.png').convert('RGB').resize((w,h)),((i%cols)*w,(i//cols)*h))
    S.save(name)
sheet('land',2,960,540,ids[:6],'stills/sheetL1.png');sheet('land',2,960,540,ids[6:10],'stills/sheetL2.png');sheet('land',2,960,540,ids[10:],'stills/sheetL3.png')
sheet('port',4,405,720,ids[:8],'stills/sheetP1.png');sheet('port',3,405,720,ids[8:],'stills/sheetP2.png')
