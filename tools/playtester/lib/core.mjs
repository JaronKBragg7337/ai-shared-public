// core.mjs - the browser session: launch, monitors, input, screenshots, findings.
// Everything the bot "feels" goes through here so every phase gets the same watching.
import { createRequire } from 'node:module';
import { mkdirSync, writeFileSync, appendFileSync } from 'node:fs';
import { join } from 'node:path';

const PW_ROOTS = [process.env.COSMOS_PLAYWRIGHT_ROOT, 'C:/Users/lilli/.codex/runtime/unfinished-island/node_modules'].filter(Boolean);
export function loadPlaywright() {
  const here = createRequire(import.meta.url);
  try { return here('playwright'); } catch {}
  for (const r of PW_ROOTS) { try { return createRequire(r + '/')('playwright'); } catch {} }
  throw new Error('playwright not found; set COSMOS_PLAYWRIGHT_ROOT to a node_modules folder that has it');
}
const MSPW = join(process.env.LOCALAPPDATA || 'C:/Users/lilli/AppData/Local', 'ms-playwright');
export const PROFILES = {
  iphone: {
    label: 'iPhone 15 (WebKit, touch)', engine: 'webkit', touch: true,
    exe: join(MSPW, 'webkit-2336', 'Playwright.exe'),
    ctx: { userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
      viewport: { width: 393, height: 852 }, deviceScaleFactor: 1, isMobile: true, hasTouch: true },
  },
  desktop: {
    label: 'Desktop (Chromium, keyboard + mouse)', engine: 'chromium', touch: false,
    exe: join(MSPW, 'chromium-1234', 'chrome-win64', 'chrome.exe'),
    ctx: { viewport: { width: 1280, height: 800 }, deviceScaleFactor: 1 },
  },
};

// ---- injected into every page: frame timer, message catcher ---------------------------------------------------------
const INIT = `(() => {
  if (window.__qa) return;
  const Q = window.__qa = { frames: [], msgs: [], t0: performance.now() };
  Q.req = 0; Q.rec = 0; Q.refused = 0; Q.lastReq = 0;
  addEventListener('cosmos-request', () => { Q.req++; Q.lastReq = performance.now(); });
  addEventListener('cosmos-receipt', e => { Q.rec++; if (e.detail && e.detail.ok === false) Q.refused++; });
  let last = performance.now();
  const loop = t => { const dt = t - last; last = t;
    if (!document.hidden && dt < 120000) { Q.frames.push([Math.round(t), Math.round(dt)]); if (Q.frames.length > 6000) Q.frames.splice(0, 3000); }
    requestAnimationFrame(loop); };
  requestAnimationFrame(loop);
  const RE = /fail|refus|error|can.?t |cannot|walk to that|reach the port|not enough|too far|wait for|disconnect|try again|no longer|denied|invalid|unavailable|not available|offline|not aboard|too heavy|hands full|nothing to|already/i;
  const push = (txt, el) => { txt = (txt || '').replace(/\\s+/g, ' ').trim(); if (txt.length < 4 || txt.length > 220) return;
    let id = ''; try { for (let e = el; e && e !== document.body; e = e.parentElement) { if (e.id) { id = e.id; break; } } } catch {}
    if (!RE.test(txt) && !/toast|caption/.test(id)) return;
    const k = id + '|' + txt, now = performance.now(); Q.last = Q.last || {}; if (Q.last[k] && now - Q.last[k] < 6000) { Q.last[k] = now; return; } Q.last[k] = now;
    Q.msgs.push({ t: Math.round(performance.now()), text: txt, id }); if (Q.msgs.length > 500) Q.msgs.splice(0, 250); };
  const start = () => new MutationObserver(ms => { for (const m of ms) {
      if (m.type === 'characterData') push(m.target.data, m.target.parentElement);
      else for (const n of m.addedNodes) { if (n.nodeType === 3) push(n.data, n.parentElement); else if (n.nodeType === 1 && n.innerText !== undefined) { if (n.innerText.length < 400) push(n.innerText, n); } } } })
    .observe(document, { subtree: true, childList: true, characterData: true });
  if (document.documentElement) start(); else document.addEventListener('DOMContentLoaded', start);
})();`;

const sleep = ms => new Promise(r => setTimeout(r, ms));
export { sleep };
export const rnd = (a, b) => a + Math.random() * (b - a);
export const pick = arr => arr[Math.floor(Math.random() * arr.length)];

