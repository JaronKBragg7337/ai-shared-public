// Live check at phone width (WebKit iPhone). node live-check.mjs <outPrefix> [scenario.mjs]
// 1) the plain page as a visitor gets it: loads, no page errors, no sideways scroll, build id.
// 2) the same build in a solo review session, optionally running a scenario for a screenshot of the new work.
import { createRequire } from 'node:module';
import { pathToFileURL } from 'node:url';
import { resolve } from 'node:path';
const pw = createRequire('C:/Users/lilli/AI-Shared/tools/site-reel/node_modules/')('playwright-core');
const [prefix, scenario] = process.argv.slice(2);
const UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1';
const URL0 = 'https://www.heartbeatobservatory.com/games/the-cosmos/';
const browser = await pw.webkit.launch({ headless: true });
const mk = async () => { const ctx = await browser.newContext({ userAgent: UA, viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true }); const page = await ctx.newPage(); const errors = []; page.on('pageerror', e => errors.push('pageerror ' + String(e).slice(0, 200))); page.on('console', m => { if (m.type() === 'error') errors.push('console ' + m.text().slice(0, 200)); }); return { ctx, page, errors }; };
{
  const { ctx, page, errors } = await mk();
  await page.goto(URL0, { waitUntil: 'domcontentloaded', timeout: 120000 });
  // a visitor's page has no window.cosmos (dev sessions only): wait for the canvas, then let the opening run a while
  await page.waitForSelector('canvas', { timeout: 120000 }).catch(e => errors.push('no canvas: ' + String(e).slice(0, 120)));
  await page.waitForTimeout(30000);
  const info = await page.evaluate(() => ({ build: document.querySelector('meta[name=cosmos-build]')?.content, sw: document.documentElement.scrollWidth, iw: innerWidth, canvas: !!document.querySelector('canvas') }));
  await page.screenshot({ path: prefix + '-live-plain.png' });
  console.log('plain', JSON.stringify(info), 'errors', JSON.stringify(errors));
  await ctx.close();
}
if (scenario) {
  const { ctx, page, errors } = await mk();
  await page.goto(URL0 + '?dev=1&solo=1&opening=off&tier=low', { waitUntil: 'domcontentloaded', timeout: 120000 });
  await page.waitForFunction(() => window.cosmos?.engine?.frameCount > 10 && window.cosmos.space, null, { timeout: 240000 });
  await page.waitForTimeout(4000);
  const mod = await import(pathToFileURL(resolve(scenario)).href);
  try { await mod.default({ page, prefix }); } catch (e) { errors.push('scenario ' + String(e).slice(0, 300)); }
  const info = await page.evaluate(() => ({ build: document.querySelector('meta[name=cosmos-build]')?.content, sw: document.documentElement.scrollWidth, iw: innerWidth }));
  console.log('solo', JSON.stringify(info), 'errors', JSON.stringify(errors));
  await ctx.close();
}
await browser.close();
