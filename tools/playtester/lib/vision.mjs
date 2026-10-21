// vision.mjs - after the run, a vision model looks at the screenshots and says what looks wrong.
// Uses the Claude API (key from keys.env, never printed). Small JPEGs, a hard dollar cap.
import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { spawn } from 'node:child_process';
import { join, basename } from 'node:path';

const MODEL = process.env.PLAYTEST_VISION_MODEL || 'claude-sonnet-5-5';
const PRICE_IN = Number(process.env.PLAYTEST_PRICE_IN || 3) / 1e6, PRICE_OUT = Number(process.env.PLAYTEST_PRICE_OUT || 15) / 1e6;   // dollars per token (assumed sonnet-class pricing; the cap is what matters)

// Since 10/8 the MSI has a year-long Claude Code token (CLAUDE_CODE_OAUTH_TOKEN): the vision pass runs on Jaron's plan by
// default instead of API credits. PLAYTEST_VISION=api forces the paid API path.
function planToken() {
  try { const m = readFileSync('C:/Users/lilli/.secrets/keys.env', 'utf8').match(/^CLAUDE_CODE_OAUTH_TOKEN=(.+)$/m); return m ? m[1].trim() : null; } catch { return null; }
}
function loadKey() {
  if (process.env.PLAYTEST_VISION !== 'api') { const t = planToken(); if (t) { process.env.CLAUDE_CODE_OAUTH_TOKEN = t; return null; } }
  if (process.env.ANTHROPIC_API_KEY) return process.env.ANTHROPIC_API_KEY;
  for (const f of ['C:/Users/lilli/.secrets/keys.env', (process.env.USERPROFILE || '') + '/.secrets/keys.env']) {
    try { const m = readFileSync(f, 'utf8').match(/^ANTHROPIC_API_KEY=(.+)$/m); if (m) return m[1].trim().replace(/^["']|["']$/g, ''); } catch {}
  }
  return null;
}

// keys made after Oct 2026 (sk-ant-usr...) need the workspace id header too (keys.env ANTHROPIC_WORKSPACE_ID)
function loadWorkspace() {
  if (process.env.ANTHROPIC_WORKSPACE_ID) return process.env.ANTHROPIC_WORKSPACE_ID;
  for (const f of ['C:/Users/lilli/.secrets/keys.env', (process.env.USERPROFILE || '') + '/.secrets/keys.env']) {
    try { const m = readFileSync(f, 'utf8').match(/^ANTHROPIC_WORKSPACE_ID=(.+)$/m); if (m) return m[1].trim(); } catch {}
  }
  return null;
}

const PROMPT = (rec, device) => `You are a QA tester looking at one screenshot from "The Cosmos", a 3D space game (Mars port, ships, people, mobile and desktop). Device: ${device}. Phase: ${rec.phase}. The test bot's last action: ${rec.ctx || 'unknown'}. What to look for in this shot: ${rec.whatToLookFor || 'general visible defects'}.
First describe, in one plain sentence, what is on screen. Then list ONLY things that look wrong or abnormal that you can actually see: buttons or text overlapping or cut off by the screen edge, a panel covering the controls, black or empty areas where the world should be, objects floating, clipped into each other or at odd angles, people or ships missing where they should be, stretched or broken textures, error messages, unreadable text.
Reply with JSON only: {"description": "...", "problems": [{"what": "...", "where": "...", "severity": 1-5}]}. Use an empty problems list if it looks fine. Do not guess about things you cannot see. DELIBERATE FRAMES, do not flag these: (a) the boot screen: near-black with the title THE COSMOS, a tagline and a pulsing 'Loading the port...' line. The game starts by itself; there is no start button by design. (b) the opening's loading or crash blackout: an all-black viewport with a small caption such as 'Preparing the opening...' or 'Impact. Hold on, the cabin is going dark.' and a Skip intro button; the black is on purpose while the wreck is built. Only flag a black frame if it has NO caption, title or loading text at all.`;


// ---- fallback when there is no API key: the logged-in Claude Code CLI reads the images (uses Jaron's plan, small batches) ----------
function cliBatch(dir, batch, label) {
  const list = batch.map((b, i) => `${i + 1}. ${b.path}  (phase: ${b.phase}; bot's last action: ${(b.ctx || '').slice(0, 90)}${b.whatToLookFor ? '; LOOK FOR: ' + b.whatToLookFor : ''})`).join('\n');
  const prompt = `You are a QA tester for "The Cosmos", a 3D space game (${label}). Use the Read tool to look at each of these screenshots:\n${list}\nFor each, say in one plain sentence what is on screen, then list ONLY things that look wrong or abnormal that you can actually see (buttons/text overlapping or cut off, a panel covering controls, black/empty areas, floating or clipped objects, missing people or ships, broken textures, error messages). Reply with a JSON array only, one object per image in order: [{"n":1,"description":"...","problems":[{"what":"...","where":"...","severity":1-5}]}]. Empty problems list if it looks fine. DELIBERATE FRAMES, do not flag these: (a) the boot screen: near-black with the title THE COSMOS, a tagline and a pulsing 'Loading the port...' line. The game starts by itself; there is no start button by design. (b) the opening's loading or crash blackout: an all-black viewport with a small caption such as 'Preparing the opening...' or 'Impact. Hold on, the cabin is going dark.' and a Skip intro button; the black is on purpose while the wreck is built. Only flag a black frame if it has NO caption, title or loading text at all.`;
  return new Promise(res => {
    const p = spawn(process.platform === 'win32' ? 'claude.exe' : 'claude', ['-p', prompt, '--model', 'sonnet', '--allowedTools', 'Read', '--output-format', 'text'], { cwd: dir });
    let out = ''; p.stdout.on('data', d => out += d); p.stderr.on('data', () => {});
    const to = setTimeout(() => { try { p.kill(); } catch {} res(null); }, 240000);
    p.on('close', () => { clearTimeout(to); const m = out.match(/\[[\s\S]*\]/); try { res(m ? JSON.parse(m[0]) : null); } catch { res(null); } });
    p.on('error', () => { clearTimeout(to); res(null); });
  });
}
export async function cliReview({ items, dir, label = 'phone and desktop', max = 36, log = console.log }) {
  const pick = []; const prob = items.filter(i => i.problem), rest = items.filter(i => !i.problem);
  pick.push(...prob.slice(0, Math.floor(max * .55))); const room = max - pick.length; const step = Math.max(1, rest.length / Math.max(1, room));
  for (let i = 0; i < rest.length && pick.length < max; i += step) pick.push(rest[Math.floor(i)]);
  let n = 0; for (let i = 0; i < pick.length; i += 6) { const batch = pick.slice(i, i + 6); const r = await cliBatch(dir, batch, label); if (!r) { log('vision (cli): a batch returned nothing'); continue; }
    for (const o of r) { const it = batch[(o.n || 0) - 1]; if (it) { it.vision = { description: o.description, problems: o.problems || [] }; n++; } } }
  log(`vision (cli): looked at ${n} screenshots through the Claude Code CLI (Jaron's plan, no API credits)`); return { n, cost: 0, model: 'claude CLI (sonnet)', cli: true };
}

export async function visionReview({ sessions, capUsd = 1.0, maxImages = 90, log = console.log }) {
  const key = loadKey(); if (!key) { log('vision: ANTHROPIC_API_KEY is empty in keys.env, using the Claude Code CLI instead'); const items = []; for (const s of sessions) for (const r of s.shots.filter(r => !r.skipVision)) items.push(r); return await cliReview({ items, dir: sessions[0].outDir, log }); }
  // choose: every problem shot first, then an even spread of the step shots
  const all = []; for (const s of sessions) for (const r of s.shots.filter(r => !r.skipVision)) all.push({ s, r });
  const prob = all.filter(x => x.r.problem), rest = all.filter(x => !x.r.problem);
  const picked = prob.slice(0, Math.floor(maxImages * .5)); const room = maxImages - picked.length;
  if (rest.length && room > 0) { const step = Math.max(1, rest.length / room); for (let i = 0; i < rest.length && picked.length < maxImages; i += step) picked.push(rest[Math.floor(i)]); }
  let cost = 0, n = 0, errors = 0; const queue = [...picked];
  const worker = async () => {
    while (queue.length) {
      if (cost >= capUsd || errors >= 5) return; const { s, r } = queue.shift();
      try {
        const b64 = readFileSync(r.path).toString('base64');
        const res = await fetch('https://api.anthropic.com/v1/messages', { method: 'POST', headers: { 'x-api-key': key, 'anthropic-version': '2023-06-01', 'content-type': 'application/json', ...(loadWorkspace() ? { 'anthropic-workspace-id': loadWorkspace() } : {}) },
          body: JSON.stringify({ model: MODEL, max_tokens: 450, messages: [{ role: 'user', content: [{ type: 'image', source: { type: 'base64', media_type: 'image/jpeg', data: b64 } }, { type: 'text', text: PROMPT(r, s.profile.label) }] }] }) });
        const j = await res.json(); if (!res.ok) { errors++; log(`vision: API ${res.status} ${(j.error?.message || '').slice(0, 100)}`); if (res.status === 401 || res.status === 404) return; continue; }
        const u = j.usage || {}; cost += (u.input_tokens || 0) * PRICE_IN + (u.output_tokens || 0) * PRICE_OUT; n++;
        const text = (j.content || []).map(c => c.text || '').join(''); const m = text.match(/\{[\s\S]*\}/); let parsed = null; try { parsed = m ? JSON.parse(m[0]) : null; } catch {}
        r.vision = parsed || { description: text.slice(0, 200), problems: [] };
      } catch (e) { errors++; log('vision: ' + String(e).slice(0, 100)); }
    }
  };
  await Promise.all([worker(), worker(), worker()]);
  log(`vision: looked at ${n} screenshots, about $${cost.toFixed(2)} (cap $${capUsd})`);
  return { cost, n, errors, model: MODEL };
}
