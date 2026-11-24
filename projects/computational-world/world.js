// Computational World, Prototype 0 (Heartbeat Observatory, 11/23/2026). CC0.
// Plain ES module with no dependencies: the same file runs under Node on the MSI and in a phone browser.
//
// A world is PARTS joined by LINKS, and it has one RULE:
//   every part keeps a running total of what its links deliver, and shows 1 when the total reaches its mark, else 0.
// STATE  = each part's total and its 0/1.          LINKS  = who tells whom, with a weight.
// EVENTS = a part changing between 0 and 1.        MEMORY = the Chronicle (append-only, replayable).
// The VERIFIER is separate code that shares nothing with the engines.
//
// A part with two inputs and mark 2 is an AND gate; with mark 1 an OR gate. That is the hardware-style vocabulary
// (the Minecraft way). A part with many inputs is a counter or a tally. That is the world's own vocabulary.
// Two engines step any world: Dense (every part, every tick) and Event (only what a change touches).

// ---------------------------------------------------------------- the card puzzle (SET in n features)
export function geometry(n) {
  const N = 3 ** n, pow = Array.from({ length: n }, (_, k) => 3 ** k);
  const dig = new Uint8Array(N * n);
  for (let c = 0; c < N; c++) { let v = c; for (let k = 0; k < n; k++) { dig[c * n + k] = v % 3; v = (v - (v % 3)) / 3; } }
  // the one card that completes a set with a and b: same digit where they agree, the missing digit where they differ
  const third = (a, b) => {
    let c = 0; const ao = a * n, bo = b * n;
    for (let k = 0; k < n; k++) { const x = dig[ao + k], y = dig[bo + k]; c += (x === y ? x : 3 - x - y) * pow[k]; }
    return c;
  };
  return { n, N, dig, pow, third };
}

export function withLines(G) {   // lookup table + every set ("line") + the lines through each card. Fine up to n = 6.
  const { N, third } = G;
  const tab = new Uint16Array(N * N);
  for (let a = 0; a < N; a++) for (let b = 0; b < N; b++) tab[a * N + b] = a === b ? a : third(a, b);
  const L = (N * (N - 1)) / 6, lines = new Uint16Array(L * 3);
  let q = 0;
  for (let a = 0; a < N; a++) for (let b = a + 1; b < N; b++) { const c = tab[a * N + b]; if (c > b) { lines[q++] = a; lines[q++] = b; lines[q++] = c; } }
  const per = (N - 1) / 2, cardLines = new Uint32Array(N * per), fill = new Uint16Array(N);
  for (let l = 0; l < L; l++) for (let m = 0; m < 3; m++) { const c = lines[l * 3 + m]; cardLines[c * per + fill[c]++] = l; }
  return Object.assign(G, { tab, lines, L, per, cardLines });
}

