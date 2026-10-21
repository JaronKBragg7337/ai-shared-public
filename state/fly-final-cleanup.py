from pathlib import Path
p=Path('state/fly-scene-build/live-systems/flies/brain/scene.js');s=p.read_text().replace('newestAction=null;if(spikeMesh)','newestAction=null;pressedAt=-Infinity;if(spikeMesh)');p.write_text(s,encoding='utf-8')
p=Path('state/fly-scene-build/live-systems/flies/brain/assets.js');s=p.read_text().replace("[.08,.025,.16]","[.08,.025,.18]");p.write_text(s,encoding='utf-8')
