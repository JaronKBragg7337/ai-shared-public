import { createRequire } from 'module';
const require = createRequire('C:/Users/lilli/.codex/runtime/unfinished-island/node_modules/');
const { webkit, devices } = require('playwright');
const b = await webkit.launch(); const c = await b.newContext({ ...devices['iPhone 13'] }); const p = await c.newPage();
const errs = []; p.on('pageerror', e => errs.push(String(e))); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
await p.goto('https://www.heartbeatobservatory.com/tv/?ch=13.1', { waitUntil: 'networkidle' }); await p.waitForTimeout(6000);
const r = await p.evaluate(() => { const v = document.querySelector('video'); return { vw: innerWidth, sw: document.documentElement.scrollWidth, title: document.body.innerText.slice(0, 300), src: v && v.currentSrc, rs: v && v.readyState, dur: v && v.duration, t: v && v.currentTime, paused: v && v.paused }; });
console.log(JSON.stringify(r), JSON.stringify(errs));
await p.screenshot({ path: 'stills/live_phone.png' }); await b.close();
