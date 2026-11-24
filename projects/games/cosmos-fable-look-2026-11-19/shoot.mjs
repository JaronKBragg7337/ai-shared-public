// node shoot.mjs <webkit|chromium> <phone|desktop> <outDir> [only,shot,names]
import { createRequire } from 'node:module';
import { join } from 'node:path';
const pw = createRequire('C:/Users/lilli/AI-Shared/tools/site-reel/node_modules/')('playwright-core');
const [eng, size, out, only] = process.argv.slice(2);
const want = only ? new Set(only.split(',')) : null;
const phone = size === 'phone';
const UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1';
const browser = await pw[eng].launch({ headless: true, args: eng === 'chromium' ? ['--use-angle=d3d11', '--enable-gpu', '--ignore-gpu-blocklist'] : [] });
const ctx = await browser.newContext(phone ? { userAgent: UA, viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true } : { viewport: { width: 1440, height: 900 } });
const page = await ctx.newPage(); const errors = [];
page.on('pageerror', e => errors.push('pageerror ' + String(e).slice(0, 300)));
page.on('console', m => { if (m.type() === 'error') errors.push('console ' + m.text().slice(0, 300)); });
const t0 = Date.now();
await page.goto(`http://127.0.0.1:4380/?dev=1&solo=1&opening=off${phone ? '&tier=low' : '&tier=high'}${process.env.Q || ''}`, { waitUntil: 'domcontentloaded', timeout: 120000 });
await page.waitForFunction(() => window.cosmos?.engine?.frameCount > 10 && window.cosmos.space, null, { timeout: 240000 });
await page.waitForTimeout(4000);
console.log('loaded ms', Date.now() - t0, await page.evaluate(() => { const g = cosmos.engine.renderer.getContext(); const e = g.getExtension('WEBGL_debug_renderer_info'); return e ? g.getParameter(e.UNMASKED_RENDERER_WEBGL) : 'n/a'; }));
const tag = `${size}-${eng}${process.env.SUF || ''}`;
const shot = async (name) => { if (want && !want.has(name)) return false; await page.waitForTimeout(700); await page.screenshot({ path: join(out, `${name}-${tag}.png`), timeout: 180000 }); console.log('shot', name); return true; };
const on = (n) => !want || want.has(n);
const step = (n) => page.evaluate((n) => { for (let i = 0; i < n; i++) cosmos.step(1 / 30); }, n);
// --- Mars
if (on('01-mars-spawn')) { await shot('01-mars-spawn'); }
if (on('02-mars-port-walk')) { await page.evaluate(() => { const c = cosmos, w = c.walker, p = c.port.site.toWorld(-60, 0.3, 52); c.ship.aboard = false; if (c.ship.seat) c.ship.stations.stand(); Object.assign(w.worldPos, p); w.velocity = { x: 0, y: 0, z: 0 }; w.yaw = 0.6; w.pitch = 0; }); await step(60); await shot('02-mars-port-walk'); }
if (on('03-mars-open-ground')) { await page.evaluate(() => { const c = cosmos, w = c.walker, p = c.port.site.toWorld(200, 0.3, 250); c.ship.aboard = false; if (c.ship.seat) c.ship.stations.stand(); Object.assign(w.worldPos, p); w.velocity = { x: 0, y: 0, z: 0 }; w.yaw = 2.2; w.pitch = -0.1; }); await step(90); await shot('03-mars-open-ground'); }
// --- Phobos
await page.evaluate(() => {
  const c = cosmos; window.land = c.space.debugLand('phobos'); for (let i = 0; i < 20; i++) c.step(1 / 30);
  const mw = c.space.worlds.get('phobos'), b = mw.body, pi = b.padInfo;
  window.P = (e, n, u = 0) => { const x = pi.point.x + pi.east.x * e + pi.north.x * n, y = pi.point.y + pi.east.y * e + pi.north.y * n, z = pi.point.z + pi.east.z * e + pi.north.z * n, l = Math.hypot(x, y, z), R = b.surfaceRadius(x / l, y / l, z / l) + u; return { x: x / l * R, y: y / l * R, z: z / l * R }; };
  window.cam = (eye, tgt) => { c.freeCam.set(P(...eye), P(...tgt)); mw.force(P(...eye)); for (let i = 0; i < 12; i++) c.step(1 / 30); };
  window.stand = (e, n, yaw, pitch, third) => { const w = c.walker; c.freeCam.off(); c.ship.aboard = false; if (c.ship.seat) c.ship.stations.stand(); Object.assign(w.worldPos, P(e, n, 0.03)); w.velocity = { x: 0, y: 0, z: 0 }; w.yaw = yaw; w.pitch = pitch; w.grounded = true; c.view.mode = third ? 'third' : 'first'; mw.force(w.worldPos); for (let i = 0; i < 20; i++) c.step(1 / 30); };
});
const ev = (s) => page.evaluate(s);
if (on('04-phobos-space')) { await ev(`cam([0,0,9000],[0,0,0])`); await shot('04-phobos-space'); }
if (on('05-phobos-approach')) { await ev(`cam([-900,-700,700],[0,0,0])`); await shot('05-phobos-approach'); }
if (on('06-phobos-final')) { await ev(`cam([-140,-110,60],[0,0,3])`); await shot('06-phobos-final'); }
if (on('07-phobos-landed-ship')) { await ev(`cam([-32,-20,2.2],[0,0,4])`); await shot('07-phobos-landed-ship'); }
if (on('08-phobos-eye-pad')) { await ev(`stand(28,-8,Math.PI/2,-0.06)`); await shot('08-phobos-eye-pad'); }
if (on('09-phobos-eye-rocks')) { await ev(`stand(130,-30,1.2,-0.05)`); await shot('09-phobos-eye-rocks'); }
if (on('10-phobos-underfoot')) { await ev(`stand(130,-30,1.2,-0.9)`); await shot('10-phobos-underfoot'); }
if (on('11-phobos-third-walk')) { await ev(`stand(110,-20,Math.PI/2,-0.1,true)`); await page.keyboard.down('KeyW'); await step(90); await shot('11-phobos-third-walk'); await page.keyboard.up('KeyW'); }
if (on('12-phobos-mars-sky')) { await ev(`stand(130,-30,1.2,0.5)`); await ev(`(()=>{const c=cosmos,w=c.walker,f=w.updateFrame(),p=w.worldPos,m=c.space.worlds.get('phobos');const o=c.engine.frameOrigin?c.engine.frameOrigin('mars'):null;window._mdbg=Object.keys(c.space).slice(0,60)})()`); await shot('12-phobos-mars-sky'); }
if (on('13-ship-interior')) { await ev(`(()=>{const c=cosmos;c.freeCam.off();c.view.mode='first';c.ship.aboard=true;})()`); await ev(`cosmos.at&&0`); await step(30); await shot('13-ship-interior'); }
const scroll = await page.evaluate(() => ({ sw: document.documentElement.scrollWidth, iw: innerWidth }));
console.log('scroll', JSON.stringify(scroll), 'errors', JSON.stringify(errors));
await browser.close();
