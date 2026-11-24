// The well run on the LIVE server, by taps. The ground is covered in short straight hops at 8 m/s (H.hopTo: the blind walker could not find its way round the
// port buildings in 15 minutes); everything else is what a player does: ask the supply clerk, read the board, take "Well samples", walk the haul road to the ice well,
// walk back, read the pay line and the ticket. Logs what the screens actually say.
const ROAD = [[90, -90], [100, -175], [140, -210], [180, -205], [195, -260], [265, -330], [245, -405], [350, -470], [385, -465], [405, -500], [407, -600], [407, -617]];
export default async ({ page, shot, log, sleep, H }) => {
  const tap = async (sel) => { const b = page.locator(sel).first(); await b.scrollIntoViewIfNeeded(); await b.tap(); await sleep(1200); };
  const clerk = await page.evaluate(async () => { const W = await import('/games/the-cosmos/src/missions/where.js'); const p = W.resolve('depot-clerk'); return p && { x: p.x, z: p.z, kind: p.kind }; });
  log('clerk', clerk, 'me', await H.me());
  const talk = async () => {
    await page.waitForFunction(() => { const b = document.querySelector('#crew-talk'); return b && b.style.display !== 'none' && /Supply/.test(b.innerText); }, null, { timeout: 40000 });
    await tap('#crew-talk'); await page.waitForSelector('#crew-panel', { state: 'visible' }); await sleep(600);
  };
  const toClerk = async () => { let r = await H.hopTo(clerk.x + 1.4, clerk.z, 2.2, 900); if (!r.ok) { log('clerk walk', r); r = await H.hopTo(clerk.x + 1.4, clerk.z + 3, 3, 200); } return r; };
  const me0 = await H.me();
  if (!me0.active) {
    await page.keyboard.down('ShiftLeft');
    log('to the clerk', await toClerk()); await page.keyboard.up('ShiftLeft');
    await shot('at-clerk'); await talk();
    log('PANEL 1', (await H.panel()).slice(0, 500));
    await tap('#crew-panel [data-a="mission-ask"]');
    log('BOARD', (await H.panel()).slice(0, 1400)); await shot('board');
    await tap('#crew-panel [data-m="mars-fr-well"]');
    log('AFTER TAKE', (await H.panel()).slice(0, 500), await H.me()); await shot('taken');
    await page.evaluate(() => { const c = document.querySelector('#crew-panel [data-a="close"]'); if (c) c.click(); }); await sleep(1500);
    log('HINT', (await H.text()).slice(0, 400));
  }
  let me = await H.me();
  if (me.active && me.active.id === 'mars-fr-well' && me.active.step === 0) {
    await page.keyboard.down('ShiftLeft');
    const [sx, , sz] = await H.local(); let i0 = 0, best = 1e9; ROAD.forEach(([x, z], i) => { const d = Math.hypot(x - sx, z - sz); if (d < best) { best = d; i0 = i; } });       // carry on from the nearest point of the road
    for (const [x, z] of ROAD.slice(i0)) { const r = await H.hopTo(x, z, x === 407 ? 2 : 6, 300); log('road', [x, z], r); if (!r.ok) break; if ((await H.me()).active?.step === 1) break; }
    await page.keyboard.up('ShiftLeft'); await sleep(2500);
    me = await H.me(); log('AT THE WELL', me, (await H.text()).slice(0, 500)); await shot('well');
  }
  if (me.active && me.active.step === 1) {
    await page.keyboard.down('ShiftLeft');
    for (const [x, z] of [...ROAD].reverse().slice(1)) { const r = await H.hopTo(x, z, 6, 300); log('road back', [x, z], r); if (!r.ok) break; }
    log('to the clerk', await toClerk()); await page.keyboard.up('ShiftLeft'); await sleep(3000);
    me = await H.me(); log('PAID?', me, (await H.text()).slice(0, 600)); await shot('paid');
    if (!me.active) { await talk(); await tap('#crew-panel [data-a="mission-ask"]'); log('BOARD AGAIN', (await H.panel()).slice(0, 900)); await shot('board-again'); }
  }
};
