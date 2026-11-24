// Heartbeat Map Briefing - one command renders any date.
//
//   node projects/map-briefing/render.mjs 2026-11-22              -> out/2026-11-22-vertical.mp4 (1080x1920) + stills
//   node projects/map-briefing/render.mjs 2026-11-22 --wide       -> out/2026-11-22-wide.mp4 (1920x1080), same scenes
//   node projects/map-briefing/render.mjs 2026-11-22 --stills     -> only the stills (fast check of every story)
//   node projects/map-briefing/render.mjs 2026-11-22 --draft      -> half size, 15 fps (quick look at motion)
//   options: --fps 30  --music <file|none>  --auto (ignore a hand-written board, build it from the episode)
//
// Input: boards/<date>.json if it exists (a storyboard written by the news writer), otherwise the board is built
// automatically from https://www.heartbeatobservatory.com/news/episodes/<date>.json by board.mjs.
// Frame-stepped and deterministic: the page draws second t exactly, we screenshot it as JPEG (no PNG reader anywhere),
// then ffmpeg encodes and the result is checked against the rendered frames. A slow MSI only makes it take longer.
import { createRequire } from "node:module";
import { spawn } from "node:child_process";
import http from "node:http";
import fs from "node:fs";
import path from "node:path";
import os from "node:os";
import { fileURLToPath } from "node:url";
import { buildBoard } from "./board.mjs";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const require = createRequire(path.join(HERE, "..", "..", "tools", "site-reel", "package.json"));
const { chromium } = require("playwright-core");

const args = process.argv.slice(2);
const date = args.find(a => /^\d{4}-\d{2}-\d{2}$/.test(a));
const has = k => args.includes("--" + k);
const opt = (k, d) => { const i = args.indexOf("--" + k); return i >= 0 ? args[i + 1] : d; };
if (!date) { console.error("usage: node render.mjs <YYYY-MM-DD> [--wide] [--stills] [--draft] [--fps 30] [--music file] [--auto]"); process.exit(1); }

const wide = has("wide"), draft = has("draft"), stillsOnly = has("stills");
const fps = Number(opt("fps", draft ? 15 : 30));
const scale = draft ? .5 : 1;
const w = Math.round((wide ? 1920 : 1080) * scale), h = Math.round((wide ? 1080 : 1920) * scale);
const outDir = path.join(HERE, "out"); fs.mkdirSync(outDir, { recursive: true });
const tagName = (wide ? "wide" : "vertical") + (draft ? "-draft" : "");
const outFile = path.join(outDir, `${date}-${tagName}.mp4`);

// ---- 1. the board
const handBoard = path.join(HERE, "boards", `${date}.json`);
let board;
if (fs.existsSync(handBoard) && !has("auto")) { board = JSON.parse(fs.readFileSync(handBoard, "utf8")); console.log("board: " + handBoard); }
else {
  const epFile = path.join(HERE, "data", `${date}.json`);
  if (!fs.existsSync(epFile)) {
    const r = await fetch(`https://www.heartbeatobservatory.com/news/episodes/${date}.json`);
    if (!r.ok) { console.error(`no episode for ${date} (HTTP ${r.status})`); process.exit(2); }
    fs.mkdirSync(path.dirname(epFile), { recursive: true }); fs.writeFileSync(epFile, await r.text());
  }
  board = buildBoard(JSON.parse(fs.readFileSync(epFile, "utf8")), JSON.parse(fs.readFileSync(path.join(HERE, "vendor", "countries.json"), "utf8")));
  fs.writeFileSync(path.join(HERE, "boards", `${date}.auto.json`), JSON.stringify(board, null, 1));
  console.log(`board: built automatically from the episode (${board.stops.length} stops) -> boards/${date}.auto.json`);
}
if (!board.stops?.length) { console.error("board has no stops (no story with a place we could map)"); process.exit(3); }

