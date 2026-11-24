// Live scenario for live-check.mjs: Earth's and Callisto's yards are in the live build (11/21), the Prospectors' Camp stands at its port.
// node live-check.mjs shots/live-p4b live-yards2.mjs
export default async ({ page, prefix }) => {
  const go = (id, yard, side, cam, own) => page.evaluate(async ([id, yard, side, cam, own]) => {
    const c = window.cosmos, out = { id, yard };
    try {
      c.space.trip = null; c.ship.flight.override = null; c.space.debugStand(id); c.ship.aboard = false; for (let i = 0; i < 40; i++) c.step(1 / 30);
      const cl = c.space.worlds.get(id).client, y = cl[yard]; if (!y) { out.error = 'no yard'; return out; }
      if (id === 'callisto') { const d = (a, b) => Math.hypot(a.x - b.x, a.y - b.y, a.z - b.z); out.campToPortM = Math.round(d(cl.camp.portPi.point, c.space.worlds.get(id).body.ports[0].point)); }
      y.jumpTo(side, 'final', 0.8); for (let i = 0; i < 20; i++) c.step(1 / 30);
      const snd = y.soundStatus(); out.sound = snd && { owner: snd.owner, voice: snd.voices[0], cutoff: Math.round(snd.cutoff[0]) };
      y.jumpTo(side, 'landed', 0.5); for (let i = 0; i < 40; i++) c.step(1 / 30);
      const s = y.status(); out.built = s.built; out.ship = s.ships[0] && { reg: s.ships[0].registry, phase: s.ships[0].phase, ramp: +s.ships[0].ramp.toFixed(2) }; out.stock = s.stocks; out.board = s.board.draws;
      const pi = own ? y.pi : c.space.activeMoon.body.padInfo, o2f = (x, yy, z) => ({ x: pi.point.x + pi.east.x * x + pi.up.x * yy - pi.north.x * z, y: pi.point.y + pi.east.y * x + pi.up.y * yy - pi.north.y * z, z: pi.point.z + pi.east.z * x + pi.up.z * yy - pi.north.z * z });
      c.freeCam.set(o2f(cam[0], cam[1], cam[2]), o2f(cam[3], cam[4], cam[5])); for (let i = 0; i < 40; i++) c.step(1 / 30);
    } catch (e) { out.error = String(e); }
    out.wide = document.documentElement.scrollWidth <= window.innerWidth + 1;
    return out;
  }, [id, yard, side, cam, own]);
  for (const [id, yard, side, cam, own, tag] of [
    ['callisto', 'yard2', 'unbound', [8, 12, -22, 34, 2, 12], true, 'unbound'],
    ['callisto', 'yard', 'mystara', [58, 14, -30, 86, 2, 6], false, 'mystara'],
    ['earth', 'yard', 'homeguard', [30, 14, 62, 58, 2, 100], false, 'homeguard'],
    ['earth', 'yard', 'skyward', [-30, 14, 62, -58, 2, 100], false, 'skyward'],
  ]) { console.log('yard', JSON.stringify(await go(id, yard, side, cam, own))); await page.waitForTimeout(1500); await page.screenshot({ path: `${prefix}-live-yard-${tag}.png` }); }
};
