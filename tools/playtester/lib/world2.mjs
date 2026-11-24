// World 2's controls and report are deliberately separate from The Cosmos.
import { mkdirSync, writeFileSync, readFileSync } from 'node:fs';
import { join, resolve, sep, relative } from 'node:path';
import { Session, sleep, fortWayne } from './core.mjs';

const distance = (a, b) => Math.hypot(a.x - b.x, a.z - b.z);
const position = s => s.safeEv(() => {
  const p = window.W2?.state;
  return p && Number.isFinite(p.x) && Number.isFinite(p.z) ? { x: p.x, y: p.y, z: p.z, yaw: p.yaw } : null;
});
const detail = p => p ? `${p.x.toFixed(2)}, ${p.z.toFixed(2)}` : 'unavailable';

async function touch(s, type, x, y) {
  await s.ev(({ type, x, y }) => document.querySelector('#game').dispatchEvent(new PointerEvent(type, {
    pointerId: 71, pointerType: 'touch', isPrimary: true, clientX: x, clientY: y,
    bubbles: true, cancelable: true, button: 0, buttons: type === 'pointerup' ? 0 : 1,
  })), { type, x, y });
}

async function phase(s, name, fn) {
  s.phase = name; const started = Date.now(); let status = 'done', note = '';
  s.log(`=== ${name}`);
  try { note = await fn() || ''; }
  catch (e) {
    status = 'bot error'; note = String(e.message || e).slice(0, 250);
    s.finding({ kind: 'harness', sev: 10, title: `Playtester could not complete ${name}`, detail: note, shot: false });
  }
  s.phaseResults.push({ name, status, note, sec: (Date.now() - started) / 1000 });
  await s.shot('end-of-' + name, { check: false });
}

function check(s, name, status, note, issue) {
  s.qa(name, status, note);
  if (status === 'FAIL' && issue) s.finding({ ...issue, detail: note, steps: issue.steps });
}

async function gesture(s, x, y, dx, dy, ms = 1800) {
  await touch(s, 'pointerdown', x, y);
  const appeared = await s.safeEv(() => {
    const e = document.querySelector('.hb-stick');
    return e ? { on: e.classList.contains('on'), transform: e.style.transform } : null;
  });
  try { await touch(s, 'pointermove', x + dx, y + dy); await sleep(ms); }
  finally { await touch(s, 'pointerup', x + dx, y + dy); }
  return appeared;
}

