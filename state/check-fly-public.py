import urllib.request,hashlib,json
from pathlib import Path
base='https://www.heartbeatobservatory.com/live-systems/flies/brain/'
p=Path('state/fly-scene-build/live-systems/flies/brain');out=[]
for name in ['index.html','scene.js','assets.js','fly.glb']:
 try:
  r=urllib.request.urlopen(base+name,timeout=25);data=r.read();local=(p/name).read_bytes();out.append({'file':name,'status':r.status,'bytes':len(data),'matches':hashlib.sha256(data.replace(b'\r\n',b'\n') if name.endswith(('.html','.js')) else data).digest()==hashlib.sha256(local.replace(b'\r\n',b'\n') if name.endswith(('.html','.js')) else local).digest()})
 except Exception as e:out.append({'file':name,'error':str(e)})
print(json.dumps(out,indent=2))
