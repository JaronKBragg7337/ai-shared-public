// A moon by day on the REAL clock, moved to a low Sun (about 20 deg) and a high one (about 60 deg): pad, rocks, underfoot, third person, the ship, the approach.
// Run with Q='&sky=live'. WORLD=phobos|deimos|moon|ceres|callisto
export default async ({ page, shot, ev, step, land, want }) => {
  await land(process.env.WORLD || 'phobos');
  await ev(`stand(28,-8,Math.PI/2,-0.06)`);
  await ev(`window.sunEl=()=>{const c=cosmos,f=c.walker.updateFrame(),s=c.space.sunLocal;return Math.asin(Math.max(-1,Math.min(1,s.x*f.up.x+s.y*f.up.y+s.z*f.up.z)))*180/Math.PI;};
    window.findSun=(deg)=>{const c=cosmos;let best=0,be=1e9;const day=${process.env.DAY_S || 27600};for(let s=0;s<day;s+=day/160){c.setSkyShift(s);c.step(1/30);const d=Math.abs(sunEl()-deg)+(c.space.sky.state.vis>0.97?0:500);if(d<be){be=d;best=s;}}c.setSkyShift(best);for(let i=0;i<10;i++)c.step(1/30);return [best,sunEl()];}`);
  for (const [tag, el] of [['low', 20], ['high', 60]]) {
    console.log(tag, 'sun', JSON.stringify(await ev(`findSun(${el})`)));
    await ev(`cosmos.freeCam.showPlayer=false`);
    await ev(`stand(28,-8,Math.PI/2,-0.06)`); await step(20); await shot('p1-eye-pad-' + tag);
    await ev(`stand(130,-30,1.2,-0.05)`); await step(20); await shot('p2-eye-rocks-' + tag);
    await ev(`stand(-40,34,-2.2,-0.12)`); await step(20); await shot('p3-eye-boulder-' + tag);
    await ev(`stand(130,-30,1.2,-0.9)`); await step(20); await shot('p4-underfoot-' + tag);
    await ev(`stand(110,-20,Math.PI/2,-0.1,true)`); await step(30); await shot('p5-third-' + tag);
    await ev(`cam([-32,-20,2.2],[0,0,4])`); await step(10); await shot('p6-ship-' + tag);
    await ev(`cam([-140,-110,60],[0,0,3])`); await step(10); await shot('p7-final-' + tag);
    await ev(`cosmos.freeCam.off()`);
  }
};
