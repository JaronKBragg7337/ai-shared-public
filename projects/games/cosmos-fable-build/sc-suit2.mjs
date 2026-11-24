// Suits on NPCs: Mars port traders and clerks, the Moon hub, Ceres, Callisto. Third-person player on Mars.
export const helpers = `
window.npcs = () => { const out = []; cosmos.engine.scene.traverse(o => { if (o.name && o.name.startsWith('person-') && !(o.parent && o.parent.name === 'player-body')) { let vis = true; for (let n = o; n; n = n.parent) if (!n.visible) vis = false; if (vis) out.push(o); } }); const V = cosmos.engine.camera.position.constructor, cr = cosmos.engine.camera.getWorldPosition(new V()); return out.map(o => [o, o.getWorldPosition(new V()).distanceTo(cr)]).filter(q => q[1] < 600).sort((a, b) => a[1] - b[1]).map(q => q[0]); };
window.camNpc = (i, dist = 3, h = 1.5, side = 0) => { const c = cosmos, o = npcs()[i]; if (!o) return false; const V = o.position.constructor;
  const p = o.getWorldPosition(new V()), d = o.getWorldDirection(new V()), cr = c.engine.camera.getWorldPosition(new V()), cw = c.engine.cameraWorldPos;
  const base = { x: cw.x + p.x - cr.x, y: cw.y + p.y - cr.y, z: cw.z + p.z - cr.z }, l = Math.hypot(base.x, base.y, base.z), up = { x: base.x / l, y: base.y / l, z: base.z / l };
  const sx = up.y * d.z - up.z * d.y, sy = up.z * d.x - up.x * d.z, sz = up.x * d.y - up.y * d.x;
  const eye = { x: base.x + d.x * dist + sx * side + up.x * h, y: base.y + d.y * dist + sy * side + up.y * h, z: base.z + d.z * dist + sz * side + up.z * h };
  const tgt = { x: base.x + up.x * 1.15, y: base.y + up.y * 1.15, z: base.z + up.z * 1.15 };
  c.freeCam.set(eye, tgt); for (let k = 0; k < 6; k++) c.step(1 / 30); return true; };
`;
export default async ({ page, shot, ev, step, land, want }) => {
  const on = (n) => !want || want.has(n);
  await ev(helpers);
  if (on('n1-mars-traders')) { await ev(`(()=>{const c=cosmos,w=c.walker,p=c.port.site.toWorld(-58,0.3,44);c.ship.aboard=false;if(c.ship.seat)c.ship.stations.stand();Object.assign(w.worldPos,p);w.velocity={x:0,y:0,z:0};w.yaw=Math.PI;w.pitch=-0.05;c.view.mode='third';})()`); await step(40); await shot('n1-mars-traders'); }
  if (on('n2-mars-walk')) { await page.keyboard.down('KeyW'); await step(40); await shot('n2-mars-walk'); await page.keyboard.up('KeyW'); }
  if (on('n2b-mars-npc')) { console.log('mars npcs', await ev(`npcs().length`)); await ev(`camNpc(0,2.6,1.5,0.8)`); await shot('n2b-mars-npc'); await ev(`cosmos.freeCam.off()`); }
  for (const w of ['moon', 'ceres', 'callisto']) {
    if (!on('n3-' + w)) continue;
    await land(w); await ev(`stand(14,-10,0.6,-0.08,true)`); await step(30);
    console.log(w, 'npcs', await ev(`npcs().length`));
    await ev(`camNpc(0,2.8,1.5,0.8)`); await shot('n3-' + w);
    await ev(`camNpc(1,6,2.2,2)`); await shot('n4-' + w + '-wide');
    await ev(`cosmos.freeCam.off()`);
  }
};
