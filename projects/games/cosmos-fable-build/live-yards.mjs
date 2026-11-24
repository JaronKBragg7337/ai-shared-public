// Live scenario for live-check.mjs: the Moon's yards are in the live build and build at Shackleton.
// node live-check.mjs shots/live-p4 live-yards.mjs
export default async ({ page, prefix }) => {
  const info = await page.evaluate(async () => {
    const c = window.cosmos, out = {};
    try {
      c.space.debugStand('moon-shackleton'); c.ship.aboard = false; for (let i = 0; i < 40; i++) c.step(1 / 30);
      const y = c.space.worlds.get('moon-shackleton').client.yard;
      y.jumpTo('fortis', 'landed', 0.5); for (let i = 0; i < 40; i++) c.step(1 / 30);
      const s = y.status(); out.built = s.built; out.ship = s.ships[0] && { reg: s.ships[0].registry, phase: s.ships[0].phase, ramp: +s.ships[0].ramp.toFixed(2) }; out.stock = s.stocks; out.board = s.board;
      const pi = c.space.activeMoon.body.padInfo, o2f = (x, yy, z) => ({ x: pi.point.x + pi.east.x * x + pi.up.x * yy - pi.north.x * z, y: pi.point.y + pi.east.y * x + pi.up.y * yy - pi.north.y * z, z: pi.point.z + pi.east.z * x + pi.up.z * yy - pi.north.z * z });
      c.freeCam.set(o2f(-2, 16, 34), o2f(-28, 2, 72)); for (let i = 0; i < 40; i++) c.step(1 / 30);
    } catch (e) { out.error = String(e); }
    out.wide = document.documentElement.scrollWidth <= window.innerWidth + 1;
    return out;
  });
  console.log('yards', JSON.stringify(info));
  await page.screenshot({ path: prefix + '-live-yard-shackleton.png' });
};
