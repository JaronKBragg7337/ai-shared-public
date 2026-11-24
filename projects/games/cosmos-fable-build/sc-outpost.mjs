// The Phobos / Deimos outposts (src/worlds/<phobos|deimos>/client.js), day and night. Run with Q='&sky=live', WORLD=phobos|deimos, BASE=http://127.0.0.1:4381/
// node cshot.mjs webkit phone shots sc-outpost.mjs
export default async ({ page, shot, ev, step, land, want }) => {
  const W = process.env.WORLD || 'phobos', pre = `p2-${W}-`;
  await land(W);
  await ev(`stand(28,-8,Math.PI/2,-0.06)`);
  await ev(`window.sunEl=()=>{const c=cosmos,f=c.walker.updateFrame(),s=c.space.sunLocal;return Math.asin(Math.max(-1,Math.min(1,s.x*f.up.x+s.y*f.up.y+s.z*f.up.z)))*180/Math.PI;};
    window.findSun=(deg,needVis)=>{const c=cosmos;let best=0,be=1e9;const day=${process.env.DAY_S || 27600};for(let s=0;s<day;s+=day/160){c.setSkyShift(s);c.step(1/30);const d=Math.abs(sunEl()-deg)+(needVis&&c.space.sky.state.vis<0.97?500:0);if(d<be){be=d;best=s;}}c.setSkyShift(best);for(let i=0;i<10;i++)c.step(1/30);return [best,sunEl()];}`);
  const info = await ev(`(()=>{const w=cosmos.space.worlds.get('${W}'),c=w.client;const o={client:!!c,vis:c&&c.root.visible,boxes:c&&c.boxes.length,folk:c&&c.folk.members.length,meshes:0,tris:0,g:[]};if(c){o.kit=[];c.root.traverse(m=>{if(m.isMesh&&m.geometry){o.meshes++;const g=m.geometry,n=(g.index?g.index.count:g.attributes.position.count)/3;o.tris+=n;if(/^(moon-kit|outpost)/.test(m.name))o.kit.push(m.name.replace('moon-kit:','')+':'+n);}});}
    const pi=w.body.padInfo;for(const [e,n] of [[0,0],[30,0],[45,5],[60,0],[0,-50],[10,45],[55,-20]]){const p=P(e,n,0);o.g.push(+((p.x-pi.point.x)*pi.up.x+(p.y-pi.point.y)*pi.up.y+(p.z-pi.point.z)*pi.up.z).toFixed(2));}return o;})()`);
  console.log('info', JSON.stringify(info));
  // stand(e, n, yaw, pitch): east/north metres from the pad. cam([e,n,up],[e,n,up]).
  const VIEWS = W === 'phobos' ? [
    ['eye-airlock', `stand(27,3,Math.PI/2,-0.02)`], ['eye-tanks', `stand(27,-12,Math.PI*0.62,-0.02)`], ['eye-yard', `stand(12,27,0.25,0.0)`], ['eye-solar', `stand(0,-28,Math.PI,-0.02)`],
    ['eye-centre-east', `stand(6,0,Math.PI/2,0.02)`], ['eye-walker', `stand(27,18,0.9,-0.03)`],
    ['cam-hab', `cam([30,14,5],[44,2,2])`], ['cam-farm', `cam([30,-8,6],[46,-21,1.5])`], ['cam-yard', `cam([0,28,7],[14,45,1.5])`], ['cam-oven', `cam([62,-34,6],[54,-21,1])`],
    ['top-300', `cam([-30,-60,300],[14,0,0])`], ['top-90', `cam([-50,-70,90],[18,0,0])`],
  ] : [
    ['eye-camp', `stand(18,2,Math.PI/2,-0.02)`], ['eye-rig', `stand(30,-4,Math.PI*0.6,0.03)`], ['eye-centre', `stand(4,0,Math.PI/2,0.0)`], ['eye-shelter', `stand(28,10,Math.PI*0.45,0.0)`],
    ['cam-camp', `cam([18,-26,7],[40,-2,1.5])`], ['cam-rig', `cam([34,-20,4],[42,-11,2.5])`], ['cam-shelter', `cam([28,14,4],[38,5,1.2])`],
    ['top-300', `cam([-20,-50,300],[14,0,0])`], ['top-90', `cam([-40,-60,90],[18,0,0])`],
  ];
  for (const [tag, el, nv] of [['day', 35, 1], ['night', -30, 0]]) {
    if (process.env.ONLY && process.env.ONLY !== tag) continue;
    console.log(tag, JSON.stringify(await ev(`findSun(${el},${nv})`)));
    await ev(`cosmos.freeCam.showPlayer=false`);
    for (const [name, code] of VIEWS) {
      if (want && !want.has(pre + name + '-' + tag)) continue;
      await ev(code); await step(name.startsWith('eye') ? 40 : 15); await shot(pre + name + '-' + tag);
      await ev(`cosmos.freeCam.off()`);
    }
  }
  console.log('folk', JSON.stringify(await ev(`(()=>{const c=cosmos.space.worlds.get('${W}').client;return c?c.folk.members.map(m=>[m.body,+m.person.group.position.x.toFixed(1),+m.person.group.position.z.toFixed(1),m.person.group.visible,!!m.person.mixer]):null})()`)));
};
