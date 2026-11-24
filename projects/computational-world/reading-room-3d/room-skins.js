import { codeText, parseCode } from 'rr-rooms';
import { paintSurface, readSurface } from 'rr-skin';

const KINDS = {
  switch: { size: [0.38, 0.53, 0.235], pixels: [144, 246] },
  lamp: { size: [0.34, 1.1, 0.33], pixels: [246, 520] },
  door: { size: [1.72, 2.36, 0.115], pixels: [246, 650] },
  shelf: { size: [2.15, 2.32, 0.665], pixels: [324, 430] },
  book: { size: [0.334, 0.47, 0.152], pixels: [176, 246] },
  bench: { size: [1.63, 0.45, 0.61], pixels: [432, 150] },
  stand: { size: [0.26, 1.02, 0.26], pixels: [96, 350] },
  lantern: { size: [0.18, 0.27, 0.18], pixels: [138, 212] },
};

export const WINDOW_COLOR = { rest: '#a07f47', glow: '#ffd67a' };
const LOOK = {
  wall: { cell: 13, lit: '#8f6d33', dim: '#1b2147', base: '#0e1230', stagger: 9 },
  floor: { cell: 16, lit: '#3d4573', dim: '#161a36', base: '#0b0d22' },
  ceiling: { cell: 16, lit: '#1a1d33', dim: '#101226', base: '#0a0c1c' },
  rest: { cell: 13, lit: WINDOW_COLOR.rest, dim: '#2a2f52', base: '#1c2038' },
};

const BOOKS = ['marks', 'history', 'skins'];
const encoder = new TextEncoder();
const number = (value) => String(Number(value.toFixed(3)));
const coords = (values) => values.map(number).join(' ');

// The maker gives the world canvases. The written strings are kept separately for the checks.
export function makeRoomPaint(things, lite) {
  const depth = 6 + 2 * Math.max(...['switch', 'lamp'].map((kind) => things.filter((t) => t.kind === kind).length));
  const half = depth / 2, height = 3.4, opening = KINDS.door.size[0], doorHeight = KINDS.door.size[1];
  const sideWidth = (8 - opening) / 2;
  const positions = { switch: 0, lamp: 0 };
  const surfaces = [], written = [];
  function make(head, kind, at, size = KINDS[kind]?.size, sized = false) {
    const text = `${head} at ${coords(at)}${sized ? ` size ${coords(size)}` : ''}`;
    const look = LOOK[kind] ?? LOOK.rest;
    const [w, h, d] = size;
    const density = kind === 'wall' ? 186 : 116;
    const pixels = kind === 'wall' ? [Math.max(w, d) * density, h * density] : [w * density, d * density];
    const cap = lite ? 1024 : 2048;
    const [width, height] = (KINDS[kind]?.pixels ?? pixels).map((n) => Math.min(cap, Math.round(n * (lite ? 0.58 : 1))));
    const canvas = document.createElement('canvas');
    canvas.width = Math.max(32, width);
    // At three pixels the reader's rounded centre can land outside the one-pixel window.
    // Leave enough height for the ruler and the full tower at four pixels or larger.
    canvas.height = Math.max(height, (encoder.encode(text).length + 6) * 4);
    const ink = canvas.getContext('2d', { willReadFrequently: true });
    const cell = lite ? Math.round(look.cell * 0.58) : look.cell;
    // On small faces, a whole tower also has to fit across the canvas.
    paintSurface(ink, canvas.width, canvas.height, text, { ...look, cell: Math.min(cell, Math.floor(canvas.width / 8)) });
    surfaces.push(canvas);
    written.push(text);
  }

  for (const thing of things) {
    const { kind } = thing;
    const at = kind === 'door' ? [0, doorHeight / 2, -depth + 0.018] :
      [kind === 'switch' ? -3.78 : 3.78, 1.48, -2.7 - 2 * positions[kind]++];
    make(codeText([thing]), kind, at);
  }
  const panel = (kind, at, size) => make(kind, kind, at, size, true);
  panel('floor', [0, -0.01, -half], [8, 0.02, depth]);
  panel('ceiling', [0, height + 0.01, -half], [8, 0.02, depth]);
  panel('wall', [0, height / 2, 0.11], [8.35, height, 0.22]);
  for (const side of [-1, 1]) {
    panel('wall', [side * 4.11, height / 2, -half], [0.22, height, depth]);
    panel('wall', [side * (opening + sideWidth) / 2, height / 2, -depth - 0.105], [sideWidth, height, 0.21]);
    panel('wall', [side * 1.02, 1.3, -depth - 1.56], [0.14, 2.6, 3.12]);
  }
  panel('wall', [0, (height + doorHeight) / 2, -depth - 0.105], [opening, height - doorHeight, 0.21]);
  panel('floor', [0, -0.01, -depth - 1.56], [2.18, 0.02, 3.12]);
  panel('ceiling', [0, 2.61, -depth - 1.56], [2.18, 0.02, 3.12]);

  const shelf = [-2.48, 0, -depth + 0.365];
  make('shelf', 'shelf', shelf);
  BOOKS.forEach((title, i) => make(`book ${i + 1} ${title}`, 'book',
    [shelf[0] + (i - 1) * 0.51, 1.408, shelf[2] + 0.122]));
  make('bench', 'bench', [2.96, 0, -depth + 0.55]);
  make('lantern stand', 'stand', [1.15, 0, -1.75]);
  make('lantern learner', 'lantern', [1.15, KINDS.stand.size[1], -1.75]);
  return { surfaces, written };
}

const coordinate = '(-?\\d+(?:\\.\\d+)?)';
const xyz = [coordinate, coordinate, coordinate].join(' ');
const linePattern = new RegExp(`^(.+) at ${xyz}(?: size ${xyz})?$`);
const structures = new Set(['wall', 'floor', 'ceiling']);
const furniture = new Map([
  ['shelf', 'shelf'], ['bench', 'bench'], ['lantern stand', 'stand'], ['lantern learner', 'lantern'],
]);

export function parseSkin(text) {
  const match = linePattern.exec(text);
  if (!match) return null;
  const [, head, x, y, z, w, h, d] = match;
  const at = [x, y, z].map(Number);
  if (!at.every(Number.isFinite)) return null;
  if (structures.has(head)) {
    const size = [w, h, d].map(Number);
    return size.every((n) => Number.isFinite(n) && n > 0) ? { kind: head, at, size, text } : null;
  }
  if (w !== undefined) return null;
  const book = /^book ([1-3]) (\w+)$/.exec(head);
  if (book && BOOKS[Number(book[1]) - 1] === book[2]) {
    return { id: `book-${book[1]}`, kind: 'book', index: Number(book[1]) - 1, at, size: KINDS.book.size, text };
  }
  const kind = furniture.get(head);
  if (kind) return { id: kind, kind, at, size: KINDS[kind].size, text };
  try {
    const [rule] = parseCode(head);
    return { id: rule.id, kind: rule.kind, rule, at, size: KINDS[rule.kind].size, text };
  } catch {
    return null;
  }
}

export function readRoomPaint(surfaces) {
  const things = [];
  let conflicts = 0;
  for (const canvas of surfaces) {
    const got = readSurface(canvas.getContext('2d'), canvas.width, canvas.height);
    if (got?.conflict) conflicts++;
    const thing = got?.text && parseSkin(got.text);
    // cell and span are what the reader measured off the ruler: the size of a window and where the towers stand.
    if (thing) things.push({ ...thing, canvas, cell: got.cell, span: got.span });
  }
  return { things, skins: { read: things.length, of: surfaces.length, conflicts } };
}
