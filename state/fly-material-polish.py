from pathlib import Path
p=Path('state/fly-scene-build/live-systems/flies/brain/assets.js');s=p.read_text(encoding='utf-8').replace('color:0xb7c6c1,transparent:true,opacity:.65','color:0x293d43,transparent:true,opacity:.8')
s=s.replace("const blade=add('PADDLE.blade'","const paddleWood=wood.clone();for(const key of ['map','normalMap','roughnessMap']){paddleWood[key]=wood[key].clone();paddleWood[key].repeat.set(.15/.8,.16/.8);}\n const blade=add('PADDLE.blade'").replace("new THREE.CylinderGeometry(1,1,.006,48),wood,","new THREE.CylinderGeometry(1,1,.006,48),paddleWood,")
s=s.replace("box('PADDLE.handle',[.028,.018,.1],wood,","const handleWood=wood.clone();for(const key of ['map','normalMap','roughnessMap']){handleWood[key]=wood[key].clone();handleWood[key].repeat.set(.028/.8,.1/.8);}\n box('PADDLE.handle',[.028,.018,.1],handleWood,")
p.write_text(s,encoding='utf-8')
