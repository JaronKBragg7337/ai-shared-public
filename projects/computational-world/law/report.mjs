// Writes law/RESULTS.md from the chronicles in law/results.   node law/report.mjs
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { makeWorld } from './world.mjs';

const here = path.dirname(fileURLToPath(import.meta.url)), dir = path.join(here, 'results'), out = [], P = (s = '') => out.push(s);
const mean = (a) => (a.length ? a.reduce((s, v) => s + v, 0) / a.length : NaN), f2 = (v) => (Number.isNaN(v) ? '' : v.toFixed(2));
const KINDS = ['power', 'plus', 'mix'], WORLDS = Array.from({ length: 12 }, (_, i) => i + 1);
const files = fs.existsSync(dir) ? fs.readdirSync(dir).filter((f) => /^chronicle-.*\.jsonl$/.test(f)).sort() : [], rowsOf = {};
for (const f of files) for (const l of fs.readFileSync(path.join(dir, f), 'utf8').split('\n')) { if (!l.trim()) continue; const e = JSON.parse(l); (rowsOf[`${e.model} | ${e.arm}`] ||= []).push(e); }

P(`# The hidden-law world: results`); P();
P(`Made by \`law/report.mjs\` from the chained records in \`law/results\`. Plan: \`law/PLAN.md\`, committed before any model was asked.`);
P(`Each world has its own made-up law of nature, so nothing can be remembered. A grade is the share of 200 unseen experiments a written law predicts within 1%.`); P();
P(`The twelve laws (never shown to any model):`); P();
P(`| world | kind | the hidden law |`); P(`|---|---|---|`); for (const s of WORLDS) { const w = makeWorld(s); P(`| ${s} | ${w.kind} | \`${w.text}\` |`); }
P(); P(`| who | arm | worlds | average grade | power | plus | mix | solved outright (0.95+) | unreadable |`); P(`|---|---|---|---|---|---|---|---|---|`);
const ARM = { 0: 'no model: straight-line fit on logs', A: 'bare: 12 random experiments, one try', B: 'built: chooses its own 12 experiments', B2: 'built + sees its law checked against its notebook',
  S: 'AFTER THE PLAN: the model writes the shape, the world finds the numbers (4 rounds)', S0: 'AFTER THE PLAN: no model, one fixed power-law shape, the same fitter' }, per = {};
for (const [key, E] of Object.entries(rowsOf).sort()) {
  const [model, arm] = key.split(' | '), worlds = [...new Set(E.map((e) => e.world))].sort((a, b) => a - b), byWorld = worlds.map((w) => mean(E.filter((e) => e.world === w).map((e) => e.grade)));
  per[key] = Object.fromEntries(worlds.map((w, i) => [w, byWorld[i]]));
  P(`| ${model} | ${arm}: ${ARM[arm]} | ${worlds.length}${worlds.length < 12 ? ' (' + worlds.join(', ') + ')' : ''} | **${f2(mean(byWorld))}** | ${KINDS.map((k) => f2(mean(E.filter((e) => e.kind === k).map((e) => e.grade)))).join(' | ')} | ${E.filter((e) => e.grade >= 0.95).length} of ${E.length} | ${E.filter((e) => !e.valid).length} |`);
}
const cmp = (a, b, label) => { const A = per[a], B = per[b]; if (!A || !B) return; const ws = Object.keys(A).filter((w) => w in B); if (!ws.length) return;
  const d = mean(ws.map((w) => A[w])) - mean(ws.map((w) => B[w])), ge = ws.filter((w) => A[w] >= B[w]).length, need = Math.ceil(ws.length * 0.75);
  P(`- ${label}: ${d > 0 && ge >= need ? '**yes**' : '**no clear difference**'} (average ${d >= 0 ? '+' : ''}${d.toFixed(3)}, higher or equal on ${ge} of ${ws.length} worlds).`); };
P(); P(`By the rule fixed in the plan (higher on average, and higher or equal on at least three quarters of the worlds):`);
for (const m of [...new Set(Object.keys(rowsOf).map((k) => k.split(' | ')[0]))]) { cmp(`${m} | B`, `${m} | A`, `${m}: choosing its own experiments helps (B over A)`); cmp(`${m} | B2`, `${m} | B`, `${m}: seeing its law checked helps (B2 over B)`); cmp(`${m} | B2`, `no-model | 0`, `${m}: built beats the no-model fit`); cmp(`${m} | A`, `no-model | 0`, `${m}: bare beats the no-model fit (same worlds)`);
  cmp(`${m} | S`, `no-model | S0`, `${m}, after the plan: its shapes beat the fixed power-law shape (S over S0)`); cmp(`${m} | S`, `${m} | B2`, `${m}, after the plan: shape-and-fit beats the best planned arm (S over B2)`); cmp(`${m} | S`, `gpt-6.2-sol | A`, `${m}, after the plan: shape-and-fit against the big model alone, same worlds (S over Sol)`); }
P(); P(`Laws written by the big models (one try each):`); P();
for (const [key, E] of Object.entries(rowsOf).sort()) if (/sol|kimi|astra/i.test(key)) for (const e of E) P(`- ${e.model}, world ${e.world} (${e.kind}): grade ${e.grade}${e.ranCode ? ' (it ran code)' : ''}: \`${String(e.law).slice(0, 110)}\``);
P();
const byHand = path.join(dir, 'kimi-by-hand.json');
if (fs.existsSync(byHand)) {
  const { rows } = JSON.parse(fs.readFileSync(byHand, 'utf8')), kimi = Object.entries(rowsOf).find(([key]) => /kimi/i.test(key));
  P(`Read both ways (Kimi K3.1 Pro). The grader reads one line and nothing else. Two of Kimi's answers put the law inside a sentence, so the grader could not read them and they count as 0 above. Pulled out by hand (this is NOT the planned reading) and graded by the same grader:`); P();
  for (const r of rows) P(`- world ${r.world}: \`${r.law}\` grades ${r.grade}`);
  if (kimi) { const E = kimi[1], solved = E.filter((e) => e.grade >= 0.95).length, extra = rows.filter((r) => r.grade >= 0.95 && !E.some((e) => e.world === r.world && e.grade >= 0.95)).length;
    P(); P(`So Kimi solved ${solved} of ${E.length} worlds as graded, and ${solved + extra} of ${E.length} if the law is lifted out of its sentence. The planned figure stays the first one.`); }
  P();
}
fs.writeFileSync(path.join(here, 'RESULTS.md'), out.join('\n')); console.log(out.join('\n'));
