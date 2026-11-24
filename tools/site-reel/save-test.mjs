import { chromium } from "playwright-core"; import fs from "fs";
const exe = process.env.CHROME || undefined;
const b = await chromium.launch({ channel: undefined, args:["--autoplay-policy=no-user-gesture-required"] }).catch(async()=>chromium.launch({channel:"chrome"}));
const ctx = await b.newContext({ viewport:{width:390,height:844}, acceptDownloads:true });
const p = await ctx.newPage(); const errs=[]; p.on("pageerror",e=>errs.push(String(e))); p.on("console",m=>{if(m.type()==="error")errs.push(m.text())});
await p.goto("http://localhost:8765/studio/index.html"); await p.click("#labOpen"); await p.click("#blNew"); await p.waitForTimeout(500);
await p.click("#blSave"); await p.waitForSelector(".svx");
console.log("menu:", (await p.innerText(".svx")).split("\n").slice(0,12).join(" | "));
const out="C:/Users/lilli/AppData/Local/Temp/svtest/"; fs.mkdirSync(out,{recursive:true});
await p.screenshot({path:out+"menu.png"});
async function get(label, wait=60000){ await p.click(`.svx button:has-text("${label}")`); await p.waitForSelector(".svx-file a",{timeout:wait}); const [d]=await Promise.all([p.waitForEvent("download"),p.click(".svx-file a")]); const f=out+d.suggestedFilename(); await d.saveAs(f); console.log(label, f, fs.statSync(f).size); await p.screenshot({path:out+label.replace(/\W/g,"")+".png"}); await p.click('.svx button:has-text("Back")'); return f; }
await get("WAV (big"); await get("MP3 (best");
await p.click('.svx button:has-text("Save as video")'); await p.click('.svx button:has-text("30 second")');
await get2();
async function get2(){ await p.waitForSelector(".svx-file a",{timeout:90000}); const [d]=await Promise.all([p.waitForEvent("download"),p.click(".svx-file a")]); const f=out+d.suggestedFilename(); await d.saveAs(f); console.log("video",f,fs.statSync(f).size); await p.click('.svx button:has-text("Back")'); }
await p.click('.svx button:has-text("Save the parts")'); await p.waitForSelector(".svx-file a",{timeout:90000}); console.log("parts files:", await p.locator(".svx-file").count());
console.log("overflowX:", await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth));
console.log("sheetOverflow:", await p.evaluate(()=>{const s=document.querySelector(".svx");return s.scrollWidth>s.clientWidth}));
console.log("errors:", errs); await b.close();
