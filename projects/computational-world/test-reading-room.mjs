// The Reading Room, checked two ways.
//   1. In Node, no browser: every room can be opened; a second engine agrees on every setting; the "flipping blind" average
//      is confirmed by playing it out on the real machine; the marks and the code page both give back the whole room.
//   2. In two phone-sized browsers (an iPhone-profile WebKit at 375 px, Edge at 390 px) with real input: walk with the pad
//      and the keys, flip switches with real taps, read things, open the three books, and go through all four doors.
// No server: the browsers are handed the project's own files.   node test-reading-room.mjs [shots-folder] [--no-browser]
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { DenseEngine, Chronicle, stateMark, rng } from './world.js';
import { ROOMS, buildRoom, marksOf, thingFromMarks, codeText, parseCode, openSettings, fewestFlips, blindAverage, settingText } from './rooms.js';

const here = path.dirname(fileURLToPath(import.meta.url)), args = process.argv.slice(2), noBrowser = args.includes('--no-browser');
const shots = args.find((a) => !a.startsWith('--')) || path.join(here, 'results', 'shots');
fs.mkdirSync(shots, { recursive: true });
let bad = 0, good = 0; const ok = (name, pass, detail = '') => { if (pass) good++; else bad++; console.log((pass ? 'PASS ' : 'FAIL ') + name + (pass ? '' : '  ' + detail)); };
const out = { made: new Date().toISOString(), rooms: [], browsers: {} };

// ---------------------------------------------------------------- 1. the rooms themselves
ROOMS.forEach((def, i) => {
  const name = `room ${i + 1}`, r = buildRoom(def.things), n = r.switches.length, door = r.at[r.door.id], open = openSettings(def.things);
  ok(`${name}: can be opened`, open.length >= 1);
  let agree = true; const openDense = [];                       // a second engine (every part, one pass) on every setting
  for (let mask = 0; mask < (1 << n); mask++) {
    const D = new DenseEngine(r.W), E = buildRoom(def.things);
    for (let b = 0; b < n; b++) if ((mask >> b) & 1) { D.set(r.at[r.switches[b].id], 1); E.E.set(E.at[E.switches[b].id], 1); }
    D.sweep(); if (D.out[door]) openDense.push(mask);
    for (let p = 0; p < r.W.P; p++) if (D.out[p] !== E.E.out[p]) agree = false;
  }
  ok(`${name}: a second engine agrees on every one of its ${1 << n} settings`, agree && JSON.stringify(openDense) === JSON.stringify(open));
  const best = fewestFlips(open), exact = blindAverage(open, n);
  const rand = rng(5150 + i), runs = 40000, sim = buildRoom(def.things), set = new Uint8Array(n); let total = 0;   // the blind flipper, played out
  for (let k = 0; k < runs; k++) {
    for (let b = 0; b < n; b++) if (set[b]) { set[b] = 0; sim.E.set(sim.at[sim.switches[b].id], 0); }
    while (!sim.E.out[door]) { const b = (rand() * n) | 0; set[b] ^= 1; sim.E.set(sim.at[sim.switches[b].id], set[b]); total++; }
  }
  const played = total / runs;
  ok(`${name}: flipping blind takes ${exact.toFixed(2)} flips on average (worked out), ${played.toFixed(2)} (played out ${runs} times)`, Math.abs(played - exact) / exact < 0.03);
  const round = def.things.map((t) => thingFromMarks(marksOf(t, 0)));
  ok(`${name}: the marks give back the whole list`, codeText(round) === codeText(def.things));
  ok(`${name}: the code page reads back the same`, codeText(parseCode(codeText(def.things))) === codeText(def.things));
  const live = buildRoom(def.things), chron = new Chronicle(), r2 = rng(77 + i);
  for (let k = 0; k < 300; k++) { const p = live.at[live.switches[(r2() * n) | 0].id], v = live.E.out[p] ? 0 : 1; live.E.set(p, v); chron.add(p, v); }
  const again = buildRoom(parseCode(codeText(round))); chron.replay((p, v) => again.E.set(p, v));
  ok(`${name}: rebuilt from its marks and 300 changes of history, it is the same room`,
    stateMark(again.E.out) === stateMark(live.E.out) && again.E.out.every((v, j) => v === live.E.out[j]) && Chronicle.chainOf(chron.buf, chron.n) === chron.chain);
  out.rooms.push({ room: i + 1, switches: n, wordsShown: def.words, opensWith: open.map((m) => settingText(m, n)), fewestFlips: best, blindAverageWorkedOut: Number(exact.toFixed(3)),
    blindAveragePlayedOut: Number(played.toFixed(3)), tryEverySettingWorstCase: (1 << n) - 1, turningEverythingOnOpensIt: open.includes((1 << n) - 1) });
  console.log(`     ${name}: ${n} switches, opens with ${open.map((m) => settingText(m, n)).join(' ; ')}. Reading: ${best} flips. Blind: ${exact.toFixed(1)} on average.`);
});