export class Session {
  constructor({ profileKey, outDir, url, label, vision }) {
    this.profileKey = profileKey; this.profile = PROFILES[profileKey]; this.outDir = outDir; this.baseUrl = url;
    this.label = label || profileKey; this.shotDir = join(outDir, 'shots-' + profileKey); mkdirSync(this.shotDir, { recursive: true });
    this.findings = new Map(); this.trail = []; this.shots = []; this.shotN = 0; this.t0 = Date.now(); this.phase = 'start';
    this.samples = []; this.lastSigChange = Date.now(); this.lastSig = ''; this.msgSeen = []; this.layoutSeen = new Set();
    this.consoleSeen = new Map(); this.phaseResults = []; this.stepSigs = []; this.heldStick = false; this.hitchSeen = new Map();
    this.opts = { skipOpening: false };
  }
  overTime(marginMin = 0) { return this.deadline ? Date.now() > this.deadline - marginMin * 60000 : false; }
  now() { return Math.round((Date.now() - this.t0) / 1000); }
  mmss() { const s = this.now(); return `${String(Math.floor(s / 60)).padStart(2, '0')}:${String(s % 60).padStart(2, '0')}`; }
  log(msg) { const line = `${this.mmss()} [${this.phase}] ${msg}`; this.trail.push(line); if (this.trail.length > 400) this.trail.splice(0, 100); console.log(`(${this.profileKey}) ${line}`); appendFileSync(join(this.outDir, `trail-${this.profileKey}.log`), line + '\n'); }

  // ---- browser lifecycle -------------------------------------------------------------------------------------------
  async launch() {
    const pw = loadPlaywright(); const P = this.profile;
    this.browser = await pw[P.engine].launch({ headless: true, executablePath: P.exe });
    this.ctx = await this.browser.newContext({ ...P.ctx, reducedMotion: 'no-preference', recordVideo: { dir: join(this.outDir, 'videos-' + this.profileKey), size: P.ctx.viewport } });
    await this.ctx.addInitScript(INIT);
    this.page = await this.ctx.newPage(); this.wire(this.page);
  }
  wire(page) {
    page.on('pageerror', e => this.finding({ kind: 'page-error', sev: 95, title: 'Page error (uncaught exception)', detail: String(e.stack || e).split('\n').slice(0, 4).join(' | ').slice(0, 400), key: 'pe:' + String(e).slice(0, 100) }));
    page.on('console', m => { const ty = m.type(); if (ty !== 'error' && ty !== 'warning') return; const t = m.text().slice(0, 300);
      if (/favicon|DevTools|Download the React|GPU stall|WebGL: INVALID|Automatic fallback to software|ReadPixels/i.test(t)) return;
      if (this.offline && /ERR_INTERNET_DISCONNECTED|Failed to load resource|NetworkError|Load failed/i.test(t)) return;   // the bot cut the network on purpose
      const key = (ty === 'error' ? 'ce:' : 'cw:') + t.replace(/\d+/g, 'N').slice(0, 90);
      this.consoleSeen.set(key, (this.consoleSeen.get(key) || 0) + 1);
      this.finding({ kind: ty === 'error' ? 'console-error' : 'console-warning', sev: ty === 'error' ? 55 : 20, title: ty === 'error' ? 'Console error' : 'Console warning', detail: t, key }); });
    page.on('response', r => { const s = r.status(); if (s >= 400) { const u = r.url(); if (/favicon/.test(u)) return;
      this.finding({ kind: 'http', sev: s >= 500 ? 70 : 50, title: `Request returned HTTP ${s}`, detail: u.slice(0, 200), key: 'http:' + s + u.replace(/\?.*/, '').slice(-60) }); } });
    page.on('requestfailed', r => { if (this.offline) return; const u = r.url(); if (/favicon|analytics|plausible|googletag|google-analytics/.test(u)) return; const f = r.failure()?.errorText || '';
      if (/ABORTED|abort/i.test(f)) return;
      this.finding({ kind: 'request-failed', sev: 45, title: 'A request failed to load', detail: `${u.slice(0, 160)} (${f})`, key: 'rf:' + u.replace(/\?.*/, '').slice(-60) }); });
    page.on('websocket', ws => { this.log('websocket open ' + ws.url().slice(0, 80));
      ws.on('close', () => { if (this.offline) { this.log('websocket closed (the bot cut the network)'); return; } this.log('websocket closed' + (this.reloadAt && Date.now() - this.reloadAt < 15000 ? ' (the bot refreshed the page)' : '')); if (this.reloadAt && Date.now() - this.reloadAt < 15000) return; this.finding({ kind: 'ws-closed', sev: 50, title: 'Server connection (websocket) closed', detail: 'The live connection closed while playing: ' + ws.url().slice(0, 100), key: 'wsclose' }); });
      ws.on('socketerror', e => this.offline || this.finding({ kind: 'ws-error', sev: 60, title: 'Server connection error', detail: String(e).slice(0, 200), key: 'wserr' })); });
    page.on('crash', () => this.finding({ kind: 'crash', sev: 100, title: 'The browser tab crashed', detail: 'Page crash event', key: 'crash' }));
  }
  async open(url, { waitCosmos = true } = {}) {
    this.log('open ' + url.replace(/key=[^&]+/, 'key=...'));
    await this.page.goto(url, { waitUntil: 'domcontentloaded', timeout: 90000 });
    if (waitCosmos) await this.page.waitForFunction(() => window.cosmos && cosmos.engine && cosmos.engine.frameCount > 20, null, { timeout: 120000 });
    await sleep(500);
  }
  async reload(why) {
    this.log('REFRESH (' + why + ')'); this.reloadAt = Date.now(); this.msgSeen = []; await this.page.reload({ waitUntil: 'domcontentloaded', timeout: 90000 });
    await this.page.waitForFunction(() => window.cosmos && cosmos.engine && cosmos.engine.frameCount > 20, null, { timeout: 120000 });
    this.heldStick = false; await sleep(800);
  }
  /** Download size, request count and slowest file of the page load that is open right now (call straight after the first open, before any refresh). */
  async loadStats() {
    return this.safeEv(() => { const n = performance.getEntriesByType('navigation')[0]; const res = performance.getEntriesByType('resource'); let bytes = 0, slow = { ms: 0, name: '' };
      for (const r of res) { bytes += r.transferSize || 0; if (r.duration > slow.ms) slow = { ms: Math.round(r.duration), name: r.name.replace(/\?.*/, '').slice(-60) }; }
      return n ? { dcl: Math.round(n.domContentLoadedEventEnd), load: Math.round(n.loadEventEnd), requests: res.length, mb: +(bytes / 1048576).toFixed(1), slow } : null; }, null, null);
  }
  async close() { try { await this.ctx?.close(); await this.browser?.close(); } catch {} }
  async ev(fn, arg) { return this.page.evaluate(fn, arg); }
  async safeEv(fn, arg, dflt = null) { try { return await this.page.evaluate(fn, arg); } catch (e) { return dflt; } }