// ---------------------------------------------------------------- building a world
export class Builder {
  constructor() { this.thr = []; this.tag = []; this.src = []; this.dst = []; this.w = []; }
  input(tag) { this.thr.push(0); this.tag.push('in:' + tag); return this.thr.length - 1; }
  part(mark, tag) { this.thr.push(mark); this.tag.push(tag); return this.thr.length - 1; }
  link(s, d, w = 1) { this.src.push(s); this.dst.push(d); this.w.push(w); }
  done(meta = {}) {
    const P = this.thr.length, K = this.src.length;
    const thr = Int32Array.from(this.thr), isInput = new Uint8Array(P);
    for (let p = 0; p < P; p++) if (this.tag[p].startsWith('in:')) isInput[p] = 1;
    const outStart = new Uint32Array(P + 1), inStart = new Uint32Array(P + 1);
    for (let j = 0; j < K; j++) {
      if (this.src[j] >= this.dst[j]) throw new Error('links must run from an earlier part to a later one');
      outStart[this.src[j] + 1]++; inStart[this.dst[j] + 1]++;
    }
    for (let p = 0; p < P; p++) { outStart[p + 1] += outStart[p]; inStart[p + 1] += inStart[p]; }
    const outDst = new Uint32Array(K), outW = new Int8Array(K), inSrc = new Uint32Array(K), inW = new Int8Array(K);
    const of = outStart.slice(0, P), nf = inStart.slice(0, P);
    for (let j = 0; j < K; j++) {
      const s = this.src[j], d = this.dst[j], w = this.w[j];
      outDst[of[s]] = d; outW[of[s]++] = w; inSrc[nf[d]] = s; inW[nf[d]++] = w;
    }
    const level = new Uint16Array(P); let maxLevel = 0;
    for (let p = 0; p < P; p++) for (let j = outStart[p]; j < outStart[p + 1]; j++) {
      const d = outDst[j]; if (level[d] < level[p] + 1) { level[d] = level[p] + 1; if (level[d] > maxLevel) maxLevel = level[d]; }
    }
    const levelCount = new Uint32Array(maxLevel + 1); for (let p = 0; p < P; p++) levelCount[level[p]]++;
    const live = []; for (let p = 0; p < P; p++) if (!isInput[p]) live.push(p);
    const bytes = thr.byteLength + isInput.byteLength + outStart.byteLength + inStart.byteLength + outDst.byteLength +
      outW.byteLength + inSrc.byteLength + inW.byteLength + level.byteLength;
    return { P, K, thr, isInput, outStart, outDst, outW, inStart, inSrc, inW, level, maxLevel, levelCount,
      live: Uint32Array.from(live), tag: this.tag, bytes, ...meta };
  }
}

// the Minecraft way: nothing but 2-input AND and OR gates
export function buildGateCheck(G) {
  const B = new Builder(), { N, L, lines } = G;
  for (let c = 0; c < N; c++) B.input('card');
  let layer = [];
  for (let l = 0; l < L; l++) {
    const a = lines[l * 3], b = lines[l * 3 + 1], c = lines[l * 3 + 2];
    const ab = B.part(2, 'and'); B.link(a, ab); B.link(b, ab);
    const abc = B.part(2, 'and'); B.link(ab, abc); B.link(c, abc);
    layer.push(abc);
  }
  while (layer.length > 1) {
    const next = [];
    for (let i = 0; i + 1 < layer.length; i += 2) { const o = B.part(1, 'or'); B.link(layer[i], o); B.link(layer[i + 1], o); next.push(o); }
    if (layer.length % 2) next.push(layer[layer.length - 1]);
    layer = next;
  }
  return B.done({ kind: 'gates', cards: N, alarm: layer[0] });
}

// the world's own parts: one counter per set, one tally that hears every counter
export function buildNativeCheck(G) {
  const B = new Builder(), { N, L, lines } = G, hit = [];
  for (let c = 0; c < N; c++) B.input('card');
  for (let l = 0; l < L; l++) { const t = B.part(3, 'line'); for (let m = 0; m < 3; m++) B.link(lines[l * 3 + m], t); hit.push(t); }
  const alarm = B.part(1, 'alarm'); for (const t of hit) B.link(t, alarm);
  return B.done({ kind: 'native', cards: N, alarm });
}

// the same, plus state that is kept for the search: which cards are still free to take, and how many
export function buildNativeSearch(G) {
  const B = new Builder(), { N, L, lines } = G, hit = [], blocks = [];
  for (let c = 0; c < N; c++) B.input('card');
  for (let l = 0; l < L; l++) {
    const m = [lines[l * 3], lines[l * 3 + 1], lines[l * 3 + 2]];
    for (let k = 0; k < 3; k++) {                      // a pair of cards in the pile blocks the third
      const p = B.part(2, 'pair'); B.link(m[(k + 1) % 3], p); B.link(m[(k + 2) % 3], p); blocks.push([p, m[k]]);
    }
    const t = B.part(3, 'line'); for (let k = 0; k < 3; k++) B.link(m[k], t); hit.push(t);
  }
  const free0 = B.thr.length;
  for (let c = 0; c < N; c++) { const f = B.part(0, 'free'); B.link(c, f, -1); }   // rests at 1: free until told otherwise
  for (const [p, c] of blocks) B.link(p, free0 + c, -1);
  const alarm = B.part(1, 'alarm'); for (const t of hit) B.link(t, alarm);
  const tally = B.part(1, 'tally'); for (let c = 0; c < N; c++) B.link(free0 + c, tally);
  return B.done({ kind: 'native-search', cards: N, alarm, free0, tally });
}