// ---------------------------------------------------------------- 2. the page, with real input
if (!noBrowser) {
  const pw = createRequire(process.env.CW_PLAYWRIGHT_ROOT || 'C:/Users/lilli/.codex/runtime/unfinished-island/node_modules/')('playwright');
  const WEBKIT = process.env.CW_WEBKIT || path.join(process.env.LOCALAPPDATA || '', 'ms-playwright', 'webkit-2336', 'Playwright.exe');
  const IPHONE = { userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
    viewport: { width: 375, height: 812 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true };
  const TYPES = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8' };
  const serve = (ctx) => ctx.route('**/*', (route) => {
    const u = new URL(route.request().url());
    if (u.hostname !== 'cw.test') return route.abort();                        // fonts and anything else: the page must work without them
    const f = path.join(here, u.pathname.slice(1));
    return fs.existsSync(f) ? route.fulfill({ status: 200, contentType: TYPES[path.extname(f)] || 'text/plain', body: fs.readFileSync(f) }) : route.fulfill({ status: 404, body: '' });
  });
  for (const [name, launch, ctxOpts] of [
    ['iphone-webkit', () => pw.webkit.launch({ headless: true, executablePath: WEBKIT }), IPHONE],
    ['edge', () => pw.chromium.launch({ headless: true, channel: 'msedge' }), { viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, hasTouch: true, isMobile: true }],
  ]) {
    let browser;
    try {
      browser = await launch();
      const ctx = await browser.newContext(ctxOpts), errors = []; await serve(ctx);
      const page = await ctx.newPage(); page.setDefaultTimeout(45000);
      page.on('pageerror', (e) => errors.push(String(e)));
      page.on('console', (m) => { if (m.type() === 'error' && !/Failed to load resource|net::ERR|fonts\.g/.test(m.text())) errors.push(m.text()); });
      await page.goto('http://cw.test/reading-room.html'); await page.waitForFunction(() => window.rr);
      const st = () => page.evaluate(() => window.rr.state()), where = () => page.evaluate(() => window.rr.pos());
      const tap = (sel) => page.tap(sel), cardText = () => page.locator('#card').innerText(), bookText = () => page.locator('#book').innerText();
      const quiet = () => page.waitForFunction(() => window.rr.state().settled);
      const narrow = () => page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth);
      const shot = (label, full = false) => page.screenshot({ path: path.join(shots, `rr-${name}-${label}.png`), fullPage: full });
      async function walkX(tx, tol = 0.3) {                                      // hold an arrow key until there, then small nudges
        for (let tries = 0; tries < 14; tries++) {
          const s = await st(), d = tx - s.x; if (Math.abs(d) <= tol) return;
          const key = d > 0 ? 'ArrowRight' : 'ArrowLeft';
          await page.keyboard.down(key);
          if (Math.abs(d) > 0.7) await page.waitForFunction(([t, dir]) => dir * (window.rr.state().x - t) >= -0.15, [tx, Math.sign(d)]); else await page.waitForTimeout(Math.max(20, Math.abs(d) / 3.6 * 600));
          await page.keyboard.up(key); await page.waitForTimeout(40);
        }
      }
      const goTo = async (id) => { const p = await where(); await walkX(id === 'doorway' ? p.doorway : p[id]); if (id !== 'doorway') await page.waitForFunction((i) => window.rr.state().facing === i, id); };
      const flipSwitch = async (id) => { await goTo(id); await tap('#use'); await quiet(); };
      const goThrough = async () => { await goTo('doorway'); await page.keyboard.down('ArrowUp'); await page.waitForFunction(() => window.rr.state().through); await page.keyboard.up('ArrowUp'); await page.waitForTimeout(80); };
      const solve = async () => { const s = await st(); for (let b = 0; b < 8; b++) if ((s.open[0] >> b) & 1) await flipSwitch(String(b + 1)); };

      // ---- room 1: the start
      let s = await st();
      ok(`${name}: the first card is there the moment the page is`, (await page.locator('#card').innerText()).length > 0);
      ok(`${name}: starts in room 1, facing nothing, and says how to walk`, s.room === 1 && s.facing === null && (await cardText()).includes('Walk up to something'), JSON.stringify(s));
      ok(`${name}: no sideways scroll`, await narrow());
      ok(`${name}: the faces alone give back room 1's list`, s.facesOk === true);
      await shot('1-start');

      // ---- the walking pad, each way a finger or mouse can reach it
      const box = await page.locator('#stick').boundingBox(), cx = box.x + box.width / 2, cy = box.y + box.height / 2;
      const moved = async (press, release) => { const a = (await st()).x; await press(); await page.waitForTimeout(350); const b = (await st()).x; await release(); await page.waitForTimeout(120); const c = (await st()).x; await page.waitForTimeout(150); return { went: b - a, drift: (await st()).x - c }; };
      let m = await moved(async () => { await page.mouse.move(cx, cy); await page.mouse.down(); await page.mouse.move(cx + 44, cy, { steps: 3 }); }, () => page.mouse.up());
      ok(`${name}: dragging the pad walks you (pointer), and letting go stops you`, m.went > 0.5 && Math.abs(m.drift) < 0.01, JSON.stringify(m));
      const fake = (type, dx) => page.evaluate(([t, x, y, d]) => {
        const el = document.getElementById('stick'); let touches = [];
        if (t !== 'touchend') touches = [new Touch({ identifier: 7, target: el, clientX: x + d, clientY: y })];
        el.dispatchEvent(new TouchEvent(t, { touches, targetTouches: touches, changedTouches: touches, bubbles: true, cancelable: true }));
      }, [type, cx, cy, dx]);
      try {
        m = await moved(async () => { await fake('touchstart', -10); await fake('touchmove', -44); }, () => fake('touchend', 0));
        ok(`${name}: dragging the pad walks you (touch events), and letting go stops you`, m.went < -0.5 && Math.abs(m.drift) < 0.01, JSON.stringify(m));
      } catch (e) { console.log(`     ${name}: this browser build cannot make a touch event by hand (${String(e).slice(0, 80)}); the pointer and finger checks stand in`); }
      if (name === 'edge') {
        const cdp = await ctx.newCDPSession(page);                               // a real finger, as far as a desktop browser can make one
        m = await moved(async () => { await cdp.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x: cx, y: cy }] }); await cdp.send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [{ x: cx + 44, y: cy }] }); },
          () => cdp.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] }));
        ok(`${name}: a real finger drag on the pad walks you, and lifting it stops you`, m.went > 0.5 && Math.abs(m.drift) < 0.01, JSON.stringify(m));
        const scrolled = await page.evaluate(() => window.scrollY);
        ok(`${name}: dragging the pad does not scroll the page`, scrolled === 0, String(scrolled));
      }

      // ---- room 1: read, flip, books, door
      await flipSwitch('1'); s = await st();
      ok(`${name}: a real tap on "Flip it" turns switch 1 on`, s.on['1'] === 1 && s.flips === 1, JSON.stringify(s.on));
      ok(`${name}: the switch reads itself out in words`, /It is ON\. While it is on, it sends light to Lamp A\./.test(await cardText()), await cardText());
      await flipSwitch('2'); s = await st();
      ok(`${name}: both switches on: lamp A is lit and the door is open`, s.shown.A === 1 && s.shown.D === 1);
      ok(`${name}: the flip count says 2`, (await page.locator('#flips').innerText()).trim() === '2 flips');
      await goTo('A');
      ok(`${name}: the lamp reads itself out, with its live sum`, /I light when my wires add up to 2 or more\. I have 2 bright wires, from Switch 1 and Switch 2\. Right now they add up to 2, so I am LIT\./.test(await cardText()), await cardText());
      ok(`${name}: the lamp's face shows 2 filled squares and 2 lit wires`, await page.evaluate(() => { const f = document.querySelector('#face svg'); return f.querySelectorAll('rect[fill="currentColor"]').length === 2 && f.querySelectorAll('circle[fill="currentColor"]').length === 2; }));
      await shot('2-lamp-lit');
      await goTo('D');
      ok(`${name}: an open door says to walk up through it`, await page.locator('#hint').isVisible() && /The door is open\. Walk up through it\./.test(await cardText()), await cardText());
      await goTo('shelf'); await tap('#b1');
      ok(`${name}: book 1 opens at page 1 of 3`, /How to read the marks/.test(await bookText()) && /Page 1 of 3/.test(await bookText()));
      await tap('#nextp'); await tap('#nextp');
      ok(`${name}: its pages turn`, /Page 3 of 3/.test(await bookText()) && await page.locator('#nextp').isDisabled());
      await shot('3-book-how-to-read');
      await tap('#b2');
      ok(`${name}: book 2 is the room's own history`, /1\. Switch 1 turned on\. Then: Lamp A dark, the door shut\./.test(await bookText()) && /2\. Switch 2 turned on\. Then: Lamp A lit, the door open\./.test(await bookText()) && /Check number: [0-9a-f]{8}/.test(await bookText()), await bookText());
      await tap('#b3');
      ok(`${name}: book 3 is the room's code, read off the faces`, (await page.locator('#code').innerText()).trim() === codeText(ROOMS[0].things) && /It matches the list/.test(await bookText()), await page.locator('#code').innerText());
      await tap('#rebuild');
      ok(`${name}: built again from that page and its history, it is the same room`, /Same room\./.test(await page.locator('#same').innerText()));
      await shot('4-book-code');
      await tap('#shut'); ok(`${name}: the book closes`, await page.locator('#book').isHidden());
      await goThrough();
      ok(`${name}: walking up through the open door`, /You are through the door/.test(await cardText()) && /You opened Room 1 in 2 flips\./.test(await cardText()) && /The fewest possible is 2\. Flipping switches without reading takes about 4 on average\./.test(await cardText()), await cardText());
      ok(`${name}: the reading so far is written down`, (await page.locator('#logbody tr').count()) === 1 && /^RR .* r1 flips=2 best=2 blind=4\.0 asked=- /.test(await page.locator('#raw').innerText()));
      await tap('#next'); s = await st();
      ok(`${name}: on to room 2`, s.room === 2 && s.facing === null && s.flips === 0 && s.facesOk === true);

      // ---- room 2: turning everything on does not open it; reading the door says why
      for (const id of ['1', '2', '3']) await flipSwitch(id);
      s = await st(); ok(`${name}: room 2 with every switch on: both lamps lit, door still shut`, s.shown.A === 1 && s.shown.B === 1 && s.shown.D === 0, JSON.stringify(s.shown));
      await goTo('D');
      ok(`${name}: the door says why`, /I have 1 dark wire, from Switch 1\. A dark wire takes one away while it carries light\. Right now they add up to 1, so I am shut\./.test(await cardText()), await cardText());
      ok(`${name}: the door's face shows the dark wire as a dashed ring, and a shut door gives no way-through hint`, await page.evaluate(() => document.querySelectorAll('#face svg circle[stroke-dasharray]').length === 1 && !!document.querySelector('#face svg path')) && await page.locator('#hint').isHidden());
      await shot('5-room2-door-shut');
      await flipSwitch('1'); s = await st();
      ok(`${name}: switch 1 off again: the door opens`, s.shown.D === 1 && s.on['1'] === 0);
      await goThrough(); ok(`${name}: through door 2 in 4 flips, fewest 2`, /You opened Room 2 in 4 flips\./.test(await cardText()) && /fewest possible is 2/.test(await cardText()), await cardText());
      await tap('#next');

      // ---- room 3: marks only. Words come only if asked for, and asking is counted.
      await goTo('B');
      ok(`${name}: room 3 shows marks only`, await page.locator('#words').isHidden() && await page.locator('#ask').isVisible());
      await shot('6-room3-marks-only');
      await tap('#ask'); await page.waitForFunction(() => !document.getElementById('words').hidden);
      s = await st(); ok(`${name}: "Read it to me" gives the words and is counted`, s.asks === 1 && /I have 1 dark wire, from Switch 3\./.test(await cardText()), await cardText());
      await goTo('1'); await page.keyboard.press('e'); await quiet(); await page.keyboard.press('e'); await quiet();
      s = await st(); ok(`${name}: the E key flips the switch you face`, s.flips === 2 && s.on['1'] === 0);
      await solve(); s = await st(); ok(`${name}: room 3 opened by its one setting`, s.shown.D === 1);
      await goThrough(); ok(`${name}: through door 3, and the ask is reported`, /You asked for the words 1 time\./.test(await cardText()), await cardText());
      await tap('#next');

      // ---- room 4: five switches, three lamps, read without asking
      s = await st(); ok(`${name}: room 4's faces give back its list too`, s.room === 4 && s.facesOk === true);
      await goTo('A'); await shot('7-room4');
      await solve(); s = await st(); ok(`${name}: room 4 opened in the fewest flips (${s.best})`, s.shown.D === 1 && s.flips === s.best && s.asks === 0, JSON.stringify(s));
      await goThrough();
      ok(`${name}: through the last door`, /You are through the last door/.test(await cardText()) && /about 42 on average/.test(await cardText()), await cardText());
      const raw = (await page.locator('#raw').innerText()).trim();
      ok(`${name}: all four rooms are in the reading`, (await page.locator('#logbody tr').count()) === 4 && /r1 flips=2 best=2 .* r2 flips=4 best=2 .* r3 flips=5 best=3 .*asked=1 .* r4 flips=4 best=4 .*asked=0 /.test(raw), raw);
      out.browsers[name] = raw; console.log('     ' + raw.slice(0, 170));
      await tap('#copy'); await page.waitForFunction(() => document.getElementById('copied').textContent.length > 0);
      ok(`${name}: still no sideways scroll at the end`, await narrow());
      await shot('8-end', true);
      await tap('#again'); s = await st();
      ok(`${name}: "Start again" goes back to room 1 with a clean sheet`, s.room === 1 && s.flips === 0 && await page.locator('#log').isHidden());
      await page.locator('#jump button').nth(2).tap(); s = await st();
      ok(`${name}: jumping to a room works`, s.room === 3);
      ok(`${name}: no page errors`, errors.length === 0, errors.slice(0, 3).join(' | '));
    } catch (e) { ok(`${name}: ran to the end`, false, String(e).slice(0, 500)); }
    finally { if (browser) await browser.close(); }
  }
  try {                                                                           // one look in the dark colours, on a phone set to reduce motion
    const browser = await pw.chromium.launch({ headless: true, channel: 'msedge' }), ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, hasTouch: true, isMobile: true, colorScheme: 'dark', reducedMotion: 'reduce' });
    await serve(ctx); const page = await ctx.newPage(); await page.goto('http://cw.test/reading-room.html'); await page.waitForFunction(() => window.rr);
    await page.locator('#jump button').nth(1).tap(); await page.keyboard.down('ArrowRight'); await page.waitForFunction(() => window.rr.state().facing === '2'); await page.keyboard.up('ArrowRight');
    await page.tap('#use'); let instant = true; try { await page.waitForFunction(() => { const s = window.rr.state(); return s.settled && s.shown.A === 1; }, null, { timeout: 400 }); } catch (e) { instant = false; }
    ok('reduce-motion phone: a flip shows at once, with no running light', instant); await page.evaluate(() => window.scrollTo(0, 0));
    await page.screenshot({ path: path.join(shots, 'rr-dark.png') }); await browser.close();
  } catch (e) { console.log('     (dark screenshot skipped: ' + String(e).slice(0, 120) + ')'); }
}
out.checks = { passed: good, failed: bad, browsers: noBrowser ? [] : Object.keys(out.browsers) };
fs.writeFileSync(path.join(here, 'results', 'reading-room.json'), JSON.stringify(out, null, 1));
const md = ['# The Reading Room: what the checks say', '', `Made by \`node test-reading-room.mjs\` on ${out.made.slice(0, 16)} UTC. Never typed.`, '',
  '| room | switches | words shown | the one setting that opens it | fewest flips (a reader) | flipping blind, average (worked out) | the same, played out 40,000 times | trying every setting, worst case | does turning everything on open it |', '|---|---|---|---|---|---|---|---|---|',
  ...out.rooms.map((r) => `| ${r.room} | ${r.switches} | ${r.wordsShown ? 'yes' : 'no, marks only'} | ${r.opensWith.join(' ; ')} | ${r.fewestFlips} | ${r.blindAverageWorkedOut} | ${r.blindAveragePlayedOut} | ${r.tryEverySettingWorstCase} | ${r.turningEverythingOnOpensIt ? 'yes' : 'no'} |`), '',
  `Checks: ${good} passed, ${bad} failed` + (noBrowser ? ' (rooms only, no browser this run).' : `, in Node and in two phone-sized browsers (${Object.keys(out.browsers).join(', ')}) with real taps and walking.`), '',
  '"Flipping blind" is someone who cannot read the things and flips one switch at random each time, starting with every switch off, until the door first opens.', ''];
fs.writeFileSync(path.join(here, 'results', 'reading-room.md'), md.join('\n'));
console.log(bad ? `\n${bad} check(s) FAILED` : '\nall Reading Room checks passed');
process.exit(bad ? 1 : 0);
