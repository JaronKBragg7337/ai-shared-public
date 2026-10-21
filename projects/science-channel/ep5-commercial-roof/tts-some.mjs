import { readFileSync } from 'node:fs'; import { join } from 'node:path'; import { pathToFileURL } from 'node:url'; import { homedir } from 'node:os';
const dir = join(homedir(), '.claude', 'voice');
const { KokoroTTS } = await import(pathToFileURL(join(dir, 'node_modules', 'kokoro-js', 'dist', 'kokoro.js')).href);
const tts = await KokoroTTS.from_pretrained('onnx-community/Kokoro-82M-v1.0-ONNX', { dtype: 'q8', device: 'cpu' });
const ids = process.argv.slice(2);
for (const s of JSON.parse(readFileSync('script.json', 'utf8'))) {
  if (!ids.includes(s.id)) continue;
  const a = await tts.generate(s.text, { voice: 'bm_george', speed: 1.0 });
  await a.save(`audio/${s.id}.wav`); console.log(s.id);
}
