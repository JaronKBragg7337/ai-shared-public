// The hidden-law world. A second small world on the same primitives: State (five numbers), Rule (a law nobody was told),
// Event (an experiment), Memory (the notebook), Verifier (the world itself, on experiments nobody saw).
// Every world's law is drawn from a seed, so no model can have read it anywhere.
import { rng } from '../world.js';

export const VARS = ['m1', 'm2', 'q1', 'q2', 'r'];
const FUNCS = { pow: [2, Math.pow], sqrt: [1, Math.sqrt], abs: [1, Math.abs], min: [2, Math.min], max: [2, Math.max] };

// ---------------------------------------------------------------- the law language (parsed here; nothing a model writes is run as code)
export function compileLaw(source, extra = []) {      // extra: letters that stand for unknown numbers in a shape
  const src = String(source).toLowerCase().replace(/\^/g, ' ^ ').trim();
  if (!src) throw new Error('empty'); if (src.length > 600) throw new Error('too long');
  const tk = src.match(/\d+\.?\d*(?:e-?\d+)?|[a-z_][a-z0-9_]*|[-+*/^(),]/g) || [];
  if (tk.join('').length !== src.replace(/\s+/g, '').length) throw new Error('cannot read part of it');
  let p = 0; const peek = () => tk[p], next = () => tk[p++];
  function add() { let a = mul(); for (;;) { const op = peek(); if (op !== '+' && op !== '-') return a; next(); const l = a, r = mul(); a = op === '+' ? (e) => l(e) + r(e) : (e) => l(e) - r(e); } }
  function mul() { let a = unary(); for (;;) { const op = peek(); if (op !== '*' && op !== '/') return a; next(); const l = a, r = unary(); a = op === '*' ? (e) => l(e) * r(e) : (e) => l(e) / r(e); } }
  function unary() { if (peek() === '-') { next(); const a = unary(); return (e) => -a(e); } if (peek() === '+') { next(); return unary(); } return power(); }
  function power() { const b = primary(); if (peek() === '^') { next(); const x = unary(); return (e) => Math.pow(b(e), x(e)); } return b; }
  function primary() {
    const t = next(); if (t === undefined) throw new Error('ends too soon');
    if (t === '(') { const a = add(); if (next() !== ')') throw new Error('expected ")"'); return a; }
    if (/^\d/.test(t)) { const v = parseFloat(t); return () => v; }
    if (peek() === '(') {
      const f = FUNCS[t]; if (!f) throw new Error(`no function "${t}"`); next(); const args = [add()]; while (peek() === ',') { next(); args.push(add()); }
      if (next() !== ')') throw new Error('expected ")"'); if (args.length !== f[0]) throw new Error(`wrong number of values for ${t}`);
      return f[0] === 1 ? (e) => f[1](args[0](e)) : (e) => f[1](args[0](e), args[1](e));
    }
    if (!VARS.includes(t) && !extra.includes(t)) throw new Error(`no name "${t}"`); return (e) => e[t];
  }
  const f = add(); if (p < tk.length) throw new Error(`unexpected "${tk[p]}"`); return f;
}

// ---------------------------------------------------------------- a made-up law of nature from a seed
const pick = (r, list) => list[(r() * list.length) | 0];
const term = (v, e) => (e === 0 ? '' : e === 1 ? v : `pow(${v}, ${e})`);
export function makeWorld(seed) {
  const r = rng(424200 + seed), kind = ['power', 'plus', 'mix'][((seed - 1) / 4) | 0 % 3] || 'power';
  const k = pick(r, [0.25, 0.5, 1.5, 2, 3, 5]), re = pick(r, [0.5, 1, 1.5, 2, 3]);
  let top = [], bottom = [`pow(r, ${re})`], text;
  if (kind === 'mix') {
    const [u, v] = pick(r, [['m1', 'm2'], ['q1', 'q2'], ['m2', 'q1']]), c = pick(r, [2, 3, 0.5]), g = pick(r, [1, 2]), other = pick(r, VARS.filter((x) => x !== u && x !== v && x !== 'r'));
    text = `${k} * ${g === 1 ? `(${u} + ${c} * ${v})` : `pow(${u} + ${c} * ${v}, ${g})`} * ${other} / pow(r, ${re})`;
  } else {
    for (const v of ['m1', 'm2', 'q1', 'q2']) { const e = pick(r, [-1, 0, 0.5, 1, 1, 2]); if (e > 0) top.push(term(v, e)); else if (e < 0) bottom.push(term(v, -e)); }
    if (top.length < 2) top = ['m2', 'pow(q1, 2)'];
    text = `${k} * ${top.join(' * ')} / (${bottom.join(' * ')})`;
    if (kind === 'plus') { const v = pick(r, VARS), h = pick(r, [0.5, 2, 4]), g = pick(r, [1, 2]); text += ` + ${h} * ${term(v, g)}`; }
  }
  return { seed, kind, text, f: compileLaw(text) };
}
const sig6 = (y) => Number(y.toPrecision(6));
export const measure = (world, x) => sig6(world.f(x));
export function randomPoint(r) { const x = {}; for (const v of VARS) x[v] = Math.round((1 + r() * 9) * 100) / 100; return x; }
export function randomRows(world, count, seed) { const r = rng(seed), rows = []; for (let i = 0; i < count; i++) { const x = randomPoint(r); rows.push({ ...x, y: measure(world, x) }); } return rows; }