  // ---- findings ----------------------------------------------------------------------------------------------------
  /** Record a problem once per key (later hits only add to the count). Takes a screenshot the first time. */
  finding({ kind, sev, title, detail = '', key, shot = true, steps }) {
    key = key || kind + ':' + title; let f = this.findings.get(key);
    if (f) { f.count++; f.lastAt = this.mmss(); if (f.count <= 3) f.extra.push(`${this.mmss()} ${detail}`.slice(0, 200)); return f; }
    f = { key, kind, sev, title, detail, count: 1, firstAt: this.mmss(), lastAt: this.mmss(), phase: this.phase, device: this.profileKey, shot: null, steps: steps || this.trail.slice(-12), extra: [], vision: null };
    this.findings.set(key, f);
    console.log(`(${this.profileKey}) !! PROBLEM [${sev}] ${title} - ${detail}`.slice(0, 260));
    if (shot && this.page) this.shot('PROBLEM-' + kind, { problem: f }).catch(() => {});
    return f;
  }

  // ---- screenshots and the pixel check -----------------------------------------------------------------------------
  async shot(label, { problem = null, check = true } = {}) {
    if (!this.page) return null; const n = ++this.shotN;
    const name = `${String(n).padStart(3, '0')}-${this.phase}-${label}`.replace(/[^a-zA-Z0-9_-]+/g, '-').slice(0, 90) + '.jpg';
    let buf; try { buf = await this.page.screenshot({ type: 'jpeg', quality: 60, timeout: 15000 }); } catch (e) { return null; }
    const path = join(this.shotDir, name); writeFileSync(path, buf);
    const rel = `shots-${this.profileKey}/${name}`; const rec = { rel, path, label, phase: this.phase, at: this.mmss(), problem: !!problem, ctx: this.trail[this.trail.length - 1] || '' };
    this.shots.push(rec); if (problem && !problem.shot) problem.shot = rel;
    if (check && !problem) await this.pixelCheck(buf, rec);
    return rec;
  }
  async pixelCheck(buf, rec) {
    const stats = await this.safeEv(async b64 => { const img = new Image(); img.src = 'data:image/jpeg;base64,' + b64; await img.decode();
      const w = 64, h = Math.max(16, Math.round(64 * img.height / img.width)); const c = document.createElement('canvas'); c.width = w; c.height = h; const x = c.getContext('2d'); x.drawImage(img, 0, 0, w, h);
      const d = x.getImageData(0, 0, w, h).data; let s = 0, s2 = 0, n = w * h, dark = 0; for (let i = 0; i < d.length; i += 4) { const l = .299 * d[i] + .587 * d[i + 1] + .114 * d[i + 2]; s += l; s2 += l * l; if (l < 8) dark++; }
      const m = s / n; return { mean: m, std: Math.sqrt(Math.max(0, s2 / n - m * m)), dark: dark / n }; }, buf.toString('base64'));
    if (!stats) return; rec.px = stats;
    const blank = stats.std < 3 || stats.mean < 4 || stats.dark > 0.985 || stats.mean > 252;
    if (!blank) return;
    // a legitimate fade (opening transition, boot screen) is not a bug: look again after a moment
    const fading = await this.safeEv(() => !!document.querySelector('.opening-transition') || (document.getElementById('opening-fade') && +document.getElementById('opening-fade').style.opacity > .3) || (document.getElementById('boot') && getComputedStyle(document.getElementById('boot')).display !== 'none'), null, false);
    if (fading) return; await sleep(1800);
    let b2; try { b2 = await this.page.screenshot({ type: 'jpeg', quality: 60, timeout: 15000 }); } catch { return; }
    const st2 = await this.safeEv(async b64 => { const img = new Image(); img.src = 'data:image/jpeg;base64,' + b64; await img.decode(); const c = document.createElement('canvas'); c.width = 48; c.height = 48; const x = c.getContext('2d'); x.drawImage(img, 0, 0, 48, 48); const d = x.getImageData(0, 0, 48, 48).data; let s = 0, s2 = 0; const n = 48 * 48; for (let i = 0; i < d.length; i += 4) { const l = .299 * d[i] + .587 * d[i + 1] + .114 * d[i + 2]; s += l; s2 += l * l; } const m = s / n; return { mean: m, std: Math.sqrt(Math.max(0, s2 / n - m * m)) }; }, b2.toString('base64'));
    if (st2 && (st2.std < 3 || st2.mean < 4 || st2.mean > 252)) this.finding({ kind: 'blank-frame', sev: 85, title: 'The screen is blank (black or one flat colour)', detail: `still blank 2 s later (average brightness ${Math.round(st2.mean)}, variation ${st2.std.toFixed(1)}) during ${rec.ctx}`, key: 'blank:' + this.phase, shot: true });
  }