async function runDevice(profileKey, opts) {
  const s = new Session({ profileKey, outDir: opts.outDir, url: opts.url });
  s.deadline = Date.now() + opts.minutes * 60000;
  let ready = false;
  try {
    await s.launch();
    if (opts.threeDir) {
      const root = resolve(opts.threeDir);
      await s.page.route('https://cdn.jsdelivr.net/npm/three@0.182.0/**', async route => {
        const part = decodeURIComponent(new URL(route.request().url()).pathname.split('/three@0.182.0/')[1] || '');
        const path = resolve(root, part);
        if (!path.startsWith(root + sep)) return route.abort();
        try { await route.fulfill({ path, contentType: 'text/javascript', headers: { 'Access-Control-Allow-Origin': '*' } }); }
        catch { await route.abort(); }
      });
    }
    const url = new URL(opts.url); url.searchParams.set('dev', '1');
    await phase(s, 'load and enter', async () => {
      const start = Date.now(); await s.open(url.toString(), { waitCosmos: false });
      try { await s.page.waitForFunction(() => window.__w2Ready && document.querySelector('#loadingWorld.hidden') && window.W2?.state, null, { timeout: 45000 }); }
      catch {
        const load = await s.safeEv(() => ({ text: document.querySelector('#loadText')?.textContent, failed: document.querySelector('#loadingWorld')?.classList.contains('failed') }));
        check(s, 'World loads', 'FAIL', `World did not reach its first frames in 45 seconds. Loading text: ${load?.text || 'unavailable'}. External requests may be blocked in this environment.`, { kind: 'boot', sev: 90, title: 'World 2 did not finish loading', steps: ['Open the reported URL and wait 45 seconds.'] });
        return 'Boot did not complete; movement and map checks skipped.';
      }
      s.loadMs = Date.now() - start; s.buildId = await s.safeEv(() => window.W2?.BUILD);
      check(s, 'World loads', 'pass', `First frames in ${(s.loadMs / 1000).toFixed(1)} seconds.`);
      await s.tap('#enterButton', { why: 'enter World 2' }); await sleep(1200);
      ready = await s.safeEv(() => document.body.classList.contains('entered') && document.querySelector('#overlay')?.classList.contains('hidden'), null, false);
      check(s, 'Enter the world', ready ? 'pass' : 'FAIL', ready ? 'The opening card closed.' : 'The opening card did not close after pressing Walk the world.', { kind: 'enter', sev: 90, title: 'Could not enter World 2', steps: ['Load World 2.', 'Tap Walk the world.'] });
    });
    if (ready) {
      await phase(s, 'ground tap', async () => {
        await sleep(1000); const a = await position(s);
        const w = s.profile.ctx.viewport.width, h = s.profile.ctx.viewport.height;
        if (!a) { check(s, 'Ground tap does not walk', 'skipped', 'Player position unavailable.'); return; }
        // Read-only scene raycast: choose a visible upward-facing surface, away from
        // every door and plot. Never call the game's action handler to probe a point.
        const point = await s.safeEv(async ({ w, h }) => {
          const THREE = await import('https://cdn.jsdelivr.net/npm/three@0.182.0/build/three.module.js');
          const game = window.W2, ray = new THREE.Raycaster();
          for (const fx of [.48, .35, .65, .22, .78]) for (const fy of [.82, .72, .9]) {
            const x = Math.round(w * fx), y = Math.round(h * fy);
            if (document.elementFromPoint(x, y)?.id !== 'game') continue;
            ray.setFromCamera(new THREE.Vector2(x / innerWidth * 2 - 1, 1 - y / innerHeight * 2), game.camera);
            if (ray.ray.direction.y >= -.02) continue;
            const hit = ray.intersectObjects(game.scene.children, true).find(h => h.face && h.object.visible);
            if (!hit || hit.distance > 40) continue;
            const normal = hit.face.normal.clone().transformDirection(hit.object.matrixWorld);
            if (normal.y < .9) continue;
            if (game.doors.some(d => Math.hypot(d.x - hit.point.x, d.z - hit.point.z) < 5)) continue;
            if (game.plotPads.some(p => p.box && Math.abs(hit.point.x - p.box.x) < p.box.width / 2 + 3 && Math.abs(hit.point.z - p.box.z) < p.box.depth / 2 + 3)) continue;
            return { x, y, worldX: hit.point.x, worldZ: hit.point.z, normalY: normal.y };
          }
          return null;
        }, { w, h }, null);
        if (!point) { check(s, 'Ground tap does not walk', 'skipped', 'Could not confidently identify an unobstructed ground surface away from doors and lots.'); return; }
        const { x, y } = point;
        s.log(`tap lower world view at ${x},${y}; do not touch a door`);
        await s.tapXY(x, y); await sleep(2200); const b = await position(s);
        const changed = await s.safeEv(() => !!window.W2?.inInterior?.() || getComputedStyle(document.querySelector('#claimOverlay')).display !== 'none', null, false);
        if (!b || changed) { check(s, 'Ground tap does not walk', 'skipped', 'Position unavailable or tap opened an object; this was not a ground-only tap.'); return; }
        const d = distance(a, b);
        check(s, 'Ground tap does not walk', d > .08 ? 'FAIL' : 'pass', `Raycast ground at ${point.worldX.toFixed(1)},${point.worldZ.toFixed(1)}; tap at ${x},${y} moved from ${detail(a)} to ${detail(b)} (${d.toFixed(3)} units).`, { kind: 'tap-walk', sev: 85, title: 'Tapping the ground moves the player', steps: ['Enter World 2.', `Tap the ground at ${x}, ${y} on the ${s.profile.label}.`, 'Leave the controls untouched for two seconds; the player should stay still.'] });
      });
      await phase(s, 'walking', async () => {
        let moved = false, tested = 0;
        for (const [index, x] of [Math.round(s.profile.ctx.viewport.width * .18), Math.round(s.profile.ctx.viewport.width * .34)].entries()) {
          const a = await position(s); if (!a) { check(s, 'Walking moves the player', 'skipped', 'Player position unavailable.'); break; }
          let stick;
          if (s.profile.touch) {
            const y = Math.round(s.profile.ctx.viewport.height * .72);
            s.log(`hold floating stick from ${x},${y}, drag ${index ? 'left and upward' : 'upward'} for 1.8 seconds`);
            stick = await gesture(s, x, y, index ? -45 : 0, index ? -25 : -55);
            const at = `translate(${x}px, ${y}px)`;
            check(s, `Stick appears at thumb ${index + 1}`, stick?.on && stick.transform === at ? 'pass' : 'FAIL', `Expected ${at}; observed ${JSON.stringify(stick)}.`, { kind: 'stick-appearance', sev: 65, title: 'Floating stick did not appear where the thumb landed', steps: ['Enter World 2 at phone width.', `Touch the left half at ${x}, ${y}.`, 'The stick should appear under the touch.'] });
          } else { const key = index ? 'KeyA' : 'KeyW'; s.log(`hold ${key} for 1.8 seconds`); await s.pressKey(key, 1800); }
          await sleep(350); const b = await position(s);
          if (!b) { check(s, 'Walking moves the player', 'skipped', 'Player position unavailable after input.'); continue; }
          const d = distance(a, b); tested++; moved ||= d > .08;
          check(s, `Walking direction ${index + 1}`, d > .08 ? 'pass' : 'info', `Position ${detail(a)} to ${detail(b)}; moved ${d.toFixed(2)} world units. A nearby obstacle may block this direction.`);
          if (s.profile.touch) {
            await sleep(1000); const c = await position(s);
            if (c) {
              const drift = distance(b, c);
              check(s, `Stopped after release ${index + 1}`, drift > .08 ? 'FAIL' : 'pass', `After release and a 0.35 s settle, position changed ${drift.toFixed(3)} units over one second.`, { kind: 'release-drift', sev: 75, title: 'Player keeps walking after the thumb is lifted', steps: ['Enter World 2 on a phone-width screen.', `Touch at ${x} on the left side and drag ${index ? 'left and upward' : 'upward'} for about two seconds.`, 'Lift the thumb and watch the player for one second.'] });
            } else check(s, `Stopped after release ${index + 1}`, 'skipped', 'Player position unavailable after release.');
          }
        }
        check(s, 'Walking moves the player', moved ? 'pass' : 'skipped', moved ? 'At least one tested direction moved the player.' : tested ? 'No movement in the tested directions; a nearby obstacle may have blocked them, so this is inconclusive.' : 'Position was unavailable.');
        if (s.profile.touch) {
          const off = await s.safeEv(() => !document.querySelector('.hb-stick')?.classList.contains('on') && !window.W2?.stick?.active, null, false);
          check(s, 'Stick disappears on release', off ? 'pass' : 'FAIL', off ? 'Stick is hidden and inactive.' : 'Stick remained shown or active.', { kind: 'stick-release', sev: 65, title: 'The floating stick did not release', steps: ['Touch and drag the stick.', 'Lift the finger.', 'The stick should disappear and movement should stop.'] });
        }
      });
      await phase(s, 'map', async () => {
        const a = await position(s); const tapped = await s.tap('#minimap', { why: 'open city map' }); await sleep(500);
        const opened = await s.safeEv(() => document.querySelector('#hbpm')?.classList.contains('on'), null, false);
        check(s, 'Map opens', opened ? 'pass' : 'FAIL', tapped ? `Map ${opened ? 'opened' : 'did not open'}.` : 'The minimap was not visible.', { kind: 'map', sev: 65, title: 'City map did not open', steps: ['Enter World 2.', 'Tap the small map in the upper right.'] });
        if (opened) {
          await s.shot('map', { check: false });
          await s.tap('#hbpm .close-btn', { why: 'close map' }); await sleep(500);
          const closed = await s.safeEv(() => !document.querySelector('#hbpm')?.classList.contains('on'), null, false);
          const b = await position(s);
          check(s, 'Map closes', closed ? 'pass' : 'FAIL', closed ? 'Map closed.' : 'Map stayed open.', { kind: 'map-close', sev: 65, title: 'City map did not close', steps: ['Open the city map.', 'Tap the close button.'] });
          if (a && b) check(s, 'Opening map does not walk', distance(a, b) > .08 ? 'FAIL' : 'pass', `Player moved ${distance(a, b).toFixed(3)} world units while opening and closing map.`, { kind: 'map-walk', sev: 75, title: 'Opening the map moved the player', steps: ['Stand still.', 'Open and close the city map.', 'Check whether the player moved.'] });
        }
      });
      await phase(s, 'exploration', async () => {
        const start = await position(s); let count = 0;
        // Bounded even with a long requested budget: prevents unattended indefinite walking.
        while (count < 6 && Date.now() < s.deadline - 4000) {
          if (s.profile.touch) {
            const x = Math.round(s.profile.ctx.viewport.width * .2), y = Math.round(s.profile.ctx.viewport.height * .72);
            s.log(`explore: stick direction ${count % 2 ? 'left' : 'forward'}`);
            await gesture(s, x, y, count % 2 ? -45 : 0, count % 2 ? -25 : -50, 1500);
          } else { const key = ['KeyW', 'KeyA', 'KeyD'][count % 3]; s.log(`explore: hold ${key}`); await s.pressKey(key, 1500); }
          count++; await sleep(300);
        }
        const end = await position(s); await s.layoutAudit('World 2 exploration');
        return `${count} short walking gestures; position ${detail(start)} to ${detail(end)}. This is a limited exploratory pass, not a full tour.`;
      });
    } else for (const name of ['Ground tap does not walk', 'Walking moves the player', 'Map opens', 'Exploration']) check(s, name, 'skipped', 'World was not entered.');
  } catch (e) {
    s.finding({ kind: 'harness', sev: 10, title: 'Playtester could not start or finish', detail: String(e.stack || e).slice(0, 500), shot: false });
    for (const name of ['World loads', 'Ground tap does not walk', 'Walking moves the player', 'Map opens']) check(s, name, 'skipped', 'Playtester encountered an error.');
  } finally {
    s.endedAt = Date.now();
    try { s.videoPath = await s.page.video().path(); } catch {}
    await s.close();
  }
  return s;
}

