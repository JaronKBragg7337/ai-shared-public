// AFTER THE PLAN: exploratory. The deeper version of explore-loop.mjs. Still no model: only the exact checker.
// Starts from where explore-loop.mjs ended (results/explore-loop.json) and keeps changing the big model's recipes:
// a number, a comparison, an and/or, a plus/minus, a name; first one change at a time (every spot), then random pairs,
// for a fixed number of minutes per recipe. A change is kept only when the checker says the grade went up.
//   node llm/explore-deep.mjs [minutes per recipe, default 8]
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { grade, sizesFor, BEST } from './recipe.mjs';
import { rng } from '../world.js';

const here = path.dirname(fileURLToPath(import.meta.url)), dir = path.join(here, 'results'), MIN = +(process.argv[2] || 8);
const LIM = { chars: 20000, nodes: 20000 }, start = JSON.parse(fs.readFileSync(path.join(dir, 'explore-loop.json'), 'utf8'));
const SWAP = { '==': ['!='], '!=': ['=='], '<': ['<=', '>'], '<=': ['<', '>='], '>': ['>=', '<'], '>=': ['>', '<='], '&&': ['||'], '||': ['&&'], '+': ['-'], '-': ['+'],
  z: ['o', 't', 'w'], o: ['z', 't', 'w'], t: ['z', 'o', 'w'], w: ['z', 'o', 't'], first: ['last'], last: ['first'] };
const TOKEN = /\d+\.?\d*|[a-z_][a-z0-9_]*|<=|>=|==|!=|&&|\|\||[-+*/%()<>!?:,]/g;

function spots(src) {                  // every place a change can be made, with the things it could become
  const out = [];
  for (const m of src.matchAll(TOKEN)) {
    const tok = m[0]; let alts = null;
    if (/^\d+$/.test(tok) && tok.length < 6) alts = [0, 1, 2, 3, 4, 5, 6, 7, 8].filter((v) => v !== +tok).map(String);
    else if (SWAP[tok]) alts = SWAP[tok];
    if (alts) out.push({ at: m.index, len: tok.length, alts });
  }
  return out;
}
const put = (src, sp, alt) => src.slice(0, sp.at) + alt + src.slice(sp.at + sp.len);
const out = { when: new Date().toISOString(), minutesPerRecipe: MIN, recipes: [] };

for (const r0 of start.recipes) {
  let cur = r0.final.expr, g = grade(cur, LIM), tries = 0; const t0 = Date.now(), log = [], r = rng(99 + out.recipes.length);
  console.log(`\n${r0.file}: starts at ${g.total.toFixed(3)}  (${Object.values(g.sizes).join(', ')})`);
  const consider = (trial, what) => {    // cheap look at the two big worlds first; the full grade only if that looks better
    tries++; let s; try { s = sizesFor(trial, [7, 8], LIM); } catch { return false; }
    if (s[7] / BEST[7] + s[8] / BEST[8] <= g.sizes[7] / BEST[7] + g.sizes[8] / BEST[8] + 1e-9) return false;
    const gt = grade(trial, LIM); if (!gt.valid || gt.total <= g.total + 1e-9) return false;
    cur = trial; g = gt; log.push({ what, grade: g.total, sizes: g.sizes, secs: Math.round((Date.now() - t0) / 1000) });
    console.log(`  ${what}: ${g.total.toFixed(3)}  (${Object.values(g.sizes).join(', ')})  after ${log[log.length - 1].secs} s`); return true;
  };
  const left = () => Date.now() - t0 < MIN * 60000;
  let better = true;
  while (better && left()) {             // one change at a time, every spot
    better = false;
    for (const sp of spots(cur)) { if (!left()) break; for (const alt of sp.alts) if (consider(put(cur, sp, alt), 'one change')) { better = true; break; } if (better) break; }
  }
  while (left()) {                       // random pairs of changes
    const S = spots(cur), a = S[(r() * S.length) | 0], b = S[(r() * S.length) | 0]; if (!a || !b || a === b) continue;
    const [lo, hi] = a.at < b.at ? [a, b] : [b, a];
    const trial = put(put(cur, hi, hi.alts[(r() * hi.alts.length) | 0]), lo, lo.alts[(r() * lo.alts.length) | 0]);
    if (consider(trial, 'two changes')) { let again = true; while (again && left()) { again = false; for (const sp of spots(cur)) { if (!left()) break; for (const alt of sp.alts) if (consider(put(cur, sp, alt), 'one change')) { again = true; break; } if (again) break; } } }
  }
  console.log(`  ends at ${g.total.toFixed(3)}  (${Object.values(g.sizes).join(', ')})  ${tries} changes tried   best known: ${Object.values(BEST).join(', ')}`);
  out.recipes.push({ file: r0.file, bigModelAlone: r0.startGrade, afterFirstLoop: r0.final.grade, final: { expr: cur, grade: g.total, sizes: g.sizes }, changesTried: tries, kept: log });
  fs.writeFileSync(path.join(dir, 'explore-deep.json'), JSON.stringify(out, null, 1));
}
console.log(`\nSaved results/explore-deep.json`);
