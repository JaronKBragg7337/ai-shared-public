// The page on a phone-sized screen: an iPhone-profile WebKit at 375 px and a Chromium at 390 px, with real taps.
// No server: the two browsers are handed the project's own files.   node test-page.mjs [shots-folder]
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url)), shots = process.argv[2] || path.join(here, 'results', 'shots');
fs.mkdirSync(shots, { recursive: true });
const pw = createRequire(process.env.CW_PLAYWRIGHT_ROOT || 'C:/Users/lilli/.codex/runtime/unfinished-island/node_modules/')('playwright');
const WEBKIT = process.env.CW_WEBKIT || path.join(process.env.LOCALAPPDATA || '', 'ms-playwright', 'webkit-2336', 'Playwright.exe');
const IPHONE = { userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
  viewport: { width: 375, height: 812 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true };
const TYPES = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8' };
let bad = 0; const ok = (name, pass, detail = '') => { if (!pass) bad++; console.log((pass ? 'PASS ' : 'FAIL ') + name + (pass ? '' : '  ' + detail)); };
const results = {};

for (const [name, launch, ctxOpts] of [
  ['iphone-webkit', () => pw.webkit.launch({ headless: true, executablePath: WEBKIT }), IPHONE],
  ['edge', () => pw.chromium.launch({ headless: true, channel: 'msedge' }), { viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, hasTouch: true, isMobile: true }],
]) {
  let browser;
  try {
    browser = await launch();
    const ctx = await browser.newContext(ctxOpts), errors = [];
    await ctx.route('**/*', (route) => {
      const u = new URL(route.request().url());
      if (u.hostname !== 'cw.test') return route.abort();                      // fonts and anything else: the page must work without them
      const f = path.join(here, u.pathname === '/' ? 'index.html' : u.pathname.slice(1));
      return fs.existsSync(f) ? route.fulfill({ status: 200, contentType: TYPES[path.extname(f)] || 'text/plain', body: fs.readFileSync(f) }) : route.fulfill({ status: 404, body: '' });
    });
    const page = await ctx.newPage(); page.setDefaultTimeout(180000);
    page.on('pageerror', (e) => errors.push(String(e)));
    page.on('console', (m) => { if (m.type() === 'error' && !/Failed to load resource|net::ERR|fonts\.g/.test(m.text())) errors.push(m.text()); });
    await page.goto('http://cw.test/'); await page.waitForFunction(() => window.cw0);
    const tap = (sel) => (ctxOpts.hasTouch ? page.tap(sel) : page.click(sel));
    ok(`${name}: 81 cards drawn`, (await page.locator('.card').count()) === 81);
    ok(`${name}: no sideways scroll`, await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth));
    await tap('#card0'); await tap('#card1');
    ok(`${name}: two cards, no set`, (await page.evaluate(() => window.cw0.state())).alarm === 0);
    ok(`${name}: the third card is shown as blocked`, await page.evaluate(() => document.getElementById('card2').classList.contains('blocked')));
    await tap('#card2');
    let st = await page.evaluate(() => window.cw0.state());
    ok(`${name}: three cards in a row make a set`, st.alarm === 1 && st.k === 3, JSON.stringify(st));
    ok(`${name}: lamp says so`, (await page.locator('#lamp').innerText()).includes('A set is in the pile'));
    ok(`${name}: all three ways agree with the checker`, (await page.locator('#agree').innerText()).includes('All three agree'));
    const cost = await page.evaluate(() => ['w-soft', 'w-gate', 'w-own'].map((id) => document.querySelector('#' + id + ' .n').textContent + ' ' + document.querySelector('#' + id + ' .unit').textContent));
    console.log(`     cost of that tap: ${cost.join(' | ')}`);
    await tap('#clear');
    ok(`${name}: clear empties the pile`, (await page.evaluate(() => window.cw0.state())).k === 0);
    await tap('#build'); await page.waitForFunction(() => !document.getElementById('build').disabled && window.cw0.state().k > 0);
    st = await page.evaluate(() => window.cw0.state());
    ok(`${name}: built a pile with no set and no free card left`, st.alarm === 0 && st.free === 0 && st.k >= 14, JSON.stringify(st));
    console.log(`     built pile: ${st.k} cards, history ${st.history} changes`);
    await page.screenshot({ path: path.join(shots, `${name}-board.png`) });
    // a part of your own: choose three cards, mark 2, add it; it must light exactly when two of them are in the pile
    await tap('#clear'); await tap('#pick'); await tap('#card40'); await tap('#card41'); await tap('#card42'); await tap('#more'); await tap('#addpart');
    ok(`${name}: own part added, dark on an empty table`, JSON.stringify((await page.evaluate(() => window.cw0.state())).mine) === '[0]');
    await tap('#card40'); ok(`${name}: own part still dark with one of its cards in`, (await page.evaluate(() => window.cw0.state())).mine[0] === 0);
    await tap('#card42'); ok(`${name}: own part lights with two of its cards in`, (await page.evaluate(() => window.cw0.state())).mine[0] === 1 && (await page.locator('#parts').innerText()).includes('Lit'));
    await tap('#card40'); ok(`${name}: and goes dark again`, (await page.evaluate(() => window.cw0.state())).mine[0] === 0);
    await tap('#rm0'); ok(`${name}: own part removed`, (await page.evaluate(() => window.cw0.state())).mine.length === 0);
    await tap('#replay');
    ok(`${name}: replay lands on the same state`, (await page.locator('#replayed').innerText()).includes('Same state'));
    await tap('#measure'); await page.waitForFunction(() => !document.getElementById('measure').disabled, null, { timeout: 240000 });
    const prog = await page.locator('#progress').innerText();
    ok(`${name}: measurement finished and every answer matched`, prog.includes('Every answer matched'), prog);
    results[name] = await page.locator('#raw').innerText(); console.log('     ' + prog);
    ok(`${name}: still no sideways scroll with the table shown`, await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth));
    await page.locator('#measure').scrollIntoViewIfNeeded(); await page.screenshot({ path: path.join(shots, `${name}-measure.png`) });
    await page.screenshot({ path: path.join(shots, `${name}-full.png`), fullPage: true });
    ok(`${name}: no page errors`, errors.length === 0, errors.slice(0, 3).join(' | '));
  } catch (e) { ok(`${name}: ran`, false, String(e).slice(0, 400)); }
  finally { if (browser) await browser.close(); }
}
fs.writeFileSync(path.join(here, 'results', 'browsers-on-msi.json'), JSON.stringify(results, null, 1));
console.log(bad ? `\n${bad} check(s) FAILED` : '\nall page checks passed');
process.exit(bad ? 1 : 0);
