// Kokoro (local, CPU) voices the closing line for the YouTube Shorts cuts, one wav per show voice.  node endtts.mjs
import { join } from 'node:path'; import { pathToFileURL } from 'node:url'; import { homedir } from 'node:os';
const dir = join(homedir(), '.claude', 'voice');
const { KokoroTTS } = await import(pathToFileURL(join(dir, 'node_modules', 'kokoro-js', 'dist', 'kokoro.js')).href);
const tts = await KokoroTTS.from_pretrained('onnx-community/Kokoro-82M-v1.0-ONNX', { dtype: 'q8', device: 'cpu' });
for (const v of ['bm_george', 'af_heart', 'am_michael']) {
  const a = await tts.generate('Full episode, free, at heartbeat observatory dot com.', { voice: v, speed: 1.0 });
  await a.save(`audio/end_${v}.wav`); console.log('ok', v);
}