  // ---- the page's own state, in plain numbers ----------------------------------------------------------------------
  async state() {
    return this.safeEv(() => {
      const c = window.cosmos; if (!c) return { nocosmos: true };
      const o = {}; const op = c.opening;
      o.opening = !!(op && op.active); o.stage = op && op.active ? op.state.stage : null; o.pending = !!(op && op.active && (op.busy || op.actionPending));
      const act = document.getElementById('btn-action'); const oa = document.getElementById('opening-action');
      o.actionLabel = oa && !oa.hidden && getComputedStyle(oa).display !== 'none' ? (oa.textContent || '').trim() : (act && getComputedStyle(act).display !== 'none' ? (act.textContent || '').trim() : '');
      o.caption = (document.getElementById('opening-caption')?.textContent || '').slice(0, 120);
      o.hint = (document.getElementById('opening-hint')?.textContent || '').slice(0, 80);
      o.aboard = !!c.ship.aboard; o.seat = c.ship.seat ? c.ship.seat.id : null;
      o.marks = c.world?.state?.economy?.marks ?? null; o.purse = (document.getElementById('purse')?.textContent || '').slice(0, 40);
      o.trip = c.space?.trip?.active ? { phase: c.space.trip.phase, dest: c.space.trip.dest.name, warp: c.space.trip.warp, eta: Math.round(c.space.trip.progress.etaS), dist: Math.round(c.space.trip.progress.distM) } : null;
      o.onMoon = !!c.space?.onMoon; o.moon = c.space?.activeMoon?.body?.name || null;
      o.flying = !!(c.ship.flight && !c.ship.flight.landed); o.landed = !!(c.ship.flight && c.ship.flight.landed);
      o.toast = document.getElementById('ship-toast')?.classList.contains('on') ? document.getElementById('ship-toast').textContent.slice(0, 100) : '';
      o.save = (document.getElementById('save-status')?.textContent || '').slice(0, 60);
      o.rover = !!c.vehicles?.seated?.();
      o.cart = (document.getElementById('hud')?.innerText.match(/(\d[\d.,]*)\s*\/\s*(\d[\d.,]*)\s*kg/) || []).slice(1, 3).join('/');
      try {
        if (op && op.active && op.model) { const p = op.model.pose(); o.pos = { x: +p.x.toFixed(1), y: +p.y.toFixed(1), z: +p.z.toFixed(1) }; o.frame = 'opening'; const sw = op.state.stage === 0 ? op.liner?.sw : op.state.stage === 2 ? op.kestrel?.sw : op.state.stage === 3 ? op.cabinSw : null; if (sw) o.pos = { x: +sw.x.toFixed(1), y: +sw.y.toFixed(1), z: +sw.z.toFixed(1) }; o.openingClock = Math.round(op.clock || 0); o.openingKind = op.actionKind || ''; }
        else if (c.ship.aboard) { const s = c.ship.sw; o.pos = { x: +s.x.toFixed(1), y: +s.y.toFixed(1), z: +s.z.toFixed(1) }; o.frame = 'ship'; }
        else if (c.space?.onMoon) { const w = c.walker.worldPos; o.pos = { x: Math.round(w.x), y: Math.round(w.y), z: Math.round(w.z) }; o.frame = 'moon'; }
        else { const p = c.port.site.toLocal(c.walker.worldPos); o.pos = { x: +p.x.toFixed(1), y: +p.y.toFixed(1), z: +p.z.toFixed(1) }; o.frame = 'port'; }
        // a settlement world (Earth, the Moon's bases): the outpost frame is what the layout and the people use
        const am = c.space?.activeMoon, pi = am?.body?.padInfo; if (am && pi && !c.ship.aboard && !(op && op.active)) { const w = c.walker.worldPos, dx = w.x - pi.point.x, dy = w.y - pi.point.y, dz = w.z - pi.point.z;
          o.outpost = { x: +(dx * pi.east.x + dy * pi.east.y + dz * pi.east.z).toFixed(1), y: +(dx * pi.up.x + dy * pi.up.y + dz * pi.up.z).toFixed(1), z: +(-(dx * pi.north.x + dy * pi.north.y + dz * pi.north.z)).toFixed(1) }; o.worldId = am.id || am.body?.name || null; }
      } catch (e) { o.posErr = String(e).slice(0, 60); }
      return o;
    }, null, { nocosmos: true });
  }
  async frameStats(reset = true) {
    const r = await this.safeEv(reset0 => { const f = window.__qa?.frames || []; const dts = f.map(x => x[1]).sort((a, b) => a - b); if (reset0) window.__qa.frames = [];
      if (!dts.length) return null; return { n: dts.length, med: dts[Math.floor(dts.length / 2)], p95: dts[Math.floor(dts.length * .95)], max: dts[dts.length - 1], over250: dts.filter(x => x > 250).length, over1000: dts.filter(x => x > 1000).length }; }, reset);
    if (!r) return null; this.frames = this.frames || []; this.frames.push({ phase: this.phase, ...r });
    if (r.max > 700 && r.max > 8 * Math.max(r.med, 16)) { const k = 'hitch:' + this.phase; this.hitchSeen.set(k, Math.max(this.hitchSeen.get(k) || 0, r.max));
      this.finding({ kind: 'frame-spike', sev: r.max > 3000 ? 62 : 38, title: `Frame-time spike during "${this.phase}"`, detail: `a single frame took ${r.max} ms (typical ${r.med} ms); ${r.over250} frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)`, key: k, shot: true }); }
    return r;
  }
  /** One sample of page health: graphics objects (leak signal on every browser), DOM size, JS heap (Chromium only). */
  async health() {
    const h = await this.safeEv(() => { const c = window.cosmos; const r = c?.engine?.renderer; const o = { dom: document.getElementsByTagName('*').length };
      try { const i = r.info; o.geometries = i.memory.geometries; o.textures = i.memory.textures; o.calls = i.render.calls; o.triangles = i.render.triangles; } catch {}
      try { if (performance.memory) o.heapMB = Math.round(performance.memory.usedJSHeapSize / 1048576); } catch {}
      return o; }, null, null);
    if (h) { (this.healthLog = this.healthLog || []).push({ t: this.now(), phase: this.phase, ...h }); if (this.healthLog.length > 400) this.healthLog.splice(0, 100); } return h;
  }
  /** Are frames still being drawn? (the render loop's own counter, twice) */
  async alive(ms = 900) { const a = await this.safeEv(() => cosmos.engine.frameCount, null, null); await sleep(ms); const b = await this.safeEv(() => cosmos.engine.frameCount, null, null); return a !== null && b !== null && b > a + 2; }
  /** Record one QA check result for the report: status 'pass' | 'FAIL' | 'skipped' | 'info'. */
  qa(check, status, note = '') { (this.qaResults = this.qaResults || []).push({ check, status, note: String(note).slice(0, 300), phase: this.phase, at: this.mmss() }); this.log(`QA ${status}: ${check}${note ? ' - ' + String(note).slice(0, 160) : ''}`); }
  /** How many requests the game has sent to the shared world and how many it has had answers for (the game's own cosmos-request / cosmos-receipt events). */
  async netCounts() { return this.safeEv(() => { const q = window.__qa; return q ? { req: q.req || 0, rec: q.rec || 0, refused: q.refused || 0 } : { req: 0, rec: 0, refused: 0 }; }, null, { req: 0, rec: 0, refused: 0 }); }
  /** Wait until every request the game sent has been answered (or `maxMs`). A tap on a button that talks to the server has not "done nothing" until the reply is in. */
  async settle(maxMs = 12000) {
    const t0 = Date.now(); let quiet = 0;
    while (Date.now() - t0 < maxMs) { const c = await this.netCounts(); if (c.req <= c.rec) { if (++quiet >= 2) return { waited: Date.now() - t0, pending: 0 }; } else quiet = 0; await sleep(120); }
    const c = await this.netCounts(); return { waited: Date.now() - t0, pending: Math.max(0, c.req - c.rec) };
  }
  async watchMessages() {
    const msgs = await this.safeEv(() => { const q = window.__qa; if (!q) return []; const m = q.msgs; q.msgs = []; return m; }, null, []);
    const BAD = /transaction failed|walk to that place|reach the port first|refus|failed|error|cannot|can.?t |not enough|too far|disconnect|denied|invalid|unavailable|offline|not available/i;
    for (const m of msgs) {
      this.msgSeen.push({ t: Date.now(), text: m.text });
      const recent = this.msgSeen.filter(x => x.text === m.text && Date.now() - x.t < 60000).length;
      if (BAD.test(m.text)) {
        const sev = /storage failed|transactions are paused/i.test(m.text) ? 96 : /transaction failed|walk to that place|reach the port first|refused|failed/i.test(m.text) ? 80 : 42;
        this.finding({ kind: 'refusal-message', sev, title: `Game said: "${m.text.slice(0, 70)}"`, detail: `shown in ${m.id || 'the page'} while the bot was: ${this.trail[this.trail.length - 1] || '?'}`, key: 'msg:' + m.text.replace(/\d+/g, 'N').slice(0, 70) });
      }
      if (recent >= 4) this.finding({ kind: 'repeating-message', sev: 70, title: `Same message repeated ${recent}+ times in a minute: "${m.text.slice(0, 60)}"`, detail: 'The game keeps saying the same thing instead of moving on.', key: 'rep:' + m.text.replace(/\d+/g, 'N').slice(0, 60) });
    }
    this.msgSeen = this.msgSeen.filter(x => Date.now() - x.t < 120000);
  }

