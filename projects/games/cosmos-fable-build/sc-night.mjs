// Night on Phobos (Sun well under the horizon), and Mars in its sky by day and by night. Run with Q='&sky=live'.
export default async ({ page, shot, ev, step, land, want }) => {
  await land(process.env.WORLD || 'phobos');
  await ev(`stand(28,-8,Math.PI/2,-0.06)`);
  await ev(`window.sunEl=()=>{const c=cosmos,f=c.walker.updateFrame(),s=c.space.sunLocal;return Math.asin(Math.max(-1,Math.min(1,s.x*f.up.x+s.y*f.up.y+s.z*f.up.z)))*180/Math.PI;};
    window.findSun=(deg,needVis)=>{const c=cosmos;let best=0,be=1e9;const day=${process.env.DAY_S || 27600};for(let s=0;s<day;s+=day/160){c.setSkyShift(s);c.step(1/30);const d=Math.abs(sunEl()-deg)+(needVis&&c.space.sky.state.vis<0.97?500:0);if(d<be){be=d;best=s;}}c.setSkyShift(best);for(let i=0;i<10;i++)c.step(1/30);return [best,sunEl(),c.space.sky.state.vis,c.space.sky.moonFill];}`);
  for (const [tag, el, nv] of [['night', -35, 0], ['day', 40, 1]]) {
    console.log(tag, JSON.stringify(await ev(`findSun(${el},${nv})`)));
    await ev(`stand(28,-8,-Math.PI/2,-0.04)`); await step(20); await shot('g1-eye-to-ship-' + tag);
    await ev(`stand(110,-20,Math.PI/2,-0.1,true)`); await step(30); await shot('g2-third-' + tag);
    await ev(`stand(130,-30,1.2,-0.3)`); await step(20); await shot('g3-eye-ground-' + tag);
    for (const [i, yaw] of [0, 1.57, 3.14, 4.71].entries()) { await ev(`stand(60,-30,${yaw},1.05)`); await step(10); await shot('g4-sky-' + i + '-' + tag); }
    await ev(`cam([-60,-40,14],[0,0,3])`); await step(10); await shot('g5-pad-' + tag);
    await ev(`cosmos.freeCam.off()`);
  }
};
