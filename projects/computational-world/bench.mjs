// Computational World, Prototype 0: the measurements.   node bench.mjs [--quick] [--energy] [--label name]
// Every way gets the same questions (fixed seeds). Every answer is compared with ordinary software, and ordinary
// software is compared with the Verifier. Work counts are exact and must be the same on any machine.
import fs from 'node:fs';
import os from 'node:os';
import { spawn } from 'node:child_process';
import { geometry, withLines, buildGateCheck, buildNativeCheck, buildNativeSearch, EventEngine, Chronicle, stateMark, findSet, findSetSlow } from './world.js';
import * as Y from './ways.js';

const argv = process.argv.slice(2), flag = (f) => argv.includes(f);
const label = flag('--label') ? argv[argv.indexOf('--label') + 1] : 'msi';
const sizes = flag('--quick') ? [4, 5] : [4, 5, 6];
const rows = [], facts = [];
const row = (r) => { rows.push(r); console.log(`${r.workload.padEnd(26)} n=${r.n}  ${r.way.padEnd(40)} ${fmt(r.nsPerOp).padStart(11)}  work ${String(r.workPerOp).padStart(11)}  ${r.ok ? 'ok' : 'WRONG'}`); };
const fmt = (ns) => (ns >= 1e6 ? (ns / 1e6).toFixed(2) + ' ms' : ns >= 1e3 ? (ns / 1e3).toFixed(2) + ' us' : ns.toFixed(0) + ' ns');
const mark = (a, n) => { let h = 0x811c9dc5 | 0; for (let i = 0; i < n; i++) h = Math.imul(h ^ a[i], 16777619); return (h >>> 0).toString(16).padStart(8, '0'); };

// ---------------------------------------------------------------- self-test: small worlds, every answer against the definition itself
function selfTest() {
  for (const n of [2, 3, 4]) {
    const G = withLines(geometry(n)), gate = buildGateCheck(G), nat = buildNativeCheck(G), srch = buildNativeSearch(G);
    const ways = [Y.waySoftNaive(G), Y.waySoftCounters(G), Y.wayWorld(G, gate, 'tick', 'gt'), Y.wayWorld(G, gate, 'sweep', 'gs'), Y.wayWorld(G, gate, 'event', 'ge'),
      Y.wayWorld(G, nat, 'tick', 'nt'), Y.wayWorld(G, nat, 'sweep', 'ns'), Y.wayWorld(G, nat, 'event', 'ne'), Y.wayWorld(G, srch, 'event', 'se')];
    const steps = n === 4 ? 1500 : 600, seq = Y.makeStream(G, 7 + n, steps, n === 4 ? 9 : n + 2), inp = new Uint8Array(G.N);
    for (let s = 0; s < steps; s++) {
      inp[seq[s]] ^= 1; const pile = []; for (let c = 0; c < G.N; c++) if (inp[c]) pile.push(c);
      const truth = findSetSlow(G, pile) ? 1 : 0, v = findSet(G, pile) ? 1 : 0;
      if (v !== truth) throw new Error(`Verifier disagrees with the definition at n=${n} step ${s}`);
      for (const w of ways) { w.toggle(seq[s]); if (w.answer() !== truth) throw new Error(`${w.name} wrong at n=${n} step ${s}`); }
    }
    // the search ways must agree on which cards are free and how many, and on the piles they build
    const S = [Y.searchSoftNaive(G), Y.searchSoftCounters(G), Y.searchWorld(G, srch)];
    for (let t = 0; t < 6; t++) {
      const order = Y.shuffled(G.N, 100 + t), piles = S.map((s) => Y.greedyOrder(s, order)), look = S.map((s) => Y.greedyLookahead(s, order));
      for (const p of [...piles, ...look]) if (findSetSlow(G, p)) throw new Error('a built pile holds a set');
      if (new Set(piles.map(String)).size !== 1 || new Set(look.map(String)).size !== 1) throw new Error(`search ways built different piles at n=${n}`);
    }
  }
  console.log('self-test passed: every way agrees with the definition on small worlds\n');
}

