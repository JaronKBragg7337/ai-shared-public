// The looks pass: phone-size pictures of the room from the places a person actually stands and turns.
// Not a test of behaviour (test-walk.mjs does that). It walks with real keys and mouse-look and saves what it sees,
// so the room can be judged by eye: the switch wall, the shelf and books, and the room once its lamps are lit.
//   node reading-room-3d/shots-looks.mjs [--browser=edge|iphone-webkit] [--room=1..4] [--cores=4]
// --cores=4 makes the test browser report four processor cores, as an iPhone does, so the pictures show the
// path a real iPhone takes through the house tier file (this machine has more cores and would otherwise skip it).
import { createRequire } from 'node:module';
import { existsSync, mkdirSync, readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url)), root = path.resolve(here, '..');
const arg = (name, fallback) => (process.argv.find((a) => a.startsWith(`--${name}=`)) || '').split('=')[1] || fallback;
const which = arg('browser', 'iphone-webkit'), roomNo = Number(arg('room', '1')), cores = Number(arg('cores', '0'));
const playwright = createRequire(path.resolve(process.env.CW_PLAYWRIGHT_ROOT || 'C:/Users/lilli/.codex/runtime/unfinished-island/node_modules', '..', 'package.json'))('playwright');
const threeDir = process.env.CW_THREE_DIR || 'C:/Users/lilli/AI-Shared/scratch/world2-remake/phase3/three/build';
const offline = ['three.module.js', 'three.core.js'].every((file) => existsSync(path.join(threeDir, file)));
const js = 'text/javascript; charset=utf-8', shotDir = path.join(here, 'screenshots');
mkdirSync(shotDir, { recursive: true });

const browser = which === 'edge'
  ? await playwright.chromium.launch({ headless: true, channel: 'msedge' })
  : await playwright.webkit.launch({ headless: true, executablePath: process.env.CW_WEBKIT || path.join(process.env.LOCALAPPDATA, 'ms-playwright', 'webkit-2336', 'Playwright.exe') });
