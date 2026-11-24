// Kokoro-82M (local, Apache-2.0) narration, one wav per script segment.  node tts.mjs [voice] [id id ...]
// kokoro-js silently truncates long inputs (~510 phoneme tokens, about 25 s / 75 words), so each segment is split at
// sentence ends into chunks of <= 45 words, voiced one by one and joined with ffmpeg (a 0.25 s gap between chunks).
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs'; import { join } from 'node:path'; import { pathToFileURL } from 'node:url';
import { homedir } from 'node:os'; import { execFileSync } from 'node:child_process';
const dir = join(homedir(), '.claude', 'voice');
const { KokoroTTS } = await import(pathToFileURL(join(dir, 'node_modules', 'kokoro-js', 'dist', 'kokoro.js')).href);
const tts = await KokoroTTS.from_pretrained('onnx-community/Kokoro-82M-v1.0-ONNX', { dtype: 'q8', device: 'cpu' });
const voice = process.argv[2] || 'bm_george'; const only = process.argv.slice(3);
mkdirSync('audio/parts', { recursive: true });
function chunks(text, limit = 45) {
  const sents = text.match(/[^.!?]+[.!?]+["']?\s*|[^.!?]+$/g).map(s => s.trim()).filter(Boolean);
  const out = []; let cur = '';
  for (const s of sents) {
    const n = (cur + ' ' + s).trim().split(/\s+/).length;
    if (cur && n > limit) { out.push(cur); cur = s; } else cur = (cur + ' ' + s).trim();
  }
  if (cur) out.push(cur); return out;
}
for (const s of JSON.parse(readFileSync('script.json', 'utf8'))) {
  if (only.length && !only.includes(s.id)) continue;
  const parts = chunks(s.say || s.text); const files = [];   // "say" = phonetic respelling for the voice only (captions use "text")
  for (let i = 0; i < parts.length; i++) {
    const a = await tts.generate(parts[i], { voice, speed: 1.06 });
    const p = `audio/parts/${s.id}_${i}.wav`; await a.save(p); files.push(p);
  }
  // join with a short silence between chunks
  const list = files.map(f => `file '${f.replace(/^audio\//, '')}'`).join('\n');
  writeFileSync(`audio/${s.id}.txt`, files.map(f => `file 'parts/${f.split('/').pop()}'\nfile 'parts/gap.wav'`).join('\n'));
  if (!files.includes('audio/parts/gap.wav')) execFileSync('ffmpeg', ['-y', '-v', 'error', '-f', 'lavfi', '-i', 'anullsrc=r=24000:cl=mono', '-t', '0.25', '-ar', '24000', '-ac', '1', 'audio/parts/gap.wav']);
  execFileSync('ffmpeg', ['-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', `audio/${s.id}.txt`, '-ar', '24000', '-ac', '1', `audio/${s.id}.wav`]);
  console.log(s.id, parts.length, 'chunks');
}
