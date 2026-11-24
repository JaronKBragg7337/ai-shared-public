// Renders card.html to the share-card files (headless Chromium via tools/site-reel's playwright-core).
//   node render.mjs            -> card-v2-1200x630.png, <email>, card-v2-1200x630.jpg, preview-600.png
import { chromium } from "file:///C:/Users/lilli/AI-Shared/tools/site-reel/node_modules/playwright-core/index.mjs";
import { execFileSync } from "node:child_process";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const dir = path.dirname(fileURLToPath(import.meta.url));
const url = pathToFileURL(path.join(dir, "card.html")).href;
const browser = await chromium.launch({ args: ["--allow-file-access-from-files"] });

async function shot(scale, file) {
  const ctx = await browser.newContext({ viewport: { width: 1200, height: 630 }, deviceScaleFactor: scale });
  const page = await ctx.newPage();
  await page.goto(url);
  await page.evaluate(() => window.__ready);
  await page.waitForTimeout(300);
  await page.screenshot({ path: path.join(dir, file), clip: { x: 0, y: 0, width: 1200, height: 630 } });
  await ctx.close();
}
await shot(1, "card-v2-1200x630.png");
await shot(2, "<email>");
await browser.close();

const magick = "magick";
execFileSync(magick, [path.join(dir, "<email>"), "-filter", "Lanczos", "-resize", "1200x630!", "-quality", "90",
  "-sampling-factor", "4:2:0", "-strip", path.join(dir, "card-v2-1200x630.jpg")]);
execFileSync(magick, [path.join(dir, "<email>"), "-filter", "Lanczos", "-resize", "600x315!", "-strip", path.join(dir, "preview-600.png")]);
console.log("rendered");
