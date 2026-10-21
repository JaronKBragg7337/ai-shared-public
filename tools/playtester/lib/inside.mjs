// The "inside the ships" pass of the spots phase. Goes aboard the ships a player can stand in and puts the camera where a person finds trouble by hand:
// every door at 5 m (door shut) and 1.5 m (door slides open by itself within 1.7 m), the far side of every door, the view back from the cockpit /
// front window toward the cabin and its door, and each room from its doorway. Layouts come from the game's own registry (read only).
// Math checks (no picture): duplicate door labels in one ship, a prop / wall screen in a door's clear opening, door signs that fall back to MEDBAY.
//   liner   = Ares liner "Hellas Dawn": only exists while the opening is on its first stage (window.cosmos.opening.liner)
//   kestrel = "Soft Landing": the opening's descent transport, shown by holding the opening on its descent stage (nothing is sent to the server)
//   own     = the player's own ship (the Skiff), via window.cosmos.ship
// Ground rules: ship-local walking is local (no server pull-back), so we place the walker directly. What to look for lives in ../spots.json "inside".
import { sleep } from './core.mjs';

const PAGE = `(() => {
  const hold = {};
  const stop = () => { if (hold.t) clearInterval(hold.t); hold.t = null; };
  window.__in = {
    async layouts() {
      const reg = await import('./src/ships/registry.js'), c = cosmos, S = c.ship?.signs, out = {};
      const uv = n => { try { return JSON.stringify(S.uvFor(n)); } catch { return null; } };
      const fallback = S ? uv('__no_such_sign__') : null, medbay = S ? uv('MEDBAY') : null;
      for (const t of reg.shipTypes()) {
        const d = reg.shipDef(t), L = d.layout;
        out[t] = { name: d.name || t, rooms: L.rooms.map(r => ({ id: r.id, name: r.name, kind: r.kind, x0: r.x0, x1: r.x1, z0: r.z0, z1: r.z1, y: r.y, h: r.h, canopy: !!r.canopy })),
          doors: L.doors.map(x => ({ id: x.id, a: x.a, b: x.b, axis: x.axis, at: x.at, c: x.c, w: x.w, h: x.h, y: x.y, kind: x.kind, sign: x.sign,
            shows: x.sign && S && uv(x.sign) === fallback && x.sign !== 'MEDBAY' ? (fallback === medbay ? 'MEDBAY' : '(fallback)') : x.sign })),
          props: L.props.map(p => ({ kind: p.kind, room: p.room, x: p.x, z: p.z, y: p.y, w: p.w, d: p.d, h: p.h, rot: p.rot, blocks: p.blocks })),
          screens: (L.wallScreens || []).map(w => ({ id: w.id, room: w.room, x: w.x, y: w.y, z: w.z, w: w.w, h: w.h, facing: w.facing })),
          seats: (L.seats || []).map(q => ({ id: q.id, room: q.room, x: q.x, z: q.z })), fallbackIsMedbay: fallback === medbay };
      }
      return out;
    },
    // Which ships can be stood in right now.
    avail() { const c = cosmos, o = c.opening; return { liner: !!(o && o.active && o.liner && o.state.stage === 0), kestrel: !!(o && o.active && o.liner), own: !!c.ship?.layout || !!c.ship?.def?.layout, ownType: c.ship?.def?.type, linerType: o?.liner?.def?.type, kestrelType: o?.kestrel?.def?.type || 'descender' }; },
    ready() { const o = cosmos.opening; return !o?.fade ? true : Number(o.fade.style.opacity || 0) < .05; },
    begin(mode) {
      stop(); const c = cosmos, o = c.opening;
      if (mode === 'liner') { const L = o.liner; hold.t = setInterval(() => { o.state.stage = 0; o.clock = 50; }, 8); hold.tgt = { sw: L.sw, type: L.def.type, stage: L }; return { type: L.def.type }; }
      if (mode === 'kestrel' || mode === 'skiff') {
        const K0 = o._ensureKestrel(); hold.k0 = hold.k0 || K0;
        if (mode === 'skiff' && !hold.skiff) hold.skiff = new K0.constructor({ engine: c.engine, type: 'lifeboat', name: 'Skiff', registry: 'MR-0001', mats: o.mats, signs: o.ship.signs, posters: o.ship.posters, tier: o.tier });
        const K = mode === 'skiff' ? hold.skiff : hold.k0; o.kestrel = K; o.kestrelDef = K.def;
        if (!hold.kInit) { hold.kInit = true; o.state.stage = 2; o.enterStage(2); o.kestrel = K; o.kestrelDef = K.def; }
        hold.t = setInterval(() => { o.state.stage = 2; o.clock = 1; c.engine.overlayScenes = [K.interiorScene]; }, 8); hold.tgt = { sw: K.sw, type: K.def.type, stage: K }; return { type: K.def.type }; }
      const sh = c.ship; hold.tgt = { sw: sh.sw, type: sh.def.type, own: sh }; if (sh.seat) sh.stations.stand(); sh.aboard = true; return { type: sh.def.type };
    },
    put(x, y, z, yaw, pitch) { const t = hold.tgt; if (t.own) t.own.aboard = true; t.sw.place(x, y, z, yaw); t.sw.pitch = pitch; return { room: (t.stage || t.own).currentRoom || null, at: [t.sw.x, t.sw.y, t.sw.z] }; },
    at() { const t = hold.tgt; return t ? { x: t.sw.x, y: t.sw.y, z: t.sw.z, room: (t.stage || t.own).currentRoom || null } : null; },
    end() { stop(); hold.tgt = null; },
  };
})()`;

