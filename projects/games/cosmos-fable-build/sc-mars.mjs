// Mars port as it is at the URL's hour (Q='&sky=night' / dusk / noon): spawn view, open ground, third person
export default async ({ page, shot, ev, step }) => {
  const tag = process.env.TAG || 'x';
  await step(20); await shot('m1-spawn-' + tag);
  await ev(`(()=>{const c=cosmos,w=c.walker,p=c.port.site.toWorld(200,0.3,250);c.ship.aboard=false;if(c.ship.seat)c.ship.stations.stand();Object.assign(w.worldPos,p);w.velocity={x:0,y:0,z:0};w.yaw=2.4;w.pitch=0.05;c.view.mode='third';})()`); await step(40); await shot('m2-open-' + tag);
  await ev(`(()=>{const c=cosmos,w=c.walker;w.yaw=5.2;w.pitch=0.3;c.view.mode='first';})()`); await step(20); await shot('m3-sky-' + tag);
};