  // ---- layout audit: overlapping, covered, or off-screen buttons ---------------------------------------------------
  async layoutAudit(tag = '') {
    const r = await this.safeEv(() => {
      const vw = window.innerWidth, vh = window.innerHeight; const out = { off: [], covered: [], overlap: [], tiny: [] };
      const els = [...document.querySelectorAll('button, a[href], input, select, [role=button]')].filter(e => { const cs = getComputedStyle(e); const r = e.getBoundingClientRect();
        return r.width > 2 && r.height > 2 && cs.visibility !== 'hidden' && cs.display !== 'none' && cs.opacity !== '0' && cs.pointerEvents !== 'none' && !e.disabled && !e.closest('[hidden]'); });
      const name = e => (e.id ? '#' + e.id : '') + ' "' + ((e.textContent || e.getAttribute('aria-label') || e.title || '').trim().replace(/\s+/g, ' ').slice(0, 28)) + '"';
      const MODAL = '#settings-panel,#account-panel,#crew-panel,#space-sheet,#multiplayer-panel,#ship-panel'; const modal = e => e.closest(MODAL);
      const boxes = els.map(e => ({ e, r: e.getBoundingClientRect() }));
      for (const { e, r } of boxes) {
        if (r.right < 0 || r.bottom < 0 || r.left > vw || r.top > vh) continue; // fully off screen = not shown (scrolled panels)
        const sc = e.closest('#settings-panel,#account-panel,#crew-panel,#space-sheet,#ship-panel,#multiplayer-panel,[id*=panel]');
        if (!sc && (r.left < -2 || r.top < -2 || r.right > vw + 2 || r.bottom > vh + 2)) out.off.push(name(e) + ` at ${Math.round(r.left)},${Math.round(r.top)} ${Math.round(r.width)}x${Math.round(r.height)} (screen ${vw}x${vh})`);
        const cx = Math.min(vw - 1, Math.max(0, r.left + r.width / 2)), cy = Math.min(vh - 1, Math.max(0, r.top + r.height / 2));
        const top = document.elementFromPoint(cx, cy); if (top && top !== e && !e.contains(top) && !top.contains(e) && top.tagName !== 'CANVAS' && (modal(top) === modal(e) || (modal(top) && modal(e))) ) {
          const tcs = getComputedStyle(top); if (tcs.pointerEvents !== 'none' && tcs.position !== 'sticky') out.covered.push(name(e) + ' is covered by ' + (top.id ? '#' + top.id : top.tagName.toLowerCase() + '.' + String(top.className).slice(0, 20)));
        }
        if (Math.min(r.width, r.height) < 30 && e.tagName === 'BUTTON' && vw < 600) out.tiny.push(name(e) + ` ${Math.round(r.width)}x${Math.round(r.height)}`);
      }
      // an element scrolled out of its panel's visible area still has a rectangle; it is clipped, not overlapping (hit test at its centre)
      const clipOk = b => { const r = b.r, cx = r.left + r.width / 2, cy = r.top + r.height / 2; for (let p = b.e.parentElement; p && p !== document.body; p = p.parentElement) { const o = getComputedStyle(p); if (/(auto|scroll|hidden)/.test(o.overflowY + o.overflowX)) { const q = p.getBoundingClientRect(); if (cx < q.left || cx > q.right || cy < q.top || cy > q.bottom) return false; } } return true; };
      for (let i = 0; i < boxes.length; i++) for (let j = i + 1; j < boxes.length; j++) {
        const a = boxes[i], b = boxes[j]; if (!clipOk(a) || !clipOk(b)) continue; if (a.e.contains(b.e) || b.e.contains(a.e) || (modal(a.e) !== modal(b.e) && (!modal(a.e) || !modal(b.e)))) continue;
        const ix = Math.min(a.r.right, b.r.right) - Math.max(a.r.left, b.r.left), iy = Math.min(a.r.bottom, b.r.bottom) - Math.max(a.r.top, b.r.top);
        if (ix > 4 && iy > 4) { const area = ix * iy, small = Math.min(a.r.width * a.r.height, b.r.width * b.r.height); if (area > .2 * small) out.overlap.push(name(a.e) + ' overlaps ' + name(b.e) + ` by ${Math.round(100 * area / small)}%`); }
      }
      return out; }, null);
    if (!r) return;
    const add = (list, kind, title, sev) => { for (const l of list.slice(0, 6)) { const k = `${kind}:${l.replace(/at -?\d+,-?\d+.*|\d+%|\d+x\d+/g, '').slice(0, 80)}`; if (this.layoutSeen.has(k)) continue; this.layoutSeen.add(k);
      this.finding({ kind, sev, title: `${title}: ${l.slice(0, 90)}`, detail: `${l} (${tag || this.phase}, ${this.profileKey})`, key: k }); } };
    add(r.overlap, 'overlap', 'Buttons overlap', 66); add(r.covered, 'covered', 'A button is covered by something else', 68); add(r.off, 'offscreen', 'A button runs off the screen', 58); add(r.tiny, 'tiny-button', 'Button too small for a thumb', 30);
  }

