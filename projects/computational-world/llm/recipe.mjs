// A recipe is ONE arithmetic expression that gives every card a score. The builder then goes through the cards
// from the highest score down and keeps each card that makes no set with the cards already kept.
// The expression is parsed here (no eval, no code from a model is ever run as code).
import { geometry, findSet } from '../world.js';

export const BEST = { 3: 9, 4: 20, 5: 45, 6: 112, 7: 236, 8: 512 };   // 9 to 112 are proven; 236 and 512 are the best anyone has found
export const SIZES = [3, 4, 5, 6, 7, 8];

// ---------------------------------------------------------------- the little language
const FUNCS = { min: Math.min, max: Math.max, abs: Math.abs, floor: Math.floor, mod: (a, b) => (b === 0 ? 0 : ((a % b) + b) % b) };
const VARS = ['n', 'z', 'o', 't', 's', 'w', 'first', 'last', 'i'];

function tokenize(src) {
  const out = [], re = /\s*(\d+\.?\d*|[a-z_][a-z0-9_]*|<=|>=|==|!=|&&|\|\||[-+*/%()<>!?:,])/gy;
  let m, at = 0;
  while (at < src.length) {
    re.lastIndex = at; m = re.exec(src);
    if (!m) { if (/^\s*$/.test(src.slice(at))) break; throw new Error(`cannot read "${src.slice(at, at + 12)}"`); }
    out.push(m[1]); at = re.lastIndex;
  }
  return out;
}

export function compile(source, limits = { chars: 300, nodes: 200 }) {
  const src = String(source).toLowerCase().trim();
  if (!src) throw new Error('empty'); if (src.length > limits.chars) throw new Error('too long');
  const tk = tokenize(src); let p = 0, nodes = 0;
  const peek = () => tk[p], next = () => tk[p++], want = (x) => { if (next() !== x) throw new Error(`expected "${x}"`); };
  const node = (f) => { if (++nodes > limits.nodes) throw new Error('too big'); return f; };
  function ternary() { const c = or(); if (peek() === '?') { next(); const a = ternary(); want(':'); const b = ternary(); return node((e) => (c(e) ? a(e) : b(e))); } return c; }
  function or() { let a = and(); while (peek() === '||') { next(); const l = a, r = and(); a = node((e) => (l(e) || r(e) ? 1 : 0)); } return a; }
  function and() { let a = cmp(); while (peek() === '&&') { next(); const l = a, r = cmp(); a = node((e) => (l(e) && r(e) ? 1 : 0)); } return a; }
  function cmp() {
    let a = add();
    for (;;) { const op = peek(); if (!['<', '>', '<=', '>=', '==', '!='].includes(op)) return a; next(); const l = a, r = add();
      a = node(op === '<' ? (e) => (l(e) < r(e) ? 1 : 0) : op === '>' ? (e) => (l(e) > r(e) ? 1 : 0) : op === '<=' ? (e) => (l(e) <= r(e) ? 1 : 0) :
        op === '>=' ? (e) => (l(e) >= r(e) ? 1 : 0) : op === '==' ? (e) => (l(e) === r(e) ? 1 : 0) : (e) => (l(e) !== r(e) ? 1 : 0)); }
  }
  function add() { let a = mul(); for (;;) { const op = peek(); if (op !== '+' && op !== '-') return a; next(); const l = a, r = mul(); a = node(op === '+' ? (e) => l(e) + r(e) : (e) => l(e) - r(e)); } }
  function mul() { let a = unary(); for (;;) { const op = peek(); if (op !== '*' && op !== '/' && op !== '%') return a; next(); const l = a, r = unary();
    a = node(op === '*' ? (e) => l(e) * r(e) : op === '/' ? (e) => { const d = r(e); return d === 0 ? 0 : l(e) / d; } : (e) => FUNCS.mod(l(e), r(e))); } }
  function unary() { const op = peek(); if (op === '-') { next(); const a = unary(); return node((e) => -a(e)); } if (op === '!') { next(); const a = unary(); return node((e) => (a(e) ? 0 : 1)); } if (op === '+') { next(); return unary(); } return primary(); }
  function primary() {
    const t = next(); if (t === undefined) throw new Error('ends too soon');
    if (t === '(') { const a = ternary(); want(')'); return a; }
    if (/^\d/.test(t)) { const v = parseFloat(t); return node(() => v); }
    if (!/^[a-z_]/.test(t)) throw new Error(`unexpected "${t}"`);
    if (peek() === '(') {
      next(); const args = []; if (peek() !== ')') { args.push(ternary()); while (peek() === ',') { next(); args.push(ternary()); } } want(')');
      if (t === 'd') { if (args.length !== 1) throw new Error('d(k) takes one number'); const k = args[0]; return node((e) => { const q = Math.floor(k(e)); return q >= 0 && q < e.n ? e.dig[e.off + q] : 0; }); }
      const f = FUNCS[t]; if (!f) throw new Error(`no function "${t}"`);
      if (args.length !== (t === 'abs' || t === 'floor' ? 1 : 2)) throw new Error(`wrong number of values for ${t}`);
      return args.length === 1 ? node((e) => f(args[0](e))) : node((e) => f(args[0](e), args[1](e)));
    }
    if (!VARS.includes(t)) throw new Error(`no name "${t}"`);
    return node((e) => e[t]);
  }
  const f = ternary(); if (p < tk.length) throw new Error(`unexpected "${tk[p]}"`);
  return f;
}

