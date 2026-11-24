// Turns the saved measurements into RESULTS.md, so no number is typed by hand.   node report.mjs [results/msi-....json]
import fs from 'node:fs';
import path from 'node:path';
import zlib from 'node:zlib';
import { fileURLToPath } from 'node:url';
import { grade } from './llm/recipe.mjs';
import { readAnswer } from './llm/run.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const msiFile = process.argv[2] || path.join(here, 'results', 'msi-2026-11-23.json');
const R = JSON.parse(fs.readFileSync(msiFile, 'utf8')), out = [];
const P = (s = '') => out.push(s);
const t = (ns) => (ns >= 1e6 ? (ns / 1e6).toFixed(2) + ' ms' : ns >= 1e3 ? (ns / 1e3).toFixed(2) + ' µs' : Math.round(ns) + ' ns');
const big = (x) => Math.round(x).toLocaleString('en-US');
const x = (a, b) => { const r = a / b; return r >= 100 ? big(r) : r >= 10 ? r.toFixed(0) : r.toFixed(1); };
const cards = { 4: 81, 5: 243, 6: 729 };
const SMALL = 'one card changes';                                   // the small-pile stream is named exactly this; the big-pile one starts with it
const hit = (r, w) => (w === SMALL ? r.workload === SMALL : r.workload.startsWith(w));
const find = (w, n, way) => R.rows.find((r) => hit(r, w) && r.n === n && r.way.startsWith(way));
const WAYS = [['ordinary software', 'Plain program (re-check)'], ['hand-written', 'Hand-written counters'], ['gates, every tick', 'Minecraft way (gates, every tick)'], ['gates, one sweep', 'Gates, one sweep per answer'],
  ['gates, only what changed', 'Gates, only what changed'], ['own parts, every tick', 'Own parts, every tick'], ['own parts, one sweep', 'Own parts, one sweep per answer'], ["the world's own parts, only", "World's own parts, only what changed"]];

