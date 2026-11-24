// The Reading Room: its rooms, and everything that is worked out from a room's own list.
// A room is a list of things in the order they stand along the wall. That list IS the room: the machine, the marks on
// every face, the wires on the floor, the words and the books are all made from it.
// Runs the same in a phone browser and in Node. No dependencies beyond world.js.
import { Builder, EventEngine } from './world.js';

const switches = (n) => Array.from({ length: n }, (_, i) => ({ id: String(i + 1), kind: 'switch' }));

// words: true = each thing also says its rule in plain words. false = marks only, with "Read it to me" if you want it.
export const ROOMS = [
  { words: true, things: [...switches(2),
    { id: 'A', kind: 'lamp', mark: 2, wires: [['1', 1], ['2', 1]] },
    { id: 'D', kind: 'door', mark: 1, wires: [['A', 1]] }] },
  { words: true, things: [...switches(3),
    { id: 'A', kind: 'lamp', mark: 1, wires: [['1', 1], ['2', 1]] },
    { id: 'B', kind: 'lamp', mark: 2, wires: [['2', 1], ['3', 1]] },
    { id: 'D', kind: 'door', mark: 2, wires: [['A', 1], ['B', 1], ['1', -1]] }] },
  { words: false, things: [...switches(4),
    { id: 'A', kind: 'lamp', mark: 2, wires: [['1', 1], ['2', 1], ['3', 1]] },
    { id: 'B', kind: 'lamp', mark: 1, wires: [['4', 1], ['3', -1]] },
    { id: 'D', kind: 'door', mark: 2, wires: [['A', 1], ['B', 1]] }] },
  { words: false, things: [...switches(5),
    { id: 'A', kind: 'lamp', mark: 3, wires: [['1', 1], ['2', 1], ['3', 1], ['4', 1]] },
    { id: 'B', kind: 'lamp', mark: 1, wires: [['5', 1], ['2', -1]] },
    { id: 'C', kind: 'lamp', mark: 2, wires: [['A', 1], ['B', 1]] },
    { id: 'D', kind: 'door', mark: 2, wires: [['C', 1], ['1', 1]] }] },
];

export const nameOf = (t) => (t.kind === 'switch' ? `Switch ${t.id}` : t.kind === 'lamp' ? `Lamp ${t.id}` : t.kind === 'door' ? 'The door' : 'The bookshelf');

// ---------------------------------------------------------------- a list becomes a running machine (Prototype 0's parts and engine)
export function buildRoom(things) {
  const B = new Builder(), at = {};
  things.forEach((t, i) => {
    if (t.id in at) throw new Error(`two things are called "${t.id}"`);
    if (t.kind === 'switch') { at[t.id] = B.input(t.id); return; }
    if (t.kind !== 'lamp' && t.kind !== 'door') throw new Error(`"${t.id}" is a ${t.kind}, which this room cannot build`);
    if (!Number.isInteger(t.mark) || t.mark < 1) throw new Error(`"${t.id}" needs a mark of 1 or more`);
    if (!t.wires || !t.wires.length) throw new Error(`"${t.id}" has no wires`);
    if (t.kind === 'door' && i !== things.length - 1) throw new Error('the door stands last');
    at[t.id] = B.part(t.mark, t.kind);
    for (const [src, w] of t.wires) {
      if (!(src in at) || src === t.id) throw new Error(`"${t.id}" has a wire from "${src}", which does not stand before it`);
      if (w !== 1 && w !== -1) throw new Error(`a wire is bright (+) or dark (-); "${t.id}" has one that is neither`);
      B.link(at[src], at[t.id], w);
    }
  });
  const door = things[things.length - 1];
  if (!door || door.kind !== 'door') throw new Error('a room ends with a door');
  const W = B.done(), ids = []; for (const t of things) ids[at[t.id]] = t.id;
  return { things, at, ids, W, E: new EventEngine(W), switches: things.filter((t) => t.kind === 'switch'), door };
}

// ---------------------------------------------------------------- what a thing shows on its face, and the rule read back off a face
// Made from the rule and nothing else. carries(k) says whether wire k has light at this thing's end right now.
export function marksOf(t, lit, carries = () => 0) {
  if (t.kind === 'switch') return { sign: t.id, kind: 'switch', lit: !!lit };
  return { sign: t.id, kind: t.kind, lit: !!lit, squares: Array.from({ length: t.mark }, () => true),      // one square for each one it needs
    wires: t.wires.map(([src, w], k) => ({ from: src, dark: w < 0, live: !!carries(k) })) };
}
export function thingFromMarks(m) {
  if (m.kind === 'switch') return { id: m.sign, kind: 'switch' };
  return { id: m.sign, kind: m.kind, mark: m.squares.filter(Boolean).length, wires: m.wires.map((w) => [w.from, w.dark ? -1 : 1]) };
}

