// Wake the lantern and watch it, with browser input. The page's test hook is used only for observation.
// node reading-room-3d/test-lantern.mjs [--browser=iphone-webkit|edge]
// WebKit runs with full motion and takes the pictures; Edge runs the same checks with "reduce motion" on.
import assert from 'node:assert/strict';
import { createRequire } from 'node:module';
import { existsSync, mkdirSync, readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.dirname(here);
const args = process.argv.slice(2);
const only = args.find((arg) => arg.startsWith('--browser='))?.split('=')[1];
assert(!only || ['iphone-webkit', 'edge'].includes(only), 'Unknown browser');
const require = createRequire(import.meta.url);
let playwright;
try {
  playwright = require('playwright');
} catch (error) {
  if (error.code !== 'MODULE_NOT_FOUND') throw error;
  const modules = process.env.CW_PLAYWRIGHT_ROOT || 'C:/Users/lilli/.codex/runtime/unfinished-island/node_modules';
  playwright = createRequire(path.resolve(modules, '..', 'package.json'))('playwright');
}
const webkitPath = process.env.CW_WEBKIT || (process.env.LOCALAPPDATA &&
  path.join(process.env.LOCALAPPDATA, 'ms-playwright', 'webkit-2336', 'Playwright.exe'));
const threeDir = process.env.CW_THREE_DIR || 'C:/Users/lilli/AI-Shared/scratch/world2-remake/phase3/three/build';
const offline = ['three.module.js', 'three.core.js'].every((file) => existsSync(path.join(threeDir, file)));
console.log(offline ? `Three.js r182 served from ${threeDir}` : 'Three.js r182 served by jsDelivr');

const js = 'text/javascript; charset=utf-8';
const files = new Set(['/reading-room-3d/index.html', '/reading-room-3d/main.js',
  '/reading-room-3d/room-skins.js', '/reading-room-3d/room-scene.js', '/skin/skincode.js',
  '/reading-room-3d/hb-thumbstick.js', '/reading-room-3d/hb-device-tier.js', '/rooms.js', '/world.js', '/learner/mind.js']);
const threePath = /^\/npm\/three@0\.182\.0\/build\/(three\.(?:module|core)\.js)$/;
async function serve(context) {
  await context.route('**/*', async (route) => {
    const url = new URL(route.request().url());
    const asset = url.pathname.match(threePath);
    if (url.hostname === 'cdn.jsdelivr.net' && asset) {
      if (!offline) return route.continue();
      return route.fulfill({ status: 200, contentType: js, headers: { 'access-control-allow-origin': '*' },
        body: readFileSync(path.join(threeDir, asset[1])) });
    }
    if (url.host !== 'cw.test') return route.abort();
    const requestPath = url.pathname === '/reading-room-3d/' ? '/reading-room-3d/index.html' : url.pathname;
    if (url.pathname === '/favicon.ico') return route.fulfill({ status: 204 });
    if (!files.has(requestPath)) return route.fulfill({ status: 404 });
    return route.fulfill({ status: 200, contentType: requestPath.endsWith('.js') ? js : 'text/html; charset=utf-8',
      body: readFileSync(path.join(root, requestPath.slice(1))) });
  });
}

const browsers = [
  { name: 'iphone-webkit', still: false, launch: () => playwright.webkit.launch({ headless: true, executablePath: webkitPath }),
    viewport: { width: 375, height: 812 },
    userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1' },
  { name: 'edge', still: true, launch: () => playwright.chromium.launch({ headless: true, channel: 'msedge' }),
    viewport: { width: 390, height: 844 } },
];
const distance = (a, b) => Math.hypot(a.x - b.x, a.z - b.z);
const angle = (v) => Math.atan2(Math.sin(v), Math.cos(v));
const bearing = (from, to) => Math.atan2(to.x - from.x, from.z - to.z);
const shotDir = path.join(here, 'screenshots');
let passes = 0, failures = 0, screenshots = 0;

function check(name, passed, details = '') {
  if (passed) passes++;
  else failures++;
  console.log(`${passed ? 'PASS' : 'FAIL'} ${name}${details ? ` (${details})` : ''}`);
}

async function walkBrowser(spec, browser) {
  const { name, viewport, still } = spec;
  const expect = (label, passed, details) => check(`${name} ${label}`, passed, details);
  const context = await browser.newContext({ viewport, userAgent: spec.userAgent, deviceScaleFactor: 2, isMobile: true, hasTouch: true,
    reducedMotion: still ? 'reduce' : 'no-preference' });
  await serve(context);
  const page = await context.newPage();
  page.setDefaultTimeout(15000);
  const errors = [];
  page.on('pageerror', (error) => errors.push(String(error)));
  page.on('console', (message) => { if (message.type() === 'error') errors.push(message.text()); });
  await page.goto('http://cw.test/reading-room-3d/');
  await page.waitForFunction(() => window.rr?.state()?.room === 1 && window.rr.state().render.decorated);

  const width = viewport.width, height = viewport.height;
  const state = () => page.evaluate(() => window.rr.state());
  const lamp = async () => (await state()).lantern;
  const positions = () => page.evaluate(() => window.rr.pos());
  const text = (id) => page.locator(id).innerText();
  const shown = (id) => page.locator(id).isVisible();
  const tap = (id) => page.locator(id).tap();
  const narrow = () => page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth && window.scrollY === 0);
  const until = (test, value, timeout = 120000) => page.waitForFunction(test, value, { timeout, polling: 50 });
  async function shot(label) {
    if (still) return;
    mkdirSync(shotDir, { recursive: true });
    await page.screenshot({ path: path.join(shotDir, `lantern-${name}-${label}.png`) });
    screenshots++;
  }
  async function mouseLook(dx, dy = 0) {
    const x = Math.round(width / 2 - dx / 2), y = Math.round(height * 0.43 - dy / 2);
    await page.mouse.move(x, y);
    await page.mouse.down();
    try { await page.mouse.move(x + dx, y + dy); } finally { await page.mouse.up(); }
  }
  async function turn(yaw, pitch) {
    for (let attempt = 0; attempt < 10; attempt++) {
      const from = await state();
      const dx = angle(yaw - from.yaw), dy = pitch === undefined ? 0 : from.pitch - pitch;
      if (Math.abs(dx) < 0.038 && Math.abs(dy) < 0.038) return;
      await mouseLook(Math.max(-220, Math.min(220, Math.round(dx / 0.0045))), Math.max(-160, Math.min(160, Math.round(dy / 0.0045))));
      await page.waitForTimeout(25);
    }
    throw new Error(`Could not turn to ${yaw.toFixed(3)}`);
  }
  async function goTo(target) {
    for (let attempt = 0; attempt < 6; attempt++) {
      const from = await state();
      if (distance(from, target) < 0.22) return;
      const yaw = bearing(from, target);
      await turn(yaw, -0.04);
      await page.keyboard.down('w');
      try {
        await page.waitForFunction(({ origin, target, yaw }) => {
          const s = window.rr.state();
          const length = Math.hypot(origin.x - target.x, origin.z - target.z);
          return (s.x - origin.x) * Math.sin(yaw) + (origin.z - s.z) * Math.cos(yaw) >= length - 0.12;
        }, { origin: { x: from.x, z: from.z }, target, yaw }, { timeout: 10000 });
      } finally { await page.keyboard.up('w'); }
    }
    throw new Error(`Could not walk to ${JSON.stringify(target)}`);
  }
  async function face(id) {
    const target = (await positions())[id];
    const spot = { x: target.x - Math.sign(target.x) * 2.15, z: target.z };
    if (distance(await state(), spot) > 0.5) await goTo(spot);
    const s = await state();
    await turn(bearing(s, target), Math.atan2((target.aimY ?? 1.45) - 1.6, distance(s, target)));
    await page.waitForFunction((which) => window.rr.state().facing === which, id);
  }
  async function watch(point, y = 1.4) {           // turn to look at a point in the room
    const s = await state();
    await turn(bearing(s, point), Math.atan2(y - 1.6, Math.max(0.5, distance(s, point))));
  }
  async function follow(room) {                    // walk through the open door after the lantern
    const { doorway } = await positions();
    await goTo({ x: doorway.x, z: doorway.z + 1.25 });
    await turn(0, -0.04);
    await page.keyboard.down('ArrowUp');
    try { await until((r) => window.rr.state().room === r, room, 15000); } finally { await page.keyboard.up('ArrowUp'); }
  }
  const noRepeat = (tried) => new Set(tried).size === tried.length;

  try {
    let s = await state();
    const map = await positions();
    expect('a lantern stands asleep by the start and the chip says so', !s.lantern.awake && s.lantern.phase === 'asleep' &&
      s.lantern.rooms === 0 && s.lantern.looks === 0 && /Lantern · asleep/.test(await text('#mind-chip')) && distance(map.start, map.lantern) < 1.4);
    await watch(map.lantern, 1.0);
    await shot('1-asleep-at-the-start');

    await face('1');                               // the person flips one lever first: that flip is the person's own
    await tap('#use');
    await page.waitForFunction(() => window.rr.state().settled);
    await face('lantern');
    expect('facing the lantern shows its card with a Wake it button', /A lantern/.test(await text('#card')) &&
      /knows nothing about the marks/.test(await text('#card')) && await shown('#wake'));
    s = await state();
    await turn(bearing(s, map.lantern), Math.atan2(map.lantern.aimY - 1.6, distance(s, map.lantern)));
    await page.touchscreen.tap(Math.round(width / 2), Math.round(height / 2));
    await until(() => window.rr.state().lantern.awake, null, 3000);
    await page.locator('#wake').waitFor({ state: 'hidden', timeout: 3000 }).catch(() => {});
    s = await state();
    expect('a real tap on the 3D lantern wakes it', s.lantern.awake && s.flips === 1 && !(await shown('#wake')), `person flips ${s.flips}`);

    if (still) {                                   // reduce motion: it steps from place to place, it never glides
      const seen = [];
      for (let i = 0; i < 70; i++) { const l = await lamp(); seen.push([l.x, l.y, l.z]); await page.waitForTimeout(35); }
      const steps = seen.slice(1).map((p, i) => Math.hypot(p[0] - seen[i][0], p[1] - seen[i][1], p[2] - seen[i][2]));
      const moves = steps.filter((d) => d > 0);
      expect('with reduce motion the lantern steps, never glides', moves.length >= 2 && moves.every((d) => d > 0.3), `${moves.length} steps`);
    } else {
      await watch({ x: 3.78, z: -2.7 }, 1.45);    // the lamp wall: it ends its first walk at Lamp A
      await until(() => window.rr.state().lantern.seeing === 'A', null, 40000);
      await shot('2-looking-at-a-skin');
      await until(() => ['go', 'flip'].includes(window.rr.state().lantern.phase), null, 20000);
      const lever = (await positions())[(await lamp()).target];
      await watch({ x: lever.x, z: lever.z }, 1.0);
      await until(() => window.rr.state().lantern.phase === 'flip', null, 20000);
      await page.waitForTimeout(150);
      await shot('3-at-a-lever');
    }

    await until(() => window.rr.state().lantern.rooms >= 1, null, 120000);
    s = await state();
    expect('the lantern opens room 1 by itself', s.room === 1 && s.lantern.doorFlips >= 1 && s.lantern.rooms === 1,
      `${s.lantern.doorFlips} door flips, ${s.lantern.looks} looks`);
    expect('it never tries the same setting twice in room 1', noRepeat(s.lantern.tried), `settings ${s.lantern.tried.join(', ')}`);
    expect('its flips are counted apart from the person’s', s.flips === 1 && /1 flip\b/.test(await text('#flips')) && s.lantern.doorFlips >= 1);
    await until(() => window.rr.state().lantern.phase === 'wait', null, 120000);
    s = await state();
    expect('after playing it goes through the door and waits', s.lantern.playFlips >= 2 && s.lantern.z < map.doorway.z && s.doorProgress >= 0.93,
      `${s.lantern.playFlips} play flips`);
    const before = s.lantern;
    await follow(2);
    s = await state();
    expect('following it through the door reaches room 2 with its learning kept', s.room === 2 && !s.through &&
      s.lantern.awake && s.lantern.rooms === 1 && s.lantern.looks >= before.looks && s.lantern.reading === before.reading &&
      !(await page.locator('#results').evaluate((dialog) => dialog.open)));
    expect('the person’s results stay empty for room 1', s.done[0] === null && s.flips === 0);
    expect('room 2 says so at the top', /Room 2 of 4/.test(await text('#where')));

    await tap('#mind-chip');
    await page.waitForFunction(() => /never seen \d+% right/.test(document.getElementById('mind').innerText), null, { timeout: 3000 }).catch(() => {});
    expect('the chip opens the belief card', await shown('#mind') && /Its eyes are simple/.test(await text('#mind')) &&
      /It reads rooms it has never seen \d+% right/.test(await text('#mind')) && await shown('#mind-live'));
    expect('the open card leaves the page in place', await narrow());
    const readings = [(await lamp()).reading];
    const rooms = [(await lamp()).rooms];
    for (let k = 0; k < 3; k++) {
      await tap('#mind-live');
      await until((n) => window.rr.state().lantern.rooms >= n, rooms[k] + 10, 5000);
      const l = await lamp();
      readings.push(l.reading);
      rooms.push(l.rooms);
      if (k === 0) expect('Let it live 10 more rooms raises the rooms count by 10 and the reading moves',
        l.rooms === rooms[0] + 10 && l.reading !== readings[0], `${rooms[0]} to ${l.rooms} rooms, reading ${pct(readings[0])} to ${pct(l.reading)}`);
    }
    const lived = await lamp();
    expect('after 30 rooms in all the reading is 90% or more', lived.rooms >= 30 && lived.reading >= 0.9,
      `${lived.rooms} rooms, reading ${readings.map(pct).join(' > ')}`);
    await page.waitForTimeout(100);
    const card = await text('#mind');
    expect('the belief card says the true thing about circles', lived.trusts === 'named' &&
      /a circle is filled by the thing whose sign is under it: right \d+ of \d+ times/.test(card), card.split('\n').find((line) => /circle is filled/.test(line)));
    expect('the card shows its weights in plain words', /A filled solid circle: counts for glowing/.test(card) && /A filled dashed circle: counts against/.test(card) &&
      new RegExp(`${lived.rooms} rooms lived through`).test(card));
    await page.locator('#mind').evaluate((element) => { element.scrollTop = 0; });
    await shot('4-belief-card');
    await tap('#mind-close');
    expect('Close hides the card', !(await shown('#mind')));

    for (let room = 2; room <= 4; room++) {
      await until(() => window.rr.state().lantern.phase === 'wait', null, 240000);
      s = await state();
      expect(`it opens room ${room} without repeating a setting, and the person’s flips stay at zero`,
        s.room === room && s.shown.D === 1 && noRepeat(s.lantern.tried) && s.flips === 0, `settings ${s.lantern.tried.join(', ')}`);
      await follow(room + 1);
    }
    s = await state();
    expect('after room 4 comes a room drawn at random', s.room === 5 && /^Room 5$/.test((await text('#where')).trim()) && s.facesOk &&
      s.done.every((row) => row === null), `${s.open.length} open settings`);
    if (!still) {
      await until(() => window.rr.state().lantern.seeing && window.rr.state().lantern.phase === 'look' &&
        window.rr.state().lantern.z < -4, null, 60000).catch(() => {});
      const l = await lamp();
      await watch({ x: l.x, z: l.z }, l.y);
      await shot('5-random-room');
    }
    await until(() => window.rr.state().lantern.rooms >= 35 && window.rr.state().shown.D === 1, null, 240000);
    s = await state();
    expect('it opens the random room too', s.shown.D === 1 && noRepeat(s.lantern.tried), `settings ${s.lantern.tried.join(', ')}`);
    expect('no sideways scroll at the end', await narrow());
    expect('no page errors', errors.length === 0, errors.join(' | '));
  } catch (error) {
    await page.screenshot({ path: path.join(shotDir, `lantern-${name}-failed.png`) }).catch(() => {});
    check(`${name} ran to the end`, false, String(error.message || error).split('\n')[0]);
    if (errors.length) console.error(errors.join(' | '));
  } finally {
    await context.close();
  }
}
const pct = (v) => `${(100 * v).toFixed(1)}%`;

for (const spec of browsers.filter(({ name }) => !only || only === name)) {
  let browser;
  try {
    browser = await spec.launch();
    console.log(`\n${spec.name} ${browser.version()}${spec.still ? ' (reduce motion)' : ''}`);
    await walkBrowser(spec, browser);
  } catch (error) {
    check(`${spec.name} ran to the end`, false);
    console.error(error.stack || error);
  } finally {
    if (browser) await browser.close();
  }
}

console.log(`\n${passes} passed, ${failures} failed, ${screenshots} screenshots`);
process.exitCode = failures ? 1 : 0;
