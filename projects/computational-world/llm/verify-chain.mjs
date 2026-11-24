// Checks a chronicle file: every line must carry the hash of the line before it and hash to its own stamp.
// Reads .jsonl or .jsonl.gz.   node llm/verify-chain.mjs llm/results/chronicle-qwen3.5-4b.jsonl.gz
import fs from 'node:fs';
import zlib from 'node:zlib';
import crypto from 'node:crypto';

for (const file of process.argv.slice(2)) {
  const raw = fs.readFileSync(file), text = (file.endsWith('.gz') ? zlib.gunzipSync(raw) : raw).toString('utf8');
  let prev = 'start', n = 0, bad = 0; const arms = {};
  for (const l of text.split('\n')) {
    if (!l.trim()) continue; n++;
    const { hash, ...rest } = JSON.parse(l);
    if (rest.prev !== prev || crypto.createHash('sha256').update(JSON.stringify(rest)).digest('hex') !== hash) bad++;
    prev = hash; arms[rest.arm] = (arms[rest.arm] || 0) + 1;
  }
  console.log(`${file}: ${n} tries, chain ${bad ? 'BROKEN at ' + bad + ' place(s)' : 'whole'}, last stamp ${prev.slice(0, 16)}, per arm ${Object.entries(arms).map(([a, c]) => a + ' ' + c).join(', ')}`);
}
