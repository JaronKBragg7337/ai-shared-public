// report.mjs - REPORT.md in plain words, worst first, each problem with a screenshot and steps to reproduce.
import { writeFileSync } from 'node:fs';
import { join, relative } from 'node:path';
import { fortWayne } from './core.mjs';

const PHASE_WORDS = {
  opening: 'the opening (crash, climb out, dig the crate, ride to the port)', panels: 'opening the Settings / Account / World / Controls panels', tour: 'walking the port (or the settlement of the start world) and talking to people', lifeboat: 'earning the first ship: buy the two lifeboat parts and fit them',
  hire: 'hiring crew from the crew hall', dig: 'digging regolith and delivering it to the weigh bay', fly: 'boarding the ship, taking a seat and flying a course',
  moonWalk: 'walking on a moon', smoke: 'smoke check (load time, download size, warm reload)', a11y: 'accessibility and readability scan', spam: 'spamming buttons and jumps', lifecycle: 'app to the background, graphics context lost, phone rotated', network: 'network cut, refresh offline, slow connection', economy: 'buy/sell loops and double taps on the shop', edges: 'walking and jumping into walls and edges in 8 directions', perf: 'turning on the spot, reading draw calls and frame times', monkey: 'random tapping everywhere', idle: 'leaving the game alone for 90 s', softlock: 'end-of-run soft-lock check', rover: 'getting into and driving the survey rover', freeplay: 'free play (random walking, tapping, refreshing)', start: 'loading the page', 'opening-bypass': 'starting from the review start (opening skipped)',
};

export function severityWord(sev) { return sev >= 90 ? 'BLOCKER' : sev >= 75 ? 'Serious' : sev >= 55 ? 'Annoying' : sev >= 35 ? 'Minor' : 'Small'; }