// ---------------------------------------------------------------- the builder and the grade
const geo = {}; const G = (n) => geo[n] || (geo[n] = geometry(n));

export function buildPile(score, n) {           // score: a compiled recipe, or null for "take the cards in number order"
  const g = G(n), { N, dig, pow } = g, val = new Float64Array(N), env = { n, dig, off: 0, z: 0, o: 0, t: 0, s: 0, w: 0, first: 0, last: 0, i: 0 };
  for (let c = 0; c < N; c++) {
    let z = 0, o = 0, t = 0; for (let k = 0; k < n; k++) { const x = dig[c * n + k]; if (x === 0) z++; else if (x === 1) o++; else t++; }
    env.off = c * n; env.z = z; env.o = o; env.t = t; env.s = o + 2 * t; env.w = o + t; env.first = dig[c * n]; env.last = dig[c * n + n - 1]; env.i = c;
    const v = score ? score(env) : 0; val[c] = Number.isFinite(v) ? v : -Infinity;
  }
  const order = Array.from({ length: N }, (_, c) => c).sort((a, b) => val[b] - val[a] || a - b);
  return greedy(g, order);
}
export function greedy(g, order) {              // ordinary software: the cheapest way to do this particular job (measured in bench.mjs)
  const { n, N, dig, pow } = g, inp = new Uint8Array(N), pile = [];
  for (const c of order) {
    let free = true; const co = c * n;
    for (let q = 0; q < pile.length && free; q++) {
      const ao = pile[q] * n; let third = 0;
      for (let k = 0; k < n; k++) { const x = dig[ao + k], y = dig[co + k]; third += (x === y ? x : 3 - x - y) * pow[k]; }
      if (inp[third]) free = false;
    }
    if (free) { inp[c] = 1; pile.push(c); }
  }
  return pile;
}

export function grade(source, limits) {         // the Verifier's verdict on a recipe: pile sizes for 3 to 8 features, and a total out of 6
  let f; try { f = compile(source, limits); } catch (e) { return { valid: false, error: String(e.message || e), sizes: {}, total: 0 }; }
  const sizes = {}, piles = {}; let total = 0;
  for (const n of SIZES) {
    const pile = buildPile(f, n); if (findSet(G(n), pile)) throw new Error('the builder produced a pile with a set in it: a bug, not a result');
    sizes[n] = pile.length; total += pile.length / BEST[n]; if (n <= 5) piles[n] = pile;
  }
  return { valid: true, sizes, total: +total.toFixed(4), sig: signature(piles) };
}
export function sizesFor(source, ns, limits) {  // pile sizes for chosen numbers of features only (each pile still checked by the Verifier)
  const f = compile(source, limits), out = {};
  for (const n of ns) { const pile = buildPile(f, n); if (findSet(G(n), pile)) throw new Error('bug: set in pile'); out[n] = pile.length; }
  return out;
}
export function gradeOrder(orderFor) {          // the same grade for a plain card order (the no-AI control)
  const sizes = {}; let total = 0;
  for (const n of SIZES) { const pile = greedy(G(n), orderFor(n, G(n).N)); if (findSet(G(n), pile)) throw new Error('bug: set in pile'); sizes[n] = pile.length; total += pile.length / BEST[n]; }
  return { valid: true, sizes, total: +total.toFixed(4) };
}

// where a recipe "stands": which cards it keeps in the 81-card and 243-card worlds. Two recipes are near when they keep nearly the same cards.
function signature(piles) { const bits = new Uint8Array(81 + 243); for (const c of piles[4]) bits[c] = 1; for (const c of piles[5]) bits[81 + c] = 1; return Buffer.from(bits).toString('base64'); }
export function distance(sigA, sigB) { const a = Buffer.from(sigA, 'base64'), b = Buffer.from(sigB, 'base64'); let d = 0; for (let i = 0; i < a.length; i++) d += a[i] ^ b[i]; return d; }
