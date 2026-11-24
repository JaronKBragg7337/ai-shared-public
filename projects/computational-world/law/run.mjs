// The hidden-law world: bare against built (see PLAN.md, committed before the first graded try).
//   node law/run.mjs --model qwen3.5:4b            local model through Ollama: arms A, B, B2 on worlds 1..12, 3 repeats
//   node law/run.mjs --control                      arm 0 (no model) on worlds 1..12
//   node law/run.mjs --print-prompt 5               the arm A prompt for world 5 (for a big model called from the shell)
//   node law/run.mjs --grade-big sol results/big-sol-w5.out 5     grade a big model's answer file for world 5
// Every graded try is appended to results/chronicle-<model>.jsonl, chained by SHA-256, and a stopped run resumes from it.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { makeWorld, measure, randomRows, randomPoint, gradeLaw, fitPowerLaw, fitShape, VARS } from './world.mjs';
import { rng } from '../world.js';

const here = path.dirname(fileURLToPath(import.meta.url)), argv = process.argv.slice(2), has = (f) => argv.includes(f), after = (f) => argv[argv.indexOf(f) + 1];
const WORLDS = Array.from({ length: 12 }, (_, i) => i + 1), REPS = 3, ARM_NO = { A: 1, B: 2, B2: 3 };
const BASE = `A small world has two bodies. Body 1 has mass m1 and charge q1. Body 2 has mass m2 and charge q2. They are a distance r apart.
An experiment sets m1, m2, q1, q2 and r (each any number from 1 to 10) and the world reports y, the push on body 1.
The push follows ONE hidden law. It is a made-up law of nature for this world only: do not expect textbook physics.
Your job: find the law. Write it as one expression using m1, m2, q1, q2, r, numbers, + - * / ( ), pow(a,b) and sqrt(a).
You are graded on 200 new experiments: your law must predict y within 1%.
`;
const table = (rows, extra) => 'm1     m2     q1     q2     r      ->  y' + (extra ? '          (your law gives)' : '') + '\n' +
  rows.map((x, i) => VARS.map((v) => String(x[v]).padEnd(6)).join(' ') + ' ->  ' + String(x.y).padEnd(12) + (extra ? String(extra[i]) : '')).join('\n');
const ASK_LAW = `\nReply with exactly one line and nothing else:\nLAW: <expression>`;
export const promptA = (seed) => BASE + `\nHere are 12 experiments:\n` + table(randomRows(makeWorld(seed), 12, 5000 + seed)) + '\n' + ASK_LAW;
const promptRun = (rows) => BASE + (rows.length ? `\nYour notebook so far:\n` + table(rows) + '\n' : '') +
  `\nYou may now run 4 experiments of your own choosing. Good experiments change one thing at a time.\nReply with exactly 4 lines and nothing else, like this:\nRUN: m1=2 m2=1 q1=1 q2=1 r=1`;
