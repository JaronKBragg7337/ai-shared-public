import { chromium } from "playwright-core";
const b = await chromium.launch(); const p = await b.newPage(); await p.goto("http://localhost:8766/studio/index.html");
const r = await p.evaluate(async()=>{ const m=await import("/studio/_dbg.js"); const o={style:"trap",mood:"dark",key:6,bpm:140,swing:.5,energy:.6,kit:"hard",bassSound:"808",keysSound:"pad",leadSound:"bell",verseMelody:true,len:0.5,seeds:{drums:1,bass:2,chords:3,melody:4},drums:null,melody:null,vol:{drums:1,bass:.5,keys:1.7,melody:1.8},mute:{}};
 const song=m.compose(o); const p1=JSON.stringify(m.plan(o,song)), p2=JSON.stringify(m.plan(o,song)); 
 const bars=m.plan(o,song), barS=4*60/o.bpm; const res=[];
 for (let k=0;k*4<bars.length;k++){ const piece=bars.slice(k*4,k*4+4); const run=async()=>{ const c=new OfflineAudioContext(2,Math.ceil((piece.length*barS+2.5)*44100),44100); const G=m.graph(c,o,"drums"); for(const bd of piece) m.schedBar(o,song,G,bd,(bd.bar-piece[0].bar)*barS); return (await c.startRendering()).getChannelData(0);}; const a=await run(),z=await run(); let n=0,mx=0,f=-1; for(let i=0;i<a.length;i++) if(a[i]!==z[i]){n++;mx=Math.max(mx,Math.abs(a[i]-z[i])); if(f<0)f=i;} res.push([n,mx,f]);} 
 return {planSame:p1===p2,res}; }); console.log(r); await b.close();
