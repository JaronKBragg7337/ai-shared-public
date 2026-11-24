// Live check scenario for the 11/23 work (run by live-check.mjs in a solo dev session on the LIVE site at phone width).
// A solo world has no jobs, so this proves what the client alone can prove: the live modules hold the tally runs and the yard book, the book agrees with
// the yard the live page draws, and Keep walking is there. A tally run taken and paid on the live server waits for the server's restart (live-run.mjs).
export default async ({ page, prefix }) => {
  const mods = await page.evaluate(async () => {
    const base = new URL('.', location.href).href;
    const C = await import(base + 'src/missions/catalog.js'), YB = await import(base + 'src/worlds/yardBook.js');
    const fr = C.MISSIONS.filter((m) => m.repeat), ta = fr.filter((m) => m.steps[0].k === 'count');
    return { freight: fr.length, tallies: ta.map((m) => m.id), book: Object.keys(YB.TALLIES).length, nextEl: !!document.getElementById('hud-next'), keep: !!(window.cosmos && cosmos.keepWalking), card: typeof cosmos.tallyUI };
  });
  console.log('live modules', JSON.stringify(mods));
  // stand on Earth and compare what the live page draws with the book, at a dozen moments of the timetable
  await page.evaluate(() => { const c = cosmos; c.space.trip = null; c.ship.flight.override = null; c.space.debugStand('earth'); c.ship.aboard = false; for (let i = 0; i < 30; i++) c.step(1 / 30); });
  await page.waitForFunction(() => { const w = cosmos.space.worlds.get('earth'); return w && w.client && w.client.yard && w.client.yard.built; }, null, { timeout: 120000 });
  const agree = await page.evaluate(async () => {
    const base = new URL('.', location.href).href, YB = await import(base + 'src/worlds/yardBook.js');
    const y = cosmos.space.worlds.get('earth').client.yard, rows = []; let ok = true; const s0 = y.shiftS;
    for (let k = 0; k < 12; k++) { y.shift(127); for (let i = 0; i < 3; i++) cosmos.step(1 / 30); const st = y.status(), a = [st.stocks[0], st.stocks[1]], b = [Math.round(YB.tallyTruth('skyward', st.time)), Math.round(YB.tallyTruth('homeguard', st.time))]; rows.push(a.join('/') + '=' + b.join('/')); if (a[0] !== b[0] || a[1] !== b[1]) ok = false; }
    y.shiftS = s0; return { ok, rows, ship: YB.yardShipWords('skyward', y.time()) };
  });
  console.log('live yard against the book', JSON.stringify(agree));
  // Keep walking: two seconds of the stick in its run zone, and the button is there
  await page.evaluate(() => { const t = cosmos.keepWalking.touch; t.active = true; t.moveNorth = 1; t.run = true; });
  await page.waitForTimeout(2600);
  const kw = await page.evaluate(() => { const r = document.getElementById('btn-keepwalk').getBoundingClientRect(); return { ...cosmos.keepWalking.status(), w: Math.round(r.width), h: Math.round(r.height), sw: document.documentElement.scrollWidth, iw: innerWidth }; });
  await page.screenshot({ path: prefix + '-live-keep-walking.png' });
  await page.evaluate(() => { const t = cosmos.keepWalking.touch; t.active = false; t.moveNorth = 0; t.run = false; });
  console.log('live keep walking', JSON.stringify(kw));
};