const context = await browser.newContext({ viewport: which === 'edge' ? { width: 390, height: 844 } : { width: 375, height: 812 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true });
await context.route('**/*', async (route) => {
  const url = new URL(route.request().url()), asset = url.pathname.match(/^\/npm\/three@0\.182\.0\/build\/(three\.(?:module|core)\.js)$/);
  if (url.hostname === 'cdn.jsdelivr.net' && asset) {
    return offline ? route.fulfill({ status: 200, contentType: js, headers: { 'access-control-allow-origin': '*' }, body: readFileSync(path.join(threeDir, asset[1])) }) : route.continue();
  }
  if (url.host !== 'cw.test') return route.abort();
  const file = path.join(root, (url.pathname === '/reading-room-3d/' ? '/reading-room-3d/index.html' : url.pathname).slice(1));
  return existsSync(file) ? route.fulfill({ status: 200, contentType: file.endsWith('.js') ? js : 'text/html; charset=utf-8', body: readFileSync(file) }) : route.fulfill({ status: 404 });
});
if (cores) await context.addInitScript((n) => Object.defineProperty(navigator, 'hardwareConcurrency', { configurable: true, get: () => n }), cores);
const page = await context.newPage(), errors = [];
page.on('pageerror', (error) => errors.push(String(error)));
await page.goto('http://cw.test/reading-room-3d/');
await page.waitForFunction(() => window.rr?.state()?.room === 1 && window.rr.state().render.decorated);
console.log('house tier', await page.evaluate(() => window.HBDevice.tier), '| room', JSON.stringify(await page.evaluate(() => window.rr.state().render)));

const state = () => page.evaluate(() => window.rr.state()), where = () => page.evaluate(() => window.rr.pos());
const angle = (v) => Math.atan2(Math.sin(v), Math.cos(v));
const size = page.viewportSize();
async function turn(yaw, pitch = -0.06) {                       // mouse-look, as a person at a computer would
  for (let tries = 0; tries < 14; tries++) {
    const s = await state(), dx = angle(yaw - s.yaw), dy = s.pitch - pitch;
    if (Math.abs(dx) < 0.03 && Math.abs(dy) < 0.03) return;
    const x = Math.round(size.width / 2), y = Math.round(size.height * 0.43);
    const mx = Math.max(-220, Math.min(220, Math.round(dx / 0.0045))), my = Math.max(-160, Math.min(160, Math.round(dy / 0.0045)));
    await page.mouse.move(x - mx / 2, y - my / 2); await page.mouse.down(); await page.mouse.move(x + mx / 2, y + my / 2); await page.mouse.up();
    await page.waitForTimeout(30);
  }
}
async function walkTo(x, z) {                                   // turn to it, then hold W
  for (let tries = 0; tries < 8; tries++) {
    const s = await state(), far = Math.hypot(x - s.x, z - s.z);
    if (far < 0.22) return;
    await turn(Math.atan2(x - s.x, s.z - z));
    await page.keyboard.down('w');
    await page.waitForFunction(([tx, tz, start]) => { const t = window.rr.state(), d = Math.hypot(tx - t.x, tz - t.z); return d < 0.18 || d > start + 0.05; }, [x, z, far], { timeout: 9000 }).catch(() => {});
    await page.keyboard.up('w');
    await page.waitForTimeout(60);
  }
}
const shot = async (name) => { await page.waitForTimeout(450); await page.screenshot({ path: path.join(shotDir, `looks-${which}${cores ? `-cores${cores}` : ''}-room${roomNo}-${name}.png`) }); console.log('saved', name); };
const settled = () => page.waitForFunction(() => window.rr.state().settled && [0, 1].includes(window.rr.state().doorProgress), null, { timeout: 8000 });
async function lookAt(x, y, z) {
  const s = await state();
  await turn(Math.atan2(x - s.x, s.z - z), Math.atan2(y - 1.6, Math.hypot(x - s.x, z - s.z)));
}

// reach the room asked for by really solving the earlier ones
for (let n = 1; n < roomNo; n++) {
  const map = await where(), open = (await state()).open[0];
  for (let b = 0; b < 8; b++) if ((open >> b) & 1) { const sw = map[String(b + 1)]; await walkTo(sw.x + 1.5, sw.z); await turn(-Math.PI / 2, -0.03); await page.keyboard.press('e'); await settled(); }
  await walkTo(0, map.doorway.z + 1.4); await turn(0); await page.keyboard.down('w'); await page.waitForFunction(() => window.rr.state().through); await page.keyboard.up('w');
  await page.locator('#next').tap(); await page.waitForFunction((r) => window.rr.state().room === r && window.rr.state().render.decorated, n + 1);
}
const map = await where(), depth = -map.doorway.z;
await turn(0, -0.08); await shot('1-start');
await walkTo(0, -Math.min(5.2, depth * 0.5)); await turn(Math.PI, -0.02); await shot('2-behind-you');
await turn(-Math.PI / 2, -0.03); await shot('3-switch-wall');
const lamp = map.A;
const lampView = [lamp.x - 2.65, lamp.z - 0.95];
await walkTo(...lampView); await lookAt(lamp.x, lamp.aimY, lamp.z); await shot('4-lamp-wall');
const open = (await state()).open[0];
for (let b = 0; b < 8; b++) if ((open >> b) & 1) { const sw = map[String(b + 1)]; await walkTo(sw.x + 1.5, sw.z); await turn(-Math.PI / 2, -0.03); if (b === 0) await shot('5-facing-a-switch'); await page.keyboard.press('e'); await settled(); }
await walkTo(0, -1.4); await turn(0, -0.08); await shot('6-lamps-lit-door-open');
await walkTo(0.4, map.doorway.z + 2.6); await turn(-0.12, -0.02); await shot('7-the-way-on');
await walkTo(...lampView); await lookAt(lamp.x, lamp.aimY, lamp.z); await shot('8-a-lit-lamp');
await walkTo(map.shelf.x, map.shelf.z + 2.65); await lookAt(map.shelf.x, map.shelf.aimY, map.shelf.z); await shot('9-the-books');
console.log(errors.length ? `page errors: ${errors.join(' | ')}` : 'no page errors');
await browser.close();
if (errors.length) process.exitCode = 1;
