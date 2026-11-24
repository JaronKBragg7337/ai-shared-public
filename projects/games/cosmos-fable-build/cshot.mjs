// Cosmos screenshot harness (Fable build run).
// node cshot.mjs <webkit|chromium> <phone|desktop> <outDir> <scenario.mjs> [only,shot,names]
// Needs the game served: PORT=4380 node server.js (in the worktree's games/the-cosmos).
// A scenario exports default async ({ page, shot, ev, step, land, phone }) => {...}
import { createRequire } from 'node:module';
import { join, resolve } from 'node:path';
import { pathToFileURL } from 'node:url';
import { mkdirSync } from 'node:fs';
const pw = createRequire('C:/Users/lilli/AI-Shared/tools/site-reel/node_modules/')('playwright-core');
const [eng, size, out, scenario, only] = process.argv.slice(2);
mkdirSync(out, { recursive: true });
const want = only ? new Set(only.split(',')) : null;
const phone = size === 'phone';
const UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1';
const browser = await pw[eng].launch({ headless: true, args: eng === 'chromium' ? ['--use-angle=d3d11', '--enable-gpu', '--ignore-gpu-blocklist'] : [] });
const ctx = await browser.newContext(phone ? { userAgent: UA, viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true } : { viewport: { width: 1440, height: 900 } });
const page = await ctx.newPage(); const errors = [];
page.on('pageerror', e => errors.push('pageerror ' + String(e).slice(0, 300)));
page.on('console', m => { if (m.type() === 'error') errors.push('console ' + m.text().slice(0, 300)); });
const base = process.env.BASE || 'http://127.0.0.1:4380/';
await page.goto(`${base}?dev=1&solo=1&opening=off${phone ? '&tier=low' : '&tier=high'}${process.env.Q || ''}`, { waitUntil: 'domcontentloaded', timeout: 120000 });
await page.waitForFunction(() => window.cosmos?.engine?.frameCount > 10 && window.cosmos.space, null, { timeout: 240000 });
await page.waitForTimeout(4000);
const tag = `${size}-${eng}${process.env.SUF || ''}`;
const shot = async (name) => { if (want && !want.has(name)) return false; await page.waitForTimeout(700); await page.screenshot({ path: join(out, `${name}-${tag}.png`), timeout: 180000 }); console.log('shot', name); return true; };
const step = (n) => page.evaluate((n) => { for (let i = 0; i < n; i++) cosmos.step(1 / 30); }, n);
const ev = (s) => page.evaluate(s);
// land on a world and define P(east,north,up), cam(eye,target), stand(e,n,yaw,pitch,third) around its pad
const land = (world) => page.evaluate((world) => {
  const c = cosmos; window.landed = c.space.debugLand(world); for (let i = 0; i < 20; i++) c.step(1 / 30);
  const mw = c.space.worlds.get(world), b = mw.body, pi = b.padInfo;
  window.P = (e, n, u = 0) => { const x = pi.point.x + pi.east.x * e + pi.north.x * n, y = pi.point.y + pi.east.y * e + pi.north.y * n, z = pi.point.z + pi.east.z * e + pi.north.z * n, l = Math.hypot(x, y, z), R = b.surfaceRadius(x / l, y / l, z / l) + u; return { x: x / l * R, y: y / l * R, z: z / l * R }; };
  window.cam = (eye, tgt) => { c.freeCam.set(P(...eye), P(...tgt)); mw.force(P(...eye)); for (let i = 0; i < 12; i++) c.step(1 / 30); };
  window.stand = (e, n, yaw, pitch, third) => { const w = c.walker; c.freeCam.off(); c.ship.aboard = false; if (c.ship.seat) c.ship.stations.stand(); Object.assign(w.worldPos, P(e, n, 0.03)); w.velocity = { x: 0, y: 0, z: 0 }; w.yaw = yaw; w.pitch = pitch; w.grounded = true; c.view.mode = third ? 'third' : 'first'; mw.force(w.worldPos); for (let i = 0; i < 20; i++) c.step(1 / 30); };
}, world);
const mod = await import(pathToFileURL(resolve(scenario)).href);
try { await mod.default({ page, shot, ev, step, land, phone, want }); } catch (e) { errors.push('scenario ' + String(e).slice(0, 400)); }
const scroll = await page.evaluate(() => ({ sw: document.documentElement.scrollWidth, iw: innerWidth }));
console.log('scroll', JSON.stringify(scroll), 'errors', JSON.stringify(errors));
await browser.close();
