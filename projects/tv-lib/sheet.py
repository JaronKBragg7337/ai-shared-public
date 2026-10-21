import sys,glob
from PIL import Image
pat,out,cols,tw=sys.argv[1],sys.argv[2],int(sys.argv[3]),int(sys.argv[4])
fs=sorted(glob.glob(pat),key=lambda f:int(''.join(c for c in f.split('_')[-1] if c.isdigit())))
ims=[Image.open(f).convert('RGB') for f in fs]
th=int(tw*ims[0].height/ims[0].width)
rows=(len(ims)+cols-1)//cols
S=Image.new('RGB',(cols*tw,rows*th),(0,0,0))
for i,im in enumerate(ims): S.paste(im.resize((tw,th)),((i%cols)*tw,(i//cols)*th))
S.save(out); print(fs)
