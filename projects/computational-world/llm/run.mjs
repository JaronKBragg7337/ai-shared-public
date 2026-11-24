// Bare against built (see PLAN.md, which was committed before this was first run).
//   node llm/run.mjs --model qwen3.5:4b [--tries 120] [--runs 5] [--arms 0a,0b,A+,B,C,D] [--print-prompt]      (after the plan: --arms E, --arms R)
// Every try is appended to results/chronicle-<model>.jsonl, each line chained to the last by SHA-256.
// The run can be stopped and started again: everything it needs is rebuilt from that file.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { grade, gradeOrder, distance } from './recipe.mjs';
import { rng } from '../world.js';

const here = path.dirname(fileURLToPath(import.meta.url)), argv = process.argv.slice(2);
const opt = (name, dflt) => (argv.includes('--' + name) ? argv[argv.indexOf('--' + name) + 1] : dflt);
const MODEL = opt('model', 'qwen3.5:4b'), TRIES = +opt('tries', 120), RUNS = +opt('runs', 5), ARMS = opt('arms', '0a,0b,A+,B,C,D').split(',');
const ARM_NO = { '0a': 1, '0b': 2, 'A+': 3, B: 4, C: 5, D: 6, E: 7, R: 8 }, APERTURE = 3;   // E and R were added after the plan (exploratory): see PLAN.md, changes

export const TASK = `A card is a row of n digits, each 0, 1 or 2 (n is 3 to 8).
Three different cards form a SET when, at every position, their three digits are all the same or all different.
Goal: collect as many cards as possible with NO SET among them.

A builder sorts all cards by a score, highest first, and keeps each card that forms no SET with the cards already kept.
You write the score as ONE arithmetic expression. Names you can use:
  n = number of digits          z, o, t = how many digits of the card are 0, 1, 2
  s = sum of the digits         w = how many digits are not 0
  first, last = the first and the last digit        d(k) = digit number k (0 is the first)
  i = the card's number
Operators: + - * / %   < > <= >= == !=   && || !   a ? b : c   and   min(a,b) max(a,b) abs(a) mod(a,b) floor(a)
Your grade is the sum over n = 3 to 8 of (cards kept / best pile known). The top grade is 6.00.
Best piles known: 9, 20, 45, 112, 236, 512.
A plain example: SCORE: -t   (it keeps 8, 16, 32, 64, 128 and 256 cards: grade 4.01)
`;
const ENDING = `\nReply with exactly one line and nothing else:\nSCORE: <expression>`;
const kept = (e) => [3, 4, 5, 6, 7, 8].map((n) => e.sizes[n]).join(', ');
const line = (e, k) => `${k}. SCORE: ${e.expr}   (grade ${e.total.toFixed(2)})`;

