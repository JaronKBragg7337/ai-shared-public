// Occator Works at work (src/worlds/ceres/activity.js): each side's people, ship, stockpile / gauges, and the standing board. Day and night.
// node cshot.mjs webkit phone shots sc-ceres-factions.mjs        (BASE=http://127.0.0.1:4384/  Q='&sky=live')
// ONLY=day|night picks one light; CHECKS=1 prints the timetable checks (pinned poses, wave-off, far-off, board redraws) and takes no pictures.
// Views are written in outpost metres [x east, y up, z south], as layout.js and activity.js are.
export default async ({ page, shot, ev, step, land, want }) => {
  const pre = 'p4-ceres-';
  await land('ceres');
  await ev(`(()=>{const c=cosmos,w=c.space.worlds.get('ceres');window.A=w.client.activity;
    window.V=(e,t)=>{cam([e[0],-e[2],e[1]],[t[0],-t[2],t[1]]);};
    window.sunEl=()=>{const f=c.walker.updateFrame(),s=c.space.sunLocal;return Math.asin(Math.max(-1,Math.min(1,s.x*f.up.x+s.y*f.up.y+s.z*f.up.z)))*180/Math.PI;};
    // the Sun deg degrees up, on the east side (morning) or the west (afternoon): the pictures are taken from the lit side
    window.findSun=(deg,needVis,east)=>{const pi=w.body.padInfo;let best=0,be=1e9;const day=32667;for(let s=0;s<day;s+=day/200){c.setSkyShift(s);c.step(1/30);const sl=c.space.sunLocal,e=sl.x*pi.east.x+sl.y*pi.east.y+sl.z*pi.east.z;const d=Math.abs(sunEl()-deg)+(needVis&&c.space.sky.state.vis<0.97?500:0)+((e>0)!==!!east?300:0);if(d<be){be=d;best=s;}}c.setSkyShift(best);for(let i=0;i<10;i++)c.step(1/30);return [best,+sunEl().toFixed(1),east?'east':'west'];};
    window.run=(n)=>{for(let i=0;i<n;i++)c.step(1/30);};
    // move the timetable until a hand is in a wanted state (the hands' beats run on the same clock)
    window.seek=(test,max=220)=>{for(let i=0;i<max;i++){A.shiftS+=1;c.step(1/30);if(test(A.status()))return true;}return false;};
    c.freeCam.showPlayer=false;stand(6,-10,0,0);})()`);
  await step(30);
  console.log('start', await ev(`JSON.stringify({tt:A.timetable(4),st:A.status()})`));
  if (process.env.CHECKS) {
    console.log('checks', await ev(`(async()=>{const c=cosmos,o={},m=await import('/src/worlds/ceres/activity.js');
      // the timetable is pure: the same world time gives the same pose and the same levels
      const T=1234567;o.pin=[60,200,300,420,560,700,900].map(d=>{const k=Math.floor((T+d)/m.SLOT_S),v=m.visitAt(k,{}),p=m.poseAt(v,T+d-v.start,{});return [k,v.side,m.PHASES[p.phase],+p.x.toFixed(2),+p.alt.toFixed(2),+p.z.toFixed(2),m.oreLevelAt(T+d),+m.waterLevelAt(T+d).toFixed(3)];});
      o.visit=[0,1].map(k=>{const v=m.visitAt(k,{});return {side:v.side,cruise:+v.t1.toFixed(1),brake:+(v.t2-v.t1).toFixed(1),hover:+(v.t3-v.t2).toFixed(1),final:+(v.t4-v.t3).toFixed(1),ground:+(v.t5-v.t4).toFixed(1),lift:+(v.t6-v.t5).toFixed(1),depart:+(v.t7-v.t6).toFixed(1),total:+v.end.toFixed(1),flareDeg:+(v.P.flare*57.3).toFixed(1)};});
      // one ship at a time over two whole slots
      let mx=0;for(let i=0;i<240;i++){A.shiftS+=5;run(1);mx=Math.max(mx,A.status().ships.length);}o.maxShipsAlive=mx;
      // the player's ship parked on the hauler's stand: the visit is waved off
      const pi=c.space.worlds.get('ceres').body.padInfo,keep={...c.ship.flight.pos},S=m.SPOTS.ironclad,q=P(S.x,-S.z,2);
      Object.assign(c.ship.flight.pos,q);A.jumpTo('ironclad','braking',0.5);run(3);const a=A.status().ships[0];o.blockedOnApproach=a&&{phase:a.phase,diverted:a.diverted};
      A.jumpTo('ironclad','landed',0.3);run(3);o.blockedLanded=A.status().ships.length;o.oreWhenWavedOff=A.status().ore;
      Object.assign(c.ship.flight.pos,keep);A.jumpTo('ironclad','landed',0.3);run(3);o.clearLanded=A.status().ships.map(x=>x.phase+':'+x.registry);
      // far away nothing is drawn or ticked
      V([0,300,7000],[0,0,0]);run(3);o.far={active:A.active,rootVisible:A.root.visible};V([-30,3,-80],[-40,1,-100]);run(3);o.near={active:A.active,rootVisible:A.root.visible};
      // the board: solo says no report; a shared world's numbers are drawn once and again only when they change
      o.boardSolo={...A.status().board};
      const home={balance:40,wealth:20,industry:30,defences:20,population:22};A.setContext({world:{snapshot:{homes:{ceres:home},ships:{}}}});A.shiftS+=2;run(2);o.boardShared={...A.status().board};
      A.shiftS+=5;run(5);o.boardSame=A.status().board.draws;home.balance=62;A.shiftS+=2;run(2);o.boardChanged={...A.status().board};
      A.setContext({world:undefined});A.shiftS+=2;run(2);o.boardBack=A.status().board.key;
      // frame cost with everything in view
      V([-20,2,-86],[-45,2,-100]);const tm=(n)=>{let s=0,x=0;for(let i=0;i<n;i++){const t=performance.now();c.step(1/30);const d=performance.now()-t;s+=d;if(d>x)x=d;}return [+(s/n).toFixed(1),+x.toFixed(1)];};o.frames=tm(90);
      let calls=0,tris=0;A.root.traverse(x=>{if(x.isMesh&&x.visible&&x.geometry){let p=x,vis=true;while(p){if(!p.visible)vis=false;p=p.parent;}if(vis){calls++;const g=x.geometry;tris+=(g.index?g.index.count:g.attributes.position.count)/3;}}});o.drawn={meshes:calls,tris:Math.round(tris)};
      o.buildMs=A.status().buildMs;o.hands=A.status().hands.length;
      return JSON.stringify(o);})()`));
    return;
  }
  const S = async (name, code, n = 14) => { if (want && !want.has(name)) return; const r = await ev(code); await step(n); if (r) console.log(name, typeof r === 'string' ? r : JSON.stringify(r)); await shot(name); };
  const ship = `(()=>{const s=A.status().ships[0];return s?JSON.stringify({side:s.side,reg:s.registry,phase:s.phase,alt:+s.alt.toFixed(1),pitch:+(s.pitch*57.3).toFixed(1),yaw:+(s.yaw*57.3).toFixed(0),gear:+s.gear.toFixed(2),ramp:+s.ramp.toFixed(2),hose:s.hose,ore:A.status().ore,water:+A.status().water.toFixed(2)}):'no ship';})()`;
  const hand = (id, test) => `seek(s=>{const h=s.hands.find(x=>x.id==='${id}');return h&&h.shown&&(${test});});`;
  for (const [tag, el, nv] of [['day', 32, 1], ['night', -30, 0]]) {
    if (process.env.ONLY && process.env.ONLY !== tag) continue;
    const N = (n) => pre + n + '-' + tag;
    // ---- Ironclad (morning light: seen from the foundry side): the yard, the skip, the hands; the hauler on final and down; the bunker full and nearly empty
    console.log(tag, JSON.stringify(await ev(`findSun(${el},${nv},true)`)));
    await S(N('01-ironclad-yard-full'), `A.jumpTo('ironclad','braking',0.1);V([-29.5,2.4,-90],[-41,1.2,-100]);${hand('skip-hand', 'h.phase===0&&h.z<-91&&h.z>-94')}${ship}`);
    await S(N('02-ironclad-skip-tipping'), `V([-33.2,1.7,-99.2],[-38,1.0,-101.2]);${hand('skip-hand', 'h.phase===1')}A.shiftS+=3.4;run(2);${ship}`);
    await S(N('03-ironclad-hands-door'), `V([-14,1.7,-79.5],[-21,1.2,-85.5]);${hand('yard-hand', "h.anim==='Walk'&&h.x<-17&&h.x>-21")}${ship}`);
    await S(N('04-ironclad-hauler-final'), `A.jumpTo('ironclad','final',0.55);run(3);V([-30.5,1.7,-91],[-60,16,-124]);${ship}`);
    await S(N('05-ironclad-hauler-landed'), `A.jumpTo('ironclad','landed',0.12);run(3);V([-31,2,-93],[-58,5,-118]);${ship}`);
    await S(N('06-ironclad-hauler-ramp'), `A.jumpTo('ironclad','landed',0.5);run(3);V([-49,1.8,-82.5],[-60,3,-100]);${hand('stand-hand', "h.x<-44")}${ship}`);
    await S(N('07-ironclad-yard-low'), `A.jumpTo('ironclad','landed',0.84);run(3);V([-29.5,2.4,-90],[-41,1.2,-100]);${ship}`);
    await S(N('08-ironclad-hauler-lifting'), `A.jumpTo('ironclad','lifting',0.75);run(3);V([-30.5,1.7,-91],[-60,26,-124]);${ship}`);
    await S(N('20-pad-to-foundry'), `V([-2,1.7,-34],[-6,2.5,-84]);''`);
    // ---- Greenhaven (afternoon light: seen from the pad side): the grow hall and the trolley, the tanks and their gauges, the tender on final and down with its hose
    console.log(tag, JSON.stringify(await ev(`findSun(${el},${nv},false)`)));
    await S(N('09-greenhaven-grow-hall'), `V([22,1.8,34],[33,2.6,50]);${ship}`);
    await S(N('10-greenhaven-trolley'), `V([42.5,1.8,60.5],[49.5,1.1,57]);${hand('filter-hand', 'h.phase===0&&h.x>47.5&&h.x<49.5')}${ship}`);
    await S(N('11-greenhaven-tanks-low'), `A.jumpTo('greenhaven','braking',0.5);run(3);V([60,1.8,50],[62.5,3.0,64]);${ship}`);
    await S(N('12-greenhaven-tender-final'), `A.jumpTo('greenhaven','final',0.5);run(3);V([47,1.8,63],[63,9,90]);${ship}`);
    await S(N('13-greenhaven-tender-landed-hose'), `A.jumpTo('greenhaven','landed',0.45);run(3);V([47.5,1.9,74],[61,2.2,86]);${ship}`);
    await S(N('14-greenhaven-tanks-full'), `A.jumpTo('greenhaven','landed',0.95);run(3);V([60,1.8,50],[62.5,3.0,64]);${ship}`);
    await S(N('15-greenhaven-hands-valve'), `V([72,1.8,54],[76,1.2,62.5]);${hand('valve-hand', "h.anim==='Walk'&&h.x>74&&h.x<77")}${ship}`);
    await S(N('16-greenhaven-salt-trays'), `V([22,3.2,58],[35,0.3,67]);${ship}`);
    // ---- between them: the standing board (solo: no report; then with a shared world's numbers), and the pad left clear
    await S(N('17-board-no-report'), `A.setContext({world:undefined});A.shiftS+=2;run(2);V([-12,1.75,25.5],[-12,2.1,34]);JSON.stringify(A.status().board)`);
    await S(N('18-board-shared'), `A.setContext({world:{snapshot:{homes:{ceres:{balance:40,wealth:20,industry:30,defences:20,population:22}},ships:{}}}});A.shiftS+=2;run(2);V([-12,1.75,25.5],[-12,2.1,34]);JSON.stringify(A.status().board)`);
    await ev(`A.setContext({world:undefined})`);
    await S(N('19-pad-to-roth'), `V([4,1.7,26],[30,1.3,44]);''`);
    await S(N('21-top'), `A.jumpTo('ironclad','landed',0.4);run(3);V([0,260,40],[0,0,-10]);''`);
  }
  console.log('end', await ev(`JSON.stringify(A.status())`));
};
