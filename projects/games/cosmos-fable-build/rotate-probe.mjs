// Rotation probe (second Fable session, 11/19): the opening and the open game on a phone turned on its side.
// node rotate-probe.mjs <outDir>   (needs the worktree's static server: PORT=4380 node server.js)
import { createRequire } from 'node:module';
import { mkdirSync } from 'node:fs';
import { join } from 'node:path';
const pw = createRequire('C:/Users/lilli/AI-Shared/tools/site-reel/node_modules/')('playwright-core');
const out = process.argv[2] || 'shots/p4-rotate'; mkdirSync(out, { recursive: true });
const UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1';
const browser = process.env.ENG === 'chromium' ? await pw.chromium.launch({ headless: true, args: ['--use-angle=d3d11', '--enable-gpu', '--ignore-gpu-blocklist'] }) : await pw.webkit.launch({ headless: true });
const ctx = await browser.newContext({ userAgent: UA, viewport: { width: 375, height: 812 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true });
const page = await ctx.newPage(); const errors = [];
page.on('pageerror', e => errors.push('pageerror ' + String(e).slice(0, 200)));
const report = async (name) => {
  await page.waitForTimeout(1200); await page.screenshot({ path: join(out, name + '.png') });
  const r = await page.evaluate(() => { const vis = el => { for (let p = el; p; p = p.parentElement) { const c = getComputedStyle(p); if (p.hidden || c.display === 'none' || c.visibility === 'hidden') return false; } const b = el.getBoundingClientRect(); return b.width > 2 && b.height > 2; };
    const bs = [...document.querySelectorAll('button')].filter(vis).map(b => { const r = b.getBoundingClientRect(); return { t: (b.textContent || b.id).trim().slice(0, 24), l: Math.round(r.left), t0: Math.round(r.top), r: Math.round(r.right), b: Math.round(r.bottom) }; });
    const off = bs.filter(b => b.r > innerWidth + 1 || b.b > innerHeight + 1 || b.l < -1 || b.t0 < -1).map(b => b.t);
    const over = []; for (let i = 0; i < bs.length; i++) for (let j = i + 1; j < bs.length; j++) { const a = bs[i], c = bs[j]; if (a.l < c.r - 2 && a.r > c.l + 2 && a.t0 < c.b - 2 && a.b > c.t0 + 2) over.push(a.t + ' x ' + c.t); }
    return { w: innerWidth, h: innerHeight, sw: document.documentElement.scrollWidth, buttons: bs.length, off, over }; });
  console.log(name, JSON.stringify(r));
};
// the opening (a solo game plays it too), upright then on its side, with Settings open
await page.goto('http://127.0.0.1:4380/?dev=1&solo=1&tier=low', { waitUntil: 'domcontentloaded', timeout: 120000 });
await page.waitForFunction(() => window.cosmos?.opening?.active && cosmos.engine.frameCount > 10, null, { timeout: 240000 });
await page.waitForTimeout(9000); await report('opening-upright');
await page.setViewportSize({ width: 812, height: 375 }); await report('opening-on-its-side');
await page.locator('#btn-settings').tap(); await report('opening-on-its-side-settings');
await page.evaluate(() => document.getElementById('settings-panel').classList.remove('open'));
// the open game
await page.setViewportSize({ width: 375, height: 812 });
await page.goto('http://127.0.0.1:4380/?dev=1&solo=1&opening=off&tier=low', { waitUntil: 'domcontentloaded', timeout: 120000 });
await page.waitForFunction(() => window.cosmos?.engine?.frameCount > 10 && window.cosmos.space, null, { timeout: 240000 });
await page.waitForTimeout(4000); await report('game-upright');
await page.setViewportSize({ width: 812, height: 375 }); await report('game-on-its-side');
await page.locator('#btn-settings').tap(); await report('game-on-its-side-settings');
console.log('errors', JSON.stringify(errors));
await browser.close();
