// The same job done different ways, and the workloads that time them. Plain ES module (Node and browser).
// Job: a pile of cards changes; after each change say whether the pile holds a set.
import { EventEngine, DenseEngine, rng } from './world.js';

class Pile {                          // who is in, kept by every way so that clearing costs the same everywhere
  constructor(N) { this.inp = new Uint8Array(N); this.list = new Uint16Array(N); this.pos = new Int32Array(N); this.k = 0; }
  flip(c) {
    if (this.inp[c]) { this.inp[c] = 0; const p = this.pos[c], last = this.list[--this.k]; this.list[p] = last; this.pos[last] = p; return 0; }
    this.inp[c] = 1; this.pos[c] = this.k; this.list[this.k++] = c; return 1;
  }
}

// ---------------------------------------------------------------- ways to answer "is there a set?"
export function waySoftNaive(G) {      // ordinary software: look at every pair again each time
  const { N, tab } = G, pile = new Pile(N); let work = 0;
  return {
    name: 'ordinary software (re-check)', bytes: tab.byteLength + N * 7,
    toggle(c) { pile.flip(c); },
    answer() {
      const { inp, list, k } = pile; let w = 0;
      for (let i = 0; i < k; i++) { const row = list[i] * N; for (let j = i + 1; j < k; j++) { w++; if (inp[tab[row + list[j]]]) { work += w; return 1; } } }
      work += w; return 0;
    },
    clear() { while (pile.k) pile.flip(pile.list[pile.k - 1]); }, work: () => work,
  };
}

export function waySoftCounters(G) {   // the same idea as the world's own parts, written by hand with no world around it
  const { N, L, per, cardLines } = G, pile = new Pile(N), cnt = new Uint8Array(L); let sets = 0, work = 0;
  const flip = (c) => {
    const base = c * per;
    if (pile.flip(c)) { for (let i = 0; i < per; i++) if (++cnt[cardLines[base + i]] === 3) sets++; }
    else { for (let i = 0; i < per; i++) if (cnt[cardLines[base + i]]-- === 3) sets--; }
    work += per;
  };
  return { name: 'hand-written counters', bytes: cardLines.byteLength + L + N * 7, toggle: flip, answer: () => (sets > 0 ? 1 : 0),
    clear() { while (pile.k) flip(pile.list[pile.k - 1]); }, work: () => work };
}

export function wayWorld(G, world, stepping, label) {   // any world, stepped 'event', 'tick' or 'sweep'
  const N = G.N, pile = new Pile(N), alarm = world.alarm;
  if (stepping === 'event') {
    const e = new EventEngine(world);
    return { name: label, bytes: world.bytes + e.bytes, engine: e,
      toggle(c) { e.set(c, pile.flip(c)); },
      toggleMany(cards, off, m) { for (let i = 0; i < m; i++) pile.flip(cards[off + i]); e.setMany(cards, off, m); },
      answer: () => e.out[alarm],
      clear() { while (pile.k) { const c = pile.list[pile.k - 1]; pile.flip(c); e.set(c, 0); } }, work: () => e.msgs };
  }
  const d = new DenseEngine(world);
  return { name: label, bytes: world.bytes + d.bytes, engine: d,
    toggle(c) { d.out[c] = pile.flip(c); },
    answer: stepping === 'tick' ? () => { d.settle(); return d.out[alarm]; } : () => { d.sweep(); return d.out[alarm]; },
    clear() { while (pile.k) { const c = pile.list[pile.k - 1]; pile.flip(c); d.out[c] = 0; } }, work: () => d.evals, ticks: () => d.ticks };
}

// ---------------------------------------------------------------- workloads (fixed by a seed, so every way gets the same questions)
export function makeStream(G, seed, steps, target) {   // one card changes at a time; the pile hovers near `target` cards
  const r = rng(seed), N = G.N, pile = new Pile(N), seq = new Uint16Array(steps);
  for (let s = 0; s < steps; s++) {
    const add = pile.k === 0 || (pile.k < N && r() < (pile.k < target ? 0.7 : 0.3));
    let c;
    if (add) { do { c = (r() * N) | 0; } while (pile.inp[c]); } else c = pile.list[(r() * pile.k) | 0];
    pile.flip(c); seq[s] = c;
  }
  return seq;
}
export function runStream(way, seq, steps, answers) {
  for (let s = 0; s < steps; s++) { way.toggle(seq[s]); answers[s] = way.answer(); }
}

export function makePiles(G, seed, count, k) {         // fresh piles of k cards, each checked from an empty table
  const r = rng(seed), N = G.N, out = new Uint16Array(count * k), seen = new Uint8Array(N);
  for (let p = 0; p < count; p++) {
    for (let i = 0; i < k; i++) { let c; do { c = (r() * N) | 0; } while (seen[c]); seen[c] = 1; out[p * k + i] = c; }
    for (let i = 0; i < k; i++) seen[out[p * k + i]] = 0;
  }
  return out;
}
export function runOneShot(way, piles, count, k, answers) {
  for (let p = 0; p < count; p++) { for (let i = 0; i < k; i++) way.toggle(piles[p * k + i]); answers[p] = way.answer(); way.clear(); }
}

export function makeChurn(G, seed, steps, m) {         // m cards change at once, every step
  const r = rng(seed), N = G.N, out = new Uint16Array(steps * m), seen = new Uint8Array(N);
  for (let s = 0; s < steps; s++) {
    for (let i = 0; i < m; i++) { let c; do { c = (r() * N) | 0; } while (seen[c]); seen[c] = 1; out[s * m + i] = c; }
    for (let i = 0; i < m; i++) seen[out[s * m + i]] = 0;
  }
  return out;
}
export function runChurn(way, seq, steps, m, answers) {
  for (let s = 0; s < steps; s++) {
    if (way.toggleMany) way.toggleMany(seq, s * m, m); else for (let i = 0; i < m; i++) way.toggle(seq[s * m + i]);
    answers[s] = way.answer();
  }
}

