from pathlib import Path
p=Path('state/fly-scene-build/live-systems/flies/brain/scene.js');s=p.read_text()
s=s.replace("import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';","import {buildTable,loadMeasuredFly,debugAssets,dimensions} from './assets.js';")
s=s.replace('avatar, mixer, rigNodes=[], clips=[]','avatar, measuredFly, debugLayer')
s=s.replace("pressedAt=performance.now();playClip('press');","pressedAt=performance.now();")
a=s.index('function box(');b=s.index('async function setup()',a)
s=s[:a]+'''async function loadAvatar(){
 try{measuredFly=await loadMeasuredFly(scene);avatar=measuredFly.holder;sceneState.glb=true;sceneState.jointBodies=measuredFly.joints.length;sceneState.jointCount=measuredFly.joints.reduce((n,b)=>n+b.userData.joints.length,0);set('assetNote','Measured flybody anatomy · 160× display size. Real joints; threshold-driven motion, not measured limb movement.');}
 catch(e){set('assetNote','Measured fly asset unavailable. Anatomy is not being shown.');sceneState.assetError=e.message;}
}
'''+s[b:]
a=s.index('  box(3.5');b=s.index('  brain=new',a)
s=s[:a]+"  buildTable(scene);sceneState.tableDimensions=dimensions;\n  debugLayer=debugAssets(scene,camera,viewport,$('assetDebug'));\n"+s[b:]
s=s.replace('brain.position.y=.32','brain.userData.assetId=\'BRAIN.atlas\';brain.position.y=.32')
s=s.replace('controls.update(dt);mixer?.update(dt);','controls.update(dt);')
a=s.index('    const pose=');b=s.index('    const label=',a)
s=s[:a]+"    measuredFly?.update(v,t-pressedAt,t,reducedMotion);debugLayer?.update();\n"+s[b:]
s=s.replace('camera.position.set(0,1.3,6.9)','camera.position.set(3.2,2.3,5.5)')
s=s.replace('renderer.setClearColor','renderer.shadowMap.enabled=true;renderer.shadowMap.type=THREE.PCFSoftShadowMap;renderer.setClearColor')
s=s.replace('light.position.set(2,5,4);scene.add(light);','light.position.set(2,5,4);light.castShadow=true;light.shadow.mapSize.set(1024,1024);light.shadow.camera.left=-3;light.shadow.camera.right=3;light.shadow.camera.top=3;light.shadow.camera.bottom=-3;light.shadow.bias=-.001;scene.add(light);')
p.write_text(s)
p=p.with_name('index.html');s=p.read_text().replace('<button id="resetView">Reset view</button>','<button id="resetView">Reset view</button><button id="assetDebug" aria-pressed="false">Asset IDs</button>')
s=s.replace('Fly avatar: three-shape placeholder. Waiting for the rigged asset.','Loading measured flybody anatomy…')
s=s.replace('<a href="/live-systems/flies/#learn">See the learning record ↗</a>','<p>Table: 2.74 × 1.525 m · height 0.76 m · net 0.1525 m. Fly enlarged 160×; brain displayed separately at an illustrative scale. Frame and paddle construction are illustrative. <a href="ASSETS.md">Asset sources &amp; licences</a> · flybody Apache 2.0 · ambientCG textures CC0.</p><a href="/live-systems/flies/#learn">See the learning record ↗</a>')
p.write_text(s)
p=p.with_name('scene.css');s=p.read_text()+'''\n.asset-debug{position:absolute;inset:0;pointer-events:none;overflow:hidden;z-index:4}.asset-bubble{position:absolute;max-width:180px;padding:3px 5px;background:#101d24ed;color:#dbedb4;border:1px solid #71815d;font:8px/1.3 ui-monospace,monospace;border-radius:3px;overflow-wrap:anywhere}.asset-debug[hidden],.asset-bubble[hidden]{display:none}.view-controls [aria-pressed=true]#assetDebug{color:var(--accent);border-color:var(--accent)}\n''';p.write_text(s)
