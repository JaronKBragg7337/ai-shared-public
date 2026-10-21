// phases.mjs - the things a player does, in the order a player does them. Each phase is allowed to fail: a failure is a finding.
import { sleep, rnd, pick } from './core.mjs';
import { Walker, STEER } from './nav.mjs';

const wait = (ms) => sleep(ms);
const chance = p => Math.random() < p;

/** A sig of what the screen is showing, to tell whether a tap changed anything. */
export const UI_SIG = () => {
  const out = [];
  for (const e of document.querySelectorAll('body *')) {
    const cs = getComputedStyle(e); if (cs.display === 'none' || cs.visibility === 'hidden') continue;
    if (!(cs.position === 'fixed' || cs.position === 'absolute')) continue; const r = e.getBoundingClientRect(); if (r.width < 8 || r.height < 8) continue;
    if (e.tagName === 'CANVAS') continue; const t = (e.innerText || '').trim().replace(/\s+/g, ' ');
    if (!t && !/BUTTON/.test(e.tagName)) continue;
    out.push((e.id || e.className.toString().slice(0, 14) || e.tagName) + '|' + Math.round(r.left / 4) + ',' + Math.round(r.top / 4) + ',' + Math.round(r.width / 4) + '|' + t.slice(0, 36));
  }
  const c = window.cosmos; if (c) { try { out.push('aboard' + c.ship.aboard + 'seat' + (c.ship.seat?.id || '') + 'm' + (c.world?.state?.economy?.marks) + 'st' + (c.opening?.active ? c.opening.state.stage : 'x')); } catch {} }
  return out.sort().join('\n');
};

