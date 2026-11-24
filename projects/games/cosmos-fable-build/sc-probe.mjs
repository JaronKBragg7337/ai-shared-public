export default async ({ page, shot, ev, step }) => {
  await ev(`(()=>{const c=cosmos,w=c.walker,p=c.port.site.toWorld(200,0.3,250);c.ship.aboard=false;if(c.ship.seat)c.ship.stations.stand();Object.assign(w.worldPos,p);w.velocity={x:0,y:0,z:0};w.yaw=5.2;w.pitch=0.3;c.view.mode='first';})()`); await step(30);
  console.log('fill k', await ev(`cosmos.marsFill.k.value`), JSON.stringify(await ev(`(()=>{const L=[];cosmos.engine.scene.traverse(o=>{if(o.isLight&&o.intensity>0)L.push([o.type,o.name,+o.intensity.toFixed(2),o.distance||0]);});return L;})()`)));
  await shot('probe-fill-on');
  await ev(`cosmos.marsFill.k={value:0}`); await ev(`(()=>{let n=0;cosmos.engine.scene.traverse(o=>{if(o.material&&o.material.userData&&o.material.userData.shader){}});})()`);
};
