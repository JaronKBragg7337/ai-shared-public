from pathlib import Path
p=Path('state/fly-scene-build/live-systems/flies/brain/assets.js');s=p.read_text();s=s[:s.index('export function debugAssets')]+'''export function debugAssets(scene,camera,viewport,button){
 const overlay=document.createElement('div');overlay.className='asset-debug';overlay.hidden=true;viewport.append(overlay);
 const select=document.createElement('select');select.className='asset-picker';select.setAttribute('aria-label','Inspect asset ID');overlay.append(select);
 let enabled=false,labels=[];const overview=new Set(['TABLE.A','TABLE.B','NET','PADDLE','FLY','BRAIN.atlas']);
 function refresh(){for(const {el} of labels)el.remove();labels=[];select.replaceChildren(new Option('Overview / coordinates in metres',''));
  scene.traverse(o=>{if(!o.userData.assetId)return;const id=o.userData.assetId,el=document.createElement('span');el.className='asset-bubble';overlay.append(el);labels.push({o,el});select.append(new Option(id,id));});}
 button.onclick=()=>{enabled=!enabled;button.setAttribute('aria-pressed',String(enabled));overlay.hidden=!enabled;if(enabled)refresh();};
 function update(){if(!enabled)return;for(const {o,el} of labels){const id=o.userData.assetId;if(select.value?select.value!==id:!overview.has(id)){el.hidden=true;continue;}
  const p=o.getWorldPosition(new THREE.Vector3());if(overview.has(id)&&id!=='BRAIN.atlas')new THREE.Box3().setFromObject(o).getCenter(p);
  const screen=p.clone().project(camera),x=(screen.x*.5+.5)*viewport.clientWidth,y=(-screen.y*.5+.5)*viewport.clientHeight;
  el.hidden=screen.z>1||screen.z< -1;el.style.left=`${Math.max(4,Math.min(x,viewport.clientWidth-180))}px`;el.style.top=`${Math.max(78,Math.min(y,viewport.clientHeight-108))}px`;el.textContent=`${id} (${p.toArray().map(n=>n.toFixed(2)).join(', ')})`;
 }}return {update};
}
''';p.write_text(s,encoding='utf-8')
p=p.with_name('scene.js');s=p.read_text();a=s.index("set('assetNote','Measured flybody");b=s.index("');",a);s=s[:a]+"set('assetNote','Measured flybody anatomy | 160x display size. Real joints; threshold-driven motion, not measured limb movement."+s[b:];p.write_text(s,encoding='utf-8')
p=p.with_name('index.html');s=p.read_text();a=s.index('Loading measured flybody');b=s.index('</p>',a);s=s[:a]+'Loading measured flybody anatomy...'+s[b:]
s=s.replace('</footer>','<p>Table: 2.74 &times; 1.525 m; height 0.76 m; net 0.1525 m. Fly enlarged 160&times;; brain displayed separately at an illustrative scale. Frame and paddle construction are illustrative. <a href="ASSETS.md">Asset sources &amp; licences</a>: flybody Apache 2.0; ambientCG textures CC0.</p></footer>');p.write_text(s,encoding='utf-8')
p=p.with_name('scene.css');s=p.read_text()+'\n.asset-picker{position:absolute;top:42px;left:12px;max-width:calc(100% - 24px);pointer-events:auto;z-index:5;background:#101d24;color:#dbedb4;border:1px solid #71815d;border-radius:4px;padding:8px;font:10px ui-monospace,monospace}\n';p.write_text(s,encoding='utf-8')
