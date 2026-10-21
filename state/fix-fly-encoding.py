from pathlib import Path
for name in ['scene.js','index.html','scene.css','README.md']:
 p=Path('state/fly-scene-build/live-systems/flies/brain')/name
 s=p.read_text(encoding='utf-8')
 try:
  fixed=s.encode('cp1252').decode('utf-8')
  p.write_text(fixed,encoding='utf-8'); print(name,'recovered UTF-8')
 except UnicodeError as e: print(name,str(e))
p=Path('state/fly-scene-build/live-systems/flies/brain/scene.js');s=p.read_text(encoding='utf-8').replace('newestAction=null;if(spikeMesh)','newestAction=null;pressedAt=-Infinity;if(spikeMesh)');p.write_text(s,encoding='utf-8')
p=Path('state/fly-scene-build/live-systems/flies/brain/assets.js');s=p.read_text(encoding='utf-8').replace('[.08,.025,.16]','[.08,.025,.18]');p.write_text(s,encoding='utf-8')
