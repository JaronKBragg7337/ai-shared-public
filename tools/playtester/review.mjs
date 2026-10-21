#!/usr/bin/env node
// Vision pass over an existing run:  node tools/playtester/review.mjs state/playtest/<run>   (adds "Vision notes" to its REPORT.md)
import { readdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { cliReview, visionReview } from './lib/vision.mjs';
const dir = resolve(process.argv[2] || '.'); const items = [];
for (const d of readdirSync(dir).filter(x => x.startsWith('shots-'))) for (const f of readdirSync(join(dir, d)).filter(x => x.endsWith('.jpg'))) {
  const m = f.match(/^(\d+)-([a-zA-Z-]+?)-(.*)\.jpg$/); items.push({ path: join(dir, d, f), rel: d + '/' + f, phase: m ? m[2] : '?', ctx: m ? m[3].replace(/-/g, ' ') : f, problem: /PROBLEM/.test(f), device: d.slice(6) }); }
const label = 'phone and desktop'; const res = await cliReview({ items, dir, label, max: Number(process.argv[3] || 36) });
const flagged = items.filter(i => i.vision?.problems?.some(p => Number(p.severity) >= 3));
const L = ['', '## Vision notes (screenshots reviewed by a vision model)', '', `${res.n} screenshots reviewed with ${res.model}. ${flagged.length} had something flagged.`, ''];
for (const i of flagged) { L.push(`### ${i.rel}`, '', `![](${i.rel})`, '', `Sees: ${i.vision.description}`, '', ...i.vision.problems.filter(p => Number(p.severity) >= 3).map(p => `- (severity ${p.severity}) ${p.what}${p.where ? ' - ' + p.where : ''}`), ''); }
const rp = join(dir, 'REPORT.md'); let r = readFileSync(rp, 'utf8'); r = r.replace(/\n## Vision notes[\s\S]*$/, '').replace('Skipped: no key.', `Done with the Claude Code CLI (the API key line in keys.env is empty): ${res.n} screenshots.`);
writeFileSync(rp, r.trimEnd() + '\n' + L.join('\n')); console.log(`vision notes added to ${rp}`);