// ---------------------------------------------------------------- engine 1: only what a change touches
export class EventEngine {
  constructor(W) {
    this.W = W; this.acc = new Int32Array(W.P); this.out = new Uint8Array(W.P); this.queued = new Uint8Array(W.P);
    this.bk = []; for (let lv = 0; lv <= W.maxLevel; lv++) this.bk.push(new Uint32Array(W.levelCount[lv]));
    this.bn = new Uint32Array(W.maxLevel + 1);
    this.bytes = this.acc.byteLength + this.out.byteLength + this.queued.byteLength + W.P * 4 + this.bn.byteLength;
    this.reset();
  }
  reset() {                                             // the resting state with every input at 0
    const { P, isInput, inStart, inSrc, inW, thr } = this.W, { acc, out } = this;
    out.fill(0); acc.fill(0); this.queued.fill(0); this.bn.fill(0);
    for (let p = 0; p < P; p++) {
      if (isInput[p]) continue;
      let s = 0; for (let j = inStart[p], e = inStart[p + 1]; j < e; j++) s += inW[j] * out[inSrc[j]];
      acc[p] = s; out[p] = s >= thr[p] ? 1 : 0;
    }
    this.msgs = 0; this.flips = 0;
  }
  set(p, v) { if (this.out[p] === v) return; this.out[p] = v; this.flips++; this._emit(p, v ? 1 : -1); this._run(); }
  setMany(parts, off, count) {                          // several inputs flip at once, then one wave
    const out = this.out;
    for (let i = 0; i < count; i++) { const p = parts[off + i], v = out[p] ^ 1; out[p] = v; this.flips++; this._emit(p, v ? 1 : -1); }
    this._run();
  }
  _emit(p, d) {
    const W = this.W, outDst = W.outDst, outW = W.outW, thr = W.thr, level = W.level;
    const acc = this.acc, out = this.out, queued = this.queued, bk = this.bk, bn = this.bn;
    const e = W.outStart[p + 1];
    for (let j = W.outStart[p]; j < e; j++) {
      const t = outDst[j], a = (acc[t] += outW[j] * d);
      if (queued[t] === 0 && (a >= thr[t] ? 1 : 0) !== out[t]) { queued[t] = 1; const lv = level[t]; bk[lv][bn[lv]++] = t; }
    }
    this.msgs += e - W.outStart[p];
  }
  _run() {
    const W = this.W, thr = W.thr, acc = this.acc, out = this.out, queued = this.queued, bn = this.bn;
    for (let lv = 1; lv <= W.maxLevel; lv++) {
      const b = this.bk[lv];
      for (let i = 0; i < bn[lv]; i++) {
        const t = b[i]; queued[t] = 0;
        const nv = acc[t] >= thr[t] ? 1 : 0;
        if (nv !== out[t]) { out[t] = nv; this.flips++; this._emit(t, nv ? 1 : -1); }
      }
      bn[lv] = 0;
    }
  }
  work() { return this.msgs; }
}

