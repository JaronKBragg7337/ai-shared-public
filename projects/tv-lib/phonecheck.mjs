// iPhone-width WebKit check of a Heartbeat TV channel page.  node phonecheck.mjs <url> <expectedTitleSubstring>
import { createRequire } from 'node:module';
const require = createRequire('C:/Users/lilli/.codex/runtime/unfinished-island/node_modules/playwright/package.json');
const { webkit, devices } = require('playwright');
const [url, expect] = process.argv.slice(2);
const browser = await webkit.launch();
const ctx = await browser.newContext({ ...devices['iPhone 13'], viewport: { width: 375, height: 812 } });
const page = await ctx.newPage();
const errors = [];
page.on('pageerror', (e) => errors.push('pageerror: ' + e.message));
page.on('console', (m) => { if (m.type() === 'error') errors.push('console: ' + m.text()); });
page.on('requestfailed', (r) => errors.push('reqfail: ' + r.url()));
await page.goto(url, { waitUntil: 'networkidle', timeout: 60000 });
await page.waitForTimeout(3000);
for (let i = 0; i < 25; i++) {
  const rs = await page.evaluate((i) => { const v = document.querySelector("video"); if (!v) return -1; if (v.readyState === 0 && i % 5 === 0) { try { v.load(); v.play().catch(() => {}); } catch (e) {} } return v.readyState; }, i).catch(() => -1);
  if (rs >= 2) break;
  await page.waitForTimeout(1000);
}
const info = await page.evaluate(() => {
  const v = document.querySelector('video');
  return {
    title: document.title, bodyText: document.body.innerText.slice(0, 400).replace(/\s+/g, ' '),
    scrollWidth: document.documentElement.scrollWidth, innerWidth: innerWidth,
    video: v ? { src: v.currentSrc, ready: v.readyState, dur: v.duration, w: v.videoWidth, h: v.videoHeight, paused: v.paused, err: v.error && v.error.code } : null,
  };
});
console.log(JSON.stringify(info, null, 1));
console.log('errors:', errors.length ? errors : 'none');
const ok = info.scrollWidth <= info.innerWidth && info.video && info.video.ready >= 2 && !info.video.err && (!expect || info.bodyText.includes(expect));
await page.screenshot({ path: 'phonecheck.png', fullPage: false });
await browser.close();
console.log(ok ? 'PHONE CHECK PASS' : 'PHONE CHECK FAIL');
process.exit(ok ? 0 : 1);
