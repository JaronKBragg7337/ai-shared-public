from PIL import Image
from pathlib import Path
p=Path('state/fly-scene-build/live-systems/flies/brain/textures'); p.mkdir(exist_ok=True)
for kind in ['Color','Roughness','NormalGL']:
 im=Image.open('state/Wood051/Wood051_1K-JPG_'+kind+'.jpg'); im.resize((512,512),Image.Resampling.LANCZOS).save(p/('wood-'+kind.lower()+'.jpg'),quality=85)
