python - <<'P'
h=open('head.py',encoding='utf-8').read().replace('History ep.1 "What if the railroads never existed?"','Science ep.1 "Turning breath back into air"')
tail=open('../../history-channel/ep1-railroads/render.py',encoding='utf-8').read(); tail=tail[tail.index('bounds = []'):]
open('render.py','w',encoding='utf-8').write(h+open('body1.py',encoding='utf-8').read()+open('body2.py',encoding='utf-8').read()+'\n'+tail)
P
