// Live scenario for live-check.mjs: the freight board's code is in the live build (the jobs themselves need the game server restarted).
// node live-check.mjs shots/live-p3 live-freight.mjs
export default async ({ page, prefix }) => {
  const info = await page.evaluate(async () => {
    const C = await import('/games/the-cosmos/src/missions/catalog.js'), T = await import('/games/the-cosmos/src/missions/talk.js'), W = await import('/games/the-cosmos/src/missions/where.js');
    const fr = C.MISSIONS.filter((m) => m.repeat), snap = { missions: { me: { active: null, done: {}, flags: {}, log: [], n: 0 } } };
    const html = T.view('depot-clerk', 'Supply clerk', 'work', snap, 'me', 'mars');
    return { freight: fr.length, sides: fr.filter((m) => m.faction).length, rank: C.freightRank(3).name, board: /The freight board/.test(html) && /Well samples · 80 credits/.test(html),
      moonPeople: ['ph-yard', 'ph-pump', 'de-driller', 'de-geo'].map((id) => (W.personById(id) || {}).name) };
  });
  console.log('freight', JSON.stringify(info));
  await page.screenshot({ path: prefix + '-live-freight.png' });
};