// ---------------------------------------------------------------- one way through one workload
function timed(way, run, steps, answers, ref, prep) {             // prep: untimed setup before each run (for example, laying out the starting pile)
  way.clear(); if (prep) prep(way); run(way, answers);              // warm-up
  let best = Infinity, work = 0;
  for (let r = 0; r < 3; r++) { way.clear(); if (prep) prep(way); const w0 = way.work(), t = Y.now(); run(way, answers); const d = Y.now() - t; work += way.work() - w0; if (d < best) best = d; }
  return { nsPerOp: (best * 1e6) / steps, workPerOp: +((work / 3) / steps).toFixed(2), ok: Y.sameAnswers(answers, ref, steps) };
}

function checkWays(G, worlds) {
  const { gate, nat } = worlds;
  return [
    ['fast', Y.waySoftNaive(G)], ['fast', Y.waySoftCounters(G)],
    ['tick', Y.wayWorld(G, gate, 'tick', 'gates, every tick (the Minecraft way)')],
    ['sweep', Y.wayWorld(G, gate, 'sweep', 'gates, one sweep per answer')],
    ['fast', Y.wayWorld(G, gate, 'event', 'gates, only what changed')],
    ['tick', Y.wayWorld(G, nat, 'tick', 'own parts, every tick')],
    ['sweep', Y.wayWorld(G, nat, 'sweep', 'own parts, one sweep per answer')],
    ['fast', Y.wayWorld(G, nat, 'event', "the world's own parts, only what changed")],
  ];
}
const STEPS = { fast: { 4: 200000, 5: 100000, 6: 50000 }, sweep: { 4: 20000, 5: 5000, 6: 1500 }, tick: { 4: 5000, 5: 1000, 6: 300 } };
const HOVER = { 4: 8, 5: 12, 6: 18 };

