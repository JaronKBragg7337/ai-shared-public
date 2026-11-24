import { chromium } from "playwright-core";
const b = await chromium.launch(); const p = await b.newPage(); await p.goto("http://localhost:8766/studio/index.html");
const r = await p.evaluate(async()=>{ const m=await import("/studio/beatlab.js"); const o={style:"trap",mood:"dark",key:6,bpm:140,swing:.5,energy:.6,kit:"hard",bassSound:"808",keysSound:"pad",leadSound:"bell",verseMelody:true,len:0.5,seeds:{drums:1,bass:2,chords:3,melody:4},drums:null,melody:null,vol:{drums:1,bass:.5,keys:1.7,melody:1.8},mute:{}};
 const song=m.compose(o); const a=await m.render(o,song), c=await m.render(o,m.compose(o)); let first=-1,cnt=0,mx=0; const A=a.getChannelData(0),C=c.getChannelData(0); for(let i=0;i<A.length;i++){const d=Math.abs(A[i]-C[i]); if(d>0){cnt++; mx=Math.max(mx,d); if(first<0)first=i;}} 
 const parts={}; for (const pt of ["drums","bass","keys","melody"]){ const x=await m.render(o,song,pt), y=await m.render(o,song,pt); let n=0,q=0; const X=x.getChannelData(0),Y=y.getChannelData(0); for(let i=0;i<X.length;i++){ if(X[i]!==Y[i]){n++;}} parts[pt]=n;} return {first,cnt,mx,len:A.length,parts}; });
console.log(r); await b.close();
