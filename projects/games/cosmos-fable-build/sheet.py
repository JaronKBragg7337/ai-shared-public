import sys,glob,os
from PIL import Image
d=sys.argv[1];out=sys.argv[2];names=sys.argv[3:]
fs=[f for f in sorted(glob.glob(os.path.join(d,'*.png'))) if not names or any(n in os.path.basename(f) for n in names)]
cols=int(os.environ.get('COLS','6'));w=int(os.environ.get('W','300'))
ims=[Image.open(f).convert('RGB') for f in fs]
ims=[i.resize((w,int(i.height*w/i.width))) for i in ims]
h=max(i.height for i in ims);rows=(len(ims)+cols-1)//cols
S=Image.new('RGB',(cols*w,rows*h),(20,20,20))
for k,i in enumerate(ims):S.paste(i,((k%cols)*w,(k//cols)*h))
S.save(out);print(len(ims),S.size)