// ---------------------------------------------------------------- ways to search (which cards can still be taken?)
export function searchSoftNaive(G) {    // ordinary software: work it out again from the pile each time it is asked
  const { N, tab } = G; let pile = new Pile(N), work = 0;
  const isFree = (c) => {
    const { inp, list, k } = pile; if (inp[c]) return 0;
    for (let i = 0; i < k; i++) { work++; if (inp[tab[list[i] * N + c]]) return 0; }
    return 1;
  };
  return { name: 'ordinary software (re-check)', reset() { pile = new Pile(N); }, place(c) { pile.flip(c); }, unplace(c) { pile.flip(c); }, isFree,
    freeCount() { let f = 0; for (let c = 0; c < N; c++) f += isFree(c); return f; }, work: () => work };
}

export function searchSoftCounters(G) { // hand-written: keep a "blocked" count on every card, change it as cards come and go
  const { N, per, cardLines, lines } = G;
  const others = new Uint16Array(N * per * 2);
  for (let c = 0; c < N; c++) for (let i = 0; i < per; i++) {
    const l = cardLines[c * per + i]; let q = 0;
    for (let m = 0; m < 3; m++) { const x = lines[l * 3 + m]; if (x !== c) others[(c * per + i) * 2 + q++] = x; }
  }
  let inp = new Uint8Array(N), blocked = new Int16Array(N), free = N, work = 0;
  return {
    name: 'hand-written counters',
    reset() { inp = new Uint8Array(N); blocked = new Int16Array(N); free = N; },
    place(x) {
      for (let i = 0; i < per; i++) {
        const y = others[(x * per + i) * 2], z = others[(x * per + i) * 2 + 1];
        if (inp[y]) { if (blocked[z]++ === 0 && !inp[z]) free--; }
        if (inp[z]) { if (blocked[y]++ === 0 && !inp[y]) free--; }
      }
      inp[x] = 1; if (blocked[x] === 0) free--; work += per;
    },
    unplace(x) {
      for (let i = 0; i < per; i++) {
        const y = others[(x * per + i) * 2], z = others[(x * per + i) * 2 + 1];
        if (inp[y]) { if (--blocked[z] === 0 && !inp[z]) free++; }
        if (inp[z]) { if (--blocked[y] === 0 && !inp[y]) free++; }
      }
      inp[x] = 0; if (blocked[x] === 0) free++; work += per;
    },
    isFree: (c) => (!inp[c] && blocked[c] === 0 ? 1 : 0), freeCount: () => free, work: () => work,
  };
}

export function searchWorld(G, world) { // the world keeps that state itself: read a part, no asking
  const e = new EventEngine(world), { free0, tally } = world, N = G.N;
  return { name: "the world's own parts", engine: e, bytes: world.bytes + e.bytes,
    reset() { for (let c = 0; c < N; c++) if (e.out[c]) e.set(c, 0); },          // take the cards back off the table
    place(c) { e.set(c, 1); }, unplace(c) { e.set(c, 0); },
    isFree: (c) => e.out[free0 + c], freeCount: () => e.acc[tally], work: () => e.msgs };
}

// a big pile with no set in it; each move tries one more card and takes it back if it makes a set
export function makeTryStream(G, seed, moves) {
  const r = rng(seed), N = G.N, S = searchSoftCounters(G), pile = new Pile(N), seq = [];
  for (const c of greedyOrder(S, shuffled(N, seed))) { pile.flip(c); seq.push(c); }
  const start = seq.length;
  for (let m = 0; m < moves; m++) {
    let c; do { c = (r() * N) | 0; } while (pile.inp[c]);
    if (S.isFree(c)) { S.place(c); pile.flip(c); seq.push(c); const out = pile.list[(r() * pile.k) | 0]; S.unplace(out); pile.flip(out); seq.push(out); }
    else { seq.push(c); seq.push(c); }
  }
  return { seq: Uint16Array.from(seq), start, size: pile.k };
}

export function greedyOrder(S, order) {       // take every card that is still free, in the given order
  S.reset(); const pile = [];
  for (let i = 0; i < order.length; i++) { const c = order[i]; if (S.isFree(c)) { S.place(c); pile.push(c); } }
  return pile;
}
export function greedyLookahead(S, order) {   // each turn, try every free card and keep the one that leaves the most cards free
  S.reset(); const pile = [];
  for (;;) {
    let best = -1, bestLeft = -1;
    for (let i = 0; i < order.length; i++) {
      const c = order[i]; if (!S.isFree(c)) continue;
      S.place(c); const left = S.freeCount(); S.unplace(c);
      if (left > bestLeft) { bestLeft = left; best = c; }
    }
    if (best < 0) break;
    S.place(best); pile.push(best);
  }
  return pile;
}
export function shuffled(N, seed) { const r = rng(seed), a = Uint16Array.from({ length: N }, (_, i) => i); for (let i = N - 1; i > 0; i--) { const j = (r() * (i + 1)) | 0; const t = a[i]; a[i] = a[j]; a[j] = t; } return a; }

// ---------------------------------------------------------------- timing
export const now = () => (typeof performance !== 'undefined' ? performance.now() : Date.now());
export function timeBest(fn, repeats = 3) { let best = Infinity; for (let i = 0; i < repeats; i++) { const t = now(); fn(); const d = now() - t; if (d < best) best = d; } return best; }
export function sameAnswers(a, b, n) { for (let i = 0; i < n; i++) if (a[i] !== b[i]) return false; return true; }
