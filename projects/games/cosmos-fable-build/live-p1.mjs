// Live check for part 1 + the shell pieces (second Fable session, 11/19). node live-p1.mjs <outPrefix>
// A visitor's page at iPhone width on the real site: new files served, the opening's first screen, Settings inside the opening.
import { createRequire } from 'node:module';
const pw = createRequire('C:/Users/lilli/AI-Shared/tools/site-reel/node_modules/')('playwright-core');
const prefix = process.argv[2] || 'shots/p1';
const UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1';
const URL0 = 'https://www.heartbeatobservatory.com/games/the-cosmos/';
for (const f of ['src/ui/sfx.js', 'src/ui/quality.js', 'manifest.webmanifest']) { const r = await fetch(URL0 + f + '?t=' + Date.now()); console.log('served', f, r.status, r.headers.get('content-type')); }
const browser = await pw.webkit.launch({ headless: true });
const ctx = await browser.newContext({ userAgent: UA, viewport: { width: 375, height: 812 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true });
const page = await ctx.newPage(); const errors = [];
page.on('pageerror', e => errors.push('pageerror ' + String(e).slice(0, 200)));
page.on('console', m => { if (m.type() === 'error') errors.push('console ' + m.text().slice(0, 200)); });
page.on('response', r => { if (r.status() >= 400) errors.push('HTTP ' + r.status() + ' ' + r.url().slice(0, 120)); });
await page.goto(URL0, { waitUntil: 'domcontentloaded', timeout: 120000 });
await page.waitForSelector('canvas', { timeout: 120000 }).catch(e => errors.push('no canvas'));
await page.waitForSelector('#opening-ui, #boot-solo', { timeout: 180000 }).catch(e => errors.push('neither the opening nor the server-down screen appeared'));
await page.waitForTimeout(25000);
const read = () => page.evaluate(() => { const t = s => document.querySelector(s)?.textContent?.trim().slice(0, 160) || ''; const vis = s => { const e = document.querySelector(s); if (!e) return false; const c = getComputedStyle(e), r = e.getBoundingClientRect(); return c.display !== 'none' && c.visibility !== 'hidden' && r.width > 2; };
  return { build: document.querySelector('meta[name=cosmos-build]')?.content, hint: t('#opening-hint'), caption: t('#opening-caption'), boot: t('#boot-status'), soloButton: vis('#boot-solo'), settingsButton: vis('#btn-settings'), manifests: [...document.querySelectorAll('link[rel=manifest]')].map(l => l.getAttribute('href')), appTitle: document.querySelector('meta[name=apple-mobile-web-app-title]')?.content, sw: document.documentElement.scrollWidth, iw: innerWidth }; });
console.log('first screen', JSON.stringify(await read()));
await page.screenshot({ path: prefix + '-live-first-screen.png' });
if (await page.locator('#btn-settings').isVisible().catch(() => false)) {
  await page.locator('#btn-settings').tap(); await page.waitForTimeout(800);
  const s = await page.evaluate(() => { const b = id => { const e = document.getElementById(id); if (!e) return null; const r = e.getBoundingClientRect(); return r.width > 2 ? [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)] : null; }; const p = document.getElementById('settings-panel').getBoundingClientRect();
    return { panel: [Math.round(p.left), Math.round(p.top), Math.round(p.right), Math.round(p.bottom)], quality: b('set-quality'), now: document.getElementById('set-quality-now')?.textContent, sfx: b('set-sfx'), ih: innerHeight, iw: innerWidth }; });
  console.log('settings', JSON.stringify(s));
  await page.screenshot({ path: prefix + '-live-settings.png' });
}
console.log('errors', JSON.stringify(errors));
await browser.close();
