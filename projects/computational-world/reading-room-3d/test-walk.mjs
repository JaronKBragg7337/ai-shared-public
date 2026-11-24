// Walk the room with browser input. The page's test hook is used only for observation.
// node reading-room-3d/test-walk.mjs [--browser=iphone-webkit|edge] [--shots=all]
import assert from 'node:assert/strict';
import { createRequire } from 'node:module';
import { existsSync, mkdirSync, readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { ROOMS, codeText } from '../rooms.js';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.dirname(here);
const args = process.argv.slice(2);
const only = args.find((arg) => arg.startsWith('--browser='))?.split('=')[1];
assert(!only || ['iphone-webkit', 'edge'].includes(only), 'Unknown browser');
const allShots = args.includes('--shots=all');
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
if (offline) {
  assert.match(readFileSync(path.join(threeDir, 'three.core.js'), 'utf8'), /REVISION\s*=\s*['"]182['"]/);
  console.log(`Three.js r182 served from ${threeDir}`);
} else {
  assert(!process.env.CW_THREE_DIR, `CW_THREE_DIR needs both Three.js build files: ${threeDir}`);
  console.log('Three.js r182 served by jsDelivr');
}

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
  { name: 'iphone-webkit', launch: () => playwright.webkit.launch({ headless: true, executablePath: webkitPath }),
    viewport: { width: 375, height: 812 },
    userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1' },
  { name: 'edge', launch: () => playwright.chromium.launch({ headless: true, channel: 'msedge' }),
    viewport: { width: 390, height: 844 } },
];
const contextOptions = ({ viewport, userAgent }) => ({ viewport, userAgent, deviceScaleFactor: 2, isMobile: true, hasTouch: true });
const distance = (a, b) => Math.hypot(a.x - b.x, a.z - b.z);
const angle = (v) => Math.atan2(Math.sin(v), Math.cos(v));
const bearing = (from, to) => Math.atan2(to.x - from.x, from.z - to.z);
const nearly = (a, b, tolerance = 0.02) => Math.abs(a - b) < tolerance;
const shotDir = path.join(here, 'screenshots');
let passes = 0;
let failures = 0;
let screenshots = 0;

function check(name, passed, details = '') {
  if (passed) passes++;
  else failures++;
  console.log(`${passed ? 'PASS' : 'FAIL'} ${name}${details ? ` (${details})` : ''}`);
}

async function startPage(context) {
  await serve(context);
  const page = await context.newPage();
  page.setDefaultTimeout(12000);
  const errors = [];
  page.on('pageerror', (error) => errors.push(String(error)));
  page.on('console', (message) => { if (message.type() === 'error') errors.push(message.text()); });
  const start = Date.now();
  await page.goto('http://cw.test/reading-room-3d/');
  await page.waitForFunction(() => window.rr?.state()?.room === 1);
  return { page, errors, loadMs: Date.now() - start };
}

async function touchDrag(spec, context, page) {
  const isWebKit = spec.name === 'iphone-webkit';
  // Playwright's public WebKit touchscreen only taps. The installed WebKit
  // exposes a native drag on its page proxy, with a touch ID even on release.
  const session = isWebKit ? page._connection.toImpl(page).delegate._pageProxySession : await context.newCDPSession(page);
  const send = (type, x, y) => session.send('Input.dispatchTouchEvent', {
    type, touchPoints: type === 'touchEnd' && !isWebKit ? [] : [{ x, y, id: 1 }],
  });
  return async (x, y, dx, dy, ms = 0) => {
    await send('touchStart', x, y);
    try {
      await send('touchMove', Math.round(x + dx / 2), Math.round(y + dy / 2));
      await send('touchMove', x + dx, y + dy);
      if (ms) await page.waitForTimeout(ms);
    } finally {
      await send('touchEnd', x + dx, y + dy);
    }
  };
}

function controls(page) {
  const width = page.viewportSize().width;
  const height = page.viewportSize().height;
  const state = () => page.evaluate(() => window.rr.state());
  const positions = () => page.evaluate(() => window.rr.pos());
  const tap = (id) => page.locator(id).tap();
  const quiet = () => page.waitForFunction(() => window.rr.state().settled);
  const untilPosition = (test, value) => page.waitForFunction(test, value, { timeout: 10000 });

  async function hold(key, until) {
    await page.keyboard.down(key);
    try {
      if (typeof until === 'number') await page.waitForTimeout(until);
      else await until();
    } finally {
      await page.keyboard.up(key);
    }
  }

  async function mouseLook(dx, dy = 0) {
    const x = Math.round(width / 2 - dx / 2);
    const y = Math.round(height * 0.43 - dy / 2);
    await page.mouse.move(x, y);
    await page.mouse.down();
    try {
      await page.mouse.move(x + dx, y + dy);
    } finally {
      await page.mouse.up();
    }
  }

  async function turn(yaw, pitch) {
    for (let attempt = 0; attempt < 8; attempt++) {
      const from = await state();
      const dx = angle(yaw - from.yaw);
      const dy = pitch === undefined ? 0 : from.pitch - pitch;
      // The house control ignores a mouse drag of 7 pixels or less.
      if (Math.abs(dx) < 0.038 && Math.abs(dy) < 0.038) return;
      const dragX = Math.max(-220, Math.min(220, Math.round(dx / 0.0045)));
      const dragY = Math.max(-160, Math.min(160, Math.round(dy / 0.0045)));
      await mouseLook(dragX, dragY);
      await page.waitForTimeout(25);
    }
    const s = await state();
    throw new Error(`Could not turn to ${yaw.toFixed(3)} (${s.yaw.toFixed(3)}) and pitch ${pitch} (${s.pitch})`);
  }

  async function goTo(target) {
    for (let attempt = 0; attempt < 6; attempt++) {
      const from = await state();
      if (distance(from, target) < 0.22) return;
      const yaw = bearing(from, target);
      await turn(yaw, -0.04);
      await hold('w', () => page.waitForFunction(({ origin, target, yaw }) => {
        const s = window.rr.state();
        const length = Math.hypot(origin.x - target.x, origin.z - target.z);
        const forward = (s.x - origin.x) * Math.sin(yaw) + (origin.z - s.z) * Math.cos(yaw);
        return forward >= length - 0.12;
      }, { origin: { x: from.x, z: from.z }, target, yaw }, { timeout: 10000 }));
    }
    throw new Error(`Could not walk to ${JSON.stringify(target)} from ${JSON.stringify(await state())}`);
  }

  async function face(id) {
    const map = await positions();
    const target = map[id];
    let spot;
    if (id === 'D') spot = { x: Math.max(0, target.x - 0.6), z: target.z + 2.65 };
    else if (id === 'shelf') spot = { x: target.x + 0.3, z: target.z + 2.2 };
    else spot = { x: target.x - Math.sign(target.x) * 2.15, z: target.z };
    // The aisle stays clear even when corner furniture lies on the direct line.
    const from = await state();
    if (distance(from, spot) > 0.5) await goTo(spot);
    const s = await state();
    const aimPitch = Math.atan2((target.aimY ?? 1.45) - 1.6, distance(s, target));
    await turn(bearing(s, target), aimPitch);
    await page.waitForFunction((name) => window.rr.state().facing === name, id);
  }

  async function tapWorld(target) {
    const s = await state();
    await turn(bearing(s, target), Math.atan2(target.y - 1.6, distance(s, target)));
    await page.touchscreen.tap(Math.round(width / 2), Math.round(height / 2));
  }

  async function goThrough() {
    const { doorway } = await positions();
    await goTo({ x: doorway.x, z: doorway.z + 1.25 });
    await turn(0, -0.04);
    await hold('ArrowUp', () => page.waitForFunction(() => window.rr.state().through));
  }

  return { state, positions, tap, quiet, hold, mouseLook, turn, goTo, face, tapWorld, goThrough, untilPosition };
}

async function walkBrowser(spec, browser) {
  const { name, viewport } = spec;
  const expect = (label, passed, details) => check(`${name} ${label}`, passed, details);
  const context = await browser.newContext(contextOptions(spec));
  const { page, errors, loadMs } = await startPage(context);
  const { state, positions, tap, quiet, hold, mouseLook, turn, goTo, face, tapWorld, goThrough, untilPosition } = controls(page);
  const text = (id) => page.locator(id).innerText();
  const shown = (id) => page.locator(id).isVisible();
  const narrow = () => page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth && window.scrollY === 0);
  const roomShots = name === 'iphone-webkit' || only === 'edge' || allShots;
  let maxCalls = 0, maxTriangles = 0;
  async function shot(label, room = false) {
    await page.waitForFunction(() => window.rr.state().render.decorated);
    const { render } = await state();
    maxCalls = Math.max(maxCalls, render.calls);
    maxTriangles = Math.max(maxTriangles, render.triangles);
    if (room && !roomShots) return;
    mkdirSync(shotDir, { recursive: true });
    await page.screenshot({ path: path.join(shotDir, `${name}-${label}.png`), animations: 'disabled' });
    screenshots++;
  }

  const initial = await state();
  const map = await positions();
  expect('loads room 1 at eye-level facing forward', initial.room === 1 && distance(initial, map.start) < 0.1 && nearly(initial.yaw, 0), `${loadMs} ms to room state`);
  expect('shows Room 1 of 4 and zero flips', (await text('#where')).includes('Room 1 of 4') && (await text('#flips')).includes('0 flips'));
  expect('fits the phone without sideways scroll', await narrow(), `${viewport.width} × ${viewport.height}`);
  await shot('room-1-start', true);

  try {
    await hold('w', 410);
    const released = await state();
    await page.waitForTimeout(180);
    expect('W walks forward and releasing stops', initial.z - released.z > 0.45 && distance(released, await state()) < 0.02,
      `${(initial.z - released.z).toFixed(2)} m`);
    await hold('s', () => untilPosition(() => window.rr.state().z > -0.29));
    await hold('s', 320);
    const backWall = await state();
    await hold('ArrowDown', 300);
    const heldBack = await state();
    expect('the near wall stops backward walking', [backWall.z, heldBack.z].every((z) => z <= -0.23 && z > -0.30),
      `${(-heldBack.z).toFixed(2)} m from the wall`);
    await hold('ArrowRight', 300);
    let s = await state();
    expect('the right arrow turns right', angle(s.yaw - backWall.yaw) > 0.15);
    await mouseLook(-84);
    const mouseYaw = (await state()).yaw;
    expect('a real mouse drag looks left', angle(mouseYaw - s.yaw) < -0.15);
    await turn(0, -0.04);

    const drag = await touchDrag(spec, context, page);
    const beforeStick = await state();
    await drag(78, viewport.height - 116, 0, -55, 400);
    const afterStick = await state();
    await page.waitForTimeout(180);
    expect('a real left finger drag walks and release stops', beforeStick.z - afterStick.z > 0.3 && distance(afterStick, await state()) < 0.02,
      `${(beforeStick.z - afterStick.z).toFixed(2)} m`);
    await drag(255, 462, 72, 0);
    const afterLook = await state();
    expect('a real right finger drag turns without walking', angle(afterLook.yaw - afterStick.yaw) > 0.25 && distance(afterLook, afterStick) < 0.02);
    expect('finger drags leave the page in place', await narrow());
    await page.touchscreen.tap(78, viewport.height - 125);
    await page.waitForTimeout(150);
    expect('a tap on the floor leaves the player in place', distance(afterLook, await state()) < 0.02);
    await turn(0, -0.04);

    await goTo({ x: 0, z: map.doorway.z + 0.8 });
    await turn(0, -0.04);
    await hold('ArrowUp', 750);
    const shut = await state();
    expect('up arrow cannot go through a shut door', shut.z > map.doorway.z && shut.z < map.doorway.z + 0.7 && !shut.through && shut.doorProgress === 0,
      `stopped ${(shut.z - map.doorway.z).toFixed(2)} m before the doorway`);
    await face('D');
    await shot('room-1-door-shut', true);
    expect('room 1 starts with a shut door', (await state()).doorProgress === 0 && !(await shown('#hint')));
    await goTo({ x: 0, z: map.start.z });
    await turn(0, -0.04);
    await hold('a', () => untilPosition(() => window.rr.state().x < -3.70));
    await hold('a', 320);
    const sideWall = await state();
    await hold('a', 260);
    const heldSide = await state();
    // Collisions stop travel into a wall and still allow sliding along it.
    expect('the side wall stops strafing into the wall', [sideWall.x, heldSide.x].every((x) => x >= -3.77 && x < -3.70),
      `${(4 + heldSide.x).toFixed(2)} m from the wall`);

    const flip = async (id, method = 'tap') => {
      await face(id);
      if (method === 'tap') await tap('#use');
      else await page.keyboard.press(method);
      await quiet();
    };

    for (let room = 1; room <= 4; room++) {
      const definition = ROOMS[room - 1];
      const lampText = `${codeText([definition.things.find((part) => part.id === 'A')])} at 3.78 1.48 -2.7`;
      s = await state();
      expect(`room ${room} starts clean and its card marks match the painted rules`, s.room === room && s.facesOk && s.flips === 0 && s.asks === 0);
      expect(`room ${room} reads every painted surface without conflicts`,
        s.skins.read === s.skins.of && s.skins.of === definition.things.length + 19 && s.skins.conflicts === 0,
        `${s.skins.read}/${s.skins.of} read, ${s.skins.conflicts} conflicts`);
      if (room > 1) await shot(`room-${room}-start`, true);

      if (room === 1) {
        await face('1');
        expect('walking up and facing switch 1 shows its card', /Switch 1/.test(await text('#card')) && await shown('#use'));
        await tap('#use');
        const first = await state();
        const moving = first.wireMotion > 0 || await page.waitForFunction(() => window.rr.state().wireMotion > 0,
          null, { timeout: 400 }).then(() => true, () => false);
        expect('a real Flip it tap turns switch 1 on and starts a travelling wave', first.on['1'] === 1 && first.flips === 1 && moving && !first.settled);
        await quiet();
        expect('switch words show the live setting', /It is ON\..*sends light to Lamp A/.test(await text('#words')));
        await face('2');
        await tap('#use');
        const beforeArrival = await state();
        const betweenLevels = await page.waitForFunction(() => {
          const { shown, wireMotion } = window.rr.state();
          return shown.A === 1 && shown.D === 0 && wireMotion > 0;
        }, null, { timeout: 2500 }).then(() => true, () => false);
        await quiet();
        const afterArrival = await state();
        expect('the lamp and door light one level at a time after the pulse reaches them',
          beforeArrival.shown.A === 0 && betweenLevels && afterArrival.shown.A === 1 && afterArrival.shown.D === 1);
      }

      if (room === 2) {
        for (const id of ['1', '2', '3']) await flip(id);
        const allOn = await state();
        expect('room 2 all on lights both lamps and keeps the door shut', allOn.shown.A === 1 && allOn.shown.B === 1 && allOn.shown.D === 0);
      }

      if (room === 3) {
        await face('B');
        expect('room 3 shows the skin and marks before asking for words',
          await shown('#skin-text') && await shown('#face') && !(await shown('#words')) && await shown('#ask'));
        await tap('#ask');
        await page.locator('#words').waitFor({ state: 'visible' });
        expect('Read it to me reveals the rule and counts once', (await state()).asks === 1 && /dark wire, from Switch 3/.test(await text('#words')));
        await flip('1', 'e');
        const on = await state();
        await flip('1', 'Enter');
        const off = await state();
        expect('E and Enter use the switch you face', on.on['1'] === 1 && off.on['1'] === 0 && off.flips === 2);
      }

      if (room !== 1) {
        await face('D');
        if (room === 2) {
          const words = await text('#words');
          const fitsCard = await page.locator('#words').evaluate((paragraph) => paragraph.scrollHeight <= paragraph.clientHeight + 1);
          const dashed = await page.locator('#face svg circle[stroke-dasharray]').count();
          expect('room 2 shut door shows its full dark-wire explanation without scrolling', dashed === 1 &&
            /dark wire, from Switch 1/.test(words) && /add up to 1.*shut/.test(words) && fitsCard && !(await shown('#hint')));
        }
        await shot(`room-${room}-door-shut`, true);
      }

      s = await state();
      const solution = s.open[0];
      assert(Number.isInteger(solution), `Room ${room} has no open setting`);
      for (const thing of definition.things.filter((part) => part.kind === 'switch')) {
        const wanted = (solution >> (Number(thing.id) - 1)) & 1;
        if (s.on[thing.id] !== wanted) await flip(thing.id);
      }
      await page.waitForFunction(() => window.rr.state().doorProgress >= 0.99);
      s = await state();
      expect(`room ${room} opens by walking to the solution`, s.shown.D === 1 && s.flips === [2, 4, 5, 4][room - 1],
        `${s.flips} flips, fewest ${s.best}, blind ${s.blind.toFixed(1)}`);

      await face('A');
      expect(`room ${room} lamp card leads with the exact text read off its skin`,
        await text('#card .card-content > :first-child q#skin-text') === lampText);
      if (room <= 2) expect(`room ${room} lamp card shows its live sum`, /Right now they add up to \d+.*LIT/.test(await text('#words')));
      else expect(`room ${room} lamp card shows marks and offers the words`, await shown('#face') && !await shown('#words') && await shown('#ask'));
      if (room === 1) {
        const squares = await page.locator('#face svg rect[fill="currentColor"]').count();
        const circles = await page.locator('#face svg circle[fill="currentColor"]').count();
        const lamp = (await positions()).A;
        const standDistance = distance(await state(), lamp);
        expect('the lit lamp card has two needs squares and two filled wires at a natural standing distance',
          squares === 2 && circles === 2 && standDistance > 1.9 && standDistance < 2.4, `${standDistance.toFixed(2)} m`);
      }
      await shot(`room-${room}-lamp-skin`, true);
      if (room === 1) {
        const lamp = (await positions()).A;
        await goTo({ x: lamp.x - 3.75, z: lamp.z });
        const from = await state();
        const range = distance(from, lamp);
        await turn(bearing(from, lamp), Math.atan2(lamp.aimY - 1.6, range));
        expect('the across-aisle lamp view is beyond card range', range > 3.5 && range < 4 && !await shown('#card'), `${range.toFixed(2)} m`);
        await shot('room-1-lamp-skin-across-aisle', true);
      }

      await face('D');
      expect(`room ${room} open door says to walk through`, await shown('#hint') && /The door is open\. Walk (?:up )?through it\./.test(await text('#hint')));
      const door = (await positions()).doorway;
      const openView = await state();
      await turn(bearing(openView, door), -0.06);
      await shot(`room-${room}-door-open`, true);

      await face('shelf');
      if (room === 1) {
        const shelf = (await positions()).shelf;
        await turn(0, -0.04);
        await hold('w', () => untilPosition((z) => window.rr.state().z < z + 0.42, shelf.z));
        await hold('w', 320);
        const stopped = await state();
        await hold('w', 300);
        const heldAtShelf = await state();
        expect('the bookshelf stops walking before its back wall', [stopped.z, heldAtShelf.z].every((z) => z > shelf.z + 0.32 && z < shelf.z + 0.42),
          `${(heldAtShelf.z - shelf.z).toFixed(2)} m from the shelf aim`);
        await goTo({ x: shelf.x + 0.3, z: shelf.z + 2.2 });
        await face('shelf');
        for (const [index, title] of ['How to read the marks', "This room's history", 'What the world read off its things'].entries()) {
          await tapWorld(shelf.books[index]);
          expect(`tapping the 3D book ${index + 1} opens its own pages`, await text('#book-title') === title);
          await tap('#shut');
        }
        await face('shelf');
      }
      if (room === 1 || room === 3) {
        await tap('#b1');
        expect(`room ${room} book 1 opens at page 1 of 3`, /How to read the marks/.test(await text('#book')) && /Page 1 of 3/.test(await text('#book')));
        await tap('#nextp');
        await tap('#nextp');
        expect(`room ${room} book 1 turns to its last page`, /Page 3 of 3/.test(await text('#book')) && await page.locator('#nextp').isDisabled());
        if (room === 1) await shot('room-1-book', true);
        await tap('#shut');
        await tap('#b2');
        expect(`room ${room} book 2 records the first flip`, /1\. Switch [1-5] turned on/.test(await text('#book')));
        await tap('#nextp');
        expect(`room ${room} book 2 has a check number`, /Check number: [0-9a-f]{8}/.test(await text('#book')));
        await tap('#shut');
        await tap('#b3');
        const lines = (await text('#code')).split('\n');
        const ruleLines = lines.slice(0, definition.things.length);
        expect(`room ${room} book 3 shows the rules and room surfaces read from paint`,
          ruleLines.map((line) => line.split(' at ')[0]).join('\n') === codeText(definition.things) &&
          ruleLines.includes(lampText) && lines.length === s.skins.of && new Set(lines).size === lines.length &&
          lines.some((line) => line.startsWith('wall at ') && line.includes(' size ')) &&
          lines.some((line) => line.startsWith('floor at ') && line.includes(' size ')) &&
          lines.some((line) => line.startsWith('book 3 skins at ')) &&
          lines.some((line) => line.startsWith('lantern stand at ')));
        await tap('#rebuild');
        expect(`room ${room} rebuilt from the code and history says Same room`, /Same room\./.test(await text('#same')));
        if (room === 3) await shot('room-3-book', true);
        await tap('#shut');
      } else {
        await tap(room === 2 ? '#b2' : '#b3');
        await shot(`room-${room}-book`, true);
        await tap('#shut');
      }

      await goThrough();
      s = await state();
      expect(`room ${room} completes by walking through the open door`, s.through && s.done[room - 1]?.flips === [2, 4, 5, 4][room - 1]);
      const result = page.getByText(`You opened Room ${room} in ${s.flips} flips.`, { exact: true });
      expect(`room ${room} shows the flip comparison`, await result.isVisible() &&
        await page.getByText(new RegExp(`The fewest possible is ${s.best}.*about ${Math.round(s.blind)} on average`)).isVisible());
      if (room < 4) await tap('#next');
    }

    expect('the final reading lists all four rooms', await page.locator('#logbody tr').count() === 4 && await shown('#copy'));
    const raw = await text('#raw');
    expect('the copy line includes the four runs and the room 3 ask', /r1 flips=2 best=2 .*r2 flips=4 best=2 .*r3 flips=5 best=3 .*asked=1 .*r4 flips=4 best=4 .*asked=0/.test(raw));
    await tap('#copy');
    await page.waitForFunction(() => document.querySelector('#copied')?.textContent.trim());
    expect('Copy my results gives feedback', !!(await text('#copied')).trim());
    expect('end still fits with no sideways scroll', await narrow());
    await shot('results');
    await tap('#again');
    expect('Start again resets the room and clears the result', (await state()).room === 1 && (await state()).flips === 0 && !(await shown('#log')));

    expect('no page errors', errors.length === 0, errors.join(' | '));
    const { render } = await state();
    console.log(`${name} screenshot samples: up to ${maxCalls} draw calls, ${maxTriangles} triangles, ${render.tier}, pixel ratio ${render.pixelRatio}`);
  } catch (error) {
    await shot('failed').catch(() => {});
    if (errors.length) console.error(errors.join(' | '));
    throw error;
  } finally {
    await context.close();
  }
}

async function reducedMotion(spec, browser) {
  const context = await browser.newContext({ ...contextOptions(spec), reducedMotion: 'reduce' });
  try {
    await context.addInitScript(() => {
      Object.defineProperty(navigator, 'deviceMemory', { configurable: true, value: 2 });
    });
    const { page, errors } = await startPage(context);
    const { state, positions, face, tap, tapWorld } = controls(page);
    const { render, skins } = await state();
    check(`${spec.name} the smallest textures still read every skin`,
      render.tier === 'mobile-lite' && skins.read === 23 && skins.of === 23 && skins.conflicts === 0);
    await tapWorld((await positions())['1'].lever);
    check(`${spec.name} a distant tap on the lever does not flip it`, (await state()).flips === 0);
    await face('1');
    await tapWorld((await positions())['1'].lever);
    const first = await state();
    check(`${spec.name} a real tap on the nearby 3D lever flips switch 1`, first.on['1'] === 1 && first.flips === 1);
    await face('2');
    await tap('#use');
    const second = await state();
    check(`${spec.name} reduced motion updates the wires, lamp and door without a wave or swing`,
      first.wireMotion === 0 && first.settled && second.wireMotion === 0 && second.settled &&
      second.shown.A === 1 && second.shown.D === 1 && second.doorProgress === 1 && errors.length === 0);
  } finally {
    await context.close();
  }
}

// An iPhone reports four processor cores, which the house tier file reads as its lite tier. This room is small,
// so such a phone still gets the full look and the full-size paint; only a phone short on memory gets the small one.
async function fourCores(spec, browser) {
  const context = await browser.newContext(contextOptions(spec));
  try {
    await context.addInitScript(() => {
      Object.defineProperty(navigator, 'hardwareConcurrency', { configurable: true, get: () => 4 });
    });
    const { page, errors } = await startPage(context);
    const house = await page.evaluate(() => window.HBDevice.tier);
    const { render, skins, facesOk } = await controls(page).state();
    check(`${spec.name} a four-core phone (as an iPhone reports) still gets the full paint, and every skin reads`,
      house === 'mobile-lite' && render.tier === 'mobile-high' && render.paint === 'full' &&
      skins.read === 23 && skins.of === 23 && skins.conflicts === 0 && facesOk && errors.length === 0,
      `house ${house}, room ${render.tier}, paint ${render.paint}, made in ${render.madeMs} ms`);
  } finally {
    await context.close();
  }
}

for (const spec of browsers.filter(({ name }) => !only || only === name)) {
  let browser;
  try {
    browser = await spec.launch();
    console.log(`\n${spec.name} ${browser.version()}`);
    await walkBrowser(spec, browser);
    await reducedMotion(spec, browser);
    await fourCores(spec, browser);
  } catch (error) {
    check(`${spec.name} ran to the end`, false);
    console.error(error.stack || error);
  } finally {
    if (browser) await browser.close();
  }
}

console.log(`\n${passes} passed, ${failures} failed, ${screenshots} screenshots`);
process.exitCode = failures ? 1 : 0;