// ---------------------------------------------------------------- the Verifier: 200 experiments nobody was shown
export function gradeLaw(world, source) {
  let f; try { f = compileLaw(source); } catch (e) { return { valid: false, error: String(e.message || e), grade: 0 }; }
  const r = rng(909000 + world.seed); let ok = 0;
  for (let i = 0; i < 200; i++) { const x = randomPoint(r), truth = world.f(x), got = f(x); if (Number.isFinite(got) && Math.abs(got - truth) <= 0.01 * Math.abs(truth)) ok++; }
  return { valid: true, grade: ok / 200 };
}

// ---------------------------------------------------------------- arm 0, no model: the textbook straight-line fit on logs
export function fitPowerLaw(rows) {
  const n = VARS.length + 1, A = Array.from({ length: n }, () => new Float64Array(n + 1));
  for (const row of rows) { if (!(row.y > 0)) continue; const x = [1, ...VARS.map((v) => Math.log(row[v]))], y = Math.log(row.y); for (let i = 0; i < n; i++) { for (let j = 0; j < n; j++) A[i][j] += x[i] * x[j]; A[i][n] += x[i] * y; } }
  for (let c = 0; c < n; c++) {                      // Gauss-Jordan
    let best = c; for (let i = c + 1; i < n; i++) if (Math.abs(A[i][c]) > Math.abs(A[best][c])) best = i; [A[c], A[best]] = [A[best], A[c]];
    if (Math.abs(A[c][c]) < 1e-12) continue; const d = A[c][c]; for (let j = c; j <= n; j++) A[c][j] /= d;
    for (let i = 0; i < n; i++) if (i !== c) { const m = A[i][c]; for (let j = c; j <= n; j++) A[i][j] -= m * A[c][j]; }
  }
  return `${Math.exp(A[0][n]).toPrecision(6)} * ` + VARS.map((v, i) => `pow(${v}, ${A[i + 1][n].toFixed(4)})`).join(' * ');
}

// ---------------------------------------------------------------- shape and fit: a model gives the SHAPE, the world finds the numbers
// A shape is a law with letters a..g where numbers are unknown, such as  a * pow(m1, b) / pow(r, c) + d * q2
export const LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g'];
export function fitShape(shape, rows, seed = 1) {
  const src = String(shape).toLowerCase(), names = LETTERS.filter((n) => new RegExp('(^|[^a-z0-9_])' + n + '($|[^a-z0-9_(])').test(src));
  const f = compileLaw(src, names), r = rng(77000 + seed), k = names.length, env = (th, x) => { const e = { ...x }; for (let i = 0; i < k; i++) e[names[i]] = th[i]; return e; };
  const miss = (th) => { let worst = 0, sum = 0; for (const x of rows) { const p = f(env(th, x)), d = Number.isFinite(p) ? Math.abs(p - x.y) / Math.abs(x.y) : 1e3; sum += Math.min(d, 1e3) ** 2; if (d > worst) worst = d; } return { loss: sum / rows.length, worst }; };
  const write = (th) => src.replace(/(^|[^a-z0-9_])([a-g])(?=$|[^a-z0-9_(])/g, (m, pre, n) => pre + Number(th[names.indexOf(n)].toPrecision(6)));
  if (!k) { const m = miss([]); return { law: src, worst: m.worst, names }; }
  let best = null;
  for (let start = 0; start < 40; start++) {           // Nelder-Mead from many starting points
    let S = Array.from({ length: k + 1 }, () => Array.from({ length: k }, () => -1 + r() * 4)), L = S.map((p) => miss(p).loss);
    for (let it = 0; it < 220 * k; it++) {
      const o = L.map((_, i) => i).sort((a, b) => L[a] - L[b]); S = o.map((i) => S[i]); L = o.map((i) => L[i]);
      const c = Array.from({ length: k }, (_, j) => S.slice(0, k).reduce((s, p) => s + p[j], 0) / k), at = (t) => c.map((v, j) => v + t * (S[k][j] - v));
      const xr = at(-1), lr = miss(xr).loss;
      if (lr < L[0]) { const xe = at(-2), le = miss(xe).loss; if (le < lr) { S[k] = xe; L[k] = le; } else { S[k] = xr; L[k] = lr; } }
      else if (lr < L[k - 1]) { S[k] = xr; L[k] = lr; }
      else { const xc = at(0.5), lc = miss(xc).loss; if (lc < L[k]) { S[k] = xc; L[k] = lc; } else for (let i = 1; i <= k; i++) { S[i] = S[i].map((v, j) => S[0][j] + 0.5 * (v - S[0][j])); L[i] = miss(S[i]).loss; } }
    }
    const i0 = L.indexOf(Math.min(...L)); if (!best || L[i0] < best.loss) best = { th: S[i0], loss: L[i0] }; if (best.loss < 1e-10) break;
  }
  const snapped = best.th.map((v) => (Math.abs(v - Math.round(v * 4) / 4) < 0.04 ? Math.round(v * 4) / 4 : v)), ms = miss(snapped), mb = miss(best.th);   // made-up laws use tidy numbers: try them
  const th = ms.worst <= Math.max(mb.worst, 0.002) ? snapped : best.th;
  return { law: write(th), worst: miss(th).worst, names };
}
