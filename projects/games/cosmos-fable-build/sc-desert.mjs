// The desert round Marineris Port (src/port/desert.js) and the traffic's sound and dust (src/port/trafficFx.js).
// node cshot.mjs webkit phone shots sc-desert.mjs      (BASE=http://127.0.0.1:4385/  Q='&sky=afternoon' or '&sky=night')
// TAG names the run (day / night). ONLY=a,b picks views. SOUND=1 (chromium) checks the sound nodes instead of taking pictures.
export default async ({ page, shot, ev, step, phone }) => {
  const tag = process.env.TAG || 'x', only = process.env.ONLY ? new Set(process.env.ONLY.split(',')) : null;
  await ev(`(()=>{const c=cosmos,s=c.port.site;
    window.D={
      gy(x,z){return c.portPeople.groundY(x,z);},
      // put the player (and so the fine terrain) at a port-local spot, look from eye height toward a target [x, height above its ground, z]
      view(e,t,up){const ey=D.gy(e[0],e[1])+(up??1.7);const w=c.walker;c.ship.aboard=false;Object.assign(w.worldPos,s.toWorld(e[0],D.gy(e[0],e[1])+0.03,e[1]));w.velocity={x:0,y:0,z:0};w.grounded=true;
        c.freeCam.set(s.toWorld(e[0],ey,e[1]),s.toWorld(t[0],D.gy(t[0],t[2])+t[1],t[2]));
        for(let i=0;i<6;i++)c.step(1/30);try{c.rebuildNear(true);c.flushTerrain();}catch(e){}for(let i=0;i<40;i++)c.step(1/30);
        const d=c.port.desert,st=d&&d.status?d.status():null;return JSON.stringify({eye:[e[0],+ey.toFixed(1),e[1]],built:st&&st.built,tris:st&&st.tris,draws:st&&st.drawCalls,ms:st&&st.buildMs,people:st&&st.people.filter(p=>p.shown)});}};
  })()`);
  await step(10);
  const V = async (name, e, t, up) => { if (only && !only.has(name)) return; console.log(name, await ev(`D.view(${JSON.stringify(e)},${JSON.stringify(t)},${up ?? 'undefined'})`)); await page.waitForTimeout(1500); await step(20); await shot('p2-desert-' + name + '-' + tag); };
  if (process.env.SOUND) { await page.keyboard.press('Shift'); await page.waitForTimeout(300); await step(5); console.log('sound', await ev(`(async()=>{${SOUND}})()`)); return; }
  await V('01-road-from-port', [86, -62], [98, 1, -150]);
  await V('02-borrow', [143, -212], [166, 1.5, -224]);
  await V('03-solar', [283, -238], [322, 0.5, -270]);
  await V('04-solar-rows', [296, -264], [330, 0.6, -264.5]);
  await V('05-well', [428, -622], [403, 4, -640]);
  await V('06-well-head', [405.5, -628.5], [399.5, 3, -640]);
  await V('07-pipeline', [150, -262], [215, 1, -385]);
  await V('08-pipe-at-farm', [78, -98], [60, 0.8, -79]);
  await V('09-mast', [496, -706], [508, 6, -719]);
  await V('10-landing', [449, -1283], [464, 1.2, -1302]);
  await V('11-landing-plaque', [457.4, -1293.2], [458.5, 0.95, -1294.6]);
  await V('12-up400-port-side', [190, -230], [215, 0, -250], 400);
  await V('13-up400-well', [420, -640], [430, 0, -660], 400);
  await V('14-road-mid', [258, -372], [250, 0.5, -400]);
  await V('17-road-to-landing', [342, -985], [395, 1, -1035]);
  if (!only || only.has('dust')) {
    console.log('dust', await ev(`(()=>{const c=cosmos,s=c.port.site,T=c.port.traffic;const w=c.walker;Object.assign(w.worldPos,s.toWorld(-150,0.03,20));for(let i=0;i<6;i++)c.step(1/30);try{c.rebuildNear(true);}catch(e){}
      const j=T.jumpTo('final',{type:'hauler',into:${process.env.INTO || 0.86}});for(let i=0;i<3;i++)c.step(1/30);c.freeCam.set(s.toWorld(-150,1.7,20),s.toWorld(-190,8,-50));for(let i=0;i<20;i++)c.step(1/30);const st=T.status().ships[0];return JSON.stringify({j,phase:st&&st.phase,alt:st&&st.alt,fx:T.fx&&T.fx.status?T.fx.status():null});})()`));
    await shot('p2-desert-15-ship-final-dust-' + tag);
    console.log('dust-lift', await ev(`(()=>{const c=cosmos,T=c.port.traffic;T.jumpTo('lifting',{type:'hauler',into:0.35});for(let i=0;i<20;i++)c.step(1/30);const st=T.status().ships[0];return JSON.stringify({phase:st&&st.phase,alt:st&&st.alt,fx:T.fx&&T.fx.status?T.fx.status():null});})()`));
    await shot('p2-desert-16-ship-lift-dust-' + tag);
  }
};
const SOUND = `
  const c=cosmos,s=c.port.site,T=c.port.traffic,F=T.fx,out={};const run=(n)=>{for(let i=0;i<n;i++)c.step(1/30);};const wait=(ms)=>new Promise(r=>setTimeout(r,ms));
  const w=c.walker;c.ship.aboard=false;Object.assign(w.worldPos,s.toWorld(-150,0.03,20));c.freeCam.set(s.toWorld(-150,1.7,20),s.toWorld(-190,8,-50));run(5);
  out.before=F.status();
  for(const [name,phase,into] of [['cruise-far','cruise',0.05],['braking','braking',0.8],['hover','hover',0.5],['final','final',0.8],['touchdown','landed',0.0002],['landed-quiet','landed',0.4],['lifting','lifting',0.5],['departing','departing',0.5]]){
    const j=T.jumpTo(phase,{type:'hauler',into});run(3);const f0=F.status(),sh=T.status().ships.find(x=>x.n===j.n),k=f0.dist.findIndex(d=>sh&&Math.abs(d-Math.hypot(sh.x+150,sh.y-1.7,sh.z-20))<3);
    await wait(700);run(2);const f=F.status();out[name]={phase:sh&&sh.phase,alt:sh&&Math.round(sh.alt),distM:k<0?null:Math.round(f0.dist[k]),wantGain:k<0?null:f0.voices[k],cutoffHz:k<0?null:Math.round(f0.cutoff[k]),wantThump:k<0?null:f0.thump[k],realGainAfter700ms:k<0?null:f.real[k]};}
  // the tug: beside it, then 60 m off
  {const v=T.status().vehicle;Object.assign(w.worldPos,s.toWorld(v.x+6,0.03,v.z));c.freeCam.set(s.toWorld(v.x+6,1.7,v.z),s.toWorld(v.x,1,v.z));for(let i=0;i<4000;i++){if(T.status().vehicle.speed>3)break;T.shiftS+=0.25;}
   const v2=T.status().vehicle;c.freeCam.set(s.toWorld(v2.x+6,1.7,v2.z),s.toWorld(v2.x,1,v2.z));run(4);await wait(500);run(2);out.tugNear=F.status().tug;c.freeCam.set(s.toWorld(v2.x+60,1.7,v2.z),s.toWorld(v2.x,1,v2.z));run(4);await wait(500);run(2);out.tugFar=F.status().tug;}
  // sound switched off in Settings
  {const a=c.ship.audio;if(a){a.setOn(false);run(4);await wait(400);run(2);out.off=F.status().master;a.setOn(true);run(4);}}
  out.after=F.status();return JSON.stringify(out);`;