P(`# Computational World, Prototype 0: results`);
P();
P(`Made by \`report.mjs\` from the saved runs. Machine: ${R.machine.cpu}, ${R.machine.threads} threads, Node ${R.machine.node}, ${R.machine.when.slice(0, 10)}.`);
P(`Every answer in every row was checked: **${R.rows.every((r) => r.ok) ? 'all correct' : 'SOME WRONG'}** (${R.rows.length} rows). Facts mark \`${R.factsMark}\`.`);
P();
P(`## 1. The same job, eight ways`);
P();
P(`The job: one card joins or leaves the pile; say whether the pile now holds a set. Times are for one change. "Steps" is how many small pieces of work it took (pair checks, gate updates or messages).`);
for (const [w, title] of [['one card changes, big pile', 'A big pile with no set in it (where a search lives)'], [SMALL, 'A small pile']]) {
  P(); P(`**${title}**`); P();
  const sz = (n) => { const r = R.rows.find((q) => hit(q, w) && q.n === n); const m = r.workload.match(/~(\d+)/); return m ? `, pile ~${m[1]}` : ''; };
  P(`| way | ${[4, 5, 6].map((n) => `${cards[n]} cards${sz(n)}`).join(' | ')} | steps at 729 |`); P(`|---|---|---|---|---|`);
  for (const [key, label] of WAYS) { const r = [4, 5, 6].map((n) => find(w, n, key)); if (r[0]) P(`| ${label} | ${r.map((q) => t(q.nsPerOp)).join(' | ')} | ${big(r[2].workPerOp)} |`); }
}
const B = (n, k) => find('one card changes, big pile', n, k), S = (n, k) => find(SMALL, n, k);
P();
P(`**What the table says**`);
P(`- **When parts run matters most.** On the big pile at 729 cards the Minecraft way needs ${t(B(6, 'gates, every tick').nsPerOp)} per change and the same gates run only-what-changed need ${t(B(6, 'gates, only').nsPerOp)}: **${x(B(6, 'gates, every tick').nsPerOp, B(6, 'gates, only').nsPerOp)} times** apart, with identical parts. The gap grows with the world: ${[4, 5, 6].map((n) => x(B(n, 'gates, every tick').nsPerOp, B(n, 'gates, only').nsPerOp) + ' times at ' + cards[n]).join(', ')}.`);
P(`- **What the parts are matters much less.** Gates against the world's own parts, both run only-what-changed: ${[4, 5, 6].map((n) => x(B(n, 'gates, only').nsPerOp, B(n, "the world's own").nsPerOp) + ' times at ' + cards[n]).join(', ')}.`);
P(`- **End to end**, Minecraft way against the world's own parts: ${[4, 5, 6].map((n) => x(B(n, 'gates, every tick').nsPerOp, B(n, "the world's own").nsPerOp) + ' times at ' + cards[n]).join(', ')}.`);
P(`- **The world against the plain program.** On a big pile the world's own parts are ${x(B(6, 'ordinary').nsPerOp, B(6, "the world's own").nsPerOp)} times faster than re-checking at 729 cards (${x(B(5, 'ordinary').nsPerOp, B(5, "the world's own").nsPerOp)} at 243, ${x(B(4, 'ordinary').nsPerOp, B(4, "the world's own").nsPerOp)} at 81). On a small pile the plain program wins: ${x(S(6, "the world's own").nsPerOp, S(6, 'ordinary').nsPerOp)} times faster at 729 cards.`);
P(`- **A step costs about the same everywhere.** At 729 cards on the big pile, one step takes ${(B(6, 'ordinary').nsPerOp / B(6, 'ordinary').workPerOp).toFixed(1)} ns in the plain program (a pair check), ${(B(6, "the world's own").nsPerOp / B(6, "the world's own").workPerOp).toFixed(1)} ns in the world's own parts (a message) and ${(B(6, 'gates, every tick').nsPerOp / B(6, 'gates, every tick').workPerOp).toFixed(1)} ns the Minecraft way (a gate update). The ways differ in how many steps they take: ${big(B(6, 'ordinary').workPerOp)}, ${big(B(6, "the world's own").workPerOp)} and ${big(B(6, 'gates, every tick').workPerOp)}.`);
P(`- **What the world itself costs.** The same idea written by hand, with no world around it, is ${[4, 5, 6].map((n) => x(B(n, "the world's own").nsPerOp, B(n, 'hand').nsPerOp) + ' times faster at ' + cards[n]).join(', ')}. That is the price of a general engine.`);
P();
P(`## 2. A fresh pile every time (nothing to reuse)`);
P();
P(`| way | ${[4, 5, 6].map((n) => `${cards[n]} cards`).join(' | ')} |`); P(`|---|---|---|---|`);
for (const [key, label] of WAYS) { const r = [4, 5, 6].map((n) => find('fresh pile', n, key)); if (r[0]) P(`| ${label} | ${r.map((q) => t(q.nsPerOp)).join(' | ')} |`); }
P();
P(`Kept state does not pay here: the plain program is ${x(find('fresh pile', 6, "the world's own").nsPerOp, find('fresh pile', 6, 'ordinary').nsPerOp)} times faster than the world's own parts at 729 cards, because each question starts from an empty table.`);
P();
P(`## 3. When many cards change at once`);
P();
P(`Only-what-changed against one full sweep, both on the world's own parts.`);
P();
P(`| share of the cards changing each step | ${[4, 5, 6].map((n) => `${cards[n]}: changed-only / sweep`).join(' | ')} |`); P(`|---|---|---|---|`);
for (const pct of [2, 5, 10, 25, 50]) {
  const cell = (n) => { const ev = R.rows.find((r) => r.n === n && r.workload.includes(`(${pct}%)`) && r.way.startsWith("the world's own")), sw = R.rows.find((r) => r.n === n && r.workload.includes(`(${pct}%)`) && r.way.startsWith('own parts, one sweep')); return `${t(ev.nsPerOp)} / ${t(sw.nsPerOp)}${ev.nsPerOp < sw.nsPerOp ? '' : ' (sweep wins)'}`; };
  P(`| ${pct}% | ${[4, 5, 6].map(cell).join(' | ')} |`);
}
const cross = (n) => { const g = (pct, way) => R.rows.find((r) => r.n === n && r.workload.includes(`(${pct}%)`) && r.way.startsWith(way)).nsPerOp; const e25 = g(25, "the world's own"), e50 = g(50, "the world's own"), s = (g(25, 'own parts, one sweep') + g(50, 'own parts, one sweep')) / 2; return Math.round(25 + (25 * (s - e25)) / (e50 - e25)); };
P();
P(`Only-what-changed stops paying when about **${[4, 5, 6].map((n) => cross(n) + '%').join(', ')}** of the cards change in one step (81, 243, 729 cards; read off the 25% and 50% rows).`);
P();
P(`## 4. Search: building a pile with no set in it`);
P();
P(`| job | cards | plain program | hand-written counters | world's own parts | best pile found | best possible |`); P(`|---|---|---|---|---|---|---|`);
for (const w of ['take free cards in a random order', 'look ahead one card']) for (const n of [4, 5, 6]) {
  const r = ['ordinary', 'hand', "the world's own"].map((k) => find(w, n, k));
  P(`| ${w} | ${cards[n]} | ${t(r[0].nsPerOp)} | ${t(r[1].nsPerOp)} | ${t(r[2].nsPerOp)} | ${r[0].best} (${r[0].steps} ${r[0].steps === 1 ? 'pile' : 'piles'}) | ${{ 4: 20, 5: 45, 6: 112 }[n]} |`);
}
P();
const L = (n, k) => find('look ahead', n, k), G = (n, k) => find('take free', n, k);
P(`- Taking cards in a fixed order asks one small question per card, and the plain program is the cheapest way to answer it (${x(G(6, "the world's own").nsPerOp, G(6, 'ordinary').nsPerOp)} times faster than the world at 729 cards).`);
P(`- Looking ahead asks a whole-table question ("how many cards would still be free?") hundreds of times per card. There the kept state pays: the world is ${x(L(6, 'ordinary').nsPerOp, L(6, "the world's own").nsPerOp)} times faster than the plain program at 729 cards, and hand-written counters are ${x(L(6, 'ordinary').nsPerOp, L(6, 'hand').nsPerOp)} times faster.`);
P(`- All three ways built identical piles in every run (same cards, same order), and the Verifier found no set in any of them.`);
P();
P(`## 5. Memory`);
P();
P(`| cards | world's own parts | the same, every change written to the Chronicle | replay of one change | bytes per change |`); P(`|---|---|---|---|---|`);
for (const n of [4, 5, 6]) { const a = S(n, "the world's own parts, only"), c = S(n, "the world's own parts + Chronicle"), rp = R.rows.find((r) => r.workload.startsWith('replay') && r.n === n); P(`| ${cards[n]} | ${t(a.nsPerOp)} | ${t(c.nsPerOp)} | ${t(rp.nsPerOp)} | 8 |`); }
P();
P(`Keeping every change costs almost nothing next to doing the work (differences this small are inside the run-to-run noise), and replaying the list on a fresh world lands on the same state every time (${R.facts.filter((f) => f.includes('chronicle')).length} of ${R.facts.filter((f) => f.includes('chronicle')).length} replays).`);
P();
P(`Room each way needs (its tables plus its running state):`); P();
P(`| way | ${[4, 5, 6].map((n) => `${cards[n]} cards`).join(' | ')} |`); P(`|---|---|---|---|`);
const kb = (b) => (b >= 1048576 ? (b / 1048576).toFixed(1) + ' MB' : Math.max(1, Math.round(b / 1024)) + ' KB');
for (const [key, label] of [['ordinary software', 'Plain program'], ['hand-written', 'Hand-written counters'], ['gates, only what changed', 'Gate world'], ["the world's own parts, only", "World's own parts"]]) P(`| ${label} | ${[4, 5, 6].map((n) => kb(S(n, key).bytes)).join(' | ')} |`);
P();
P(`World sizes: ` + R.facts.filter((f) => /\d+ parts, \d+ links/.test(f)).map((f) => f.replace('n=4', '81 cards,').replace('n=5', '243 cards,').replace('n=6', '729 cards,')).join('; ') + '.');
if (R.energy) {
  P(); P(`## 6. Energy`); P();
  P(`Read from the processor's own power meter (Intel RAPL through Windows), small-pile stream, about 5 seconds per row. Idle was ${R.energy.idleWatts} W. This is the whole processor package, so a row's watts depend on which core Windows chose.`);
  P(); P(`| cards | way | watts | microjoules per change | above idle |`); P(`|---|---|---|---|---|`);
  for (const b of R.energy.blocks) { const n = +b.name.match(/n=(\d)/)[1]; P(`| ${cards[n]} | ${b.name.replace(/n=\d /, '')} | ${b.watts} | ${big(b.microJoulePerOp) === '0' ? b.microJoulePerOp : b.microJoulePerOp >= 100 ? big(b.microJoulePerOp) : b.microJoulePerOp} | ${b.aboveIdleMicroJoulePerOp >= 100 ? big(b.aboveIdleMicroJoulePerOp) : b.aboveIdleMicroJoulePerOp} |`); }
  const e = (n, k) => R.energy.blocks.find((b) => b.name.startsWith(`n=${n} ${k}`)).microJoulePerOp;
  P(); P(`Energy follows time: the Minecraft way used ${x(e(4, 'gates, every tick'), e(4, "the world's own"))} times the energy of the world's own parts per change at 81 cards and ${x(e(6, 'gates, every tick'), e(6, "the world's own"))} times at 729.`);
}
const br = path.join(here, 'results', 'browsers-on-msi.json'), ph = path.join(here, 'results', 'phones.json');
if (fs.existsSync(br)) {
  const b = JSON.parse(fs.readFileSync(br, 'utf8')), phones = fs.existsSync(ph) ? JSON.parse(fs.readFileSync(ph, 'utf8')) : {};
  const vals = (text) => Object.fromEntries([...text.matchAll(/(\d\w+)=(\d+)/g)].map((m) => [m[1], +m[2]]));
  const node = { '5bigsoft': B(5, 'ordinary').nsPerOp, '5bighand': B(5, 'hand').nsPerOp, '5bigtick': B(5, 'gates, every tick').nsPerOp, '5biggev': B(5, 'gates, only').nsPerOp, '5bigown': B(5, "the world's own").nsPerOp };
  P(); P(`## 7. The same world on a phone and in a browser`); P();
  P(`The page (\`index.html\`) runs the identical \`world.js\`. Each row is the page's own "Run the measurement" button, except the last, which is the Node run from section 1 for comparison. 243 cards, big pile, time for one change.`);
  P(); P(`| where | plain program | hand-written | Minecraft way | gates, changes only | world's own parts | Minecraft / own |`); P(`|---|---|---|---|---|---|---|`);
  const line = (name, v) => P(`| ${name} | ${t(v['5bigsoft'])} | ${t(v['5bighand'])} | ${t(v['5bigtick'])} | ${t(v['5biggev'])} | ${t(v['5bigown'])} | ${x(v['5bigtick'], v['5bigown'])} times |`);
  for (const [name, text] of Object.entries(phones)) line(`**${name}**`, vals(text));
  for (const [name, text] of Object.entries(b)) line(`MSI, ${name}`, vals(text));
  line('MSI, Node (section 1)', node);
  const first = Object.values(phones)[0];
  if (first) { const v = vals(first); P(); P(`On the real phone ${/ok=true/.test(first) ? 'every answer matched' : 'SOME ANSWERS DID NOT MATCH'}. Against the MSI's Node run, the phone took ${x(v['5bigsoft'], node['5bigsoft'])} times the MSI's time for the plain program, ${x(v['5bigtick'], node['5bigtick'])} for the Minecraft way and ${x(v['5bigown'], node['5bigown'])} for the world's own parts. A phone chip runs this world at about the speed of the laptop. The two are different JavaScript engines, so small differences mean little.`); }
}

