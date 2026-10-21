// nav.mjs - walking like a person: face where you are going, hold the stick, notice when you are not getting anywhere.
import { sleep, rnd, pick } from './core.mjs';

// ---- port map for route planning (port-local metres; x east, z south) -------------------------------------------------
const BUILD = [ // [x, z, w, d, doorSide]  door is on the +z face at the building's x, width doorW
  { n: 'depot', x: -62, z: 18, w: 24, d: 18, door: 3.2 }, { n: 'market', x: -58, z: 53, w: 32, d: 8, door: 0 },
  { n: 'tower', x: -60, z: -39, w: 12, d: 12, door: 2.4 }, { n: 'fuel', x: 57, z: -70, w: 24, d: 12, door: 0 },
  { n: 'containers', x: 51, z: 65, w: 26, d: 6, door: 0 }, { n: 'sign', x: -28, z: 65, w: 16, d: 1, door: 0 },
];
const CELL = 2, X0 = -140, X1 = 360, Z0 = -130, Z1 = 130;
let CAB = false, EXTRA = [];
function blocked(x, z) {
  for (const e of EXTRA) if (Math.hypot(x - e.x, z - e.z) < e.r) return true;
  if (CAB) return x > -61.8 && x < -58.2 && z > -44.6 && z < -38.2;
  for (const b of BUILD) {
    const hx = b.w / 2, hz = b.d / 2; const dx = Math.abs(x - b.x), dz = Math.abs(z - b.z);
    if (dx > hx + 1.2 || dz > hz + 1.2) continue;
    if (!b.door) return true;                       // solid block, no way in
    // a walled building: the wall ring is blocked except the door gap on the +z (south) face; the inside is free
    const inside = dx < hx - 0.9 && dz < hz - 0.9; if (inside) continue;
    const doorGap = Math.abs(x - b.x) < b.door / 2 - 0.2 && z > b.z + hz - 1.6 && z < b.z + hz + 1.8;
    if (doorGap) continue; return true;
  }
  return false;
}
export function planRoute(from, to, cab = false, extra = []) {
  CAB = cab; EXTRA = extra.filter(e => Math.hypot(from.x - e.x, from.z - e.z) > e.r * .5 || true);
  const key = (ix, iz) => ix * 10000 + iz; const ix0 = Math.round((from.x - X0) / CELL), iz0 = Math.round((from.z - Z0) / CELL), ix1 = Math.round((to.x - X0) / CELL), iz1 = Math.round((to.z - Z0) / CELL);
  const W = Math.round((X1 - X0) / CELL), H = Math.round((Z1 - Z0) / CELL);
  const open = [{ ix: ix0, iz: iz0, g: 0, f: 0 }], best = new Map([[key(ix0, iz0), 0]]), came = new Map(); let found = null, guard = 0;
  const h = (ix, iz) => Math.hypot(ix - ix1, iz - iz1);
  while (open.length && guard++ < 40000) {
    let bi = 0; for (let i = 1; i < open.length; i++) if (open[i].f < open[bi].f) bi = i; const cur = open.splice(bi, 1)[0];
    if (Math.hypot(cur.ix - ix1, cur.iz - iz1) < 1.5) { found = cur; break; }
    for (const [dx, dz] of [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1]]) {
      const nx = cur.ix + dx, nz = cur.iz + dz; if (nx < 0 || nz < 0 || nx > W || nz > H) continue;
      const wx = X0 + nx * CELL, wz = Z0 + nz * CELL; if (blocked(wx, wz) && Math.hypot(nx - ix1, nz - iz1) > 2) continue;
      const g = cur.g + (dx && dz ? 1.414 : 1); const k = key(nx, nz); if (best.has(k) && best.get(k) <= g) continue; best.set(k, g); came.set(k, key(cur.ix, cur.iz));
      open.push({ ix: nx, iz: nz, g, f: g + h(nx, nz) });
    }
  }
  if (!found) return [to];
  const pts = []; let k = key(found.ix, found.iz); while (k !== undefined) { pts.push({ x: X0 + Math.floor(k / 10000) * CELL, z: Z0 + (k % 10000) * CELL }); k = came.get(k); }
  pts.reverse(); // string-pull lightly: keep every 4th point
  const out = pts.filter((_, i) => cab ? i % 1 === 0 : i % 4 === 0); out.push(to); return out;
}