// ---- 2. tiny local server for the scene (closed at the end)
const MIME = { ".html": "text/html", ".js": "text/javascript", ".mjs": "text/javascript", ".json": "application/json", ".jpg": "image/jpeg", ".png": "image/png", ".svg": "image/svg+xml" };
const server = http.createServer((req, res) => {
  const p = path.normalize(path.join(HERE, decodeURIComponent(req.url.split("?")[0])));
  if (!p.startsWith(HERE) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { "content-type": MIME[path.extname(p)] || "application/octet-stream" }); fs.createReadStream(p).pipe(res);
});
await new Promise(r => server.listen(0, "127.0.0.1", r));
const base = `http://127.0.0.1:${server.address().port}`;

let browser, total = 0, duration = 0, rewrites = 0;
const tmp = path.join(outDir, `.frames-${date}-${tagName}`), t0 = Date.now();
try {
  // ---- 3. the page
  browser = await chromium.launch({ args: ["--use-angle=d3d11", "--enable-gpu", "--ignore-gpu-blocklist", "--enable-webgl", "--disable-gpu-vsync", "--force-device-scale-factor=1"] });
  const page = await browser.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 1 });
  page.on("console", m => { if (m.type() === "error") console.log("[page] " + m.text()); });
  page.on("pageerror", e => console.log("[page error] " + e.message));
  await page.goto(base + "/scene.html");
  await page.waitForFunction(() => typeof window.setup === "function");
  const info = await page.evaluate(([b, o]) => window.setup(b, o), [board, { w, h, wide, lowTex: has("lowtex") }]);
  const gpu = await page.evaluate(() => { const g = document.createElement("canvas").getContext("webgl"); const e = g.getExtension("WEBGL_debug_renderer_info"); return e ? g.getParameter(e.UNMASKED_RENDERER_WEBGL) : "?"; });
  console.log(`scene ready: ${info.duration.toFixed(1)} s, ${board.stops.length} stops, texture ${info.texture}, ${w}x${h} @ ${fps} fps, gpu: ${gpu}`);

  const shot = async t => { await page.evaluate(t => { window.draw(t); return new Promise(r => requestAnimationFrame(() => r())); }, t); return page.screenshot({ type: "jpeg", quality: stillsOnly ? 92 : 93 }); };

  // ---- 4. stills (one per stop, at its "hero" moment, plus intro and end card)
  const stills = [["00-intro", 2.2], ...info.stops.map((s, i) => [`${String(i + 1).padStart(2, "0")}-${s.id}`, s.hero]), ["99-end", info.duration - 1.2]];
  for (const f of fs.readdirSync(outDir)) if (f.startsWith(`${date}-${tagName}-still-`)) fs.rmSync(path.join(outDir, f));
  for (const [name, t] of stills) fs.writeFileSync(path.join(outDir, `${date}-${tagName}-still-${name}.jpg`), await shot(t));
  console.log(`stills: ${stills.length} -> out/${date}-${tagName}-still-*.jpg`);

  // ---- 5. frames -> JPEG files (each one read back and compared, because on 11/22 the MSI zeroed stray bytes in
  //         files written during a render)
  if (!stillsOnly) {
    total = Math.round(Math.min(info.duration, Number(opt("seconds", 1e9))) * fps);
    fs.rmSync(tmp, { recursive: true, force: true }); fs.mkdirSync(tmp, { recursive: true });
    for (let i = 0; i < total; i++) {
      const buf = await shot(i / fps), f = path.join(tmp, `f_${String(i).padStart(6, "0")}.jpg`);
      let good = false;
      for (let k = 0; k < 4 && !good; k++) { fs.writeFileSync(f, buf); good = fs.readFileSync(f).equals(buf); if (!good) rewrites++; }
      if (!good) throw new Error("frame " + i + " would not write cleanly to disk");
      if (i % (fps * 10) === 0) console.log(`  frame ${i}/${total}  ${((Date.now() - t0) / 1000).toFixed(0)} s`);
    }
    duration = info.duration;
  }
} finally {
  if (browser) await browser.close();
  await new Promise(r => server.close(r));
}

