// Grade one recipe with the exact checker and print the piles. Reads the recipe from the first argument or from stdin.
//   node llm/grade-one.mjs 'z*o*t'        (PowerShell: keep the single quotes)
// Writes nothing. No length cap here (the cap in the planned runs was a safety limit for the small local model).
import fs from 'node:fs';
import { grade, BEST } from './recipe.mjs';

let src = process.argv.slice(2).join(' ').trim();
if (!src) src = fs.readFileSync(0, 'utf8').trim();
src = src.replace(/^SCORE\s*:\s*/i, '');
const g = grade(src, { chars: 20000, nodes: 20000 });
if (!g.valid) { console.log('COULD NOT READ THE RECIPE: ' + g.error); process.exit(1); }
console.log('cards kept for 3..8 digits: ' + [3, 4, 5, 6, 7, 8].map((n) => g.sizes[n]).join(', ') + '   best known: ' + [3, 4, 5, 6, 7, 8].map((n) => BEST[n]).join(', '));
console.log('grade ' + g.total.toFixed(4) + ' of 6');
