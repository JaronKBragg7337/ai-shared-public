// A thing's own code, worn on its outside as lit windows: one letter per floor, eight windows per floor.
// Jaron, 11/23/2026, pointing at the night-city picture: "picture a wall with the code as a design... only each object's
// design on the outside, it's its code for its object."
//
// THE WHOLE CONVENTION (this is all a reader has to know; it is told nothing else about a surface):
//   1. Along the top edge runs a ruler: one short lit dash above each column of windows. The gap from one dash to the
//      next is the size of a window cell. Towers are 8 windows wide with one dark column between them.
//   2. The floors start one cell down from the top edge. Each floor is one letter: 8 windows, lit = 1, first window = 128.
//   3. A tower is: a roofline (all 8 lit), a floor that says how many letters follow, the letters, two check floors
//      (a 16-bit check over the count and the letters: CRC-16/CCITT), one dark floor. Then it may repeat.
//      Towers side by side must say the same. If two readable towers disagree, the surface is refused, never guessed.
//   4. Bright or dim paint changes nothing about what a surface says. Only which windows are lit, relative to the rest.
// WHAT THE CHECK DOES AND DOES NOT DO. A spoiled window, a swapped pair of letters, or any change that is not a careful
// repaint fails the check, and that tower is passed over. A careful painter can always paint a different valid code:
// that is a repaint, not damage, and it only counts when EVERY readable tower on the surface says the same thing.
// (The first version used a plain sum for the check and took the first tower that read. ChatGPT read the code on
// 11/23/2026 and pointed out both holes: a swap passed the sum, and a disagreement was settled silently.)
// Runs in a browser and in Node. No dependencies.
const enc = new TextEncoder(), dec = new TextDecoder();
export const WIDE = 9;

export function toFloors(text) {
  const bytes = [...enc.encode(text)];
  if (bytes.length < 1 || bytes.length > 250) throw new Error('a tower holds 1 to 250 letters');
  const check = crc16([bytes.length, ...bytes]);
  return [255, bytes.length, ...bytes, check >> 8, check & 255, 0];
}
function crc16(bytes) {                    // CRC-16/CCITT: it depends on where each letter stands, so a swap changes it
  let c = 0xffff;
  for (const b of bytes) { c ^= b << 8; for (let i = 0; i < 8; i++) c = c & 0x8000 ? ((c << 1) ^ 0x1021) & 0xffff : (c << 1) & 0xffff; }
  return c;
}
export function fromFloors(floors) {       // starting anywhere; null if no whole tower with right check floors is there
  for (let i = 0; i + 4 < floors.length; i++) {
    if (floors[i] !== 255) continue;
    const n = floors[i + 1]; if (n < 1 || n > 250 || i + 3 + n >= floors.length) continue;
    const bytes = floors.slice(i + 2, i + 2 + n), check = crc16([n, ...bytes]);
    if ((check >> 8) === floors[i + 2 + n] && (check & 255) === floors[i + 3 + n]) return dec.decode(new Uint8Array(bytes));
  }
  return null;
}

// Paint one surface with its code. look: { cell (largest window cell), lit, dim, base, stagger }.
// The windows shrink until one whole tower fits. Returns where things ended up, for the painter's own use only.
export function paintSurface(ink, W, H, text, look) {
  const floors = toFloors(text), need = floors.length;
  let c = look.cell; while (c > 3 && Math.floor((H - c) / c) < need) c--;
  const rows = Math.floor((H - c) / c), towers = Math.max(1, Math.floor((W + c) / (WIDE * c))), pad = Math.max(1, Math.round(c * 0.19));
  const x0 = Math.round((W - (towers * WIDE - 1) * c) / 2), spare = rows - need, shifts = [];
  ink.fillStyle = look.base; ink.fillRect(0, 0, W, H);
  for (let t = 0; t < towers; t++) {
    const shift = look.stagger && spare > 0 ? (t * 5 + 2) % Math.min(look.stagger, spare + 1) : 0; shifts.push(shift);
    ink.fillStyle = look.lit;
    for (let b = 0; b < 8; b++) ink.fillRect(x0 + (t * WIDE + b) * c + pad, 0, c - 2 * pad, Math.max(2, Math.round(c / 3)));     // the ruler
    for (let r = shift; r < rows; r++) {
      const floor = floors[(r - shift) % need];
      for (let b = 0; b < 8; b++) { ink.fillStyle = (floor >> (7 - b)) & 1 ? look.lit : look.dim; ink.fillRect(x0 + (t * WIDE + b) * c + pad, c + r * c + pad, c - 2 * pad, c - 2 * pad); }
    }
  }
  return { c, pad, x0, rows, towers, shifts, fits: rows >= need };
}
export const windowRect = (info, tower, row, bit) => [info.x0 + (tower * WIDE + bit) * info.c + info.pad, info.c + row * info.c + info.pad, info.c - 2 * info.pad, info.c - 2 * info.pad];

// Read a surface knowing only the convention above: find the ruler, measure the cell, look at the middle of every window.
// Reads EVERY tower. A spoiled tower is passed over. If the readable towers all agree, that is what the surface says.
// If they disagree, it says nothing and reports the disagreement: { text: null, conflict: [the different texts] }.
// Returns { text, tower (the first that read), towers, cell, span (where the windows stand, left to right, in pixels),
// said (each tower's text or null), conflict? }.
const lum = (d, p) => 0.299 * d[p] + 0.587 * d[p + 1] + 0.114 * d[p + 2];
export function readSurface(ink, W, H) {
  const all = ink.getImageData(0, 0, W, H).data, L = new Float32Array(W); let lo = 255, hi = 0;
  for (let x = 0; x < W; x++) { L[x] = lum(all, 4 * (W + x)); lo = Math.min(lo, L[x]); hi = Math.max(hi, L[x]); }      // the second line of pixels: the ruler
  if (hi - lo < 10) return null;                                                                                         // no ruler: this surface says nothing
  const cut = (lo + hi) / 2, runs = [];
  for (let x = 0; x < W; x++) if (L[x] > cut) { const start = x; while (x < W && L[x] > cut) x++; runs.push([start, x]); }
  if (runs.length < 8) return null;
  const c = runs[1][0] - runs[0][0], x0 = runs[0][0] - (c - (runs[0][1] - runs[0][0])) / 2, towers = Math.floor(runs.length / 8), rows = Math.floor((H - c) / c);
  if (c < 3 || rows < 4) return null;
  const said = [];
  for (let t = 0; t < towers; t++) {
    const seen = []; let dark = 255, bright = 0;
    for (let r = 0; r < rows; r++) for (let b = 0; b < 8; b++) {
      const v = lum(all, 4 * (Math.round(c + (r + 0.5) * c) * W + Math.round(x0 + (t * WIDE + b + 0.5) * c))); seen.push(v); dark = Math.min(dark, v); bright = Math.max(bright, v);
    }
    const mid = (dark + bright) / 2, floors = [];
    for (let r = 0; r < rows; r++) { let floor = 0; for (let b = 0; b < 8; b++) floor = (floor << 1) | (seen[r * 8 + b] > mid ? 1 : 0); floors.push(floor); }
    said.push(fromFloors(floors));
  }
  const texts = [...new Set(said.filter((text) => text !== null))], span = [x0, x0 + (towers * WIDE - 1) * c];
  if (texts.length !== 1) return { text: null, tower: -1, towers, cell: c, span, said, conflict: texts.length > 1 ? texts : undefined };
  return { text: texts[0], tower: said.indexOf(texts[0]), towers, cell: c, span, said };
}