// ---- 6. encode AFTER the browser is closed (same x264 settings as the news: veryfast, crf 21, yuv420p, faststart),
//         into the system temp folder, then prove the result: (a) every frame decodes, (b) verify_frames.py compares the
//         decoded video with the frames we rendered. A damaged encode is thrown away and done again another way.
if (total) {
  const run = (cmd, a, feeder) => new Promise(res => { let err = "", out = "";
    const p = spawn(cmd, a, { stdio: [feeder ? "pipe" : "ignore", "pipe", "pipe"] }); p.stderr.on("data", d => err += d); p.stdout.on("data", d => out += d);
    if (feeder) { const f = spawn(feeder[0], feeder.slice(1), { stdio: ["ignore", "pipe", "pipe"] }); f.stderr.on("data", d => err += d); f.stdout.pipe(p.stdin); p.stdin.on("error", () => {}); }
    p.on("exit", c => res({ code: c, err: err.trim(), out: out.trim() })); });
  const bed = path.join(HERE, "music", "bed.mp3");   // our own Studio beat (studio-rnb-68), kept low and soft under the type
  const music = opt("music", "") === "none" ? null : opt("music", fs.existsSync(bed) ? bed : null);
  const work = path.join(os.tmpdir(), `map-briefing-${date}-${tagName}-${process.pid}.mp4`);
  const tail = [];
  if (music) tail.push("-stream_loop", "-1", "-i", music, "-af", `lowpass=f=1400,volume=0.20,afade=t=in:d=1.5,afade=t=out:st=${(total / fps - 2.5).toFixed(2)}:d=2.5`, "-c:a", "aac", "-b:a", "160k", "-t", (total / fps).toFixed(3));
  tail.push("-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-pix_fmt", "yuv420p", "-r", String(fps), "-movflags", "+faststart", work);
  const A = ["ffmpeg reads the frames", ["-y", "-loglevel", "error", "-framerate", String(fps), "-i", path.join(tmp, "f_%06d.jpg"), ...tail], null];
  const B = ["raw frames piped in (PIL)", ["-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", `${w}x${h}`, "-framerate", String(fps), "-i", "-", ...tail], ["python", path.join(HERE, "raw_frames.py"), tmp]];
  let ok = false, tries = 0;
  for (const [name, fa, feeder] of [A, B, A, B]) {
    tries++;
    const enc = await run("ffmpeg", fa, feeder);
    const chk = enc.code === 0 && !enc.err ? await run("ffmpeg", ["-v", "error", "-i", work, "-f", "null", "-"]) : { code: 1, err: "" };
    const ver = chk.code === 0 && !chk.err ? await run("python", [path.join(HERE, "verify_frames.py"), tmp, work]) : { code: 1, out: "" };
    let copied = false;
    if (ver.code === 0) for (let k = 0; k < 4 && !copied; k++) { fs.copyFileSync(work, outFile); copied = fs.readFileSync(outFile).equals(fs.readFileSync(work)); }
    ok = copied;
    console.log(`  encode ${tries}, ${name}: ${ok ? ver.out : "THROWN AWAY: " + (enc.err || chk.err || ver.out || ver.err || "copy did not match").split("\n")[0]}`);
    if (ok) break;
  }
  fs.rmSync(work, { force: true });
  if (ok && !has("keep")) fs.rmSync(tmp, { recursive: true, force: true });
  if (!ok) { console.error("FAILED: four encodes, none matched the rendered frames. Frames kept in " + tmp); process.exitCode = 4; }
  else console.log(`done: ${outFile}  (${(total / fps).toFixed(1)} s${total / fps < duration - .1 ? " of " + duration.toFixed(1) : ""}, ${total} frames, ${music ? "music bed: " + path.basename(music) : "no sound"}, frame rewrites: ${rewrites}, encodes needed: ${tries}, ${((Date.now() - t0) / 1000).toFixed(0)} s)`);
}
