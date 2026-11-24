// The skin study, checked: the wall is built only from its own paint; damage, mending and repainting; then pictures.
//   node skin/shots.mjs
import { createRequire } from 'node:module';
import { existsSync, mkdirSync, readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { toFloors, fromFloors } from './skincode.js';

const here = path.dirname(fileURLToPath(import.meta.url)), root = path.resolve(here, '..'), out = path.join(here, 'shots');
mkdirSync(out, { recursive: true });
let bad = 0, good = 0;
const check = (name, pass, detail = '') => { if (pass) good++; else bad++; console.log(`${pass ? 'PASS' : 'FAIL'} ${name}${detail ? '  (' + detail + ')' : ''}`); };

// the code itself, with no picture: every letter a tower can hold comes back, starting anywhere
check('the code alone: text to floors and back', ['1 switch', 'D door needs 2 wires +A +B -1 at 0 1.15 -4.95', 'x'.repeat(250)].every((text) => fromFloors([7, 0, 255, ...toFloors(text), ...toFloors(text)]) === text));
check('a swapped pair of letters is caught (a plain sum would miss it)', (() => { const f = toFloors('D door needs 2 wires +A +B -1'); [f[24], f[27]] = [f[27], f[24]]; return fromFloors(f) === null; })());
check('a spoiled floor is caught by the check floors', (() => { const f = toFloors('A lamp needs 1 wires +1 +2'); f[5] ^= 4; return fromFloors(f) === null; })());

const playwright = createRequire(path.resolve(process.env.CW_PLAYWRIGHT_ROOT || 'C:/Users/lilli/.codex/runtime/unfinished-island/node_modules', '..', 'package.json'))('playwright');
const threeDir = process.env.CW_THREE_DIR || 'C:/Users/lilli/AI-Shared/scratch/world2-remake/phase3/three/build';
const js = 'text/javascript; charset=utf-8';
const browser = await playwright.chromium.launch({ headless: true, channel: 'msedge' });
for (const [name, viewport, scale] of [['wide', { width: 1500, height: 860 }, 1], ['phone', { width: 390, height: 844 }, 2]]) {
  const context = await browser.newContext({ viewport, deviceScaleFactor: scale });
  await context.route('**/*', async (route) => {
    const url = new URL(route.request().url()), asset = url.pathname.match(/^\/npm\/three@0\.182\.0\/build\/(three\.(?:module|core)\.js)$/);
    if (url.hostname === 'cdn.jsdelivr.net' && asset) return route.fulfill({ status: 200, contentType: js, headers: { 'access-control-allow-origin': '*' }, body: readFileSync(path.join(threeDir, asset[1])) });
    if (url.host !== 'cw.test') return route.abort();
    const file = path.join(root, url.pathname.slice(1));
    return existsSync(file) ? route.fulfill({ status: 200, contentType: file.endsWith('.js') ? js : 'text/html; charset=utf-8', body: readFileSync(file) }) : route.fulfill({ status: 404 });
  });
  const page = await context.newPage(), errors = [];
  page.on('pageerror', (error) => errors.push(String(error)));
  await page.goto('http://cw.test/skin/study.html');
  try { await page.waitForFunction(() => window.study, null, { timeout: 15000 }); } catch (error) { check(`${name}: the page came up`, false, errors.join(' | ') || String(error).slice(0, 200)); await context.close(); continue; }
  const call = (fn, ...args) => page.evaluate(([f, a]) => window.study[f](...a), [fn, args]);
  const shot = async (label, views = [0]) => { for (const n of views) { await call('view', n); await page.waitForTimeout(120); await page.screenshot({ path: path.join(out, `skin-${name}-${label}${views.length > 1 ? '-' + (n + 1) : ''}.png`) }); } };

  const first = await page.evaluate(() => window.study.first);
  check(`${name}: the world read every surface it was handed`, first.read === first.of && first.unread === 0, `${first.read} of ${first.of}`);
  check(`${name}: every thing is where and what the maker meant`, first.propsRight === first.propsOf, `${first.propsRight} of ${first.propsOf}`);
  check(`${name}: picture against picture, the same dot for dot`, first.pictureSame === true);
  check(`${name}: with every lever up, both lamps glow and the door stays shut`, first.on.A === 1 && first.on.B === 1 && first.on.D === 0, JSON.stringify(first.on));
  check(`${name}: the things' codes, put together, build the same room`, await call('wholeRoom'));
  if (name === 'wide') for (const text of first.texts) console.log(`     read: "${text}"`);
  await shot('built-from-paint', [0, 1, 2]);

  await call('spoil', 'D', 'one'); let seen = await call('peek', 'D');
  check(`${name}: one tower on the door spoiled: the reader passes it over and reads the next`, seen.text === 'D door needs 2 wires +A +B -1 at 0 1.15 -4.95' && seen.tower === 1, JSON.stringify(seen));
  let now = await call('run'); seen = await call('peek', 'D');
  check(`${name}: and the world mends the paint from what it read`, seen.tower === 0 && now.read === now.of && now.mark === first.mark);

  await call('repaintOne', 'D', 'D door needs 2 wires +A +B +1'); seen = await call('peek', 'D');
  check(`${name}: one tower repainted to say something else, validly: the reader reports the disagreement and picks neither`, seen.text === null && Array.isArray(seen.conflict) && seen.conflict.length === 2, JSON.stringify(seen.conflict));
  now = await call('run');
  check(`${name}: the world will not guess: the door is not built while its towers disagree`, now.conflicts === 1 && now.on.D === undefined && now.read === now.of - 1, JSON.stringify(now.on));
  await shot('door-towers-disagree');
  await call('repaint', 'D', 'D door needs 2 wires +A +B -1'); now = await call('run');
  check(`${name}: painted whole again, the door is back as it was`, now.read === now.of && now.mark === first.mark && now.conflicts === 0);

  await call('spoil', 'B', 'all'); seen = await call('peek', 'B');
  check(`${name}: every tower on lamp B spoiled: it reads as nothing`, seen === null || seen.text === null, JSON.stringify(seen));
  now = await call('run');
  check(`${name}: the world no longer has lamp B, and the door cannot work without it`, now.unread === 1 && now.on.B === undefined && now.on.D === 'dead' && now.stuck.some((s) => s.id === 'D' && s.needs.includes('B')), JSON.stringify({ on: now.on, stuck: now.stuck }));
  await shot('lamp-b-unreadable');
  await call('repaint', 'B', 'B lamp needs 2 wires +2 +3'); now = await call('run');
  check(`${name}: painted again, lamp B is back and the room is as it was`, now.read === now.of && now.mark === first.mark && now.pictureSame);

  const windows = await call('repaint', 'D', 'D door needs 2 wires +A +B +1');
  now = await call('run', `<b>${windows} windows on each of the door's towers were repainted: its dark wire now reads as a bright one. The door opened.</b>`);
  check(`${name}: repainting ${windows} windows per tower on the door changed the door itself: it opened`, first.on.D === 0 && now.on.D === 1 && now.read === now.of, JSON.stringify(now.on));
  await shot('door-repainted', [0, 1]);
  check(`${name}: no page errors`, errors.length === 0, errors.join(' | '));
  await context.close();
}
await browser.close();
console.log(bad ? `\n${good} passed, ${bad} FAILED` : `\n${good} passed, 0 failed. Pictures in skin/shots`);
process.exit(bad ? 1 : 0);