const inRoom = (r, x, z, m = .3) => x >= r.x0 + m && x <= r.x1 - m && z >= r.z0 + m && z <= r.z1 - m;
const doorCentre = d => d.axis === 'x' ? { x: d.at, z: d.c } : { x: d.c, z: d.at };
const doorNormal = d => d.axis === 'x' ? { x: 1, z: 0 } : { x: 0, z: 1 };
const yawTo = (dx, dz) => Math.atan2(dx, -dz);
const label = v => String(v == null ? 'x' : v).toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');

// Pure geometry: boxes that sit in a door's clear opening. Door: slab 'clearApproach' m each side for props that block, a thin slab for wall-mounted things.
export function doorOverlaps(L, rules) {
  const out = [], roomsById = new Map(L.rooms.map(r => [r.id, r]));
  for (const d of L.doors) {
    const c = doorCentre(d), along = d.axis === 'x' ? 'z' : 'x', across = d.axis === 'x' ? 'x' : 'z', hw = d.w / 2, y0 = d.y, y1 = d.y + d.h;
    for (const p of L.props) {
      if (p.room !== d.a && p.room !== d.b) continue;
      const swap = (p.rot || 0) % 2 !== 0, w = swap ? p.d : p.w, dd = swap ? p.w : p.d, py0 = p.y, py1 = p.y + p.h;
      const bx = [p.x - w / 2, p.x + w / 2], bz = [p.z - dd / 2, p.z + dd / 2];
      const slab = p.blocks === false ? rules.clearWallMounted : rules.clearApproach;
      const ox = d.axis === 'x' ? [c.x - slab, c.x + slab] : [c.x - hw, c.x + hw], oz = d.axis === 'x' ? [c.z - hw, c.z + hw] : [c.z - slab, c.z + slab];
      if (bx[0] < ox[1] && bx[1] > ox[0] && bz[0] < oz[1] && bz[1] > oz[0] && py0 < y1 - 0.1 && py1 > y0 + 0.1 && (p.blocks !== false || py1 - py0 > 0.05)) out.push({ door: d, what: `${p.kind} in ${p.room}`, blocks: p.blocks !== false });
    }
    for (const sc of L.screens || []) {
      if (sc.room !== d.a && sc.room !== d.b) continue;
      const fx = /^x/.test(sc.facing || ''), ext = fx ? [sc.z - sc.w / 2, sc.z + sc.w / 2] : [sc.x - sc.w / 2, sc.x + sc.w / 2], plane = fx ? sc.x : sc.z;
      if (d.axis === (fx ? 'x' : 'z') && Math.abs(plane - d.at) < .5 && ext[0] < d.c + hw && ext[1] > d.c - hw && sc.y - sc.h / 2 < y1 && sc.y + sc.h / 2 > y0) out.push({ door: d, what: `wall screen ${sc.id || ''} in ${sc.room}`, blocks: false });
    }
  }
  return out;
}

