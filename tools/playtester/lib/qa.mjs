// qa.mjs - the things professional game testers do that a plain "play through" does not (see tools/playtester/PRACTICES.md).
// Each phase is short, safe for the saved game, and records its verdicts with s.qa(check, 'pass'|'FAIL'|'skipped'|'info', note) for the report,
// and real problems as findings. Run them all with --phases qa (or by name); the default run puts them between the normal phases.
import { sleep, rnd, pick } from './core.mjs';

const wait = ms => sleep(ms);

export const QA_PHASES = ['smoke', 'a11y', 'spam', 'lifecycle', 'network', 'economy', 'edges', 'perf', 'monkey', 'idle', 'softlock'];

export function addQaPhases(P, s, W) {
  const marks = async () => (await s.state()).marks;
  const modalOpen = () => s.safeEv(() => [...document.querySelectorAll('#settings-panel,#account-panel,#crew-panel,#space-sheet,#multiplayer-panel,#ship-panel')].filter(p => getComputedStyle(p).display !== 'none' && p.getBoundingClientRect().height > 20).map(p => p.id), null, []);
  async function closeEverything() {
    for (let k = 0; k < 4; k++) {
      const open = await modalOpen(); if (!open.length) return true;
      if (await s.visible('#btn-close-settings')) await s.tap('#btn-close-settings', { why: 'close settings' });
      else if (!await s.tapText(/^(Close|Goodbye|Not now|✕|×)$/i, '#' + open[0], { why: 'close ' + open[0] })) { if (!s.profile.touch) await s.pressKey('Escape'); else if (await s.visible('#space-sheet .close')) await s.tap('#space-sheet .close'); }
      await wait(500);
    }
    return !(await modalOpen()).length;
  }
  const busyAboard = async () => { const st = await s.state(); return st.aboard || st.seat || st.trip || st.rover || st.opening; };

  // ---- smoke: how fast does it load, how much does it pull over the wire, does a warm reload work ---------------------------------------
  P.smoke = async () => {
    const nav = (s.perf && s.perf.firstLoad) || await s.loadStats();
    s.perf = s.perf || {}; if (nav) { s.perf.firstLoad = nav; s.qa('smoke: page transfer on a cold load', nav.mb > 60 ? 'FAIL' : 'info', `${nav.requests} requests, ${nav.mb} MB over the wire (slowest: ${nav.slow.name} ${nav.slow.ms} ms)`);
      if (nav.mb > 60) s.finding({ kind: 'heavy-load', sev: 45, title: `The game pulls ${nav.mb} MB to load (a lot for a phone on mobile data)`, detail: `${nav.requests} requests; slowest ${nav.slow.name} took ${nav.slow.ms} ms`, key: 'heavy-load' }); }
    if (s.loadMs) { s.qa('smoke: time from opening the link to the first drawn frames', s.loadMs > 30000 ? 'FAIL' : 'pass', `${(s.loadMs / 1000).toFixed(1)} s (headless software rendering, a real phone is usually quicker to draw but slower to download)`);
      if (s.loadMs > 30000) s.finding({ kind: 'slow-load', sev: 50, title: `The game took ${(s.loadMs / 1000).toFixed(0)} s to start drawing`, detail: 'from opening the link to the 3D view running', key: 'slow-load' }); }
    const st = await s.state(); if (st.opening || await busyAboard()) { s.qa('smoke: warm reload', 'skipped', 'mid-story, the refresh checks cover this'); return; }
    const t0 = Date.now(); await s.reload('smoke: warm reload (cache filled)'); s.perf.warmReloadMs = Date.now() - t0;
    s.qa('smoke: warm reload comes back', 'pass', `${((Date.now() - t0) / 1000).toFixed(1)} s`);
  };

  // ---- a11y + readability: text size, contrast, tap size, names on buttons, zoom lock, guidance on screen --------------------------------
  const SCAN = () => {
    const vis = e => { const cs = getComputedStyle(e), r = e.getBoundingClientRect(); return cs.display !== 'none' && cs.visibility !== 'hidden' && cs.opacity !== '0' && r.width > 2 && r.height > 2 && r.bottom > 0 && r.right > 0 && r.left < innerWidth && r.top < innerHeight; };
    const lum = ([r, g, b]) => { const f = v => { v /= 255; return v <= .03928 ? v / 12.92 : Math.pow((v + .055) / 1.055, 2.4); }; return .2126 * f(r) + .7152 * f(g) + .0722 * f(b); };
    const parse = c => { const m = c.match(/rgba?\(([^)]+)\)/); if (!m) return null; const p = m[1].split(',').map(Number); return { r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1 }; };
    const bgOf = e => { for (let p = e; p; p = p.parentElement) { const c = parse(getComputedStyle(p).backgroundColor); if (c && c.a > .85) return [c.r, c.g, c.b]; if (c && c.a > 0) return null; } return null; };
    const out = { small: [], contrast: [], noName: [], tap: [], texts: 0 };
    for (const e of document.querySelectorAll('body *')) {
      if (e.tagName === 'CANVAS' || e.tagName === 'SCRIPT' || e.tagName === 'STYLE' || !vis(e)) continue;
      const own = [...e.childNodes].filter(n => n.nodeType === 3).map(n => n.data).join('').trim(); const label = (e.id ? '#' + e.id : e.tagName.toLowerCase() + '.' + String(e.className).split(' ')[0]);
      if (own.length >= 3) { out.texts++; const cs = getComputedStyle(e), fs = parseFloat(cs.fontSize); if (fs < 11) out.small.push(`${label} ${fs}px "${own.slice(0, 24)}"`);
        const fg = parse(cs.color), bg = bgOf(e); if (fg && bg && fg.a > .5) { const a = lum([fg.r, fg.g, fg.b]), b = lum(bg), ratio = (Math.max(a, b) + .05) / (Math.min(a, b) + .05); const need = fs >= 18 || (fs >= 14 && +cs.fontWeight >= 700) ? 3 : 4.5; if (ratio < need) out.contrast.push(`${label} ${ratio.toFixed(1)}:1 (needs ${need}) "${own.slice(0, 24)}"`); } }
      if (/^(BUTTON|A|INPUT|SELECT)$/.test(e.tagName) || e.getAttribute('role') === 'button') { const r = e.getBoundingClientRect();
        const name = (e.textContent || '').trim() || e.getAttribute('aria-label') || e.getAttribute('title') || e.getAttribute('alt') || ''; if (!name && !e.querySelector('img[alt]')) out.noName.push(label);
        if (Math.min(r.width, r.height) < 44) out.tap.push(`${label} ${Math.round(r.width)}x${Math.round(r.height)}`); }
    }
    const vp = document.querySelector('meta[name=viewport]')?.content || ''; out.zoomLocked = /user-scalable\s*=\s*(no|0)|maximum-scale\s*=\s*1(\.0)?\b/.test(vp); out.viewport = vp;
    out.hasVolume = !!document.querySelector('input[type=range], [id*=volume i], [id*=mute i], [id*=voice i]');
    out.lang = document.documentElement.lang || '';
    return out;
  };
  P.a11y = async () => {
    const scans = []; scans.push(['the main screen', await s.safeEv(SCAN, null, null)]);
    if (await s.visible('#btn-settings') && !await busyAboard()) { await s.tap('#btn-settings', { why: 'open Settings for the accessibility scan' }); await wait(700); scans.push(['the Settings panel', await s.safeEv(SCAN, null, null)]); await s.shot('a11y-settings'); await closeEverything(); }
    const sum = { small: new Set(), contrast: new Set(), noName: new Set(), tap: new Set() }; let zoom = false, vol = false, vp = '';
    for (const [, r] of scans) { if (!r) continue; for (const k of Object.keys(sum)) for (const x of r[k]) sum[k].add(x); zoom = zoom || r.zoomLocked; vol = vol || r.hasVolume; vp = r.viewport; }
    const cut = k => [...sum[k]].slice(0, 6).join(' ; ');
    s.qa('a11y: text is at least 11 px', sum.small.size ? 'FAIL' : 'pass', sum.small.size ? `${sum.small.size} small: ${cut('small')}` : '');
    if (sum.small.size) s.finding({ kind: 'a11y-small-text', sev: 36, title: `Text smaller than 11 px in ${sum.small.size} places (hard to read on a phone)`, detail: cut('small'), key: 'a11y-small' });
    s.qa('a11y: text contrast (4.5:1, or 3:1 for big text)', sum.contrast.size ? 'FAIL' : 'pass', sum.contrast.size ? `${sum.contrast.size} low: ${cut('contrast')}` : '');
    if (sum.contrast.size) s.finding({ kind: 'a11y-contrast', sev: 38, title: `Low text contrast in ${sum.contrast.size} places`, detail: cut('contrast'), key: 'a11y-contrast' });
    s.qa('a11y: every button has a name', sum.noName.size ? 'FAIL' : 'pass', cut('noName'));
    if (sum.noName.size) s.finding({ kind: 'a11y-noname', sev: 34, title: `${sum.noName.size} buttons have no text or label (a screen reader says nothing)`, detail: cut('noName'), key: 'a11y-noname' });
    s.qa('a11y: tap targets at least 44 px (Apple guideline)', sum.tap.size > 3 ? 'FAIL' : 'pass', `${sum.tap.size} smaller: ${cut('tap')}`);
    if (s.profile.touch && sum.tap.size > 3) s.finding({ kind: 'a11y-tap-size', sev: 30, title: `${sum.tap.size} buttons are smaller than the 44 px thumb size`, detail: cut('tap'), key: 'a11y-tapsize' });
    s.qa('a11y: pinch-zoom is not locked off', zoom ? 'FAIL' : 'pass', vp); if (zoom) s.finding({ kind: 'a11y-zoom-locked', sev: 30, title: 'Zooming the page is switched off in the viewport tag', detail: vp, key: 'a11y-zoomlock' });
    s.qa('a11y: a volume or mute control exists', vol ? 'pass' : 'FAIL', '');
    // readability: with nobody touching anything, is a next step visible?
    if (!await busyAboard()) { await s.stickUp();
      const g = await s.safeEv(() => { const t = id => { const e = document.getElementById(id); return e && getComputedStyle(e).display !== 'none' && e.getBoundingClientRect().height > 4 ? (e.innerText || '').replace(/\s+/g, ' ').trim().slice(0, 120) : ''; };
        return { action: t('btn-action'), hint: t('opening-hint'), caption: t('opening-caption'), hud: t('hud'), jobs: t('chip-jobs') || t('quest-panel') || t('quest-deliver'), toast: t('ship-toast') }; }, null, null);
      if (g) { const any = Object.values(g).some(Boolean); s.qa('readability: something on screen tells a player what to do next', any ? 'pass' : 'FAIL', JSON.stringify(g).slice(0, 220));
        if (!any) s.finding({ kind: 'no-guidance', sev: 48, title: 'Standing still after the opening, nothing on screen says what to do next', detail: 'no action button, hint, caption, jobs chip or HUD text was visible', key: 'no-guidance' }); }
      await s.shot('readability-standing-still'); }
  };

  // ---- spam: hammer buttons, double taps, jump spam ----------------------------------------------------------------------------------
  P.spam = async () => {
    if (await busyAboard()) { s.qa('spam: panel buttons hammered', 'skipped', 'aboard or mid-flight'); return; }
    const m0 = await marks(); const n0 = await s.netCounts();
    for (const sel of ['#btn-settings', '#purse', '#multiplayer-button', '#btn-key-controls']) {
      if (!await s.visible(sel)) continue; const r = await s.rect(sel);
      for (let i = 0; i < 10; i++) { await s.tapXY(r.x + r.w * rnd(.3, .7), r.y + r.h * rnd(.3, .7)); await wait(rnd(30, 90)); }
      await wait(600); const open = await modalOpen(); if (open.length > 1) s.finding({ kind: 'spam-two-panels', sev: 55, title: `Hammering ${sel} left ${open.length} panels open at once`, detail: open.join(', '), key: 'spam-panels:' + sel });
      if (!await closeEverything()) s.finding({ kind: 'panel-wont-close', sev: 72, title: `After hammering ${sel} a panel will not close`, detail: (await modalOpen()).join(', '), key: 'spam-stuck:' + sel });
    }
    s.qa('spam: opener buttons hammered 10 times each, panels still open and close cleanly', (await modalOpen()).length ? 'FAIL' : 'pass');
    // the action button: whatever it says right now, 20 taps in two seconds; the game must neither hang nor charge twice
    const lbl = (await s.state()).actionLabel;
    if (lbl && !/ride|board|lift|sit|leave|climb|pilot/i.test(lbl)) { const r = await s.rect('#btn-action') || await s.rect('#opening-action'); if (r) { for (let i = 0; i < 20; i++) { await s.tapXY(r.x + r.w * rnd(.35, .65), r.y + r.h * rnd(.35, .65)); await wait(rnd(40, 110)); } const st = await s.settle(15000);
      s.qa(`spam: action button "${lbl.slice(0, 20)}" tapped 20 times in 2 s`, st.pending ? 'FAIL' : 'pass', st.pending ? `${st.pending} requests never answered` : 'every request answered');
      if (st.pending) s.finding({ kind: 'spam-hang', sev: 80, title: 'After spamming the action button, requests are never answered', detail: `${st.pending} still waiting after ${Math.round(st.waited / 1000)} s`, key: 'spam-hang' }); }
    } else s.qa('spam: action button', 'skipped', `button says "${lbl}" (not safe to hammer)`);
    // jump spam and look spam: frames must keep coming, the player must not leave the ground for good
    for (let i = 0; i < 25; i++) { await s.jump(); await wait(rnd(40, 120)); if (i % 5 === 0) await s.lookDrag(rnd(-200, 200), rnd(-40, 40)); }
    await wait(1500); const alive = await s.alive();
    s.qa('spam: 25 jumps and wild looks, game keeps drawing', alive ? 'pass' : 'FAIL'); if (!alive) s.finding({ kind: 'spam-froze', sev: 92, title: 'The game froze after jump and look spam', detail: 'frame counter stopped', key: 'spam-froze' });
    const m1 = await marks(); const n1 = await s.netCounts(); s.log(`spam: ${n1.req - n0.req} requests sent, purse ${m0} -> ${m1}`);
    if (m0 != null && m1 != null && m1 !== m0) s.finding({ kind: 'spam-money', sev: 78, title: 'The purse changed while only panel buttons and jumps were hammered', detail: `marks ${m0} -> ${m1}`, key: 'spam-money' });
    await s.shot('after-spam');
  };

  // ---- lifecycle: background and return, WebGL context loss, rotation -------------------------------------------------------------------
  P.lifecycle = async () => {
    const before = await s.state(); const same = (a, b) => a.pos && b.pos && a.frame === b.frame && Math.hypot(a.pos.x - b.pos.x, a.pos.z - b.pos.z) < 3;
    // 1. app backgrounded: the same events the browser fires when you press Home on an iPhone
    await s.safeEv(() => { Object.defineProperty(document, 'hidden', { configurable: true, get: () => true }); Object.defineProperty(document, 'visibilityState', { configurable: true, get: () => 'hidden' });
      document.dispatchEvent(new Event('visibilitychange')); window.dispatchEvent(new Event('blur')); window.dispatchEvent(new PageTransitionEvent('pagehide', { persisted: true })); });
    s.log('app sent to the background (hidden, blur, pagehide)'); await wait(8000);
    await s.safeEv(() => { delete document.hidden; delete document.visibilityState; document.dispatchEvent(new Event('visibilitychange')); window.dispatchEvent(new PageTransitionEvent('pageshow', { persisted: true })); window.dispatchEvent(new Event('focus')); });
    await wait(2500); const after = await s.state(); const alive = await s.alive();
    if (after.nocosmos || !alive) { s.qa('lifecycle: back from the background', 'FAIL', 'the game is not drawing'); s.finding({ kind: 'background-broke', sev: 90, title: 'After the app went to the background and came back, the game is frozen or gone', detail: `alive=${alive}`, key: 'background-broke' }); await s.reload('recovering from a background freeze'); }
    else { const bad = []; if (!same(before, after) && !before.opening) bad.push(`position moved ${JSON.stringify(before.pos)} -> ${JSON.stringify(after.pos)}`); if (before.marks != null && before.marks !== after.marks) bad.push(`marks ${before.marks} -> ${after.marks}`); if (before.aboard !== after.aboard) bad.push('aboard changed');
      s.qa('lifecycle: background 8 s and return keeps place, money and ship state', bad.length ? 'FAIL' : 'pass', bad.join('; ')); if (bad.length) s.finding({ kind: 'background-state', sev: 74, title: 'Going to the background and back changed the game state', detail: bad.join('; '), key: 'background-state' }); }
    // 2. the graphics context is taken away (iOS does this to a backgrounded page). The game's own answer is to reload itself in "safe mode" (?tier=safe, reduced graphics).
    const lose = await s.safeEv(() => { const gl = cosmos.engine.renderer.getContext(); const ext = gl && gl.getExtension('WEBGL_lose_context'); if (!ext) return 'unsupported'; window.__ctxEvents = []; const cv = cosmos.engine.renderer.domElement;
      cv.addEventListener('webglcontextlost', () => window.__ctxEvents.push('lost')); cv.addEventListener('webglcontextrestored', () => window.__ctxEvents.push('restored')); ext.loseContext(); return 'lost'; }, null, 'error');
    if (lose !== 'lost') s.qa('lifecycle: graphics context lost and restored', 'skipped', 'this browser does not allow forcing it');
    else {
      await wait(3500); const url = s.page.url(); const safe = /[?&]tier=safe/.test(url);
      if (safe) { await s.page.waitForFunction(() => window.cosmos && cosmos.engine && cosmos.engine.frameCount > 20, null, { timeout: 90000 }).catch(() => {}); await wait(1500); }
      const banner = await s.safeEv(() => document.getElementById('graphics-problem')?.textContent || '', null, ''); const drawing = await s.alive(1200); { const rec = await s.shot('after-context-loss', { check: false }); if (rec) rec.skipVision = true; }   // a deliberate safe-mode screen would only confuse the vision pass
      if (safe) {
        s.qa('lifecycle: graphics context lost, game reloads itself into safe mode and still plays', drawing ? 'info' : 'FAIL', `the game restarted with ?tier=safe (reduced graphics). Banner: "${banner.slice(0, 120)}"`);
        s.finding({ kind: 'context-lost-safe-mode', sev: drawing ? 52 : 85, title: 'When the graphics context is lost (iPhones do this after the app was in the background) the game restarts itself in reduced-graphics "safe mode"' + (drawing ? '' : ' and then does not draw'), detail: `by design (src/core/graphicsHealth.js). The page address gets ?tier=safe and it stays that way for the session, with a red graphics banner: "${banner.slice(0, 100)}". A player who just switched apps and came back is left on worse graphics.`, key: 'context-lost-safe-mode' });
        const u = new URL(url); u.searchParams.delete('tier'); await s.open(u.href); await wait(800);   // back to normal graphics for the rest of the run
      } else {
        await s.safeEv(() => { const gl = cosmos.engine.renderer.getContext(); const ext = gl.getExtension('WEBGL_lose_context'); if (gl.isContextLost()) ext.restoreContext(); }); await wait(4000);
        const ok = await s.alive(1200) && await s.safeEv(() => !cosmos.engine.renderer.getContext().isContextLost(), null, false);
        s.qa('lifecycle: graphics context lost and restored, game draws again', ok ? 'pass' : 'FAIL', 'events: ' + JSON.stringify(await s.safeEv(() => window.__ctxEvents, null, [])));
        if (!ok) { s.finding({ kind: 'context-not-restored', sev: 80, title: 'After the graphics context was lost and restored, the game never drew again', detail: '', key: 'context-lost' }); await s.reload('recovering after a lost graphics context'); } }
    }
    // 3. rotation: landscape and back, with a panel open as well
    const vp0 = s.profile.ctx.viewport; const land = s.profile.touch ? { width: vp0.height, height: vp0.width } : { width: 900, height: 560 };
    for (const withPanel of [false, true]) {
      if (withPanel) { if (!await s.visible('#btn-settings') || await busyAboard()) break; await s.tap('#btn-settings', { why: 'open Settings, then rotate' }); await wait(600); }
      await s.page.setViewportSize(land); await wait(1500);
      const fit = await s.safeEv(() => { const c = document.querySelector('canvas'); const r = c.getBoundingClientRect(); return { cw: Math.round(r.width), ch: Math.round(r.height), iw: innerWidth, ih: innerHeight }; }, null, null);
      await s.shot('rotated' + (withPanel ? '-panel' : '')); await s.layoutAudit('rotated to ' + land.width + 'x' + land.height);
      const bad = fit && (Math.abs(fit.cw - fit.iw) > 6 || Math.abs(fit.ch - fit.ih) > 6);
      s.qa(`lifecycle: rotate to ${land.width}x${land.height}${withPanel ? ' with Settings open' : ''}, the 3D view fills the screen`, bad ? 'FAIL' : 'pass', fit ? JSON.stringify(fit) : '');
      if (bad) s.finding({ kind: 'rotate-canvas', sev: 68, title: 'After rotating the phone the 3D view does not fill the screen', detail: JSON.stringify(fit), key: 'rotate-canvas' + withPanel });
      await s.page.setViewportSize(vp0); await wait(1200); if (withPanel) await closeEverything();
    }
    await s.layoutAudit('rotated back'); if (!await s.alive()) s.finding({ kind: 'rotate-froze', sev: 88, title: 'The game stopped drawing after rotating', detail: '', key: 'rotate-froze' });
  };

  // ---- network: offline mid-play, back online; refresh while offline; slow network (Chromium) ----------------------------------------------------
  P.network = async () => {
    if (await busyAboard()) { s.qa('network: offline and back', 'skipped', 'aboard or mid-flight'); return; }
    const m0 = await marks(); const conn0 = await s.safeEv(() => !!cosmos.world?.connected, null, null); const st0 = await s.state();
    s.offline = true; await s.ctx.setOffline(true); s.log('NETWORK CUT');
    await wait(2500); if (await s.visible('#purse')) { await s.tap('#purse', { why: 'tap while offline' }); await wait(900); await s.shot('offline-purse'); await closeEverything(); }
    await s.stickDown(); await wait(2500); await s.stickUp(); await wait(7000);
    const said = (await s.safeEv(() => (window.__qa?.msgs || []).map(m => m.text).slice(-6), null, [])).filter(m => /offline|connect|lost|reconnect|network|internet|sync|saved|save/i.test(m)); const conn1 = await s.safeEv(() => !!cosmos.world?.connected, null, null); await s.shot('offline-after-8s');
    const stillDrawing = await s.alive(); s.qa('network: while offline the game keeps drawing and does not crash', stillDrawing ? 'pass' : 'FAIL');
    s.qa('network: the game tells the player the connection is gone (within about 12 s)', (conn1 === false || said.length) ? 'pass' : 'info', `connected flag ${conn0} -> ${conn1}; messages: ${said.join(' | ').slice(0, 140)}`);
    if (conn1 !== false && !said.length) s.finding({ kind: 'offline-silent', sev: 28, title: 'Network cut for about 12 s and the game said nothing and still thinks it is connected', detail: `connected=${conn1}. A hint only: the bot's offline switch may not cut a socket that is already open, so a real phone going into a tunnel could behave differently.`, key: 'offline-silent' });
    await s.ctx.setOffline(false); s.log('NETWORK BACK'); const t0 = Date.now(); let back = false;
    while (Date.now() - t0 < 45000) { const c = await s.safeEv(() => !!cosmos.world?.connected, null, null); const nc = await s.netCounts(); if ((c === true || c === null) && nc.req <= nc.rec) { back = true; break; } await wait(1000); }
    s.offline = false; await wait(1500); const m1 = await marks(); const st1 = await s.state();
    s.qa('network: after the network returns the game reconnects and answers again', back ? 'pass' : 'FAIL', `${((Date.now() - t0) / 1000).toFixed(0)} s`);
    if (!back) s.finding({ kind: 'no-reconnect', sev: 88, title: 'The game never reconnected after the network came back', detail: '45 s after reconnecting, still not connected or requests unanswered', key: 'no-reconnect' });
    const bad = []; if (m0 != null && m1 != null && m0 !== m1) bad.push(`marks ${m0} -> ${m1}`); if (st0.pos && st1.pos && st0.frame === st1.frame && Math.hypot(st0.pos.x - st1.pos.x, st0.pos.z - st1.pos.z) > 40) bad.push('player ended up somewhere else');
    s.qa('network: money and place unchanged by a network blip', bad.length ? 'FAIL' : 'pass', bad.join('; ')); if (bad.length) s.finding({ kind: 'offline-state', sev: 78, title: 'A short network cut changed money or place', detail: bad.join('; '), key: 'offline-state' });
    // a refresh while offline (a phone in a lift), then the network returns and a refresh must bring the game back
    s.offline = true; await s.ctx.setOffline(true); try { await s.page.reload({ waitUntil: 'domcontentloaded', timeout: 12000 }); } catch {} await wait(1000); s.offline = false; await s.ctx.setOffline(false); await wait(500);
    let recovered = true; try { await s.reload('refresh after being offline'); } catch { recovered = false; }
    s.qa('network: refresh while offline, then online again, the game comes back', recovered ? 'pass' : 'FAIL'); if (!recovered) s.finding({ kind: 'offline-refresh', sev: 82, title: 'Refreshing while offline and then going online did not bring the game back', detail: '', key: 'offline-refresh' });
    // slow connection (Chromium only: the DevTools protocol)
    if (!s.profile.touch) { try { const cdp = await s.ctx.newCDPSession(s.page); await cdp.send('Network.enable'); await cdp.send('Network.emulateNetworkConditions', { offline: false, latency: 900, downloadThroughput: 60 * 1024, uploadThroughput: 30 * 1024 });
        s.log('SLOW NETWORK on (900 ms delay, 60 KB/s)'); const t1 = Date.now(); if (await s.visible('#btn-settings')) { await s.tap('#btn-settings', { why: 'tap on a slow network' }); await wait(1500); await closeEverything(); }
        const sq = await s.settle(20000); await cdp.send('Network.emulateNetworkConditions', { offline: false, latency: 0, downloadThroughput: -1, uploadThroughput: -1 }); await cdp.detach();
        s.qa('network: slow connection (900 ms, 60 KB/s) for a panel tap', sq.pending ? 'FAIL' : 'pass', `${Math.round((Date.now() - t1) / 1000)} s`); } catch (e) { s.qa('network: slow connection', 'skipped', String(e.message).slice(0, 80)); } }
    else s.qa('network: slow connection', 'skipped', 'throttling only exists in Chromium; the phone profile does the offline test');
  };

  // ---- economy: buy/sell loops must not profit, money never negative, a double tap charges once ---------------------------------------------------
  P.economy = async () => {
    const shop = await (P.findShop ? P.findShop() : null);
    if (!shop) { s.qa('economy: buy then sell loop', 'skipped', 'no shop reachable on this world'); return; }
    const m0 = await marks(); if (m0 == null) { s.qa('economy', 'skipped', 'cannot read the purse'); await closeEverything(); return; }
    await s.tapText(/Show me what you buy/i, '#crew-panel', { why: 'open the shop' }); await wait(900); await s.shot('economy-shop');
    let unit = null; const log = [];
    for (let round = 0; round < 3; round++) {
      const a = await marks(); if (!await s.tapText(/^Buy/i, '#crew-panel', { why: 'buy one' })) { s.qa('economy: shop has something to buy', 'skipped', 'no Buy button'); break; } await s.settle(10000); await wait(500);
      const b = await marks(); if (round === 0 && a != null && b != null) unit = a - b; if (b == null) break;
      if (b > a) s.finding({ kind: 'buy-pays-you', sev: 92, title: 'Buying something INCREASED the purse', detail: `marks ${a} -> ${b}`, key: 'buy-pays' });
      if (!await s.tapText(/^Sell/i, '#crew-panel', { why: 'sell it straight back' })) { log.push('no Sell button after buying'); break; } await s.settle(10000); await wait(500);
      const c = await marks(); log.push(`round ${round + 1}: ${a} -> ${b} -> ${c}`);
      if (c != null && c > a) s.finding({ kind: 'buy-sell-profit', sev: 95, title: 'EXPLOIT: buying and then selling straight back makes money', detail: `marks ${a} -> bought -> ${b} -> sold -> ${c}; repeat for free money`, key: 'buy-sell-profit' });
      if (c != null && c < 0) s.finding({ kind: 'negative-money', sev: 95, title: 'The purse went below zero', detail: `marks ${c}`, key: 'negative-money' });
    }
    // double tap: two Buy taps 40 ms apart must charge about twice, never once-for-two or three-times-for-two
    const d0 = await marks(); const r = (await s.safeEv(() => { const e = [...document.querySelectorAll('#crew-panel button')].find(b => /^Buy/i.test((b.textContent || '').trim())); if (!e) return null; e.scrollIntoView?.({ block: 'nearest' }); const q = e.getBoundingClientRect(); return { x: q.left + q.width / 2, y: q.top + q.height / 2 }; }, null, null));
    if (r && unit > 0) { await s.tapXY(r.x, r.y); await wait(40); await s.tapXY(r.x, r.y); await s.settle(12000); await wait(600); const d1 = await marks(); const spent = d0 - d1; const ok = spent === unit || spent === 2 * unit;
      s.qa('economy: double-tapping Buy charges for exactly what was delivered (1x or 2x the price)', ok ? 'pass' : 'FAIL', `price ${unit}, spent ${spent}`); if (!ok) s.finding({ kind: 'double-charge', sev: 85, title: 'Double-tapping Buy charged an odd amount', detail: `price ${unit}, spent ${spent}`, key: 'double-charge' });
      for (let i = 0; i < 3; i++) { if (!await s.tapText(/^Sell/i, '#crew-panel', { why: 'sell the extras back' })) break; await s.settle(8000); await wait(400); } }
    const m1 = await marks(); s.qa('economy: buy/sell loops never make a profit and the purse stays at or above zero', (m1 != null && m1 > m0) || (m1 != null && m1 < 0) ? 'FAIL' : 'pass', `purse ${m0} -> ${m1}; ${log.join(' | ')}`);
    await s.tapText(/Back to conversation/i, '#crew-panel', { why: 'back' }); await closeEverything(); await s.shot('economy-done');
  };

  // ---- edges: walk into everything --------------------------------------------------------------------------------------------------------
  P.edges = async () => {
    if (await busyAboard()) { s.qa('edges: walking into walls and edges', 'skipped', 'aboard or mid-flight'); return; }
    await closeEverything(); const start = await s.safeEv(() => { const w = cosmos.walker.worldPos; return { x: w.x, y: w.y, z: w.z }; }, null, null); if (!start) return;
    let far = 0; const legMs = s.profile.touch ? 9000 : 7000;
    for (let k = 0; k < 8; k++) {
      if (s.overTime(0.3)) break;
      await s.safeEv(a => { cosmos.walker.yaw = a; cosmos.walker.pitch = 0; }, k * Math.PI / 4); await s.stickDown(); if (!s.profile.touch) await s.run(true);
      const t0 = Date.now(); let n = 0; while (Date.now() - t0 < legMs) { await wait(1000); if (++n % 2 === 0) await s.jump(); }
      if (!s.profile.touch) await s.run(false); await s.stickUp();
      const here = await s.safeEv(() => { const w = cosmos.walker.worldPos; return { x: w.x, y: w.y, z: w.z }; }, null, null); if (here) far = Math.max(far, Math.hypot(here.x - start.x, here.y - start.y, here.z - start.z));
      await s.watchMessages();
      if (k % 3 === 2) await s.shot('edges-leg-' + k);
      await s.safeEv(a => { cosmos.walker.yaw = a + Math.PI; }, k * Math.PI / 4); await s.stickDown(); await wait(legMs * .8); await s.stickUp();   // and back the way it came
    }
    const fell = [...s.findings.values()].some(f => f.kind === 'fell-through'); const alive = await s.alive();
    s.qa('edges: walked and jumped into walls in 8 directions, never fell through', fell ? 'FAIL' : 'pass', `furthest ${Math.round(far)} m from where it started`); s.qa('edges: still drawing afterwards', alive ? 'pass' : 'FAIL');
    if (far > 900) s.finding({ kind: 'no-boundary', sev: 35, title: `The player can wander ${Math.round(far)} m from the settlement (is there an edge of the world?)`, detail: 'info: only a problem if there is nothing out there', key: 'no-boundary' });
    await s.shot('edges-done');
  };

  // ---- perf: look all the way round and read the graphics counters ---------------------------------------------------------------------------
  P.perf = async () => {
    if (await busyAboard()) { s.qa('perf: draw calls and triangles', 'skipped', 'aboard or mid-flight'); return; }
    await s.stickUp(); await s.frameStats(); let peak = { calls: 0, triangles: 0 }, worst = null;
    for (let k = 0; k < 12; k++) { await s.safeEv(a => { cosmos.walker.yaw = a; cosmos.walker.pitch = (a % 2) * .25 - .1; }, k * Math.PI / 6); await wait(700); const h = await s.health(); if (h?.calls > peak.calls) peak = { calls: h.calls, triangles: h.triangles || 0 }; }
    const f = await s.frameStats(); s.perf = s.perf || {}; s.perf.peak = peak; s.perf.lookRound = f;
    const budget = s.profile.touch ? 33 : 17; const slowP = f && f.p95 > budget * 2;
    s.qa(`perf: turning on the spot, 95 percent of frames under ${budget * 2} ms`, slowP ? 'FAIL' : 'pass', f ? `median ${f.med} ms, 95th ${f.p95} ms, slowest ${f.max} ms; peak ${peak.calls} draw calls, ${Math.round(peak.triangles / 1000)}k triangles (headless software rendering, judge relatively)` : '');
    if (peak.calls > 1500 && s.profile.touch) s.finding({ kind: 'many-draw-calls', sev: 34, title: `${peak.calls} draw calls in one view (a phone GPU likes under about 1000)`, detail: `${Math.round(peak.triangles / 1000)}k triangles`, key: 'drawcalls' });
  };

  // ---- monkey: random taps everywhere for a while, nothing destructive; money and place must not move -------------------------------------------------
  P.monkey = async () => {
    if (await busyAboard()) { s.qa('monkey: random taps', 'skipped', 'aboard or mid-flight'); return; }
    await closeEverything(); const m0 = await marks(); const end = Date.now() + (s.profile.touch ? 40000 : 30000); let taps = 0;
    const SKIP = /buy|sell|hire|delete|reset|erase|sign ?out|log ?out|new game|clear|wipe|solo|offline|leave|quit|exit|disconnect|switch|accept|deliver|ride|board|join|take|pay|purchase|drop all|stand/i;
    while (Date.now() < end && !s.overTime(0.2)) {
      const r = Math.random();
      if (r < .55) { const t = await s.safeEv(skip => { const re = new RegExp(skip, 'i'); const els = [...document.querySelectorAll('button, [role=button], a[href]')].filter(e => { const q = e.getBoundingClientRect(), cs = getComputedStyle(e); return q.width > 4 && q.height > 4 && cs.display !== 'none' && cs.visibility !== 'hidden' && q.bottom > 0 && q.top < innerHeight && !e.disabled && !re.test(e.textContent || '') && !re.test(e.id) && !e.closest('a[href^="http"]') && !(e.tagName === 'A'); });
          if (!els.length) return null; const e = els[Math.floor(Math.random() * els.length)]; const q = e.getBoundingClientRect(); return { x: q.left + q.width * (.3 + Math.random() * .4), y: q.top + q.height * (.3 + Math.random() * .4), n: (e.id || e.textContent || '').trim().slice(0, 24) }; }, SKIP.source, null);
        if (t) { await s.tapXY(t.x, t.y); s.log('monkey tap ' + t.n); taps++; } }
      else if (r < .70) await s.tapEmpty(); else if (r < .80) await s.jump(); else if (r < .92) await s.lookDrag(rnd(-250, 250), rnd(-60, 60));
      else if (s.profile.touch) { await s.stickDown(); await wait(rnd(300, 1500)); await s.stickUp(); } else await s.pressKey(pick(['KeyA', 'KeyD', 'KeyW', 'KeyS', 'Escape', 'KeyE', 'KeyM', 'Tab']), rnd(60, 400));
      await wait(rnd(120, 450)); if (taps % 8 === 0) await s.watchMessages();
    }
    await s.stickUp(); await closeEverything(); await s.settle(8000); const m1 = await marks(); const alive = await s.alive();
    s.qa(`monkey: ${taps} random button taps and wild gestures, no crash`, alive ? 'pass' : 'FAIL'); if (!alive) s.finding({ kind: 'monkey-froze', sev: 92, title: 'Random tapping froze the game', detail: '', key: 'monkey-froze' });
    if (m0 != null && m1 != null && m0 !== m1) s.finding({ kind: 'monkey-money', sev: 70, title: 'Random tapping on harmless buttons changed the purse', detail: `marks ${m0} -> ${m1}`, key: 'monkey-money' });
    await s.shot('monkey-done'); await s.layoutAudit('after monkey');
  };

  // ---- idle: leave it alone ---------------------------------------------------------------------------------------------------------------------------
  P.idle = async () => {
    const stop = s.stop; if (stop) stop.paused = true;
    try {
      await s.stickUp(); await closeEverything(); const st0 = await s.state(); const h0 = await s.health(); const f0 = await s.frameStats(); const secs = 90; const t0 = Date.now(); s.log(`idle for ${secs} s, no input`);
      let lastShot = 0; while (Date.now() - t0 < secs * 1000 && !s.overTime(0.1)) { await wait(15000); await s.health(); await s.watchMessages(); if (Date.now() - lastShot > 40000) { lastShot = Date.now(); await s.shot('idle'); } }
      const st1 = await s.state(); const h1 = await s.health(); const f1 = await s.frameStats(); const alive = await s.alive();
      const drift = st0.pos && st1.pos && st0.frame === st1.frame ? Math.hypot(st0.pos.x - st1.pos.x, st0.pos.z - st1.pos.z) : 0;
      s.qa('idle: 90 s with no input, still drawing, still connected', alive && !st1.nocosmos ? 'pass' : 'FAIL'); if (!alive) s.finding({ kind: 'idle-froze', sev: 90, title: 'The game stopped drawing while left idle', detail: '', key: 'idle-froze' });
      s.qa('idle: the player does not drift or slide while standing still', drift > 1.5 ? 'FAIL' : 'pass', `${drift.toFixed(1)} m`); if (drift > 1.5) s.finding({ kind: 'idle-drift', sev: 55, title: `The player slid ${drift.toFixed(1)} m while nobody touched anything`, detail: `from ${JSON.stringify(st0.pos)} to ${JSON.stringify(st1.pos)}`, key: 'idle-drift' });
      if (f0 && f1) s.qa('idle: frame time stays steady', f1.med > Math.max(f0.med * 2, 40) ? 'FAIL' : 'pass', `median ${f0.med} ms -> ${f1.med} ms`);
      if (h0 && h1) { const grew = (h1.heapMB != null && h0.heapMB != null && h1.heapMB > h0.heapMB * 1.5 && h1.heapMB - h0.heapMB > 40) || (h0.geometries && h1.geometries > h0.geometries * 1.5 && h1.geometries - h0.geometries > 50) || (h0.textures && h1.textures > h0.textures * 1.5 && h1.textures - h0.textures > 30);
        s.qa('idle: memory does not grow while nothing happens', grew ? 'FAIL' : 'pass', `heap ${h0.heapMB ?? '?'} -> ${h1.heapMB ?? '?'} MB, geometries ${h0.geometries ?? '?'} -> ${h1.geometries ?? '?'}, textures ${h0.textures ?? '?'} -> ${h1.textures ?? '?'}`);
        if (grew) s.finding({ kind: 'idle-leak', sev: 60, title: 'Memory kept growing while the game sat idle (a leak)', detail: JSON.stringify({ before: h0, after: h1 }), key: 'idle-leak' }); }
    } finally { if (stop) stop.paused = false; }
  };

  // ---- softlock: after everything above, can the player still move and act? -----------------------------------------------------------------------------
  P.softlock = async () => {
    await s.stickUp(); await closeEverything(); const st = await s.state();
    if (st.aboard || st.seat || st.trip || st.rover || st.opening) { s.qa('softlock: the player can still move at the end', 'skipped', 'aboard or mid-flight (stand-up and exit are covered by the fly phase)'); return; }
    await s.reload('end-of-run soft-lock check'); await closeEverything(); const a = await s.state();
    await s.safeEv(() => { cosmos.walker.pitch = 0; }); await s.stickDown(); await wait(3500); await s.stickUp(); const b = await s.state();
    const moved = a.pos && b.pos ? Math.hypot(a.pos.x - b.pos.x, a.pos.z - b.pos.z) : 0; const modals = await modalOpen();
    s.qa('softlock: after a refresh the player can still walk', moved > 1 ? 'pass' : 'FAIL', `moved ${moved.toFixed(1)} m in 3.5 s`);
    if (moved <= 1) { await s.shot('softlock-cannot-move'); s.finding({ kind: 'soft-lock', sev: 93, title: 'After a refresh the player cannot walk (soft lock?)', detail: `held the stick forward 3.5 s and moved ${moved.toFixed(1)} m; panels open: ${modals.join(',') || 'none'}; button "${b.actionLabel}"`, key: 'soft-lock-end' }); }
    s.qa('softlock: no panel stuck on screen after a refresh', modals.length ? 'FAIL' : 'pass', modals.join(','));
  };
}