export function buildPrompt(arm, tries, pool = [], seed = 0) {   // tries: this run's earlier tries in this arm, oldest first; pool: arm E's starting record; seed: arm R's draw
  let p = TASK; const last = tries[tries.length - 1];
  if (arm === 'E') {                             // the model as a changer, not an author: the record starts with the no-model arm's finds
    const got = new Set(), top = [...pool, ...tries].filter((e) => e.valid && e.expr && !got.has(e.expr) && got.add(e.expr)).sort((a, b) => b.total - a.total).slice(0, APERTURE);
    return p + '\nHere are recipes that already grade well:\n' + top.map((e, k) => line(e, k + 1)).join('\n') +
      '\n\nChange ONE small thing in one of them (a number, a name, an operator, or one added term) so that it may grade higher.' + ENDING;
  }
  if (arm === 'A+' || !last) return p + ENDING;
  p += last.valid ? `\nYour last try:\nSCORE: ${last.expr}\nIt kept ${kept(last)} cards: grade ${last.total.toFixed(2)}.\n`
    : `\nYour last try could not be read (${last.error}): ${String(last.raw || '').slice(0, 80)}\n`;
  const seen = new Set(last.valid ? [last.expr] : []), valid = tries.filter((e) => e.valid && !seen.has(e.expr) && seen.add(e.expr));
  if (arm === 'C' && valid.length) {
    const top = [...valid].sort((a, b) => b.total - a.total || a.step - b.step).slice(0, APERTURE);
    p += `\nThe best tries so far:\n` + top.map((e, k) => line(e, k + 1)).join('\n') + '\n';
  }
  if (arm === 'R' && valid.length) {             // the control for C and D: the same three places, filled by a random draw from the same record
    const r = rng(seed * 31 + 7), bag = [...valid]; for (let i = bag.length - 1; i > 0; i--) { const j = (r() * (i + 1)) | 0; [bag[i], bag[j]] = [bag[j], bag[i]]; }
    p += `\nSome of your earlier tries:\n` + bag.slice(0, APERTURE).map((e, k) => line(e, k + 1)).join('\n') + '\n';
  }
  if (arm === 'D' && valid.length) {
    const stand = last.valid ? last : [...tries].reverse().find((e) => e.valid);
    let pick;
    if (stand) {
      const near = valid.map((e) => ({ e, d: distance(stand.sig, e.sig) })).sort((a, b) => a.d - b.d || b.e.total - a.e.total || a.e.step - b.e.step);
      pick = near.filter((x) => x.e.total > stand.total).slice(0, APERTURE).map((x) => x.e);
      for (const x of near) { if (pick.length >= APERTURE) break; if (!pick.includes(x.e)) pick.push(x.e); }
    } else pick = [...valid].sort((a, b) => b.total - a.total).slice(0, APERTURE);
    p += `\nTries that keep nearly the same cards as your last one:\n` + pick.map((e, k) => line(e, k + 1)).join('\n') + '\n';
  }
  return p + `\nWrite a different expression that grades higher.` + ENDING;
}

export function randomRecipe(r, depth = 0) {            // arm 0b: recipes with no mind behind them, in the same little language
  const T = ['z', 'o', 't', 's', 'w', 'first', 'last', 'i', 'n', 'd(0)', 'd(1)', 'd(2)', '1', '2', '3'];
  if (depth >= 3 || (depth > 0 && r() < 0.3)) return T[(r() * T.length) | 0];
  const a = randomRecipe(r, depth + 1), b = randomRecipe(r, depth + 1), k = (r() * 8) | 0;
  const e = k === 0 ? `(${a} + ${b})` : k === 1 ? `(${a} - ${b})` : k === 2 ? `(${a} * ${b})` : k === 3 ? `mod(${a}, ${b})` : k === 4 ? `(${a} == ${b})` :
    k === 5 ? `(${a} < ${b})` : k === 6 ? `min(${a}, ${b})` : `(${a} ? ${b} : ${randomRecipe(r, depth + 1)})`;
  return depth === 0 && r() < 0.3 ? `-${e}` : e;
}

