import { chromium } from "playwright-core";
const b = await chromium.launch(); const p = await b.newPage(); await p.goto("http://localhost:8766/studio/index.html");
const r = await p.evaluate(async()=>{ const m=await import("/studio/_dbg.js"); const o={style:"trap",mood:"dark",key:6,bpm:140,swing:.5,energy:.6,kit:"hard",bassSound:"808",keysSound:"pad",leadSound:"bell",verseMelody:true,len:0.5,seeds:{drums:1,bass:2,chords:3,melody:4},drums:null,melody:null,vol:{drums:1,bass:.5,keys:1.7,melody:1.8},mute:{}};
 const song=m.compose(o), bars=m.plan(o,song), barS=4*60/o.bpm, out={};
 const run=async(only,verbOff)=>{ const c=new OfflineAudioContext(2,Math.ceil((4*barS+2.5)*44100),44100); const G=m.graph(c,o,only); for(const bd of bars.slice(0,4)) m.schedBar(o,song,G,bd,(bd.bar-bars[0].bar)*barS); return (await c.startRendering()).getChannelData(0); };
 for (const only of ["drums","bass","keys","melody"]){ const a=await run(only), z=await run(only); let n=0,mx=0; for(let i=0;i<a.length;i++){ if(a[i]!==z[i]){n++; mx=Math.max(mx,Math.abs(a[i]-z[i]));}} out[only]=[n,mx]; }
 return out; }); console.log(r); await b.close();