export function makePhases(s, opts) {
  const W = new Walker(s);
  const P = {};
  const ctx = { talked: new Set(), hired: [], questAccepted: false, dug: 0 };
  P.ctx = ctx;

  // ---------------------------------------------------------------------------------------------------------------
  async function tapExpectChange(sel, why, { miss = 0.15, waitMs = 3000, allowSame = false, text = null, scope = null } = {}) {
    const before = await s.safeEv(UI_SIG, null, ''); const t0 = Date.now(); const n0 = await s.netCounts();
    const ok = text ? await s.tapText(text, scope, { why }) : await s.tap(sel, { miss, why });
    if (!ok) return null; let changed = false, lat = 0;
    for (let i = 0; i < waitMs / 90; i++) { await wait(90); const after = await s.safeEv(UI_SIG, null, before); if (after !== before) { changed = true; lat = Date.now() - t0; break; } }
    const nm = text ? text.source : sel;
    // ROUND7: a tap that sent something to the shared world is not "dead" until the world has answered: wait for the reply, then look again.
    const n1 = await s.netCounts(); const sent = n1.req > n0.req;
    if (!changed && sent) { const st = await s.settle(12000); await wait(250); const after = await s.safeEv(UI_SIG, null, before); if (after !== before) { changed = true; lat = Date.now() - t0; }
      const n2 = await s.netCounts(); if (!changed && n2.rec > n0.rec) { s.log(`${nm}: the world answered (${n2.refused > n0.refused ? 'refused' : 'accepted'}) but the screen looks the same`); changed = true; lat = Date.now() - t0; }
      else if (!changed && st.pending) s.finding({ kind: 'server-no-reply', sev: 82, title: `Tapping ${nm} sent a request the server never answered`, detail: `${why}: ${st.pending} request(s) still unanswered after ${Math.round(st.waited / 1000)} s`, key: 'noreply:' + nm + ':' + s.phase }); }
    if (!changed && !allowSame && !sent) { await wait(2000); const after = await s.safeEv(UI_SIG, null, before); if (after !== before) { changed = true; lat = Date.now() - t0; } }
    if (!changed && !allowSame && !(sent && (await s.netCounts()).rec > n0.rec)) { if (!s.findings?.has?.('noreply:' + nm + ':' + s.phase)) s.finding({ kind: 'no-response', sev: 74, title: `Tapping ${nm} did nothing visible`, detail: `${why}: nothing on screen changed ${Math.round((Date.now() - t0) / 1000)} s after the tap${sent ? ' (the request was sent but never answered)' : ' and nothing was sent to the world'}`, key: 'noresp:' + nm + ':' + s.phase }); }
    else if (changed && lat > 1500) s.finding({ kind: 'slow-button', sev: lat > 4000 ? 66 : 44, title: `Slow button: ${nm} took ${(lat / 1000).toFixed(1)} s to respond`, detail: why, key: 'slow:' + nm });
    if (changed) { (s.latencies = s.latencies || []).push(lat); }
    return changed;
  }
  P.tapExpectChange = tapExpectChange;

  async function postStep(label) { await s.watchMessages(); await s.frameStats(); await s.shot(label); }

  // ---------------------------------------------------------------------------------------------------------------
  // OPENING (rebuilt 10/3, 7 steps): 0 wake aboard the liner Hellas Dawn (about 200 s of flight, then walk off by the starboard gangway),
  // 1 the port (arrivals hall world board, then the Kestrel gate), 2 the Kestrel flight (scripted, ~1 min), 3 the wreck (locker, climb out),
  // 4 dig the crate, 5 wait for the driver, 6 ride to the port. The liner takes ~3.3 minutes by itself: that is NOT stuck.
  // ---------------------------------------------------------------------------------------------------------------
  P.opening = async () => {
    const t0 = Date.now(); let refreshedDig = false, refreshedRide = false, lastStage = -1, stageSince = Date.now(), lastShot = 0, digTaps = 0, stuckRefresh = 0, lastClock = -1, clockMoved = Date.now();
    const done = { liner: false, board: false, locker: false, landedAt: 0 };
    const STAGE_LIMIT = { 0: 330, 1: 240, 2: 150, 3: 180, 4: 240, 5: 90, 6: 160 };
    if (!await s.safeEv(() => !!(window.cosmos?.opening?.active), null, false)) { s.log('opening is not active for this player (returning save?)'); return 'no opening'; }
    const walkAll = async (frame, pts, label, o = {}) => { const stg = lastStage; const gone = async () => { const q = await s.state(); return !q.opening || q.stage !== stg; }; // stop walking the moment the step changes (the gangway ends the liner step mid-walk)
      for (const [x, z] of pts) { if (!await W.to(frame, x, z, { r: o.r || 1.0, timeout: o.timeout || 60, label, wander: false, quickCheck: gone })) return false; if (await gone()) return true; } return true; };
    for (;;) {
      if (Date.now() - t0 > 14 * 60 * 1000) { s.finding({ kind: 'opening-timeout', sev: 98, title: 'The opening never finished (14 minutes)', detail: 'The bot followed the on-screen prompts for fourteen minutes and still was not at the port.', key: 'opening-timeout' }); return 'timeout'; }
      const st = await s.state();
      if (st.nocosmos) { await wait(1000); continue; }
      if (!st.opening) { s.log('opening finished'); await wait(2500); await s.shot('opening-done'); return 'done'; }
      if (st.stage !== lastStage) { s.log(`opening stage ${lastStage} -> ${st.stage} (${st.caption || st.hint})`); lastStage = st.stage; stageSince = Date.now(); await s.shot('stage-' + st.stage); await s.layoutAudit('opening stage ' + st.stage); }
      // the liner flight is a clock: only a clock that stopped moving (or a landed ship nobody can leave) is stuck
      if (st.stage === 0) { if (st.openingClock !== lastClock) { lastClock = st.openingClock; clockMoved = Date.now(); } if (st.openingClock >= 197 && !done.landedAt) done.landedAt = Date.now(); }
      const stalled = st.stage === 0 ? (Date.now() - clockMoved > 60000 || (done.landedAt && Date.now() - done.landedAt > 120000)) : Date.now() - stageSince > (STAGE_LIMIT[st.stage] || 150) * 1000;
      if (stalled) {
        const why = await s.safeEv(() => { const o = cosmos.opening; return { busy: o.busy, status: o.status, actionPending: o.actionPending, active: o.active, stage: o.state.stage, clock: o.clock, held: cosmos.touch?.active, label: document.getElementById('opening-action')?.textContent }; }, null, null);
        s.finding({ kind: 'stuck-stage', sev: 97, title: `The opening is stuck at step ${st.stage}`, detail: `no progress for ${Math.round((Date.now() - stageSince) / 1000)} s. caption: "${st.caption}", hint: "${st.hint}", button: "${st.actionLabel}", position ${JSON.stringify(st.pos)}, the game's own view: ${JSON.stringify(why)}`, key: 'opening-stuck:' + st.stage });
        if (stuckRefresh < 2) { stuckRefresh++; await s.reload('opening stuck, trying a refresh'); }
        else if (opts.fallbackOpening) { s.log('opening is blocked: bypassing with opening=off so the rest of the game can still be tested'); s.finding({ kind: 'opening-bypassed', sev: 99, title: 'The opening could not be finished, so the bot had to bypass it', detail: 'After two refreshes the opening still would not move on. The rest of the run used the review start (?opening=off).', key: 'opening-bypassed' }); return 'bypass'; }
        stageSince = Date.now() + 20000; clockMoved = Date.now() + 20000; done.landedAt = done.landedAt ? Date.now() + 20000 : 0;
      }
      if (Date.now() - lastShot > 15000) { lastShot = Date.now(); await postStep('opening'); }
      switch (st.stage) {
        case 0: { // the liner: look around, then walk the real way out: lounge -> promenade -> boarding hall -> gangway
          if (/Tap the screen/i.test(st.hint) && (done.unlock = (done.unlock || 0) + 1) <= 2) { await s.tapXY(rnd(100, 300), rnd(300, 500)); s.log('tap screen to unlock sound'); }
          if (!done.liner) {
            if (st.openingClock < 25) { if (chance(.5)) await s.lookDrag(rnd(-120, 120), rnd(-25, 25)); await wait(rnd(2500, 4000)); break; }
            if (!await walkAll('opening-liner', [[4.6, 5.3], [1.9, 5.3], [1.9, 26.7], [8, 26.7]], 'the boarding hall', { timeout: 70 })) { await wait(1500); break; }
            done.liner = true; s.log('in the boarding hall, waiting for the gangway to come down'); }
          if (st.openingClock < 197 || !/Welcome to Marineris/i.test(st.hint)) { if (chance(.25)) await s.lookDrag(rnd(-120, 120), rnd(-15, 15)); await wait(rnd(2500, 4500)); break; }
          await walkAll('opening-liner', [[13.3, 26.7], [18, 26.7], [22.5, 26.7]], 'down the gangway', { timeout: 60, r: .8 }); await wait(1500); break; }
        case 1: { // the port: walk the lit way to the arrivals hall, read the board, pick a world, then to the Kestrel gate
          if (!done.board) {
            if (!/board/i.test(st.actionLabel || '')) { if (!await walkAll('opening', [[-150, 31.7], [-120, 36], [-103, 40], [-96, 42], [-88, 44.5]], 'the arrivals hall board', { timeout: 90, r: 1.6 })) { await wait(1000); break; } await wait(600); break; }
            await s.stickDown(); await wait(300); await s.stickUp();
            if (!await s.action({ miss: .1 })) { await wait(800); break; }
            if (!await s.safeEv(async () => { for (let i = 0; i < 60; i++) { if (document.querySelector('#opening-board')) return true; await new Promise(r => setTimeout(r, 150)); } return false; }, null, false)) { s.finding({ kind: 'board-not-open', sev: 85, title: 'Tapping "Read the board" did not open the world board', detail: 'the arrivals hall board never appeared', key: 'board-not-open' }); await wait(1500); break; }
            await s.shot('world-board'); await wait(rnd(800, 1800));
            const startW = opts?.start || 'mars';
            if (startW !== 'mars') {   // pick another start world (and side) the way a person taps the board tabs
              if (!await s.tap(`[data-w="${startW}"]`, { why: `pick the ${startW} tab on the world board` })) { s.finding({ kind: 'board-no-world', sev: 85, title: `The world board has no ${startW} tab`, detail: 'could not tap the start world tab' }); }
              await wait(1200); await s.shot(`world-board-${startW}`);
              if (opts?.side) { await s.safeEv((f) => document.querySelector(`[data-f="${f}"]`)?.scrollIntoView({ block: 'center' }), opts.side); await wait(400); await s.tap(`[data-f="${opts.side}"]`, { why: `pick ${opts.side}` }); await wait(800); }
            }
            await s.safeEv(() => document.querySelector('[data-act="go"]')?.scrollIntoView({ block: 'center' })); await wait(500); // the board scrolls: a person swipes up to the button
            await s.shot('world-board-go');
            if (!await s.tap('[data-act="go"]', { why: 'fly from the world board' })) { s.finding({ kind: 'board-no-go', sev: 85, title: 'The world board has no Go button on screen', detail: 'could not tap the button that sends the Kestrel off', key: 'board-no-go' }); await wait(1500); break; }
            await s.settle(12000); await wait(1200); done.board = true; break; }
          if (!/Kestrel/i.test(st.actionLabel || '')) { if (!await walkAll('opening', [[-60, 38], [-30, 38], [-6, 38], [19, 38], [19.5, 22], [18.8, 12]], 'the Kestrel gate', { timeout: 120, r: 2.2 })) { await wait(1000); break; } await wait(600); break; }
          await s.stickDown(); await wait(300); await s.stickUp(); await s.action({ miss: .1 }); await wait(1500); break; }
        case 2: { // the Kestrel flight is scripted: sit through it, look out of the window now and then
          if (chance(.3)) await s.lookDrag(rnd(-100, 100), rnd(-15, 15)); await wait(rnd(2500, 4000)); break; }
        case 3: { // the wreck: the crew locker, then climb out
          const lbl = st.actionLabel || '';
          if (!done.locker) {
            if (!/locker/i.test(lbl)) { if (!await walkAll('opening-cabin', [[1.2, 6.8]], 'the crew locker', { timeout: 40, r: 1.3 })) { await wait(1000); break; } await wait(600); break; }
            await s.action({ miss: .1 }); await wait(1200);
            if (await s.safeEv(() => !!document.querySelector('#opening-note button'), null, false)) { await s.shot('locker-note'); await wait(1500); await s.tap('#opening-note button', { why: 'close the locker note' }); done.locker = true; }
            else s.finding({ kind: 'locker-no-note', sev: 70, title: 'Using the crew locker showed no note', detail: 'no #opening-note appeared after tapping the locker button', key: 'locker-no-note' });
            await wait(800); break; }
          if (!/climb/i.test(lbl)) { await walkAll('opening-cabin', [[0, 11], [0, 13.4]], 'the cabin exit', { timeout: 40, r: 1.0 }); await wait(500); break; }
          await s.stickDown(); await wait(400); await s.stickUp(); await s.action({ miss: .15 }); await wait(1500); break; }
        case 4: { // dig out the crate
          await s.stickUp();
          const pos = st.pos || { x: 0, z: 0 };
          if (Math.hypot(pos.x - 4, pos.z - 20) > 4.2) { await W.to('opening', 4, 18.5, { r: 1.2, timeout: 60, label: 'the crate', pitch: -.2 }); break; }
          if (chance(.5)) await s.stickDown(); // sometimes hold the thumb while digging
          await s.safeEv(({ x, z }) => { const m = cosmos.opening.model, w = m.walker, e = w.eyeWorldPos({}), p = m.toWorld(x, .35, z), f = w.updateFrame(); const d = { x: p.x - e.x, y: p.y - e.y, z: p.z - e.z }, l = Math.hypot(d.x, d.y, d.z), dot = v => d.x * v.x + d.y * v.y + d.z * v.z; w.yaw = Math.atan2(dot(f.east), dot(f.north)); w.pitch = Math.asin(dot(f.up) / l); },
            { x: 4 + rnd(-.2, .2), z: 20 + rnd(-.2, .2) });
          const lbl = (await s.state()).actionLabel;
          if (!lbl) { s.log('no dig button shown while standing at the crate'); await wait(1200); break; }
          const beforeCuts = await s.safeEv(() => cosmos.opening.state.cuts.length, null, 0);
          await s.action({ miss: .12 }); digTaps++; await wait(rnd(400, 1100)); await s.settle(12000);
          await s.stickUp();
          if (/carry/i.test(lbl)) { await wait(500); break; }
          const afterCuts = await s.safeEv(() => cosmos.opening.state.cuts.length, null, beforeCuts);
          if (afterCuts === beforeCuts && /dig/i.test(lbl)) { await s.settle(12000); await wait(800); const again = await s.safeEv(() => cosmos.opening.state.cuts.length, null, beforeCuts); if (again === beforeCuts) s.finding({ kind: 'dig-tap-lost', sev: 66, title: 'A Dig tap in the opening made no cut', detail: `cuts stayed ${beforeCuts} after tapping "${lbl}"`, key: 'dig-tap-lost' }); }
          if (digTaps === 4 && !refreshedDig) { refreshedDig = true; await s.shot('before-refresh-dig'); await s.reload('mid-dig'); const a = await s.state(); if (a.stage !== 4) s.finding({ kind: 'refresh-lost-progress', sev: 88, title: 'Refreshing during the dig changed the opening step', detail: `was step 4, after refresh step ${a.stage}`, key: 'refresh-dig' }); }
          break; }
        case 5: { // the driver arrives (about 8 s), then walk up and tap Ride
          if (!st.actionLabel || !/ride/i.test(st.actionLabel)) {
            const pos = st.pos || { x: 0, z: 0 };
            if (Math.hypot(pos.x + 7, pos.z - 23) > 3.2) { await W.to('opening', -5.6, 22.7, { r: 1.2, timeout: 50, label: 'the rescue vehicle', pitch: 0 }); }
            await wait(rnd(800, 2000)); break; }
          await s.stickDown(); await wait(300); await s.stickUp();
          await s.action({ miss: .15 }); await wait(1200); break; }
        case 6: { // riding: look around, refresh once mid-ride
          if (!refreshedRide && st.pos && (await s.safeEv(() => cosmos.opening.rideSeconds, null, 0)) > 15) { refreshedRide = true; await s.shot('before-refresh-ride'); await s.reload('mid-ride'); const a = await s.state(); if (a.opening && a.stage !== 6) s.finding({ kind: 'refresh-lost-progress', sev: 88, title: 'Refreshing during the ride changed the opening step', detail: `was step 6, after refresh step ${a.stage}`, key: 'refresh-ride' }); else if (!a.opening) s.log('after the refresh the opening was already over (fine if the ride had finished)'); }
          if (chance(.3)) await s.lookDrag(rnd(-100, 100), rnd(-15, 15)); await wait(rnd(2000, 4000)); break; }
        default: await wait(1500);
      }
    }
  };

  return P;
}