  // ---- input -------------------------------------------------------------------------------------------------------
  async rect(sel) { return this.safeEv(s => { const e = typeof s === 'string' ? document.querySelector(s) : null; if (!e) return null; const r = e.getBoundingClientRect(); const cs = getComputedStyle(e);
    if (r.width < 2 || r.height < 2 || cs.display === 'none' || cs.visibility === 'hidden') return null; return { x: r.left, y: r.top, w: r.width, h: r.height }; }, sel); }
  async visible(sel) { return !!(await this.rect(sel)); }
  /** A real tap (touchscreen on the phone, mouse on desktop) at a screen point. */
  async tapXY(x, y) { if (this.profile.touch) await this.page.touchscreen.tap(x, y); else { /* the game locks the mouse to the 3D view after a click on it (look with the mouse); a person presses Esc before clicking a button, so the bot lets go of the lock the same way */ try { await this.page.evaluate(() => document.pointerLockElement && document.exitPointerLock()); await sleep(80); } catch {} await this.page.mouse.move(x, y); await this.page.mouse.down(); await sleep(rnd(40, 90)); await this.page.mouse.up(); } }
  /** Tap an element, like a thumb: not dead centre, with an occasional near-miss first. */
  async tap(sel, { miss = 0, why = '' } = {}) {
    const r = await this.rect(sel); if (!r) { return false; }
    if (miss && Math.random() < miss) { const mx = Math.random() < .5 ? r.x - rnd(6, 16) : r.x + r.w + rnd(6, 16); await this.tapXY(Math.max(2, mx), r.y + r.h / 2); this.log(`mis-tap beside ${sel}`); await sleep(rnd(300, 800)); }
    const x = r.x + r.w * rnd(.3, .7), y = r.y + r.h * rnd(.3, .7); await this.tapXY(x, y); this.log(`tap ${sel}${why ? ' (' + why + ')' : ''}`); return true;
  }
  async tapText(re, scopeSel, { why = '' } = {}) {
    const pos = await this.safeEv(({ src, flags, scope }) => { const rx = new RegExp(src, flags); const root = scope ? document.querySelector(scope) : document; if (!root) return null;
      for (const e of root.querySelectorAll('button, [role=button], a')) { const r = e.getBoundingClientRect(); const cs = getComputedStyle(e); if (r.width < 2 || r.height < 2 || cs.display === 'none' || cs.visibility === 'hidden' || e.disabled) continue;
        if (rx.test((e.textContent || '').trim())) { e.scrollIntoView?.({ block: 'nearest' }); const r2 = e.getBoundingClientRect(); return { x: r2.left + r2.width * .5, y: r2.top + r2.height * .5, w: r2.width, h: r2.height, text: (e.textContent || '').trim().slice(0, 40) }; } } return null; }, { src: re.source, flags: re.flags, scope: scopeSel });
    if (!pos) return null; await this.tapXY(pos.x + rnd(-pos.w * .2, pos.w * .2), pos.y + rnd(-pos.h * .15, pos.h * .15)); this.log(`tap button "${pos.text}"${why ? ' (' + why + ')' : ''}`); return pos.text;
  }
  /** Tap somewhere that is just the 3D view (not on a button or panel). */
  async tapEmpty() { const vw = this.profile.ctx.viewport.width, vh = this.profile.ctx.viewport.height;
    for (let i = 0; i < 12; i++) { const x = rnd(30, vw - 30), y = rnd(vh * .25, vh * .8);
      const ok = await this.safeEv(({ x, y }) => { const e = document.elementFromPoint(x, y); return !e || e.tagName === 'CANVAS'; }, { x, y }, false); if (ok) { await this.tapXY(x, y); this.log(`tap on empty 3D view at ${Math.round(x)},${Math.round(y)}`); return true; } } return false; }
  async pressKey(code, ms = 80) { await this.page.keyboard.down(code); await sleep(ms); await this.page.keyboard.up(code); }
  /** Tap the main action button: the thing the game says to do right now. */
  async action({ miss = 0 } = {}) {
    if (await this.visible('#opening-action')) return this.tap('#opening-action', { miss, why: 'opening action' });
    if (await this.visible('#btn-action')) return this.tap('#btn-action', { miss, why: 'action' });
    if (!this.profile.touch) { await this.pressKey('KeyE'); this.log('press E'); return true; }
    return false;
  }

