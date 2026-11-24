// Marineris Port ambient traffic (src/port/traffic.js): a ship on approach, on final, landed with the ramp down, lifting off, and the apron tug.
// node cshot.mjs webkit phone shots/p2-traffic sc-traffic.mjs      (BASE=http://127.0.0.1:4382/  Q='&sky=afternoon')
// TAG names the run; PIN=<seconds> pins the timetable clock to an absolute world time and prints every ship's pose (two loads must agree).
export default async ({ page, shot, ev, step, phone }) => {
  const tag = process.env.TAG || 'x';
  if (phone && !process.env.NORESIZE) { await page.setViewportSize({ width: 375, height: 812 }); await page.waitForTimeout(500); }
  await ev(`(()=>{const c=cosmos,s=c.port.site,T=c.port.traffic;
    window.TR={T,
      cam(e,t){c.freeCam.set(s.toWorld(e[0],e[1],e[2]),s.toWorld(t[0],t[1],t[2]));},
      ship(){const st=T.status();return st.ships[0]||null;},
      go(phase,o,e,off){const j=T.jumpTo(phase,o);for(let i=0;i<3;i++)c.step(1/30);const sh=TR.ship();if(!sh)return JSON.stringify({j,none:T.status()});
        const eye=e||[sh.x+off[0],Math.max(1.7,sh.y+off[1]),sh.z+off[2]];TR.cam(eye,[sh.x,sh.y+(off&&off[3]||0),sh.z+(off&&off[4]||0)]);for(let i=0;i<10;i++)c.step(1/30);
        const s2=TR.ship();return JSON.stringify({j,phase:s2.phase,alt:+s2.alt.toFixed(1),y:+s2.y.toFixed(2),gear:+s2.gear.toFixed(2),ramp:+s2.ramp.toFixed(2),lift:+s2.lift.toFixed(2),main:+s2.main.toFixed(2),pitch:+(s2.pitch*57.3).toFixed(1),yaw:+(s2.yaw*57.3).toFixed(1),d:Math.round(Math.hypot(s2.x-eye[0],s2.z-eye[2]))});}};
  })()`);
  await step(10);
  console.log('start', await ev(`JSON.stringify({tt:TR.T.timetable(5),st:TR.T.status()})`));
  if (process.env.PIN) {
    for (const off of [60, 110, 125, 200, 340, 380]) {
      const r = await ev(`(()=>{const T=TR.T;T.shiftS=0;T.shiftS=${+process.env.PIN + off}-T.time();for(let i=0;i<3;i++)cosmos.step(1/30);const st=T.status();return JSON.stringify(st.ships.map(s=>[s.n,s.type,s.spot,s.phase,(st.time-${+process.env.PIN + off}).toFixed(2),s.t,s.x.toFixed(2),s.y.toFixed(2),s.z.toFixed(2),s.yaw.toFixed(3)]).concat([['tug',st.vehicle.x.toFixed(2),st.vehicle.z.toFixed(2),st.vehicle.stop]]));})()`);
      console.log('PIN+' + off, r);
    }
    return;
  }
  if (process.env.CHECKS) {
    console.log('checks', await ev(`(()=>{const T=TR.T,c=cosmos,s=c.port.site,out={};const run=(n)=>{for(let i=0;i<n;i++)c.step(1/30);};
      TR.cam([-150,1.7,30],[-190,20,-50]);
      // a player's ship parked on the hauler's spot: the visit is waved off (overflies, never lands)
      T.setContext({ship:{flight:{pos:s.toWorld(-190,2.2,-50)}}});T.jumpTo('braking',{type:'hauler',into:0.5});run(3);const a=T.status().ships[0];out.blockedOnApproach={phase:a.phase,diverted:a.diverted};
      const v=T.visits[a.n&3];T.shiftS+=v.t3+6-a.t;run(3);const b=T.status().ships[0];out.afterHover={phase:b.phase,alt:Math.round(b.alt),t:b.t};
      // joining while it would already be on the ground there: left out
      T.jumpTo('landed',{type:'hauler'});run(3);out.blockedLanded=T.status().ships.length;
      T.setContext({ship:c.ship});T.jumpTo('landed',{type:'hauler'});run(3);out.clearLanded=T.status().ships.map(x=>x.phase);
      // the opening hides it; so does distance
      T.setContext({opening:()=>({active:true})});run(2);out.opening={active:T.active,rootVisible:T.root.visible};T.setContext({opening:()=>c.opening});run(2);out.back=T.active;
      c.freeCam.set(s.toWorld(0,300,9000),s.toWorld(0,0,0));run(3);out.far={active:T.active,rootVisible:T.root.visible};
      TR.cam([-150,1.7,30],[-190,20,-50]);run(3);out.near={active:T.active,ships:T.status().ships.length,pool:T.pool.length};
      return JSON.stringify(out);})()`));
    return;
  }
  // the hauler on Apron A north: watched from the arrivals walkway
  const H = `{type:'hauler'}`;
  console.log('approach-far', await ev(`TR.go('braking',{type:'hauler',into:0.35},[-150,1.7,30])`)); await shot('p2-traffic-1-approach-far-' + tag);
  console.log('approach', await ev(`TR.go('braking',{type:'hauler',into:0.9},[-150,1.7,30])`)); await shot('p2-traffic-2-approach-' + tag);
  console.log('hover', await ev(`TR.go('hover',{type:'hauler',into:0.5},[-150,1.7,30])`)); await shot('p2-traffic-3-hover-' + tag);
  console.log('final', await ev(`TR.go('final',{type:'hauler',into:0.72},[-150,1.7,20])`)); await shot('p2-traffic-4-final-' + tag);
  console.log('touch', await ev(`TR.go('landed',{type:'hauler',into:0.004},null,[34,-0.6,30,0,8])`)); await shot('p2-traffic-5-touchdown-' + tag);
  console.log('landed', await ev(`TR.go('landed',{type:'hauler',into:0.3},null,[26,-0.6,64,0,16])`)); await shot('p2-traffic-6-landed-ramp-' + tag);
  console.log('landed-gear', await ev(`TR.go('landed',{type:'hauler',into:0.3},null,[13,-0.6,-15,-1.6,-6])`)); await shot('p2-traffic-7-landed-gear-' + tag);
  console.log('lifting', await ev(`TR.go('lifting',{type:'hauler',into:0.6},[-150,1.7,20])`)); await shot('p2-traffic-8-lifting-' + tag);
  console.log('departing', await ev(`TR.go('departing',{type:'hauler',into:0.16},[-150,1.7,20])`)); await shot('p2-traffic-9-departing-' + tag);
  // the courier on Pad 03, from the taxi spine
  console.log('courier-final', await ev(`TR.go('final',{type:'courier',spot:'pad-03',into:0.8},[36,1.7,52])`)); await shot('p2-traffic-10-courier-final-' + tag);
  console.log('courier-landed', await ev(`TR.go('landed',{type:'courier',spot:'pad-03',into:0.3},null,[-17,-0.2,24,0,4])`)); await shot('p2-traffic-11-courier-landed-' + tag);
  // the tug: driving the south lane, and stopped at the depot
  const veh = async (name, want) => { console.log(name, await ev(`(()=>{const T=TR.T,c=cosmos;for(let i=0;i<4000;i++){const v=T.status().vehicle;if(${want})break;T.shiftS+=0.25;}
      const v=T.status().vehicle;TR.cam([v.x+7,1.7,v.z+9],[v.x,0.9,v.z+1.5]);for(let i=0;i<10;i++)c.step(1/30);return JSON.stringify(T.status().vehicle);})()`)); await shot(name + '-' + tag); };
  await veh('p2-traffic-12-tug-driving', `v.speed>3.4&&v.z>47.5&&v.x>-25&&v.x<-10`);
  await veh('p2-traffic-13-tug-depot', `v.stop==='depot'`);
  await veh('p2-traffic-14-tug-turn', `v.speed>3.4&&v.x>19&&v.z>40&&v.z<46`);
  // frame time around a spawn (the first build of a class, then a later visit that reuses it)
  console.log('frames', await ev(`(()=>{const T=TR.T,c=cosmos;TR.cam([-150,1.7,30],[-190,20,-50]);const run=(n)=>{let mx=0,sum=0;for(let i=0;i<n;i++){const t=performance.now();c.step(1/30);const d=performance.now()-t;sum+=d;if(d>mx)mx=d;}return [+(sum/n).toFixed(1),+mx.toFixed(1)];};
    run(150);const out={built:T.pool.length,buildMs:T.status().buildMs};T.jumpTo('cruise',{type:'hauler',into:0});T.shiftS-=3;out.before=run(40);T.shiftS+=3.2;out.spawn=run(5);out.after=run(40);out.ships=T.status().ships.map(s=>s.phase);return JSON.stringify(out);})()`));
  console.log('end', await ev(`JSON.stringify(TR.T.status().buildMs)`));
};