// ---------------------------------------------------------------- engine 2: every part, every tick
export class DenseEngine {
  constructor(W) { this.W = W; this.out = new Uint8Array(W.P); this.nxt = new Uint8Array(W.P); this.bytes = W.P * 2; this.reset(); }
  reset() { this.out.fill(0); this.sweep(); this.evals = 0; this.ticks = 0; }
  set(p, v) { this.out[p] = v; }
  tick() {            // clocked, like redstone: each part sees its inputs as they stood when the tick began
    const W = this.W, live = W.live, inStart = W.inStart, inSrc = W.inSrc, inW = W.inW, thr = W.thr, out = this.out, nxt = this.nxt;
    let changed = 0;
    for (let i = 0; i < live.length; i++) {
      const p = live[i]; let s = 0;
      for (let j = inStart[p], e = inStart[p + 1]; j < e; j++) s += inW[j] * out[inSrc[j]];
      const nv = s >= thr[p] ? 1 : 0; nxt[p] = nv; if (nv !== out[p]) changed++;
    }
    for (let i = 0; i < live.length; i++) { const p = live[i]; out[p] = nxt[p]; }
    this.evals += live.length; this.ticks++;
    return changed;
  }
  settle() { let n = 1; while (this.tick()) n++; return n; }   // ticks until one whole tick changes nothing
  sweep() {           // one pass in build order: the best a dense engine can do (a compiled circuit)
    const W = this.W, live = W.live, inStart = W.inStart, inSrc = W.inSrc, inW = W.inW, thr = W.thr, out = this.out;
    for (let i = 0; i < live.length; i++) {
      const p = live[i]; let s = 0;
      for (let j = inStart[p], e = inStart[p + 1]; j < e; j++) s += inW[j] * out[inSrc[j]];
      out[p] = s >= thr[p] ? 1 : 0;
    }
    this.evals += live.length;
  }
  work() { return this.evals; }
}

// ---------------------------------------------------------------- memory: the Chronicle
export class Chronicle {            // append-only; each entry folds into a running chain value; replay must land on the same state
  constructor() { this.buf = new Int32Array(1 << 12); this.n = 0; this.chain = 0x811c9dc5 | 0; }
  add(part, value) {
    if (this.n * 2 >= this.buf.length) { const b = new Int32Array(this.buf.length * 2); b.set(this.buf); this.buf = b; }
    this.buf[this.n * 2] = part; this.buf[this.n * 2 + 1] = value; this.n++;
    let h = this.chain; h = Math.imul(h ^ part, 16777619); h = Math.imul(h ^ value, 16777619); this.chain = h | 0;
  }
  bytes() { return this.n * 8; }
  replay(apply) { for (let i = 0; i < this.n; i++) apply(this.buf[i * 2], this.buf[i * 2 + 1]); }
  static chainOf(buf, n) { let h = 0x811c9dc5 | 0; for (let i = 0; i < n; i++) { h = Math.imul(h ^ buf[i * 2], 16777619); h = Math.imul(h ^ buf[i * 2 + 1], 16777619); } return h | 0; }
}
export function stateMark(out) { let h = 0x811c9dc5 | 0; for (let i = 0; i < out.length; i++) h = Math.imul(h ^ out[i], 16777619); return h >>> 0; }

// ---------------------------------------------------------------- the Verifier (digit arithmetic only; shares no table or engine)
export function findSet(G, pile) {   // pile: array of card numbers. Returns null when clean, else the three cards of a set.
  const { n, dig, pow } = G, has = new Set(pile);
  for (let i = 0; i < pile.length; i++) for (let j = i + 1; j < pile.length; j++) {
    const a = pile[i], b = pile[j]; let c = 0;
    for (let k = 0; k < n; k++) { const s = dig[a * n + k] + dig[b * n + k]; c += ((6 - s) % 3) * pow[k]; }
    if (c !== a && c !== b && has.has(c)) return [a, b, c];
  }
  return null;
}
export function findSetSlow(G, pile) {   // the definition itself, three cards at a time (checks the Verifier on small piles)
  const { n, dig } = G;
  for (let i = 0; i < pile.length; i++) for (let j = i + 1; j < pile.length; j++) for (let k = j + 1; k < pile.length; k++) {
    let ok = true;
    for (let d = 0; d < n && ok; d++) if ((dig[pile[i] * n + d] + dig[pile[j] * n + d] + dig[pile[k] * n + d]) % 3) ok = false;
    if (ok) return [pile[i], pile[j], pile[k]];
  }
  return null;
}

// ---------------------------------------------------------------- small helpers
export function rng(seed) {          // mulberry32: the same stream on every machine
  let a = seed >>> 0;
  return () => { a = (a + 0x6d2b79f5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
}
