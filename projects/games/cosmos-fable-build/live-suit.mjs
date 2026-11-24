// live scenario: land on Phobos, third person, walk; report whether the suit is on
export default async ({ page, prefix }) => {
  await page.evaluate(() => { const c = cosmos; c.space.debugLand('phobos'); for (let i = 0; i < 20; i++) c.step(1 / 30);
    const mw = c.space.worlds.get('phobos'), b = mw.body, pi = b.padInfo, w = c.walker;
    const P = (e, n, u = 0) => { const x = pi.point.x + pi.east.x * e + pi.north.x * n, y = pi.point.y + pi.east.y * e + pi.north.y * n, z = pi.point.z + pi.east.z * e + pi.north.z * n, l = Math.hypot(x, y, z), R = b.surfaceRadius(x / l, y / l, z / l) + u; return { x: x / l * R, y: y / l * R, z: z / l * R }; };
    c.ship.aboard = false; if (c.ship.seat) c.ship.stations.stand(); Object.assign(w.worldPos, P(110, -20, 0.03)); w.velocity = { x: 0, y: 0, z: 0 }; w.yaw = Math.PI / 2; w.pitch = -0.1; w.grounded = true; c.view.mode = 'third'; mw.force(w.worldPos); for (let i = 0; i < 40; i++) c.step(1 / 30); });
  await page.waitForTimeout(1500);
  console.log('suit on:', await page.evaluate(() => !!cosmos.playerPerson.suit, null), 'gait:', await page.evaluate(() => cosmos.playerPerson.gait));
  await page.screenshot({ path: prefix + '-live-solo.png' });
};
