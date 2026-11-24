import { chromium } from "playwright-core"; import fs from "fs"; import crypto from "crypto";
const out = "C:/Users/lilli/AppData/Local/Temp/mbtest/"; fs.rmSync(out,{recursive:true,force:true}); fs.mkdirSync(out,{recursive:true});
const b = await chromium.launch({ args:["--autoplay-policy=no-user-gesture-required"] }).catch(()=>chromium.launch({channel:"chrome"}));
const ctx = await b.newContext({ viewport:{width:390,height:844}, acceptDownloads:true });
const p = await ctx.newPage(); const errs=[]; p.on("pageerror",e=>errs.push(String(e))); p.on("console",m=>{if(m.type()==="error")errs.push(m.text())});
const URL="http://localhost:8766/studio/index.html";
await p.goto(URL); await p.click("#labOpen");
for (let i=0;i<3;i++){ await p.click("#blNew"); await p.waitForTimeout(600); }
await p.waitForTimeout(500);
console.log("entries after 3 rolls:", await p.locator(".blEntry").count());
// keep the 2nd newest (entry index 1)
await p.locator(".blEntry").nth(1).locator('button:has-text("Keep")').click();
const keptName = await p.locator(".blEntry").first().innerText(); console.log("first entry now:", keptName.replace(/\n/g," | "));
const stored = await p.evaluate(()=>JSON.parse(localStorage.getItem("hb-studio-beats-v1")));
const kept = stored.find(e=>e.kept); console.log("stored", stored.length, "kept", !!kept, kept.r.style, kept.r.bpm);
// determinism: render the recipe twice in page
const cmp = (r)=>p.evaluate(async (r)=>{ const m=await import("/studio/beatlab.js"); const mk=async()=>{const o=JSON.parse(JSON.stringify(r)); delete o.v; const song=m.compose(o); if(o.drums) song.drums=o.drums; return {notes:JSON.stringify([song.chords,song.drums,song.motif,song.arr]), buf:await m.render(o,song)};}; const A=await mk(), B=await mk(); let mx=0,se=0,sp=0; const x=A.buf.getChannelData(0), y=B.buf.getChannelData(0); for(let i=0;i<x.length;i++){const d=x[i]-y[i]; mx=Math.max(mx,Math.abs(d)); se+=d*d; sp+=x[i]*x[i];} return {notesSame:A.notes===B.notes, maxDiff:mx, snrDb:10*Math.log10(sp/Math.max(se,1e-30))}; }, r);
console.log("render twice:", await cmp(kept.r));
async function saveWav(tag, label="WAV (big"){ await p.click("#blSave"); await p.waitForSelector(".svx"); await p.click(`.svx button:has-text("${label}")`); await p.waitForSelector(".svx-file a",{timeout:90000}); const [d]=await Promise.all([p.waitForEvent("download"),p.click(".svx-file a")]); const f=out+tag+"-"+d.suggestedFilename(); await d.saveAs(f); await p.click('.svx .svx-close:has-text("Done")'); return f; }
// open kept via UI, save
await p.locator(".blEntry").filter({hasText:"Kept"}).first(); 
await p.locator(".blEntry button", {hasText:/BPM/}).nth(0).waitFor();
const keptIdx = stored.findIndex(e=>e.kept); // list shows kept group first
await p.locator(".blEntry").first().locator("button").first().click(); await p.waitForTimeout(300);
const fA = await saveWav("A");
await p.reload(); await p.click("#labOpen"); await p.waitForTimeout(300);
console.log("after reload entries:", await p.locator(".blEntry").count(), "kept shown first:", (await p.locator(".blEntry").first().innerText()).replace(/\n/g," | "));
await p.locator(".blEntry").first().locator("button").first().click(); await p.waitForTimeout(300);
const fB = await saveWav("B");
const md=(f)=>crypto.createHash("md5").update(fs.readFileSync(f)).digest("hex"); { const ra=fs.readFileSync(fA), rb=fs.readFileSync(fB); const ia=new Int16Array(ra.buffer.slice(ra.byteOffset+44,ra.byteOffset+44+(ra.length-44-2000)&~1)), ib=new Int16Array(rb.buffer.slice(rb.byteOffset+44,rb.byteOffset+44+(rb.length-44-2000)&~1)); let mx=0,se=0,sp=0; for(let i=0;i<Math.min(ia.length,ib.length);i++){const d=ia[i]-ib[i]; mx=Math.max(mx,Math.abs(d)); se+=d*d; sp+=ia[i]*ia[i];} console.log("WAV A vs B after reload: sameSize", ra.length===rb.length, "maxDiff(LSB)", mx, "SNR dB", (10*Math.log10(sp/Math.max(se,1e-9))).toFixed(1), "md5same", md(fA)===md(fB)); }
const fM = await saveWav("M","MP3 (best");
console.log("files", fA, fM);
// re-import into Lab via "Open a saved beat file"
await p.evaluate(()=>localStorage.removeItem("hb-studio-beats-v1")); await p.reload(); await p.click("#labOpen");
await p.setInputFiles("#blOpenFile", fB); await p.waitForTimeout(800); console.log("lab open wav msg:", await p.innerText("#blOpenMsg")); console.log("entries:", await p.locator(".blEntry").count());
await p.setInputFiles("#blOpenFile", fM); await p.waitForTimeout(800); console.log("lab open mp3 msg:", await p.innerText("#blOpenMsg"));
// plain file (no recipe)
fs.writeFileSync(out+"plain.wav", fs.readFileSync("C:/Users/lilli/AppData/Local/Temp/svtest/Trap-Gm-148.wav"));
await p.setInputFiles("#blOpenFile", out+"plain.wav"); await p.waitForTimeout(800); console.log("plain msg:", await p.innerText("#blOpenMsg"));
// index upload path
await p.reload(); await p.setInputFiles("#beatFile", fM); await p.waitForSelector("#recipeOffer:not(.hide)",{timeout:20000}); console.log("offer shown for mp3");
await p.click("#recipeOpen"); await p.waitForTimeout(600); console.log("lab opened, entries:", await p.locator(".blEntry").count());
await p.screenshot({path:out+"mine.png"});
// delete two-tap
const n0=await p.locator(".blEntry").count(); const del=p.locator(".blEntry").first().locator('button:has-text("Delete")'); await del.click(); console.log("confirm text:", await p.locator(".blEntry").first().innerText().then(t=>t.includes("Tap again"))); await p.locator(".blEntry").first().locator('button:has-text("Tap again")').click(); console.log("deleted:", n0, "->", await p.locator(".blEntry").count());
console.log("overflowX:", await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth));
console.log("errors:", errs); await b.close();
