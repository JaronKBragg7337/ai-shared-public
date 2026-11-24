// Probe: where the purse line sits under the status card on the iPhone (WebKit) profile. node purse-probe.mjs [chromium]
import { createRequire } from 'node:module';
const pw = createRequire('C:/Users/lilli/AI-Shared/tools/site-reel/node_modules/')('playwright-core');
const eng = process.argv[2] === 'chromium' ? 'chromium' : 'webkit';
const UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1';
const browser = await pw[eng].launch({ headless: true });
const page = await (await browser.newContext({ userAgent: UA, viewport: { width: 375, height: 812 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true })).newPage();
await page.goto('http://127.0.0.1:4380/?dev=1&solo=1&opening=off&tier=low&test=1', { waitUntil: 'domcontentloaded', timeout: 120000 });
await page.waitForFunction(() => window.cosmos?.engine?.frameCount > 10 && window.cosmos.space, null, { timeout: 240000 });
await page.waitForTimeout(3000);
console.log(eng, JSON.stringify(await page.evaluate(() => { const r = e => { if (!e) return null; const b = e.getBoundingClientRect(); return [Math.round(b.top), Math.round(b.bottom), Math.round(b.height)]; };
  const ro = document.getElementById('hud-readout'), pu = document.getElementById('purse'), cs = pu && getComputedStyle(pu);
  const range = document.createRange(); let text = null; if (pu?.firstChild) { range.selectNodeContents(pu); const b = range.getBoundingClientRect(); text = [Math.round(b.top), Math.round(b.bottom)]; }
  return { opening: !!cosmos.opening?.active, readout: r(ro), lastChild: r(ro?.lastElementChild), purse: r(pu), purseText: text, mt: cs?.marginTop, pt: cs?.paddingTop, mh: cs?.minHeight, bs: cs?.boxSizing, disp: cs?.display, lh: cs?.lineHeight, hud: r(document.getElementById('hud')) }; })));
await page.screenshot({ path: 'shots/purse-' + eng + '.png', clip: { x: 0, y: 0, width: 375, height: 260 } });
await browser.close();