export async function runWorld2({ argv, shared }) {
  const val = (n, d) => { const i = argv.indexOf('--' + n); return i >= 0 && argv[i + 1] && !argv[i + 1].startsWith('--') ? argv[i + 1] : d; };
  const date = fortWayne();
  const outDir = resolve(val('out', join(shared, 'state', 'playtest', date.date + '_' + date.hm.replace(':', '-') + '-world2')));
  mkdirSync(outDir, { recursive: true });
  const url = val('url', 'https://www.heartbeatobservatory.com/world2/');
  const only = val('only', 'both');
  if (!['both', 'phone', 'desktop'].includes(only)) throw new Error('--only must be phone or desktop');
  const threeDir = val('three-dir', ''); let version = '';
  if (threeDir) { try { version = JSON.parse(readFileSync(join(threeDir, 'package.json'), 'utf8')).version || 'unknown'; } catch { throw new Error('--three-dir must point to a Three.js package directory'); } }
  const phoneMinutes = Number(val('minutes', '30')), desktopMinutes = Number(val('desktop-minutes', '7'));
  if (!Number.isFinite(phoneMinutes) || phoneMinutes <= 0 || !Number.isFinite(desktopMinutes) || desktopMinutes < 0) throw new Error('Minutes must be positive; desktop minutes may be zero');
  console.log('World 2 playtest -> ' + outDir);
  const sessions = [];
  if (only !== 'desktop') sessions.push(await runDevice('iphone', { outDir, url, threeDir, minutes: phoneMinutes }));
  if (only !== 'phone' && desktopMinutes > 0) sessions.push(await runDevice('desktop', { outDir, url, threeDir, minutes: desktopMinutes }));
  const findings = sessions.flatMap(s => [...s.findings.values()].map(f => ({ ...f, device: s.profileKey })));
  const lines = ['# World 2 playtest report', '', `Run: ${date.date} ${date.hm} Fort Wayne time`, `Site: ${url}`, `Build: ${sessions.map(s => s.buildId).find(Boolean) || 'unknown'}`, ''];
  if (threeDir) lines.push(`**Offline substitution:** requests for Three.js 0.182.0 were served from local Three.js ${version} at ${threeDir}. This is an approximation, not a test of the exact live dependency.`, '');
  lines.push('The page was opened with `dev=1` only to read player coordinates and inspect the scene for ground. The phone run uses 393 × 852 WebKit. A real Playwright tap tests the ground; the held thumb is a synthetic pointer gesture. Desktop movement uses keyboard input. The requested minutes set the exploration budget, not a required duration: exploration stops at six gestures or when the budget runs out, while loading and fixed checks may exceed that budget.', '', '## Checks', '');
  for (const s of sessions) {
    lines.push(`### ${s.profile.label}`, '', '| Check | Result | Evidence |', '|---|---|---|');
    for (const q of s.qaResults || []) lines.push(`| ${q.check.replace(/\|/g, '/')} | ${q.status} | ${q.note.replace(/\|/g, '/').replace(/\n/g, ' ')} |`);
    lines.push('', ...s.phaseResults.map(p => `- ${p.name}: ${p.status}${p.note ? ' — ' + p.note : ''} (${Math.round(p.sec)} s)`), '');
  }
  const environment = f => ['http', 'request-failed', 'console-error', 'console-warning', 'harness', 'boot'].includes(f.kind);
  for (const [heading, list, intro] of [
    ['Game behavior observations', findings.filter(f => !environment(f)), 'Confirm each observation with its reproduction steps before treating it as a live bug.'],
    ['Environment, requests and tool observations', findings.filter(environment), 'Local hosting, blocked external dependencies, missing Vercel services, or the test harness can cause these. They do not by themselves establish a live game bug.'],
  ]) {
    lines.push(`## ${heading}`, '', intro, '');
    if (!list.length) lines.push('None recorded.', '');
    for (const f of list.sort((a, b) => b.sev - a.sev)) {
      lines.push(`### ${f.title}`, '', `- Device: ${f.device}; phase: ${f.phase}; score: ${f.sev}`, `- ${f.detail || 'See screenshot.'}`);
      if (f.steps?.length) lines.push('- Steps:', ...f.steps.slice(-8).map(step => `  1. ${String(step).replace(/^\d\d:\d\d \[[^\]]*\] /, '')}`));
      if (f.shot) lines.push(`- [Screenshot](${f.shot})`);
      lines.push('');
    }
  }
  lines.push('## Limits', '', '- This is a short scripted walk and map check, not a complete city, door, multiplayer, visual, or accessibility review.', '- Synthetic pointer gestures and Windows WebKit do not reproduce real iPhone touch, Safari, GPU, heat or battery behavior.', '- A read-only scene raycast seeks a horizontal surface away from doors and lots; the ground check is skipped if no safe target is found.', '- Network failures and local dependency substitutions are reported as observations; they do not establish what happens on the live site.', '');
  for (const s of sessions) if (s.videoPath) lines.push(`- ${s.profile.label}: [session video](${relative(outDir, s.videoPath).replace(/\\/g, '/')})`);
  writeFileSync(join(outDir, 'REPORT.md'), lines.join('\n'));
  writeFileSync(join(outDir, 'findings.json'), JSON.stringify(findings, null, 2));
  console.log(`REPORT: ${join(outDir, 'REPORT.md')} (${findings.length} observations)`);
}