/** Route around the solid boxes of a settlement layout ([{x0,z0,x1,z1,h}], outpost metres). 1 m cells, 8-way, light string-pull. */
export function planRouteBoxes(from, to, boxes, margin = 0.9) {
  const bx = boxes.filter(b => (b.h ?? 1) >= 0.4); const C = 1, X0 = -300, Z0 = -300, N = 600;
  const blocked = (x, z) => { for (const b of bx) if (x > b.x0 - margin && x < b.x1 + margin && z > b.z0 - margin && z < b.z1 + margin) return true; return false; };
  const k = (i, j) => i * 1000 + j, ix = v => Math.max(0, Math.min(N, Math.round((v - X0) / C))), toW = i => X0 + i * C; const i0 = ix(from.x), j0 = ix(from.z), i1 = ix(to.x), j1 = ix(to.z);
  const heap = []; const push = n => { heap.push(n); let c = heap.length - 1; while (c > 0) { const p = (c - 1) >> 1; if (heap[p].f <= heap[c].f) break; [heap[p], heap[c]] = [heap[c], heap[p]]; c = p; } };
  const pop = () => { const top = heap[0], last = heap.pop(); if (heap.length) { heap[0] = last; let c = 0; for (;;) { let l = 2 * c + 1, r = l + 1, m = c; if (l < heap.length && heap[l].f < heap[m].f) m = l; if (r < heap.length && heap[r].f < heap[m].f) m = r; if (m === c) break; [heap[m], heap[c]] = [heap[c], heap[m]]; c = m; } } return top; };
  push({ i: i0, j: j0, g: 0, f: 0 }); const best = new Map([[k(i0, j0), 0]]), came = new Map(); let found = null, guard = 0;
  while (heap.length && guard++ < 400000) { const cur = pop(); if (cur.g > (best.get(k(cur.i, cur.j)) ?? 1e9)) continue;
    if (Math.hypot(cur.i - i1, cur.j - j1) < 1.5) { found = cur; break; }
    for (const [di, dj] of [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1]]) { const ni = cur.i + di, nj = cur.j + dj; if (ni < 0 || nj < 0 || ni > N || nj > N) continue;
      if (blocked(toW(ni), toW(nj)) && Math.hypot(ni - i1, nj - j1) > 2.5 && Math.hypot(ni - i0, nj - j0) > 3) continue; const g = cur.g + (di && dj ? 1.414 : 1), kk = k(ni, nj); if (best.has(kk) && best.get(kk) <= g) continue; best.set(kk, g); came.set(kk, k(cur.i, cur.j));
      push({ i: ni, j: nj, g, f: g + Math.hypot(ni - i1, nj - j1) }); } }
  if (!found) return [to]; const pts = []; let kk = k(found.i, found.j); while (kk !== undefined) { pts.push({ x: toW(Math.floor(kk / 1000)), z: toW(kk % 1000) }); kk = came.get(kk); }
  pts.reverse(); const out = pts.filter((_, n) => n % 3 === 0); out.push(to); return out;
}

// ---- page-side steering (one evaluate per tick) -----------------------------------------------------------------------
// frame: 'port' (port-local x,z), 'opening' (opening-local), 'ship' (ship-local, aboard), 'world' (a function name on window.__qaTarget)
export const STEER = ({ frame, x, z, pitch }) => {
  const c = window.cosmos; const wrap = a => { while (a > Math.PI) a -= 2 * Math.PI; while (a < -Math.PI) a += 2 * Math.PI; return a; };
  const faceWorld = (w, tp) => { const f = w.updateFrame(); const dx = tp.x - w.worldPos.x, dy = tp.y - w.worldPos.y, dz = tp.z - w.worldPos.z;
    const e = dx * f.east.x + dy * f.east.y + dz * f.east.z, n = dx * f.north.x + dy * f.north.y + dz * f.north.z; w.yaw = Math.atan2(e, n); return Math.hypot(e, n); };
  if (frame === 'port') { const w = c.walker, p = c.port.site.toLocal(w.worldPos); faceWorld(w, c.port.site.toWorld(x, p.y, z)); if (pitch !== undefined) w.pitch = pitch; return { d: Math.hypot(p.x - x, p.z - z), x: p.x, y: p.y, z: p.z }; }
  if (frame === 'opening') { const op = c.opening, m = op.model, w = m.walker, p = m.pose(); faceWorld(w, m.toWorld(x, 0, z)); if (pitch !== undefined) w.pitch = pitch; return { d: Math.hypot(p.x - x, p.z - z), x: p.x, y: p.y, z: p.z }; }
  if (frame === 'opening-cabin') { const sw = c.opening.cabinSw; const dx = x - sw.x, dz = z - sw.z; sw.yaw = Math.atan2(dx, -dz); return { d: Math.hypot(dx, dz), x: sw.x, y: sw.y, z: sw.z }; }
  if (frame === 'opening-liner' || frame === 'opening-kestrel') { const sw = frame === 'opening-liner' ? c.opening.liner.sw : c.opening.kestrel.sw; const dx = x - sw.x, dz = z - sw.z; sw.yaw = Math.atan2(dx, -dz); return { d: Math.hypot(dx, dz), x: sw.x, y: sw.y, z: sw.z }; }
  if (frame === 'ship') { const sw = c.ship.sw; const dx = x - sw.x, dz = z - sw.z; sw.yaw = Math.atan2(dx, -dz); return { d: Math.hypot(dx, dz), x: sw.x, y: sw.y, z: sw.z }; }
  if (frame === 'shipworld') { const w = c.walker; const tp = c.ship.flight.toWorld({ x, y: 0, z }); const d = faceWorld(w, tp); const l = c.ship.flight.toLocal(w.worldPos, {}); return { d: Math.hypot(l.x - x, l.z - z), x: l.x, y: l.y, z: l.z }; }
  if (frame === 'outpost') { // a settlement world's own frame (Earth's launch complex, the Moon's bases): x east, z south, origin the middle of the main pad
    const w = c.walker, pi = c.space.activeMoon.body.padInfo, q = w.worldPos, dx = q.x - pi.point.x, dy = q.y - pi.point.y, dz = q.z - pi.point.z;
    const px = dx * pi.east.x + dy * pi.east.y + dz * pi.east.z, py = dx * pi.up.x + dy * pi.up.y + dz * pi.up.z, pz = -(dx * pi.north.x + dy * pi.north.y + dz * pi.north.z);
    faceWorld(w, { x: pi.point.x + pi.east.x * x + pi.up.x * py - pi.north.x * z, y: pi.point.y + pi.east.y * x + pi.up.y * py - pi.north.y * z, z: pi.point.z + pi.east.z * x + pi.up.z * py - pi.north.z * z });
    if (pitch !== undefined) w.pitch = pitch; return { d: Math.hypot(px - x, pz - z), x: px, y: py, z: pz }; }
  if (frame === 'moonworld') { const w = c.walker; const tp = window.__moonTarget; const d = faceWorld(w, tp); return { d, x: w.worldPos.x, y: w.worldPos.y, z: w.worldPos.z }; }
  return { d: 999 };
};

