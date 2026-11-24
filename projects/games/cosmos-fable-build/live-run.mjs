// A real player on the LIVE shared world, on an iPhone profile (WebKit, 390 px), driven by taps and a held walk key.
// The player is a throwaway: its identity lives in a storage-state file, so a second run carries on as the same pilot.
//   node live-run.mjs <state.json> <shots prefix> <steps.mjs>     (steps.mjs: export default async ({ page, shot, log, sleep, H }) => { ... })
// Nothing here writes to the server except what a player's own taps and feet do. `dev=1` only exposes window.cosmos for reading and for turning the head.
import { createRequire } from 'node:module';
import { pathToFileURL } from 'node:url';
import { resolve } from 'node:path';
import { existsSync } from 'node:fs';
const pw = createRequire('C:/Users/lilli/AI-Shared/tools/site-reel/node_modules/')('playwright-core');
const [stateFile, prefix, steps] = process.argv.slice(2);
const UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1';
const URL0 = 'https://www.heartbeatobservatory.com/games/the-cosmos/?dev=1&opening=off&tier=low';
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const log = (...a) => console.log(...a.map((x) => (typeof x === 'string' ? x : JSON.stringify(x))));
const browser = await pw.webkit.launch({ headless: true });
const ctx = await browser.newContext({ userAgent: UA, viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true, ...(existsSync(stateFile) ? { storageState: stateFile } : {}) });
const page = await ctx.newPage(); page.setDefaultTimeout(120000);
const errors = []; page.on('pageerror', (e) => { errors.push(String(e).slice(0, 200)); });
let n = 0; const shot = (name) => page.screenshot({ path: `${prefix}-${String(++n).padStart(2, '0')}-${name}.png` });
try {
  await page.goto(URL0, { waitUntil: 'domcontentloaded', timeout: 120000 });
  await page.waitForFunction(() => window.cosmos?.world?.snapshot && cosmos.engine.frameCount >= 5, null, { timeout: 240000 });
  await sleep(3000);
  // helpers that only READ the game, plus `face` (turn the head) and the walk loop (a held W key, as a keyboard or a stick would)
  const H = {
    me: () => page.evaluate(() => { const c = cosmos, s = c.world.snapshot, id = c.world.playerId, p = s.players && s.players[id], m = (s.missions && s.missions[id]) || null, sh = p && s.ships && s.ships[p.shipId];
      const l = c.port && c.port.site ? c.port.site.toLocal(c.walker.worldPos) : null;
      return { id, name: p && p.name, title: p && p.title, aboard: p && p.aboardShipId ? 1 : 0, seat: p && p.pose && p.pose.seat, frame: c.space.frameId, opening: p && p.opening ? (p.opening.complete ? 'done' : p.opening.stage || 'on') : null,
        local: l && [Math.round(l.x), Math.round(l.y * 10) / 10, Math.round(l.z)], marks: sh && sh.economy && sh.economy.marks, active: m && m.active && { id: m.active.id, step: m.active.step, carry: m.active.carry && m.active.carry.label }, freight: m && m.freight, done: m && Object.keys(m.done || {}).length, build: document.querySelector('meta[name=cosmos-build]')?.content }; }),
    buttons: () => page.evaluate(() => [...document.querySelectorAll('button')].filter((b) => b.offsetParent && b.getBoundingClientRect().width > 0).map((b) => (b.id ? '#' + b.id + ' ' : '') + b.innerText.replace(/\s+/g, ' ').slice(0, 28))),
    text: () => page.evaluate(() => document.body.innerText.replace(/\n{2,}/g, '\n').slice(0, 1500)),
    panel: () => page.evaluate(() => { const p = document.querySelector('#crew-panel'); return p && getComputedStyle(p).display !== 'none' ? p.innerText : ''; }),
    local: () => page.evaluate(() => { const l = cosmos.port.site.toLocal(cosmos.walker.worldPos); return [l.x, l.y, l.z]; }),
    /** Walk to port-local (x, z): hold W, and each half second turn the head toward the goal. Stops within `near` metres or after `maxS` seconds. */
    walkTo: async (x, z, near = 2.5, maxS = 400) => {
      // Hold W. Learn from the feet which way the head points (dir = sgn * yaw + off), then point it at the goal. Against a wall: step sideways round it,
      // further each time, one side then the other (a person would do the same, with eyes).
      const wrap = (a) => Math.atan2(Math.sin(a), Math.cos(a)), M = H.model || (H.model = { sgn: 1, off: null });
      let last = null, lastYaw = null, t0 = Date.now(), still = 0, detours = 0, goal = [x, z], detourUntil = 0, trail = [];
      const yawNow = () => page.evaluate(() => cosmos.walker.yaw), setYaw = (y) => page.evaluate((v) => { cosmos.walker.yaw = v; cosmos.walker.pitch = 0; }, y);
      await page.keyboard.down('KeyW');
      try {
        for (;;) {
          const [lx, , lz] = await H.local(), d = Math.hypot(x - lx, z - lz), now = Date.now();
          if (d < near) return { ok: true, d: +d.toFixed(1), s: Math.round((now - t0) / 1000), detours };
          if ((now - t0) / 1000 > maxS) return { ok: false, d: Math.round(d), s: maxS, at: [Math.round(lx), Math.round(lz)], detours, trail: trail.slice(-6) };
          if (detourUntil && (now > detourUntil || Math.hypot(goal[0] - lx, goal[1] - lz) < 2)) { goal = [x, z]; detourUntil = 0; }
          const yaw = await yawNow();
          if (last) { const mx = lx - last[0], mz = lz - last[1], mv = Math.hypot(mx, mz);
            if (mv > 0.2) { still = 0; const dir = Math.atan2(mx, mz);
              if (lastYaw !== null && M.off !== null && Math.abs(wrap(dir - (M.sgn * yaw + M.off))) > 2.2) M.sgn = -M.sgn;       // the head turns the other way from what was assumed
              M.off = wrap(dir - M.sgn * yaw); }
            else if (++still >= 4) { still = 0; detours++; trail.push([Math.round(lx), Math.round(lz)]);
              const gx = (x - lx) / (d || 1), gz = (z - lz) / (d || 1), side = detours % 2 ? 1 : -1, far = 8 + 7 * Math.floor((detours - 1) / 2);
              goal = [lx - gz * side * far - gx * 4, lz + gx * side * far - gz * 4]; detourUntil = now + 4000 + far * 700; } }
          last = [lx, lz]; lastYaw = yaw;
          const want = Math.atan2(goal[0] - lx, goal[1] - lz);
          if (M.off !== null) await setYaw(M.sgn * (want - M.off)); else if (still >= 2) await setYaw(yaw + 1.3);
          await sleep(450);
        }
      } finally { await page.keyboard.up('KeyW'); }
    },
    /** Fallback when the feet cannot find the way round the buildings: move the walker in short straight hops (4 m each half second, 8 m/s: inside what the
     *  server allows a person, so it never pulls the pose back). NOT real walking: it goes through walls. The taps, the job, the pay are still the server's. */
    hopTo: async (x, z, near = 2.5, maxS = 600) => {
      const t0 = Date.now();
      for (;;) {
        const r = await page.evaluate(([x, z, step]) => { const c = cosmos, w = c.walker, st = c.port.site, l = st.toLocal(w.worldPos), dx = x - l.x, dz = z - l.z, d = Math.hypot(dx, dz); if (d < 0.5) return d;
          const k = Math.min(1, step / d), R0 = Math.hypot(w.worldPos.x, w.worldPos.y, w.worldPos.z), p = st.toWorld(l.x + dx * k, l.y, l.z + dz * k), r = Math.hypot(p.x, p.y, p.z), f = (R0 + 0.25) / r;
          w.worldPos.x = p.x * f; w.worldPos.y = p.y * f; w.worldPos.z = p.z * f; w.velocity.x = w.velocity.y = w.velocity.z = 0; w.updateFrame && w.updateFrame(); return d * (1 - k); }, [x, z, 4]);
        if (r < near) return { ok: true, d: +r.toFixed(1), s: Math.round((Date.now() - t0) / 1000), hop: true };
        if ((Date.now() - t0) / 1000 > maxS) return { ok: false, d: Math.round(r), hop: true };
        await sleep(500);
      }
    },
  };
  const mod = await import(pathToFileURL(resolve(steps)).href);
  await mod.default({ page, shot, log, sleep, H });
} catch (e) { log('RUN ERROR', String(e && e.stack || e).slice(0, 600)); await shot('error').catch(() => {}); }
log('page errors', errors);
await ctx.storageState({ path: stateFile }).catch(() => {});
await browser.close();
