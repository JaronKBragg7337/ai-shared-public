// Kokoro-82M (local, Apache-2.0) narration, one wav per script segment.  node tts.mjs [voice]
import { readFileSync } from 'node:fs'; import { join } from 'node:path'; import { pathToFileURL } from 'node:url'; import { homedir } from 'node:os';
const dir = join(homedir(), '.claude', 'voice');
const { KokoroTTS } = await import(pathToFileURL(join(dir, 'node_modules', 'kokoro-js', 'dist', 'kokoro.js')).href);
const tts = await KokoroTTS.from_pretrained('onnx-community/Kokoro-82M-v1.0-ONNX', { dtype: 'q8', device: 'cpu' });
const voice = process.argv[2] || 'bm_george';
for (const s of JSON.parse(readFileSync('script.json', 'utf8'))) {
  const a = await tts.generate(s.text, { voice, speed: 1.0 });
  await a.save(`audio/${s.id}.wav`); console.log(s.id);
}
