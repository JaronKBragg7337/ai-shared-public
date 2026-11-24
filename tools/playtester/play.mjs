#!/usr/bin/env node
// The Cosmos AI playtester.   node tools/playtester/play.mjs [--minutes 20]
//   --target world2      run the World 2 playtester (default: cosmos)
//   --three-dir PATH     World 2 only: substitute a local Three.js package for the CDN version
//
//   --minutes N          how long the iPhone run plays (default 30)
//   --desktop-minutes N  how long the desktop run plays (default 7; 0 = skip desktop)
//   --only phone|desktop run just one
//   --url URL            site to test (default the live game, as a ?qa=1 test client)
//   --no-vision          skip the screenshot review by the vision model
//   --vision-cap USD     spend cap for the vision pass (default 1)
//   --phases a,b,c       dev: run only these phases (opening,panels,tour,lifeboat,hire,dig,fly,rover,spots,freeplay, plus the QA ones)
//   --phases qa          shorthand for all the QA-practice phases (smoke,a11y,spam,lifecycle,network,economy,edges,perf,monkey,idle,softlock); see PRACTICES.md
//   --no-qa              leave the QA-practice phases out of the default run
//   --desktop-opening    play the whole opening on the desktop run too (by default a desktop run under 11 minutes starts from the review start, because the opening alone takes about 10)
//   --skip-opening       dev: start from the review start instead of playing the opening
//   --solo, --teleport x,z   dev: offline local world, optionally start at a port position
//   --start WORLD [--side FACTION]   which start world to pick on the arrivals board (default mars; e.g. --start earth --side skyward)
// Output: state/playtest/<date-time>/REPORT.md plus screenshots, and one line appended to state/timeline.md.
import { mkdirSync, appendFileSync, readFileSync, writeFileSync } from 'node:fs';
import { join, dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { Session, sleep, fortWayne } from './lib/core.mjs';
import { makePhases } from './lib/phases.mjs';
import { addWorldPhases } from './lib/world.mjs';
import { Walker } from './lib/nav.mjs';
import { visionReview } from './lib/vision.mjs';
import { buildReport } from './lib/report.mjs';
import { addSpotsPhase } from './lib/spots.mjs';
import { addQaPhases, QA_PHASES } from './lib/qa.mjs';

const here = dirname(fileURLToPath(import.meta.url)); const SHARED = resolve(here, '..', '..');
const argv = process.argv.slice(2); const flag = n => argv.includes('--' + n); const val = (n, d) => { const i = argv.indexOf('--' + n); return i >= 0 && argv[i + 1] && !argv[i + 1].startsWith('--') ? argv[i + 1] : d; };
const target = val('target', 'cosmos');
if (!['cosmos', 'world2'].includes(target)) throw new Error('Unknown target: ' + target);
if (target === 'world2') {
  const { runWorld2 } = await import('./lib/world2.mjs');
  await runWorld2({ argv, shared: SHARED });
} else {
const args = { minutes: Number(val('minutes', 30)), desktopMinutes: Number(val('desktop-minutes', 7)), only: val('only', 'both'), url: val('url', 'https://www.heartbeatobservatory.com/games/the-cosmos/'), vision: !flag('no-vision'), visionCap: Number(val('vision-cap', 1)), phases: val('phases', ''), skipOpening: flag('skip-opening'), noQa: flag('no-qa'), desktopOpening: flag('desktop-opening'), solo: flag('solo'), teleport: val('teleport', '') };
const startedAt = new Date(); const stamp = (() => { const f = fortWayne(startedAt); return f.date + '_' + f.hm.replace(':', '-'); })();   // local (Fort Wayne) time, not UTC
const outDir = val('out', join(SHARED, 'state', 'playtest', stamp)); mkdirSync(outDir, { recursive: true });
const withQuery = (u, extra) => u + (u.includes('?') ? '&' : '?') + extra;
const playUrl = (extra = '') => withQuery(args.url, 'qa=1&dev=1' + extra);

// ---- the background watcher: stuck, falling, missing people, frame times, messages ----------------------------------------
async function monitor(s, stop) {
  let busySince = 0, lastLayout = 0, lastFrames = 0, lastPeople = 0, lastSig = '', lastChange = Date.now(), fallStrikes = 0, stackedDone = false;
  while (!stop.v) {
    await sleep(2500); if (stop.v) break;
    try {
      const st = await s.state(); if (st.nocosmos) continue;
      const sig = JSON.stringify([st.pos && [Math.round(st.pos.x / .5), Math.round(st.pos.z / .5), Math.round(st.pos.y)], st.stage, st.actionLabel, st.caption, st.trip && [st.trip.phase, Math.round(st.trip.dist / 500)], st.marks, st.aboard, st.seat, st.landed, st.onMoon, st.cart, st.toast]);
      // ROUND7: "pending" is only stuck if no answer came back for the whole window: the opening saves its pose one request after another, so the flag can stay on while the server is just slow
      if (st.pending) { const nc = await s.netCounts(); if (nc.rec !== (monitor.lastRec ?? -1)) { monitor.lastRec = nc.rec; busySince = Date.now(); } busySince = busySince || Date.now(); if (Date.now() - busySince > 25000) { s.finding({ kind: 'server-not-answering', sev: 97, title: 'A game action stays "pending" forever (the server never answers), so the buttons are dead', detail: `in the opening step ${st.stage}: the game's own busy flag has been on for ${Math.round((Date.now() - busySince) / 1000)} s; button text "${st.actionLabel}", caption "${st.caption}"`, key: 'pending-forever:' + st.stage }); busySince = Date.now() + 60000; } } else busySince = 0;
      if (sig !== lastSig) { lastSig = sig; lastChange = Date.now(); }
      else if (Date.now() - lastChange > (st.trip ? 150000 : 60000) && !stop.paused) { s.finding({ kind: 'stuck-state', sev: 86, title: 'Nothing changed for 60+ seconds (same message, same place)', detail: `in "${s.phase}": position ${JSON.stringify(st.pos)}, button "${st.actionLabel}", caption "${st.caption}", toast "${st.toast}", ship ${st.aboard ? 'aboard' : 'outside'}${st.trip ? ', trip ' + st.trip.phase : ''}`, key: 'stuck:' + s.phase }); lastChange = Date.now(); }
      s.samples.push({ t: s.now(), phase: s.phase, pos: st.pos, frame: st.frame });
      // falling through the ground / out of the ship
      const fall = await s.safeEv(() => { const c = cosmos; if (c.opening?.active) return null;
        if (c.ship.aboard) { const b = c.ship.def.dock.bounds; const y = c.ship.sw.y; return y < b.y0 - 2 ? { why: 'aboard but below the hull (ship-local y ' + y.toFixed(1) + ')' } : null; }
        const w = c.walker.worldPos, r = Math.hypot(w.x, w.y, w.z); if (c.space?.onMoon) return null; const g = c.ship.ground(w.x / r, w.y / r, w.z / r); const gap = r - g;
        const p = c.port.site.toLocal(w); const inTower = p.x > -68 && p.x < -52 && p.z > -47 && p.z < -30;
        if (gap < -1.5 && !inTower && !c.vehicles?.seated?.()) return { why: `${(-gap).toFixed(1)} m below the ground surface at port ${p.x.toFixed(0)},${p.z.toFixed(0)}` }; return null; }, null, null);
      if (fall) { fallStrikes++; if (fallStrikes >= 2) { s.finding({ kind: 'fell-through', sev: 92, title: 'Player fell through the ground or out of the ship', detail: fall.why + ' during ' + (s.trail[s.trail.length - 1] || ''), key: 'fell:' + s.phase }); } } else fallStrikes = 0;
      // moons-fix: walking on a moon must keep the boots down; airborne for 8+ s in a row is "floated away" (Jaron, Phobos, 10/3)
      const air = await s.safeEv(() => { const c = cosmos; if (c.opening?.active || c.ship.aboard || !c.space?.onMoon) return null; const w = c.walker, p = w.worldPos, r = Math.hypot(p.x, p.y, p.z), dx = p.x / r, dy = p.y / r, dz = p.z / r; const gs = w.groundSampler ? w.groundSampler(dx, dy, dz, r) : 'nosampler'; const gd = w.worldPos && c.ship.ground ? c.ship.ground(dx, dy, dz) : null; const vr = (w.velocity.x * dx + w.velocity.y * dy + w.velocity.z * dz);
  return { grounded: !!w.grounded, alt: Math.round(Math.hypot(w.velocity.x, w.velocity.y, w.velocity.z) * 100) / 100, dbg: { r: +r.toFixed(2), sampler: typeof gs === 'number' ? +(r - gs).toFixed(3) : gs, shipGround: typeof gd === 'number' ? +(r - gd).toFixed(3) : gd, vRad: +vr.toFixed(3), suitHold: w.suitHoldAccel, jump: w.jumpSpeed } }; }, null, null);
      if (air && !air.grounded && !s._airTraceOn && Date.now() - (s._airSince || Date.now()) > 3000) { s._airTraceOn = true; await s.safeEv(() => { const w = cosmos.walker; if (w.__wrapped) return; w.__wrapped = true; window.__air = []; const t = w.tick.bind(w); w.tick = (dt, inp) => { const r0 = Math.hypot(w.worldPos.x, w.worldPos.y, w.worldPos.z), gr0 = w.groundSampler ? w.groundSampler(w.worldPos.x / r0, w.worldPos.y / r0, w.worldPos.z / r0, r0) : null; const gb = w.grounded; t(dt, inp); const r = Math.hypot(w.worldPos.x, w.worldPos.y, w.worldPos.z); if (window.__air.length < 90) { const ux = w.worldPos.x / r, uy = w.worldPos.y / r, uz = w.worldPos.z / r; window.__air.push([gb ? 1 : 0, w.grounded ? 1 : 0, gr0 === null ? 'n' : +(r0 - gr0).toFixed(3), +(w.velocity.x * ux + w.velocity.y * uy + w.velocity.z * uz).toFixed(3), inp && (inp.moveNorth || inp.moveEast) ? 1 : 0, w.lastPushOutM ? +w.lastPushOutM.toFixed(2) : 0]); } }; }); }
      if (air && !air.grounded) { s._airSince = s._airSince || Date.now(); if (Date.now() - s._airSince > 8000) s.finding({ kind: 'floating-on-moon', sev: 90, title: 'Floating off the ground on a moon (airborne for 8+ seconds)', detail: `walking on the moon, still airborne after ${Math.round((Date.now() - s._airSince) / 1000)} s, speed ${air.alt} m/s ${JSON.stringify(air.dbg)}`, key: 'floating-moon' }); if (s._airTraceOn && !s._airDumped) { const tr = await s.safeEv(() => window.__air, null, null); if (tr && tr.length >= 60) { s._airDumped = true; s.log('AIRTRACE [grounded-before, grounded-after, dist-to-drawn-ground, radial-vel, moving, pushOut]: ' + JSON.stringify(tr.slice(0, 40))); } } } else s._airSince = 0;
      await s.watchMessages();
      if (Date.now() - lastFrames > 12000) { lastFrames = Date.now(); await s.frameStats(); }
      if (Date.now() - (monitor.lastHealth || 0) > 20000) { monitor.lastHealth = Date.now(); await s.health(); }
      if (Date.now() - lastLayout > 30000) { lastLayout = Date.now(); await s.layoutAudit(); }
      if (Date.now() - lastPeople > 10000) { lastPeople = Date.now();
        const pr = await s.safeEv(() => { const c = cosmos, cam = c.engine.camera; if (c.opening?.active) return null; const out = { missing: [], stacked: [] }; const V = cam.position.constructor;
          const all = [...c.portPeople.members.map(m => ({ id: m.id, name: m.name || m.def?.title, person: m.person, kind: 'port worker' })), ...[...c.crew.members.values()].map(m => ({ id: m.id, name: m.name, person: m.person, kind: m.status, m }))];
          const pts = [];
          for (const a of all) { const g = a.person?.group; if (!g || !g.parent) continue; const v = g.getWorldPosition(new V()); const d = v.distanceTo(cam.position);
            const n = v.clone().project(cam); const inView = n.z < 1 && Math.abs(n.x) < .9 && Math.abs(n.y) < .9; if (inView && d < 14 && (!g.visible || !a.person.loaded)) out.missing.push(`${a.name || a.id} (${a.kind}) ${Math.round(d)} m away: ${!g.visible ? 'hidden' : 'model not loaded'}`);
            if (a.kind === 'candidate' || a.kind === 'port worker') pts.push({ n: a.name || a.id, x: v.x, y: v.y, z: v.z, g }); }
          for (let i = 0; i < pts.length; i++) for (let j = i + 1; j < pts.length; j++) if (Math.hypot(pts[i].x - pts[j].x, pts[i].y - pts[j].y, pts[i].z - pts[j].z) < .3 && pts[i].g.visible && pts[j].g.visible) out.stacked.push(`${pts[i].n} and ${pts[j].n}`);
          return out; }, null, null);
        if (pr) { for (const m of pr.missing.slice(0, 3)) s.finding({ kind: 'person-not-drawn', sev: 66, title: 'A person who should be visible is not drawn: ' + m.split(' (')[0], detail: m, key: 'notdrawn:' + m.split(' (')[0] });
          if (pr.stacked.length) s.finding({ kind: 'people-stacked', sev: 52, title: `People standing exactly on top of each other (${pr.stacked.length} pairs)`, detail: pr.stacked.slice(0, 4).join('; '), key: 'stacked' }); }
      }
    } catch (e) { /* the page may be reloading; try again */ }
  }
}

// refresh in the middle of something, then check the game put us back
async function refreshCheck(s, why) {
  const before = await s.state(); if (before.nocosmos || before.opening) return;
  await s.stickUp(); await s.shot('before-refresh'); await s.reload(why); await sleep(2500); await s.safeEv(() => cosmos.engine.frameCount); const after = await s.state();
  if (after.nocosmos) { s.finding({ kind: 'refresh-broke', sev: 92, title: 'After a refresh the game did not come back', detail: why, key: 'refresh-broke' }); return; }
  const d = before.pos && after.pos && before.frame === after.frame ? Math.hypot(before.pos.x - after.pos.x, before.pos.z - after.pos.z) : null;
  s.log(`refresh check: moved ${d === null ? '?' : d.toFixed(1)} m, marks ${before.marks} -> ${after.marks}, aboard ${before.aboard} -> ${after.aboard}`);
  if (d !== null && d > 15) s.finding({ kind: 'refresh-moved', sev: 70, title: 'After a refresh the player was somewhere else', detail: `${why}: was at ${JSON.stringify(before.pos)} (${before.frame}), came back at ${JSON.stringify(after.pos)} (${after.frame}), ${Math.round(d)} m apart`, key: 'refresh-moved:' + s.phase });
  if (before.marks != null && after.marks != null && before.marks !== after.marks) s.finding({ kind: 'refresh-money', sev: 80, title: 'Money changed across a refresh', detail: `${why}: marks ${before.marks} -> ${after.marks}`, key: 'refresh-money' });
  if (before.aboard !== after.aboard) s.finding({ kind: 'refresh-aboard', sev: 72, title: 'A refresh changed whether the player is aboard the ship', detail: `${why}: aboard ${before.aboard} -> ${after.aboard}`, key: 'refresh-aboard' });
  await s.shot('after-refresh');
}

async function runSession(profileKey, minutes, only) {
  const s = new Session({ profileKey, outDir, url: args.url }); s.cover = {}; s.t0 = Date.now(); s.deadline = Date.now() + minutes * 60000;
  const stop = { v: false, paused: false };
  let monitorP = null, P = null;
  try {
    await s.launch();
    const shortDesktop = profileKey === 'desktop' && !args.phases && !args.desktopOpening && !args.skipOpening && minutes < 11;   // the opening alone takes about 10 minutes
    s.phase = 'start'; s.stop = stop; const tLoad = Date.now(); await s.open(playUrl(((args.skipOpening || shortDesktop) ? '&opening=off' : '') + (args.solo ? '&solo=1' : '')));
    if (args.teleport) { const [tx, tz] = args.teleport.split(',').map(Number); await sleep(4000); await s.safeEv(({ tx, tz }) => { const w = cosmos.walker, t = cosmos.port.site.toWorld(tx, .5, tz); w.worldPos.x = t.x; w.worldPos.y = t.y; w.worldPos.z = t.z; w.velocity = { x: 0, y: 0, z: 0 }; }, { tx, tz }); s.log('teleported (dev) to ' + args.teleport); } s.loadMs = Date.now() - tLoad; s.perf = s.perf || {}; s.perf.firstLoad = await s.loadStats(); await s.shot('loaded'); s.buildId = await s.safeEv(() => cosmos.buildId, null, null);
    monitorP = monitor(s, stop);
    const startW = (shortDesktop || args.skipOpening) ? 'mars' : val('start', 'mars');   // the review start is always Mars
    P = makePhases(s, { fallbackOpening: true, start: startW, side: val('side', '') }); const W = new Walker(s); addWorldPhases(P, s, { start: startW }, W, { tapExpectChange: P.tapExpectChange }); addSpotsPhase(P, s); addQaPhases(P, s, W);
    const QA = args.noQa ? [] : QA_PHASES;
    const full = ['opening', 'panels', 'tour', 'lifeboat', 'smoke', 'a11y', 'lifecycle', 'network', 'spam', 'economy', 'edges', 'hire', 'dig', 'fly', 'rover', 'spots', 'perf', 'monkey', 'idle', 'softlock', 'freeplay'].filter(x => !QA_PHASES.includes(x) || QA.includes(x));
    const deskList = ['opening', 'panels', 'smoke', 'a11y', 'spam', 'lifecycle', 'network', 'perf', 'monkey', 'edges', 'tour', 'lifeboat', 'economy', 'hire', 'dig', 'idle', 'softlock', 'freeplay'].filter(x => !QA_PHASES.includes(x) || QA.includes(x));   // desktop budgets are short: the cheap QA checks first, the long walks after
    let list = args.phases ? args.phases.split(',').flatMap(x => x === 'qa' ? QA_PHASES : [x]) : (profileKey === 'desktop' ? deskList : full);
    if (shortDesktop) { s.log(`desktop budget is ${minutes} min and the opening alone takes about 10: started from the review start (use --desktop-opening to play it)`); list = list.filter(x => x !== 'opening'); }
    if (args.skipOpening) list = list.filter(x => x !== 'opening');
    if (!args.phases && startW !== 'mars') list = list.filter(x => x !== 'spots' && x !== 'rover');   // the trouble-spot sweep and the survey rover are Marineris Port / Meridian things
    let refreshed = 0;
    for (const name of list) {
      if (s.overTime(name === 'freeplay' ? 0 : 0.5) && name !== 'opening') { s.phaseResults.push({ name, status: 'skipped (out of time)', sec: 0 }); continue; }
      s.phase = name; const t0 = Date.now(); let status = 'done', note = '';
      s.log(`=== phase ${name} starts`);
      try {
        const r = await P[name](); if (typeof r === 'string') note = r; if (r === 'bypass') { await s.open(playUrl('&opening=off')); s.phase = 'opening-bypass'; }
      } catch (e) { status = 'bot error'; note = String(e.message || e).slice(0, 140); s.log('PHASE ERROR ' + (e.stack || e).toString().split('\n').slice(0, 3).join(' | ')); s.botErrors = (s.botErrors || 0) + 1;
        if (/Target closed|has been closed|crash/i.test(note)) { s.finding({ kind: 'browser-died', sev: 95, title: 'The browser tab died during ' + name, detail: note, key: 'died:' + name }); } }
      await s.stickUp(); await s.watchMessages(); await s.frameStats(); await s.health(); await s.shot('end-of-' + name);
      s.phaseResults.push({ name, status, note, sec: (Date.now() - t0) / 1000 });
      if (name === 'tour' && !refreshed) { refreshed++; await refreshCheck(s, 'refresh after the port tour'); }
      if (name === 'dig') await refreshCheck(s, 'refresh right after digging');
      s.cover.panels = s.cover.panels || []; if (name === 'panels') s.cover.panels = ['Settings', 'Account', 'World / crew', 'Controls'];
      if (/Ctrl|quota/.test(note)) break;
    }
  } catch (e) { s.log('SESSION ERROR ' + (e.stack || e)); s.finding({ kind: 'harness', sev: 10, title: 'Bot harness error: ' + String(e.message || e).slice(0, 80), detail: String(e.stack || e).slice(0, 300), key: 'harness:' + String(e.message).slice(0, 40) }); }
  finally {
    stop.v = true; await sleep(300); try { await Promise.race([monitorP, sleep(5000)]); } catch {}
    try { s.videoPath = await s.page.video().path(); } catch {}
    try { const h = (s.healthLog || []).filter(x => x.t > 60); if (h.length >= 6) { const a = h[Math.floor(h.length * .15)], b = h[h.length - 1];
      for (const [k, minGrow, label] of [['geometries', 150, 'graphics shapes (geometries)'], ['textures', 60, 'textures'], ['heapMB', 80, 'JS memory (MB)']]) if (a[k] != null && b[k] != null && b[k] > a[k] * 1.6 && b[k] - a[k] > minGrow) s.finding({ kind: 'memory-growth', sev: 30, title: `${label} grew from ${a[k]} to ${b[k]} over the run (new areas loading, or a leak)`, detail: `samples ${h.length}; phases ${a.phase} -> ${b.phase}. Only a leak if it keeps climbing while standing still: the idle check measures that.`, key: 'leak:' + k, shot: false }); } } catch {}
    s.talkedCount = P ? P.ctx.talked.size : 0; s.hiredCount = P ? P.ctx.hired.length : 0; s.endedAt = Date.now();
    try { s.buildId = s.buildId || await s.safeEv(() => cosmos.buildId, null, null); } catch {}
    await s.close();
  }
  return s;
}

console.log(`Playtest -> ${outDir}`);
const sessions = [];
if (args.only !== 'desktop') sessions.push(await runSession('iphone', args.minutes, args));
if (args.only !== 'phone' && args.desktopMinutes > 0) sessions.push(await runSession('desktop', args.desktopMinutes, args));
let vision = null;
if (args.vision) vision = await visionReview({ sessions, capUsd: args.visionCap, log: m => console.log(m) });
const buildId = sessions.map(s => s.buildId).find(Boolean);
const rep = buildReport({ sessions, vision, outDir, args, buildId, startedAt });
const worst = rep.top.slice(0, 3).map(f => f.title.replace(/\s+/g, ' ').slice(0, 70)).join('; ');
const mins = Math.round(sessions.reduce((a, s) => a + (s.endedAt - s.t0), 0) / 60000);
const line = `- ${fortWayne().date} ${fortWayne().hm}: Cosmos AI playtest (${mins} min, ${sessions.length} device runs): ${rep.list.length} problems (${rep.block.length} blockers, ${rep.serious.length} serious). Worst: ${worst || 'none'}. Report: state/playtest/${stamp}/REPORT.md`;
try { if (!val('out', '')) appendFileSync(join(SHARED, 'state', 'timeline.md'), '\n' + line + '\n'); } catch (e) { console.log('could not append to timeline: ' + e.message); }
console.log('\n' + line); console.log('REPORT: ' + join(outDir, 'REPORT.md'));
}
