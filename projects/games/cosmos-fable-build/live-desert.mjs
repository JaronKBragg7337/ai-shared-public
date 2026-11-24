// Live scenario for live-check.mjs: the desert north of Marineris Port and the traffic's sound and dust are in the live build.
// node live-check.mjs shots/live-p2b live-desert.mjs
export default async ({ page, prefix }) => {
  const info = await page.evaluate(async () => {
    const c = window.cosmos, s = c.port.site, gy = (x, z) => c.portPeople.groundY(x, z);
    const w = c.walker; c.ship.aboard = false; Object.assign(w.worldPos, s.toWorld(428, gy(428, -622) + 0.05, -622)); w.velocity = { x: 0, y: 0, z: 0 }; w.grounded = true;
    try { c.freeCam.set(s.toWorld(428, gy(428, -622) + 1.7, -622), s.toWorld(403, gy(403, -640) + 4, -640)); } catch (e) { /* no free camera: the walker's own view will do */ }
    await new Promise((r) => setTimeout(r, 9000));
    const d = c.port.desert, st = d && d.status ? d.status() : null, fx = c.port.traffic && c.port.traffic.fx;
    return { desert: !!d, built: st && st.built, draws: st && st.drawCalls, fx: !!fx, fxStatus: fx && fx.status ? { tapped: fx.status().tapped, on: fx.status().on } : null };
  });
  console.log('desert', JSON.stringify(info));
  await page.screenshot({ path: prefix + '-live-desert-well.png' });
};
