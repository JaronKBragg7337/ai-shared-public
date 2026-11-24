// Save the Beat Lab beat a post2 shot list shows (same Math.random seed) as a WAV: node grab-beat.mjs <seed> <out.wav> [text the chords line must contain]
import { chromium } from "playwright-core";
const [seed, out] = process.argv.slice(2);
const b = await chromium.launch(); const p = await (await b.newContext({ acceptDownloads: true, viewport: { width: 390, height: 844 } })).newPage();
await p.goto("https://www.heartbeatobservatory.com/studio/", { waitUntil: "load" });
await p.click("#labOpen"); await p.waitForSelector("#blNew");
const want = process.argv[4] || "";
for (let skip = 0; skip < 400; skip++) {
await p.evaluate(([s, k]) => { let a = s; Math.random = () => { a |= 0; a = (a + 0x6d2b79f5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; ; for (let i = 0; i < k; i++) Math.random(); document.querySelector("#blNew").click(); }, [+seed, skip]);
if (!want || (await p.locator("#blParts").innerText()).includes(want)) { console.log("skip", skip); break; } }
console.log(await p.locator("#blMsg").innerText().catch(() => ""), "|", (await p.locator("#blParts").innerText()).match(/E\w? .*minor\)|[A-G].{0,40}\(i.*?\)/)?.[0]);
const [d] = await Promise.all([p.waitForEvent("download", { timeout: 120000 }), p.click("#blSave")]);
await d.saveAs(out); console.log("saved", out); await b.close();