function benchSize(n) {
  const t0 = Y.now(), G = withLines(geometry(n)), tg = Y.now();
  const gate = buildGateCheck(G), nat = buildNativeCheck(G), srch = buildNativeSearch(G), tb = Y.now();
  for (const [name, w] of [['gates', gate], ['own parts', nat], ['own parts + search state', srch]]) {
    facts.push(`n=${n} ${name}: ${w.P} parts, ${w.K} links, ${w.maxLevel} deep`);
    console.log(`n=${n}  ${name}: ${w.P} parts, ${w.K} links, ${w.maxLevel} levels deep, ${(w.bytes / 1024).toFixed(0)} KB`);
  }
  console.log(`n=${n}  ${G.N} cards, ${G.L} sets; geometry ${(tg - t0).toFixed(0)} ms, three worlds built in ${(tb - tg).toFixed(0)} ms\n`);
  const worlds = { gate, nat, srch };

  // --- A. one card changes at a time
  { const full = STEPS.fast[n], seq = Y.makeStream(G, 1000 + n, full, HOVER[n]), ref = new Uint8Array(full);
    const soft = Y.waySoftNaive(G); Y.runStream(soft, seq, full, ref);
    const inp = new Uint8Array(G.N); let bad = 0;                   // ordinary software against the Verifier
    for (let s = 0; s < 3000; s++) { inp[seq[s]] ^= 1; const pile = []; for (let c = 0; c < G.N; c++) if (inp[c]) pile.push(c); if ((findSet(G, pile) ? 1 : 0) !== ref[s]) bad++; }
    if (bad) throw new Error('ordinary software disagrees with the Verifier');
    let yes = 0; for (let s = 0; s < full; s++) yes += ref[s];
    facts.push(`n=${n} stream: ${full} changes, a set is present after ${yes} of them, answers ${mark(ref, full)}`);
    for (const [cls, way] of checkWays(G, worlds)) {
      const steps = STEPS[cls][n], ans = new Uint8Array(steps), r = timed(way, (w, a) => Y.runStream(w, seq, steps, a), steps, ans, ref);
      row({ workload: 'one card changes', n, way: way.name, steps, bytes: way.bytes, ...r });
      if (cls !== 'fast' || way.engine) facts.push(`n=${n} stream ${way.name}: work per change ${r.workPerOp} over ${steps}`);
    }
    // what memory costs: the same run with every change written to the Chronicle, then replayed on a fresh world
    const steps = full, ans = new Uint8Array(steps), chron = new Chronicle(), way = Y.wayWorld(G, nat, 'event', "the world's own parts + Chronicle");
    const run = (w, a) => { for (let s = 0; s < steps; s++) { w.toggle(seq[s]); a[s] = w.answer(); chron.add(seq[s], a[s]); } };
    const r = timed(way, (w, a) => { chron.n = 0; chron.chain = 0x811c9dc5 | 0; run(w, a); }, steps, ans, ref);
    row({ workload: 'one card changes', n, way: way.name, steps, bytes: way.bytes + chron.bytes(), ...r });
    const fresh = new EventEngine(nat); let good = true, i = 0; const t = Y.now();
    chron.replay((card, answer) => { fresh.set(card, fresh.out[card] ^ 1); if (fresh.out[nat.alarm] !== answer) good = false; i++; });
    const replayMs = Y.now() - t, same = stateMark(fresh.out) === stateMark(way.engine.out) && Chronicle.chainOf(chron.buf, chron.n) === chron.chain;
    row({ workload: 'replay the Chronicle', n, way: 'fresh world, same history', steps, bytes: chron.bytes(), nsPerOp: (replayMs * 1e6) / steps, workPerOp: +(fresh.msgs / steps).toFixed(2), ok: good && same });
    facts.push(`n=${n} chronicle: ${chron.n} entries, chain ${(chron.chain >>> 0).toString(16)}, replay lands on the same state: ${good && same}`);
  }

  // --- A2. the same, on a big pile with no set in it (where a search actually lives): try a card, take it back if it makes a set
  { const moves = STEPS.fast[n] / 4, T = Y.makeTryStream(G, 1500 + n, moves), size = T.size, lay = T.seq.subarray(0, T.start), seq = T.seq.subarray(T.start), full = seq.length, ref = new Uint8Array(full);
    const prep = (w) => { for (let i = 0; i < lay.length; i++) w.toggle(lay[i]); };     // lay the starting pile down first; only the moves are timed
    { const w = Y.waySoftNaive(G); prep(w); Y.runStream(w, seq, full, ref); }
    const inp = new Uint8Array(G.N); let bad = 0; for (const c of lay) inp[c] ^= 1;
    for (let s = 0; s < Math.min(full, 2500); s++) { inp[seq[s]] ^= 1; const pile = []; for (let c = 0; c < G.N; c++) if (inp[c]) pile.push(c); if ((findSet(G, pile) ? 1 : 0) !== ref[s]) bad++; }
    if (bad) throw new Error('ordinary software disagrees with the Verifier (big pile)');
    facts.push(`n=${n} big pile of about ${size}: ${full} changes, answers ${mark(ref, full)}`);
    for (const [cls, way] of checkWays(G, worlds)) {
      const steps = Math.min(full, STEPS[cls][n]), ans = new Uint8Array(steps), r = timed(way, (w, a) => Y.runStream(w, seq, steps, a), steps, ans, ref, prep);
      row({ workload: `one card changes, big pile (~${size})`, n, way: way.name, steps, bytes: way.bytes, ...r });
    }
  }

  // --- B. a fresh pile each time
  { const k = HOVER[n], count = Math.round(STEPS.fast[n] / 10), piles = Y.makePiles(G, 2000 + n, count, k), ref = new Uint8Array(count);
    Y.runOneShot(Y.waySoftNaive(G), piles, count, k, ref);
    let bad = 0; for (let p = 0; p < 500; p++) if ((findSet(G, Array.from(piles.subarray(p * k, p * k + k))) ? 1 : 0) !== ref[p]) bad++;
    if (bad) throw new Error('ordinary software disagrees with the Verifier (fresh piles)');
    facts.push(`n=${n} fresh piles of ${k}: ${count} piles, answers ${mark(ref, count)}`);
    for (const [cls, way] of checkWays(G, worlds)) {
      const c = Math.max(50, Math.round(STEPS[cls][n] / 10)), ans = new Uint8Array(c), r = timed(way, (w, a) => Y.runOneShot(w, piles, c, k, a), c, ans, ref);
      row({ workload: `fresh pile of ${k} cards`, n, way: way.name, steps: c, bytes: way.bytes, ...r });
    }
  }

  // --- C. many cards change at once: where does "only what changed" stop paying?
  for (const share of [0.02, 0.05, 0.1, 0.25, 0.5]) {
    const m = Math.max(2, Math.round(G.N * share)), steps = Math.round(STEPS.sweep[n] / 2), seq = Y.makeChurn(G, 3000 + n + m, steps, m), ref = new Uint8Array(steps);
    Y.runChurn(Y.waySoftNaive(G), seq, steps, m, ref);
    for (const way of [Y.waySoftCounters(G), Y.wayWorld(G, nat, 'event', "the world's own parts, only what changed"), Y.wayWorld(G, nat, 'sweep', 'own parts, one sweep per answer')]) {
      const ans = new Uint8Array(steps), r = timed(way, (w, a) => Y.runChurn(w, seq, steps, m, a), steps, ans, ref);
      row({ workload: `${m} cards change at once (${Math.round(share * 100)}%)`, n, way: way.name, steps, bytes: way.bytes, ...r });
    }
  }

  // --- D. search: build a pile with no set in it
  { const S = [Y.searchSoftNaive(G), Y.searchSoftCounters(G), Y.searchWorld(G, srch)];
    const builds = { 4: 300, 5: 60, 6: 12 }[n], looks = { 4: 12, 5: 3, 6: 1 }[n];
    for (const [title, fn, count] of [['take free cards in a random order', Y.greedyOrder, builds], ['look ahead one card', Y.greedyLookahead, looks]]) {
      const piles = [];
      for (const s of S) {
        const mine = []; fn(s, Y.shuffled(G.N, 4000));               // warm-up
        const w0 = s.work(), t = Y.now(); for (let b = 0; b < count; b++) mine.push(fn(s, Y.shuffled(G.N, 4000 + b)));
        const ms = Y.now() - t; piles.push(mine);
        const clean = mine.every((p) => findSet(G, p) === null), sizes = mine.map((p) => p.length);
        row({ workload: title, n, way: s.name, steps: count, bytes: s.bytes || 0, nsPerOp: (ms * 1e6) / count, workPerOp: Math.round((s.work() - w0) / count), ok: clean,
          best: Math.max(...sizes), mean: +(sizes.reduce((a, b) => a + b, 0) / count).toFixed(2) });
      }
      const agree = piles.every((p) => String(p) === String(piles[0]));
      if (!agree) throw new Error(`the search ways built different piles (${title}, n=${n})`);
      const sizes = piles[0].map((p) => p.length);
      facts.push(`n=${n} ${title}: ${count} piles, sizes ${sizes.slice(0, 12).join(' ')}${sizes.length > 12 ? ' ...' : ''}, best ${Math.max(...sizes)}`);
    }
  }
  console.log('');
}

