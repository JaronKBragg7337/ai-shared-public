// Marineris Port, people at work (src/port/portPeople.js WALK_BEATS): the porter along the market, the pad hand, the fuel hand.
// node cshot.mjs webkit phone shots sc-walkers.mjs     (BASE=http://127.0.0.1:4383/  Q='&sky=afternoon')
export default async ({ shot, ev, step }) => {
  await step(10);
  const at = async (name, i, back, side) => {
    const r = await ev(`(()=>{const c=cosmos,s=c.port.site,P=c.port.people,w=P.walkers[${i}];if(!w)return 'no walker ${i}';
      for(let k=0;k<400&&!w.pose.moving;k++){P.clock+=1;c.step(1/30);}
      const q=w.pose,e=[q.x-Math.sin(q.yaw)*${back}+Math.cos(q.yaw)*${side},1.7,q.z-Math.cos(q.yaw)*${back}-Math.sin(q.yaw)*${side}];
      // stand the player's eye near the walker so the people system draws it
      c.ship.aboard=false;if(c.ship.seat)c.ship.stations.stand();Object.assign(c.walker.worldPos,s.toWorld(e[0],P.groundY(e[0],e[2])+.3,e[2]));c.walker.velocity={x:0,y:0,z:0};c.walker.grounded=true;
      {const gy=P.groundY(q.x,q.z);c.freeCam.set(s.toWorld(e[0],gy+e[1],e[2]),s.toWorld(q.x,gy+1.1,q.z));}for(let k=0;k<20;k++){c.step(1/30);P.tick(1/30,s.toWorld(e[0],1,e[2]));}c.step(0);
      return JSON.stringify({id:w.beat.id,x:+q.x.toFixed(1),z:+q.z.toFixed(1),moving:q.moving,vis:w.person.group.visible,n:P.walkers.length});})()`);
    console.log(name, r); await shot('p2-walker-' + name);
  };
  await at('porter', 0, -7, 2.5);
  await at('pad-hand', 1, -8, 3);
  await at('fuel-hand', 2, -7, 2.5);
};
