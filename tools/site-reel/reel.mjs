// site-reel: records heartbeatobservatory.com the way a phone user would see it, from a shot list.
// Frame-stepped: the page clock is frozen and advanced one frame at a time, so a slow or busy MSI
// makes the recording take longer, never makes the video stutter. Headless: nothing on the MSI
// screen (pop-ups, terminals) can ever end up in the video.
//
//   node reel.mjs shots/post1.json            -> out/post1.mp4
//   node reel.mjs shots/post1.json --fps 15   (quick draft)
//
// Shot list: { base, fps, hide:[css], shots:[ {goto}, {hold}, {scroll}, {tap}, {card} ] } - see README.md.
import { webkit, chromium } from "playwright-core";
import { execFileSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";

const args = process.argv.slice(2);
const listPath = args.find(a => !a.startsWith("--"));
const opt = (k, d) => { const i = args.indexOf("--" + k); return i >= 0 ? args[i + 1] : d; };
if (!listPath) { console.error("usage: node reel.mjs <shots.json> [--out file.mp4] [--fps 30] [--engine webkit|chromium]"); process.exit(1); }

const list = JSON.parse(fs.readFileSync(listPath, "utf8"));
const fps = Number(opt("fps", list.fps || 30));
const frameMs = 1000 / fps;
const out = opt("out", path.join("out", path.basename(listPath, ".json") + ".mp4"));
const frames = path.join("out", "frames-" + path.basename(listPath, ".json"));
fs.rmSync(frames, { recursive: true, force: true });
fs.mkdirSync(frames, { recursive: true });

// 414x736 is 9:16 (iPhone Plus size); x3 = 1242x2208, scaled to 1080x1920 at the end.
const engine = opt("engine", list.engine || "webkit") === "chromium" ? chromium : webkit;
const browser = await engine.launch();
const ctx = await browser.newContext({
  viewport: { width: 414, height: 736 }, deviceScaleFactor: 3, isMobile: engine === chromium, hasTouch: true,
  userAgent: "Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1",
});
const page = await ctx.newPage();
await page.clock.install();

let n = 0;
async function frame() {
  await page.clock.runFor(frameMs);
  await page.screenshot({ path: path.join(frames, String(n++).padStart(5, "0") + ".jpg"), type: "jpeg", quality: 92 });
}
const ease = t => t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
const count = s => Math.max(1, Math.round(s * fps));

async function hideChrome() {
  const css = (list.hide || []).map(s => `${s}{display:none!important}`).join("") + "html{scroll-behavior:auto!important}";
  for (const f of page.frames()) await f.addStyleTag({ content: css }).catch(() => {});   // embedded players too
}
async function settle(ms = 1500) {
  await page.waitForLoadState("networkidle", { timeout: 15000 }).catch(() => {});
  await page.clock.runFor(ms);                       // let page timers/animations reach their resting state
  await page.evaluate(() => document.fonts && document.fonts.ready).catch(() => {});
}
async function scrollTarget(to) {
  if (typeof to === "number") return to;
  return page.evaluate(sel => { const el = document.querySelector(sel); return el ? el.getBoundingClientRect().top + scrollY - 80 : scrollY; }, to);
}

const t0 = Date.now();
for (const s of list.shots) {
  if (s.goto) {
    await page.goto(new URL(s.goto, list.base).href, { waitUntil: "load", timeout: 45000 });
    await hideChrome(); await settle(s.settle); await hideChrome();   // again: embedded players load late
    if (s.hold) for (let i = 0; i < count(s.hold); i++) await frame();
  } else if (s.scroll !== undefined) {
    const from = await page.evaluate(() => scrollY), to = await scrollTarget(s.scroll), k = count(s.dur || 2);
    for (let i = 1; i <= k; i++) { await page.evaluate(y => scrollTo(0, y), from + (to - from) * ease(i / k)); await frame(); }
  } else if (s.tap) {
    // A soft finger dot grows on the target, then the real tap happens.
    const box = await page.locator(s.tap).first().boundingBox();
    if (!box) { console.warn("tap target not found:", s.tap); continue; }
    const x = box.x + box.width / 2, y = box.y + box.height / 2;
    await page.evaluate(([x, y]) => { const d = document.createElement("div"); d.id = "reel-tap";
      d.style.cssText = `position:fixed;left:${x - 22}px;top:${y - 22}px;width:44px;height:44px;border-radius:50%;background:rgba(255,255,255,.55);box-shadow:0 0 0 2px rgba(0,0,0,.25);z-index:2147483647;pointer-events:none;transform:scale(.4);opacity:0`;
      document.body.appendChild(d); }, [x, y]);
    const k = count(0.45);
    for (let i = 1; i <= k; i++) { await page.evaluate(t => { const d = document.getElementById("reel-tap"); d.style.opacity = String(Math.min(1, t * 2)); d.style.transform = `scale(${0.4 + 0.6 * t})`; }, i / k); await frame(); }
    await page.evaluate(() => document.getElementById("reel-tap")?.remove());
    await page.mouse.click(x, y);
    await hideChrome(); await settle(s.settle); await hideChrome();   // again: embedded players load late
    if (s.hold) for (let i = 0; i < count(s.hold); i++) await frame();
  } else if (s.card) {
    // Text card in the site's warm palette; fades in over the first 0.4 s.
    // about:blank first: setContent keeps the old window, and its leftover timers would fire on the card.
    await page.goto("about:blank");
    await page.setContent(`<html><head><meta name=viewport content="width=device-width">
      <link rel=stylesheet href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600&family=Atkinson+Hyperlegible:wght@400;700&display=swap">
      <style>html,body{margin:0;height:100%;background:${s.bg || "#1d1916"};color:${s.fg || "#efe6da"}}
      .c{height:100%;display:grid;place-content:center;gap:18px;padding:0 34px;text-align:center;opacity:0}
      h1{font:600 ${s.card.split(" ").some(w => w.length > 16) ? 26 : 34}px/1.15 Fraunces,Georgia,serif;margin:0;text-wrap:balance;overflow-wrap:anywhere}
      p{font:400 18px/1.45 "Atkinson Hyperlegible",system-ui,sans-serif;margin:0;color:${s.sub_fg || "#a89a8b"}}</style></head>
      <body><div class=c id=c><h1>${s.card}</h1>${s.sub ? `<p>${s.sub}</p>` : ""}</div></body></html>`, { waitUntil: "networkidle" });
    await page.evaluate(() => document.fonts.ready);
    const k = count(s.dur || 2.5), fade = count(0.4);
    for (let i = 1; i <= k; i++) { await page.evaluate(o => document.getElementById("c").style.opacity = String(o), Math.min(1, i / fade)); await frame(); }
  } else if (s.eval) {                                // run page JS (e.g. seed Math.random so a demo is repeatable)
    await page.evaluate(s.eval);
    if (s.settle) await settle(s.settle);
    if (s.hold) for (let i = 0; i < count(s.hold); i++) await frame();
  } else if (s.hold) {                                // plain hold last: tap/goto shots carry their own hold
    for (let i = 0; i < count(s.hold); i++) await frame();
  }
}
await browser.close();

fs.mkdirSync(path.dirname(out), { recursive: true });
execFileSync("ffmpeg", ["-y", "-loglevel", "error", "-framerate", String(fps), "-i", path.join(frames, "%05d.jpg"),
  "-vf", "scale=1080:1920:flags=lanczos", "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out]);
console.log(`${out}: ${n} frames, ${(n / fps).toFixed(1)} s of video, made in ${((Date.now() - t0) / 1000).toFixed(0)} s`);