export function buildReport({ sessions, vision, outDir, args, buildId, startedAt }) {
  // merge by key across devices
  const merged = new Map();
  for (const s of sessions) for (const f of s.findings.values()) {
    const m = merged.get(f.key);
    if (!m) merged.set(f.key, { ...f, devices: [f.device], count: f.count, session: s });
    else { m.count += f.count; if (!m.devices.includes(f.device)) m.devices.push(f.device); m.sev = Math.max(m.sev, f.sev); if (!m.shot && f.shot) { m.shot = f.shot; m.session = s; } }
  }
  // vision-found problems
  const seenV = new Set();
  for (const s of sessions) for (const r of s.shots) { if (!r.vision?.problems?.length) continue;
    for (const p of r.vision.problems) { const sev = Number(p.severity) || 2; if (sev < 3) continue; const k = 'vision:' + String(p.what).toLowerCase().replace(/[^a-z ]/g, '').slice(0, 50); if (seenV.has(k)) { const m = merged.get(k); if (m) m.count++; continue; } seenV.add(k);
      merged.set(k, { key: k, kind: 'vision', sev: 28 + sev * 7, title: 'Looks wrong in the screenshot: ' + String(p.what).slice(0, 110), detail: `${p.where || ''} (the vision model's description of the screen: ${r.vision.description || ''})`.slice(0, 400), count: 1, firstAt: r.at, lastAt: r.at, phase: r.phase, device: s.profileKey, devices: [s.profileKey], shot: r.rel, steps: [r.ctx].filter(Boolean), extra: [], session: s, visionNote: true }); } }
  // attach what the vision model said about a finding's own screenshot
  for (const m of merged.values()) { if (m.visionNote || !m.shot) continue; const rec = m.session.shots.find(r => r.rel === m.shot); if (rec?.vision) m.vision = rec.vision; }
  // fold the many overlap / covered / off-screen button findings into one entry each, so they do not bury the real problems
  for (const kind of ['overlap', 'covered', 'offscreen', 'tiny-button']) { const g = [...merged.values()].filter(f => f.kind === kind); if (g.length < 2) continue;
    const first = g.sort((a, b) => b.sev - a.sev)[0]; const names = { overlap: 'Buttons overlap each other', covered: 'Buttons are covered by something on top of them', offscreen: 'Buttons run off the screen edge', 'tiny-button': 'Buttons too small for a thumb' };
    const all = g.map(f => f.detail.replace(/\s*\(.*$/, '')).slice(0, 8); for (const f of g) merged.delete(f.key);
    merged.set('group:' + kind, { ...first, key: 'group:' + kind, title: `${names[kind]} (${g.length} places)`, detail: all.join(' ;  '), count: g.reduce((a, f) => a + f.count, 0) }); }
  const list = [...merged.values()].sort((a, b) => b.sev - a.sev || b.count - a.count);
  const top = list.filter(f => f.kind !== 'console-warning');
  const date = (() => { const f = fortWayne(startedAt); return f.date + ' ' + f.hm; })();
  const L = [];
  L.push(`# The Cosmos playtest report`, ``, `Run: ${date} (local)  |  Build under test: \`${buildId || 'unknown'}\`  |  Site: ${args.url}`, ``);
  L.push(`A bot played the live game like a person: real taps, a held thumb on the stick, random waits, mis-taps and refreshes mid-action. It was marked as a test client (\`?qa=1\`) so the server sweeps it away. ` + `\`dev=1\` was added only so the bot can read the game's state (where people stand, button labels); every button was pressed with a real tap.`, ``);
  L.push(`**How to read this:** items titled "Stuck while walking to ..." come from the bot's own steering (its path planner, run-ups and jumps). Treat them as bot-only unless a human also gets stuck at that spot. Black boot and crash-blackout frames that carry a caption are deliberate.`, ``);
  const runs = sessions.map(s => `- **${s.profile.label}**: ${Math.round((s.endedAt - s.t0) / 60000 * 10) / 10} minutes, ${s.shots.length} screenshots, ${s.findings.size} distinct problems`);
  L.push(...runs, ``);
  const videos = sessions.filter(s => s.videoPath).map(s => `- ${s.profile.label}: [session video](${relative(outDir, s.videoPath).replace(/\\/g, '/')})`);
  if (videos.length) L.push(`## Videos`, ``, `Playwright recordings (session length; include the spots phase):`, ...videos, ``);
  L.push(`## Short version`, ``);
  const block = list.filter(f => f.sev >= 90), serious = list.filter(f => f.sev >= 75 && f.sev < 90);
  L.push(`${list.length} distinct problems found: ${block.length} blockers, ${serious.length} serious, ${list.length - block.length - serious.length} smaller.`, ``);
  for (const f of top.slice(0, 5)) L.push(`- **${f.title}** (${severityWord(f.sev)}${f.count > 1 ? ', seen ' + f.count + ' times' : ''})`);
  L.push(``, `## Problems, worst first`, ``);
  let i = 0;
  for (const f of top.slice(0, 40)) {
    i++; const shotPath = f.shot ? `shots-${f.devices[0]}/${f.shot.split('/').pop()}` : null;
    L.push(`### ${i}. ${f.title}`, ``, `- **How bad:** ${severityWord(f.sev)} (score ${f.sev})${f.count > 1 ? `, happened ${f.count} times` : ''}`, `- **Where:** ${PHASE_WORDS[f.phase] || f.phase}, first at ${f.firstAt} into the run, on ${f.devices.map(d => d === 'iphone' ? 'iPhone (WebKit)' : 'desktop (Chromium)').join(' and ')}`);
    L.push(`- **What happened:** ${f.detail || '(see screenshot)'}`);
    if (f.vision?.description) L.push(`- **What the vision model saw:** ${f.vision.description}${f.vision.problems?.length ? ' Flagged: ' + f.vision.problems.map(p => p.what).join('; ') : ''}`);
    if (f.extra?.length) L.push(`- **Later hits:** ${f.extra.slice(0, 2).join(' / ')}`);
    if (f.shot) L.push(`- **Screenshot:** [${f.shot.split('/').pop()}](${f.shot.includes('/') ? f.shot : shotPath})`, ``, `  ![${f.title.slice(0, 40)}](${f.shot.includes('/') ? f.shot : shotPath})`);
    const steps = (f.steps || []).slice(-8); if (steps.length) L.push(``, `- **Steps to reproduce (what the bot did just before):**`, ...steps.map(x => `  1. ${String(x).replace(/^\d\d:\d\d \[[^\]]*\] /, '')}`));
    L.push(``);
  }
  if (top.length > 40) { L.push(`### Smaller problems (not detailed)`, ``, ...top.slice(40).map(f => `- ${f.title} (${f.devices.join('+')}, x${f.count})`), ``); }
  const warns = list.filter(f => f.kind === 'console-warning'); if (warns.length) L.push(`### Console warnings (${warns.length} kinds)`, ``, ...warns.slice(0, 12).map(f => `- ${f.detail.slice(0, 160)} (x${f.count})`), ``);
  // coverage
  L.push(`## What the bot got through`, ``);
  for (const s of sessions) {
    L.push(`### ${s.profile.label}`, ``, `| Step | Result | Time |`, `|---|---|---|`);
    for (const r of s.phaseResults) L.push(`| ${PHASE_WORDS[r.name] || r.name} | ${r.status}${r.note ? ' - ' + r.note : ''} | ${Math.round(r.sec)} s |`);
    const c = s.cover || {}; L.push(``, `People talked to: ${s.talkedCount || 0} of 16. Crew hired: ${s.hiredCount || 0}. Panels opened: ${(c.panels || []).join(', ') || 'none'}. Course to Phobos: ${c['trip-Phobos'] ? 'started' : 'not started'}; Deimos: ${c['trip-Deimos'] ? 'started' : 'not started'}.`, ``);
  }
  const fr = []; for (const s of sessions) for (const f of (s.frames || [])) fr.push({ d: s.profileKey, ...f });
  if (fr.length) { const worst = fr.sort((a, b) => b.max - a.max).slice(0, 5); L.push(`## Frame times (headless software rendering, so a real phone is usually smoother)`, ``, ...worst.map(f => `- ${f.d} / ${f.phase}: typical ${f.med} ms, slowest ${f.max} ms, ${f.over250} frames over 250 ms`), ``);
    const lat = sessions.flatMap(s => s.latencies || []).sort((a, b) => a - b); if (lat.length) L.push(`Button response time (tap to something changing on screen): median ${lat[Math.floor(lat.length / 2)]} ms, slowest ${lat[lat.length - 1]} ms over ${lat.length} taps.`, ``); }

  // QA checks (what professional testers do): a pass/fail table per device
  const qaSessions = sessions.filter(s => (s.qaResults || []).length);
  if (qaSessions.length) { L.push(`## QA checks (the things real testers do besides playing through)`, ``, `See \`tools/playtester/PRACTICES.md\` for why each one exists. FAIL rows are also listed as problems above where they are real bugs.`, ``);
    for (const s of qaSessions) { const q = s.qaResults; const c = k => q.filter(x => x.status === k).length; L.push(`### ${s.profile.label}: ${c('pass')} passed, ${c('FAIL')} failed, ${c('skipped')} skipped, ${c('info')} info`, ``, `| Check | Result | Notes |`, `|---|---|---|`);
      for (const x of q) L.push(`| ${x.check.replace(/\|/g, '/')} | ${x.status} | ${String(x.note || '').replace(/\|/g, '/').replace(/\n/g, ' ').slice(0, 220)} |`); L.push(``); } }
  // performance and memory trend
  const perfRows = []; for (const s of sessions) { const p = s.perf || {}; const h = (s.healthLog || []);
    const first = h.find(x => x.t > 60) || h[0], last = h[h.length - 1];
    perfRows.push(`- **${s.profile.label}**: load to first frames ${s.loadMs ? (s.loadMs / 1000).toFixed(1) + ' s' : '?'}; cold-load download ${p.firstLoad ? p.firstLoad.mb + ' MB in ' + p.firstLoad.requests + ' requests' : '?'}; warm reload ${p.warmReloadMs ? (p.warmReloadMs / 1000).toFixed(1) + ' s' : 'not measured'}; busiest view ${p.peak ? p.peak.calls + ' draw calls, ' + Math.round(p.peak.triangles / 1000) + 'k triangles' : 'not measured'}.` +
      (first && last && h.length > 2 ? ` Over the run (${h.length} samples): graphics geometries ${first.geometries ?? '?'} -> ${last.geometries ?? '?'}, textures ${first.textures ?? '?'} -> ${last.textures ?? '?'}, page elements ${first.dom} -> ${last.dom}${last.heapMB != null ? ', JS heap ' + first.heapMB + ' -> ' + last.heapMB + ' MB' : ' (JS heap is only readable in Chromium)'}.` : '')); }
  if (perfRows.length) L.push(`## Load, size and memory`, ``, ...perfRows, ``);
  if (vision) L.push(`## Vision pass`, ``, vision.skipped ? `Skipped: ${vision.skipped}.` : `A vision model (${vision.model}) looked at ${vision.n} screenshots for about $${vision.cost.toFixed(2)} (cap $1).`, ``);
  for (const s of sessions) if (s.spotInventory) L.push(`## Trouble spot coverage`, ``, `Spot shots by type: ${Object.entries(s.spotCounts || {}).map(([k, v]) => k + ' ' + v).join(', ') || 'none'}. Live inventory: ${s.spotInventory.doors.length} port doors, ${s.spotInventory.counts.pads} pads, ${(s.spotInventory.ships || []).length} parked ships (${(s.spotInventory.ships || []).map(x => x.type).join(', ')}), ${s.spotInventory.signs} port signs. Each shot carries a what-to-look-for line for the vision review; targets and prompts are in spots.json.`, `Math findings (no picture needed): door opening vs prop boxes, duplicate door names, lowered ramp without a visible mesh, repeated sign text, interior door signs falling back to MEDBAY. Inside the ships (aboard, doors at 5 m and 1.5 m, cockpit looking back, each room from its doorway): ${(s.spotInventory.inside?.ships || []).map(x => `${x.ship} ${x.shots} shots`).join(', ') || 'none boarded'}; layouts checked by math only: ${(s.spotInventory.inside?.notBoarded || []).join(', ') || 'none'}. Not yet covered: boarding ships the player does not own (the Meridian), posters over doors, hull see-through is judged by the vision pass only.`, ``);
  L.push(`## Not covered / limits`, ``, `- Real iOS Safari audio, GPU speed and real thumbs are not tested; the phone run uses Playwright's Windows WebKit with a synthetic held thumb (a real second finger is not possible there), but every button is a real touch tap.`, `- Voice chat, other human players and signing in are not exercised.`, `- The bot never sees the world except through the page, so a visual problem is only caught by the pixel check or the vision pass.`, `- Not possible from here (needs a real iPhone or two players): a real phone call or notification banner, lock screen, battery and heat, low-end phone speed, many device models, race-condition duplication between two players. The full list of what real QA does and which parts the bot covers is in tools/playtester/PRACTICES.md.`, ``);
  writeFileSync(join(outDir, 'REPORT.md'), L.join('\n'));
  writeFileSync(join(outDir, 'findings.json'), JSON.stringify(list.map(f => ({ title: f.title, sev: f.sev, kind: f.kind, count: f.count, phase: f.phase, devices: f.devices, firstAt: f.firstAt, detail: f.detail, shot: f.shot, steps: f.steps })), null, 1));
  return { list, top, block, serious };
}