// ---------------------------------------------------------------- energy: the processor's own power meter (Windows, Intel RAPL)
async function energyPass() {
  const csv = `results/_power-${label}.csv`; try { fs.unlinkSync(csv); } catch {}
  const tp = spawn('typeperf', ['\\Energy Meter(RAPL_Package0_PKG)\\Power', '-si', '1', '-o', csv, '-y'], { stdio: 'ignore' });
  const sleep = (ms) => new Promise((r) => setTimeout(r, ms)), blocks = [];
  await sleep(6000); blocks.push({ name: 'idle', t0: Date.now() - 4000, t1: Date.now(), ops: 0 });
  for (const n of [4, 6]) {
    const G = withLines(geometry(n)), gate = buildGateCheck(G), nat = buildNativeCheck(G);
    const seq = Y.makeStream(G, 1000 + n, STEPS.fast[n], HOVER[n]), ans = new Uint8Array(STEPS.fast[n]);
    const list = [[Y.waySoftNaive(G), STEPS.fast[n]], [Y.waySoftCounters(G), STEPS.fast[n]], [Y.wayWorld(G, nat, 'event', "the world's own parts, only what changed"), STEPS.fast[n]],
      [Y.wayWorld(G, gate, 'event', 'gates, only what changed'), STEPS.fast[n]], [Y.wayWorld(G, gate, 'tick', 'gates, every tick (the Minecraft way)'), STEPS.tick[n]]];
    for (const [way, steps] of list) {
      await sleep(1500);
      const t0 = Date.now(); let ops = 0;
      while (Date.now() - t0 < 5000) { way.clear(); Y.runStream(way, seq, steps, ans); ops += steps; }
      blocks.push({ name: `n=${n} ${way.name}`, t0, t1: Date.now(), ops });
    }
  }
  await sleep(2500); tp.kill(); await sleep(500);
  const samples = fs.readFileSync(csv, 'utf8').split(/\r?\n/).slice(1).map((l) => l.replace(/"/g, '').split(',')).filter((c) => c.length >= 2 && !isNaN(+c[1]))
    .map((c) => ({ t: new Date(c[0]).getTime(), w: +c[1] / 1000 }));
  const avg = (b) => { const s = samples.filter((x) => x.t >= b.t0 + 1000 && x.t <= b.t1); return s.length ? s.reduce((a, x) => a + x.w, 0) / s.length : NaN; };
  const idle = avg(blocks[0]), out = [];
  console.log(`\nEnergy (processor package meter): idle ${idle.toFixed(1)} W`);
  for (const b of blocks.slice(1)) {
    const w = avg(b), secs = (b.t1 - b.t0) / 1000, e = { name: b.name, watts: +w.toFixed(1), ops: b.ops, microJoulePerOp: +((w * secs * 1e6) / b.ops).toFixed(3), aboveIdleMicroJoulePerOp: +(((w - idle) * secs * 1e6) / b.ops).toFixed(3) };
    out.push(e); console.log(`  ${b.name.padEnd(52)} ${e.watts} W   ${e.microJoulePerOp} uJ per change  (${e.aboveIdleMicroJoulePerOp} above idle)`);
  }
  try { fs.unlinkSync(csv); } catch {}
  return { idleWatts: +idle.toFixed(1), blocks: out };
}

// ---------------------------------------------------------------- main
if (!flag('--no-write')) fs.mkdirSync('results', { recursive: true });
selfTest();
for (const n of sizes) benchSize(n);
const energy = flag('--energy') ? await energyPass() : null;
let h = 0x811c9dc5 | 0; for (const f of facts) for (let i = 0; i < f.length; i++) h = Math.imul(h ^ f.charCodeAt(i), 16777619);
const machine = { cpu: os.cpus()[0].model.trim(), threads: os.cpus().length, node: process.version, platform: process.platform, when: new Date().toISOString() };
console.log('\nFacts that must match on any machine:'); for (const f of facts) console.log('  ' + f);
console.log(`\nfacts mark ${(h >>> 0).toString(16)}   all answers correct: ${rows.every((r) => r.ok)}`);
if (!flag('--no-write')) fs.writeFileSync(`results/${label}.json`, JSON.stringify({ machine, sizes, rows, facts, factsMark: (h >>> 0).toString(16), energy }, null, 1));