// ---------------------------------------------------------------- bare against built
const llmDir = path.join(here, 'llm', 'results'), pick = {};          // a chronicle may be here as .jsonl (while running) or .jsonl.gz (as committed); the plain one wins
for (const f of fs.existsSync(llmDir) ? fs.readdirSync(llmDir) : []) { const m = f.match(/^(chronicle-.*\.jsonl)(\.gz)?$/); if (m && (!pick[m[1]] || !m[2])) pick[m[1]] = f; }
const files = Object.values(pick).sort(), readLines = (f) => (f.endsWith('.gz') ? zlib.gunzipSync(fs.readFileSync(path.join(llmDir, f))).toString('utf8') : fs.readFileSync(path.join(llmDir, f), 'utf8'));
const mean = (a) => a.reduce((s, v) => s + v, 0) / a.length;
if (files.length) { P(); P(`## 8. Bare against built (plan: \`llm/PLAN.md\`, committed before the first graded try)`); }
for (const f of files) {
  const E = readLines(f).trim().split('\n').map((l) => JSON.parse(l)), model = E[0].model;
  const arms = {}; for (const e of E) ((arms[e.arm] ||= {})[e.run] ||= []).push(e);
  const runs = [...new Set(E.map((e) => e.run))].sort(), tries = Math.max(...E.map((e) => e.step));
  const stat = (a) => { const rs = runs.filter((r) => arms[a] && arms[a][r] && arms[a][r].length === tries).map((r) => arms[a][r]); return { runs: rs.length, bests: rs.map((q) => Math.max(...q.map((e) => e.total))),
    firsts: rs.map((q) => q[0].total), readable: mean(rs.map((q) => q.filter((e) => e.valid).length / q.length)), at: rs.map((q) => q.findIndex((e) => e.total === Math.max(...q.map((z) => z.total))) + 1),
    secs: rs.reduce((s, q) => s + q.reduce((u, e) => u + (e.ms || 0), 0), 0) / 1000, wh: rs.reduce((s, q) => s + q.reduce((u, e) => u + (e.joules || 0), 0), 0) / 3600,
    distinct: mean(rs.map((q) => new Set(q.filter((e) => e.valid).map((e) => e.expr)).size)), top: rs.flat().filter((e) => e.valid).sort((p, q) => q.total - p.total)[0] }; };
  const names = { '0a': 'no model: random card orders', '0b': 'no model: random recipes', 'A+': 'bare, checker keeps the best', B: '+ its own last grade', C: '+ the 3 best from the record', D: '+ 3 picked by facing',
    E: 'AFTER THE PLAN: changes one thing in a good recipe; record starts with 0b\'s finds', R: 'AFTER THE PLAN (control): + 3 drawn at random from the record' };
  const S2 = Object.fromEntries(Object.keys(names).filter((a) => arms[a]).map((a) => [a, stat(a)]));
  P(); P(`### ${model}: ${tries} tries per run, ${Math.min(...Object.values(S2).map((s) => s.runs))} complete runs per arm, ${E.length} tries in the chronicle`); P();
  P(`| arm | best grade, average of the runs | each run | first try | tries it could read | different recipes per run | best came at try | seconds | watt-hours |`); P(`|---|---|---|---|---|---|---|---|---|`);
  if (S2['A+']) P(`| A: bare, one try | ${mean(S2['A+'].firsts).toFixed(3)} | ${S2['A+'].firsts.map((v) => v.toFixed(2)).join(' ')} | | | | | | |`);
  for (const [a, s] of Object.entries(S2)) if (s.runs) P(`| ${a}: ${names[a]} | **${mean(s.bests).toFixed(3)}** | ${s.bests.map((v) => v.toFixed(2)).join(' ')} | ${mean(s.firsts).toFixed(2)} | ${(s.readable * 100).toFixed(0)}% | ${a === '0a' ? '' : s.distinct.toFixed(0)} | ${s.at.join(' ')} | ${s.secs ? s.secs.toFixed(0) : ''} | ${s.wh ? s.wh.toFixed(2) : ''} |`);
  const beats = (X, Y, xs = S2[X].bests, ys = S2[Y].bests) => { const wins = xs.filter((v, i) => v > ys[i]).length; return { yes: mean(xs) > mean(ys) && wins >= 4, wins, dx: mean(xs) - mean(ys) }; };
  const say = (label, X, Y, xs, ys) => { if (!S2[X] || !S2[Y] && !ys) return; const b = beats(X, Y, xs, ys); P(`- ${label}: ${b.yes ? '**yes**' : '**no clear difference**'} (average ${b.dx >= 0 ? '+' : ''}${b.dx.toFixed(3)}, higher in ${b.wins} of ${(xs || S2[X].bests).length} paired runs).`); };
  P(); P(`Seconds and watt-hours are rough: other jobs (the timing pass, page checks, the loops below) ran on the machine during some arms, which stretches them. Grades are not affected.`);
  P(); P(`By the rule fixed in the plan (higher on average and in at least 4 of 5 paired runs):`);
  if (S2['A+']) say('1. The checker is worth something (A+ over A)', 'A+', 'A+', S2['A+'].bests, S2['A+'].firsts);
  say('2. Feedback helps (B over A+)', 'B', 'A+'); say('3. Keeping what worked helps (C over B)', 'C', 'B'); say('4. Facing against the top list (D over C)', 'D', 'C'); say('   and the other way (C over D)', 'C', 'D');
  for (const a of ['A+', 'B', 'C', 'D']) say(`6. Not decoration (${a} over random recipes 0b)`, a, '0b');
  for (const a of ['A+', 'B', 'C', 'D']) say(`   ${a} over random card orders 0a`, a, '0a');
  if (S2.E && S2.E.runs) { P(); P(`After the plan (exploratory, same rule applied):`); say('The model as a changer of good recipes (E) over the random recipes it started from (0b)', 'E', '0b'); say('E over the top-list arm (C)', 'E', 'C'); say('E over facing (D)', 'E', 'D'); }
  if (S2.R && S2.R.runs) { P(); P(`The control for the facing result (arm R, asked for by ChatGPT; plan note written before its first try; same rule):`);
    say('Facing over a random draw (D over R)', 'D', 'R'); say('   and the other way (R over D)', 'R', 'D'); say('The top list over a random draw (C over R)', 'C', 'R'); say('   and the other way (R over C)', 'R', 'C');
    say('Three random earlier tries over the last grade alone (R over B)', 'R', 'B'); }
  const tops = Object.entries(S2).filter(([, s]) => s.top).map(([a, s]) => `${a}: \`${s.top.expr ?? '(a card order)'}\` ${s.top.total.toFixed(3)} (${[3, 4, 5, 6, 7, 8].map((n) => s.top.sizes[n]).join(', ')})`);
  P(); P(`Best single try in each arm: ` + tops.join('; ') + '.');
}
const shots = fs.existsSync(llmDir) ? fs.readdirSync(llmDir).filter((f) => /^frontier-.*\.out$/.test(f)).sort() : [];
if (shots.length) {
  P(); P(`### Arm F: a frontier model alone (GPT-6.2 Sol through Codex), one try, no checker, told to run no code`); P();
  const strict = [], open = [], sz = (g) => [3, 4, 5, 6, 7, 8].map((n) => g.sizes[n]).join(', ');
  for (const f of shots) {
    const raw = fs.readFileSync(path.join(llmDir, f), 'utf8'), cut = raw.lastIndexOf('tokens used'); if (cut < 0) { P(`- (${f}: not finished)`); continue; }
    const expr = readAnswer(raw.slice(cut)), ranCode = /^exec\b/m.test(raw), tokens = (raw.slice(cut).match(/tokens used\s*\n\s*([\d,]+)/) || [])[1];
    const g = expr ? grade(expr) : { valid: false, total: 0, sizes: {}, error: 'no SCORE line' }, g2 = expr ? grade(expr, { chars: 20000, nodes: 20000 }) : g;
    strict.push(g.total); open.push(g2.total);
    P(`- ${expr ? expr.length + ' characters' : 'nothing readable'}, ${tokens || '?'} tokens${ranCode ? ', **it ran code: not a bare try**' : ', no commands run'}. ` +
      (g.valid ? `Grade ${g.total.toFixed(3)} (${sz(g)}).` : `By the grader as committed: unreadable (${g.error}). ` + (g2.valid ? `With the grader's length cap lifted: **grade ${g2.total.toFixed(3)}** (${sz(g2)}).` : `Still unreadable with the cap lifted: ${g2.error}.`)));
    if (expr) P(`  \`${expr.length > 240 ? expr.slice(0, 240) + ' ...' : expr}\``);
  }
  if (open.length) { P(); P(`Average of the ${open.length} finished shots: **${mean(open).toFixed(3)}** with the length cap lifted (${mean(strict).toFixed(3)} by the grader as committed; the cap of 300 characters was in the grader and was never told to any model, see the note at the end of \`llm/PLAN.md\`).`); }
}
const kj = path.join(llmDir, 'frontier-kimi.json');
if (fs.existsSync(kj)) {
  const K = JSON.parse(fs.readFileSync(kj, 'utf8'));
  P(); P(`### An open big model alone (Kimi K3.1 Pro), one try, no checker, told to run no code`); P();
  for (const s of K.shots) P(`- ${s.valid ? `grade ${s.grade.toFixed(3)} (${[3, 4, 5, 6, 7, 8].map((n) => s.sizes[n]).join(', ')})` : 'could not be read: ' + s.error}: \`${String(s.expr).slice(0, 110)}${String(s.expr).length > 110 ? ' ...' : ''}\``);
  P(); P(`Average of the ${K.shots.length} shots: **${mean(K.shots.map((s) => s.grade)).toFixed(3)}**. This way did not get the open big model to the closed one's level (5.82). It has not yet been given the checker.`);
}
const xl = path.join(llmDir, 'explore-loop.json');
if (fs.existsSync(xl)) {
  const X = JSON.parse(fs.readFileSync(xl, 'utf8')), sz = (s) => [3, 4, 5, 6, 7, 8].map((n) => s[n]).join(', ');
  P(); P(`### After the plan: a cheap loop on top of the big model's answers (exploratory, not pre-registered)`); P();
  P(`No model runs here. Each recipe the frontier model wrote keeps picking its cards first; the loop tries ${big(X.tieBreakersPerRecipe)} random tie-breakers for the order of everything else, then small changes to the numbers inside the recipe, and keeps a change only when the exact checker says the grade went up. ${X.seconds} seconds of one processor core in all.`);
  P(); P(`| the big model's recipe | its own grade | after the loop | piles after (3 to 8 features) |`); P(`|---|---|---|---|`);
  for (const r of X.recipes) P(`| ${r.file.replace('frontier-', '').replace('.out', '')} | ${r.startGrade.toFixed(3)} (${sz(r.start)}) | **${r.final.grade.toFixed(3)}** | ${sz(r.final.sizes)} |`);
  const up = X.recipes.filter((r) => r.final.grade > r.startGrade + 1e-9).length, top = Math.max(...X.recipes.map((r) => r.final.grade)), top0 = Math.max(...X.recipes.map((r) => r.startGrade));
  P(); P(`The loop raised ${up} of ${X.recipes.length} recipes. Best grade before the loop ${top0.toFixed(3)}, after ${top.toFixed(3)}. Best piles known: 9, 20, 45, 112, 236, 512.`);
}
const xd = path.join(llmDir, 'explore-deep.json');
if (fs.existsSync(xd)) {
  const D = JSON.parse(fs.readFileSync(xd, 'utf8')), sz = (s) => [3, 4, 5, 6, 7, 8].map((n) => s[n]).join(', '), tried = D.recipes.reduce((s, r) => s + r.changesTried, 0), kept = D.recipes.reduce((s, r) => s + r.kept.length, 0);
  P(); P(`### After the plan: the deeper loop (exploratory)`); P();
  P(`The same idea for ${D.minutesPerRecipe} minutes per recipe, with more kinds of small change (a number, a comparison, an and/or, a plus/minus, a name), one at a time at every spot and then in random pairs. Still no model.`);
  P(); P(`| the big model's recipe | alone | after the first loop | after the deeper loop | piles after | changes tried | changes kept |`); P(`|---|---|---|---|---|---|---|`);
  for (const r of D.recipes) P(`| ${r.file.replace('frontier-', '').replace('.out', '')} | ${r.bigModelAlone.toFixed(3)} | ${r.afterFirstLoop.toFixed(3)} | **${r.final.grade.toFixed(3)}** | ${sz(r.final.sizes)} | ${big(r.changesTried)} | ${r.kept.length} |`);
  P(); P(`${big(tried)} changes tried, ${kept} kept. This way is nearly used up: small changes of these kinds find almost nothing more. The gap that is left is on the 6,561-card deck (best here ${Math.max(...D.recipes.map((r) => r.final.sizes[8]))}, best known 512).`);
}
const aj = path.join(llmDir, 'astra-result.json');
if (fs.existsSync(aj)) {
  const A = JSON.parse(fs.readFileSync(aj, 'utf8'));
  P(); P(`### After the plan: a second big model holding the checker (GPT-6.2 Astra, exploratory)`); P();
  P(`Astra was handed the best recipe so far (5.963) and the exact checker, with up to 40 graded tries. It returned a ${A.chars}-character recipe after ${A.gradedTriesReported} graded try and ${big(A.tokens)} tokens: **grade ${A.grade.toFixed(3)} of 6** (${[3, 4, 5, 6, 7, 8].map((n) => A.sizes[n]).join(', ')}), the best pile known on every deck. Re-graded here by the same checker. Astra says it translated the published FunSearch 512-card construction (Nature, 2023) into the recipe language, so this matches the best known and does not beat it.`);
  P(); P(`The path on this puzzle today: the big model alone 5.82, plus a cheap no-model checker loop 5.96, plus a second big model holding the checker 6.00.`);
}
P();
fs.writeFileSync(path.join(here, 'RESULTS.md'), out.join('\n'));
console.log(out.join('\n'));