export class Walker {
  constructor(s) { this.s = s; }
  /** Walk to a point. Returns true if you got there. Notices when it is stuck and tries what a person would. */
  async to(frame, x, z, { r = 1.4, timeout = 90, pitch, label = '', wander = true, route = false, quickCheck = null } = {}) {
    const s = this.s; const t0 = Date.now(); s.log(`walk to ${label || `${frame} ${Math.round(x)},${Math.round(z)}`}`);
    let pts = [{ x, z }]; let wi = 0; let lastD = 1e9, lastProg = Date.now(), tries = 0, lastLook = Date.now(), lastShot = Date.now();
    await s.stickDown(); if (!s.profile.touch && Math.random() < .5) await s.run(true);
    try {
      for (;;) {
        if (Date.now() - t0 > timeout * 1000) { s.finding({ kind: 'cannot-reach', sev: 72, title: `Could not walk to ${label || frame + ' ' + Math.round(x) + ',' + Math.round(z)}`, detail: `gave up after ${timeout}s; last distance ${Math.round(lastD)} m`, key: 'cannot-reach:' + (label || frame) }); return false; }
        let info = await s.safeEv(STEER, { frame, x: pts[wi].x, z: pts[wi].z, pitch }); if (!info) { await sleep(300); continue; }
        if (route && frame === 'port' && wi === 0 && pts.length === 1 && info.d > (route === 'cab' ? 2.5 : 6)) { const extra = route === 'cab' ? [] : await s.safeEv(({ tx, tz }) => { const c = cosmos, out = []; try { for (const sh of Object.values(c.world.snapshot?.ships || {})) { const p = sh.pose?.pos; if (!p) continue; const l = c.port.site.toLocal(p); if (Math.hypot(l.x - tx, l.z - tz) < 45) continue; out.push({ x: l.x, z: l.z, r: 15 }); } } catch {} return out; }, { tx: x, tz: z }, []);
          pts = planRoute({ x: info.x, z: info.z }, { x, z }, route === 'cab', extra); wi = 0; if (pts.length > 1) s.log(`route of ${pts.length} legs`); continue; }
        if (route && frame === 'outpost' && wi === 0 && pts.length === 1 && info.d > 5) { const boxes = await s.safeEv(() => cosmos.space.activeMoon.client.people.layout.BOXES.map(b => ({ x0: b.x0, z0: b.z0, x1: b.x1, z1: b.z1, h: b.h })), null, []);
          pts = planRouteBoxes({ x: info.x, z: info.z }, { x, z }, boxes); wi = 0; if (pts.length > 1) s.log(`outpost route of ${pts.length} legs around ${boxes.length} solid things`); continue; }
        const finalPt = wi === pts.length - 1;
        if (info.d < (finalPt ? r : 2.2)) { if (finalPt) return true; wi++; lastD = 1e9; lastProg = Date.now(); continue; }
        // a person glances around and sometimes drags the look finger; the bot does too (then re-faces the target next tick)
        if (wander && Date.now() - lastLook > rnd(9000, 17000)) { lastLook = Date.now(); await s.lookDrag(rnd(-90, 90), rnd(-20, 20)); }
        if (info.d < lastD - 0.6) { lastD = info.d; lastProg = Date.now(); }
        else if (Date.now() - lastProg > 7000) {
          tries = Math.floor(tries) + 1; s.log(`not getting closer (${Math.round(info.d)} m away), trying to get unstuck #${tries}`);
          if (tries === 1 && await s.visible('#btn-climb')) { await s.tap('#btn-climb', { why: 'climb the ledge' }); await sleep(1800); }
          else if (tries <= 4) { // a person backs off, takes a run-up and jumps (a jump from standing against a wall goes straight up)
            const run = 520 + tries * 90 + rnd(-60, 60); s.log(`run-up jump #${tries}`);
            await s.safeEv(() => { const w = cosmos.walker; w.yaw += Math.PI; }); await sleep(1000 + tries * 120);
            await s.safeEv(STEER, { frame, x: pts[wi].x, z: pts[wi].z }); await sleep(run); await s.jump(); await sleep(1500); }
          else if (tries === 5) { const dir = Math.random() < .5 ? 1 : -1; s.log('sidestep around whatever is in the way'); await s.safeEv(({ d }) => { const w = cosmos.walker; w.yaw += d * 1.57; }, { d: dir }); await sleep(3800); pts = [{ x, z }]; wi = 0; tries = 5.5; }
          else if (tries >= 8) { s.finding({ kind: 'stuck-walking', sev: 80, title: `Stuck while walking to ${label || frame}`, detail: (frame === 'port' && Math.abs(info.x) > 100 && Math.abs(info.x) < 108 ? 'This is at the port perimeter kerb (a ~0.6 m high concrete wall ring at x = +/-103; walking steps up only 0.35 m, and a jump from a standstill against it goes straight up). ' : '') + `no progress for ${tries * 7}s at ${frame} ${Math.round(info.x)},${Math.round(info.z)} (target ${Math.round(x)},${Math.round(z)}, ${Math.round(info.d)} m away)`, key: 'stuck-walk:' + (label || frame) }); return false; }
          lastProg = Date.now(); lastD = info.d + 0.1;
        }
        if (Date.now() - lastShot > 25000) { lastShot = Date.now(); await s.shot('walking'); }
        if (quickCheck) { const q = await quickCheck(); if (q) return true; }
        await sleep(rnd(110, 190));
      }
    } finally { await s.stickUp(); if (!s.profile.touch) await s.run(false); }
  }