const promptLaw = (rows) => BASE + `\nYour notebook (you chose these experiments):\n` + table(rows) + '\n' + ASK_LAW;
const promptFix = (rows, law, gives) => BASE + `\nYour notebook, with what your law gives beside what was measured:\n` + table(rows, gives) + `\n\nYour law was:\nLAW: ${law}\nIf it does not match the measurements, fix it.` + ASK_LAW;
export const readLaw = (text) => { const m = String(text).match(/LAW\s*:\s*([^\n\r]+)/i); return m ? m[1].replace(/`/g, '').replace(/^y\s*=\s*/i, '').replace(/[.;]\s*$/, '').trim() || null : null; };
function readRuns(text, r) {                       // up to 4 experiments the model asked for; anything unreadable becomes a random one
  const out = [];
  for (const m of String(text).matchAll(/RUN\s*:\s*([^\n\r]+)/gi)) { if (out.length >= 4) break; const x = {}; let ok = 0;
    for (const v of VARS) { const q = m[1].match(new RegExp(v + '\\s*=\\s*(-?\\d+\\.?\\d*)', 'i')); if (q) { x[v] = Math.min(10, Math.max(1, +q[1])); ok++; } else x[v] = 1; }
    if (ok >= 3) out.push(x); }
  const asked = out.length; while (out.length < 4) out.push(randomPoint(r)); return { rows: out, asked };
}

function openChronicle(name) {
  fs.mkdirSync(path.join(here, 'results'), { recursive: true });
  const file = path.join(here, 'results', `chronicle-${name.replace(/[^a-z0-9.]+/gi, '-')}.jsonl`), all = [], byKey = new Map(); let last = 'start';
  if (fs.existsSync(file)) for (const l of fs.readFileSync(file, 'utf8').split('\n')) { if (!l.trim()) continue; const e = JSON.parse(l), { hash, ...rest } = e;
    if (rest.prev !== last || crypto.createHash('sha256').update(JSON.stringify(rest)).digest('hex') !== hash) throw new Error('chronicle chain broken'); last = hash; all.push(e); byKey.set(`${e.arm}|${e.world}|${e.rep}`, e); }
  const append = (e) => { e.seq = all.length + 1; e.prev = last; const hash = crypto.createHash('sha256').update(JSON.stringify(e)).digest('hex'); last = hash; const full = { ...e, hash }; fs.appendFileSync(file, JSON.stringify(full) + '\n'); all.push(full); byKey.set(`${e.arm}|${e.world}|${e.rep}`, full); return full; };
  return { file, all, byKey, append };
}
const graded = (world, law) => (law ? gradeLaw(world, law) : { valid: false, error: 'no LAW line', grade: 0 });

if (has('--print-prompt')) process.stdout.write(promptA(+after('--print-prompt')));
else if (has('--control')) {
  const C = openChronicle('no-model');
  for (const s of WORLDS) { if (C.byKey.has(`0|${s}|1`)) continue; const w = makeWorld(s), law = fitPowerLaw(randomRows(w, 12, 5000 + s)); C.append({ model: 'no-model', arm: '0', world: s, rep: 1, kind: w.kind, law, ...gradeLaw(w, law) }); }
  console.log('arm 0: ' + C.all.map((e) => e.grade).join(' '));
} else if (has('--grade-big')) {
  const name = after('--grade-big'), file = argv[argv.indexOf('--grade-big') + 2], seed = +argv[argv.indexOf('--grade-big') + 3], C = openChronicle(name), w = makeWorld(seed);
  const raw = fs.readFileSync(file, 'utf8'), cut = raw.lastIndexOf('tokens used'), law = readLaw(cut >= 0 ? raw.slice(cut) : raw.split('\n').slice(-12).join('\n')) || readLaw(raw.slice(raw.lastIndexOf('LAW')));
  const e = C.byKey.get(`A|${seed}|1`) || C.append({ model: name, arm: 'A', world: seed, rep: 1, kind: w.kind, law, ranCode: /^exec\b/m.test(raw), ...graded(w, law) });
  console.log(`${name} world ${seed} (${w.kind}): ${e.valid ? e.grade : 'UNREADABLE ' + e.error}   ${String(e.law).slice(0, 90)}`);
} else if (has('--control-shape')) {               // arm S0 (added after the plan): no model, one fixed shape, the same fitter
  const C = openChronicle('no-model'), POWER = 'a * pow(m1, b) * pow(m2, c) * pow(q1, d) * pow(q2, e) * pow(r, f)';
  for (const s of WORLDS) { if (C.byKey.has(`S0|${s}|1`)) continue; const w = makeWorld(s), fit = fitShape(POWER, randomRows(w, 12, 5000 + s), s); C.append({ model: 'no-model', arm: 'S0', world: s, rep: 1, kind: w.kind, law: fit.law, worst: fit.worst, ...gradeLaw(w, fit.law) }); }
  console.log('arm S0: ' + C.all.filter((e) => e.arm === 'S0').map((e) => e.grade).join(' '));
} else if (has('--shape')) {                       // arm S (added after the plan): the model writes the SHAPE, the world finds the numbers
  const MODEL = after('--shape'), C = openChronicle(MODEL);
  const ask = async (prompt, seed) => { const t0 = Date.now(), r = await fetch('http://127.0.0.1:11434/api/generate', { method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ model: MODEL, prompt, think: false, stream: false, keep_alive: '15m', options: { temperature: 0.6, seed, num_predict: 300 } }) }); const d = await r.json(); if (d.error) throw new Error('ollama: ' + d.error); return { text: d.response || '', ms: Date.now() - t0 }; };
  const readShape = (text) => { const m = String(text).match(/SHAPE\s*:\s*([^\n\r]+)/i); return m ? m[1].replace(/`/g, '').replace(/^y\s*=\s*/i, '').replace(/[.;]\s*$/, '').trim() || null : null; };
  console.log(`model ${MODEL}: arm S x ${WORLDS.length} worlds x ${REPS} repeats`);
  for (let rep = 1; rep <= REPS; rep++) for (const s of WORLDS) {
    if (C.byKey.has(`S|${s}|${rep}`)) continue;
    const w = makeWorld(s), rows = randomRows(w, 12, 5000 + s), tried = []; let best = null, ms = 0;
    for (let round = 1; round <= 4; round++) {
      const prompt = BASE + `\nHere are 12 experiments:\n` + table(rows) + `\n\nYou do NOT have to find the numbers. Write only the SHAPE of the law: use the letters a, b, c, d, e, f, g for numbers you do not know.\nThe world will find the best numbers for your shape and tell you how far off it is.\nExample of a shape:  a * pow(m1, b) * q2 / pow(r, c) + d * m2\n` +
        (tried.length ? `\nShapes you have tried, and the worst miss of each on your 12 experiments (0% is a perfect fit):\n` + tried.map((t, i) => `${i + 1}. SHAPE: ${t.shape}   -> ${t.note}`).join('\n') + `\nWrite a DIFFERENT shape that fits better.\n` : '') + `\nReply with exactly one line and nothing else:\nSHAPE: <expression>`;
      const a = await ask(prompt, 100000 * rep + 1000 * s + 400 + round), shape = readShape(a.text); ms += a.ms; let note;
      if (!shape) note = 'no SHAPE line'; else { try { const fit = fitShape(shape, rows, s); note = `worst miss ${(fit.worst * 100).toFixed(1)}%`; if (!best || fit.worst < best.worst) best = { ...fit, shape }; } catch (e) { note = 'could not be read: ' + (e.message || e); } }
      tried.push({ shape: shape || a.text.slice(0, 60), note }); if (best && best.worst < 0.001) break;
    }
    const e = C.append({ model: MODEL, arm: 'S', world: s, rep, kind: w.kind, law: best ? best.law : null, shape: best ? best.shape : null, worst: best ? best.worst : null, tried, ms, ...graded(w, best ? best.law : null) });
    console.log(`  repeat ${rep} world ${String(s).padStart(2)} (${w.kind.padEnd(5)})  S ${e.grade.toFixed(2)}  rounds ${tried.length}  ${String(e.shape).slice(0, 70)}`);
  }
  console.log('done: ' + C.file);
} else if (has('--model')) {
  const MODEL = after('--model'), C = openChronicle(MODEL);
  const ask = async (prompt, seed) => { const t0 = Date.now(), r = await fetch('http://127.0.0.1:11434/api/generate', { method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ model: MODEL, prompt, think: false, stream: false, keep_alive: '15m', options: { temperature: 0.6, seed, num_predict: 300 } }) }); const d = await r.json(); if (d.error) throw new Error('ollama: ' + d.error); return { text: d.response || '', ms: Date.now() - t0 }; };
  console.log(`model ${MODEL}: arms A, B, B2 x ${WORLDS.length} worlds x ${REPS} repeats; ${C.all.length} tries already in the chronicle`);
  for (let rep = 1; rep <= REPS; rep++) for (const s of WORLDS) {
    const w = makeWorld(s), seed = (arm, round) => 100000 * rep + 1000 * s + 100 * ARM_NO[arm] + round, line = [];
    if (!C.byKey.has(`A|${s}|${rep}`)) { const a = await ask(promptA(s), seed('A', 0)), law = readLaw(a.text); C.append({ model: MODEL, arm: 'A', world: s, rep, kind: w.kind, law, raw: a.text.slice(0, 300), ms: a.ms, ...graded(w, law) }); }
    if (!C.byKey.has(`B|${s}|${rep}`)) {
      const rows = [], r = rng(seed('B', 9)); let asked = 0, ms = 0;
      for (let round = 1; round <= 3; round++) { const a = await ask(promptRun(rows), seed('B', round)), got = readRuns(a.text, r); asked += got.asked; ms += a.ms; for (const x of got.rows) rows.push({ ...x, y: measure(w, x) }); }
      const a = await ask(promptLaw(rows), seed('B', 4)), law = readLaw(a.text);
      C.append({ model: MODEL, arm: 'B', world: s, rep, kind: w.kind, law, raw: a.text.slice(0, 300), ms: ms + a.ms, asked, rows, ...graded(w, law) });
    }
    if (!C.byKey.has(`B2|${s}|${rep}`)) {
      const b = C.byKey.get(`B|${s}|${rep}`); let law = b.law, raw = '', ms = 0;
      if (b.valid) { const f = (await import('./world.mjs')).compileLaw(b.law), gives = b.rows.map((x) => Number(f(x)).toPrecision(6)); const a = await ask(promptFix(b.rows, b.law, gives), seed('B2', 1)); raw = a.text.slice(0, 300); ms = a.ms; law = readLaw(a.text) || b.law; }
      else { const a = await ask(promptLaw(b.rows) + `\n(Your last answer could not be read: ${b.error}.)`, seed('B2', 1)); raw = a.text.slice(0, 300); ms = a.ms; law = readLaw(a.text); }
      C.append({ model: MODEL, arm: 'B2', world: s, rep, kind: w.kind, law, raw, ms, ...graded(w, law) });
    }
    for (const arm of ['A', 'B', 'B2']) line.push(`${arm} ${C.byKey.get(`${arm}|${s}|${rep}`).grade.toFixed(2)}`);
    console.log(`  repeat ${rep} world ${String(s).padStart(2)} (${w.kind.padEnd(5)})  ${line.join('   ')}`);
  }
  console.log('done: ' + C.file);
}