export function readAnswer(text) {              // the one line the model was asked for
  const m = String(text).match(/SCORE\s*:\s*([^\n\r]+)/i); if (!m) return null;
  return m[1].replace(/`/g, '').replace(/^\*+|\*+$/g, '').replace(/<\/?expression>/gi, '').replace(/[.;]\s*$/, '').trim() || null;
}

if (argv.includes('--print-prompt')) { process.stdout.write(buildPrompt('A+', []) ); process.exit(0); }
if (path.resolve(process.argv[1] || '') !== fileURLToPath(import.meta.url)) { /* imported by another script: do not run */ }
else await main();

async function main() {
  fs.mkdirSync(path.join(here, 'results'), { recursive: true });
  const file = path.join(here, 'results', process.env.CW_SMOKE ? 'smoke.jsonl' : `chronicle-${MODEL.replace(/[^a-z0-9.]+/gi, '-')}.jsonl`);
  const all = [], byKey = new Map(); let lastHash = 'start';
  if (fs.existsSync(file)) for (const l of fs.readFileSync(file, 'utf8').split('\n')) {
    if (!l.trim()) continue; const e = JSON.parse(l), { hash, ...rest } = e;
    if (rest.prev !== lastHash || crypto.createHash('sha256').update(JSON.stringify(rest)).digest('hex') !== hash) throw new Error('the chronicle chain is broken at line ' + (all.length + 1));
    lastHash = hash; all.push(e); byKey.set(`${e.arm}|${e.run}|${e.step}`, e);
  }
  const append = (e) => { e.seq = all.length + 1; e.prev = lastHash; const hash = crypto.createHash('sha256').update(JSON.stringify(e)).digest('hex'); lastHash = hash;
    const full = { ...e, hash }; fs.appendFileSync(file, JSON.stringify(full) + '\n'); all.push(full); byKey.set(`${e.arm}|${e.run}|${e.step}`, full); return full; };

  const watts = [], smi = spawn('nvidia-smi', ['--query-gpu=power.draw', '--format=csv,noheader,nounits', '-lms', '2000']);
  smi.stdout.on('data', (d) => { for (const s of String(d).split('\n')) { const w = parseFloat(s); if (!isNaN(w)) watts.push({ t: Date.now(), w }); } });
  smi.on('error', () => {});
  const joules = (t0, t1) => { const s = watts.filter((x) => x.t >= t0 - 2500 && x.t <= t1 + 500); return s.length ? +((s.reduce((a, x) => a + x.w, 0) / s.length) * ((t1 - t0) / 1000)).toFixed(2) : null; };

  async function ask(prompt, seed) {
    const t0 = Date.now(), r = await fetch('http://127.0.0.1:11434/api/generate', { method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ model: MODEL, prompt, think: false, stream: false, keep_alive: '15m', options: { temperature: 0.8, seed, num_predict: 80 } }) });
    const d = await r.json(); if (d.error) throw new Error('ollama: ' + d.error);
    return { text: d.response || '', tokens: d.eval_count || 0, ms: Date.now() - t0, t0, t1: Date.now() };
  }

  console.log(`model ${MODEL}: ${ARMS.join(' ')} x ${RUNS} runs x ${TRIES} tries; ${all.length} tries already in the chronicle`);
  for (let run = 1; run <= RUNS; run++) for (const arm of ARMS) {
    const tries = []; for (let s = 1; s <= TRIES; s++) { const e = byKey.get(`${arm}|${run}|${s}`); if (e) tries.push(e); else break; }
    const t0 = Date.now(); let fresh = 0;
    for (let step = tries.length + 1; step <= TRIES; step++) {
      const seed = 1000000 * run + 10000 * ARM_NO[arm] + step; let e = { model: MODEL, arm, run, step, seed, at: new Date().toISOString() };
      if (arm === '0a') { const r = rng(seed); Object.assign(e, { expr: null }, gradeOrder((n, N) => { const a = Array.from({ length: N }, (_, i) => i); for (let i = N - 1; i > 0; i--) { const j = (r() * (i + 1)) | 0; [a[i], a[j]] = [a[j], a[i]]; } return a; })); }
      else if (arm === '0b') { const expr = randomRecipe(rng(seed)); Object.assign(e, { expr }, grade(expr)); }
      else {
        const pool = arm === 'E' ? Array.from({ length: TRIES }, (_, i) => byKey.get(`0b|${run}|${i + 1}`)).filter(Boolean) : [];
        const a = await ask(buildPrompt(arm, tries, pool, seed), seed), expr = readAnswer(a.text);
        Object.assign(e, { expr, raw: a.text.slice(0, 300), tokens: a.tokens, ms: a.ms, joules: joules(a.t0, a.t1) }, expr ? grade(expr) : { valid: false, error: 'no SCORE line', sizes: {}, total: 0 });
      }
      tries.push(append(e)); fresh++;
    }
    const best = Math.max(0, ...tries.map((e) => e.total));
    console.log(`  run ${run} arm ${arm.padEnd(2)}  best ${best.toFixed(3)}  first ${tries[0].total.toFixed(3)}  readable ${tries.filter((e) => e.valid).length}/${tries.length}` + (fresh ? `  (${((Date.now() - t0) / 1000).toFixed(0)} s)` : '  (already done)'));
  }
  smi.kill(); console.log('done: ' + file);
}