  // the thumb: held stick on the left half (touch), WASD (desktop)
  async stickDown(strength = 1) {
    this.stickStrength = strength; if (this.heldStick) return; this.heldStick = true;
    if (this.profile.touch) await this.safeEv(({ y }) => { const c = document.querySelector('canvas'); const ev = (t, dy) => c.dispatchEvent(new PointerEvent(t, { pointerId: 71, pointerType: 'touch', isPrimary: false, clientX: 80, clientY: y - dy, bubbles: true, cancelable: true })); ev('pointerdown', 0); ev('pointermove', 62 * 1); window.__stickY = y; }, { y: Math.round(this.profile.ctx.viewport.height * .76) });
    else await this.page.keyboard.down('KeyW');
  }
  async stickUp() {
    if (!this.heldStick) return; this.heldStick = false;
    if (this.profile.touch) await this.safeEv(({ y }) => { const c = document.querySelector('canvas'); c.dispatchEvent(new PointerEvent('pointerup', { pointerId: 71, pointerType: 'touch', isPrimary: false, clientX: 80, clientY: y, bubbles: true, cancelable: true })); }, { y: Math.round(this.profile.ctx.viewport.height * .76) });
    else { await this.page.keyboard.up('KeyW'); await this.page.keyboard.up('ShiftLeft').catch(() => {}); }
  }
  async run(on) { if (this.profile.touch) return; if (on) await this.page.keyboard.down('ShiftLeft'); else await this.page.keyboard.up('ShiftLeft'); }
  /** A real look-drag with a second finger (touch) or mouse move (desktop). */
  async lookDrag(dx = 60, dy = 0) {
    const vw = this.profile.ctx.viewport.width, vh = this.profile.ctx.viewport.height;
    if (this.profile.touch) await this.safeEv(async ({ vw, vh, dx, dy }) => { const c = document.querySelector('canvas'); const x0 = vw * .75, y0 = vh * .4; const ev = (t, x, y) => c.dispatchEvent(new PointerEvent(t, { pointerId: 72, pointerType: 'touch', isPrimary: false, clientX: x, clientY: y, bubbles: true, cancelable: true }));
      ev('pointerdown', x0, y0); for (let i = 1; i <= 6; i++) { ev('pointermove', x0 + dx * i / 6, y0 + dy * i / 6); await new Promise(r => setTimeout(r, 16)); } ev('pointerup', x0 + dx, y0 + dy); }, { vw, vh, dx, dy });
    else { await this.page.mouse.move(vw / 2, vh / 2); await this.page.mouse.move(vw / 2 + dx, vh / 2 + dy, { steps: 5 }); }
  }
  async jump() { if (this.profile.touch) { const vw = this.profile.ctx.viewport.width, vh = this.profile.ctx.viewport.height; await this.tapXY(vw * .8, vh * .35); } else await this.pressKey('Space'); this.log('jump'); }
  async releaseAll() { await this.stickUp(); }
}

/** Fort Wayne wall-clock time (America/Indiana/Indianapolis), never UTC: { date: 'YYYY-MM-DD', hm: 'HH:MM' }. */
export function fortWayne(d = new Date()) {
  const p = Object.fromEntries(new Intl.DateTimeFormat('en-CA', { timeZone: 'America/Indiana/Indianapolis', year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', hourCycle: 'h23' }).formatToParts(d).map(x => [x.type, x.value]));
  return { date: `${p.year}-${p.month}-${p.day}`, hm: `${p.hour}:${p.minute}` };
}