  /** Follow a dense list of points (a planned path) with the stick held the whole way, steering a step ahead. */
  async along(frame, pts, { label = 'path', timeout = 120, ahead = 0 } = {}) {
    const s = this.s; const t0 = Date.now(); let i = 0, lastProg = Date.now(), best = 1e9;
    await s.stickDown();
    try {
      while (i < pts.length) {
        if (Date.now() - t0 > timeout * 1000) { s.finding({ kind: 'cannot-reach', sev: 72, title: `Could not follow the walking route: ${label}`, detail: `gave up after ${timeout}s at point ${i} of ${pts.length}`, key: 'cannot-reach:' + label }); return false; }
        const tgt = pts[Math.min(pts.length - 1, i + ahead)]; const info = await s.safeEv(STEER, { frame, x: tgt.x, z: tgt.z }); if (!info) { await sleep(200); continue; }
        // advance past every point we are already close to
        while (i < pts.length) { const p = pts[i]; if (Math.hypot(info.x - p.x, info.z - p.z) < 0.45 && (p.y === undefined || Math.abs(info.y - p.y) < 0.9)) i++; else break; }
        const rest = Math.hypot(info.x - pts[pts.length - 1].x, info.z - pts[pts.length - 1].z); if (rest < best - 0.4) { best = rest; lastProg = Date.now(); }
        if (Date.now() - lastProg > 9000) { await s.jump(); lastProg = Date.now() - 4000; if (Date.now() - t0 > 30000 && rest > 3) { s.finding({ kind: 'stuck-walking', sev: 78, title: `Stuck on a walking route: ${label}`, detail: `at ${Math.round(info.x * 10) / 10},${Math.round(info.z * 10) / 10} (y ${info.y}), ${Math.round(rest)} m from the end`, key: 'stuck-walk:' + label }); return false; } }
        await sleep(120);
      }
      return true;
    } finally { await s.stickUp(); }
  }
}
