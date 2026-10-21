// The "spots" phase: walks the game's own object lists (window.cosmos) and puts the camera at the places a person finds trouble by hand.
// What to visit and what to look for lives in ../spots.json (one block per trouble type). Each screenshot carries a "whatToLookFor"
// line the vision review reads. Math checks (no screenshot needed) become findings.
import { readFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { sleep } from './core.mjs';
import { insidePass } from './inside.mjs';

const rules = JSON.parse(readFileSync(join(dirname(fileURLToPath(import.meta.url)), '..', 'spots.json'), 'utf8'));

// Installed in the page once: put the walker at a port-local spot (feet) and aim the camera at a port-local point.
const PAGE_HELPERS = `(() => {
  const dot = (u, n) => u.x * n.x + u.y * n.y + u.z * n.z;
  window.__spot = {
    place(from, to) {
      const c = cosmos, site = c.port.site, w = c.walker;
      Object.assign(w.worldPos, site.toWorld(from.x, from.y, from.z));
      if (w.velocity) { w.velocity.x = 0; w.velocity.y = 0; w.velocity.z = 0; }
      const f = w.updateFrame(), eyeY = from.y + (w.eyeHeightM || 1.65);
      const dx = to.x - from.x, dz = to.z - from.z, dy = to.y - eyeY;
      const a = site.toWorld(from.x, from.y, from.z), b = site.toWorld(from.x + dx, from.y, from.z + dz);
      const v = { x: b.x - a.x, y: b.y - a.y, z: b.z - a.z };
      w.yaw = Math.atan2(dot(v, f.east), dot(v, f.north)); w.pitch = Math.atan2(dy, Math.hypot(dx, dz));
      return { yaw: w.yaw, pitch: w.pitch, eye: eyeY };
    },
    // The shared-world server pulls a player back to the furthest point a person could have walked (about 12 m/s), so a teleport does not stick.
    // Walk there instead: slide the walker at a human pace and let the server's copy catch up before the picture is taken.
    async glide(to, mps = 9) {
      const c = cosmos, w = c.walker, site = c.port.site, t0 = performance.now(); let last = t0;
      while (performance.now() - t0 < 90000) {
        const cur = site.toLocal(w.worldPos), dx = to.x - cur.x, dz = to.z - cur.z, d = Math.hypot(dx, dz); if (d < .3) break;
        await new Promise(r => setTimeout(r, 70)); const now = performance.now(), dt = Math.min(.2, (now - last) / 1000); last = now;
        const k = Math.min(d, mps * dt) / d; Object.assign(w.worldPos, site.toWorld(cur.x + dx * k, to.y, cur.z + dz * k));
        if (w.velocity) { w.velocity.x = 0; w.velocity.y = 0; w.velocity.z = 0; }
      }
      const pid = c.world.playerId; let ack = false;
      for (let i = 0; i < 30; i++) { const sp = c.world.snapshot.players?.[pid]?.pose?.worldPos; if (sp) { const q = site.toLocal(sp); if (Math.hypot(q.x - to.x, q.z - to.z) < 2.5) { ack = true; break; } } await new Promise(r => setTimeout(r, 150)); }
      return { ack, secs: Math.round((performance.now() - t0) / 1000) };
    },
    // Every ship parked at the port: pose, type, ramp state and (when its model can be found) the ramp meshes, in port-local metres.
    ships() {
      const c = cosmos, snap = c.world.snapshot, cam = c.engine.camera, Q = cam.quaternion.constructor, V = cam.position.constructor, scene = c.engine.scene;
      const out = [];
      for (const [id, sh] of Object.entries(snap.ships || {})) {
        if (!sh.pad || !sh.pose?.pos || !sh.pose.quaternion) continue;
        const q = new Q().fromArray(sh.pose.quaternion), pos = sh.pose.pos;
        const P = (x, y, z) => { const v = new V(x, y, z).applyQuaternion(q); return c.port.site.toLocal({ x: pos.x + v.x, y: pos.y + v.y, z: pos.z + v.z }); };
        const centre = P(0, 0, 0); if (Math.hypot(centre.x, centre.z) > 2000) continue;
        const states = sh.state?.ramps || {};
        out.push({ id, type: sh.type, pad: sh.pad.number, centre, states });
      }
      return out;
    },
    // Ramp meshes of one parked ship, read from the game's own ship model (ext.ramps), in port-local metres. Only exists once the model is built (the player is near).
    ramps(id) {
      const c = cosmos, cam = c.engine.camera, V = cam.position.constructor, Q = cam.quaternion.constructor, sh = c.world.snapshot.ships[id];
      let view = c.multiplayer?.fleetView?.views?.get(id), ext = view?.ext, kind = ext ? 'remote' : null;
      if (!ext && c.ship?.exterior?.ramps && [c.ship.id, c.ship.shipId, c.ship.state?.id].includes(id)) { ext = c.ship.exterior; kind = 'own'; }
      const q = new Q().fromArray(sh.pose.quaternion), pos = sh.pose.pos;
      const P = v => { const w = v.clone().applyQuaternion(q); return c.port.site.toLocal({ x: pos.x + w.x, y: pos.y + w.y, z: pos.z + w.z }); };
      const out = { kind, ramps: [] };
      for (const key of ['cargo', 'airlock']) {
        const st = sh.state?.ramps?.[key] || {}; const r = { key, lowered: !!st.lowered, found: false };
        const rr = ext?.ramps?.[key];
        if (rr?.hinge) {
          r.found = true; let tris = 0, vis = true, opacity = 1, mn = null, mx = null; const M = rr.hinge.matrix.constructor;
          const mesh = rr.mesh; r.mesh = !!mesh;
          if (mesh) {
            mesh.traverse(o => { if (!o.isMesh || !o.geometry) return; tris += (o.geometry.index ? o.geometry.index.count : (o.geometry.attributes.position?.count || 0)) / 3;
              const m = Array.isArray(o.material) ? o.material[0] : o.material; if (m && m.opacity < opacity) opacity = m.opacity;
              o.geometry.computeBoundingBox(); const bb = o.geometry.boundingBox.clone(); const mat = o.matrix.clone(); for (let p = o.parent; p && p !== rr.hinge; p = p.parent) mat.premultiply(p.matrix);
              bb.applyMatrix4(mat); mn = mn ? mn.min(bb.min) : bb.min.clone(); mx = mx ? mx.max(bb.max) : bb.max.clone(); });
            for (let o = mesh; o && o !== ext.root.parent; o = o.parent) if (o.visible === false) vis = false;
          }
          r.tris = Math.round(tris); r.visible = vis; r.opacity = opacity;
          const ctr = mn && mx ? mn.clone().add(mx).multiplyScalar(.5) : new V(0, 0, (rr.def?.length || 5) / 2);
          r.hingeP = P(rr.hinge.position); r.footP = P(ctr.clone().multiplyScalar(2).applyMatrix4(rr.hinge.matrix));
        }
        else if (!ext && c.ship?.def?.type === sh.type && c.ship.def.ramps?.[key]) {   // model not built yet: same class as the player's ship, so use the ship definition's ramp hardware
          const R = c.ship.def.ramps[key], ang = st.angle ?? .47, run = R.length * Math.cos(ang);
          r.found = true; r.derived = true; r.hingeP = P(new V(R.hinge.x, R.hinge.y, R.hinge.z)); r.footP = P(new V(R.hinge.x + R.dir.x * run, R.hinge.y - R.length * Math.sin(ang), R.hinge.z + R.dir.z * run));
        }
        out.ramps.push(r);
      }
      out.derivedKind = out.ramps.some(r => r.derived) ? 'definition' : null;
      return out;
    },
    // Door signs inside the player's own ship: what text each one really shows (an unknown name falls back to the first atlas entry).
    interiorSigns() {
      const c = cosmos, L = c.ship?.layout || c.ship?.def?.layout, S = c.ship?.signs; if (!L?.doors || !S?.uvFor) return null;
      const uv = n => JSON.stringify(S.uvFor(n)), fallback = uv('__no_such_sign__'), medbay = uv('MEDBAY');
      return { type: c.ship.def?.type, fallbackIsMedbay: fallback === medbay,
        doors: L.doors.filter(d => d.sign).map(d => ({ id: d.id, sign: d.sign, shows: uv(d.sign) === fallback && d.sign !== 'MEDBAY' ? (fallback === medbay ? 'MEDBAY' : '(fallback)') : d.sign })) };
    },
  };
})()`;

export function addSpotsPhase(P, s) {
  P.spots = async () => {
    const R = rules, settle = R.settleMs || 450, counts = {}; s.spotCounts = counts;
    const bump = k => { counts[k] = (counts[k] || 0) + 1; };
    await s.safeEv(PAGE_HELPERS);
    // Put the camera at `from` (port-local feet) aimed at `to`, then take the picture. Returns null if the game refused.
    const view = async (kind, label, from, to, look) => {
      const g = await s.safeEv(({ from }) => window.__spot.glide(from), { from }, null); if (g && !g.ack) s.log(`spots: server copy did not confirm the move to ${kind} ${label} (${g.secs}s)`);
      await s.safeEv(({ from, to }) => window.__spot.place(from, to), { from, to }); await sleep(settle);
      await s.safeEv(({ from, to }) => window.__spot.place(from, to), { from, to }); await sleep(120);   // re-pin: gravity moved us a hair
      // if the game still moved the player (server pull-back, dock zone), a picture from the wrong place would mislead
      const off = await s.safeEv(({ from }) => { const l = cosmos.port.site.toLocal(cosmos.walker.worldPos); return Math.hypot(l.x - from.x, l.z - from.z); }, { from }, 0);
      if (off > 3) { counts.skippedMoved = (counts.skippedMoved || 0) + 1; s.log(`spots: skipped ${kind} ${label}: the game moved the player ${off.toFixed(0)} m away from the requested spot`); return null; }
      const rec = await s.shot(`spot-${kind}-${label}`); if (rec) { rec.whatToLookFor = look; rec.spotKind = kind; bump(kind); } return rec;
    };
    const finding = (f) => s.finding({ shot: false, ...f });

    // ---- inside the ships (liner, Kestrel, the player's own Skiff); reloads the page out of the opening when it used it -------------------
    s.insideSummary = await insidePass(s, { R, counts, bump, finding, PAGE_HELPERS });

    if (process.env.SPOTS_INSIDE_ONLY) { s.spotInventory = { doors: [], counts: { pads: 0 }, ships: [], signs: 0, inside: s.insideSummary }; s.spotRules = rules; return `inside-the-ships only: ${Object.values(counts).reduce((a, b) => a + b, 0)} shots`; }

    // ---- inventory --------------------------------------------------------------------------------------------------------
    const data = await s.safeEv(() => {
      const c = window.cosmos, doors = c.port?.doors || [], boxes = c.port?.boxes || [], snap = c.world?.snapshot || {};
      const pack = doors.map((d, i) => ({ i, id: d.asset?.id, name: d.asset?.name || d.asset?.id || `door ${i + 1}`, kind: d.asset?.kind, x: d.asset?.x, z: d.baseZ, bz: d.baseZ, ax: d.asset?.x, az: d.asset?.z, ad: d.asset?.d, aw: d.asset?.w, width: d.asset?.doorW }));
      const names = new Map(); for (const d of pack) names.set(d.name.toLowerCase(), (names.get(d.name.toLowerCase()) || 0) + 1);
      const overlaps = pack.flatMap(d => boxes.filter(b => b.id !== d.id && d.x != null && d.width && b.x0 < d.x + d.width / 2 && b.x1 > d.x - d.width / 2 && b.z0 < d.z + .35 && b.z1 > d.z - .35 && b.y1 - b.y0 > .3).map(b => ({ door: d.name, prop: b.id || 'box' })));
      const buildings = (c.port?.assets || []).map(a => ({ id: a.id, name: a.name, type: a.type }));
      return { doors: pack, duplicate: [...names].filter(([, n]) => n > 1), overlaps, pads: (snap.pads || []).map(p => ({ id: p.id, number: p.number, x: p.x, z: p.z, w: p.w, d: p.d })), buildings,
        counts: { portRooms: c.port?.assets?.length || 0, pads: (snap.pads || []).length, ships: Object.keys(snap.ships || {}).length } };
    }, null, { doors: [], duplicate: [], overlaps: [], pads: [], buildings: [], counts: {} });
    s.log('spots source inventory ' + JSON.stringify({ doors: data.doors.length, pads: data.pads.length, counts: data.counts }));
    for (const [name, n] of data.duplicate) finding({ kind: 'spot-duplicate-door-name', sev: 42, title: `Duplicate door name: ${name}`, detail: `${n} port doors share this name`, key: 'spot-door-name:' + name });
    for (const x of data.overlaps) finding({ kind: 'spot-door-obstruction', sev: 78, title: `Prop box overlaps the clear opening at ${x.door}`, detail: `Port collision box ${x.prop} intersects the door opening (cheap bounds check).`, key: `spot-door-box:${x.door}:${x.prop}` });

    // ---- doors: three distances x shut/open, then one look down through the open doorway ------------------------------------------------
    for (const d of data.doors) {
      if (d.x == null || d.z == null) continue;
      const setDoor = open => s.safeEv(({ i, open }) => { const door = cosmos.port.doors[i]; if (!door) return; if (open) { door.progress = 1; door.mesh.position.set(door.asset.x + door.asset.doorW + .2, 0, door.baseZ); } else { door.progress = 0; door.mesh.position.set(door.asset.x, 0, door.baseZ); } }, { i: d.i, open });
      for (const dist of R.doors.distances) for (const state of R.doors.states) {
        await setDoor(state === 'open');
        await view('door', `${d.name}-${dist}m-${state}`, { x: d.x, y: .5, z: d.z - dist - 1.4 }, { x: d.x, y: 1.2, z: d.z }, R.doors.look);
      }
      if (R.doors.floorView) { await setDoor(true); await view('door-floor', `${d.name}-looking-down-through-opening`, { x: d.x, y: .5, z: d.z - 1.3 }, { x: d.x, y: 0, z: d.z + .5 }, R.doors.lookFloor); }
    }

    // ---- ships and ramps -------------------------------------------------------------------------------------------------
    const ships = await s.safeEv(() => window.__spot.ships(), null, []);
    s.log(`spots: ${ships.length} parked ships: ` + ships.map(x => `${x.type}@pad${x.pad}`).join(', '));
    ships.sort((a, b) => a.centre.x - b.centre.x);
    const rampDone = new Set(), shipModels = [];
    for (const sh of ships) {
      const rad = R.ships.radius[sh.type] ?? R.ships.radius.default, n = R.ships.ring, ly = sh.centre.y > 1 ? Math.min(sh.centre.y + 1, R.ships.lookAtHeight + 1) : R.ships.lookAtHeight;
      for (let k = 0; k < n; k++) {
        const a = (k / n) * Math.PI * 2;
        await view('ship', `${sh.type}-pad${sh.pad}-ring${k + 1}of${n}`, { x: sh.centre.x + Math.sin(a) * rad, y: .1, z: sh.centre.z - Math.cos(a) * rad }, { x: sh.centre.x, y: ly, z: sh.centre.z }, R.ships.look);
        if (k === 0 && !(await s.safeEv(id => !!cosmos.multiplayer?.fleetView?.views?.get(id) || cosmos.ship?.id === id, sh.id, false))) await sleep(2500);   // the model is built when the player gets near
      }
      // we are next to it now, so its model exists: read the ramps
      let rd = { kind: null, ramps: [] }; const own = await s.safeEv(t => cosmos.ship?.def?.type === t, sh.type, false);
      for (let t = 0; t < (own ? 1 : 4) && !rd.kind; t++) { rd = await s.safeEv(id => window.__spot.ramps(id), sh.id, null) || rd; if (!rd.kind) await sleep(1200); }   // models are built a few at a time
      shipModels.push({ type: sh.type, pad: sh.pad, model: rd.kind || rd.derivedKind });
      if (!rd.kind) s.log(`spots note: model for ${sh.type}@pad${sh.pad} not found (no ramp mesh check)`);
      for (const r of rd.ramps) {
        const tag = `${sh.type}-pad${sh.pad}-${r.key}`; r.lowered = r.lowered || false;
        if (r.lowered && rd.kind) {
          const why = !r.found ? 'no ramp record on the ship model' : !r.mesh ? 'ramp record has no mesh' : !r.tris ? 'ramp mesh has no triangles' : !r.visible ? 'ramp mesh is hidden' : r.opacity < .2 ? 'ramp mesh is almost fully transparent' : null;
          if (why) finding({ kind: 'spot-ramp-no-mesh', sev: 85, title: `Walkable ${r.key} ramp on the ${sh.type} has no visible mesh`, detail: `${tag}: ramp is lowered (walkable) but ${why}. You would float down it.`, key: `spot-ramp-mesh:${sh.type}:${r.key}` });
        }
        if (!r.lowered) { s.log(`spots: ${tag} ramp is raised, no walk views`); continue; }
        if (!r.found || !r.footP) continue;
        if (R.ramps.perType) { const key = sh.type + ':' + r.key; if (rampDone.has(key)) continue; rampDone.add(key); }
        const h = r.hingeP, f = r.footP; let dx = f.x - h.x, dz = f.z - h.z; const m = Math.hypot(dx, dz) || 1; dx /= m; dz /= m;
        s.log(`spots: ${tag} hinge ${[h.x, h.y, h.z].map(v => v.toFixed(1))} foot ${[f.x, f.y, f.z].map(v => v.toFixed(1))} (foot height above ground should be ~0)`);
        const spec = Object.fromEntries(R.ramps.views.map(v => [v.id, v.look]));
        await view('ramp', `${tag}-walking-up`, { x: f.x + dx * 1.5, y: Math.max(f.y, 0) + .05, z: f.z + dz * 1.5 }, { x: h.x, y: h.y + 1.2, z: h.z }, spec.up);
        await view('ramp', `${tag}-walking-down`, { x: h.x - dx * .4, y: h.y + .05, z: h.z - dz * .4 }, { x: f.x + dx * 4, y: Math.max(f.y, 0), z: f.z + dz * 4 }, spec.down);
        await view('ramp', `${tag}-from-bottom-looking-back`, { x: f.x + dx * 7, y: Math.max(f.y, 0) + .05, z: f.z + dz * 7 }, { x: h.x, y: h.y + 1.5, z: h.z }, spec.back);
      }
    }
    if (!ships.length) s.log('spots note: no parked ships found in the world snapshot');

    // ---- signs: close enough to read, and repeated text ------------------------------------------------------------------------
    const signs = [];
    for (const d of data.doors) if (d.ax != null && R.signs.buildingText[d.kind]) { const bs = R.signs.buildingSign; signs.push({ id: `${d.name} sign`, text: R.signs.buildingText[d.kind], x: d.ax, y: bs.y, z: d.az + d.ad / 2 + .05, w: Math.min(d.aw - 1, bs.w), h: bs.h }); }
    signs.push(...R.signs.extra.map(e => ({ ...e })));
    for (const sg of signs) {
      const dist = Math.max(R.signs.closeDistance, Math.min(R.signs.maxDistance, sg.w * R.signs.widthFactor));
      await view('sign', sg.id.replace(/\s+/g, '-'), { x: sg.x, y: .1, z: sg.z + dist }, { x: sg.x, y: sg.y, z: sg.z }, `${R.signs.look} Expected text: "${sg.text}".`);
    }
    if (R.signs.flagRepeatedText) {
      const by = new Map(); for (const sg of signs) { const k = sg.text.toLowerCase(); by.set(k, [...(by.get(k) || []), sg.id]); }
      for (const [text, ids] of by) if (ids.length > 1) finding({ kind: 'spot-repeated-sign-text', sev: ids.length >= 3 ? 55 : 22, title: `Same sign text on ${ids.length} port signs: "${text}"`, detail: ids.join(', '), key: 'spot-sign-repeat:' + text });
    }
    const interior = await s.safeEv(() => window.__spot.interiorSigns(), null, null);
    if (interior) {
      const shows = new Map(); for (const d of interior.doors) shows.set(d.shows, [...(shows.get(d.shows) || []), d.id]);
      const lost = interior.doors.filter(d => d.shows !== d.sign && d.shows === (interior.fallbackIsMedbay ? 'MEDBAY' : '(fallback)'));
      if (lost.length) finding({ kind: 'spot-interior-sign-fallback', sev: 70, title: `${lost.length} door sign(s) inside the ${interior.type} show the wrong text (${interior.fallbackIsMedbay ? 'MEDBAY' : 'fallback'})`, detail: lost.map(d => `${d.id} wants "${d.sign}"`).join('; '), key: 'spot-interior-sign-fallback:' + interior.type });
      for (const [text, ids] of shows) if (ids.length >= 3) finding({ kind: 'spot-repeated-sign-text', sev: 60, title: `Door text "${text}" repeats on ${ids.length} doors inside the ${interior.type}`, detail: ids.join(', '), key: `spot-interior-repeat:${interior.type}:${text}` });
      s.log(`spots: interior door signs (${interior.type}): ` + interior.doors.map(d => `${d.id}=${d.shows}`).join(' '));
    } else s.log('spots note: interior door sign list not reachable (cosmos.ship.layout / signs.uvFor); interior doors need an aboard pass');

    // ---- night: from each pad toward the buildings ----------------------------------------------------------------------------
    const here = await s.safeEv(() => location.href, null, null);
    if (R.night && here && data.pads.length) {
      const nightUrl = new URL(here); nightUrl.searchParams.set('sky', R.night.sky); nightUrl.searchParams.delete('skyshift');
      await s.open(nightUrl.toString()); await s.safeEv(PAGE_HELPERS); await sleep(2500);
      const nk = await s.safeEv(() => cosmos.port?.night ?? null, null, null); s.log(`spots: night level ${nk} after sky=${R.night.sky}`);
      if (nk !== null && nk < .5) finding({ kind: 'spot-night-not-night', sev: 20, title: 'Could not get the port to night for the night views', detail: `port.night = ${nk} after ?sky=${R.night.sky}`, key: 'spot-night-not-night' });
      const targets = data.doors.filter(d => R.night.towardKinds.includes(d.kind) && d.ax != null).map(d => ({ x: d.ax, z: d.az, name: d.name }));
      targets.push({ x: -88, z: 40, name: 'arrivals hall' });
      const sorted = [...data.pads].sort((a, b) => a.x - b.x || a.z - b.z), mx = R.night.maxViews || sorted.length, pickPads = sorted.filter((_, i) => i % Math.ceil(sorted.length / mx) === 0);
      for (const p of pickPads) {
        const t = targets.reduce((b, c) => Math.hypot(c.x - p.x, c.z - p.z) < Math.hypot(b.x - p.x, b.z - p.z) ? c : b, targets[0]);
        const dx = t.x - p.x, dz = t.z - p.z, m = Math.hypot(dx, dz) || 1, off = (p.w || 38) / 2 + 3;
        await view('night', `pad${p.number}-toward-${t.name}-${Math.round(m)}m`, { x: p.x + dx / m * off, y: .1, z: p.z + dz / m * off }, { x: t.x, y: 3, z: t.z }, `${R.night.look} Nearest building: ${t.name}, about ${Math.round(m)} m away.`);
      }
      await s.open(here); await s.safeEv(PAGE_HELPERS); await sleep(1500);   // back to the daytime page for whatever runs next
    }

    s.spotInventory = { ...data, ships: shipModels, signs: signs.length, inside: s.insideSummary }; s.spotRules = rules;
    return `${Object.values(counts).reduce((a, b) => a + b, 0)} spot shots (${Object.entries(counts).map(([k, v]) => `${k} ${v}`).join(', ')}); ${data.overlaps.length} door overlaps; ${ships.length} ships.`;
  };
}