// ---------------------------------------------------------------- the same rule in plain words (templates; the numbers and names come from the rule)
const inSentence = (t) => (t.kind === 'door' ? 'the door' : nameOf(t));
const andList = (a) => (a.length < 2 ? a.join('') : a.slice(0, -1).join(', ') + ' and ' + a[a.length - 1]);
export const count = (n, word) => `${n} ${word}${n === 1 ? '' : 's'}`;
export function wordsOf(t, things, lit, sum) {
  if (t.kind === 'switch') {
    const to = (sign) => things.filter((o) => o.wires && o.wires.some(([s, w]) => s === t.id && Math.sign(w) === sign)).map(inSentence), bright = to(1), dark = to(-1);
    return `A switch. It is ${lit ? 'ON' : 'OFF'}.` + (bright.length ? ` While it is on, it sends light to ${andList(bright)}.` : '') +
      (dark.length ? ` ${bright.length ? 'It also runs' : 'While it is on, it runs'} a dark wire to ${andList(dark)}.` : '');
  }
  const from = (sign) => t.wires.filter(([, w]) => Math.sign(w) === sign).map(([s]) => nameOf(things.find((o) => o.id === s))), bright = from(1), dark = from(-1), door = t.kind === 'door';
  return `I ${door ? 'open' : 'light'} when my wires add up to ${t.mark} or more.` +
    (bright.length ? ` I have ${count(bright.length, 'bright wire')}, from ${andList(bright)}.` : '') +
    (dark.length ? ` I have ${count(dark.length, 'dark wire')}, from ${andList(dark)}. A dark wire takes one away while it carries light.` : '') +
    ` Right now they add up to ${sum}, so I am ${lit ? (door ? 'OPEN' : 'LIT') : (door ? 'shut' : 'dark')}.`;
}

// ---------------------------------------------------------------- the room's code as a page of text, and back (read by this parser; nothing is ever run)
export function codeText(things) {
  return things.map((t) => (t.kind === 'switch' ? `${t.id} switch` : `${t.id} ${t.kind} needs ${t.mark} wires ${t.wires.map(([s, w]) => (w < 0 ? '-' : '+') + s).join(' ')}`)).join('\n');
}
export function parseCode(text) {
  const things = [];
  for (const raw of String(text).split('\n')) {
    const line = raw.trim(); if (!line) continue;
    let m = /^(\w+) switch$/.exec(line); if (m) { things.push({ id: m[1], kind: 'switch' }); continue; }
    m = /^(\w+) (lamp|door) needs (\d+) wires((?: [+-]\w+)+)$/.exec(line); if (!m) throw new Error(`cannot read the line "${line}"`);
    things.push({ id: m[1], kind: m[2], mark: Number(m[3]), wires: m[4].trim().split(' ').map((s) => [s.slice(1), s[0] === '-' ? -1 : 1]) });
  }
  return things;
}

// ---------------------------------------------------------------- the Verifier's side: what opens the door, and what it costs to find out without reading
// Every way the switches can stand, tried on a fresh machine one flip at a time. Returns the settings that open the door,
// each as a number whose bit b says whether switch b (in list order) is on.
export function openSettings(things) {
  const r = buildRoom(things), n = r.switches.length, door = r.at[r.door.id], open = []; let mask = 0;
  if (r.E.out[door]) open.push(0);
  for (let i = 1; i < (1 << n); i++) {
    const b = 31 - Math.clz32(i & -i); mask ^= 1 << b; r.E.set(r.at[r.switches[b].id], (mask >> b) & 1);
    if (r.E.out[door]) open.push(mask);
  }
  return open.sort((a, b) => a - b);
}
const ones = (m) => { let c = 0; while (m) { m &= m - 1; c++; } return c; };
export const fewestFlips = (open) => (open.length ? Math.min(...open.map(ones)) : Infinity);   // starting with every switch off
export const settingText = (mask, n) => { const on = []; for (let b = 0; b < n; b++) if ((mask >> b) & 1) on.push(b + 1); return on.length ? `${on.join(', ')} on` : 'all off'; };

// Someone who cannot read the things and flips one switch at random each time: the average number of flips until the door
// first opens, starting with every switch off. Worked out exactly (one unknown per setting, solved as a set of equations).
export function blindAverage(open, n) {
  const S = 1 << n, isOpen = new Uint8Array(S); for (const m of open) isOpen[m] = 1;
  if (!open.length) return Infinity;
  const A = Array.from({ length: S }, () => new Float64Array(S + 1));
  for (let s = 0; s < S; s++) { A[s][s] = 1; if (isOpen[s]) continue; A[s][S] = 1; for (let b = 0; b < n; b++) A[s][s ^ (1 << b)] -= 1 / n; }
  for (let c = 0; c < S; c++) {
    let best = c; for (let i = c + 1; i < S; i++) if (Math.abs(A[i][c]) > Math.abs(A[best][c])) best = i; [A[c], A[best]] = [A[best], A[c]];
    const d = A[c][c]; for (let j = c; j <= S; j++) A[c][j] /= d;
    for (let i = 0; i < S; i++) if (i !== c && A[i][c] !== 0) { const m = A[i][c]; for (let j = c; j <= S; j++) A[i][j] -= m * A[c][j]; }
  }
  return A[0][S];
}
