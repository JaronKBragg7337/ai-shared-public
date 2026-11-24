// AFTER THE PLAN: exploratory, not pre-registered. Started 11/23/2026 after the planned arms showed the big model alone
// far ahead of the small local model on this job. Jaron, 2:56 PM: "It's not that things aren't possible. It's that the
// way to make it possible hasn't been found yet."
//
// The way tried here is Fed Not Filled's ladder: rent the big brain ONCE, then let a cheap loop with the exact checker
// push further. No model runs in this script. It takes each recipe the frontier model wrote and
//   1. tries thousands of random tie-breakers: the big model's recipe still picks its cards first, the tie-breaker only
//      decides the order of everything else (so more cards may fit afterwards);
//   2. tries small changes to the numbers inside the recipe itself.
// Only the 2,187-card and 6,561-card worlds can improve: the four smaller ones are already at the proven best.
//   node llm/explore-loop.mjs [tie-breakers per recipe, default 3000]
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { grade, sizesFor, BEST } from './recipe.mjs';
import { readAnswer, randomRecipe } from './run.mjs';
import { rng } from '../world.js';

const here = path.dirname(fileURLToPath(import.meta.url)), dir = path.join(here, 'results'), T = +(process.argv[2] || 3000);
const LIM = { chars: 20000, nodes: 20000 }, BIG = '1000000000000000';
const base = fs.readdirSync(dir).filter((f) => /^frontier-.*\.out$/.test(f)).sort().map((f) => { const raw = fs.readFileSync(path.join(dir, f), 'utf8'); return { file: f, expr: readAnswer(raw.slice(raw.lastIndexOf('tokens used'))) }; }).filter((b) => b.expr);
const withTie = (sol, tie7, tie8) => `((${sol}) ? ${BIG} : 0) + (n == 7 ? (${tie7}) : n == 8 ? (${tie8}) : 0)`;
const out = { when: new Date().toISOString(), tieBreakersPerRecipe: T, recipes: [] }, t0 = Date.now();

for (const b of base) {
  const g0 = grade(b.expr, LIM), rec = { file: b.file, start: g0.sizes, startGrade: g0.total, steps: [] };
  console.log(`\n${b.file}: starts at ${g0.total.toFixed(3)}  (${Object.values(g0.sizes).join(', ')})`);
  // 1. tie-breakers, best one kept separately for each of the two big worlds
  let best7 = { size: g0.sizes[7], tie: '0' }, best8 = { size: g0.sizes[8], tie: '0' };
  for (let k = 1; k <= T; k++) {
    const tie = randomRecipe(rng(7000000 + k)); let s;
    try { s = sizesFor(withTie(b.expr, tie, tie), [7, 8], LIM); } catch { continue; }
    if (s[7] > best7.size) { best7 = { size: s[7], tie, at: k }; console.log(`  tie-breaker ${k}: 2,187 cards ${s[7]}   ${tie}`); }
    if (s[8] > best8.size) { best8 = { size: s[8], tie, at: k }; console.log(`  tie-breaker ${k}: 6,561 cards ${s[8]}   ${tie}`); }
  }
  let cur = withTie(b.expr, best7.tie, best8.tie), g = grade(cur, LIM);
  rec.steps.push({ what: `${T} random tie-breakers`, sizes: g.sizes, grade: g.total, tie7: best7.tie, tie8: best8.tie });
  console.log(`  after tie-breakers: ${g.total.toFixed(3)}  (${Object.values(g.sizes).join(', ')})`);
  // 2. small changes to the numbers inside the big model's own recipe (hill climb: keep a change only if the grade goes up)
  let sol = b.expr, improved = true, rounds = 0;
  while (improved && rounds < 3) {
    improved = false; rounds++;
    const spots = [...sol.matchAll(/(?<![a-z0-9_.])\d+(?![0-9.])/g)].map((m) => ({ at: m.index, len: m[0].length, val: +m[0] }));
    for (const sp of spots) for (const v of [0, 1, 2, 3, 4, 5, 6, 7]) {
      if (v === sp.val) continue;
      const trial = sol.slice(0, sp.at) + v + sol.slice(sp.at + sp.len); let gt;
      try { gt = grade(withTie(trial, best7.tie, best8.tie), LIM); } catch { continue; }
      if (gt.valid && gt.total > g.total + 1e-9) { sol = trial; g = gt; cur = withTie(sol, best7.tie, best8.tie); improved = true; console.log(`  number change (${sp.val} -> ${v} at ${sp.at}): ${g.total.toFixed(3)}  (${Object.values(g.sizes).join(', ')})`); break; }
    }
  }
  rec.steps.push({ what: `number changes, ${rounds} round(s)`, sizes: g.sizes, grade: g.total });
  rec.final = { expr: cur, sizes: g.sizes, grade: g.total, chars: cur.length };
  console.log(`  ends at ${g.total.toFixed(3)}  (${Object.values(g.sizes).join(', ')})   best known: ${Object.values(BEST).join(', ')}`);
  out.recipes.push(rec);
}
out.seconds = +((Date.now() - t0) / 1000).toFixed(0);
fs.writeFileSync(path.join(dir, 'explore-loop.json'), JSON.stringify(out, null, 1));
console.log(`\n${out.seconds} s. Saved results/explore-loop.json`);
