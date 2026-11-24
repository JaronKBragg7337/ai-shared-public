import { chromium } from "playwright-core";
const b = await chromium.launch(); const p = await b.newPage(); await p.goto("http://localhost:8766/studio/index.html");
const r = await p.evaluate(async()=>{
 const tests={
  saw:(c)=>{const o=c.createOscillator();o.type="sawtooth";o.frequency.value=220;o.connect(c.destination);o.start(0.1);},
  sine:(c)=>{const o=c.createOscillator();o.frequency.value=220;o.connect(c.destination);o.start(0.1);},
  noiseBiq:(c)=>{const n=c.createBuffer(1,44100,44100),d=n.getChannelData(0);let a=1;for(let i=0;i<d.length;i++){a=(a*1664525+1013904223)>>>0;d[i]=a/2147483648-1;} const s=c.createBufferSource();s.buffer=n;const f=c.createBiquadFilter();f.frequency.value=3000;s.connect(f);f.connect(c.destination);s.start(0.1);},
  conv:(c)=>{const n=c.createBuffer(1,44100,44100),d=n.getChannelData(0);let a=1;for(let i=0;i<d.length;i++){a=(a*1664525+1013904223)>>>0;d[i]=(a/2147483648-1)*(1-i/d.length);} const ir=c.createBuffer(2,79380,44100);for(let ch=0;ch<2;ch++){const q=ir.getChannelData(ch);for(let i=0;i<q.length;i++){a=(a*1664525+1013904223)>>>0;q[i]=(a/2147483648-1)*(1-i/q.length);}} const s=c.createBufferSource();s.buffer=n;const v=c.createConvolver();v.buffer=ir;s.connect(v);v.connect(c.destination);s.start(0.1);},
  delay:(c)=>{const o=c.createOscillator();o.frequency.value=220;const dl=c.createDelay(2),fb=c.createGain();fb.gain.value=.4;dl.delayTime.value=.3;o.connect(dl);dl.connect(fb);fb.connect(dl);dl.connect(c.destination);o.start(0.1);o.stop(.3)},
  shaper:(c)=>{const o=c.createOscillator();o.frequency.value=220;const w=c.createWaveShaper();const cv=new Float32Array(1024);for(let i=0;i<1024;i++)cv[i]=Math.tanh(2.4*(i/512-1));w.curve=cv;w.oversample="4x";o.connect(w);w.connect(c.destination);o.start(0.1);},
  panner:(c)=>{const o=c.createOscillator();o.frequency.value=220;const pn=c.createStereoPanner();pn.pan.value=.4;o.connect(pn);pn.connect(c.destination);o.start(0.1);},
  gainRamp:(c)=>{const o=c.createOscillator();const g=c.createGain();g.gain.setValueAtTime(.0001,.1);g.gain.exponentialRampToValueAtTime(1,.2);g.gain.exponentialRampToValueAtTime(.0001,.8);o.connect(g);g.connect(c.destination);o.start(0.1);},
 }; const res={};
 for(const [k,f] of Object.entries(tests)){ const run=async()=>{const c=new OfflineAudioContext(2,44100*2,44100);f(c);return (await c.startRendering()).getChannelData(0);}; const a=await run(), z=await run(); let n=0;for(let i=0;i<a.length;i++) if(a[i]!==z[i]) n++; res[k]=n;} return res; });
console.log(r); await b.close();