export async function insidePass(s, ctx) {
  const { R, counts, bump, finding, PAGE_HELPERS } = ctx, I = R.inside; if (!I) return { ships: [] };
  await s.safeEv(PAGE);
  const lay = await s.safeEv(() => window.__in.layouts(), null, null);
  const covered = [];
  if (!lay) { s.log('spots inside: could not read the ship registry'); return { ships: covered }; }

  // ---- math, every ship in the registry (no picture) ----------------------------------------------------------------------------------
  for (const [type, L] of Object.entries(lay)) {
    const by = new Map(); for (const d of L.doors) if (d.sign) by.set(d.sign, [...(by.get(d.sign) || []), d.id]);
    for (const [sign, ids] of by) if (ids.length > 1) finding({ kind: 'spot-inside-duplicate-door-label', sev: ids.length >= 3 ? 60 : 42, title: `Door label "${sign}" used on ${ids.length} doors inside the ${L.name}`, detail: ids.join(', '), key: `spot-inside-dup:${type}:${sign}` });
    const lost = L.doors.filter(d => d.sign && d.shows !== d.sign);
    if (lost.length) finding({ kind: 'spot-interior-sign-fallback', sev: 70, title: `${lost.length} door sign(s) inside the ${L.name} show the wrong text (${L.fallbackIsMedbay ? 'MEDBAY' : 'fallback'})`, detail: lost.map(d => `${d.id} wants "${d.sign}"`).join('; '), key: 'spot-interior-sign-fallback:' + type });
    for (const o of doorOverlaps(L, I)) finding({ kind: 'spot-inside-door-obstruction', sev: o.blocks ? 78 : 66, title: `${o.what} sits in the clear opening of door ${o.door.id}${o.door.sign ? ' (' + o.door.sign + ')' : ''} inside the ${L.name}`, detail: `Layout bounds check: door ${o.door.axis}=${o.door.at}, centre ${o.door.c}, width ${o.door.w}.`, key: `spot-inside-door-box:${type}:${o.door.id}:${o.what}` });
  }

  // ---- go aboard ------------------------------------------------------------------------------------------------------------------------
  const av = await s.safeEv(() => window.__in.avail(), null, {});
  const wasOpening = !!(av.liner || av.kestrel);
  const todo = [];
  if (av.liner) todo.push(['liner', av.linerType]); else s.log('spots inside: the opening is not on its liner stage, so the Hellas Dawn cannot be boarded in this run (run the spots phase on a fresh player)');
  if (av.kestrel) { todo.push(['kestrel', av.kestrelType]); todo.push(['skiff', 'lifeboat']); }
  const pending = todo.slice();
  const runShip = async (mode, type) => {
    const L = lay[type]; if (!L) return;
    const b = await s.safeEv(m => window.__in.begin(m), mode, null); if (!b) { s.log(`spots inside: could not go aboard (${mode})`); return; }
    for (let i = 0; i < 40 && mode === 'liner' && !(await s.safeEv(() => window.__in.ready(), null, true)); i++) await sleep(500);
    await sleep(mode === 'kestrel' ? 2500 : 1500);
    const shipName = mode === 'skiff' ? 'Skiff (lifeboat)' : mode === 'liner' ? 'Hellas Dawn (Ares liner)' : mode === 'kestrel' ? 'Kestrel (Soft Landing)' : mode === 'own' ? `${L.name} (own ship)` : L.name; const tag = shipName.toLowerCase().replace(/[^a-z]+/g, '-').replace(/-$/, ''); const rooms = new Map(L.rooms.map(r => [r.id, r]));
    let n = 0;
    const view = async (kind, name, p, tgt, look) => {
      const yaw = yawTo(tgt.x - p.x, tgt.z - p.z), eye = p.y + I.eyeHeight, pitch = Math.atan2(tgt.y - eye, Math.hypot(tgt.x - p.x, tgt.z - p.z));
      await s.safeEv(a => window.__in.put(a.x, a.y, a.z, a.yaw, a.pitch), { ...p, yaw, pitch }); await sleep(I.settleMs);
      await s.safeEv(a => window.__in.put(a.x, a.y, a.z, a.yaw, a.pitch), { ...p, yaw, pitch }); await sleep(250);
      const rec = await s.shot(`spot-inside-${tag}-${name}`); if (rec) { rec.whatToLookFor = look; rec.spotKind = 'inside-' + kind; bump('inside'); n++; } return rec;
    };
    // doors
    for (const d of L.doors) {
      const c = doorCentre(d), nrm = doorNormal(d), y = d.y, sides = [];
      for (const sgn of [-1, 1]) {
        let best = 0, rm = null;
        for (let dist = 5; dist >= 1; dist -= .25) { const x = c.x + nrm.x * sgn * dist, z = c.z + nrm.z * sgn * dist, r = L.rooms.find(q => Math.abs(q.y - y) < 1.2 && inRoom(q, x, z)); if (r && (r.id === d.a || r.id === d.b)) { best = dist; rm = r; break; } }
        if (best >= 1) sides.push({ sgn, maxd: best, room: rm });
      }
      if (!sides.length) { s.log(`spots inside: no standing room in front of door ${d.id}`); continue; }
      sides.sort((p, q) => (q.room.id === d.a) - (p.room.id === d.a) || q.maxd - p.maxd);
      const word = d.sign ? `"${d.sign}"` : 'unsigned';
      const [prim, sec] = sides;
      const done = new Set();
      for (const dist of I.distances) {
        const dd = Math.min(dist, prim.maxd); if (done.has(dd)) continue; done.add(dd);
        const open = dd <= 1.7;
        await view('door', `door-${label(d.id)}-${label(d.sign)}-${dd.toFixed(1)}m-${open ? 'open' : 'shut'}-from-${label(prim.room.id)}`,
          { x: c.x + nrm.x * prim.sgn * dd, y, z: c.z + nrm.z * prim.sgn * dd }, { x: c.x, y: y + 1.1, z: c.z }, `${open ? I.look['door-open'] : I.look.door} Door ${d.id}, label ${word}, between ${d.a} and ${d.b}; viewed from ${prim.room.name || prim.room.id}, ${dd.toFixed(1)} m away.`);
      }
      if (sec) { const dd = Math.min(I.secondSideDistance, sec.maxd);
        await view('door', `door-${label(d.id)}-${label(d.sign)}-${dd.toFixed(1)}m-open-from-${label(sec.room.id)}`, { x: c.x + nrm.x * sec.sgn * dd, y, z: c.z + nrm.z * sec.sgn * dd }, { x: c.x, y: y + 1.1, z: c.z }, `${I.look['door-open']} This is the OTHER side of door ${d.id} (label ${word}); viewed from ${sec.room.name || sec.room.id}.`); }
    }
    // cockpit / front window looking back at the cabin and its door
    for (const r of L.rooms.filter(q => q.canopy || q.kind === 'bridge')) {
      const dr = L.doors.find(d => (d.a === r.id || d.b === r.id) && d.a !== 'outside' && d.b !== 'outside'); if (!dr) continue;
      const c = doorCentre(dr), cx = (r.x0 + r.x1) / 2, front = r.z0 + .55, mid = { x: c.x, y: r.y + 1.2, z: c.z };
      await view('cockpit', `cockpit-${label(r.id)}-front-window-looking-back`, { x: cx, y: r.y, z: front }, { x: cx, y: r.y + 1.0, z: r.z1 + 6 }, `${I.look.cockpit} Standing at the front window of ${r.name || r.id}, looking straight back (past the door ${dr.id}${dr.sign ? ' "' + dr.sign + '"' : ''}).`);
      await view('cockpit', `cockpit-${label(r.id)}-front-window-at-door`, { x: cx, y: r.y, z: front }, mid, `${I.look.cockpit} Same spot, aimed at the door ${dr.id}.`);
      for (const q of L.seats.filter(q => q.room === r.id).slice(0, 2)) await view('cockpit', `cockpit-${label(r.id)}-seat-${label(q.id)}-looking-back`, { x: q.x, y: r.y, z: q.z }, mid, `${I.look.cockpit} From the ${q.id} seat position, looking back at door ${dr.id}.`);
    }
    // each room from its doorway
    for (const r of L.rooms) {
      const dr = L.doors.find(d => d.a === r.id || d.b === r.id); if (!dr) continue;
      const c = doorCentre(dr), nrm = doorNormal(dr); let p = null;
      for (const sgn of [-1, 1]) { const x = c.x + nrm.x * sgn * .45, z = c.z + nrm.z * sgn * .45; if (inRoom(r, x, z, .1)) { p = { x, y: r.y, z }; break; } }
      if (!p) continue;
      await view('room', `room-${label(r.id)}-from-door-${label(dr.id)}`, p, { x: (r.x0 + r.x1) / 2, y: r.y + 1.2, z: (r.z0 + r.z1) / 2 }, `${I.look.room} Room: ${r.name || r.id} (${r.kind}), from the doorway ${dr.id}.`);
    }
    await s.safeEv(() => window.__in.end());
    covered.push({ ship: shipName, type, mode, shots: n, doors: L.doors.length, rooms: L.rooms.length });
    s.log(`spots inside: ${L.name} (${mode}): ${n} shots, ${L.doors.length} doors, ${L.rooms.length} rooms`);
  };

  for (const [mode, type] of pending) { await runShip(mode, type); }
  if (wasOpening) {   // the opening scene is now dirty and the port pass needs the player at the port: reload with the opening off
    const here = await s.safeEv(() => location.href, null, null);
    if (here) { const u = new URL(here); u.searchParams.set('opening', 'off'); await s.open(u.toString()); await s.safeEv(PAGE_HELPERS); await s.safeEv(PAGE); await sleep(2500); }
  }
  let ownAv = {};
  for (let i = 0; i < 30; i++) { ownAv = await s.safeEv(() => window.__in.avail(), null, {}) || {}; if (ownAv.own) break; await sleep(1000); }
  s.log('spots inside: own ship ' + JSON.stringify(ownAv));
  if (ownAv.own && !covered.some(c => c.type === ownAv.ownType)) await runShip('own', ownAv.ownType);
  else s.log('spots inside: own ship ' + (ownAv.own ? ownAv.ownType + ' already covered' : 'has no layout to board'));
  return { ships: covered, notBoarded: Object.keys(lay).filter(t => !covered.some(c => c.type === t)) };
}
